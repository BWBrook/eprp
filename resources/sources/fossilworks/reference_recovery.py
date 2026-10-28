#!/usr/bin/env python3
"""Recover missing reference metadata into a separate, evidence-backed overlay.

extract-input DATABASE INPUT.json; collect INPUT.json NEW_EVIDENCE_DIR;
build INPUT.json EVIDENCE_DIR NEW_OVERLAY.json. No command modifies DATABASE.
"""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sqlite3
import time
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen

DATABASE_SHA256 = "ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610"
BASE = "https://fossilworks.org/"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, value):
    with Path(path).open("x", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def extract_input(database):
    database = Path(database).resolve()
    digest = sha256(database.read_bytes())
    if digest != DATABASE_SHA256:
        raise ValueError("Not the pinned 2026-10-28 assembly")
    connection = sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)
    try:
        rows = connection.execute('''SELECT "ref no", _fw_row_id, "sample no"
            FROM register_linked WHERE _fw_reference_status='unresolved'
            ORDER BY CAST("ref no" AS INTEGER), _fw_row_id''').fetchall()
    finally:
        connection.close()
    grouped = {}
    for ref_no, row_id, sample_no in rows:
        group = grouped.setdefault(ref_no, {"ref_no": ref_no, "row_ids": [], "sample_ids": set()})
        group["row_ids"].append(row_id)
        group["sample_ids"].add(sample_no)
    for group in grouped.values():
        group["sample_ids"] = sorted(group["sample_ids"], key=int)
        group["register_rows"] = len(group["row_ids"])
    if len(grouped) != 58 or len(rows) != 1266:
        raise ValueError("Missing-reference cohort differs from the pinned assembly")
    return {"database_sha256": digest, "missing_references": list(grouped.values())}


class ReferencePage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.divs, self.sample_ids = [], [], set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "div":
            if self.stack:
                self.stack[-1]["children"] += 1
            self.stack.append({"text": [], "children": 0})
        if tag == "a":
            query = parse_qs(urlparse(attrs.get("href", "")).query)
            if query.get("a") == ["sampleResults"]:
                for value in query.get("sample_no", []):
                    if re.fullmatch(r"[0-9]+", value):
                        self.sample_ids.add(value)

    def handle_endtag(self, tag):
        if tag == "div" and self.stack:
            div = self.stack.pop()
            div["text"] = re.sub(r"\s+", " ", "".join(div["text"])).strip()
            self.divs.append(div)

    def handle_data(self, data):
        for div in self.stack:
            div["text"].append(data)


def parse_reference(data, ref_no, expected_sample_ids, sample_page_id=None):
    page = ReferencePage()
    page.feed(data.decode("utf-8-sig"))
    citations = [d["text"].removeprefix("Reference: ") for d in page.divs if not d["children"]
                 and re.search(r"\[ER\s+[0-9]+\]$", d["text"])]
    explicit_sample_ids = set()
    for div in page.divs:
        if not div["children"]:
            match = re.fullmatch(r"Sample no\s*:\s*([0-9]+)", div["text"])
            if match:
                explicit_sample_ids.add(match[1])
    if sample_page_id is not None and explicit_sample_ids == {sample_page_id}:
        page.sample_ids.add(sample_page_id)
    result = {"status": "unresolved_no_unique_exact_id", "provider_citation": None,
              "provider_sample_ids": sorted(page.sample_ids, key=int),
              "expected_sample_ids_missing_on_page": sorted(set(expected_sample_ids) - page.sample_ids, key=int),
              "external_bibliographic_verification": "not_performed"}
    if any("No matching references were found" in div["text"] for div in page.divs):
        result["provider_access_message"] = "No matching references were found"
    if len(citations) != 1:
        return result
    if sample_page_id is not None and explicit_sample_ids != {sample_page_id}:
        return result
    citation = citations[0]
    ids = re.findall(r"\[ER\s+([0-9]+)\]", citation)
    if ids != [ref_no] or len(citation.split()) < 8:
        return result
    result["provider_citation"] = citation
    result["provider_contribution_statement"] = next(
        (d["text"] for d in page.divs if not d["children"] and d["text"].startswith("Contributed by ")), None)
    result["status"] = ("exact_id_sample_link_discrepancy" if result["expected_sample_ids_missing_on_page"]
                        else "provider_metadata_recovered")
    result["bibliographic_fields_review"] = "provider_rendered_text_with_collapsed_whitespace_original_html_retained"
    return result


