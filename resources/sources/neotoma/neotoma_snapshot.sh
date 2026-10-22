#!/usr/bin/env bash
# Snapshot every Indo-Pacific Pollen Database dataset in Neotoma, plus any other
# dataset in Australia (gpid 303), Papua New Guinea (3361) or Indonesian New
# Guinea (2026), as dataset listings and full downloads in batches of ten.
# Run on deep-server from anywhere; writes /data/paleodata/neotoma/ippd-sahul.
set -euo pipefail
A="https://api.neotomadb.org/v2.0/data"
W=/data/codex/scratch/eprp-paleodata/neotoma_ids
mkdir -p "$W"
LISTS=("datasets_ippd.json::$A/datasets/db?database=Indo-Pacific%20Pollen%20Database&limit=10000"
       "datasets_gpid303.json::$A/datasets?gpid=303&limit=5000&offset=0"
       "datasets_gpid3361.json::$A/datasets?gpid=3361&limit=5000&offset=0"
       "datasets_gpid2026.json::$A/datasets?gpid=2026&limit=5000&offset=0")
python3 - "$W" "${LISTS[@]}" <<'PY'
import json, sys, urllib.request
w, specs = sys.argv[1], sys.argv[2:]
ids = set()
for spec in specs:
    url = spec.split("::", 1)[1]
    req = urllib.request.Request(url, headers={"User-Agent": "eprp-data-mirror/4 (research data archive)"})
    with urllib.request.urlopen(req, timeout=300) as r:
        d = json.load(r)
    assert d["status"] == "success", url
    ids |= {ds["datasetid"] for rec in d["data"] for ds in rec["site"]["datasets"]}
ids = sorted(ids)
with open(f"{w}/specs.txt", "w") as f:
    for s in specs:
        f.write(s + "\n")
    for i in range(0, len(ids), 10):
        batch = ids[i:i + 10]
        f.write(f"downloads_{i // 10 + 1:03d}.json::https://api.neotomadb.org/v2.0/data/downloads/{','.join(map(str, batch))}\n")
print(len(ids), "datasets")
PY
mapfile -t SPECS < "$W/specs.txt"
cd /data/paleodata
python3 _tools/data_mirror.py url neotoma/ippd-sahul \
  --license "CC BY 4.0 (Neotoma data use and embargo policy v.2025)" "${SPECS[@]}"
echo DONE
