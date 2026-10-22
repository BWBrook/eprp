"""Profile a PBDB regional extract written by pbdb_snapshot.sh (data_mirror.py url).

Usage: python3 pbdb_profile.py SNAPSHOT_DIR SUFFIX OUT_TSV
SUFFIX is "" for the core extract or "_idng" for the Indonesian box (New Guinea,
Raja Ampat, Misool and Seram).

Writes long-format counts (table, metric, key, value). Checks every CSV row count
against the provider count file, checks duplicated CSV columns are identical, then
profiles geography, time (period of the interval midpoint, on the GTS2020-era
boundaries PBDB's ages use), age resolution,
taxonomy, plate models, entry history, specimens, references and strata.
Standard library only.
"""

import csv
import json
import os
import statistics
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
PERIODS = [(0, 2.58, "Quaternary"), (2.58, 23.04, "Neogene"), (23.04, 66.0, "Paleogene"), (66.0, 143.1, "Cretaceous"),
           (143.1, 201.4, "Jurassic"), (201.4, 251.902, "Triassic"), (251.902, 298.9, "Permian"),
           (298.9, 358.86, "Carboniferous"), (358.86, 419.62, "Devonian"), (419.62, 443.1, "Silurian"),
           (443.1, 486.85, "Ordovician"), (486.85, 538.8, "Cambrian"), (538.8, 635.0, "Ediacaran"),
           (635.0, 4600.0, "pre-Ediacaran")]
COUNT_FILES = {"collections": "colls-list", "specimens": "specs-list", "measurements": "specs-measurements",
               "references": "occs-refs", "taxa": "occs-taxa", "strata": "occs-strata"}
out = []


def add(table, metric, key, value):
    out.append((table, metric, key, value))


def tab(table, metric, values, n=25):
    for k, v in Counter(values).most_common(n):
        add(table, metric, k, v)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def period(r):
    lo, hi = num(r.get("min_ma")), num(r.get("max_ma"))
    if lo is None or hi is None:
        return "no age"
    mid = (lo + hi) / 2
    return next(name for a, b, name in PERIODS if a <= mid < b)


