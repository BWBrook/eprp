# /// script
# requires-python = ">=3.10"
# dependencies = ["pdfplumber==0.11.4"]
# ///
"""Extract Appendix Tables A1-A12 (taxon, rock unit, age range, reference) from Poropat et al. (2023).

Usage: uv run poropat_tables.py POROPAT_PDF OUT_TSV CHECK_TSV   (needs pdftotext from poppler)

The tables have no ruling and their headers are not aligned with the columns,
so each table (or continuation page) takes its column starts from its first
line that splits into four cells at gaps wider than 10 points; lines above it
(top-of-page continuations of the previous row) are placed with those starts.
Each word goes to the column whose start is nearest at or left of it. A line
with text in both the taxon and rock-unit columns starts a new row unless its
taxon text is a wrapped bracketed synonym; other lines continue the row above
(wrapped cells, and rows split across a page break). Words are grouped into
lines by their bottoms, because glyphs such as en dashes shift a word's top.

Font artefacts are mapped back to the printed characters: the font draws grave
and acute accents as separate glyphs before the base letter (pdfplumber reads
them as (cid:2) and (cid:3)), and "=" as "¼". The paper prints "Goméz-Pérez"
with the acute on the e, and omits the closing bracket after 'Plesiosaurus'
macrospondylus (Table A5); the extraction keeps both as printed.

Checks, which fail the run: no (cid: placeholder, no empty cell, balanced
brackets (apart from the one printed defect), and completeness against
pdftotext -layout. Every text segment of every appendix line (split at runs of
two or more spaces) must occur in a cell of the same table, unless the line is
a page header, caption, column header or "(continued)" marker, and the
non-space characters of those segments must equal those of the cells. CHECK_TSV
lists the lines set aside and the check results. Output is a derived table of
a CC BY 4.0 paper.
"""

import csv
import re
import subprocess
import sys
import unicodedata
from collections import Counter

import pdfplumber

COLS = ("taxon", "rock_unit", "age_range", "reference")
ACCENT = {"2": "̀", "3": "́"}
PRINTED_UNBALANCED = {("A5", "taxon", "Elasmosauridae incertae sedis (‘Plesiosaurus’ macrospondylus")}
CAPTION = re.compile(r"Table\s*(A\d+)\.")
PAGE_HEADER = re.compile(r"^\d+\s+(STEPHEN|ALCHERINGA)|^(ALCHERINGA|STEPHEN)")


def clean(s):
    s = re.sub(r"\(cid:(\d+)\)(\w)", lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENT[m.group(1)]), s)
    s = re.sub(r"([\x02\x03])(\w)", lambda m: unicodedata.normalize("NFC", m.group(2) + ACCENT[str(ord(m.group(1)))]), s)
    return s.replace("¼", "=")


def cell_groups(ws):
    groups = [[ws[0]]]
    for a, b in zip(ws, ws[1:]):
        if b["x0"] - a["x1"] > 10:
            groups.append([b])
        else:
            groups[-1].append(b)
    return groups


def category(line):
    s = line.strip()
    if CAPTION.match(s):
        return "caption"
    if PAGE_HEADER.match(s):
        return "page header"
    if s == "(continued)":
        return "continued marker"
    if s.startswith("Taxon") and "Reference" in s:
        return "column header"
    if s == "Appendix":
        return "appendix title"
    return None


pdf_path, out_path, check_path = sys.argv[1:4]
pdf = pdfplumber.open(pdf_path)
start = next(i for i, p in enumerate(pdf.pages) if "Appendix" in (p.extract_text() or "")[:400])

segments = []
for page in pdf.pages[start:]:
    words = sorted(page.extract_words(x_tolerance=1.2, keep_blank_chars=False), key=lambda w: w["bottom"])
    lines = []
    for w in words:
        if lines and w["bottom"] - lines[-1][0]["bottom"] <= 3:
            lines[-1].append(w)
        else:
            lines.append([w])
    for line in lines:
        ws = sorted(line, key=lambda w: w["x0"])
        for w in ws:
            w["text"] = clean(w["text"])
        text = " ".join(w["text"] for w in ws)
        m = CAPTION.match(text)
        if m:
            segments.append((m.group(1), []))
        elif segments and category(text) is None:
            segments[-1][1].append(ws)

