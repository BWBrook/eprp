"""Profile a STRATDAT snapshot (GA resfacs:Biostratigraphy WFS layer) and check its zone ages against ASUD.

Usage: python3 stratdat_profile.py BIOSTRATIGRAPHY_CSV ASUD_STRATIGRAPHICUNIT_CSV OUT_TSV

Counts picks, boreholes, basins (first token of BOREHOLE_PROVINCE, then the
second token), classes, zones, pick types, confidence grades and sources; age
coverage, placeholders, zone spans and period bins; the ages the layer carries
for chronostratigraphic units; depth anomalies; and how far picks link to ASUD.
Then, for picks whose STRAT_UNIT_TOP resolves to an ASUD unit by name, whether
the zone's age range overlaps the unit's numeric age range (inverted ASUD ranges
swapped; placeholder ASUD ages of 0-0 and 4,000 Ma or more excluded), with the
overlap of randomly reassigned units as a null, the per-borehole spread, and
the same check through STRAT_UNIT_MIDPOINT. Writes long-format (table, metric,
key, value). Standard library only. See stratdat_midpoint_check.py for the test
of what the *_MIDPOINT fields are evaluated at.
"""

import csv
import os
import random
import re
import statistics
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
out = []
SEED = 20261022
NULL_REPS = 20
OVERLAP, LE5, LE20, GT20 = "overlap", "gap_le_5myr", "gap_5_20myr", "gap_gt_20myr"
GTS2012_EDGES = [("Neogene+Quaternary", 23.03), ("Paleogene", 66.0), ("Cretaceous", 145.0), ("Jurassic-Triassic", 252.17), ("Palaeozoic", 541.0)]
LAYER_EDGES = [("Neogene+Quaternary", 23.03), ("Paleogene", 66.04), ("Cretaceous", 145.7), ("Jurassic-Triassic", 251.9), ("Palaeozoic", 541.0)]


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


def filled(r, k):
    return bool(r[k].strip())


def share(m, n):
    return f"{m} of {n} ({100 * m / n:.1f}%)" if n else "0 of 0"


def bin_of(base, edges):
    for label, edge in edges:
        if base <= edge + 1e-9:
            return label
    return "Precambrian"


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
with open(sys.argv[2], newline="", encoding="utf-8") as f:
    asud_rows = list(csv.DictReader(f))
asud = {u["STRATNO"]: u for u in asud_rows}
by_name = defaultdict(list)
for u in asud_rows:
    by_name[u["NAME"].strip().lower()].append(u)
n_rows = len(rows)
n_holes = len({r["ENO"] for r in rows})

t = "inputs"
add(t, "stratdat_snapshot", "", os.path.basename(os.path.dirname(os.path.abspath(sys.argv[1]))))
add(t, "asud_snapshot", "", os.path.basename(os.path.dirname(os.path.abspath(sys.argv[2]))))
add(t, "asud_rows", "", len(asud_rows))
add(t, "asud_names_shared_by_several_units", "", sum(len(v) > 1 for v in by_name.values()))

t = "picks"
add(t, "rows", "", n_rows)
add(t, "distinct_stratdat_no", "", len({r["STRATDAT_NO"] for r in rows}))
add(t, "boreholes", "", n_holes)
add(t, "distinct_zone_names_nonblank", "", len({r["ZONE_NAME"] for r in rows if filled(r, "ZONE_NAME")}))
add(t, "picks_with_blank_zone_name", "", share(sum(not filled(r, "ZONE_NAME") for r in rows), n_rows))
add(t, "blank_zone_name_picks_with_an_age", "", sum(not filled(r, "ZONE_NAME") and num(r["TOP_AGE_MA"]) is not None for r in rows))
add(t, "named_zone_picks_without_an_age", "", sum(filled(r, "ZONE_NAME") and num(r["TOP_AGE_MA"]) is None for r in rows))
for k in ("ONSHORE_OFFSHORE", "STATE", "CLASS", "HIGH_LOW", "PICK_DESC", "PREFERRED_ALTERNATE", "SOURCE_REF",
          "BOREHOLE_TYPE", "ACTIVE", "OVERALL_ACCESS", "DEPTH_REF_TYPE", "DEPTH_REF_POINT_ELEV_UOM"):
    tab(t, f"by:{k}", [r[k] for r in rows], 15)
