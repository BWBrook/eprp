"""Distinct PBDB occurrence numbers in delimited text files and zip members.

Usage: python3 csv_occurrence_ids.py ROOT OUT_DIR

Walks every holding (first-level directory) under ROOT. Each .csv, .tsv and
.txt file, and each such member of a .zip (nested zips one level down), whose
header within its first 100 lines has an occurrence_no column is read; its
distinct numbers go to OUT_DIR/<holding>__<n>.ids, and OUT_DIR/ids_files.tsv
maps each .ids file to its source. Same column rule as
register-deposits/embedded_pbdb_check.py. Standard library only.
"""

import csv
import io
import os
import re
import sys
import zipfile

root, out_dir = sys.argv[1], sys.argv[2]
os.makedirs(out_dir, exist_ok=True)
csv.field_size_limit(1 << 30)
OCC = re.compile(r"^(?:.*\.)?occurrence_no(?:\.x)?$", re.I)
TEXT = (".csv", ".tsv", ".txt")
index = [["ids_file", "holding", "source", "column", "rows"]]
count = {}


def scan(holding, label, stream):
    for _ in range(100):
        line = stream.readline()
        if not line:
            return
        if "occurrence_no" in line:
            break
    else:
        return
    delim = "\t" if line.count("\t") > line.count(",") else ","
    header = next(csv.reader([line], delimiter=delim))
    cols = [i for i, h in enumerate(header) if OCC.match(h.strip())]
    if not cols:
        return
    ids, n = set(), 0
    for row in csv.reader(stream, delimiter=delim):
        n += 1
        for i in cols:
            if i < len(row) and row[i].strip().isdigit():
                ids.add(int(row[i]))
    count[holding] = count.get(holding, 0) + 1
    name = f"{holding}__{count[holding]:03d}.ids"
    with open(os.path.join(out_dir, name), "w") as f:
        f.write("\n".join(map(str, sorted(ids))) + "\n")
    index.append([name, holding, label, ";".join(header[i] for i in cols), n])


def walk_zip(holding, label, zf, depth=0):
    for m in zf.infolist():
        if m.is_dir() or "__MACOSX" in m.filename:
            continue
        low = m.filename.lower()
        if low.endswith(TEXT):
            with zf.open(m) as raw:
                scan(holding, f"{label} :: {m.filename}", io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline=""))
        elif low.endswith(".zip") and depth == 0:
            with zf.open(m) as raw:
                walk_zip(holding, f"{label} :: {m.filename}", zipfile.ZipFile(io.BytesIO(raw.read())), 1)


for holding in sorted(os.listdir(root)):
    for dp, dn, fn in os.walk(os.path.join(root, holding)):
        dn[:] = sorted(x for x in dn if x != ".Rproj.user")
        for f in sorted(fn):
            p = os.path.join(dp, f)
            rel = os.path.relpath(p, os.path.join(root, holding))
            if f.lower().endswith(TEXT):
                with open(p, encoding="utf-8", errors="replace", newline="") as s:
                    scan(holding, rel, s)
            elif f.lower().endswith(".zip"):
                walk_zip(holding, rel, zipfile.ZipFile(p))
with open(os.path.join(out_dir, "ids_files.tsv"), "w", newline="") as f:
    csv.writer(f, delimiter="\t", lineterminator="\n").writerows(index)
print(len(index) - 1, "files with occurrence numbers")
