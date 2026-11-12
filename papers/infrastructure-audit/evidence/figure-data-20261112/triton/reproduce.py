"""Extract C045 figure values and independently verify the unrounded means.

python3 reproduce.py RETAINED_REPLAY_DIR TRITON_V4_RDATA [OUTPUT_DIR]
Only OUTPUT_DIR is written. Occurrence-level data stay in the retained inputs.
"""
import collections
import csv
import gzip
import hashlib
import json
import math
import pathlib
import platform
import statistics
import subprocess
import sys


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1048576), b""):
            h.update(block)
    return {"bytes": path.stat().st_size, "sha256": h.hexdigest()}


def table(path):
    with path.open() as stream:
        return list(csv.DictReader(stream, delimiter="\t"))


scripts = pathlib.Path(__file__).resolve().parent
work = pathlib.Path(sys.argv[1]).resolve()
source = pathlib.Path(sys.argv[2]).resolve()
out = pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else scripts
out.mkdir(parents=True, exist_ok=True)
pinned = {
    "triton_update_2023.RData": "7275120da2727e37b7d951632ea15364b0135d4aeaa5e67dee64a4a3d738af46",
    "inputs/lineage_edges.tsv": "ea616c1a73678879f5d55f6b384254e475c0affaa3ee310f59b4dbcf79a710bb",
    "inputs/name_crosswalk.tsv": "0b935bdf497e926d0c7ead29cc183844b40e238d02ca8be52f5bfb4bde9b0682",
    "inputs/species.tsv": "654bed448487179e3cd7b8d35cd872bf618fb75f516d21d276fee1c0f56d4420",
    "scripts/q012_original.R": "1ea8d57d5fe70ac58112f6c3e472201effc45e186a3b58ff1fdabc5f65707e5b",
    "scripts/raw_mean_check.R": "05eb23d55b5f235b694b425655f5db990a64ede99b24cb8ac4a65d3e6734771a",
    "scripts/triton_independent.py": "cfe40a469fcd315b9687620fa69e7608b2459c022f692672e899325b845cae90",
    "scripts/triton_prepare.R": "4d764e624845bee1716a0f9627c21df1323e79bf3ad808c21b894d7dc13726a6",
}
inputs = {name: digest(source if name == "triton_update_2023.RData" else work / name) for name in pinned}
for name, expected in pinned.items():
    assert inputs[name]["sha256"] == expected, (name, "pinned hash disagreement")
for name in ["projection.tsv.gz", "drop_rows.txt"]:
    inputs[name] = digest(work / name)
subprocess.run(["Rscript", str(scripts / "extract.R"), str(work), str(source), str(out)], check=True)

priority = ["ForCenS", "IODP", "Neptune", "Pangaea", "Lloydetal2012", "Fentonetal2016"]
with gzip.open(work / "projection.tsv.gz", "rt") as stream:
    rows = list(csv.DictReader(stream, delimiter="\t"))
groups = collections.defaultdict(list)
for r in rows:
    key = (r["species"], float(r["abundance"]),
           *(float(r[k]) if r[k] else None for k in ["sample.depth", "latitude_key", "longitude_key"]))
    groups[key].append(r)
drop = set()
for key, group in groups.items():
    if len(group) > 1 and key[2] is not None and len({r["db.source"] for r in group}) > 1:
        best = min(priority.index(r["db.source"]) for r in group)
        drop.update(int(r["row_index"]) for r in group if priority.index(r["db.source"]) > best)
retained_drop = {int(x) for x in (work / "drop_rows.txt").read_text().splitlines()}
assert drop == retained_drop and len(drop) == 16260
sp = [r for r in table(work / "inputs/species.tsv") if r["in_scope"] == "True"]
le = [r for r in table(work / "inputs/lineage_edges.tsv") if r["in_scope"] == "True"]
xw = {r["triton_name"]: r["s1_name"] for r in table(work / "inputs/name_crosswalk.tsv") if r["s1_name"]}
ranges = {r["morphospecies"].strip(): (float(r["end_Ma"]), float(r["start_Ma"])) for r in sp}
members = collections.defaultdict(set)
for r in sp:
    for lin in r["lineages"].split(";"):
        if lin:
            members[lin].add(r["morphospecies"].strip())
