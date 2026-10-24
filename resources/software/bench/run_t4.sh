#!/usr/bin/env bash
# Tranche-4 driver (declared in VALIDATION_T4.md). On deep-server: copy validate/ and this script to
# /data/paleosoft/bench/t4, then run it there inside tmux.
set -euo pipefail
cd "$(dirname "$0")"
U="$(id -u):$(id -g)"
R() { docker run --rm -u "$U" -e HOME=/tmp -e BENCH_CORES=10 -v "$PWD":/work eprp-sw/bench-r4:t4 "$@"; }
PY() { docker run --rm -u "$U" -e HOME=/tmp -v "$PWD":/work eprp-sw/bench-py4:t4 "$@"; }
log() { echo "$(date -u +%FT%TZ) $*"; }
mkdir -p data results logs deepdive

for s in S E M; do
  log "generate $s"; R Rscript validate/t4_generate.R data "$s" 1 20
  log "deepdive inputs $s"; R Rscript validate/t4_deepdive_prep.R data "${s}_001_020" "$s" "deepdive/$s"
done
for s in S E M; do
  ( PY bash -c "cd /work/deepdive/$s && nice -n 10 python /opt/deepdive/run_dd_config.py config.ini -wd /work/deepdive/$s -cpu 16" \
      > "logs/dd_train_$s.log" 2>&1 && log "deepdive trained $s" || log "deepdive training FAILED $s" ) &
done
for s in S E M; do log "estimate $s"; R Rscript validate/t4_estimate.R data "${s}_001_020" "results/est_$s.csv"; done
wait
for s in S E M; do
  log "deepdive predict $s"; PY python validate/t4_deepdive_predict.py "deepdive/$s" "results/deepdive_$s.csv"
  cat deepdive/"$s"/dd_"$s"_models/*/testset_pred_*MSA.txt > "results/deepdive_testset_$s.txt"
done
log "summary"; R Rscript validate/t4_summary.R data results
log "done"
