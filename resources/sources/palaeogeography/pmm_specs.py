"""NAME::URL lines for every file the GPlates Plate Model Manager index lists.

Usage: python3 pmm_specs.py MODELS_JSON SPECS_OUT

The index (https://repo.gplates.org/webdav/pmm/config/models.json) names each
plate model's rotation file and layers (static polygons, coastlines,
topologies and others) as zip URLs; aliases ("@name") are skipped. Files are
named <model>__<layer>.zip. Time-dependent rasters (age grids) are not listed:
they run to thousands of files per model. Standard library only.
"""

import json
import sys

models = json.load(open(sys.argv[1], encoding="utf-8"))
lines = []
for name, m in models.items():
    if not isinstance(m, dict) or "Rotations" not in m:
        continue
    for layer, url in {"Rotations": m["Rotations"], **m.get("Layers", {})}.items():
        lines.append(f"{name}__{layer}.zip::{url}")
with open(sys.argv[2], "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(len(lines), "files from", sum(1 for m in models.values() if isinstance(m, dict) and "Rotations" in m), "models")
