"""Profile a STRATDAT snapshot (GA resfacs:Biostratigraphy WFS layer) and check its zone ages against ASUD.

Usage: python3 stratdat_profile.py BIOSTRATIGRAPHY_CSV ASUD_STRATIGRAPHICUNIT_CSV OUT_TSV

Counts picks, boreholes, basins, classes, zones, pick types, confidence and
sources; age coverage; then, for picks whose sample sits in an ASUD unit
(STRATNO_MIDPOINT), whether the zone's age range overlaps the unit's numeric age
range (inverted ASUD ranges swapped; placeholder ASUD ages of 0-0 and 4,000 Ma or
more excluded). Writes long-format (table, metric, key, value). Standard library only.
"""

import csv
import statistics
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
out = []


def add(*row):
    out.append(row)


def tab(t, m, values, n=15):
    for k, v in Counter(values).most_common(n):
        add(t, m, k, v)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
t = "picks"
add(t, "rows", "", len(rows))
add(t, "distinct_stratdat_no", "", len({r["STRATDAT_NO"] for r in rows}))
add(t, "boreholes", "", len({r["ENO"] for r in rows}))
add(t, "distinct_zone_names", "", len({r["ZONE_NAME"] for r in rows}))
for k in ("ONSHORE_OFFSHORE", "STATE", "BOREHOLE_PROVINCE", "CLASS", "HIGH_LOW", "PICK_DESC", "PREFERRED_ALTERNATE",
          "CONFIDENCE_CODE", "SOURCE_REF", "BOREHOLE_TYPE", "ACTIVE", "OVERALL_ACCESS"):
    tab(t, f"by:{k}", [r[k] for r in rows], 35 if k == "BOREHOLE_PROVINCE" else 15)
tab(t, "boreholes_by:BOREHOLE_PROVINCE", [p for p in {(r["ENO"], r["BOREHOLE_PROVINCE"]) for r in rows} for p in [p[1]]], 35)
tab(t, "borehole_rig_release_decade", [f'{d[:3]}0s' for d in {(r["ENO"], r["RIG_RELEASE_DATE"]) for r in rows} for d in [d[1]] if d], 10)
ages = [(num(r["TOP_AGE_MA"]), num(r["BASE_AGE_MA"])) for r in rows]
add(t, "with_top_and_base_age", "", sum(a is not None and b is not None for a, b in ages))
add(t, "base_younger_than_top", "", sum(a is not None and b is not None and b < a for a, b in ages))
spans = [b - a for a, b in ages if a is not None and b is not None and b >= a]
add(t, "zone_span_myr_median", "", round(statistics.median(spans), 2))
tab(t, "base_age_period_bin_ma", [("0-23" if b < 23.04 else "23-66" if b < 66 else "66-145" if b < 143.1 else "145-252" if b < 251.9 else "252-541" if b < 538.8 else ">539") for a, b in ages if b is not None])
depth = [num(r["SAMPLE_DEPTH_M"]) for r in rows if num(r["SAMPLE_DEPTH_M"]) is not None]
add(t, "sample_depth_m_median_max", "", f"{statistics.median(depth):.0f} {max(depth):.0f}")
add(t, "with_stratno_midpoint", "", sum(bool(r["STRATNO_MIDPOINT"].strip()) for r in rows))
add(t, "with_strat_unit_midpoint", "", sum(bool(r["STRAT_UNIT_MIDPOINT"].strip()) for r in rows))
add(t, "with_coordinates", "", sum(num(r["COLLAR_LAT_GDA94"]) is not None for r in rows))

both = [r for r in rows if r["STRAT_UNIT_TOP"].strip() and r["STRAT_UNIT_MIDPOINT"].strip()]
add(t, "picks_with_top_and_midpoint_units", "", len(both))
add(t, "top_unit_differs_from_midpoint_unit", "", sum(r["STRAT_UNIT_TOP"] != r["STRAT_UNIT_MIDPOINT"] for r in both))

with open(sys.argv[2], newline="", encoding="utf-8") as f:
    asud_rows = list(csv.DictReader(f))
asud = {u["STRATNO"]: u for u in asud_rows}
by_name = {}
for u in asud_rows:
    by_name.setdefault(u["NAME"].strip().lower(), []).append(u)


