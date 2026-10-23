# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5", "xlrd==2.0.1"]
# ///
"""Profile the mirrored copies of Benton's The Fossil Record 2 (family ranges).

Usage: uv run fr2_profile.py BRISTOL_RAW WAYBACK_RAW OUT_DIR OUT_TSV

BRISTOL_RAW is the 2019 re-posting: 45 chapter workbooks (one family or
family-surrogate per row; columns 1-5 name, kingdom, phylum, other, habitat;
columns 6-91 the 86 FR2 time divisions, Hadean to Holocene; column 92 NFR, no
fossil record), All-Life.xlsx, FR2.zip, the stage summary behind Benton (1995)
(Diversitydata95.xlsx), Holman's tallies (All-data.xlsx), and the WordPress
page and media listings. WAYBACK_RAW holds the 1997-2006 Bristol originals: the
chapter files as BinHex-encoded tab-delimited text, four 2004 .xls files, the
StuffIt archives, and the HTML pages.

Checks: every media file is in the snapshot; FR2.zip and All-Life.xlsx against
the chapter files; the range codes (F1, F2, ?F, 1, ?, L1, L2, ?L, FL) and their
order within each row. Builds each family's maximum range (every coded cell)
and minimum range (Benton 1995: from the confident first code F1/F2 to the
confident last code L1/L2, or to the Holocene for a range to the Recent; a
single-stage FL; none for a range given only to an interval longer than a
stage), and stage-by-stage counts, written to OUT_DIR. Dates the divisions
from the Vendian on with the Harland et al. (1990) durations and midpoints in
the 1998 stage table (fr2_divisions.csv). Compares those counts
with Diversitydata95 and Holman's family tallies, and every Wayback capture of
every chapter with the 2019 workbook, row by row. Exit status 1 if a structural
check fails.
"""

import csv
import glob
import html
import io
import json
import os
import re
import sys
import zipfile
from collections import Counter, defaultdict

import openpyxl
import xlrd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import binhex4  # noqa: E402

bristol, wayback, out_dir, out_tsv = sys.argv[1:5]
out, failures = [], []
CODES = {"1", "?", "F1", "F2", "?F", "L1", "L2", "?L", "FL", "?FL"}


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def cell(v):
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v).strip()


def xlsx_rows(src):
    wb = openpyxl.load_workbook(src, read_only=True, data_only=True)
    rows = [[cell(c) for c in r] for r in wb.worksheets[0].iter_rows(values_only=True)]
    return [r + [""] * (92 - len(r)) for r in rows if any(r)]


def text_rows(data):
    lines = data.decode("mac_roman").replace("\r\n", "\r").replace("\n", "\r").split("\r")
    rows = [[c.strip() for c in l.split("\t")] for l in lines]
    return [r + [""] * (92 - len(r)) for r in rows if any(r)]


def key_of(r):
    return tuple(r[:92])


# --- Bristol files ------------------------------------------------------------
chapter_files = sorted(glob.glob(os.path.join(bristol, "[0-9]*-*.xlsx")), key=lambda p: int(os.path.basename(p).split("-")[0]))
chapters = {int(os.path.basename(p).split("-")[0]): (os.path.basename(p), xlsx_rows(p)) for p in chapter_files}
put("bristol", "chapters", "files", len(chapters))
media = json.load(open(os.path.join(bristol, "wp_media.json")))
data_media = [m["source_url"].rsplit("/", 1)[1] for m in media if not m["mime_type"].startswith("image/")]
absent = [n for n in data_media if not os.path.exists(os.path.join(bristol, n))]
put("bristol", "media_listing", "data_files_listed", f"{len(data_media)}; absent from snapshot: {', '.join(absent) or 'none'}")
if absent:
    failures.append(f"media files absent: {absent}")

