#!/usr/bin/env bash
# Mirror the Alien Species First Records Database (Seebens et al.): the newest version and v3.1,
# the open version SInAS 3.x harmonises; every version indexed (1.1 to 2.0 are restricted on Zenodo).
# Usage: first_records_snapshot.sh
set -uo pipefail
cd /data/paleodata
python3 _tools/data_mirror.py zenodo 18759840 alien-first-records --latest --only 3.1_10039630 || echo "first records FAILED"
echo DONE
