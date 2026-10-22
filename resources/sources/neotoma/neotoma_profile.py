"""Profile a Neotoma IPPD/Sahul snapshot written by neotoma_snapshot.sh.

Usage: python3 neotoma_profile.py SNAPSHOT_DIR OUT_TSV OUT_DATASETS_TSV

Checks that every dataset in the listings was downloaded, flattens each download
to one row per dataset (type, site, coordinates, region, samples, taxa, units,
chronology), and writes long-format counts (table, metric, key, value) for the
whole snapshot and for Sahul. Sahul regions as in rpd_profile.py.

Neotoma can flag one default chronology per age type. The "API default" is the
first flagged (the collection unit's defaultchronology); the "preferred default"
takes a flagged calibrated or calendar chronology when there is one. Dating
controls are radiocarbon (finite), Pb-210, U-series and "other dating methods";
core tops, interpolations and other tie-points are not. Standard library only.
"""

import csv
import glob
import json
import os
import statistics
import sys
from collections import Counter

DATED = {"Radiocarbon", "Radiocarbon, calibrated", "Radiocarbon, calibrated, Bayesian modelled", "Lead-210",
         "Uranium-series", "Other dating methods"}
out = []


def add(*row):
    out.append(row)


def region(lat, lon):
    if lat is None or lon is None:
        return "no_coordinates"
    if 141 <= lon <= 144.5 and -10.6 < lat <= -9:
        return "torres_strait"
    if -45 <= lat <= -10.6 and 112 <= lon <= 155 and not (lon < 121 and lat > -17):
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
    if ring[0] == ring[-1]:
        ring = ring[:-1]
    return sum(p[0] for p in ring) / len(ring), sum(p[1] for p in ring) / len(ring)


def ages_under(ds, cid):
    return [a["age"] for smp in ds["samples"] for a in smp.get("ages") or [] if a.get("chronologyid") == cid and a.get("age") is not None]


snap = sys.argv[1]
listed, created = set(), {}
for f in glob.glob(os.path.join(snap, "datasets_*.json")):
    with open(f) as fh:
        for rec in json.load(fh)["data"]:
            for ds in rec["site"]["datasets"]:
                listed.add(ds["datasetid"])
                created[ds["datasetid"]] = ds.get("recdatecreated") or ""
rows, dois = [], []
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
        defaults = [c for c in chrons if c["chronology"].get("isdefault")]
        api = defaults[0] if defaults else (chrons[0] if chrons else None)
        pref = next((c for c in defaults if (c["chronology"].get("modelagetype") or "").startswith(("Calibrated", "Calendar"))), api)
        ages = ages_under(ds, pref["chronologyid"]) if pref else []
        controls = pref.get("chroncontrols") or [] if pref else []
        dated = [c for c in controls if c.get("chroncontroltype") in DATED]
        data = [x for smp in ds["samples"] for x in smp.get("datum") or []]
        dois += ds.get("doi") or []
        rows.append({
            "datasetid": ds["datasetid"], "datasettype": ds["datasettype"], "database": ds["database"],
            "siteid": s["siteid"], "sitename": s["sitename"], "collectionunitid": cu["collectionunitid"],
            "lon": round(lon, 5) if lon is not None else "", "lat": round(lat, 5) if lat is not None else "",
            "geometry": json.loads(s["geography"])["type"] if s["geography"] else "",
            "country": (s.get("geopolitical") or [""])[0], "region": region(lat, lon),
            "created": created.get(ds["datasetid"], "")[:10],
            "samples": len(ds["samples"]),
            "taxa": len({x["variablename"] for x in data if x.get("ecologicalgroup") != "LABO"}),
            "units": ";".join(sorted({x["units"] for x in data if x.get("ecologicalgroup") != "LABO" and x.get("units")})),
            "chronologies": len(chrons), "flagged_defaults": len(defaults),
            "api_default_agetype": api["chronology"].get("modelagetype") if api else "",
            "default_agetype": pref["chronology"].get("modelagetype") if pref else "",
            "default_agemodel": pref["chronology"].get("agemodel") if pref else "",
            "default_controls": len(controls), "default_dated_controls": len(dated),
            "oldest_dated_control": max((c["chroncontrolage"] for c in dated if c.get("chroncontrolage") is not None), default=""),
            "max_age_default": max(ages) if ages else "",
            "dois": len(ds.get("doi") or []),
        })
