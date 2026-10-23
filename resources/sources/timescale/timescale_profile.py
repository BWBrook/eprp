# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["rdflib==7.1.1"]
# ///
"""Profile the mirrored geological time scale sources.

Usage: uv run timescale_profile.py ISC_RAW ICS_RAW MACROSTRAT_RAW PBDB_INTERVALS_CSV FARRELL_RAW OUT_DIR OUT_TSV
(needs pdftotext from poppler)

ISC_RAW is the CGI-IUGS timescale-data repository (one RDF file per ICS chart
release, 2004-2020). Each release's boundaries are read in either vocabulary:
the older one (tm:temporalPosition, tm:value, thors:positionalUncertainty with
basic:value) or the newer one (time:inTemporalPosition, time:numericPosition,
gts:positionalUncertainty with time:numericDuration). OUT_DIR receives
isc_boundaries_by_version.tsv: one row per boundary, the age and uncertainty in
every release. The profile counts boundaries and uncertainties per release and
the age changes between releases, and flags ages over 4,600 Ma (late
Quaternary boundaries recorded in years). The RDF releases follow the ICS chart,
not the GTS2020 book: the release labelled 2020 is the 2020/03 chart. It is
compared by name with PBDB's scale-1 intervals and Macrostrat's "international
intervals". The numbers printed on the ICS 2024/12 chart (pdftotext) are matched
to PBDB's base ages, which follow the current chart, to give
ics2024_pbdb_bases.tsv: each PBDB base with the chart's printed value and its
uncertainty where the chart gives one.
"""

import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter

from rdflib import Graph, Namespace
from rdflib.namespace import RDFS, SKOS

isc_raw, ics_raw, ms_raw, pbdb_csv, farrell_raw, out_dir, out_tsv = sys.argv[1:8]
TM = Namespace("http://def.seegrid.csiro.au/isotc211/iso19108/2002/temporal#")
TIME = Namespace("http://www.w3.org/2006/time#")
GTS = Namespace("http://resource.geosciml.org/ontology/timescale/gts#")
THORS = Namespace("http://resource.geosciml.org/ontology/timescale/thors#")
BASIC = Namespace("http://def.seegrid.csiro.au/isotc211/iso19103/2005/basic#")
out = []


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def num(v):
    return None if v is None else float(str(v))


def boundaries(path):
    g = Graph().parse(path, format="turtle")
    res = {}
    for pred in (TM.temporalPosition, TIME.inTemporalPosition):
        for b, pos in g.subject_objects(pred):
            label = g.value(b, RDFS.label) or g.value(b, SKOS.prefLabel)
            if label is None or not str(label).startswith("Base of"):
                continue
            age = num(g.value(pos, TM.value)) if g.value(pos, TM.value) is not None else num(g.value(pos, TIME.numericPosition))
            un = g.value(pos, THORS.positionalUncertainty) or g.value(pos, GTS.positionalUncertainty)
            unc = None
            if un is not None:
                unc = num(g.value(un, BASIC.value)) if g.value(un, BASIC.value) is not None else num(g.value(un, TIME.numericDuration))
            res[str(label)[8:].strip()] = (age, unc)
    return res


rdf_dir = os.path.join(isc_raw, "rdf")
files = sorted(f for f in os.listdir(rdf_dir) if re.fullmatch(r"isc\d{4}(-1)?\.ttl|isc2016-12-time\.ttl", f))
releases = {}
for f in files:
    rel = re.sub(r"-time$", "", f[3:-4])
    releases[rel] = boundaries(os.path.join(rdf_dir, f))
put("isc", "files_used", "", ", ".join(files))
order = sorted(releases)
prev = None
for rel in order:
    b = releases[rel]
    ages = [a for a, _ in b.values() if a is not None]
    put("isc", "release", rel, f"{len(b)} boundaries; with an age {len(ages)}; with an uncertainty {sum(u is not None for _, u in b.values())}; "
        f"oldest {max(ages) if ages else ''} Ma")
    if prev:
        p = releases[prev]
        common = [k for k in b if k in p and b[k][0] is not None and p[k][0] is not None]
        changed = sorted(((abs(b[k][0] - p[k][0]), k) for k in common if abs(b[k][0] - p[k][0]) > 1e-6), reverse=True)
        put("isc", "changes_from_previous", f"{prev} -> {rel}",
            f"{len(changed)} of {len(common)} shared boundaries moved; added {len(set(b) - set(p))}, dropped {len(set(p) - set(b))}; largest: "
            + ", ".join(f"{k} {p[k][0]:g}->{b[k][0]:g}" for _, k in changed[:5]))
    prev = rel
