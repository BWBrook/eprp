# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""List the PBDB snapshots in chronosphere's public dataset registry.

Usage: uv run resources/software/chronosphere/pbdb_versions.py
Writes pbdb_versions.tsv beside this script: one row per PBDB product version,
with the registry file's sha256 and retrieval time in the header comment.
"""

import csv
import datetime as dt
import hashlib
import io
import pathlib
import urllib.request

REGISTRY = "https://github.com/chronosphere-info/chrono_arch_2/raw/main/users/public/master.csv"
OUT = pathlib.Path(__file__).with_name("pbdb_versions.tsv")
FIELDS = ["ser", "seriesName", "ver", "productDate", "licenseName", "dataDOI", "datafileName", "dateAdded"]

raw = urllib.request.urlopen(urllib.request.Request(REGISTRY, headers={"User-Agent": "eprp-software/1"}), timeout=120).read()
rows = [r for r in csv.DictReader(io.StringIO(raw.decode("utf-8"))) if r["src"].lower() == "pbdb"]
rows.sort(key=lambda r: (r["ser"], r["ver"]))
stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
with OUT.open("w", newline="", encoding="utf-8") as f:
    f.write(f"# {REGISTRY}\n# sha256 {hashlib.sha256(raw).hexdigest()}  retrieved {stamp}\n")
    w = csv.DictWriter(f, FIELDS, delimiter="\t", extrasaction="ignore", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)

series = {}
for r in rows:
    series.setdefault(r["ser"], []).append(r["ver"])
for ser, vers in series.items():
    print(f"{ser}: {len(vers)} versions, {vers[0]} to {vers[-1]}")
