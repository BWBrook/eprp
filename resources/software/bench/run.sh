#!/usr/bin/env bash
# Tranche-1 driver: run every declared test on deep-server, in order, inside tmux.
# Usage (on deep-server): tmux new-session -d -s eprp-t1 'bash /data/paleosoft/bench/run.sh'
set -u
B=/data/paleosoft/bench
cd "$B"
export BENCH_CORES=${BENCH_CORES:-12}
R="docker run --rm --user $(id -u):$(id -g) -e BENCH_CORES -v $B:/b -w /b eprp-sw/bench-r:t1"
PY="docker run --rm --user $(id -u):$(id -g) -v $B:/b -w /b eprp-sw/bench-pyrate:t1"
mkdir -p results logs
log() { echo "$(date -u +%FT%TZ) $*" | tee -a logs/run.log; }

log "start; images: $(cat logs/image-ids.txt | tr '\n' ' ')"
log "E3a skyfbdr deposited coverage"
$PY python validate/skyfbdr_coverage.py /b/skyfbdr_simstudy /b/results/e3a > logs/e3a.txt 2>&1; log "E3a exit $?"
log "G1-G5 generators"
$R Rscript validate/generators.R /b/results/generators > logs/generators.txt 2>&1; log "generators exit $?"
log "E1 divDyn"
$R Rscript validate/divdyn.R /b/results/e1 200 > logs/e1.txt 2>&1; log "E1 exit $?"
log "E2 PyRate simulation"
$R Rscript validate/pyrate_sim.R /b/results/e2 high 100 > logs/e2-sim-high.txt 2>&1; log "E2 sim high exit $?"
$R Rscript validate/pyrate_sim.R /b/results/e2 low 50 > logs/e2-sim-low.txt 2>&1; log "E2 sim low exit $?"
log "E2 PyRate runs"
bash validate/pyrate_run.sh "$B" results/e2 2000001 "$BENCH_CORES" > logs/e2-runs.txt 2>&1; log "E2 exit $?"
log "done"
