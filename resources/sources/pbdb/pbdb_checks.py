"""Targeted checks behind the PBDB entry's claims, on the Australia and New Guinea region.

Usage: python3 pbdb_checks.py REGION_DIR INTERVALS_CSV OUT_TSV

REGION_DIR is pbdb_region.py's output. Covers: Australian state labels;
Quaternary composition; plate-model coverage and GPlates-Scotese palaeolatitude
differences by period; which time-scale boundary values the ages use;
timestamps; direct ages; qualifiers and `species not entered`; difference
codes; ocean-drilling collections; the Indonesian box; and coordinate sanity.
Writes long-format counts
(table, metric, key, value). Standard library only.
"""

import csv
import re
import statistics
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
PERIODS = [(0, 2.58, "Quaternary"), (2.58, 23.04, "Neogene"), (23.04, 66.0, "Paleogene"), (66.0, 143.1, "Cretaceous"),
           (143.1, 201.4, "Jurassic"), (201.4, 251.902, "Triassic"), (251.902, 298.9, "Permian"),
           (298.9, 358.86, "Carboniferous"), (358.86, 419.62, "Devonian"), (419.62, 443.1, "Silurian"),
           (443.1, 486.85, "Ordovician"), (486.85, 538.8, "Cambrian"), (538.8, 4600.0, "Precambrian")]
STATES = {"Queensland", "New South Wales", "Victoria", "Western Australia", "South Australia", "Tasmania",
          "Northern Territory", "Australian Capital Territory"}
PLANTS = {"Angiospermae", "Gymnospermae", "Pteridophyta", "Equisetophyta", "Lycopodiophyta", "Spermatophyta",
          "Anthocerophyta", "Bryophyta"}
out = []


def add(*row):
    out.append(row)


def tab(table, metric, values, n=50):
    for k, v in Counter(values).most_common(n):
        add(table, metric, k, v)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def mid(r):
    lo, hi = num(r["min_ma"]), num(r["max_ma"])
    return None if lo is None or hi is None else (lo + hi) / 2


def period(m):
    return "no age" if m is None else next(n for a, b, n in PERIODS if a <= m < b)


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        h = next(rd)
        first = {}
        for i, k in enumerate(h):
            first.setdefault(k, i)
        return [{k: r[i] for k, i in first.items()} for r in rd]


snap = sys.argv[1]
occ, col = load(f"{snap}/occurrences.csv"), load(f"{snap}/collections.csv")
occ_id, col_id = load(f"{snap}/occurrences_idng.csv"), load(f"{snap}/collections_idng.csv")

t = "state_labels_au"
au = [r for r in occ if r["cc"] == "AU"]
add(t, "occurrences", "", len(au))


def label_class(s):
    if s in STATES:
        return "canonical"
    if not s.strip():
        return "blank"
    if s.strip() == "Macquarie Island":
        return "Macquarie Island"
    if any(s.strip().lower().replace(" ", "")[:6] == x.lower().replace(" ", "")[:6] for x in STATES) or \
            re.match(r"(?i)(northern|northwest|north west) terr|australian capital|queel|west australia|new south", s.strip()):
        return "variant of a state or territory name"
    return "sub-state place name"


tab(t, "by:class", [label_class(r["state"]) for r in au])
tab(t, "non_canonical_labels", [r["state"] for r in au if label_class(r["state"]) != "canonical"])
tab("state_labels_all", "blank_by:cc", [r["cc"] for r in occ if not r["state"].strip()])

