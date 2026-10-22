# Q-038 primary probe: implementation and the five-dataset S2 pilot

Contract: [v3](../q038-predictor-contract/contract.md), section D. Cleared for
implementation by Codex in 76/2195. This pilot measures **runtime and
convergence only**: five datasets cannot pass any recovery gate. The larger
campaign and any empirical fit remain held.

| File | Role |
| --- | --- |
| [core.py](core.py) | The one feature and scaling convention (fixed affine transforms from [deposit_constants.json](deposit_constants.json)), the generator, the reference CJS likelihood, the fold builder, Stan data, and the forecast |
| [model.stan](model.stan) | The ε = 1 CJS with Binomial(E_t, 1 − e^{−θ}) reference-count emissions, conditional on the first record and its count; `reduce_sum` over components |
| [checks.py](checks.py) | Implementation checks C1–C5, against the actual code; [checks.json](checks.json) |
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

## Benchmark and execution plan (22 October 2026, deep-server)

**Benchmark** ([pilot/bench_38001.json](pilot/bench_38001.json)): dataset
38001, with 2,777 components and 126,305 rows.
- **Run:** 100 warmup and 100 sampling iterations, 4 chains × 12 threads.
  It took **1,334 s, about 6.7 s per iteration**, with no divergences and
  no tree-depth hits. R-hat was 1.04 and the minimum bulk ESS 83, as
  expected from so short a run.
- **β̄_e:** Rhynchonellata 0.73 ± 0.16 and Bivalvia 0.46 ± 0.16, with
  truth 0.5 inside both 95% intervals. The posterior SD of 0.16 against a
  prior SD of 1 shows real contraction.

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
