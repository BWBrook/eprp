# EPRP question register

**Purpose.** This register is EPRP's standing deliverable. Barry's direction in
Claude chat on 9 October 2026, quoted exactly:

> "We're not trying to come up with a single research target to tackle. We're
> trying to accumulate a whole list of well posed and deeply contextualised
> questions, that might be useful for other Claude/Code teams to later work on.
> The goal for this work is, and will always remain, constant ideation:
> proposing ideas, investigating them, validating/invalidating, proposing data
> sources and methodologies, ranking, adding to proposed lists, removing from
> said lists, whatever. So, as you narrow, so should you also consider expanding
> with new ideas/options!"

He also wants "the big stuff". Questions should be consequential, and tractable
with modern statistics, simulation and current databases. Incremental
applications do not belong here.

## How to use and maintain it

- **Who reads it.** A future team should be able to pick up any entry and start.
  Each entry states the question, why it matters, the nearest prior work with
  access depth, data, methods, the main obstacle or kill criterion, and the next
  step. Detailed evidence lives in the linked notes.
- **Status values.**
  - `sketch`: posed, not yet checked against prior work.
  - `under review`: prior-work and feasibility checks under way.
  - `promising`: has survived a prior-work check and has a feasible route.
  - `ready for handoff`: posed well enough for another team to start.
  - `parked`: blocked or occupied, with the reason and a revisit trigger.
  - `rejected`: with the reason.
  Parked and rejected entries stay in the register.
- **Tier.** A provisional judgement of size × tractability × openness: 1 is
  big, plausibly tractable and apparently open; 2 is valuable but crowded,
  harder or narrower; 3 is modest or methodological. Tiers are agents' opinions,
  not validation.
- **Novelty is unverified** unless an entry says a prior-work check was done.
  "Not found" means not found in a bounded search.
- **Both agents add, revise, demote and remove entries.** Edit only the entries
  you own; disagree in Correspondence. Each round should both narrow, by
  investigating and parking, and expand, with new sketches.
- **Access depth labels:** meta = existence via Crossref; abs = abstract;
  sect = named sections; full = full text.

## Lessons from prior-work checks

These are inferences from the
[round-1 checks](../literature/2026-10-09-register-checks-round1.md). They
describe the sources and designs reviewed so far, not universal limits (Codex,
9 October). Use them as cautions when posing new entries.

1. **Cross-event questions hit a ceiling of roughly 6–30 events.** Few events
   are well dated, forcing metrics share no common scale, and attributing an
   event to its driver is often circular. A question that needs many events is
   weak by default.
2. **Stronger designs use replication within events, or continuous records.**
   That means spatial and taxonomic contrasts within one event, all stage
   transitions treated as a continuum, species-level microfossil series, and
   lineage-resolved phylogenies.
3. **Resolution sets what can be identified.** Lags, precursors and pulses
   shorter than about 50–100 kyr are mostly unresolvable before the Cenozoic.
4. **Live disputes make good seeds**, when they turn on identification rather
   than on data volume.

## Index

| ID | Question | Status | Tier | Owner |
| --- | --- | --- | --- | --- |
| Q-001 | Does an end-Permian-calibrated physiological habitat-loss model transfer to other events? | parked | — | Claude |
| Q-002 | Is mass-extinction selectivity a switch or a continuous function of dose? | parked | — | Claude |
| Q-003 | Can stage-level data tell a warming–extinction threshold from a smooth response? | under review | 3 | Claude |
| Q-004 | A pseudoextinction-corrected background rate for modern comparisons | sketch | 2 | Claude |
| Q-005 | Are there detectable precursors before extinction events? | sketch | 2 | Claude |
| Q-006 | What can fossils identify about diversification that extant trees provably cannot? | sketch | 2 | Claude |
| Q-007 | How long does a biotic loss leave a legacy, given the environmental path? | under review | 2 | Joint |
| Q-008 | Does geographic differentiation help determine subsequent recovery? | under review | 2 | Codex |
| Q-009 | Does ecological organisation retain predictive memory after richness recovers? | under review | 2 | Codex |
| Q-010 | Can biological innovation change how much diversity an environment supports? | under review | 2 | Codex |
| Q-011 | What sets the size distribution of extinction events: forcing or biotic amplification? | under review | 2 | Claude |
| Q-012 | Heritable susceptibility versus intrinsic ageing in extinction risk | under review | 2 | Claude |
| Q-013 | Would the current extinction register as a mass extinction in the rock record? | under review | 2 | Claude |
| Q-014 | How long is the extinction debt after a deep-time perturbation? | sketch | 3 | Claude |
| Q-015 | Could past lineages evolve thermal niches as fast as climate changed? | under review | 2 | Claude |
| Q-016 | Do Red List-style risk criteria predict extinction over geological time? | sketch | 2 | Claude |
| Q-017 | Dark extinction across scales: one detection framework for unseen losses | sketch | 2 | Claude |
| Q-018 | Do plants and terrestrial biotas have mass extinctions in the same sense? | sketch | 2 | Claude |
| Q-019 | How much of macroevolutionary turnover is climate-driven versus biotic? | sketch | 2 | Claude |
| Q-020 | When does geographic range cease to insure against global extinction? | under review | 2 | Codex |
| Q-021 | Which lost biological functions prolong Earth-system recovery? | under review | 2 | Codex |
| Q-022 | How much evolutionary history does each extinction prune? | promising | 1 | Claude |
| Q-023 | Are biodiversity crises origination failures rather than extinction spikes? | under review | 2 | Claude |
| Q-024 | Do ecological early-warning signals work on real Quaternary transitions? | sketch | 2 | Claude |
| Q-025 | How do local losses scale to global extinction, then and now? | sketch | 2 | Claude |

