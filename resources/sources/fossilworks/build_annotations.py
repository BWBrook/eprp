#!/usr/bin/env python3
"""Build a separate, hash-guarded annotation SQLite; never modify the assembly.

Usage: build_annotations.py ASSEMBLY.sqlite PROFILE_DIR NEW_SIDECAR.sqlite
       --expected-hashes HASHES.json

HASHES.json maps the six keys returned by input_paths() to their SHA256 values.
Freeze these hashes after the source reviews are complete. No network is used.
All input documents are embedded verbatim; external HTML/PDF evidence remains
in its separately archived location with its original provenance and hashes.
"""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import re
import sqlite3
import tempfile

import count_conventions as counts


BASE_SHA256 = "ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610"
EXPECTED_COHORT = (58, 1266, 96)
EXPECTED_SOURCE_ROWS = (26046, 1697, 1675)
REGISTER_FIELDS = {
    "row_id": "_fw_row_id", "interval_id": "_fw_interval_id",
    "sample_no": "sample no", "ref_no": "ref no", "genus_raw": "genus",
    "species_raw": "species", "life_form_raw": "life form",
    "count_raw": "count", "comments_raw": "comments",
}
SAMPLE_FIELDS = {
    "sample_source_row_id": "_fw_row_id", "interval_id": "_fw_interval_id",
    "sample_no": "sample no", "sample_name": "sample name", "ref_no": "ref no",
    "taphonomic_context_raw": "taphonomic context", "preservation_raw": "preservation",
    "archaeology_raw": "archaeology", "sampling_methods_raw": "sampling methods",
}
JOIN_QUERIES = '''-- Open the base assembly read-only, then attach this sidecar read-only:
-- sqlite3 'file:/absolute/path/assembly.sqlite?mode=ro'
ATTACH DATABASE 'file:/absolute/path/annotations.sqlite?mode=ro' AS annotations;
-- Both LEFT JOINs have at most one match per original register row.
SELECT r.*, c.count_unit, c.review_level, c.review_id, c.issues,
       c.evidence_spans, rr.provider_citation AS recovered_provider_citation,
       rr.status AS reference_recovery_status,
       rr.evidence_json AS reference_recovery_evidence,
       b.evidence_json AS selected_bibliographic_check
FROM main.register_linked AS r
LEFT JOIN annotations.register_count_evidence AS c ON c.row_id=r._fw_row_id
LEFT JOIN annotations.reference_recovery AS rr ON rr.ref_no=r."ref no"
LEFT JOIN annotations.bibliographic_checks AS b ON b.ref_no=r."ref no";
-- Sample source row IDs, rather than sample numbers, preserve duplicate records.
SELECT s.*, c.register_rows, c.unit_counts, c.source_review
FROM main.samples_rows AS s
LEFT JOIN annotations.sample_count_evidence AS c
  ON c.sample_source_row_id=s._fw_row_id;
'''


def input_paths(profile):
    profile = Path(profile)
    return {
        "reference_recovery": profile / "reference-recovery-overlay-2026-10-28.json",
        "bibliographic_checks": profile / "reference-recovery-bibliographic-checks-2026-10-28.json",
        "count_register": profile / "count-conventions-2026-10-28/register-count-evidence.tsv",
        "count_samples": profile / "count-conventions-2026-10-28/sample-count-evidence.tsv",
        "count_summary": profile / "count-conventions-2026-10-28/summary.json",
        "count_review": profile / "count-conventions-reviewed-2026-10-28.json",
    }


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def read_tsv(data):
    reader = csv.DictReader(io.StringIO(data.decode("utf-8"), newline=""), delimiter="\t")
    if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames):
        raise ValueError("Missing or duplicate TSV columns")
    rows = list(reader)
    if any(None in r or None in r.values() for r in rows):
        raise ValueError("Malformed TSV row")
    return rows


def unique_rows(rows, key):
    result = {}
    for row in rows:
        identity = row[key]
        if not identity or identity in result:
            raise ValueError(f"Missing or duplicate {key}: {identity}")
        result[identity] = row
    return result