t = "quaternary"
q = [r for r in occ if (m := mid(r)) is not None and m < 2.58]
add(t, "occurrences", "", len(q))
add(t, "occurrences_max_ma_gt_2.58", "", sum(num(r["max_ma"]) > 2.58 for r in q))
tab(t, "by:enterer", [r["enterer"] for r in q], 8)
tab(t, "by:reference", [f'{r["ref_author"]} {r["ref_pubyr"]}' for r in q], 15)
jar = [r for r in q if r["enterer"] == "C. Jaramillo"]
tab(t, "jaramillo_by:phylum", [r["phylum"] for r in jar], 8)
tab(t, "jaramillo_by:plant_organ", [r["plant_organ"] for r in jar], 6)
add(t, "plant_phyla_other_enterers", "", sum(r["phylum"] in PLANTS for r in q if r["enterer"] != "C. Jaramillo"))
tab(t, "chordata_by:class", [r["class"] for r in q if r["phylum"] == "Chordata"])
tab(t, "anthozoa_by:reference", [f'{r["ref_author"]} {r["ref_pubyr"]}' for r in q if r["class"] == "Anthozoa"], 6)
tab(t, "cave_like_by:formation_blank", [bool(r["formation"].strip()) for r in q if r["environment"] in ("cave", "fissure fill", "sinkhole", "karst indet.")])

t = "plate_models"
col_mid = {r["collection_no"]: mid(r) for r in col}
for k, name in (("", "gplates"), ("2", "scotese"), ("3", "seton")):
    ok = [col_mid[r["collection_no"]] for r in col if num(r["paleolat" + k]) is not None]
    add(t, "computed", name, len(ok))
    add(t, "computed_midpoint_range", name, f"{min(ok):.3f} to {max(ok):.1f}")
by_p = defaultdict(list)
for r in col:
    a, b = num(r["paleolat"]), num(r["paleolat2"])
    if a is not None and b is not None:
        by_p[period(col_mid[r["collection_no"]])].append(abs(a - b))
for p in [n for _, _, n in PERIODS]:
    if by_p[p]:
        add(t, "abs_dlat_gplates_scotese_median_by_period", p, round(statistics.median(by_p[p]), 1))
        add(t, "abs_dlat_gt_10_by_period", p, f"{sum(x > 10 for x in by_p[p])} of {len(by_p[p])}")
qo = [r for r in occ if (m := mid(r)) is not None and m < 2.58]
add(t, "quaternary_occurrences_without_gplates", "", f"{sum(num(r['paleolat']) is None for r in qo)} of {len(qo)}")
young = [r for r in occ if (m := mid(r)) is not None and m < 0.39]
add(t, "occurrences_midpoint_lt_0.39_without_gplates", "", f"{sum(num(r['paleolat']) is None for r in young)} of {len(young)}")

t = "time_scale_values"
bounds = Counter(v for r in occ for v in (r["max_ma"], r["min_ma"]))
for v in ("11.63", "11.608", "143.1", "145", "419.62", "419.2", "358.86", "358.9", "443.1", "443.8", "486.85", "485.4",
          "538.8", "541", "251.902", "252.17", "23.04", "23.03"):
    add(t, "count_in_max_or_min_ma", v, bounds[v])
with open(sys.argv[2], newline="", encoding="utf-8") as f:
    scale1 = set()
    for r in csv.DictReader(f):
        if r["scale_no"] == "1":
            scale1 |= {float(r["b_age"]), float(r["t_age"])}
for c in ("max_ma", "min_ma"):
    add(t, f"{c}_equal_to_a_scale1_boundary", "", f"{sum(num(r[c]) in scale1 for r in occ)} of {len(occ)}")

t = "timestamps"
tab(t, "collections_modified_top", [r["modified"] for r in col], 3)
add(t, "occurrences_with_collection_bulk_modified_date", "", sum(r["modified"].startswith("2025-02-22") for r in occ))
valid = [r for r in occ if r["created"] and r["modified"] and not r["created"].startswith("0000") and not r["modified"].startswith("0000")]
bad = [r for r in valid if r["modified"] < r["created"]]
add(t, "occurrences_modified_before_created", "", f"{len(bad)} of {len(occ)}")
tab(t, "occurrences_modified_before_created_by:created_year", [r["created"][:4] for r in bad], 6)
add(t, "occurrences_zero_dates", "", len(occ) - len(valid))
add(t, "collections_modified_before_created", "", sum(r["modified"] < r["created"] for r in col if r["created"][:1] != "0" and r["modified"][:1] != "0"))
tab(t, "occurrences_created_top_days", [r["created"][:10] for r in occ], 3)
add(t, "updated_or_updater_nonblank", "", sum(bool(r.get("updated") or r.get("updater")) for r in occ))

