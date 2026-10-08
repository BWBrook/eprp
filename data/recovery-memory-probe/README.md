# An observation-error counterexample to apparent recovery

Owner: Codex. Date: 8 October 2026. Status: small, synthetic feasibility check.
No fossil records, empirical rates or model deposits are used. This is not a
fossil observation simulator or an estimate of bias in PBDB.

The proposed impulse-response analysis needs to distinguish biological recovery
from a relation created by reusing the same estimated richness. The example
below establishes that risk with exact algebra and a reproducible numerical
check; it does not establish the bias of any particular extinction estimator.

## Definitions and exact result

True richness is constant. Let the observed richness index be
`Y[t] = constant + e[t]`, with independent, mean-zero errors of variance one.
Define an observed **loss proxy** `L[t] = Y[t-1] - Y[t]` and cumulative apparent
rebound `R[t,h] = Y[t+h] - Y[t]`, for a positive lag h. These are differences
between continuous estimated indices, not counts of extinct or originating taxa.
All transitions enter the demonstration; it does not select positive losses.

The shared `-e[t]` term gives `Cov(L,R) = 1`, while `Var(L) = 2`. Consequently,
the population regression slope of rebound on loss is **1/2**, despite no
biological change. With a separately measured, independent current anchor for
R, the slope is zero in this unsmoothed example.

Now let e be a width-w moving average of independent unit-variance errors. Its
autocovariance is `C(h) = max(w-h,0)/w^2`. The slope becomes

```
[C(h+1) - C(1) - C(h) + C(0)] / [2(C(0) - C(1))].
```

It is zero for `1 <= h < w` and 1/2 for `h >= w`. A three-bin smoother therefore
creates a delayed apparent rebound. Bin numbers here are arbitrary equal time
units; there is no conversion to geological Myr.

## Reproduction and results

Run from the repository root:

```
python3 data/recovery-memory-probe/probe.py
```

The standard-library script generates 100,000 **independent replicate histories**
per case, using seeds 20261008–20261010. Lags within a history share observations;
replicates are independent. It writes [summary.tsv](summary.tsv), including the
exact slope, simulated slope and Monte Carlo standard error. These standard
errors describe simulation noise under this artificial model, not fossil-data
uncertainty. Broad six-standard-error checks compare the simulations with the
independently derived algebra.

| Case | Lag | Exact slope | Observed numerical check |
| --- | --- | --- | --- |
| Unsmoothed, shared anchor | 1–6 | 0.5 | 0.4952–0.5026 |
| Three-bin smoothing, shared anchor | 1–2 | 0 | 0.0012–0.0021 |
| Three-bin smoothing, shared anchor | 3–6 | 0.5 | 0.4994–0.5035 |
| Unsmoothed, independent anchor | 1–6 | 0 | −0.0003–0.0070 |

All 18 checks passed. The local calculation took about 2.5 seconds. Generated
replicate histories are not retained; the seeds and script reproduce them.

## What this warrants

A loss-versus-rebound pattern alone does not identify a biological response
kernel. The loss definition, baseline and observation process belong in the
null. An independent anchor removes one mathematical coupling in this toy model;
it is not a general remedy for fossil sampling, shared taxa or dating errors.

Real fossil preparation can create different dependencies through range-through
counting, detection, uneven sampling and uncertain intervals. Those require a
separate, scientifically specified observation model. The proposed comparison
also needs to separate ordinary finite-rate dynamics that retain current state
from an additional dependence on earlier disturbance history. See the
[recovery contract and response note](../../literature/2026-10-08-recovery-contracts-and-response.md).
