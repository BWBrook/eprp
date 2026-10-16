# Q-012: finite generator, working likelihood and prediction contract

Owner: Claude | 16 October 2026 | The single defined object Codex asked for
(76/1699,
[ruling](../ideas/2026-10-16-b004-analytic-close-and-q012-addendum-check-codex.md)).
It supersedes the [freeze proposal](2026-10-15-q012-freeze-proposal.md) and
the [addendum](2026-10-16-q012-events-exposure-addendum.md) where they
differ.

**Status: defined, for Codex's single check.** Nothing has been simulated or
fitted, and no outcomes of relatives have been compared.

**What kind of exercise this is.** It is a **finite misspecification
experiment**.
- The working estimator assumes complete ascertainment.
- The generator includes declared incomplete-observation scenarios.
- The truth is always the generator's η = ρσ.
- A pass establishes operating characteristics in the tested scenarios. It
  does not establish empirical robustness, or identification under
  arbitrary missing histories.

## 1. Data the estimator receives

These come from the
[event dictionary](../data/q012-event-dictionary/README.md) and the
[exposure audit](../data/q012-exposure-support/README.md).

**Lineages and links:**
- 268 lineages: start and end in Ma, and an end label:
  - extinction (191);
  - present (52), censored at a fixed 0 Ma;
  - bifurcation candidate (24);
  - single coincident daughter (1).
- 257 links: 208 budding and 49 bifurcation-candidate.
- 11 roots.

**Exposure:** the lagged, past-only `used_value` for each lineage-bin,
with a missingness indicator.

**Not given to the estimator:**
- latent frailties;
- pruned lineages;
- the true parents of reassigned links;
- anything a compiler would not have recorded.

**Chronology rules**, with ages in Ma:
- end ≤ start, and duration > 0;
- parent start ≥ daughter start;
- for budding, parent end < daughter start;
- bifurcation candidates keep parent end = daughter starts.
- **Four compiled start ties** (`T321`, `L_Globoturborotalita occlusa`,
  `N106-T107`, `L_Neogloboquadrina incompta`, each budding at its own start
  date) follow a **joint-age rule**: the daughter starts at the parent's
  origination, which is a bud at parent age 0, and the tie is preserved.
- **The ±0.5 Myr jitter is a declared sensitivity distribution,** not a
  chronology model. It uses rejection sampling under all the rules above.
  The ties are jittered jointly, and present-day censors stay at 0.

## 2. The generator (one declared stochastic history per replicate)

**Roots and origins.**
- The 11 roots enter at their observed origin ages (72.44 to 17.95 Ma),
  conditional on those times. They are immigrant lineages from outside
  the scope.
- Root log frailty is drawn independently from N(0, σ²).
  - This is an **assumption**. Seven roots share the excluded
    `L_Bolivina Clade` ancestor.
  - Scenario R-root: those seven share one latent ancestor frailty, with
    each root at ρ from it.

**The left-boundary cohort, a declared conditional experiment.**
- The cut is τ = 66.05 Ma: the K–Pg within compiled-date precision. Several
  lineages start at 66.02–66.04 Ma, after τ.
- **The cohort is the six recorded lineages alive at τ:**
  - five roots (72.44, 71.12, 70.14, 70.14 and 69.46 Ma);
  - `N256-N2-N198-T67`, budded from the root `N1-N3` at 69.81 Ma. It
    survives to 66.02 Ma and is the ancestor of five lineages starting at
    66.02–66.04 Ma.
- **The generator conditions on that cohort's structure.**
  - The cohort's frailties are drawn from the prior: independent roots,
    with N256's frailty drawn through the kernel from `N1-N3`.
  - Draws are **rejected unless all six survive to τ**, given their observed
    origins. That produces the survival-tilted law.
  - The budding at 69.81 Ma is taken as observed.
  - Other pre-τ history is not simulated and is not observed.
- **After τ**, everything is simulated forward without conditioning.

**Processes along each lineage** (latent x, with z = exp(x − σ²/2)):