---

## Parked and under review (Claude's disruption area)

### Q-001 Physiological habitat-loss transfer across events
Status **parked** (9 October). Revisit when the NSF consortium publishes its
multi-event results.

- **Question.** Does a frozen metabolic-index model calibrated on the
  end-Permian predict extinction magnitude and selectivity in other events,
  better than traits plus thermal exposure?
- **Why parked.** An NSF five-institution project, "Testing the reduction of
  aerobic habitat as a common kill mechanism for major mass extinction events"
  (Payne, Deutsch, Ridgwell, Blättler, Anbar; 2021–2027), is testing exactly
  this. Its Late Devonian and Late Ordovician tests are already in abstracts.
  Penn 2018 states that selectivity is insensitive to the calibration parameters.
- **Residual angle.** An adversarial mechanism test at events or observables
  where thermal-only (Reddin 2022, 10.1111/gcb.16333) and O₂-limited predictions
  diverge.
- **Evidence.** [A prior-work note](../literature/2026-10-09-a-mi-transfer-prior-work.md);
  [transfer inputs](../literature/2026-10-08-transfer-inputs.md). End-Permian
  fields are on Figshare 7357193 (CC0).

### Q-002 Selectivity as a continuous function of dose
Status **parked** (9 October).

- **Why parked.** Malanoski et al. 2024 (10.1126/science.adj5763, Table S8,
  checked) already fit every ΔT × trait interaction, and all were null. What
  remains is methodological completeness, with weak leverage.
- **Residual angle.** The sign conflict between Smits 2019 (bioRxiv
  10.1101/523811: selectivity strengthens with intensity) and the null or inverse
  results.
- **Evidence.** [B prior-work note](../literature/2026-10-09-b-selectivity-prior-work.md).

### Q-003 Threshold or smooth warming–extinction response: a detectability design
Status **under review**, tier 3.

- **Question.** Under an explicit observation model (proxy time-averaging,
  dating, stage-level sampling), what effect sizes and data would distinguish a
  threshold from a smooth dose–response at about 45 stages?
- **Prior.** Song et al. 2021 (10.1038/s41467-021-25019-2, full); Kaiho 2022
  (10.5194/bg-19-3369-2022, sect); Hillebrand et al. 2020
  (10.1038/s41559-020-1256-9, abs); Kemp et al. 2015 (10.1038/ncomms9890, full).
- **Assets.** The [interval crosswalk](../data/interval-crosswalk/README.md) and
  the [PhanDA dependence sensitivity](../data/phanda-stage-differences/README.md).
- **Obstacle.** A modest result: it reports detectability, not biology. Keep it
  as a diagnostic. It also serves as the detectability component of Q-011's
  reduced dose–response test.

### Q-004 Pseudoextinction-corrected background rate
Status **sketch**, tier 2.

- **Question.** Fossil μ\* includes pseudoextinction, whereas modern counts are
  terminal losses. How much does correcting μ = μ\* − (λ\* − λ) change modern
  versus background ratios?
- **Prior.** Silvestro et al. 2018 (10.1038/s41467-018-07622-y, full);
  Louca & Pennell 2020 (10.1038/s41586-020-2176-1, abs).
- **Obstacle.** Extant-tree μ depends on congruence, so the intervals may be
  unbounded.

### Q-005 Precursors before extinction events
Status **sketch**, tier 2.

- **Question.** Do variance, autocorrelation or range-contraction indicators rise
  before extinction pulses beyond what sampling surrogates produce?
- **Prior.** Sudakow et al. 2026 (10.1038/s41467-026-75655-9, sect: abiotic
  only); Crampton et al. 2026 (10.1017/pab.2026.10107, sect: graptoloid pulses).
- **Data.** Graptoloid composites; NSB/Triton microfossils.
- **Obstacle.** Signor–Lipps truncation and ordering artefacts.

### Q-006 Fossils versus trees: identifiability of diversification
Status **sketch**, tier 2.

- **Question.** What diversification features are provably unidentifiable from
  extant trees but recoverable from occurrences, and at what sampling level?
- **Prior.** Louca & Pennell 2020; Truman et al. 2025 (10.1093/sysbio/syae058,
  sum); Morlon et al. 2022 (10.1016/j.tree.2022.02.004, abs).
- **Obstacle.** A methods frontier with active groups. Needs a sharp,
  application-facing angle.

## Joint and Codex-owned

### Q-007 Biotic legacy under a specified environmental path
Status **under review**, tier 2, joint (agreed 9 October; support gate pending).

- **Question.** After a loss episode, how long does the observable biota carry
  its imprint, given the forcing path? Equivalently, is diversity tracking the
  environment instantly, or running finite-rate dynamics?
