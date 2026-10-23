"""Build data_mirror.py url specs for ALA facets of EPBC extinct species that have records from 1950 on.

Usage: python3 ala_extinct_specs.py ALA_FACETS_SNAPSHOT EPBC_SPECIES_CSV OUT_SPECS

For each EPBC extinct species (current name where EPBC gives one; species-level
entries only) with records from 1950 on in the facet snapshot, one query
returning those records' basis of record, data resource, decade, state, year
and raw name. Also the NSW BioNet Atlas records of Perameles fasciata and P.
nasuta by year from 2015, to compare the two names in that provider. Standard
library only.
"""

import csv
import glob
import json
import os
import sys
import urllib.parse

snap, epbc_csv, out = sys.argv[1:4]
B = "https://biocache-ws.ala.org.au/ws/occurrences/search?q=*:*&pageSize=0&flimit=50"
F = "&facets=basis_of_record&facets=dataResourceName&facets=decade&facets=stateProvince&facets=year&facets=raw_scientificName"
since = {}
for p in glob.glob(os.path.join(snap, "species_*_since1950.json")):
    with open(p, encoding="utf-8") as f:
        since.update({r["label"]: r["count"] for r in json.load(f)["facetResults"][0]["fieldResult"]})
specs = []
with open(epbc_csv, newline="", encoding="utf-8-sig") as f:
    for r in csv.DictReader(f):
        name = r["Scientific Name"].strip() if r["Current Scientific Name"].strip() in ("", "-") else r["Current Scientific Name"].strip()
        if r["Threatened status"] == "Extinct" and len(name.split()) == 2 and since.get(name):
            q = urllib.parse.quote(f'species:"{name}"')
            specs.append(f'extinct__{name.replace(" ", "_")}.json::{B}&fq=country:Australia&fq={q}&fq=year:%5B1950%20TO%20*%5D{F}')
for name in ("Perameles fasciata", "Perameles nasuta"):
    q = urllib.parse.quote(f'species:"{name}"')
    r = urllib.parse.quote('dataResourceName:"NSW BioNet Atlas"')
    specs.append(f'bionet__{name.replace(" ", "_")}.json::{B}&fq={q}&fq={r}&fq=year:%5B2015%20TO%20*%5D&facets=year')
with open(out, "w") as f:
    f.write("\n".join(sorted(set(specs))) + "\n")
print(len(specs), "specs")
