"""Profile a Macrostrat snapshot for B-005, B-007 and B-008.

Usage: python3 macrostrat_profile.py SNAPSHOT_DIR PBDB_GLOBAL_RAW OUT_TSV SERIES_TSV [AGE_MODEL_DIR]

SNAPSHOT_DIR is one dated api snapshot (macrostrat_snapshot.sh); AGE_MODEL_DIR,
if given, the matching age-model snapshot. Project 14 ("core") composites
other projects and is left out of every total. Writes section, project,
metric, value rows:
- reconciliation with the stats route and the definition tables; sections
  and fossil links against what the units imply;
- columns, units, gap-bound sections, unit spans;
- age support: age-bearing Phanerozoic unit tops and bottoms on an interval
  edge and on an international stage boundary, by age band, against a chance
  baseline (boundaries interpolated inside an interval); distinct
  column-age boundaries; dates in units of Ma split into igneous or ash
  samples (their median compared with the unit's age range) and other
  samples (detrital spectra); the age models' boundary statuses;
- environments of units by class;
- PBDB links against our public PBDB snapshot (counts only);
- measurements by name.
SERIES_TSV gives, for each international stage, the summed area of active
columns with a marine, a non-marine and any unit spanning the stage's
midpoint, for North America (project 1), the North American Ediacaran
project (10, nested in North America) and the other land projects, and for
North America the same using only units spanning 5 Myr or less. Standard
library only.
"""

import collections
import csv
import glob
import json
import os
import re
import statistics
import sys

snap, pbdb, out_tsv, series_tsv = sys.argv[1:5]
age_dir = sys.argv[5] if len(sys.argv) > 5 else None
csv.field_size_limit(1 << 30)
out = []
COMPOSITE, OCEAN, NA, EDIACARAN = 14, {3, 4}, 1, 10


def put(section, project, metric, value):
    out.append([section, str(project), metric, str(value)])


def counts(c, top=10):
    return "; ".join(f"{k or '(blank)'} {v}" for k, v in c.most_common(top))


def defs(name):
    return json.load(open(os.path.join(snap, f"defs__{name}.json"), encoding="utf-8"))["success"]["data"]


def rows(name):
    path = os.path.join(snap, name)
    if not os.path.exists(path) or os.path.getsize(path) < 10:
        return []
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def share(a, b):
    return f"{a} of {b} ({a / b:.3f})" if b else f"{a} of 0"


projects = {int(p["project_id"]): p["project"] for p in defs("projects")}
lith_def = {str(x["lith_id"]): x for x in defs("lithologies")}
stages = sorted((i for i in defs("intervals") if any(t["timescale_id"] == 1 for t in i["timescales"] or [])),
                key=lambda i: i["t_age"])
edges = {round(float(i["t_age"]), 3) for i in stages} | {round(float(i["b_age"]), 3) for i in stages}
put("inputs", "", "snapshot", os.path.basename(snap.rstrip("/")))
put("inputs", "", "international stages (timescale 1); distinct boundary ages", f"{len(stages)}; {len(edges)}")
put("inputs", "", "definition tables: intervals; lithologies; environments (by class); measurement types; strat names; strat-name concepts",
    f"{len(defs('intervals'))}; {len(lith_def)}; {len(defs('environments'))} ({counts(collections.Counter(e['class'] for e in defs('environments')))}); "
    f"{len(defs('measurements'))}; {len(defs('strat_names'))}; {len(defs('strat_name_concepts'))}")
stats = {int(r["project_id"]): r for r in rows("stats.csv")}

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

