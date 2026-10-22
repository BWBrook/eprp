"""Compare Poropat et al. (2023) Mesozoic tetrapod occurrences with the PBDB extract and ASUD.

Usage: python3 poropat_overlap.py POROPAT_PDF POROPAT_TABLES_TSV PBDB_AU_NG_SNAPSHOT PBDB_INTERVALS_CSV ASUD_CSV OUT_TSV
(needs pdftotext from poppler; otherwise standard library only)

Taxa. Binomials (body fossils, tables A1-A11) are looked up among the names
(identified and accepted, cf./aff./? and quotes removed) of Australian PBDB
occurrences in two windows on the occurrence's interval midpoint: the original
66-256 Ma, and a Permian-aware 66 Ma to the base of the Wuchiapingian in PBDB's
interval table (Mesozoic plus Lopingian, since the tables include uppermost
Permian taxa). Tiers: exact; spelling variant (Levenshtein distance up to 2 in
genus and in species epithet, at most 3 in all); absent. Absence is also tested
against every name in the AU+NG extract (any taxon, any age, occurrences and
taxon table). The spelling rows count each spelling in the paper's main text
and references against its appendix. "First words" of taxon cells are genera
plus the higher taxa named in "indet." rows.

Rock units. Poropat unit names (bracketed parent units and quotes removed;
upper/lower/middle and trailing rank and lithology words folded) against the
formation, member and group names of PBDB occurrences, and against ASUD unit
names. For ASUD, age compatibility compares the unit's Poropat age (union of
the stages named in its rows, with stage ages from PBDB's interval table,
scale 1) with each ASUD unit of that name (NUMERICOLDERAGE, NUMERICYOUNGERAGE);
the gap is zero if the ranges overlap, and the best-matching ASUD unit counts.
"""

import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
pdf_path, tables_path, pbdb_dir, intervals_path, asud_path, out_path = sys.argv[1:7]
RANK = {"formation", "fm", "group", "member", "beds", "bed", "subgroup", "supergroup", "sandstone", "mudstone",
        "shale", "limestone", "siltstone", "greensand", "calcarenite", "measures"}
FISH = ("Osteichthyes", "Chondrichthyes", "Conodonta")
NOT_EPITHET = {"indet", "sp", "spp", "isp", "incertae", "cf", "aff", "nov", "gen", "sedis"}
out = []


def add(*row):
    out.append(row)


def norm_unit(s):
    s = re.sub(r"\(.*?\)|[‘’'?]", " ", s.lower())
    w = [x for x in re.sub(r"[^a-z ]", " ", s).split() if x not in ("upper", "lower", "middle")]
    while w and w[-1] in RANK:
        w.pop()
    return " ".join(w)


def poropat_names(taxon):
    t = re.sub(r"\(.*?\)", " ", taxon).strip()
    m = re.match(r"(?:cf\.\s*|aff\.\s*|\?)?([A-Z][a-z]+)\s+([a-z]+)\b", t)
    g = re.match(r"(?:cf\.\s*|aff\.\s*|\?)?([A-Z][a-z]+)", t)
    binom = (m.group(1), m.group(2)) if m and m.group(2) not in NOT_EPITHET else None
    return binom, g.group(1) if g else None


def pbdb_binom(name):
    w = re.sub(r"\b(?:cf|aff)\.|[?\"‘’']|\([^)]*\)", " ", name).split()
    if len(w) >= 2 and re.fullmatch(r"[A-Z][a-z]+", w[0]) and re.fullmatch(r"[a-z]{3,}", w[1]) and w[1] not in NOT_EPITHET:
        return w[0], w[1]
    return None


def lev(a, b):
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def variants(g, e, pool):
    found = []
    for gp, ep in pool:
        if abs(len(gp) - len(g)) > 2 or abs(len(ep) - len(e)) > 2:
            continue
        dg, de = lev(g, gp), lev(e, ep)
        if (dg, de) != (0, 0) and dg <= 2 and de <= 2 and dg + de <= 3:
            found.append((dg + de, gp, ep))
    return sorted(found)


def span(info):
    return f'{info["n"]} occurrences, {info["max"]:g}-{info["min"]:g} Ma'


with open(intervals_path, newline="", encoding="utf-8") as f:
    stage = {r["interval_name"]: (float(r["t_age"]), float(r["b_age"])) for r in csv.DictReader(f) if r["scale_no"] == "1"}
OLD = (66.0, 256.0)
WIDE = (66.0, stage["Wuchiapingian"][1])

