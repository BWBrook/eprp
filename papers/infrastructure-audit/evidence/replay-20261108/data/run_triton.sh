#!/bin/sh
set -eu
repo=$1
mirror=$2
work=$3
script_dir=$(CDPATH='' cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$work/scripts" "$work/inputs" "$work/out"
cp "$script_dir"/*.py "$script_dir"/*.R "$work/scripts/"
cp "$repo/data/q012-event-dictionary/species.tsv" "$repo/data/q012-event-dictionary/lineage_edges.tsv" "$repo/data/q012-exposure-support/name_crosswalk.tsv" "$work/inputs/"
cp "$repo/data/q012-exposure-support/build.R" "$work/scripts/q012_original.R"
cp "$repo/data/triton-event-support/build.R" "$work/scripts/q007_original.R"
Rscript --vanilla "$work/scripts/triton_prepare.R" "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData" "$work"
python3 "$work/scripts/triton_independent.py" "$work" --prepare-only
Rscript --vanilla "$work/scripts/triton_builds.R" "$work" "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData" "$mirror/climate-forcing/phansst/raw/2023-03-09_32cc98ed53/PhanSST_v001.csv"
python3 "$work/scripts/triton_independent.py" "$work"
python3 "$work/scripts/compare_builds.py" "$work/out"
Rscript --vanilla "$work/scripts/raw_mean_check.R" "$work" "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData"
python3 "$work/scripts/input_manifest.py" "$mirror" "$work"
