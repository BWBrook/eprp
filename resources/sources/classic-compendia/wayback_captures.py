"""List the Wayback Machine captures of Bristol's original FR2 pages and files
(palaeo.gly.bris.ac.uk/frwhole, 1997-2006): the earliest capture of every
distinct payload (CDX digest) of every URL that returned HTTP 200.

Usage: python3 wayback_captures.py OUT_TSV
"""

import json
import sys
import urllib.request
from collections import defaultdict

CDX = ("https://web.archive.org/cdx/search/cdx?url=palaeo.gly.bris.ac.uk/frwhole/*&output=json"
       "&fl=timestamp,original,mimetype,statuscode,digest&filter=statuscode:200&limit=5000")

req = urllib.request.Request(CDX, headers={"User-Agent": "eprp-data-mirror/4 (research data archive)"})
rows = json.load(urllib.request.urlopen(req, timeout=300))[1:]
first = defaultdict(dict)
for ts, orig, mime, status, digest in sorted(rows):
    name = orig.split("/frwhole/", 1)[1]
    first[name].setdefault(digest, (ts, orig, mime))
with open(sys.argv[1], "w") as out:
    out.write("timestamp\tname\tmimetype\tdigest\tlocal_name\toriginal\n")
    for name in sorted(first):
        for digest, (ts, orig, mime) in sorted(first[name].items(), key=lambda kv: kv[1]):
            local = f"{ts}__{name}"
            if mime == "text/html" and not name.endswith(".html"):
                local += ".html"
            out.write(f"{ts}\t{name}\t{mime}\t{digest}\t{local}\t{orig}\n")
print(len(rows), "captures;", sum(len(v) for v in first.values()), "distinct payloads;", len(first), "URLs")
