#!/usr/bin/env bash
# Tranche-4 amendment A5 driver (VALIDATION_T4.md): collection-size scenario, evenness doses, geometric Weibull arm.
# Run in /data/paleosoft/bench/t4 inside tmux.
set -euo pipefail
cd "$(dirname "$0")"
U="$(id -u):$(id -g)"
R() { docker run --rm -u "$U" -e HOME=/tmp -e BENCH_CORES=12 -v "$PWD":/work eprp-sw/bench-r4:t4 nice -n 5 "$@"; }
GW() { docker run --rm -u "$U" -e HOME=/tmp -e BENCH_CORES=12 -v "$PWD":/work eprp-sw/bench-r4gw:t4 nice -n 5 "$@"; }
log() { echo "$(date -u +%FT%TZ) $*"; }
mkdir -p data_v2 data_dose results logs

for s in S E M C; do log "generate $s"; R Rscript validate/t4_generate.R data_v2 "$s" 1 20; done
for d in 075:0.75 100:1 150:1.5; do log "generate E${d%%:*}"; R Rscript validate/t4_generate.R "data_dose/E${d%%:*}" E 1 20 "sd_late=${d##*:}"; done
python3 validate/t4_identity.py data data_v2 S_001_020 E_001_020 M_001_020
log "identity check passed"

log "estimate C and doses"
R Rscript validate/t4_estimate.R data_v2 C_001_020 results/est_C.csv
for d in 075 100 150; do R Rscript validate/t4_estimate.R "data_dose/E$d" E_001_020 "results/est_E$d.csv"; done

log "K4"; GW Rscript validate/t4_gw_k4.R results
for s in S E M; do log "gw ML,LD $s"; GW Rscript validate/t4_gw.R data_v2 "${s}_001_020" "results/est_gw_$s.csv" ML,LD; done
log "gw ML C"; GW Rscript validate/t4_gw.R data_v2 C_001_020 results/est_gw_C.csv ML
for d in 075 100 150; do log "gw ML E$d"; GW Rscript validate/t4_gw.R "data_dose/E$d" E_001_020 "results/est_gw_E$d.csv" ML; done
log "summary"; GW Rscript validate/t4_ext_summary.R results
log "done"
