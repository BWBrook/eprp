"""Compare PBDB Quaternary vertebrate localities with FosSahul (March 2021) sites and genera.

Usage: python3 pbdb_fossahul_overlap.py PBDB_SNAPSHOT_DIR FOSSAHUL_CSV OUT_TSV

PBDB side: core and _idng occurrences of Mammalia, Aves, Reptilia and Amphibia whose
interval midpoint is under 2.58 Ma. FosSahul side: records with numeric coordinates.
Reports nearest-neighbour distances between localities in both directions, genus-set
overlap overall and at paired localities, and megafauna genus coverage.
Standard library only.
"""

import csv
import math
import statistics
import sys
from collections import Counter, defaultdict

csv.field_size_limit(1 << 30)
CLASSES = {"Mammalia", "Aves", "Reptilia", "Amphibia"}
out = []


def add(*row):
    out.append(row)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def km(a, b):
    la1, lo1, la2, lo2 = map(math.radians, (a[0], a[1], b[0], b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def nearest(p, pts):
    return min(((km(p, q), k) for k, q in pts.items()), default=(math.inf, None))


snap, fs_csv = sys.argv[1], sys.argv[2]
pb_pts, pb_gen, pb_late = {}, defaultdict(set), set()
pb_all_gen = Counter()
for sfx in ("", "_idng"):
    with open(f"{snap}/occurrences{sfx}.csv", newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        h = next(rd)
        ix = {k: h.index(k) for k in ("collection_no", "lat", "lng", "class", "genus", "max_ma", "min_ma")}
        for r in rd:
            hi, lo = num(r[ix["max_ma"]]), num(r[ix["min_ma"]])
            if r[ix["class"]] not in CLASSES or hi is None or lo is None or (hi + lo) / 2 >= 2.58:
                continue
            cno = r[ix["collection_no"]]
            pb_pts[cno] = (float(r[ix["lat"]]), float(r[ix["lng"]]))
            if hi <= 0.9:
                pb_late.add(cno)
            if r[ix["genus"]]:
                pb_gen[cno].add(r[ix["genus"]])
                pb_all_gen[(r[ix["genus"]], r[ix["class"]])] += 1

fs_pts, fs_gen, fs_mega, fs_names = {}, defaultdict(set), set(), {}
with open(fs_csv, newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        la, lo = num(r["Latitude"]), num(r["Longitude"])
        if la is None or lo is None:
            continue
        k = (round(la, 3), round(lo, 3))
        fs_pts[k] = k
        fs_names[k] = r["Cave.Site.Deposit"]
        g = r["Genus"].strip()
        if g and g.lower() not in ("na", "indet", "indet."):
            fs_gen[k].add(g)
            if r["Megafauna..40kg."].strip() == "Yes":
                fs_mega.add(g)

add("pbdb", "quaternary_tetrapod_collections", "", len(pb_pts))
add("pbdb", "of_which_max_ma_le_0.9", "", len(pb_late))
add("fossahul", "distinct_coordinate_sites_3dp", "", len(fs_pts))
for label, src, dst in (("pbdb_to_fossahul", pb_pts, fs_pts), ("fossahul_to_pbdb", fs_pts, pb_pts)):
    d = [nearest(p, dst)[0] for p in src.values()]
    add(label, "nearest_km_median", "", round(statistics.median(d), 1))
    for thr in (1, 5, 25):
        add(label, "within_km", thr, sum(x <= thr for x in d))

pairs = []
for cno, p in pb_pts.items():
    d, k = nearest(p, fs_pts)
    if d <= 5 and pb_gen[cno]:
        nearby = set().union(*(fs_gen[q] for q in fs_pts if km(p, q) <= 5))
        pairs.append((len(pb_gen[cno] & nearby), len(pb_gen[cno])))
add("paired_within_5km", "pbdb_collections_with_genera", "", len(pairs))
if pairs:
    shares = [s / n for s, n in pairs]
    add("paired_within_5km", "share_of_pbdb_genera_also_in_fossahul_within_5km_median", "", round(statistics.median(shares), 2))
    add("paired_within_5km", "share_mean", "", round(statistics.mean(shares), 2))
    add("paired_within_5km", "pooled_shared_of_collection_genera", "", f"{sum(s for s, _ in pairs)} of {sum(n for _, n in pairs)}")
    add("paired_within_5km", "collections_all_genera_shared", "", sum(s == n for s, n in pairs))
    add("paired_within_5km", "collections_with_no_shared_genus", "", sum(s == 0 for s, _ in pairs))
    add("paired_within_5km", "collections_with_one_genus", "", sum(n == 1 for _, n in pairs))

pg = {g for g, _ in pb_all_gen}
fg = set().union(*fs_gen.values())
add("genera", "pbdb", "", len(pg))
add("genera", "fossahul", "", len(fg))
add("genera", "shared", "", len(pg & fg))
by_class = Counter(c for (g, c) in pb_all_gen if g not in fg)
for c, v in by_class.most_common():
    add("genera", "pbdb_only_by_class", c, v)
add("megafauna", "fossahul_megafauna_genera", "", len(fs_mega))
add("megafauna", "of_which_in_pbdb", "", len(fs_mega & pg))
add("megafauna", "missing_from_pbdb", "", ", ".join(sorted(fs_mega - pg)))
mega_cols = {cno for cno, gs in pb_gen.items() if gs & fs_mega}
add("megafauna", "pbdb_collections_with_fossahul_megafauna_genus", "", len(mega_cols))
far = Counter()
for cno, p in pb_pts.items():
    d, k = nearest(p, fs_pts)
    if d > 25:
        far[tuple(sorted(pb_gen[cno]))[:3]] += 1
add("pbdb_to_fossahul", "collections_gt_25km_from_any_fossahul_site", "", sum(far.values()))

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
