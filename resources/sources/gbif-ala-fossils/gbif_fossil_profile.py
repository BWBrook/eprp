"""Profile the GBIF fossil-specimen harvest for Australia and Papua New Guinea.

Usage: python3 gbif_fossil_profile.py GBIF_SNAPSHOT BASIS_SNAPSHOT PBDB_AU_NG_SNAPSHOT FOSSAHUL_CSV OUT_TSV

Reconciles the harvest with GBIF's reported counts (exit status 1 on a
mismatch), dedupes by record key, and counts records by dataset, licence,
taxon, rank, institution, geological time, lithostratigraphy, coordinates and
issue flag. Describes the Quaternary mammals (a Quaternary period, or a
Pleistocene or Holocene earliest or latest epoch) and UCMP's share of them,
the PANGAEA data publications, records outside the Australian region and
placeholder coordinates. Reads the basis-of-record check (gbif_basis_specs.py).
Compares genera with PBDB's Australian and New Guinean occurrences (strict and
widened name sets) and Australian mammal genera with FosSahul's rows in the
Australian region. Collector and identifier names are not read. Writes
long-format (table, metric, key, value). Standard library only.
"""

import csv
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
snap, basis, pbdb, fs_csv = sys.argv[1:5]
out = []
UCMP = "58d0f326-2e85-4d0a-a744-571461220f00"
QUAT = {"Quaternary", "Pleistocene", "Holocene"}


def add(*row):
    out.append(row)


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def in_au(lat, lon):
    mainland = -45 <= lat <= -10.6 and 112 <= lon <= 155 and not (lon < 121 and lat > -17)
    return mainland or (-10.6 <= lat <= -9 and 141 <= lon <= 144.5)


def counts(cc, metric, values, n=None):
    for v, k in Counter(values).most_common(n):
        add(cc, metric, v, k)


def chrono(r, sides=("earliest", "latest")):
    return any(k.startswith(sides) for k in r)


def quaternary(r):
    return bool({r.get("earliestPeriodOrLowestSystem"), r.get("earliestEpochOrLowestSeries"), r.get("latestEpochOrHighestSeries")} & QUAT)


titles = {os.path.basename(p)[9:-5]: load(p) for p in glob.glob(os.path.join(snap, "dataset__*.json"))}
recs = defaultdict(dict)
pages, rows = Counter(), Counter()
for p in sorted(glob.glob(os.path.join(snap, "??__*__p*.json"))):
    cc = os.path.basename(p)[:2]
    pages[cc] += 1
    for r in load(p)["results"]:
        rows[cc] += 1
        recs[cc][r["key"]] = r
