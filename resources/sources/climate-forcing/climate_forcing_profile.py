# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Profile the mirrored climate-forcing series and event tables.

Usage: uv run climate_forcing_profile.py CLIMATE_FORCING_DIR OUT_DIR OUT_TSV   (needs pdftotext)

Reads the newest raw version of each route under CLIMATE_FORCING_DIR:
- phanda: PhanDA's GMST and CO2 percentiles by stage slice, checked against the
  SHA-256 pins in the main project's data/interval-crosswalk/sources.tsv;
- phansst: PhanSST v001 proxy rows by proxy type, value type, period and age;
- song2021, scotese2021-gmst: file inventories;
- cenogrid: every PANGAEA member table in the zip (rows, columns, age range);
- lr04: the stack's rows and age range in the author's file, and its agreement
  with the first data block of NOAA's copy;
- rothman2017-carbon-events: Table 1 of the article (31 carbon-isotope events),
  from the Europe PMC full-text XML;
- green2022-lips: Tables S1 (stage boundaries and extinction magnitudes), S2
  (LIPs), S3 (impacts), S4 (Rothman-method calculations) and S5 (predicted
  extinction magnitudes) of the SI appendix, parsed by column position from
  pdftotext -layout; tables in two column blocks are joined on the row number.
  Numbered rows must be consecutive; S2 start ages must not be younger than end
  ages. S1-S3 are compared with the authors' repository tables (green2022-code).
