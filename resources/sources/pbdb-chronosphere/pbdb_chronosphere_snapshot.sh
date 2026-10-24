#!/usr/bin/env bash
# Mirror chronosphere's dated PBDB downloads (one Zenodo concept, 10.5281/zenodo.7808071, with
# about 1,180 versions): the download metadata of every version, and the occurrence table (zipped
# CSV) of a sample across the years.
# Usage: pbdb_chronosphere_snapshot.sh [metadata] [tables] (default: both)
#   metadata  each version's metadata file (PBDB's datainfo header: the API call, access time,
#             records found and returned), every version
#   tables    pbdb_csv.zip and the metadata of the sampled versions below: the first of each year,
#             each change of API call, the one archive much smaller than its neighbours, the newest,
#             and the two versions either side of each of PBDB's three interval re-datings
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=pbdb-chronosphere
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want metadata; then
  $M zenodo 7808072 "$D/metadata" --files 'metadata*.txt' --jobs 2 || echo "metadata FAILED"
fi
if want tables; then
  $M zenodo 7808072 "$D/tables" --files pbdb_csv.zip 'metadata*.txt' --jobs 8 --only \
    20191122_7808072 20200217_7845041 20200909_7845143 20210101_7845868 20210518_7846821 \
    20220101_7850252 20230104_7877929 20231228_10437013 20240107_10466717 20250102_14588615 \
    20260227_18803370 20261018_23468334 \
    20240331_10931491 20240401_10931518 20250331_15111554 20250410_15187705 \
    20260802_21869245 20260809_21869343 || echo "tables FAILED"
fi
echo DONE
