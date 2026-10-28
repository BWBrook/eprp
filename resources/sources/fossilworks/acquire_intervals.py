#!/usr/bin/env python3
"""Acquire separate public fossil-interval exports without assembling them."""

import argparse
import collections
import csv
import datetime as dt
import hashlib
import html.parser
import io
import json
from pathlib import Path
import re
import time
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://fossilworks.org/"
TABLES = ("register", "species", "samples", "references", "matrix")


def now():
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


class Form(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.active = False
        self.intervals = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "form":
            self.active = attrs.get("name") == "size_form"
        if self.active and tag == "input" and attrs.get("type") == "checkbox":
            if attrs.get("value") == "yes":
                self.intervals.append(attrs["name"])

    def handle_endtag(self, tag):
        if tag == "form":
            self.active = False


def fetch(url, path, payload=None):
    started = now()
    encoded = urllib.parse.urlencode(payload).encode() if payload is not None else None
    request = urllib.request.Request(url, encoded, headers={"User-Agent": "EPRP-public-source-mirror/1.0", "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = response.read()
            meta = {"status": response.status, "response_url": response.url, "headers": dict(response.headers)}
    except urllib.error.HTTPError as error:
        data = error.read()
        meta = {"status": error.code, "response_url": error.url, "headers": dict(error.headers)}
    path.write_bytes(data)
    return dict(meta, url=url, method="POST" if payload is not None else "GET", request_parameters=payload,
                started_utc=started, finished_utc=now(), key=str(path.name), size=len(data), sha256=sha(data),
                checksum="none supplied by provider")


def parse_table(path):
    data = path.read_bytes().decode("utf-8-sig")
    rows = list(csv.reader(io.StringIO(data, newline=""), delimiter="\t", quoting=csv.QUOTE_NONE))
    if not rows or "<html" in data[:500].lower():
        raise ValueError(f"{path.name}: no TSV header")
    return rows[0], rows[1:]


def validate(directory, interval, expected, output_directory=None):
    parsed = {name: parse_table(directory / (name + ".txt")) for name in TABLES}
    tables = {name: [dict(zip(header, row)) for row in rows] for name, (header, rows) in parsed.items() if name != "matrix"}
    counts = {name: len(rows) for name, (_, rows) in parsed.items()}
    checks = {"result_page_counts": all(counts[name] == expected[name] for name in expected),
              "rectangular_tables": all(all(len(row) == len(header) for row in rows) for header, rows in parsed.values())}
    register, species, samples, references = (tables[name] for name in TABLES[:4])
    register_ids = {r["sample no"] for r in register}
    sample_ids = {r["sample no"] for r in samples}
    checks["register_sample_id_sets"] = register_ids == sample_ids
    checks["register_reference_id_sets"] = {r["ref no"] for r in register} == {r["ref_no"] for r in references}
    checks["sample_reference_id_sets"] = {r["ref no"] for r in samples} == {r["ref_no"] for r in references}
    intervals = dict(collections.Counter(r["time interval"] for r in register))
    checks["selected_interval_labels"] = set(intervals) <= {interval}
    matrix_header, matrix_rows = parsed["matrix"]
    matrix_names = matrix_header[1:]
    sample_names = [r["sample name"] for r in samples]
    checks["matrix_sample_names_known"] = set(matrix_names) <= set(sample_names)
    checks["matrix_species_set"] = {r[0] for r in matrix_rows} == {r["species"] for r in species}
    names_to_ids = collections.defaultdict(set)
    for row in samples:
        names_to_ids[row["sample name"]].add(row["sample no"])
    duplicate_names = sum(len(ids) > 1 for ids in names_to_ids.values())
    summed = collections.Counter()
    last = {}
    for row in register:
        key = (row["genus"] + " " + row["species"], row["sample name"])
        count = float(row["count"])
        summed[key] += count
        last[key] = count
    sum_differences = 0
    last_differences = 0
    differences = []
    if not duplicate_names:
        for row in matrix_rows:
            for name, value in zip(matrix_names, row[1:]):
                key = (row[0], name)
                count = float(value or 0)
                sum_differences += count != summed[key]
                last_differences += count != last.get(key, 0)
                if count != summed[key] or count != last.get(key, 0):
                    differences.append({"species": row[0], "sample_name": name, "matrix_count": count,
                                        "summed_register_count": summed[key], "last_register_count": last.get(key, 0)})
    save((output_directory or directory) / "matrix-comparison.json", {"duplicate_sample_names": duplicate_names, "differing_cells": differences,
         "interpretation": "Observed comparisons only; agreement with last-row values does not establish provider implementation."})
    return {"passed": all(checks.values()), "checks": checks, "rows": counts,
            "distinct_sample_ids": len(sample_ids), "interval_labels": intervals,
            "repeated_sample_summary_rows": len(samples) - len(sample_ids),
            "matrix_sample_columns": len(matrix_names),
            "sample_names_absent_from_matrix": sorted(set(sample_names) - set(matrix_names)),
            "duplicate_sample_names": duplicate_names,
            "matrix_columns_in_sample_table_order": matrix_names == sample_names,
            "matrix_cells_differing_from_summed_register": None if duplicate_names else sum_differences,
            "matrix_cells_differing_from_last_register_row": None if duplicate_names else last_differences,
            "matrix_limitation": "Provider matrix excludes non-species names; observed matrix cells can differ from summed repeated species/sample rows and agree with last-row values. Duplicate sample names make identity matching ambiguous. Original files retained."}


def expected_counts(text):
    match = re.search(r"(\d+)\s*<a[^>]*>register records</a> including (\d+)\s*<a[^>]*>named species</a> from (\d+)\s*<a[^>]*>samples</a> tied to (\d+)\s*<a[^>]*>references</a>", text)
    return dict(zip(TABLES[:4], map(int, match.groups()))) if match else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dest", type=Path)
    parser.add_argument("--resume", action="store_true", help="Post-audit retained bundles and skip accepted downloads")
    args = parser.parse_args()
    root = args.dest
    root.mkdir(parents=True, exist_ok=args.resume)
    if (root / "MANIFEST.json").exists():
        raise RuntimeError("A finalized snapshot is immutable; choose a new destination")
    tool_sha = sha(Path(__file__).read_bytes())
    (root / (f"acquisition-resume-{tool_sha[:12]}.py" if args.resume else "acquisition-tool.py")).write_bytes(Path(__file__).read_bytes())
    files = []
    if not args.resume:
        form_meta = fetch(BASE + "?a=downloadForm", root / "download-form.html")
        save(root / "download-form-receipt.json", form_meta)
        files.append(form_meta)
    form = Form()
    form.feed((root / "download-form.html").read_text())
    if len(form.intervals) != 20:
        raise RuntimeError(f"Expected 20 visible interval inputs; found {form.intervals}")
    save(root / "intervals.json", form.intervals)
    outcomes = []
    for number, interval in enumerate(form.intervals, 1):
        slug = re.sub(r"[^a-z0-9]+", "-", interval.lower()).strip("-")
        directory = root / f"{number:02d}-{slug}"
        directory.mkdir(exist_ok=args.resume)
        outcome = {"interval": interval, "directory": directory.name, "attempts": []}
        existing = sorted(directory.glob("attempt-*"))
        for work in existing:
            if not (work / "receipts.json").exists() or not (work / "assessment.json").exists():
                continue
            receipts = json.loads((work / "receipts.json").read_text())
            for receipt in receipts:
                files.append(dict(receipt, key=str((work / receipt["key"]).relative_to(root))))
            original = json.loads((work / "assessment.json").read_text())
            corrected = dict(original)
            if original.get("expected_rows") is not None and all((work / (name + ".txt")).exists() for name in TABLES):
                audit_dir = work / "post-acquisition-audit"
                audit_dir.mkdir(exist_ok=True)
                corrected["validation"] = validate(work, interval, original["expected_rows"], audit_dir)
                corrected["post_audited_utc"] = now()
                corrected["audit_tool_sha256"] = tool_sha
                corrected["state"] = ("coherent_export" if corrected["validation"]["passed"] else "downloaded_source_inconsistency") if all(original.get("stable_second_get", {}).get(name, False) for name in TABLES) else "unresolved"
                save(audit_dir / f"reassessment-{tool_sha[:12]}.json", corrected)
            outcome["attempts"].append(corrected)
            if corrected["state"] in {"coherent_export", "downloaded_source_inconsistency"} and "accepted_attempt" not in outcome:
                outcome.update(state=corrected["state"], accepted_attempt=int(work.name.split("-")[-1]))
        if outcome.get("state") in {"coherent_export", "downloaded_source_inconsistency"}:
            outcomes.append(outcome)
            save(root / "progress.json", outcomes)
            print(f"{now()} {number}/20 {interval}: accepted retained attempt {outcome['accepted_attempt']}", flush=True)
            continue
        print(f"{now()} {number}/20 {interval}", flush=True)
        first_attempt = max((int(p.name.split("-")[-1]) for p in existing), default=0) + 1
        for attempt in range(first_attempt, first_attempt + 2):
            work = directory / f"attempt-{attempt}"
            work.mkdir()
            query = {"a": "downloadResults", "pot": "", interval: "yes"}
            save(work / "request.json", {"url": BASE, "method": "POST", "parameters": query,
                 "body": urllib.parse.urlencode(query), "scope": "One visible fossil interval; all geographic and taxonomic inputs omitted/unrestricted"})
            receipts = []
            record = {"attempt": attempt, "started_utc": now(), "tool_sha256": tool_sha}
            try:
                result_meta = fetch(BASE, work / "results.html", query)
                receipts.append(result_meta)
                result_text = (work / "results.html").read_text(errors="replace")
                expected = expected_counts(result_text)
                record["expected_rows"] = expected
                if result_meta["status"] != 200 or expected is None:
                    record["state"] = "no_linked_export_or_http_failure"
                    record["result_status"] = result_meta["status"]
                else:
                    for name in TABLES:
                        path = f"/eco/downloads/{name}.txt"
                        if path not in result_text:
                            raise ValueError(f"Results page missing {path}")
                        url = BASE.rstrip("/") + path + "?" + urllib.parse.urlencode({"eprp_interval": slug, "eprp_attempt": attempt})
                        receipts.append(fetch(url, work / (name + ".txt")))
                    record["validation"] = validate(work, interval, expected)
                    time.sleep(2)
                    stability = {}
                    for name in TABLES:
                        original = next(r for r in receipts if r["key"] == name + ".txt")
                        url = BASE + "eco/downloads/" + name + ".txt?" + urllib.parse.urlencode({"eprp_verify": slug, "attempt": attempt})
                        verification = fetch(url, work / (name + ".verify.txt"))
                        receipts.append(verification)
                        stability[name] = original["sha256"] == verification["sha256"]
                    record["stable_second_get"] = stability
                    record["state"] = ("coherent_export" if record["validation"]["passed"] else "downloaded_source_inconsistency") if all(stability.values()) else "unstable_export"
            except Exception as error:
                record.update(state="request_or_validation_error", error=repr(error))
            record["finished_utc"] = now()
            save(work / "receipts.json", receipts)
            save(work / "assessment.json", record)
            for receipt in receipts:
                files.append(dict(receipt, key=str((work / receipt["key"]).relative_to(root))))
            outcome["attempts"].append(record)
            print(json.dumps({"interval": interval, "attempt": attempt, "state": record["state"], "rows": record.get("validation", {}).get("rows")}), flush=True)
            if record["state"] in {"coherent_export", "downloaded_source_inconsistency"}:
                outcome.update(state=record["state"], accepted_attempt=attempt)
                break
            if attempt == first_attempt:
                time.sleep(15)
        outcome.setdefault("state", "unresolved")
        outcomes.append(outcome)
        save(root / "progress.json", outcomes)
        time.sleep(2)
    known = {f["key"] for f in files}
    for path in sorted(root.rglob("*")):
        if path.is_file() and str(path.relative_to(root)) not in known:
            data = path.read_bytes()
            files.append({"key": str(path.relative_to(root)), "size": len(data), "sha256": sha(data),
                          "checksum": "local acquisition metadata"})
    manifest = {"provider": "Fossilworks public download form", "record": BASE + "?a=downloadForm",
                "version": root.name, "license": "CC0 for data per current Fossilworks FAQ",
                "retrieved_utc": now(), "tool": {"name": Path(__file__).name, "sha256": tool_sha},
                "files": files, "intervals": outcomes,
                "complete_visible_intervals": all(o["state"] in {"coherent_export", "downloaded_source_inconsistency"} for o in outcomes),
                "fully_coherent_visible_intervals": all(o["state"] == "coherent_export" for o in outcomes),
                "limitations": ["Generic provider files are mutable and publicly accessible without a session; coherence and repeated hashes reduce but do not eliminate concurrent-writer risk.", "Each interval retained separately; intervals may overlap. No deduplication or assembly performed.", "Observed provider matrix cells can differ from summed repeated taxon/sample counts; retain register as original count evidence."]}
    save(root / "MANIFEST.json", manifest)
    for path in root.rglob("*"):
        if path.is_file():
            path.chmod(0o444)
    for path in sorted(root.rglob("*"), reverse=True):
        if path.is_dir():
            path.chmod(0o555)
    root.chmod(0o555)
    print(f"COMPLETE {sum(o['state'] in {'coherent_export', 'downloaded_source_inconsistency'} for o in outcomes)}/20 acquired intervals: {root}", flush=True)


if __name__ == "__main__":
    main()