def read_input(path):
    value = json.loads(Path(path).read_text())
    if value.get("database_sha256") != DATABASE_SHA256:
        raise ValueError("Input is not pinned to the original assembly")
    groups = value["missing_references"]
    if len(groups) != 58 or len({g["ref_no"] for g in groups}) != 58:
        raise ValueError("Input must contain the 58 distinct missing IDs")
    if sum(g["register_rows"] for g in groups) != 1266:
        raise ValueError("Input must cover 1266 register rows")
    for group in groups:
        if not re.fullmatch(r"[0-9]+", group["ref_no"]):
            raise ValueError("Invalid reference ID")
    return value


def collect(input_path, destination, delay=1.0, missing_from=None):
    if delay < 1:
        raise ValueError("At least one second between ordinary public requests")
    inputs = read_input(input_path)
    destination = Path(destination)
    destination.mkdir(exist_ok=False)
    receipts = []
    groups = inputs["missing_references"]
    if missing_from is not None:
        initial = build(input_path, missing_from)
        unresolved = {r["ref_no"] for r in initial["references"]
                      if r["status"] != "provider_metadata_recovered"}
        groups = [g for g in groups if g["ref_no"] in unresolved]
    for index, group in enumerate(groups):
        if index:
            time.sleep(delay)
        ref_no = group["ref_no"]
        sample_page_id = group["sample_ids"][0] if missing_from is not None else None
        url = (BASE + "?a=sampleResults&sample_no=" + sample_page_id if sample_page_id is not None
               else BASE + "?a=getRefs&ref_no=" + ref_no)
        receipt = {"ref_no": ref_no, "request_method": "GET", "url": url,
                   "requested_utc": datetime.now(timezone.utc).isoformat()}
        if sample_page_id is not None:
            receipt["sample_page_id"] = sample_page_id
        try:
            request = Request(url, headers={"User-Agent": "EPRP-reference-metadata-check/1.0"})
            with urlopen(request, timeout=40) as response:
                body = response.read()
                receipt.update({"status": response.status, "final_url": response.url,
                                "response_headers": {key: value for key, value in response.headers.items()
                                                     if key.lower() != "set-cookie"}})
            key = "ref-" + ref_no + ".html"
            with (destination / key).open("xb") as handle:
                handle.write(body)
            receipt.update({"body_file": key, "size": len(body), "sha256": sha256(body)})
        except Exception as error:
            receipt["access_error"] = str(error)
        receipt["completed_utc"] = datetime.now(timezone.utc).isoformat()
        receipts.append(receipt)
        write_new(destination / ("receipt-" + ref_no + ".json"), receipt)
    write_new(destination / "manifest.json", {"provider": "Fossilworks / Ecological Register",
              "input_sha256": sha256(Path(input_path).read_bytes()), "receipts": receipts})