def load(name):
    with open(os.path.join(snap, name + sfx + ".csv"), newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        header = next(rd)
        rows = list(rd)
    first = {}
    for i, h in enumerate(header):
        first.setdefault(h, i)
    dup_bad = 0
    for i, h in enumerate(header):
        if first[h] != i:
            dup_bad += sum(r[i] != r[first[h]] for r in rows)
    add(name, "duplicated_column_names", "", len(header) - len(first))
    add(name, "duplicated_column_value_mismatches", "", dup_bad)
    return [{h: r[i] for h, i in first.items()} for r in rows]


def provider_count(fname):
    with open(os.path.join(snap, fname)) as f:
        return json.load(f)["records_found"]


def history(table, rows):
    tab(table, "created_year", [r["created"][:4] for r in rows], 40)
    tab(table, "modified_date_top", [r["modified"][:10] for r in rows], 5)
    tab(table, "enterer_top", [r["enterer"] for r in rows], 10)


def models(table, rows):
    for k in ("", "2", "3"):
        name = Counter(r["paleomodel" + k] for r in rows).most_common(1)[0][0]
        ok = sum(num(r["paleolat" + k]) is not None for r in rows)
        add(table, "paleocoords_computed", name, ok)
    d = [abs(num(r["paleolat"]) - num(r["paleolat2"])) for r in rows
         if num(r["paleolat"]) is not None and num(r["paleolat2"]) is not None]
    if d:
        add(table, "abs_paleolat_diff_gplates_vs_scotese_median_deg", "", round(statistics.median(d), 2))
        for thr in (5, 10, 20):
            add(table, "abs_paleolat_diff_gplates_vs_scotese_gt_deg", thr, sum(x > thr for x in d))
    tab(table, "by:geoplate", [r["geoplate"] for r in rows], 10)


snap, sfx = sys.argv[1], sys.argv[2]
tables = {n: load(n) for n in ("occurrences", "collections", "specimens", "measurements", "references", "taxa", "strata")}
add("check", "occurrences_rows_vs_datainfo", provider_count(f"datainfo{sfx}.json"), len(tables["occurrences"]))
for n, c in COUNT_FILES.items():
    add("check", f"{n}_rows_vs_count", provider_count(f"count{sfx}-{c}.json"), len(tables[n]))

occ, col = tables["occurrences"], tables["collections"]
t = "occurrences"
add(t, "rows", "", len(occ))
add(t, "distinct_occurrence_no", "", len({r["occurrence_no"] for r in occ}))
add(t, "rows_with_reid_no", "", sum(r["reid_no"] not in ("", "0") for r in occ))
add(t, "distinct_collections", "", len({r["collection_no"] for r in occ}))
tab(t, "by:cc", [r["cc"] for r in occ])
tab(t, "by:state", [r["state"] for r in occ], 30)
tab(t, "by:period_of_interval_midpoint", [period(r) for r in occ], 20)
spans = [num(r["max_ma"]) - num(r["min_ma"]) for r in occ if num(r["max_ma"]) is not None and num(r["min_ma"]) is not None]
add(t, "age_span_myr_median", "", round(statistics.median(spans), 3))
for thr in (1, 5, 10, 20):
    add(t, "age_span_gt_myr", thr, sum(s > thr for s in spans))
add(t, "with_direct_ma_value", "", sum(bool(r["direct_ma_value"]) for r in occ))
tab(t, "by:direct_ma_method", [r["direct_ma_method"] for r in occ if r["direct_ma_method"]], 10)
tab(t, "by:phylum", [r["phylum"] for r in occ], 20)
tab(t, "by:class", [r["class"] for r in occ], 30)
tab(t, "by:accepted_rank", [r["accepted_rank"] for r in occ])
tab(t, "by:identified_rank", [r["identified_rank"] for r in occ])
add(t, "identified_name_open_nomenclature", "", sum(any(q in r["identified_name"] for q in (" cf.", " aff.", "?", " sp.", " indet.", " n. sp.")) for r in occ))
add(t, "accepted_name_blank", "", sum(not r["accepted_name"] for r in occ))
tab(t, "by:difference", [r["difference"] for r in occ], 10)
tab(t, "by:environment", [r["environment"] for r in occ], 20)
add(t, "rows_with_abundance", "", sum(bool(r["abund_value"]) for r in occ))
tab(t, "by:abund_unit", [r["abund_unit"] for r in occ if r["abund_value"]], 10)
add(t, "distinct_accepted_names", "", len({r["accepted_name"] for r in occ if r["accepted_name"]}))
add(t, "with_formation", "", sum(bool(r["formation"]) for r in occ))
quat = [r for r in occ if period(r) == "Quaternary"]
tab(t, "quaternary_by:class", [r["class"] for r in quat], 15)
tab(t, "quaternary_by:environment", [r["environment"] for r in quat], 10)
add(t, "quaternary_chordate_genera", "", len({r["genus"] for r in quat if r["phylum"] == "Chordata" and r["genus"]}))
history(t, occ)

t = "collections"
add(t, "rows", "", len(col))
add(t, "with_zero_occurrences", "", sum(r["n_occs"] == "0" for r in col))
tab(t, "by:cc", [r["cc"] for r in col])
tab(t, "by:state", [r["state"] for r in col], 30)
tab(t, "by:latlng_precision", [r["latlng_precision"] for r in col])
tab(t, "by:latlng_basis", [r["latlng_basis"] for r in col])
tab(t, "by:geogscale", [r["geogscale"] for r in col])
add(t, "with_formation", "", sum(bool(r["formation"]) for r in col))
add(t, "with_geological_group", "", sum(bool(r["geological_group"]) for r in col))
add(t, "with_member", "", sum(bool(r["member"]) for r in col))
add(t, "with_zone", "", sum(bool(r["zone"]) for r in col))
for k in ("collection_type", "environment", "lithology1", "stratscale", "temporal_resolution", "access_level"):
    if k in col[0]:
        tab(t, f"by:{k}", [r[k] for r in col], 15)
tab(t, "by:period_of_interval_midpoint", [period(r) for r in col], 20)
models(t, col)
history(t, col)
tab(t, "top_references_by_collections", [r["reference_no"] for r in col], 10)

t = "specimens"
spm = tables["specimens"]
add(t, "rows", "", len(spm))
tab(t, "by:class", [r["class"] for r in spm], 10)
tab(t, "by:is_type", [r["is_type"] for r in spm], 10)
tab(t, "by:specimen_part", [r["specimen_part"] for r in spm], 10)
add(t, "distinct_occurrences", "", len({r["occurrence_no"] for r in spm if r["occurrence_no"] not in ("", "0")}))
mea = tables["measurements"]
add("measurements", "rows", "", len(mea))
tab("measurements", "by:measurement_type", [r["measurement_type"] for r in mea], 15)
tab("measurements", "by:class", [r["class"] for r in mea], 10)

t = "references"
ref = tables["references"]
add(t, "rows", "", len(ref))
tab(t, "by:publication_type", [r["publication_type"] for r in ref])
add(t, "with_doi", "", sum(bool(r["doi"]) for r in ref))
years = [int(r["pubyr"]) for r in ref if r["pubyr"].isdigit()]
if years:
    add(t, "pubyr_range", "", f"{min(years)} to {max(years)}")
tab(t, "by:decade", [f"{y // 10 * 10}s" for y in years], 25)
tab(t, "by:language", [r["language"] for r in ref], 5)

t = "taxa"
tax = tables["taxa"]
add(t, "rows", "", len(tax))
tab(t, "by:taxon_rank", [r["taxon_rank"] for r in tax])
tab(t, "by:is_extant", [r["is_extant"] for r in tax])

t = "strata"
stra = tables["strata"]
add(t, "rows", "", len(stra))
add(t, "with_formation", "", sum(bool(r["formation"]) for r in stra))
add(t, "distinct_formations", "", len({r["formation"] for r in stra if r["formation"]}))
add(t, "distinct_groups", "", len({r["group"] for r in stra if r["group"]}))
for r in sorted(stra, key=lambda r: -int(r["n_occs"] or 0))[:15]:
    add(t, "top_strata_by_occs", f'{r["group"]} | {r["formation"]} | {r["member"]}', r["n_occs"])

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
