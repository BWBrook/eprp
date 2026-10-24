"""A naive crosswalk of alien plant species by country across GloNAF, the First Records Database and GRIIS (Q-047's first gate).

Usage: python3 crosswalk_plants.py GLONAF_DIR FR_V4_DIR GRIIS_RAW GRIIS_DATASETS_TSV GRIIS_COMPENDIUM_CSV OUT_TSV

Countries (ISO3):
- GloNAF regions whose code is a Compendium country code, or that GloNAF
  flags iso_equivalent = 1 with a three-letter code (its flag alone is not
  reliable: 0, 1, 2 and blank, and some codes are not ISO3);
- GRIIS checklists that are not protected-area lists, the GISD or nested
  units ("unit, country" titles): the unit named in the title where it is a
  known country, otherwise the ISO2 country code converted with the
  Compendium's table (so territories such as the Faroes keep their own code);
- First Records locations whose name matches a country name in GloNAF or the
  Compendium after case, accent and punctuation folding, plus seven aliases.
Species: the first two words of the accepted name (GloNAF's WCVP name, First
Records' GBIF species, GRIIS's acceptedNameUsage or else scientificName),
hybrids and names below two words dropped. First Records rows count only
when occurrenceStatus is present. Writes the species-country pairs in each
source, their overlaps, and the First Records confidence of the pairs found
in all three. Exact-name matching and country units make every overlap a
lower bound, and the sources' inclusion rules differ (GloNAF: naturalized or
invasive; GRIIS: present aliens; First Records: first records of any status);
SInAS does the full harmonisation. Standard library only.
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
iso3 = set(a2to3.values())
names = {fold(r["country"]): r["countryCode_alpha3"] for r in comp}

g_reg = {r["id"]: r for r in table(os.path.join(glonaf, "glonaf_region.csv"))}
g_iso = {k: r["code"] for k, r in g_reg.items()
         if r["code"] in iso3 or (r["iso_equivalent"] == "1" and re.fullmatch(r"[A-Z]{3}", r["code"]))}
names.update({fold(r["name"]): g_iso[k] for k, r in g_reg.items() if k in g_iso})
names.update({"russia": "RUS", "south korea": "KOR", "north korea": "PRK", "laos": "LAO", "brunei": "BRN",
              "republic of the congo": "COG", "micronesia": "FSM"})
g_tax = {r["id"]: binomial(r["taxa_accepted"]) for r in table(os.path.join(glonaf, "glonaf_taxon_wcvp.csv"))}
glo = {(g_tax[r["taxon_wcvp_id"]], g_iso[r["region_id"]]) for r in table(os.path.join(glonaf, "glonaf_flora2.csv"))
       if r["region_id"] in g_iso and g_tax.get(r["taxon_wcvp_id"])}

f_loc = {r["locationID"]: names.get(fold(r["location"])) for r in table(os.path.join(fr, "FirstRecords_location_table_public_v4.0.csv"))}
f_tax = {r["taxonID"]: r for r in table(os.path.join(fr, "FirstRecords_taxonomy_table_public_v4.0.csv"))}
first, confidence = set(), {}
for r in table(os.path.join(fr, "FirstRecords_dataset_public_v4.0.csv"), ";"):
    t = f_tax.get(r["taxonID"], {})
    sp, iso = binomial(t.get("species") or r["taxon"]), f_loc.get(r["locationID"])
    if t.get("kingdom") == "Plantae" and sp and iso and r["occurrenceStatus"].strip() == "present":
        first.add((sp, iso))
        confidence[(sp, iso)] = r["confidenceFirstRecordEvent"].strip()

gri, lists_used, lists_skipped = set(), 0, 0
for d in csv.DictReader(open(griis_ds, encoding="utf-8"), delimiter="\t"):
    unit = re.sub(r"^Global Register of Introduced and Invasive Species\s*-\s*", "", d["title"])
    if not d["file"] or ", " in unit or "Global Invasive Species Database" in d["title"] \
            or re.search(r"protected area|conservation area|ramsar|national park", d["title"], re.I):
        lists_skipped += 1
        continue
    own = names.get(fold(re.sub(r"\(.*?\)", "", unit)))
    with zipfile.ZipFile(os.path.join(griis_raw, d["file"])) as z:
        if "taxon.txt" not in z.namelist() or "distribution.txt" not in z.namelist():
            lists_skipped += 1
            continue
        lists_used += 1
        rd = lambda n: list(csv.DictReader(io.TextIOWrapper(z.open(n), encoding="utf-8", errors="replace", newline=""),
                                           delimiter="\t", quoting=csv.QUOTE_NONE))
        tx = {r["id"]: r for r in rd("taxon.txt")}
        for r in rd("distribution.txt"):
            t = tx.get(r["id"], {})
            cc = a2to3.get((r.get("countryCode") or "").strip().upper())
            sp = binomial(t.get("acceptedNameUsage")) or binomial(t.get("scientificName"))
            if t.get("kingdom") == "Plantae" and (own or cc) and sp and r.get("occurrenceStatus", "").lower() != "absent":
                gri.add((sp, own or cc))
put("GRIIS checklists used; skipped (protected areas, GISD, nested units, no distribution)", f"{lists_used}; {lists_skipped}")

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
put("pairs in all three by First Records confidence",
    "; ".join(f"{k} {v}" for k, v in collections.Counter(confidence[p] for p in G & F & R).most_common()))
per = collections.Counter(c for _, c in G & F & R)
put("countries with the most pairs in all three", "; ".join(f"{c} {n}" for c, n in per.most_common(8)))

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
