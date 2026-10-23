"""Profile the global PBDB snapshot written by pbdb_global_snapshot.sh.

Usage: python3 pbdb_global_profile.py GLOBAL_SNAPSHOT OUT_TSV

Reconciles every occurrence and collection partition with its rowcount, checks
that each record's creation time falls inside its partition's window and that
no occurrence or collection appears twice, and compares the total with the
datainfo counts taken before and after the pull. Occurrence rows carry only
record-level fields (see the snapshot script), so country, environment,
formation and coordinates come from the collections table by collection_no.
Measurements (fetched in chunks by specimen) are reconciled per chunk and
checked against the public specimens, and specimens against the public
occurrences.
Counts occurrences by rank, phylum, class, period (interval midpoint, PBDB's
own period table), continent (PBDB's country table), environment, temporal
resolution, coordinates and palaeocoordinates per plate model, creation year,
and modified-before-created; describes the partition stamped 2025-09-21 22:25
(classes, references, countries, ages); and checks the other tables against
their rowcounts. Personal-name columns are never read. Exit status 1 if any
partition fails to reconcile. Writes long-format (table, metric, key, value).
Standard library only.
"""

import csv
import glob
import json
import os
import statistics
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
snap = sys.argv[1]
out = []
BULK = ("2025-09-21 22:25:00", "2025-09-21 22:26:00")
OCC_EDGES = ["", "1999-01-01", "2001-01-01", "2003-01-01", "2005-01-01", "2008-01-01", "2011-01-01",
             "2014-01-01", "2018-01-01", "2022-01-01", BULK[0], BULK[1], ""]
COL_EDGES = ["", "2010-01-01", BULK[0], BULK[1], ""]
AU_CODES = {"AU", "PG", "NF", "CX", "CC", "HM"}
bad = False


def add(*row):
    out.append(row)


def load(name):
    with open(os.path.join(snap, name), encoding="utf-8") as f:
        return json.load(f)


def found(name):
    return load(name)["records_found"]


def rows(path):
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        rd = csv.reader(f)
        head = next(rd)
        idx = {}
        for i, h in enumerate(head):
            idx.setdefault(h, i)
        for r in rd:
            yield idx, r


def check_partition(table, part, files, edges, i, idkey, seen):
    global bad
    lo, hi = edges[i - 1].replace("T", " "), edges[i].replace("T", " ")
    n = outside = dup = 0
    for p in files:
        for idx, r in rows(p):
            n += 1
            c = r[idx["created"]]
            if (lo and c < lo) or (hi and c >= hi):
                outside += 1
            k = r[idx[idkey]]
            if k in seen:
                dup += 1
            seen.add(k)
            yield idx, r
    expected = found(f"count__{table}__{part}.json")
    ok = n == expected and outside == 0 and dup == 0
    bad |= not ok
    add(table, "partition", part, f"rows {n}; rowcount {expected}; created outside window {outside}; duplicates {dup}; {'ok' if ok else 'MISMATCH'}")


with open(os.path.join(snap, "intervals.csv"), newline="", encoding="utf-8") as f:
    periods = sorted(((float(r["b_age"]), float(r["t_age"]), r["interval_name"]) for r in csv.DictReader(f)
                      if r["type"] == "period" and r["scale_no"] == "1"), reverse=True)
continent = {rec["cod"]: rec.get("con", "") for rec in load("config.json")["records"] if rec.get("cfg") == "cou"}


def period_of(mx, mn):
    try:
        mid = (float(mx) + float(mn)) / 2
    except ValueError:
        return "(no age)"
    for top, base, name in periods:
        if base <= mid <= top:
            return name
    return "(outside table)"


coll = {}
seen_col = set()
n_col = 0
for i in range(1, len(COL_EDGES)):
    part = f"p{i:02d}"
    for idx, r in check_partition("collections", part, [os.path.join(snap, f"collections__{part}.csv")], COL_EDGES, i, "collection_no", seen_col):
        n_col += 1
        coll[r[idx["collection_no"]]] = (r[idx["cc"]], r[idx["environment"]], r[idx["formation"]], bool(r[idx["lat"]] and r[idx["lng"]]),
                                         int(r[idx["n_occs"]] or 0))
add("collections", "rows", "", n_col)
add("collections", "by:continent", "AU, PG, NF, CX, CC, HM codes", sum(v[0] in AU_CODES for v in coll.values()))
public_per_coll = Counter()

C = defaultdict(Counter)
spans, n_occ, no_coll = [], 0, 0
seen_occ = set()
bulk = defaultdict(Counter)
for i in range(1, len(OCC_EDGES)):
    part = f"p{i:02d}"
    files = sorted(glob.glob(os.path.join(snap, f"occurrences__{part}*.csv")))
    for idx, r in check_partition("occurrences", part, files, OCC_EDGES, i, "occurrence_no", seen_occ):
        n_occ += 1
        g = lambda k: r[idx[k]]
        cc, env, fm, has_xy, _ = coll.get(g("collection_no"), ("", "", "", False, 0))
        no_coll += g("collection_no") not in coll
        public_per_coll[g("collection_no")] += 1
        C["accepted_rank"][g("accepted_rank") or "(none)"] += 1
        C["phylum"][g("phylum") or "(none)"] += 1
        C["class"][g("class") or "(none)"] += 1
        C["period"][period_of(g("max_ma"), g("min_ma"))] += 1
        C["continent"][continent.get(cc, "") or "(none)"] += 1
        C["environment"][env or "(none)"] += 1
        C["created_year"][g("created")[:4]] += 1
        C["has_reid"]["yes" if g("reid_no") else "no"] += 1
        C["collection_has_coordinates"]["yes" if has_xy else "no"] += 1
        for k, model in (("paleolat", "1"), ("paleolat2", "2"), ("paleolat3", "3")):
            C["palaeolatitude_model_" + model]["yes" if g(k) else "no"] += 1
        C["collection_has_formation"]["yes" if fm else "no"] += 1
        zero = g("modified").startswith("0000") or g("created").startswith("0000")
        C["modified_before_created"]["zero date" if zero else "yes" if g("modified") and g("modified") < g("created") else "no"] += 1
        C["in_au_ng_codes"]["yes" if cc in AU_CODES else "no"] += 1
        try:
            spans.append(float(g("max_ma")) - float(g("min_ma")))
        except ValueError:
            pass
        if part == "p11":
            for k in ("class", "reference_no", "early_interval"):
                bulk[k][g(k) or "(none)"] += 1
            bulk["cc"][cc or "(none)"] += 1
            bulk["collections"][g("collection_no")] += 1
