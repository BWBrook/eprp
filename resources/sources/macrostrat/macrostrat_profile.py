"""Profile a Macrostrat snapshot for B-005, B-007 and B-008.

Usage: python3 macrostrat_profile.py SNAPSHOT_DIR PBDB_GLOBAL_RAW OUT_TSV SERIES_TSV

SNAPSHOT_DIR is one dated snapshot (macrostrat_snapshot.sh). Project 14
("core") composites other projects and is left out of every total. Writes
section, project, metric, value rows:
- columns by status and type, area, units, gap-bound sections, ages;
- age support: unit tops and bottoms that sit on an interval edge (t_prop or
  b_prop 0 or 1) and that equal an international stage boundary, and units
  with a geochronological measurement (units of Ma);
- environments of units by class;
- PBDB links: collections, and Macrostrat's occurrence counts against the
  public occurrences in our PBDB snapshot (counts only);
- measurements by name.
SERIES_TSV gives, for each international stage, the summed area of columns
with a marine unit, a non-marine unit and any unit spanning the stage's
midpoint, for North America and for the other land projects. Standard library
only.
"""

import collections
import csv
import glob
import json
import os
import re
import sys

snap, pbdb, out_tsv, series_tsv = sys.argv[1:5]
csv.field_size_limit(1 << 30)
out = []
COMPOSITE = 14
OCEAN = {3, 4}


def put(section, project, metric, value):
    out.append([section, str(project), metric, str(value)])


def counts(c, top=10):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def defs(name):
    return json.load(open(os.path.join(snap, f"defs__{name}.json"), encoding="utf-8"))["success"]["data"]


