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
