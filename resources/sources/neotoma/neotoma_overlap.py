"""Compare the Neotoma IPPD/Sahul snapshot with OCTOPUS's IPPD copy and PBDB's Quaternary plant records.

Usage: python3 neotoma_overlap.py NEOTOMA_DATASETS_TSV OCTOPUS_IPPD_DIR PBDB_SNAPSHOT_DIR OUT_TSV

NEOTOMA_DATASETS_TSV is the per-dataset table from neotoma_profile.py.
OCTOPUS side: ippd_datasets.csv and ippd_baseline_pollen.csv, joined to Neotoma
by NEO_SITEID. PBDB side: core occurrences of plants (Angiospermae, Gymnospermae,
Pteridophyta and allied phyla) with interval midpoint under 2.58 Ma, matched to
Neotoma Sahul pollen sites within 5 km. Standard library only.
"""

import csv
import math
import os
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
PLANTS = {"Angiospermae", "Gymnospermae", "Pteridophyta", "Equisetophyta", "Lycopodiophyta", "Spermatophyta", "Bryophyta"}
out = []


def add(*row):
    out.append(row)


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    neo = list(csv.DictReader(f, delimiter="\t"))
sah = [r for r in neo if r["region"] not in ("outside", "no_coordinates")]
pollen = [r for r in sah if r["datasettype"] == "pollen"]
with open(os.path.join(sys.argv[2], "ippd_datasets.csv"), newline="", encoding="utf-8") as f:
    oc = list(csv.DictReader(f))
add("octopus", "datasets", "", len(oc))
for k, v in Counter(r["DATSETTYPE"] for r in oc).most_common(6):
    add("octopus", "datasets_by:type", k, v)
oc_sites = {r["NEO_SITEID"].strip() for r in oc if r["NEO_SITEID"].strip()}
add("octopus", "datasets_without_neo_siteid", "", sum(not r["NEO_SITEID"].strip() for r in oc))
neo_sites = {r["siteid"] for r in neo}
add("octopus", "neo_siteids_not_in_neotoma_snapshot", "", len(oc_sites - neo_sites))
pollen_sites = {r["siteid"] for r in pollen}
add("neotoma_sahul_pollen", "sites", "", len(pollen_sites))
add("neotoma_sahul_pollen", "sites_in_octopus", "", len(pollen_sites & oc_sites))
add("neotoma_sahul_pollen", "sites_not_in_octopus", "", len(pollen_sites - oc_sites))
add("neotoma_sahul", "surface_sample_datasets", "", sum(r["datasettype"] == "pollen surface sample" for r in sah))
add("octopus", "surface_sample_datasets", "", sum("surface" in r["DATSETTYPE"] for r in oc))
with open(os.path.join(sys.argv[2], "ippd_baseline_pollen.csv"), newline="", encoding="utf-8") as f:
    base = list(csv.DictReader(f))
add("octopus_baseline", "rows", "", len(base))
for k, v in Counter(r["AGETYPE"] for r in base).most_common(6):
    add("octopus_baseline", "rows_by:AGETYPE", k, v)
for k, v in Counter(r["AGEMODEL"] for r in base).most_common(8):
    add("octopus_baseline", "rows_by:AGEMODEL", k, v)

with open(os.path.join(sys.argv[3], "occurrences.csv"), newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    h = next(rd)
    ix = {k: h.index(k) for k in ("collection_no", "collection_name", "phylum", "lat", "lng", "max_ma", "min_ma")}
    cols = {}
    for r in rd:
        try:
            mid = (float(r[ix["max_ma"]]) + float(r[ix["min_ma"]])) / 2
        except ValueError:
            continue
        if r[ix["phylum"]] in PLANTS and mid < 2.58:
            c = cols.setdefault(r[ix["collection_no"]], {"p": (float(r[ix["lat"]]), float(r[ix["lng"]])), "name": r[ix["collection_name"]], "n": 0})
            c["n"] += 1
pts = {r["siteid"]: (float(r["lat"]), float(r["lon"])) for r in pollen}
add("pbdb_quaternary_plants", "collections", "", len(cols))
add("pbdb_quaternary_plants", "occurrences", "", sum(c["n"] for c in cols.values()))
near = {k: c for k, c in cols.items() if any(km(c["p"], q) <= 5 for q in pts.values())}
add("pbdb_quaternary_plants", "collections_within_5km_of_neotoma_pollen_site", "", len(near))
add("pbdb_quaternary_plants", "occurrences_within_5km_of_neotoma_pollen_site", "", sum(c["n"] for c in near.values()))
for name, n in Counter(c["name"].split(" ")[0] for c in near.values()).most_common(8):
    add("pbdb_quaternary_plants", "near_collections_by_first_word", name, n)

with open(sys.argv[4], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