mismatch = False
genera, mammal_genera, quat_mammal_genera = {}, {}, {}
for cc in sorted(recs):
    rs = list(recs[cc].values())
    facets = load(os.path.join(snap, f"{cc}__datasets.json"))["facets"][0]["counts"]
    skipped = sum(f["count"] for f in facets if "Neptune" in titles[f["name"]].get("title", ""))
    reported = load(os.path.join(snap, f"{cc}__count.json"))["count"]
    add(cc, "reported_count", "", reported)
    add(cc, "neptune_skipped", "", skipped)
    add(cc, "pages", "", pages[cc])
    add(cc, "rows_fetched", "", rows[cc])
    add(cc, "unique_records", "", len(rs))
    ok = len(rs) == reported - skipped
    mismatch |= not ok
    add(cc, "reconciled", "", "yes" if ok else "NO")
    add(cc, "datasets", "", len({r["datasetKey"] for r in rs}))
    for k, n in Counter(r["datasetKey"] for r in rs).most_common(15):
        add(cc, "by:dataset", f'{titles[k].get("title", k)} [{k}]', n)
    for field in ("publishingCountry", "license", "kingdom", "phylum", "taxonRank", "institutionCode",
                  "earliestEraOrLowestErathem", "earliestPeriodOrLowestSystem", "earliestEpochOrLowestSeries"):
        counts(cc, f"by:{field}", (r.get(field, "(none)") for r in rs), 12)
    counts(cc, "by:class", (r.get("class", "(none)") for r in rs), 20)
    pang = [r for r in rs if r.get("institutionCode") == "Pangaea"]
    add(cc, "pangaea_records", "", len(pang))
    add(cc, "pangaea_datasets", "", len({r["datasetKey"] for r in pang}))
    counts(cc, "pangaea_by:class", (r.get("class", "(none)") for r in pang), 5)
    add(cc, "individualCount_sum", "", sum(r.get("individualCount", 0) for r in rs))
    coords = [r for r in rs if "decimalLatitude" in r and "decimalLongitude" in r]
    add(cc, "with_coordinates", "", len(coords))
    add(cc, "placeholder_coordinates_-9_-9", "", sum(r["decimalLatitude"] == -9 and r["decimalLongitude"] == -9 for r in coords))
    if cc == "AU":
        outside = [r for r in coords if not in_au(r["decimalLatitude"], r["decimalLongitude"])]
        add(cc, "coordinates_outside_sahul_au_region", "", len(outside))
        add(cc, "outside_with_COUNTRY_DERIVED_FROM_COORDINATES", "", sum("COUNTRY_DERIVED_FROM_COORDINATES" in r.get("issues", []) for r in outside))
        counts(cc, "outside_by:dataset", (titles[r["datasetKey"]].get("title", r["datasetKey"]) for r in outside), 6)
    add(cc, "with_earliest_chronostratigraphy", "", sum(chrono(r, ("earliest",)) for r in rs))
    add(cc, "with_any_chronostratigraphy", "", sum(chrono(r) for r in rs))
    add(cc, "with_formation_group_member_bed", "", sum(any(k in r for k in ("formation", "group", "member", "bed")) for r in rs))
    add(cc, "with_lithostratigraphy_incl_terms", "", sum(any(k in r for k in ("formation", "group", "member", "bed", "lithostratigraphicTerms")) for r in rs))
    add(cc, "with_collection_year", "", sum("year" in r for r in rs))
    add(cc, "species_or_lower", "", sum(r.get("taxonRank") in ("SPECIES", "SUBSPECIES", "VARIETY", "FORM") for r in rs))
    counts(cc, "by:issue", (i for r in rs for i in r.get("issues", [])), 15)
    mam = [r for r in rs if r.get("class") == "Mammalia"]
    qm = [r for r in mam if quaternary(r)]
    add(cc, "homo_sapiens_records", "", sum(r.get("species") == "Homo sapiens" for r in rs))
    for label, sub in (("quaternary_mammals", qm), ("quaternary_mammals_ucmp", [r for r in qm if r["datasetKey"] == UCMP])):
        add(cc, label, "", len(sub))
        add(cc, f"{label}_with_coordinates", "", sum("decimalLatitude" in r for r in sub))
        add(cc, f"{label}_with_formation", "", sum("formation" in r for r in sub))
        add(cc, f"{label}_with_genus", "", sum("genus" in r for r in sub))
        add(cc, f"{label}_individualCount_sum", "", sum(r.get("individualCount", 0) for r in sub))
        add(cc, f"{label}_without_individualCount", "", sum("individualCount" not in r for r in sub))
        add(cc, f"{label}_homo_sapiens", "", sum(r.get("species") == "Homo sapiens" for r in sub))
        counts(cc, f"{label}_by:taxonRank", (r.get("taxonRank", "(none)") for r in sub))
        counts(cc, f"{label}_by:stateProvince", (r.get("stateProvince", "(none)") for r in sub), 8)
        counts(cc, f"{label}_by:formation", (r.get("formation", "(none)") for r in sub), 8)
    add(cc, "quaternary_mammals_only_via_latestEpoch", "", sum(r.get("earliestPeriodOrLowestSystem") not in QUAT and r.get("earliestEpochOrLowestSeries") not in QUAT for r in qm))
    counts(cc, "quaternary_mammals_by:dataset", (titles[r["datasetKey"]].get("title", r["datasetKey"]) for r in qm), 6)
    nochron = [r for r in mam if not chrono(r)]
    add(cc, "mammals_without_chronostratigraphy", "", len(nochron))
    counts(cc, "mammals_without_chronostratigraphy_by:dataset", (titles[r["datasetKey"]].get("title", r["datasetKey"]) for r in nochron), 6)
    ucmp = [r for r in rs if r["datasetKey"] == UCMP]
    counts(cc, "ucmp_by:stateProvince", (r.get("stateProvince", "(none)") for r in ucmp), 8)
    counts(cc, "ucmp_by:formation", (r.get("formation", "(none)") for r in ucmp), 12)
    genera[cc] = {r["genus"] for r in rs if r.get("genus")}
    genera[cc + "_wide"] = genera[cc] | {r[k] for r in rs for k in ("genericName",) if r.get(k)} | \
        {r["scientificName"].split()[0] for r in rs if r.get("scientificName")}
    mammal_genera[cc] = {r["genus"] for r in mam if r.get("genus")}
    quat_mammal_genera[cc] = {r["genus"] for r in qm if r.get("genus")}