kept = []
for r in rows:
    species = xw.get(r["species"].strip())
    if r["trim"] != "inc" or not r["pal.lat"] or not r["age"] or species not in ranges:
        continue
    age = float(r["age"])
    if ranges[species][0] <= age <= ranges[species][1]:
        kept.append((species, age, abs(float(r["pal.lat"])), int(r["row_index"])))


def build(dedup):
    result = {}
    for lin in le:
        name = lin["lineage"]
        young, old = float(lin["end_Ma"]), float(lin["start_Ma"])
        bins = range(math.floor(young), max(math.floor(young), math.ceil(old) - 1) + 1)
        bybin = collections.defaultdict(list)
        for species, age, lat, index in kept:
            if species in members[name] and young <= age <= old and (not dedup or index not in drop):
                bybin[math.floor(age)].append(lat)
        for b in bins:
            result[(name, b)] = statistics.fmean(bybin[b]) if bybin[b] else None
    return result


before, after = build(False), build(True)
paired = {k for k in before if before[k] is not None and after[k] is not None}
missing = {k for k in before if before[k] is not None and after[k] is None}
assert len(paired) == 2267 and len(missing) == 4
max_difference = collections.Counter()
for name, expected_keys in [("comparable.tsv", paired), ("newly_missing.tsv", missing)]:
    actual = table(out / name)
    assert len(actual) == len(expected_keys)
    actual_keys = {(r["lineage"], int(r["bin"])) for r in actual}
    assert actual_keys == expected_keys
    for r in actual:
        k = r["lineage"], int(r["bin"])
        expected = {"before_mean_deg": before[k], "after_mean_deg": after[k],
                    "delta_after_minus_before_deg": after[k] - before[k] if k in paired else None}
        for col, value in expected.items():
            observed = None if r[col] == "NA" else float(r[col])
            assert (observed is None) == (value is None), (k, col)
            if value is not None:
                difference = abs(observed - value)
                assert difference <= 1e-12, (k, col, difference)
                max_difference[col] = max(max_difference[col], difference)
deltas = [after[k] - before[k] for k in paired]
assert sum(abs(d) > 1e-9 for d in deltas) == 1388
assert sum(abs(d) >= 1 - 1e-9 for d in deltas) == 411
assert abs(max(map(abs, deltas)) - 26.89925) < 1e-9
r_summary = {r["field"]: r["value"] for r in table(out / "r_summary.tsv")}
assert int(r_summary["total_lineage_bins"]) == len(before)
assert int(r_summary["both_missing"]) == sum(before[k] is None and after[k] is None for k in before)
receipt = {
    "claim": "C045", "source_revision": "5c37437",
    "quantity": "Observed mean absolute palaeolatitude per lineage and 1-Myr bin; before/after conservative cross-source removal. Unlagged, unstandardised.",
    "precision": "R binary64 means exported with sprintf(%.17g); no three-decimal tables used.",
    "versions": {"R": r_summary.pop("R"), "python": platform.python_version()},
    "r_summary": {k: float(v) if k == "max_abs_change_deg" else int(v) for k, v in r_summary.items()},
    "independent_python_check": {
        "route": "Numeric-tuple duplicate grouping, deletion membership, species/lineage/range/bin selection and statistics.fmean from retained 17-significant-digit raw projection, independently of original R emat builder.",
        "raw_presence_rows": len(rows), "rows_removed": len(drop), "deletion_membership_matches_retained": True,
        "verification_tolerance_deg": 1e-12, "changed_tolerance_deg": 1e-9,
        "one_degree_predicate": "abs(delta) >= 1 - 1e-9",
        "max_abs_R_minus_python_deg": dict(sorted(max_difference.items())),
        "comparable_values_checked": len(paired), "newly_missing_values_checked": len(missing),
    },
    "source_priority": priority,
    "inputs": inputs,
    "scripts": {name: digest(scripts / name) for name in ["extract.R", "reproduce.py"]},
    "outputs": {name: digest(out / name) for name in ["comparable.tsv", "newly_missing.tsv", "r_summary.tsv"]},
    "limitations": ["Key collisions do not establish duplicate physical observations.", "This is an EPRP descriptive support covariate, not a fitted biological outcome or a correction of an external published result.", "The independent Python route shares the raw RData projection, support tables and source-priority policy; it independently implements grouping and means."]
}
(out / "receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
print(json.dumps({"paired": len(paired), "newly_missing": len(missing), "changed": 1388, "at_least_one_degree": 411, "max_abs_change_deg": max(map(abs, deltas))}))
