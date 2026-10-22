"""Profile an ASUD WFS snapshot (stratunit:StratigraphicUnit CSV written by data_mirror.py wfs).

Usage: python3 asud_profile.py STRATIGRAPHICUNIT_CSV PBDB_INTERVALS_CSV OUT_TSV

Writes long-format counts (table, metric, key, value): ranks, unit types, states,
age coverage, hierarchy fields, duplicate names and placeholder ages. Checks the
numeric ages against the unit's own text age (GEOLOGICHISTORY, e.g. "Barremian -
Albian"), read through the PBDB interval table plus the series names it lacks
("Late Permian", "Early Silurian"), in either order. Inverted numeric ranges are
counted, then swapped. A unit is disjoint when its numeric range does not overlap
the named range at all; a stricter test asks that it lie within the named range
widened by max(5%, 1 Myr). Standard library only.
"""

import csv
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
out = []


def add(*row):
    out.append(row)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))
ages = {"recent": (0.0, 0.0)}
with open(sys.argv[2], newline="", encoding="utf-8") as f:
    for r in sorted(csv.DictReader(f), key=lambda r: r["scale_no"] != "1"):
        ages.setdefault(r["interval_name"].lower(), (float(r["b_age"]), float(r["t_age"])))
for name, (older, younger) in {"early permian": ("cisuralian", "cisuralian"), "middle permian": ("guadalupian", "guadalupian"),
                               "late permian": ("lopingian", "lopingian"), "early silurian": ("llandovery", "wenlock"),
                               "late silurian": ("ludlow", "pridoli")}.items():
    ages.setdefault(name, (ages[older][0], ages[younger][1]))
t = "units"
add(t, "rows", "", len(rows))
add(t, "distinct_stratno", "", len({r["STRATNO"] for r in rows}))
for k in ("RANK", "GEOLOGICUNITTYPE", "REPRESENTATIVEAGE_CLASS", "OBSERVATIONMETHOD", "OLDERAGE", "YOUNGERAGE"):
    for v, n in Counter(r[k] for r in rows).most_common(15):
        add(t, f"by:{k}", v, n)
for v, n in Counter(r["STATE"] for r in rows).most_common(20):
    add(t, "by:STATE", v, n)
add(t, "with_numeric_ages", "", sum(num(r["NUMERICOLDERAGE"]) is not None for r in rows))
add(t, "with_description", "", sum(bool(r["DESCRIPTION"].strip()) for r in rows))
add(t, "with_geologic_history", "", sum(bool(r["GEOLOGICHISTORY"].strip()) for r in rows))
add(t, "older_lt_younger", "", sum(num(r["NUMERICOLDERAGE"]) is not None and num(r["NUMERICYOUNGERAGE"]) is not None
                                   and num(r["NUMERICOLDERAGE"]) < num(r["NUMERICYOUNGERAGE"]) for r in rows))
for k in ("SUPERGROUP", "GROUPNAME", "SUBGROUP", "FORMATION", "MEMBER", "BED"):
    add(t, "with_hierarchy_field", k, sum(bool(r[k]) for r in rows))
names = Counter(r["NAME"].strip().lower() for r in rows)
add(t, "duplicate_names", "", sum(v > 1 for v in names.values()))
add(t, "numeric_ages_0_0", "", sum(num(r["NUMERICOLDERAGE"]) == 0 and num(r["NUMERICYOUNGERAGE"]) == 0 for r in rows))
for v, n in Counter(r["GEOLOGICHISTORY"] for r in rows if num(r["NUMERICOLDERAGE"]) == 0 and num(r["NUMERICYOUNGERAGE"]) == 0).most_common(5):
    add(t, "numeric_ages_0_0_by_text_age", v, n)
for v, n in Counter(r["NUMERICOLDERAGE"] for r in rows if (num(r["NUMERICOLDERAGE"]) or 0) >= 4000).most_common(5):
    add(t, "numeric_older_age_ge_4000_ma", v, n)
for b in ("66", "251.902", "538.8", "1000", "1600", "2500"):
    for v, n in Counter(r["OLDERAGE"] for r in rows if r["NUMERICOLDERAGE"] == b).most_common(3):
        add(t, "older_era_label_at_boundary", f"{b} Ma", f"{v} {n}")
check, bad = Counter(), []
for r in rows:
    old, yng = num(r["NUMERICOLDERAGE"]), num(r["NUMERICYOUNGERAGE"])
    parts = [p.strip().lower() for p in r["GEOLOGICHISTORY"].split(" - ")]
    if old is None or yng is None or (old == 0 and yng == 0) or old >= 4000:
        check["no_real_numeric_age"] += 1
        continue
    if not r["GEOLOGICHISTORY"].strip():
        check["no_text_age"] += 1
        continue
    if not all(p in ages for p in parts):
        check["text_age_not_resolved"] += 1
        continue
    if old < yng:
        check["inverted_then_swapped"] += 1
        old, yng = yng, old
    named_old = max(ages[p][0] for p in parts)
    named_yng = min(ages[p][1] for p in parts)
    tol = max(0.05 * (named_old - named_yng), 1.0)
    if yng > named_old or old < named_yng:
        check["numeric_disjoint_from_text_age"] += 1
        bad.append((max(yng - named_old, named_yng - old), r))
    elif old > named_old + tol or yng < named_yng - tol:
        check["numeric_overlaps_but_extends_beyond_text_age"] += 1
    else:
        check["numeric_within_text_age"] += 1
for k, v in sorted(check.items()):
    add(t, "text_vs_numeric_age", k, v)
for lo, hi in ((0, 1), (1, 5), (5, 20), (20, 1e9)):
    add(t, "disjoint_gap_myr", f"{lo}-{hi if hi < 1e9 else 'more'}", sum(lo < g <= hi or (lo == 0 and g == 0) for g, _ in bad))
for gap, r in sorted(bad, key=lambda x: -x[0])[:25]:
    add(t, "disjoint_example", r["STRATNO"], f'{r["NAME"]} | {r["STATE"]} | text {r["GEOLOGICHISTORY"]} | numeric {r["NUMERICOLDERAGE"]}-{r["NUMERICYOUNGERAGE"]} Ma | gap {gap:.1f} Myr')

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
