#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12,<3.13"
# dependencies = ["numpy==2.1.3", "openpyxl==3.1.5"]
# ///
"""Describe common-size ratios without inferring maturity or evolutionary coupling."""

import argparse
from collections import Counter
import csv
import hashlib
import json
import math
from pathlib import Path
import platform

import numpy as np
import openpyxl
from openpyxl.utils import get_column_letter


ROOT = Path(__file__).resolve().parents[2]
EXPECTED_SHA = "fbe2012f1d420ef7b292141ae0ed0ea8d046c4c15303663565dc72e0727ebe40"
RATIOS = ("CWI", "UWI", "WER")
PAIRS = ((2.0, 10.0), (5.0, 20.0))


def numeric(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def interpolate(points, target):
    for point in points:
        if point[0] == target:
            return {"values": point[1], "low_cell": point[2], "high_cell": point[2], "weight": 0.0}, "ok"
    for low, high in zip(points, points[1:]):
        if low[0] < target < high[0]:
            if high[0] / low[0] > 2.0:
                return None, "bracket_exceeds_factor_two"
            weight = math.log(target / low[0]) / math.log(high[0] / low[0])
            values = tuple(a + weight * (b - a) for a, b in zip(low[1], high[1]))
            return {"values": values, "low_cell": low[2], "high_cell": high[2], "weight": weight}, "ok"
    return None, "outside_joint_coverage"


def summary(rows):
    if len(rows) < 5:
        return {"n_rows": len(rows), "fit": "insufficient_rows"}
    late = np.array([[r[f"late_{k}"] for k in RATIOS] for r in rows])
    design = np.column_stack([np.ones(len(rows)), late])
    output = {"n_rows": len(rows), "n_source_family_labels": len({r["family"] for r in rows}), "ratios": {}}
    for idx, ratio in enumerate(RATIOS):
        early = np.array([r[f"early_{ratio}"] for r in rows])
        coefficients, _, rank, _ = np.linalg.lstsq(design, early, rcond=None)
        residual = early - design @ coefficients
        total = float(np.sum((early - early.mean()) ** 2))
        correlation = float(np.corrcoef(early, late[:, idx])[0, 1]) if np.std(early) and np.std(late[:, idx]) else None
        output["ratios"][ratio] = {
            "linear_in_sample_r2": 1.0 - float(residual @ residual) / total if total else None,
            "same_ratio_pearson_r": correlation,
            "design_rank": int(rank),
            "coefficients_intercept_CWI_UWI_WER": coefficients.tolist(),
            "early_range": [float(early.min()), float(early.max())],
            "late_range": [float(late[:, idx].min()), float(late[:, idx].max())],
        }
    return output


def run(source, outdir):
    source_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    if source_hash != EXPECTED_SHA:
        raise ValueError("Source does not match the original workbook hash")
    book = openpyxl.load_workbook(source, data_only=True)
    if book.sheetnames != ["Species", "dm", *RATIOS]:
        raise ValueError("Workbook schema changed")
    species = book["Species"]
    expected_whorls = [f"Whorl {12-i/2:g}" for i in range(25)]
    for name in ("dm", *RATIOS):
        sheet = book[name]
        if sheet.max_row != species.max_row or [c.value for c in sheet[1][6:]] != expected_whorls:
            raise ValueError(f"Unexpected shape or whorl headers: {name}")
        if [c.value for c in sheet["A"]] != [c.value for c in species["A"]]:
            raise ValueError(f"Taxon row order mismatch: {name}")
    records = []
    eligibility = []
    for row in range(2, species.max_row + 1):
        diameters = [book["dm"].cell(row, col).value for col in range(7, 32)]
        observed_dm = [float(x) for x in diameters if numeric(x)]
        monotone = all(x > 0 for x in observed_dm) and all(a > b for a, b in zip(observed_dm, observed_dm[1:]))
        points = []
        for col in range(7, 32):
            dm = book["dm"].cell(row, col).value
            values = tuple(book[k].cell(row, col).value for k in RATIOS)
            if numeric(dm) and all(numeric(v) for v in values):
                points.append((float(dm), values, f"{get_column_letter(col)}{row}"))
        points.sort()
        for early_size, late_size in PAIRS:
            pair = f"{early_size:g}_to_{late_size:g}"
            early, early_status = interpolate(points, early_size) if monotone else (None, "nonmonotone_diameter")
            late, late_status = interpolate(points, late_size) if monotone else (None, "nonmonotone_diameter")
            eligible = early is not None and late is not None
            eligibility.append({"workbook_row": row, "pair": pair, "early_status": early_status, "late_status": late_status, "eligible": eligible})
            if not eligible:
                continue
            record = {"workbook_row": row, "taxon_label": species.cell(row, 1).value, "family": species.cell(row, 2).value,
                      "source_label": species.cell(row, 8).value, "pair": pair, "early_native_diameter": early_size, "late_native_diameter": late_size}
            for label, value in (("early", early), ("late", late)):
                record.update({f"{label}_{k}": v for k, v in zip(RATIOS, value["values"])})
                record.update({f"{label}_{k}": value[k] for k in ("low_cell", "high_cell", "weight")})
            records.append(record)
    outdir.mkdir(parents=True, exist_ok=True)
    for filename, rows in (("workbook_size_pairs.tsv", records), ("workbook_eligibility.tsv", eligibility)):
        with (outdir / filename).open("w", newline="") as stream:
            writer = csv.DictWriter(stream, delimiter="\t", lineterminator="\n", fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    results = {"source_sha256": source_hash, "source_rows": species.max_row - 1, "source_unchanged": hashlib.sha256(source.read_bytes()).hexdigest() == source_hash,
               "python": platform.python_version(), "numpy": np.__version__, "openpyxl": openpyxl.__version__,
               "protocol_sha256": hashlib.sha256(Path(__file__).with_name("PROTOCOL.md").read_bytes()).hexdigest(),
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "pairs": {}}
    for early, late in PAIRS:
        pair = f"{early:g}_to_{late:g}"
        results["pairs"][pair] = summary([r for r in records if r["pair"] == pair])
        results["pairs"][pair]["eligibility_counts"] = dict(Counter(f"{r['early_status']} / {r['late_status']}" for r in eligibility if r["pair"] == pair))
    (outdir / "workbook_summary.json").write_text(json.dumps(results, indent=2, allow_nan=False) + "\n")
    print(json.dumps(results, indent=2, allow_nan=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=ROOT / "data/raw/ammonoid-growth-walton-korn-2018/Ontogenetic_Conch_Parameter_Data.xlsx")
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    run(args.source, args.output)
