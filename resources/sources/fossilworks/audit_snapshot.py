#!/usr/bin/env python3
"""Audit retained interval bundles, keeping all source bytes unchanged."""

import argparse
import csv
import json
from pathlib import Path

from acquire_intervals import TABLES, now, parse_table, save, sha, validate


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    manifest_path = args.snapshot / "MANIFEST.json"
    manifest = json.loads(manifest_path.read_text())
    failures = []
    for record in manifest["files"]:
        path = args.snapshot / record["key"]
        if not path.exists() or sha(path.read_bytes()) != record["sha256"]:
            failures.append(record["key"])
    outcomes = []
    rows = []
    for interval in manifest["intervals"]:
        destination = args.output / interval["directory"]
        destination.mkdir()
        attempts = []
        for work in sorted((args.snapshot / interval["directory"]).glob("attempt-*")):
            if not (work / "assessment.json").exists() or not all((work / (name + ".txt")).exists() for name in TABLES):
                continue
            original = json.loads((work / "assessment.json").read_text())
            if original.get("expected_rows") is None:
                continue
            audit_directory = destination / work.name
            audit_directory.mkdir()
            check = validate(work, interval["interval"], original["expected_rows"], audit_directory)
            stable = {name: (work / (name + ".verify.txt")).exists() and
                      sha((work / (name + ".txt")).read_bytes()) == sha((work / (name + ".verify.txt")).read_bytes()) for name in TABLES}
            register_header, register_rows = parse_table(work / "register.txt")
            sample_header, sample_rows = parse_table(work / "samples.txt")
            reference_header, reference_rows = parse_table(work / "references.txt")
            register_refs = {r[register_header.index("ref no")] for r in register_rows}
            sample_refs = {r[sample_header.index("ref no")] for r in sample_rows}
            reference_ids = {r[reference_header.index("ref_no")] for r in reference_rows}
            details = {"source_attempt": str(work.relative_to(args.snapshot)), "expected_rows": original["expected_rows"],
                       "validation": check, "stable_second_get": stable,
                       "reference_ids_absent_from_reference_table": sorted((register_refs | sample_refs) - reference_ids),
                       "reference_ids_without_register_rows": sorted(reference_ids - register_refs),
                       "original_acquisition_state": original["state"],
                       "source_files": [{"key": str((work / (name + ".txt")).relative_to(args.snapshot)),
                                         "size": (work / (name + ".txt")).stat().st_size,
                                         "sha256": sha((work / (name + ".txt")).read_bytes())} for name in TABLES]}
            details["state"] = ("coherent_export" if check["passed"] else "downloaded_source_inconsistency") if all(stable.values()) else "unstable_export"
            attempts.append(details)
            save(audit_directory / "audit.json", details)
        selected = next((a for a in attempts if a["state"] == "coherent_export"), None)
        selected = selected or next((a for a in attempts if a["state"] == "downloaded_source_inconsistency"), None)
        if selected:
            outcome = {"interval": interval["interval"], **selected,
                       "attempts_retained": len(attempts),
                       "repeat_download_hashes_identical": all(a["source_files"] == selected["source_files"] for a in attempts) if len(attempts) > 1 else None}
            if len(attempts) > 1:
                outcome["repeat_download_hashes_identical"] = all(
                    [f["sha256"] for f in a["source_files"]] == [f["sha256"] for f in selected["source_files"]] for a in attempts)
            rows.append({"interval": interval["interval"], "state": selected["state"], "source_attempt": selected["source_attempt"],
                         **selected["validation"]["rows"], "distinct_sample_ids": selected["validation"]["distinct_sample_ids"],
                         "duplicate_sample_summary_rows": selected["validation"]["repeated_sample_summary_rows"],
                         "matrix_sample_columns": selected["validation"]["matrix_sample_columns"],
                         "matrix_cells_different_from_sum": selected["validation"]["matrix_cells_differing_from_summed_register"],
                         "matrix_cells_different_from_last": selected["validation"]["matrix_cells_differing_from_last_register_row"],
                         "missing_reference_records": len(selected["reference_ids_absent_from_reference_table"])})
        else:
            outcome = {"interval": interval["interval"], "state": "no_stable_five_table_bundle", "attempts": attempts}
        outcomes.append(outcome)
    report = {"audited_utc": now(), "snapshot": str(args.snapshot), "manifest_sha256": sha(manifest_path.read_bytes()),
              "audit_tool_sha256": sha(Path(__file__).read_bytes()), "manifest_hash_failures": failures,
              "visible_intervals": len(outcomes), "stable_five_table_bundles": len(rows),
              "coherent_bundles": sum(o["state"] == "coherent_export" for o in outcomes), "intervals": outcomes,
              "scope": "Acquisition and cross-table integrity audit only. No data assembly, deduplication, harmonization or scientific suitability validation."}
    save(args.output / "audit.json", report)
    if rows:
        with (args.output / "intervals.tsv").open("w") as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
            writer.writeheader()
            writer.writerows(rows)
    print(json.dumps({key: report[key] for key in ("manifest_hash_failures", "visible_intervals", "stable_five_table_bundles", "coherent_bundles")}, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