def build(input_path, evidence_dir, supplemental_dir=None):
    inputs = read_input(input_path)
    evidence_dir = Path(evidence_dir)
    manifest_path = evidence_dir / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    if manifest["input_sha256"] != sha256(Path(input_path).read_bytes()):
        raise ValueError("Input does not match retrieval manifest")
    receipts = manifest["receipts"]
    by_id = {r["ref_no"]: r for r in receipts}
    groups = inputs["missing_references"]
    if len(receipts) != len(groups) or set(by_id) != {g["ref_no"] for g in groups}:
        raise ValueError("Receipt cohort differs from missing references")
    output = []
    for group in groups:
        receipt = by_id[group["ref_no"]]
        if json.loads((evidence_dir / ("receipt-" + group["ref_no"] + ".json")).read_text()) != receipt:
            raise ValueError("Individual receipt differs from retrieval manifest")
        entry = {"ref_no": group["ref_no"], "affected_register_rows": group["register_rows"],
                 "affected_sample_ids": group["sample_ids"], "source": receipt,
                 "source_collection": "initial_reference_pages"}
        if receipt.get("status") != 200 or "body_file" not in receipt:
            entry["status"] = "unresolved_access_error"
        else:
            key = receipt["body_file"]
            if key != "ref-" + group["ref_no"] + ".html":
                raise ValueError("Unexpected evidence filename")
            body = (evidence_dir / key).read_bytes()
            if len(body) != receipt["size"] or sha256(body) != receipt["sha256"]:
                raise ValueError("Source evidence hash/size mismatch: " + key)
            entry.update(parse_reference(body, group["ref_no"], group["sample_ids"]))
        output.append(entry)
    supplemental_manifest_hash = None
    if supplemental_dir is not None:
        supplemental_dir = Path(supplemental_dir)
        extra_manifest_path = supplemental_dir / "manifest.json"
        extra_manifest = json.loads(extra_manifest_path.read_text())
        supplemental_manifest_hash = sha256(extra_manifest_path.read_bytes())
        if extra_manifest["input_sha256"] != sha256(Path(input_path).read_bytes()):
            raise ValueError("Supplement input does not match retrieval manifest")
        seen = set()
        entries = {entry["ref_no"]: entry for entry in output}
        for receipt in extra_manifest["receipts"]:
            ref_no = receipt["ref_no"]
            if ref_no in seen or ref_no not in entries:
                raise ValueError("Duplicate or unknown supplement reference")
            seen.add(ref_no)
            if json.loads((supplemental_dir / ("receipt-" + ref_no + ".json")).read_text()) != receipt:
                raise ValueError("Individual supplement receipt differs from manifest")
            entry = entries[ref_no]
            sample_id = receipt["sample_page_id"]
            if sample_id not in entry["affected_sample_ids"]:
                raise ValueError("Supplement sample not in original reference cohort")
            if entry["status"] == "provider_metadata_recovered":
                raise ValueError("Supplement must not replace a recovered citation")
            if receipt.get("status") == 200 and "body_file" in receipt:
                key = receipt["body_file"]
                if key != "ref-" + ref_no + ".html":
                    raise ValueError("Unexpected supplement filename")
                body = (supplemental_dir / key).read_bytes()
                if sha256(body) != receipt["sha256"] or len(body) != receipt["size"]:
                    raise ValueError("Supplement evidence hash/size mismatch")
                recovered = parse_reference(body, ref_no, entry["affected_sample_ids"], sample_id)
                entry["initial_reference_page_result"] = {"status": entry["status"], "source": entry["source"],
                                                         "provider_access_message": entry.get("provider_access_message")}
                entry.pop("provider_access_message", None)
                entry.update(recovered)
                entry["source"] = receipt
                entry["source_collection"] = "sample_page_supplement"
                entry["recovery_route"] = "original_sample_page_with_explicit_sample_id_and_exact_reference_id"
    return {"kind": "separate missing-reference metadata overlay; original assembly unchanged",
            "database_sha256": DATABASE_SHA256,
            "input_sha256": sha256(Path(input_path).read_bytes()),
            "evidence_manifest_sha256": sha256(manifest_path.read_bytes()),
            "evidence_directory": evidence_dir.name,
            "supplemental_manifest_sha256": supplemental_manifest_hash,
            "supplemental_directory": Path(supplemental_dir).name if supplemental_dir is not None else None,
            "provider": manifest["provider"],
            "access_depth": "full provider reference pages; bibliographic metadata only",
            "counts": dict(Counter(r["status"] for r in output)),
            "references": output,
            "limitations": ["Provider metadata recovery does not independently verify bibliographic accuracy or source contents.",
                            "Missing original reference-sheet rows remain missing; join this overlay explicitly by ref_no.",
                            "Sample links are supporting identity checks, not evidence of independent communities.",
                            "Current provider pages are later observations, not corrections to the retained interval exports."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    extract = sub.add_parser("extract-input")
    extract.add_argument("database")
    extract.add_argument("output")
    acquire = sub.add_parser("collect")
    acquire.add_argument("input")
    acquire.add_argument("evidence_directory")
    acquire.add_argument("--delay", type=float, default=1.0)
    acquire.add_argument("--missing-from", help="Use original sample pages for initially unresolved IDs")
    rebuild = sub.add_parser("build")
    rebuild.add_argument("input")
    rebuild.add_argument("evidence_directory")
    rebuild.add_argument("output")
    rebuild.add_argument("--supplement")
    args = parser.parse_args()
    if args.command == "extract-input":
        value = extract_input(args.database)
        if args.output == "-":
            print(json.dumps(value, ensure_ascii=False, indent=2))
        else:
            write_new(args.output, value)
    elif args.command == "collect":
        collect(args.input, args.evidence_directory, args.delay, args.missing_from)
    else:
        write_new(args.output, build(args.input, args.evidence_directory, args.supplement))


if __name__ == "__main__":
    main()
