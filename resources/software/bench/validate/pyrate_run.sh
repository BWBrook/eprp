#!/usr/bin/env bash
# Tranche-1 E2: run PyRate on every input in <outdir>/inputs, <jobs> at a time, then summarise.
# Usage: pyrate_run.sh <bench_dir> <outdir_rel> <generations> <jobs>
set -u
bench=$1; outrel=$2; gens=$3; jobs=$4
uid=$(id -u); gid=$(id -g)
run_one() {
  name=$(basename "$1" .py)
  mkdir -p "$bench/$outrel/runs/$name"
  docker run --rm --user "$uid:$gid" -v "$bench:/b" eprp-sw/bench-pyrate:t1 \
    python /opt/PyRate/PyRate.py "/b/$outrel/inputs/$name.py" -A 0 -mHPP -n "$gens" -s 2000 -p 100000 \
    -seed "${name##*_}" -wd "/b/$outrel/runs/$name" > "$bench/$outrel/runs/$name/stdout.txt" 2>&1
  echo "$name exit $?"
}
export -f run_one
export bench outrel gens uid gid
ls "$bench/$outrel/inputs"/*.py | xargs -P "$jobs" -I{} bash -c 'run_one {}'
docker run --rm --user "$uid:$gid" -v "$bench:/b" eprp-sw/bench-pyrate:t1 \
  python /b/validate/pyrate_summary.py "/b/$outrel"