os.makedirs(out_dir, exist_ok=True)
names = sorted({k for b in releases.values() for k in b}, key=lambda k: min((releases[r][k][0] or 1e9) for r in order if k in releases[r]))
with open(os.path.join(out_dir, "isc_boundaries_by_version.tsv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["boundary"] + [f"{r}_{x}" for r in order for x in ("ma", "uncertainty")])
    for k in names:
        w.writerow([k] + [("" if v is None else v) for r in order for v in releases[r].get(k, (None, None))])

for rel in order:
    years = sorted(k for k, (a, _) in releases[rel].items() if a is not None and a > 4600)
    if years:
        put("isc", "ages_above_4600_ma (recorded in years, not Ma)", rel, ", ".join(f"{k} {releases[rel][k][0]:g}" for k in years))

ics2020 = releases.get("2020", {})
ms = json.load(open(os.path.join(ms_raw, "intervals_all.json")))["success"]["data"]
in_scale = lambda d, i: any(t.get("timescale_id") == i for t in (d.get("timescales") or []))
intl = {d["name"]: float(d["b_age"]) for d in ms if in_scale(d, 11)}
put("macrostrat", "intervals", "all", len(ms))
put("macrostrat", "timescales", "international intervals (id 11); New Zealand ages (id 6)",
    f"{len(intl)}; {sum(in_scale(d, 6) for d in ms)}")
pbdb = {}
with open(pbdb_csv, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["scale_no"] == "1" and r["b_age"]:
            pbdb.setdefault(r["interval_name"], float(r["b_age"]))
put("pbdb", "intervals", "scale 1 with a base age", len(pbdb))


def compare(label, a, b):
    shared = [k for k in a if k in b and a[k] is not None]
    diff = sorted(((abs(b[k] - a[k]), k) for k in shared if abs(b[k] - a[k]) > 0.005), reverse=True)
    put("bases_compared", label, "same names", f"{len(shared)} shared; equal within 0.005 Myr {len(shared) - len(diff)}; differing {len(diff)}"
        + (": " + "; ".join(f"{k} {a[k]:g} vs {b[k]:g}" for _, k in diff[:20]) if diff else ""))


rdf2020 = {k: v[0] for k, v in ics2020.items()}
compare("ICS 2020/03 (RDF) vs PBDB", rdf2020, pbdb)
compare("ICS 2020/03 (RDF) vs Macrostrat international intervals", rdf2020, intl)
compare("PBDB vs Macrostrat international intervals", pbdb, intl)

charts = {}
for f in sorted(glob.glob(os.path.join(ics_raw, "ChronostratChart*.pdf"))):
    text = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True).stdout
    vals = [v.replace(" ", "") for v in re.findall(r"~?\s?\d{1,4}\.\d+(?:\s*±\s*\d+(?:\.\d+)?)?", text)]
    charts[os.path.basename(f)] = vals
    put("ics_chart", "numbers_printed", os.path.basename(f), f"{len(vals)} ({len(set(vals))} distinct)")
age_of = lambda v: float(v.lstrip("~").split("±")[0])
if "ChronostratChart2024-12.pdf" in charts:
    printed = {}
    for v in charts["ChronostratChart2024-12.pdf"]:
        printed.setdefault(round(age_of(v), 4), v)
    rows, matched = [], 0
    for name, b in sorted(pbdb.items(), key=lambda kv: kv[1]):
        v = printed.get(round(b, 4))
        unc = v.split("±")[1] if v and "±" in v else ""
        approx = bool(v and v.startswith("~"))
        matched += v is not None
        rows.append([name, b, v or "", unc, int(approx)])
    with open(os.path.join(out_dir, "ics2024_pbdb_bases.tsv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["pbdb_interval", "pbdb_base_ma", "ics_2024_12_printed", "uncertainty_ma", "approximate"])
        w.writerows(rows)
    with_unc = sum(1 for r in rows if r[3])
    unmatched_chart = sorted({v for v in printed.values() if round(age_of(v), 4) not in {round(b, 4) for b in pbdb.values()}}, key=age_of)
    put("ics_chart", "2024/12 values matched to PBDB scale-1 bases", "",
        f"{matched} of {len(pbdb)} PBDB bases appear on the chart ({with_unc} with ±, {sum(r[4] for r in rows)} approximate); "
        f"chart values with no PBDB base: {', '.join(unmatched_chart)}")
if len(charts) == 2:
    old, new = (set(charts[k]) for k in sorted(charts))
    put("ics_chart", "values on 2024/12, not on 2020/03", "", f"{len(new - old)}; on 2020/03, not on 2024/12: {len(old - new)}")

fr = sorted(os.listdir(farrell_raw))
put("farrell2025", "files", "", ", ".join(f for f in fr if f != "MANIFEST.json"))

with open(out_tsv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
