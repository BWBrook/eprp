#!/usr/bin/env bash
# Tranche-2 driver on deep-server, inside tmux: stratigraphic tools, then the extinction benchmark.
set -u
B=/data/paleosoft/bench
cd "$B"
export BENCH_CORES=${BENCH_CORES:-12}
R="docker run --rm --user $(id -u):$(id -g) -e BENCH_CORES -v $B:/b -w /b eprp-sw/bench-r2:t2"
mkdir -p results/t2 logs
log() { echo "$(date -u +%FT%TZ) $*" | tee -a logs/run_t2.log; }
log "start; image $(docker image inspect --format '{{.Id}}' eprp-sw/bench-r2:t2)"
log "S1-S5, P1"; $R Rscript validate/t2_strat.R /b/results/t2 200 > logs/t2_strat.txt 2>&1; log "exit $?"
log "E4-E6 benchmark"; $R Rscript validate/t2_extinction.R /b/results/t2 2000 1000 > logs/t2_extinction.txt 2>&1; log "exit $?"
log "summary"; $R Rscript validate/t2_summary.R /b/results/t2 > logs/t2_summary.txt 2>&1; log "exit $?"
log "done"
