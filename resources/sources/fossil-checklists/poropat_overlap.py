"""Compare Poropat et al. (2023) Mesozoic tetrapod occurrences with the PBDB extract and ASUD.

Usage: python3 poropat_overlap.py POROPAT_TABLES_TSV PBDB_AU_NG_SNAPSHOT ASUD_CSV OUT_TSV

Taxa: binomials and genera named in the Poropat tables (body fossils, A1-A11)
against PBDB identified and accepted names of Australian non-fish chordate
occurrences with interval midpoints of 66-256 Ma (the tables include uppermost
Permian taxa); "genera" include higher taxa named in "X indet." rows. Rock
units: Poropat unit names (bracketed parent units and quotes removed) against
PBDB formations and ASUD unit names, with trailing rank and lithology words
folded. Standard library only.
"""

import csv
import re
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
RANK = {"formation", "fm", "group", "member", "beds", "bed", "subgroup", "supergroup", "sandstone", "mudstone",
        "shale", "limestone", "siltstone", "greensand", "calcarenite", "measures"}
TETRAPODS = {"Amphibia", "Reptilia", "Aves", "Mammalia", "Synapsida", "Temnospondyli"}
out = []


def add(*row):
    out.append(row)


def norm_unit(s):
    s = re.sub(r"\(.*?\)|[‘’'?]", " ", s.lower())
    w = [x for x in re.sub(r"[^a-z ]", " ", s).split() if x not in ("upper", "lower", "middle")]
    while w and w[-1] in RANK:
        w.pop()
    return " ".join(w)


def names(taxon):
    t = re.sub(r"\(.*?\)", " ", taxon)
    m = re.match(r"(?:cf\.\s*|aff\.\s*|\?)?([A-Z][a-z]+)\s+([a-z]+)\b", t.strip())
    g = re.match(r"(?:cf\.\s*|aff\.\s*|\?)?([A-Z][a-z]+)", t.strip())
    binom = f"{m.group(1)} {m.group(2)}" if m and m.group(2) not in ("indet", "sp", "isp", "incertae", "cf", "aff", "nov", "gen") else None
    return binom, g.group(1) if g else None


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    pr = list(csv.DictReader(f, delimiter="\t"))
body = [r for r in pr if r["table"] != "A12"]
with open(f"{sys.argv[2]}/occurrences.csv", newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    h = next(rd)
    ix = {k: h.index(k) for k in ("identified_name", "accepted_name", "class", "phylum", "max_ma", "min_ma", "formation", "cc", "genus")}
    pb = []
    for r in rd:
        try:
            mid = (float(r[ix["max_ma"]]) + float(r[ix["min_ma"]])) / 2
        except ValueError:
            continue
        if r[ix["cc"]] == "AU" and 66 <= mid < 256 and r[ix["phylum"]] == "Chordata" and r[ix["class"]] not in ("Osteichthyes", "Chondrichthyes", "Conodonta"):
            pb.append(r)
pb_species = {" ".join(r[ix[k]].split()[:2]) for r in pb for k in ("identified_name", "accepted_name")}
pb_genera = {r[ix["genus"]] for r in pb} | {r[ix["accepted_name"]].split()[0] for r in pb if r[ix["accepted_name"]]}
add("pbdb", "australian_mesozoic_non_fish_chordate_occurrences", "", len(pb))
binoms = {names(r["taxon"])[0] for r in body} - {None}
genera = {names(r["taxon"])[1] for r in body} - {None}
add("poropat", "rows", "", len(pr))
add("poropat", "body_fossil_rows", "", len(body))
add("poropat", "distinct_binomials", "", len(binoms))
add("poropat", "binomials_in_pbdb_extract", "", len(binoms & pb_species))
add("poropat", "distinct_genera", "", len(genera))
add("poropat", "genera_in_pbdb_extract", "", len(genera & pb_genera))
for b in sorted(binoms - pb_species)[:40]:
    add("poropat", "binomial_not_in_pbdb_extract", b, "")

units = {norm_unit(r["rock_unit"]) for r in pr}
pb_units = {norm_unit(r[ix["formation"]]) for r in pb if r[ix["formation"]]}
with open(sys.argv[3], newline="", encoding="utf-8") as f:
    asud_units = {norm_unit(u["NAME"]) for u in csv.DictReader(f)}
add("units", "poropat_distinct_normalised", "", len(units))
add("units", "in_pbdb_formations", "", len(units & pb_units))
add("units", "in_asud_names", "", len(units & asud_units))
for u in sorted(units - asud_units):
    add("units", "not_in_asud", u, "")

with open(sys.argv[4], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
