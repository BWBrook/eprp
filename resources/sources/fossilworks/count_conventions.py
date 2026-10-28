#!/usr/bin/env python3
"""Build an additive count-evidence overlay; never edit the assembled source.

Usage: python3 count_conventions.py ASSEMBLY.sqlite NEW_OUTPUT_DIRECTORY
Literal matches are retrieval flags, never biological unit assignments.
Only hash-pinned, row-guarded human-readable reviews assign units.
"""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import csv
from decimal import Decimal, InvalidOperation
import hashlib
import json
from pathlib import Path
import re
import sqlite3


REVIEW = Path(__file__).parent / "profile/count-conventions-reviewed-2026-10-28.json"
PATTERNS = {
    "mni_mention": r"\bMNI\b",
    "nisp_mention": r"\bNISP\b",
    "individual_mention": r"\bindividuals?\b|\banimals?\b",
    "material_mention": r"\b(?:teeth|tooth|bones?|fragments?|mandibles?|maxillae|jaws?|skeletons?|osteoderms?|postcrania|scales|shells?|burial)\b",
    "specimen_mention": r"\bspecimens?\b",
    "approximation_mention": r"\b(?:approximate(?:ly)?|estimated|about|several|numerous|a few|many)\b",
    "bound_mention": r"\b(?:minimum|maximum|at least|more than|less than)\b",
    "inclusion_exclusion_mention": r"\b(?:plus|also present|not counted|excludes?|does not include|included in the count|not enumerated|not described|additional)\b",
    "association_mention": r"\b(?:belong|belonging|representing|represent|associated|same individual|counted together|single burial)\b",
}


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def evidence_spans(comment):
    return [{"flag": flag, "start": m.start(), "end": m.end(), "text": m.group()}
            for flag, pattern in PATTERNS.items()
            for m in re.finditer(pattern, comment, re.I)]


def checked_reviews(rows, review):
    by_id = {r["_fw_row_id"]: r for r in rows}
    result = {}
    for item in review["rows"]:
        key = item["row_id"]
        if key in result:
            raise ValueError(f"Duplicate reviewed row: {key}")
        if key not in by_id or any(by_id[key][k] != v for k, v in item["expected"].items()):
            raise ValueError(f"Reviewed evidence guard failed: {key}")
        result[key] = item
    return result


def annotate(row, reviews):
    item = reviews.get(row["_fw_row_id"])
    spans = evidence_spans(row["comments"])
    return {
        "row_id": row["_fw_row_id"], "interval_id": row["_fw_interval_id"],
        "sample_no": row["sample no"], "ref_no": row["ref no"],
        "genus_raw": row.get("genus", ""), "species_raw": row.get("species", ""),
        "life_form_raw": row.get("life form", ""),
        "count_raw": row["count"], "comments_raw": row["comments"],
        "provider_default": "specimens_unspecified_protocol",
        "count_unit": item["unit"] if item else "unknown",
        "review_level": item["level"] if item else "not_reviewed",
        "review_id": item["review_id"] if item else "",
        "issues": encoded(item.get("issues", [])) if item else "[]",
        "flags": encoded(sorted({e["flag"] for e in spans})),
        "evidence_spans": encoded(spans),
    }


