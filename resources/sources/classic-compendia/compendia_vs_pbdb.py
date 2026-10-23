# /// script
# requires-python = ">=3.10"
# dependencies = ["rdata==0.11.2"]
# ///
"""Compare the two compendia with the public PBDB snapshot.

Usage: uv run compendia_vs_pbdb.py FR2_DERIVED SEPKOSKI_DERIVED SEPKOSKI_RDA PBDB_GLOBAL_RAW OUT_TSV

FR2_DERIVED holds fr2_families.csv and fr2_divisions.csv from fr2_profile.py
(the divisions dated from the Vendian on with the Harland et al. 1990 ages in
Bristol's 1998 stage table) and receives fr2_vs_pbdb.csv. SEPKOSKI_DERIVED holds
sepkoski_genera.csv from sepkoski_profile.py and receives sepkoski_vs_pbdb.csv.
SEPKOSKI_RDA is data/sepkoski.rda from the palaeoverse package, the source of
the genus ages (the package's stage ages; CRAN 0.0.1 and the GitHub head agree).

Names: each compendium name, with any "?" removed, is looked up among PBDB taxon
names whose accepted rank is the same (taxon_rank is blank in PBDB's list
output), accepted or not, and failing that among names of any rank; this
includes the 28 Sepkoski names with corrupted letters, as captured and with bit
7 cleared. Ranges: first and last appearances from PBDB's public occurrences
(oldest max_ma, youngest min_ma, over occurrences identified to the genus or
below for genera, the family or below for families; an occurrence whose genus
field reads "Genus (Subgenus)" counts for both names; a name that PBDB treats as
a junior synonym is looked up under its senior name), against Sepkoski's genus
ranges and FR2's maximum family ranges, also by age of the compendium's first
appearance. Time scales differ (the package's, PBDB's own, Harland 1990), so
differences within 5 Myr are treated as agreement. Also counts PBDB opinions,
taxa and occurrences that cite the compendia, against all genus-rank records.
Personal-name columns of PBDB records are not used.
"""

import csv
import glob
import os
import re
import statistics
import sys
from collections import Counter, defaultdict

import rdata
from rdata.parser import RObjectType as T

fr2_dir, sep_dir, rda, pbdb, out_tsv = sys.argv[1:6]
out = []
TOL = 5.0
csv.field_size_limit(1 << 30)


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def r_frame(path):
    o = rdata.parser.parse_file(path, extension=".rda").object.value[0]
    a, names = o.attributes, None
    while a is not None and a.info.type == T.LIST:
        if a.tag.value.value == b"names":
            names = [c.value.decode() for c in a.value[0].value]
        a = a.value[1]
    cols = {}
    for n, col in zip(names, o.value):
        if col.info.type == T.STR:
            cols[n] = [None if c.value is None else c.value.decode("utf-8", "replace") for c in col.value]
        else:
            cols[n] = [float(x) for x in col.value]
    return cols


