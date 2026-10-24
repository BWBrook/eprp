#!/usr/bin/env bash
# Mirror BioTIME: the newest 2.0 release on Zenodo, the St Andrews CSV export of the same release,
# and the version index of BioTIME 1.
# Usage: biotime_snapshot.sh [zenodo] [csv] [v1index] (default: all)
#   zenodo   BioTIME 2.0 (concept 10932823; the newest version, 15222193 when written), all files but
#            the 1.2 GB MySQL dump, which holds the same records as the RDS and the CSV export
#   csv      the raw-data CSV zip offered by the St Andrews site (not on Zenodo)
#   v1index  BioTIME 1 (concept 1095627): versions indexed, files on demand
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=biotime
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want zenodo; then $M zenodo 15222193 "$D/zenodo" --latest --files '*.rds' '*.csv*' || echo "zenodo FAILED"; fi
if want csv; then
  $M url "$D/standrews-csv" \
    "biotime_v2_rawdata_2025.zip::https://biotime.st-andrews.ac.uk/downloads/biotime_v2_rawdata_2025.zip" \
    --license "CC BY 4.0 for the database; each study keeps its own licence (metadata PERMISSIONS)" || echo "csv FAILED"
fi
if want v1index; then $M zenodo 5026943 "$D/v1" --index-only || echo "v1 index FAILED"; fi
echo DONE
