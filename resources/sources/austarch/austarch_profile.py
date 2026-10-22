"""Profile the AustArch CSV (ADS deposit, 28 Nov 2013 merge).

Usage: python3 austarch_profile.py AUSTARCH_CSV OUT_TSV

Writes long-format counts (metric, key, value). Standard library only.
"""

import csv
import re
import sys
from collections import Counter

rows = list(csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8-sig")))
out = []


def add(metric, key, value):
    out.append((metric, key, value))


def tab(metric, values, n=20):
    for k, v in Counter(values).most_common(n):
        add(metric, k, v)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


add("rows", "", len(rows))
add("distinct_ADSID", "", len({r["ADSID"] for r in rows}))
add("distinct_sites", "", len({r["SITE"].strip() for r in rows}))
add("distinct_IBRA_regions", "", len({r["IBRA_REGION"].strip() for r in rows if r["IBRA_REGION"].strip()}))
for col in ["METHOD", "RECORD_SOURCE", "MATERIAL_TOP_LEVEL", "SITE_TYPE", "AGE_NORM",
            "Data pertinent for time-series analysis or calibration", "Open or Closed Site",
            "Directly Related to occupation? Yes/Unknown"]:
    tab(f"by:{col}", [r[col].strip() for r in rows])
tab("by:DATE_ISSUES (first 40 chars)", [r["DATE_ISSUES"].strip()[:40] for r in rows], 10)
ages = [r["AGE"].strip() for r in rows]
add("ages_numeric", "", sum(num(a) is not None for a in ages))
add("ages_with_inequality_or_qualifier", "", sum(bool(re.match(r"^[<>~c]", a)) for a in ages))
tab("age_nonnumeric_examples", [a for a in ages if num(a) is None], 10)
lat = [r["LATITUDE"].strip() for r in rows]
add("coordinates_numeric", "", sum(num(x) is not None for x in lat))
tab("latitude_decimals", [len(x.split(".")[1]) if "." in x else 0 for x in lat if num(x) is not None])
c14 = [num(r["AGE"]) for r in rows if r["METHOD"] == "Radiocarbon" and num(r["AGE"]) is not None]
add("radiocarbon_age_range_bp", "", f"{min(c14)} to {max(c14)}")
add("radiocarbon_older_than_10000_bp", "", sum(a > 10000 for a in c14))
add("radiocarbon_older_than_30000_bp", "", sum(a > 30000 for a in c14))
with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["metric", "key", "value"])
    w.writerows(out)
