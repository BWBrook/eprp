#!/usr/bin/env bash
# Tranche-5 cGENIE driver (VALIDATION_T5.md C1-C3, amendment A1) for one version and toolchain: regression test, then
# the Pohl et al. 2023 540 Ma cold baseline. Run in /data/paleosoft/bench/t5 inside tmux, one session per run.
# Usage: ./run_t5_cgenie.sh <label> <v0.9.35|v0.9.78> <image> [years, default 10000]
set -euo pipefail
cd "$(dirname "$0")"
label="$1"; ver="$2"; image="$3"; years="${4:-10000}"
case "$ver" in
  v0.9.35) src=inputs/zenodo7545805/derpycode-cgenie.muffin-f9b7eb6 ;;
  v0.9.78) src=src/cgenie.muffin-v0.9.78 ;;
  *) echo "unknown version $ver" >&2; exit 2 ;;
esac
home="runs/$label/home"
log() { echo "$(date -u +%FT%TZ) $*"; }
mkdir -p "$home/cgenie_output" logs results
[ -d "$home/cgenie.muffin" ] || cp -a "$src" "$home/cgenie.muffin"
CG() { docker run --rm -u "$(id -u):$(id -g)" -e HOME=/home/cg -v "$PWD/$home":/home/cg -w /home/cg/cgenie.muffin/genie-main "$image" "$@"; }
exp=AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN

log "C1 testbiogem $label"
CG bash -c "make testbiogem > testbiogem.make.log 2>&1; grep -B1 '\*\*TEST' testbiogem.out || echo 'no TEST line'" | tee "results/c1_$label.txt"
log "run $label for $years yr"
CG bash -c "make cleanall > /dev/null 2>&1; nice -n 5 ./runmuffin.sh muffin.AP.540ebP2_.eb_go_gs_ac_bg.PO4.SPIN PUBS/submitted/Pohl_et_al.SciAdv.2023 $exp $years" \
  > "logs/cgenie_run_$label.log" 2>&1 && log "run finished $label" || log "run FAILED $label"
log "done $label"
