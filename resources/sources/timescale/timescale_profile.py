# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["rdflib==7.1.1"]
# ///
"""Profile the mirrored geological time scale sources.

Usage: uv run timescale_profile.py ISC_RAW ICS_RAW MACROSTRAT_RAW PBDB_INTERVALS_CSV FARRELL_RAW OUT_DIR OUT_TSV
(needs pdftotext from poppler)

ISC_RAW is the CGI-IUGS timescale-data repository: one RDF (Turtle) file per
ICS chart release, 2004 to the chart of 2020/01, and copies of the chart PDFs
2014-10 to 2020-01 with the ICS change logs.

RDF. Boundaries are keyed by URI. A boundary's age is read from its position in
either vocabulary (tm:temporalPosition with tm:value and tm:frame, or
time:inTemporalPosition with time:numericPosition and time:hasTRS); positions
in the years-before-present system (.../geologicage/bp) are converted to Ma, and
where a boundary has both, the Ma position is used. Uncertainties are read the
same way (basic:value or time:numericDuration, converted from years where the
unit is years). Every "Base of ..." label (rdfs:label, skos:prefLabel,
skos:altLabel) and the labels of owl:sameAs aliases name the boundary.
OUT_DIR/isc_boundaries_by_version.tsv gives each boundary's labels and its age
and uncertainty in every release, sorted by age then URI.

Comparisons. The 2020 release is compared by name with PBDB's scale-1 intervals
and Macrostrat's "international intervals" (by PBDB interval type); PBDB with
Macrostrat. Each chart PDF's printed ages (decimals, integers of three or four
digits, optional "~" and "± u") are read with pdftotext, and successive charts
compared by age. The 2024/12 chart's ages are matched to PBDB base ages by value:
OUT_DIR/ics2024_pbdb_bases.tsv gives each PBDB base with the chart's printed
value and uncertainty where they match.
"""

import csv
import glob
import json
import os
import re
import subprocess
import sys
from collections import Counter, defaultdict

from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDFS, SKOS

isc_raw, ics_raw, ms_raw, pbdb_csv, farrell_raw, out_dir, out_tsv = sys.argv[1:8]
TM = Namespace("http://def.seegrid.csiro.au/isotc211/iso19108/2002/temporal#")
TIME = Namespace("http://www.w3.org/2006/time#")
GTS = Namespace("http://resource.geosciml.org/ontology/timescale/gts#")
THORS = Namespace("http://resource.geosciml.org/ontology/timescale/thors#")
BASIC = Namespace("http://def.seegrid.csiro.au/isotc211/iso19103/2005/basic#")
out = []


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def norm(label):
    return " ".join(str(label).replace("Base of", "").split()).lower()


def boundaries(path):
    g = Graph().parse(path, format="turtle")
    res, frames = {}, Counter()
    for pred in (TM.temporalPosition, TIME.inTemporalPosition):
        for b, pos in g.subject_objects(pred):
            val = g.value(pos, TM.value) if g.value(pos, TM.value) is not None else g.value(pos, TIME.numericPosition)
            try:
                val = float(str(val))
            except (TypeError, ValueError):  # e.g. the Present, given as a date
                continue
            if not any(str(x).startswith("Base of") for p in (RDFS.label, SKOS.prefLabel) for x in g.objects(b, p)):
                continue
            trs = str(g.value(pos, TM.frame) or g.value(pos, TIME.hasTRS) or "")
            bp = trs.endswith("/bp")
            frames["bp" if bp else trs.rsplit("/", 1)[-1] or "none"] += 1
            age = val / (1e6 if bp else 1)
            un = g.value(pos, THORS.positionalUncertainty) or g.value(pos, GTS.positionalUncertainty)
            unc = None
            if un is not None:
                u = g.value(un, BASIC.value) if g.value(un, BASIC.value) is not None else g.value(un, TIME.numericDuration)
                unit = str(g.value(un, TIME.unitType) or g.value(un, BASIC.uom) or "")
                if u is not None:
                    unc = float(str(u)) / (1e6 if unit.endswith("/a") else 1)
            prev = res.get(b)
            if prev is None or (prev["bp"] and not bp):
                res[b] = {"age": age, "unc": unc, "bp": bp}
    labels = defaultdict(set)
    for b in res:
        for p in (RDFS.label, SKOS.prefLabel, SKOS.altLabel):
            labels[b].update(str(x) for x in g.objects(b, p) if str(x).startswith("Base of"))
        for alias in set(g.objects(b, OWL.sameAs)) | set(g.subjects(OWL.sameAs, b)):
            for p in (RDFS.label, SKOS.prefLabel, SKOS.altLabel):
                labels[b].update(str(x) for x in g.objects(alias, p) if str(x).startswith("Base of"))
    return {str(b).rsplit("/", 1)[-1]: dict(v, labels=sorted(labels[b])) for b, v in res.items()}, frames


