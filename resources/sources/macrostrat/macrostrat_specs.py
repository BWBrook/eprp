"""Write the file list for a dated Macrostrat snapshot (`data_mirror.py url --specs-file`).

Usage: python3 macrostrat_specs.py SPECS_OUT

Macrostrat has no bulk download, so a snapshot is a set of API v2 requests.
The project list is read first (defs/projects); for every project the
columns (GeoJSON), units, sections, PBDB collection links and measurements
are requested with all three column statuses (active, in process,
obsolete), and every definition table is requested once, with the
per-project statistics. Standard library only; no contact details are sent.
"""

import json
import sys
import urllib.request

B = "https://macrostrat.org/api/v2"
UA = {"User-Agent": "eprp-data-mirror/4 (research data archive)"}
STATUS = "status_code=active,in%20process,obsolete"
DEFS = ["lithologies", "lithology_attributes", "environments", "econs", "intervals", "timescales", "strat_names",
        "strat_name_concepts", "sources", "refs", "projects", "groups", "measurements", "grainsizes",
        "drilling_sites", "minerals", "structures", "plates", "columns"]

projects = json.load(urllib.request.urlopen(urllib.request.Request(f"{B}/defs/projects?all", headers=UA), timeout=120))
ids = sorted(int(p["project_id"]) for p in projects["success"]["data"])
lines = [f"stats.csv::{B}/stats?all&format=csv"]
lines += [f"defs__{d}.json::{B}/defs/{d}?all" for d in DEFS]
for p in ids:
    lines += [
        f"columns__p{p:02d}.geojson::{B}/columns?project_id={p}&{STATUS}&response=long&format=geojson",
        f"units__p{p:02d}.csv::{B}/units?project_id={p}&{STATUS}&response=long&format=csv",
        f"sections__p{p:02d}.csv::{B}/sections?project_id={p}&{STATUS}&response=long&format=csv",
        f"fossils__p{p:02d}.csv::{B}/fossils?project_id={p}&format=csv",
        f"measurements__p{p:02d}.csv::{B}/measurements?project_id={p}&response=long&show_values&format=csv",
    ]
with open(sys.argv[1], "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(json.dumps({"projects": ids, "requests": len(lines)}))
