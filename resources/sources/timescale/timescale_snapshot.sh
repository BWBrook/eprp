#!/usr/bin/env bash
# Mirror the geological time scale sources: the ICS chart as RDF for every
# release from 2004 to 2020 (CGI-IUGS, CC0; numeric boundary ages and
# uncertainties), the ICS chart PDFs for 2020/03 (GTS2020) and the current
# 2024/12, Macrostrat's interval definitions, and the late Cambrian revision of
# Farrell et al. (2025). PBDB's interval table is mirrored under pbdb/intervals.
# Usage: timescale_snapshot.sh [ROUTE ...]   ROUTE: isc ics macrostrat farrell (default: all)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=timescale
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want isc; then $M github CGI-IUGS/timescale-data "$D/isc-rdf" --latest || echo "isc FAILED"; fi
if want ics; then
  ICS="https://stratigraphy.org/ICSchart"
  $M url "$D/ics-chart" "ChronostratChart2024-12.pdf::$ICS/ChronostratChart2024-12.pdf" \
    "ChronostratChart2020-03.pdf::$ICS/ChronostratChart2020-03.pdf" --pause 2 \
    --license "ICS chart; terms as printed on the chart (International Commission on Stratigraphy)" || echo "ics FAILED"
fi
if want macrostrat; then
  MS="https://macrostrat.org/api/v2/defs"
  $M url "$D/macrostrat" "intervals_all.json::$MS/intervals?all" "timescales_all.json::$MS/timescales?all" --pause 2 \
    --license "CC BY 4.0 (Macrostrat API)" || echo "macrostrat FAILED"
fi
if want farrell; then $M figshare article/28207634 "$D/farrell2025-late-cambrian" --latest || echo "farrell FAILED"; fi
echo DONE
