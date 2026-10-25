#!/usr/bin/env bash
# Mirror Macrostrat (API v2) as dated snapshots.
# Usage: macrostrat_snapshot.sh [api] [agemodels] (default: both)
#   api        columns, units, sections, PBDB collection links and measurements for every project and
#              column status, every definition table, and the per-project statistics
#              (macrostrat_specs.py builds the list). Geologic maps are not mirrored. The fossils route
#              ignores status_code and leaves out obsolete columns.
#   agemodels  the age model (unit boundaries and their status) of every column in the newest api
#              snapshot, one request per column (age_model_specs.py), into macrostrat-age-models
set -uo pipefail
cd /data/paleodata
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }
LIC="CC BY 4.0 (Macrostrat API meta: 'All data are licensed under Creative Commons BY 4.0 International')"
TMP=$(mktemp -d)
if want api; then
  if python3 _tools/macrostrat_macrostrat_specs.py "$TMP/specs"; then
    python3 _tools/data_mirror.py url macrostrat --specs-file "$TMP/specs" --pause 1 --license "$LIC" || echo "api FAILED"
  else
    echo "project list FAILED"
  fi
fi
if want agemodels; then
  SNAP=$(ls -d macrostrat/raw/*_url | tail -1)
  python3 _tools/macrostrat_age_model_specs.py "$SNAP" "$TMP/agespecs" \
    && python3 _tools/data_mirror.py url macrostrat/age-models --specs-file "$TMP/agespecs" --pause 1 --license "$LIC" \
    || echo "agemodels FAILED"
fi
rm -rf "$TMP"
echo DONE
