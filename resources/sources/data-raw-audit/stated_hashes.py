"""Check the sha256 values that tracked notes state against a data/raw inventory.

Usage: python3 stated_hashes.py REPO_DATA_DIR RAW_INVENTORY_TSV MAIN_MEMBERS_TSV OUT_TSV

Every 64-hex string in a tracked file under REPO_DATA_DIR (README.md, .tsv,
.json, .py, .R) that names data/raw/ anywhere is looked up among the raw
files and zip members, and written with its file, line and match. Such a file
also states hashes of its own outputs and of scratch files, so an unmatched
hash needs reading in context. Standard library only.
"""

import csv
import os
import re
import sys

data, inv, mem, out = sys.argv[1:5]
known = {}
for r in csv.DictReader(open(inv), delimiter="\t"):
    known.setdefault(r["sha256"], f"{r['holding']}/{r['path']}")
for r in csv.DictReader(open(mem), delimiter="\t"):
    known.setdefault(r["sha256"], f"{os.path.basename(r['zip'].split('::')[0])} :: {r['member']}")
HEX = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")
rows = [["note", "line", "sha256", "matches"]]
for dp, dn, fn in os.walk(data):
    dn[:] = sorted(d for d in dn if d not in ("raw", "derived"))
    for f in sorted(fn):
        if not f.endswith((".md", ".tsv", ".json", ".py", ".R")):
            continue
        p = os.path.join(dp, f)
        text = open(p, encoding="utf-8", errors="replace").read()
        if "data/raw/" not in text:
            continue
        for i, line in enumerate(text.splitlines()):
            for h in HEX.findall(line):
                rows.append([os.path.relpath(p, os.path.dirname(data)), i + 1, h, known.get(h, "-")])
with open(out, "w", newline="") as fo:
    csv.writer(fo, delimiter="\t", lineterminator="\n").writerows(rows)
n = len(rows) - 1
print(f"{n} stated hashes in notes that name data/raw; {sum(1 for r in rows[1:] if r[3] != '-')} match a raw file or zip member")
