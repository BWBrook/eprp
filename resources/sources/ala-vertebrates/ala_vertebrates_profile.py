"""Profile ALA species-level counts for Australian vertebrates and check them against EPBC's extinct list.

Usage: python3 ala_vertebrates_profile.py ALA_FACETS_SNAPSHOT EPBC_SPECIES_CSV OUT_TSV

For each class: records in all, before 1950, from 1950 and undated; species
with records; species with no record from 1950 on. EPBC's extinct species
(under EPBC's current name where it gives one; species-level entries only,
so extinct subspecies of living species are left out) are matched by binomial to show how many ALA holds and how many have
records from 1950 on, with those records' counts. Writes long-format (table,
metric, key, value). Standard library only.
"""

import csv
import glob
import json
import os
import sys

snap, epbc_csv = sys.argv[1:3]
out = []


def facet(path):
    with open(path, encoding="utf-8") as f:
        d = json.load(f)
    counts = {r["label"]: r["count"] for r in d["facetResults"][0]["fieldResult"] if r["label"] != "Not supplied"}
    return d["totalRecords"], counts


with open(epbc_csv, newline="", encoding="utf-8-sig") as f:
    extinct = {}
    for r in csv.DictReader(f):
        name = r["Scientific Name"].strip() if r["Current Scientific Name"].strip() in ("", "-") else r["Current Scientific Name"].strip()
        if r["Threatened status"] == "Extinct" and len(name.split()) == 2:
            extinct.setdefault(r["Class"], set()).add(name)
for p in sorted(glob.glob(os.path.join(snap, "species_*_all.json"))):
    cls = os.path.basename(p)[8:-9]
    total, allc = facet(p)
    total_pre, pre = facet(p.replace("_all.json", "_pre1950.json"))
    total_new, new = facet(p.replace("_all.json", "_since1950.json"))
    old = sorted(s for s in allc if s not in new)
    out += [(cls, "records", "", total), (cls, "records_pre1950", "", total_pre),
            (cls, "records_since1950", "", total_new), (cls, "records_undated", "", total - total_pre - total_new),
            (cls, "species", "", len(allc)), (cls, "species_with_pre1950_records", "", len(pre)),
            (cls, "species_no_record_since_1950", "", len(old))]
    ext = extinct.get(cls, set())
    if ext:
        out += [(cls, "epbc_extinct_species", "", len(ext)),
                (cls, "epbc_extinct_in_ala", "", len(ext & allc.keys())),
                (cls, "epbc_extinct_no_record_since_1950", "", len(ext & set(old)))]
        out += [(cls, "epbc_extinct_records_since1950", s, new[s]) for s in sorted(ext & new.keys())]
    if cls in ("Mammalia", "Aves"):
        out += [(cls, "no_record_since_1950_not_epbc_extinct", s, allc[s]) for s in old if s not in ext]

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
