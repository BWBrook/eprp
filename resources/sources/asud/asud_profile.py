"""Profile an ASUD WFS snapshot (stratunit:StratigraphicUnit CSV written by data_mirror.py wfs).

Usage: python3 asud_profile.py STRATIGRAPHICUNIT_CSV PBDB_INTERVALS_CSV OUT_TSV

Writes long-format counts (table, metric, key, value): ranks, unit types, states,
age coverage, hierarchy fields and duplicate names. Checks the numeric ages against
the unit's own text age (GEOLOGICHISTORY, e.g. "Barremian - Albian"), read through
the PBDB interval table: a unit is inconsistent when its numeric range does not
overlap the named range at all. Standard library only.
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
check, bad = Counter(), []
for r in rows:
    old, yng = num(r["NUMERICOLDERAGE"]), num(r["NUMERICYOUNGERAGE"])
    parts = [p.strip().lower() for p in r["GEOLOGICHISTORY"].split(" - ")]
    if old is None or yng is None or (old == 0 and yng == 0):
        check["no_numeric_age"] += 1
        continue
    if not all(p in ages for p in parts):
        check["text_age_not_in_interval_table"] += 1
        continue
    named_old, named_yng = ages[parts[0]][0], ages[parts[-1]][1]
    if yng > named_old or old < named_yng:
        check["numeric_disjoint_from_text_age"] += 1
        bad.append((max(yng - named_old, named_yng - old), r))
    else:
        check["numeric_overlaps_text_age"] += 1
for k, v in sorted(check.items()):
    add(t, "text_vs_numeric_age", k, v)
for gap, r in sorted(bad, key=lambda x: -x[0])[:25]:
    add(t, "disjoint_example", r["STRATNO"], f'{r["NAME"]} | {r["STATE"]} | text {r["GEOLOGICHISTORY"]} | numeric {r["NUMERICOLDERAGE"]}-{r["NUMERICYOUNGERAGE"]} Ma | gap {gap:.1f} Myr')

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
