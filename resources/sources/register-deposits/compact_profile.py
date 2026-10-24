"""Compact a deposits profile for the repository; the full profile stays in the mirror's derived/.

Usage: python3 compact_profile.py FULL_TSV OUT_TSV

For zips with more than 250 members, the per-member zip_member and not_parsed
rows are replaced by one zip_members_by_extension row (count and bytes per
extension). Table, sheet and text rows are kept, except those for files in a
bundled R package library (a path containing /renv/library/), which are dropped
and counted in a renv_library_rows_dropped row.
"""

import csv
import sys
from collections import Counter, defaultdict

LIMIT = 250
rows = list(csv.reader(open(sys.argv[1], newline=""), delimiter="\t"))
head, body = rows[0], rows[1:]
members = {(r[0], r[1]): int(r[3]) for r in body if r[2] == "zip_members"}
big = {k for k, n in members.items() if n > LIMIT}
renv = Counter()
ext_n, ext_b = defaultdict(Counter), defaultdict(Counter)
out = []
for r in body:
    dep, f, metric, value = r[0], r[1], r[2], r[3]
    zipname = f.split("::", 1)[0]
    member = f.split("::", 1)[1] if "::" in f else (value.rsplit(" ", 1)[0] if metric == "zip_member" else "")
    if (dep, zipname) in big and metric in ("zip_member", "not_parsed"):
        if metric == "zip_member":
            name, size = value.rsplit(" ", 1)
            base = name.rsplit("/", 1)[-1]
            ext = base.rsplit(".", 1)[-1].lower() if "." in base else "(none)"
            ext_n[(dep, zipname)][ext] += 1
            ext_b[(dep, zipname)][ext] += int(size)
        continue
    if "/renv/library/" in member:
        renv[(dep, zipname)] += 1
        continue
    out.append(r)
    if metric == "zip_members" and (dep, f) in big:
        out.append([dep, f, "zip_members_by_extension", ""])
for r in out:
    if r[2] == "zip_members_by_extension":
        k = (r[0], r[1])
        r[3] = "; ".join(f"{e} {n} ({ext_b[k][e]})" for e, n in ext_n[k].most_common())
for (dep, z), n in sorted(renv.items()):
    i = max(i for i, r in enumerate(out) if r[0] == dep)
    out.insert(i + 1, [dep, z, "renv_library_rows_dropped", str(n)])
with open(sys.argv[2], "w", newline="") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(head)
    w.writerows(out)
print(len(body), "->", len(out), "rows; big zips", sorted(big), "; renv rows dropped", dict(renv))
