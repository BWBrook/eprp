"""A naive crosswalk of alien plant species by country across GloNAF, the First Records Database and GRIIS (Q-047's first gate).

Usage: python3 crosswalk_plants.py GLONAF_DIR FR_V4_DIR GRIIS_RAW GRIIS_DATASETS_TSV GRIIS_COMPENDIUM_CSV OUT_TSV

Countries: GloNAF regions flagged as ISO-equivalent (their ISO3 code), GRIIS
country-level checklists (ISO2 country codes, converted to ISO3 with the
Compendium's table), and First Records locations whose name matches a
country name in GloNAF or the Compendium after case, accent and punctuation
folding. Species: the first two words of the accepted name (GloNAF's WCVP
name, First Records' GBIF species, GRIIS's scientific name), hybrids and
names below two words dropped. Writes the species-country pairs in each
source and their overlaps. Exact-name matching makes every overlap a lower
bound; SInAS does the full harmonisation. Standard library only.
"""

import collections
import csv
import io
import os
import re
import sys
import unicodedata
import zipfile

glonaf, fr, griis_raw, griis_ds, comp_csv, out_tsv = sys.argv[1:7]
csv.field_size_limit(1 << 30)
out = []


def put(metric, value):
    out.append(["crosswalk", metric, str(value)])


def fold(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]+", " ", s).strip()


def binomial(name):
    w = (name or "").replace("×", " x ").split()
    if len(w) < 2 or w[1] == "x" or not w[0][:1].isupper() or not w[1].islower():
        return None
    return f"{w[0]} {w[1]}"


def table(path, delim=","):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
        return list(csv.DictReader(f, delimiter=delim))


comp = table(comp_csv)
a2to3 = {r["countryCode_alpha2"]: r["countryCode_alpha3"] for r in comp if r["countryCode_alpha2"]}
names = {fold(r["country"]): r["countryCode_alpha3"] for r in comp}

g_reg = {r["id"]: r for r in table(os.path.join(glonaf, "glonaf_region.csv"))}
g_iso = {k: r["code"] for k, r in g_reg.items() if r["iso_equivalent"] == "1"}
names.update({fold(r["name"]): r["code"] for r in g_reg.values() if r["iso_equivalent"] == "1"})
g_tax = {r["id"]: binomial(r["taxa_accepted"]) for r in table(os.path.join(glonaf, "glonaf_taxon_wcvp.csv"))}
glo = {(g_tax[r["taxon_wcvp_id"]], g_iso[r["region_id"]]) for r in table(os.path.join(glonaf, "glonaf_flora2.csv"))
       if r["region_id"] in g_iso and g_tax.get(r["taxon_wcvp_id"])}

f_loc = {r["locationID"]: names.get(fold(r["location"])) for r in table(os.path.join(fr, "FirstRecords_location_table_public_v4.0.csv"))}
f_tax = {r["taxonID"]: r for r in table(os.path.join(fr, "FirstRecords_taxonomy_table_public_v4.0.csv"))}
first, years = set(), {}
for r in table(os.path.join(fr, "FirstRecords_dataset_public_v4.0.csv"), ";"):
    t = f_tax.get(r["taxonID"], {})
    sp, iso = binomial(t.get("species") or r["taxon"]), f_loc.get(r["locationID"])
    if t.get("kingdom") == "Plantae" and sp and iso and r["occurrenceStatus"] != "absent":
        first.add((sp, iso))
        if re.fullmatch(r"-?\d+", r["firstRecordEvent"].strip()):
            years[(sp, iso)] = int(r["firstRecordEvent"])

gri = set()
for d in csv.DictReader(open(griis_ds, encoding="utf-8"), delimiter="\t"):
    if not d["file"] or "Protected Area" in d["title"] or "Global Invasive Species Database" in d["title"]:
        continue
    with zipfile.ZipFile(os.path.join(griis_raw, d["file"])) as z:
        if "taxon.txt" not in z.namelist() or "distribution.txt" not in z.namelist():
            continue
        rd = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8", errors="replace", newline=""),
                                           delimiter="\t", quoting=csv.QUOTE_NONE))
        tx = {r["id"]: r for r in rd("taxon.txt")}
        for r in rd("distribution.txt"):
            t = tx.get(r["id"], {})
            cc = (r.get("countryCode") or "").strip().upper()
            if t.get("kingdom") == "Plantae" and cc in a2to3 and binomial(t.get("scientificName")) \
                    and r.get("occurrenceStatus", "").lower() != "absent":
                gri.add((binomial(t["scientificName"]), a2to3[cc]))

countries = {s: {c for _, c in pairs} for s, pairs in (("GloNAF", glo), ("FirstRecords", first), ("GRIIS", gri))}
shared = countries["GloNAF"] & countries["FirstRecords"] & countries["GRIIS"]
put("countries matched: GloNAF; First Records; GRIIS; in all three",
    f"{len(countries['GloNAF'])}; {len(countries['FirstRecords'])}; {len(countries['GRIIS'])}; {len(shared)}")
put("locations of First Records matched to a country (of all)", f"{sum(1 for v in f_loc.values() if v)} of {len(f_loc)}")
G, F, R = ({p for p in s if p[1] in shared} for s in (glo, first, gri))
put("plant species-country pairs in the shared countries: GloNAF; First Records; GRIIS", f"{len(G)}; {len(F)}; {len(R)}")
put("pairs in GloNAF and GRIIS; GloNAF and First Records; First Records and GRIIS; all three",
    f"{len(G & R)}; {len(G & F)}; {len(F & R)}; {len(G & F & R)}")
put("pairs in only one source: GloNAF; First Records; GRIIS", f"{len(G - F - R)}; {len(F - G - R)}; {len(R - G - F)}")
put("pairs in all three with a first-record year", sum(1 for p in G & F & R if p in years))
per = collections.Counter(c for _, c in G & F & R)
put("countries with the most pairs in all three", "; ".join(f"{c} {n}" for c, n in per.most_common(8)))

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
