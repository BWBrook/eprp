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
- **Caveat on "divergent draws".** These are the states CmdStan *saved*
  for transitions flagged divergent: the selected states, not the points
  where the integrator failed (as Codex established for Q-012 on
  18 October). The step-size and redundancy findings do not depend on
  them. The s_α-tail association is indicative only.

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

## Scenario generators for the redesign (implemented, not run)

`core.TRUTH`, `truth_params(..., scenario)`, `calibrate_omega(..., scenario)`
and `simulate(..., obs=None | "S3" | "S4")` now generate contract v3
section B's scenarios. Nothing has been fitted. Three choices are made
here and flagged for Codex:

1. **S0 zeroes the shared nuisance and clade effects globally** (γ = 0,
   s_f = s_o = 0), with β̄_e = 0 and τ = 0. This is the first of Codex's
   two options in 76/2195. Events are then exactly η = α + ω, while
   background occupancy (β_b) and detection heterogeneity remain. The
   fitted model is therefore not misspecified under S0.
2. **S3: survivor-tracking exposure** uses E_t × (1 − L_c,k), rounded, for
   t = k+1 … k+3 (the forecast window M) after each event. L_c,k is the
   calibrated class event loss, not each dataset's realised loss, so
   genera are still simulated one at a time. The fit still uses E_t.
3. **S4: reference-level clustering** draws one ζ_r ~ N(0, 0.5²) per
   reference and stage, shared by all genera of both classes. Each genus
   is detected by reference r with probability 1 − exp(−θ e^{ζ_r}).

S3 and S4 change only the observation process, so each needs a stated
biological baseline (Codex 76/2215): S1 for the occupancy-mean claim, or
S0 for a generic selectivity claim. That is the redesign's choice.

**Check C7** (all of C1–C7 pass):
- The S2 path is unchanged: all five pilot datasets regenerate
  identically.
- S0 and S1 calibrations reproduce the deposit event losses on a fresh
  seed, to 1.5e-14 and 0.0035. S0's event η has zero spread.
- S3: a tiny design's post-event mean count matches round(40 × 0.735) × p
  (z = 1.0), while the fitted path matches 40 × p (z = 1.3).
- S4: the stage mean matches the ζ-integrated expectation (z = 1.6),
  0.947 against 0.792 for the plain binomial.

## Posterior-predictive scoring (implemented; redesign item 2)

[score.py](score.py) implements contract v2 section 4 under v3 section A,
vectorised over posterior draws.
- `from_stan` maps a fit's draws to a draws-last layout, which `core.eta`
  already broadcasts over.
- **Exact stage-k branching.** For each draw, q sums the stage-k reference
  count exactly; the binomial tail dropped has mass below 1e-18. It then
  applies the zero-record survival recursion through k + M. Both q and
  1 − q come from complementary log formulas.
- **Set and count laws.** The O law (no record in k+1 … k+M, over the
  prefix risk set) and the synthetic B law (deaths at k among true
  members) both condition **after** integration:
  log Σ_m P(S|θ_m) − log Σ_m P(D|θ_m). The count law uses a
  Poisson-binomial dynamic programme.
- **Also reported:** the gain per genus against log 1/C(N, D), the
  unconditional score, and batch-means delta-method Monte Carlo SEs
  (Codex's minor item).

**Checks** ([score_checks.json](score_checks.json)):
- **S1:** the vectorised q equals `core.predict_q(exact=True)` to 8.7e-14
  over 216 genus-draw comparisons (actual design, events 21, 38 and 68,
  M = 2).
- **S2:** q + (1 − q) = 1 exactly.
- **S3:** by brute force over all 2⁹ sets of a nine-genus risk set, the
  conditional set law is normalised to 3.6e-15 for every D, and the count
  DP matches enumeration to 2.8e-16.
- **S4, cost:** one event's O and B scores over 400 draws take 7 s (331
  genera). The integrated score's Monte Carlo SE is about 0.43 nats in
  total (0.0013 per genus). The draws here are truth-perturbed stand-ins,
  not a posterior, so the scores carry no inferential meaning.

## Per-gradient cost benchmark (queued 22 October; Codex 76/2215)

`run.py tbench SEED THREADS GRAIN` times gradients for one chain.
- **Start:** the pilot fit's last draw, with its adapted step size and
  diagonal metric. Tree depth ≤ 4 and no adaptation, so every iteration
  runs 15 leapfrog steps.
- **Timing:** (wall₄₁ − wall₁) / (gradients₄₁ − gradients₁) removes start-up
  and data loading.
- **Smoke test:** on deep-server under load, 0.102 s per gradient at 2
  threads (15 gradients per iteration, as designed).
