"""How far do PBDB's ocean-drilling collections duplicate NSB? Hole- and core-level matching.

Usage: python3 pbdb_nsb_overlap.py GLOBAL_SNAPSHOT NSB_SQLITE OUT_TSV

PBDB collections named like "363-U1482A-1H-CC 0/14 FORAMB" (expedition, site
and hole, core, section, then a fossil-group code) are parsed to an NSB-style
hole key ("363_1482A": the U or C prefix dropped) and a core number, and
matched to NSB's holes and to the cores of its samples. Reports collections
and occurrences parsed, by creation date (the 2025-09-21 bulk partition or
not), matched at hole and at core level, and NSB holes and samples that PBDB
lacks. Standard library only.
"""

import csv
import glob
import os
import re
import sqlite3
import sys
from collections import Counter

csv.field_size_limit(1 << 30)
snap, db, out_path = sys.argv[1:4]
NAME = re.compile(r"^(\d+)-([UC]?)(\d+[A-Z])-(\d+)[A-Z]?-")
BULK = "2025-09-21 22:25"
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
nsb_holes = {h for (h,) in con.execute("select hole_id from neptune_hole_summary")}
nsb_cores = Counter((h, str(c).lstrip("0")) for h, c in con.execute("select hole_id, core from neptune_sample"))
out, coll_key = [], {}
for p in sorted(glob.glob(os.path.join(snap, "collections__p*.csv"))):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        h = next(rd)
        i = {k: h.index(k) for k in ("collection_no", "collection_name", "created")}
        for r in rd:
            m = NAME.match(r[i["collection_name"]])
            if m:
                coll_key[r[i["collection_no"]]] = (f"{m.group(1)}_{m.group(3)}", m.group(4).lstrip("0"), r[i["created"]].startswith(BULK))
occ = Counter()
for p in sorted(glob.glob(os.path.join(snap, "occurrences__p*.csv"))):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        ci = next(rd).index("collection_no")
        for r in rd:
            if r[ci] in coll_key:
                occ[r[ci]] += 1
stats = Counter()
pbdb_holes = set()
for cno, (hole, core, bulk) in coll_key.items():
    tag = "bulk_2025_09_21" if bulk else "other"
    stats[(tag, "collections")] += 1
    stats[(tag, "occurrences")] += occ[cno]
    pbdb_holes.add(hole)
    if hole in nsb_holes:
        stats[(tag, "collections_hole_in_nsb")] += 1
        stats[(tag, "occurrences_hole_in_nsb")] += occ[cno]
    if (hole, core) in nsb_cores:
        stats[(tag, "collections_core_in_nsb")] += 1
        stats[(tag, "occurrences_core_in_nsb")] += occ[cno]
for (tag, metric), n in sorted(stats.items()):
    out.append(("pbdb_drilling_collections", metric, tag, n))
out += [("holes", "pbdb_holes", "", len(pbdb_holes)), ("holes", "nsb_holes", "", len(nsb_holes)),
        ("holes", "shared", "", len(pbdb_holes & nsb_holes)), ("holes", "pbdb_only", "", len(pbdb_holes - nsb_holes)),
        ("holes", "nsb_only", "", len(nsb_holes - pbdb_holes))]
shared = pbdb_holes & nsb_holes
out.append(("holes", "nsb_samples_in_shared_holes", "", sum(n for (h, _), n in nsb_cores.items() if h in shared)))
legs = Counter(h.split("_")[0] for h in pbdb_holes - nsb_holes)
out += [("holes", "pbdb_only_by:expedition", k, n) for k, n in legs.most_common(10)]
with open(out_path, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
