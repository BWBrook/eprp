#!/bin/bash
# Package one scenario's evidence on kunanyi for transfer (run by fetch.sh over SSH, from the pilot directory).
# Includes whatever exists, so an early build failure with no run directory is still retrievable.
set -u
SCEN="${1:?scenario}"
QSTAT=/opt/pbs/bin/qstat
: > "accounting-$SCEN.txt"
if [ -f submitted.txt ] && [ -x "$QSTAT" ]; then
  for j in $(tr ' ' '\n' < submitted.txt | cut -d= -f2); do "$QSTAT" -xf "$j" >> "accounting-$SCEN.txt" 2>&1; done
fi
paths=()
for p in submitted.txt "accounting-$SCEN.txt" manifest.sha256 build "runs/$SCEN" q012_*.o*; do
  [ -e "$p" ] && paths+=("$p")
done
tar czf "fetch-$SCEN.tar.gz" "${paths[@]}" || exit 1
echo "PACKED ${paths[*]}"
sha256sum "fetch-$SCEN.tar.gz"
