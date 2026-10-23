"""How far do PBDB's ocean-drilling collections overlap NSB? Hole- and core-level matching.

Usage: python3 pbdb_nsb_overlap.py GLOBAL_SNAPSHOT NSB_SQLITE OUT_TSV

PBDB collections named like "363-U1482A-1H-CC 0/14 FORAMB" (expedition, site
and hole, core, section, then a fossil-group code) are parsed to an NSB-style
hole key ("363_1482A": the U or C prefix dropped) and a core number. NSB's
neptune_hole_summary is a catalogue of drilled holes; holes with data are those
with rows in neptune_sample. Reports PBDB collections and occurrences parsed;
holes in NSB's catalogue and holes NSB sampled; collections and occurrences in
sampled holes and at sampled cores; and, within the holes both sampled, the
cores each holds and shares. Standard library only.
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
NAME = re.compile(r"^(\d+)-([UC]?)(\d+[A-Z])-(\d+)[A-Z]*-")
con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
catalogue = {h for (h,) in con.execute("select hole_id from neptune_hole_summary")}
nsb_cores = Counter((h, str(c).lstrip("0")) for h, c in con.execute("select hole_id, core from neptune_sample"))
sampled = {h for h, _ in nsb_cores}
coll_key = {}
for p in sorted(glob.glob(os.path.join(snap, "collections__p*.csv"))):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        h = next(rd)
        i = {k: h.index(k) for k in ("collection_no", "collection_name")}
        for r in rd:
            m = NAME.match(r[i["collection_name"]])
            if m:
                coll_key[r[i["collection_no"]]] = (f"{m.group(1)}_{m.group(3)}", m.group(4).lstrip("0"))
occ = Counter()
for p in sorted(glob.glob(os.path.join(snap, "occurrences__p*.csv"))):
    with open(p, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        ci = next(rd).index("collection_no")
        for r in rd:
            if r[ci] in coll_key:
                occ[r[ci]] += 1
holes = {h for h, _ in coll_key.values()}
both = holes & sampled
pbdb_core_pairs = {k for k in coll_key.values() if k[0] in both}
nsb_core_pairs = {k for k in nsb_cores if k[0] in both}
out = [
    ("pbdb", "collections_parsed", "", len(coll_key)),
    ("pbdb", "occurrences_in_parsed_collections", "", sum(occ.values())),
    ("holes", "pbdb_holes", "", len(holes)),
    ("holes", "pbdb_holes_in_nsb_catalogue", "", len(holes & catalogue)),
    ("holes", "pbdb_holes_nsb_sampled", "", len(both)),
    ("holes", "nsb_samples_in_those_holes", "", sum(n for (h, _), n in nsb_cores.items() if h in both)),
    ("collections", "in_nsb_sampled_holes", "", sum(1 for k in coll_key.values() if k[0] in both)),
    ("collections", "at_nsb_sampled_cores", "", sum(1 for k in coll_key.values() if k in nsb_cores)),
    ("occurrences", "in_nsb_sampled_holes", "", sum(n for c, n in occ.items() if coll_key[c][0] in both)),
    ("occurrences", "at_nsb_sampled_cores", "", sum(n for c, n in occ.items() if coll_key[c] in nsb_cores)),
    ("cores_in_shared_holes", "pbdb", "", len(pbdb_core_pairs)),
    ("cores_in_shared_holes", "nsb", "", len(nsb_core_pairs)),
    ("cores_in_shared_holes", "shared", "", len(pbdb_core_pairs & nsb_core_pairs)),
]
out += [("holes", "pbdb_holes_not_nsb_sampled_by:expedition", k, n)
        for k, n in Counter(h.split("_")[0] for h in holes - sampled).most_common(10)]
with open(out_path, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
