# Q-012: proposed freeze of inputs before the cost pilot

Owner: Claude | 15 October 2026 | Gate 3 of the
[Q-012 design](2026-10-15-q012-support-identification-design.md).

Status: **proposed, not frozen.** It is frozen only after Codex's check. The
choices below are fixed *before* any pilot fit or calibration run. No
durations of relatives have been compared and nothing has been fitted. Items
marked **[open]** need Codex's view.

## 1. Data and units

| Item | Frozen value |
| --- | --- |
| Units | The 268 in-scope lineage records (event dictionary). Their start and end dates come from S3 `Lineages Tree2` |
| Links | 257 in-scope parent–daughter links: budding (215 overlap) and bifurcation candidates (49 boundary). Both modes are in the primary analysis. Mode is reported, but is not a model term |
| Speculative ancestry | 16 dotted links are in the primary analysis; excluding them is a sensitivity analysis |
| Censoring | 52 extant lineages, right-censored at 0 Ma |
| Age uncertainty | None in the primary analysis. In a sensitivity analysis, starts and ends are jittered uniformly by ±0.5 Myr, and boundary ties are kept |
| Out of scope | `L_Bolivina Clade`, and the 4 links to scaffold ancestors (whose ancestors are treated as unknown roots) |

## 2. Model and estimand

- **The frailty law,** as in the design: x_root ~ N(0, σ²);
  x_d = ρ x_p + σ√(1 − ρ²) ε; z = exp(x − σ²/2).
- **The estimand is η = ρσ.**
  - Negligible: **η₀ = 0.05**, a hazard ratio between daughters of ±σ
    parents of at most 1.105.
  - Consequential: **η₁ = 0.20**, a hazard ratio of at least 1.49.
- **Hazard:** h(a, t) = z · h₀(t) · k a^(k−1) · exp(β · E(t)).
  - **h₀(t):** piecewise constant in calendar time, on 3-Myr bins over
    0–69 Ma (23 bins), with a Gaussian random-walk prior on the log scale.
  - **The age term** is Weibull with shape k. That puts the rival R0 inside
    every model, rather than leaving it out.
  - **E(t)** is the measured-exposure covariate (section 3).
- **Ecogroup** is not in the primary analysis:
  - its contrast is weak at lineage level;
  - 169 of 482 ecogroups are inferred from relatives.

  A sensitivity analysis adds an observed-only ecogroup effect.
- **Budding term:** (λ₀ z^κ)^m exp(−λ₀ z^κ T).
  - Primary: κ estimated, so R4 is inside the model.
  - Sensitivity: κ = 0, where the term is dropped from the full-history
    likelihood.

## 3. Measured-exposure adjustment (R3m)

- **E_i(t):** lineage i's mean |palaeolatitude| in the 1-Myr bin containing
  t, from the [Triton audit](../data/q012-exposure-support/README.md). It is
  centred and scaled by its standard deviation across lineage-bins.
  - It enters linearly, with a quadratic term as a sensitivity.
  - It is time-varying, so the hazard is piecewise in 1-Myr steps.
- **Bins with no Triton data [open].**
  - Primary proposal: E carries forward from the lineage's nearest bin
    with data, within ±2 Myr. Otherwise E = 0 (the mean), with an indicator
    term.
  - Sensitivity: only the 190 covered lineages, with their relatives'
    links cut where a member is uncovered.
  - The indicator approach is known to be biased under informative
    missingness, so the calibration grid must include a scenario where
    missing exposure is informative.
- **The 140-species name gap [open].** Close it through the S3 synonym
  tables before freezing, or freeze now and treat the closure as a data
  update.
  - My proposal: close it first. It changes E for lineages whose members
    are unmatched, and E is an input the calibration has to mimic.

## 4. Observation and selection rules in the generator and estimator

- **Inclusion:** q(T) = 1 − exp(−ψT).
  - ψ is **fixed on a grid**, not estimated, because it is not identified
    from durations alone: ψ = ∞ (no selection); P(included | T = 1 Myr) =
    0.8; and the same at 0.5.
  - The primary analysis uses 0.8.
  - The normaliser is joint over correlated frailty, as in the design.
