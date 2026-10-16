# Q-012: finite generator, working likelihood and prediction contract

Owner: Claude | 16 October 2026 | The single defined object Codex asked for
(76/1699,
[ruling](../ideas/2026-10-16-b004-analytic-close-and-q012-addendum-check-codex.md)).
It supersedes the [freeze proposal](2026-10-15-q012-freeze-proposal.md) and
the [addendum](2026-10-16-q012-events-exposure-addendum.md) where they
differ.

**Amendment 1 (section 8),** after Codex's check (76/1709), supersedes
sections 2–6 wherever they differ. Execution evidence from the separate
component check is in
[data/q012-component-check](../data/q012-component-check/README.md).

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
   - *(Superseded by §8.2: 0.667 is lagged availability, not the raw
     probability.)* A lineage-bin's mean is observed with probability
     p_obs = 0.667, the
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
| Without relatives | *(Superseded by §8.3.)* The daughter's frailty comes from the marginal N(0, σ²) and E from the population mean, all else equal |
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
  - *(Superseded by §8.4: R1 is not a positive-support alternative.)*
    Power at least 0.8 with a lower bound of at least 0.75, under R2 at η₁
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

## 8. Amendment 1 (16 October 2026), after Codex's check (76/1709)

All four repair groups are accepted. This section supersedes the earlier
text wherever they differ.

### 8.1 The cohort likelihood matches the generator

**The design claim is a forced-design cohort.** It consists of:
- five designated roots;
- `N256-N2-N198-T67`, introduced at the **fixed design time 69.81 Ma**,
  with its frailty drawn through the kernel from `N1-N3`.

All six are conditioned on avoiding termination (μ + b) until the
boundary. This is not a natural bud conditioned on being observed, and not
a full pre-boundary branching process.

