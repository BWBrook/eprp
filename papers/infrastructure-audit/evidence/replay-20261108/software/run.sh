#!/usr/bin/env bash
set -euo pipefail
repo=$(realpath "$1")
raw=$(realpath "$2")
out=$(realpath "$3")
source_dir=papers/infrastructure-audit/evidence/replay-20261108/software
r_image=sha256:44432c896c3622e92c68f11716d639745b0fa2b4d6c47124538461389f6daab6
py_image=sha256:8c333ab2e7a7d6f54f42730c047227acd4c70688c702ca288a873c88ad975bac
docker image inspect "$r_image" "$py_image" >/dev/null
docker run --rm --user "$(id -u):$(id -g)" -v "$repo:/repo:ro" -v "$out:/replay" -w /replay \
  "$r_image" Rscript "/repo/$source_dir/replay_packages.R" /replay >"$out/package-run.log" 2>&1
docker run --rm --user "$(id -u):$(id -g)" -v "$repo:/repo:ro" -v "$raw:/raw:ro" -v "$out:/replay" -w /replay \
  "$py_image" python "/repo/$source_dir/replay_plate.py" /repo /raw /replay >"$out/plate-run.log" 2>&1
python3 "$repo/$source_dir/receipt.py" "$repo" "$out"
