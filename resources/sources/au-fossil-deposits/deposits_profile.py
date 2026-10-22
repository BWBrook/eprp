# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Inventory the small Australian fossil-biota deposits mirrored under au-fossil-deposits/.

Usage: uv run deposits_profile.py AU_FOSSIL_DEPOSITS_DIR OUT_TSV

For each deposit's latest raw version: every file with its size; spreadsheet
sheets with rows and columns and their header row; CSV rows and header; zip
members. Writes long-format (deposit, file, metric, value).
"""

import csv
import glob
import io
import os
import sys
import zipfile

import openpyxl

csv.field_size_limit(1 << 30)
out = []
root = sys.argv[1]
for dep in sorted(d for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))):
    versions = sorted(glob.glob(os.path.join(root, dep, "raw", "*")))
    if not versions:
        continue
    v = versions[-1]
    out.append((dep, "", "version_dir", os.path.basename(v)))
    for path in sorted(glob.glob(os.path.join(v, "*"))):
        name = os.path.basename(path)
        if name == "MANIFEST.json":
            continue
        out.append((dep, name, "bytes", os.path.getsize(path)))
        low = name.lower()
        try:
            if low.endswith((".xlsx", ".xlsm")):
                wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
                for ws in wb.worksheets:
                    rows = list(ws.iter_rows(values_only=True))
                    filled = [r for r in rows if any(c not in (None, "") for c in r)]
                    head = [str(c) for c in (filled[0] if filled else []) if c not in (None, "")][:12]
                    out.append((dep, name, f"sheet:{ws.title}", f'{len(filled)} rows x {max((len(r) for r in filled), default=0)} cols | {"; ".join(head)[:200]}'))
            elif low.endswith((".csv", ".txt", ".tsv")):
                with open(path, newline="", encoding="utf-8", errors="replace") as f:
                    text = f.read()
                lines = [l for l in text.splitlines() if l.strip()]
                out.append((dep, name, "lines", len(lines)))
                out.append((dep, name, "header", lines[0][:200] if lines else ""))
            elif low.endswith(".zip"):
                with zipfile.ZipFile(path) as z:
                    members = [i for i in z.infolist() if not i.is_dir()]
                    out.append((dep, name, "zip_members", len(members)))
                    for i in members[:8]:
                        out.append((dep, name, "zip_member", f"{i.filename} {i.file_size}"))
        except Exception as e:  # report unreadable files, do not stop the inventory
            out.append((dep, name, "error", str(e)[:150]))

with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["deposit", "file", "metric", "value"])
    w.writerows(out)