with zipfile.ZipFile(os.path.join(bristol, "FR2.zip")) as z:
    members = [n for n in z.namelist() if n.endswith(".xlsx") and not n.startswith("__MACOSX")]
    same_bytes = same_cells = 0
    for n in members:
        b = z.read(n)
        base = os.path.basename(n)
        src = os.path.join(bristol, base)
        if os.path.exists(src) and open(src, "rb").read() == b:
            same_bytes += 1
        if os.path.exists(src) and xlsx_rows(io.BytesIO(b)) == xlsx_rows(src):
            same_cells += 1
    put("bristol", "FR2.zip", "workbooks", f"{len(members)}; byte-identical to the chapter downloads {same_bytes}; same cells {same_cells}")
    extra = [n for n in members if not os.path.exists(os.path.join(bristol, os.path.basename(n)))]
    for n in extra:
        rows = xlsx_rows(io.BytesIO(z.read(n)))
        basal = [r for ch in (1, 2, 3) for r in xlsx_rows(chapter_files[ch - 1])]
        put("bristol", "FR2.zip", f"{os.path.basename(n)} (not on the downloads page)",
            f"{len(rows)} rows; identical to chapters 1-3 ({len(basal)} rows): {Counter(map(key_of, rows)) == Counter(map(key_of, basal))}")

all_rows = Counter(key_of(r) for _, rows in chapters.values() for r in rows)
life = xlsx_rows(os.path.join(bristol, "All-Life.xlsx"))
header, life = life[0], life[1:]
stages = header[5:91]
life_c = Counter(key_of(r) for r in life)
put("bristol", "All-Life.xlsx", "rows_vs_chapters",
    f"All-Life {len(life)}; chapters {sum(all_rows.values())}; only in All-Life {sum((life_c - all_rows).values())}; "
    f"only in chapters {sum((all_rows - life_c).values())}")
put("bristol", "time_divisions", "columns_6_to_91", f"{len(stages)}: {stages[0]} ... {stages[-1]}")
sequence = [(ch, i, r) for ch, (_, rows) in chapters.items() for i, r in enumerate(rows, 1)]
kinds, shifted = Counter(), defaultdict(list)
for (ch, i, r), lr in zip(sequence, life):
    if key_of(r) == key_of(lr):
        continue
    j = next(j for j in range(92) if r[j] != lr[j])
    if " ".join(r[0].split()) == " ".join(lr[0].split()) and r[1:92] == lr[1:92]:
        kinds["family name differs only in spacing"] += 1
    elif lr[j:91] == r[j + 1:92] and not r[j]:
        kinds["shifted one column left: NFR moved into the Holocene column" if r[91] == "NFR" and not any(r[5:91])
              else "shifted one column left: range one division older" if j >= 5
              else "shifted one column left: habitat in column 4 and range one division older"] += 1
        shifted[ch].append(i)
    else:
        kinds["other difference"] += 1
put("bristol", "All-Life.xlsx", "order", "same families in the same order as the chapters: "
    + str(len(life) == len(sequence) and all(" ".join(r[0].split()) == " ".join(l[0].split()) for (_, _, r), l in zip(sequence, life))))
put("bristol", "All-Life.xlsx", "rows_differing_from_chapters", "; ".join(f"{k} {v}" for k, v in sorted(kinds.items())))
put("bristol", "All-Life.xlsx", "shifted_rows_by_chapter", "; ".join(
    f"{ch}: {len(v)} (rows {v[0]}-{v[-1]})" for ch, v in sorted(shifted.items())))

# --- Codes, ranges and anomalies -------------------------------------------
families = []
code_count, anomalies = Counter(), defaultdict(list)
for ch, (fname, rows) in chapters.items():
    put("chapters", "rows", fname, len(rows))
    for i, r in enumerate(rows, 1):
        tag = f"{ch}:{i} {r[0]}"
        cells = [(j, c) for j, c in enumerate(r[5:91]) if c]
        for _, c in cells:
            code_count[c] += 1
            if c not in CODES:
                anomalies["code outside the key"].append(f"{tag} '{c}'")
        if r[91] and r[91] != "NFR":
            anomalies["column 92 holds a value other than NFR"].append(f"{tag} '{r[91]}'")
        if not cells:
            (anomalies["no coded cell (NFR)"] if r[91] == "NFR" else anomalies["no coded cell, no NFR"]).append(tag)
            families.append(dict(chapter=ch, row=i, name=r[0], kingdom=r[1], phylum=r[2], other=r[3], habitat=r[4],
                                 max_first=None, max_last=None, min_first=None, min_last=None, extant=False))
            continue
        idx = [j for j, _ in cells]
        if idx[-1] - idx[0] + 1 != len(idx):
            anomalies["gap inside the range"].append(tag)
        codes = [c for _, c in cells]
        fcodes = [j for j, c in cells if c in ("F1", "F2")]
        lcodes = [j for j, c in cells if c in ("L1", "L2")]
        fl = [j for j, c in cells if c == "FL"]
        if len(fcodes) > 1:
            anomalies["more than one F1/F2"].append(tag)
        if len(lcodes) > 1:
            anomalies["more than one L1/L2"].append(tag)
        if codes[0] not in ("F1", "?F", "FL", "?FL"):
            anomalies["first coded cell not F1, ?F, FL or ?FL"].append(f"{tag} '{codes[0]}'")
        extant = idx[-1] == 85
        if codes[-1] not in ("L1", "?L", "FL", "?FL") and not extant:
            anomalies["last coded cell not L1, ?L or FL and not Holocene"].append(f"{tag} '{codes[-1]}'")
        if fcodes and lcodes and lcodes[0] < fcodes[0]:
            anomalies["L code before F code"].append(tag)
        if len(fl) == 1 and len(cells) == 1:
            mn = (fl[0], fl[0])
        elif fcodes and (lcodes or extant):
            mn = (fcodes[0], lcodes[-1] if lcodes else 85)
        else:
            mn = (None, None)
        families.append(dict(chapter=ch, row=i, name=r[0], kingdom=r[1], phylum=r[2], other=r[3], habitat=r[4],
                             max_first=idx[0], max_last=idx[-1], min_first=mn[0], min_last=mn[1], extant=extant))
