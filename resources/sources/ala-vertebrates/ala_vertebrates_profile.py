"""Profile ALA species-level counts for Australian vertebrates and check them against EPBC's extinct list.

Usage: python3 ala_vertebrates_profile.py ALA_FACETS_SNAPSHOT EXTINCT_SNAPSHOT EPBC_SPECIES_CSV OUT_TSV

For each class: records in all, before 1950, from 1950 and undated; records
not identified to species; species facet entries and species-rank names among
them; species with no dated record from 1950 on. EPBC's extinct species (under
EPBC's current name where it gives one; species-level entries only, so extinct
subspecies of living species are left out) are matched by binomial: how many
ALA holds, their dated and undated records, and, from the EXTINCT_SNAPSHOT
(ala_extinct_specs.py), the basis of record, data resource, decade, state and
raw name of their records from 1950 on. Also NSW BioNet Atlas records of
Perameles fasciata and P. nasuta by year. Writes long-format (table, metric,
key, value). Standard library only.
"""

import csv
import glob
import json
import os
import sys
from collections import Counter

snap, ext_snap, epbc_csv = sys.argv[1:4]
out = []


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def facet(path):
    d = load(path)
    counts = {r["label"]: r["count"] for r in d["facetResults"][0]["fieldResult"]}
    return d["totalRecords"], counts.pop("Not supplied", 0), counts


with open(epbc_csv, newline="", encoding="utf-8-sig") as f:
    extinct, entries = {}, Counter()
    for r in csv.DictReader(f):
        if r["Threatened status"] != "Extinct":
            continue
        entries[r["Class"]] += 1
        name = r["Scientific Name"].strip() if r["Current Scientific Name"].strip() in ("", "-") else r["Current Scientific Name"].strip()
        if len(name.split()) == 2:
            extinct.setdefault(r["Class"], set()).add(name)
for p in sorted(glob.glob(os.path.join(snap, "species_*_all.json"))):
    cls = os.path.basename(p)[8:-9]
    total, nos, allc = facet(p)
    total_pre, _, pre = facet(p.replace("_all.json", "_pre1950.json"))
    total_new, _, new = facet(p.replace("_all.json", "_since1950.json"))
    old = sorted(s for s in allc if s not in new)
    rank = [s for s in allc if len(s.split()) == 2 and " X " not in s and not s.endswith(("sp.", "sp"))]
    out += [(cls, "records", "", total), (cls, "records_pre1950", "", total_pre),
            (cls, "records_since1950", "", total_new), (cls, "records_undated", "", total - total_pre - total_new),
            (cls, "records_not_identified_to_species", "", nos),
            (cls, "species", "", len(allc)), (cls, "species_rank_names", "", len(rank)),
            (cls, "species_with_pre1950_records", "", len(pre)),
            (cls, "species_no_record_since_1950", "", len(old))]
    out += [(cls, "facet_entry_not_species_rank", s, allc[s]) for s in sorted(set(allc) - set(rank))]
    ext = extinct.get(cls, set())
    if ext:
        out += [(cls, "epbc_extinct_entries", "", entries[cls]), (cls, "epbc_extinct_species", "", len(ext)),
                (cls, "epbc_extinct_in_ala", "", len(ext & allc.keys())),
                (cls, "epbc_extinct_not_in_ala", "; ".join(sorted(ext - allc.keys())), len(ext - allc.keys())),
                (cls, "epbc_extinct_no_record_since_1950", "", len(ext & set(old)))]
        out += [(cls, "epbc_extinct_records_since1950", s, new[s]) for s in sorted(ext & new.keys())]
        out += [(cls, "epbc_extinct_no_record_since_1950_pre1950_undated", s, f"{pre.get(s, 0)} {allc[s] - pre.get(s, 0)}")
                for s in sorted(ext & set(old))]
    if cls in ("Mammalia", "Aves"):
        out += [(cls, "no_record_since_1950_not_epbc_extinct", s, allc[s]) for s in old if s not in ext]

cls_of = {s: c for c, names in extinct.items() for s in names}
totals = Counter()
for p in sorted(glob.glob(os.path.join(ext_snap, "extinct__*.json"))):
    sp = os.path.basename(p)[9:-5].replace("_", " ")
    d = load(p)
    out.append(("extinct_since1950", "records", sp, d["totalRecords"]))
    totals[(cls_of[sp], "records", "")] += d["totalRecords"]
    for fr in d["facetResults"]:
        for r in fr["fieldResult"]:
            out.append(("extinct_since1950", f"{fr['fieldName']}", f"{sp} | {r['label']}", r["count"]))
            if fr["fieldName"] in ("basis_of_record", "dataResourceName", "decade"):
                totals[(cls_of[sp], fr["fieldName"], r["label"])] += r["count"]
out += [("extinct_since1950", f"{c}_all_species_by:{k}" if k != "records" else f"{c}_records", v, n)
        for (c, k, v), n in sorted(totals.items(), key=lambda x: (x[0][0], x[0][1], -x[1]))]
for p in sorted(glob.glob(os.path.join(ext_snap, "bionet__*.json"))):
    sp = os.path.basename(p)[8:-5].replace("_", " ")
    for r in sorted(load(p)["facetResults"][0]["fieldResult"], key=lambda r: r["label"]):
        out.append(("bionet_by_year", sp, r["label"], r["count"]))

with open(sys.argv[4], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
