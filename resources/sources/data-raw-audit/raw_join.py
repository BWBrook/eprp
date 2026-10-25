"""Join a data/raw inventory and its zip members against the mirror, by sha256.

Usage: python3 raw_join.py DIR MIRROR_ROOT

Reads DIR/raw_inventory.tsv (raw_inventory.py), DIR/main_members.tsv
(zip_members.py over the raw tree's zips) and every DIR/mirror_members*.tsv
(zip_members.py over mirror zips, run from MIRROR_ROOT so paths are relative).
The mirror side also has every sha256 in every MANIFEST.json under
MIRROR_ROOT. Writes DIR/raw_join.tsv (kind, holding, path, bytes, first two
mirror matches) and prints, per holding, the files and bytes matched.
"""

import collections
import csv
import glob
import json
import os
import sys

d, root = sys.argv[1], sys.argv[2]
idx = collections.defaultdict(list)
for m in glob.glob(os.path.join(root, "**", "MANIFEST.json"), recursive=True):
    try:
        man = json.load(open(m))
    except (OSError, ValueError):
        continue
    for f in man.get("files", []):
        if f.get("sha256"):
            idx[f["sha256"]].append(os.path.relpath(os.path.join(os.path.dirname(m), f.get("key") or f.get("name", "")), root))
for p in sorted(glob.glob(os.path.join(d, "mirror_members*.tsv"))):
    for r in csv.DictReader(open(p), delimiter="\t"):
        idx[r["sha256"]].append(f"{r['zip'].split('/raw/')[0]} zip member {r['member']}")
items = [("file", r["holding"], r["path"], int(r["bytes"]), r["sha256"])
         for r in csv.DictReader(open(os.path.join(d, "raw_inventory.tsv")), delimiter="\t")]
for r in csv.DictReader(open(os.path.join(d, "main_members.tsv")), delimiter="\t"):
    holding = r["zip"].split("/data/raw/")[1].split("/")[0]
    items.append(("zip member", holding, f"{os.path.basename(r['zip'].split('::')[0])} :: {r['member']}", int(r["bytes"]), r["sha256"]))
summary = collections.defaultdict(lambda: [0, 0, 0, 0, collections.Counter()])
with open(os.path.join(d, "raw_join.tsv"), "w", newline="") as fo:
    w = csv.writer(fo, delimiter="\t", lineterminator="\n")
    w.writerow(["kind", "holding", "path", "bytes", "mirror_match"])
    for kind, h, p, b, s in items:
        hits = sorted(set(idx.get(s, [])))
        w.writerow([kind, h, p, b, "; ".join(hits[:2]) or "-"])
        if kind == "file":
            su = summary[h]
            su[0] += 1
            su[1] += b
            if hits:
                su[2] += 1
                su[3] += b
                su[4][hits[0].split("/raw/")[0].split(" zip member")[0]] += 1
for h, (n, b, m, mb, where) in sorted(summary.items()):
    print(f"{h}\t{m}/{n} files\t{mb}/{b} bytes matched\t{dict(where)}")
