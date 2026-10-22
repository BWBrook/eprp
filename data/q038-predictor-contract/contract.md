# Q-038 replacement contract, v2: target, model, folds, scores and checks

Owner: Claude | 21 October 2026 | Status: **v2, for Codex's review; no fit;
no empirical score.**

**v1** (`c523389`) was reviewed by Codex in 76/2153
([review](../../ideas/2026-10-21-q038-replacement-contract-review-codex.md)).
Codex approved the conceptual repair: the prefix risk set, latent
membership, and the separation of O from B. v2 makes its four major
amendments:
1. The severity-matched score is replaced by a predictive law that
   conditions after integration (section 4; checks S1–S3).
2. Leave-one-event-out masking cuts every component that crosses the
   held-out transition, including tails never seen again (section 5;
   M1–M4).
3. Explicit laws are given for the unknown nuisance quantities, and O is
   renamed an exposure-conditioned hindcast (sections 1, 3 and 5).
4. An executable full-model and probe specification is added, with E3's
   scope qualified (sections 3, 7 and 8; F1–F3 and T1–T2).

The [support tables](README.md#support-findings) remain the reviewed
snapshot.

**Unchanged since v1:**
- the unit is PBDB `genus_no`, with subgenera merged;
- the classes are Rhynchonellata and Bivalvia;
- the event intervals are k = 7, 21, 38, 45 and 68;
- body size is excluded;
- taxonomy is learned within the prefix (76/2139).

**Checks:**

```bash
Rscript --vanilla data/q038-predictor-contract/contract_checks.R
Rscript --vanilla data/q038-predictor-contract/contract_checks_v2.R
```

The outputs are [contract_checks.tsv](contract_checks.tsv),
[prefix_features_check.tsv](prefix_features_check.tsv),
[exposure.tsv](exposure.tsv), [contract_checks_v2.tsv](contract_checks_v2.tsv)
and [loeo_features_check.tsv](loeo_features_check.tsv).

## 1. Two assessments, kept apart

**O, an exposure-conditioned observation hindcast.** From the record before
event k, predict which genera are not recorded in k + 1, …, k + M.
- O is conditional on the **realised** post-boundary exposure series and on
  the training fold's predictive law. That future exposure is information
  not available at the origin, and the other-class series can itself
  respond to the crisis.
- **O is not an origin-only forecast**, which would need a model for future
  exposure.
- O may gain from detection heterogeneity alone (E2: 0.3752 nats with zero
  biological selectivity), and makes no claim about deaths.

**B, biological selectivity of latent event loss.**
- **Synthetic data:** scored against true simulated deaths and membership.
- **Empirical data:** reported as posterior inference, never as labels:
  - β̄_e,c and τ, prior against posterior;
  - contraction relative to the prior;
  - a model-implied expected set gain.

**The retrospective cohort** (fad < k ≤ lad) is descriptive only. Its
membership depends on the future (E1).

## 2. Target

- **The origin** is the end of stage k − 1. Records in stage k are never
  predictors.
- **The risk set** contains genera first recorded by k − 1 with last prefix
  record ℓᵢ ≥ k − W, with W = 3 primary.
- **Membership** is mᵢ = 1{zᵢₖ = 1}. **Biological loss** is
  vᵢ = 1{zᵢₖ = 1, zᵢ,ₖ₊₁ = 0}.
- **Observation:** yᵢ⁺ = 1{recorded in k + 1, …, k + M}, with M = 3
  primary.
- **Sensitivities:** W = 1 and W = all; M = all later stages.
- W and M are score-independent operational choices (Codex: retain). Three
  stages are not a fixed number of Myr: durations range from 0.78 to 19.5
  Myr, median 5.
- **Every score also reports:** stage durations, the number of old genera
  outside W that were excluded, and the distribution of membership
  probabilities.
- Stage-k entrants form a descriptive stratum.

## 3. The model

**One primary slope.** The selectivity parameter of interest is the slope
on **x_occ**: the risk-set z-score of log(distinct references at ℓ), that
is, prefix occupancy. Every other predictor is a declared nuisance with its
own coefficient:
- recency, in Myr;
- age, in Myr;
- completeness;
- log10(range km + 1), with an NA indicator;
- a single-locality indicator.

A vector of slopes with one shared event deviation would impose equal
deviations on every covariate. That is avoided.

**Hazard.** logit(1 − φᵢₜ) = ηᵢₜ.

| Interval | ηᵢₜ |
| --- | --- |
| Background t | α_c,t + β_b,c x_occ,i⁽ᵗ⁾ + γ_cᵀuᵢ⁽ᵗ⁾ + f_fam(i) + g_ord(i) |
| Event k | α_c,k + ω_c,k + (β̄_e,c + δₖ) x_occ,i⁽ᵏ⁾ + γ_cᵀuᵢ⁽ᵏ⁾ + f_fam(i) + g_ord(i) |

- The event row's nuisance coefficients γ_c are the background ones. δₖ
  applies to the occupancy slope only, and is **shared by both classes**,
  so an event is one unit.
- **Covariates are always prefix covariates** from stages < t. The
  transition out of the first-record stage f uses covariates computed from
  stage f's own records.
- **Priors:**
  - α_c,1 ~ N(logit 0.1, 1.5²); α_c,t+1 = α_c,t + σ_α,c ξ_t, with
    ξ_t ~ N(0, 1) and σ_α,c ~ half-N(0, 0.5). The walk runs through event
    stages.
  - **The event excess** is ω_c,k ~ N(μ_ω, s_ω²), with μ_ω ~ N(1, 1) and
    s_ω ~ half-N(0, 1). This is the law for unknown event severity.
  - β_b,c, β̄_e,c and the components of γ_c are each N(0, 1).
  - δₖ ~ N(0, τ²), with τ ~ half-N(0, 0.5). Sensitivities: scales 0.25
    and 1. Prior and posterior τ are always reported.
  - f_fam ~ N(0, s_f²) and g_ord ~ N(0, s_o²), with s_f, s_o ~
    half-N(0, 0.5).
- **Unknown, unresolved and new clades** take an effect *drawn* from
  N(0, s²) in every prediction. Predictive variance is kept; the effect is
  never set to zero.

**Detection by exposure.** For t > fᵢ:

  pᵢₜ = 1 − exp(−θᵢₜ Eₜ),
  log θᵢₜ = γᵈ_c,0 + γᵈ_c wᵢ⁽ᵗ⁾ + b_fam(i) + ν_c,t.

- wᵢ⁽ᵗ⁾ is the log mean references per recorded stage over stages < t (at
  the first transition, log references at f). Priors:
  - γᵈ_c,0 ~ N(log 0.01, 2²);
  - γᵈ_c ~ N(0, 1);
  - b_fam ~ N(0, s_b²), with s_b ~ half-N(0, 0.5);
  - ν_c,t ~ N(0, s_ν²), with s_ν ~ half-N(0, 0.5).
- **Eₜ is a declared proxy**, not an external effort instrument: distinct
  references in stage t with any occurrence of the six other deposited
  classes. It avoids direct feedback from the focal class (Rhynchonellata
  references fall from 127 to 29 across the end-Permian).
  - Sensitivities: focal-class leave-one-out, collections, and an
    all-animal series once its binning is verified.
- **Exposure in the final stage alive.** Primary ε = 1.
  - The ε = 0.5 sensitivity uses the pair-state likelihood. Emission in the
    stage of death uses pᵉ = 1 − (1 − p)^ε.
  - **First capture is tilted:**
    P(z_f+1 = 1 | detected at f) = φ_f p_f / (φ_f p_f + (1 − φ_f) pᵉ_f).
    The ε = 1 conditioning cannot be reused unchanged.
  - Derived and enumerated in F1–F3: total probability 1 at both ε; ε = 1
    equals standard CJS to 6e-17; the tilted first survival is 0.889
    against an untilted 0.83.

**Genus likelihood** (ε = 1). This is as in v1. Codex verified it by
absorbing-state enumeration to 7e-18, and π and q to 1e-16:

  Lᵢ = ∏ₜ₌f^{ℓ−1} φᵢₜ · ∏ₜ₌f₊₁^{ℓ} pᵢₜ^{yᵢₜ}(1 − pᵢₜ)^{1−yᵢₜ} · χᵢ,ℓ,

  χᵢ,ₜ = (1 − φᵢₜ) + φᵢₜ(1 − pᵢ,ₜ₊₁)χᵢ,ₜ₊₁, with χᵢ,C = 1.

## 4. Predictive quantities and scores

For each training posterior draw θ⁽ᵐ⁾, the unknown quantities are drawn
from their predictive laws:
- the event excess ω_new ~ N(μ_ω, s_ω²);
- the event deviation δ_new ~ N(0, τ²);
- the one-step random-walk predictions of α for k − 1 → k and for the
  post-event background stages;
- future ν ~ N(0, s_ν²);
- new-clade effects.

Then πᵢ, λᵢ = πᵢ(1 − φᵢₖ) and qᵢ follow the v1 formulas, using realised
future Eₜ.

**O, the conditional set score** (primary). The law conditions **after**
integration:

  P(S_O | D_O, train) = Σₘ P(S_O | θ⁽ᵐ⁾) / Σₘ P(D_O | θ⁽ᵐ⁾).

- P(S | θ) is the product of independent Bernoulli terms in q(θ).
- P(D | θ) comes from the elementary symmetric polynomials of q(θ).
- The gain is reported against log[1 / C(N, D_O)], per genus.

**Rules for the score:**
- **No severity matching.** Σq = D_O can have no root (S3: the minimum of
  Σq is 1.52 while P(D_O = 1) = 0.378).
- **The two rejected alternatives are not used.** Averaging conditionals
  gives 0.775, and conditioning on averaged q gives 0.694, against the
  proper 0.794 (S1). The law is normalised to 2e-16 over every D (S2).
- **Endpoints** D_O = 0 or N have conditional probability 1. They are
  reported as uninformative and excluded from conditional gains.
- **O, unconditional score:** log of the mean over m of P(S_O | θ⁽ᵐ⁾),
  from the same predictive law.
- Averaging log scores is not the same as scoring the averaged law. Only
  the averaged law is scored.

**B, synthetic.** The biological set law among the true members, given
D_B, also conditions after integration: Σₘ P_m(S_B) / Σₘ P_m(D_B), with
event-loss probabilities 1 − φᵢₖ(θ⁽ᵐ⁾). The gain is against
log[1 / C(|members|, D_B)].

**B, empirical:** posteriors and contraction (section 1). The model-implied
expected B gain is labelled "model-based, not validated".

## 5. Folds and masking

**Forward chaining** (exposure-conditioned historical hindcast).
- All histories are censored at k − 1.
- Forecasts use random-walk prediction, not future fitted states.
- **The first event (k = 7)** has no earlier event. Its primary is a
  **prior-predictive** event forecast. A background-transfer baseline
  (β̄_e := β_b) is reported separately, labelled as such, and never
  substituted silently.

**Leave-one-event-out** (retrospective transport). It holds out event k*
for both classes. **Masking rule:**
- **Every history component that begins at or before k* is censored on the
  left side of the held-out transition, whatever its later records:**
  - held-out risk-set genera at k* − 1;
  - all others at k*.
- **Any component with a later record restarts**, conditional on its first
  post-boundary detection. Held-out genera never restart.
- No inferred death time, last record or range-through classification
  decides which χ tail is cut.

What the checks show:
- **M1:** under the rejected "spanning only" rule, an old genus outside W
  that never reappears still informs event survival through its unseen
  tail (0.1886 against 0.2413, reproducing Codex's example). The masked
  likelihood has range 0.
- **M2:** for old never-reappearing genera, bridging gaps, k* entrants,
  recent spanning genera and later entrants, the masked likelihood is
  invariant to the held-out φ. The spanning-only rule fails for the old
  genus.
- **M3:** a held-out genus's masked contribution is identical across all
  16 future patterns and across event φ.
- **M4:** restarted components are proper conditional laws (total
  probability 1).

**Retrospective-transport information is declared.** Other genera's
unmasked later records may resolve family-to-order mappings.
- **T1:** perturbing held-out genera's future rows (delete, shuffle, or
  inject relabelled references) leaves every held-out feature, label and
  z-score identical, in 30 of 30 cases on the deposit.
- **T2:** other genera's later labels *do* change held-out order labels in
  5 of 10 class-events. That is exactly the declared policy, now tested.
- The forward fold allows no such information (v1 check P: 30 of 30).

**Standardisation:** within each event's risk set, from prefix values;
zero variance gives 0; all-missing drops the predictor but keeps its
indicator.

**Forbidden in every fold:**
- a target genus's records, traits or labels after its prefix;
- **any likelihood contribution from a held-out transition, including
  unseen tails**;
- scaling constants from future cohorts;
- future fitted states in forward folds;
- choosing events, W, M, exposure or priors after any score.

## 6. Prefix predictors

As in v1, with one change: **x_occ is the single primary slope**, and the
rest are nuisances (section 3).

| Predictor | Definition |
| --- | --- |
| Recency | stages and Myr |
| Age | first-record base minus evaluation age |
| Occupancy at ℓ | references (primary) and collections |
| Location at ℓ | located rows and coordinate pairs |
| Range | log10(km + 1), with an NA indicator |
| Completeness | recorded prefix stages ÷ (ℓ − f + 1) |
| Clade | prefix-learned |

## 7. Deterministic checks

**From v1** ([contract_checks.tsv](contract_checks.tsv)):
- **E1, prefix invariance:** retrospective membership varies in 4 of 4
  enumerated prefixes; the prefix forecast in 0 of 4.
- **E2, detection-only null:** O = 0.3752104, B = 0.
- **E4, labels:** the prefix-learned label cannot be outvoted by future
  references.
- **P:** on the deposit, 30 of 30 strictly identical.
- **E3 is qualified (Codex 76/2153).**
  - It is a toy: constant background survival, two detection types, and
    constant post-boundary detection within each type.
  - Its results stand **for that toy only**:
    - naive last appearance is spurious under the null;
    - the joint model recovers β when it is identified;
    - M = 1 with free post-boundary detection is a flat ridge;
    - M = 3 is identified.
  - "At least two post-event occasions" is not a general sufficiency
    theorem for a model with changing covariates, stage, family and
    random-walk effects.
  - The profile-derived standard errors (0.45–1.06) are illustrative local
    approximations, not power calculations for the deposit or the
    hierarchical model.

**New in v2** ([contract_checks_v2.tsv](contract_checks_v2.tsv)):

| Group | What it checks |
| --- | --- |
| S1–S3 | The score law: the mixture example; normalisation and endpoints; the no-root example |
| M1–M4 | Masking: Codex's tail example; invariance across five history types; held-out futures; restart normalisation |
| F1–F3 | ε = 0.5 enumeration and the tilted first capture |
| T1–T2 | Asymmetric leave-one-event-out taxonomy on the deposit ([loeo_features_check.tsv](loeo_features_check.tsv)) |

## 8. The synthetic recovery probe

This is a proposal for Codex. Nothing has been run.

**Generator.** It simulates histories forward. It never selects histories
to hit risk-set sizes.
- **Entries:** genera enter each stage and class at Poisson rates equal to
  the deposit's first-record counts per stage (medians: 14 Rhynchonellata
  and 10 Bivalvia per stage). This approximately matches the design sizes;
  the frozen W rule is then applied.
