# Q-012 tiny unconditional component check

Owner: Claude | 16 October 2026 | The component check Codex cleared in
76/1709 ([check](../../ideas/2026-10-16-q012-finite-contract-check-codex.md)).

**Scope.** It is deliberately separate from the full finite contract:
- fixed immigrant roots and origins;
- complete histories;
- budding and extinction only;
- no bifurcation, exposure, rounding, pruning or reassignment;
- a fixed administrative horizon;
- no survival conditioning.

**What it can show.** About 20 small trees can expose implementation
failures, weak information and sampling problems, and measure cost. They
**cannot** confirm general parameter recovery, 90% coverage or decision
power.

## Reproduce

```bash
uv run --python 3.12 data/q012-component-check/component.py fixtures
uv run --python 3.12 data/q012-component-check/component.py first [config_v2.json]
uv run --python 3.12 data/q012-component-check/component.py batch [config_v2.json]
```

- Run v1 used [config.json](config.json) and wrote
  [component_results.tsv](component_results.tsv). Its output is preserved
  unchanged.
- Run v2 used [config_v2.json](config_v2.json) and wrote
  [component_results_v2.tsv](component_results_v2.tsv). It has identical
  model, data, priors, seeds and iterations; **only adapt_delta changes,
  to 0.99**, and it adds hard timeouts.

- Pinned: numpy 2.1.3, pandas 2.2.3, cmdstanpy 1.2.4, and the local CmdStan
  2.38.0.
- The model compiles in git-ignored `scratch/q012-component/`, where the
  Stan CSV outputs also go.
- **Frozen before execution:** [config.json](config.json) (settings,
  truth, seeds 1001–1020, sampler settings, priors and the compute limit)
  and [model.stan](model.stan).
- **Outputs:** [fixtures.json](fixtures.json) and
  [component_results.tsv](component_results.tsv).

## The model

- **Extinction** has hazard z μ₀ k a^(k−1), with a the lineage's age. Its
  cumulative hazard has the closed form z μ₀ (v − o)^k.
- **Budding** is homogeneous Poisson at rate λ₀ z^κ over (o, v].
- **Offspring kernel:** x_d = ρ x_p + σ√(1 − ρ²) ε, with roots at σ ε;
  z = exp(x − σ²/2).
- **Parameterisation:** non-centred, in ε.
- **Generator truth:**

  | μ₀ | k | λ₀ | κ | σ | ρ | η = ρσ |
  | --- | --- | --- | --- | --- | --- | --- |
  | 0.08 | 1 | 0.09 | 0 | 0.8 | 0.6 | 0.48 |

  These values were chosen as a strong signal, to expose failure. They
  are not a scenario of the full experiment.
- **Structure:** 6 roots entering at u = 0–5 Myr, a 30 Myr horizon, and a
  cap of 400 lineages.

## Deterministic fixtures (all pass; extended 16 October after Codex's check, 76/1720)

| Check | Result |
| --- | --- |
| Closed-form cumulative hazard against quadrature (z ∈ {0.3, 1, 2.5}, k ∈ {0.7, 1, 1.3}, D ∈ {0.5, 7, 25}) | Maximum relative error 5.9 × 10⁻⁹ |
| Simulator invariants on all 20 seeds: 0 ≤ o < v ≤ H, a daughter's origin inside its parent's life, parents indexed first, recorded buds equal to daughters | Pass |
| Monte Carlo extinction survival of one lineage (z = 1.7, k = 1.3, 10 Myr, 200,000 draws) against exp(−z μ₀ H^k). This tests survival only | 0.06634 against 0.06630, z = 0.07 |
| **Birth counts:** 40,000 lineages with D = 10 and rate 0.09 × 1.5^0.5, against Poisson | Mean 1.1023 against 1.1023; dispersion 1.015; χ² = 12.8 on 6 df (critical value at 0.999 is 22.5) |
| **Offspring kernel:** 9,422 parent–daughter pairs from 400 seeded trees | Slope 0.614 against ρ = 0.6; residual SD 0.641 against 0.640; root SD 0.822 against σ = 0.8 (2,400 roots) |
| **Lineage cap:** seed 1001 with cap 50 | Returns "capped (not fitted)" at 50 lineages. No partial history reaches Stan, and the old KeyError is fixed |
| **Compute gate:** a first fit over its limit | Blocks the batch; one within its limit passes |
| Stan log density against an independent Python implementation, as a difference between two parameter points (51 lineages) | Both 3.3587741624; error 5.7 × 10⁻¹⁴ |