add(t, "picks_with_collar_coordinates", "", share(sum(num(r["COLLAR_LAT_GDA94"]) is not None and num(r["COLLAR_LONG_GDA94"]) is not None for r in rows), n_rows))
add(t, "picks_with_sample_depth", "", share(sum(num(r["SAMPLE_DEPTH_M"]) is not None for r in rows), n_rows))
for k in ("SOURCE_REF", "CONFIDENCE_CODE", "SAMPLENO"):
    add(t, f"picks_with_{k}", "", share(sum(filled(r, k) for r in rows), n_rows))
for k in ("BOREHOLE_PID", "SAMPLE_PID"):
    add(t, f"{k}_ends_in_a_number", "", share(sum(bool(re.search(r"\d$", r[k])) for r in rows), n_rows))
add(t, "SAMPLE_PID_distinct_values", "", dict(Counter(r["SAMPLE_PID"] for r in rows)))
hl = Counter(r["HIGH_LOW"] for r in rows)
add(t, "high_or_low_datums_H_plus_L", "", share(hl["H"] + hl["L"], n_rows))
codes = [re.fullmatch(r"(.*?)(\d?)", r["CONFIDENCE_CODE"].strip()) for r in rows]
tab(t, "by:CONFIDENCE_SAMPLE_TYPE", [c.group(1) or "(blank)" for c in codes], 30)
tab(t, "by:CONFIDENCE_GRADE", [c.group(2) or "(none)" for c in codes], 15)

t = "basins"
hole_provinces = defaultdict(set)
for r in rows:
    hole_provinces[r["ENO"]].add(r["BOREHOLE_PROVINCE"])


def tokens(r):
    return [x.strip() for x in r["BOREHOLE_PROVINCE"].split(",") if x.strip()]


def basin(r):
    return (tokens(r) or ["(blank)"])[0]


def second(r):
    return (tokens(r)[1:2] or ["(none)"])[0]


add(t, "boreholes_with_several_province_strings", "", sum(len(v) > 1 for v in hole_provinces.values()))
tab(t, "picks_by_basin", [basin(r) for r in rows], 20)
tab(t, "boreholes_by_basin", [b for _, b in {(r["ENO"], basin(r)) for r in rows}], 20)
tab(t, "picks_by_basin|second_token", [f"{basin(r)} | {second(r)}" for r in rows], 30)
tab(t, "boreholes_by_basin|second_token", [f"{b} | {s}" for _, b, s in {(r["ENO"], basin(r), second(r)) for r in rows}], 30)
cooper = [r for r in rows if "Cooper Basin" in tokens(r)]
add(t, "picks_with_Cooper_Basin_token", "", len(cooper))
add(t, "boreholes_with_Cooper_Basin_token", "", len({r["ENO"] for r in cooper}))

t = "boreholes"
pairs = {(r["ENO"], r["RIG_RELEASE_DATE"]) for r in rows}
add(t, "distinct_borehole_release_date_pairs", "", len(pairs))
for d, v in sorted(Counter(f"{d[:3]}0s" if d else "undated" for _, d in pairs).items()):
    add(t, "rig_release_decade", d, v)
add(t, "boreholes_released_before_2000", "", share(sum(bool(d) and d[:4] < "2000" for _, d in pairs), n_holes))

