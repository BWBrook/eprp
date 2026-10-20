#!/bin/bash
# Local runtime projection for the Q80 + adapt_delta 0.999 trial: the real settings (seed, starts, 2,000 warmup) then
# 200 retained draws, four chains, trace off. Local compiler, so not the cluster path; adaptation outcome and cost only.
cd "$(dirname "$0")"
R=../../../..
for k in 1 2 3 4; do
  ( /usr/bin/time -v ../../trace_build/model_v6 sample num_samples=200 num_warmup=2000 adapt delta=0.999 algorithm=hmc engine=nuts \
      max_depth=12 stepsize=0.01 id=$k data file=$R/data/q012-pilot/payload_v6q80/data/P11.json \
      init=$R/data/q012-pilot/payload_v6q80/inits/P11/chain$k.json random seed=77017 output file=chain$k.csv refresh=100 \
      > chain$k.log 2> chain$k.time ) &
done
wait
