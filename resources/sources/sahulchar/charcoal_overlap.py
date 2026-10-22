"""Compare Sahul charcoal records across SahulCHAR, RPD v1b, GCD 4.0.7 and Neotoma by location.

Usage: python3 charcoal_overlap.py SAHULCHAR_UNITS_CSV RPD_CSV_ZIP GCD_SITES_TSV NEOTOMA_DATASETS_TSV OUT_TSV

Each source is reduced to Sahul record locations (regions as in rpd_profile.py):
SahulCHAR cores, RPD entities, GCD sites, Neotoma charcoal datasets. For each
pair of sources, counts records with a record of the other source within 0.02
and 0.05 degrees (about 2 and 5 km). Then clusters all locations within 0.02
degrees to estimate distinct places and how many sources hold each.
Location matching is a heuristic, not an identity check. Standard library only.
"""

import csv
import io
import sys
import zipfile
from collections import Counter

out = []


def add(*row):
    out.append(row)


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def region(lat, lon):
    if lat is None or lon is None:
        return None
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if -45 <= lat <= -10.6 and 112 <= lon <= 155 and not (lon < 121 and lat > -17):
        return "australia"
    if 130.8 <= lon <= 156 and -12 <= lat <= 0:
        return "new_guinea"
    return None


def keep(points):
    return [(la, lo) for la, lo in points if region(la, lo)]


with open(sys.argv[1], newline="", encoding="utf-8") as f:
    sc = keep((num(u["Y_WGS84"]), num(u["X_WGS84"])) for u in csv.DictReader(f))
z = zipfile.ZipFile(sys.argv[2])
name = next(n for n in z.namelist() if n.startswith("rpd_csv_files/rpd_entity_tb_") and n.endswith(".csv"))
with z.open(name) as f:
    rpd = keep((num(e["latitude"]), num(e["longitude"])) for e in csv.DictReader(io.TextIOWrapper(f, encoding="utf-8-sig")))
with open(sys.argv[3], newline="", encoding="utf-8") as f:
    gcd = keep((num(s["lat"]), num(s["long"])) for s in csv.DictReader(f, delimiter="\t"))
with open(sys.argv[4], newline="", encoding="utf-8") as f:
    neo = keep((num(r["lat"]), num(r["lon"])) for r in csv.DictReader(f, delimiter="\t") if r["datasettype"] == "charcoal")
sources = {"sahulchar": sc, "rpd": rpd, "gcd": gcd, "neotoma": neo}
for k, v in sources.items():
    add("records", "sahul", k, len(v))


def near(p, pts, tol):
    return any(abs(p[0] - q[0]) <= tol and abs(p[1] - q[1]) <= tol for q in pts)


for a, pa in sources.items():
    for b, pb in sources.items():
        if a != b:
            for tol in (0.02, 0.05):
                add("pairwise", f"{a}_records_with_{b}_within_deg", tol, sum(near(p, pb, tol) for p in pa))

clusters = []
for src, pts in sources.items():
    for p in pts:
        for c in clusters:
            if abs(p[0] - c["lat"]) <= 0.02 and abs(p[1] - c["lon"]) <= 0.02:
                c["sources"].add(src)
                break
        else:
            clusters.append({"lat": p[0], "lon": p[1], "sources": {src}})
add("places", "distinct_within_0.02deg", "", len(clusters))
for k, v in Counter(len(c["sources"]) for c in clusters).most_common():
    add("places", "by_number_of_sources", k, v)
for k, v in Counter(tuple(sorted(c["sources"])) for c in clusters).most_common(12):
    add("places", "by_source_combination", "+".join(k), v)
for src in sources:
    add("places", "only_in", src, sum(c["sources"] == {src} for c in clusters))

with open(sys.argv[5], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
