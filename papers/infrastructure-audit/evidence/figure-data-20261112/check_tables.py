"""Validate the committed plotting values without loading the large source data."""

import bisect
import csv
import gzip
import hashlib
import json
import math
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / "replay-20261108"


def digest(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def table(path):
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def verify_files(directory, entries):
    for name, expected in entries.items():
        path = directory / name
        assert digest(path) == expected["sha256"], path
        assert path.stat().st_size == expected["bytes"], path


triton_dir = ROOT / "triton"
triton_receipt = json.loads((triton_dir / "receipt.json").read_text())
verify_files(triton_dir, triton_receipt["scripts"])
verify_files(triton_dir, triton_receipt["outputs"])
triton = table(triton_dir / "comparable.tsv")
lost = table(triton_dir / "newly_missing.tsv")
keys = {(r["lineage"], int(r["bin"])) for r in triton}
lost_keys = {(r["lineage"], int(r["bin"])) for r in lost}
assert len(triton) == len(keys) == 2267 and len(lost) == len(lost_keys) == 4
assert keys.isdisjoint(lost_keys)
deltas = []
for row in triton:
    before = float(row["before_mean_deg"])
    after = float(row["after_mean_deg"])
    delta = float(row["delta_after_minus_before_deg"])
    assert all(map(math.isfinite, (before, after, delta)))
    assert 0 <= before <= 90 and 0 <= after <= 90
    assert delta == after - before
    deltas.append(delta)
assert sum(abs(d) > 1e-9 for d in deltas) == 1388
assert sum(abs(d) >= 1 - 1e-9 for d in deltas) == 411
assert abs(max(map(abs, deltas)) - 26.89925) < 1e-12
assert all(r["after_mean_deg"] == r["delta_after_minus_before_deg"] == "NA" for r in lost)
assert all(math.isfinite(float(r["before_mean_deg"])) for r in lost)
assert triton_receipt["independent_python_check"]["comparable_values_checked"] == len(triton)
assert triton_receipt["independent_python_check"]["deletion_membership_matches_retained"]

nsb_dir = ROOT / "nsb"
nsb_receipt = json.loads((nsb_dir / "receipt.json").read_text())
assert digest(nsb_dir / nsb_receipt["script"]["file"]) == nsb_receipt["script"]["sha256"]
verify_files(nsb_dir, {nsb_receipt["output"]["file"]: nsb_receipt["output"]})
nsb_inputs = json.loads((PRIOR / "data/results/inputs_monarrez_nsb.json").read_text())["inputs"]
assert nsb_receipt["input"]["sha256"] == nsb_inputs["nsb/derived/2023-06-05_10063218/nsb.sqlite"]["sha256"]
old_nsb = json.loads((PRIOR / "data/results/nsb_2023-06-05.json").read_text())
assert nsb_receipt["classes"] == old_nsb["classes"]
assert nsb_receipt["exact_duplicate_depth_sensitivity"] == old_nsb["exact_duplicate_depth_sensitivity"]
nsb = table(nsb_dir / nsb_receipt["output"]["file"])
assert len(nsb) == len({r["sample_id"] for r in nsb}) == 56387
nsb_delta = [float(r["stored_minus_interpolated_age_myr"]) for r in nsb]
assert all(map(math.isfinite, nsb_delta))
nsb_bad = [(r, d) for r, d in zip(nsb, nsb_delta) if abs(d) > .01]
assert len(nsb_bad) == 4111 and len({r["site_hole"] for r, _ in nsb_bad}) == 56
assert sum(abs(d) <= .01 for d in nsb_delta) == 52276
assert sum(.01 < abs(d) <= .5 for d in nsb_delta) == 2475
assert sum(.5 < abs(d) <= 1 for d in nsb_delta) == 683
assert sum(abs(d) > 1 for d in nsb_delta) == 953
assert any(d < 0 for d in nsb_delta) and any(d > 0 for d in nsb_delta)

adm_dir = ROOT / "admtools"
adm_receipt = json.loads((adm_dir / "receipt.json").read_text())
assert digest(adm_dir / "extract_admtools.R") == adm_receipt["script_sha256"]
for name in ["sparse_curve.tsv", "tie_points.tsv"]:
    assert digest(adm_dir / name) == adm_receipt["output_sha256"][name.replace(".", "_")]
old_adm = json.loads((PRIOR / "software/case05_admtools.json").read_text())
old_env = json.loads((PRIOR / "software/package_environment.json").read_text())
assert adm_receipt["inputs"]["input_sha256"] == old_adm["input_sha256"]
for name, value in adm_receipt["environment"]["function_sha256"].items():
    assert value == old_env["function_sha256"][name]
curve = table(adm_dir / "sparse_curve.tsv")
assert len(curve) == len({int(r["draw_index"]) for r in curve}) == 8282
knots = [(0, 0), (8, 4), (14, 12), (26, 21), (32, 24), (38, 30)]
segments = [(0, 8, 0, 4), (8, 14, 6, 12), (14, 26, 15, 21),
            (26, 32, 21, 24), (32, 38, 24, 30)]
errors = []
truth_differences = []
returned_differences = []
for row in curve:
    h, truth, estimated, error = (float(row[name]) for name in
                                ["height", "truth_time_myr", "estimated_time_myr", "error_myr"])
    assert all(map(math.isfinite, (h, truth, estimated, error)))
    assert error == estimated - truth and 1 <= int(row["draw_index"]) <= 10000
    i = bisect.bisect_right([h for h, _ in knots], h) - 1
    assert int(row["deposition_segment"]) == i + 1
    h0, t0 = knots[i]
    h1, t1 = knots[i + 1]
    returned_differences.append(abs(estimated - (t0 + (h - h0) * (t1 - t0) / (h1 - h0))))
    lo, hi, start, end = segments[i]
    truth_differences.append(abs(truth - (start + (h - lo) * (end - start) / (hi - lo))))
    errors.append(error)
assert max(truth_differences) < 1e-12 and max(returned_differences) < 1e-12
assert sum(abs(e) > 1e-9 for e in errors) == 3972
assert max(map(abs, errors)) == old_adm["sparse_max_error"]
assert [float(r["height"]) for r in curve] == sorted(float(r["height"]) for r in curve)

files = {str(path.relative_to(ROOT)): {"sha256": digest(path), "bytes": path.stat().st_size}
         for directory in [triton_dir, nsb_dir, adm_dir]
         for path in sorted(directory.iterdir()) if path.is_file()}
assert all(entry["bytes"] < 1_000_000 for entry in files.values())
print(json.dumps({
    "checked_by": "main Codex; saved-table arithmetic and receipt/hash comparison",
    "source_revision": "5c37437", "checker_sha256": digest(Path(__file__)),
    "triton_C045": {"comparable": len(triton), "changed_gt_1e_9": 1388,
                    "change_ge_one_degree_with_tolerance": 411, "newly_missing_separate": len(lost),
                    "max_abs_delta_deg": max(map(abs, deltas))},
    "nsb_C040": {"comparable": len(nsb), "abs_delta_gt_0_01_myr": len(nsb_bad),
                 "holes_disagreeing": 56, "noncomparable_excluded": 61862 - len(nsb)},
    "admtools_C096": {"deposited": len(curve), "wrong_gt_1e_9_myr": 3972,
                      "max_abs_error_myr": max(map(abs, errors)),
                      "max_independent_truth_difference_myr": max(truth_differences),
                      "max_first_tie_interpolation_difference_myr": max(returned_differences)},
    "files": files,
    "limits": "Plotting values reproduce the bounded claims. No new biological analysis, causal attribution or figure rendering."
}, indent=2, sort_keys=True))
