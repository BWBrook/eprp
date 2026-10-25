#!/usr/bin/env bash
# Tranche-4 amendment A6 driver (VALIDATION_T4.md): null control, quorum 0.8, abundance-family robustness.
# Run in /data/paleosoft/bench/t4 inside tmux.
set -euo pipefail
cd "$(dirname "$0")"
U="$(id -u):$(id -g)"
R() { docker run --rm -u "$U" -e HOME=/tmp -e BENCH_CORES=12 -v "$PWD":/work eprp-sw/bench-r4:t4 nice -n 5 "$@"; }
GW() { docker run --rm -u "$U" -e HOME=/tmp -e BENCH_CORES=12 -v "$PWD":/work eprp-sw/bench-r4gw:t4 nice -n 5 "$@"; }
log() { echo "$(date -u +%FT%TZ) $*"; }
mkdir -p data_rob results logs

log "generate E050"; R Rscript validate/t4_generate.R data_dose/E050 E 1 20 sd_late=0.5
declare -A ROB=([gamma10]="fam=1" [gamma4]="fam=1 coll_mean=4" [pareto10]="fam=2" [pareto4]="fam=2 coll_mean=4"
                [loguni10]="fam=3" [loguni4]="fam=3 coll_mean=4" [lnorm4]="coll_mean=4"
                [lnormhet10]="size_sdlog=1" [lnormhet4]="size_sdlog=1 coll_mean=4")
for c in "${!ROB[@]}"; do log "generate $c"; R Rscript validate/t4_generate.R "data_rob/$c" S 1 20 ${ROB[$c]}; done

log "estimate E050"; R Rscript validate/t4_estimate.R data_dose/E050 E_001_020 results/est_E050.csv
for c in "${!ROB[@]}"; do log "estimate $c"; R Rscript validate/t4_estimate.R "data_rob/$c" S_001_020 "results/est_rob_$c.csv"; done
declare -A Q8=([S]="data_v2 S" [C]="data_v2 C" [E]="data_v2 E" [E050]="data_dose/E050 E" [E075]="data_dose/E075 E"
               [E100]="data_dose/E100 E" [E150]="data_dose/E150 E")
for x in "${!Q8[@]}"; do
  set -- ${Q8[$x]}
  log "quorum 0.8 $x"; R Rscript validate/t4_estimate.R "$1" "${2}_001_020" "results/est_q08_$x.csv" 0.8
done

log "gw E050"; GW Rscript validate/t4_gw.R data_dose/E050 E_001_020 results/est_gw_E050.csv ML
for c in "${!ROB[@]}"; do log "gw $c"; GW Rscript validate/t4_gw.R "data_rob/$c" S_001_020 "results/est_gw_rob_$c.csv" ML; done
log "summary"; GW Rscript validate/t4_rob_summary.R results
log "done"