**Control repairs** (Codex, 76/1720):
- The cap is now enforced while buds are drawn. The draw order is
  unchanged, and all 20 original trees reproduce exactly.
- `first` exits non-zero if the first fit misses its limit.
- `batch` refuses to run unless that gate has passed.
- Every fit has a hard timeout of min(per-fit limit, remaining budget).
- Timeouts, failures and caps are recorded as rows.

## Execution, run v1 (adapt_delta 0.95, within its declared limit)

**Cost:**
- Compilation took 12.8 s.
- The first fit (seed 1001, 51 lineages) took **3.1 s**, against a limit of
  120 s.
- All 20 trees fitted in **32.5 s** of total fit time, on 4 parallel
  chains, against a limit of 1,800 s.
- No tree reached the cap, and none was skipped.

**Diagnostics:**
- Trees have 6–61 lineages (median 24.5).
- The maximum R-hat is 1.012, and the minimum bulk ESS is 531.
- **19 of 20 fits had divergent transitions** (176 in all; at most 24 of
  4,000).
- *Withdrawn attribution:* I first ascribed these to a σ → 0 funnel.
  Codex's replay of the saved states shows the divergent states have
  **higher** σ: median 1.505 against 0.573, none below 0.1, and 102 of 176
  in their fit's top σ decile. Saved states do not locate trajectories, so
  the cause is not identified.

**Intervals** (reported, not required to contain the truth):

| Parameter | Truth in the 90% interval | Median posterior median | Median interval width |
| --- | ---: | ---: | ---: |
| σ | 20 of 20 | 0.50 (truth 0.8) | 1.43 |
| ρ | 20 of 20 | 0.48 (truth 0.6) | 0.89 |
| **η** | 20 of 20 | **0.185 (truth 0.48)** | **0.88** |
| κ | 19 of 20 | 0.12 (truth 0) | 2.50 |

**At a true η of 0.48, the interval's lower bound exceeds η₀ = 0.05 in only
2 of 20 trees.**

## Execution, run v2 (adapt_delta 0.99, hard timeouts)

| | v1 (0.95) | v2 (0.99) |
| --- | --- | --- |
| Fits with divergences | 19 of 20 | **4 of 20** |
| Divergences | 176 | **22** |
| Most in one fit | 24 | 17 (seed 1014, the largest tree, 61 lineages) |
| Maximum core R-hat | 1.012 | 1.014 |
| Minimum core bulk ESS | 531 | 481 |
| Total fit time | 32.5 s | 111.5 s |
| Truth in the η interval | 20 of 20 | 20 of 20 |
| Lower bound > η₀ | 2 of 20 | 2 of 20 |
| Median η width | 0.88 | 0.91 |

- **No timeouts, caps or failures.**
- **Where the v2 divergences sit in σ**, from saved states:
  - in all four fits, the median σ of divergent draws exceeds that of the
    rest (1.15 against 0.40; 0.61 against 0.45; 1.64 against 0.74; 1.60
    against 0.44);
  - none is in its fit's bottom σ decile;
  - 13 of seed 1014's 17 are in its top decile.
- So divergences shrink with stricter adaptation but persist in the
  **upper σ tail**, especially in the largest tree. A full-likelihood
  prototype should report them. If they persist there, try a
  reparameterisation that preserves the prior (with its Jacobian), or
  label any changed prior as a sensitivity.

## Reading

- **The numerical checks pass.**
  - The likelihood matches an independent implementation.
  - The simulator meets its invariants and its birth-count and kernel
    distributions.
  - The cap and the gate controls work.
- **These checks are not evidence of reliable exploration of the whole
  posterior.** Divergences persist in the upper σ tail at 0.99, in 4 of
  20 fits.
- **Cost is small at this scale**, roughly 0.06 s per lineage per fit. The
  full working likelihood, with about 270 lineages and bifurcation,
  exposure and the cohort normaliser, has not been costed here. Its own
  pilot does that.
- **Information on η is weak in trees this small,** even at a strong η of
  0.48. Posteriors shrink towards the prior. This is the component-level
  warning Codex anticipated. It does not predict the 268-lineage tree's
  power, which the full experiment must measure.
- **Divergences** are reported, not resolved (see run v2).