col_info, series_units = {}, []
for p in sorted(projects):
    path = os.path.join(snap, f"columns__p{p:02d}.geojson")
    feats = json.load(open(path, encoding="utf-8"))["success"]["data"]["features"] if os.path.getsize(path) > 200 else []
    props = [f["properties"] for f in feats]
    for c in props:
        col_info[(p, str(c["col_id"]))] = c
    us = rows(f"units__p{p:02d}.csv")
    if not props and not us:
        continue
    st = stats.get(p, {})
    if p != COMPOSITE:
        put("reconcile", p, "columns; units; sections from units — snapshot against the stats route",
            f"{len(props)} / {st.get('columns')}; {len(us)} / {st.get('units')}; {len({u['section_id'] for u in us})} / {st.get('packages')}")
    put("columns", p, "columns; by status; by type",
        f"{len(props)}; {counts(collections.Counter(c['status_code'] for c in props))}; {counts(collections.Counter(c['col_type'] for c in props))}")
    put("columns", p, "summed column area, km2: all statuses; active only",
        f"{round(sum(num(c['col_area']) or 0 for c in props))}; {round(sum(num(c['col_area']) or 0 for c in props if c['status_code'] == 'active'))}")
    if p == COMPOSITE:
        put("units", p, "units (a composite of other projects, excluded from totals)", len(us))
        continue
    status = {str(c["col_id"]): c["status_code"] for c in props}
    sec_file = {r["section_id"] for r in rows(f"sections__p{p:02d}.csv")}
    sec_units = collections.defaultdict(set)
    for u in us:
        sec_units[u["section_id"]].add(status.get(u["col_id"], "?"))
    missing = [s for s in sec_units if s not in sec_file]
    put("reconcile", p, "sections implied by units; in the sections file; missing from it, by column status",
        f"{len(sec_units)}; {len(sec_file)}; {len(missing)} ({counts(collections.Counter('/'.join(sorted(sec_units[s])) for s in missing))})")

    # spans and ages
    aged = [u for u in us if num(u["b_age"]) is not None and num(u["t_age"]) is not None]
    spans = sorted(num(u["b_age"]) - num(u["t_age"]) for u in aged)
    put("units", p, "units; with ages; gap-bound sections; columns with units",
        f"{len(us)}; {len(aged)}; {len(sec_units)}; {len({u['col_id'] for u in us})}")
    if aged:
        put("units", p, "oldest base; youngest top (Ma); unit span median (Myr); spanning more than 20 Myr",
            f"{max(num(u['b_age']) for u in aged):g}; {min(num(u['t_age']) for u in aged):g}; {statistics.median(spans):.2f}; "
            f"{share(sum(1 for s in spans if s > 20), len(spans))}")
        tops = [(u, "t") for u in aged] + [(u, "b") for u in aged]
        phan = [(u, k) for u, k in tops if 0 < num(u[f"{k}_age"]) <= 538.8]
        on_edge = [(u, k) for u, k in phan if num(u[f"{k}_prop"]) in (0.0, 1.0)]
        on_stage = [(u, k) for u, k in phan if round(num(u[f"{k}_age"]), 3) in edges]
        inner = [(u, k) for u, k in phan if num(u[f"{k}_prop"]) not in (0.0, 1.0)]
        inner_on = sum(1 for u, k in inner if round(num(u[f"{k}_age"]), 3) in edges)
        put("age support", p, "age-bearing Phanerozoic tops and bottoms (0 Ma tops excluded): on an interval edge; on an international stage boundary",
            f"{share(len(on_edge), len(phan))}; {share(len(on_stage), len(phan))}")
        put("age support", p, "chance baseline: boundaries interpolated inside an interval (prop not 0 or 1) that land on a stage boundary",
            share(inner_on, len(inner)))
        put("age support", p, "edge-aligned boundaries that are international stage boundaries", share(sum(1 for x in on_edge if x in on_stage), len(on_edge)))
        distinct = {(u["col_id"], round(num(u[f"{k}_age"]), 3)) for u, k in phan}
        put("age support", p, "distinct column-age boundaries on a stage boundary", share(sum(1 for _, a in distinct if a in edges), len(distinct)))
        bands = [(0, 2.58), (2.58, 66), (66, 251.902), (251.902, 538.8)]
        put("age support", p, "on a stage boundary by age band (Ma): 0-2.58; 2.58-66; 66-251.9; 251.9-538.8",
            "; ".join(share(sum(1 for u, k in on_stage if lo < num(u[f"{k}_age"]) <= hi),
                            sum(1 for u, k in phan if lo < num(u[f"{k}_age"]) <= hi)) for lo, hi in bands))

    # dates in units of Ma
    unit_age = {u["unit_id"]: (num(u["t_age"]), num(u["b_age"])) for u in us}
    single, spectra, consistent, rows_ma, exact = set(), set(), set(), 0, 0
    for m in rows(f"measurements__p{p:02d}.csv"):
        if m["measure_units"] != "Ma" or not m["unit_id"]:
            continue
        rows_ma += 1
        exact += m["match_basis"] == "exact"
        vals = [num(v) for v in m["measure_value"].split("|") if num(v) is not None]
        lith = lith_def.get(m["samp_lith_id"], {})
        igneous = lith.get("class") == "igneous" or re.search(r"tuff|ash|bentonite|volcan", f"{lith.get('name', '')} {m['samp_lith']}", re.I)
        if vals and igneous:  # a volcanic grain population: its median approximates the eruption age
            single.add(m["unit_id"])
            t, b = unit_age.get(m["unit_id"], (None, None))
            if t is not None and b is not None and t - 5 <= statistics.median(vals) <= b + 5:
                consistent.add(m["unit_id"])
        elif vals:
            spectra.add(m["unit_id"])
    if rows_ma:
        put("age support", p, "Ma measurement rows; tied to a unit by exact match", share(exact, rows_ma))
        put("age support", p, "units with a date from an igneous or ash sample; of them, with the sample median within the unit's age range +-5 Myr",
            f"{share(len(single), len(us))}; {len(consistent)}")
        put("age support", p, "units with dates from other samples only (detrital spectra: provenance, not unit ages)", len(spectra - single))

    # environments
    cls = collections.Counter()
    for u in us:
        found = {e.split("~")[0].split()[-1] for e in u["environ"].split("|") if e.strip()}
        cls["marine" if found == {"marine"} else "non-marine" if found == {"non-marine"} else "both" if len(found) > 1 else "none given"] += 1
        if p not in OCEAN and status.get(u["col_id"]) == "active":
            series_units.append((p, u["col_id"], num(u["t_age"]), num(u["b_age"]), found))
    put("environments", p, "units by environment class", counts(cls))

    # PBDB links
    obsolete_links = sum(int(num(u["pbdb_collections"]) or 0) for u in us if status.get(u["col_id"]) == "obsolete")
    put("pbdb", p, "units' summed pbdb_collections; in obsolete columns; stats route's pbdb_collections",
        f"{sum(int(num(u['pbdb_collections']) or 0) for u in us)}; {obsolete_links}; {st.get('pbdb_collections')}")
    fos = rows(f"fossils__p{p:02d}.csv")
    if fos:
        cl = {}
        for r in fos:
            cl[r["cltn_id"]] = max(cl.get(r["cltn_id"], 0), int(num(r["pbdb_occs"]) or 0))
        nonpublic = [c for c in cl if coll_n.get(c) and not coll_public.get(c)]
        partial = [c for c in cl if coll_public.get(c) and coll_n.get(c, 0) > coll_public[c]]
        put("pbdb", p, "fossil-route collections (obsolete columns are not served); Macrostrat occurrences; public occurrences today; net difference",
            f"{len(cl)}; {sum(cl.values())}; {sum(coll_public.get(c, 0) for c in cl)}; {sum(cl.values()) - sum(coll_public.get(c, 0) for c in cl)}")
        put("pbdb", p, "collections where Macrostrat's count equals PBDB's n_occs today", share(sum(1 for c in cl if cl[c] == coll_n.get(c)), len(cl)))
        put("pbdb", p, "collections with no public occurrence today; their occurrences by Macrostrat; by PBDB's n_occs; collections partly public",
            f"{len(nonpublic)}; {sum(cl[c] for c in nonpublic)}; {sum(coll_n[c] for c in nonpublic)}; {len(partial)}")
        lag_up = sum(coll_public[c] - cl[c] for c in cl if c not in nonpublic and coll_public.get(c, 0) > cl[c])
        lag_down = sum(cl[c] - coll_public.get(c, 0) for c in cl if c not in nonpublic and cl[c] > coll_public.get(c, 0))
        put("pbdb", p, "elsewhere: public occurrences beyond Macrostrat's count (newer); Macrostrat's beyond the public (deleted or moved); collections not in PBDB today",
            f"{lag_up}; {lag_down}; {sum(1 for c in cl if c not in coll_n)}")

    meas = rows(f"measurements__p{p:02d}.csv")
    if meas:
        names = collections.Counter(m["measurement"] for m in meas)
        values = sum(len([v for v in m["measure_value"].split("|") if v.strip()]) for m in meas)
        put("measurements", p, "rows; values (grain lists expanded); stats route; distinct measurement names; most common",
            f"{len(meas)}; {values}; {st.get('measurements')}; {len(names)}; {counts(names, 8)}")

