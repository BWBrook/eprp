#!/usr/bin/env bash
# Tranche-5 C1 alone (VALIDATION_T5.md, amendment A1): make testbiogem in a fresh code tree, keeping its output.
# Usage: ./run_t5_c1.sh <label> <v0.9.35|v0.9.78> <image>
set -euo pipefail
cd "$(dirname "$0")"
label="$1"; ver="$2"; image="$3"
case "$ver" in
  v0.9.35) src=inputs/zenodo7545805/derpycode-cgenie.muffin-f9b7eb6 ;;
  v0.9.78) src=src/cgenie.muffin-v0.9.78 ;;
  *) echo "unknown version $ver" >&2; exit 2 ;;
esac
home="runs/c1-$label/home"
rm -rf "runs/c1-$label"
mkdir -p "$home/cgenie_output" results
cp -a "$src" "$home/cgenie.muffin"
docker run --rm -u "$(id -u):$(id -g)" -e HOME=/home/cg -v "$PWD/$home":/home/cg -w /home/cg/cgenie.muffin/genie-main "$image" \
  bash -c "make testbiogem > testbiogem.make.log 2>&1 || true"
cp "$home/cgenie.muffin/genie-main/testbiogem.out" "results/c1_$label.out"
grep -B1 '\*\*TEST' "results/c1_$label.out" > "results/c1_$label.txt" || echo "no TEST line" > "results/c1_$label.txt"
cat "results/c1_$label.txt"
