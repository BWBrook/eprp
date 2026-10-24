#!/usr/bin/env bash
# Tranche-3 driver on deep-server, inside tmux.
set -u
B=/data/paleosoft/bench
cd "$B"
PD=/data/paleodata
PUB=/pd/pbdb/global/raw/2026-10-23T0329Z_url
R="docker run --rm --user $(id -u):$(id -g) -e HOME=/b/t3 -v $B:/b -v $PD:/pd:ro -w /b eprp-sw/bench-r3:t3"
PY="docker run --rm --user $(id -u):$(id -g) -v $B:/b -v $PD:/pd:ro -w /b eprp-sw/bench-py3:t3"
mkdir -p results/t3 logs t3
log() { echo "$(date -u +%FT%TZ) $*" | tee -a logs/run_t3.log; }
log "start; images r3 $(docker image inspect --format '{{.Id}}' eprp-sw/bench-r3:t3) py3 $(docker image inspect --format '{{.Id}}' eprp-sw/bench-py3:t3)"
log "V1-V5, F1-F2"; $R Rscript validate/t3_palaeoverse.R /b/results/t3 /pd/timescale/derived/2026-10-23T0844Z/ics2024_pbdb_bases.tsv /pd/timescale/derived/2026-10-23T0844Z/isc_boundaries_by_version.tsv 200 > logs/t3_palaeoverse.txt 2>&1; log "exit $?"
log "V6 palaeorotate"; $R Rscript validate/t3_rotate.R /b/results/t3 $PUB 300 > logs/t3_rotate_r.txt 2>&1; log "exit $?"
log "V6 pygplates"; $PY python validate/t3_rotate.py /pd/palaeogeography/gplates-models/raw/2026-10-24T0301Z_url /b/results/t3/v6_points.tsv /b/results/t3/v6_pygplates.tsv > logs/t3_rotate_py.txt 2>&1; log "exit $?"
log "V6 summary"; $PY python validate/t3_rotate_summary.py /b/results/t3 > logs/t3_rotate_summary.txt 2>&1; log "exit $?"
log "C1 chronosphere"; $R Rscript validate/t3_chronosphere.R /b/results/t3 /b/t3/chronosphere $PUB 150 50 > logs/t3_chronosphere.txt 2>&1; log "exit $?"
log "done"
