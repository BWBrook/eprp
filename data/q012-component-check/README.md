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
uv run --python 3.12 data/q012-component-check/component.py first
uv run --python 3.12 data/q012-component-check/component.py batch
```

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

## Deterministic fixtures (all pass)

| Check | Result |
| --- | --- |
| Closed-form cumulative hazard against quadrature (z ∈ {0.3, 1, 2.5}, k ∈ {0.7, 1, 1.3}, D ∈ {0.5, 7, 25}) | Maximum relative error 5.9 × 10⁻⁹ |
| Simulator invariants on all 20 seeds: 0 ≤ o < v ≤ H, a daughter's origin inside its parent's life, parents indexed first, recorded buds equal to daughters | Pass |
| Monte Carlo survival of one lineage (z = 1.7, k = 1.3, 10 Myr, 200,000 draws) against exp(−z μ₀ H^k) | 0.06634 against 0.06630, z = 0.07 |
| Stan log density against an independent Python implementation, as a difference between two parameter points (51 lineages) | Both 3.3587741624; error 5.7 × 10⁻¹⁴ |

## Execution (within the declared compute limit)

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
- **19 of 20 fits had divergent transitions**, at most 24 of 4,000. These
  come from the σ → 0 funnel, where ρ is unidentified.

**Intervals** (reported, not required to contain the truth):

| Parameter | Truth in the 90% interval | Median posterior median | Median interval width |
| --- | ---: | ---: | ---: |
| σ | 20 of 20 | 0.50 (truth 0.8) | 1.43 |
| ρ | 20 of 20 | 0.48 (truth 0.6) | 0.89 |
| **η** | 20 of 20 | **0.185 (truth 0.48)** | **0.88** |
| κ | 19 of 20 | 0.12 (truth 0) | 2.50 |

**At a true η of 0.48, the interval's lower bound exceeds η₀ = 0.05 in only
2 of 20 trees.**

## Reading

- **The implementation works.** The likelihood matches an independent
  implementation, the simulator meets its invariants, and sampling is
  stable apart from the funnel.
- **Cost is small at this scale**, roughly 0.06 s per lineage per fit. The
  full working likelihood, with about 270 lineages and bifurcation,
  exposure and the cohort normaliser, has not been costed here. Its own
  pilot does that.
- **Information on η is weak in trees this small,** even at a strong η of
  0.48. Posteriors shrink towards the prior. This is the component-level
  warning Codex anticipated. It does not predict the 268-lineage tree's
  power, which the full experiment must measure.
- **The funnel needs attention before the full pilot.** One option is to
  sample (η, σ) or (σ, ρ) on a scale that separates the σ → 0 region.
  Another is a stricter adapt_delta, with divergences reported either way.
  It is recorded as an implementation item, not fixed here.
