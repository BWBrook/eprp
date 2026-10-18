#!/bin/bash
# Q-012 pilot runner: one fit is four single-threaded CmdStan chains.
# It verifies the payload, the build receipt (manifest and binary) and the runtime, never retries,
# keeps every attempt, and writes a receipt on completion, failure, timeout or signal.
# Each chain writes ONE ordered log (stdout and stderr on the same open file, refresh from run.env), so every
# progress marker and rejection message keeps its order. Each chain runs in its own process group within the job's
# session; on TERM or INT the groups get TERM,
# then KILL after a short grace, and the receipt is written only after they are gone.
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
refuse() { log "REFUSED: $1"; echo "REFUSED: $1"; exit 2; }

sha256sum -c --strict --quiet manifest.sha256 > "$RUN/manifest_check.txt" 2>&1 \
  || refuse "payload manifest mismatch; see $RUN/manifest_check.txt"
MANIFEST_SHA="$(sha256sum manifest.sha256 | cut -d' ' -f1)"
field() { awk -F= -v k="$1" '$1 == k { print substr($0, length(k) + 2) }' build/receipt.txt 2>/dev/null; }
[ "$(field status)" = "ok" ] || refuse "build receipt status is '$(field status)', not ok"
[ "$(field manifest_sha256)" = "$MANIFEST_SHA" ] || refuse "build receipt is for a different payload manifest"
BIN_SHA="$(sha256sum "$MODEL_BIN" 2>/dev/null | cut -d' ' -f1)"
[ -n "$BIN_SHA" ] && [ "$BIN_SHA" = "$(field binary_sha256)" ] || refuse "binary hash differs from the build receipt"
if [ -n "${MODULE:-}" ]; then
  case ":${LOADEDMODULES:-}:" in
    *":$MODULE:"*) ;;
    *) refuse "runtime module $MODULE is not loaded (LOADEDMODULES='${LOADEDMODULES:-}')" ;;
  esac
fi
ldd "$MODEL_BIN" > "$RUN/ldd.txt" 2>&1
grep -q "not found" "$RUN/ldd.txt" && refuse "missing shared libraries; see $RUN/ldd.txt"
[ -f "data/$SCEN.json" ] && [ -d "inits/$SCEN" ] || refuse "no data or starts for $SCEN"
[ "${LOG_FORMAT:-}" = "combined" ] && [ -n "${REFRESH:-}" ] || refuse "run.env must declare LOG_FORMAT=combined and REFRESH"

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
cp "$RUN/ldd.txt" "$A/ldd.txt"
START="$(date +%s)"
START_ISO="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PGIDS=""
CLEANUP="none"
log "START attempt $n on $(hostname), job ${PBS_JOBID:-none}"

write_receipt() {
  local k
  {
    echo "scenario=$SCEN"
    echo "attempt=$n"
    echo "status=$1"
    echo "manifest_sha256=$MANIFEST_SHA"
    echo "binary_sha256=$BIN_SHA"
    echo "module=${MODULE:-none}"
    echo "host=$(hostname)"
    echo "pbs_jobid=${PBS_JOBID:-none}"
    echo "start=$START_ISO"
    echo "end=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "seconds=$(( $(date +%s) - START ))"
    echo "settings=chains $CHAINS; warmup $WARMUP; sampling $SAMPLING; adapt_delta $ADAPT_DELTA; max_depth $MAX_DEPTH; stepsize $STEPSIZE; seed $SEED; fit_seconds $FIT_SECONDS; refresh $REFRESH; log $LOG_FORMAT"
    echo "cleanup=$CLEANUP"
    for k in $(seq 1 "$CHAINS"); do
      echo "chain${k}_exit=$(cat "$A/chain$k.exit" 2>/dev/null || echo missing)"
      if grep -q "seconds (Total)" "$A/chain$k.csv" 2>/dev/null; then echo "chain${k}_complete=yes"; else echo "chain${k}_complete=no"; fi
      echo "chain${k}_maxrss_kb=$(awk -F': ' '/Maximum resident set size/ { print $2 }' "$A/chain$k.time" 2>/dev/null)"
    done
  } > "$A/receipt.tmp"
  mv "$A/receipt.tmp" "$A/receipt.txt"
  cp "$A/receipt.txt" "$RUN/receipt.txt"
}

groups_alive() {
  local g
  for g in $PGIDS; do kill -0 -- "-$g" 2>/dev/null && return 0; done
  return 1
}

on_signal() {
  trap '' TERM INT
  local g end escalated=no survivors=no
  log "SIGNAL $1: TERM to chain process groups:$PGIDS"
  for g in $PGIDS; do kill -TERM -- "-$g" 2>/dev/null; done
  end=$(( $(date +%s) + 5 ))
  while groups_alive && [ "$(date +%s)" -lt "$end" ]; do sleep 1; done
  if groups_alive; then
    escalated=yes
    log "SIGNAL $1: KILL to chain process groups after 5 s"
    for g in $PGIDS; do kill -KILL -- "-$g" 2>/dev/null; done
  fi
  wait 2>/dev/null
  end=$(( $(date +%s) + 5 ))
  while groups_alive && [ "$(date +%s)" -lt "$end" ]; do sleep 1; done
  groups_alive && survivors=yes
  CLEANUP="signal $1; kill_escalated $escalated; survivors $survivors"
  write_receipt "terminated_$1"
  log "END attempt $n: terminated_$1 ($CLEANUP)"
  exit 3
}
trap 'on_signal TERM' TERM
trap 'on_signal INT' INT

TIMEBIN=""
if [ -x /usr/bin/time ] && /usr/bin/time -v true > /dev/null 2>&1; then TIMEBIN=/usr/bin/time; fi
set -m
for k in $(seq 1 "$CHAINS"); do
  (
    set +m
    set -- timeout --foreground --signal=TERM --kill-after=60 "$FIT_SECONDS" "$MODEL_BIN" sample \
      num_samples="$SAMPLING" num_warmup="$WARMUP" adapt delta="$ADAPT_DELTA" \
      algorithm=hmc engine=nuts max_depth="$MAX_DEPTH" stepsize="$STEPSIZE" \
      id="$k" data file="data/$SCEN.json" init="inits/$SCEN/chain$k.json" \
      random seed="$SEED" output file="$A/chain$k.csv" refresh="$REFRESH"
    if [ -n "$TIMEBIN" ]; then set -- "$TIMEBIN" -v -o "$A/chain$k.time" "$@"; fi
    "$@" > "$A/chain$k.log" 2>&1
    echo $? > "$A/chain$k.exit"
  ) &
  PGIDS="$PGIDS $!"
done
set +m
log "chain process groups:$PGIDS"
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
