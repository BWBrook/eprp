#!/usr/bin/env python3
"""Export C040 comparable signed NSB age differences; Python standard library only."""

import argparse
import bisect
import collections
import csv
import decimal
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform
import sqlite3


INPUT_SHA256 = "3fee4add2459c80529ab8cd018cdf2db2e60117b16fbdd2fb4be6a218d7a5a49"
EXPECTED = {
    "agree (<=0.01 Myr)": 52276,
    "both undated": 4712,
    "differ 0.01-0.5 Myr": 2475,
    "differ 0.5-1 Myr": 683,
    "differ >1 Myr": 953,
    "stored dated, model cannot": 294,
    "stored undated, model dates it": 469,
}


def sha256(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def category(stored, calculated, has_model):
    if stored is None:
        return "both undated" if calculated is None else "stored undated, model dates it"
    if calculated is None:
        return "stored dated, model cannot" if has_model else "stored dated, hole has no current model"
    diff = abs(stored - calculated)
    return ("agree (<=0.01 Myr)" if diff <= .01 else
            "differ 0.01-0.5 Myr" if diff <= .5 else
            "differ 0.5-1 Myr" if diff <= 1 else "differ >1 Myr")


def extract(database, output):
    assert sha256(database) == INPUT_SHA256, "Unexpected source database"
    output.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database.resolve().as_uri() + "?mode=ro", uri=True)
    connection.execute("PRAGMA query_only=ON")
    models = collections.defaultdict(list)
    for hole, depth, age in connection.execute("""
        SELECT m.site_hole, m.depth_mbsf, m.age_ma
        FROM neptune_age_model m JOIN neptune_age_model_history h
        ON h.site_hole=m.site_hole AND h.revision_no=m.revision_no
        WHERE h.current_flag='Y' AND m.depth_mbsf IS NOT NULL AND m.age_ma IS NOT NULL
    """):
        models[hole].append((float(depth), float(age)))
    models = {hole: sorted(points) for hole, points in models.items()}
    depths = {hole: [depth for depth, age in points] for hole, points in models.items()}
    collapsed = {}
    for hole, points in models.items():
        grouped = collections.defaultdict(list)
        for depth, age in points:
            grouped[depth].append(age)
        collapsed[hole] = (list(grouped), {d: (min(a), max(a)) for d, a in grouped.items()})

    counts = collections.Counter()
    holes = set()
    sensitivity = collections.Counter()
    plotted = duplicate_samples = conflicting_samples = checked = 0
    maximum_error = 0.0
    table = output / "nsb_signed_age_differences.tsv.gz"
    decimal.getcontext().prec = 50
    D = decimal.Decimal.from_float
    with table.open("wb") as raw:
        with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0, compresslevel=9) as compressed:
            with io.TextIOWrapper(compressed, encoding="utf-8", newline="") as handle:
                writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
                writer.writerow(["sample_id", "site_hole", "stored_minus_interpolated_age_myr"])
                for sid, hole, depth, stored in connection.execute("""
                    SELECT s.sample_id,h.site_hole,s.sample_depth_mbsf,s.sample_age_ma
                    FROM neptune_sample s JOIN neptune_hole_summary h USING(hole_id)
                    ORDER BY s.sample_id
                """):
                    calc = alternative = None
                    if hole in models and depth is not None and depths[hole][0] <= depth <= depths[hole][-1]:
                        ds, points = depths[hole], models[hole]
                        j = bisect.bisect_left(ds, depth)
                        if ds[j] == depth:
                            calc = points[j][1]
                            last = bisect.bisect_right(ds, depth)
                            duplicate_samples += last-j > 1
                            conflicting_samples += len({a for d, a in points[j:last]}) > 1
                            if last-j > 1 and stored is not None:
                                first_bad = abs(stored-points[j][1]) > .01
                                last_bad = abs(stored-points[last-1][1]) > .01
                                sensitivity['samples_differing_gt_001_first_tie'] += first_bad
                                sensitivity['samples_differing_gt_001_last_tie'] += last_bad
                                sensitivity['agreement_class_changes_first_vs_last'] += first_bad != last_bad
                        else:
                            d0, a0 = points[j-1]
                            d1, a1 = points[j]
                            calc = (a0*(d1-depth) + a1*(depth-d0))/(d1-d0)

                        # Separate check: collapse ties and use a high-precision slope formula.
                        unique, bounds = collapsed[hole]
                        k = bisect.bisect_right(unique, depth)
                        if unique[k-1] == depth:
                            alternative = D(bounds[depth][0])
                        else:
                            lower, upper = unique[k-1], unique[k]
                            low_age, high_age = bounds[lower][1], bounds[upper][0]
                            alternative = D(low_age)+(D(high_age)-D(low_age))*(D(float(depth))-D(lower))/(D(upper)-D(lower))
                        error = abs(calc-float(alternative))
                        maximum_error = max(maximum_error, error)
                        assert error <= 1e-11
                        checked += 1
                    label = category(stored, calc, hole in models)
                    counts[label] += 1
                    if stored is not None and calc is not None:
                        alt_diff = abs(D(float(stored))-alternative)
                        alt_label = ("agree (<=0.01 Myr)" if alt_diff <= decimal.Decimal("0.01") else
                                     "differ 0.01-0.5 Myr" if alt_diff <= decimal.Decimal("0.5") else
                                     "differ 0.5-1 Myr" if alt_diff <= 1 else "differ >1 Myr")
                        assert label == alt_label
                        writer.writerow([sid, hole, format(stored-calc, ".17g")])
                        plotted += 1
                        if abs(stored-calc) > .01:
                            holes.add(hole)
    connection.close()
    assert dict(counts) == EXPECTED
    assert plotted == 56387 and sum(counts.values()) == 61862 and len(holes) == 56
    assert sum(counts[k] for k in counts if k.startswith("differ")) == 4111
    assert duplicate_samples == conflicting_samples == 8
    assert dict(sensitivity) == {"samples_differing_gt_001_first_tie": 8,
                                  "samples_differing_gt_001_last_tie": 0,
                                  "agreement_class_changes_first_vs_last": 8}
    assert sha256(database) == INPUT_SHA256, "Source changed during extraction"
    with gzip.open(table, "rt", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(rows) == plotted
    assert len({r["sample_id"] for r in rows}) == plotted
    assert sum(abs(float(r["stored_minus_interpolated_age_myr"])) > .01 for r in rows) == 4111
    script = Path(__file__)
    receipt = {
        "claim": "C040", "figure": "Fig2D", "input_release": "2023-06-05_10063218",
        "input": {"file": database.name, "sha256": INPUT_SHA256, "bytes": database.stat().st_size},
        "script": {"file": script.name, "sha256": sha256(script)},
        "output": {"file": table.name, "sha256": sha256(table), "bytes": table.stat().st_size},
        "versions": {"python": platform.python_version(), "sqlite": sqlite3.sqlite_version},
        "units": "Myr", "sign": "stored sample age minus interpolated current-model age",
        "sample_order": "sample_id ascending", "float_export": ".17g",
        "gzip": "empty filename, mtime=0, compression level 9",
        "total_samples": sum(counts.values()), "plotted_comparable_samples": plotted,
        "classes": dict(counts), "samples_abs_difference_gt_0_01": 4111,
        "holes_disagreeing": len(holes),
        "duplicate_tie_depths": sum(len(p)-len(set(d for d,a in p)) for p in models.values()),
        "samples_at_duplicate_depth": duplicate_samples,
        "samples_at_conflicting_tie_age": conflicting_samples,
        "exact_duplicate_depth_sensitivity": dict(sensitivity),
        "interpolation": "Current_flag='Y' revision join; sort (depth,age). bisect_left selects first age at exact depth. Between depths use last lower tie and first upper tie, weighted endpoints. No extrapolation.",
        "independent_check": {"route": "Collapse equal-depth ties into min/max ages; bisect_right on unique depths; 50-digit Decimal slope interpolation from exact binary-float values. Independent arithmetic and tie lookup; shared source SQL.",
                              "model_dated_samples_checked": checked,
                              "maximum_absolute_interpolated_age_difference_myr": maximum_error,
                              "comparable_category_mismatches": 0},
        "checks": "Pinned input hash before/after; exact prior receipt categories/counts/tie sensitivity; gzip readback, unique sample IDs and threshold count. Noncomparable samples remain in classes only.",
        "limits": "Frozen database comparison under the recorded first-tie convention; not a claim of true sample ages or downstream analytical effect. Exact conflicting-depth classification is convention-sensitive."
    }
    (output / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"comparable": plotted, "total": sum(counts.values()), "disagreeing": 4111, "holes": len(holes), "output_bytes": table.stat().st_size}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", required=True, type=Path)
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()
    extract(args.database, args.output_directory)
