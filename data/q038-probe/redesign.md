# Q-038 costed redesign (draft; not frozen, nothing launched)

> **PARKED (23 October; Codex 76/2330).** This draft is historical. The
> estimator failed every gate, and any future tranche needs a new
> model/design contract.

Owner: Claude | 22 October 2026 | Replaces the blanket campaign of contract
section 8, following Codex 76/2215 and the
[cost note](../../ideas/2026-10-22-q038-campaign-cost-and-triton-codex.md).

**Status:**
- **Blocked on convergence.** The five-fit pilot failed its screen in all
  five datasets (README, "Pilot outcome"). No experiment below runs until a
  model passes the screen on the pilot seeds.
- The declared diagnostic (ad95 against stz95) decides the repair. Costs
  are written per full-fit equivalent, **c core-hours**: c ≈ 37 for the
  pilot model at 4 chains × 3 threads, to be replaced by the repaired
  model's measured value.
- **This is a design ceiling, not launch permission** (Codex).

## 1. Three experiments, kept apart

| | Recovery | Falsification | Prediction |
| --- | --- | --- | --- |
| **Question** | Does the fit recover β̄_e,c? | Does a false selectivity pattern escape its predeclared diagnostic? | Does event occupancy improve held-out forecasts? |
| **Scenarios** | S1 (β̄_e = 0) and S2 (β̄_e = 0.5), separately | S0 null; S3 and S4 on a stated baseline | S1 and S2 |
| **Fits per dataset** | 1 full | 1 full (S3, S4); 2 × 5 forward folds (S0) | full model and matched model, 5 forward folds each |
| **Datasets** | looks at 20, 60, at most 100 attempts per scenario | 10 each, initially | 5 S1 + 5 S2, fixed seeds |

Fresh seed ranges, declared in a manifest before any data: 381xxx (S1),
382xxx (S2), 380xxx (S0), 383xxx (S3), 384xxx (S4). The five development
pilot datasets are **never pooled** into any experiment (Codex).

## 2. Recovery: sequential looks with error spending

- **Looks** at 20, 60 and 100 **attempted** datasets per scenario. A failed
  fit counts as non-coverage, and its failure type is kept.
- **Coverage gate per class and scenario.** Clopper–Pearson intervals with
  error spending .010, .015 and .025 at the three looks; the sum is .05 by
  union bound.
  - **Pass:** point ≥ 0.90 and the spent lower bound ≥ 0.85.
  - **Fail:** the spent upper bound < 0.90.
  - Otherwise continue. At the cap the result is unresolved and stays so.
- **Claims are per class and scenario (four claims).** No simultaneous
  claim is made. If one is wanted, the .05 is divided across the four.
- **Bias** is assessed once, at the terminal look of each scenario, with
  its Monte Carlo SE. It is conditioned on successful fits and reported
  beside the failure rate. There are no early bias declarations.
- **Stopping:** a scenario stops at the first look where both classes have
  passed or failed.
- **For scale** (Codex): 57/60 is still unresolved under spending (lower
  bound .837), and 95/100 passes (.877).

## 3. Falsification panels

- **S0** (uniform biological null; shared nuisance and clade zeroed
  globally; README, "Scenario generators"):
  - Gate: null B gain within ±0.02 nats per genus, with its Monte Carlo
    interval.
  - This needs forward-fold scoring of the full and matched models, so
    S0 costs as much per dataset as the prediction experiment.
- **S3** (survivor-tracking exposure) and **S4** (reference-level
  clustering):
  - **Proposed baseline: S1**, because the primary estimand is the
    occupancy mean, and S1 is where false inference about it would show.
  - An S0 baseline would test a generic selectivity claim. It would be a
    separate, labelled panel, not mixed in (Codex).
  - **Predeclared diagnostics:**
    - S3: a posterior predictive check of post-event detection rates by
      stage.
    - S4: a posterior predictive check of between-stage dispersion in
      reference counts.
  - **The finding of interest:** a 95% interval for β̄_e excluding 0
    while the diagnostic stays silent.
- **Ten datasets per panel** can expose a counterexample but cannot
  establish a small false-positive rate. Expand only against a declared
  uncertainty target.

## 4. Prediction

- **Datasets:** 5 S1 and 5 S2, fixed seeds. All five forward events are
  kept; none is selected after results.
- **Matched model:** removes the whole event-occupancy contribution,
  β̄_e,c *and* δ_k. The nuisance structure is unchanged.
- **Score:** the marked-history predictive q (contract v3 A), integrated
  over posterior draws. Exact enumeration as in `predict_q(exact=True)`,
  in stable log arithmetic. Paired differences are taken on the same
  datasets.
- **LOEO:** secondary and deferred. Its restart defect is repaired (C6).

## 5. Cost (c = core-hours per full-fit equivalent)

Row-work multiples from the cost note: five forward folds together = 1.08
full fits.

| Component | Fit-equivalents, first stage | Fit-equivalents, maximum |
| --- | ---: | ---: |
| Recovery S1 + S2 | 40 | 200 |
| S0 panel (10 × 2 models × 1.08) | 21.6 | 21.6 |
| S3 + S4 panels (10 + 10 full) | 20 | 20 |
| Prediction (10 × 2 models × 1.08) | 21.6 | 21.6 |
| **Total** | **103** | **263** |

- **At c = 37:** about **3,800 core-hours first stage** and **9,700
  maximum**.
- On deep-server (about 62 usable threads, roughly 1,500 core-hours a day)
  that is about 2.5 days first stage and 6.5 days maximum.
- kunanyi would shorten wall time. It does not change whether the
  experiment earns its cost (Codex).
- Fold posteriors may differ in per-row cost, so row multiples are work
  counts, not runtime predictions.

## 6. Implementation still needed

1. Forward-fold fitting (the fold builder exists) and the matched model.
2. ~~The outer posterior-predictive scoring workflow~~: done in
   [score.py](score.py), checks S1–S4. It costs about 7 s per event per 400
   draws, negligible beside the fits.
3. Posterior predictive diagnostics for S3 and S4.
4. A campaign runner with durable attempt and failure receipts, so the
   denominator never comes from completed result files.
5. Per-scenario manifests: truths, calibrated ω and seeds, frozen before
   data.