for p in sorted(glob.glob(os.path.join(basis, "*.json"))):
    if not p.endswith("MANIFEST.json"):
        d = load(p)
        add("basis_check", "count", os.path.basename(p)[:-5], d["count"])
        for f in d.get("facets", []):
            for x in f["counts"]:
                key = titles[x["name"]].get("title", x["name"]) if f["field"] == "DATASET_KEY" and x["name"] in titles else x["name"]
                add("basis_check", f'{os.path.basename(p)[:-5]}_by:{f["field"]}', key, x["count"])

with open(os.path.join(pbdb, "occurrences.csv"), newline="", encoding="utf-8") as f:
    occ = list(csv.DictReader(f))
for cc in sorted(recs):
    pg = {r["genus"] for r in occ if r["cc"] == cc and r["genus"]}
    pw = pg | {r[k].split()[0] for r in occ if r["cc"] == cc for k in ("accepted_name", "identified_name") if r[k]}
    add("cross", "genera_gbif", cc, len(genera[cc]))
    add("cross", "genera_pbdb", cc, len(pg))
    add("cross", "genera_shared", cc, len(genera[cc] & pg))
    add("cross", "genera_gbif_only", cc, len(genera[cc] - pg))
    add("cross", "names_gbif_widened", cc, len(genera[cc + "_wide"]))
    add("cross", "names_shared_widened", cc, len(genera[cc + "_wide"] & pw))

fsg, fs_all = set(), set()
with open(fs_csv, newline="", encoding="utf-8-sig", errors="replace") as f:
    for r in csv.DictReader(f):
        g = r["Genus"].strip()
        if r["Class"].strip() != "Mammalia" or not re.fullmatch(r"[A-Z][a-z]+", g):
            continue
        fs_all.add(g)
        try:
            if in_au(float(r["Latitude"]), float(r["Longitude"])):
                fsg.add(g)
        except ValueError:
            pass
add("cross", "fossahul_mammal_genera_single_name", "", len(fs_all))
add("cross", "fossahul_mammal_genera_au_region", "", len(fsg))
add("cross", "gbif_au_mammal_genera", "", len(mammal_genera["AU"]))
add("cross", "gbif_au_quaternary_mammal_genera", "", len(quat_mammal_genera["AU"]))
add("cross", "fossahul_au_genera_in_gbif_au_mammals", "", len(fsg & mammal_genera["AU"]))
add("cross", "fossahul_au_genera_in_gbif_au_quaternary_mammals", "", len(fsg & quat_mammal_genera["AU"]))
add("cross", "fossahul_au_genera_without_gbif_specimen", "; ".join(sorted(fsg - mammal_genera["AU"])), len(fsg - mammal_genera["AU"]))

with open(sys.argv[5], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
sys.exit(1 if mismatch else 0)
