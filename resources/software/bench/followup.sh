#!/usr/bin/env bash
# Follow-up after the independent review (VALIDATION.md A2): G3b, timings,
# corrected ESS summary, PyRate interval and truncated-MLE diagnostics, divDyn replicate SEs.
set -u
B=/data/paleosoft/bench
cd "$B"
export BENCH_CORES=${BENCH_CORES:-12}
R="docker run --rm --user $(id -u):$(id -g) -e BENCH_CORES -v $B:/b -w /b eprp-sw/bench-r:t1"
PY="docker run --rm --user $(id -u):$(id -g) -v $B:/b -w /b eprp-sw/bench-pyrate:t1"
log() { echo "$(date -u +%FT%TZ) $*" | tee -a logs/followup.log; }
log "G3b and timings"; $R Rscript validate/g3b_timing.R /b/results/generators > logs/g3b.txt 2>&1; log "exit $?"
log "E2 summary (ESS pairing fixed)"; $PY python validate/pyrate_summary.py /b/results/e2 > logs/e2-summary.txt 2>&1; log "exit $?"
log "E2 durations and intervals"; $PY python validate/pyrate_durations.py /b/results/e2 > logs/e2-durations.txt 2>&1; log "exit $?"
log "E1 replicate SEs"; $PY python validate/divdyn_se.py /b/results/e1 > logs/e1-se.txt 2>&1; log "exit $?"
log "done"
