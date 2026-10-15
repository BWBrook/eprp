# B-001: target contract for a repeatable order of recovery after crises

Owner: Claude | 14 October 2026, amended 15 October 2026 | The first bounded
product for
[B-001](../ideas/register-blue-sky.md#b-001-do-ecosystems-reassemble-in-a-repeatable-order-after-crises).
It applies Codex's corrections from cross-critique and the repairs from
[Codex's merge review](../ideas/2026-10-14-blue-sky-merge-review-codex.md).
The first version is at `f3bf6a4`; section 9 records what changed.

Status: **a design contract, now on hold.** Its support audit (15 October)
led to a practical hold of the global guild-grain empirical route, agreed
with Codex; see section 10. No restoration time was computed and no model
was fitted.

Sources:
- A Sonnet subagent read Song et al. 2018, Dunhill et al. 2024 and Nicholls
  et al. 2026 in full; Cribb et al. 2023 and Dunhill et al. 2018 in their
  Methods; Chen & Benton 2012 by abstract only (paywalled); the rest by
  abstract.
- Claude checked the decisive points against the extraction.
- All DOIs were checked against Crossref.

## 1. The two end-Permian accounts measure different things

| Work | What it measures | Scale and resolution | What "order" means there |
| --- | --- | --- | --- |
| Chen & Benton 2012, 10.1038/ngeo1475 (abstract) | Rebuilding of **trophic structure**, asserted narratively: "rebuilt stepwise from low to high trophic levels"; a stable ecosystem "did not re-emerge until ... 8–9 Myr after the crisis". It allows ammonoids and others to diversify within 1–3 Myr | Global review; south China figure | A narrative sequence of tiers |
| Song, Wignall & Dunhill 2018, 10.1126/sciadv.aat5091 (full) | **Subsampled genus richness and proportion** for three motility classes: non-motile (which lumps planktonic protists with sessile benthos), motile, and nekton. "Top-down" is inferred by *assuming* nekton are top predators | Global; 17 bins, mean 3.1 Myr; 4,321 genera | Group curves and the nekton proportion, not first reappearance |
| Dunhill et al. 2024, 10.1038/s41467-024-53000-2 (full) | Feasible **food webs** (13 metrics) reconstructed from trait-defined guilds, not observed feeding links; guild richness | One basin (Cleveland, Toarcian), 4 intervals | Metrics recover at different times: the early community was "tall, thin and top-heavy" |
| Nicholls et al. 2026, 10.1038/s44185-025-00117-2 (full; a perspective) | Reconciles the accounts as different metrics: "rapid recovery of multiple trophic levels albeit in the form of top-heavy, unstable Early Triassic ecosystems" | Global against local | — |

**Inference.** Chen & Benton and Song et al. are not a test between
bottom-up and top-down assembly rules. They differ in:
- endpoint: trophic completeness against richness and proportion by
  motility class;
- the meaning of "recovery";
- classification: motility is not trophic level.

So B-001's residual is: for a *defined* endpoint, is there a shared order of
recovery across events, beyond survivor pools, sampling, clade contingency
and shared tolerances?

Other single-event or descriptive work: Foster & Twitchett 2014; Dunhill et
al. 2018 (10.1111/pala.12332, end-Triassic, recovery timing by mode of
life); Cribb et al. 2023; Edie et al. 2018; Alvarez et al. 2019 and Lowery &
Fraass 2019 (K–Pg plankton function and complexity). This bounded search
found no cross-event test of order.

## 2. The target

- **Primary endpoint: partial richness restoration time** T(g, e) for guild
  g in event e. It is renamed from "re-establishment": a guild that keeps
  80% of its richness never lost its presence.
  - T is the time in Myr from the event horizon to the first post-event bin
    in which the guild's subsampled genus richness reaches f = 0.5 of its
    pre-event baseline *and* does not fall below it in the next resolved
    bin (a sustained return).
  - Sensitivity, never a second primary: the first crossing without the
    sustain rule; f = 0.25 and f = 0.75.
  - Time is in Myr from bin age bounds, not bin index, so unequal stage
    durations do not create ties or gaps by themselves.
- **Secondary endpoints, reported separately and never pooled:**
  - relative dominance;
  - local trophic completeness, only where Lagerstätten or basin-scale data
    exist, as in Dunhill et al. 2024.
  - Recovery of process (for example reef building) is out of scope except
    as context.
- **Guild:** Bambach-style tiering × motility × feeding, from Knope et al.
  2015's coding. The guild list and a rule for merging sparse categories
  into declared coarser parents are fixed using pre-event support only,
  before any restoration time is computed.
- **Events:** the end-Permian, end-Triassic and K–Pg recoveries (the
  best-sampled), with stage or substage bins. Others may be added only
  before restoration times are computed.
- **Scope:** global marine animal genera within Knope's list, with the same
  taxonomic and realm scope in every event. The endpoint is global; local
  recolonisation is a different quantity.
- **Inference concerns these named events and this guild set.** Three
  events are not a sample from a population of crises. Guild resampling
  does not measure uncertainty about other crises, and no such claim is
  made.

## 3. Censoring, ties and the at-risk set

| Case | Rule |
| --- | --- |
| Baseline | Subsampled richness in the last pre-event stage (Changhsingian, Rhaetian, Maastrichtian), with its resampling distribution. The penultimate stage is a stability diagnostic only: the Norian lasts 21.6 Myr, so a two-stage mean would not be comparable across events |
| At-risk set | Guild–event pairs whose baseline meets the support rule (section 8), judged from pre-event data only. A guild absent or unsupported before an event is *not at risk* in that event: missing by design, not dropped after outcomes are seen |
| Zero or small baseline | Not at risk. A minimum baseline of 5 subsampled genera keeps f × baseline meaningful |
| Follow-up | Post-event stages whose base lies within H = 10 Myr of the event: Induan–Anisian (to 10.44 Myr), Hettangian–Pliensbachian (to 17.2 Myr) and Danian–Thanetian (to 10.0 Myr). The next stage (Ladinian, Toarcian, Ypresian) can only confirm a crossing; it is never a crossing itself. The Toarcian carries its own extinction, so confirmation there is conservative |
| Sustain rule, everywhere | A crossing counts only if the next resolved stage is also at or above f. This applies to the first post-event stage as well. A first stage at or above f followed by a resolved stage below f fails, and the search continues |
| At or above f in the first stage, sustained | Left-censored: T is in (0, end of the first stage]. These guilds were at or above f by the end of that stage. A coarse first stage cannot tell uninterrupted retention from loss and rapid return within it |
| Candidate crossing with no resolved confirming stage | Unresolved, not a failure to restore. Right-censored at the *base of the candidate stage*, not at the horizon |
| No candidate crossing in follow-up | Right-censored at the top of the last follow-up stage. The Smithian–Spathian crisis falls inside the end-Permian follow-up and counts as continuing stress, not truncation |
| Sustained crossing observed | Interval-censored on the age span of the crossing stage. The model receives explicit lower and upper bounds |
| Post-event guild cell below the coverage quorum | Kept as unresolved, not dropped: no crossing or confirmation can be declared in it, so the censoring interval widens across it. Dropping it would select on the outcome |
| Uncertainty in baseline and richness | Repeated subsampling draws give a censoring interval per draw. The analysis is repeated over draws and the results are combined |

Ties are not broken arbitrarily. Overlapping intervals carry uncertain
order into the model.

## 4. Conditioning and the observation model

The order is interpreted *given*:
- the **surviving functional pool**: survivor genera per guild, including
  zero. A guild with no survivors must re-evolve or immigrate;
- **pre-event occupancy**: baseline richness. Dominant guilds have more
  survivors and recover faster mechanically;
- **continuing stress and severity**: event-level, absorbed by the event
  effect. Three events cannot separate them, and the target is the order
  *within* events;
- **detection**:
  - nekton and soft-bodied predators preserve poorly;
  - aragonite and calcite mineralogy matters;
  - facies change after events (for example microbialites);
  - Lagerstätten inflate local completeness.

**Identification problem.** A guild's detection that is constant across
events is exactly confounded with a repeatable guild order. Detection must
therefore enter from an estimate made independently of the restoration
times: per guild and bin, a sampling completeness or coverage computed from
occurrences. Any concordance left over is regularity *not explained by the
modelled observation process*. It is biological only to the extent the
detection model is adequate; the positive controls in section 7 test this.

**Coding dependence.**
- In PBDB's taxa service, ecospace values are mostly inherited from higher
  taxa ([provenance script and table](../data/b001-support/README.md)):
  - across 89,623 valid metazoan genera, 98.0–99.0% of populated motility,
    life-habit and diet values;
  - 96.2–98.6% among genera whose ranges reach the three recovery windows
    (all Metazoa, not restricted to marine).
- This concerns PBDB's annotations. The proposed route uses Knope's
  coding, whose provenance the support audit must establish.
- Inheritance implies dependence between guild assignment and
  classification, not identity. Many clades share a guild, and broad clades
  span several. What matters is the joint guild × clade table at a declared
  rank, which the support audit tabulates.

## 5. Statistic, parameter and interval

**Kendall's W is descriptive only.**
- For m independent, complete, untied rankings, E(W) = 1/m, and
  W = [1 + (m − 1) × mean pairwise Spearman] / m (Codex).
- An exact enumeration of three independent rankings of six guilds
  confirms:
  - mean W = 1/3;
  - 95th percentile 29/45 ≈ 0.644;
  - P(W ≥ 0.5) = 0.177.
- The first version's thresholds are withdrawn. W ≥ 0.5 is not a 5% test,
  and "W below 0.2" means negative mean correlation, not negligible
  positive order.
- W is reported only beside its distribution simulated under R0 for the
  actual support. It is also invariant to reversing every event's order, so
  it cannot carry direction.

**The parameter.** An interval-censored log-normal accelerated-failure-time
model, for example with brms `cens()` (Bürkner 2017,
10.18637/jss.v080.i01):

log T(g, e) = α(e) + x(g, e)β + c(k(g, e)) + θ(g) + ε(g, e)

- α(e): event effect.
- x(g, e): log(1 + survivor count), log baseline richness, and the
  detection estimate. Guilds with zero survivors are counted and reported.
- c(k): the effect of the dominant clade k (the class contributing most
  baseline occurrences to the guild in that event), with variance σ_c².
- θ(g): the guild effect, with variance σ_θ².
- ε: residual, with variance σ_ε².

**Repeatability ρ = σ_θ² / (σ_θ² + σ_c² + σ_ε²).**
- It is the expected correlation, on the log-delay scale, between one
  guild's restoration delays in two events filled by *different* dominant
  clades, after the event effects and covariates.
- ρ = 0 means no shared guild order beyond the modelled nulls and clades.
- This reading assumes independent, homoscedastic guild, clade and residual
  effects.

**Identification is a property of the whole incidence structure** (Codex,
second review).
- The covariance is V = σ_θ² G + σ_c² C + σ_ε² I, where G and C mark cells
  sharing a guild or a dominant class.
- Clade switches within guilds are neither necessary nor sufficient:
  - two classes, each holding two guilds that never switch across three
    events, can still separate the components;
  - a unique clade in every cell makes C = I, so clade and residual
    variance cannot be separated, even though every guild switches.
- The audit therefore reports:
  - the full guild × event × class incidence and composition;
  - the rank of the covariance basis {PGP, PCP, P} after projecting out the
    fixed design P (rank 3 is necessary, not sufficient);
  - counts of each pair type.
- Switches are reported as a biological diagnostic, not a gate.
- Removing a shared class effect does not remove all phylogenetic
  dependence.

**Working thresholds:**
- **Negligible, ρ₀ = 0.1.** Guild identity explains at most a tenth of the
  residual variance in delay.
- **Rule strength, ρ₁ = 0.5.** Guild identity explains at least half the
  residual variance.
- These are working discrimination scenarios, not established boundaries of
  ecological usability. They are not an implication of the stepwise-rule
  literature. Their interpretation and sensitivity belong in the design
  product, and they are frozen with the priors before the section 7 check.

**Interval.** A 90% posterior interval for ρ, used for two one-sided
decisions. The prior is stated, with a sensitivity run under an alternative
prior on the variance components. Posterior tail probabilities do not by
themselves give frequentist 5% error rates; section 7 calibrates them.

## 6. Rival processes and outcomes

| Rival | What generates the order | Signed prediction |
| --- | --- | --- |
| R0. Sampling and survivor null | Survivor counts, baseline and detection; no guild effect | ρ near 0 once detection is modelled; W at its simulated null |
| R1. Clade contingency | Clades recover at their own rates | σ_c² large, σ_θ² small: order follows clade, not guild, when clades change |
| R2. Bottom-up rule | Primary consumers recover before predators | δ > 0 (below) |
| R3. Top-down or opportunistic | Predators recover early ("top-heavy") | δ < 0 |
| R4. Shared tolerance | Guild tolerances to the post-event environment set the order | σ_θ² falls into the negligible range once a tolerance covariate is added |

**Direction (R2 against R3).**
- A second model adds a signed contrast δ: assigned predators against
  primary consumers (suspension and deposit feeders, grazers).
- A consequential direction is |δ| ≥ log 1.5: a 50% longer median delay.
- The share of σ_θ² that δ removes shows whether the shared order is
  trophic.
- Trophic position here is assigned from feeding codes, not observed energy
  flow.

**R4.**
- A third model adds a physiological-buffering class (Knoll et al. 2007,
  10.1016/j.epsl.2007.02.018) as a guild tolerance covariate.
- That class is coded at higher-taxon level, so separating R4 from R1 again
  depends on clade turnover within guilds.
- An event-specific environmental trajectory enters only through α(e). A
  guild × environment interaction needs co-registered proxy timing with
  stated uncertainty, and is secondary.
- The decomposition is predictive, not causal. Communities can alter their
  environment (bioturbation, carbonate production), so conditioning on it
  can remove part of a biological effect.

**Outcomes** (lo and hi are the 90% interval for ρ):

| | hi < ρ₁ (rule strength excluded) | hi ≥ ρ₁ |
| --- | --- | --- |
| **lo > ρ₀** (shared order present) | Weak shared order: present, below rule strength | Shared order present. Rule strength is supported if lo ≥ ρ₁, otherwise unresolved |
| **lo ≤ ρ₀** | Informative negative for a rule-strength order at this grain; whether a weak order exists is unresolved | Inadequate discrimination: park the empirical route at this grain and keep the question |

- The primary claim is *residual cross-event regularity conditional on the
  tested nulls*. It names a mechanism only through δ, the R4 covariate, and
  rival generative models compared on common observables with equal
  nuisance information.
- A precise negative constrains the shared-order claim. It does not show
  that ecological recovery is contingent in general.

## 7. Discrimination check before any restoration time is computed

After the support audit, simulate the whole pipeline on the actual supported
table (at-risk set, survivor counts, baselines, detection, bins and
censoring rules) under:
- R0, with ρ = 0;
- ρ = ρ₀ and ρ = ρ₁;
- clade-only (σ_θ = 0);
- tolerance-only.

Also simulate a detection-only control: guild-constant detection
differences with σ_θ = 0.

Freeze the priors, ρ₀ and ρ₁, the censoring rules and the data generator
first. Then estimate the probability of each outcome cell, with Monte Carlo
uncertainty.

**Proceed only if all of these hold:**
- **Power:**
  - with ρ = ρ₁, the interval excludes ρ₀ with probability ≥ 0.8;
  - with ρ = 0, it excludes ρ₁ with probability ≥ 0.8.
- **False decisions** (Codex, second review). A procedure that always
  returned [0.2, 0.3] would pass both power criteria.
  - P(lo > ρ₀ | ρ ≤ ρ₀) ≤ 0.05;
  - P(hi < ρ₁ | ρ ≥ ρ₁) ≤ 0.05;
  - both evaluated at ρ = 0, ρ₀, ρ₁ and 0.7.
- **Coverage:** the 90% interval covers the true ρ at close to its nominal
  rate on the same grid.
- **Controls, in acceptance and not only reported:**
  - clade-only and detection-only (true ρ = 0): P(lo > ρ₀) ≤ 0.05;
  - tolerance-only: the model with the tolerance covariate gives
    P(lo > ρ₀) ≤ 0.05.

If the check fails, **park the empirical route** before restoration times
are looked at.
- The grid is finite, so it is not a uniform bound.
- The check uses post-event sampling summaries but not crossing times.
- This check, not a guild count, decides whether the data can inform. A
  smaller well-resolved table may pass; a larger tied or confounded one may
  fail.

## 8. Next gate: a support audit, with support defined first

Definitions, fixed on 15 October 2026 before any screening. They are
committed separately from the audit's results.

**Population, bins and support:**
- **Population:** PBDB occurrences with these settings:
  - marine (`envtype=marine`);
  - regular preservation;
  - genus certain;
  - lumped to one occurrence per genus per collection;
  - in Knope's nine phyla.
- **Bins:** PBDB timescale 1 stages, with ages as served on 15 October 2026.
  An occurrence is assigned to a stage only if its age range lies within
  that stage.
- **Events:** 251.902 Ma (end-Permian), 201.4 Ma (end-Triassic) and 66.0
  Ma (K–Pg).
- **Follow-up:** as in section 3.
- **Coverage:**
  - Good's u, computed from the genus occurrence counts in a guild × stage
    cell, estimates coverage;
  - a cell is resolved if u ≥ 0.5;
  - subsampled richness is the coverage-based rarefaction expectation at
    coverage 0.5 (Chao & Jost 2012, 10.1890/11-1952.1).
- **Baseline support:** the last pre-event stage is resolved, with
  subsampled richness of at least 5 genera.
- **Stage support (all guilds pooled):** at least 50 collections with a
  qualifying occurrence. A stage below this is unresolved for every guild.

**Guilds, survivors and clades:**
- **Guilds** use Knope's codes, which follow the numbering of Bambach et al.
  2007. They are coarsened as follows:
  - tiering: pelagic (1), epifaunal (2–3), infaunal (4–6);
  - motility: fast (1), slow (2), stationary or facultative (3–6);
  - feeding: suspension (1), deposit or mining (2–3), grazing (4),
    predatory (5), other (6).
- **Merge rule:** a guild unsupported at baseline in all three events
  merges fast and slow into "mobile". If it is still unsupported, it is
  excluded and counted.
- **Join:**
  - PBDB accepted genus name plus phylum to Knope's `taxon_name` plus
    phylum;
  - otherwise the name alone, if it is unique in Knope;
  - otherwise unjoined and counted.
  - *Implementation clarified after Codex's check:*
    - the accepted genus is the first word of `accepted_name`, so a
      subgenus counts under its parent genus;
    - rows are deduplicated by collection and genus;
    - a repeated Knope key is used only if every repeat agrees.
- **Survivors:** genera occurring in the baseline stage whose PBDB last
  appearance lies wholly after the event (`lastapp_max_ma` below the event
  age, from the taxa service).
- **Dominant class:** the class with the most baseline occurrences in that
  guild and event.
- **Trait confidence:** Knope records a source reference per genus
  (`eco_ref`), but not whether a code was entered for the genus or applied
  from a higher taxon. Provenance is reported by reference, and the coding
  level is unknown.

Audit steps:
1. Download Knope et al. 2015 Dataset S1 (10.1038/ncomms7455; CC BY 4.0)
   and record how its genera join to PBDB genera in the three recovery
   windows. Report join failures by guild: missing codes can be
   outcome-related, for example among post-event genera.
2. Report:
   - the at-risk guild × event table;
   - survivor counts, including zeros;
   - unresolved bins;
   - the full guild × event × class incidence and composition;
   - the rank of the projected covariance basis, and counts of each pair
     type (section 5);
   - the number of guilds whose dominant clade changes between events, as
     a diagnostic.
3. The join must not choose a different population just because those
   genera joined successfully.

**Planning target, not an information bound:** about 6 at-risk guilds in
each of the 3 events. Section 7 decides whether to proceed.

**Data.**

| Resource | Contents | Terms | Coverage |
| --- | --- | --- | --- |
| Knope et al. 2015 Supplementary Data 1 (10.1038/ncomms7455) | The paper reports 18,621 genera. The deposited sheet has 18,317 rows and 18,228 distinct names. Bambach-numbered tiering, motility and feeding; stage first and last appearances; a source reference per genus | CC BY 4.0; 3,911,680 bytes; downloaded 15 October 2026, sha256 `e5c1eef4…f181` | Whole Phanerozoic, range-through only |
| PBDB occurrences | Occurrences for subsampling | CC0, API | All events |
| Foster & Twitchett, PANGAEA 824825 | Permian–Triassic occurrences and ranges, 12 substages | CC BY 3.0 | Permian–Triassic check |
| Dunhill et al. 2018 Dryad (10.5061/dryad.bg30k); Cribb et al. 2023 Zenodo (10.5281/zenodo.8398420) | End-Triassic modes of life | Open | End-Triassic check |
| Dunhill et al. 2024 Zenodo (10.5281/zenodo.11400588) | Toarcian guild tables and PFIM scripts | CC BY 4.0 | Secondary endpoint, one basin |

This bounded search found no open occurrence-level ecospace matrix spanning
three or more recoveries. The route is PBDB occurrences joined to Knope's
coding by genus.

**Overlap.** Q-007 and Q-009 are linked. B-010 (reef export) and B-011
(energetic autonomy) may share trait resources but are different tests.

## 9. Amendment record (15 October 2026)

All of the following come from the
[merge review](../ideas/2026-10-14-blue-sky-merge-review-codex.md).
All were accepted.

| Review point | Change |
| --- | --- |
| 1. W's chance baseline | W is demoted to a descriptive statistic beside its R0 simulation. The 0.5 and 0.2 thresholds on W are withdrawn. The target is now ρ, with ρ₀ and ρ₁ and a 90% interval; scope is these events |
| 2. Ties, censoring and selection | The endpoint is renamed "partial richness restoration time". Section 3 adds rules for left, right and interval censoring, zero baselines, a sustained return, and an at-risk set judged from pre-event data only. Time is in Myr |
| 3. Mechanism | Signed contrast δ for direction; an R4 covariate; residual-regularity wording; a precise negative does not prove contingency |
| 4. Guild against clade | "A guild is largely a clade" is withdrawn. The provenance of the inheritance share is now [reproducible](../data/b001-support/README.md), with denominators. It is labelled as PBDB's coding, not Knope's. The data-absence claim is bounded to this search |
| 5. Six guilds | Kept as a planning target only. The section 7 discrimination check decides |

**Second review (15 October 2026;
[Codex's response](../ideas/2026-10-15-blue-sky-support-response-codex.md)).**
All points were accepted, and they were applied before any screening.

| Review point | Change |
| --- | --- |
| Identification needs the whole incidence structure | Section 5: covariance basis and its rank; switches become a diagnostic, not a gate |
| The power gate passes a constant interval | Section 7: false-decision limits, coverage, a detection-only control, and acceptance criteria for the controls. Priors and the generator are frozen first |
| Sustain rule at the window edges | Section 3: the sustain rule applies to the first stage as well; an unconfirmed terminal candidate is right-censored at its own base; confirmation-only stages; explicit bounds |
| log(0) survivors and the unnamed collection threshold | log(1 + s); at least 50 collections per stage |
| The 201.4–191 Ma window was 10.4 Myr, not 10 | Follow-up is defined by stage bases within 10 Myr, giving declared spans of 10.44, 17.2 and 10.0 Myr |
| 0.1 and 0.5 | Relabelled as working discrimination scenarios |

The baseline was also changed from the mean of the last two stages to the
last stage alone. The two-stage mean would have included the 21.6 Myr
Norian, which is not comparable with the other events' stages.

## 10. Support audit result (15 October 2026): practical hold

Full record: [support audit](../data/b001-support/README.md#b-001-support-audit-knope-coding-joined-to-pbdb-15-october-2026).
It was run under the section 8 definitions, which were committed first
(`e7697d9`). No post-event richness or crossing was computed.

The first release (`451a96b`) had three faults, which
[Codex's check](../ideas/2026-10-15-blue-sky-support-adjudication-codex.md)
found:
- a subgenus defect in genus identity;
- a merge universe that included post-event stages;
- an overstated power claim.

The corrected results are below.

**Support:**
- 4, 5 and 7 guilds are at risk (16 cells); 4 are at risk in all three
  events. The binding constraint is the minimum baseline; stage support is
  adequate.
- The covariance basis has rank 3.
- 27–53% of window genera join Knope's coding.
  - Within classes, join rates are stable across events.
  - Fishes, sharks, conodonts and ostracods are barely coded, which is a
    risk for any guild they might fill.

**Exact balanced no-clade F benchmark:**
- With 4 complete guilds: 0.29 and 0.27 against the 0.8 targets.
- Completing all 7 at-risk guilds to three events, a design containing the
  actual table: 0.47 and 0.53.
- This is a benchmark for one procedure and scenario. It is not a bound on
  every calibrated analysis of the actual design.

**Disposition: HOLD as a practical programme decision**, agreed with Codex.
- The question is kept.
- No impossibility is claimed, and this is not evidence against repeatable
  reassembly.
- **Reopening:**
  - support that materially enlarges the set of guilds repeated across
    events;
  - or a justified alternative target or design with adequate calibrated
    errors and power, under its own contract.