- **Prior.** Kirchner & Weil 2000; Lu et al. 2006; Alroy 2008 and 2010; Cermeño
  et al. 2022. Codex read these at Results/Methods depth. None tests prediction
  for withheld regions.
- **Support debate.**
  - PBDB regional continuity is doubtful: Close et al. 2020 cannot follow fixed
    regions.
  - Claude proposes the Cenozoic deep-sea record: CENOGRID forcing
    (10.1126/science.aba6853), fixed DSDP/ODP sites, Triton/NSB species, and
    losses of graded size (K–Pg, PETM, Eocene–Oligocene).
  - Susceptibility composition enters as an effect modifier, not an instrument
    (agreed in 82/1220).
  - **Audit result (9 October, Claude).** The Cenozoic support is *not adequate*
    across events. Sites with both species-level biota and site-level
    temperature number 0 at the K–Pg, 0–2 at the PETM and 4–5 at the
    Eocene–Oligocene transition (clustered at 57–65°S). Abundance is largely
    categorical, and ages are mostly interpolated from biozones.
  - Only a within-event Eocene–Oligocene pilot is feasible. Claude's
    hyperthermal-loop design (82/1224) fails the gate as currently known.
  - **Gate run (9 October; [Triton event support](../data/triton-event-support/README.md)).**
    The criterion: at least 5 samples each side of onset, ages mostly not from
    biozones, and at least 3 PhanSST temperatures each side. Gate sites per
    event:
    - K–Pg (post-event only; Triton has no pre-66 Ma baseline): 4.
    - PETM: 2.
    - ETM2 and ETM3: 0.
    - EOT: 6 (277, 511, 689, 744, 803, 1090). Only 689 and 744 have temperatures
      flagged good, and none has mostly quantitative abundance.
  - The hyperthermal-loop design is therefore out on deposited compilations. The
    EOT is a state transition, not a closed excursion.
  - Lag or loop statistics do not uniquely indicate memory. Recovery to a fixed
    fraction of deficit takes log(1/f)/k whatever the loss, and smooth forcing
    alone makes loops (Codex 82/1238). Any test must compare simulated
    alternatives run through the actual age and sampling process.
  - These counts are specific to this screen, not a claim that suitable sites do
    not exist.
- **Linked:** Q-009 (state variables beyond richness), which uses the same
  dense-series support.
- **Evidence.** [Codex recovery notes](../literature/2026-10-09-recovery-observation-contract.md);
  Correspondence 82.

### Q-008 Geographic differentiation as a determinant of recovery
Status **under review**, tier 2 (9 October).

- **Question.** At comparable richness and environmental conditions, does the
  distribution of distinct biotas among regions predict subsequent recovery?
  Does differentiation preserve sources for recolonisation, or impede recovery
  through isolation? The order in which provinciality and richness return is
  an intermediate observation, not the principal contribution.
- **Why big.** Global richness can conceal the loss of regional biological
  options. This asks whether geographic organisation changes the biosphere's
  ability to rebuild, beyond simply counting its survivors.
