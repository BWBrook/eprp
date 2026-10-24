"""List every version of chronosphere's PBDB record on Zenodo with its version index and API calls.

Usage: python3 zenodo_survey.py OUT_TSV

One row per version: record, version string, Zenodo's version index,
publication date, the occurrence and taxon API calls quoted in the
description, file names and sizes, licence. Zenodo's index is kept because it
is broken for this record (see the entry). Standard library only; no contact
details are sent.
"""

import csv
import html
import json
import re
import sys
import time
import urllib.request

UA = {"User-Agent": "eprp-data-mirror/4 (research data archive)"}
rows, page = [], 1
while True:
    url = f"https://zenodo.org/api/records/7808072/versions?size=25&page={page}"
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120))
    for h in d["hits"]["hits"]:
        m = h["metadata"]
        calls = re.findall(r"<code>(https://paleobiodb\.org/[^<]+)</code>", html.unescape(m.get("description") or ""))
        sizes = {f["key"]: f["size"] for f in h["files"]}
        rows.append({"record": h["id"], "version": m.get("version"),
                     "index": ((m.get("relations") or {}).get("version") or [{}])[0].get("index"),
                     "publication_date": m.get("publication_date"),
                     "occs_call": next((c for c in calls if "/occs/" in c), ""),
                     "taxa_call": next((c for c in calls if "/taxa/" in c), ""),
                     "files": ";".join(sorted(sizes)), "csv_zip_bytes": sizes.get("pbdb_csv.zip", ""),
                     "total_bytes": sum(sizes.values()), "license": (m.get("license") or {}).get("id", "")})
    if len(rows) >= d["hits"]["total"] or not d["hits"]["hits"]:
        break
    page += 1
    time.sleep(1)
rows.sort(key=lambda r: (r["version"], r["record"]))
with open(sys.argv[1], "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(len(rows), "versions")
