#!/bin/bash
# Fixed-metric step-size sweep for the Q80 + adapt_delta 0.999 runtime projection (local, no adaptation).
cd "$(dirname "$0")"
B=../trace_build/model_v6
go() {  # chain eps_base factor Q
  local tag="c$1_f$3_Q$4"; local eps; eps=$(python3 -c "print($2*$3)")
  "$B" sample num_samples=300 num_warmup=0 adapt engaged=0 algorithm=hmc engine=nuts max_depth=12 stepsize="$eps" \
    metric_file="metric_c$1.json" id=1 data file="P11_Q$4.json" init="init_c$1.json" random seed=77017 \
    output file="$tag.csv" refresh=0 > "$tag.log" 2>&1
  echo "$tag $eps exit $?"
}
for f in 1.0 0.8 0.65 0.5; do go 1 0.039571317 $f 80 & go 3 0.028885989 $f 80 & done
go 1 0.039571317 1.0 64 & go 3 0.028885989 1.0 64 &
wait
