# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl==3.1.5"]
# ///
"""Profile the SHAPE / OZ-INTIMATE palaeoarchive index (PANGAEA 879515, one xlsx sheet).

Usage: uv run shape_profile.py DATABASE_SUPPLEMENT2_XLSX OUT_TSV

Counts records and filled cells per column, record types and region codes, and
how many rows give a link to data. Writes long-format (table, metric, key, value).
"""

import csv
import re
import sys
from collections import Counter

import openpyxl

ws = openpyxl.load_workbook(sys.argv[1], read_only=True).worksheets[0]
rows = [r for r in ws.iter_rows(values_only=True)]
header = [str(h).strip() if h is not None else "" for h in rows[0]]
data = [r for r in rows[1:] if any(v not in (None, "") for v in r)]
out = [("sheet", "name", "", ws.title), ("sheet", "dimensions", "", ws.max_row and f"{ws.max_row} x {ws.max_column}"),
       ("records", "rows", "", len(data))]
for i, h in enumerate(header):
    if h:
        out.append(("columns", "filled", h, sum(r[i] not in (None, "") for r in data)))
col = {h.split(" (")[0]: i for i, h in enumerate(header)}
kinds = {"coral": "coral", "marine": "marine core", "speleothem": "speleothem", "lake": "lake", "swamp": "swamp or peat",
         "peat": "swamp or peat", "pollen": "swamp or peat"}
for k, v in Counter(next((n for w, n in kinds.items() if w in str(r[col["Record Type"]]).lower()), "other")
                    for r in data).most_common():
    out.append(("records", "by:record_type_class", k, v))
codes = Counter(c for r in data for c in re.findall(r"\b(TNW|TSW|TNE|TSE|StA|TeE|TeS|NSO|SSO)\b", str(r[col["Region/Country"]])))
for k, v in codes.most_common():
    out.append(("records", "by:region_code", k, v))
link = header.index(next(h for h in header if h.startswith("Link")))
out.append(("records", "link_cell_with_url", "", sum("http" in str(r[link]) or "doi" in str(r[link]).lower() for r in data)))
with open(sys.argv[2], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
