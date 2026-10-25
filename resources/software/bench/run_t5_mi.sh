#!/usr/bin/env bash
# Tranche-5 metabolic-index driver (VALIDATION_T5.md M1-M3). Run in /data/paleosoft/bench/t5 inside tmux.
set -euo pipefail
cd "$(dirname "$0")"
U="$(id -u):$(id -g)"
log() { echo "$(date -u +%FT%TZ) $*"; }
exp=AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN
mkdir -p work results logs
[ -d work/mi ] || cp -a inputs/pohl_mi/cGENIE_based_metabolic_index work/mi
[ -d "work/mi/input/$exp" ] || cp -a "inputs/pohl_mi/deposit/$exp" work/mi/input/
log "doMI.R"
docker run --rm -u "$U" -e HOME=/tmp -v "$PWD/work/mi":/work -w /work eprp-sw/bench-r5:t5 \
  Rscript doMI.R --path "input/" --dir "$exp" --year 7999.5 --neco 10000 --vertical_dimension "upperocean" --mask "shelves" \
  --exclude_poles TRUE --output_netcdf TRUE --set_seed 1993 > logs/mi_doMI.log 2>&1
out=$(ls work/mi/output/*habitat_viability.nc | head -1)
log "checks on $out"
docker run --rm -u "$U" -v "$PWD":/work eprp-sw/bench-py5:t5 python /work/validate/t5_mi_checks.py \
  "/work/$out" "/work/inputs/pohl_mi/deposit/$exp/biogem/fields_biogem_3d.nc" 7999.5 /work/results/t5_mi.json
log "done"
