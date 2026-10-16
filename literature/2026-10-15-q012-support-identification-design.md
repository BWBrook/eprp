# Q-012 (with D1): support, events and identification design

Owner: Claude | 15 October 2026, amended the same day after Codex's single
review | The next decision in Q-012's
[current contract](../ideas/register.md#q-012-heritable-susceptibility-versus-intrinsic-ageing-in-extinction-risk),
after the [prior check](2026-10-14-q012-prior-check.md). It folds in Codex's
blue-sky D1: speciation as a reset of vulnerability, or its transmission.

**History:**
- The first version is at `0f0cd35`.
- [Codex's review](../ideas/2026-10-15-blue-sky-route-amendment-and-q012-review-codex.md)
  found four binding problems, all accepted (section 9):
  - the event units;
  - identification under persistent exposure;
  - selection;
  - the missing forecast landmark.

**Status:** a design contract. No outcomes of relatives were compared, no
model was fitted, and no calibration was run.

## 1. Data and event units

- **Source:** Lamyman, Fordham & Pearson 2026, supplementary data, Zenodo
  21414007 (concept 10.5281/zenodo.18854730; CC BY 4.0).
  - Codex's [source audit](../data/q012-source-support/README.md) pins
    the members and reconciles scope: 482 − 2 benthic *Praepararotalia* =
    480.
  - It preserves a source disagreement: 73/407 present/extinct by row,
    against 72/408 in S3's summary.
- **Event dictionary**
  ([record](../data/q012-event-dictionary/README.md); source-located;
  rerun reproduces it exactly).
  - **Primary unit: the source's 268 in-scope lineage records**, with their
    ancestor codes.
    - Date relation to the ancestor, for in-scope ancestors: 208 overlap and 49 boundary. Corrected 16 October: 7 further overlap links point to the excluded `L_Bolivina Clade`.
    - 257 in-scope parent–daughter links (188 with both extinct; 16 with
      speculative ancestry).
    - 234 sister pairs from 72 sibships (150 with both extinct).
    - 52 extant.
  - **The article confirms the unit.** Barry supplied it; it is open
    access under CC BY 4.0, so the earlier 403 was a site block. It is
    git-ignored in `data/raw/lamyman2026/article/`, PDF sha256
    `bf479249…7579`.
    - "Evolutionary lineages" are assigned to fossil populations that
      show morphological intergradation, and "The lineage phylogeny aims
      to retain only true cladogenetic events, thereby removing all cases
      of anagenesis" (pp. 3–4).
    - "Budding" means "the ancestor continues to survive after giving rise
      to its descendant". "Bifurcating" means "two descendants are
      produced from one ancestor at the same time with the ancestor not
      surviving" (p. 4, after Foote 1996). So the 208 in-scope overlap links are
      budding and the 49 boundary links are bifurcation candidates.
    - The conversion follows Aze et al. 2011. Where literature was lacking,
      "qualitative decisions were made" (p. 5).
    - Ancestry is stratophenetic: "A cladistic approach has been
      consciously avoided" (p. 5). It therefore uses stratigraphic order,
      which is why the generator needs its ancestor-assignment rule
      (section 4).
  - **The morphospecies level is a sensitivity layer only.** The workbook
    does not define speciation modes there:
    - only 127 of 269 lineage `Start Source` fields name an S1 species;
    - membership is many-to-many;
    - 350 overlapping links share a listed lineage.
  - **The 18 morphospecies boundary links** stay unresolved: 9 share a
    lineage and 9 do not. None is censored as a pseudoextinction.
- **The Nexus chronograms are not used as a budding graph.** S3 E5 warns
  that they convert buds into bifurcations.
- **Support summary.** At lineage level, the first version's ecogroup lever
  collapses: only 10 parent–daughter pairs differ in a single known
  ecogroup.
- **Ecogroups are partly assigned from relatives.** Where no geochemistry
  exists, ecogroups are assigned "based on phylogenetic affinity and
  geographic information", marked "No Data" (p. 6). That applies to 169 of
  482 S1 rows. Such ecogroups cannot serve as independent exposure
  evidence, because similarity among relatives is partly built in.
- **Triton coverage, as reported** (pp. 6–7; to be verified in our audit):
  - 501,629 macroperforate and 40,673 microperforate records were matched
    to the 480 morphospecies;
  - 81 have no Triton records, and 15 have records only outside their
    assigned ranges;
  - for the remaining 384, median completeness in 1 Myr bins is 100%
    (mean 86.4%).

  Separating inheritance from exposure therefore rests on Triton's observed
  geography (section 7).

## 2. The frailty law, with an effect-size estimand

- **Root lineages:** log frailty x ~ N(0, σ²).
- **Along each parent → daughter link:**
  x_d = ρ x_p + σ √(1 − ρ²) ε, with ε ~ N(0, 1).
- **Frailty:** z = exp(x − σ²/2), so the unconditional mean frailty is 1.
- **Hazard:** h_i(a, t) = z_i h₀(t, e_i) g(a, s_i), where:
  - a is the lineage's age;
  - t is calendar time;
  - e_i is its exposure class (ecogroup, and Triton exposure where
    available);
  - s_i is an inherited age state, used only by the R0′ rival in section
    3.

**Primary estimand: η = ρσ.**
- η is the standard deviation of the part of a daughter's log frailty
  predicted by its parent's.
- **Effect size:** daughters of parents at +σ and −σ differ in hazard by a
  factor of exp(2η).
- **η is well defined at σ = 0, where ρ is not:** then η = 0 whatever ρ
  is. Being well defined does not make it identified; section 3 sets out
  what identifies it. ρ is reported only with σ.
- **Working thresholds:**
  - negligible: η₀ = 0.05, a hazard ratio of at most 1.105;
  - consequential: η₁ = 0.20, a hazard ratio of at least 1.49.

  They are frozen before calibration, and Codex may challenge them.

**Two correlations.**
- In the unselected stationary model:
  - sister log-frailty correlation is ρ²;
  - raw-frailty correlation is (exp(ρ²σ²) − 1)/(exp(σ²) − 1) (Codex).
- Selection and observation change both. Neither is used as an observed
  signature: signatures are computed by simulation under the declared
  selection.
- A small fitted ρ does not by itself establish a reset.

## 3. Finite rival and decision table

| Rival | Generator | What could distinguish it | Status without exposure data |
| --- | --- | --- | --- |
| R0. Own-clock ageing | g(a) varies; σ = 0 | No dependence among relatives beyond h₀ | Identified against R2 (η = 0) |
| R0′. Inherited ageing clock | An explicit inherited state: daughter age offset s_d = parent's age at budding, with g(a + s_d) | Daughters of old budders have *shorter* durations | Identified in sign, conditional on the selection model |
| R1. Frailty, not inherited | σ > 0, ρ = 0 | The same marginal survival curve as R0; no dependence among relatives | Identified against R2 |
| R2. Inherited frailty | σ > 0, ρ > 0 | η > 0 | — |
| R3a. Exposure by time and ecogroup | h₀(t, ecogroup) | Absorbed by the baseline | Identified (weak lever at lineage level) |
| R3b. Persistent exposure tied to clades, **unmeasured** | An environmental field with tree-structured covariance, for example a persistent province, *left after* adjustment for measured exposure | **The same survival likelihood as R2** (Codex's counterexample). It also produces a positive parent-age signature | **Not identified, with or without Triton.** Two independent Gaussian fields with the same tree correlation K give covariance (σ_A² + σ_U²)K, so no data on survival alone can split them |
| R4. Budding depends on frailty | Budding rate λ_i = λ₀ z_i^κ | An association between budding count and duration, within the joint likelihood | Identified, if budding is modelled (section 4) |

**What Triton can and cannot do (corrected after Codex's closure check).**
- Triton's palaeolatitude and ocean-basin histories can **adjust for
  measured exposure**: dependence among relatives that follows their shared
  observed geography is removed.
- They cannot remove **unmeasured** exposure that shares the tree's
  correlation structure (R3b). After adjustment, η therefore measures
  **residual phylogenetic dependence after adjustment for measured
  exposure**.
- "Inherited susceptibility" may be claimed only under an explicit,
  defended restriction that separates the two covariance structures, for
  example an exposure field that decorrelates with time while inherited
  frailty does not. Any such restriction must be stated before
  calibration. None is assumed here.

**D1's parent-age signature is a conditional prediction, not a test of
mechanism.**
- R2 with survivorship predicts it positive, as does R3b.
- R0′ predicts it negative.
- R0 and R1 predict zero.

It is reported with this table, never alone.

## 4. A joint likelihood for the realised history

The data are one realised history of budding, extinction and observation.
With latent log frailties x, durations T (censored at the present),
budding times B and the observation and inclusion process O:

L(θ) = ∫ p(x | σ, ρ) ∏ᵢ [ h_i(T_i | x_i)^δᵢ S_i(T_i | x_i) ]
       × ∏ᵢ p(B_i | T_i, x_i; λ₀, κ) × P(O | T, B; ψ) dx

- **Budding.** The budding term is (λ₀ z_i^κ)^{m_i} exp(−λ₀ z_i^κ T_i),
  for m_i buds. It also encodes knowledge that there were no later buds.
  - **Only when κ = 0** is it free of x and of the extinction parameters
    given the observed T. It can then be **dropped from the full-history
    likelihood**.
  - That does not license conditioning on B as a fixed design. The
    conditional law p(T | B) needs the generally θ-dependent denominator
    ∫ p_θ(T) p(B | T) dT (Codex). The full-history formulation is kept.
  - Otherwise it stays in the likelihood, as rival R4.
- **No "left truncation at last budding" is used.** The first version's
  rule is withdrawn. With durations observed, T_i > B_last holds
  automatically, and the joint likelihood above already carries the
  parent-survival tilt through f(T_p | x_p) and p(x).
  - Codex's tilted law, p(x | T > B) ∝ p(x) ∏ S(B | x), is the right object
    only when T beyond B is unobserved.
  - Conditioning the topology as a fixed design while treating durations
    as random would be the wrong conditional experiment.
- **Inclusion.** O includes a declared inclusion probability, for example
  P(included | T) = q_i(T) = 1 − exp(−ψT): short-lived lineages are less
  likely to be described.
  - Because the frailties are correlated, the normaliser is joint, not
    per lineage (Codex):
    L_inc = ∫ p(x) ∏ᵢ [f_i(T_i | x_i) q_i(T_i)] dx / ∫ p(x) ∏ᵢ Q_i(x_i) dx,
    where Q_i(x) = ∫ f_i(t | x) q_i(t) dt.
  - That is the fixed-population scheme. The branching and ascertainment
    history needs its own corresponding normaliser in the generator, and
    the estimator must use the same one.
- **Ancestor assignment** depends on stratigraphic ranges, so the generator
  carries an explicit rule for it. Speculative links are a sensitivity
  subset.
- **Fitting:** a tree-structured latent Gaussian with survival terms,
  fitted by MCMC (for example Stan) over about 270 latent variables. The
  cost is to be measured in a small pilot.

## 5. Prediction at a landmark (the secondary estimand)

*Relabelled 16 October:* this is **retrospective cross-clade prediction**,
not prospective forecasting (see the
[addendum](2026-10-16-q012-events-exposure-addendum.md), section 4).

| Element | Specification |
| --- | --- |
| Landmark | The daughter lineage's origination t_d |
| Target | Survival of the daughter to h = 5 Myr after t_d (median lineage duration 6.49 Myr) |
| Risk set | In-scope daughters with t_d ≥ 5 Ma, so that the horizon is observable. Younger ones are censored by the present and enter only through a censoring-aware score |
| Permitted relative information | The parent's age at t_d, its earlier budding count and exposure class; older sisters' status and ages at t_d; extinctions of any lineage before t_d; calendar time; Triton exposure up to t_d |
| Excluded (would leak the future) | The parent's later duration or later buds; sisters' futures; anything after t_d |
| Parameters | Cross-fitted: estimated from other clade blocks, using their full histories only |
| Score | Inverse-probability-of-censoring-weighted Brier score at h, and the censoring-aware log score |
| Comparison | Paired: the same model, with and without the permitted relative information |
| Skill threshold | The paired skill interval excludes 0, *and* its point estimate reaches at least half the skill expected at η₁ under the frozen generator |

## 6. Calibration of the combined decision

**The combined decision:**
- **Dependence supported:** the η interval has lo > η₀, *and* the
  landmark skill threshold is met. It is reported as **"residual
  phylogenetic dependence after adjustment for measured exposure"**. The
  word "inheritance" is used only under a pre-declared restriction that
  separates R3b (section 3).
- **Informative negative:** hi < η₁.
- **Inadequate:** anything else.

**Grid:**
- R0;
- R0′;
- R1 with σ ∈ {0.5, 1};
- R2 with η ∈ {0, 0.05, 0.20, 0.35};
- R3a;
- R3m, persistent clade-tied exposure that is *measured* and supplied to the
  adjustment;
- R3b, the same exposure left *unmeasured*;
- R4 with κ ∈ {−0.5, 0.5};
- each crossed with the inclusion and ancestor rules.

**Pass rules**, each with its Monte Carlo interval:

| Criterion | Requirement |
| --- | --- |
| False "supported" under R0, R0′, R1, R3a, R3m (the adjustment must remove it), R2 at η ≤ η₀, and R4 | At most 0.05, with the upper 95% Monte Carlo bound at most 0.07 |
| Power, P(supported \| η = η₁) | At least 0.8, with the lower bound at least 0.75 |
| Power, P(hi < η₁ \| η = 0) | At least 0.8, with the lower bound at least 0.75 |
| Coverage of the 90% interval for η | Between 0.85 and 0.95 at each grid point |

- **Non-identifying cases are labelled, not forced:**
  - σ = 0 for ρ, though η is fine;
  - R3b, unmeasured exposure. It counts as a true positive for "residual
    phylogenetic dependence" and as non-identifying for "inheritance".
- A small measured pilot sets the replicate count before the full grid is
  run.

## 7. Next gates, in order

1. ~~Lineage-record definition~~ **Done** (15 October; section 1). The
   lineage records are anagenesis-free units. Overlap means budding;
   boundary links are bifurcation candidates.
2. **Triton joint exposure audit: done** (15 October;
   [record](../data/q012-exposure-support/README.md)).
   - 340 of 480 species match exactly; there is a 140-species mapping gap,
     with the S3 synonyms as the route to close it.
   - 190 of 268 lineages are covered (median coverage 0.99).
   - Among relatives co-existing with at least 3 joint data bins, 73 pairs
     (31 parent–daughter, 42 sister) have observably different
     palaeolatitude occupancy, and 78 are similar.
   - So the measured-exposure adjustment (R3m) has a real lever. R3b stays
     non-identifiable.

   *Original definition of the gate:* join Triton occurrences to the member
   morphospecies of each lineage. Count lineages with palaeolatitude and
   basin coverage through their ranges, and count relative pairs whose
   observed exposures differ.
   - This sizes the *measured-exposure adjustment* (R3m). It cannot
     separate unmeasured exposure (R3b).
   - Observed exposure is kept separate from ecogroups assigned by
     phylogenetic affinity.
3. **Freeze the section 2 and 6 inputs**, then run a small pilot for cost.
4. **Calibration**, then estimation only if it passes.

## 8. Unchanged from the first version

- The unit of replication is the tree structure.
- Extant lineages are right-censored.
- Speculative ancestry is a sensitivity subset.
- Inference is restricted to Cenozoic planktonic foraminifera.

## 9. Amendment record (15 October 2026)

| Review finding | Change |
| --- | --- |
| Event units: the Nexus files are bifurcating, membership is many-to-many, and the 18 boundary links are not pseudoextinctions; ecogroup count 148, not 150 | A source-located event dictionary. Lineage records are the primary unit, pending their definition. The morphospecies level is sensitivity only, with no mode assigned. The boundary links are unresolved and not censored |
| Persistent exposure tied to clades is equivalent to inherited frailty; the frailty law was incomplete; ρ alone is not an effect size | R3b added and labelled non-identifying without exposure data. The full law is stated. The estimand becomes η = ρσ. Triton exposure is the separating data. D1's sign is conditional |
| Truncation at the last bud omits the survival tilt; the topology is endogenous | A joint likelihood for the realised history. The truncation rule is withdrawn. Budding stays in unless κ = 0. An inclusion term is added |
| No forecast landmark | A landmark and information table, cross-fitting, censoring-aware scores, a paired comparison and a skill threshold |
| Calibrate the combined decision | A finite grid, Monte Carlo pass rules, a coverage band, labelled non-identifying cases and a cost pilot first |

**Closure check (15 October 2026;
[Codex's note](../ideas/2026-10-15-b004-contract-and-q012-amendment-closure-codex.md)).**
Accepted and applied:
- the inclusion normaliser is joint over correlated frailty;
- at κ = 0 the budding factor is dropped from the full-history likelihood,
  not used to condition on B;
- η is well defined at σ = 0 but not thereby identified;
- R3b, unmeasured exposure after adjustment, cannot be identified even with
  Triton, so the positive outcome is worded "residual phylogenetic
  dependence after adjustment for measured exposure";
- boundary links are bifurcation *candidates*.
