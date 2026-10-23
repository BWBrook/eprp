"""Fetch OBIS Bivalvia (AphiaID 105) occurrences in a coastal strip along eastern Australia (coast - 0.5 to coast + 1.5
degrees longitude, 11-37 S). Public OBIS API v3; no account or contact parameters."""
import json, sys, time, urllib.parse, urllib.request
out = sys.argv[1]
coast = [(-11, 142.8), (-13, 143.6), (-15, 145.3), (-17, 145.9), (-19, 146.8), (-21, 149.0), (-23, 150.8), (-25, 152.8),
         (-27, 153.4), (-29, 153.4), (-31, 153.0), (-33, 151.6), (-35, 150.7), (-37, 150.0)]
west = [(lon - 0.5, lat) for lat, lon in coast]
east = [(lon + 1.5, lat) for lat, lon in reversed(coast)]
ring = west + east + [west[0]]
wkt = "POLYGON((" + ",".join(f"{x} {y}" for x, y in ring) + "))"
fields = "id,scientificName,species,decimalLatitude,decimalLongitude,basisOfRecord,date_year,dataset_id,depth,taxonRank"
after, n, rows = None, 0, []
while True:
    q = dict(taxonid=105, geometry=wkt, size=10000, fields=fields)
    if after:
        q["after"] = after
    url = "https://api.obis.org/v3/occurrence?" + urllib.parse.urlencode(q)
    with urllib.request.urlopen(url, timeout=300) as r:
        d = json.load(r)
    res = d.get("results", [])
    if not res:
        break
    rows += res
    after = res[-1]["id"]
    n += len(res)
    print(n, "of", d.get("total"), flush=True)
    time.sleep(0.5)
json.dump(dict(wkt=wkt, rows=rows), open(out, "w"))
print("done", len(rows))
