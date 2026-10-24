# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5", "xlrd==2.0.1"]
# ///
"""Inventory the small Australian fossil-biota deposits mirrored under au-fossil-deposits/.

Usage: uv run deposits_profile.py AU_FOSSIL_DEPOSITS_DIR OUT_TSV

For each deposit's latest raw version: the manifest's title, DOI, publication
date and licence, then every file (in subdirectories too, named by relative path) with its size. Spreadsheets
(.xlsx, .xls and the .xlsx members of zips) and .csv/.tsv files (and members) are read as
tables; .txt, .md, .R and .m files give a line count and (for .txt and .md) the
first line; .tps files give their specimen blocks; other types are listed as
not_parsed, and a summary row lists the types skipped.

Table rules. A sheet or file with "readme" in its name is text: non-empty rows
only. Otherwise the header is the first row with at least 3 non-empty cells (when
it is not the first row, the first row is echoed as first_row), and
data rows are the later rows with at least 2 non-empty cells whose first cell is
not "Total" or "Totals". Everything else is counted as dropped: rows before the
header, totals rows, and short rows (titles, captions, footnotes, sub-headings).
columns = non-empty header cells; numeric_columns = columns where at least half
the filled data cells are numbers; distinct[...] gives distinct values against
filled values for specimen, taxon, sample, site and ID columns (placeholders
such as na, n/a, -- do not count as filled).

Writes long-format (deposit, file, metric, value).
"""

import collections
import csv
import glob
import io
import json
import os
import re
import sys
import zipfile

import openpyxl
import xlrd

csv.field_size_limit(1 << 30)
KEYS = {"specimen", "id", "taxon", "scientific name", "fossahul_id", "site i.d.", "sample id", "sample"}
PLACEHOLDERS = {"na", "n/a", "none", "null", "nan", "--"}
out = []
skipped = collections.Counter()
n_files = n_bytes = 0


def blank(c):
    return c is None or (isinstance(c, str) and not c.strip())


def numeric(c):
    if isinstance(c, bool):
        return False
    if isinstance(c, (int, float)):
        return True
    try:
        float(str(c).strip())
        return True
    except ValueError:
        return False


def table(dep, name, label, rows):
    pre = f"{label}:" if label else ""
    filled = [r for r in rows if any(not blank(c) for c in r)]
    header = next((k for k, r in enumerate(filled) if sum(not blank(c) for c in r) >= 3), None)
    if "readme" in (name + label).lower() or header is None:
        out.append((dep, name, pre + "text_rows", len(filled)))
        return
    head = filled[header]
    data, totals, short = [], 0, 0
    for r in filled[header + 1 :]:
        cells = [c for c in r if not blank(c)]
        if str(cells[0]).strip().lower() in ("total", "totals"):
            totals += 1
        elif len(cells) < 2:
            short += 1
        else:
            data.append(r)
    names = [str(c).strip() for c in head if not blank(c)]
    n_numeric = 0
    distinct = []
    for j, c in enumerate(head):
        if blank(c):
            continue
        vals = [r[j] for r in data if j < len(r) and not blank(r[j])]
        n_numeric += bool(vals) and 2 * sum(numeric(v) for v in vals) >= len(vals)
        if str(c).strip().lower() in KEYS:
            keys = [str(v).strip() for v in vals if str(v).strip().lower() not in PLACEHOLDERS]
            distinct.append((dep, name, f"{pre}distinct[{str(c).strip()}]", f"{len(set(keys))} of {len(keys)} filled"))
    if header:
        out.append((dep, name, pre + "first_row", str(next(c for c in filled[0] if not blank(c))).strip()[:200]))
    out.append((dep, name, pre + "data_rows", len(data)))
    out.append((dep, name, pre + "dropped_rows", f"before header {header}; totals {totals}; short {short}"))
    out.append((dep, name, pre + "columns", len(names)))
    out.append((dep, name, pre + "numeric_columns", n_numeric))
    out.extend(distinct)
    out.append((dep, name, pre + "header", "; ".join(names[:12])[:200]))


def xlsx_sheets(dep, name, source):
    wb = openpyxl.load_workbook(source, read_only=True, data_only=True)
    for ws in wb.worksheets:
        table(dep, name, f"sheet:{ws.title}", [list(r) for r in ws.iter_rows(values_only=True)])


def newest(dep_dir):
    """The newest mirrored version: last in data_mirror's versions.tsv (the provider's order), else by name."""
    raw = glob.glob(os.path.join(dep_dir, "raw", "*"))
    try:
        with open(os.path.join(dep_dir, "versions.tsv"), encoding="utf-8") as f:
            order = [line.split("\t")[0] for line in f.read().splitlines()[1:]]
    except FileNotFoundError:
        order = []
    return max(raw, key=lambda p: (order.index(os.path.basename(p)) if os.path.basename(p) in order else -1, p), default=None)