| Process | Rate | Effect |
| --- | --- | --- |
| Extinction | μ(a, t) = z h₀(t) k a^{k−1} exp(β E(t) + U(t)) | Terminates |
| Bifurcation | b₀ z^{κ_b} | Terminates and produces 2 daughters |
| Budding | λ₀ z^κ | The parent persists and 1 daughter is produced |

- **h₀(t) is piecewise constant on 25 bins of 3 Myr, from 0 to 75 Ma.**
  - It is set from the data's **marginal** extinction rate by bin
    (extinctions over lineage-Myr in each bin). Pairs of relatives are
    never used.
  - Overall marginal rates: extinction 0.065, bifurcation 0.0082 and
    budding 0.0708 per lineage-Myr.
  - λ₀ and b₀ are scaled from the same totals, divided by E[z^κ], so the
    marginal event rates match.
- **Offspring kernel:** each daughter has
  x_d = ρ x_p + σ√(1 − ρ²) ε. Sisters are conditionally independent given
  the parent.
- **Exposure E(t):**
  - within a lineage, an AR(1) process on 1-Myr bins;
  - inherited at speciation with correlation ρ_E;
  - with marginal mean and SD matched to the data (26.26°, 13.38°).
- **U(t)** is the *unmeasured* clade-tied field (R3b): built the same way,
  never observed, with variance σ_U². It is zero unless the scenario sets
  it.
- **Horizon:** 0 Ma, which is administrative censoring.
- **No conditioning on survival, lineage counts or topology,** beyond the
  root rules above.
- **A computational cap** of 3,000 lineages. A replicate that hits it is
  counted and reported as a cap event. It is never silently redrawn, and it
  is excluded from the decision summaries only with that count shown.

## 3. Observation process: what a compiler would record

These steps are applied in order to each latent history.

1. **Inclusion (thinning).** A lineage is recorded with probability
   q(T_obs) = 1 − exp(−ψ T_obs), where T_obs is its duration *observed by
   the horizon*: origin to end, or origin to 0 Ma if extant. Under ψ = ∞,
   every lineage is recorded.
2. **Pruning.**
   - An unrecorded lineage is removed.
   - Its recorded descendants are reattached to its nearest recorded
     ancestor. If there is none, they become roots.
   - A bifurcation with one unrecorded daughter appears as a **single
     coincident daughter**.
   - A link's label (budding or boundary) is recomputed from the recorded
     dates.
3. **Ancestor reassignment.** With probability ε, a recorded daughter is
   reattached to the longest-ranging recorded lineage co-existing with it in
   the same root clade. The true parent is not reported.
4. **Dates** are rounded to 0.01 Myr. End labels are assigned by the same
   0.005 Myr rule as the data, so rounding ties arise as they do in the
   source.
5. **Exposure observation.**
   - A lineage-bin's mean is observed with probability p_obs = 0.667, the
     empirical share of non-missing used values. In the
     informative-missingness scenario, p_obs depends on E or on z.
   - The same past-only lag rule produces `used_value`.

## 4. The working likelihood (complete ascertainment)

With log frailties x on the recorded tree (the observed links), the
likelihood is

L = ∫ p(x | σ, ρ) ∏_i [ exp(−∫_{t_i}^{T_i} (μ_i + b_i) dt) μ_i(T_i)^{I_ext} b_i(T_i)^{I_bif}
     × (λ₀ z_i^κ)^{m_i} exp(−λ₀ z_i^κ D_i) ] / π dx

**Terms:**
- **D_i** is the observed duration, and m_i the recorded buds.
- **Present censors** have neither terminal multiplier.
- **The single coincident daughter** is primarily treated as **censored**,
  with neither multiplier, which keeps the ambiguity.
  - Sensitivity: extinction.
  - Sensitivity: a one-descendant bifurcation.
- **Bifurcation candidates** take the b multiplier. Their two daughters
  attach through the kernel.
- **Roots:** x ~ N(0, σ²), independently, with the R-root scenario as a
  sensitivity.
- **The τ cohort** (the six lineages above): a single joint normaliser
  π = ∫ p(x_cohort) ∏_{i ∈ cohort} S_i(τ | x_i) dx.
  - It factorises into four one-dimensional root integrals and one
    two-dimensional integral for `N1-N3` with `N256`.
  - Integrals start at each lineage's origin, and events are counted from
    τ.
  - The 69.81 Ma bud is a conditioned design event.
