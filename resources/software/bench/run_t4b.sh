#!/usr/bin/env bash
# Tranche-4 per-dataset DeepDive arm (amendment A4 in VALIDATION_T4.md). Run in /data/paleosoft/bench/t4 inside tmux;
# it waits for run_t4.sh to finish first.
set -euo pipefail
cd "$(dirname "$0")"
U="$(id -u):$(id -g)"
R() { docker run --rm -u "$U" -e HOME=/tmp -v "$PWD":/work eprp-sw/bench-r4:t4 "$@"; }
log() { echo "$(date -u +%FT%TZ) $*"; }
until grep -q " done$" logs/run.log; do sleep 120; done
for s in S E M; do R Rscript validate/t4_deepdive_own.R "deepdive/$s" "$s" "deepdive_own/$s" 2 3 4; done
log "per-dataset configs written"
train() {
  docker run --rm -u "$U" -e HOME=/tmp -v "$PWD":/work eprp-sw/bench-py4:t4 bash -c \
    "cd /work/$1 && nice -n 10 python /opt/deepdive/run_dd_config.py config.ini -wd /work/$1 -cpu 16 && cd /work && python validate/t4_deepdive_predict.py $1 $1/prediction.csv" \
    > "$1/train.log" 2>&1 && log "trained $1" || log "FAILED $1"
}
export -f train log
export U
ls -d deepdive_own/*/rep_* | xargs -P 3 -I{} bash -c 'train {}'
for s in S E M; do
  awk 'FNR > 1 || NR == 1' deepdive_own/"$s"/rep_*/prediction.csv > "results/deepdive_own_$s.csv"
done
R Rscript validate/t4_summary.R data_check results
R Rscript validate/t4_deepdive_summary.R data_check results
log "done"