- **Survival** follows section 3, at declared true values:
  - background loss of about 0.19 for Rhynchonellata and 0.05 for
    Bivalvia per stage (the deposit's background medians);
  - β_b = 0.3; nuisance γ = 0.2; τ = 0.3; s_f = s_o = 0.3;
  - ω set to give event loss fractions near the observed event D/N.
  - **β̄_e = 0 (null) or 0.5 per SD (positive control)**, for each class.
- **Detection is generated at the reference level.**
  - Stage t has Eₜ references, the other-class series.
  - Each detects each living genus with probability 1 − exp(−θᵢₜ).
  - Genus-stage presence and reference counts follow from that. x_occ comes
    from the simulated counts, exactly as from the deposit.

**Scenarios:**
1. Null.
2. Positive control.
3. **Exposure tracks survivors.** The true post-event opportunity is
   Eₜ × (class survivor fraction)^1.0, while the fit uses Eₜ. The
   predeclared diagnostic is a posterior predictive check of detection
   rates by stage after events.
4. **Reference-level clustering.** Each reference carries a shared
   log-intensity ζ_r ~ N(0, 0.5²) across all genera; the fit omits it.
   The predeclared diagnostic is a check of dispersion in reference
   counts.

Repeated rows within an already-collapsed reference are not trials. Only a
shared reference effect is a meaningful clustering challenge.

**Execution:**
- **First, a benchmarked pilot** of 5 datasets, to measure runtime,
  convergence and the cost of a full run. No gate can pass on it.
- **Then 200 attempted datasets** each for scenarios 1 and 2, and 100 each
  for scenarios 3 and 4, with fixed seed ranges.
- The fit is Stan CJS with latent states marginalised by the forward
  algorithm: four chains, R-hat ≤ 1.01 and ESS ≥ 400. Any divergence is a
  failed fit.
- **Failed fits stay in the denominator,** and every failure type is
  reported.

**Gates** (provisional, per class, with Monte Carlo uncertainty):

| Gate | Pass | Fail | Unresolved |
| --- | --- | --- | --- |
| 95% interval coverage for β̄_e,c | point ≥ 0.90 and binomial 95% lower bound ≥ 0.85 | upper bound < 0.90 | otherwise |
| Bias | \|bias\| ≤ 0.1, with its Monte Carlo SE reported | | |
| Null B gain | within ±0.02 nats per genus, with its Monte Carlo interval | | |

- **Precision:** report the posterior SD of β̄_e,c and its contraction
  relative to the prior. An SD above 0.5 is an **operational precision
  hold for this design**, not a failure of Q-038.
  - A strong prior can produce a small SD on its own, so contraction must
    accompany it.
  - Under the positive control, report the held-out B gain.
- **If scenario 3 or 4 produces false biological selectivity that its
  predeclared diagnostic does not flag,** the B claim is not earned. O
  keeps its observational scope.

## 9. Open choices for Codex

1. The generator's true values (section 8). Are they plausible?
2. The coverage rule (pass, fail, unresolved).
3. Should event-interval nuisance coefficients equal background ones, or
   take their own priors?
4. The ω structure: independent per class-event, or shared per event like
   δ.

## v3 amendments (Codex 76/2166; [review](../../ideas/2026-10-22-q038-v2-contract-review-codex.md))

These supersede the matching parts of sections 3, 4, 5 and 8 above. The new
oracle is [marked_history_oracle.R](marked_history_oracle.R), with output
[marked_history_oracle.tsv](marked_history_oracle.tsv).

### A. The marked-history predictive law (replaces the fixed-path q in section 4)

**What updates during prediction.** The detection covariate w (log mean
references per recorded stage, from stages < t) and the history covariates
update with each genus's **own** future records:
- x_occ: log references at the last recorded stage before s, for the
  transition s → s + 1;
- recency;
- completeness.

Age advances deterministically.

**What is frozen.** Every z-score's mean and SD are fixed at the forecast
origin, from the risk set's prefix values. Future values are transformed
with the same constants.
- With scaling frozen, genera are conditionally independent given θ and
  their own marks, so the joint set law factorises within each draw.
  **O3:** a brute-force joint enumeration of two genera matches the product
  of their marginals to 1.1e-16.
- Re-standardising over future risk sets would couple them (O3: an error
  of 1.5e-4), so it is not used.

**How the unseen marks are integrated.** For each training posterior draw
θ⁽ᵐ⁾, the stage-k and later reference counts are integrated over:
- **exactly** when the count space is small (the oracle);
- **by Monte Carlo** otherwise, with at least 2,000 future paths per genus
  per draw, and the Monte Carlo SE of each q reported.

The realised post-boundary exposure Eₜ is conditioned on: this is the
hindcast. The set and count law then conditions after integration, as in
v2.

**Oracle results:**
- **O1** reproduces Codex's example exactly: q = 0.6686077 integrated,
  against 0.6852245 with predictors frozen.
- **O2:** total probability is 1; the joint total is 1; and set and count
  normalisation holds.
- **O4:** the predictive function takes only the prefix. All 18 replaced
  future record patterns leave it unchanged, range 0.
- **O5:** Monte Carlo agrees with exact enumeration, |z| = 0.19 at
  200,000 paths.

**Entry and first capture.**
- A genus enters (originates) at a latent stage, as a Poisson count per
  stage and class.
- While alive, its stage-t reference count is Binomial(Eₜ, 1 − e^{−θ}), so
  P(recorded) = 1 − e^{−θE}, which is v2's exposure law. θ uses w = 0
  before any record.
- The first record is the first positive count, and the CJS conditions on
  it. The first-capture count is zero-truncated binomial.
- **With ε < 1,** the stage of death has exposure εθ, and first capture
  tilts survival out of f, as in F3 and O6. At ε = 0.5 the tilted survival
  is 0.796 against an untilted 0.70, with the generator enumeration in
  agreement.

**Spatial marks.** Range is **removed from the primary nuisance set.** It
returns later as a sensitivity, with its own spatial-mark kernel. The
primary nuisance set is recency, age and completeness, all functions of the
record history and integrated as above.

### B. Null definitions and scenario labels (replace section 8's scenarios)

| Label | Truth | Expected B gain | Gates applied |
| --- | --- | --- | --- |
| **S0, uniform biological null** | Event transition η = α_c,k + ω_c,k only: no occupancy, nuisance, clade or event-deviation terms. Background and detection heterogeneity kept | 0 | null B gain within ±0.02 nats per genus; O gain reported (positive is expected, not a failure) |
| **S1, zero-mean occupancy with other selectivity** | β̄_e = 0, τ = 0.3, nuisance γ = 0.2, clade s = 0.3 at events | Positive (Codex's two-member example: 0.0555 nats) | coverage and bias for β̄_e,c only; **no B-null gate** |
| **S2, positive control** | β̄_e = 0.5 per SD; otherwise as S1 | Positive | coverage and bias for β̄_e,c; held-out B gain reported |
| **S3 and S4** | Survivor-tracking exposure; reference-level clustering (section 8) | — | false-selectivity diagnostics, as in section 8 |

**Incremental occupancy gain** is reported separately. It is the B gain of
the full model minus that of a matched model with the occupancy slope fixed
at 0 and the same nuisance structure.

### C. Masking for the ε = 0.5 sensitivity (amends section 5)

- **With ε < 1, every left component is censored at k* − 1, not k*.**
  Stage-k emission depends on the held-out transition when ε < 1:
  φp + (1 − φ)[1 − (1 − p)^ε] is 0.4140 at φ = 0.2 and 0.5768 at φ = 0.9
  (O7).
- **O7, enumerated:**

  | Cut | Range of the likelihood over φ_k |
  | --- | ---: |
  | At k, with ε = 0.5 | 0.094 |
  | At k − 1, with ε = 0.5 | 0 |
  | At k, with ε = 1 | 1e-16 |

- **Genera first recorded at k*** lose that record under the k − 1 cut, and
  restart at their first record after k*.
- The primary ε = 1 rule (cut at k*) is unchanged.

### D. Manifest for the five-dataset pilot

This pilot measures runtime and convergence only. It cannot pass any
recovery gate.

**Design:**
- Scenario **S2**; seeds **38001 to 38005**, one dataset each.
- The deposit's 87 stages and their durations ([stages.tsv](stages.tsv)),
  both classes, and the five events at k = 7, 21, 38, 45 and 68.
- **Entries:** Poisson per stage and class, with mean equal to the
  deposit's first-record count for that stage and class.
- **Exposure Eₜ:** `refs_other_classes` ([exposure.tsv](exposure.tsv)).

**Hazard truth:**
- α_c,t constant: logit 0.19 for Rhynchonellata and logit 0.05 for
  Bivalvia (σ_α = 0).
- **Event excess ω_c,k:** solved deterministically, before the run, so
  that the mean event loss among members at the design covariates equals
  the deposit's class-event D/N:
  - Rhynchonellata 0.27, 0.53, 0.77, 0.53, 0.49;
  - Bivalvia 0.21, 0.09, 0.34, 0.19, 0.30.
- β_b = 0.3; β̄_e,c = 0.5.
- τ = 0.3, with δₖ drawn once per dataset from its seed.
- γ = 0.2 for each z-scored nuisance (recency in Myr, age, completeness).
- Taxonomy: 40 families in 8 orders per class, assigned uniformly at entry,
  with s_f = s_o = 0.3.

**Detection truth:**
- θ = 0.01 · exp(0.5 w + b_fam + ν_c,t), with s_b = 0.3 and
  ν_c,t ~ N(0, 0.2²).
- ε = 1; W = M = 3.

**Fit and gates:**
- Stan CJS with latent states marginalised by the forward algorithm: 4
  chains, 1,000 warmup and 1,000 draws.
- A fit succeeds only with R-hat ≤ 1.01, bulk and tail ESS ≥ 400 and zero
  divergences.
- **Record:** runtime per dataset, every failure type, and contraction of
  β̄_e,c relative to the prior.

**Decision conventions for the later campaign** (declared now; nothing
runs yet):
- **Coverage:** Clopper–Pearson 95% intervals.
- **Bias and gain:** pass only if the 95% Monte Carlo interval lies inside
  the tolerance band; fail if it lies wholly outside; otherwise
  unresolved.
- **Failed fits** count as non-coverage. Bias and score are reported
  conditional on successful fits, alongside the failure rate, with no
  values imputed.
