#!/usr/bin/env bash
# Mirror palaeogeographic plate models and palaeotopography: every model in the GPlates
# Plate Model Manager index (rotations and layers), the PALEOMAP PaleoDEMs, and the
# supplement of Wright et al. 2013 (PBDB's default "gplates" palaeocoordinate model).
# Usage: palaeogeography_snapshot.sh [models] [paleodem] [wright2013] (default: all)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=palaeogeography
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want models; then
  TMP=$(mktemp -d)
  IDX=https://repo.gplates.org/webdav/pmm/config/models.json
  curl -sf -A "eprp-data-mirror/4 (research data archive)" "$IDX" -o "$TMP/models.json" || { echo "index FAILED"; exit 1; }
  python3 _tools/palaeogeography_pmm_specs.py "$TMP/models.json" "$TMP/specs"
  # the index itself first, then every model file, from the same snapshot of the index
  $M url "$D/gplates-models" "models.json::$IDX" --specs-file "$TMP/specs" --pause 0.5 \
    --license "per model: see each model's URL and Version in models.json" || echo "models FAILED"
  rm -rf "$TMP"
fi
# Scotese & Wright 2018 PaleoDEMs (concept 5348491); the notes cite the first version, 5348492
if want paleodem; then $M zenodo 5348492 "$D/paleomap-paleodem" --latest || echo "paleodem FAILED"; fi
if want wright2013; then
  $M url "$D/wright2013-supplement" \
    "bg-10-1529-2013-supplement.zip::https://bg.copernicus.org/articles/10/1529/2013/bg-10-1529-2013-supplement.zip" \
    --license "CC BY 3.0 (Biogeosciences article and supplement)" || echo "wright2013 FAILED"
fi
echo DONE