def verify_raw(annotations, source, key, fields):
    indexed = unique_rows(annotations, key)
    original = unique_rows(source, "_fw_row_id")
    if indexed.keys() != original.keys():
        raise ValueError(f"Overlay {key} coverage differs from assembly")
    for identity, annotation in indexed.items():
        if any(annotation[k] != original[identity][v] for k, v in fields.items()):
            raise ValueError(f"Raw source mismatch for {identity}")
    return indexed


def verify_counts(register, samples, annotations, sample_annotations, review, summary, blobs):
    actual_counts = (len(register), len(samples),
                     len({(r["_fw_interval_id"], r["sample no"]) for r in samples}))
    if actual_counts != EXPECTED_SOURCE_ROWS:
        raise ValueError("Unexpected assembly source cardinalities")
    if tuple(summary[k] for k in ("register_rows", "sample_source_rows", "distinct_interval_sample_keys")) != actual_counts:
        raise ValueError("Count summary cardinalities disagree")
    for label, name in [("count_register", "register-count-evidence.tsv"),
                        ("count_samples", "sample-count-evidence.tsv")]:
        receipt = summary["outputs"][name]
        if receipt["sha256"] != sha256(blobs[label]) or receipt["bytes"] != len(blobs[label]):
            raise ValueError(f"Count summary output hash/size mismatch: {name}")
    if summary["review_sha256"] != sha256(blobs["count_review"]):
        raise ValueError("Count review hash mismatch")
    indexed = verify_raw(annotations, register, "row_id", REGISTER_FIELDS)
    verify_raw(sample_annotations, samples, "sample_source_row_id", SAMPLE_FIELDS)
    reviewed = counts.checked_reviews(register, review)
    grouped = defaultdict(list)
    for source in register:
        actual = indexed[source["_fw_row_id"]]
        expected = counts.annotate(source, reviewed)
        if actual != {k: str(v) for k, v in expected.items()}:
            raise ValueError(f"Count annotation does not reproduce review: {source['_fw_row_id']}")
        grouped[(actual["interval_id"], actual["sample_no"])].append(actual)
    sample_reviews = {}
    for item in review.get("sample_reviews", []):
        key = (item["interval_id"], item["sample_no"])
        if key in sample_reviews:
            raise ValueError("Duplicate sample review")
        sample_reviews[key] = item
    for annotation in sample_annotations:
        key = (annotation["interval_id"], annotation["sample_no"])
        members = grouped[key]
        units = Counter(r["count_unit"] for r in members)
        # The originating overlay orders the source rows by their unique row ID.
        members = sorted(members, key=lambda r: r["row_id"])
        expected = {
            "register_rows": str(len(members)),
            "reviewed_rows": str(sum(r["review_level"] != "not_reviewed" for r in members)),
            "unit_counts": counts.encoded(dict(sorted(units.items()))),
            "multiple_reviewed_units": str(len(set(units) - {"unknown"}) > 1),
            "unreviewed_or_unresolved_unit_rows": str(units.get("unknown", 0)),
            "issue_row_ids": counts.encoded([r["row_id"] for r in members if r["issues"] != "[]"]),
            "source_review": counts.encoded(sample_reviews.get(key, {})),
        }
        if set(annotation) != set(SAMPLE_FIELDS) | set(expected) or any(annotation[k] != v for k, v in expected.items()):
            raise ValueError(f"Sample annotation aggregation differs: {annotation['sample_source_row_id']}")
    for field, name in [("count_unit", "unit_counts"), ("review_level", "review_level_counts")]:
        if dict(Counter(r[field] for r in annotations)) != summary[name]:
            raise ValueError(f"Summary {name} differs")
    if summary["reviewed_rows"] != len(reviewed) or summary["source_checked_rows"] != sum(r["review_level"] == "primary_source_checked" for r in annotations):
        raise ValueError("Summary review totals differ")