# --- PBDB ---------------------------------------------------------------------
taxa_rank, senior, any_rank = defaultdict(dict), defaultdict(dict), {}
with open(os.path.join(pbdb, "taxa.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        rank = r["taxon_rank"] or r["accepted_rank"]
        any_rank.setdefault(r["taxon_name"], rank)
        if rank in ("genus", "family"):
            prev = taxa_rank[rank].get(r["taxon_name"])
            status = "accepted" if not r["difference"] else r["difference"]
            if prev != "accepted":
                taxa_rank[rank][r["taxon_name"]] = status
                if status != "accepted" and r["accepted_rank"] == rank and r["accepted_name"] != r["taxon_name"]:
                    senior[rank][r["taxon_name"]] = r["accepted_name"]
                else:
                    senior[rank].pop(r["taxon_name"], None)
put("pbdb", "taxa", "names", f"genus {len(taxa_rank['genus'])}; family {len(taxa_rank['family'])}")

GENUS_OR_BELOW = {"genus", "subgenus", "species", "subspecies"}
FAMILY_OR_BELOW = GENUS_OR_BELOW | {"family", "subfamily", "tribe", "subtribe"}
grange, frange = {}, {}
n_occ = 0
for path in sorted(glob.glob(os.path.join(pbdb, "occurrences__p*.csv"))):
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            n_occ += 1
            try:
                hi, lo = float(r["max_ma"]), float(r["min_ma"])
            except ValueError:
                continue
            rank = r["accepted_rank"]
            m = re.fullmatch(r"(\S+) \((\S+)\)", r["genus"])
            gnames = m.groups() if m else (r["genus"],)
            for names, store, ok in ((gnames, grange, rank in GENUS_OR_BELOW), ((r["family"],), frange, rank in FAMILY_OR_BELOW)):
                for name in names:
                    if ok and name and not name.startswith("NO_"):
                        old = store.get(name)
                        store[name] = (max(hi, old[0]), min(lo, old[1]), old[2] + 1) if old else (hi, lo, 1)
put("pbdb", "occurrences", "public rows read", n_occ)
put("pbdb", "occurrences", "ranges", f"genera {len(grange)}; families {len(frange)}")

refs = {}
with open(os.path.join(pbdb, "references.csv"), newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        t = r["reftitle"].lower() + " " + r["pubtitle"].lower()
        if (r["author1last"] == "Sepkoski" and r["pubyr"] in ("1982", "1992", "2002") and "compendium" in t) or \
                (r["author1last"] == "Benton" and r["pubyr"] == "1993" and "fossil record 2" in t):
            refs[r["reference_no"]] = f"{r['author1last']} {r['pubyr']}: {r['reftitle'] or r['pubtitle']}"
cites, genus_total, genus_citing = defaultdict(Counter), Counter(), defaultdict(Counter)
for table, rank_col in (("opinions", "taxon_rank"), ("taxa", "accepted_rank")):
    with open(os.path.join(pbdb, f"{table}.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            genus = r[rank_col] == "genus"
            genus_total[table] += genus
            if r["reference_no"] in refs:
                cites[r["reference_no"]][table] += 1
                genus_citing[r["reference_no"]][table] += genus
for path in sorted(glob.glob(os.path.join(pbdb, "occurrences__p*.csv"))):
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["reference_no"] in refs:
                cites[r["reference_no"]]["occurrences"] += 1
for no, label in sorted(refs.items(), key=lambda kv: int(kv[0])):
    put("pbdb", "records citing a compendium", f"reference {no} ({label[:90]})",
        "; ".join(f"{k} {v}" for k, v in sorted(cites[no].items())) or "none")
    put("pbdb", "genus-rank records citing it", f"reference {no}", "; ".join(
        f"{t} {genus_citing[no][t]} of {genus_total[t]} ({100 * genus_citing[no][t] / genus_total[t]:.1f}%)" for t in ("opinions", "taxa")))


def name_status(names, rank):
    found = Counter()
    for name in names:
        name = name.replace("?", "").strip()
        status = taxa_rank[rank].get(name)
        found[f"accepted PBDB {rank} name" if status == "accepted" else f"PBDB {rank} name, {status}" if status
              else f"PBDB name at another rank ({any_rank[name]})" if name in any_rank else "not a PBDB name"] += 1
    other = sum(v for k, v in found.items() if k.startswith("PBDB name at another rank"))
    main = [(k, v) for k, v in found.most_common() if not k.startswith("PBDB name at another rank")]
    return "; ".join(f"{k} {v}" for k, v in main) + f"; PBDB name at another rank {other} (" + \
        ", ".join(f"{k[27:-1]} {v}" for k, v in found.most_common() if k.startswith("PBDB name at another rank")) + ")"


BRACKETS = ((485, 1e9, "first appearance older than 485 Ma"), (252, 485, "485-252 Ma"), (66, 252, "252-66 Ma"), (-1, 66, "younger than 66 Ma"))


def by_bracket(pairs):
    out_ = []
    for lo, hi, label in BRACKETS:
        d = [x for a, x in pairs if lo < a <= hi]
        if d:
            out_.append(f"{label}: n {len(d)}, median {statistics.median(d):+.1f} Myr, within 5 Myr {sum(abs(x) <= TOL for x in d)}")
    return "; ".join(out_)


def compare(rows, store, rank):
    fad, lad, fpairs = [], [], []
    bins = Counter()
    detail = []
    for name, first, last, extant in rows:
        used = senior[rank].get(name, name)
        if used != name:
            bins["looked up under the PBDB senior name"] += 1
        occ = store.get(used)
        if not occ:
            bins["no public occurrences"] += 1
            detail.append([name, used, first, last, int(extant), "", "", 0])
            continue
        d1 = occ[0] - first
        fad.append(d1)
        fpairs.append((first, d1))
        bins["first: PBDB older by >5 Myr" if d1 > TOL else "first: PBDB younger by >5 Myr" if d1 < -TOL else "first: within 5 Myr"] += 1
        if not extant:
            d2 = occ[1] - last
            lad.append(d2)
            bins["last: PBDB younger by >5 Myr" if d2 < -TOL else "last: PBDB older by >5 Myr" if d2 > TOL else "last: within 5 Myr"] += 1
        detail.append([name, used, first, last, int(extant), occ[0], occ[1], occ[2]])
    return bins, fad, lad, detail, fpairs


# --- Sepkoski ------------------------------------------------------------------
genera = list(csv.DictReader(open(os.path.join(sep_dir, "sepkoski_genera.csv"), encoding="utf-8")))
put("sepkoski", "names", "captured genus rows in PBDB", name_status([g["genus"] for g in genera], "genus"))
odd = sorted({g["genus"] for g in genera if any(ord(ch) > 127 for ch in g["genus"])})
low7 = lambda n: "".join(chr(ord(ch) & 0x7F) for ch in n)
put("sepkoski", "names", "28 corrupted names as captured", name_status(odd, "genus"))
put("sepkoski", "names", "28 corrupted names with bit 7 cleared", name_status([low7(n) for n in odd], "genus")
    + "; not found: " + (", ".join(low7(n) for n in odd if low7(n) not in taxa_rank["genus"]) or "none"))
sep = r_frame(rda)
counts = Counter(sep["genus"])
srows = [(g, sep["max_ma"][i], sep["min_ma"][i], sep["min_ma"][i] == 0)
         for i, g in enumerate(sep["genus"]) if counts[g] == 1 and sep["max_ma"][i] == sep["max_ma"][i]]
put("sepkoski", "input", "package genus rows; with a unique name and ages", f"{len(sep['genus'])}; {len(srows)}")
bins, fad, lad, detail, fpairs = compare(srows, grange, "genus")
put("sepkoski", "ranges_vs_pbdb_occurrences", "classes", "; ".join(f"{k} {v}" for k, v in sorted(bins.items())))
put("sepkoski", "ranges_vs_pbdb_occurrences", "median PBDB minus Sepkoski (Myr)",
    f"first {statistics.median(fad):+.1f} (n {len(fad)}); last {statistics.median(lad):+.1f} (n {len(lad)}, extinct genera)")
put("sepkoski", "ranges_vs_pbdb_occurrences", "first appearance, PBDB minus Sepkoski, by age of the Sepkoski first appearance", by_bracket(fpairs))
with open(os.path.join(sep_dir, "sepkoski_vs_pbdb.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["genus", "pbdb_name_used", "sepkoski_max_ma", "sepkoski_min_ma", "extant", "pbdb_first_max_ma", "pbdb_last_min_ma", "pbdb_public_occurrences"])
    w.writerows(detail)

# --- FR2 -------------------------------------------------------------------------
lookup = {r["division"]: (float(r["base_ma"]), float(r["top_ma"]))
          for r in csv.DictReader(open(os.path.join(fr2_dir, "fr2_divisions.csv"), encoding="utf-8")) if r["base_ma"]}
fam = list(csv.DictReader(open(os.path.join(fr2_dir, "fr2_families.csv"), encoding="utf-8")))
put("fr2", "names", "family rows in PBDB (all chapters)", name_status([f["family"] for f in fam], "family"))
fcount = Counter(f["family"] for f in fam)
frows = []
for f in fam:
    a, b = lookup.get(f["max_first"]), lookup.get(f["max_last"])
    if fcount[f["family"]] == 1 and a and b and f["chapter"] != "45" and "?" not in f["family"]:
        frows.append((f["family"], a[0], b[1], f["extant"] == "1"))
put("fr2", "input", "families with a unique name, a maximum range from the Vendian on, not angiosperms or questioned", len(frows))
bins, fad, lad, detail, fpairs = compare(frows, frange, "family")
put("fr2", "ranges_vs_pbdb_occurrences", "classes", "; ".join(f"{k} {v}" for k, v in sorted(bins.items())))
put("fr2", "ranges_vs_pbdb_occurrences", "median PBDB minus FR2 (Myr)",
    f"first {statistics.median(fad):+.1f} (n {len(fad)}); last {statistics.median(lad):+.1f} (n {len(lad)}, extinct families)")
put("fr2", "ranges_vs_pbdb_occurrences", "first appearance, PBDB minus FR2, by age of the FR2 first appearance", by_bracket(fpairs))
with open(os.path.join(fr2_dir, "fr2_vs_pbdb.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["family", "pbdb_name_used", "fr2_max_first_base_ma", "fr2_max_last_top_ma", "to_holocene", "pbdb_first_max_ma", "pbdb_last_min_ma", "pbdb_public_occurrences"])
    w.writerows(detail)

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