got = {r["datasetid"] for r in rows}
add("check", "datasets_listed", "", len(listed))
add("check", "datasets_downloaded", "", len(got))
add("check", "listed_not_downloaded", "", len(listed - got))
add("check", "duplicate_downloads", "", len(rows) - len(got))
add("check", "doi_strings_and_case_insensitive", "", f"{len(dois)} {len({x.lower() for x in dois})}")
for k, v in Counter(r["database"] for r in rows).most_common():
    add("all", "datasets_by:database", k, v)
for k, v in Counter(r["country"] for r in rows).most_common(20):
    add("all", "datasets_by:country", k, v)
for k, v in Counter(r["region"] for r in rows).most_common():
    add("all", "datasets_by:region", k, v)
add("all", "default_agemodel_labels_distinct", "", len({r["default_agemodel"] for r in rows if r["default_agemodel"]}))

sah = [r for r in rows if r["region"] not in ("outside", "no_coordinates")]
add("sahul", "datasets", "", len(sah))
add("sahul", "proxy_datasets_excluding_geochronologic", "", sum(r["datasettype"] != "geochronologic" for r in sah))
add("sahul", "sites", "", len({r["siteid"] for r in sah}))
for k, v in Counter((r["datasettype"], r["region"]) for r in sah).most_common(30):
    add("sahul", "datasets_by:type_region", f"{k[0]} | {k[1]}", v)
for k, v in Counter(r["geometry"] for r in sah).most_common():
    add("sahul", "datasets_by:geometry", k, v)
for t in ("pollen", "pollen surface sample"):
    for k, v in sorted(Counter(r["created"][:4] for r in sah if r["datasettype"] == t).items()):
        add("sahul", f"created_year:{t}", k, v)
pollen = [r for r in sah if r["datasettype"] == "pollen"]
t = "sahul_pollen"
add(t, "datasets", "", len(pollen))
add(t, "sites", "", len({r["siteid"] for r in pollen}))
multi = Counter(r["siteid"] for r in pollen)
add(t, "sites_with_multiple_pollen_datasets", "", sum(v > 1 for v in multi.values()))
add(t, "of_which_sharing_a_collection_unit", "", sum(1 for s, v in multi.items() if v > 1 and len({r["collectionunitid"] for r in pollen if r["siteid"] == s}) < v))
add(t, "samples", "", sum(r["samples"] for r in pollen))
add(t, "taxa_median_per_dataset", "", statistics.median(r["taxa"] for r in pollen))
for k, v in Counter(r["units"] for r in pollen).most_common(10):
    add(t, "datasets_by:units", k, v)
add(t, "datasets_with_several_flagged_defaults", "", sum(r["flagged_defaults"] > 1 for r in pollen))
for k, v in Counter(r["api_default_agetype"] for r in pollen).most_common(6):
    add(t, "datasets_by:api_default_agetype", k, v)
for k, v in Counter(r["default_agetype"] for r in pollen).most_common(6):
    add(t, "datasets_by:preferred_default_agetype", k, v)
for k, v in Counter(r["default_agemodel"] for r in pollen).most_common(30):
    add(t, "datasets_by:default_agemodel", k, v)
add(t, "default_agemodel_labels_distinct", "", len({r["default_agemodel"] for r in pollen if r["default_agemodel"]}))
add(t, "default_controls_lt_5", "", sum(r["default_controls"] < 5 for r in pollen))
for n in (5, 3, 1):
    add(t, "default_dated_controls_lt", n, sum(r["default_dated_controls"] < n for r in pollen))
aged = [r for r in pollen if r["max_age_default"] != ""]
add(t, "datasets_with_default_ages", "", len(aged))
add(t, "max_age_median", "", round(statistics.median(r["max_age_default"] for r in aged)))
for thr in (2000, 20000, 40000):
    add(t, "max_age_ge", thr, sum(r["max_age_default"] >= thr for r in aged))
for r in aged:
    oc = r["oldest_dated_control"]
    if r["max_age_default"] >= 20000 and oc != "" and r["max_age_default"] > 1.2 * oc:
        add(t, "ages_beyond_oldest_dated_control_by_20pct", f'{r["datasetid"]} {r["sitename"]}', f'max {r["max_age_default"]}; oldest dated control {oc}; {r["default_agetype"]}')
long_rc = [r for r in aged if r["default_agetype"].startswith(("Calibrated radiocarbon", "Radiocarbon")) and r["max_age_default"] > 50000]
for r in long_rc:
    add(t, "radiocarbon_type_ages_gt_50ka", f'{r["datasetid"]} {r["sitename"]}', f'{r["max_age_default"]} ({r["default_agetype"]})')
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