def verify_references(unresolved, recovery, checks):
    unique_rows(unresolved, "_fw_row_id")
    grouped = defaultdict(list)
    for row in unresolved:
        grouped[row["ref no"]].append(row)
    cohort = (len(grouped), len(unresolved), len({r["sample no"] for r in unresolved}))
    if cohort != EXPECTED_COHORT:
        raise ValueError(f"Unexpected unresolved reference cohort: {cohort}")
    references = unique_rows(recovery["references"], "ref_no")
    if references.keys() != grouped.keys():
        raise ValueError("Recovered reference IDs differ from unresolved assembly IDs")
    for ref_no, entry in references.items():
        sample_ids = {r["sample no"] for r in grouped[ref_no]}
        if (entry["affected_register_rows"] != len(grouped[ref_no])
                or len(entry["affected_sample_ids"]) != len(sample_ids)
                or set(entry["affected_sample_ids"]) != sample_ids):
            raise ValueError(f"Reference row/sample metadata mismatch: {ref_no}")
        citation = entry["provider_citation"]
        if not isinstance(citation, str) or re.findall(r"\[ER\s+([0-9]+)\]", citation) != [ref_no]:
            raise ValueError(f"Provider citation ID mismatch: {ref_no}")
        if entry["status"] != "provider_metadata_recovered" or entry["expected_sample_ids_missing_on_page"]:
            raise ValueError(f"Reference not completely recovered: {ref_no}")
        if not sample_ids.issubset(set(entry["provider_sample_ids"])) or entry["source"]["ref_no"] != ref_no:
            raise ValueError(f"Provider sample/reference evidence mismatch: {ref_no}")
    if recovery["counts"] != dict(Counter(r["status"] for r in references.values())):
        raise ValueError("Reference recovery status totals disagree")
    bibliography = unique_rows(checks["checks"], "ref_no")
    if bibliography.keys() != {"4030", "3996", "4414"} or not bibliography.keys() <= references.keys():
        raise ValueError("Selected bibliography check IDs differ")
    return references, cohort


def write_text_table(connection, table, rows, primary_key):
    columns = list(rows[0])
    if any(list(row) != columns for row in rows):
        raise ValueError(f"Inconsistent column order: {table}")
    quote = lambda value: '"' + value.replace('"', '""') + '"'
    declaration = ",".join(quote(k) + " TEXT NOT NULL" + (" PRIMARY KEY" if k == primary_key else "") for k in columns)
    connection.execute(f"CREATE TABLE {quote(table)} ({declaration})")
    placeholders = ",".join("?" for _ in columns)
    connection.executemany(f"INSERT INTO {quote(table)} VALUES ({placeholders})", [tuple(r[k] for k in columns) for r in rows])