t = "period_binning"
cuts = [b for _, b, _ in PERIODS[:-1]]
strad = [r for r in occ if num(r["max_ma"]) is not None and any(num(r["min_ma"]) < c < num(r["max_ma"]) for c in cuts)]
add(t, "occurrences_spanning_a_period_boundary", "", f"{len(strad)} of {len(occ)}")
tab(t, "spanning_by:midpoint_period", [period(mid(r)) for r in strad], 14)

t = "misc_counts"
add(t, "pseudofossil_occurrences", "", sum("Pseudofossil" in r["identified_name"] for r in occ))
spm = load(f"{snap}/specimens.csv")
add(t, "specimens_permian_brachiopods", "", f'{sum(r["phylum"] == "Brachiopoda" and period(mid(r)) == "Permian" for r in spm)} of {len(spm)}')
tet = {r["collection_no"]: r["cc"] for r in occ if r["class"] in ("Mammalia", "Aves", "Reptilia", "Amphibia") and (m := mid(r)) is not None and m < 2.58}
tab(t, "quaternary_tetrapod_collections_by:cc", tet.values())

t = "direct_ages"
d = [r for r in occ if r["direct_ma_value"]]
add(t, "occurrences", "", len(d))
add(t, "collections", "", len({r["collection_no"] for r in d}))
tab(t, "occurrences_by:reference", [f'{r["ref_author"]} {r["ref_pubyr"]}' for r in d], 3)
for m in sorted({r["direct_ma_method"] for r in d}):
    add(t, "occurrences_and_collections_by:method", m, f'{sum(r["direct_ma_method"] == m for r in d)} in {len({r["collection_no"] for r in d if r["direct_ma_method"] == m})}')

t = "identification"
sp = [r for r in occ if r["identified_rank"] == "species"]
add(t, "species_rank_identifications", "", len(sp))
add(t, "species_rank_with_species_not_entered", "", sum("species not entered" in r["difference"] for r in sp))
tab(t, "species_not_entered_exact_code_by:identified_rank", [r["identified_rank"] for r in occ if r["difference"] == "species not entered"], 8)


def qual(name):
    q = bool(re.search(r"(\bcf\.|\baff\.|\?)", name))
    nsp = " n. sp." in name or " n. gen." in name
    ph = bool(re.search(r"\b(sp|spp|indet)\.", name)) and not nsp
    return f"{'cf/aff/?' if q else ''}{'+' if q and (nsp or ph) else ''}{'n. sp.' if nsp else 'sp./indet.' if ph else ''}" or "none"


tab(t, "identified_name_partition", [qual(r["identified_name"]) for r in occ])
tab(t, "difference_codes_all", [r["difference"] for r in occ], 30)

t = "collections_misc"
drill = [r for r in col if re.search(r"\b(DSDP|ODP|IODP)\b|\bSites? \d{3,4}\b|\bLeg \d+", r["collection_name"])]
add(t, "ocean_drilling_named", "", len(drill))
for r in drill:
    add(t, "ocean_drilling_example", r["collection_no"], f'{r["collection_name"][:80]} | {r["n_occs"]} occs')
add(t, "au_lng_negative_or_lat_positive", "", sum(num(r["lng"]) < 0 or num(r["lat"]) > 0 for r in col if r["cc"] == "AU"))
add(t, "pg_lat_positive", "", sum(num(r["lat"]) > 0 for r in col if r["cc"] == "PG"))
add(t, "extant_distribution_pseudo_collections", "", sum("Extant" in r["collection_name"] for r in col + col_id))

t = "indonesian_box"
seram = {r["collection_no"] for r in col_id if re.search(r"(?i)seram|ceram", r["collection_name"] + r["state"])}
add(t, "collections", "", len(col_id))
add(t, "seram_collections", "", len(seram))
add(t, "seram_occurrences", "", sum(r["collection_no"] in seram for r in occ_id))
add(t, "other_occurrences", "", sum(r["collection_no"] not in seram for r in occ_id))
tab(t, "occurrences_by:state", [r["state"] for r in occ_id])

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