if age_dir:
    project_of = {c: p for (p, c) in col_info if p != COMPOSITE}
    statuses, by_project, cols, empty = collections.Counter(), collections.defaultdict(collections.Counter), 0, 0
    for path in glob.glob(os.path.join(age_dir, "age_model__c*.csv")):
        cols += 1
        with open(path, newline="", encoding="utf-8", errors="replace") as f:
            rs = list(csv.DictReader(f)) if os.path.getsize(path) > 10 else []
        empty += not rs
        p = project_of.get(str(int(re.search(r"c(\d+)", os.path.basename(path)).group(1))), "?")
        for r in rs:
            statuses[r.get("boundary_status", "")] += 1
            by_project[p][r.get("boundary_status", "")] += 1
    put("age models", "", "columns requested; with no boundaries; boundaries by status", f"{cols}; {empty}; {counts(statuses)}")
    for p in sorted(by_project, key=str):
        put("age models", p, "boundaries by status", counts(by_project[p]))

area = {(p, c): num(col_info.get((p, c), {}).get("col_area")) or 0 for p, c, *_ in series_units}
with open(series_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    head = ["stage", "mid_ma"]
    for g in ("na", "na_ediacaran", "other_land"):
        head += [f"{g}_marine_km2", f"{g}_nonmarine_km2", f"{g}_any_km2", f"{g}_columns"]
    w.writerow(head + ["na_any_km2_units_le_5myr"])
    for s in reversed(stages):
        mid = (float(s["t_age"]) + float(s["b_age"])) / 2
        acc = collections.defaultdict(set)
        for p, c, t, b, found in series_units:
            if t is None or b is None or not t <= mid <= b:
                continue
            g = "na" if p == NA else "na_ediacaran" if p == EDIACARAN else "other_land"
            acc[(g, "any")].add((p, c))
            for k in ("marine", "non-marine"):
                if k in found:
                    acc[(g, k)].add((p, c))
            if p == NA and b - t <= 5:
                acc[("na", "fine")].add((p, c))
        cell = lambda g, k: round(sum(area[x] for x in acc[(g, k)]))
        row = [s["name"], round(mid, 3)]
        for g in ("na", "na_ediacaran", "other_land"):
            row += [cell(g, "marine"), cell(g, "non-marine"), cell(g, "any"), len(acc[(g, "any")])]
        w.writerow(row + [cell("na", "fine")])

with open(out_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["section", "project", "metric", "value"])
    w.writerows(out)
print(len(out), "rows")