def age_key(r, u):
    a, b = num(r["TOP_AGE_MA"]), num(r["BASE_AGE_MA"])
    o, y = num(u["NUMERICOLDERAGE"]), num(u["NUMERICYOUNGERAGE"])
    if o is None or y is None or (o == 0 and y == 0) or o >= 4000:
        return "asud_no_real_age", 0
    o, y = max(o, y), min(o, y)
    lo, hi = min(a, b), max(a, b)
    gap = max(y - hi, lo - o, 0)
    return ("overlap" if gap == 0 else "gap_le_5myr" if gap <= 5 else "gap_5_20myr" if gap <= 20 else "gap_gt_20myr"), gap


t = "age_check_top_unit_vs_asud"
check, by_class = Counter(), Counter()
for r in rows:
    if num(r["TOP_AGE_MA"]) is None or num(r["BASE_AGE_MA"]) is None or not r["STRAT_UNIT_TOP"].strip():
        continue
    names = [n.strip().lower() for n in r["STRAT_UNIT_TOP"].split(",") if n.strip()]
    hits = [by_name[n] for n in names if n in by_name and len(by_name[n]) == 1]
    if not hits:
        check["top_unit_not_matched_uniquely"] += 1
        continue
    key, _ = age_key(r, hits[-1][0])
    check[key] += 1
    by_class[(r["CLASS"] or "(blank)", key == "overlap")] += 1
for k, v in sorted(check.items()):
    add(t, "picks", k, v)
for c in sorted({c for c, _ in by_class}, key=lambda c: -(by_class[(c, True)] + by_class[(c, False)]))[:12]:
    add(t, "overlap_by:CLASS", c, f"{by_class[(c, True)]} of {by_class[(c, True)] + by_class[(c, False)]}")

t = "age_check_vs_asud"
check, gaps, by_class = Counter(), [], Counter()
add(t, "stratno_midpoint_with_several_units", "", sum("," in r["STRATNO_MIDPOINT"] for r in rows))
for r in rows:
    sn = r["STRATNO_MIDPOINT"].strip()
    a, b = num(r["TOP_AGE_MA"]), num(r["BASE_AGE_MA"])
    if not sn or a is None or b is None:
        continue
    found = [asud[s.strip().split(".")[0]] for s in sn.split(",") if s.strip().split(".")[0] in asud]
    if not found:
        check["stratno_not_in_asud"] += 1
        continue
    u = found[-1]  # the list runs from group to formation; take the most specific unit
    o, y = num(u["NUMERICOLDERAGE"]), num(u["NUMERICYOUNGERAGE"])
    if o is None or y is None or (o == 0 and y == 0) or o >= 4000:
        check["asud_no_real_age"] += 1
        continue
    o, y = max(o, y), min(o, y)
    lo, hi = min(a, b), max(a, b)
    gap = max(y - hi, lo - o, 0)
    key = "overlap" if gap == 0 else "gap_le_5myr" if gap <= 5 else "gap_5_20myr" if gap <= 20 else "gap_gt_20myr"
    check[key] += 1
    by_class[(r["CLASS"] or "(blank)", key == "overlap")] += 1
    if gap > 20:
        gaps.append((gap, r, u))
for k, v in sorted(check.items()):
    add(t, "picks", k, v)
for c in sorted({c for c, _ in by_class}, key=lambda c: -(by_class[(c, True)] + by_class[(c, False)])):
    add(t, "overlap_by:CLASS", c, f"{by_class[(c, True)]} of {by_class[(c, True)] + by_class[(c, False)]}")
for gap, r, u in sorted(gaps, key=lambda x: -x[0])[:10]:
    add(t, "gap_example", r["STRATDAT_NO"], f'{r["BOREHOLE_NAME"]} {r["SAMPLE_DEPTH_M"]} m | {r["ZONE_NAME"]} {r["TOP_AGE_MA"]}-{r["BASE_AGE_MA"]} Ma | ASUD {u["NAME"]} {u["NUMERICOLDERAGE"]}-{u["NUMERICYOUNGERAGE"]} Ma | gap {gap:.1f}')

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