The parsed tables are written to OUT_DIR. Exit status 1 if a check fails.
"""

import csv
import glob
import hashlib
import html
import io
import json
import os
import re
import statistics
import subprocess
import sys
import tempfile
import zipfile
from collections import Counter

import openpyxl

root, out_dir, out_tsv = sys.argv[1:4]
out, failures = [], []
PINS = {"PhanDA_GMSTandCO2_percentiles.csv": "22cad7964bac3b679ad83bf8a9c83eb66e995898a01eb9e93142087b2d4f6e1f",
        "PhanDA_GMST_ensemble.mat": "6213e8164af32b7e67daee1acb603f6e8a186286041b54b0897c934fa51246ce",
        "R code for extinction rate.R": "47585e1266d9be9448ac8e00941902c0e7ac14afbded377173135fc6e6c4750b"}
csv.field_size_limit(1 << 30)
os.makedirs(out_dir, exist_ok=True)


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def latest(route):
    """The newest mirrored version: last in data_mirror's versions.tsv (the provider's order), else by name."""
    raw = glob.glob(os.path.join(root, route, "raw", "*"))
    try:
        with open(os.path.join(root, route, "versions.tsv"), encoding="utf-8") as f:
            order = [line.split("\t")[0] for line in f.read().splitlines()[1:]]
    except FileNotFoundError:
        order = []
    return max(raw, key=lambda p: (order.index(os.path.basename(p)) if os.path.basename(p) in order else -1, p), default=None)


def manifest(v):
    return {f["key"]: f for f in json.load(open(os.path.join(v, "MANIFEST.json")))["files"]}


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def write(name, header, rows):
    with open(os.path.join(out_dir, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# --- PhanDA -------------------------------------------------------------------------
v = latest("phanda")
if v:
    m = manifest(v)
    for key, pin in PINS.items():
        hits = [f for k, f in m.items() if os.path.basename(k) == key]
        for f in hits:
            ok = f["sha256"] == pin
            put("phanda", "sha256 vs main-project pin", f["key"], "match" if ok else f"DIFFERS ({f['sha256'][:12]})")
            if not ok:
                failures.append(f"phanda pin {key}")
    put("phanda", "files", "", f"{len(m)} files, {sum(f['size'] for f in m.values())} bytes; commit {os.path.basename(v)}")
    rows = list(csv.DictReader(open(os.path.join(v, "5_Outputs", "PhanDA_GMSTandCO2_percentiles.csv"), encoding="utf-8")))
    g = [(fnum(r["GMST_50"]), r["Stage"]) for r in rows]
    c = [(fnum(r["CO2_50"]), r["Stage"]) for r in rows]
    put("phanda", "GMSTandCO2_percentiles", "rows", f"{len(rows)} stage slices; ages {min(fnum(r['UpperAge']) for r in rows):g}-"
        f"{max(fnum(r['LowerAge']) for r in rows):g} Ma")
    put("phanda", "GMSTandCO2_percentiles", "GMST_50 range (degC)", f"{min(g)[0]:.1f} ({min(g)[1]}) to {max(g)[0]:.1f} ({max(g)[1]})")
    put("phanda", "GMSTandCO2_percentiles", "CO2_50 range (ppm)", f"{min(c)[0]:.0f} ({min(c)[1]}) to {max(c)[0]:.0f} ({max(c)[1]})")
    merged = [r["Stage"] for r in rows if "/" in r["Stage"]]
    other = [r["Stage"] for r in rows if "petm" in r["Stage"].lower()]
    put("phanda", "GMSTandCO2_percentiles", "slices: single stages; merged pairs ('/'); PETM",
        f"{len(rows) - len(merged) - len(other)}; {len(merged)} ({', '.join(merged)}); {len(other)} ({', '.join(other)})")
    ltg = glob.glob(os.path.join(v, "5_Outputs", "PhanDA_LTG_percentiles", "PhanDA_SATgradient_percentiles_bystage", "*.csv"))
    put("phanda", "SAT gradient percentiles", "stage files", len(ltg))

# --- PhanSST --------------------------------------------------------------------------
v = latest("phansst")
if v:
    rows = list(csv.DictReader(open(os.path.join(v, "PhanSST_v001.csv"), encoding="utf-8", errors="replace")))
    put("phansst", "PhanSST_v001", "rows", len(rows))
    for col in ("ProxyType", "ValueType", "Period"):
        put("phansst", "PhanSST_v001", col, "; ".join(f"{k or '(blank)'} {n}" for k, n in Counter(r[col] for r in rows).most_common(12)))
    ages = [a for a in (fnum(r["Age"]) for r in rows) if a is not None and a == a]
    put("phansst", "PhanSST_v001", "Age (Ma)", f"{len(ages)} rows with an age; {min(ages):g}-{max(ages):g}; median {statistics.median(ages):g}")
    put("phansst", "PhanSST_v001", "site names; site name + hole; lead author + year; publication DOIs (rows without a DOI)",
        f"{len({r['SiteName'] for r in rows})}; {len({(r['SiteName'], r['SiteHole']) for r in rows})}; "
        f"{len({(r['LeadAuthor'], r['Year']) for r in rows})}; {len({r['PublicationDOI'] for r in rows if r['PublicationDOI']})} "
        f"({sum(1 for r in rows if not r['PublicationDOI'])}); DOI or author-year {len({r['PublicationDOI'] or (r['LeadAuthor'], r['Year']) for r in rows})}")
    put("phansst", "PhanSST_v001", "negative ages; AgeFlag; DiagenesisFlag NaN",
        f"{sum(1 for a in ages if a < 0)}; " + ", ".join(f"{k} {n}" for k, n in sorted(Counter(r['AgeFlag'] for r in rows).items()))
        + f"; {sum(1 for r in rows if r['DiagenesisFlag'] in ('', 'NaN'))}")
    gh_rows = len(rows)
    wb = openpyxl.load_workbook(os.path.join(v, "PhanSST_v001_RefList.xlsx"), read_only=True)
    put("phansst", "PhanSST_v001_RefList.xlsx", "rows", sum(1 for _ in wb.worksheets[0].iter_rows(values_only=True)) - 1)
    z = latest("phansst-zenodo")
    if z:
        with zipfile.ZipFile(glob.glob(os.path.join(z, "**", "*.zip"), recursive=True)[0]) as zf:
            names = [n for n in zf.namelist() if n.endswith("PhanSST_v001.csv")]
            zrows = sum(1 for _ in csv.DictReader(io.TextIOWrapper(zf.open(names[0]), encoding="utf-8", errors="replace"))) if names else None
        put("phansst", "Zenodo release v0.0.1-beta vs GitHub head", "PhanSST_v001.csv rows",
            f"release {zrows}; head {gh_rows}" if zrows is not None else "no PhanSST_v001.csv in the release zip")

# --- Song 2021, Scotese 2021 ------------------------------------------------------------
for route in ("song2021-temperature-thresholds", "scotese2021-gmst"):
    v = latest(route)
    if not v:
        continue
    m = manifest(v)
    for k, f in sorted(m.items()):
        desc = f"{f['size']} bytes"
        if k.lower().endswith(".zip"):
            with zipfile.ZipFile(os.path.join(v, k)) as z:
                names = [i.filename for i in z.infolist() if not i.is_dir()]
            desc += f"; {len(names)} members ({', '.join(f'{e} {n}' for e, n in Counter(os.path.splitext(x)[1].lower() for x in names).most_common())})"
        if os.path.basename(k) in PINS:
            ok = f["sha256"] == PINS[os.path.basename(k)]
            desc += "; sha256 matches the main-project pin" if ok else "; sha256 DIFFERS from the main-project pin"
            if not ok:
                failures.append(f"{route} pin {k}")
        put(route, "file", k, desc)

# --- CENOGRID ------------------------------------------------------------------------------
v = latest("cenogrid")
if v:
    with zipfile.ZipFile(os.path.join(v, "Westerhold-etal_2020.zip")) as z:
        tabs = [i.filename for i in z.infolist() if i.filename.endswith(".tab")]
        put("cenogrid", "zip", "member tables", len(tabs))
        for t in tabs:
            text = z.read(t).decode("utf-8", "replace")
            body = text.split("*/", 1)[1].lstrip("\r\n") if "*/" in text else text
            lines = [l for l in body.splitlines() if l.strip()]
            head = lines[0].split("\t")
            agecol = next((i for i, h in enumerate(head) if re.match(r"(age|tuned time)\b", h.lower())), None)
            ages = [fnum(l.split("\t")[agecol]) for l in lines[1:]] if agecol is not None else []
            ages = [a for a in ages if a is not None]
            put("cenogrid", "table", os.path.basename(t)[:80], f"{len(lines) - 1} rows x {len(head)} columns"
                + (f"; {head[agecol]} {min(ages):g}-{max(ages):g}" if ages else "") + f"; columns: {', '.join(h[:30] for h in head[:8])}")

# --- LR04 --------------------------------------------------------------------------------------
v = latest("lr04")
if v:
    def stack(lines):
        rows = []
        for l in lines:
            p = l.split()
            if len(p) >= 3 and all(fnum(x) is not None for x in p[:3]):
                rows.append(tuple(float(x) for x in p[:3]))
            elif rows:
                break
        return rows
    a = stack(open(os.path.join(v, "LR04stack.txt"), encoding="utf-8", errors="replace").read().splitlines())
    n = open(os.path.join(v, "lisiecki2005.txt"), encoding="utf-8", errors="replace").read().splitlines()
    start = next(i for i, l in enumerate(n) if l.strip().lower().startswith("time") and "d18o" in l.lower())
    b = stack(n[start + 1:])
    put("lr04", "LR04stack.txt", "rows", f"{len(a)}; {a[0][0]:g}-{a[-1][0]:g} ka")
    put("lr04", "lisiecki2005.txt (NOAA)", "first data block", f"{len(b)} rows; identical to the author's file in {sum(x == y for x, y in zip(a, b))}")

# --- Rothman 2017 ---------------------------------------------------------------------------------
v = latest("rothman2017-carbon-events")
if v:
    x = open(os.path.join(v, "PMC5606709_fullText.xml"), encoding="utf-8").read()
    t = re.search(r'<table-wrap id="T1".*?</table-wrap>', x, re.S).group(0)
    cell = lambda c: " ".join(html.unescape(re.sub(r"<[^>]+>", " ", c)).split()).replace("−", "-")
    rows = [[cell(c) for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", r, re.S)] for r in re.findall(r"<tr>(.*?)</tr>", t, re.S)]
    header = [h.replace("δ 1", "δ1").replace("τ env", "τ_env").replace(" )", ")").replace("Date[Ma]", "Date [Ma]") for h in rows[0]]
    data = rows[1:]
    write("rothman2017_events.tsv", header, data)
    put("rothman2017", "Table 1", "events", f"{len(data)}; dates {min(fnum(r[2]) for r in data):g}-{max(fnum(r[2]) for r in data):g} Ma")
    if len(data) != 31:
        failures.append(f"rothman2017: {len(data)} events, abstract says 31")
    lic = re.search(r'licenses/([a-z-]+/[0-9.]+)', x)
    put("rothman2017", "licence", "", lic.group(1) if lic else "not found")

# --- Green, Renne & Keller 2022 -------------------------------------------------------------------------
TOK = re.compile(r"\S+(?: \S+)*")


def layout_block(lines, i):
    """Parse a column-aligned block starting at header line i; return (columns, rows, next index)."""
    cols = [(m.start(), m.group(0)) for m in TOK.finditer(lines[i])]
    rows, j, blanks = [], i + 1, 0
    while j < len(lines):
        l = lines[j]
        if not l.strip():
            blanks += 1
            if blanks >= 2 and rows:
                break
            j += 1
            continue
        if l.lstrip().startswith(("List of", "Table S")) or re.search(r"\d+ of 19", l):
            break
        blanks = 0
        row = {}
        for m in TOK.finditer(l):
            k = min(range(len(cols)), key=lambda c: abs(cols[c][0] - m.start()))
            row[cols[k][1]] = (row.get(cols[k][1], "") + " " + m.group(0)).strip()
        rows.append(row)
        j += 1
    return [c for _, c in cols], rows, j


v = latest("green2022-lips")
if v:
    with zipfile.ZipFile(os.path.join(v, "PMC9499591_supplementaryFiles.zip")) as z, tempfile.TemporaryDirectory() as tmp:
        pdf = [n for n in z.namelist() if n.endswith("sapp.pdf")][0]
        p = os.path.join(tmp, "sapp.pdf")
        open(p, "wb").write(z.read(pdf))
        lines = subprocess.run(["pdftotext", "-layout", p, "-"], capture_output=True, text=True).stdout.splitlines()
    put("green2022", "SI appendix", pdf, f"{len(lines)} text lines")
    tables = {}
    for name in ("S1", "S2", "S3", "S4", "S5"):
        i = next(k for k, l in enumerate(lines) if f"Table {name}." in l)
        h = next(k for k in range(i + 1, len(lines)) if lines[k].strip())
        cols, rows, j = layout_block(lines, h)
        if "..." in cols:
            h2 = next(k for k in range(j, len(lines)) if lines[k].strip().startswith("..."))
            cols2, rows2, _ = layout_block(lines, h2)
            extra = {r.get("#"): r for r in rows2}
            for r in rows:
                r.update({k: x for k, x in extra.get(r.get("#"), {}).items() if k not in ("#", "...")})
            cols = [c for c in cols if c != "..."] + [c for c in cols2 if c not in ("#", "...")]
        tables[name] = (cols, rows)
        nums = [r.get("#") for r in rows]
        if "#" in cols and nums != [str(k) for k in range(1, len(rows) + 1)]:
            failures.append(f"green {name}: row numbers not consecutive")
        put("green2022", f"Table {name}", "rows; columns", f"{len(rows)}; {', '.join(cols)}")
        write(f"green2022_table_{name}.tsv", cols, [[r.get(c, "") for c in cols] for r in rows])
    s1 = tables["S1"]
    comment = s1[0][-1]
    lsd = [r["#"] for r in s1[1] if "least significant digit" in r.get(comment, "")]
    put("green2022", "Table S1", "rows whose 1-sigma is the least significant digit (rounding, not an uncertainty)",
        f"{len(lsd)}: rows {', '.join(lsd)}")
    lips = tables["S2"][1]
    bad = [r["Name"] for r in lips if fnum(r.get("Start Age [Ma]")) is None or fnum(r.get("End Age [Ma]")) is None
           or fnum(r["Start Age [Ma]"]) < fnum(r["End Age [Ma]"])]
    put("green2022", "Table S2", "LIPs with unreadable ages or start younger than end", ", ".join(bad) or "none")
    if bad:
        failures.append("green S2 ages")
    rates = [fnum(r.get("Eruption rate [km3/yr]")) for r in lips]
    put("green2022", "Table S2", "rows with an eruption rate", sum(x is not None for x in rates))
    aus = [r["Name"] for r in lips if re.search(r"Kalkarindji|Bunbury|Whitsunday|Gascoyne|Kennedy", r["Name"])]
    put("green2022", "Table S2", "Australian LIPs (by name)", ", ".join(aus))

    code = latest("green2022-code")
    if code:
        def repo_table(name):
            with open(os.path.join(code, "data", name), encoding="utf-8", errors="replace", newline="") as fh:
                return list(csv.DictReader(fh, delimiter="\t"))
        same = lambda a, b: fnum(a) is not None and fnum(b) is not None and abs(fnum(a) - fnum(b)) < 1e-6
        full = lambda n: re.sub(r"[\s'\u2019]", "", n.replace("\u2013", "-")).lower()
        key = lambda n: full(re.sub(r"\s*\(.*?\)", "", n))
        rl = {}
        for t in ("LIPs.tsv", "LIPs Including Oceanic.tsv"):
            for r in repo_table(t):
                rl.setdefault(full(r["Name"]), r)
                rl.setdefault(key(r["Name"]), r)
        fields = (("Start Age [Ma]", "Start Age [Ma]"), ("Start Age 1σ [Ma]", "Start Age sigma [Ma]"), ("End Age [Ma]", "End Age [Ma]"),
                  ("End Age 1σ [Ma]", "End Age sigma [Ma]"))
        ok, unmatched, differ = [], [], []
        for r in lips:
            q = rl.get(full(r["Name"])) or rl.get(key(r["Name"]))
            if q is None:
                unmatched.append(r["Name"])
            elif all(same(r.get(a), q.get(b)) for a, b in fields):
                ok.append(r["Name"])
            else:
                differ.append(f"{r['Name']} (" + "; ".join(f"{a} {r.get(a)} vs {q.get(b)}" for a, b in fields if not same(r.get(a), q.get(b))) + ")")
        put("green2022", "S2 vs repository LIPs.tsv and LIPs Including Oceanic.tsv (names normalised)",
            "LIPs with equal start and end ages and sigmas",
            f"{len(ok)} of {len(lips)}; differing: {'; '.join(differ) or 'none'}; not found: {', '.join(unmatched) or 'none'}")
        if differ:  # names the repository lacks are reported above, not failed
            failures.append(f"green S2 vs repository: {len(differ)} LIPs differ")
        rb = {r["Number"]: r for r in repo_table("boundaries.tsv")}
        okb = sum(1 for r in tables["S1"][1] if r["#"] in rb and same(r.get("Age [Ma]"), rb[r["#"]]["Age [Ma]"])
                  and (same(r.get("Age 1σ [Ma]"), rb[r["#"]]["Age sigma [Ma]"]) or not r.get("Age 1σ [Ma]")))
        put("green2022", "S1 vs repository data/boundaries.tsv", "boundaries with equal age and sigma",
            f"{okb} of {len(tables['S1'][1])}; repository rows {len(rb)}")
        if okb != len(tables["S1"][1]):
            failures.append(f"green S1 vs repository: {len(tables['S1'][1]) - okb} boundaries missing or differing")
        ri = {key(r["Name"]): r for r in repo_table("impacts.tsv")}
        s3 = tables["S3"][1]
        bad = [f"{r['Name']} ({r.get('Age [Ma]')} ± {r.get('Age 1σ [Ma]')} vs "
               + (f"{ri[key(r['Name'])]['Age [Ma]']} ± {ri[key(r['Name'])]['Age_sigma [Ma]']})" if key(r["Name"]) in ri else "not found)")
               for r in s3 if not (key(r["Name"]) in ri and same(r.get("Age [Ma]"), ri[key(r["Name"])]["Age [Ma]"])
                                   and same(r.get("Age 1σ [Ma]"), ri[key(r["Name"])]["Age_sigma [Ma]"]))]
        put("green2022", "S3 vs repository data/impacts.tsv", "impacts with equal age and sigma",
            f"{len(s3) - len(bad)} of {len(s3)}; repository rows {len(ri)}; differing: {'; '.join(bad) or 'none'}")
        if bad:
            failures.append(f"green S3 vs repository: {len(bad)} impacts missing or differing")

for f in failures:
    put("checks", "failure", "", f)
put("checks", "summary", "", "ok" if not failures else f"{len(failures)} failures")
with open(out_tsv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
sys.exit(1 if failures else 0)