def rows(name):
    with open(os.path.join(snap, name), newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


projects = {int(p["project_id"]): p["project"] for p in defs("projects")}
put("inputs", "", "environment classes defined", counts(collections.Counter(e["class"] for e in defs("environments"))))
stages = sorted((i for i in defs("intervals") if any(t["timescale_id"] == 1 for t in i["timescales"] or [])),
                key=lambda i: i["t_age"])
edges = {round(float(i["t_age"]), 3) for i in stages} | {round(float(i["b_age"]), 3) for i in stages}
put("inputs", "", "snapshot", os.path.basename(snap.rstrip("/")))
put("inputs", "", "international stages (timescale 1); distinct boundary ages", f"{len(stages)}; {len(edges)}")

# columns
col_info = {}
for p in sorted(projects):
    path = os.path.join(snap, f"columns__p{p:02d}.geojson")
    feats = json.load(open(path, encoding="utf-8"))["success"]["data"]["features"] if os.path.getsize(path) > 200 else []
    props = [f["properties"] for f in feats]
    for c in props:
        col_info[(p, c["col_id"])] = c
    if props:
        put("columns", p, "columns; by status; by type",
            f"{len(props)}; {counts(collections.Counter(c['status_code'] for c in props))}; {counts(collections.Counter(c['col_type'] for c in props))}")
        put("columns", p, "summed column area (km2)", round(sum(num(c["col_area"]) or 0 for c in props)))

# units
coll_public = collections.Counter()
for path in glob.glob(os.path.join(pbdb, "occurrences__p*.csv")):
    with open(path, newline="", encoding="utf-8") as f:
        r = csv.reader(f)
        h = next(r)
        ic = h.index("collection_no")
        for row in r:
            coll_public[row[ic]] += 1
coll_n = {}
for path in glob.glob(os.path.join(pbdb, "collections__p*.csv")):
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            coll_n[row["collection_no"]] = int(row["n_occs"] or 0)

meas_units = collections.defaultdict(set)
for p in sorted(projects):
    path = os.path.join(snap, f"measurements__p{p:02d}.csv")
    if p == COMPOSITE or os.path.getsize(path) < 10:
        continue
    names = collections.Counter()
    n = 0
    for r in rows(f"measurements__p{p:02d}.csv"):
        n += 1
        names[r["measurement"]] += 1
        if r["measure_units"] == "Ma" and r["unit_id"]:
            meas_units[p].add(r["unit_id"])
    put("measurements", p, "rows; distinct measurement names; most common", f"{n}; {len(names)}; {counts(names, 8)}")

series_units = []
for p in sorted(projects):
    if p == COMPOSITE or os.path.getsize(os.path.join(snap, f"units__p{p:02d}.csv")) < 10:
        continue
    us = rows(f"units__p{p:02d}.csv")
    n = len(us)
    secs = {u["section_id"] for u in us}
    ages = [(num(u["t_age"]), num(u["b_age"])) for u in us if num(u["b_age"]) is not None]
    put("units", p, "units; gap-bound sections; columns with units", f"{n}; {len(secs)}; {len({u['col_id'] for u in us})}")
    put("units", p, "units with a numeric base age; oldest base; youngest top (Ma)",
        f"{len(ages)}; {max(b for _, b in ages):g}; {min(t for t, _ in ages if t is not None):g}" if ages else "0")
    edge = sum(1 for u in us for k in ("t_prop", "b_prop") if num(u[k]) in (0.0, 1.0))
    on_stage = sum(1 for u in us for k in ("t_age", "b_age") if num(u[k]) is not None and round(num(u[k]), 3) in edges)
    put("age support", p, "unit tops and bottoms (2 per unit) on an interval edge (prop 0 or 1); equal to an international stage boundary",
        f"{edge} of {2 * n} ({edge / (2 * n):.3f}); {on_stage} ({on_stage / (2 * n):.3f})")
    dated = len(meas_units[p] & {u["unit_id"] for u in us})
    put("age support", p, "units with a geochronological measurement (units of Ma)", f"{dated} ({dated / n:.3f})")
    cls = collections.Counter()
    for u in us:
        envs = [e.split("~")[0].strip() for e in u["environ"].split("|") if e.strip()]
        found = {e.split()[-1] for e in envs}  # each environment is written "name type class"
        cls["marine" if found == {"marine"} else "non-marine" if found == {"non-marine"} else "both" if len(found) > 1
            else "none given" if not envs else "/".join(sorted(found)) or "unmatched"] += 1
        if p not in OCEAN:
            series_units.append((p, u["col_id"], num(u["t_age"]), num(u["b_age"]), found))
    put("environments", p, "units by environment class", counts(cls))
    put("pbdb", p, "units with PBDB collections; summed pbdb_collections; summed pbdb_occurrences",
        f"{sum(1 for u in us if (num(u['pbdb_collections']) or 0) > 0)}; {sum(int(num(u['pbdb_collections']) or 0) for u in us)}; "
        f"{sum(int(num(u['pbdb_occurrences']) or 0) for u in us)}")
    fpath = os.path.join(snap, f"fossils__p{p:02d}.csv")
    if os.path.getsize(fpath) > 10:
        fos = rows(f"fossils__p{p:02d}.csv")
        cl = {}
        for r in fos:
            cl[r["cltn_id"]] = max(cl.get(r["cltn_id"], 0), int(num(r["pbdb_occs"]) or 0))
        nonpublic = [c for c in cl if coll_n.get(c) and not coll_public.get(c)]
        excess = sum(max(0, cl[c] - coll_public.get(c, 0)) for c in cl if c in coll_n)
        put("pbdb", p, "fossil links: rows; distinct collections; Macrostrat occurrences; public occurrences today",
            f"{len(fos)}; {len(cl)}; {sum(cl.values())}; {sum(coll_public.get(c, 0) for c in cl)}")
        put("pbdb", p, "linked collections with no public occurrence today; occurrences counted beyond the public ones; collections not in PBDB today",
            f"{len(nonpublic)}; {excess}; {sum(1 for c in cl if c not in coll_n)}")

# rock area through time, at each stage midpoint
area = {(p, c): num(col_info.get((p, int(c)), {}).get("col_area")) or 0 for p, c, *_ in series_units}
with open(series_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["stage", "mid_ma", "na_marine_km2", "na_nonmarine_km2", "na_any_km2", "na_columns",
                "other_land_marine_km2", "other_land_nonmarine_km2", "other_land_any_km2", "other_land_columns"])
    for s in reversed(stages):
        mid = (float(s["t_age"]) + float(s["b_age"])) / 2
        acc = {k: collections.defaultdict(set) for k in ("marine", "non-marine", "any")}
        for p, c, t, b, found in series_units:
            if t is not None and b is not None and t <= mid <= b:
                region = "na" if p == 1 else "other"
                acc["any"][region].add((p, c))
                for k in ("marine", "non-marine"):
                    if k in found:
                        acc[k][region].add((p, c))
        cell = lambda k, r: round(sum(area[x] for x in acc[k][r]))
        w.writerow([s["name"], round(mid, 3), cell("marine", "na"), cell("non-marine", "na"), cell("any", "na"),
                    len(acc["any"]["na"]), cell("marine", "other"), cell("non-marine", "other"), cell("any", "other"),
                    len(acc["any"]["other"])])

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "project", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