- **Queued:** `q038_tbench_queue.sh` on deep-server waits for the four
  diagnostic fits to finish. It then runs threads 1, 2, 3, 4, 6, 8, 12 and
  16 at grain sizes 50, 1 and 250, **one at a time** on the idle machine,
  writing `pilot/tbench_tT_gG.json`.
- The pilot suggests 3 threads per chain costs about a fifth of the
  core-hours of 12. This measures the curve, in isolation, before any
  model simplification.

## Divergence diagnostic: results (23 October)

`pilot/diag_VARIANT_SEED.json`. The screen and receipts are those of the
pilot.

| Variant | Divergences (38001 / 38005) | Max R-hat | Min bulk ESS | Min tail ESS | Wall (h) |
| --- | --- | --- | --- | --- | --- |
| pilot (model.stan, 0.80) | 50 / 119 | 1.053 / 1.024 | 119 / 153 | 405 / 38 | 3.2 / 3.1 |
| ad95 (model.stan, 0.95) | 10 / 12 | 1.019 / 1.009 | 342 / 345 | 475 / 617 | 3.4 / 3.4 |
| stz95 (model_stz.stan, 0.95) | **3 / 6** | **1.007 / 1.007** | **515 / 508** | **1044 / 859** | 3.5 / 4.0 |

- **Step size alone (ad95)** cuts divergences about tenfold, but gd0 still
  fails R-hat (1.019) and bulk ESS stays below 400.
- **Sum-to-zero plus 0.95 (stz95)** passes R-hat and both ESS gates on both
  seeds. **Only the zero-divergence rule fails**, on 3 and 6.
- **β̄_e is stable across all six fits:** Rhynchonellata 0.73 ± 0.16 and
  Bivalvia 0.46 ± 0.16 on 38001; 0.47–0.49 ± 0.24 and 0.71–0.72 ± 0.24 on
  38005. The parameterisation moves mixing, not the estimand.
- **Where the remaining divergences sit:**
  - **In the chain that adapted the largest step**, as in the pilot: 5 of 6
    (step 0.060 against 0.036–0.038), 2 of 3 (0.054 against 0.036–0.041),
    8 of 10 in ad95 38001 (0.063 against 0.032–0.044), and all 12 in the
    two large-step chains of ad95 38005 (0.060 and 0.057 against
    0.034–0.037).
  - **In the Bivalvia baseline-walk scale s_α[2]** (truth 0): its upper
    tail, at the 0.8–1.0 quantile, in 25 of 31 divergent transitions. No
    other scale shows a pattern. These are saved states, so this is
    indicative only.
- **Cost:** median 127 leapfrog steps (tree depth 7), against 63 in the
  pilot, but only about 10–25% more wall time with four fits running
  concurrently instead of five.

**Next diagnostic, declared before launch: `stz99`.** model_stz.stan at
adapt_delta 0.99, on seeds 38001 and 38005, under the same pilot design
and screen.
- It tests whether a sampler-level change removes the residual
  divergences that come from one chain's larger step.
- **Ceiling:** 12 h per fit; both fits run concurrently on deep-server.
- **If it fails,** the remaining lever is s_α (the Bivalvia baseline walk
  when its truth is 0). That would be a model or prior choice for Codex,
  not a sampler setting.

## Per-gradient benchmark: results (23 October)

`pilot/tbench_tT_gG.json`: deep-server, one chain alone on the idle
machine, seed 38001.

| Threads | 1 | 2 | 3 | 4 | 6 | 8 | 12 | 16 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| s/gradient, grain 1 | 0.078 | 0.041 | 0.028 | 0.022 | 0.015 | 0.012 | 0.0081 | 0.0063 |
| efficiency, grain 1 | 1.00 | 0.95 | 0.93 | 0.90 | 0.86 | 0.84 | 0.80 | 0.77 |
| efficiency, grain 50 | 1.00 | 0.92 | 0.91 | 0.86 | 0.80 | 0.76 | 0.68 | 0.61 |
| efficiency, grain 250 | 1.00 | 0.91 | 0.85 | 0.74 | 0.67 | 0.55 | 0.37 | 0.21 |

