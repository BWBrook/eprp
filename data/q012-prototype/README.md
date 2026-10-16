# Q-012 timed one-dataset prototype of the full working likelihood

Owner: Claude | 16 October 2026 | The next stage cleared by Codex once the
component checks passed (76/1720). It implements the
[finite contract](../../literature/2026-10-16-q012-finite-contract.md),
including Amendment 1.

**It does two things only:**
- measures the cost of one fit at a realistic tree size;
- checks the cohort normaliser and the full target.

It does **not** estimate power, coverage or parameter recovery. Nothing
is fitted to the real data.

## Reproduce

```bash
uv run --python 3.12 data/q012-prototype/prototype.py checks
uv run --python 3.12 data/q012-prototype/prototype.py fit
```

- Pinned: numpy 2.1.3, pandas 2.2.3, cmdstanpy 1.2.4, and local CmdStan
  2.38.0.
- Compilation and Stan output go to git-ignored `scratch/q012-prototype/`.
- **Frozen first:** [config.json](config.json) and
  [model.stan](model.stan). config.json also records one declared deviation
  (below).
- **Outputs:** [checks.json](checks.json) and
  [fit_result.json](fit_result.json).

## What is implemented

| Part | Implementation |
| --- | --- |
| Generator | Primary reference: σ 0.5, ρ 0.4 (η 0.2); κ = κ_b = 0; β = 0; k = 1 |
| Rates | Baseline from the data's marginal extinction rates by 3-Myr bin, with a declared floor of 0.065 for the four bins older than 63 Ma; λ₀ 0.0708; b₀ 0.0082 |
| Exposure | AR(1) on 1-Myr bins (φ 0.8), inherited at speciation (ρ_E 0.9) |
| Roots | The 11 roots enter at their observed origins |
| Boundary cohort | Forced design: five roots plus a daughter at 69.81 Ma, all six conditioned on surviving to c = 8.95 (66.05 Ma), by rejection |
| Termination | Piecewise-exponential extinction and bifurcation; bifurcation produces 2 kernel daughters |
| Budding | After entry only |
| Observation | Thinning q(1 Myr) = 0.8 on observed duration; compatible-parent pruning; acyclic ε = 0.06 reassignment; rounding precedence; end labels from recorded daughters only; data-matched Markov exposure observation; past-only lag |
| Working likelihood | Calendar-time baseline as a 25-bin random walk; Weibull age, never reset at entry; extinction and bifurcation terminal factors; budding after entry; time-varying lagged E with a missing indicator; cohort survival before entry; normaliser by 24-node Gauss–Hermite quadrature over the retained graph's components |

## Checks (all pass)

| Check | Frozen seed 20261017 (62 recorded) | Fit seed 20261060 (264 recorded) |
| --- | --- | --- |
| Log normaliser: quadrature against Monte Carlo (10⁶ draws), two parameter points | z = −1.09 and 0.10 | z = −1.09 and 0.10 (the same cohort) |
| Stan target against an independent Python target, as a difference between two points | Error 5.7 × 10⁻¹⁴ | Error 7.7 × 10⁻¹² (3,202 hazard segments) |

## A declared deviation, and a finding for the full experiment

**The frozen seed gave a tree too small to measure cost.**
- It produced only 62 recorded lineages, against 268 in the real tree.
- Over 300 seeds, the reference generator gives a **median of 94 recorded
  lineages**:

  | | 5th percentile | Median | 95th percentile |
  | --- | ---: | ---: | ---: |
  | Recorded lineages | 35 | 94 | 241 |

  Only 4.3% of seeds reach 268.
- **Rates matched to the data's marginal totals do not reproduce its
  realised tree size.** This is the selection and branching effect Codex
  warned about.
- **For costing only,** the fit uses the first seed from 20261017 upward
  whose recorded tree has 240–300 lineages: seed 20261060, with 264
  recorded, after skipping 43 seeds. The rule was declared before the fit.
  No inference is drawn from this fit.

**For the full experiment**, the generator's tree size needs a declared
calibration. Two options for Codex's view:
- calibrate λ₀ by simulation, so that the median recorded size matches
  268;
- condition on the recorded size falling in a declared band.

Either way it is stated as a design choice, not left implicit.

## The timed fit (seed 20261060; 264 recorded lineages; 4 chains in parallel, 1,000 + 1,000 iterations, adapt_delta 0.99, hard limit 1,200 s)

| Quantity | Value |
| --- | --- |
| Wall time | **792.8 s** (13.2 min), inside the limit |
| Cost | About **53 core-minutes** per fit |
| Divergences | 4 of 4,000 |
| Tree-depth hits | 0 |
| Maximum R-hat, core parameters and all parameters | **1.037** |
| Minimum bulk ESS, core and all | **173** |

**These diagnostics are not adequate for decision-grade inference.** R-hat
is above 1.01 and ESS is below 400, so longer chains or a reparameterisation
would be needed.

**90% intervals, with the truth.** This is one dataset, so it shows
behaviour, not recovery:

| Parameter | 5% | Median | 95% | Truth |
| --- | ---: | ---: | ---: | ---: |
| σ | 0.45 | 1.00 | 1.81 | 0.5 |
| ρ | 0.03 | 0.20 | 0.42 | 0.4 |
| **η** | **0.026** | **0.189** | **0.50** | **0.2** |
| κ | −1.12 | −0.39 | −0.13 | 0 |
| κ_b | −0.59 | 0.22 | 1.07 | 0 |
| β | −0.19 | 0.00 | 0.21 | 0 |
| log k | −0.05 | 0.17 | 0.50 | 0 |
| log λ₀ | −3.41 | −3.09 | −2.82 | −2.65 |
| log b₀ | −6.32 | −5.41 | −4.62 | −4.80 |

**Observations**, labelled as observations from one dataset only:
- σ and ρ trade off: σ comes out high and ρ low. η = ρσ is located better
  than either.
- **The intervals for λ₀ and κ exclude the truth.** That is the direction
  the complete-ascertainment working model should be biased under
  thinning:
  - unrecorded short-lived daughters lower the recorded budding rate;
  - because frailty is inherited, high-frailty parents lose more recorded
    daughters, which pushes κ below 0.

  Whether η keeps its decision properties under that misspecification is
  exactly what the finite experiment tests. One fit cannot tell.

## Cost for the full experiment

The finite contract's grid is about 15 core scenarios × 500 replicates,
about **7,500 fits**.

| Basis | Total |
| --- | --- |
| At the measured 53 core-minutes per fit | About **6,600 core-hours** |
| With chains long enough for ESS ≥ 400 (roughly 2–3× more) | About 13,000–20,000 core-hours |

- **Not feasible on this laptop.**
- On kunanyi's permitted 48 jobs × 28 CPUs (1,344 cores): about 5 hours of
  wall time, or 10–15 hours with longer chains. kunanyi needs Barry to
  open the TPAC jumpbox first.
- deep-server's capacity for this has not been checked here.

**Ways to bring the cost down, before any grid:**
1. **Model efficiency.**
   - Vectorise the 3,202-segment hazard sum.
   - Precompute the segment structure.
   - Use within-chain parallelism (`reduce_sum`).

   Likely several-fold.
2. **A smaller grid.** Fewer replicates on scenarios far from the decision
   boundaries, while keeping the Monte Carlo precision the pass rules need.
3. **A cheaper calibration estimator** (Laplace or variational) for the
   grid, with full MCMC spot checks on a declared subset. That would be
   labelled as a change of estimator.

**The generator's size calibration** (above) has to be settled before any
grid as well.
