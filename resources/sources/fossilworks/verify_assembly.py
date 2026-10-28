#!/usr/bin/env python3
"""Check an assembled Fossilworks database against its selected literal TSVs."""

import argparse
import hashlib
import json
from pathlib import Path
import sqlite3
from itertools import zip_longest


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(snapshot, database):
    con = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    require(con.execute("PRAGMA integrity_check").fetchone()[0] == "ok", "SQLite integrity check failed")
    require(not con.execute("PRAGMA foreign_key_check").fetchall(), "Foreign-key check failed")
    meta = {r["key"]: json.loads(r["value_json"]) for r in con.execute("SELECT * FROM metadata")}
    manifest_hash = sha(snapshot / "MANIFEST.json")
    require(manifest_hash == meta["manifest_sha256"], "Snapshot manifest hash differs")
    files = con.execute("SELECT file_id,sha256,header_json,row_count FROM source_files ORDER BY file_id").fetchall()
    require(len(files) == 100, "Expected 100 selected source files")
    checked_rows = 0
    for f in files:
        key = f["file_id"]
        path = snapshot / key
        require(path.resolve().is_relative_to(snapshot.resolve()), "Source path escapes snapshot: " + key)
        require(sha(path) == f["sha256"], "Source file hash mismatch: " + key)
        with path.open(encoding="utf-8-sig", newline="") as source:
            def fields(line):
                if line.endswith("\n"):
                    line = line[:-1]
                    if line.endswith("\r"):
                        line = line[:-1]
                return line.split("\t")

            header = fields(next(source))
            require(header == json.loads(f["header_json"]), "Header mismatch: " + key)
            db_rows = con.execute("SELECT record_number,line_start,line_end,values_json FROM source_rows WHERE file_id=? ORDER BY record_number", (key,))
            observed = 0
            for number, (line, row) in enumerate(zip_longest(source, db_rows), 1):
                require(line is not None and row is not None, f"Row-count mismatch: {key}")
                require(row["record_number"] == number and row["line_start"] == number + 1 and row["line_end"] == number + 1,
                        f"Row provenance mismatch: {key}#{number}")
                require(fields(line) == json.loads(row["values_json"]), f"Source field mismatch: {key}#{number}")
                observed += 1
                checked_rows += 1
            require(observed == f["row_count"], "Stored source row count differs: " + key)
    count = lambda sql: con.execute(sql).fetchone()[0]
    tables = {name: count('SELECT COUNT(*) FROM "' + name + '"') for name in
              ("intervals", "source_files", "source_rows", "register_rows", "register_linked",
               "samples_rows", "references_rows", "species_rows", "matrix_qc")}
    require(checked_rows == tables["source_rows"], "Source-row total mismatch")
    require(tables["register_rows"] == tables["register_linked"], "Register view multiplies or drops rows")
    stats = {
        "distinct_sample_ids": count('SELECT COUNT(DISTINCT "sample no") FROM samples_rows'),
        "register_rows_missing_within_interval_reference": count("SELECT COUNT(*) FROM register_linked WHERE _fw_reference_status='unresolved'"),
        "missing_reference_ids": count('SELECT COUNT(DISTINCT "ref no") FROM register_linked WHERE _fw_reference_status=\'unresolved\''),
        "sample_ids_with_missing_reference": count('SELECT COUNT(DISTINCT "sample no") FROM register_linked WHERE _fw_reference_status=\'unresolved\''),
        "sample_rows_with_identical_multiple_candidates": count("SELECT COUNT(*) FROM register_linked WHERE _fw_sample_status='repeated_identical'"),
        "sample_ids_with_total_discrepancy": count('SELECT COUNT(DISTINCT s."sample no") FROM sample_qc q JOIN samples_rows s ON s._fw_row_id=q.sample_row_id WHERE q.status IN (\'summary_lower\',\'summary_higher\')'),
        "matrix_cells_differing_from_register_sum": count("SELECT COUNT(*) FROM matrix_qc WHERE differs_from_sum=1"),
        "matrix_cells_differing_from_last_register_row": count("SELECT COUNT(*) FROM matrix_qc WHERE differs_from_last=1"),
        "species_rows_with_mass_field_absent": count('SELECT COUNT(*) FROM species_rows WHERE "mass (g)" IS NULL'),
        "species_rows_with_mass_field_present_empty": count('SELECT COUNT(*) FROM species_rows WHERE "mass (g)"=\'\''),
        "species_rows_with_mass_field_present_nonempty": count('SELECT COUNT(*) FROM species_rows WHERE "mass (g)" IS NOT NULL AND "mass (g)"<>\'\''),
    }
    result = {"database": str(database), "database_sha256": sha(database), "database_bytes": database.stat().st_size,
              "snapshot_manifest_sha256": manifest_hash, "source_files_checked": len(files),
              "source_rows_checked_field_by_field": checked_rows, "sqlite_integrity": "ok",
              "foreign_key_violations": 0, "tables": tables, "checks": stats}
    con.close()
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("database", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.snapshot, args.database), indent=2))
