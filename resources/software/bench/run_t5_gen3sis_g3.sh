#!/usr/bin/env bash
# Tranche-5 G3 driver (VALIDATION_T5.md A3): compile Hagen et al.'s two 4-degree landscapes, rerun ten deposited M1 configs.
# Run in /data/paleosoft/bench/t5 inside tmux.
set -euo pipefail
cd "$(dirname "$0")"
D=inputs/zenodo5006413/Data/Data
W=work/g3
log() { echo "$(date -u +%FT%TZ) $*"; }
G() { docker run --rm -u "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD":/work -w /work eprp-sw/bench-r5g:t5 nice -n 5 "$@"; }
mkdir -p "$W/configs" "$W/landscapes_rds" "$W/out" results logs
unzip -q -o "$D/config.zip" 'config/configs_m1/*' -d "$W/unz" && cp "$W"/unz/config/configs_m1/*.R "$W/configs/"
for ls in straume_4d scotese_4d; do
  sub=$([ "$ls" = straume_4d ] && echo L2 || echo L1)
  mkdir -p "$W/landscapes_rds/$ls" && unzip -q -o -j "$D/landscapes.zip" "landscapes/$sub/$ls/landscapes.rds" -d "$W/landscapes_rds/$ls"
done
G Rscript validate/t5_gen3sis_hagen.R select "$D" | tee "$W/selected.txt"
for ls in straume_4d scotese_4d; do
  ( log "compile $ls"; G Rscript validate/t5_gen3sis_hagen.R compile "$ls" "$D" "$W" > "logs/g3_compile_$ls.log" 2>&1 && log "compiled $ls" ) &
done
wait
cut -d' ' -f1 "$W/selected.txt" | xargs -P 10 -I{} bash -c "docker run --rm -u $(id -u):$(id -g) -e HOME=/tmp -v $PWD:/work -w /work eprp-sw/bench-r5g:t5 nice -n 5 Rscript validate/t5_gen3sis_hagen.R run {} $D $W > logs/g3_run_{}.log 2>&1 && echo ran {} || echo FAILED {}"
awk 'FNR > 1 || NR == 1' "$W"/g3_m1_*.csv > results/t5_gen3sis_g3.csv
log "done"
