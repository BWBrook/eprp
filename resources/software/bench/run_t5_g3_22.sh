#!/usr/bin/env bash
set -euo pipefail
source_dir=/data/paleosoft/bench/t5
task_dir=/data/codex/artifacts/eprp/g3-config22-20261028
image=eprp-sw/bench-r5g:t5
mkdir -p "$(dirname "$task_dir")"
mkdir "$task_dir"
mkdir -p "$task_dir/work/configs" "$task_dir/logs"
cp "$source_dir/work/g3/configs/config_auto_22.R" "$task_dir/work/configs/"
ln -s /source/work/g3/landscapes "$task_dir/work/landscapes"
sha256sum "$source_dir/work/g3/configs/config_auto_22.R" \
  "$source_dir/inputs/zenodo5006413/Data/Data/numerical_values/S3 Data/M1_summary.csv" \
  "$source_dir/work/g3/landscapes_rds/scotese_4d/landscapes.rds" \
  "$source_dir/work/g3/landscapes/scotese_4d/landscapes.rds" \
  "$source_dir/validate/t5_gen3sis_hagen.R" > "$task_dir/input-sha256.txt"
docker image inspect "$image" --format '{{.Id}}' > "$task_dir/image-id.txt"
printf '%s\n' "$(date -u +%FT%TZ) starting config 22; 12h wall ceiling" > "$task_dir/status.txt"
set +e
timeout 12h docker run --rm --network none --cpus=2 --memory=12g -u "$(id -u):$(id -g)" \
  -e HOME=/tmp -v "$source_dir:/source:ro" -v "$task_dir/work:/work" -w /work \
  "$image" nice -n 5 Rscript /source/validate/t5_gen3sis_hagen.R run 22 \
  /source/inputs/zenodo5006413/Data/Data /work > "$task_dir/logs/config22.log" 2>&1
exit_status=$?
set -e
printf '%s\n' "$(date -u +%FT%TZ) finished config 22; exit=$exit_status" >> "$task_dir/status.txt"
exit "$exit_status"
