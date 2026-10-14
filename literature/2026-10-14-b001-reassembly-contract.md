# B-001: target contract for a repeatable order of recovery after crises

Owner: Claude | 14 October 2026, amended 15 October 2026 | The first bounded
product for
[B-001](../ideas/register-blue-sky.md#b-001-do-ecosystems-reassemble-in-a-repeatable-order-after-crises).
It applies Codex's corrections from cross-critique and the repairs from
[Codex's merge review](../ideas/2026-10-14-blue-sky-merge-review-codex.md).
The first version is at `f3bf6a4`; section 9 records what changed.

Status: **a design contract.** No data were analysed and no model was fitted.

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
| Baseline | The mean subsampled richness of the last two pre-event bins, with its resampling distribution |
| At-risk set | Guild–event pairs whose baseline meets the support rule (section 8), judged from pre-event data only. A guild absent or unsupported before an event is *not at risk* in that event: missing by design, not dropped after outcomes are seen |
| Zero or small baseline | Not at risk. A minimum baseline (proposed: 5 subsampled genera) keeps f × baseline meaningful |
| Retained above f in the first post-event bin | Left-censored: T is in (0, end of the first bin]. These are counted and reported as guilds that did not lose half their richness at this resolution |
| Never sustained above f within the horizon | Right-censored at H = 10 Myr after the event. For all three events this lies before the next major event (Toarcian, PETM). The Smithian–Spathian crisis falls inside the end-Permian window and counts as continuing stress, not truncation |
| Crossing observed | Interval-censored on the age span of the crossing bin |
| Post-event guild cell below the coverage quorum | Kept as unresolved, not dropped: no crossing can be declared in it, so the censoring interval widens across it. Dropping it would select on the outcome |
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
- x(g, e): log survivor count, log baseline richness, and the detection
  estimate.
- c(k): the effect of the dominant clade k (the class contributing most
  baseline occurrences to the guild in that event), with variance σ_c².
- θ(g): the guild effect, with variance σ_θ².
- ε: residual, with variance σ_ε².

**Repeatability ρ = σ_θ² / (σ_θ² + σ_c² + σ_ε²).**
- It is the expected correlation, on the log-delay scale, between one
  guild's restoration delays in two events filled by *different* dominant
  clades, after the event effects and covariates.
- ρ = 0 means no shared guild order beyond the modelled nulls and clades.
- θ is separated from c only by guilds whose dominant clade changes between
  events. The audit counts these. If there are too few, R1 cannot be
  excluded, and the result is inadequate discrimination on R1, whatever ρ̂
  is.

**Thresholds, fixed before data:**
- **Negligible, ρ₀ = 0.1.** Guild identity explains at most a tenth of the
  residual variance in delay, so no usable shared sequence exists.
- **Rule strength, ρ₁ = 0.5.** Guild identity explains at least half the
  residual variance. A sequence that recurs more than it varies is the
  minimum the stepwise-rule literature implies.
- These are choices on a new scale, not the W values carried over. Codex can
  challenge them before the discrimination check.

**Interval.** A 90% posterior interval for ρ, read as two one-sided
decisions at 5%. The prior is stated, with a sensitivity run under an
alternative prior on the variance components.

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

Estimate the probability of each outcome cell.
- **Proceed only if** both hold:
  - with ρ = ρ₁, the interval excludes ρ₀ with probability ≥ 0.8;
  - with ρ = 0, it excludes ρ₁ with probability ≥ 0.8.
- **Otherwise park the empirical route** before restoration times are
  looked at.
- The check uses post-event sampling summaries but not crossing times.
- This check, not a guild count, decides whether the data can inform. A
  smaller well-resolved table may pass; a larger tied or confounded one may
  fail.

## 8. Next gate: a support audit, with support defined first

Definitions, fixed before counting:
- **Bins:** stages or substages on the repository's interval crosswalk.
  Occurrences resolved to one bin only.
- **Coverage:** coverage-based subsampling within guild and bin, at quorum
  0.5.
- **Baseline support:** quorum reached in both of the last two pre-event
  bins, and a subsampled baseline of at least 5 genera.
- **Bin support (all guilds pooled):** a minimum collection count per
  post-event bin. Bins below it are unresolved for every guild.
- **Horizon:** 10 Myr.
- **Trait confidence:** whether each Knope code was entered for the genus
  or inherited, if the dataset records it; otherwise reported as unknown.

Audit steps:
1. Download Knope et al. 2015 Dataset S1 (10.1038/ncomms7455; CC BY 4.0)
   and record how its genera join to PBDB genera in the three recovery
   windows. Report join failures by guild: missing codes can be
   outcome-related, for example among post-event genera.
2. Report:
   - the at-risk guild × event table;
   - survivor counts, including zeros;
   - unresolved bins;
   - the joint guild × dominant-clade table at class rank;
   - the number of guilds whose dominant clade changes between events.
3. The join must not choose a different population just because those
   genera joined successfully.

**Planning target, not an information bound:** about 6 at-risk guilds in
each of the 3 events. Section 7 decides whether to proceed.

**Data.**

| Resource | Contents | Terms | Coverage |
| --- | --- | --- | --- |
| Knope et al. 2015 Supplementary Dataset 1 (10.1038/ncomms7455) | 18,621 genera, Bambach-coded tiering, motility and feeding; stage first and last appearances | CC BY 4.0; 3.8 MB (not yet downloaded) | Whole Phanerozoic, range-through only |
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
