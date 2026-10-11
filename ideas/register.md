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

**First tranche: 50 questions; expansion paused for review (11 October 2026).**
Barry's instruction in Codex chat, quoted exactly:

> "Back to you. Let's get one more good question, to take the current list to 50, and then we'll pause and review the whole first tranche."

Q-050 completes this tranche. The pause supersedes the expand-each-round
cadence below until Barry resumes it. Existing statuses and tiers remain
provisional; no entry is promoted by reaching 50. The agents now lead phase-2
categorisation, prioritisation and deeper contextual/data work (Barry's
clarification on 11 October, 76/1476). His project selection comes later.
See [Claude's first pass](2026-10-11-phase2-portfolio-first-pass-claude.md) and
[Codex's response](2026-10-11-phase2-response-codex.md); neither changes the
entry statuses or tiers below.

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
5. **Separate "non-random" from "event-specific".** In the Q-022 pre-mortem,
   phylogenetic-diversity loss exceeded size-matched random pruning at ordinary
   times as well as at events.
   - Random pruning tests loss beyond exchangeable tips.
   - Whether an event differs from ordinary times needs background slices
     matched on size and loss fraction, or a process model, plus a power check
     (Codex, 10 October).
   - Pooled background percentiles are descriptive only.

## Index

| ID | Question | Status | Tier | Owner |
| --- | --- | --- | --- | --- |
| Q-001 | Does an end-Permian-calibrated physiological habitat-loss model transfer to other events? | parked | — | Claude |
| Q-002 | Is mass-extinction selectivity a switch or a continuous function of dose? | parked | — | Claude |
| Q-003 | Can stage-level data tell a warming–extinction threshold from a smooth response? | under review | 3 | Claude |
| Q-004 | A pseudoextinction-corrected background rate for modern comparisons | under review | 2 | Claude |
| Q-005 | Are there detectable precursors before extinction events? | under review | 2 | Claude |
| Q-006 | What can fossils identify about diversification that extant trees provably cannot? | under review | 3 | Claude |
| Q-007 | How long does a biotic loss leave a legacy, given the environmental path? | under review | 2 | Joint |
| Q-008 | Does geographic differentiation help determine subsequent recovery? | under review | 2 | Codex |
| Q-009 | Does ecological organisation retain predictive memory after richness recovers? | under review | 2 | Codex |
| Q-010 | Can biological innovation change how much diversity an environment supports? | under review | 2 | Codex |
| Q-011 | What sets the size distribution of extinction events: forcing or biotic amplification? | under review | 2 | Claude |
| Q-012 | Heritable susceptibility versus intrinsic ageing in extinction risk | under review | 2 | Claude |
| Q-013 | Would the current extinction register as a mass extinction in the rock record? | under review | 2 | Claude |
| Q-014 | How long is the extinction debt after a deep-time perturbation? | sketch | 3 | Claude |
| Q-015 | Could past lineages evolve thermal niches as fast as climate changed? | under review | 2 | Claude |
| Q-016 | Do range-based risk criteria predict extinction over geological time? | under review | 3 | Claude |
| Q-017 | Dark extinction across scales: one detection framework for unseen losses | under review | 2 | Claude |
| Q-018 | Do plants and terrestrial biotas have mass extinctions in the same sense? | under review | 2 | Claude |
| Q-019 | How much of macroevolutionary turnover is climate-driven versus biotic? | under review | 3 | Claude |
| Q-020 | When does geographic range cease to insure against global extinction? | under review | 2 | Codex |
| Q-021 | Which lost biological functions prolong Earth-system recovery? | under review | 2 | Codex |
| Q-022 | How much evolutionary history does each extinction prune? | under review | 2 | Claude |
| Q-023 | Are biodiversity crises origination failures rather than extinction spikes? | under review | 2 | Claude |
| Q-024 | Do ecological early-warning signals work on real Quaternary transitions? | under review | 2 | Claude |
| Q-025 | How do local losses scale to global extinction, then and now? | under review | 2 | Claude |
| Q-026 | Can we distinguish reversible clade decline from terminal decline before knowing the outcome? | under review | 2 | Codex |
| Q-027 | Is the latitudinal diversity gradient a climate-state variable? | under review | 2 | Claude |
| Q-028 | Do the winners of past crises share traits with today's winners? | under review | 2 | Claude |
| Q-029 | Does the sequence of geographic isolation and reconnection determine how much diversity lasts? | under review | 3 | Codex |
| Q-030 | Is the biosphere becoming less sensitive to environmental perturbation? | under review | 2 | Claude |
| Q-031 | Is shrinking under warming a predictable macroevolutionary response? | under review | 3 | Claude |
| Q-032 | Have insects had ecological crises that family counts miss? | parked | — | Claude |
| Q-033 | Can arrival order determine which clades radiate? | under review | 2 | Codex |
| Q-034 | What was the extinction rate of island endemics before people arrived? | under review | 2 | Claude |
| Q-035 | Do land ecosystems collapse before marine ones, and what sets the lag? | under review | 3 | Claude |
| Q-036 | What maintains morphological stasis as environments change? | under review | 3 | Codex |
| Q-037 | Is the present crisis's top-down trophic signature unprecedented? | under review | 3 | Claude |
| Q-038 | Bad genes or bad luck: how predictable is which genera die, and does it change in mass extinctions? | under review | 2 | Claude |
| Q-039 | Did Sepkoski's evolutionary faunas interact, beyond sharing limits and shocks? | sketch | 2 | Claude |
| Q-040 | Did marine diversity really rise since the Palaeozoic, and is a global curve the right estimand? | sketch | 2 | Claude |
| Q-041 | Is there periodicity in extinction once modern timescale uncertainty is propagated? | under review | 2 | Claude |
| Q-042 | How many species died in the great mass extinctions? | under review | 2 | Claude |
| Q-043 | Does survivor composition determine what can evolve next? | parked | — | Codex |
| Q-044 | Why is life on land so diverse if regional terrestrial richness is bounded? | under review | 2 | Claude |
| Q-045 | How robust are headline macroevolutionary estimates to future data? | parked | — | Claude |
| Q-046 | Did marine diversification increase total energy use or divide it among more taxa? | parked | — | Codex |
| Q-047 | When biotas meet: do past interchanges forecast today's biotic mixing? | under review | 2 | Claude |
| Q-048 | Can climate-driven predator decline reduce extinction risk for their prey? | under review | 2 | Codex |
| Q-049 | Did failure to track shifting isotherms predict extinction at past hyperthermals? | sketch | 2 | Claude |
| Q-050 | How does the capacity to evolve change during environmental upheaval? | under review | 2 | Codex |

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
Status **under review**, tier 2. Prior-work check on 10 October: the algebra
and some pseudoextinction fractions are published, but the correction has not
been applied to the background rates used for modern comparisons. This entry
is the umbrella for "what background rate should modern extinction be compared
with?"; Q-034 is its island-specific branch.

- **Question.** The common baselines of 1.8–2 E/MSY are fossil species-level
  rates μ\*: Barnosky et al. 2011 (10.1038/nature09678) and Ceballos et al.
  2015 (10.1126/sciadv.1400253). They include pseudoextinction. The about
  0.1 E/MSY baseline (De Vos et al. 2015, 10.1111/cobi.12380) comes from
  molecular phylogenies. It excludes pseudoextinction, but trees are limited by
  congruence classes (Louca & Pennell 2020, 10.1038/s41586-020-2176-1).
  - What happens to the fossil background, and to modern-to-background ratios,
    if the correction μ = μ\* − (λ\* − λ) is applied?
  - The correction lowers the background and raises the ratios. It works
    against Barnosky's point that phylogenetic species concepts inflate modern
    counts. Nobody has netted the two effects.
- **Prior.**
  - Silvestro et al. 2018 (10.1038/s41467-018-07622-y, full): λ\* − λ = μ\* − μ,
    with "3- to 18-fold rate differences" in Feliformia. No correction of
    background rates is proposed.
  - Archibald 1993 (10.1017/s0094837300012288, abstract checked by Claude):
    depending on the speciation model, "true extinction can be overestimated
    by as much as" several-fold in Paleocene mammals.
  - Strotz & Allen 2013 (10.1073/pnas.1208302110): anagenesis below 19% of
    Cenozoic foraminiferal speciation events.
  - Hagen et al. 2018 (10.1093/sysbio/syx082): mean longevity of Carnivora
    species is 2.0 Myr from fossils against 9.8 Myr from phylogenies.
  - In the rate-comparison papers checked, pseudoextinction is not mentioned:
    Barnosky 2011, Ceballos 2015, De Vos 2015, Spalding & Hull 2021 and Lamkin
    & Miller 2016.
- **Design.** For clades with both fossil and tree data (mammal clades,
  foraminifera), estimate λ\* − λ with the BDC model. Recompute background μ,
  and modern-to-background ratios, under both corrections at once.
- **Kill criterion.**
  - Park if a paper already applies the BDC correction to a background rate
    and reports the changed ratio.
  - Demote to a note if λ\* − λ is small against the existing twenty-fold
    spread of baselines in every clade with both data types.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

### Q-005 Precursors before extinction events
Status **under review**, tier 2. Prior-work check on 10 October: case studies
of biotic precursors exist, but no test of the generic indicators against a
sampling null was found.

- **Question (narrowed).** In high-resolution deep-time biotic series, do
  variance and autocorrelation of richness or occupancy rise before extinction
  pulses? The comparison must be against a surrogate that simulates
  instantaneous extinction under the observed sampling, and against a null of
  memoryless extinction rates. (Q-024 covers Quaternary ecological records.)
- **Prior.**
  - Swain et al. 2024 (10.1038/s41586-024-07337-9, full text by scout): in
    Triton planktonic foraminifera, a specialisation index rises about 2 Myr
    before the richness loss at the Eocene–Oligocene transition. The test uses
    logistic fits, not variance or autocorrelation. The authors call for
    research on "ancient community tipping points that precede extinction".
  - Single-section precursors:
    - Piazza et al. 2019 (10.1017/pab.2019.11): Toarcian shell size falls
      before richness.
    - Kießling et al. 2018 (10.1130/g39866.1): end-Permian ammonoid turnover
      and size decline.
    - Wang et al. 2014 (10.1666/13022): end-Permian deterioration about 1.2 Myr
      before the main loss; multi-phase claims attributed to Signor–Lipps and
      facies effects.
    - Huang et al. 2023 (10.1016/j.cub.2023.02.007): richness falls before
      food-web stability collapses.
  - Indicators on abiotic series only: Sudakow et al. 2026
    (10.1038/s41467-026-75655-9) apply AR(1) to isotopes.
  - Crampton et al. 2026 (10.1017/pab.2026.10107) is a rate-spectrum paper,
    not a precursor test. It supplies a graptoloid CONOP composite at
    0.125-Myr steps and a memoryless null.
- **Data.** The graptoloid CONOP composite; Triton.
- **Kill criterion.**
  - Park if a pilot shows the sampling surrogate alone reproduces the rise
    before an event.
  - Park if fewer than about three events have enough bins.
  - Merge if a published test of these indicators on biotic fossil series
    with a sampling null appears.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

### Q-006 Fossils versus trees: identifiability of diversification
Status **under review**, tier 3. Prior-work check on 10 October: the main
theoretical result is published.

- **Occupied.** Truman et al. 2025 (10.1093/sysbio/syae058, abstract checked by
  Claude): "widely used time-dependent fossilized birth–death (FBD) models are
  identifiable", for arbitrary rate functions, when the fossil sampling rate is
  strictly positive and sampled lineages stay in the process. Earlier results
  bound the problem:
  - Gavryushkina et al. 2014 (10.1371/journal.pcbi.1003919): sampling with
    removal is not identifiable.
  - Louca & Pennell 2020 (10.1038/s41586-020-2176-1): extant-only congruence.
  - Morlon et al. 2022 (10.1016/j.tree.2022.02.004) and Andréoletti & Morlon
    2023 (10.1111/2041-210X.14240) had listed the time-varying case as open.
- **Residual (narrow).**
  1. A power criterion. How large must fossil sampling be, relative to λ and
     μ, before the collapse of the congruence class gives usefully narrow
     intervals with finite data? Truman et al. note that no fixed finite
     quantity of data guarantees a given precision.
  2. Identifiability from occurrences alone, without a tree: PyRate-style
     range data. No theorem either way was found.
- **Practical relevance.** Beaulieu & O'Meara 2022 (10.1093/sysbio/syac049)
  find that fossils rarely beat extant-only analyses in practice. Upham et al.
  2021 (10.1016/j.cub.2021.07.012) fix fossil genus-level μ, which brings back
  the μ\* versus μ mismatch of Q-004.
- **Kill criterion.** Park if a minimum-sampling or power criterion, or an
  occurrence-only identifiability result, is found.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

## Joint and Codex-owned

### Q-007 Biotic legacy under a specified environmental path
Status **under review**, tier 2, joint (agreed 9 October; support limits below).

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
  Close & Reijenga 2025
  ([10.1073/pnas.2419052122](https://doi.org/10.1073/pnas.2419052122), Results,
  Discussion and Methods §§3.1–3.7 checked 11 October) already estimates
  species–area slopes and intercepts across North American K–Pg recovery.
  Another provinciality/recovery curve would occupy established ground;
  whether differentiation predicts subsequent recovery remains the target.
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
- **Evidence.** [Register expansion and source checks](../literature/2026-10-09-register-expansion.md);
  [round-10 closest-prior check](../literature/2026-10-11-interchange-transfer-and-spatial-temporal-support.md).

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

- **Boundary with Q-040 (10 October).** Retain both entries: reconstructing
  regional/global richness histories is distinct from identifying biological
  construction of capacity. Flat regional and rising global richness can
  coexist through geographic differentiation or changing habitable area.
  Agree taxonomic unit, spatial support and observation model before treating
  those patterns as rival predictions. See the
  [round-8 adjudication](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md).

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
  - The Big Five are not statistically distinct from background (Marshall
    2023, 10.1017/ext.2022.4, abstract checked by Claude). Graptoloid
    extinction-rate magnitudes form "a continuous, unimodal distribution"
    (Crampton et al. 2026, 10.1017/pab.2026.10107).
  - Raup's kill curve (1991, 10.1017/s0094837300010332) and its impact form
    (Raup 1992, 10.1017/s0094837300012227) attributed most pulsed extinction to
    impacts. Coincidence tests find no impact link beyond the K–Pg (Green et
    al. 2022). The strong form, a completeness-corrected impact flux run
    through the kill curve, is untested. It is a narrow sub-question here
    (round-7 legacy map).
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

### Q-016 Do range-based risk criteria predict extinction over geological time?
Status **under review**, tier 3. Narrowed on 10 October to range predictors,
by agreement with Codex (76/1300); Q-026 owns trajectory and rate-partition
predictors. Prior-work check the same day: partly occupied.

- **Question.** Take predeclared landmark times and use only data older than
  each landmark. Does range *trend* (contraction) add out-of-sample
  discrimination and calibration over absolute range size, taxon age and
  sampling effort, for extinction within 1, 2 and 5 Myr? Does fragmentation
  add more?
  - This is an analogy to IUCN criterion B (extent of occurrence, area of
    occupancy, fragmentation, continuing decline). It does not test literal
    IUCN thresholds: a decline in genus range is not a population reduction.
  - Where does range-based prediction fail? Break the results down by clade,
    interval, sampling completeness and proximity to mass extinctions.
- **Prior (partly occupied).**
  - **Smits & Finnegan 2019** (10.1098/rstb.2019.0392; abstract checked by
    Claude, sections by scout):
    - Data and model: Cenozoic plankton from Neptune, 1-Myr bins, Bayesian
      discrete-time survival.
    - Predictors include current range and range change. Range change is
      bundled with other history terms and never isolated.
    - Validation: expanding-window time-series cross-validation, with an
      out-of-sample pairwise rank accuracy of 70–80%. No calibration is
      reported.
    - Abstract: models with historical covariates or with time-varying effects
      "yield equivalent forecasts, but a model including both is overfit and
      yields biased forecasts".
  - **Straube et al. 2026** (10.1111/geb.70226, full by scout): Neogene–Holocene
    PBDB marine genera. For a given absolute range, the effect of range loss on
    extinction risk "largely disappears". Validation is leave-one-out only, with
    no temporal holdout.
  - **Casey, Saupe & Lieberman 2021** (10.1017/pab.2020.52, abs checked by
    Claude): late Palaeozoic brachiopods declined in abundance before extinction
    but showed no range contraction.
  - **Smith, Kocsis & Kiessling 2025** (10.5194/bg-22-3503-2025, full by scout):
    plankton occupancy and occupancy change, in-sample only. Predictive ability
    rises as temporal resolution coarsens.
  - **Earlier in-sample work:** Kiessling & Kocsis 2016 (10.1098/rsbl.2015.0813);
    Harnik et al. 2012 (10.1098/rspb.2012.1902).
  - **Peak range as a landmark** for extinction timing: Tietje & Kiessling 2013
    (10.1111/jbi.12030).
  - **Descriptive rise-and-fall occupancy:** Foote et al. 2007
    (10.1126/science.1146303); Liow & Stenseth 2007 (10.1098/rspb.2007.1006).
  - Finnegan et al. 2015 (10.1126/science.aaa6635) was not accessed beyond its
    abstract.
  - No fossil study was found that scores IUCN-style criteria against known
    outcomes, or that tests fragmentation as a predictor.
- **Residual.** Three things remain open:
  - an isolated, calibrated, landmark-frozen test of range trend and
    fragmentation;
  - criterion-analogue hit and false-alarm rates;
  - a map of where the criteria fail.
  This is a methodological and conservation-validation project, not a new
  mechanism. Hence tier 3.
- **Data.**
  - Neptune Sandbox Berlin (open; Renaudie et al. 2020) for foraminifera and
    nannofossils.
  - PBDB Neogene molluscs as a second system.
  - NOW for mammals; access terms not checked.
- **Design.**
  1. Forward-chain landmarks, for example every 5 Myr from 60 Ma.
  2. Fit nested models: effort and age; then add size; then trend; then
     fragmentation.
  3. Score Brier skill, calibration slope and intercept, and AUC.
  4. Use the Q-026 competing-risk machinery where useful.
- **Obstacle and kill criterion.**
  - A last occurrence is not extinction. Range is entangled with outcrop and
    detection: Dean et al. 2025 (10.1016/j.cub.2025.03.025) find that apparent
    occupancy decline tracks detection.
  - Macrofossil stages of about 5 Myr cannot resolve a 1–5 Myr horizon, so use
    microfossils first.
  - Kill the trend framing if trend adds no Brier or AUC gain over size, age
  and effort under standardised sampling. That would still be a useful negative
  result for criterion B.
- **Evidence.** [Round-3 note](../literature/2026-10-10-register-checks-round3.md).

### Q-017 Dark extinction across scales
Status **under review**, tier 2. Prior-work check on 10 October: each domain is
mature, and the bridge between them appears open.

- **Question (reframed).** Are the modern estimator of undetected extinctions
  and the fossil completeness estimator the same statistical object?
  - Modern: Chisholm et al. 2016 (10.1111/cobi.12640, abstract checked by
    Claude). It uses only "the first and last date at which each species ...
    was recorded", and assumes that extinction rate is independent of
    detection.
  - Fossil: Foote & Raup 1996 (10.1017/s0094837300016134, abstract checked by
    Claude). It estimates durations, preservation probability and completeness
    "given only the observed ranges".
  If they are equivalent, can a system with both records calibrate one against
  the other?
- **Why it matters.** Counts of unseen modern extinctions and of unrecorded
  fossil species enter every comparison between modern and fossil extinction
  (Q-004, Q-013, Q-034). The estimate of a lineage still alive at a landmark,
  from its sighting record, is the same machinery (Q-026, round-6 note).
- **Prior.**
  - **Modern.**
    - Tedesco et al. 2014: undiscovered share of extinctions 0.15–0.59.
    - Boehm & Cronk 2021 (10.1098/rsbl.2021.0007).
    - Cooke et al. 2023 (10.1038/s41467-023-43445-2): completeness is proxied
      by research effort.
    - Duncan et al. 2013 (10.1073/pnas.1216511110): mark–recapture on island
      fossils.
  - **Fossil.**
    - Valentine et al. 2006 (10.1073/pnas.0601264103): 308 of 1,292 living
      bivalve genera have no fossils.
    - Foote et al. 2019 (10.1144/jgs2019-061).
  - **Partial bridges.**
    - Krone et al. 2024 (10.1017/pab.2023.34) treat modern tetrapods as a
      future fossil record.
    - Alroy 2014 (10.1666/13074) and Alroy 2015 (10.1073/pnas.1508681112)
      transfer sighting methods.
  - In the full texts the scout read, the modern and fossil estimator
    literatures do not cite each other.
- **Design.**
  1. Establish equivalence, or the conditions for it, analytically.
  2. Run both estimators on one species set with independent ground truth:
     island birds with fossil and historical records, or Cenozoic molluscs
     with a living census.
- **Kill criterion.** Merge if a paper already proves equivalence or applies
  one estimator to both domains. Demote to a methods note if no system has
  both records with independent ground truth.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

### Q-018 Do plants and terrestrial biotas have mass extinctions in the same sense?
Status **under review**, tier 2. Prior-work check on 10 October: the asymmetry
is well documented, a near-occupant has appeared, and tests of biological
mechanisms are scarce.

- **Question (narrowed).** Is the marine–terrestrial asymmetry in mass
  extinction biological buffering (dormancy, seed banks, clonality,
  resprouting), or does it come from rank and sampling? Test it by projecting
  species-level losses to genus and family in both realms under the same
  preservation models. Does higher-rank survivorship alone reproduce the
  asymmetry?
- **Prior.**
  - **Near-occupant.** McElwain et al. 2026 (Research Square preprint,
    10.21203/rs.3.rs-9282628/v1, abstract checked by Claude) critically
    evaluate metrics for plant mass extinction. They apply concepts from the
    IUCN Red List of Ecosystems to fossil floras, and find "strong evidence for
    ecosystem collapse" at five events. This also bears on Q-016's use of IUCN
    criteria in deep time.
  - **Sampling explains part of it.** Nowak et al. 2019
    (10.1038/s41467-018-07945-w, abstract checked by Claude): evidence for an
    end-Permian plant mass extinction "is not robust", because Early Triassic
    gymnosperm macrofossils are undersampled.
  - **Rank explains part of it.** Wilf et al. 2023 (10.1017/ext.2023.13): K–Pg
    regional species losses generally above 50%, with no loss at family level.
    Thompson & Ramírez-Barahona 2023 (10.1098/rsbl.2023.0314): no phylogenetic
    signal of a K–Pg angiosperm mass extinction.
  - **The one explicit mechanism test.** Berry 2020 (10.35535/acpa-2020-0016):
    recalcitrant versus orthodox seeds at the K–Pg. It covers one event, with
    seed traits inferred from phylogeny.
  - **Framing.** Cascales-Miñana & Cleal 2013 (10.1111/ter.12086); McElwain &
    Punyasena 2007 (10.1016/j.tree.2007.09.003); Lucas 2021 (10.2517/2021pr004);
    Silvestro et al. 2015 (10.1111/nph.13247).
- **Kill criterion.**
  - Merge or demote if McElwain et al. is published with rank-standardised,
    sampling-corrected comparisons of plant and marine magnitudes.
  - Park if only the end-Permian and the K–Pg have plant species occurrences
    adequate for sampling-corrected rates.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

### Q-019 How much macroevolutionary turnover is climate-driven versus biotic?
Status **under review**, tier 3. Prior-work check on 10 October: the headline
answer is largely occupied.

- **Occupied.** Rineau et al. 2022 (10.1126/sciadv.add9620, abstract checked by
  Claude) analysed causal dependence in nine marine taxa across the
  Phanerozoic. "While the effect of environmental factors on origination and
  extinction rates is variable and taxon specific, the diversity dependence of
  the rates is almost universal".
  - Sampling was handled by pre-processing (SQS, gap-filler rates), not by an
    observation model.
  - No variance shares were reported.
- **Clade-level partitions.**
  - Ezard et al. 2011 (10.1126/science.1203060): in foraminifera, speciation is
    more diversity-dependent and extinction more climate-driven.
  - The PyRate multivariate birth–death model with joint preservation
    (Lehtonen et al. 2017, 10.1038/s41598-017-05263-7) has been applied to
    conifers and dinosaurs (Condamine et al. 2020, 10.1073/pnas.2005571117;
    2021, 10.1038/s41467-021-23754-0).
  - It has also been applied to Permian–Jurassic brachiopods and bivalves (Guo
    et al. 2023, 10.1038/s41467-023-41358-8), using a pre-PhanDA temperature
    curve.
  - Foote et al. 2018 (10.1098/rspb.2018.0122): diversity dependence explains
    "up to 12% of the variance" in graptoloids, with a warning about
    regression to the mean.
  - **Scale dependence.** Spiridonov & Lovejoy 2022 (10.1038/s41586-022-04867-y,
    meta; title "Life rather than climate influences diversity at scales
    greater than 40 million years"). Benton's 2009 framing
    (10.1126/science.1157719) has biotic factors local and short, and abiotic
    factors regional and long. Any partition should report its answer as a
    function of timescale.
- **Residual.** A hierarchical birth–death model across clades and the whole
  Phanerozoic, with a shared PhanDA covariate, lagged own-clade diversity and a
  preservation model. Report explained shares for origination and extinction
  separately, and test Ezard's pattern across clades.
- **Kill criterion.** Park if simulation under PBDB-like sampling shows the
  shares cannot be identified, because of collinearity, autocorrelation and
  regression to the mean. The PhanDA stage-coupling limits also apply.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

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
  Cao et al. 2022 ([10.1038/s41561-022-01009-x](https://doi.org/10.1038/s41561-022-01009-x),
  sect: main text/Methods) and Rauzi et al. 2024
  ([10.1073/pnas.2318860121](https://doi.org/10.1073/pnas.2318860121),
  sect: Results/Methods) supply Li-based reverse-weathering precedents with
  differing archive interpretations. These were missing from the initial map.
- **Data and discriminator.** Compare these mechanisms under common external
  forcing assumptions and evaluate predictions for terrestrial productivity,
  silica burial, clay mineralogy and carbon-cycle proxies, as well as temperature.
  Use independently constrained proxy predictions where possible; the mechanisms
  can coexist. SCION_Xu2025 and TREED are candidate reusable implementations,
  with source and execution limits recorded in the evidence note.
- **Obstacle / next step.** Different feedbacks and prolonged outgassing can fit
  similar temperature histories. The prediction/calibration map is complete:
  Xu prescribes vegetation recovery, Isson selects simulations on temperature,
  and Rogger 2025 prescribes climate recovery. These uses must be separated from
  evaluation evidence. Next check whether independently age-constrained land
  function and marine mineralogical records overlap through recovery.
  Park if proxy and forcing uncertainty make the alternatives indistinguishable,
  or a fuller prior-work check already covers that joint comparison.
- **Proposed discriminator.** Relative recovery of vegetation function and
  marine authigenic-clay formation, compared with cooling under a common,
  independently constrained carbon-forcing envelope. Asynchronous recovery could
  distinguish restricted mechanisms, but physical lag, proxy-to-flux conversion,
  spatial sampling and shared age errors may erase the contrast. Joint support
  is unverified; inspected stage-scale inputs do not establish this contrast.
  Li cross-prediction is an additional candidate, not a demonstrated stronger
  discriminator. Native models lack some required Li/vegetation outputs, so
  the next contract must map common observables and comparable nuisance
  assumptions, including reverse climate-to-vegetation effects. A record/age/
  evidence-role crosswalk precedes model harmonisation; non-use of a proxy in
  earlier fits alone establishes neither identification nor novelty.
- **Evidence.** [Source checks, corrections and deposits](../literature/2026-10-09-register-expansion.md).
  [Contrasting predictions and calibration roles](../literature/2026-10-11-q021-predictions-and-calibration.md).
  [Li evidence and native model capabilities](../literature/2026-10-11-q021-lithium-and-model-capability.md).

## New sketches, round 2 (Claude, 9 October)

Posed only. The anchor references were verified via Crossref; no prior-work check has been run yet.

### Q-022 How much evolutionary history does each extinction prune?
Status **under review**, tier 2. Moved down from promising/tier 1 on 9 October,
on Codex's precedent check and Claude's pre-mortem. Revised 10 October after
Codex's corrections (76/1306) and a matched-background follow-up.

- **Question.** In past extinction events, how much phylogenetic diversity
  (PD, the summed branch length) was lost? Two comparisons answer different
  questions, and both are needed:
  - against size-matched random pruning: was the loss beyond what
    exchangeable tips would give?
  - against ordinary times of similar size in the same trees: was the loss
    event-specific? An event-specific effect can be a deficit as well as an
    excess.
  Then: is the event-specific shift predictable from phylogenetic selectivity
  and event size?
- **Why it matters.** Conservation prioritises evolutionary distinctiveness
  (EDGE), partly on the theory that random extinction prunes little PD (Nee &
  May 1997, 10.1126/science.278.5338.692). Modern results diverge:
  - Late Quaternary mammals lost more PD than null (Davis, Faurby & Svenning
    2018, 10.1073/pnas.1804906115).
  - Extinct birds lost no more PD than null (Matthews et al. 2024,
    10.1126/science.adk7898).
  Deep time could show whether large events prune more history than their size
  implies, and whether that differs from ordinary times.
- **Prior work.** Novelty is withdrawn; the residual is a harmonised,
  power-calibrated comparison of event-specific branch-sum PD loss across mass
  extinctions.
  - **Huang, Goldberg & Roy 2015** (10.1073/pnas.1409886112) already measured
    branch-length PD loss for one fossil event against random loss: Californian
    scallops in the Plio–Pleistocene, with 25 of 50 species lost over 1,000
    time-calibrated trees. Loss was below the random expectation (Codex,
    author's PDF).
    - They also define stratigraphic diversity (SD), a separate quantity built
      from stratigraphic ranges. Their simulations show SD and PD can move in
      opposite directions.
    - SD and mean pairwise distance (MPD) are therefore complementary
      quantities, not robustness checks for PD.
  - **Krug, Congreve & Patzkowsky 2015** (AbSciCon abstract 7737): Late
    Ordovician PD loss on a preliminary strophomenid brachiopod tree.
  - **Edie et al. 2025** (10.1126/sciadv.adv1171): K–Pg phylogenetic
    restructuring, measured with MPD rather than branch-sum PD.
  - **Flannery-Sutherland et al. 2026** (10.1093/evolut/qpag116): an
    early-vertebrate supertree with extinction-clustering results.
  - **Gap statements.** Erwin 2008 (10.1073/pnas.0801913105; quote checked by
    Claude) and Jablonski & Edie 2025 (10.1017/pab.2024.13) describe the field
    as thin. Given the precedents above, they do not establish novelty.
  - **Clustering without PD:** Roy, Hunt & Jablonski 2009
    (10.1126/science.1173073); Krug & Patzkowsky 2015
    (10.1371/journal.pone.0144354).
  - **Simulation:** clustering raises PD loss only modestly, except under
    extreme conditions (Parhar & Mooers 2011, 10.1371/journal.pone.0023528).
- **Pre-mortem** ([data/q022-premortem](../data/q022-premortem/README.md)).
  - *Data.* Four Cenozoic events on the open dated trees of Cantalapiedra et al.
    2019 (10.1098/rspb.2018.2896). The trees were retrieved from the Royal
    Society's Figshare mirror (CC BY 4.0), because the Dryad deposit
    (10.5061/dryad.gd8038s, CC0) refuses unauthenticated download.
  - *Method.* Exact random-pruning null, 100 posterior trees per clade, three
    windows.
  - *Against random pruning.* Event loss mostly exceeds it (median SES +0.7 to
    +1.8). So does loss at ordinary times: clustered loss is common in these
    trees.
  - *Against background matched on lineage count and loss fraction:*
    - All eight testable clade × window cases sit above the matched median, by
      +0.1 to +1.7 SES.
    - Three reach the matched 95th percentile at the median tree.
    - Most shifts are below an illustrative Gaussian detectable shift of
      1.5–2.7 SES. These eight positive contrasts are descriptive and
      correlated; they do not establish an event-specific effect (Codex
      76/1340).
    - The first comparison, against pooled background, was too negative
      (Codex 76/1306).
  - *Noise.* Tree uncertainty and window choice move SES by as much as the
    effects.
  - *Scope.* The Big Five cannot be tested on these trees: in the dinosaur tree
    every lineage is lost, and the other Mesozoic trees lack an absolute anchor.
- **Data for a real study.**
  - Fossil-inclusive dated trees that span mass extinctions *with* survivors:
    brachiopods (Krug & Patzkowsky), bivalves (Edie et al. 2025), ammonoids,
    and early vertebrates (Flannery-Sutherland et al. 2026).
  - PHYLACINE (10.1002/ecy.2443) for the Late Quaternary comparison.
- **Method.**
  1. Cut each tree at the event and compute lost branch-sum PD.
  2. Use the exact random null (closed-form mean and variance) for loss beyond
     exchangeable tips.
  3. Test event specificity against matched-background slices or a process
     model.
  4. Before testing any event, calibrate on the same trees. Measure false
     positives against ordinary-time clustered loss fitted to the background,
     and power for incremental event effects above it. Report the induced
     clustering and PD-loss distributions
     ([design](../data/q022-premortem/README.md#next-gate-power-calibration-design-not-run)).
  5. Relate the event-specific shift to selectivity (Fritz–Purvis D, age
     selectivity) and event size. Report MPD and SD alongside PD, not as
     substitutes for it.
- **Obstacle and kill criterion.** Only about 5–10 clade × event cases are
  available. Ghost lineages, pseudoextinction, sampled ancestors and tip-dating
  artefacts can produce clustered loss at all times. Park if either holds:
  - power calibration on the available mass-extinction trees cannot detect
    shifts of the size seen here (about 1–2 SES);
  - those trees lack survivors across the events.
- **Evidence.**
  - [Round-2 note](../literature/2026-10-09-register-checks-round2.md)
  - Codex's [precedent note](../literature/2026-10-09-pd-loss-and-clade-recovery.md)
  - Codex's [10 October review](../literature/2026-10-10-clade-futures-and-geographic-cycles.md)
  - [Pre-mortem README](../data/q022-premortem/README.md)

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
Status **under review**, tier 2. Posed 9 October; a prior-work check on 10
October found it partly occupied. It is kept and reframed as a calibration
study.

- **Question.** Take many dated pollen sequences (diatoms and chironomids
  second). Define abrupt compositional transitions independently of any
  indicator. What are the hit rate, the false-alarm rate and the lead-time
  distribution of rolling autocorrelation and variance, and of an estimator for
  irregular sampling? Measure them against matched stable controls, with
  surrogates run through the same pipeline and with age-model ensembles.
- **Why it matters.** Resilience indicators are already being applied at scale
  to palaeo records without that validation. Liao et al. 2025 (bioRxiv,
  10.1101/2025.10.24.684258, abstract checked by Claude) apply them to 482
  pollen records and infer a millennia-long decline in vegetation resilience.
  Whether such inferences mean anything depends on this calibration.
- **Prior (partly occupied).**
  - **Monitored, non-palaeo data with false-positive accounting.** Burthe et
    al. 2016 (10.1111/1365-2664.12519, abstract checked by Claude): true
    positives in only 9–13% of cases, and "False positives were more prevalent
    than false negatives". Further studies:
    - Gsell et al. 2016 (10.1073/pnas.1608242113) had no controls;
    - O'Brien et al. 2023 (10.1038/s41467-023-43744-8) found most indicators
      no better than chance.
  - **Palaeo pitfalls.**
    - Carstensen, Telford & Birks 2013 (10.1038/nature12272) show that
      interpolation and aggregation mimic the signal; the original authors'
      reply has not been read.
    - Taranu et al. 2018 (10.1002/ecs2.2438) show that smoothing in sediment
      cores degrades rolling autocorrelation, and call for broad syntheses.
  - **Single-core ecological cases:** Spanbauer et al. 2014
    (10.1371/journal.pone.0108936); Beck et al. 2018 (10.1002/2017jg004135).
  - **Palaeoclimate, not ecology:**
    - Dakos et al. 2008 (10.1073/pnas.0802430105): eight transitions, with no
      age uncertainty and no controls;
    - Hennekam et al. 2020 (10.1029/2020gl089183);
    - Bury et al. 2021 (10.1073/pnas.2106140118).
  - **Prosecutor's fallacy:** Boettiger & Hastings 2012
    (10.1098/rspb.2012.2085). Conditioning on observed transitions inflates
    false positives.
- **Data.** LegacyPollen 1.0 and LegacyAge 1.0 (10.5194/essd-14-3213-2022;
  10.5194/essd-14-1331-2022): 2,831 records with Bacon age models. BioDeepTime
  stores only median ages, so the age ensembles must be regenerated.
- **Design.**
  1. Define transitions from compositional change with support across the age
     ensemble.
  2. Choose controls matched on sample count, spacing and accumulation rate.
  3. Build stationary surrogates at the true sample ages, passed through the
     same aggregation, age draws and interpolation.
  4. Endpoints: true-positive rate at a 5% false-positive rate, and AUC with
     site-clustered bootstrap.
- **Kill criterion.** Park if fewer than about 30 transitions survive
  screening for length and resolution. Dakos et al. 2008 found strong signals
  only in series with more than 450 points. An AUC interval spanning 0.5, or
  lead times under two sampling intervals, would be a useful negative result.
- **Evidence.** [Round-6 note](../literature/2026-10-10-register-checks-round6.md).

### Q-025 How do local losses scale to global extinction, then and now?
Status **under review**, tier 2. Posed 9 October; prior-work check on 10
October found it partly occupied, with the cross-scale conversion itself
apparently open.

- **Question.** Two estimands. State which one each analysis targets, and keep
  both denominators (Codex, 10 October).
  - (a) **Unconditional conversion.** C(A) = P(global extinction within a fixed
    horizon | extirpation at grain A), with per-species loss against area, in
    crisis and background intervals.
  - (b) **Conditional spatial allocation.** At matched global severity, how
    is loss distributed across grains? Matching on severity answers (b), not
    (a).
  Both need one taxonomic unit, explicit eligibility at baseline, and a common
  follow-up horizon.
  - Local abundance decline is not local extirpation.
  - Global threat status is not observed global extinction.
  - Comparing regional species loss with global family survival (as in Wilf
    et al. 2023) mixes taxonomic rank with spatial grain.
  Does today's local-loss data fall inside the crisis envelope or the
  background envelope, once it is put on the same unit and filter?
- **Why it matters.** Modern monitoring mostly sees local change. Deep time is
  the only place where many local and regional losses have known global
  outcomes.
- **Prior.**
  - **Modern theory and data, no fossils.** Keil et al. 2018
    (10.1111/geb.12669; preprint sections by scout): per-species loss falls
    with area, and "simple interpolation between scales should be done with
    caution, if at all". Chase et al. 2019 (10.1111/oik.05968) and Yan et al.
    2022 (10.1111/ecog.05828) add to this.
  - **Local trends against global threat.** Antão et al. 2026
    (10.1038/s41467-026-74132-7, abstract checked by Claude): over 60,000
    populations of 2,362 species. Fewer than 10% of populations show
    consistent trends. Higher IUCN risk goes with more frequent local decline.
    The link is correlational, with no conversion across scales.
  - **Fossil, regional rates.**
    - Allen et al. 2023 (10.1017/pab.2023.1, abstract checked by Claude):
      Permian–Triassic extinction rates "generally uniform across latitudes",
      with a caution about sampling bias.
    - Flannery-Sutherland et al. 2022 (10.1038/s41467-022-30507-0): regional
      rates are heterogeneous, and global trends are biased by the regional
      fossil record.
    - Raup & Jablonski 1993 (10.1126/science.11537491): K–Pg bivalve
      intensities "uniformly global".
  - **Fossil, local against global.** Wilf et al. 2023 (10.1017/ext.2023.13,
    abstract checked by Claude): K–Pg plant losses "primarily occurred among
    species observed in regional studies but left no global trace at the
    family or major-clade level". Regional losses were generally above 50%.
    This illustrates the conversion problem for one event and one group, but
    it compares species with families, so rank and grain are confounded.
  - **Range trend predicting extinction:** Kiessling & Kocsis 2016
    (10.1098/rsbl.2015.0813); Straube et al. 2026 (10.1111/geb.70226). See
    Q-016.
  - **Same-region modern versus fossil rates:** Neubauer et al. 2021
    (10.1038/s43247-021-00167-x), for European freshwater gastropods.
- **Residual.** Estimate C(A) and per-species loss against area at four or
  more nested grains:
  - through and outside crises;
  - with spatial standardisation (Close et al. 2020, 10.1126/science.aay8309;
    Antell et al. 2020, 10.1016/j.cub.2019.10.065);
  - with regional estimators tested in simulation (Allen 2023);
  - for estimand (b), comparing crisis and background stages at matched global
    severity.
  Then place modern local-loss data (Keil 2018's datasets, BioTIME, IUCN as in
  Antão 2026) on the same observation filter.
- **Kill criterion.** Before estimating anything, run a sampling null:
  stationary global ranges on the real occurrence geometry. Park if that null
  reproduces the observed fractions of regional loss, because the record then
  cannot separate range shift, sampling gaps and true loss.
  - Second obstacle: the time grain differs by orders of magnitude between the
    fossil and modern records.
  - Few modern global extinctions exist, so C(A) for today will be imprecise.
- **Evidence.** [Round-5 note](../literature/2026-10-10-register-checks-round5.md).

## New sketch (Codex, 9 October): clade recovery versus terminal decline

### Q-026 Can we distinguish reversible clade decline from terminal decline before knowing the outcome?
Status **under review**, tier 2. Revised 10 October after Claude's critiques
(76/1272, 1320, 1347, 1362); predictive novelty and prospective data support remain
unverified.

- **Question.** Among clades already declining at a specified time, can their
  preceding richness trajectory and origination/extinction partition predict
  rebound, continued low diversity or extinction? Does proportional diversity
  add predictive value beyond absolute richness, net decline, environmental
  information and sampling?
- **Why big.** Survival through a crisis does not guarantee a future radiation.
  Knowing which declines can reverse would connect immediate losses to the
  longer-term replacement of major branches of life. This concerns clade fate;
  Q-009 concerns ecosystem state, and Q-012 inherited lineage susceptibility.
- **Nearest prior.** Jablonski 2002
  ([10.1073/pnas.102163299](https://doi.org/10.1073/pnas.102163299), abs/opening
  results) establishes survival without recovery. Barnes et al. 2021
  ([10.1073/pnas.2019208118](https://doi.org/10.1073/pnas.2019208118), abs/design)
  documents widespread, persistent decline among marine orders. Song et al.
  2026 ([10.1038/s41559-026-03134-x](https://doi.org/10.1038/s41559-026-03134-x),
  abs, reporting summary, supplementary tables, author responses and selected
  code; final main Methods gated) proposes declining proportional diversity
  followed by environmentally triggered extinction in 12 extinct marine clades.
  Quental & Marshall 2013
  ([10.1126/science.1239431](https://doi.org/10.1126/science.1239431), full main
  article) already partition contributions to temporary increases within clade
  decline. Neither inspected analysis establishes the proposed held-out
  prediction. The broad mechanism is occupied; predictive novelty is unverified.
- **Data and discriminator.** Song's public
  [data/code repository](https://github.com/haijunsong/Clade-extinction)
  contains SQS/PyRate materials (selected files inspected at `80f6258`; no
  workflow run). Its surviving comparator groups are denominator pools, not
  an assembled cohort of declining clades that later recover. Establish all
  eligible declining clades at predeclared landmark times, including later
  recoveries, persistent small
  clades and censored histories. Fit predictor histories only to data ending
  at each landmark; whole-history smoothing can leak the outcome. Hold out
  clades/events rather than randomly splitting correlated time slices. Separate
  a first rebound from sustained recovery and from extinction before rebound,
  over common horizons. A small birth–death counterexample shows that at the
  same net decline, higher turnover can raise both rebound and extinction
  probabilities; rate partition does not imply a universal risk ordering.
- **Baseline and endpoint contract.** Compare against a prefix-fitted
  birth–death model only when its rates describe the counted biological unit.
  Silvestro et al. 2018
  ([10.1038/s41467-018-07622-y](https://doi.org/10.1038/s41467-018-07622-y),
  relevant Results/equations) separates fossil turnover from branching/loss.
  A verified example adds one-for-one replacement, increasing apparent
  turnover without changing lineage-count rebound/extinction probabilities.
  Stable focal-clade membership alone does not solve constituent-taxon coding.
  A model of richness increments is a candidate alternative, but instantaneous
  standing count is not sampled-in-bin richness: successive names can both
  appear within one bin. SQS replicate variance alone does not account for
  that aggregation or all observation uncertainty.
  True boundary counts solve the ideal aggregation example. Observed
  boundary crossers reconstructed from fossil ranges remain sensitive to
  detection and replacement; the new synthetic check confirms this even at
  constant true richness. Such counts also require later fossils, so they
  cannot be used at their own boundary as prefix-only predictors. Either fit
  a latent-state/observation model to the prefix, or use older boundaries
  whose full detection window ends before the actual forecast cutoff.
  Three-timer and capture–recapture corrections were not evaluated in the
  check; their failure is not established.
  Claude's prefix-only survival-probability sum is a candidate model, but
  summing over previously observed names omits the expected surviving unseen
  component. A probability model and consistent lineage/name units are needed;
  a last-sighting test's p-value is not a posterior survival probability.
  Prefix truncation solves future-information leakage, not those remaining
  observation problems. No proposed correction has yet been fitted.
  Keep first threshold crossing distinct from confirmed persistence. For a
  two-observation rule, confirmation occurs at the second qualifying observation;
  the comparator must retain qualification history and allow intervening failure.
  Unequal bin durations and unobserved reversals require explicit treatment.
- **Obstacle / next step.** Full-history decline descriptions are not evidence
  of prospective prediction. A lower share can arise without loss of focal
  genera, and richness share is not ecological dominance. The next data gate
  is one concrete cohort with a defensible mapping from latent standing counts
  to observations, plus support for later recoveries and non-recoveries using
  the same eligibility, sampling and follow-up rules. Rate uncertainty must
  propagate through predictions. A departure from the baseline is not uniquely
  biological: taxonomy and observation misspecification are rival explanations.
  Park if that predictive comparison is already occupied or cannot be assembled.
  No universal 0.13 threshold or irreversible fate is assumed. Codex owns this
  trajectory question; Claude owns Q-016's range-based predictors, with an
  explicit analogy rather than literal transfer of IUCN criteria.
- **Evidence.** [Original sketch](../literature/2026-10-09-pd-loss-and-clade-recovery.md);
  [landmark design, source check and counterexample](../literature/2026-10-10-clade-futures-and-geographic-cycles.md);
  [rate units, confirmation and observation limits](../literature/2026-10-10-prediction-units-and-priority.md);
  [boundary-count observation and cutoff check](../literature/2026-10-10-boundary-counts-and-incumbency.md);
  [prefix-only model qualification](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md).

## New sketches, round 3 (Claude, 9 October)

### Q-027 Is the latitudinal diversity gradient a climate-state variable?

Status **under review**, tier 2. Posed 9 October as a tier-1 sketch. Moved down
on 10 October after a prior-work check: partly occupied.

- **Question.** Does the shape of the latitudinal diversity gradient (LDG)
  follow continuous global climate state, and with what lag, once regional
  sampling bias is controlled? The sharpest form is a live identification
  dispute: is the warm-interval mid-latitude peak (a tropical dip) real?
  - Boag et al. 2021 explain it with a metabolic hump.
  - Benson et al. 2025 attribute it to intense sampling in Europe and North
    America.
- **Why it matters.** Modern tropical marine richness is dipping under warming
  (Chaudhary et al. 2021, 10.1073/pnas.2015094118). Planktonic foraminifera
  show that the modern tropical dip began with post-glacial warming about
  15,000 years ago (Yasuhara et al. 2020, 10.1073/pnas.1916923117; abstract
  checked by Claude).
  - *Correction (10 October):* the sketch said Yasuhara et al. showed the same
    in past warm intervals. They did not; their record runs from the last
    glacial maximum to the present.
  - Deep time is the only place to see whether hothouses hollow out the
    tropics.
- **Prior (partly occupied).**
  - **Benson et al. 2025** (10.1111/pala.70006; abstract checked by Claude,
    sections by scout): a direct Phanerozoic test.
    - Design: PBDB marine genera, spatial and coverage standardisation, local
      model SST, hothouse versus icehouse classes.
    - The LDG "was shallower on average when Earth's climate was hotter,
      although this signal is weak".
    - Only 36 of 99 stages were usable.
    - Strong Europe/North America sampling bias "may have led previous studies
      to incorrectly infer a mid-latitude diversity peak during warm
      intervals".
    - No lag was tested.
  - **Boag, Gearty & Stockey 2021** (10.1016/j.cub.2021.04.021; abstract checked
    by Claude, full text by scout): molluscs over 145 Myr. Diversity is a
    non-monotonic function of temperature, matching a model that combines
    metabolic kinetics with the Metabolic Index. Spatial sampling bias was not
    modelled.
  - **Marcot et al. 2016** (10.1073/pnas.1524750113): for Cenozoic North
    American mammals, LDG strength varies with global temperature and is
    weakest in warm periods.
  - **Fenton et al. 2023** (10.1038/s41586-023-05712-6) and **Fenton et al.
    2016** (10.1098/rstb.2015.0224): planktonic foraminifera, 40–0 Ma.
    - The modern-style gradient emerged 15–10 Ma, about 20 Myr after cooling
      began.
    - The model of the modern diversity–environment relationship transfers to
      the mid and late Eocene but not to the early Eocene.
  - **Model-only:** Balembois et al. 2025 (10.1038/s41467-025-63428-9) and
    Ontiveros et al. 2023 (10.1038/s41467-023-41685-w).
  - **Power warning:** Jones et al. 2021 (10.1098/rspb.2020.2762) show that
    sampling windows obscure gradient type, worst at 200–20 Ma.
  - **Opposite-sign case:** Powell 2007 (10.1111/j.1466-8238.2007.00300.x)
    reports a gentler gradient at the onset of glaciation.
- **Residual.**
  1. Replace binary regimes with continuous local SST and PhanDA global mean
     temperature, with region random effects.
  2. Test whether Boag's hump survives Benson-grade regional control.
  3. Use Triton foraminifera, from ocean drilling, as an independent Cenozoic
     replicate whose coverage is less biased towards Europe.
  4. **Lags.** PhanDA's stages are assimilated independently, so it has no
     joint temporal posterior. A lagged coefficient fitted on PhanDA inherits
     that limit; adding the term alone does not resolve it (Codex, 10 October).
     - Test lags first in the Cenozoic: Triton foraminiferal gradients against
       the continuous, astronomically dated CENOGRID benthic record (Westerhold
       et al. 2020, 10.1126/science.aba6853), at sub-stage resolution.
     - For the Phanerozoic, report lags only under the explicit stage-coupling
       scenarios of
       [data/phanda-stage-differences](../data/phanda-stage-differences/README.md),
       as a sensitivity analysis.
- **Data.**
  - Benson et al.'s Dryad data (10.5061/dryad.6djh9w1bx) and Zenodo code
    (10.5281/zenodo.15269136), both DataCite-verified by the scout.
  - PBDB, and Triton (10.1038/s41597-021-00942-7).
  - Climate: PhanDA (10.1126/science.adk3705) and Valdes et al. 2021 HadCM3
    stage simulations (10.5194/cp-17-1483-2021).
- **Data support (11 October; [support screen](../data/q027-joint-support/README.md), [Codex audit](../data/q027-support-audit/README.md)).**
  - Source: Benson et al.'s Zenodo archive (CC BY 4.0), with its 2022 PBDB
    download of non-chordate marine animals. Barry has since supplied the
    Dryad companion files. They hold only PBDB CSV downloads and a README, nothing
    beyond the Zenodo archive.
  - **Screen result.** Requiring at least 10 occupied cells per palaeolatitude
    band (0–20°, 20–40°, ≥40°) *outside* Europe and North America, 26 of 95
    stages pass, under full stage containment. That is 27 before Codex's
    fixes: unknown countries no longer count as outside, and the era
    boundaries were corrected.
  - **What the count means (revised after Codex's audit).** It is the output
    of one conservative presence screen, not a ceiling or a power design. The
    first version's "possible in only a handful of warm stages" is withdrawn.
    - The source's age rule (more than 50% of an occurrence's age range in
      one stage) gives 46 passing stages, including the Turonian and
      Lutetian. It does so by admitting records that spill into neighbouring
      stages.
    - Requiring at least 2 outside collections per cell drops the count
      to 14.
    - The two effects run in opposite directions; their joint effect is
      unknown.
  - **Next gate.** A support contract specific to the estimator (age rule,
    midpoint palaeocoordinates, dggridR cells, modal-region exclusion,
    coverage eligibility, region identity), before any power simulation.
    Proposed as next work, not yet allocated.
- **Kill criterion.** Before any empirical fit, run a power simulation on the
  real sampling windows (in the style of Jones et al. 2021). Park if the
  climate–slope coefficient cannot be recovered.
  - Confound: continental configuration and shelf area are collinear with
    climate state.
  - Fallback: well-sampled windows (Cenozoic foraminifera, Permian–Triassic,
    Late Triassic).
- **Evidence.** [Round-3 note](../literature/2026-10-10-register-checks-round3.md).

### Q-028 Do the winners of past crises share traits with today's winners?
Status **under review**, tier 2. Posed 9 October; prior-work check on 10
October.

- **Question.** Three questions, which the literature tends to blur.
  - (i) Which traits predict *survival*? This is occupied.
  - (ii) Among survivors, do traits coded only from the stage before a crisis
    predict post-crisis *dominance*? Dominance means sampling-standardised
    occupancy or abundance in the first post-event bins. Radiation (descendant
    richness) is a separate outcome.
  - (iii) Does a model trained on past events discriminate modern winners
    (species increasing in assemblage time series, successful invaders) beyond
    a range-only baseline?
  Questions (ii) and (iii) are the residual.
- **Why it matters.** McKinney & Lockwood 1999 (10.1016/s0169-5347(99)01679-1)
  framed the current crisis as a few winners replacing many losers. If
  post-crisis dominance is predictable from pre-crisis traits, deep time shows
  what the winners of the present crisis will be like and how long they will
  dominate.
- **Prior.**
  - **Dominance described, not predicted.** Aftermath faunas are "dominated by
    widespread, eurytopic species" (Erwin 1998, 10.1016/s0169-5347(98)01436-0,
    abs). Further descriptions:
    - disaster taxa (Rodland & Bottjer 2001,
      10.1669/0883-1351(2001)016<0095:brftep>2.0.co;2);
    - Early Triassic dominance (Petsios & Bottjer 2016, 10.1017/pab.2015.47);
    - survival without recovery (Jablonski 2002, 10.1073/pnas.102163299).
  - **Named as open.** Jablonski & Edie 2025 (10.1017/pab.2024.13, full by
    scout) list it among open questions: "Why do some clades rebound from
    taxonomic and morphologic bottlenecks, while others remain in the collapsed
    state?"
  - **Transfer is poor.** Foster et al. 2023 (10.1098/rsos.221507; abstract
    checked by Claude) trained trait models on one of the end-Permian,
    end-Triassic and end-Cretaceous events and tested on the others. They found
    selectivity "inconsistent", with poor prediction, and attribute this to the
    Mesozoic Marine Revolution. That is survival, not dominance, and a critique
    exists (Reddin et al. 2023, 10.1098/rsos.230400; title only).
  - **Modern selectivity differs.** Modern ocean threat tracks large body size
    (Payne et al. 2016, 10.1126/science.aaf2416).
  - **No pervasive modern winner profile:** Terry 2021
    (10.1038/s41559-021-01624-8); Santini 2019 (10.1111/ele.13199).
  - **Range is the only trait tested:** Newbold et al. 2018
    (10.1371/journal.pbio.2006841) find that land use favours widespread
    species.
  - **Outcome is contingent:** Edie, Collins & Jablonski 2025
    (10.1126/sciadv.adv1171) call the K–Pg outcome "contingent".
- **Design.**
  1. Fit a pre-registered two-stage hurdle model: survival, then dominance
     given survival. Fix the dominance outcome, its time window, the
     eligibility rules and the predictors before evaluation.
  2. Train on one event and hold out the others.
  3. Compare against a range-only baseline.
  4. Code living genera the same way. Define winners in advance from BioTIME
     and invasion status, with covariates for human transport.
  "Winner" is the future outcome being predicted. Define it in advance, and
  freeze predictors and eligibility at the landmark (Codex, 10 October).
  - A survivor-conditional trait forecast is a valid predictive target.
  - It is not, by itself, a causal effect of the trait.
  - It need not transfer between events with different survival filters.
- **Data.**
  - PBDB.
  - Modern: BioTIME (10.1111/geb.12729), GRIIS (10.1038/sdata.2017.202),
    Seebens first records (10.1038/ncomms14435).
  - Physiology: metabolic-index models (10.1126/science.aat1327).
- **Kill criterion.** Park if, on held-out events, dominance given survival is
  predicted no better than by range alone. Park also if past-event models fail
  to discriminate modern winners once human transport is included.
  - Related obstacle: dominance and radiation can decouple, because traits that
    make clades widespread can lower diversification (Faurby & Antonelli 2018,
    10.1111/jbi.13411).
- **Not accessed.** The full text of McKinney & Lockwood 1999 (403). If it
  already asserts a post-extinction winner profile, the profile is an old
  conceptual claim, and only the test is open.
- **Evidence.** [Round-3 note](../literature/2026-10-10-register-checks-round3.md).

## New sketch (Codex, 10 October): geographic cycles and durable diversity

### Q-029 Does the sequence of geographic isolation and reconnection determine how much diversity lasts?
Status **under review**, tier 3 (10 October, after Claude's 76/1362 critique).
Broad timing mechanisms occupied;
residual novelty and joint data support unverified. The Pontocaspian empirical
route is on hold pending independent chronology and comparable observations.
The remaining ordering/sufficiency refinement does not yet justify a larger
investigation. A new application must earn its own prior-work and data check.

- **Question.** For comparable habitat area and average isolation, does the
  ordering or clustering of geographic fragmentation and reconnection predict
  lasting lineage accumulation? When do speciation pulses leave diversity that
  survives reconnection, rather than transient richness?
- **Why big.** This concerns how changing planetary geography creates and
  retains diversity. It distinguishes production of taxa from durable diversity,
  and could explain why comparable geographic states have different histories.
  Q-008 concerns recovery after biotic loss; Q-020 concerns extinction insurance.
- **Nearest prior.** Zaffos et al. 2017
  ([10.1073/pnas.1702297114](https://doi.org/10.1073/pnas.1702297114), abs/opening
  Results) already associate continental fragmentation and marine richness.
  Aguilée et al. 2018
  ([10.1038/s41467-018-05419-7](https://doi.org/10.1038/s41467-018-05419-7),
  relevant Results/Methods) separate switching pace from isolation fraction;
  pace changes turnover without necessarily changing stationary richness.
  Princepe et al. 2024
  ([10.1093/evolut/qpad210](https://doi.org/10.1093/evolut/qpad210), named
  primary Methods/Results/Discussion passages via publisher index) compare
  irregular history with regular isolation/contact cycles, so duration-dependent
  speciation and persistence are occupied. Freitas et al. 2024
  ([10.1093/jeb/voae035](https://doi.org/10.1093/jeb/voae035), Methods/opening
  Results, with further indexed sections) already track phylogenetic consequences,
  pooling fusion and extinction as disappearance. A generic timing or
  fragmentation hypothesis is therefore insufficient.
- **Data and discriminator.** PBDB and independently dated regional geography
  are candidate inputs; an adequate paired record is not yet established.
  Compare models in which geographic timing affects only turnover with models
  predicting persistence of newly generated lineages. A theory contrast can
  hold area, mean isolation, switching counts and duration distributions fixed
  while changing their ordering. Empirical comparisons need repeated regional
  contrasts, observation-process controls, and validation outside the fitted
  region/interval. Local first appearances must not be assumed to be origination.
  Follow cohorts defined before reconnection over a common horizon, separating
  production, immediate losses and later persistence. Final richness favours
  recently produced taxa; selecting only post-contact survivors misses immediate
  losses. Lineage ages also need treatment. Completion/fusion time ratios are
  candidate mechanistic scales, not demonstrated sufficient summaries of history.
- **Strongest rival / kill criterion.** Reconnection changes immigration,
  ecological sorting and preserved rock, producing apparent diversity change
  without lasting lineage production. Park if the exact test is already done,
  dates cannot resolve the cycles, geography cannot be separated from sampling,
  or only a single global trend is available. Another two-patch simulation
  without a consequential new prediction does not earn a downstream project.
- **Regional gate / next.** Krijgsman et al. 2019
  ([10.1016/j.earscirev.2018.10.013](https://doi.org/10.1016/j.earscirev.2018.10.013),
  sections 4.2–4.5/Fig. 14) supplies Pontocaspian orientation, not an assembled
  cohort dataset. Some connections are inferred from the same shared fauna
  that would be the biological response; salinity and taxonomy also matter.
  If a consequential application earns further work, the bounded data check
  is two episodes with independent physical chronology and comparable
  taxonomic follow-up. Park this empirical route if
  either condition fails. Neither the exact ordering contrast nor two-ratio
  sufficiency was established in inspected model sections; inaccessible
  supplements prevent an absence claim.
- **Evidence.** [Original source comparison](../literature/2026-10-10-clade-futures-and-geographic-cycles.md);
  [closer priors and regional support limits](../literature/2026-10-10-prediction-units-and-priority.md);
  [tier adjudication](../literature/2026-10-10-boundary-counts-and-incumbency.md).

## New sketches, round 4 (Claude, 10 October)

Anchor DOIs were verified in Crossref; access depth is given per source. Q-030
and Q-031 were checked against prior work on 10 October
([round-4 note](../literature/2026-10-10-register-checks-round4.md)); Q-032 has
not been checked yet.

### Q-030 Is the biosphere becoming less sensitive to environmental perturbation?
Status **under review**, tier 2. Posed 10 October; a prior-work check the same
day found it partly occupied. The idea has been argued in words, and disputed,
but not quantified.

- **Question.** For a perturbation of independently estimated size, did the
  extinction response decline through the Phanerozoic, for example across the
  mid-Mesozoic? Three explanations compete for any decline:
  - **Forcing:** carbonate buffering improved after pelagic calcifiers.
  - **Response:** biotas were sorted towards robust, low-turnover clades.
  - **Geography:** palaeogeography and climate state changed.
  How much of the change in response lies between clades (composition), and
  how much within them (slope)?
- **Why big.** Deep-time dose–response estimates, such as temperature
  thresholds for mass extinction, pool the whole Phanerozoic. If sensitivity
  has fallen, those estimates overstate the risk for today's biota. If the
  decline is in forcing rather than response, they do not. The answer affects
  every transfer question here (Q-001, Q-003, Q-013).
- **Prior.**
  - **Stated in words.** Clapham & Renne 2019
    (10.1146/annurev-earth-053018-060136; abstract checked by Claude, full text
    by scout) explain the varied outcomes of flood basalts by "the rate of
    volatile release modulated by longer trends in ocean carbon cycle buffering
    and the composition of marine ecosystems". They note (p. 293) that "the
    only post-Jurassic hyperthermal to trigger even moderate extinction was
    Cenomanian OAE2". Payne et al. 2020 (10.1098/rsfs.2019.0106) list the same
    candidate causes. Neither paper estimates or tests them.
  - **Disputed.**
    - Green, Renne & Keller 2022 (10.1073/pnas.2120441119): extinction
      magnitude scales with LIP eruptive rate across all ages. They describe
      the pattern as explicable "without invoking a state change in ecosystem
      stability" (scout).
    - Henehan & Witts 2023 (10.1073/pnas.2303700120) reply with the title
      "Continental flood basalts do not drive later Phanerozoic extinctions".
    - No time term was fitted on either side.
  - **The composition side, partly done.** Wang & Bush 2008 (10.1666/07060.1,
    abstract checked by Claude) estimate a class-level taxonomic susceptibility
    that "has generally declined through the Phanerozoic", and adjust extinction
    rates for it. They use no independent forcing. Gilinsky 1994
    (10.1017/s0094837300012926) and Foote 2000 attribute declining rates to the
    loss of high-turnover taxa.
  - **The geography side, in models.** Pohl et al. 2023 (10.1126/sciadv.adg7679,
    abstract checked by Claude) find early Palaeozoic extinction susceptibility
    an order of magnitude higher, from climate and continental configuration.
    The result holds at present-day pO₂. Stockey et al. 2021
    (10.1073/pnas.2101900118) instead emphasise pO₂.
  - **Forcing proxies.**
    - Rothman 2017 and 2019 (10.1126/sciadv.1700906; 10.1073/pnas.1905164116):
      the size of a carbon-isotope excursion partly reflects the carbon cycle's
      own dynamics.
    - Bachan et al. 2017 (10.2475/06.2017.01): excursion amplitude declines
      through the Phanerozoic, independently of extinction.
    - Li et al. 2021 (10.7185/geochemlet.2137): extinction against a δ13C
      turbulence index for 41 events, with Cambrian–Silurian outliers.
    - Song et al. 2021 (10.1038/s41467-021-25019-2): ΔT pooled over 45 bins of
      about 10 Myr.
  - **Selectivity changes:** Foster et al. 2023 (10.1098/rsos.221507).
  - **The forcing-side model test may already exist.** Ridgwell & Zeebe-era
    carbonate-cycle modelling has not been read.
- **Residual (not found in a bounded search).**
  1. Estimate extinction per unit of independently estimated forcing, using
     ΔT, LIP eruptive rate or carbon mass as separate proxies.
  2. Let that sensitivity vary through time, with a mid-Mesozoic break and a
     free breakpoint.
  3. Partition the change in mean sensitivity between clades and within them.
     The between-clade term is Σ Δw_c β_c(pre); the within-clade term is
     Σ w_c(post) Δβ_c.
  The forcing side can be tested in an Earth-system model: carbon pulses of
  equal size in time slices with and without a pelagic carbonate sink. This
  would suit the kunanyi allocation once the jumpbox is open.
- **Data.**
  - PBDB, via divDyn.
  - PhanDA (10.1126/science.adk3705).
  - LIP eruptive rates and CO₂ estimates from the Green 2022 supplement.
  - Carbon-isotope event tables (Rothman 2017).
- **Gate and kill criterion.**
  - First count the post-Jurassic events that have forcing estimated
    independently of extinction. Park the empirical route if there are fewer
    than about 8–10.
  - Park it also if the era interaction changes sign with the extinction metric
    or the binning.
  - Then only the model test of forcing and a composition-only partition remain.
- **Evidence.** [Round-4 note](../literature/2026-10-10-register-checks-round4.md).

### Q-031 Is shrinking under warming a predictable macroevolutionary response?
Status **under review**, tier 3. Posed 10 October; a prior-work check the same
day found the headline occupied.

- **Question (residual).** Across warming events with lineage-resolved data,
  does the *within-lineage* size change per °C match the experimental
  temperature–size rule for that size class and habitat? Does the share of
  change produced by turnover (extinction, origination, immigration) rise with
  the size or duration of warming? Does the response reverse on cooling?
- **Headline occupied.** Nätscher, De Baets & Kiessling 2026
  (10.1073/pnas.2505564123; abstract checked by Claude, preprint full text by
  scout) compiled about 9,000 body-size changes in marine ectotherms.
  - Dwarfing is general in crises, and larger in hyperthermals than in other
    events.
  - Greater warming brought greater dwarfing. The slope is shallow: −0.018
    lnRR per °C, R² 0.018 (preprint Fig. 3).
  - ΔT is one value per event, and there is no within- versus among-lineage
    partition.
  - The scout found no comparison with the temperature–size rule.
  - Their open data are on Zenodo (10.5281/zenodo.15096088, CC BY 4.0).
- **Event-level partitions disagree, even within one event.**
  - Within-lineage shrinkage dominates in:
    - Permian–Triassic foraminifera (Rego et al. 2012, 10.1666/11040.1);
    - Toarcian belemnites (Rita et al. 2019, 10.1098/rsos.190494);
    - PETM and ETM2 equids (Secord et al. 2012, 10.1126/science.1213859;
      D'Ambrosia et al. 2017, 10.1126/sciadv.1601430; ETM2 −14% mass at about
      3 °C).
  - Turnover dominates in:
    - Permian–Triassic bivalves of the Dolomites (Foster et al. 2026,
      10.5194/bg-23-1181-2026, abstract checked by Claude). They do "not find a
      species-level body size reduction to be a forecastable response", and
      surviving species did not shrink.
    - Permian–Triassic ostracods (Nätscher et al. 2023, 10.1111/pala.12667).
    - Toarcian bivalves (Piazza et al. 2020, 10.1038/s41598-020-61393-5).
  - Both act in PETM mammals: an extended Price equation shows shrinking by
    within-lineage change and immigration, while species selection favoured
    *larger* species (Rankin et al. 2015, 10.1098/rspb.2015.1097, abstract
    checked by Claude).
- **Experimental reference.** Forster et al. 2012 (10.1073/pnas.1210460109):
  about −5% mass per °C in aquatic and −0.5% per °C in terrestrial animals of
  about 100 mg dry mass. Oxygen-limitation theory predicts size dependence
  (Deutsch et al. 2022, 10.1073/pnas.2201345119). Verberk et al. 2021
  (10.1111/brv.12653) argue the temperature–size rule is itself evolved, so
  "plastic versus adaptive" cannot be separated. The discriminator is therefore
  within- versus among-lineage change, plus consistency with the rule.
- **Design.**
  1. Apply one decomposition to at least 8 event × taxon series: disappearance,
     within-lineage change, and appearance or immigration (Rego/Price style).
  2. Use local ΔT with uncertainty.
  3. Fit a hierarchical regression of within-lineage Δln mass on ΔT, converting
     length to mass explicitly.
  4. Compare with the size-class expectation from the temperature–size rule.
- **Kill criteria.**
  - Park if fewer than 8 events have both lineage-resolved data and
    event-specific ΔT.
  - Park also if the published PNAS supplement already contains the partition,
    or the comparison with the temperature–size rule. It was not accessed
    (403).
  - The terrestrial and mammal arm is outside Nätscher's compilation and may be
    the larger gap.
- **Evidence.** [Round-4 note](../literature/2026-10-10-register-checks-round4.md).

### Q-032 Have insects had ecological crises that family counts miss?
Status **parked**. Posed 10 October; parked the same day after a prior-work
check.

- **Question (as posed).** Can plant–insect damage records serve as a proxy for
  insect abundance or interaction intensity? Do they show crises at events
  where insect family counts show only turnover (Schachat & Labandeira 2021,
  10.1093/aesa/saaa042)?
- **Why parked.**
  1. **The proxy is uncalibrated for abundance.**
     - Azevedo-Schmidt, Meineke & Currano 2022 (10.1073/pnas.2202852119,
       abstract checked by Claude) find modern total damage frequency "greater
       than any fossil locality" from 66.8 to 2.06 Ma, "despite widespread
       insect declines".
     - That is not a failed calibration. They measured leaf damage, not insect
       abundance. Their Discussion keeps both greater per-capita feeding and
       greater population density as explanations. Broad reports of decline
       are not a paired host/site abundance series (Codex, 10 October).
     - Carvalho et al. 2014 (10.1371/journal.pone.0094950) calibrate damage
       against herbivore richness, not abundance.
     - The safe conclusion is that damage cannot be assumed to measure
       abundance. It remains an endpoint for ecological interactions.
  2. **The clearest case is already done.** At the K–Pg, specialised
     associations almost disappeared while family counts show no loss
     (Labandeira, Johnson & Wilf 2002, 10.1073/pnas.042492999). Currano et al.
     2021 (10.1016/j.palaeo.2021.110636; 66 censuses) and Labandeira & Wappler
     2023 (10.1146/annurev-ento-120120-102849) restate it.
  3. **Other events.** The end-Permian has no usable floras with damage data
     for about 5 Myr of the Early Triassic (Labandeira et al. 2016,
     10.1371/journal.pone.0165205). At the end-Triassic, a test exists and
     found almost no change in damage (Xu et al. 2024,
     10.3389/fevo.2023.1338865). That is contrary evidence for the hypothesis,
     not a missing test.
- **What remains, small.** Schachat et al. 2022
  (10.1016/j.revpalbo.2021.104564) propose, but do not run, a test of whether
  change after an event exceeds expected change without it. It could be run on
  open census data: Currano 2021 on Zenodo (10.5281/zenodo.7242861), and Xiao
  et al. 2025 (10.1073/pnas.2412036122) on Dryad.
- **Revisit if** either of these appears:
  - a modern calibration showing that damage frequency tracks herbivore
    abundance at the same hosts and sites;
  - Early Triassic floras with damage censuses.
- **Evidence.** [Round-5 note](../literature/2026-10-10-register-checks-round5.md).

## New sketch (Codex, 10 October): arrival order and radiation

### Q-033 Can arrival order determine which clades radiate?
Status **under review**, tier 2 (10 October). Mechanism, generic model and
repeated deep-time replacement occupied; the proposed establishment-order
discriminator's novelty and data support are unverified.

- **Question.** Does earlier establishment itself change later diversification
  and persistence, beyond habitat, antecedent traits and source-pool opportunity?
  When does historical priority determine the identity of major radiations?
- **Why big / boundary.** This tests a mechanism by which historical contingency
  could shape major branches of biodiversity. Q-009 asks about predictive
  ecosystem state, Q-028 about winner traits, and Q-029 about geographic cycles;
  this question concerns the effect of arrival order itself, including outside
  extinction/recovery episodes.
- **Nearest prior.** Reijenga, Murrell & Pigot 2021
  ([10.1111/ele.13766](https://doi.org/10.1111/ele.13766), primary Methods and
  relevant Results) compare resident advantage, invader advantage and symmetric
  competition. A slowdown in diversification is not diagnostic of priority.
  Muschick et al. 2018
  ([10.1098/rspb.2018.0462](https://doi.org/10.1098/rspb.2018.0462),
  Introduction/Results/Table 1) already test a simple priority explanation
  using Lake Victoria fossil teeth. Neither generic modelling nor fossil
  testing alone is a new contribution.
  Rosenzweig & McCord 1991
  ([10.1017/S0094837300010563](https://doi.org/10.1017/S0094837300010563),
  official abstract only) describe repeated provincial turtle replacement
  limited by incumbent extinction; full methods remain inaccessible.
  Brusatte et al. 2008
  ([10.1126/science.1161833](https://doi.org/10.1126/science.1161833), main
  author manuscript) already challenge general dinosaur superiority.
  Carrillo et al. 2020
  ([10.1073/pnas.2009397117](https://doi.org/10.1073/pnas.2009397117), full main
  text and selected deposited code) attribute interchange asymmetry mainly
  to South American native extinction. Two-way dispersal is not a matched
  test of reversed establishment order.
- **Data and discriminator.** Seek repeated regional contrasts in which
  comparable clades exchange early/late arrival roles. Compare subsequent
  persistence and diversification over fixed follow-up, modelling antecedent
  environment, traits, source pools and observation. Local resident advantage
  predicts a change with arrival role; fixed intrinsic superiority predicts
  the same clade tends to succeed across roles. Environment-dependent
  superiority remains a rival. PBDB and regional stratigraphic compilations
  are leads, not a verified dataset. The published model and its official
  [simulation deposit](https://doi.org/10.5522/04/14400947.v1) provide a
  starting comparator; metadata inspected, archive/code not executed.
  Carrillo's [versioned deposit](https://doi.org/10.5281/zenodo.3770348) is a
  regional-support lead. Its diversification input excludes immigrant genera
  also recorded on their source continent; it does not compare the same genera
  in both roles. The occurrence table retains locality and age-bound fields,
  but continental origin labels do not date local establishment.
- **Next / kill criterion.** First build a bounded support matrix for one
  guild, two competing clades and two recipient regions: A-before-B and
  B-before-A, overlapping antecedent environments, source-pool support and
  comparable follow-up. Only then test model discrimination under fossil-like
  sampling and dating uncertainty. Do not infer causation from arrival rank or richness
  imbalance alone. Park if dating erases the relevant sequence, role reversal
  cannot be supported, or the exact contrast is occupied; merge if it reduces
  to Q-009 or Q-028. No new fieldwork or large archive download is proposed.
  The initial crossed pair is a support gate, not an identified causal design.
  Replicated reversals are needed, but no fixed three-to-four-pair threshold
  rules out clade-by-environment effects. Test a specified rival model using
  actual dating and sampling support; persistence of island ecomorphs alone
  does not establish arrival order.
- **Evidence.** [Source comparison and design limits](../literature/2026-10-10-prediction-units-and-priority.md);
  [deep-time precedents and deposited-code check](../literature/2026-10-10-boundary-counts-and-incumbency.md);
  [replication qualification](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md).

## New sketches, round 5 (Claude, 10 October)

Posed only. Anchor DOIs were verified in Crossref; access depth is given per
source. No prior-work check has been run yet.

### Q-034 What was the extinction rate of island endemics before people arrived?
Status **under review**, tier 2. Posed 10 October; a prior-work check the same
day found it partly occupied. It is closely related to Q-004 (a background
rate for modern comparisons) and could merge into it.

- **Question.** For islands with dated strata from before people arrived,
  estimate four things:
  - each island's extinction hazard for endemics before and after human
    arrival, under one shared preservation and detection model;
  - how much of the pre-human hazard sea-level-driven change in island area
    explains;
  - how widely quoted multipliers change when the denominator is island
    endemics;
  - how they change when the baseline is each island's own pre-human rate.
- **Why it matters.** Cooke et al. 2023 (10.1038/s41467-023-43445-2; full text
  checked by scout, abstract by Claude) report the about-1300 CE bird
  extinction wave as "approximately 80 (60–95) times the background extinction
  rate, here set to 2 E/MSY". The rate is computed over all 10,865 living
  birds. Published background rates range from about 0.1 E/MSY (De Vos et al.
  2014, 10.1111/cobi.12380) to 2 E/MSY (Ceballos et al. 2015,
  10.1126/sciadv.1400253). That twenty-fold range alone moves the headline
  multiplier twenty-fold.
- **Prior (partly occupied).**
  - **Rozzi et al. 2023** (10.1126/science.add8606; abstract checked by Claude,
    sections by scout): island mammals, 1,231 extant and 350 extinct species
    over 23 Myr. Arrival of modern humans "accelerated extinction rates more
    than 10-fold" (median 16.7-fold over the pre-modern-human background).
    The model has no sea-level or climate term. Data are on Figshare and code
    on GitHub. **Nearest prior**, for mammals.
  - **Fernández-Palacios et al. 2025** (10.1093/pnasnexus/pgaf215, abstract
    checked by Claude): 220 Macaronesian extinctions. Half match human
    occupation. Crude pre- and post-human rates without a detection model;
    pre-human losses are dominated by land snails.
  - **Pre-human losses tied to sea level and climate:**
    - Bermuda: Olson & Hearty 2003, 10.1073/pnas.1934576100.
    - Bahamas: Steadman & Franklin 2017, 10.1073/pnas.1707660114; 2020,
      10.1073/pnas.2013368117.
    - Galápagos: Steadman et al. 1991, 10.1016/0033-5894(91)90021-V.
    - New Zealand: Holdaway et al. 2001, 10.1080/03014223.2001.9518262, a
      fauna stable for about 100 kyr; Worthy et al. 2026,
      10.1080/03115518.2025.2605684, with 33–50% avian turnover over 1 Myr.
  - **Detection models that assume no pre-human extinction** (Duncan et al.
    2013, 10.1073/pnas.1216511110) cannot supply the baseline.
  - **Sea-level island-area model to reuse:** Rijsdijk et al. 2014
    (10.1111/jbi.12336).
- **Residual.** Per-island or per-archipelago baselines for birds and other
  vertebrates, under a shared detection model with area through time as a
  covariate, used to rescale Cooke-type multipliers. Candidate systems:
  Bahamas, Bermuda, New Zealand, the Gymnesics, the Canaries, Kaua'i.
- **Data.** Rozzi et al.'s Figshare and GitHub deposit; Cooke et al.'s Zenodo
  deposit (10.5281/zenodo.10014585, not opened); island fossil compilations.
- **Kill criterion.** Park if the best-sampled islands have too few dated
  pre-human horizons. The posterior pre-human rate would then span 0.1 to
  2 E/MSY, and the result would collapse to an upper bound or duplicate Rozzi
  et al.
- **Evidence.** [Round-6 note](../literature/2026-10-10-register-checks-round6.md).

### Q-035 Do land ecosystems collapse before marine ones, and what sets the lag?
Status **under review**, tier 3. Posed 10 October; a prior-work check the same
day found the concept published and the premise contradicted within one
event.

- **Question (revised).** Across volcanic-driven crises, is the gap between
  marine and terrestrial onset (Δ = marine onset − terrestrial onset) a
  function of palaeolatitude and of the phase of large-igneous-province
  activity? Is it larger at those events than at the K–Pg impact, after dating
  uncertainty is propagated?
- **Prior.**
  - **The concept is published.** Pálfy et al. 2000
    (10.1130/0091-7613(2000)28<39:ttemef>2.0.co;2; title checked by Claude,
    full text by scout) is titled "First on land, then in the sea?". They
    proposed a shorter response time or lower threshold in terrestrial biotas,
    and argued against a single impact cause. Their marine age has since been
    superseded (Lindström et al. 2017, 10.1016/j.palaeo.2016.12.025).
  - **End-Permian: the lag is quantified, reviewed and modelled.**
    - Fielding et al. 2019 (10.1038/s41467-018-07934-z) and Mays et al. 2020
      (10.1130/b35355.1): about 300–370 kyr at high southern latitudes.
    - Dal Corso et al. 2022 (10.1038/s43017-021-00259-4), a review.
    - Dal Corso et al. 2020 (10.1038/s41467-020-16725-4) and Li et al. 2026
      (10.1038/s41467-026-74636-2) model a cascade from land to sea.
  - **The premise reverses within the same event.** Wu et al. 2024
    (10.1126/sciadv.adi7284, abstract checked by Claude): the terrestrial
    extinction "occurred diachronously with latitude, beginning at high
    latitudes during the late Changhsingian and progressing to the tropics by
    the early Induan, spanning a duration of nearly 1 million years". The
    tropical collapse came after the marine onset. Chu et al. 2024
    (10.1130/g52655.1): North China precedes South China. This supersedes the
    tropical reading of Chu et al. 2020.
  - **Sceptical view:** Lucas 2021 (10.2517/2021pr004) doubts that nonmarine
    mass extinctions exist at several events, which would leave Δ undefined
    there.
- **Residual.** A compilation across events in one framework, not found in a
  bounded search:
  1. Define each realm's onset as a change-point.
  2. Put both realms on one Bayesian age frame.
  3. Fit Δ against palaeolatitude, LIP phase and event, propagating dating
     error.
  First tranche: recompute the end-Triassic lag with current ages.
- **Kill criterion.** Park if Δ cannot be distinguished from zero in at least
  two of three LIP events with paired high-precision records. Dating errors
  (±60–100 kyr) are already comparable to the lags.
- **Evidence.** [Round-6 note](../literature/2026-10-10-register-checks-round6.md).

## New direction (Codex, 10 October): morphological stasis and geography

### Q-036 What maintains morphological stasis as environments change?
Status **under review**, tier 3 (10 October, round 8). The simple geographic
decomposition is occupied. Pause the current empirical route until a distinct
mechanism-specific prediction and crossed spatial/temporal support are found.

- **Question.** How much long-term morphological stability persists after
  accounting for geographic redistribution and change within comparable local
  units? Can spatially resolved fossils distinguish those contributions well
  enough to explain when stasis is maintained or breaks down?
- **Why big / boundary.** Long-lived forms persist through major environmental
  changes despite the possibility of rapid evolution. Explaining that stability
  connects population processes with macroevolutionary patterns. Stabilizing
  selection, habitat tracking and population replacement can coexist; they are
  not mutually exclusive alternatives. Q-015 addresses thermal-niche evolution,
  Q-031 warming-associated size changes; this concerns multi-trait stasis and
  its spatial maintenance beyond crisis intervals.
- **Nearest prior.** Hunt 2007
  ([10.1073/pnas.0704088104](https://doi.org/10.1073/pnas.0704088104), Methods
  and relevant Discussion) distinguishes patterns of stasis from mechanisms.
  Hopkins & Lidgard 2012
  ([10.1073/pnas.1209901109](https://doi.org/10.1073/pnas.1209901109), relevant
  Results/Discussion/Methods) demonstrates differing modes among traits and
  discusses geographic sampling, migration and replicate-section comparisons.
  Raia et al. 2012
  ([10.1098/rsbl.2011.0613](https://doi.org/10.1098/rsbl.2011.0613), main text)
  already associates mammal movement with longevity and clade-level disparity.
  Hunt et al. 2015
  ([10.1073/pnas.1403662111](https://doi.org/10.1073/pnas.1403662111), relevant
  Results/Discussion/Methods) already obtains broad fossil mode frequencies
  from climate-tracking simulations. Neither finding stasis nor proposing
  geographic/environmental tracking alone is new.
  Lieberman, Brett & Eldredge 1995
  ([10.1017/S0094837300013051](https://doi.org/10.1017/S0094837300013051),
  official abstract) directly analyse population-level change beneath overall
  stasis in two Devonian brachiopod lineages. Slattery et al. 2025
  ([10.1017/pab.2025.10046](https://doi.org/10.1017/pab.2025.10046), main
  Methods and relevant Results/Discussion) test climatic variability and stasis
  in nuculid bivalves; lineage, climate regime and geological time differ together.
- **Data and discriminator.** The
  [Dryad trait-series compilation](https://doi.org/10.5061/dryad.m010p)
  is a locator and comparator, not yet a spatial dataset (landing page and
  usage notes only). Seek crossed locality × time morphometry, independent
  facies/environmental information, several traits and sample distributions.
  Separate within-unit change from changes in the weights of sampled units;
  test predictions for spatial covariance and held-out local trajectories.
  An unchanged pooled mean alone cannot identify the process. Repeated samples
  at one locality do not prove continuity of the biological population.
- **Data-contract result / next gate.** Kim, Sheets & Mitchell 2009's *Triarthrus
  beckii* official abstract
  ([10.1111/j.1502-3931.2008.00144.x](https://doi.org/10.1111/j.1502-3931.2008.00144.x);
  now read) describes spatial comparisons at approximately one level and an
  eight-bin New York series, not a verified crossed panel. Slattery's
  [Dryad deposit](https://doi.org/10.5061/dryad.sqv9s4ndb), version 367275,
  documents locality/formation/size data and shape summaries. Metadata and
  embedded README were inspected; API/public file downloads returned 401/403,
  so the CSV geometry and values remain unchecked. Find independent
  environmental information and overlapping locality-by-time support before
  further analysis. Park if time and geography lack overlapping
  support, only pooled means survive, the exact discriminator is occupied,
  or alternative mechanisms remain observationally equivalent. Species
  delimitation must not impose constancy of the tested traits. Without
  independent continuity evidence, report geographic decomposition, not proof
  of stabilizing selection or population replacement.
- **Evidence.** [Initial stasis orientation and limits](../literature/2026-10-10-boundary-counts-and-incumbency.md);
  [closer precedents, deposit limits and tier adjudication](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md).

## New sketch, round 6 (Claude, 10 October)

### Q-037 Is the present crisis's top-down trophic signature unprecedented?
Status **under review**, tier 3. Posed and checked on 10 October. The modern
half of the premise did not hold up.

- **Question (revised).** Once body size is controlled, does trophic position
  predict whether and when a taxon is lost? Does the sign of that effect differ
  between past events and the Late Quaternary or Holocene?
- **Premise correction.** The modern signature found in the sources is body
  size, not trophic level.
  - Payne et al. 2016 (10.1126/science.aaf2416, full text by scout): "Habitat
    zone and feeding mode are not correlated with threat".
  - Smith et al. 2018 (10.1126/science.aao5987, abstract checked by Claude):
    the large-bodied bias follows hominin dispersal; the scout reports it
    operates "within all trophic modes".
  - Late Quaternary losses included 81% of megaherbivores (Svenning et al.
    2024, 10.1017/ext.2024.4).
  - The view that the present crisis is top-down first, from Estes et al. 2011
    (10.1126/science.1205106), therefore reduces largely to size selectivity.
- **Past events, order within events.**
  - Toarcian (Dunhill et al. 2024, 10.1038/s41467-024-53000-2): infaunal
    primary losses cascading upwards fit best. There was no explicit
    trophic-level scenario, and the early recovery was "top-heavy".
  - Meishan, end-Permian (Karapunar et al. 2026, bioRxiv
    10.64898/2026.06.22.733099, abstract checked by Claude; not peer reviewed):
    losses "propagating upwards from benthic herbivores to higher-level
    consumers". An earlier decline of apex predators may be a Signor–Lipps
    artefact.
  - Late Triassic and Toarcian also selected against pelagic predators (Dunhill
    et al. 2018, 10.1098/rspb.2018.0404).
  - So past events are not uniformly bottom-up.
- **Residual.**
  - Tier 1 analysis: extend Payne's logistic framework with a graded
    trophic-level term for five or more events and for modern and Late
    Quaternary data, and test the event × trophic interaction.
  - Tier 2 analysis: rank correlation, stratified by size, between trophic
    level and last-appearance bed at Meishan and in the Cleveland Basin
    (Dunhill's data). Test it against a Signor–Lipps null matched for
    abundance.
- **Kill criterion.** Park if the trophic term is about zero once size is
  controlled, in both past and present. The question then reduces to the size
  result of Payne and Smith. Order within an event is unresolvable if the
  Signor–Lipps null reproduces it.
- **Evidence.** [Round-7 note](../literature/2026-10-10-register-checks-round7.md).

## New sketches, round 7 (Claude, 10 October): the Raup–Sepkoski legacy revisited

Prompted by Barry's question in chat on 10 October: is foundational Raup and
Sepkoski work worth revisiting with modern data and methods? See the legacy
map in the [round-7 note](../literature/2026-10-10-register-checks-round7.md),
which says where each classic idea now sits in this register. These entries
had a bounded prior-work scan before posing, recorded in that note. Their
novelty is still unverified.

### Q-038 Bad genes or bad luck: how predictable is which genera die, and does it change in mass extinctions?

Status **under review**, tier 2. Posed 10 October as a tier-1 variance
partition; reformulated the same day after Codex's identification critique
(76/1380).

- **Why the partition was dropped** (Codex, accepted). A partition into event,
  clade, trait and residual is not a unique biological decomposition:
  - within a stage, the shared event intercept has no variance across genera;
  - trait and clade effects can carry the same information;
  - one binary fate per genus-stage cannot identify an individual residual;
  - the logistic latent residual is a convention of the link function, not a
    measured amount of chance.
  "Bad luck" is therefore not an estimand. What is left after a model is fitted
  also contains missing traits, exposure, taxonomy, observation error and
  misspecification.
- **Question (reformulated).** Given the incoming cohort and the number of
  extinctions in a stage, how much do traits and clade or survival history,
  known before the event, improve held-out prediction of *which* genera
  disappear? Raup's field of bullets (uniform loss) is the baseline.
  - Does the gain differ between background and mass-extinction stages?
  - Does it transfer between events?
  Conditioning on the number lost removes the event intercept. Forecasting the
  size of an event is a separate problem.
- **Why it matters.** It measures how far the biology of extinction is
  predictable, which underlies any use of deep time for modern risk assessment.
  Raup 1994 (10.1073/pnas.91.15.6758) judged taxonomic selectivity "present but
  minor".
- **Prior.**
  - Jablonski 1986 (10.1126/science.231.4734.129): selectivity regimes.
  - Payne & Finnegan 2007 (10.1073/pnas.0701257104).
  - Monarrez, Heim & Payne 2023 (10.1098/rsos.230795, abstract checked by
    Claude): traits combined with capture–mark–recapture survival models.
    Range selectivity is reduced or eliminated in mass extinctions.
  - Smits & Finnegan 2019 (10.1098/rstb.2019.0392): forward-validated
    survival prediction in deep time.
  - Foster et al. 2023 (10.1098/rsos.221507): poor transfer between events.
  - Roy, Hunt & Jablonski 2009 (10.1126/science.1173073).
  - Tikhonov et al. 2026 (bioRxiv 10.64898/2026.07.21.739780): a
    survivorship-bias model with fixed toughness plus event luck already
    quantifies how predictable survival is, conditioned on age.
    - *Correction (10 October):* their 57.3% is the share of *simulated deaths*
      among genera whose modelled toughness exceeds the fitted event threshold,
      across 20 simulations.
    - It is not a variance share, and not an empirical fraction caused by
      chance (Codex, from the main text).
- **Design.**
  1. Compare uniform loss, persistent frailty, traits, clade or history, and
     joint models by held-out predictive score. Integrate uncertainty about
     cohort membership and loss counts from the fossil record.
  2. Report the joint gain, and each component's conditional gain, leaving
     shared information unallocated.
  3. Fix the date each predictor is known: lifetime maximum size or range
     within the focal stage are not pre-event inputs.
  4. Treat prediction for new clades and for known clades as separate targets.
  5. Declare the scoring scale (Codex, 76/1404). For N incoming genera and D
     losses, uniform loss has log loss log C(N, D). Raw gains therefore change
     with cohort size and severity. Stages with D = 0 or D = N carry no
     information about victim identity. Use a per-lineage scale or a
     calibration matched for severity; neither removes all dependence. A low
     gain is not evidence that traits lack mechanisms.
- **Data contract (11 October; [contract](../data/q038-monarrez-contract/README.md), [Codex design audit](../data/q038-flag-audit/README.md)).**
  Barry, in chat on 11 October 2026: "Lift the deferral on Q-038 now, it's
  live again now that we have the dataset." He downloaded the Dryad files
  (10.5061/dryad.931zcrjqw, CC0).
  - *Access and histories.*
    - Access is resolved.
    - The capture histories in the Rdata are intact: 6,562 genera,
      86 occasions.
    - The float corruption is only in the Zenodo spreadsheet copy.
  - *Classes.*
    - Rhynchonellata (1,827) and Bivalvia (1,600) span all five events.
      Strophomenata spans the first three and Trilobita the first two.
    - The deposited occurrence CSV has no Strophomenata or Trilobita, so
      their ranges cannot be rebuilt from it.
  - *Event flags.* The deposited design puts `mass.ext` on survival *out of*
    the first post-extinction stage. Codex confirmed this by building the
    design with RMark 3.0.0.
    - Which code produced the published coefficients is unresolved: the
      class indices and file names in the deposited scripts disagree.
    - [Detail withheld pending disclosure to the data custodian.]
    - For Q-038, define the event intervals independently, ending at each
      boundary.
  - *Predictors.*
    - The deposited range is measured in the focal stage, and range at
      k − 1 is in the same columns.
    - But zero is ambiguous: it marks every absent cell and 812 of 29,486
      present cells.
    - Standardisation and ascertainment need a prospective audit.
    - Body size is one value per genus.
  - *Clade fields.* Order and family come from the genus table, missing for
    8.1% and 5.5% of rows.
  - *Taxonomic unit.* The paper elevates subgenera to genera.
    - No occurrence is assigned to both a genus and its own subgenus, so
      these are nested units, not duplicates. The earlier "about 20%
      duplicates" is withdrawn.
    - Choose the unit in advance and report the other as a sensitivity.
    - Key genera by PBDB number: 18 homonym names fan out in the deposited
      join.
  - *Next gate.* A prospective predictor contract for Rhynchonellata and
    Bivalvia: zero-coding, standardisation window, timing of body-size
    measurement, and the unit.
  - Code is on Zenodo (10.5281/zenodo.7816408, MIT; R and RMark).
- **Kill criterion.**
  - Park if joint observation modelling, persistent susceptibility and transfer
    between events add nothing beyond Monarrez, Smits & Finnegan and Tikhonov.
- **Evidence.** [Round-7 legacy map](../literature/2026-10-10-register-checks-round7.md);
  [Codex round-8 note](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md).
- **Links.** Q-012, Q-022, Q-028, Q-030, Q-016.

### Q-039 Did Sepkoski's evolutionary faunas interact, beyond sharing limits and shocks?
Status **sketch**, tier 2 (provisional; scanned 10 October).

- **Question.** Sepkoski's coupled-logistic model (1984,
  10.1017/s0094837300008186) let the Cambrian, Palaeozoic and Modern faunas
  interact. With sampling-standardised data, is there coupling between faunas
  or classes beyond a shared dependence on total diversity and shared
  extinction shocks?
- **Prior.**
  - The structure has been re-tested. No sampling-standardised re-test of the
    coupled dynamics was found in a bounded search.
    - Rojas et al. 2021 (10.1038/s42003-021-01805-y, abstract checked by
      Claude) find "four global benthic mega-assemblages", with transitions at
      494, 252 and 129 Ma. The mid-Cretaceous transition is protracted.
    - Muscente et al. 2018 (10.1073/pnas.1719976115) recover the three faunas
      by network analysis.
  - Diversity dependence in aggregate is established: Foote 2023
    (10.1086/723626) and Rineau et al. 2022 (10.1126/sciadv.add9620).
  - Close, Benson & Kiessling 2025 (10.1126/sciadv.adv9793): the Modern fauna
    was already part of reef-supporting regions in the Palaeozoic.
  - Alroy 2010 (10.1126/science.1189910): group diversity limits shift
    idiosyncratically.
- **Design.** A Bayesian state-space generalised Lotka–Volterra model on
  SQS-standardised class or fauna richness. Compare it with uncoupled logistic
  growth plus common shocks by leave-future-out prediction. Replicate in reef
  and non-reef regions.
- **Caution (Codex, 10 October).** Coupling in fitted trajectories can absorb
  shared forcing that was not measured. A predictive interaction is not
  automatically competition. Define the response before fitting: standing
  richness, standardised richness, or proportional composition. Each has
  different observation constraints.
- **Kill criterion.** Park if the coupling terms cannot be identified at about
  50–100 bins, or if the answer flips between standardised and range-through
  series.

- **Evidence.** [Round-7 note, legacy map](../literature/2026-10-10-register-checks-round7.md).
### Q-040 Did marine diversity really rise since the Palaeozoic, and is a global curve the right estimand?
Status **sketch**, tier 2 (provisional; scanned 10 October). Kept separate from
Q-010 (Codex, 76/1380). Q-040 asks what regional and global histories the
observations support; Q-010 asks whether biological innovation changes the
diversity that comparable physical conditions support.

- **Question.** On a common support (one taxonomic unit, spatial grain and
  domain, time window and observation process), how did global marine richness
  change? How much came from richness within regions (mean alpha), and how much from
  differentiation between regions (Whittaker beta, β_W = gamma / mean alpha)?
  - Beta already contains the effects of extent and overlap. A separate
    contribution from area needs a defined counterfactual: fixed grain,
    changing extent, cell weights and a rule for allocating interactions.
    Otherwise area is counted twice (Codex, 76/1404).
  - Equal per-cell richness does not identify overlap. Estimating beta needs
    joint occupancy or an explicit estimator of turnover.
  Close et al. 2020 (10.1126/science.aay8309) report regional variation as
  large as variation through time. Cermeño et al. 2022
  (10.1038/s41586-022-04932-6, abstract checked by Claude) model a global rise
  driven by hotspots. These are not necessarily rival results: flat regional
  richness can coexist with rising global richness through differentiation or
  area (Codex).
- **Why big.** This question runs from Raup 1976
  (10.1017/s0094837300004929; "no compelling evidence" of a rise) through
  Sepkoski's curve and Alroy et al. 2008 (10.1126/science.1156963). The
  decomposition says whether any rise came from within-region packing, from
  geography, or from area. Those answers bear on diversity limits differently.
- **Prior.** Close et al. 2020; Cermeño et al. 2022, whose under-2% saturation
  fraction is a model-derived quantity, not a census of filled niches; Fan et
  al. 2020 (10.1126/science.aax4953); Benson et al. 2025 (10.1111/pala.70006);
  Jablonski et al. 2003 (10.1126/science.1083246).
- **Design.**
  1. A hierarchical occupancy or SQS model per grid cell and bin.
  2. A decomposition of global change into mean alpha and Whittaker beta on
     the common support, using joint occupancy. Add an area counterfactual
     only if it is explicitly defined.
  3. Propagate uncertainty across plate models.
  4. Score predictions on held-out regions.
  Neither a flat nor a rising curve alone identifies a ceiling.
- **Kill criterion.** Park if the intervals on the components overlap zero
  throughout, or if the choice of plate model dominates. This is a crowded
  area (the Close, Benson and Kiessling groups), with a high risk of being
  scooped.
- **Evidence.** [Round-7 legacy map](../literature/2026-10-10-register-checks-round7.md).

### Q-041 Is there periodicity in extinction once modern timescale uncertainty is propagated?
Status **under review**, tier 2. Tractability is unresolved (Codex, 76/1420).

- **Question.** Raup & Sepkoski 1984 (10.1073/pnas.81.3.801) reported a period
  of about 26 Myr. Using GTS2020 boundary ages, drawn jointly with their
  uncertainties, and sampling-standardised extinction rates, does a periodic
  model beat aperiodic nulls by marginal likelihood? Use a log-uniform period
  prior over 10–100 Myr, with sensitivity checked on 10–60 Myr. Include
  quasi-periodic and periodic-plus-trend variants.
  - The target is periodic structure in extinction *severity, conditional on
    the inherited stage grid*. Some boundaries are defined by biotic turnover:
    the Famennian base sits just above the Kellwasser extinction horizon.
    Conditioning cannot remove that dependence.
  - Timing against independently dated sections, or bins fixed independently
    of the grid, is a different, complementary target.
- **Why big.** A real period would point to a periodic forcing, which could be
  astronomical or internal to the Earth (for example mantle or sea-level
  cycles); periodicity alone would not identify the cause (Codex, 76/1404). A
  decisive null, or a bound on amplitude, would settle a 40-year dispute that
  still produces papers.
- **Prior (disputed; no fully propagated test since 2013).**
  - Stigler & Wagner 1987 (10.1126/science.238.4829.940): the original test is
    biased by unequal stage spacing and Signor–Lipps effects.
  - Benton 1995 (10.1126/science.7701342): "no support".
  - Feng & Bailer-Jones 2013 (10.1088/0004-637x/768/2/152, full preprint by
    scout): the only Bayesian model comparison on extinction data. They found
    evidence against simple periodic models, using approximate age errors and
    pre-GTS2020 event lists.
  - Melott & Bambach 2014 (10.1666/13047, abstract checked by Claude): on
    GTS2012, an excess of extinction "follows a 27-Myr timing interval" at
    p ≈ 0.02. They used fixed ±3 Myr windows and did not resample boundary
    ages.
  - Erlykin et al. 2018 (10.1111/pala.12334): the 27-Myr peak vanishes when 5
    of 136 events are removed.
  - Rampino & Prokoph 2020 (10.1089/ast.2019.2043): a vote count of spectral
    trials, not a model comparison.
  - Bailer-Jones 2011 (10.1111/j.1365-2966.2011.19112.x): Bayesian tests on
    craters disfavour periodicity.
  - Rampino & Caldeira 2025 (10.1016/j.earscirev.2025.105100, meta only), on
    stage-boundary cyclicity, should be read first.
- **Deeper check (11 October; round-9 note).**
  - No published test was found that combines GTS2020, correlated monotone
    age uncertainty and model comparison on extinction timing.
  - Feng & Bailer-Jones 2013 used independent Gaussian errors, pre-GTS2012
    ages and a smooth cosine model. Narrow-pulse periodic models were never
    tested.
  - **The stage lattice itself may be periodic.**
    - Boulila et al. 2023 (10.1073/pnas.2221149120, abstract checked by
      Claude) find a 36 ± 1 Myr cycle in marine genus diversity and in
      tectonic, sea-level and macrostratigraphic data; the scout reports 28-
      and 36-Myr components in stage durations.
    - Rampino et al. 2021 (10.1016/j.gsf.2021.101245) report about 27.5 Myr in
      GTS2020 stage-boundary ages.
    - Extinction periodicity tested on stage-binned data is therefore
      confounded unless the null preserves the actual stage grid.
  - **Earth-internal alternatives to astronomical forcing.**
    - Mantle–slab tectono-eustasy (Boulila et al. 2023).
    - A 26-Myr oceanic crustal carbon cycle (Müller & Dutkiewicz 2018,
      10.1126/sciadv.aaq0500).
    - Sea-level hiatuses at stage boundaries (Rampino & Caldeira 2025, closed
      access; only relayed content seen).
    - Chronostratigraphic artefact (Stigler & Wagner 1987).
- **Design (revised).**
  1. **Age model.** Use GTS2020 spline Monte Carlo replicates with shared
     boundaries, forced monotone, and recompute interval exposures on every
     draw.
     - GTS2020 (chapter 14A) notes that treating errors as independent
       underestimates interpolated uncertainty, so add correlated external
       error.
     - No ready-made global joint ensemble has been verified. Obtain the
       inputs, the internal/external error partition and the sampler
       provenance.
     - GTS2004, 2012 and 2020 are alternative reconstructions, not equally
       probable uncertainty draws.
     - Treat event placement within a stage as a nuisance parameter.
  2. **Generative null (revised after Codex, 76/1420).** Fit an aperiodic null
     integrated over the actual intervals, including the fossil observation
     and estimation process. Raw permutation among intervals is not
     exchangeable:
     - durations, sampling, cohort size, trend and serial dependence differ;
     - under a constant hazard of 0.1 per Myr, expected loss is 0.095 in a
       1-Myr bin and 0.632 in a 10-Myr bin;
     - rotating the grid changes physical-time separations.
     Restricted randomisation is a diagnostic only where it can be justified.
  3. **Models.** Uniform, trend, red noise or Gaussian process, narrow-pulse
     periodic, periodic plus background, and quasi-periodic. Put log-uniform
     priors on the period over 10–100 Myr and test sensitivity to the prior.
  4. **Evidence.** Marginalise age error within the evidence. Judge whole
     models, not periodogram peaks: Bailer-Jones 2011 reports that peak-only
     claims give about 20% false positives.
  5. **Injection-recovery** on the real GTS2020 lattice, varying pulse width
     and the periodic fraction.
  6. Data: PBDB three-timer or gap-filler rates at stage and substage level,
     with the Sepkoski compendium as a second series.
- **Decision rule (revised after Codex, 10 October).**
  - Specify the joint age model that produces correlated, monotone boundary
    draws. Marginal age errors alone do not define it.
  - Use Bayes factors in a stated direction. A periodic-versus-null Bayes
    factor below 3 is inconclusive, not a rejection of periodicity.
  - Count the null as supported only if the null-versus-periodic Bayes factor
    is at least 10 in both datasets and for both estimators. Two compilations
    and two estimators share records and chronology, so their agreement is
    robustness, not replication.
  - Injection-recovery measures sensitivity; it is not an exclusion bound
    (Codex, 76/1420). For a bound, specify period, phase, pulse width and
    amplitude or periodic fraction, then invert a calibrated test or compute a
    defined posterior bound. Allow for the outcome that no useful bound is
    possible.
  - Dropping the five largest events changes the target. It is a separate
    analysis with its own calibrated selection rule, not a robustness
    condition.
  - Periodicity alone would not identify an impact cause.

- **Evidence.** [Round-7 note, legacy map](../literature/2026-10-10-register-checks-round7.md).
### Q-042 How many species died in the great mass extinctions?
Status **under review**, tier 2. Scanned 10 October; deeper check 11 October.

- **Question.** Raup 1979 (10.1126/science.206.4415.217) estimated by reverse
  rarefaction that "as many as 96 percent" of marine species died at the
  end-Permian. Stanley 2016 (10.1073/pnas.1613094113, abstract checked by
  Claude, sections by scout) revised this to "only about 81%". Define the
  estimand in numeric time: the fraction of skeletal marine animal species
  alive at t0 that are globally extinct by t1. Once extinction clustered
  within genera and species sampling are both modelled, what interval does the
  evidence support? Can genus-to-species inversion recover it at all?
- **Why big.** The 90–96% figure is still widely stated. Kiessling, Smith &
  Raja 2023 (10.1073/pnas.2201926119) note that "numbers of 90 to 95% are still
  more widely stated than lower numbers". The ">75%" benchmark for a mass
  extinction, used in comparisons with the present (Barnosky et al. 2011,
  10.1038/nature09678), is itself extrapolated from species-to-genus ratios in
  well-known groups. It traces to Jablonski 1994 (10.1098/rstb.1994.0045, not
  accessed).
- **What Stanley 2016 does** (sections read by the scout).
  - Uses Sepkoski's genus and family compendia, not PBDB.
  - Subtracts background extinction using extinction/origination ratios, and
    corrects backward smearing.
  - Converts about 62% genus loss to species loss with "a composite
    rarefaction curve at the genus level that was the average for 12 extant
    higher taxa", weighted per higher taxon to about 81% (σ 0.29 from
    resampling).
  - Excludes the Triassic.
  - Its own caveat: earlier species estimates "are based on the false
    assumption that extinction struck all taxa with equal probability".
  - Loss is still assumed random within higher taxa and genera, and species
    sampling is not modelled.
- **Prior.**
  - McKinney 1995 (10.1017/s0094837300013312): estimates may be 6–15% too
    high.
  - Smith & Roy 2006 (10.1666/05078.1, abstract checked by Claude): in
    Plio-Pleistocene scallops, "species-level extinctions were higher in more
    speciose genera, but these genera were buffered against genus-level
    extinctions". Selectivity can therefore bias reverse rarefaction either
    way.
  - Direct regional species data: Wang et al. 2014 (10.1666/13022), 62% of
    1,450 species within 200 kyr. Fan et al. 2020 (10.1126/science.aax4953)
    give about 11,000 species, Cambrian to Early Triassic only.
  - Genus-level inputs differ widely: 56% (Barnosky; Bambach), 62% (Stanley),
    79% for the Changhsingian in PBDB (Payne & Clapham 2012,
    10.1146/annurev-earth-042711-105329; a different metric), and DeepDive's
    model-based estimates (10.1038/s41467-024-48434-7).
  - No simulation validating the inversion under clade-structured selectivity
    and incomplete sampling was found.
- **A partial bound** (scout's derivation, checked by Claude). Suppose a
  fraction g of genera dies, each surviving genus keeps at least one species,
  and the true mean is m species per genus. Then species loss is at most
  1 − (1 − g)/m.

  | Genus loss g | m = 3 | m = 5 | m = 9.5 |
  | --- | --- | --- | --- |
  | 0.56 | 0.853 | 0.912 | 0.954 |
  | 0.62 | 0.873 | 0.924 | 0.960 |
  | 0.79 | 0.930 | 0.958 | 0.978 |

  Whether 96% is possible therefore depends on the genus-level input and on
  the true number of species per genus, including species never sampled.
- **Design.**
  1. Calibrate within a matched region and window, using species data with
     genus labels (Wang; Fan). Measure observed species and genus loss jointly,
     and estimate the clustering of deaths within genera, for example by
     beta-binomial overdispersion.
  2. Run a hierarchical birth–death simulator with a genus random effect on
     kill probability (including a sign-flip scenario), heterogeneous
     preservation, and regional versus global extinction. Score raw reverse
     rarefaction and Stanley's correction for bias and coverage.
  3. Carry the 56–79% genus-level interval through as an input, and report the
     bound intersected with the calibrated range.
  Regional disappearance is roughly an upper bound on global extinction of
  that region's species. It is not a global estimate.
- **Kill criterion.** Report bounds, not a point estimate, if inversion bias
  exceeds about 10 percentage points under plausible selectivity. Failing to
  separate 81% from 96% can still leave useful bounds.
- **Evidence.** [Round-7 legacy map](../literature/2026-10-10-register-checks-round7.md);
  [round-10 note](../literature/2026-10-11-register-checks-round10.md).

## New question, round 8 (Codex, 10 October): evolutionary futures

### Q-043 Does survivor composition determine what can evolve next?
Status **parked** (11 October). The broad bottleneck/recovery question is
occupied; a distinct feasible residual has not yet been established.

- **Question.** Does the lineage and character composition retained after
  extinction predict subsequent morphological evolution, beyond survivor
  richness, retained geometry and ecological opportunity?
- **Why it matters / boundary.** Extinction could change future possibilities
  as well as current diversity. Q-022 concerns lost evolutionary history;
  Q-009 concerns ecological organisation and future recovery. The distinction
  is meaningful but does not establish novelty or feasibility.
- **Nearest priors.** The original Ruta et al. 2013, Puttick et al. 2020 and
  Liu et al. 2026 leads are retained in the round-8 note. Claude's expanded
  map adds replicated ammonoid and foraminiferal radiations and contrasting
  crinoid, graptoloid and ichthyosaur outcomes. Codex checked Saunders et al.
  2008 ([10.1666/07053.1](https://doi.org/10.1666/07053.1), official abstract),
  Norris 1991 ([10.1017/S0094837300010721](https://doi.org/10.1017/S0094837300010721),
  official abstract), and Bapst et al. 2012
  ([10.1073/pnas.1113870109](https://doi.org/10.1073/pnas.1113870109),
  Results/Discussion and Methods). These occupy the generic claim; a formal
  prediction framework alone does not rescue it.
- **Two estimands to preserve.** Comparing alternative survivor compositions
  under shared evolutionary rules measures a model-based survivor-state
  effect. Comparing outcomes with an unchanged-process baseline conditional
  on one survivor state tests process departures. The latter can be zero
  while the former is substantial; the round-9 analytical illustration shows
  this explicitly. Neither automatically identifies a causal fossil effect.
- **Data constraints.** Survivor membership is inferred, including ghost and
  Lazarus lineages. Fordham 2018's corrected Aze resource is Cenozoic, so it
  does not provide the proposed mid-Cretaceous contrast. Its alternative tree
  representations are not independent phylogenetic evidence. ANU metadata is
  accessible; files and joint support remain uninspected. Norris & Nishi's
  coiling study does not supply an Eocene–Oligocene coiling replicate.
- **Horizon / mechanism.** Prespecify a horizon curve and environmental path.
  A fixed horizon is a valid outcome; choosing it after seeing results is not.
  Bapst's environmental explanation remains one of several alternatives.
  Reduced disparity does not establish lost evolvability, and fossil
  morphological covariance is not genetic covariance.
- **Revisit trigger.** A specific survivor-state or process contrast unresolved
  by the closest studies, with verified lineage, character and environmental
  support plus an observation-aware discriminator. Stop generic method/data
  expansion until then; retain the distinctions for Q-009 and recovery work.
- **Evidence.** [Original round-8 check](../literature/2026-10-10-selectivity-stasis-and-evolutionary-futures.md);
  [Claude's replicated priors](../literature/2026-10-10-register-checks-round8.md);
  [round-9 adjudication](../literature/2026-10-11-survivors-spatial-richness-and-data-vintages.md).

## New sketches, round 8 (Claude, 10 October): building on Benton's big picture

Prompted by Barry's question in chat on 10 October about building on Michael
Benton's big-picture work. See the Benton legacy map in the
[round-8 note](../literature/2026-10-10-register-checks-round8.md). Both
entries had a bounded prior-work scan before posing; novelty is unverified.

### Q-044 Why is life on land so diverse if regional terrestrial richness is bounded?

**11 October audit update:** the [independent check](../data/q044-support-audit/README.md)
confirms near-maximal turnover of recorded species names in the screen, but
challenges the biological-saturation inference and the claim that the kill
criterion is unreachable. Missing identities, detection, weights and common
spatial support remain unresolved. Claude owns reconciliation of the entry
and original contract below; no estimand replacement is yet agreed.

Status **under review**, tier 2. Posed 10 October as tier 1 (provisional).
Moved down on 11 October after Codex's estimand critique (76/1404). A deeper
check the same day sharpened it.

- **Question.** About 85% of living species are terrestrial (Benton, Wilf &
  Sauquet 2021, 10.1111/nph.17822). Codex reports that the authors call their
  diversity curves largely conjectural. Equal-area studies give a different
  picture for non-marine tetrapods:
  - Close et al. 2017 (10.1038/ncomms15381, abstract checked by Claude):
    "no significant increase in species richness between the Late Triassic and
    the K/Pg boundary", then "an abrupt tripling of richness in the earliest
    Palaeogene".
  - Close et al. 2019 (10.1038/s41559-019-0811-8) and 2020
    (10.1098/rspb.2020.0372): a ten-fold global rise would need increases in
    beta diversity that are "as-yet undocumented". The scout checked this
    against the full text.

  These are different quantities, not conflicting measurements.
  - **Closer precedent (Codex, 76/1420).** Close & Reijenga 2025
    (10.1073/pnas.2419052122) analyse North American tetrapods from the
    Campanian to the Ypresian. They estimate species–area slopes and
    intercepts with spatial and coverage standardisation, and so occupy the
    within-region comparison of K–Pg recovery. Their small-scale intercept is
    not literal community alpha.

  The residual is narrower: through the Mesozoic and Cenozoic, did
  differentiation *between* regions rise while within-region richness stayed
  flat? It holds only where contemporaneous regional coverage supports it.
- **Estimand (per time bin, on common support).** Fix the grain, the K
  equal-spread windows (summed minimum-spanning-tree length, or divvy), the
  coverage quorum and the Hill order. Then

  ln Γ_K = ln ᾱ + ln β_within + ln β_between

  where, with fixed window weights p_w summing to one (Codex, 76/1420):
  - ᾱ = Σ p_w α_w, using declared within-window collection weights;
  - γ̄ = Σ p_w γ_w, where γ_w is the richness of window w's union;
  - β_within = γ̄ / ᾱ;
  - β_between = Γ_K / γ̄.

  Averaging window-specific beta ratios breaks the identity; Codex gives an
  exact counterexample, 16.5 against 12. Γ_K is richness in the union of the
  chosen windows, not global terrestrial richness. Equal MST length does not
  force equal area or habitat. Coverage-standardised estimates made
  separately at each level do not form one consistent hierarchy: joint
  sampling and shared taxon identities are needed.

  Distance-decay of dissimilarity is a diagnostic of spatial organisation,
  not a test of whether beta changed. Taxa can be strongly partitioned among
  windows with a flat distance relationship.

  Area has no separate multiplicative term. Fragmentation acts *through* the
  differentiation being measured, so it cannot be subtracted as an
  independent component. Its effect is a model-dependent counterfactual:
  define a reference geography and the assumptions about overlap and
  environment, simulate both configurations on the same support, and report
  the difference. Vavrek 2016 (10.1098/rsbl.2016.0528, abstract checked by
  Claude) is the model precedent. It expects terrestrial vertebrate richness
  "to nearly double through the Mesozoic owing to continental fragmentation,
  despite a decrease of 24% in total terrestrial area".
  - The arithmetic residual from round 9, which combined Vavrek, the K–Pg step
    and a hypothetical ten-fold rise, is withdrawn. Those are not established
    additive components on one domain.
- **Prior.**
  - Close et al. 2017, 2019 and 2020 (above).
  - Dunne et al. 2018 (10.1098/rspb.2017.2730) criticise ratio-based
    "endemism".
  - Button et al. 2017 (10.1038/s41467-017-00827-7): connectedness and
    provinciality from the Permian to the Early Jurassic, not linked to
    richness.
  - Brocklehurst & Fröbisch 2018 (10.3389/feart.2018.00200): beta depends on
    region scale.
  - Alpha–beta–gamma precedents exist for North American Palaeogene ungulates
    (Darroch et al. 2014, 10.1111/geb.12156) and for marine biotas (Sepkoski
    1988; Holland 2010; Penny & Kröger 2019).
  - Close et al. 2020 find no effect of the early angiosperm expansion on
    regional tetrapod diversity.
  - Alroy 2018 (10.1111/ele.13152): trees break the bounded pattern.
  - Insects (Clapham et al. 2016; Schachat et al. 2019,
    10.1098/rspb.2019.2054) are not spatially standardised.
- **Data.** PBDB non-marine tetrapods, using the Close et al. 2019 code and
  data (Dryad). Repeat with marine animals as the contrast. Plants and insects
  need their own datasets and are separate comparisons.
- **Out of scope.** The date of the land–sea crossover cannot be recovered from
  tetrapod fossils, because tetrapods are a small fraction of land species.
  Published crossover dates (about 110 Ma, Vermeij & Grosberg 2010; 100–125 Ma,
  Benton 2016, 10.1371/journal.pbio.2000724) are argued, not estimated. Treat
  any such date as a separate, model-based or phylogenetic question.
- **Kill criterion.** Drop the between-region claim if, from the Late
  Triassic to the Neogene, the change in ln β_between has an interval that
  contains 0 and excludes ln 1.5. The next gate is joint support by taxon,
  region and time, and a discriminator that goes beyond Close & Reijenga 2025.
  "At least four equal-spread windows in at least six bins" is a screening
  rule, not validated power.
- **Data support (11 October; [support screen](../data/q044-joint-support/README.md)).**
  The Close et al. 2019 deposit (Barry's download) holds raw PBDB downloads
  from 2017 and local-richness code. It has no window-level outputs and
  cannot be run as deposited.
  - *Window counts.* Of 26 bins from the Late Triassic to the Neogene, 19
    have at least four disjoint 1,000 km windows with at least 10
    collections each.
    - 16 still pass with Good's u ≥ 0.5.
    - Only 5 pass with u ≥ 0.7, all Cenozoic.
    - The Jurassic gaps (J2–J4) fall where break-up should matter most.
  - **The decisive finding is saturation.** Primary windows share almost no
    species.
    - The share of union species found in two or more windows is at most
      0.033 in every Mesozoic and Palaeogene bin; at genus level, at most
      0.14.
    - So β_between is close to K, its ceiling, and as specified it cannot
      rise.
  - *Geometry.* The windows mostly sit on different continents, with centres
    5,000–12,000 km apart. Only 5 bins have at least four windows on one
    continent.
  - *Consequence.* The estimand and the kill criterion need revising before
    a power gate. Candidates:
    - within-continent windows at a fixed separation (a Cenozoic-only
      design, close to Close & Reijenga 2025);
    - a less saturated level or measure;
    - distance-conditioned sharing.

    Within-window spread must be fixed by subsampling to a fixed MST, and
    the configuration of the windows must be fixed as well. D stays 2.
- **Robustness.** The bounded data-vintage check from Q-045 belongs here:
  compare the Close et al. 2019 deposited extract with a current extract by
  stable identifiers.
- **Evidence.** [Round-8 note, Benton legacy map](../literature/2026-10-10-register-checks-round8.md);
  [round-9 note](../literature/2026-10-11-register-checks-round9.md).

### Q-045 How robust are headline macroevolutionary estimates to future data?
Status **parked** as a standalone audit (11 October). A bounded robustness
check is kept inside Q-044 and other biological questions.

- **Why parked** (Codex, 76/1404, with a direct API diagnostic).
  - The PBDB parameters `occs_created_before` and `occs_modified_*` filter
    *current* records, with current taxonomy and linked information. They do
    not restore historical versions.
  - An old creation cutoff admits records modified since then; a modification
    cutoff drops rows rather than restoring them.
  - "Data vintage" therefore has three different meanings:
    1. robustness on archived extracts, using the taxonomy and processing
       then in use;
    2. sensitivity by publication cohort. Tennant et al. 2018
       (10.7717/peerj.4417) did this, filtering a 2017 extract by publication
       year with taxonomy as of 2015;
    3. sensitivity by entry cohort.

    Only the first is a true historical replay, and no usable historical
    backup has been verified.
- **The common-cause benchmark is also reframed.** Accuracy below about 70% for
  selected methods at about 100 bins is a performance result for those methods
  and scenarios. It is not proof that time-series inference is impossible.
- **Retained prior.**
  - Benton & Storrs 1994 (10.1130/0091-7613(1994)022<0111:ttqotf>2.3.co;2).
  - Benton, Wills & Hitchin 2000 (10.1038/35000558).
  - Sepkoski 1993 (10.1017/s0094837300012306).
  - Dunhill, Hannisdal & Benton 2014 (10.1038/ncomms5818).
  - Dunhill et al. 2018 (10.1111/pala.12331).
- **Revisit if** a preserved historical PBDB extract with its then-current
  taxonomy becomes available, or a specific biological claim needs a declared
  type of vintage check.
- **Evidence.** [Round-8 note](../literature/2026-10-10-register-checks-round8.md);
  [Codex round-9 note](../literature/2026-10-11-survivors-spatial-richness-and-data-vintages.md).

## New direction, round 9 (Codex, 11 October)

### Q-046 Did marine diversification increase total energy use or divide it among more taxa?
Status **parked** on entry. The broad question is occupied; absolute-density
support for a distinct total-flux question remains unverified.

- **Question.** Did the growth of marine animal diversity increase total
  animal metabolic flux per unit habitat area, or primarily redistribute a
  similar flux among more taxa?
- **Why big / boundary.** More species need not mean a larger biosphere energy
  budget. This concerns energy use rather than Q-010's diversity capacity or
  Q-021's Earth-system recovery, although the mechanisms can overlap.
- **Nearest priors.** Bambach 1993
  ([10.1017/S0094837300000336](https://doi.org/10.1017/S0094837300000336),
  official abstract) already argues for energetic expansion. Finnegan & Droser
  2008 ([10.1666/07074.1](https://doi.org/10.1666/07074.1), Introduction,
  Methods and findings) analyse Ordovician energetic redistribution with
  relative abundances. Finnegan et al. 2011
  ([10.1666/09066.1](https://doi.org/10.1666/09066.1), Methods, Results and
  relevant Discussion) estimate gastropod mean per-capita metabolism and
  explicitly consider compensatory density decline. These primary sections
  were inspected by a bounded Codex subagent; no dataset was reproduced.
- **Why parked.** Richness, biomass, individual metabolism, total metabolic
  flux and primary-production supply are distinct. Relative abundance and
  shell sizes do not establish living density. Deposited shells integrate
  production, mortality, transport, destruction and time; sediment volume is
  not habitat area. Increased per-capita demand can coexist with unchanged
  total flux if density falls. A novel total-flux claim cannot rest on the
  existing per-capita signal or a generic reanalysis.
- **Revisit / support gate.** One original quantitative assemblage dataset must
  independently constrain living density using counts, sizes, depositional
  duration/context and skeletal production/destruction. Then determine whether
  flux bounds distinguish expansion from redistribution. With only relative
  counts or maximum sizes, abandon total-flux inference and retain the narrower
  compositional/per-capita result. No dataset has passed this gate here.
- **Evidence.** [Round-9 sources and measurement distinctions](../literature/2026-10-11-survivors-spatial-richness-and-data-vintages.md).

## New sketch, round 9 (Claude, 11 October)

### Q-047 When biotas meet: do past interchanges forecast today's biotic mixing?
Status **under review**, tier 2 (scanned 11 October; reviewed by Codex,
76/1420). Novelty is unverified.

- **Question.** Fit a model of interchange outcome on past interchanges. The
  outcomes are asymmetry of flow and, where measurable, native loss against
  immigrant gain. The predictors are the source-to-recipient richness ratio,
  phylogenetic distance, environmental match and timing. Does that model
  predict modern human-mediated flows out of sample, better than a null built
  only from trade and propagule pressure?
- **Why big.** Human transport is mixing biotas at a scale no single past
  interchange matched. Deep time holds the only completed experiments, where
  the long-term outcomes are known.
- **Prior.**
  - **Qualitative synthesis.** Vermeij 1991 (10.1126/science.253.5024.1099,
    abstract checked by Claude): "large-scale extinction of species before the
    onset of interchange renders biotas especially prone to invasion".
  - Brock & Bernard 2025 (BioScience, 10.1093/biosci/biaf152, abstract checked
    by Claude) review prehistoric exchanges. They find that the number of
    species exchanged and the spatial extent of mixing "correlate with
    long-term consequences". The scout reports this rests on comparing cases,
    not on statistics.
  - **Single interchanges, quantified.**
    - The Great American Biotic Interchange (Carrillo et al. 2020,
      10.1073/pnas.2009397117): no dispersal asymmetry; higher extinction of
      South American natives.
    - Faurby & Svenning 2016 (10.1111/geb.12504).
    - Wallace's Line (Skeels et al. 2023, 10.1126/science.adf7122).
    - Late Devonian speciation collapse (Stigall 2010,
      10.1371/journal.pone.0015584).
    - The invasion hierarchy (Stigall 2019,
      10.1146/annurev-ecolsys-110617-062638).
  - **Modern theory without deep time.** Fridley & Sax 2014
    (10.1111/geb.12221, abstract checked by Claude) propose an evolutionary
    imbalance hypothesis, predicting invasion patterns from source-region
    phylogenetic diversity. Further tests: Fristoe et al. 2023
    (10.1038/s41559-023-02172-z).
  - **Forecasts never tested.** Vermeij & Roopnarine 2008
    (10.1126/science.1160852) project 77 Pacific mollusc lineages invading the
    Atlantic.
  - Not found: a quantitative comparison of outcome determinants across
    interchanges, or a deep-time model validated on modern flows.
  - **RECOMBINE (checked 11 October).** H2020 MSCA Global Fellowship 896323
    (10.3030/896323), 2021–2024, ENS Paris and ANU. Its CORDIS periodic report
    names source-community size as "the main predictor driving the asymmetry
    of dispersal events in biotic interchanges". That rests on DEC models over
    tetrapod phylogenies, and the report flags constant-rate DEC as
    "not methodologically correct" for rate variation. No peer-reviewed output
    was found, and the report makes no forecast and no validation. It is grey
    literature and does not occupy the transfer test.
- **Design.**
  1. Leave-one-interchange-out validation across at least six corridors, run
     with one pipeline (DES or PyRate) and including extinct taxa in the
     source pools. Candidate corridors: the Great American Biotic Interchange,
     the Gomphotherium bridge, Bering, India–Asia, Sunda–Sahul, and the
     trans-Arctic molluscs.
  2. Freeze the coefficients, then predict the direction and magnitude of
     modern alien flows for matching region pairs. Sources: GRIIS
     (10.1038/sdata.2017.202), GloNAF, and Seebens first records.
- **First gate: a crosswalk of outcomes and denominators within one taxon**
  (Codex, 76/1420). It comes before assembling six corridors.
  - Fossil genus range-expansion hazards, modern naturalisation stocks, first
    detections and actual transport routes are different quantities.
  - A taxon native to A and alien in B does not show transport from A to B;
    it may have arrived via C. SInAS 3.1.1 (10.1038/s41597-025-06379-6) joins
    distributions, but does not give routes or native source pools.
- **The modern comparator to beat is biological, not only trade.** Fristoe et
  al. 2023 and Fan et al. 2025 (10.1038/s41467-025-65455-y) already predict
  modern flows from source-region biology. The deep-time model must add
  information beyond them.
- **Limit.** Separate native loss already observed from eventual net
  consequences that cannot yet be observed (extinction debt). The modern stage
  can validate flows and asymmetry, and observed native losses, but not the
  eventual net diversity change.
- **Kill criterion.** Park in any of these cases:
  - fewer than five interchanges give bidirectional counts comparable in taxon
    and scale;
  - the cross-validated skill interval includes zero;
  - the transfer test is already published.
- **Links.** Q-023 (speciation collapse during invasion), Q-028 (winners),
  Q-033 (arrival order).
- **Evidence.** [Round-9 note](../literature/2026-10-11-register-checks-round9.md).

## New question, round 10 (Codex, 11 October): opposing environmental and trophic effects

### Q-048 Can climate-driven predator decline reduce extinction risk for their prey?
Status **under review**, tier 2 (provisional). Climate-mediated predator
release is established; novelty and support for the persistence contrast
remain unverified.

- **Question.** At comparable physical exposure, does suppression of predators
  by climatic change reduce local extinction risk for their previously
  resident prey? Can reduced predation offset direct environmental harm?
- **Why big / boundary.** Environmental vulnerability may depend on how enemies
  respond, as well as on the prey's own physiology. Q-037 asks about trophic
  extinction signatures; this asks whether a documented interaction changes
  prey persistence. Q-019 provides the broader biotic/abiotic context.
- **Nearest priors.** Aronson, Blake & Oji 1997 (institutional abstract) and
  Aronson et al. 2009
  ([10.1371/journal.pone.0004385](https://doi.org/10.1371/journal.pone.0004385),
  Methods/Results/relevant Discussion) already connect Antarctic cooling,
  reduced shell-breaking predation and differential prey responses. Chiba &
  Sato 2016 ([10.1017/pab.2015.38](https://doi.org/10.1017/pab.2015.38),
  official abstract) already studies climate-mediated drilling interactions.
  Harper, Crame & Sogot 2018
  ([10.1016/j.palaeo.2018.03.009](https://doi.org/10.1016/j.palaeo.2018.03.009),
  accepted-manuscript Methods/selected Results and Discussion) finds changing
  prey choice across the Antarctic K–Pg without a significant change in attack
  failure. The broad mechanism and community response are not new claims.
- **Discriminator.** Compare resident prey populations with similar physical
  exposure but different predator suppression. Predict improved persistence
  specifically among prey previously exposed to those predators. Distinguish
  reduced enemy pressure from direct physiological benefit, habitat change,
  immigration and selective preservation. Such a contrast supports a test;
  matching alone does not establish causality.
- **Data gate.** Existing La Meseta assemblage tables, shell counts and climatic
  history in Aronson 2009, plus Harper's documented specimen collections, are
  leads. Require repeated horizons/localities, the same resident prey,
  attacked/unattacked denominators, independent environmental/age evidence and
  prey persistence or abundance trajectories. Joint reusable support is not
  verified. Harper did not count undrilled molluscs; its drillhole measurements
  cannot alone supply attack frequency. Injuries and holes do not directly
  measure per-time predation hazards.
- **Kill / merge.** Park or merge into Q-019 if predator decline is inseparable
  from physical change, only replacement communities are observed, or necessary
  attack denominators are absent. Do not substitute another demonstration of
  climate-mediated predator release for the extinction-protection question.
- **Evidence.** [Round-10 mechanism, rivals and primary-source record](../literature/2026-10-11-interchange-transfer-and-spatial-temporal-support.md).

## New sketch, round 10 (Claude, 11 October)

### Q-049 Did failure to track shifting isotherms predict extinction at past hyperthermals?
Status **sketch**, tier 2 (provisional; scanned 11 October). Novelty is
unverified.

- **Question.** At hyperthermal boundaries, take a genus's tracking ratio R:
  the observed displacement of its thermal range edge divided by the
  displacement of the isotherm over the same interval. Does R predict
  extinction beyond two existing models?
  - Paleogeographic dispersal-pathway geometry (Malanoski et al. 2026).
  - Loss of thermal habitat with thermal optimum (Reddin et al. 2022).

  How does R scale with the length of the interval?
- **Why the "speed limit" framing was dropped.** An absolute deep-time limit
  on tracking speed cannot be measured at the resolution of PBDB stages.
  Using the scout's arithmetic, a shift of about 2,500 km over at least 1 Myr
  is at most a few metres per year, orders of magnitude below modern isotherm
  velocities (Burrows et al. 2011, 10.1126/science.1210288: medians of
  21.7 km per decade in the ocean and 27.3 km per decade on land).
  Kiessling et al. 2024 (10.1017/pab.2024.20, abstract checked by Claude)
  argue that observed rates of change "cannot currently be compared across
  different timescales" (quoted from the text by the scout). A dimensionless
  ratio over a common interval avoids that comparison.
- **Prior.**
  - Malanoski et al. 2026 (10.1126/science.adv2627, abstract checked by
    Claude): taxa whose potential dispersal pathways are long relative to the
    latitude they traverse "consistently exhibit higher extinction risk". The
    effect is amplified in mass extinctions and hyperthermals. Pathway length
    is a geometric proxy, not observed tracking.
  - Reddin et al. 2022 (10.1111/gcb.16333, abstract checked by Claude):
    extinction at seven hyperthermals follows the geometry of thermal-habitat
    loss. Genera with optima above about 21 °C or below about 11 °C have raised
    odds of extinction.
  - Reddin, Kocsis & Kiessling 2018 (10.1111/geb.12732): range centres of
    taxa that survive a boundary shift with temperature. Conditioning on
    survivors makes victims invisible.
  - Quantitative tracking against climate velocity is occupied in the
    Quaternary: Ordonez & Williams 2013 (10.1111/ele.12110); Antell et al. 2021
    (10.1073/pnas.2017105118).
  - Deep-time evidence is only qualitative: Wing et al. 2005
    (10.1126/science.1116913); Smith, Rose & Gingerich 2006
    (10.1073/pnas.0511296103).
  - Sandel et al. 2011 (10.1126/science.1210173) use climate velocity as an
    exogenous exposure, not observed lag.
- **Design.**
  1. Estimate R from bins before the boundary, using the Reddin 2018 pipeline
     on PBDB and PETM isotherms from data assimilation (Tierney et al. 2022,
     10.1073/pnas.2205326119). Test extinction in the next bin.
  2. Compare nested models: range size, thermal optimum and pathway length,
     each with and without R.
  3. Require a negative R effect in hyperthermals, absent in matched
     non-hyperthermal controls.
  4. Check whether R absorbs the pathway-length effect.
- **Kill criterion.**
  - Abandon if simulations matched for sampling and palaeolatitude error
    cannot separate R = 0.5 from R = 1 for at least half the events.
  - Abandon if warming onset and extinction fall in the same bin for most
    events.
  - Range-edge sampling bias and shelf-area geometry are collinear with R.
- **Links.** Q-015 (thermal-niche evolution), Q-027 (latitudinal gradient),
  Q-031 (body size).
- **Evidence.** [Round-10 note](../literature/2026-10-11-register-checks-round10.md).

## Final addition to the first tranche (Codex, 11 October)

### Q-050 How does the capacity to evolve change during environmental upheaval?
Status **under review**, tier 2 (provisional). The conceptual question and
several component tests are established; novelty and feasibility of the joint
mechanism test remain unverified.

- **Question.** Does the pattern of variation already present within a
  population channel its initial evolutionary response to environmental
  change, and how quickly does that pattern itself reorganise? Can fossil
  sequences distinguish inherited constraints, selection reshaping variation,
  and feedback between them?
- **Why big / boundary.** This asks how the capacity to evolve links variation
  among individuals to long-term evolutionary trajectories. Q-036 concerns
  geographic explanations for stasis; this concerns multivariate variation and
  change, including substantial evolution. Extinction is not a required frame.
- **Nearest work.** Hunt 2007
  ([10.1111/j.1558-5646.2007.00129.x](https://doi.org/10.1111/j.1558-5646.2007.00129.x),
  abs) already tests directional alignment in fossil ostracods. Brombacher et
  al. 2017 ([10.1086/692570](https://doi.org/10.1086/692570), sect) already
  predicts next-sample change from covariance and tests climatic-regime
  breakdown. Their 2023 spatial comparison
  ([10.3389/fevo.2023.1165174](https://doi.org/10.3389/fevo.2023.1165174), sect)
  warns against transfer among populations. Holstad et al. 2024
  ([10.1126/science.adi8722](https://doi.org/10.1126/science.adi8722), main-text
  sections) already evaluates mechanisms and advances fluctuating-optimum
  tracking. Tsuboi et al. 2024
  ([10.1093/jeb/voae103](https://doi.org/10.1093/jeb/voae103), sect) explicitly
  proposes environmental shifts to distinguish constraint from selection
  shaping variation. Neither the correlation nor the broad proposal is new.
- **Residual / discriminator.** Compare explicit models for the joint sequence
  of initial covariance, mean displacement and subsequent covariance
  reorganisation, allowing feedback. Use independently dated environmental
  transitions and, where possible, replicated populations or lineages with
  differing initial covariance. Test predictions of direction, magnitude and
  relaxation time under one observation model. Temporal precedence alone
  cannot establish causation; another alignment regression is insufficient.
- **Data lead.** The [phase-2 numerical inspection](../data/q050-covariance-support/README.md)
  of Tsuboi's versioned [archive](https://doi.org/10.5281/zenodo.13294509)
  confirms means, covariance matrices and specimen counts for two Brombacher
  series, each with 75 samples on an identical stored 474.57-kyr grid.
  `tt` stores elapsed coordinates, not successive increments; this corrects
  our earlier README-based description. Brombacher's
  [Dryad deposit](https://doi.org/10.5061/dryad.8jf2k) lists specimen-level
  measurements and sample ages. The archive objects passed internal numerical
  checks; the original sample/absolute-age/environmental crosswalk, age
  uncertainty and sufficient replication remain unverified. No model was fitted.
- **Main obstacle / kill criterion.** Phenotypic covariance is not genetic
  covariance, and environmental proxies do not identify selection gradients.
  Plasticity, persistent common selection, immigration and temporal mixing
  can mimic the proposed ordering. First test recovery of constrained rival
  models at actual sample spacing and uncertainty. Park the mechanistic route
  if plausible alternatives are observationally equivalent or covariance
  reorganisation is unresolved. This gate is proposed, not passed.
- **Next step and evidence.** Phase 2 has verified two numerical objects;
  establish their original-sample, environmental and age support before a
  bounded simulation. Source
  access, exact data version, rival models and prior-work boundaries are in
  the [Q-050 evidence note](../literature/2026-10-11-evolvability-and-first-tranche-close.md).
