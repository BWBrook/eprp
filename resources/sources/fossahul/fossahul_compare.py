"""Compare FosSahul copies: the 2019 and March 2021 CSVs, and the OCTOPUS WFS layer.

Usage: python3 fossahul_compare.py CSV_2019 CSV_2021 OCTOPUS_CSV

Matches records by ID (OCTOPUS OBSID1 is "FOS" + zero-padded ID) and reports
records added, removed and changed in age, quality, coordinates or taxonomy.
Standard library only.
"""

import csv
import re
import sys
from collections import Counter


def load(path):
    # Normalise 2019 raw headers to the R make.names() forms used in 2021.
    rows = csv.DictReader(open(path, newline="", encoding="utf-8-sig"))
    return {r["ID"]: {re.sub(r"[^A-Za-z0-9_]", ".", k): v for k, v in r.items()} for r in rows}


old, new = load(sys.argv[1]), load(sys.argv[2])
octo = list(csv.DictReader(open(sys.argv[3], newline="", encoding="utf-8", errors="replace")))
old = {k: v for k, v in old.items() if k.strip().isdigit()}
new = {k: v for k, v in new.items() if k.strip().isdigit()}
print(f"rows_2019_numeric_ids\t{len(old)}")
print(f"rows_2021_numeric_ids\t{len(new)}")
print(f"ids_added_2021\t{len(new.keys() - old.keys())}")
print(f"ids_removed_2021\t{len(old.keys() - new.keys())}")
shared = old.keys() & new.keys()
for col in ["Age", "Precision", "Quality", "preQuality", "Latitude", "Longitude", "Genus", "Species", "Status",
            "Association", "DatingTechnique"]:
    print(f"shared_ids_changed:{col}\t{sum(old[i][col] != new[i][col] for i in shared)}")
moves = Counter(f"{old[i]['Quality']}->{new[i]['Quality']}" for i in shared if old[i]["Quality"] != new[i]["Quality"])
for k, v in moves.most_common():
    print(f"quality_change\t{k}\t{v}")
octo_ids = {r["OBSID1"][3:].lstrip("0") for r in octo if r["OBSID1"].startswith("FOS")}
print(f"octopus_rows\t{len(octo)}")
print(f"octopus_ids_matching_2021\t{len(octo_ids & new.keys())}")
print(f"2021_ids_missing_from_octopus\t{len(new.keys() - octo_ids)}")
missing = sorted(new.keys() - octo_ids, key=lambda x: int(x) if x.isdigit() else 0)
print(f"2021_ids_missing_from_octopus_list\t{','.join(missing[:30])}")
print(f"missing_from_octopus_with_nonnumeric_coords\t{sum(1 for i in missing if not new[i]['Latitude'].replace('.', '', 1).replace('-', '', 1).isdigit())}")
print(f"octopus_by:DBVERNO\t{dict(Counter(r['DBVERNO'] for r in octo))}")
