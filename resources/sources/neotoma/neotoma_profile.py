"""Profile a Neotoma IPPD/Sahul snapshot written by neotoma_snapshot.sh.

Usage: python3 neotoma_profile.py SNAPSHOT_DIR OUT_TSV OUT_DATASETS_TSV

Checks that every dataset in the listings was downloaded, flattens each download
to one row per dataset (type, site, coordinates, region, samples, taxa, units,
default chronology), and writes long-format counts (table, metric, key, value)
for the whole snapshot and for Sahul. Sahul regions as in rpd_profile.py.
Standard library only.
"""

import csv
import glob
import json
import os
import statistics
import sys
from collections import Counter

out = []


def add(*row):
    out.append(row)


def region(lat, lon):
    if lat is None or lon is None:
        return "no_coordinates"
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if lat <= -10.6 and 112 <= lon <= 155:
        return "australia"
    if 130.8 <= lon <= 156 and -12 <= lat <= 0:
        return "new_guinea"
    return "outside"


def lonlat(geography):
    g = json.loads(geography) if geography else None
    if not g:
        return None, None
    if g["type"] == "Point":
        return g["coordinates"]
    ring = g["coordinates"][0]
    return sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring)


snap = sys.argv[1]
listed = set()
for f in glob.glob(os.path.join(snap, "datasets_*.json")):
    with open(f) as fh:
        listed |= {ds["datasetid"] for rec in json.load(fh)["data"] for ds in rec["site"]["datasets"]}
rows = []
for f in sorted(glob.glob(os.path.join(snap, "downloads_*.json"))):
    with open(f) as fh:
        d = json.load(fh)
    assert d["status"] == "success", f
    for rec in d["data"]:
        s = rec["site"]
        cu = s["collectionunit"]
        ds = cu["dataset"]
        lon, lat = lonlat(s["geography"])
        chrons = [c["chronology"] for c in cu.get("chronologies") or [] if c.get("chronology") and c["chronology"].get("chronology")]
        default = next((c for c in chrons if c["chronology"].get("isdefault")), chrons[0] if chrons else None)
        did = default["chronologyid"] if default else None
        ages = [a["age"] for smp in ds["samples"] for a in smp.get("ages") or []
                if a.get("chronologyid") == did and a.get("age") is not None]
        data = [x for smp in ds["samples"] for x in smp.get("datum") or []]
        rows.append({
            "datasetid": ds["datasetid"], "datasettype": ds["datasettype"], "database": ds["database"],
            "siteid": s["siteid"], "sitename": s["sitename"], "lon": lon, "lat": lat,
            "geometry": json.loads(s["geography"])["type"] if s["geography"] else "",
            "country": (s.get("geopolitical") or [""])[0], "region": region(lat, lon),
            "samples": len(ds["samples"]),
            "taxa": len({x["variablename"] for x in data if x.get("ecologicalgroup") != "LABO"}),
            "units": ";".join(sorted({x["units"] for x in data if x.get("ecologicalgroup") != "LABO" and x.get("units")})),
            "chronologies": len(chrons),
            "default_agetype": default["chronology"].get("modelagetype") if default else "",
            "default_agemodel": default["chronology"].get("agemodel") if default else "",
            "default_controls": len(default.get("chroncontrols") or []) if default else 0,
            "max_age_default": max(ages) if ages else "",
            "dois": len(ds.get("doi") or []),
        })
got = {r["datasetid"] for r in rows}
add("check", "datasets_listed", "", len(listed))
add("check", "datasets_downloaded", "", len(got))
add("check", "listed_not_downloaded", "", len(listed - got))
add("check", "duplicate_downloads", "", len(rows) - len(got))
for k, v in Counter(r["database"] for r in rows).most_common():
    add("all", "datasets_by:database", k, v)
for k, v in Counter(r["country"] for r in rows).most_common(15):
    add("all", "datasets_by:country", k, v)
for k, v in Counter(r["region"] for r in rows).most_common():
    add("all", "datasets_by:region", k, v)

sah = [r for r in rows if r["region"] not in ("outside", "no_coordinates")]
add("sahul", "datasets", "", len(sah))
add("sahul", "sites", "", len({r["siteid"] for r in sah}))
for k, v in Counter((r["datasettype"], r["region"]) for r in sah).most_common(30):
    add("sahul", "datasets_by:type_region", f"{k[0]} | {k[1]}", v)
for k, v in Counter(r["geometry"] for r in sah).most_common():
    add("sahul", "datasets_by:geometry", k, v)
pollen = [r for r in sah if r["datasettype"] == "pollen"]
add("sahul_pollen", "datasets", "", len(pollen))
add("sahul_pollen", "sites", "", len({r["siteid"] for r in pollen}))
add("sahul_pollen", "sites_with_multiple_pollen_datasets", "", sum(v > 1 for v in Counter(r["siteid"] for r in pollen).values()))
add("sahul_pollen", "samples", "", sum(r["samples"] for r in pollen))
add("sahul_pollen", "taxa_median_per_dataset", "", statistics.median(r["taxa"] for r in pollen))
for k, v in Counter(r["units"] for r in pollen).most_common(6):
    add("sahul_pollen", "datasets_by:units", k, v)
for k, v in Counter(r["default_agetype"] for r in pollen).most_common(6):
    add("sahul_pollen", "datasets_by:default_agetype", k, v)
for k, v in Counter(r["default_agemodel"] for r in pollen).most_common(12):
    add("sahul_pollen", "datasets_by:default_agemodel", k, v)
add("sahul_pollen", "default_controls_lt_5", "", sum(r["default_controls"] < 5 for r in pollen))
ages = [r["max_age_default"] for r in pollen if r["max_age_default"] != ""]
add("sahul_pollen", "max_age_median", "", round(statistics.median(ages)))
for thr in (2000, 20000, 40000):
    add("sahul_pollen", "max_age_ge", thr, sum(a >= thr for a in ages))
odd = [r for r in pollen if r["default_agetype"].startswith("Calibrated") and r["max_age_default"] != "" and r["max_age_default"] > 55000]
for r in odd:
    add("sahul_pollen", "calibrated_default_age_gt_55ka", f'{r["datasetid"]} {r["sitename"]}', r["max_age_default"])
add("sahul", "datasets_without_doi", "", sum(r["dois"] == 0 for r in sah))
for k, v in Counter(r["datasettype"] for r in sah if r["dois"] == 0).most_common():
    add("sahul", "datasets_without_doi_by:type", k, v)

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
with open(sys.argv[3], "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(sorted(rows, key=lambda r: r["datasetid"]))
