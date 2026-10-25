"""Compare a PBDB intervals JSON download (compact vocabulary) with the catalogue's intervals.csv.

Usage: python3 intervals_compare.py INTERVALS_JSON INTERVALS_CSV

Matches on interval number and compares name, base age and top age; prints
each difference and a summary line. Standard library only.
"""

import csv
import json
import sys

j = json.load(open(sys.argv[1]))
cur = {r["interval_no"]: r for r in csv.DictReader(open(sys.argv[2], newline=""))}
missing = differ = 0
for r in j["records"]:
    n = r["oid"].split(":")[1]
    c = cur.get(n)
    if c is None:
        missing += 1
        print("missing", n, r["nam"])
        continue
    a = (r["nam"], float(r["eag"]), float(r["lag"]))
    b = (c["interval_name"], float(c["b_age"]), float(c["t_age"]))
    if a != b:
        differ += 1
        print("differs", n, a, b)
print(f"{len(j['records'])} intervals; {missing} missing from the snapshot; {differ} differ in name or ages")
