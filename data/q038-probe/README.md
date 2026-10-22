# Q-038 primary probe: implementation and the five-dataset S2 pilot

Contract: [v3](../q038-predictor-contract/contract.md), section D. Cleared for
implementation by Codex in 76/2195. This pilot measures **runtime and
convergence only**: five datasets cannot pass any recovery gate. The larger
campaign and any empirical fit remain held.

| File | Role |
| --- | --- |
| [core.py](core.py) | The one feature and scaling convention (fixed affine transforms from [deposit_constants.json](deposit_constants.json)), the generator, the reference CJS likelihood, the fold builder, Stan data, and the forecast |
| [model.stan](model.stan) | The ε = 1 CJS with Binomial(E_t, 1 − e^{−θ}) reference-count emissions, conditional on the first record and its count; `reduce_sum` over components |
| [checks.py](checks.py) | Implementation checks C1–C6, against the actual code; [checks.json](checks.json) |
| [deposit_constants.py](deposit_constants.py) | Derives [deposit_constants.json](deposit_constants.json) from `pbdb.cleaned.classes.csv` (SHA-256 `239d668a…`) and [stages.tsv](../q038-predictor-contract/stages.tsv) (`bdbfe924…`); reproduces it byte for byte (`e1323eec…`) |
| [run.py](run.py) | Manifest, generation, benchmark, fits and summary |
| [manifest.json](manifest.json) | Truth values, event excesses calibrated deterministically (seed 38000) **before** any dataset was generated, seeds, the feature convention, fit settings and input hashes |

**Declared conventions** (Codex 76/2195, implementation requirements):

1. **Emissions.** A living genus emits a reference count
   Binomial(E_t, 1 − e^{−θ}) after its first record; a dead genus emits
   zero. The likelihood conditions on the first record and its count.
2. **Hazard covariates.** For s → s + 1 they use records in stages before
   s, with the first-record stage always included. Detection uses
   w = log mean count over recorded stages before t.
3. **Fixed affine transforms**, frozen from 19,426 deposit
   genus-transitions, replace data-dependent z-scores. Coefficients
   therefore mean the same in generator, fit and forecast. Before the
   first record (generator only), covariates and w are 0.
4. **Shared future effects.** Event, class-stage and clade effects belong
   in the outer predictive draw. Each genus's own future marks are
   integrated given that draw.
5. **LOEO restarts keep the observed history** (contract section E). The
   restart conditions on its capture and count; its covariates use the
   genus's history from its own first record.

## Benchmark and execution plan (22 October 2026, deep-server)

**Benchmark** ([pilot/bench_38001.json](pilot/bench_38001.json)): dataset
38001, with 2,777 components and 126,305 rows.
- **Run:** 100 warmup and 100 sampling iterations, 4 chains × 12 threads.
  It took **1,334 s, about 6.7 s per iteration**, with no divergences and
  no tree-depth hits. R-hat was 1.04 and the minimum bulk ESS 83, as
  expected from so short a run.
- **β̄_e:** Rhynchonellata 0.73 ± 0.16 and Bivalvia 0.46 ± 0.16, with
  truth 0.5 inside both 95% intervals. The posterior SD is 0.16 against a
  prior SD of 1. **This is provisional:** the run fails its own screen
  (R-hat 1.04, bulk ESS 83), so it does not establish posterior precision,
  and truth inside two intervals in one dataset is not coverage evidence.

**The five full fits** (1,000 warmup and 1,000 sampling iterations) run
**concurrently**, at 4 chains × 3 threads each (60 threads).
- **Forecast:** about 3.7 h per fit at 12 threads per chain, and roughly
  three times longer at 3, so **about 11 h** in total.
- **Execution limit: 24 h.** Each fit writes its own result file as it
  finishes, so an interruption keeps the completed fits.

**Cost signal for the planned campaign.** About 3.7 h × 48 threads per fit
means the 600-dataset campaign of section 8 would need on the order of
**10⁵ core-hours**. Its design and cost therefore need revising before
anyone proposes it. The completed pilot will make that estimate precise.
- **Correction (Codex 76/2215).** 10⁵ core-hours (106,736 by linear
  extrapolation) is only the **full-fit subtotal**. Five forward folds add
  1.08 times a full fit's rows and five LOEO folds 3.09 times, so all
  eleven fits per dataset come to about 5.2 times the work before the
  matched model. Row counts measure work, not runtime.
- **Pilot accounting:** allocated core-hours are wall time × 4 chains × 3
  threads = **wall × 12**. `run.py summarise` reports every attempted
  seed, including any without a result file.
- The blanket campaign is withdrawn. A costed redesign follows the pilot.

## LOEO restart repair (22 October 2026; Codex 76/2213)

**The defect.** `component_loglik` and `stan_data` rebuilt the history from
the restart stage. A restarted genus therefore lost its age, earlier counts
and detection history, and had the first-record exception applied twice.
In Codex's counterexample the suffix log likelihood moved by −0.201.

**The repair.** `core.component_history` builds the history from the
genus's first record through the component start. Likelihood still starts
at the restart capture. The Stan model is unchanged; its precomputed rows
are now correct.

