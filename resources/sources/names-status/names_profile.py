# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Profile the names, status and trait lists (APC, EPBC, AVONET, COMBINE, PHYLACINE) and cross-check them.

Usage: uv run names_profile.py NAMES_STATUS_DIR FOSSAHUL_CSV OUT_TSV

Counts rows and categories in each list; matches EPBC's extinct mammal
species and FosSahul's extinct mammal species to PHYLACINE (exactly, then
through PHYLACINE's synonymy table), with close-name candidates for the rest;
counts COMBINE's Australasian mammals. Writes long-format (table, metric, key, value).
"""

import csv
import difflib
import glob
import io
import os
import re
import sys
import zipfile
from collections import Counter

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


with open(glob.glob(os.path.join(latest("apc"), "*.csv"))[0], newline="", encoding="utf-8") as f:
    apc = list(csv.DictReader(f))
add("apc", "rows", "", len(apc))
for k in ("taxonomicStatus", "nameType", "license"):
    for v, n in Counter(r[k] for r in apc).most_common(8):
        add("apc", f"by:{k}", v, n)
acc = [r for r in apc if r["taxonomicStatus"] == "accepted"]
add("apc", "accepted", "", len(acc))
for v, n in Counter(r["taxonRank"] for r in acc).most_common(6):
    add("apc", "accepted_by:taxonRank", v, n)
add("apc", "max_modified", "", max(r["modified"] for r in apc))

with open(glob.glob(os.path.join(latest("epbc"), "*spcs.csv"))[0], newline="", encoding="utf-8-sig") as f:
    epbc = list(csv.DictReader(f))
add("epbc", "species_rows", "", len(epbc))
for v, n in Counter(r["Threatened status"] for r in epbc).most_common():
    add("epbc", "by:status", v, n)
for v, n in Counter(r["Class"] for r in epbc if r["Threatened status"] == "Extinct").most_common():
    add("epbc", "extinct_by:class", v, n)
add("epbc", "date_extracted", "", ";".join(sorted({r["Date extracted"] for r in epbc})))
add("epbc", "rows_with_different_current_name", "", sum(r["Current Scientific Name"] not in ("", "-") and r["Current Scientific Name"] != r["Scientific Name"] for r in epbc))


def current(r):
    c = r["Current Scientific Name"].strip()
    return r["Scientific Name"].strip() if c in ("", "-") else c


ext_m = {current(r): r["Family"].strip() for r in epbc if r["Threatened status"] == "Extinct" and r["Class"] == "Mammalia"}
add("epbc", "extinct_mammal_entries_by_words", "", "; ".join(f"{k} words {n}" for k, n in sorted(Counter(len(s.split()) for s in ext_m).items())))
ext_mammals = {s: f for s, f in ext_m.items() if len(s.split()) == 2}

wb = openpyxl.load_workbook(glob.glob(os.path.join(latest("avonet"), "*Supplementary dataset 1.xlsx"))[0], read_only=True)
for ws in wb.worksheets:
    add("avonet", "sheet_rows", ws.title, ws.max_row)

with find_csv("combine", "trait_data_reported.csv") as f:
    combine = list(csv.DictReader(f))
add("combine", "rows", "", len(combine))
add("combine", "columns", "", len(combine[0]))
add("combine", "iucn2020_not_recognised", "", sum(r["iucn2020_binomial"] == "Not recognised" for r in combine))
add("combine", "phylacine_not_recognised", "", sum(r["phylacine_binomial"] == "Not recognised" for r in combine))
add("combine", "distinct_phylacine_binomials", "", len({r["phylacine_binomial"] for r in combine} - {"Not recognised"}))
for v, n in Counter(r["biogeographical_realm"] for r in combine).most_common(10):
    add("combine", "by:biogeographical_realm", v, n)

with find_csv("phylacine", "Trait_data.csv") as f:
    phy = {r["Binomial.1.2"]: r for r in csv.DictReader(f)}
add("phylacine", "rows", "", len(phy))
for v, n in Counter(r["IUCN.Status.1.2"] for r in phy.values()).most_common():
    add("phylacine", "by:IUCN.Status.1.2", v, n)
syn = {}
with find_csv("phylacine", "Synonymy_table_with_unaccepted_species.csv") as f:
    for r in csv.DictReader(f):
        if r["Binomial.1.2"] in phy:
            for g, s in (("Genus.1.1", "Species.1.1"), ("Genus.1.0", "Species.1.0"),
                         ("EltonTraits.1.0.Genus", "EltonTraits.1.0.Species"), ("IUCN.2016.3.Genus", "IUCN.2016.3.Species")):
                syn.setdefault(f"{r[g]}_{r[s]}", r["Binomial.1.2"])
aus = {r["phylacine_binomial"].replace(" ", "_") for r in combine if "Australasian" in r["biogeographical_realm"]}
add("combine", "australasian_species", "", len(aus))
add("combine", "australasian_species_in_phylacine", "", sum(b in phy for b in aus))


def cross(label, names):
    """Match binomials to PHYLACINE exactly, then through its synonymy table; list close candidates for the rest."""
    add("cross", f"{label}_binomials", "", len(names))
    tiers, status = Counter(), Counter()
    for b, fam in sorted(names.items()):
        k = b.replace(" ", "_")
        hit = ("exact", k) if k in phy else ("synonym", syn[k]) if k in syn else None
        if not hit:
            tiers["unmatched"] += 1
            g, s = b.split()
            cands = [p for p in phy if (p.split("_")[1] == s and phy[p]["Family.1.2"].lower() == fam.lower()) or
                     (p.split("_")[0] == g and difflib.SequenceMatcher(None, p.split("_")[1], s).ratio() >= 0.8)]
            add("cross", f"{label}_unmatched", b, "; ".join(f'{c} {phy[c]["IUCN.Status.1.2"]}' for c in cands) or "no candidate")
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
fs_ext = {f'{r["Genus"].strip()} {r["Species"].strip()}': r["Family"].strip() for r in fs
          if r["Status"].strip().lower() in ("extinct", "exinct") and r["Class"].strip() == "Mammalia"
          and re.fullmatch(r"[A-Z][a-z]+", r["Genus"].strip()) and re.fullmatch(r"[a-z]+", r["Species"].strip())
          and r["Species"].strip() not in ("sp", "spp", "indet")}
cross("fossahul_extinct_mammal", fs_ext)

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
