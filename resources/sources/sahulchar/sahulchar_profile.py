"""Profile a SahulCHAR snapshot from OCTOPUS (sahulchar.csv observations, sahulchar_units.csv cores).

Usage: python3 sahulchar_profile.py SNAPSHOT_DIR OUT_TSV

Sahul regions as in rpd_profile.py; everything else (New Zealand, Pacific) is
"outside". Writes long-format counts (table, metric, key, value). Standard
library only.
"""

import csv
import os
import statistics
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
MISSING = {"-9999.99", "-9999", "ND", "NA", ""}
out = []


def add(*row):
    out.append(row)


def num(x):
    if x is None or x.strip() in MISSING:
        return None
    try:
        return float(x)
    except ValueError:
        return None


def region(lat, lon):
    if lat is None or lon is None:
        return "no_coordinates"
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if lat <= -10.6 and 112 <= lon <= 155:
        return "australia"
    if 130.8 <= lon <= 156 and -12 <= lat <= 0:
        return "new_guinea"
    return "outside"


def load(name):
    with open(os.path.join(sys.argv[1], name), newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


units, obs = load("sahulchar_units.csv"), load("sahulchar.csv")
for t, rows in (("units", units), ("observations", obs)):
    add(t, "rows", "", len(rows))
    for k, v in Counter(r["DBVERNO"] for r in rows).most_common():
        add(t, "by:DBVERNO", k, v)
reg = {u["UNITID"]: region(num(u["Y_WGS84"]), num(u["X_WGS84"])) for u in units}
add("units", "n_char_rec_sum", "", sum(int(u["N_CHAR_REC"] or 0) for u in units))
add("units", "metasites", "", len({u["METASITEID"] for u in units}))
for k, v in Counter(reg.values()).most_common():
    add("units", "by:region", k, v)
for col in ("CNTRY", "UNITTYPE", "DEPOSIT", "COL_MTD"):
    for k, v in Counter(u[col] for u in units).most_common(10):
        add("units", f"by:{col}", k, v)
sah = [u for u in units if reg[u["UNITID"]] not in ("outside", "no_coordinates")]
add("sahul_units", "rows", "", len(sah))
add("sahul_units", "n_char_rec_sum", "", sum(int(u["N_CHAR_REC"] or 0) for u in sah))
add("sahul_units", "with_neotoma_site_id", "", sum(bool(u["NEO_SITEID"].strip()) for u in sah))
add("sahul_units", "with_n_char_rec_zero", "", sum((u["N_CHAR_REC"] or "0") == "0" for u in sah))
ages = [num(u["MAXAGE"]) for u in sah if num(u["MAXAGE"]) is not None]
add("sahul_units", "with_maxage", "", len(ages))
add("sahul_units", "maxage_median", "", round(statistics.median(ages)))
for thr in (20000, 50000, 130000):
    add("sahul_units", "maxage_ge", thr, sum(a >= thr for a in ages))
for k, v in Counter(u["DEPOSIT"] for u in sah if (num(u["MAXAGE"]) or 0) >= 130000).most_common(5):
    add("sahul_units", "maxage_ge_130000_by:DEPOSIT", k, v)
years = [int(u["PUBYEAR"]) for u in sah if u["PUBYEAR"].isdigit()]
add("sahul_units", "pubyear_range", "", f"{min(years)} to {max(years)}")

ids = {u["UNITID"] for u in sah}
so = [o for o in obs if o["UNITID"] in ids]
add("sahul_observations", "rows", "", len(so))
for k, v in Counter(o["WHATAMI"] for o in so).most_common(10):
    add("sahul_observations", "by:WHATAMI", k, v)
char = [o for o in so if o["WHATAMI"] != "age"]
age = [o for o in so if o["WHATAMI"] == "age"]
for col in ("CHARMETHOD", "CHARMEAS", "DATASOURCE"):
    for k, v in Counter(o[col] for o in char).most_common(10):
        add("sahul_char", f"by:{col}", k, v)
add("sahul_char", "charvalue_missing", "", sum(num(o["CHARVALUES"]) is None for o in char))
add("sahul_char", "est_age_missing", "", sum(num(o["EST_AGE"]) is None for o in char))
for col in ("AGETYPE", "METHOD", "CALCURVE"):
    for k, v in Counter(o[col] for o in age).most_common(8):
        add("sahul_ages", f"by:{col}", k, v)

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
