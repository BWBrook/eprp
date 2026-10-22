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