t = "ages"
ages = [(num(r["TOP_AGE_MA"]), num(r["BASE_AGE_MA"])) for r in rows]
have = [(a, b) for a, b in ages if a is not None and b is not None]
real = [(a, b) for a, b in have if not (a == 0 and b == 0)]
add(t, "picks_with_top_and_base_age", "", len(have))
add(t, "placeholder_0_0_ages", "", len(have) - len(real))
add(t, "placeholder_0_0_zone_names", "", dict(Counter(r["ZONE_NAME"] for r in rows if num(r["TOP_AGE_MA"]) == 0 and num(r["BASE_AGE_MA"]) == 0)))
add(t, "picks_with_real_ages", "", share(len(real), n_rows))
add(t, "real_ages_base_younger_than_top", "", sum(b < a for a, b in real))
spans = [b - a for a, b in real if b >= a]
add(t, "real_zone_span_myr_median", "", round(statistics.median(spans), 2))
add(t, "real_zone_span_myr_deciles_10_to_90", "", " ".join(f"{q:.1f}" for q in statistics.quantiles(spans, n=10, method="inclusive")))
add(t, "real_zone_span_zero", "", sum(s == 0 for s in spans))
add(t, "real_zone_span_over_20_myr", "", share(sum(s > 20 for s in spans), len(spans)))
for name, edges in (("gts2012_edges_23.03_66.0_145.0_252.17_541.0", GTS2012_EDGES), ("layer_system_edges_23.03_66.04_145.7_251.9_541", LAYER_EDGES)):
    c = Counter(bin_of(b, edges) for _, b in real)
    for label in [x for x, _ in edges] + ["Precambrian"]:
        add(t, f"real_base_age_bins:{name}", label, c[label])
add(t, "real_base_age_in_145.0_to_145.7_window", "", sum(145.0 < b <= 145.7 for _, b in real))
add(t, "real_base_age_in_65.9_to_66.04_window", "", sum(66.0 < b <= 66.04 for _, b in real))

t = "chronostrat_ages"
for cls in ("system/period", "series/epoch", "stage/age"):
    per = defaultdict(Counter)
    for r in rows:
        if r["CLASS"] == cls and num(r["TOP_AGE_MA"]) is not None:
            per[r["ZONE_NAME"]][(r["TOP_AGE_MA"], r["BASE_AGE_MA"])] += 1
    for zone, c in sorted(per.items(), key=lambda kv: (float(kv[1].most_common(1)[0][0][0]), kv[0])):
        (top, base), n = c.most_common(1)[0]
        add(t, f"modal_top-base_ma:{cls}", zone, f"{top}-{base} ({n} of {sum(c.values())} picks)")

t = "depth"
depth = [num(r["SAMPLE_DEPTH_M"]) for r in rows if num(r["SAMPLE_DEPTH_M"]) is not None]
add(t, "sample_depth_m_median", "", f"{statistics.median(depth):.0f}")
add(t, "sample_depth_m_max", "", f"{max(depth):.0f}")
add(t, "picks_with_depth_le_0", "", sum(d <= 0 for d in depth))
deep = [r for r in rows if (num(r["SAMPLE_DEPTH_M"]) or 0) > 5000]
add(t, "picks_deeper_than_5000_m", "", len(deep))
add(t, "boreholes_with_picks_deeper_than_5000_m", "", len({r["ENO"] for r in deep}))
add(t, "deeper_than_5000_m_picks_with_elevation_unit_ft", "", sum(r["DEPTH_REF_POINT_ELEV_UOM"] == "ft" for r in deep))
deepest = defaultdict(float)
for r in rows:
    deepest[r["BOREHOLE_NAME"]] = max(deepest[r["BOREHOLE_NAME"]], num(r["SAMPLE_DEPTH_M"]))
for name, d in sorted(deepest.items(), key=lambda kv: -kv[1])[:8]:
    add(t, "deepest_pick_by_borehole_m", name, f"{d:g}")
ft = [r for r in rows if r["DEPTH_REF_POINT_ELEV_UOM"] == "ft"]
add(t, "picks_with_elevation_unit_ft", "", len(ft))
add(t, "boreholes_with_elevation_unit_ft", "", dict(Counter(r["BOREHOLE_NAME"] for r in ft)))


def names_of(field):
    return [n.strip() for n in re.split(r"[,;]", field) if n.strip()]