def build(database, profile, destination, expected_hashes):
    database, destination = Path(database).resolve(), Path(destination)
    if destination.exists() or destination.is_symlink():
        raise FileExistsError(destination)
    paths = input_paths(profile)
    if set(expected_hashes) != set(paths) or any(not re.fullmatch(r"[a-f0-9]{64}", v) for v in expected_hashes.values()):
        raise ValueError("Expected hashes must specify exactly all six input documents")
    blobs = {label: path.read_bytes() for label, path in paths.items()}
    for label, data in blobs.items():
        if sha256(data) != expected_hashes[label]:
            raise ValueError(f"Input SHA256 mismatch: {label}")
    if digest(database) != BASE_SHA256:
        raise ValueError("Assembly SHA256 mismatch")
    recovery, checks, summary, review = (json.loads(blobs[k]) for k in ("reference_recovery", "bibliographic_checks", "count_summary", "count_review"))
    if any(obj[field] != BASE_SHA256 for obj, field in [(recovery, "database_sha256"), (summary, "assembly_sha256"), (review, "assembly_sha256")]):
        raise ValueError("Overlay assembly SHA256 mismatch")
    annotations, sample_annotations = (read_tsv(blobs[k]) for k in ("count_register", "count_samples"))
    with closing(sqlite3.connect(database.as_uri() + "?mode=ro", uri=True)) as source:
        source.row_factory = sqlite3.Row
        source.execute("PRAGMA query_only=ON")
        source.execute("BEGIN")
        register = [dict(r) for r in source.execute("SELECT * FROM register_rows ORDER BY _fw_row_id")]
        samples = [dict(r) for r in source.execute("SELECT * FROM samples_rows ORDER BY _fw_row_id")]
        unresolved = [dict(r) for r in source.execute("SELECT * FROM register_linked WHERE _fw_reference_status='unresolved'")]
    verify_counts(register, samples, annotations, sample_annotations, review, summary, blobs)
    references, cohort = verify_references(unresolved, recovery, checks)
    if digest(database) != BASE_SHA256:
        raise ValueError("Assembly changed during read-only verification")
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=".annotations-", suffix=".sqlite", dir=destination.parent)
    os.close(descriptor)
    temporary = Path(temporary)
    metadata = {
        "schema_version": 1, "base_sha256": BASE_SHA256,
        "input_sha256": dict(expected_hashes), "builder_sha256": digest(__file__),
        "count_builder_sha256": digest(counts.__file__),
        "source_rows": dict(zip(("register", "samples", "distinct_interval_samples"), EXPECTED_SOURCE_ROWS)),
        "recovery_cohort": dict(zip(("references", "register_rows", "sample_ids"), cohort)),
        "limits": ["Counts and original citations are never replaced or normalized.",
                   "Count units apply only to explicitly reviewed rows; no unit is inferred by this builder.",
                   "Selected bibliographic checks remain separate evidence; other references are not externally validated.",
                   "Original overlay documents are embedded verbatim; archived external HTML/PDF evidence remains external.",
                   "Join sample annotations by original sample source row ID, not sample number."],
    }
    try:
        with closing(sqlite3.connect(temporary)) as output:
            output.execute("CREATE TABLE metadata (key TEXT PRIMARY KEY, value_json TEXT NOT NULL)")
            output.executemany("INSERT INTO metadata VALUES (?,?)", [(key, encode(value)) for key, value in metadata.items()])
            output.execute("CREATE TABLE input_documents (label TEXT PRIMARY KEY, source_path TEXT NOT NULL, sha256 TEXT NOT NULL, content BLOB NOT NULL)")
            output.executemany("INSERT INTO input_documents VALUES (?,?,?,?)", [(label, str(paths[label]), expected_hashes[label], data) for label, data in blobs.items()])
            write_text_table(output, "register_count_evidence", annotations, "row_id")
            write_text_table(output, "sample_count_evidence", sample_annotations, "sample_source_row_id")
            output.execute("CREATE TABLE reference_recovery (ref_no TEXT PRIMARY KEY, provider_citation TEXT NOT NULL, status TEXT NOT NULL, affected_register_rows INTEGER NOT NULL, evidence_json TEXT NOT NULL)")
            output.executemany("INSERT INTO reference_recovery VALUES (?,?,?,?,?)", [(k, r["provider_citation"], r["status"], r["affected_register_rows"], encode(r)) for k, r in references.items()])
            output.execute("CREATE TABLE bibliographic_checks (ref_no TEXT PRIMARY KEY REFERENCES reference_recovery(ref_no), status TEXT NOT NULL, evidence_json TEXT NOT NULL)")
            output.executemany("INSERT INTO bibliographic_checks VALUES (?,?,?)", [(r["ref_no"], r["status"], encode(r)) for r in checks["checks"]])
            output.execute("CREATE TABLE suggested_queries (name TEXT PRIMARY KEY, sql_text TEXT NOT NULL)")
            output.execute("INSERT INTO suggested_queries VALUES ('attach_and_join',?)", (JOIN_QUERIES,))
            if output.execute("PRAGMA integrity_check").fetchall() != [("ok",)] or output.execute("PRAGMA foreign_key_check").fetchall():
                raise ValueError("Sidecar SQLite integrity check failed")
            output.commit()
        with temporary.open("rb") as stream:
            os.fsync(stream.fileno())
        if digest(database) != BASE_SHA256 or any(digest(paths[k]) != v for k, v in expected_hashes.items()):
            raise ValueError("An input changed during sidecar construction")
        os.link(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)
    return {"sidecar_sha256": digest(destination), **metadata}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("profile", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--expected-hashes", type=Path, required=True)
    arguments = parser.parse_args()
    print(json.dumps(build(arguments.database, arguments.profile, arguments.destination,
                           json.loads(arguments.expected_hashes.read_text())), indent=2))
