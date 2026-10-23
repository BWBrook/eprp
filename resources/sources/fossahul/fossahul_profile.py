"""Profile a FosSahul CSV (one row per dated record).

Usage: python3 fossahul_profile.py FOSSAHUL_CSV OUT_TSV

Writes long-format counts (metric, key, value): records, taxa, sites, dating
techniques, quality ratings, age types, calibration flags, associations,
regions, coordinate precision and uncertainty, and age ranges by technique.
Standard library only.
"""

import csv
import re
import statistics
import sys
from collections import Counter

def rnames(name):
    # The 2019 CSV has raw headers ("Cave/Site/Deposit"); the 2021 one has R's make.names() forms.
    return re.sub(r"[^A-Za-z0-9_]", ".", name)


rows = [{rnames(k): v for k, v in r.items()} for r in csv.DictReader(open(sys.argv[1], newline="", encoding="utf-8-sig"))]
out = []


def add(metric, key, value):
    out.append((metric, key, value))


def tab(metric, values):
    for k, n in sorted(Counter(values).items(), key=lambda kv: (-kv[1], str(kv[0]))):
        add(metric, k, n)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def decimals(x):
    x = (x or "").strip()
    return len(x.split(".")[1]) if "." in x else 0


add("records", "", len(rows))
add("columns", "", len(rows[0]))
add("distinct_ID", "", len({r["ID"] for r in rows}))
add("distinct_AgeID", "", len({r["AgeID"] for r in rows}))
add("records_sharing_AgeID_with_another", "", sum(n for n in Counter(r["AgeID"] for r in rows).values() if n > 1))
taxa = {(r["Genus"].strip(), r["Species"].strip()) for r in rows}
add("distinct_genus_species", "", len(taxa))
add("distinct_genera", "", len({r["Genus"].strip() for r in rows}))
sites = {(r["Cave.Site.Deposit"].strip(), r["Latitude"], r["Longitude"]) for r in rows}
add("distinct_site_name_coordinate_pairs", "", len(sites))
add("distinct_site_names", "", len({r["Cave.Site.Deposit"].strip() for r in rows}))
add("distinct_coordinates", "", len({(r["Latitude"], r["Longitude"]) for r in rows}))
for col in ["Class", "Status", "Megafauna..40kg.", "DatingTechnique", "Calibration", "AgeType", "PrecisionType",
            "Association", "Quality", "preQuality", "OverallRegion", "AdministrativeDivision", "DatedRemain"]:
    if col in rows[0]:
        tab(f"records_by:{col}", [r[col].strip() for r in rows])
tab("records_by:Quality_x_Megafauna", [f"{r['Quality'].strip()}|{r['Megafauna..40kg.'].strip()}" for r in rows])
tab("records_by:Technique_x_Quality", [f"{r['DatingTechnique'].strip()}|{r['Quality'].strip()}" for r in rows])
tab("coordinate_decimals:Latitude", [decimals(r["Latitude"]) for r in rows])
tab("coordinate_decimals:Longitude", [decimals(r["Longitude"]) for r in rows])
unc = [num(r.get("Uncertainty")) for r in rows if num(r.get("Uncertainty")) is not None]
add("uncertainty_nonmissing", "", len(unc))
if unc:
    add("uncertainty_min", "", min(unc))
    add("uncertainty_median", "", statistics.median(unc))
    add("uncertainty_max", "", max(unc))
lat = [num(r["Latitude"]) for r in rows if num(r["Latitude"]) is not None]
lon = [num(r["Longitude"]) for r in rows if num(r["Longitude"]) is not None]
add("latitude_range", "", f"{min(lat)} to {max(lat)}")
add("longitude_range", "", f"{min(lon)} to {max(lon)}")
for tech in sorted({r["DatingTechnique"].strip() for r in rows}):
    ages = [num(r["Age"]) for r in rows if r["DatingTechnique"].strip() == tech and num(r["Age"]) is not None]
    if ages:
        add("age_ka_range_by_technique", tech, f"{min(ages)} to {max(ages)} (n={len(ages)}, median {statistics.median(ages)})")
ages = [num(r["Age"]) for r in rows if num(r["Age"]) is not None]
add("age_nonnumeric", "", len(rows) - len(ages))
tab("age_ka_bins", ["<12" if a < 12 else "12-30" if a < 30 else "30-50" if a < 50 else "50-130" if a < 130 else
                    "130-500" if a < 500 else ">=500" for a in ages])
years = [int(r.get("Year", "")) for r in rows if r.get("Year", "").strip().isdigit()]
add("publication_year_range", "", f"{min(years)} to {max(years)}")
add("records_with_quality_reason", "", sum(bool(r.get("QualityReason", "").strip()) for r in rows))

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["metric", "key", "value"])
    w.writerows(out)