def match(names, strict):
    """The ASUD unit for the most specific name that is unique in ASUD (strict: the last name only)."""
    for n in reversed(names[-1:] if strict else names):
        candidates = by_name.get(n.lower())
        if candidates and len(candidates) == 1:
            return candidates[0]
    return None


def asud_age(u):
    o, y = num(u["NUMERICOLDERAGE"]), num(u["NUMERICYOUNGERAGE"])
    if o is None or y is None or (o == 0 and y == 0) or o >= 4000:
        return None
    return max(o, y), min(o, y)


def gap_of(lo, hi, older, younger):
    return max(younger - hi, lo - older, 0)


def gap_class(gap):
    return OVERLAP if gap == 0 else LE5 if gap <= 5 else LE20 if gap <= 20 else GT20


def real_ages(r):
    a, b = num(r["TOP_AGE_MA"]), num(r["BASE_AGE_MA"])
    return None if a is None or b is None or (a == 0 and b == 0) else (min(a, b), max(a, b))


t = "asud_link_coverage"
top_rows = [r for r in rows if filled(r, "STRAT_UNIT_TOP")]
state_rows = [r for r in rows if filled(r, "STATE_STRAT_UNIT_TOP")]
add(t, "picks_with_STRAT_UNIT_TOP", "", share(len(top_rows), n_rows))
add(t, "boreholes_with_STRAT_UNIT_TOP", "", share(len({r["ENO"] for r in top_rows}), n_holes))
add(t, "picks_with_STATE_STRAT_UNIT_TOP", "", share(len(state_rows), n_rows))
add(t, "boreholes_with_STATE_STRAT_UNIT_TOP", "", share(len({r["ENO"] for r in state_rows}), n_holes))
add(t, "picks_with_either_unit_field", "", share(sum(filled(r, "STRAT_UNIT_TOP") or filled(r, "STATE_STRAT_UNIT_TOP") for r in rows), n_rows))
add(t, "picks_with_STATE_STRAT_UNIT_TOP_and_no_STRAT_UNIT_TOP", "", sum(not filled(r, "STRAT_UNIT_TOP") for r in state_rows))
add(t, "picks_with_STRAT_UNIT_TOP_resolving_to_an_ASUD_unit_by_name", "", share(sum(match(names_of(r["STRAT_UNIT_TOP"]), False) is not None for r in top_rows), len(top_rows)))
add(t, "picks_with_STRAT_UNIT_TOP_whose_last_name_is_unique_in_ASUD", "", share(sum(match(names_of(r["STRAT_UNIT_TOP"]), True) is not None for r in top_rows), len(top_rows)))
state_hits = sum(
    any(len(by_name.get(s.strip().lstrip("_").lower(), [])) == 1 for s in r["STATE_STRAT_UNIT_TOP"].split(";"))
    for r in state_rows
)
add(t, "picks_with_a_STATE_STRAT_UNIT_TOP_string_equal_to_a_unique_ASUD_name", "", share(state_hits, len(state_rows)))
add(t, "picks_with_STRATNO_MIDPOINT_the_only_ASUD_identifier", "", share(sum(filled(r, "STRATNO_MIDPOINT") for r in rows), n_rows))

t = "stratno_midpoint"
multi_id = [r for r in rows if "," in r["STRATNO_MIDPOINT"]]
add(t, "picks_with_several_ids", "", len(multi_id))
ascending = 0
for r in multi_id:
    ids = [int(float(i)) for i in r["STRATNO_MIDPOINT"].split(",")]
    ascending += ids == sorted(ids)
add(t, "several_ids_in_ascending_numeric_order", "", share(ascending, len(multi_id)))
position = Counter()
for r in multi_id:
    if ";" in r["STRAT_UNIT_MIDPOINT"] or not filled(r, "STRAT_UNIT_MIDPOINT"):
        continue
    ids = [i.strip() for i in r["STRATNO_MIDPOINT"].split(",")]
    specific = names_of(r["STRAT_UNIT_MIDPOINT"])[-1].lower()
    hit = [k for k, i in enumerate(ids) if i in asud and asud[i]["NAME"].strip().lower() == specific]
    position["most_specific_unit_id_absent"] += not hit
    position["most_specific_unit_id_first"] += bool(hit) and hit[0] == 0
    position["most_specific_unit_id_last"] += bool(hit) and hit[0] == len(ids) - 1
    position["most_specific_unit_id_in_the_middle"] += bool(hit) and 0 < hit[0] < len(ids) - 1