rdf_dir = os.path.join(isc_raw, "rdf")
files = sorted(f for f in os.listdir(rdf_dir) if re.fullmatch(r"isc\d{4}(-1)?\.ttl|isc2016-1[02]-t(m|ime)\.ttl", f))
releases = {}
for f in files:
    rel = re.sub(r"-(tm|time)$", "", f[3:-4])
    releases[rel], frames = boundaries(os.path.join(rdf_dir, f))
    put("isc", "position reference systems", rel, "; ".join(f"{k} {v}" for k, v in frames.most_common()))
put("isc", "files_used", "", ", ".join(files))
order = sorted(releases)
prev = None
for rel in order:
    b = releases[rel]
    ages = [x["age"] for x in b.values()]
    uncs = [x["unc"] for x in b.values() if x["unc"] is not None]
    put("isc", "release", rel, f"{len(b)} boundaries ({len(set(ages))} distinct ages); with an uncertainty {len(uncs)} "
        f"({sum(u == 0 for u in uncs)} of them 0); oldest {max(ages):g} Ma; from years before present {sum(x['bp'] for x in b.values())}")
    if prev:
        p = releases[prev]
        common = [k for k in b if k in p]
        changed = sorted(((abs(b[k]["age"] - p[k]["age"]), k) for k in common if abs(b[k]["age"] - p[k]["age"]) > 1e-9), reverse=True)
        put("isc", "changes_from_previous (by URI)", f"{prev} -> {rel}",
            f"{len(changed)} of {len(common)} shared boundaries moved; added {len(set(b) - set(p))}, dropped {len(set(p) - set(b))}; largest: "
            + ", ".join(f"{k} {p[k]['age']:g}->{b[k]['age']:g}" for _, k in changed[:6]))
    prev = rel
meta = open(os.path.join(rdf_dir, "isc2020.ttl"), encoding="utf-8").read()
vi = re.search(r'owl:versionInfo "([^"]+)"', meta)
put("isc", "isc2020.ttl", "owl:versionInfo", vi.group(1) if vi else "none")
logs = sorted(glob.glob(os.path.join(isc_raw, "stratigraphy.org", "ChangeLog*.txt")), key=lambda p: (len(p), p))
if logs:
    line = next((l.strip() for l in open(logs[-1], encoding="utf-8", errors="replace") if "actual version" in l), "")
    put("isc", "newest change log", os.path.basename(logs[-1]), line[:160])

os.makedirs(out_dir, exist_ok=True)
uris = sorted({k for b in releases.values() for k in b},
              key=lambda k: (min(releases[r][k]["age"] for r in order if k in releases[r]), k))
