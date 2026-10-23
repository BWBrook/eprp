"""Link Triton's Neptune-sourced records to an NSB snapshot, record by record.

Usage: python3 link_nsb.py TRITON_NEPTUNE_ROWS_TSV NSB_SQLITE [NSB_RECOMPUTED_AGES_TSV]

The rows file is written by triton_profile.R. Triton sampleIDs for Neptune rows
are "<leg>-<sitehole>_<NSB sample_id>". Reports how many link to the snapshot,
whether holes and depths agree, whether Triton's pre-conversion age (orig.age)
equals NSB's stored age, the Triton (GTS2020) minus NSB (GTS2012) age
differences, whether Triton's palaeolatitude equals NSB's, how often Triton's
original name(s) match an NSB occurrence name in the same sample, and how much
of NSB's foraminifera the link covers. With the recomputed-ages file written by
nsb/age_check.py, also compares against NSB ages recomputed from current models.
"""

import csv
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
con = sqlite3.connect(f"file:{sys.argv[2]}?mode=ro", uri=True)
recomputed = {}
if len(sys.argv) > 3:
    for r in csv.DictReader(open(sys.argv[3]), delimiter="\t"):
        if r["recomputed_age_ma"]:
            recomputed[int(r["sample_id"])] = float(r["recomputed_age_ma"])
samples = {r[0]: r[1:] for r in con.execute(
    "select sample_id, hole_id, sample_depth_mbsf, sample_age_ma, fossil_group, paleo_latitude from neptune_sample")}
names = defaultdict(set)
q = """select st.sample_id, lower(trim(t.genus || ' ' || t.species || coalesce(' ' || nullif(t.subspecies, ''), '')))
       from neptune_sample_taxa st join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
for sid, name in con.execute(q):
    names[sid].add(name)


def num(x):
    return None if x in ("", "NA", None) else float(x)


keys = ["triton_neptune_rows", "rows_linked", "rows_sample_not_in_snapshot", "linked_rows_hole_mismatch",
        "linked_rows_depth_differs_gt_0.01m", "linked_rows_orig_age_equals_nsb_age", "linked_rows_orig_age_differs",
        "linked_rows_pal_lat_equals_nsb", "linked_rows_pal_lat_differs", "linked_rows_nsb_pal_lat_null",
        "linked_rows_whole_name_matches", "linked_rows_any_name_part_matches", "linked_rows_all_name_parts_match"]
out = Counter({k: 0 for k in keys})
age_diffs, recomputed_diffs, tri_samples = [], [], set()
for r in rows:
    out["triton_neptune_rows"] += 1
    sid = int(r["sampleID"].rsplit("_", 1)[1])
    tri_samples.add(sid)
    s = samples.get(sid)
    if s is None:
        out["rows_sample_not_in_snapshot"] += 1
        continue
    hole, depth, age, group, pal_lat = s
    out["rows_linked"] += 1
    out[f"linked_rows_nsb_group_{group}"] += 1
    if hole.replace("_", "-") != r["holeID"]:
        out["linked_rows_hole_mismatch"] += 1
    if depth is not None and num(r["sample.depth"]) is not None and abs(float(depth) - num(r["sample.depth"])) > 0.01:
        out["linked_rows_depth_differs_gt_0.01m"] += 1
    if age is not None and num(r.get("orig.age")) is not None:
        same = abs(float(age) - num(r["orig.age"])) <= 1e-6
        out["linked_rows_orig_age_equals_nsb_age" if same else "linked_rows_orig_age_differs"] += 1
    if age is not None and num(r["age"]) is not None:
        age_diffs.append(num(r["age"]) - float(age))
    if sid in recomputed and num(r["age"]) is not None:
        recomputed_diffs.append(abs(num(r["age"]) - recomputed[sid]))
    if pal_lat is None:
        out["linked_rows_nsb_pal_lat_null"] += 1
    elif num(r.get("pal.lat")) is not None:
        same = abs(float(pal_lat) - num(r["pal.lat"])) <= 1e-4
        out["linked_rows_pal_lat_equals_nsb" if same else "linked_rows_pal_lat_differs"] += 1
    whole = r["orig.species"].lower().strip()
    parts = [p.strip() for p in whole.split(", ")]
    out["linked_rows_whole_name_matches"] += whole in names[sid]
    out["linked_rows_any_name_part_matches"] += any(p in names[sid] for p in parts)
    out["linked_rows_all_name_parts_match"] += all(p in names[sid] for p in parts)

for k, v in sorted(out.items()):
    print(f"{k}\t{v}")
print(f"triton_neptune_samples\t{len(tri_samples)}")
print(f"triton_neptune_samples_in_snapshot\t{len(tri_samples & samples.keys())}")
abs_d = [abs(d) for d in age_diffs]
print(f"age_pairs\t{len(age_diffs)}")
print(f"age_diff_median_triton_minus_nsb_myr\t{statistics.median(age_diffs):.4f}")
for thr in (0.01, 0.1, 0.5, 1.0):
    print(f"age_absdiff_gt_{thr}_myr\t{sum(d > thr for d in abs_d)}")
if recomputed_diffs:
    for thr in (0.5, 1.0):
        print(f"age_absdiff_vs_nsb_recomputed_gt_{thr}_myr\t{sum(d > thr for d in recomputed_diffs)}")
nsb_f = {sid for sid, s in samples.items() if s[3] == "F"}
nsb_f_dated = {sid for sid, s in samples.items() if s[3] == "F" and s[2] is not None}
print(f"nsb_foram_samples\t{len(nsb_f)}")
print(f"nsb_foram_samples_linked_from_triton_neptune_rows\t{len(nsb_f & tri_samples)}")
print(f"nsb_dated_foram_samples_linked_from_triton_neptune_rows\t{len(nsb_f_dated & tri_samples)} of {len(nsb_f_dated)}")
