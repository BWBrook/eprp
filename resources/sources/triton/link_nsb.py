"""Link Triton's Neptune-sourced records to an NSB snapshot, record by record.

Usage: python3 link_nsb.py TRITON_NEPTUNE_ROWS_TSV NSB_SQLITE

The rows file is written by triton_profile.R. Triton sampleIDs for Neptune rows
are "<leg>-<sitehole>_<NSB sample_id>". Reports how many link to the snapshot,
whether holes and depths agree, the Triton (GTS2020) minus NSB (GTS2012) age
differences, how often Triton's original name matches an NSB occurrence name in
the same sample, and how much of NSB's foraminifera the link covers.
"""

import csv
import sqlite3
import statistics
import sys
from collections import Counter, defaultdict

rows = list(csv.DictReader(open(sys.argv[1]), delimiter="\t"))
con = sqlite3.connect(f"file:{sys.argv[2]}?mode=ro", uri=True)
samples = {r[0]: r[1:] for r in con.execute(
    "select sample_id, hole_id, sample_depth_mbsf, sample_age_ma, fossil_group from neptune_sample")}
names = defaultdict(set)
q = """select st.sample_id, lower(trim(t.genus || ' ' || t.species || coalesce(' ' || nullif(t.subspecies, ''), '')))
       from neptune_sample_taxa st join neptune_taxonomy t on t.taxon_id = st.taxon_id"""
for sid, name in con.execute(q):
    names[sid].add(name)

out = Counter()
age_diffs, tri_samples = [], set()
for r in rows:
    out["triton_neptune_rows"] += 1
    sid = int(r["sampleID"].rsplit("_", 1)[1])
    tri_samples.add(sid)
    s = samples.get(sid)
    if s is None:
        out["rows_sample_not_in_snapshot"] += 1
        continue
    hole, depth, age, group = s
    out["rows_linked"] += 1
    out[f"linked_rows_nsb_group_{group}"] += 1
    if hole.replace("_", "-") != r["holeID"]:
        out["linked_rows_hole_mismatch"] += 1
    if depth is not None and r["sample.depth"] not in ("", "NA") and abs(float(depth) - float(r["sample.depth"])) > 0.01:
        out["linked_rows_depth_differs_gt_0.01m"] += 1
    if age is not None and r["age"] not in ("", "NA"):
        age_diffs.append(float(r["age"]) - float(age))
    if r["orig.species"].lower().strip() in names[sid]:
        out["linked_rows_orig_name_matches_nsb_name_in_sample"] += 1

for k, v in sorted(out.items()):
    print(f"{k}\t{v}")
print(f"triton_neptune_samples\t{len(tri_samples)}")
print(f"triton_neptune_samples_in_snapshot\t{len(tri_samples & samples.keys())}")
abs_d = [abs(d) for d in age_diffs]
print(f"age_pairs\t{len(age_diffs)}")
print(f"age_diff_median_triton_minus_nsb_myr\t{statistics.median(age_diffs):.4f}")
for thr in (0.01, 0.1, 0.5, 1.0):
    print(f"age_absdiff_gt_{thr}_myr\t{sum(d > thr for d in abs_d)}")
nsb_f = {sid for sid, s in samples.items() if s[3] == "F"}
nsb_f_dated = {sid for sid, s in samples.items() if s[3] == "F" and s[2] is not None}
print(f"nsb_foram_samples\t{len(nsb_f)}")
print(f"nsb_foram_samples_linked_from_triton\t{len(nsb_f & tri_samples)}")
print(f"nsb_dated_foram_samples_linked_from_triton\t{len(nsb_f_dated & tri_samples)} of {len(nsb_f_dated)}")
