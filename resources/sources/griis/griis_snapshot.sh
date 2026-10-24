#!/usr/bin/env bash
# Mirror GRIIS: the Country Compendium on Zenodo, and a dated snapshot of every GRIIS checklist
# on GBIF as its Darwin Core Archive.
# Usage: griis_snapshot.sh [compendium] [checklists] (default: both)
#   compendium  GRIIS Country Compendium V1.0 (Zenodo 6348164), every version indexed
#   checklists  the ISSG publisher's datasets on GBIF (griis_specs.py), each archive from its IPT;
#               the dataset index is kept beside each snapshot (datasets-<snapshot>.tsv)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=griis
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want compendium; then $M zenodo 6348164 "$D/compendium" --latest || echo "compendium FAILED"; fi
if want checklists; then
  TMP=$(mktemp -d)
  if python3 _tools/griis_griis_specs.py "$TMP/specs" "$TMP/datasets.tsv"; then
    $M url "$D/checklists" --specs-file "$TMP/specs" --pause 1 \
      --license "per checklist: see datasets-<snapshot>.tsv (GBIF: CC BY 4.0 for most, CC0 for some)" || echo "checklists FAILED"
    v=$(ls -d $D/checklists/raw/*_url | tail -1)
    cp "$TMP/datasets.tsv" "$D/checklists/datasets-$(basename "$v").tsv"
  else
    echo "GBIF listing FAILED"
  fi
  rm -rf "$TMP"
fi
echo DONE