**Correction (to 76/2225 and this README's earlier cost note).**
- `reduce_sum` does **not** scale poorly to 12 threads. With grain 1 it
  keeps 80% efficiency at 12 threads and 77% at 16. Grain 50, the pilot's
  setting, drops to 68% at 12; grain 250 collapses.
- The "178 core-hours per fit at 12 threads" figure was an artefact. It
  linearly extrapolated a 200-iteration benchmark dominated by early
  warmup, where trees run up to 1,023 leapfrog steps (about 725 per
  iteration implied, against 63 in sampling).
- **Use grain size 1.**
- **Load matters more than thread count.** Under the four-fit load, stz95
  took an *estimated* 0.047 s per gradient per chain at 3 threads (from
  the median of 127 leapfrog steps and an assumed warmup share), against
  0.028 in isolation, so contention costs roughly 1.7×.
- **For the redesign, use measured fits per day,** not per-fit core-hours
  extrapolated from a short run. With four concurrent fits deep-server
  completes about one stz95 fit per hour.

## Scorer repairs (23 October; Codex 76/2247)

- **Per class.** `score_event` now returns separate O and B scores for each
  class. The outer draws stay shared, but pooling is removed, as the
  contract's section 8 gates require.
- **Log-space count DP,** so rare counts cannot underflow.
- **Validity.** A non-finite result, or a conditional log probability above
  zero, raises an error. Endpoints (D = 0 or N) return exactly 0.

**New checks:**
- **S5:** Codex's two-class uniform null, with q = (0.2, 0.2, 0.8, 0.8) and
  D = 2. The pooled expected gain reproduces 0.248857705 nats per genus;
  within-class gains are 5.6e-17.
- **S6:** N = 1,000, q = 0.99, D = 1 gives −6.907755279, which is −log 1000
  to 4.5e-12. The old DP returned +∞.
- **S7:** both endpoints are exactly 0.
- S1–S3 are unchanged.

**Correction to the earlier S4 report.** The pooled B gain of 0.086 per
genus on truth-perturbed stand-in draws mostly disappears per class: −0.0005
for Rhynchonellata and 0.0035 for Bivalvia. Most of it was the class
severity difference that Codex's counterexample isolates. None of these
stand-in scores is inferential, and a score Monte Carlo precision target
still has to be declared before any campaign uses the scores.

## Exact prior-preserving centring: model_ctr.stan (23 October; Codex 76/2249)

**What it is.** [model_ctr.stan](model_ctr.stan) keeps model.stan's
likelihood and every other prior. The four effect vectors become zero-sum
deviations with an *unscaled* standard-normal density, covariance
s²(I − J/N). Their independent Gaussian means are integrated into the
effective intercepts:
- α₁,c ~ N(logit 0.1, √(1.5² + s_fam²/40 + s_ord²/8));
- gd0,c ~ N(log 0.01, √(2² + s_b²/40 + s_ν²/T)).

**Pre-fit checks** ([ctr_checks.py](ctr_checks.py),
[ctr_checks.json](ctr_checks.json)):
- **V1:** Stan's `sum_to_zero_vector` with `std_normal` has covariance
  I − J/N. Sampled at N = 8 (40,000 draws), the largest deviation is 0.025
  (Monte Carlo noise) and the marginal variance 0.877 against 0.875.
- **V2:** the joint prior on likelihood predictors equals the original's to
  4.4e-16 for N = 8, 40 and 87.
- **V3:** at a fixed truth state, mapped across representations, the
  likelihood is identical (difference 0.0) on the full and LOEO folds. All
  208 shared-parameter gradients agree to 2.3e-13.

So **model_ctr is the original model, reparameterised, not a new prior.**
The stz95/stz99 candidate did change the prior: by Codex's arithmetic it
inflates contrast variance by 14.3% for 8 orders and drops the random-mean
variance from the intercepts.

## stz99 result (23 October): no divergences, but both fail the screen narrowly

| Seed | Divergences | Max R-hat (worst) | Min bulk / tail ESS | Wall (h, 6 threads per chain) |
| --- | --- | --- | --- | --- |
| 38001 | **0** | 1.0104 (s_b) | 371 / 516 | 2.76 |
| 38005 | **0** | 1.0138 (s_ord; then s_b and g_ord) | 470 / 342 | 2.83 |

**Every declared attempt, so far:**

| Attempt | Divergences (38001 / 38005) | Screen |
| --- | --- | --- |
| Pilot (0.80) | 50 / 119 | fail |
| ad95 | 10 / 12 | fail |
| stz95 | 3 / 6 | fail on divergences |
| stz99 | 0 / 0 | fail on R-hat and ESS |

**Reading.**
- adapt_delta 0.99 removes the divergences.
- The slowest-mixing quantities are now the hierarchical scales (s_b; s_ord,
  with only 8 orders; s_fam).
- The adapted steps were 0.019–0.035, with median trees of 127–255 leapfrog
  steps.
- β̄_e is unchanged again: 0.74 ± 0.16 and 0.46 ± 0.16 on 38001; 0.49 and
  0.72 ± 0.24 on 38005.
- stz99 used the *changed* prior, so it is evidence about that candidate
  only.

## The one finite centring evaluation (declared 23 October, before launch; Codex 76/2249 stopping rule)

**Design:**
- model_ctr.stan (the exact original prior), seeds 38001 and 38005,
  adapt_delta 0.99, 4 chains × 6 threads, 1,000 warmup iterations.
- **2,000 post-warmup draws per chain** (`run.py diag SEED ctr99 6`).
- **The screen is unchanged:** zero divergences, R-hat ≤ 1.01, and bulk and
  tail ESS ≥ 400.

**Why the longer chain.** stz99 removed the divergences but left the
slow-mixing scales just short at 1,000 draws. Doubling the draws is a
declared resource choice, not a relaxed gate. If adopted, it roughly
doubles the per-fit sampling cost of any campaign; the redesign's cost
would be re-measured.

**Resource allowance:** two concurrent fits on deep-server (48 threads), at
most 10 h wall each, so at most 480 allocated core-hours. The forecast is
about 4–5 h.

**Stopping rule (Codex's):** if either fit fails the screen, sampler tuning
stops and this returns to Codex as a model or design decision. There will
be no further adaptation or prior cycling.

## Centring evaluation result (23 October): FAIL; sampler tuning stops (Codex's rule)

| Seed | Divergences | Max R-hat (worst) | Min bulk / tail ESS | Wall (h) |
| --- | --- | --- | --- | --- |
| 38001 | 1 | 1.0141 (s_b) | 703 / 1016 | 3.2 |
| 38005 | 6 | 1.0046 (s_ord) | 1211 / 1787 | 3.8 |

- **ESS now passes comfortably** at 2,000 draws. **Divergences return**
  under the exact original prior (stz99, with the changed prior, had none).
  R-hat fails on 38001.
- **Where they sit.** As in every variant, the divergences are in the one
  chain that adapted the largest step: 6 of 6 in the chain at 0.042 (others
  0.019–0.028), and 1 of 1 in the chain at 0.036. They are also at the
  extreme upper tail of **s_α[2], the Bivalvia baseline random-walk scale,
  whose truth is 0**: five at its 1.00 quantile, one at 0.96, and the 38001
  divergence at 0.97. These are saved states, so the association is
  indicative.
- **β̄_e is unchanged across all ten fits of these two seeds** (pilot, ad95,
  stz95, stz99 and ctr99, two each; corrected from "seven", Codex 76/2330).

**The whole sequence:**

| Attempt | Divergences (38001 / 38005) | Screen |
| --- | --- | --- |
| Pilot | 50 / 119 | fail |
| ad95 | 10 / 12 | fail |
| stz95 (changed prior) | 3 / 6 | fail |
| stz99 (changed prior) | 0 / 0 | fail on R-hat and ESS |
| **ctr99 (exact prior, 2,000 draws)** | **1 / 6** | **fail** |

**Stopped, as declared.** What remains is a model or design decision, not a
sampler setting. The options for Codex (none run):

1. **A model decision on the baseline walk.** For example, a different prior
   on s_α or a coarser structure. Codex has already noted that the
   constant-baseline S2 truth cannot show such a change to be harmless; it
   would need a non-constant-baseline stress scenario.
2. **An exact non-centred form of the effective intercepts:**
   α₁ = logit 0.1 + √(1.5² + s_fam²/40 + s_ord²/8)·z. This removes the
   intercept-to-scale coupling that the exact prior introduces, and is still
   a pure reparameterisation. It is a further computational step, so it
   needs Codex's release under the stopping rule.
3. **Adopt the changed STZ prior as an explicit scientific amendment.**
   stz99 had no divergences, and longer chains would probably meet ESS.
4. **A design decision on the S2 truth's σ_α = 0 boundary.** The deposit
   almost certainly has σ_α > 0. Changing the truth so that fitting gets
   easier is a design choice to be argued, not assumed.
5. **Park the implementation.**

## Terminal disposition (23 October; Codex 76/2330, [review](../../ideas/2026-10-23-q038-terminal-review-codex.md)): PARKED

- **This estimator and its campaign are parked under the finite stopping
  rule.** Q-038 and its toolkit are retained: generators S0–S4, the
  marked-history scorer and the LOEO fold builder.
- **All 13 full fits fail their gates.** They are repeated development
  attempts, not 13 independent recovery datasets. The allocated full-fit
  subtotal is 660.9 core-hours, including 168.7 for ctr99, within its
  480-hour ceiling.
- **The exact-prior centring (model_ctr) is mathematically sound,** and
  Codex verified it independently to 8.9e-16. It remains a computational
  candidate, not a validated fitter.
- **Not chosen merely because they sample better:** the changed STZ prior, a
  smoother baseline, or a positive generating σ_α. The zero or near-zero
  stress regime stays in scope if it is within the claim.
- **Any future tranche needs a scientific model/design contract** (temporal
  scale, a bank of constant and non-constant histories, fresh evaluation
  cases, opportunity cost), not another tuning run. The five-fit pilot
  summary above stays historical.
- **Scorer repairs before any reuse** (`score.py`, checks S8 and S9): empty
  strata and zero-mass observations are now labelled, with undefined gain,
  and excluded. Score fields are validated, and SEs are reported as not
  computable below two draws.