**Check C6:**
- Codex's counterexample suffix is **−8.98842587328**, matching his
  independent alive/dead recursion (−8.9884258733) to 2.3e-11. It is
  exactly invariant (0.0) when the held-out event's ω and δ shift by +10.
- A restarted suffix with fixed earlier history has total probability 1
  to 4e-16, for first counts 1 and 2.
- **All 169 LOEO restarts** on the real design (C4's simulated data, five
  events) satisfy suffix = full history − prefix to capture to 1.4e-14.
  Their Stan rows equal the full-fold rows for the same transitions
  exactly.
- C1, C3, C4 and C5 are unchanged. C2's 400-genus LOEO subset contains no
  restart, so its value is unchanged.

**The running fits are unaffected.** On all five pilot datasets, the
repaired code's full-fold and all forward-fold Stan data are identical to
those of the pre-repair code the fits run on.

## Pilot outcome (22 October 2026): 0 of 5 pass the convergence screen

[pilot/summary.json](pilot/summary.json) and `pilot/fit_SEED.json`. All
five attempted seeds completed and wrote results.

| Seed | Wall (h) | Allocated core-h | Divergences | Max R-hat | Min bulk / tail ESS | β̄_e Rhynch. [95%] | β̄_e Bival. [95%] |
| --- | ---: | ---: | ---: | ---: | --- | --- | --- |
| 38001 | 3.19 | 38.3 | 50 | 1.053 | 119 / 405 | 0.73 [0.42, 1.04] | 0.46 [0.15, 0.75] |
| 38002 | 3.10 | 37.2 | 96 | 1.013 | 383 / 168 | 0.53 [−0.17, 1.19] | 0.37 [−0.30, 1.02] |
| 38003 | 3.04 | 36.5 | 20 | 1.008 | 337 / 687 | 1.02 [0.26, 1.67] | 0.79 [0.12, 1.38] |
| 38004 | 3.19 | 38.3 | 9 | 1.010 | 176 / 353 | 0.98 [0.61, 1.36] | 0.32 [−0.00, 0.66] |
| 38005 | 3.08 | 37.0 | 119 | 1.024 | 153 / 38 | 0.47 [−0.00, 0.98] | 0.71 [0.23, 1.18] |

- **Screen:** R-hat ≤ 1.01, bulk and tail ESS ≥ 400, zero divergences. No
  fit passes. There were no tree-depth hits; the median is 63 leapfrog
  steps.
- **Recovery:** truth β̄_e = 0.5 lies in 9 of 10 intervals. Given the
  failed screen, this is not recovery evidence.
- **Cost:** 3.0–3.2 h wall at 4 chains × 3 threads, **about 37 allocated
  core-hours per fit**. That is a fifth of the 178 extrapolated from the
  48-thread benchmark: `reduce_sum` scales poorly to 12 threads per chain.
  At this configuration, 600 full fits would be about 22,500 core-hours.
  Convergence, not runtime, is now the binding problem.

**Diagnosis** (`divergence_diagnosis.json`, from the CmdStan draws):
- **Divergences are chain-specific and track the adapted step size.** In
  38005, 84 of 119 are in the chain with step 0.099 (the others have
  0.060–0.085). In 38002, 52 of 96 are in the chain with step 0.092 (the
  others ≈ 0.07).
- **Additive redundancy:**
  - corr(gd0, mean b_fam) is −0.80 to −0.90;
  - corr(gd0, mean ν) is −0.25 to −0.46;
  - corr(mean α, mean g_ord) is −0.58 to −0.88;
  - gd0's posterior SD (0.049–0.066) is 2.5–3× that of the identified sum
    gd0 + mean ν + mean b_fam (0.017–0.029).

  The worst R-hat is on gd0 in three seeds.
- **Baseline walk:** the median of Bivalvia's s_α in divergent draws sits
  at its 0.82–0.98 quantile in four seeds. Its truth is 0 (σ_α = 0 in S2).
- **No single funnel.** The other hierarchical scales show no consistent
  shift in divergent draws.

## Divergence diagnostic (declared before launch; not an adopted model)

**Runs:** seeds **38001** (worst R-hat) and **38005** (most divergences),
same data, same 4 × (1,000 + 1,000) iterations, deep-server, 4 chains × 3
threads, all four fits concurrent (48 threads).

| Variant | Model | adapt_delta | Isolates |
| --- | --- | ---: | --- |
| `ad95` | [model.stan](model.stan), unchanged | 0.95 | step-size tuning |
| `stz95` | [model_stz.stan](model_stz.stan) | 0.95 | additive redundancy, at the same tuning |

- **`model_stz.stan`:** f_fam, g_ord, b_fam and ν are `sum_to_zero_vector`
  within class, scaled so each element keeps marginal SD s. The
  intercepts α and gd0 then carry the means. The likelihood is
  unchanged.
- This changes the prior, not the data model. It is offered to Codex as a
  candidate repair, not adopted.
- **Reported:** the same screen and receipts as the pilot, via
  `run.py diag SEED VARIANT THREADS` writing `pilot/diag_VARIANT_SEED.json`.
- **Ceiling:** 12 h wall per fit, about 600 allocated core-hours at most.
  The forecast is 4–6 h, because adapt_delta 0.95 takes smaller steps.