for k, v in sorted(position.items()):
    add(t, "several_ids_single_unit_list", k, v)


def top_records(strict):
    """(eno, state, basin, lo, hi, older, younger, class) for picks with real ages and a STRAT_UNIT_TOP."""
    recs, skipped = [], Counter()
    for r in top_rows:
        z = real_ages(r)
        if z is None:
            skipped["no_real_zone_age"] += 1
            continue
        u = match(names_of(r["STRAT_UNIT_TOP"]), strict)
        if u is None:
            skipped["top_unit_not_matched_uniquely"] += 1
            continue
        a = asud_age(u)
        if a is None:
            skipped["asud_no_real_age"] += 1
            continue
        recs.append((r["ENO"], r["STATE"], basin(r), z[0], z[1], a[0], a[1], gap_class(gap_of(z[0], z[1], a[0], a[1])), u["NAME"], r["CLASS"] or "(blank)"))
    return recs, skipped


def overlap_of(rec):
    return rec[7] == OVERLAP


for label, strict in (("lenient_most_specific_unique_name", False), ("strict_last_name_only", True)):
    t = f"age_check_top_unit_vs_asud:{label}"
    recs, skipped = top_records(strict)
    add(t, "picks_with_STRAT_UNIT_TOP", "", len(top_rows))
    for k, v in sorted(skipped.items()):
        add(t, "not_checked", k, v)
    add(t, "checked_picks", "", len(recs))
    for cls in (OVERLAP, LE5, LE20, GT20):
        add(t, "picks", cls, sum(r[7] == cls for r in recs))
    add(t, "overlap", "", share(sum(map(overlap_of, recs)), len(recs)))
    if strict:
        continue
    top_recs = recs
    add(t, "boreholes_checked", "", len({r[0] for r in recs}))
    by_class = defaultdict(lambda: [0, 0])
    for r in recs:
        by_class[r[9]][0] += overlap_of(r)
        by_class[r[9]][1] += 1
    for c, (m, n) in sorted(by_class.items(), key=lambda kv: -kv[1][1])[:12]:
        add(t, "overlap_by:CLASS", c, f"{m} of {n}")
    per_hole = defaultdict(list)
    for r in recs:
        per_hole[r[0]].append(overlap_of(r))
    rates = [sum(v) / len(v) for v in per_hole.values()]
    add(t, "per_borehole_overlap_rate_deciles_10_to_90", "", " ".join(f"{q:.2f}" for q in statistics.quantiles(rates, n=10, method="inclusive")))
    add(t, "boreholes_with_all_picks_overlapping", "", share(sum(x == 1 for x in rates), len(rates)))
    add(t, "boreholes_with_under_half_overlapping", "", share(sum(x < 0.5 for x in rates), len(rates)))
    add(t, "boreholes_with_5_or_fewer_checked_picks", "", share(sum(len(v) <= 5 for v in per_hole.values()), len(per_hole)))

