"""Profile the GBIF fossil-specimen harvest for Australia and Papua New Guinea.

Usage: python3 gbif_fossil_profile.py GBIF_SNAPSHOT PBDB_AU_NG_SNAPSHOT FOSSAHUL_CSV OUT_TSV

Checks the harvest against GBIF's reported counts, dedupes by record key, and
counts records by dataset, licence, taxon, rank, coordinates, geological
context and issue flag; counts Quaternary mammals; compares genera with PBDB's
Australian and New Guinean occurrences and FosSahul's mammals. Collector and
identifier names are not read. Writes long-format (table, metric, key, value).
Standard library only.
"""

import csv
import glob
import json
import os
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
snap, pbdb, fs_csv = sys.argv[1:4]
out = []


def add(*row):
    out.append(row)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def in_au(lat, lon):
    return -45 <= lat <= -10.6 and 112 <= lon <= 155 and not (lon < 121 and lat > -17)


titles = {os.path.basename(p)[9:-5]: load(p) for p in glob.glob(os.path.join(snap, "dataset__*.json"))}
recs = defaultdict(dict)
pages = Counter()
for p in sorted(glob.glob(os.path.join(snap, "??__*__p*.json"))):
    cc = os.path.basename(p)[:2]
    pages[cc] += 1
    for r in load(p)["results"]:
        recs[cc][r["key"]] = r
QUAT = {"Quaternary", "Pleistocene", "Holocene", "UpperPleistocene", "MiddlePleistocene", "LowerPleistocene"}
genera = {}
for cc in sorted(recs):
    rs = list(recs[cc].values())
    facets = load(os.path.join(snap, f"{cc}__datasets.json"))["facets"][0]["counts"]
    skipped = sum(f["count"] for f in facets if "Neptune" in titles[f["name"]].get("title", ""))
    add(cc, "reported_count", "", load(os.path.join(snap, f"{cc}__count.json"))["count"])
    add(cc, "neptune_skipped", "", skipped)
    add(cc, "pages", "", pages[cc])
    add(cc, "unique_records", "", len(rs))
    add(cc, "datasets", "", len({r["datasetKey"] for r in rs}))
    for k, n in Counter(r["datasetKey"] for r in rs).most_common(15):
        d = titles[k]
        add(cc, "by:dataset", f'{d.get("title", k)} [{k}]', n)
    for field in ("publishingCountry", "license", "kingdom", "phylum", "class", "taxonRank", "institutionCode",
                  "earliestEraOrLowestErathem", "earliestPeriodOrLowestSystem", "earliestEpochOrLowestSeries"):
        for v, n in Counter(r.get(field, "(none)") for r in rs).most_common(12):
            add(cc, f"by:{field}", v, n)
    coords = [r for r in rs if "decimalLatitude" in r and "decimalLongitude" in r]
    add(cc, "with_coordinates", "", len(coords))
    if cc == "AU":
        add(cc, "coordinates_outside_sahul_au_box", "", sum(not in_au(r["decimalLatitude"], r["decimalLongitude"]) for r in coords))
    add(cc, "with_any_chronostratigraphy", "", sum(any(k.startswith("earliest") for k in r) for r in rs))
    add(cc, "with_lithostratigraphy", "", sum(any(k in r for k in ("formation", "group", "member", "bed", "lithostratigraphicTerms")) for r in rs))
    add(cc, "with_collection_year", "", sum("year" in r for r in rs))
    add(cc, "species_or_lower", "", sum(r.get("taxonRank") in ("SPECIES", "SUBSPECIES", "VARIETY", "FORM") for r in rs))
    for v, n in Counter(i for r in rs for i in r.get("issues", [])).most_common(10):
        add(cc, "by:issue", v, n)
    qm = [r for r in rs if r.get("class") == "Mammalia" and
          ({r.get("earliestPeriodOrLowestSystem"), r.get("earliestEpochOrLowestSeries"), r.get("latestEpochOrHighestSeries")} & QUAT)]
    add(cc, "quaternary_mammals", "", len(qm))
    for k, n in Counter(r["datasetKey"] for r in qm).most_common(6):
        add(cc, "quaternary_mammals_by:dataset", titles[k].get("title", k), n)
    add(cc, "mammals_without_chronostratigraphy", "", sum(r.get("class") == "Mammalia" and not any(k.startswith("earliest") for k in r) for r in rs))
    genera[cc] = {r["genus"] for r in rs if r.get("genus")}
    genera[cc + "_mammal"] = {r["genus"] for r in rs if r.get("genus") and r.get("class") == "Mammalia"}

with open(os.path.join(pbdb, "occurrences.csv"), newline="", encoding="utf-8") as f:
    occ = list(csv.DictReader(f))
for cc in sorted(recs):
    pg = {r["genus"] for r in occ if r["cc"] == cc and r["genus"]}
    add("cross", "genera_gbif", cc, len(genera[cc]))
    add("cross", "genera_pbdb", cc, len(pg))
    add("cross", "genera_shared", cc, len(genera[cc] & pg))
    add("cross", "genera_gbif_only", cc, len(genera[cc] - pg))
with open(fs_csv, newline="", encoding="utf-8-sig", errors="replace") as f:
    fsg = {r["Genus"].strip() for r in csv.DictReader(f) if r["Class"].strip() == "Mammalia" and r["Genus"].strip()[:1].isupper() and " " not in r["Genus"].strip()}
add("cross", "mammal_genera_gbif_au", "", len(genera["AU_mammal"]))
add("cross", "mammal_genera_fossahul", "", len(fsg))
add("cross", "mammal_genera_shared", "", len(genera["AU_mammal"] & fsg))
add("cross", "mammal_genera_fossahul_only", "", len(fsg - genera["AU_mammal"]))

with open(sys.argv[4], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