with open(os.path.join(out_dir, "isc_boundaries_by_version.tsv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["boundary_uri", "labels"] + [f"{r}_{x}" for r in order for x in ("ma", "uncertainty")])
    for k in uris:
        labs = sorted({l for r in order if k in releases[r] for l in releases[r][k]["labels"]})
        row = [k, " | ".join(labs)]
        for r in order:
            x = releases[r].get(k)
            row += ["", ""] if x is None else [round(x["age"], 9), "" if x["unc"] is None else round(x["unc"], 9)]
        w.writerow(row)

# --- PBDB and Macrostrat by name --------------------------------------------------
ms_doc = json.load(open(os.path.join(ms_raw, "intervals_all.json")))
ms = ms_doc["success"]["data"]
put("macrostrat", "intervals", "all; licence field", f"{len(ms)}; {ms_doc['success'].get('license')}")
in_scale = lambda d, i: any(t.get("timescale_id") == i for t in (d.get("timescales") or []))
intl = {d["name"]: float(d["b_age"]) for d in ms if in_scale(d, 11)}
nz = [d for d in ms if in_scale(d, 6)]
put("macrostrat", "timescales", "international intervals (id 11); New Zealand (id 6) by interval type",
    f"{len(intl)}; " + ", ".join(f"{k} {v}" for k, v in Counter(d["int_type"] for d in nz).most_common()))
pbdb, ptype = {}, {}
with open(pbdb_csv, newline="", encoding="utf-8") as fh:
    for r in csv.DictReader(fh):
        if r["scale_no"] == "1" and r["b_age"] and r["interval_name"] not in pbdb:
            pbdb[r["interval_name"]] = float(r["b_age"])
            ptype[r["interval_name"]] = r["type"]
put("pbdb", "intervals", "scale 1 with a base age, by type", f"{len(pbdb)}: " + ", ".join(f"{k} {v}" for k, v in Counter(ptype.values()).most_common()))

by_name = {}
for k, x in releases["2020"].items():
    for l in x["labels"]:
        by_name[norm(l)] = x["age"]


def compare(label, a, b, types=None):
    shared = [k for k in a if norm(k) in b] if types is not None else [k for k in a if k in b]
    get = (lambda k: b[norm(k)]) if types is not None else (lambda k: b[k])
    diff = sorted(((abs(get(k) - a[k]), k) for k in shared if abs(get(k) - a[k]) > 0.005), reverse=True)
    detail = ""
    if types is not None:
        detail = "; by PBDB type, shared/differing: " + ", ".join(
            f"{t} {sum(types[k] == t for k in shared)}/{sum(types[k] == t for _, k in diff)}" for t in sorted({types[k] for k in shared}))
        unmatched = sorted(k for k in a if norm(k) not in b)
        detail += f"; PBDB names with no RDF label: {len(unmatched)} ({', '.join(unmatched)})"
    put("bases_compared", label, "by name", f"{len(shared)} shared; equal within 0.005 Myr {len(shared) - len(diff)}; differing {len(diff)}"
        + detail + ("; largest: " + "; ".join(f"{k} {a[k]:g} vs {get(k):g}" for _, k in diff[:12]) if diff else ""))


compare("PBDB vs RDF 2020 (chart 2020/01)", pbdb, by_name, ptype)
compare("PBDB vs Macrostrat international intervals", pbdb, intl)

# --- Chart PDFs ------------------------------------------------------------------------
NUM = re.compile(r"(~\s?)?(\d{1,4}\.\d+|\d{3,4})(?:\s*±\s*(\d+(?:\.\d+)?))?")
charts = {}
pdfs = glob.glob(os.path.join(isc_raw, "stratigraphy.org", "ChronostratChart*.pdf")) + glob.glob(os.path.join(ics_raw, "ChronostratChart*.pdf"))
for f in sorted(set(pdfs), key=os.path.basename):
    name = re.search(r"ChronostratChart(\d{4}-\d{2})", f).group(1)
    if name in charts:
        continue
    text = subprocess.run(["pdftotext", "-layout", f, "-"], capture_output=True, text=True).stdout
    toks = [(m.group(0).replace(" ", ""), float(m.group(2)), m.group(3), bool(m.group(1))) for m in NUM.finditer(text)]
    charts[name] = toks
names = sorted(charts)
for i, n in enumerate(names):
    ages = {round(t[1], 4) for t in charts[n]}
    line = f"{len(charts[n])} tokens, {len(ages)} distinct values"
    if i:
        prev_ages = {round(t[1], 4) for t in charts[names[i - 1]]}
        line += f"; vs {names[i - 1]}: new values {len(ages - prev_ages)}, gone {len(prev_ages - ages)}"
    put("ics_chart", "printed numbers", n, line)

if "2024-12" in charts:
    printed = {}
    for tok, age, unc, approx in charts["2024-12"]:
        key = round(age, 4)
        if key not in printed or (unc and not printed[key][2]):
            printed[key] = (tok, age, unc, approx)
    rows = []
    for name, b in sorted(pbdb.items(), key=lambda kv: (kv[1], kv[0])):
        t = printed.get(round(b, 4))
        rows.append([name, ptype[name], b, t[0] if t else "", (t[2] or "") if t else "", int(bool(t and t[3])), int(bool(t and "." not in t[0].split("±")[0]))])
    with open(os.path.join(out_dir, "ics2024_pbdb_bases.tsv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["pbdb_interval", "pbdb_type", "pbdb_base_ma", "ics_2024_12_printed", "uncertainty_ma", "approximate", "integer_token"])
        w.writerows(rows)
    hit = [r for r in rows if r[3]]
    put("ics_chart", "2024-12 values matched to PBDB scale-1 bases", "rows",
        f"{len(hit)} of {len(rows)} rows ({len({r[2] for r in hit})} distinct ages); with ± {sum(1 for r in hit if r[4])} rows "
        f"({len({r[2] for r in hit if r[4]})} distinct ages); approximate {sum(r[5] for r in hit)} rows "
        f"({len({r[2] for r in hit if r[5]})} distinct); matched through an integer token {sum(r[6] for r in hit)}")
    put("ics_chart", "PBDB bases not printed on 2024-12", "", "; ".join(f"{r[0]} ({r[1]}) {r[2]:g}" for r in rows if not r[3]) or "none")
    approx = sorted({t[0] for t in charts["2024-12"] if t[3]}, key=lambda s: float(re.sub(r"[^\d.].*$", "", s.lstrip("~"))))
    put("ics_chart", "2024-12 approximate (~) values", "", f"{len(approx)}: " + ", ".join(approx))

fr = sorted(os.listdir(farrell_raw))
put("farrell2025", "files", "", ", ".join(f for f in fr if f != "MANIFEST.json"))

with open(out_tsv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