def write_tsv(path, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def build(database, destination, review_path=REVIEW):
    database, destination, review_path = map(Path, (database, destination, review_path))
    if destination.exists():
        raise FileExistsError(destination)
    review = json.loads(review_path.read_text())
    before = digest(database)
    if before != review["assembly_sha256"]:
        raise ValueError("Assembly SHA256 differs from reviewed evidence")
    with closing(sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)) as con:
        con.row_factory = sqlite3.Row
        con.execute("PRAGMA query_only=ON")
        rows = [dict(r) for r in con.execute("SELECT * FROM register_rows ORDER BY _fw_row_id")]
        samples = [dict(r) for r in con.execute("SELECT * FROM samples_rows ORDER BY _fw_row_id")]
    reviews = checked_reviews(rows, review)
    annotations = [annotate(r, reviews) for r in rows]
    grouped = defaultdict(list)
    sample_reviews = {(s["interval_id"], s["sample_no"]): s
                      for s in review.get("sample_reviews", [])}
    for a in annotations:
        grouped[(a["interval_id"], a["sample_no"])].append(a)
    sample_rows = []
    for s in samples:
        a = grouped[(s["_fw_interval_id"], s["sample no"])]
        units = Counter(r["count_unit"] for r in a)
        known = sorted(set(units) - {"unknown"})
        sample_review = sample_reviews.get((s["_fw_interval_id"], s["sample no"]), {})
        sample_rows.append({
            "sample_source_row_id": s["_fw_row_id"], "interval_id": s["_fw_interval_id"],
            "sample_no": s["sample no"], "sample_name": s["sample name"],
            "ref_no": s["ref no"], "register_rows": len(a),
            "reviewed_rows": sum(r["review_level"] != "not_reviewed" for r in a),
            "unit_counts": encoded(dict(sorted(units.items()))),
            "multiple_reviewed_units": len(known) > 1,
            "unreviewed_or_unresolved_unit_rows": units.get("unknown", 0),
            "issue_row_ids": encoded([r["row_id"] for r in a if r["issues"] != "[]"]),
            "taphonomic_context_raw": s["taphonomic context"],
            "preservation_raw": s["preservation"], "archaeology_raw": s["archaeology"],
            "sampling_methods_raw": s["sampling methods"],
            "source_review": encoded(sample_review),
        })
    nonpositive, noninteger, nonnumeric = [], [], []
    for row in rows:
        try:
            value = Decimal(row["count"])
            if not value.is_finite():
                raise InvalidOperation
            if value <= 0:
                nonpositive.append(row["_fw_row_id"])
            if value != value.to_integral_value():
                noninteger.append(row["_fw_row_id"])
        except InvalidOperation:
            nonnumeric.append(row["_fw_row_id"])
    flag_counts = Counter(f for a in annotations for f in json.loads(a["flags"]))
    unique_samples = {(s["_fw_interval_id"], s["sample no"]) for s in samples}
    summary = {
        "assembly_sha256": before, "script_sha256": digest(__file__),
        "review_sha256": digest(review_path), "register_rows": len(rows),
        "sample_source_rows": len(samples), "distinct_interval_sample_keys": len(unique_samples),
        "reviewed_rows": len(reviews),
        "source_checked_rows": sum(a["review_level"] == "primary_source_checked" for a in annotations),
        "unit_counts": dict(Counter(a["count_unit"] for a in annotations)),
        "review_level_counts": dict(Counter(a["review_level"] for a in annotations)),
        "life_form_row_counts": dict(Counter(r.get("life form", "") for r in rows)),
        "literal_flag_row_counts": dict(flag_counts),
        "rows_with_any_literal_flag": sum(bool(json.loads(a["flags"])) for a in annotations),
        "numeric_checks": {"nonpositive_rows": nonpositive, "noninteger_rows": noninteger,
                           "nonnumeric_rows": nonnumeric},
        "sample_metadata_nonempty_source_rows": {f: sum(bool(s[f]) for s in samples)
            for f in ("taphonomic context", "preservation", "archaeology", "sampling methods")},
        "multiple_reviewed_unit_sample_keys": sorted({(s["interval_id"], s["sample_no"])
            for s in sample_rows if s["multiple_reviewed_units"]}),
        "limits": ["Literal flags are retrieval aids with no precision or recall claim.",
                   "No unit propagates from one row to a sample or reference.",
                   "Unknown is not NISP, MNI, or validated specimen equivalence.",
                   "Taphonomic and sampling fields are source metadata, not quantitative corrections.",
                   "Source checks assess reported counting protocols, not ecological abundance validity."],
    }
    if digest(database) != before:
        raise ValueError("Assembly changed during read-only profiling")
    destination.mkdir(parents=True)
    write_tsv(destination / "register-count-evidence.tsv", annotations)
    write_tsv(destination / "sample-count-evidence.tsv", sample_rows)
    summary["outputs"] = {p.name: {"sha256": digest(p), "bytes": p.stat().st_size}
                          for p in sorted(destination.iterdir())}
    (destination / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--review", type=Path, default=REVIEW)
    args = parser.parse_args()
    print(json.dumps(build(args.database, args.destination, args.review), indent=2))
