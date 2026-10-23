# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Profile the names, status and trait lists (APC, EPBC, AVONET, COMBINE, PHYLACINE) and cross-check them.

Usage: uv run names_profile.py NAMES_STATUS_DIR FOSSAHUL_CSV OUT_TSV

Counts rows and every category in each list. Matches EPBC's extinct mammal
species and FosSahul's extinct mammal species to PHYLACINE: exactly, then
through PHYLACINE's synonymy table, then against the names PHYLACINE lists as
not accepted; close-name candidates (same genus and similar epithet, or same
family and epithet) for the rest. For FosSahul it also reports the filter's
exclusions, species with mixed status rows, and whether each species has a
record dated within 130 ka. Counts COMBINE's rows by taxonomy and its
Australasian and prehistoric species. Writes long-format (table, metric, key, value).
"""

import csv
import difflib
import glob
import io
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import openpyxl

csv.field_size_limit(1 << 30)
root, fs_csv = sys.argv[1], sys.argv[2]
out = []


def add(*row):
    out.append(row)


def latest(name):
    return sorted(glob.glob(os.path.join(root, name, "raw", "*")))[-1]


def find_csv(name, fname):
    d = latest(name)
    hits = glob.glob(os.path.join(d, "**", fname), recursive=True)
    if hits:
        return open(hits[0], newline="", encoding="utf-8-sig", errors="replace")
    for z in glob.glob(os.path.join(d, "*.zip")):
        zf = zipfile.ZipFile(z)
        for n in zf.namelist():
            if n.endswith(fname):
                return io.TextIOWrapper(zf.open(n), encoding="utf-8-sig", errors="replace")
    raise FileNotFoundError(fname)


def counts(table, metric, values):
    for v, n in Counter(values).most_common():
        add(table, metric, v, n)


with open(glob.glob(os.path.join(latest("apc"), "*.csv"))[0], newline="", encoding="utf-8") as f:
    apc = list(csv.DictReader(f))
add("apc", "rows", "", len(apc))
for k in ("taxonomicStatus", "nameType", "license"):
    counts("apc", f"by:{k}", (r[k] for r in apc))
acc = [r for r in apc if r["taxonomicStatus"] == "accepted"]
add("apc", "accepted", "", len(acc))
counts("apc", "accepted_by:taxonRank", (r["taxonRank"] for r in acc))
counts("apc", "accepted_species_by:nameType", (r["nameType"] for r in acc if r["taxonRank"] == "Species"))
add("apc", "accepted_with_taxonDistribution", "", sum(bool(r["taxonDistribution"].strip()) for r in acc))
add("apc", "max_modified", "", max(r["modified"] for r in apc))

with open(glob.glob(os.path.join(latest("epbc"), "*spcs.csv"))[0], newline="", encoding="utf-8-sig") as f:
    rd = csv.DictReader(f)
    head = rd.fieldnames
    epbc = list(rd)
add("epbc", "species_rows", "", len(epbc))
counts("epbc", "by:status", (r["Threatened status"] for r in epbc))
counts("epbc", "extinct_by:class", (r["Class"] for r in epbc if r["Threatened status"] == "Extinct"))
add("epbc", "date_extracted", "", ";".join(sorted({r["Date extracted"] for r in epbc})))
add("epbc", "rows_with_different_current_name", "", sum(r["Current Scientific Name"] not in ("", "-") and r["Current Scientific Name"] != r["Scientific Name"] for r in epbc))
places = [c for c in head[head.index("Threatened status") + 1:head.index("Kingdom")] if "SPRAT" not in c]
add("epbc", "place_columns", "", ";".join(places))
counts("epbc", "place_column_values", (r[c] for r in epbc for c in places))
for r in epbc:
    if r["Scientific Name"] in ("Pseudomys gouldii", "Pseudomys fieldi"):
        add("epbc", "status_of", r["Scientific Name"], r["Threatened status"])
with open(glob.glob(os.path.join(latest("epbc"), "*cmty.csv"))[0], newline="", encoding="utf-8-sig") as f:
    add("epbc", "community_rows", "", sum(1 for _ in csv.DictReader(f)))


def current(r):
    c = r["Current Scientific Name"].strip()
    return r["Scientific Name"].strip() if c in ("", "-") else c


ext_m = {current(r): r["Family"].strip() for r in epbc if r["Threatened status"] == "Extinct" and r["Class"] == "Mammalia"}
add("epbc", "extinct_mammal_entries_by_words", "", "; ".join(f"{k} words {n}" for k, n in sorted(Counter(len(s.split()) for s in ext_m).items())))
ext_mammals = {s: f for s, f in ext_m.items() if len(s.split()) == 2}

wb = openpyxl.load_workbook(glob.glob(os.path.join(latest("avonet"), "*Supplementary dataset 1.xlsx"))[0], read_only=True)
for ws in wb.worksheets:
    add("avonet", "sheet_rows_below_header", ws.title, ws.max_row - 1)
rows = wb["AVONET_Raw_Data"].iter_rows(values_only=True)
h = next(rows)
raw = [dict(zip(h, r)) for r in rows if any(c is not None for c in r)]
add("avonet", "raw_rows", "", len(raw))
counts("avonet", "raw_by:Data.type", (str(r["Data.type"]) for r in raw))
add("avonet", "raw_gapspecies_rows", "", sum(r["Measurer"] == "GAPSPECIES" for r in raw))
add("avonet", "raw_with_Country_WRI", "", sum(r["Country_WRI"] not in (None, "", "NA") for r in raw))
add("avonet", "raw_Country_WRI_Australia", "", sum(r["Country_WRI"] == "Australia" for r in raw))
add("avonet", "raw_with_Country", "", sum(r["Country"] not in (None, "", "NA") for r in raw))

with find_csv("combine", "trait_data_reported.csv") as f:
    combine = list(csv.DictReader(f))
add("combine", "rows", "", len(combine))
add("combine", "columns", "", len(combine[0]))
add("combine", "iucn2020_not_recognised", "", sum(r["iucn2020_binomial"] == "Not recognised" for r in combine))
add("combine", "phylacine_not_recognised", "", sum(r["phylacine_binomial"] == "Not recognised" for r in combine))
add("combine", "distinct_phylacine_binomials", "", len({r["phylacine_binomial"] for r in combine} - {"Not recognised"}))
per_phy = Counter(r["phylacine_binomial"] for r in combine if r["phylacine_binomial"] != "Not recognised")
add("combine", "phylacine_species_in_several_rows", "", sum(n > 1 for n in per_phy.values()))
add("combine", "max_rows_per_phylacine_species", "", max(per_phy.values()))
counts("combine", "by:biogeographical_realm", (r["biogeographical_realm"] for r in combine))

with find_csv("phylacine", "Trait_data.csv") as f:
    phy = {r["Binomial.1.2"]: r for r in csv.DictReader(f)}
add("phylacine", "rows", "", len(phy))
counts("phylacine", "by:IUCN.Status.1.2", (r["IUCN.Status.1.2"] for r in phy.values()))
syn, rejected = {}, set()
with find_csv("phylacine", "Synonymy_table_with_unaccepted_species.csv") as f:
    for r in csv.DictReader(f):
        pairs = (("Genus.1.1", "Species.1.1"), ("Genus.1.0", "Species.1.0"),
                 ("EltonTraits.1.0.Genus", "EltonTraits.1.0.Species"), ("IUCN.2016.3.Genus", "IUCN.2016.3.Species"))
        names = {f"{r[g]}_{r[s]}" for g, s in pairs if not r[g].startswith("000")}
        if r["Binomial.1.2"] in phy:
            for n in names:
                syn.setdefault(n, r["Binomial.1.2"])
        elif r["Binomial.1.2"].startswith("000"):
            rejected |= names
add("phylacine", "names_not_accepted", "", len(rejected))

aus = [r for r in combine if "Australasian" in r["biogeographical_realm"]]
add("combine", "australasian_rows", "", len(aus))
add("combine", "australasian_iucn2020_species", "", len({r["iucn2020_binomial"] for r in aus} - {"Not recognised"}))
aus_phy = {r["phylacine_binomial"].replace(" ", "_") for r in aus} - {"Not_recognised"}
add("combine", "australasian_phylacine_species", "", len(aus_phy))
add("combine", "australasian_phylacine_species_in_phylacine", "", sum(b in phy for b in aus_phy))
for r in aus:
    if r["phylacine_binomial"] == "Not recognised":
        add("combine", "australasian_no_phylacine_name", r["iucn2020_binomial"], "")
ep = {b for b, r in phy.items() if r["IUCN.Status.1.2"] == "EP"}
no_iucn = [r for r in combine if r["iucn2020_binomial"] == "Not recognised"]
add("combine", "iucn2020_not_recognised_that_are_phylacine_EP", "", sum(r["phylacine_binomial"].replace(" ", "_") in ep for r in no_iucn))
for r in no_iucn:
    if r["phylacine_binomial"].replace(" ", "_") not in ep:
        add("combine", "iucn2020_not_recognised_not_EP", r["phylacine_binomial"], "")
ep_rows = [r for r in combine if r["phylacine_binomial"].replace(" ", "_") in ep]
traits = list(combine[0])[6:]
add("combine", "phylacine_EP_rows", "", len(ep_rows))
add("combine", "phylacine_EP_rows_realm_NA", "", sum(r["biogeographical_realm"] == "NA" for r in ep_rows))
add("combine", "phylacine_EP_rows_with_adult_mass", "", sum(r["adult_mass_g"] not in ("", "NA") for r in ep_rows))
counts("combine", "phylacine_EP_rows_by:nonmissing_traits", (str(sum(r[t] not in ("", "NA") for t in traits)) for r in ep_rows))


def cross(label, names):
    """Match binomials to PHYLACINE: exact, synonymy table, not-accepted list; close candidates for the rest."""
    add("cross", f"{label}_binomials", "", len(names))
    tiers, status = Counter(), Counter()
    for b, fam in sorted(names.items()):
        k = b.replace(" ", "_")
        hit = ("exact", k) if k in phy else ("synonym", syn[k]) if k in syn else None
        if not hit:
            if k in rejected:
                tiers["listed as not accepted"] += 1
                add("cross", f"{label}_not_accepted_by_phylacine", b, "")
                continue
            tiers["unmatched"] += 1
            g, s = b.split()
            cands = [p for p in phy if (p.split("_")[1] == s and phy[p]["Family.1.2"].lower() == fam.lower()) or
                     (p.split("_")[0] == g and difflib.SequenceMatcher(None, p.split("_")[1], s).ratio() >= 0.8)]
            add("cross", f"{label}_unmatched", b, "; ".join(f'{c} {phy[c]["IUCN.Status.1.2"]}' for c in cands) or "no similar name")
            add("cross", f"{label}_unmatched_genus_in_phylacine", b, "yes" if any(p.startswith(g + "_") for p in phy) else "no")
            continue
        tiers[hit[0]] += 1
        st = phy[hit[1]]["IUCN.Status.1.2"]
        status[st] += 1
        if hit[0] == "synonym":
            add("cross", f"{label}_matched_by_synonym", b, hit[1])
        if st not in ("EX", "EP", "EW"):
            add("cross", f"{label}_living_in_phylacine", b, f"{hit[1]} {st}")
    for v, n in tiers.most_common():
        add("cross", f"{label}_by:match", v, n)
    for v, n in status.most_common():
        add("cross", f"{label}_matched_by:IUCN.Status.1.2", v, n)


cross("epbc_extinct_mammal", ext_mammals)

with open(fs_csv, newline="", encoding="utf-8-sig") as f:
    fs = list(csv.DictReader(f))
add("cross", "fossahul_rows_by_status", "", "; ".join(f"{k or '(blank)'} {n}" for k, n in Counter(r["Status"] for r in fs).most_common()))


def clean(r):
    g, s = r["Genus"].strip(), r["Species"].strip()
    return bool(re.fullmatch(r"[A-Z][a-z]+", g) and re.fullmatch(r"[a-z]+", s) and s not in ("sp", "spp", "indet"))


ext_rows = [r for r in fs if r["Status"].strip().lower() in ("extinct", "exinct") and r["Class"].strip() == "Mammalia"]
add("cross", "fossahul_extinct_mammal_rows", "", len(ext_rows))
add("cross", "fossahul_extinct_mammal_rows_excluded_by_name_filter", "", sum(not clean(r) for r in ext_rows))
counts("cross", "fossahul_extinct_mammal_excluded_names", (f'{r["Genus"].strip()} {r["Species"].strip()}' for r in ext_rows if not clean(r)))
fs_ext = {f'{r["Genus"].strip()} {r["Species"].strip()}': r["Family"].strip() for r in ext_rows if clean(r)}
by_name = defaultdict(Counter)
dated = defaultdict(bool)
for r in fs:
    if r["Class"].strip() == "Mammalia" and clean(r):
        b = f'{r["Genus"].strip()} {r["Species"].strip()}'
        by_name[b][r["Status"].strip()] += 1
        try:
            if r["AgeType"].strip() in ("=", "<", "<=") and float(r["Age"]) <= 130:
                dated[b] = True
        except ValueError:
            pass
for b in sorted(fs_ext):
    if len(by_name[b]) > 1:
        add("cross", "fossahul_extinct_mammal_mixed_status", b, "; ".join(f"{k or '(blank)'} {n}" for k, n in by_name[b].most_common()))
cross("fossahul_extinct_mammal", fs_ext)
for b in sorted(fs_ext):
    add("cross", "fossahul_extinct_mammal_dated_within_130ka", b, "yes" if dated[b] else "no")

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
