#!/bin/bash
# Preflight of a built model binary, run by build.pbs on the compute node (and locally by pilot.py selftest).
# (1) Log density and gradients at three fixed points against the local reference, relative tolerance 1e-6.
# (2) CHAINS real chains through initialisation, the step-size search and ten warmup iterations on the replay dataset.
# (3) Divergence capture (Codex 76/2066), retained for the reused instrumented binary: P11 at fixed step 0.2 (finite energy errors) and 0.5 (rejections), unit
#     metric, no adaptation, 4 warmup + 8 saved draws: every transition diverges, so the trace must hold exactly the
#     CSV's divergent transitions with correct phases, full records for the first 2 warmup and 3 sampling events, short
#     records for the rest and a write_ok summary; the CSV must equal a trace-off run byte for byte.
# Trace-on/off identity is a property of the reused binary, established by its own v6d preflight; it is not repeated.
# Appends key=value lines to the receipt file given as $1; on failure writes the reason and exits 1.
set -u
REC="${1:?receipt file}"
. ./run.env
unset Q012_TRACE_FILE
mkdir -p build build/smoke
reason() { echo "$1" > build/preflight_reason.txt; exit 1; }

for f in preflight/point_*.json; do
  name="$(basename "$f" .json)"
  "$MODEL_BIN" log_prob jacobian=1 constrained_params="$f" data file=data/R00.json \
    output file="build/$name.csv" sig_figs=15 > "build/$name.stdout" 2>&1 || reason "preflight_log_prob_$name"
  awk -F, '/^#/ || /^lp__/ || NF == 0 { next }
           FNR == NR { for (i = 1; i <= NF; i++) ref[i] = $i; nref = NF; next }
           { seen = 1; if (NF != nref) bad = 1
             for (i = 1; i <= NF; i++) { d = $i - ref[i]; if (d < 0) d = -d; s = ref[i]; if (s < 0) s = -s; if (s < 1) s = 1
               if (d > 1e-6 * s) bad = 1 } }
           END { exit (bad || !seen || !nref) }' "preflight/ref_$name.csv" "build/$name.csv" || reason "preflight_mismatch_$name"
done
echo "preflight_log_prob=pass" >> "$REC"

# Deterministic solver controls: each reject_*.json point must be refused with a Powell residual failure.
for f in preflight/reject_*.json; do
  [ -e "$f" ] || continue
  name="$(basename "$f" .json)"
  if "$MODEL_BIN" log_prob jacobian=1 constrained_params="$f" data file=data/R00.json \
       output file="build/$name.csv" sig_figs=15 > "build/$name.stdout" 2>&1; then
    reason "preflight_control_not_rejected_$name"
  fi
  grep -q "algebra_solver: the norm of the algebraic function" "build/$name.stdout" || reason "preflight_control_wrong_rejection_$name"
done
echo "preflight_controls=pass" >> "$REC"

for k in $(seq 1 "$CHAINS"); do
  (
    timeout --signal=TERM --kill-after=30 "$SMOKE_SECONDS" "$MODEL_BIN" sample num_samples=1 num_warmup=10 \
      adapt delta="$ADAPT_DELTA" algorithm=hmc engine=nuts max_depth="$MAX_DEPTH" stepsize="$STEPSIZE" \
      id="$k" data file=data/R00.json init="inits/R00/chain$k.json" random seed="$SEED" \
      output file="build/smoke/chain$k.csv" refresh=1 > "build/smoke/chain$k.stdout" 2>&1
    echo $? > "build/smoke/chain$k.exit"
  ) &
done
wait
for k in $(seq 1 "$CHAINS"); do
  code="$(cat "build/smoke/chain$k.exit")"
  echo "smoke_chain${k}_exit=$code" >> "$REC"
  [ "$code" = "0" ] || reason "smoke_chain$k"
  grep -q "seconds (Total)" "build/smoke/chain$k.csv" || reason "smoke_chain${k}_incomplete"
  if grep -q "Unrecoverable\|Exception initializing" "build/smoke/chain$k.stdout"; then reason "smoke_chain${k}_fatal"; fi
done
echo "preflight_smoke=pass" >> "$REC"

# (3) Divergence capture.
mkdir -p build/exercise
exercise() {  # $1 step, $2 on|off
  (
    if [ "$2" = on ]; then
      export Q012_TRACE_FILE="build/exercise/s$1.trace.jsonl" Q012_TRACE_CHAIN=1 Q012_TRACE_WARMUP=4 \
        Q012_TRACE_CAP_WARMUP=2 Q012_TRACE_CAP_SAMPLING=3
    fi
    timeout --signal=TERM --kill-after=30 300 "$MODEL_BIN" sample num_samples=8 num_warmup=4 save_warmup=1 adapt engaged=0 \
      algorithm=hmc engine=nuts max_depth=8 stepsize="$1" id=1 data file=data/P11.json init=inits/P11/chain1.json \
      random seed="$SEED" output file="build/exercise/s$1_$2.csv" refresh=1 > "build/exercise/s$1_$2.log" 2>&1
  )
}
for st in 0.2 0.5; do
  exercise "$st" on || reason "exercise_${st}_on"
  exercise "$st" off || reason "exercise_${st}_off"
  cmp -s <(grep -v '^#' "build/exercise/s${st}_on.csv") <(grep -v '^#' "build/exercise/s${st}_off.csv") \
    || reason "exercise_${st}_trace_changes_output"
  T="build/exercise/s$st.trace.jsonl"
  head -1 "$T" | grep -q "^{\"type\":\"header\",\"schema\":\"$TRACE_SCHEMA\",\"chain\":1,\"warmup\":4,\"cap_warmup\":2,\"cap_sampling\":3,.*\"config_ok\":true}$" \
    || reason "exercise_${st}_header"
  tail -1 "$T" | grep -q '^{"type":"summary","transitions":12,.*"write_ok":true}$' || reason "exercise_${st}_summary"
  csv_div="$(awk -F, '/^#/ { next } !h { for (i = 1; i <= NF; i++) if ($i == "divergent__") c = i; h = 1; next }
                      { n++; if ($c == 1) printf "%d ", n }' "build/exercise/s${st}_on.csv")"
  trace_div="$(grep -o '^{"type":"divergence","chain":1,"transition":[0-9]*' "$T" | grep -o '[0-9]*$' | tr '\n' ' ')"
  [ -n "$csv_div" ] && [ "$csv_div" = "$trace_div" ] || reason "exercise_${st}_events_differ_from_csv"
  for ph in warmup sampling; do
    cap=2; [ "$ph" = sampling ] && cap=3
    n="$(grep -c "\"phase\":\"$ph\"" "$T")"
    grep "\"phase\":\"$ph\"" "$T" > "$T.$ph"
    full="$(grep -c '"captured":true,.*"initial":{"q":\[.*"previous":{"q":\[.*"failing":{"q":\[.*"inv_metric":\[' "$T.$ph")"
    want=$(( n < cap ? n : cap ))
    [ "$n" -gt "$cap" ] && [ "$full" = "$want" ] || reason "exercise_${st}_${ph}_capture_${n}_${full}"
    [ "$(head -n "$cap" "$T.$ph" | grep -c '"captured":true')" = "$cap" ] || reason "exercise_${st}_${ph}_order"
    [ "$(tail -n +"$((cap + 1))" "$T.$ph" | grep -c '"captured":true\|"initial"')" = 0 ] || reason "exercise_${st}_${ph}_dropped"
  done
  echo "preflight_exercise_${st}=pass events ${csv_div% }" >> "$REC"
done
