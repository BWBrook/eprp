#!/usr/bin/env bash
# Mirror GloNAF (Global Naturalized Alien Flora): the newest Zenodo version (concept 13235356),
# every version indexed.
# Usage: glonaf_snapshot.sh
set -uo pipefail
cd /data/paleodata
python3 _tools/data_mirror.py zenodo 17105725 glonaf --latest || echo "glonaf FAILED"
echo DONE
