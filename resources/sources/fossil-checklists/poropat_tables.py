# /// script
# requires-python = ">=3.10"
# dependencies = ["pdfplumber==0.11.4"]
# ///
"""Extract Appendix Tables A1-A12 (taxon, rock unit, age range, reference) from Poropat et al. (2023).

Usage: uv run poropat_tables.py POROPAT_PDF OUT_TSV

The tables have no ruling and their headers are not aligned with the columns,
so column starts are taken from the first line of each table that splits into
four cells at gaps wider than 10 points. Each word goes to the column whose
start is nearest at or left of it. A line with text in both the taxon and
rock-unit columns starts a new row unless its taxon text is a wrapped
bracketed synonym; other lines continue the row above (wrapped cells).
Words are grouped into lines by their bottoms, because glyphs such as en
dashes shift a word's top. Output is a derived table of a CC BY 4.0 paper;
check rows against the PDF before relying on them.
"""

import csv
import re
import sys

import pdfplumber

COLS = ("taxon", "rock_unit", "age_range", "reference")
rows, table, starts = [], None, None
pdf = pdfplumber.open(sys.argv[1])
start = next(i for i, p in enumerate(pdf.pages) if "Appendix" in (p.extract_text() or "")[:400])
for page in pdf.pages[start:]:
    words = sorted(page.extract_words(x_tolerance=1.2, keep_blank_chars=False), key=lambda w: w["bottom"])
    lines = []
    for w in words:  # glyphs such as en dashes shift a word's top, so cluster on bottoms within 3 pt
        if lines and w["bottom"] - lines[-1][0]["bottom"] <= 3:
            lines[-1].append(w)
        else:
            lines.append([w])
    for line in lines:
        ws = sorted(line, key=lambda w: w["x0"])
        text = " ".join(w["text"] for w in ws)
        m = re.match(r"Table\s*(A\d+)\.", text)
        if m:
            table, starts = m.group(1), None
            continue
        if table is None or (text.startswith("Taxon") and "Reference" in text) \
                or re.match(r"^\d+\s+(STEPHEN|ALCHERINGA)|^(ALCHERINGA|STEPHEN)", text):
            continue
        groups = [[ws[0]]]
        for a, b in zip(ws, ws[1:]):
            if b["x0"] - a["x1"] > 10:
                groups.append([b])
            else:
                groups[-1].append(b)
        if starts is None:
            if len(groups) != 4:
                continue
            starts = [g[0]["x0"] - 3 for g in groups]
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
    for c in COLS:
        r[c] = re.sub(r"\s*\(continued\)$", "", r[c].replace("¼", "="))  # the font maps "=" to "¼"; page-break marker
    m = re.match(r"([A-Z][a-z]+ian)\s+(.*)", r["reference"])
    if m and re.search(r"(–|\b)(lower|middle|upper)$", r["age_range"]):  # a wrapped stage name landed in the reference
        r["age_range"], r["reference"] = f'{r["age_range"]} {m.group(1)}', m.group(2)
with open(sys.argv[2], "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["table", *COLS], delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "rows", {t: sum(r["table"] == t for r in rows) for t in sorted({r["table"] for r in rows})})
