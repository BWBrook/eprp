"""List the GRIIS checklists on GBIF and write a file list for `data_mirror.py url`.

Usage: python3 griis_specs.py SPECS_OUT INDEX_TSV

Every dataset published on GBIF by the Invasive Species Specialist Group
(ISSG, the publisher of all GRIIS checklists) is listed through the GBIF
registry API. For each one with a Darwin Core Archive endpoint, SPECS_OUT gets
a NAME::URL line (NAME is a slug of the title plus the first eight
characters of the GBIF dataset key), and INDEX_TSV gets the dataset key,
title, DOI, dates, licence, the version cited by GBIF, the archive URL and
the file name. No contact fields are written. Standard library only; no
contact details are sent.
"""

import csv
import json
import re
import sys
import time
import urllib.request

ISSG = "cdef28b1-db4e-4c58-aa71-3c5238c2d0b5"
UA = {"User-Agent": "eprp-data-mirror/4 (research data archive)"}
specs_out, index_tsv = sys.argv[1:3]
datasets, offset = [], 0
while True:
    url = f"https://api.gbif.org/v1/organization/{ISSG}/publishedDataset?limit=200&offset={offset}"
    page = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120))
    datasets += page["results"]
    if page.get("endOfRecords", True):
        break
    offset += 200
    time.sleep(1)
rows = []
for d in datasets:
    dwca = [e["url"] for e in d.get("endpoints", []) if e["type"] == "DWC_ARCHIVE"]
    cite = (d.get("citation") or {}).get("text", "")
    version = re.search(r"\bv(\d+(?:\.\d+)*)\.", cite)
    slug = re.sub(r"[^A-Za-z0-9]+", "-", re.sub(r"^Global Register of Introduced and Invasive Species\s*-\s*", "", d["title"])).strip("-")
    rows.append({"key": d["key"], "title": d["title"], "doi": d.get("doi", ""), "created": d["created"][:10],
                 "modified": d["modified"][:10], "license": d.get("license", ""),
                 "version_cited": version.group(1) if version else "", "dwca_url": dwca[0] if dwca else "",
                 "file": f"{slug[:60]}__{d['key'][:8]}.zip" if dwca else ""})
rows.sort(key=lambda r: r["title"])
names = [r["file"] for r in rows if r["file"]]
if len(set(names)) != len(names):
    raise SystemExit("file names repeat")
with open(specs_out, "w", encoding="utf-8") as f:
    f.writelines(f"{r['file']}::{r['dwca_url']}\n" for r in rows if r["file"])
with open(index_tsv, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(json.dumps({"datasets": len(rows), "with archive": len(names)}))
