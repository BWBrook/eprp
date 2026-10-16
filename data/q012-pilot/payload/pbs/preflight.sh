#!/bin/bash
# Preflight of a built model binary, run by build.pbs on the compute node (and locally by pilot.py selftest).
# (1) Log density and gradients at three fixed points against the local reference, relative tolerance 1e-6.
# (2) Four real chains through initialisation, the step-size search and ten warmup iterations on the replay dataset.
# Appends key=value lines to the receipt file given as $1; on failure writes the reason and exits 1.
set -u
REC="${1:?receipt file}"
. ./run.env
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
