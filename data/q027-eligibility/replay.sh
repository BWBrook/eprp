#!/usr/bin/env bash
set -euo pipefail
if [[ $# -ne 1 || -e "$1" ]]; then
  echo 'Usage: replay.sh NEW_ABSOLUTE_OUTPUT_DIRECTORY' >&2
  exit 2
fi
case "$1" in
  /*) ;;
  *) echo 'Output path must be absolute' >&2; exit 2 ;;
esac
task_code_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
task_output=$1
task_image=sha256:b7d5a9f9b91b153a29e38b7c117dcf5d3298adb4618a409d7d779280b16adef8
docker image inspect "$task_image" >/dev/null
python3 -c 'import sys; assert sys.version_info[:3] == (3, 12, 3), "Preparation requires CPython 3.12.3"'
sha256sum -c "$task_code_dir/source-inputs.sha256"
mkdir -p "$task_output"
python3 "$task_code_dir/prepare.py" \
  --source /data/paleodata/register-deposits/benson2025-marine-latitudinal-diversity/raw/v4_361737/marine-lbg-ms-dryad-repo.zip \
  --code '/data/paleodata/register-deposits/close2025-marine-latitudinal-diversity-code/raw/15269137/marine-lbg-ms-code-submission-2025-04-22 2.zip' \
  --public /data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url \
  --output "$task_output/preparation" > "$task_output/preparation.log"
sha256sum "$task_code_dir/prepare.py" "$task_code_dir/run.R" \
  "$task_code_dir/environment/legacy_geometry.R" \
  "$task_output/preparation/original.csv" \
  "$task_output/preparation/dated_public_member.csv" > "$task_output/run-input-freeze.sha256"
docker run --rm --network none --cpus 2 --memory 8g --read-only \
  --user "$(id -u):$(id -g)" --tmpfs /tmp:rw,size=512m \
  -v "$task_code_dir:/code:ro" -v "$task_output:/work" "$task_image" \
  Rscript /code/run.R /work/preparation /code/environment/legacy_geometry.R /work/results \
  > "$task_output/run.log" 2> "$task_output/run.stderr"
