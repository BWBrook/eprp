#!/usr/bin/env bash
# Mirror Macrostrat (API v2) as a dated snapshot: columns, units, sections, PBDB collection links
# and measurements for every project and column status, every definition table, and the
# per-project statistics (macrostrat_specs.py builds the list). Geologic maps are not mirrored.
# Usage: macrostrat_snapshot.sh
set -uo pipefail
cd /data/paleodata
TMP=$(mktemp -d)
if python3 _tools/macrostrat_macrostrat_specs.py "$TMP/specs"; then
  python3 _tools/data_mirror.py url macrostrat --specs-file "$TMP/specs" --pause 1 \
    --license "CC BY 4.0 (Macrostrat API meta: 'All data are licensed under Creative Commons BY 4.0 International')" \
    || echo "macrostrat FAILED"
else
  echo "project list FAILED"
fi
rm -rf "$TMP"
echo DONE
