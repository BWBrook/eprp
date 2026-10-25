"""Inventory a data/raw tree (read-only): holding, path, bytes, sha256 and zip member count per file.

Usage: python3 raw_inventory.py ROOT OUT_TSV

A holding is ROOT's first-level directory. .DS_Store, .Rhistory and
.Rproj.user are skipped. Standard library only.
"""

import collections
import csv
import hashlib
import os
import sys
import zipfile

root, out = sys.argv[1], sys.argv[2]
rows = []
for d in sorted(os.listdir(root)):
    for dp, dn, fn in os.walk(os.path.join(root, d)):
        dn[:] = sorted(x for x in dn if x != ".Rproj.user")
        for f in sorted(fn):
            if f in (".DS_Store", ".Rhistory"):
                continue
            p = os.path.join(dp, f)
            h = hashlib.sha256()
            with open(p, "rb") as fh:
                for b in iter(lambda: fh.read(1 << 22), b""):
                    h.update(b)
            members = ""
            if f.endswith(".zip"):
                try:
                    with zipfile.ZipFile(p) as z:
                        members = str(len(z.namelist()))
                except zipfile.BadZipFile:
                    members = "bad zip"
            rows.append([d, os.path.relpath(p, os.path.join(root, d)), os.path.getsize(p), h.hexdigest(), members])
with open(out, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["holding", "path", "bytes", "sha256", "zip_members"])
    w.writerows(rows)
n, b = collections.Counter(), collections.Counter()
for r in rows:
    n[r[0]] += 1
    b[r[0]] += r[2]
for k in sorted(n):
    print(f"{k}\t{n[k]} files\t{b[k]} bytes")