with open(tables_path, newline="", encoding="utf-8") as f:
    pr = list(csv.DictReader(f, delimiter="\t"))
body = [r for r in pr if r["table"] != "A12"]

with open(f"{pbdb_dir}/occurrences.csv", newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    h = next(rd)
    ix = {}
    for i, k in enumerate(h):
        ix.setdefault(k, i)
    allocc = []
    for r in rd:
        try:
            mid = (float(r[ix["max_ma"]]) + float(r[ix["min_ma"]])) / 2
        except ValueError:
            mid = None
        allocc.append((r, mid))


def select(window, fish_out):
    return [r for r, mid in allocc if r[ix["cc"]] == "AU" and mid is not None and window[0] <= mid < window[1]
            and (not fish_out or (r[ix["phylum"]] == "Chordata" and r[ix["class"]] not in FISH))]


def name_info(occs):
    info = {}
    for r in occs:
        for b in {pbdb_binom(r[ix["identified_name"]]), pbdb_binom(r[ix["accepted_name"]])} - {None}:
            d = info.setdefault(b, {"n": 0, "max": 0.0, "min": 1e9})
            d["n"] += 1
            d["max"] = max(d["max"], float(r[ix["max_ma"]]))
            d["min"] = min(d["min"], float(r[ix["min_ma"]]))
    return info


chordates_old, chordates_wide = select(OLD, True), select(WIDE, True)
info_old, info_wide = name_info(chordates_old), name_info(chordates_wide)
add("pbdb", "australian_non_fish_chordate_occurrences_midpoint_66_256", "", len(chordates_old))
add("pbdb", "australian_non_fish_chordate_occurrences_permian_aware_window", f"66-{WIDE[1]:g}", len(chordates_wide))

binoms = {names[0] for names in (poropat_names(r["taxon"]) for r in body)} - {None}
exact_old = {b for b in binoms if b in info_old}
exact_wide = {b for b in binoms if b in info_wide}
add("poropat", "rows", "", len(pr))
add("poropat", "body_fossil_rows", "", len(body))
add("poropat", "distinct_binomials", "", len(binoms))
add("taxa", "binomials_exact_original_window", "", len(exact_old))
add("taxa", "binomials_exact_permian_aware_window", "", len(exact_wide))

variant_of = {b: variants(*b, info_wide) for b in sorted(binoms - exact_wide)}
matched_variant = {b: v for b, v in variant_of.items() if v}
add("taxa", "binomials_exact_or_variant_permian_aware_window", "", len(exact_wide) + len(matched_variant))

all_names = {pbdb_binom(r[ix[k]]) for r, _ in allocc for k in ("identified_name", "accepted_name")} - {None}
with open(f"{pbdb_dir}/taxa.csv", newline="", encoding="utf-8") as f:
    trd = csv.reader(f)
    th = next(trd)
    tix = th.index("taxon_name")
    all_names |= {pbdb_binom(r[tix]) for r in trd} - {None}
add("pbdb", "distinct_binomials_in_au_ng_extract_any_taxon_any_age", "", len(all_names))
for b in sorted(binoms - exact_old):
    gen = " ".join(b)
    if b in exact_wide:
        add("taxa", "exact_only_in_permian_aware_window", gen, span(info_wide[b]))
    elif b in matched_variant:
        for _, gp, ep in matched_variant[b]:
            add("taxa", "spelling_variant_in_pbdb", gen, f"{gp} {ep}; " + span(info_wide[(gp, ep)]))
    else:
        add("taxa", "no_exact_or_variant_in_window", gen, "exact in au-ng extract: " + str(b in all_names)
            + "; variant anywhere in au-ng extract: " + str(bool(variants(*b, all_names))))

pages = subprocess.run(["pdftotext", pdf_path, "-"], capture_output=True, text=True, check=True).stdout.split("\f")
first = next(i for i, p in enumerate(pages) if re.search(r"^Table A1\. Chron", p, re.M))
main_text, appendix = " ".join(" ".join(pages[:first]).split()), " ".join(" ".join(pages[first:]).split())
for b, v in matched_variant.items():
    for _, gp, ep in v:
        for tok in sorted({b[0], gp, b[1], ep}):
            pat = re.compile(r"\b" + tok + r"\b")
            add("spelling", tok, f"{len(pat.findall(main_text))} in main text and references; "
                f"{len(pat.findall(appendix))} in appendix")

genera = {b[0] for b in binoms}
pb_genera_wide = {r[ix["genus"]] for r in chordates_wide if r[ix["genus"]]} | {g for g, _ in info_wide}
genus_variant = {g: sorted(p for p in pb_genera_wide if len(g) >= 6 and lev(g, p) <= 2) for g in genera - pb_genera_wide}
first_words = {names[1] for names in (poropat_names(r["taxon"]) for r in body)} - {None}
add("taxa", "distinct_genera_in_binomials", "", len(genera))
add("taxa", "genera_in_binomials_in_pbdb_exact", "", len(genera & pb_genera_wide))
add("taxa", "genera_in_binomials_in_pbdb_exact_or_variant", "", len(genera & pb_genera_wide) + sum(bool(v) for v in genus_variant.values()))
for g, v in sorted(genus_variant.items()):
    add("taxa", "genus_not_exact_in_pbdb", g, "variant: " + ", ".join(v) if v else "none")
add("taxa", "distinct_first_words_of_taxon_cells", "genera plus higher taxa named in indet. rows", len(first_words))
pb_any_rank = pb_genera_wide | {r[ix[c]] for r in chordates_wide for c in ("family", "order", "class") if r[ix[c]]} \
    | {r[ix[c]].split()[0] for r in chordates_wide for c in ("identified_name", "accepted_name") if r[ix[c]]}
add("taxa", "first_words_in_pbdb_names_of_any_rank", "genus, family, order, class, first words of names", len(first_words & pb_any_rank))

units = {norm_unit(r["rock_unit"]) for r in pr}
add("units", "poropat_distinct_unit_strings", "", len({r["rock_unit"] for r in pr}))
add("units", "poropat_distinct_normalised", "", len(units))


def unit_names(occs, cols):
    return {norm_unit(r[ix[c]]) for r in occs for c in cols if r[ix[c]]}


any_taxon_wide = select(WIDE, False)
cases = (
    ("formation_chordates_original_window", chordates_old, ("formation",)),
    ("formation_chordates_permian_aware_window", chordates_wide, ("formation",)),
    ("formation_member_group_chordates_permian_aware_window", chordates_wide, ("formation", "member", "geological_group")),
    ("formation_member_group_any_taxon_permian_aware_window", any_taxon_wide, ("formation", "member", "geological_group")),
)
for label, occs, cols in cases:
    add("units", f"in_pbdb_{label}", "", len(units & unit_names(occs, cols)))
for u in sorted(units - unit_names(any_taxon_wide, ("formation", "member", "geological_group"))):
    add("units", "not_in_pbdb_any_taxon_permian_aware_window", u, "")

with open(asud_path, newline="", encoding="utf-8") as f:
    asud = defaultdict(list)
    for u in csv.DictReader(f):
        try:
            asud[norm_unit(u["NAME"])].append((float(u["NUMERICYOUNGERAGE"]), float(u["NUMERICOLDERAGE"])))
        except ValueError:
            asud[norm_unit(u["NAME"])].append(None)
add("units", "in_asud_names", "", len(units & set(asud)))
for u in sorted(units - set(asud)):
    near = sorted(a for a in asud if a.startswith(u + " "))
    add("units", "not_in_asud", u, "ASUD names that start with it: " + (", ".join(near) or "none"))


def poropat_age(text):
    s = text.replace("uppermost Permian", "Changhsingian").replace("lowermost Triassic", "Induan") \
        .replace("Lower Triassic", "Induan–Olenekian")
    names = re.findall(r"[A-Z][a-z]+", s)
    assert names and all(n in stage for n in names), text
    return min(stage[n][0] for n in names), max(stage[n][1] for n in names)


age = {}
for r in pr:
    lo, hi = poropat_age(r["age_range"])
    u = norm_unit(r["rock_unit"])
    age[u] = (min(age.get(u, (lo, hi))[0], lo), max(age.get(u, (lo, hi))[1], hi))
gaps = {}
for u in units & set(asud):
    lo, hi = age[u]
    ok = [max(0.0, max(lo, a[0]) - min(hi, a[1])) for a in asud[u] if a]
    gaps[u] = min(ok) if ok else None
add("units", "asud_same_name_age_overlap", "", sum(g == 0 for g in gaps.values() if g is not None))
add("units", "asud_same_name_age_within_5_myr", "", sum(g <= 5 for g in gaps.values() if g is not None))
for u, g in sorted(gaps.items()):
    if g is None or g > 0:
        add("units", "asud_age_gap_myr", u, "no numeric ages" if g is None else f"{g:.1f}; Poropat {age[u][0]:g}-{age[u][1]:g} Ma")

with open(out_path, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