t = "age_check_null_reassigned_units"
add(t, "observed_overlap", "all checked picks", share(sum(map(overlap_of, top_recs)), len(top_recs)))
for gname, key in (("all picks", lambda r: 0), ("same state", lambda r: r[1]), ("same basin", lambda r: r[2]), ("same borehole", lambda r: r[0])):
    groups = defaultdict(list)
    for i, r in enumerate(top_recs):
        groups[key(r)].append(i)
    for restrict in (False, True):
        if restrict and gname in ("all picks", "same state", "same basin"):
            continue
        usable = {k: v for k, v in groups.items() if not restrict or len({top_recs[i][8] for i in v}) > 1}
        members = [i for v in usable.values() for i in v]
        rng = random.Random(SEED)
        rates = []
        for _ in range(NULL_REPS):
            hit = 0
            for v in usable.values():
                units = [(top_recs[i][5], top_recs[i][6]) for i in v]
                rng.shuffle(units)
                for i, (o, y) in zip(v, units):
                    hit += gap_of(top_recs[i][3], top_recs[i][4], o, y) == 0
            rates.append(hit / len(members))
        tag = f"{gname}" + (", groups with 2+ distinct units only" if restrict else "")
        obs = sum(overlap_of(top_recs[i]) for i in members)
        add(t, f"reassigned_within:{tag}", "picks | observed | null mean (min-max over 20 shuffles)",
            f"{len(members)} | {100 * obs / len(members):.1f}% | {100 * statistics.mean(rates):.1f}% ({100 * min(rates):.1f}-{100 * max(rates):.1f})")

t = "age_check_top_vs_midpoint_unit"
pairs_checked = []
excluded = Counter()
for r in rows:
    if not (filled(r, "STRAT_UNIT_TOP") and filled(r, "STRAT_UNIT_MIDPOINT")):
        continue
    z = real_ages(r)
    if z is None:
        excluded["no_real_zone_age"] += 1
        continue
    if ";" in r["STRAT_UNIT_TOP"] or ";" in r["STRAT_UNIT_MIDPOINT"]:
        excluded["a_unit_field_lists_several_units"] += 1
        continue
    u1, u2 = match(names_of(r["STRAT_UNIT_TOP"]), False), match(names_of(r["STRAT_UNIT_MIDPOINT"]), False)
    a1, a2 = (asud_age(u) if u else None for u in (u1, u2))
    if a1 is None or a2 is None:
        excluded["a_unit_unmatched_or_without_real_asud_age"] += 1
        continue
    pairs_checked.append((gap_of(z[0], z[1], *a1) == 0, gap_of(z[0], z[1], *a2) == 0, u1 is u2))
add(t, "picks_with_both_unit_fields", "", sum(filled(r, "STRAT_UNIT_TOP") and filled(r, "STRAT_UNIT_MIDPOINT") for r in rows))
for k, v in sorted(excluded.items()):
    add(t, "excluded", k, v)
add(t, "checked_picks", "", len(pairs_checked))
add(t, "overlap_through_STRAT_UNIT_TOP", "", share(sum(p[0] for p in pairs_checked), len(pairs_checked)))
add(t, "overlap_through_STRAT_UNIT_MIDPOINT", "", share(sum(p[1] for p in pairs_checked), len(pairs_checked)))
add(t, "midpoint_unit_is_the_top_unit", "", share(sum(p[2] for p in pairs_checked), len(pairs_checked)))

t = "example_yampi_1_1863m"
for r in rows:
    if r["BOREHOLE_NAME"] == "Yampi 1" and num(r["SAMPLE_DEPTH_M"]) == 1863:
        def unit_ages(field):
            n = names_of(r[field])[-1].lower() if names_of(r[field]) else ""
            return "; ".join(f'{u["NAME"]} {u["NUMERICOLDERAGE"]}-{u["NUMERICYOUNGERAGE"]} Ma' for u in by_name.get(n, [])) or "none"
        add(t, r["STRATDAT_NO"], "zone | HIGH_LOW | class",
            f'{r["ZONE_NAME"]} {r["TOP_AGE_MA"]}-{r["BASE_AGE_MA"]} Ma | {r["HIGH_LOW"]} | {r["CLASS"]}')
        add(t, r["STRATDAT_NO"], "STRAT_UNIT_TOP | ASUD age", f'{r["STRAT_UNIT_TOP"]} | {unit_ages("STRAT_UNIT_TOP")}')
        add(t, r["STRATDAT_NO"], "STRAT_UNIT_MIDPOINT | ASUD age", f'{r["STRAT_UNIT_MIDPOINT"]} | {unit_ages("STRAT_UNIT_MIDPOINT")}')

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