add("occurrences", "rows", "", n_occ)
add("occurrences", "without_collection_row", "", no_coll)
n_occs_sum = sum(v[4] for v in coll.values())
add("collections", "with_a_public_occurrence", "", sum(1 for k in coll if public_per_coll[k]))
add("collections", "n_occs_zero", "", sum(1 for v in coll.values() if v[4] == 0))
add("occurrences", "rowcount_before", "", found("datainfo.json"))
if os.path.exists(os.path.join(snap, "datainfo_end.json")):
    add("occurrences", "rowcount_after", "", found("datainfo_end.json"))
for k, top in (("accepted_rank", None), ("phylum", 20), ("class", 25), ("period", None), ("continent", None),
               ("environment", 15), ("created_year", None), ("has_reid", None), ("collection_has_coordinates", None),
               ("palaeolatitude_model_1", None), ("palaeolatitude_model_2", None), ("palaeolatitude_model_3", None),
               ("collection_has_formation", None), ("modified_before_created", None), ("in_au_ng_codes", None)):
    for v, n in (sorted(C[k].items()) if k == "created_year" else C[k].most_common(top)):
        add("occurrences", f"by:{k}", v, n)
q = statistics.quantiles(spans, n=10)
add("occurrences", "age_span_ma_deciles", "", "; ".join(f"{x:.2f}" for x in q))
add("occurrences", "age_span_ma_median", "", round(statistics.median(spans), 2))
add("bulk_2025_09_21", "occurrences", "", sum(bulk["class"].values()))
add("bulk_2025_09_21", "collections", "", len(bulk["collections"]))
for k in ("class", "cc", "early_interval"):
    for v, n in bulk[k].most_common(10):
        add("bulk_2025_09_21", f"by:{k}", v, n)
refs = {}
for idx, r in rows(os.path.join(snap, "references.csv")):
    refs[r[idx["reference_no"]]] = (r[idx["pubyr"]], r[idx["reftitle"]][:120])
for v, n in bulk["reference_no"].most_common(10):
    add("bulk_2025_09_21", "by:reference", f"{v} {refs.get(v, ('', ''))[0]} {refs.get(v, ('', ''))[1]}", n)
add("bulk_2025_09_21", "references", "", len(bulk["reference_no"]))

for t in ("specimens", "references", "taxa", "opinions"):
    n = sum(1 for _ in rows(os.path.join(snap, f"{t}.csv")))
    ok = n == found(f"count__{t}.json")
    bad |= not ok
    add(t, "rows", "", f"{n}; rowcount {found(f'count__{t}.json')}; {'ok' if ok else 'MISMATCH'}")
spec_ids, spec_orphans = set(), 0
for idx, r in rows(os.path.join(snap, "specimens.csv")):
    spec_ids.add(r[idx["specimen_no"]])
    spec_orphans += r[idx["occurrence_no"]] not in ("", "0") and r[idx["occurrence_no"]] not in seen_occ
add("specimens", "with_an_occurrence_outside_the_public_set", "", spec_orphans)
n_mea = chunks_bad = mea_orphans = 0
for p in sorted(glob.glob(os.path.join(snap, "measurements__c*.csv"))):
    c = os.path.basename(p)[len("measurements__"):-len(".csv")]
    n = 0
    for idx, r in rows(p):
        n += 1
        mea_orphans += r[idx["specimen_no"]] not in spec_ids
    chunks_bad += n != found(f"count__measurements__{c}.json")
    n_mea += n
bad |= bool(chunks_bad or mea_orphans or spec_orphans)
add("measurements", "rows", "", n_mea)
add("measurements", "chunks_not_matching_rowcount", "", chunks_bad)
add("measurements", "with_a_specimen_outside_the_public_set", "", mea_orphans)
add("intervals", "rows", "", sum(1 for _ in rows(os.path.join(snap, "intervals.csv"))))
taxa, blank, n_occs, tno = Counter(), 0, {}, Counter()
for idx, r in rows(os.path.join(snap, "taxa.csv")):
    blank += not r[idx["taxon_rank"]]
    tno[r[idx["taxon_no"]]] += 1
    if r[idx["taxon_no"]] == r[idx["accepted_no"]]:
        taxa[r[idx["accepted_rank"]]] += 1
        if r[idx["taxon_name"]] in ("Mammalia", "Brachiopoda"):
            n_occs[r[idx["taxon_name"]]] = r[idx["n_occs"]]
add("taxa", "taxon_rank_blank", "", blank)
add("taxa", "taxon_no_values_on_several_rows", "", sum(1 for n in tno.values() if n > 1))
for v, n in taxa.most_common(12):
    add("taxa", "accepted_taxa_by:accepted_rank", v, n)

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
sys.exit(1 if bad else 0)
