"""Compare two copies of the AustArch CSV (e.g. the ADS download and a copy from the authors).

Usage: python3 compare_copies.py CSV_A CSV_B

Reports encoding and line-ending traits, row and column counts, header
differences, ADSIDs present in only one copy, and per-column value differences
for shared ADSIDs (after stripping whitespace). Standard library only.
"""

import csv
import io
import sys
from collections import Counter


def load(path):
    raw = open(path, "rb").read()
    traits = {"bytes": len(raw), "bom": raw.startswith(b"\xef\xbb\xbf"), "crlf": raw.count(b"\r\n"),
              "lf_only": raw.count(b"\n") - raw.count(b"\r\n")}
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            text = raw.decode(enc)
            traits["decodes_as"] = enc
            break
        except UnicodeDecodeError:
            continue
    rows = list(csv.reader(io.StringIO(text, newline="")))
    return traits, rows[0], rows[1:]


(ta, ha, ra), (tb, hb, rb) = load(sys.argv[1]), load(sys.argv[2])
print("A", ta, "rows", len(ra), "cols", len(ha))
print("B", tb, "rows", len(rb), "cols", len(hb))
print("header_only_in_A", [h for h in ha if h not in hb])
print("header_only_in_B", [h for h in hb if h not in ha])
ia, ib = ha.index("ADSID"), hb.index("ADSID")
da = {r[ia].strip(): r for r in ra if len(r) > ia}
db = {r[ib].strip(): r for r in rb if len(r) > ib}
print("ADSID_only_in_A", len(da.keys() - db.keys()), sorted(da.keys() - db.keys())[:10])
print("ADSID_only_in_B", len(db.keys() - da.keys()), sorted(db.keys() - da.keys())[:10])
diffs = Counter()
example = {}
for k in da.keys() & db.keys():
    for col in ha:
        if col in hb and col:
            va = da[k][ha.index(col)].strip() if ha.index(col) < len(da[k]) else ""
            vb = db[k][hb.index(col)].strip() if hb.index(col) < len(db[k]) else ""
            if va != vb:
                diffs[col] += 1
                example.setdefault(col, (k, va[:60], vb[:60]))
for col, n in diffs.most_common():
    print("column_differs", col, n, "e.g.", example[col])
print("shared_ADSIDs", len(da.keys() & db.keys()), "with_any_difference",
      sum(1 for k in da.keys() & db.keys() if any(
          (da[k][ha.index(c)].strip() if ha.index(c) < len(da[k]) else "") !=
          (db[k][hb.index(c)].strip() if hb.index(c) < len(db[k]) else "") for c in ha if c in hb and c)))