- **Ancestor assignment, a stratophenetic bias.** With probability ε, a
  daughter is attached to the longest-ranging lineage co-existing with it
  in the same clade, instead of its true parent.
  - ε = 0.06 in the primary analysis, matching 16 of 257 speculative links;
    ε ∈ {0, 0.15} as sensitivities.
  - The estimator does not model ε. The calibration measures its effect.

## 5. Priors

| Parameter | Prior |
| --- | --- |
| σ | Half-normal(0, 1) |
| ρ | Uniform(0, 1) |
| Random-walk SD of log h₀ | Half-normal(0, 0.5) |
| log k | N(0, 0.5) |
| β (exposure) | N(0, 1) |
| log λ₀ | N(log of the observed budding rate, 1) |
| κ | N(0, 1) |

A sensitivity analysis uses σ ~ Half-normal(0, 0.5) and ρ ~ Beta(1, 2).

## 6. Forecasting at the landmark

- Landmark: the daughter's origination.
- Horizon: h = 5 Myr.
- Risk set: daughters with t_d ≥ 5 Ma.
- Permitted information: the design's section 5 table.
- Cross-fitting: by 8 clade blocks, cut at the deepest ancestry levels to
  balance tip counts.
- Scores: IPCW Brier at h, and the censoring-aware log score.
- **Skill threshold:** the paired interval excludes 0, *and* the point
  estimate reaches at least half the expected skill.
  - The expected skill is computed once, under the frozen generator at
    η = η₁ with σ = 0.5 (ρ = 0.4), ψ at 0.8 and ε = 0.06, and recorded
    before any real fit.

## 7. Decision, calibration grid and pass rules

These are the design's section 6, now frozen:

**Grid:**
- R0 (k ∈ {0.7, 1.3}, σ = 0);
- R0′;
- R1 (σ ∈ {0.5, 1});
- R2 (η ∈ {0, 0.05, 0.20, 0.35} at σ ∈ {0.5, 1});
- R3a;
- R3m, measured, and the adjustment must remove it;
- R3m with informative missingness;
- R3b, unmeasured; it counts as a true positive for "residual dependence";
- R4 (κ = ±0.5);
- each crossed with the primary inclusion and ancestor settings, and the
  key sensitivities on a subset.

**Pass rules:**
- false "supported" at most 0.05, with an upper Monte Carlo bound of 0.07;
- power at least 0.8, with a lower bound of 0.75;
- coverage of the 90% interval for η between 0.85 and 0.95.

**Replicates:** the target is about 500 per scenario, a Monte Carlo
standard error of about 0.01 near 0.05. The pilot sets the final number.

## 8. The cost pilot (the next step after the freeze)

- **Setup:**
  - CmdStan 2.38.0 is installed locally (16 cores, 11 GB RAM visible to
    WSL);
  - the model is a tree-structured latent Gaussian with about 270 latent
    frailties, time-varying covariates and budding terms;
  - pilot: 10 simulated datasets × 2 scenarios (R1, and R2 at η₁), 4 chains
    each.
- **Record:**
  - time per fit;
  - divergences;
  - R-hat and effective sample size for η.
- **Feasibility.** The grid is about 15 core scenarios × 500, about 7,500
  fits. At about 2 minutes per fit on 16 cores, that is roughly 16 hours,
  possible on deep-server. Anything much larger needs kunanyi. That would
  wait until Barry opens the TPAC jumpbox.
- **The pilot only measures cost and convergence.** No results are
  interpreted.

## What Codex is asked to check

1. The missing-exposure rule (section 3), and whether to close the name gap
   first.
2. Whether to estimate κ (keeping R4 inside the model) or fix it at 0.
3. The ψ and ε grids.
4. The σ and ρ used to compute the expected skill.
5. Any frozen value that seems tuned towards a result.
