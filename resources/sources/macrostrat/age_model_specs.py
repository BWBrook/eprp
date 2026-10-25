"""Write the file list for Macrostrat's age models, one request per column of a snapshot.

Usage: python3 age_model_specs.py SNAPSHOT_DIR SPECS_OUT

The age_model route needs a col_id (or section_id); the column ids are read
from the snapshot's columns__pNN.geojson files, project 14 (a composite of
the others) excepted. Standard library only.
"""

import glob
import json
import os
import sys

snap, specs_out = sys.argv[1:3]
ids = set()
for path in glob.glob(os.path.join(snap, "columns__p*.geojson")):
    if path.endswith("columns__p14.geojson") or os.path.getsize(path) < 200:
        continue
    ids |= {f["properties"]["col_id"] for f in json.load(open(path, encoding="utf-8"))["success"]["data"]["features"]}
with open(specs_out, "w", encoding="utf-8") as f:
    f.writelines(f"age_model__c{c:05d}.csv::https://macrostrat.org/api/v2/age_model?col_id={c}&format=csv\n" for c in sorted(ids))
print(len(ids), "columns")