put("codes", "cells", "all", "; ".join(f"{k} {v}" for k, v in code_count.most_common()))
for k, v in sorted(anomalies.items()):
    put("codes", "anomaly", k, f"{len(v)}: " + "; ".join(v[:12]) + (" ..." if len(v) > 12 else ""))

names = Counter(f["name"] for f in families)
put("families", "rows", "total", len(families))
put("families", "rows", "by_kingdom", "; ".join(f"{k} {v}" for k, v in Counter(f["kingdom"] for f in families).most_common()))
put("families", "names", "distinct", len(names))
put("families", "names", "repeated", f"{sum(1 for n in names.values() if n > 1)} names on {sum(n for n in names.values() if n > 1)} rows: "
    + ", ".join(n for n, c in names.most_common(15) if c > 1))
put("families", "names", "questioned ('?' in name)", sum("?" in f["name"] for f in families))
put("families", "names", "ending -idae or -aceae", sum(bool(re.search(r"(idae|aceae)$", f["name"])) for f in families))
put("families", "ranges", "with a range", sum(f["max_first"] is not None for f in families))
put("families", "ranges", "with a minimum range", sum(f["min_first"] is not None for f in families))
put("families", "ranges", "to the Holocene", sum(f["extant"] for f in families))
put("families", "ranges", "single division (maximum)", sum(f["max_first"] is not None and f["max_first"] == f["max_last"] for f in families))
put("families", "habitat", "codes", "; ".join(f"{k or '(blank)'} {v}" for k, v in Counter(f["habitat"] for f in families).most_common(15)))

os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "fr2_families.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["chapter", "row", "family", "kingdom", "phylum", "other", "habitat", "max_first", "max_last", "min_first", "min_last", "to_holocene"])
    for f in families:
        st = lambda j: "" if j is None else stages[j]
        w.writerow([f["chapter"], f["row"], f["name"], f["kingdom"], f["phylum"], f["other"], f["habitat"],
                    st(f["max_first"]), st(f["max_last"]), st(f["min_first"]), st(f["min_last"]), int(f["extant"])])


def marine(h):
    return "M" in h.replace("?M", "")


def continental(h):
    return any(c in h.replace("?F", "").replace("?T", "") for c in "FTV")


def counts(fams, which):
    n = [Counter() for _ in stages]
    for f in fams:
        a, b = f[f"{which}_first"], f[f"{which}_last"]
        if a is None:
            continue
        groups = ["all"] + (["marine"] if marine(f["habitat"]) else []) + (["continental"] if continental(f["habitat"]) else [])
        for g in groups:
            n[a][g + "_orig"] += 1
            n[b][g + "_ext"] += 1
            for j in range(a, b + 1):
                n[j][g] += 1
    return n