**Likelihood (Codex's forward-time form, adopted).**
- Definitions:
  - u = 75 − t_Ma, with boundary c = 75 − 66.05 = 8.95;
  - original origin o_i, observed end or censor v_i, and entry
    r_i = max(o_i, c);
  - age a_i(u) = u − o_i, which is never reset at entry.
- The expression:

  S_i(c | x_i) = exp[−∫_{o_i}^{c} (μ_i + b_i) du]
  π_θ = ∫ p_θ(x_C) ∏_{i∈C} S_i(c | x_i) dx_C
  L_θ = (1/π_θ) ∫ p_θ(x_tree) ∏_{i∈C} S_i(c | x_i) ∏_{i∈tree} { exp[−∫_{r_i}^{v_i}(μ_i + b_i) du]
        μ_i(v_i)^{I_ext} b_i(v_i)^{I_bif} (λ₀ z_i^κ)^{m_i⁺} exp[−λ₀ z_i^κ (v_i − r_i)] } dx_tree

- **m_i⁺ counts buds after entry only.** Budding before entry is
  integrated out. Survival from termination before entry is kept.
- **Exposure before the boundary** is unavailable, because Triton starts at
  66 Ma. Both the generator's observation map and the likelihood therefore
  carry the missing indicator there. In R3m, the generator's true pre-τ E
  still acts on the hazard, which is an allowed misspecification.
- **The working cohort under thinning** is defined from recorded data only:
  - recorded lineages with origin older than τ and end younger than τ;
  - a recorded parent–daughter pair within it, with the daughter's origin
    before τ, keeps the fixed design bud.

  π is computed over that working cohort. No latent six-lineage
  information is used. If a designated lineage is unrecorded, its recorded
  descendants follow the pruning rule (§8.2).
- **R-root is a generator-only stress scenario.** The fitted root law stays
  independent.
- **The normaliser's factors come from the retained working graph**
  (corrected 16 October).
  - π factorises over the connected components of the working cohort's
    recorded ancestry. Each component's dimension is its number of cohort
    lineages.
  - Four one-dimensional factors and one two-dimensional factor is only the
    intact reference cohort. Dropping N256, for example, leaves five
    one-dimensional factors.
  - Nothing is hard-coded to the original six.

### 8.2 The observation map is defined for every history

**Compatible parents.**
- After pruning, a recorded descendant attaches to its nearest recorded
  ancestor that is **alive at the descendant's origin**: in Ma, ancestor
  origin ≥ descendant origin ≥ ancestor end. Strict inequality gives a
  budding label; equality gives a boundary label.
- If there is none, the descendant becomes a **new observed root**, and
  each replicate reports its loss of ancestry.
- This handles Codex's A–B–D example: D becomes a root.

**Reassignment (ε).**
- Candidates are recorded lineages alive at the daughter's origin, in the
  same recorded root clade, excluding the daughter itself and all its
  descendants. That keeps the result acyclic.
- The longest-ranging candidate is chosen. Ties go to the older origin,
  then the lineage identifier.

**Rounding to 0.01 Myr**, under labelled working conventions. Corrected
16 October: the original end = start − 0.005 rule could move a present
censor beyond the horizon (Codex, 76/1720). The rules apply in this order
of precedence:
1. **Present censors stay at 0 Ma.** Extinction and bifurcation ends keep
   their rounded dates.
2. **Short intervals keep the end and move the origin.** If the rounded
   duration is ≤ 0, set origin = end + 0.005. A lineage originating at
   0.004 Ma and censored at 0 therefore becomes 0.005 → 0.
3. **Parent–daughter chronology is checked jointly after step 2.**
   - If a daughter's origin is now older than its parent's, set it equal
     to the parent's origin, under the joint-age tie.
   - If that leaves the daughter's duration ≤ 0, or breaks the parent's own
     ordering, both lineages keep their **unrounded** dates. Such cases are
     flagged "unroundable" and counted.
4. **Shared event times** (bifurcation ties, buds at parent age 0) are
   rounded together, as one time.
5. **A budding parent whose rounded end equals the daughter's start:** the
   link becomes a boundary candidate, as rounding does in the source.

Each replicate records the counts for every rule.
- Treating a single coincident daughter as censored is a working
  convention. It is not proof of non-informative censoring.

**Exposure observation, a data-matched raw process.** It is fitted to the
recorded *raw* pattern, a marginal summary of the data with no relatives'
outcomes.
- **Coverage:** a lineage has any Triton coverage with π_L = 0.877 (235 of
  268).
- **Within covered lineages, after 66 Ma**, observation follows a two-state
  Markov chain:
  - first bin observed: 0.804;
  - observed, given the previous bin observed: 0.963;
  - observed, given the previous bin missing: 0.218.
- **All bins before 66 Ma are unobserved.**
- **Derived values**, simulated over the actual 3,184 lineage-bins
  (200 replicates, seed 20261016;
  [script](../data/q012-exposure-support/observation_process.py), output
  `observation_process.json`, replay identical):

  | | Raw availability | Lagged availability |
  | --- | ---: | ---: |
  | This process | 0.731 | 0.692 |
  | Recorded data | 0.713 | 0.667 |

  The remaining gap reflects heterogeneity this process does not capture.
- **Simpler processes miss more**, which is why they were not used (Codex
  reproduced the first figure):

  | Process | Lagged availability |
  | --- | ---: |
  | iid at p = 0.667, no mask | 0.796 |
  | iid with the mask | 0.786 |
  | Two-level iid | 0.758 |

- **Informative scenarios:** both transition logits are shifted by α = 1
  per SD of E (R3m-informative), or by α = 1 per unit of x
  (frailty-informative).

### 8.3 The prediction contrast isolates relatives' history

**Target, coded in Ma:** Y_d = 1 iff t_d − 5 ≤ t_ext ≤ t_d, *and* the
extinction precedes any bifurcation.
- For example, with origin at 10 Ma, extinction at 8 Ma counts, and
  extinction at 4 Ma does not.
- The predicted probability is the cumulative incidence
  ∫₀⁵ S_all(s) μ(s) ds, with S_all = exp(−∫(μ + b)), in forward time since
  origination. It is not 1 − S_ext(5).

**Both arms get the same exposure forecast:**
- persistence of the parent's last used E before t_d;
- if the parent's E is missing, the population mean with the missing
  indicator, identically in both arms.

Only the relatives' history used to predict frailty differs.

| Arm | Daughter frailty |
| --- | --- |
| With relatives | From the cross-fitted posterior for the parent's x, given its recorded history up to t_d: survival to its age at t_d, its recorded buds, and **the birth event at t_d itself**, which informs the parent's x when κ ≠ 0. Then the kernel |
| Without relatives | The **birth-conditioned marginal**: the distribution of x among daughters at birth under the cross-fitted model, obtained by forward simulation. It is not the root prior, since intensity weighting shifts it, for example by ρκσ² |

**Other rules:**
- **The combined contrast** (parental E against mean E) is a separately
  labelled secondary question. Codex's counterexample shows it can give a
  Brier gain of 0.09 with no inherited frailty.
- **Replacing β·E by its expectation** is a plug-in sensitivity, not
  integration over future E.
- **If the reference gain is not positive,** the prediction arm is
  dropped. The primary rule then becomes:
  - supported iff lo(η) > η₀;
  - informative negative iff hi(η) < η₁;
  - inadequate otherwise.

### 8.4 Distinct decision endpoints and a complete numerical table

**The outcome is two flags, not one exclusive label** (corrected 16
October). An interval such as [0.08, 0.15] satisfies lo > η₀ and hi < η₁
at once: dependence is detected, and a consequential effect is excluded
(Codex, 76/1720).
- **D**, dependence detected: lo > η₀.
- **X**, consequential effect excluded: hi < η₁.

| D | X | Reading |
| --- | --- | --- |
| Yes | No | **Supported**: consequential dependence possible |
| Yes | Yes | **Small but non-zero dependence** |
| No | Yes | **Informative negative** |
| No | No | **Inadequate** |

In the endpoints below:
- false support means P(D) where η ≤ η₀;
- positive power means P(D and not X | η₁);
- informative-negative power means P(X and not D | η = 0).

The joint frequencies of D and X are reported in every scenario.

**Endpoints, all against the generator's truth:**

| Endpoint | Requirement | Scenarios |
| --- | --- | --- |
| (a) False support, P(D) | At most 0.05; upper Monte Carlo bound at most 0.07 | Every scenario with η ≤ η₀: R0; R0′; R1; R3m; R3m-informative; R2 at η = 0 and 0.05; R4 at η = 0; R-root at η = 0 |
| (b) Positive power, P(D and not X \| η = η₁) | At least 0.8; lower bound at least 0.75 | R2 at η₁ = 0.20, σ ∈ {0.5, 1} |
| (c) Informative-negative power, P(X and not D \| η = 0) | At least 0.8; lower bound at least 0.75 | R1 and R2 at η = 0 |
| (d) Coverage of the 90% interval for η | Between 0.85 and 0.95 | Where the working η is the generator's η: R0, R1, R2, R4 at ψ = ∞, ε = 0 |
| (e) R3b, separately | P(D \| R3b, η = 0) is reported as the rate at which unmeasured clade-tied exposure is reported as residual dependence. It is not counted as coverage of η, and it is not a pass of anything | R3b |

- Under ψ < ∞, ε > 0, R3m and R3m-informative, coverage is reported
  against the same truth. Any loss is a finding.

**The numerical scenario table, all placeholders filled:**

| Item | Setting |
| --- | --- |
| E within a lineage | AR(1) per 1-Myr bin around 26.26°: φ = 0.8, innovations N(0, 13.38²(1 − φ²)), truncated to [0, 90] |
| E at speciation | Daughter's initial E = 26.26 + ρ_E(E_p − 26.26) + N(0, 13.38²(1 − ρ_E²)), with ρ_E ∈ {0.5, 0.9} |
| E standardisation | As in the data (mean 26.26, SD 13.38) |
| β | 0 in the reference; 0.5 per SD in R3m (hazard ratio 1.65) |
| Informative missingness | α = 1 (§8.2) |
| U (R3b) | The same AR and inheritance structure, ρ_U = 0.9, scaled to SD 0.5 on the log-hazard scale; never observed |
| R0′ | Inherited age offset s_d = parent's age at budding, with k = 1.3 |
| Reference rates | h₀(t) by 3-Myr bin from marginal extinctions per lineage-Myr. λ₀ = 0.0708 / E[z^κ] and b₀ = 0.0082 / E[z^{κ_b}], with E[z^κ] = exp(κ(κ − 1)σ²/2) |
| Crossed subset | The full ψ × ε cross only for R1 (σ = 0.5) and R2 at η₁ (σ = 0.5). Every other scenario runs at the primary reference and at ψ = ∞, ε = 0 |
| Primary reference | ψ = 0.8 at 1 Myr, ε = 0.06, κ = κ_b = 0, β = 0, σ = 0.5 |

- **The rate matching is to prior frailty moments,** not realised at-risk
  event rates under selection and branching. Realised rates are reported
  per scenario.

**Caps.** With capped fraction c and an event rate p among the uncapped
replicates, the all-attempt rate lies in [(1 − c)p, (1 − c)p + c].
- A pass requires the worst end of that interval to satisfy the rule.
- An unresolved decision driven by caps is not a pass.

**An item carried from the component check.** Divergent transitions from
the σ → 0 funnel appeared in 19 of 20 component fits. Before the full
pilot, either reparameterise (for example, sample η and the residual
scale) or use a stricter adapt_delta. Divergences are reported either way.

### 8.5 Next

1. Codex checks the component execution evidence and this amendment.
2. Then a measured-cost pilot of the full working likelihood, under its
   own declared compute limit. Placement (local, deep-server) is decided by
   the measured cost.
3. No grid and no empirical fit until then.