root = sys.argv[1]
deposits = sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d)))
for dep in deposits:
    v = newest(os.path.join(root, dep))
    if v is None:
        continue
    out.append((dep, "", "version_dir", os.path.basename(v)))
    with open(os.path.join(v, "MANIFEST.json")) as f:
        manifest = json.load(f)
    for metric, field in (("title", "title"), ("doi", "doi"), ("published", "publication_date"), ("licence", "license")):
        out.append((dep, "", metric, manifest.get(field) or "none"))
    for path in sorted(p for p in glob.glob(os.path.join(v, "**"), recursive=True) if os.path.isfile(p)):
        name = os.path.relpath(path, v)
        if name == "MANIFEST.json":
            continue
        size = os.path.getsize(path)
        n_files += 1
        n_bytes += size
        out.append((dep, name, "bytes", size))
        low = name.lower()
        try:
            if low.endswith((".xlsx", ".xlsm")):
                xlsx_sheets(dep, name, path)
            elif low.endswith(".xls"):
                for ws in xlrd.open_workbook(path).sheets():
                    table(dep, name, f"sheet:{ws.name}", [ws.row_values(i) for i in range(ws.nrows)])
            elif low.endswith((".csv", ".tsv")):
                with open(path, newline="", encoding="utf-8-sig", errors="replace") as f:
                    table(dep, name, "", list(csv.reader(f, delimiter="\t" if low.endswith(".tsv") else ",")))
            elif low.endswith((".txt", ".md", ".r", ".m")):
                with open(path, encoding="utf-8-sig", errors="replace") as f:
                    lines = [l for l in f.read().splitlines() if l.strip()]
                out.append((dep, name, "lines", len(lines)))
                if low.endswith((".txt", ".md")):
                    out.append((dep, name, "first_line", lines[0][:200] if lines else ""))
            elif low.endswith(".tps"):
                with open(path, encoding="utf-8", errors="replace") as f:
                    lines = f.read().splitlines()
                out.append((dep, name, "tps_specimens", sum(l.startswith("ID=") for l in lines)))
                out.append((dep, name, "tps_landmark_blocks", sum(bool(re.match(r"LM3?=", l)) for l in lines)))
            elif low.endswith(".zip"):
                with zipfile.ZipFile(path) as z:
                    members = [i for i in z.infolist() if not i.is_dir()]
                    out.append((dep, name, "zip_members", len(members)))
                    forks = [i for i in members if "__MACOSX/" in i.filename or os.path.basename(i.filename).startswith("._")]
                    if forks:
                        out.append((dep, name, "zip_mac_resource_forks_skipped", len(forks)))
                    for i in members:
                        if i in forks:
                            continue
                        out.append((dep, name, "zip_member", f"{i.filename} {i.file_size}"))
                        if i.filename.lower().endswith(".xlsx"):
                            xlsx_sheets(dep, f"{name}::{i.filename}", io.BytesIO(z.read(i.filename)))
                        elif i.filename.lower().endswith((".csv", ".tsv")):
                            text = io.TextIOWrapper(io.BytesIO(z.read(i.filename)), encoding="utf-8-sig", errors="replace", newline="")
                            table(dep, f"{name}::{i.filename}", "", list(csv.reader(text, delimiter="\t" if i.filename.lower().endswith(".tsv") else ",")))
                        else:
                            out.append((dep, f"{name}::{i.filename}", "not_parsed", os.path.splitext(i.filename)[1]))
                            skipped[os.path.splitext(i.filename)[1].lower()] += 1
            else:
                ext = os.path.splitext(low)[1]
                out.append((dep, name, "not_parsed", ext))
                skipped[ext] += 1
        except Exception as e:  # report unreadable files, do not stop the inventory
            out.append((dep, name, "error", str(e)[:150]))

out.append(("(all)", "", "deposit_directories", len(deposits)))
out.append(("(all)", "", "files", n_files))
out.append(("(all)", "", "bytes", n_bytes))
out.append(("(all)", "", "not_parsed_types", "; ".join(f"{k} {n}" for k, n in sorted(skipped.items())) or "none"))

EMAIL = re.compile(r"[\w.+-]+\s*(@|\[at\])\s*[\w-]+((\.|\[dot\])[\w-]+)+")
with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["deposit", "file", "metric", "value"])
    w.writerows([[EMAIL.sub("[email removed]", str(c)) for c in row] for row in out])  # headers can carry authors' addresses
