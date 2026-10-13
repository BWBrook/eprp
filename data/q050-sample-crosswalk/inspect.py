#!/usr/bin/env python3
"""Inventory pinned PANGAEA exports; never join, deduplicate or interpolate."""

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path


SOURCES = {
    "761442": ("2fefa59ea76b1e8147afd32be8b1a2fbd52a3dc98f213060d577b758ddf0678b", "Sample label", "Depth comp [mcd]"),
    "761443": ("0b74d767943046e7b1e117b9dc35cd7d4e56855582f3d45eafdb98b10ff2eab5", "Depth comp [mcd]", "Depth comp [mcd]"),
    "736778": ("dded079f10fde1dcc303ad5a3f301517fc34cdae2352f680bf72353499e764c3", "Sample label", "Depth adj mcd [amcd]"),
    "892803": ("ecbc22e8945a0327edfd9726f8915526e952d5d951eaf995179901b435bc91ed", "Depth comp [mcd] (Primary shipboard splice)", "Depth comp [mcd] (Primary shipboard splice)"),
    "892804": ("063524e2a7b3a6d5887db3eb21374faf512961be63e339906ed8ce84c6119a83", "Depth comp [mcd]", "Depth comp [mcd]"),
}


def inventory(source_dir):
    result = []
    for dataset, (expected_sha, key, depth) in SOURCES.items():
        filename = f"q050-PANGAEA-{dataset}.txt"
        raw = (source_dir / filename).read_bytes()
        sha = hashlib.sha256(raw).hexdigest()
        if sha != expected_sha:
            raise ValueError(f"{filename}: source hash differs from inspected export")
        metadata, table = raw.decode("utf-8").split("*/\n", 1)
        if "CC-BY-3.0" not in metadata:
            raise ValueError(f"{filename}: expected source licence missing")
        parsed = list(csv.reader(io.StringIO(table), delimiter="\t"))
        fields, values = parsed[0], parsed[1:]
        if len(set(fields)) != len(fields) or any(len(r) != len(fields) for r in values):
            raise ValueError(f"{filename}: duplicate field or ragged row")
        rows = [dict(zip(fields, row)) for row in values]
        ages = [float(r["Age [ka BP]"]) for r in rows]
        depths = [float(r[depth]) for r in rows]
        counts = {field: sum(r[field] != "" for r in rows) for field in fields}
        key_counts = {}
        for row in rows:
            key_counts[row[key]] = key_counts.get(row[key], 0) + 1
        result.append({
            "dataset": f"10.1594/PANGAEA.{dataset}",
            "download_url": f"https://doi.pangaea.de/10.1594/PANGAEA.{dataset}?format=textfile",
            "retrieved": "2026-10-13", "filename": filename,
            "bytes": len(raw), "sha256": sha, "licence": "CC-BY-3.0",
            "rows": len(rows), "key_field": key, "unique_keys": len(key_counts),
            "repeated_keys": {k: v for k, v in key_counts.items() if v > 1},
            "age_ka_bp_min": min(ages), "age_ka_bp_max": max(ages),
            "depth_field": depth, "depth_min": min(depths), "depth_max": max(depths),
            "nonempty_by_field": counts,
        })
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output", type=Path, nargs="?", default=Path(__file__).with_name("inventory.json"))
    args = parser.parse_args()
    args.output.write_text(json.dumps(inventory(args.source_dir), ensure_ascii=False, indent=2) + "\n")