rows = []
for table, lines in segments:
    starts = next([g[0]["x0"] - 3 for g in cell_groups(ws)] for ws in lines if len(cell_groups(ws)) == 4)
    for ws in lines:
        cells = ["", "", "", ""]
        for w in ws:
            col = max(i for i, s in enumerate(starts) if s <= w["x0"]) if w["x0"] >= starts[0] else 0
            cells[col] = (cells[col] + " " + w["text"]).strip()
        taxon = cells[0]
        wrapped = taxon.startswith("(") or (taxon[:1].islower() and not taxon.startswith(("cf.", "aff."))) \
            or (")" in taxon and ("(" not in taxon or taxon.index(")") < taxon.index("(")))
        if taxon and cells[1] and not wrapped:
            rows.append({"table": table, **dict(zip(COLS, cells))})
        elif rows and rows[-1]["table"] == table:
            for c, v in zip(COLS, cells):
                if v:
                    rows[-1][c] = (rows[-1][c] + " " + v).strip()
for r in rows:
    m = re.match(r"([A-Z][a-z]+ian)\s+(.*)", r["reference"])
    if m and re.search(r"(–|\b)(lower|middle|upper)$", r["age_range"]):  # a wrapped stage name landed in the reference
        r["age_range"], r["reference"] = f'{r["age_range"]} {m.group(1)}', m.group(2)
with open(out_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["table", *COLS], delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

report = []
counts = Counter(r["table"] for r in rows)
for t in sorted(counts, key=lambda t: int(t[1:])):
    report.append(("rows", t, counts[t]))
report.append(("rows", "all", len(rows)))

report.append(("cells_with_cid_placeholder", "all", sum("(cid:" in v for r in rows for v in r.values())))
report.append(("empty_cells", "all", sum(not r[c] for r in rows for c in COLS)))
unbalanced = {(r["table"], c, r[c]) for r in rows for c in COLS
              if r[c].count("(") != r[c].count(")") or r[c].count("[") != r[c].count("]")}
report.append(("cells_with_unbalanced_brackets", "all", len(unbalanced)))
for t, c, v in sorted(unbalanced):
    report.append(("unbalanced_cell", t, f"{c}: {v}"))

layout = subprocess.run(["pdftotext", "-layout", "-f", str(start + 1), "-l", str(len(pdf.pages)), pdf_path, "-"],
                        capture_output=True, text=True, check=True).stdout
pools = {t: [" ".join(r[c].split()) for r in rows if r["table"] == t for c in COLS] for t in counts}
table, skipped, unmatched, body_chars = None, Counter(), [], Counter()
for raw in layout.splitlines():
    line = clean(raw.replace("\x0c", " ")).strip()
    if not line:
        continue
    m = CAPTION.match(line)
    if m:
        table = m.group(1)
    cat = category(line)
    if cat:
        skipped[cat] += 1
        report.append(("set_aside_line", cat, " ".join(line.split())))
        continue
    for seg in re.split(r"\s{2,}", line):
        seg = " ".join(seg.split())
        body_chars.update(seg.replace(" ", ""))
        if not any(seg in c for c in pools[table]):
            unmatched.append((table, seg))
cell_chars = Counter("".join(r[c] for r in rows for c in COLS).replace(" ", ""))
report.append(("body_segments_not_in_a_cell_of_their_table", "all", len(unmatched)))
for t, s in unmatched:
    report.append(("unmatched_segment", t, s))
diff = {ch: body_chars[ch] - cell_chars[ch] for ch in body_chars | cell_chars if body_chars[ch] != cell_chars[ch]}
report.append(("nonspace_character_count_differences", "all", len(diff)))
for ch, d in sorted(diff.items()):
    report.append(("character_difference", "all", f"{ch!r}: pdftotext minus cells = {d}"))
with open(check_path, "w", newline="") as f:
    wr = csv.writer(f, delimiter="\t", lineterminator="\n")
    wr.writerow(["check", "key", "value"])
    wr.writerows(report)
print(len(rows), "rows", dict(counts), "| set aside:", dict(skipped), "| unmatched segments:", len(unmatched),
      "| character differences:", len(diff))
assert not any("(cid:" in v for r in rows for v in r.values())
assert not any(not r[c] for r in rows for c in COLS)
assert unbalanced == PRINTED_UNBALANCED, unbalanced
assert not unmatched, unmatched
assert not diff, diff