- **Nearest prior.** Kocsis, Reddin & Kiessling 2018
  ([10.1098/rspb.2018.0232](https://doi.org/10.1098/rspb.2018.0232), sect:
  Methods/Results) already track Phanerozoic bioregions and their turnover.
  Al Aswad et al. 2025 ([10.1126/sciadv.adr4199](https://doi.org/10.1126/sciadv.adr4199),
  sect: survivor/similarity analyses) link end-Permian homogenisation with physiology.
  Another provinciality curve would occupy established ground.
- **Data and discriminator.** Use deposited bioregion/occurrence data to ask
  whether pre-existing differentiation improves predictions of later regional
  recolonisation or diversification in withheld regions or intervals. Compare
  environmental sorting, dispersal limitation and sampling alone. Separate
  immigration from origination; predictive success would still not establish
  a causal effect of differentiation.
- **Obstacle / next step.** The published bioregions use all time slices in one
  network, potentially leaking future information into forecasts. First establish
  comparable regional histories and training-only partitions; separate turnover
  from richness-driven nestedness. Park the predictive
  route if this support fails or differentiation adds no information beyond
  environment, richness and geographic coverage.
- **Shared mechanism with Q-020.** Use a common habitat-network representation
  with time-varying suitability and taxon-specific dispersal, not necessarily
  one scalar connectivity measure for both extinction and rebuilding. Compare
  predicted directional recolonisation from surviving source regions; first
  detections alone cannot establish source or arrival time. Standardise sampling
  coverage and preserve uncertainty in latent occupancy and immigration.
- **Evidence.** [Register expansion and source checks](../literature/2026-10-09-register-expansion.md).

### Q-009 Ecological memory beyond recovered richness
Status **under review**, tier 2 (9 October).

- **Question.** Once richness has recovered, do functional composition and
  incumbent ecological groups still predict diversification, stability or
  response to the next disturbance? Which biological state variables are
  necessary to describe recovery?
- **Why big.** A restored species count may conceal a different ecosystem with
  different future behaviour. The target is the consequence of reorganisation,
  rather than another demonstration that taxonomy and function recover separately.
- **Nearest prior.** Dunhill et al. 2024
  ([10.1038/s41467-024-53000-2](https://doi.org/10.1038/s41467-024-53000-2), sect)
  reconstruct Toarcian food webs. Alvarez et al. 2019
  ([10.1038/s41586-019-1590-8](https://doi.org/10.1038/s41586-019-1590-8), sect:
  Results/Methods) report nannoplankton function and stability returning before
  richness after K–Pg. Edie et al. 2025
  ([10.1126/sciadv.adv1171](https://doi.org/10.1126/sciadv.adv1171), sect:
  Results/Methods) already examine bivalve incumbency and functional reshuffling.
- **Data and discriminator.** Candidate inputs include nannoplankton abundance
  series, Toarcian guild tables and bivalve traits/stratigraphic bounds; only the
  first offers a dense trajectory. Compare a richness-plus-environment model
  with one carrying functional composition, evaluated on subsequent held-out
  observations. Look for comparable richness with contrasting organisation and
  divergent subsequent outcomes; allow environmental persistence and immigration
  to explain those differences.
- **Obstacle / next step.** Guilds and inferred feeding links are imperfect
  proxies for ecosystem processes. First identify an independently measured
  outcome and a usable later interval; prevent outcome information entering
  guild definitions. Park if the result reduces to familiar recovery ordering,
  or if the apparent memory disappears under observation-aware comparisons.
- **Boundary with Q-007.** Q-009 asks which biological variables must be carried
  forward; Q-007 asks about response times and residual history dependence given
  that state. Claude's Cenozoic support check serves both. An incomplete or
  imprecisely measured state can itself create apparent additional memory.
- **Evidence.** [Register expansion and source checks](../literature/2026-10-09-register-expansion.md).

### Q-010 Biological construction of diversity capacity
Status **under review**, tier 2 (9 October); original either/or framing retired.

- **Question.** Can biological innovations and ecosystem engineering change
  the diversity supported under comparable physical conditions, or can the
  apparent expansion be explained by habitat area, environmental heterogeneity,
  geographic differentiation and finite-rate diversification?
- **Why big.** Is biological opportunity mostly imposed by the planet, or can
  life substantially construct it? This concerns long-term diversification as
  well as recovery from extinction.
- **Nearest prior.** The inspected INDITEK and SNCI models define capacity
  differently; an environmental limit and finite-rate dynamics can coexist
  ([source comparison](../literature/2026-10-08-recovery-contracts-and-response.md)).
  Bambach et al. 2002 ([10.1073/pnas.092150999](https://doi.org/10.1073/pnas.092150999),
  sect: Discussion) already link diversity constraints to ecological structure.
  Cribb et al. 2026 ([10.1038/s41467-026-73628-6](https://doi.org/10.1038/s41467-026-73628-6),
  sect: Results/Methods) find higher formation-level diversity with ecosystem
  engineers. Generic biological control of capacity is therefore occupied.
- **Data and discriminator.** The Cribb occurrence, engineer-trait and analysis
  deposits offer a starting point. Compare local diversity and regional
  differentiation across physical habitat, then ask whether independently coded
  engineering innovations predict subsequent expansion across multiple regions.
  Distinguish engineers creating opportunity from favourable habitat supporting
  both engineers and diversity. Finite-rate models remain comparators throughout.
- **Obstacle / next step.** Observed richness is not capacity; an unconstrained
  time-varying ceiling can explain almost any trajectory. First identify an
  innovation with independent functional and environmental evidence. Park if
  capacity must be inferred solely from the diversity curve it explains, or
  if the proposal reproduces the existing engineer-presence association.
- **Concrete proposed design.** Claude suggests comparing basins receiving the
  same innovation at different times. Retain this staggered-arrival comparison
  at tier 2 until dates, pre-arrival trends and comparable basins are established.
  Arrival follows habitat change and dispersal, so timing alone does not identify
  an effect. Check preservation changes and inter-basin spillovers; distinguish
  pre-existing conditions from habitat changes caused by the engineers. See the
  [design critique](../literature/2026-10-09-feedback-on-register-round1.md).
- **Evidence.** [Register expansion and source checks](../literature/2026-10-09-register-expansion.md).

## New sketches (Claude, 9 October): the big stuff

These are posed for a prior-work check, nothing more. Prior work is listed at
metadata depth unless stated, and none of it has been read for this register yet.

### Q-011 What sets the size distribution of extinction events?
Status **under review**, tier 2 (prior-work check on 9 October).

- **Question.** Given a perturbation catalogue chosen independently of
  extinction, what is the form of the forcing → extinction dose–response
  (linear, threshold, state-dependent)? Does the fitted map reproduce the
  observed extinction-size tail, or is biotic amplification needed?
- **Established.**
  - Magnitudes form a continuum.
  - The tail exponent cannot discriminate mechanisms: Newman 1997
    (10.1006/jtbi.1997.0508) gets an exponent of about 2 for almost any stress
    distribution.
  - Forcing and extinction relate positively but coarsely: Song 2021;
    Kaiho 2022; Green et al. 2022 (10.1073/pnas.2120441119, flood basalts).
  - Across 73 stages, extinction is uncorrelated with LIP or crater size alone
    (Arens & West 2008, 10.1666/07034.1).
  - Rothman 2019 (10.1073/pnas.1905164116) places disruption size in the carbon
    cycle's intrinsic dynamics.
- **Open.** A fitted transfer function with an amplification test was not found.
- **Obstacle.** Only about 10–30 well-dated events; forcing metrics with no
  common scale; stage averaging that hides pulses. The full tail comparison is
  probably underpowered, and the reduced form test is incremental.
  Linked: Q-003.
- **Evidence.** [Round-1 checks](../literature/2026-10-09-register-checks-round1.md).

### Q-012 Heritable susceptibility versus intrinsic ageing in extinction risk
Status **under review**, tier 2. Reframed again on 9 October after Codex's
identifiability point.

- **Identification problem.** Declining hazard with age is widely observed
  (Silvestro et al. 2019, 10.1111/ele.13441; Hagen et al. 2018). Survival curves
  alone cannot separate fixed heterogeneity from intrinsic ageing. Lifelong
  constant rates λ ~ Gamma(α, β) give S(t) = (β/(β+t))^α and hazard α/(β+t),
  exactly the curve of a homogeneous intrinsic-age model, even under perfect
  observation (Codex, [feedback note](../literature/2026-10-09-feedback-on-register-round1.md)).
  Better data improve observation but do not by themselves identify mechanism.
- **Sharper question.** Is extinction susceptibility heritable along lineages,
  so that ancestors' and sisters' survival predicts held-out descendants'
  survival? Does that inherited component explain the apparent age effect?
  Compare models deliberately matched on marginal survival, with shared
  exposure and observation represented, and a stated age convention for
  branching and persistent ancestors.
- **Live dispute.**
  - Quintero et al. 2025 (10.1038/s41559-025-02873-7): heritable rates drift
    upward over time.
  - Tikhonov et al. 2026 (openRxiv 10.64898/2026.07.21.739780): fixed
    "toughness" plus event "luck".
  - Saulsbury et al. 2023 (10.1073/pnas.2307629121): a neutral model with
    sampling.
- **Data.** Triton species-level foraminifera with a pseudoextinction-free
  lineage phylogeny (Aze et al. 2011), and dated palaeo-trees (Cantalapiedra et
  al. 2019, Dryad 10.5061/dryad.gd8038s, CC0).
- **Obstacle.** Arbitrary unshared frailty remains unidentifiable. Inherited
  susceptibility needs enough sister and descendant replication. An active
  field (Quental, Silvestro, Liow, Saulsbury).
- **Evidence.** [Round-1 checks](../literature/2026-10-09-register-checks-round1.md);
  [Codex feedback](../literature/2026-10-09-feedback-on-register-round1.md).

### Q-013 Would the current extinction register as a mass extinction in the rock record?
Status **under review**, tier 2. Downgraded from promising on 9 October pending
a bounded demonstration (Codex).

- **Question.** Take committed and realised modern losses. Aggregate correctly to
  genera, so that a genus counts as lost only when all its species are.
  Filter by clade-specific preservation and compress to stage grain with
  Signor–Lipps smearing. Where does the result fall in the Phanerozoic magnitude
  spectrum, and what counts as "registering"?
- **Nearest work.**
  - Payne et al. 2016 (10.1126/science.aaf2416). *Corrected:* genus threat is
    assigned by both the least- and the most-threatened assessed member
    species, as conditional scenarios, not by a single any-member rule.
    - Table S1 gives 24.2% and 40.4% at Near Threatened or worse, and 14.7% and
      35.1% at Vulnerable or worse.
    - The main text attaches 24–40% to Vulnerable or worse, an internal
      discrepancy (Codex, checked).
    - These are not probabilities of committed or realised extinction.
  - Krone et al. 2024 (10.1017/pab.2023.34): tetrapod geographic gaps.
  - Plotnick et al. 2016 (mammals); Spalding & Hull 2021 (rates); Shaw et al.
    2021 (38% of marine assemblage taxa are in PBDB).
  - Strona & Bradshaw 2026 concerns *undescribed* extinctions, not the rock
    record. This corrects the earlier sketch.
- **Bounded first step (Codex).** Choose a well-assessed, fossil-rich clade
  and build a completely enumerated species–genus crosswalk. Separate four
  things: assessment category, a stated future-loss scenario, true extinction
  of all congeners (which needs explicit dependence assumptions), and
  disappearance as a fossil-recognised taxon. Apply preservation, recognition
  and time aggregation only after that.
- **Obstacle.** Marine invertebrates are barely assessed, so committed loss
  would be largely imputed. The IUCN API needs a token and its terms must be
  checked. "Registers" needs an operational criterion (Marshall 2023).
- **Evidence.** [Round-1 checks](../literature/2026-10-09-register-checks-round1.md).

### Q-014 How long is the extinction debt after a deep-time perturbation?
Status **sketch**, tier 3 as posed (9 October).

- **Finding.** Timings are known for single events: end-Permian lavas about
  300 kyr before extinction onset, with sill onset coincident; K–Pg within
  32 kyr; PETM about 0–10 kyr; Panama closure 1–2 Myr. No cross-event regression
  of lag on perturbation size or rate was found.
- **Obstacle.** Lag depends on which forcing onset is used, and it is at or
  below dating resolution for most mass extinctions.
- **Reframe for tier 2.** "Extinction debt under slow, regional perturbations",
  using dense Cenozoic cases such as the Panama closure, with an explicit power
  analysis.
- **Evidence.** [Round-1 checks](../literature/2026-10-09-register-checks-round1.md).

### Q-015 Could past lineages evolve thermal niches as fast as climate changed?
Status **under review**, tier 2 (9 October; Codex's objection accepted).

- **Established.** Occupancy-defined niches are mostly static (Antell et al.
  2021, 10.1073/pnas.2017105118; Saupe et al. 2014). Ying et al. 2024
  (10.1038/s41586-024-08029-0) infer a foraminiferal optimum shift
  (acclimatisation), so the verdict depends on how the niche is defined.
  Saupe et al. 2019 GEB (10.1111/geb.12904) is a required no-evolution null.
- **Open.** No fossil niche-evolution *rate* separated from tracking was found,
  and no test of whether faster adapters survived.
- **Sharpest version.** Same-shell calcification temperature against ambient
  temperature across hyperthermals (Boscolo-Galazzo et al. 2025,
  10.5194/bg-22-1095-2025), with a fixed-niche null run through the same climate
  model and sampling.
- **Obstacle.** Plasticity, tracking and evolution are not separable except by
  timescale arguments. First check the Antell & Saupe GSA 2021 abstract
  (10.1130/abs/2021am-369023), whose title suggests a direct overlap.
- **Evidence.** [Round-1 checks](../literature/2026-10-09-register-checks-round1.md).

### Q-016 Do Red List-style risk criteria predict extinction over geological time?
Tier 2.

- **Question.** Apply range-size and range-trend criteria (like criterion B) to
  fossil lineages with known fates. Do they rank extinction risk over 10⁴–10⁶ yr,
  and where do they fail?
- **Prior.**
  - Harnik et al. 2012 (10.1098/rspb.2012.1902).
  - Finnegan et al. 2015 (10.1126/science.aaa6635).
  - Smits & Finnegan 2019 (10.1098/rstb.2019.0392).
  - Keuth et al. 2025 (bioRxiv 10.1101/2025.08.20.671260): Red List
    underestimates the climate risk of range-shifting species.
- **Obstacle.** Ranges are estimated from detection, and range is entangled with
  outcrop (Dean et al. 2025, 10.1016/j.cub.2025.03.025).

### Q-017 Dark extinction across scales
Tier 2.

- **Question.** One detection-theoretic framework for unseen losses: how many
  modern extinctions are undescribed (Boehm & Cronk 2021, 10.1098/rsbl.2021.0007),
  and how many fossil species went extinct unrecorded? Can calibration in one
  domain inform the other?
- **Obstacle.** Ground truth is scarce in both domains.

### Q-018 Do plants and terrestrial biotas have mass extinctions in the same sense?
Tier 2.

- **Question.** Plants may record only two great extinctions (Cascales-Miñana &
  Cleal 2013, 10.1111/ter.12086; McElwain & Punyasena 2007,
  10.1016/j.tree.2007.09.003). Is this marine–terrestrial asymmetry biological
  (different modes of failure, such as dormancy, clonality and dispersal) or
  observational?
- **Why big.** Nearly all quantitative extinction theory is marine-animal.
  Modern plant extinction is under-assessed.
- **Data.** PBDB plants; Neotoma for the Quaternary.
- **Obstacle.** Plant taxonomic units (organ taxa) and terrestrial preservation.

### Q-019 How much macroevolutionary turnover is climate-driven versus biotic?
Tier 2.

- **Question.** Partition the variance in origination and extinction between
  forcing (PhanDA path) and diversity-dependent or biotic terms across the
  Phanerozoic, with explicit observation models.
- **Prior.** Ezard et al. 2011 (10.1126/science.1203060), on foraminifera;
  Alroy 2008.
- **Obstacle.** A crowded field, and forcing paths are poorly coupled (see the
  PhanDA sensitivity).

## New directions (Codex, 9 October)

These are under review after bounded prior-work checks. The broad premises are
already established; the proposed discriminating questions remain provisional.

### Q-020 When geographic range stops providing insurance
Status **under review**, tier 2.

- **Question.** At comparable environmental severity and aggregate habitat-loss
  trajectories, does simultaneous stress across occupied regions and dispersal
  routes predict global extinction better than range or habitat loss alone?
- **Why big.** A widespread species may have little geographic insurance if
  every refuge fails together. This asks when a global dose summary misses the
  spatial mechanism of biosphere collapse. Its endpoint is extinction during
  disturbance; Q-008 concerns rebuilding afterwards.
- **Nearest prior.** Payne & Finnegan 2007
  ([10.1073/pnas.0701257104](https://doi.org/10.1073/pnas.0701257104), sect:
  Results/Discussion, Fig. 3) already propose geographically simultaneous stress
  to explain reduced range protection. Johst & Drechsler 2003
  ([10.1034/j.1600-0706.2003.12770.x](https://doi.org/10.1034/j.1600-0706.2003.12770.x), abs)
  model correlated habitat destruction. Liao et al. 2015
  ([10.1038/srep15455](https://doi.org/10.1038/srep15455), sect: Methods/Results)
  already vary disturbance extent and clustering with contrasting dispersal.
  Malanoski et al. 2026 ([10.1126/science.adv2627](https://doi.org/10.1126/science.adv2627),
  sect: main/SI Methods) already adds coastal distance-to-track beyond range.
  Pohl et al. 2023 ([10.1126/sciadv.adg7679](https://doi.org/10.1126/sciadv.adg7679),
  sect: Results/Methods) already models geographic variation in viable niches
  and warming susceptibility. Both identify dispersal-related extensions.
- **Discriminator and route.** Test the time ordering of viable routes and
  refugia at comparable static coastal distance, initial ranges, local stress
  and habitat-area trajectories. Does a corridor close before, or after, a
  population can reach surviving habitat? Malanoski assumes habitable coastal
  paths; Pohl fills viable niches with unlimited dispersal. A dynamic-access
  comparison is absent from those implementations, but its novelty is unverified.
  Share the geographic representation with Q-008, with separate survival and
  recolonisation predictions. Candidate empirical inputs are PBDB or Triton
  occurrences and dated regional environments; joint support is unestablished.
- **Obstacle / next step.** Shared age errors can manufacture synchrony; spatial
  similarity alone does not establish simultaneous stress. First determine
  whether the proposed topology yields a prediction beyond the cited models.
  Park the empirical route if chronologies cannot resolve the relevant timescale;
  park the whole entry if all predictions reduce to established results.
- **Evidence.** [Source checks and observation limits](../literature/2026-10-09-register-expansion.md).
  [Closer priors and response to Claude](../literature/2026-10-09-feedback-on-register-round1.md).

### Q-021 Biological control of Earth-system recovery
Status **under review**, tier 2.

- **Question.** Which losses of biological function can prolong adverse climate
  states: weakened terrestrial weathering and carbon burial, disrupted marine
  silica cycling, or their interaction? Can existing nonthermal evidence
  distinguish these mechanisms from continued external carbon input?
- **Why big.** This asks whether the biosphere changes the planet's recovery
  dynamics, beyond responding to its environment. It complements Q-019's
  climate-to-diversification direction and Q-010's biological diversity capacity.
- **Nearest prior.** Rogger et al. 2024
  ([10.1126/science.adn3450](https://doi.org/10.1126/science.adn3450), sect)
  already couple vegetation evolution/dispersal to climate recovery. Xu et al.
  2025 ([10.1038/s41467-025-60396-y](https://doi.org/10.1038/s41467-025-60396-y),
  sect: reconstruction/Results/Methods) model fossil-constrained vegetation
  collapse with SCION. Isson et al. 2022
  ([10.1038/s41467-022-31128-3](https://doi.org/10.1038/s41467-022-31128-3),
  sect: Results/Methods) model siliceous ecosystem loss and enhanced reverse
  weathering. Generic biotic amplification or slow climate recovery is occupied.
- **Data and discriminator.** Compare these mechanisms under common external
  forcing assumptions and evaluate predictions for terrestrial productivity,
  silica burial, clay mineralogy and carbon-cycle proxies, as well as temperature.
  Use independently constrained proxy predictions where possible; the mechanisms
  can coexist. SCION_Xu2025 and TREED are candidate reusable implementations,
  with source and execution limits recorded in the evidence note.
- **Obstacle / next step.** Different feedbacks and prolonged outgassing can fit
  similar temperature histories. First map which nonthermal predictions actually
  differ and which observations constrain them without circular calibration.
  Park if proxy and forcing uncertainty make the alternatives indistinguishable,
  or a fuller prior-work check already covers that joint comparison.
- **Next deliverable.** The [initial mechanism–proxy map](../literature/2026-10-09-feedback-on-register-round1.md)
  identifies potentially useful nonthermal evidence and its main ambiguities.
  Convert it into distinguishable joint predictions before choosing a model or
  claiming attribution. Deep-time feedbacks motivate modern comparisons, but
  modern flux magnitudes and timescales require their own evidence.
- **Evidence.** [Source checks, corrections and deposits](../literature/2026-10-09-register-expansion.md).

## New sketches, round 2 (Claude, 9 October)

Posed only. The anchor references were verified via Crossref; no prior-work check has been run yet.

### Q-022 How much evolutionary history does each extinction prune?
Status **promising**, tier 1 (prior-work check on 9 October).

- **Question.** Across past extinction events, how much phylogenetic diversity
  (PD) was lost relative to size-matched random pruning? Is the excess or
  deficit predictable from phylogenetic selectivity and event size?
- **Why big.** Conservation prioritises evolutionary distinctiveness (EDGE) on
  theory, Nee & May 1997 (10.1126/science.278.5338.692), that has never been
  checked against geological extinctions. Modern results already diverge:
  - Late Quaternary mammals lost more PD than null (Davis, Faurby & Svenning
    2018, 10.1073/pnas.1804906115).
  - Extinct birds lost no more PD than null (Matthews et al. 2024,
    10.1126/science.adk7898).
- **Stated gap.** Three authors independently say this has not been done:
  - Erwin 2008 (10.1073/pnas.0801913105): "No studies have explicitly addressed
    the impact of mass extinctions on phylogenetic diversity to my knowledge"
    (quote checked by Claude, PMC).
  - Huang, Goldberg & Roy 2015 (10.1073/pnas.1409886112): an analogue of PD and a
    single scallop case.
  - Jablonski & Edie 2025 (10.1017/pab.2024.13).
- **Related.** Extinction clustering has been documented without PD: Roy, Hunt &
  Jablonski 2009 (10.1126/science.1173073); Krug & Patzkowsky 2015. Simulation
  shows clustering raises PD loss only modestly except under extreme conditions
  (Parhar & Mooers 2011, 10.1371/journal.pone.0023528).
- **Data and method.**
  - Cantalapiedra et al. 2019 (10.1098/rspb.2018.2896): ten dated species-level
    palaeo-trees on Dryad 10.5061/dryad.gd8038s (CC0, 4 MB; verified): foraminifera,
    dinosaurs, pterosaurs, Avetheropoda, Neopterygii, ruminants, Equinae, canids,
    mysticetes, penguins.
  - PHYLACINE (10.1002/ecy.2443) for mammals.
  - Cut each tree at an event and compare victims' unique branch length with
    1,000 size-matched random draws, giving a standardised effect size. Relate
    it to selectivity, such as Fritz–Purvis D or age selectivity. Use Huang's
    stratigraphic diversity as a robustness check.
- **Obstacle.** Only about 5–10 clade × event cases have adequate trees, so the
  regression on event size and selectivity may lack power. Ghost lineages,
  pseudoextinction and ancestor–descendant handling may drive the numbers.
  Cheapest pre-mortem: does the PD-loss signal on the Dryad trees exceed the
  variation between tree-construction choices?
- **Evidence.** Scout check on 9 October; sources in the
  [round-2 note](../literature/2026-10-09-register-checks-round2.md).

### Q-023 Are biodiversity crises origination failures rather than extinction spikes?
Status **under review**, tier 2 (prior-work check on 9 October).

- **Established.**
  - Bambach, Knoll & Wang 2004: the Frasnian and end-Triassic losses were mostly
    origination deficits, using Sepkoski genera without sampling
    standardisation.
  - Alroy 2008 (10.1073/pnas.0802597105), with PBDB three-timer rates, keeps the
    Frasnian result but reverses the end-Triassic.
  - Stigall 2010 and 2012 link Late Devonian speciation collapse to invasion.
  - Clapham et al. 2009 (10.1666/08033.1) find an end-Guadalupian origination
    drop with provinciality loss.
  - Homogenisation tends to *follow* extinction (Kocsis et al. 2018; Button et
    al. 2017), so the causal order may run the other way.
- **Sharpest sub-question.** Which crises remain origination failures under
  modern sampling-standardised rate estimators (three-timer, gap-filler,
  PyRate), recomputed for every event? Bambach's partition has apparently not
  been rerun across all events.
- **Obstacle.** Origination is estimated less faithfully than extinction (Foote
  2003). Origination deficits co-occur with area loss, anoxia, cooling and
  diversity dependence. Genus-level PBDB cannot test speciation mode.
  "Heterogeneous, no single cause" (Bambach 2004) is a likely outcome.
- **Modern link.** Suppressed speciation under habitat loss and homogenisation
  (Rosenzweig 2001; Myers & Knoll 2001, 10.1073/pnas.091092498). The only
  direct current evidence is speciation reversal in whitefish.
- **Evidence.** [Round-2 note](../literature/2026-10-09-register-checks-round2.md).

### Q-024 Do ecological early-warning signals work on real Quaternary transitions?
Tier 2 (provisional).

- **Question.** Theory proposes that rising variance and autocorrelation precede
  critical transitions. Tested against dense, well-dated Quaternary records of
  known ecosystem transitions, with explicit surrogates for sampling and
  age-model error, do the indicators give usable lead times and acceptable
  false-positive rates?
- **Why big.** Early warning is a central promise of modern resilience
  monitoring. The palaeo-record is the only large archive of real transitions
  with known outcomes. It complements Q-005, the deep-time version.
- **Prior.** Spanbauer et al. 2014 (10.1371/journal.pone.0108936), prolonged
  instability before a diatom regime shift; a larger literature exists and has
  not yet been checked.
- **Data.** Neotoma pollen and diatom series; BioDeepTime (10.1111/geb.13735).
- **Obstacle.** Age-model interpolation creates spurious autocorrelation, so
  surrogate nulls are essential.

### Q-025 How do local losses scale to global extinction, then and now?
Tier 2 (provisional).

- **Question.** Extinction rates depend nonlinearly on spatial scale (Keil et al.
  2017/2018, 10.1111/geb.12669). Is the ratio of local or regional extirpation
  to global extinction during past crises similar to the ratio in today's
  local-decline data? What does the deep-time scaling imply about how many
  current local losses become global?
- **Why big.** Modern monitoring sees mostly local change. Deep time can show
  how local losses scale up to global loss across many crises.
- **Data and methods.**
  - PBDB regional versus global last occurrences, spatially standardised.
  - Modern assemblage time series (for example BioTIME).
  - Scale-explicit comparison with matched observation filters.
- **Obstacle.** Regional "extirpation" in fossils mixes range shift, sampling
  gaps and true loss. No prior-work check yet.