mx, mn = counts(families, "max"), counts(families, "min")
with open(os.path.join(out_dir, "fr2_stage_counts.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    groups = ["all", "marine", "continental"]
    w.writerow(["division"] + [f"{g}_{k}_{m}" for m in ("min", "max") for g in groups for k in ("families", "orig", "ext")])
    for j, s in enumerate(stages):
        w.writerow([s] + [c[j][g + suf] for c in (mn, mx) for g in groups for suf in ("", "_orig", "_ext")])

# --- The 1997-2006 Bristol originals (Wayback Machine) -----------------------
captures = defaultdict(list)
for n in sorted(os.listdir(wayback)):
    m = re.fullmatch(r"(\d{14})__(\d+)\.hqx", n)
    if not m:
        continue
    data, layers = open(os.path.join(wayback, n), "rb").read(), 0
    try:
        while b"(This file must be converted with BinHex" in data[:200]:
            name, ftype, creator, data, _ = binhex4.decode(data)
            layers += 1
    except Exception as e:
        put("wayback", "undecodable", n, repr(e))
        continue
    captures[int(m.group(2))].append((m.group(1), name, ftype, creator, text_rows(data) if ftype == "TEXT" else None, layers))
types = Counter(f"{c[2]}/{c[3]}" for caps in captures.values() for c in caps)
put("wayback", "chapter_captures", "decoded", f"{sum(map(len, captures.values()))} captures of {len(captures)} chapters; "
    f"Macintosh type/creator after decoding: {', '.join(f'{k} {v}' for k, v in types.most_common())}; "
    f"BinHex inside BinHex: {', '.join(c[0][:8] + ' ch' + str(ch) for ch, caps in sorted(captures.items()) for c in caps if c[5] > 1) or 'none'}")
if set(captures) != set(chapters):
    failures.append(f"chapters without a Wayback capture: {sorted(set(chapters) - set(captures))}")


def compare(old, new):
    co, cn = Counter(map(key_of, old)), Counter(map(key_of, new))
    names_o, names_n = Counter(r[0] for r in old), Counter(r[0] for r in new)
    gone = {r[0] for r in (co - cn).elements()}
    return dict(old=len(old), new=len(new), same=sum((co & cn).values()),
                only_old_names=sum((names_o - names_n).values()), only_new_names=sum((names_n - names_o).values()),
                changed=sorted(gone & set(names_n)))


tot = Counter()
changed_chapters, revisions = [], []
for ch in sorted(captures):
    caps = [c for c in captures[ch] if c[4] is not None]
    if not caps:
        continue
    first = caps[0]
    c = compare(first[4], chapters[ch][1])
    tot.update({k: v for k, v in c.items() if k != "changed"})
    if c["same"] != c["old"] or c["old"] != c["new"]:
        changed_chapters.append(f"{ch} ({first[0][:8]}: {c['old']} rows, {c['same']} identical in 2019; "
                                f"2019 {c['new']} rows; names only then {c['only_old_names']}, only now {c['only_new_names']}; "
                                f"changed: {', '.join(c['changed'])})")
    for later in caps[1:]:
        d = compare(first[4], later[4])
        if d["same"] != d["old"] or d["old"] != d["new"]:
            revisions.append(f"{ch} {first[0][:8]}->{later[0][:8]}: {d['old']}->{d['new']} rows, {d['same']} unchanged")
put("wayback", "earliest_capture_vs_2019", "all_chapters",
    f"{tot['old']} rows then, {tot['new']} in 2019; {tot['same']} identical; family names only then {tot['only_old_names']}, only in 2019 {tot['only_new_names']}")
put("wayback", "earliest_capture_vs_2019", "chapters_with_differences", "; ".join(changed_chapters) or "none")
put("wayback", "later_captures_vs_earliest", "chapters_revised", "; ".join(revisions) or "none")

earliest = {ch: [c for c in caps if c[4] is not None][0][4] for ch, caps in captures.items() if any(c[4] is not None for c in caps)}
agree = Counter()
for (ch, i, r), lr in zip(sequence, life):
    if ch in shifted and i in shifted[ch] and ch in earliest:
        old = Counter(map(key_of, earliest[ch]))
        agree["1998 agrees with the chapter file" if old[key_of(r)] else
              "1998 agrees with All-Life" if old[key_of(lr)] else "1998 agrees with neither"] += 1
put("wayback", "All-Life_shifted_rows", "vs_earliest_capture", "; ".join(f"{k} {v}" for k, v in agree.most_common()))
stray = sum(1 for rows in earliest.values() for r in rows if r[91] and r[91] != "NFR")
put("wayback", "column_92", "earliest captures: values other than NFR", stray)

for n in sorted(os.listdir(wayback)):
    p = os.path.join(wayback, n)
    if n.endswith(".xls"):
        book = xlrd.open_workbook(p)
        sh = book.sheet_by_index(0)
        rows = [[cell(sh.cell_value(i, j)) for j in range(sh.ncols)] for i in range(sh.nrows)]
        rows = [r + [""] * (92 - len(r)) for r in rows if any(r)]
        target = {"Monera": [1], "Fungi": [2], "Algae": [3], "basal": [1, 2, 3]}[n.split("__")[1][:-4]]
        new = [r for ch in target for r in chapters[ch][1]]
        c = compare(rows, new)
        put("wayback", "xls_2004", n, f"{c['old']} rows; {c['same']} identical to 2019 chapter(s) {target} ({c['new']} rows)")
    elif re.search(r"chapters\.(sit|hqx)$", n):
        raw = open(p, "rb").read()
        put("wayback", "archive", n, f"{len(raw)} bytes; starts {raw[:4]!r}"
            + ("; a StuffIt archive (not unpacked; the chapter captures cover its contents)" if raw[:4] == b"SIT!" else ""))


def html_table(path, pre):
    text = html.unescape(re.sub(r"<[^>]+>", "", open(path, "rb").read().decode("latin-1")))
    rows = []
    for line in text.splitlines():
        parts = line.split("\t") if not pre else line.split()
        if len(parts) > 5 and re.fullmatch(r"[-.\d]+", parts[-1].strip() or "x"):
            try:
                rows.append([parts[0].strip()] + [float(x) for x in parts[1:] if x.strip()])
            except ValueError:
                continue
    return rows


d95_old = sorted(n for n in os.listdir(wayback) if re.search(r"__(FR2\.data95|FR2data\.html)", n))
tables = {n: html_table(os.path.join(wayback, n), False) for n in d95_old}
base = tables[d95_old[0]]


def cells_differing(t):
    return [f"{a[0]} column {k - 2}: {x:g} -> {y:g}" for a, b in zip(base, t) for k, (x, y) in enumerate(zip(a[1:], b[1:]), 1)
            if abs(x - y) > 1e-6 * max(1, abs(x))] + [f"{a[0]}: {len(a)} -> {len(b)} values" for a, b in zip(base, t) if len(a) != len(b)]


put("wayback", "data95_html", "captures", "; ".join(f"{n.split('__')[0][:8]} {len(t)} stages x {max(map(len, t)) - 1} values, "
    f"{len(cells_differing(t))} values differ from the first" for n, t in tables.items()))
changes = sorted({c for t in tables.values() for c in cells_differing(t)})
put("wayback", "data95_html", "values revised after 2000", "; ".join(changes) or "none")
with open(os.path.join(out_dir, "fr2_divisions.csv"), "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["division", "name_1998", "base_ma", "top_ma"])
    for j, s in enumerate(stages):
        a = base[j - 8] if j >= 8 else None
        w.writerow([s, a[0] if a else "", round(a[2] + a[1] / 2, 3) if a else "", round(max(a[2] - a[1] / 2, 0), 3) if a else ""])
d95_new = xlsx_rows(os.path.join(bristol, "Diversitydata95.xlsx"))[2:]
num = lambda v: float(v) if re.fullmatch(r"-?[\d.]+(e-?\d+)?", v) else None
new = [[r[0]] + [num(v) for v in r[1:45]] for r in d95_new]
put("diversity95", "xlsx_2019", "shape", f"{len(new)} stages; non-empty value columns {max(sum(v is not None for v in r[3:]) for r in new)} of 42 labelled")
names_ok = sum(" ".join(a[0].split()).upper().replace(".", "") == " ".join(b[0].split()).upper().replace(".", "")
               for a, b in zip(base, new))
put("diversity95", "xlsx_2019_vs_1998", "stage names in the same order", f"{names_ok} of {len(base)}")
mapping = []
for j in range(3, 45):
    best, hits = None, 0
    for k in range(3, len(base[0])):
        h = sum(1 for a, b in zip(base, new) if b[j] is not None and k < len(a) and abs(a[k] - b[j]) < 1e-3 * max(1, abs(a[k])))
        if h > hits:
            best, hits = k, h
    mapping.append(f"{j - 2}->{'-' if best is None else best - 2}({hits})")
put("diversity95", "xlsx_2019_vs_1998", "xlsx data column -> 1998 column (stages equal)", " ".join(mapping))

def window_counts(fams, which, lo):
    res = []
    for j in range(lo, 86):
        res.append(sum(1 for f in fams if f[f"{which}_first"] is not None and f[f"{which}_first"] <= j <= f[f"{which}_last"]))
    return res


for pair, label in ((3, "all"), (5, "continental"), (7, "marine")):
    first_larger = sum(1 for a in base if a[pair] > a[pair + 1])
    put("diversity95", "1998_table", f"{label}: column labelled min larger than column labelled max",
        f"{first_larger} of {len(base)} stages")
groups = (("all", lambda f: True, 3), ("continental", lambda f: continental(f["habitat"]), 5), ("marine", lambda f: marine(f["habitat"]), 7))
for g, test, k in groups:
    sub = [f for f in families if test(f)]
    ours_min, ours_max = window_counts(sub, "min", 8), window_counts(sub, "max", 8)
    lo = [min(a[k], a[k + 1]) for a in base]
    hi = [max(a[k], a[k + 1]) for a in base]
    ratio = sorted(x / y for x, y in zip(ours_min, lo) if y)
    put("diversity95", "recount_from_chapters_vs_1998", g,
        f"recounted minimum within the 1998 pair at {sum(1 for x, a, b in zip(ours_min, lo, hi) if a <= x <= b)} of {len(base)} stages; "
        f"recounted maximum within it at {sum(1 for x, a, b in zip(ours_max, lo, hi) if a <= x <= b)}; "
        f"median recounted minimum / smaller 1998 value {ratio[len(ratio) // 2]:.3f}")

hol_old = sorted(n for n in os.listdir(wayback) if re.search(r"__FR2\.?families", n))
hol = html_table(os.path.join(wayback, hol_old[0]), True)
wbk = openpyxl.load_workbook(os.path.join(bristol, "All-data.xlsx"), read_only=True, data_only=True)
fam_sheet = [[cell(c) for c in r] for r in wbk["Families"].iter_rows(values_only=True)][1:]
same = sum(1 for a, b in zip(hol, fam_sheet) if a[0] == b[0] and all(abs(x - float(y)) < 1e-3 for x, y in zip(a[1:], b[1:10]) if y != ""))
put("holman", "families_1998_html_vs_2019_xlsx", "intervals equal", f"{same} of {len(hol)} ({len(fam_sheet)} in the workbook)")
conservative = [f for f in families if "?" not in f["name"] and f["chapter"] != 45]
div, ori, ext = Counter(), Counter(), Counter()
for f in conservative:
    if f["min_first"] is None:
        continue
    a, b = max(f["min_first"], 7) - 7, max(f["min_last"], 7) - 7
    ori[a] += 1
    if f["min_last"] != 85:
        ext[b] += 1
    for j in range(a, b + 1):
        div[j] += 1
for label, ours, k in (("DIV", div, 4), ("ORI", ori, 2), ("EXT", ext, 3)):
    eq = sum(1 for j, a in enumerate(hol) if ours[j] == a[k])
    mad = sum(abs(ours[j] - a[k]) for j, a in enumerate(hol)) / len(hol)
    put("holman", "recount_from_chapters_vs_1998", label, f"equal in {eq} of {len(hol)} intervals; mean absolute difference {mad:.1f} "
        "(Holman also tallied orders, which the chapter files do not record)")

pages = {p["slug"]: p for p in json.load(open(os.path.join(bristol, "wp_pages.json")))}
for slug in ("fossil-amphibian-families", "fossil-reptile-families", "fossil-bird-families", "fossil-mammal-families-1", "fossil-mammal-families-2"):
    trs = re.findall(r"<tr[^>]*>(.*?)</tr>", pages[slug]["content"]["rendered"], re.S)
    n = sum(1 for t in trs if len(re.findall(r"<td", t)) >= 6) - 1
    put("tetrapods", "benton_1996_tables", slug, f"{n} rows")
birds = xlsx_rows(os.path.join(bristol, "Birds.xlsx"))
put("tetrapods", "fountaine_2005_birds", "Birds.xlsx", f"{len(birds) - 1} species rows")

# --- write -------------------------------------------------------------------
for f in failures:
    put("checks", "failure", "", f)
put("checks", "summary", "", "ok" if not failures else f"{len(failures)} failures")
with open(out_tsv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
sys.exit(1 if failures else 0)
