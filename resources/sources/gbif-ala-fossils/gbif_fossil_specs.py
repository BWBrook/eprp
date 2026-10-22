"""Build data_mirror.py url specs for GBIF fossil-specimen records of given countries.

Usage: python3 gbif_fossil_specs.py OUT_SPECS COUNTRY [COUNTRY ...]

GBIF's occurrence search pages slowly beyond an offset of about 10,000, so each
query is partitioned to 9,000 records or fewer: by dataset, then, for larger
datasets, by latitude bisection plus the records without coordinates. The
Neptune deep-sea microfossil dataset is left out (it is NSB's frozen copy; see
the nsb entry). Writes one NAME::URL line per page, plus each country's count
and dataset facet and each dataset's metadata. Standard library only.
"""

import json
import sys
import time
import urllib.request

G = "https://api.gbif.org/v1/occurrence/search"
UA = "eprp-data-mirror/4 (research data archive)"
LIMIT, MAXPART = 300, 9000


def get(url):
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=300) as r:
                time.sleep(0.5)
                return json.load(r)
        except OSError:
            if attempt == 3:
                raise
            time.sleep(10 * (attempt + 1))


def count(q):
    return get(f"{G}?{q}&limit=0")["count"]


def split_lat(q, lo, hi):
    n = count(f"{q}&decimalLatitude={lo},{hi}")
    if n == 0:
        return []
    if n <= MAXPART or hi - lo < 0.001:
        return [(f"decimalLatitude={lo},{hi}", n)]
    mid = round((lo + hi) / 2, 6)
    return split_lat(q, lo, mid) + split_lat(q, mid, hi)


specs, out = [], sys.argv[1]
for cc in sys.argv[2:]:
    base = f"basisOfRecord=FOSSIL_SPECIMEN&country={cc}"
    specs.append(f"{cc}__count.json::{G}?{base}&limit=0")
    specs.append(f"{cc}__datasets.json::{G}?{base}&limit=0&facet=datasetKey&facetLimit=1000")
    facets = get(f"{G}?{base}&limit=0&facet=datasetKey&facetLimit=1000")["facets"][0]["counts"]
    for f in facets:
        key, n = f["name"], f["count"]
        meta = get(f"https://api.gbif.org/v1/dataset/{key}")
        specs.append(f"dataset__{key}.json::https://api.gbif.org/v1/dataset/{key}")
        if "Neptune" in meta.get("title", ""):
            print(cc, "skipping", meta["title"], n, flush=True)
            continue
        q = f"{base}&datasetKey={key}"
        parts = [("", n)] if n <= MAXPART else \
            split_lat(q, -90, 90) + [("hasCoordinate=false", count(f"{q}&hasCoordinate=false"))]
        for i, (pq, pn) in enumerate(p for p in parts if p[1] > 0):
            qq = f"{q}&{pq}" if pq else q
            for off in range(0, pn, LIMIT):
                specs.append(f"{cc}__{key}__p{i:02d}__{off:05d}.json::{G}?{qq}&limit={LIMIT}&offset={off}")
with open(out, "w") as f:
    f.write("\n".join(dict.fromkeys(specs)) + "\n")
print(len(specs), "specs", flush=True)
