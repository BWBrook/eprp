#!/usr/bin/env bash
# Audit the main checkout's data/raw against the catalogue's mirror on deep-server.
# Usage: run_audit.sh RAW WORK    (RAW: the main checkout's data/raw, read only; WORK: a local scratch dir)
# Local steps read RAW; deep-server steps read /data/paleodata and write only under $D.
# Outputs land in WORK and are copied to profile/ next to this script.
set -euo pipefail
RAW=$(cd "$1" && pwd)
WORK=$2
HERE=$(cd "$(dirname "$0")" && pwd)
D=/data/codex/scratch/eprp-paleodata/raw-audit
SNAP=/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url
mkdir -p "$WORK"
rm -rf "$WORK/ids" "$WORK/rbin_work"

# 1. Inventory and zip members of the raw tree (local, read only)
python3 -I "$HERE/raw_inventory.py" "$RAW" "$WORK/raw_inventory.tsv"
mapfile -t zips < <(find "$RAW" -name '*.zip' -not -path '*/.Rproj.user/*' | sort)
python3 -I "$HERE/zip_members.py" "$WORK/main_members.tsv" "${zips[@]}"
python3 -I "$HERE/stated_hashes.py" "$(dirname "$RAW")" "$WORK/raw_inventory.tsv" "$WORK/main_members.tsv" "$WORK/stated_hashes.tsv"

# 2. Members of the mirror zips the raw files correspond to, then the sha256 join (deep-server)
ssh -n deep-server "mkdir -p $D/tools $D/ids"
scp -q "$HERE"/*.py "$HERE"/*.R "deep-server:$D/tools/"
scp -q "$WORK/raw_inventory.tsv" "$WORK/main_members.tsv" "deep-server:$D/"
ssh -n deep-server "cd /data/paleodata && R=register-deposits && python3 -I $D/tools/zip_members.py $D/mirror_members.tsv \
  \$R/benson2025-marine-latitudinal-diversity/raw/v4_361737/marine-lbg-ms-dryad-repo.zip \
  \$R/cantalapiedra2019-phylogenetic-diversity/raw/v1_26492/*.zip \
  \$R/lamyman2026-pforam-phylogeny/raw/21414007/*.zip \
  \$R/close2019-tetrapod-local-richness/raw/v1_23260/*.zip \
  \$R/close2025-marine-latitudinal-diversity-code/raw/15269137/*.zip \
  && python3 -I $D/tools/raw_join.py $D /data/paleodata"
scp -q "deep-server:$D/raw_join.tsv" "$WORK/"

# 3. PBDB intervals file against the catalogue's intervals snapshot
scp -q "$RAW/pbdb/intervals_scale1.json" "deep-server:$D/"
ssh -n deep-server "python3 -I $D/tools/intervals_compare.py $D/intervals_scale1.json \
  /data/paleodata/pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv" | tee "$WORK/intervals_compare.txt"

# 4. PBDB occurrence numbers in text files, zip members and R binaries (local), checked against the public snapshot (deep-server)
python3 -I "$HERE/csv_occurrence_ids.py" "$RAW" "$WORK/ids"
python3 -I "$HERE/rbin_scan.py" "$RAW" "$WORK/ids" "$WORK/rbin_work"
ssh -n deep-server "rm -f $D/ids/*.ids"
scp -q "$WORK"/ids/*.ids "deep-server:$D/ids/"
ssh -n deep-server "cd $D && python3 -I tools/ids_pbdb_check.py $SNAP 12 20261025 ids_pbdb_check.tsv ids/*.ids"
scp -q "deep-server:$D/ids_pbdb_check.tsv" "$WORK/"

# 5. R binaries across the whole mirror, which embedded_pbdb_check.py lists but does not read (deep-server)
ssh -n deep-server "cd $D && rm -rf rbin_mirror rbin_work && python3 -I tools/rbin_scan.py /data/paleodata rbin_mirror rbin_work > rbin_mirror.log 2>&1 \
  && python3 -I tools/ids_pbdb_check.py $SNAP 12 20261025 rbin_mirror_check.tsv rbin_mirror/*.ids && rm -rf rbin_work"
scp -q "deep-server:$D/rbin_mirror/rdata_files.tsv" "$WORK/rbin_mirror_files.tsv"
scp -q "deep-server:$D/rbin_mirror_check.tsv" "$WORK/"

mkdir -p "$HERE/profile"
cp "$WORK/raw_inventory.tsv" "$WORK/raw_join.tsv" "$WORK/stated_hashes.tsv" "$WORK/intervals_compare.txt" \
   "$WORK/ids_pbdb_check.tsv" "$WORK/rbin_mirror_check.tsv" "$HERE/profile/"
cp "$WORK/ids/ids_files.tsv" "$HERE/profile/text_ids_files.tsv"
sed "s|$WORK/rbin_work/[^/]*/||; s|$RAW/||" "$WORK/ids/rdata_objects.tsv" > "$HERE/profile/raw_rdata_objects.tsv"
sed "s|$D/rbin_work/[^/]*/||; s|/data/paleodata/||" "$WORK/rbin_mirror_files.tsv" > "$HERE/profile/rbin_mirror_files.tsv"