- **Exposure:** β · E_used(t) + γ · 1[E missing] in the log hazard.
- **Not modelled:** ψ, ε, U and the pruning. These are the misspecifications
  under test.

**Priors** are as in the freeze proposal, plus:
- log b₀ ~ N(log 0.0082, 1);
- κ_b ~ N(0, 1);
- γ ~ N(0, 1).

**Estimand:** η = ρσ.
- Working values: η₀ = 0.05 and η₁ = 0.20.
- Reporting wording: "residual phylogenetic dependence after adjustment for
  measured exposure".

## 5. Retrospective cross-clade prediction (secondary)

| Element | Definition |
| --- | --- |
| Landmark | Daughter origination t_d |
| Target | **Extinction cumulative incidence within 5 Myr**: Y_d = 1 if the daughter goes extinct before t_d − 5 Ma *and* before any bifurcation. Bifurcation within 5 Myr gives Y_d = 0, as a competing event |
| Risk set | Daughters with t_d ≥ 5 Ma; the single coincident daughter is excluded |
| Permitted information at t_d | The parent's age at t_d, its recorded buds before t_d, and its last used E before t_d; older sisters' status and ages at t_d; calendar time. The daughter's own E is unknown |
| Future exposure rule | **Persistence:** over the 5 Myr, the daughter's E is set to the parent's last used E. Sensitivity: β · E replaced by its expectation over the empirical E distribution |
| Without relatives | The daughter's frailty comes from the marginal N(0, σ²) and E from the population mean, all else equal |
| Parameters | Cross-fitted: fitted on the other 7 clade blocks, using their full histories |
| Scores | Brier score on Y_d, and log score, paired with and without relatives |
| Reference gain | Expected paired Brier skill under the generator at η₁ (σ = 0.5, ρ = 0.4) with the primary ψ and ε. **It must be positive**; otherwise the prediction arm is dropped as non-informative |
| Skill threshold | The paired interval excludes 0, and the point estimate is at least half the reference gain |

## 6. The finite experiment

**Grid:**

| Scenario | Settings |
| --- | --- |
| R0 | k ∈ {0.7, 1.3}, σ = 0 |
| R0′ | Inherited age offset |
| R1 | σ ∈ {0.5, 1}, ρ = 0 |
| R2 | η ∈ {0, 0.05, 0.20, 0.35} at σ ∈ {0.5, 1} |
| R3m | Measured E affects hazard, with ρ_E ∈ {0.5, 0.9} |
| R3m-informative | Missing E informative |
| R3b | σ_U > 0, unmeasured |
| R4 | κ = ±0.5, and κ_b = ±0.5 |
| R-root | Correlated roots |

- Each is crossed with ψ ∈ {∞, 0.8 at 1 Myr, 0.5 at 1 Myr} and ε ∈ {0,
  0.06, 0.15}. These are stress settings, and the full cross runs on a
  declared subset.
- **Pass rules** (against the generator's η):
  - false "supported" at most 0.05, with an upper Monte Carlo bound of at
    most 0.07, under R0, R0′, R1, R3m, R3m-informative, R2 at η ≤ η₀, R4 and
    R-root;
  - power at least 0.8 with a lower bound of at least 0.75, under R2 at η₁
    and R1;
  - coverage of the 90% interval between 0.85 and 0.95.
- **R3b counts as a true positive** for "residual dependence".
- **σ = 0 is labelled non-identifying for ρ.**

## 7. Not launched by this contract

- **After Codex's check:** a *tiny component check*:
  - complete history, ψ = ∞, ε = 0;
  - budding only, with no bifurcation and no exposure;
  - about 20 small trees.

  It confirms that the working likelihood recovers σ, ρ and η, and measures
  the cost per fit with CmdStan 2.38.0. It is followed by a measured-cost
  pilot of the full working likelihood.
- The full grid and the empirical fit come only after those. Each needs its
  own go-ahead.
