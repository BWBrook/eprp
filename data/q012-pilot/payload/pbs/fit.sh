#!/bin/bash
# Q-012 pilot runner: one fit is four single-threaded CmdStan chains.
# It verifies the payload and binary hashes, never retries, keeps every attempt,
# and writes a receipt on completion, failure, timeout or signal.
# Exit codes: 0 complete or skipped, 1 a chain failed, 2 refused, 3 signal, 4 timeout.
set -u
ROOT="${PILOT_ROOT:-${PBS_O_WORKDIR:-$(cd "$(dirname "$0")/.." && pwd)}}"
cd "$ROOT" || exit 2
. ./run.env
if [ -n "${PBS_ARRAY_INDEX:-}" ]; then
  SCEN="$(awk -F'\t' -v i="$PBS_ARRAY_INDEX" '$2 == "panel" { n++; if (n == i) print $1 }' scenarios.tsv)"
fi
: "${SCEN:?SCEN is not set}"
RUN="runs/$SCEN"
mkdir -p "$RUN"
log() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$*" >> "$RUN/runner.log"; }

if ! sha256sum -c --strict --quiet manifest.sha256 > "$RUN/manifest_check.txt" 2>&1; then
  log "REFUSED: payload manifest mismatch"
  echo "REFUSED: payload manifest mismatch; see $RUN/manifest_check.txt"
  exit 2
fi
MANIFEST_SHA="$(sha256sum manifest.sha256 | cut -d' ' -f1)"
BUILD_STATUS="$(awk -F= '$1 == "status" { print $2 }' build/receipt.txt 2>/dev/null)"
BIN_EXPECT="$(awk -F= '$1 == "binary_sha256" { print $2 }' build/receipt.txt 2>/dev/null)"
BIN_SHA="$(sha256sum "$MODEL_BIN" 2>/dev/null | cut -d' ' -f1)"
if [ "$BUILD_STATUS" != "ok" ] || [ -z "$BIN_EXPECT" ] || [ "$BIN_SHA" != "$BIN_EXPECT" ]; then
  log "REFUSED: build status '$BUILD_STATUS' or binary hash mismatch"
  echo "REFUSED: build status '$BUILD_STATUS' or binary hash mismatch"
  exit 2
fi
if [ ! -f "data/$SCEN.json" ] || [ ! -d "inits/$SCEN" ]; then
  log "REFUSED: no data or starts for $SCEN"
  echo "REFUSED: no data or starts for $SCEN"
  exit 2
fi

if [ -f "$RUN/receipt.txt" ] && grep -qx "status=complete" "$RUN/receipt.txt" \
   && grep -qx "manifest_sha256=$MANIFEST_SHA" "$RUN/receipt.txt" && grep -qx "binary_sha256=$BIN_SHA" "$RUN/receipt.txt"; then
  log "SKIP: complete receipt under the same manifest and binary"
  echo "SKIP: $SCEN is already complete"
  exit 0
fi

n=1
while [ -e "$RUN/attempt$n" ]; do n=$((n + 1)); done
A="$RUN/attempt$n"
mkdir "$A"
START="$(date +%s)"
START_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
log "START attempt $n on $(hostname), job ${PBS_JOBID:-none}"

write_receipt() {
  local k
  {
    echo "scenario=$SCEN"
    echo "attempt=$n"
    echo "status=$1"
    echo "manifest_sha256=$MANIFEST_SHA"
    echo "binary_sha256=$BIN_SHA"
    echo "host=$(hostname)"
    echo "pbs_jobid=${PBS_JOBID:-none}"
    echo "start=$START_ISO"
    echo "end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "seconds=$(( $(date +%s) - START ))"
    echo "settings=warmup $WARMUP; sampling $SAMPLING; adapt_delta $ADAPT_DELTA; max_depth $MAX_DEPTH; stepsize $STEPSIZE; seed $SEED; fit_seconds $FIT_SECONDS"
    for k in $(seq 1 "$CHAINS"); do
      echo "chain${k}_exit=$(cat "$A/chain$k.exit" 2>/dev/null || echo missing)"
      if grep -q "seconds (Total)" "$A/chain$k.csv" 2>/dev/null; then echo "chain${k}_complete=yes"; else echo "chain${k}_complete=no"; fi
      echo "chain${k}_maxrss_kb=$(awk -F': ' '/Maximum resident set size/ { print $2 }' "$A/chain$k.time" 2>/dev/null)"
    done
  } > "$A/receipt.tmp"
  mv "$A/receipt.tmp" "$A/receipt.txt"
  cp "$A/receipt.txt" "$RUN/receipt.txt"
}

on_signal() {
  trap '' TERM INT
  log "SIGNAL $1: stopping chains"
  pkill -TERM -f -- "$A/chain" 2>/dev/null
  sleep 2
  write_receipt "terminated_$1"
  exit 3
}
trap 'on_signal TERM' TERM
trap 'on_signal INT' INT

TIMEBIN=""
if [ -x /usr/bin/time ] && /usr/bin/time -v true > /dev/null 2>&1; then TIMEBIN=/usr/bin/time; fi
for k in $(seq 1 "$CHAINS"); do
  (
    set -- timeout --signal=TERM --kill-after=60 "$FIT_SECONDS" "$MODEL_BIN" sample \
      num_samples="$SAMPLING" num_warmup="$WARMUP" adapt delta="$ADAPT_DELTA" \
      algorithm=hmc engine=nuts max_depth="$MAX_DEPTH" stepsize="$STEPSIZE" \
      id="$k" data file="data/$SCEN.json" init="inits/$SCEN/chain$k.json" \
      random seed="$SEED" output file="$A/chain$k.csv" refresh=100
    if [ -n "$TIMEBIN" ]; then set -- "$TIMEBIN" -v -o "$A/chain$k.time" "$@"; fi
    "$@" > "$A/chain$k.stdout" 2> "$A/chain$k.stderr"
    echo $? > "$A/chain$k.exit"
  ) &
done
wait

status=complete
for k in $(seq 1 "$CHAINS"); do
  code="$(cat "$A/chain$k.exit" 2>/dev/null || echo missing)"
  if [ "$code" = "124" ] || [ "$code" = "137" ]; then
    status=timeout
  elif [ "$code" != "0" ] && [ "$status" = "complete" ]; then
    status=failed
  elif ! grep -q "seconds (Total)" "$A/chain$k.csv" 2>/dev/null && [ "$status" = "complete" ]; then
    status=failed
  fi
done
write_receipt "$status"
log "END attempt $n: $status"
echo "$SCEN attempt $n: $status"
case "$status" in
  complete) exit 0 ;;
  timeout) exit 4 ;;
  *) exit 1 ;;
esac
