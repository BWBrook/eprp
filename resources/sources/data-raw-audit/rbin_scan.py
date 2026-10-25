"""Find R binaries (loose and in zips) under a tree and read their PBDB occurrence numbers.

Usage: python3 rbin_scan.py ROOT OUT_DIR WORK_DIR
       python3 rbin_scan.py --summarise OUT_DIR

A holding is the path before /raw/ when the file sits under a raw/ directory
(the mirror's layout), otherwise ROOT's first-level directory (data/raw's
layout). Loose .RData, .rda and .rds files are read in place; such members
of .zip files (nested zips one level down) are extracted to WORK_DIR first.
Package internals (renv libraries, Meta/, help/, R/sysdata.rda) are skipped,
and so is the literature library. rdata_occurrence_ids.R, next to this
script, does the reading, one Rscript call per holding. Finally its
per-object table is summarised to OUT_DIR/rdata_files.tsv, one row per file
(--summarise redoes only that step).
"""

import collections
import csv
import io
import os
import re
import subprocess
import sys
import zipfile


def summarise(out_dir):
    per = {}
    with open(os.path.join(out_dir, "rdata_objects.tsv"), newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            d = per.setdefault((r["prefix"], r["file"]), [0, set(), r["distinct_in_file"], r["ids_file"], []])
            if r["object"] == "-":
                if r["occurrence_column"] != "no data frames":
                    d[4].append(r["occurrence_column"])
            else:
                d[0] += 1
                if r["occurrence_column"] != "-":
                    d[1].add(r["occurrence_column"])
    with open(os.path.join(out_dir, "rdata_files.tsv"), "w", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["prefix", "file", "data_frames", "occurrence_columns", "distinct", "ids_file", "notes"])
        for (p, fn), (n, occ, dist, ids, notes) in per.items():
            w.writerow([p, fn, n, ";".join(sorted(occ)) or "-", dist, ids, " | ".join(notes) or "-"])


if sys.argv[1] == "--summarise":
    summarise(sys.argv[2])
    sys.exit()

root, out_dir, work = (os.path.abspath(a) for a in sys.argv[1:4])
RBIN = (".rdata", ".rda", ".rds")
PKG = re.compile(r"(^|/)(renv|Meta|help|library)/|(^|/)R/sysdata\.rda$")
here = os.path.dirname(os.path.abspath(__file__))


def holding(rel):
    return rel.split("/raw/")[0] if "/raw/" in rel else rel.split("/")[0]


def safe(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "~", name)


found = {}


def from_zip(h, zf, dest, depth=0):
    for m in zf.infolist():
        f = m.filename
        if m.is_dir() or "__MACOSX" in f or PKG.search(f):
            continue
        if f.lower().endswith(RBIN):
            os.makedirs(dest, exist_ok=True)
            target = os.path.join(dest, safe(f))
            if not os.path.exists(target):
                with zf.open(m) as src, open(target, "wb") as out:
                    while chunk := src.read(1 << 22):
                        out.write(chunk)
            found.setdefault(h, []).append(target)
        elif f.lower().endswith(".zip") and depth == 0:
            with zf.open(m) as src:
                from_zip(h, zipfile.ZipFile(io.BytesIO(src.read())), os.path.join(dest, safe(f)), 1)


for dp, dn, fn in os.walk(root):
    rel_dir = os.path.relpath(dp, root)
    dn[:] = sorted(d for d in dn if not (rel_dir == "." and d == "library") and d not in ("derived", ".Rproj.user"))
    for f in sorted(fn):
        p = os.path.join(dp, f)
        rel = os.path.relpath(p, root)
        h = holding(rel)
        if f.lower().endswith(RBIN) and not PKG.search(rel):
            found.setdefault(h, []).append(p)
        elif f.lower().endswith(".zip"):
            try:
                from_zip(h, zipfile.ZipFile(p), os.path.join(work, safe(h), safe(rel)))
            except zipfile.BadZipFile:
                print("bad zip:", rel)

os.makedirs(out_dir, exist_ok=True)
for h, files in sorted(found.items()):
    subprocess.run(["Rscript", os.path.join(here, "rdata_occurrence_ids.R"), out_dir, safe(h), *files], check=False)
summarise(out_dir)
print(sum(len(v) for v in found.values()), "R binaries in", len(found), "holdings")
