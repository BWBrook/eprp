"""Compare NSB's stored sample ages with ages interpolated from each hole's current age model.

Usage: python3 age_check.py NSB_SQLITE [OUT_TSV]

Linear interpolation between the current revision's tie points, ordered by depth
then age (as NSBcompanion's findAge does). Samples outside the tie-point range
get no age. Prints counts by agreement class; with OUT_TSV also writes
sample_id, site_hole, stored and recomputed ages and the class for every sample.
"""

import bisect
import sqlite3
import sys
from collections import Counter, defaultdict

con = sqlite3.connect(f"file:{sys.argv[1]}?mode=ro", uri=True)
ties = defaultdict(list)
q = """select m.site_hole, m.depth_mbsf, m.age_ma from neptune_age_model m
       join neptune_age_model_history h on h.site_hole = m.site_hole and h.revision_no = m.revision_no
       where h.current_flag = 'Y' and m.depth_mbsf is not null and m.age_ma is not null
       order by m.site_hole, m.depth_mbsf, m.age_ma"""
for site_hole, depth, age in con.execute(q):
    ties[site_hole].append((float(depth), float(age)))


def interpolate(points, depth):
    depths = [d for d, _ in points]
    if not points or depth < depths[0] or depth > depths[-1]:
        return None
    i = bisect.bisect_left(depths, depth)
    if depths[i] == depth:
        return points[i][1]
    (d0, a0), (d1, a1) = points[i - 1], points[i]
    return a0 + (a1 - a0) * (depth - d0) / (d1 - d0)


classes = Counter()
by_hole = Counter()
out = open(sys.argv[2], "w") if len(sys.argv) > 2 else None
if out:
    out.write("sample_id\tsite_hole\tstored_age_ma\trecomputed_age_ma\tclass\n")
q = """select s.sample_id, hs.site_hole, s.sample_depth_mbsf, s.sample_age_ma
       from neptune_sample s join neptune_hole_summary hs using (hole_id) order by s.sample_id"""
for sid, site_hole, depth, stored in con.execute(q):
    model = ties.get(site_hole)
    calc = interpolate(model, float(depth)) if model and depth is not None else None
    if stored is None and calc is None:
        c = "both undated"
    elif stored is None:
        c = "stored undated, model dates it"
    elif calc is None:
        c = "stored dated, model cannot" if model else "stored dated, hole has no current model"
    else:
        diff = abs(float(stored) - calc)
        c = "agree (<=0.01 Myr)" if diff <= 0.01 else "differ 0.01-0.5 Myr" if diff <= 0.5 else "differ 0.5-1 Myr" if diff <= 1 else "differ >1 Myr"
        if diff > 0.01:
            by_hole[site_hole] += 1
    classes[c] += 1
    if out:
        out.write(f"{sid}\t{site_hole}\t{'' if stored is None else stored}\t{'' if calc is None else round(calc, 6)}\t{c}\n")
for c, n in sorted(classes.items()):
    print(f"{c}\t{n}")
print(f"holes with any sample differing >0.01 Myr\t{len(by_hole)}")
