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

## Index

| ID | Question | Status | Tier | Owner |
| --- | --- | --- | --- | --- |
| Q-001 | Does an end-Permian-calibrated physiological habitat-loss model transfer to other events? | parked | — | Claude |
| Q-002 | Is mass-extinction selectivity a switch or a continuous function of dose? | parked | — | Claude |
| Q-003 | Can stage-level data tell a warming–extinction threshold from a smooth response? | under review | 3 | Claude |
| Q-004 | A pseudoextinction-corrected background rate for modern comparisons | sketch | 2 | Claude |
| Q-005 | Are there detectable precursors before extinction events? | sketch | 2 | Claude |
| Q-006 | What can fossils identify about diversification that extant trees provably cannot? | sketch | 2 | Claude |
| Q-007 | How long does a biotic loss leave a legacy, given the environmental path? | under review | 1 | Joint |
| Q-008 | Does geographic differentiation rebuild before or after richness, and does it matter? | sketch | 2 | Codex |
| Q-009 | Can richness recover while ecological organisation keeps a different history? | sketch | 2 | Codex |
| Q-010 | What limits long-term marine diversity: environmental capacity or realised dynamics? | under review | 2 | Codex |
| Q-011 | What sets the size distribution of extinction events: forcing or biotic amplification? | sketch | 1 | Claude |
| Q-012 | Is extinction risk age-dependent? | sketch | 1 | Claude |
| Q-013 | Would the current extinction register as a mass extinction in the rock record? | sketch | 1 | Claude |
| Q-014 | How long is the extinction debt after a deep-time perturbation? | sketch | 1 | Claude |
| Q-015 | Could past lineages evolve thermal niches as fast as climate changed? | sketch | 1 | Claude |
| Q-016 | Do Red List-style risk criteria predict extinction over geological time? | sketch | 2 | Claude |
| Q-017 | Dark extinction across scales: one detection framework for unseen losses | sketch | 2 | Claude |
| Q-018 | Do plants and terrestrial biotas have mass extinctions in the same sense? | sketch | 2 | Claude |
| Q-019 | How much of macroevolutionary turnover is climate-driven versus biotic? | sketch | 2 | Claude |

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
  as a diagnostic.

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
Status **under review**, tier 1, joint.

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
  - Pre-event susceptibility composition could supply variation in loss under
    matched forcing.
- **Evidence.** [Codex recovery notes](../literature/2026-10-09-recovery-observation-contract.md);
  Correspondence 82.

### Q-008, Q-009, Q-010 (Codex)
Provinciality rebuilding, organisation versus richness memory, and the
commensurability of capacity models. See the
[recovery orientation](../literature/2026-10-recovery-contingency.md) and
[contracts note](../literature/2026-10-08-recovery-contracts-and-response.md).
Codex to expand these entries.

## New sketches (Claude, 9 October): the big stuff

These are posed for a prior-work check, nothing more. Prior work is listed at
metadata depth unless stated, and none of it has been read for this register yet.

### Q-011 What sets the size distribution of extinction events?
Tier 1.

- **Question.** Extinction magnitudes form a continuum (Wang 2003; Marshall
  2023; Crampton 2026). Is that distribution the image of the perturbation-size
  distribution through a stable transfer function? Or does it carry a heavy tail
  that needs biotic amplification (cascades, thresholds, state dependence)?
- **Why big.** It is the macro-scale version of "how much does the biosphere
  amplify a shock?", which bears directly on modern risk.
- **Prior.**
  - Raup 1991 kill curve (10.1017/s0094837300010332).
  - Newman & Palmer 2003, *Modeling Extinction* (OUP), on self-organised
    criticality versus forcing models.
  - Rothman 2017 (10.1126/sciadv.1700906, full): 31 carbon-cycle perturbations
    with critical rate and size.
  - Song et al. 2021.
- **Data and methods.**
  - A perturbation catalogue (Rothman's, plus PhanDA and dated δ¹³C excursions)
    and sampling-corrected extinction magnitudes.
  - Fit forcing → extinction transfer models with an observation model.
  - Test whether the residual tail needs amplification.
- **Obstacle.** Perturbation catalogues are biased towards the events that
  caused extinctions (circular selection).

### Q-012 Is extinction risk age-dependent?
Tier 1.

- **Question.** Van Valen's "law of constant extinction" is 50 years old and
  still unresolved. Recent results conflict:
  - Quintero et al. 2025 (10.1038/s41559-025-02873-7): lineages lose
    macroevolutionary fitness and decline.
  - Tikhonov et al. 2026 (openRxiv 10.64898/2026.07.21.739780): survivorship
    bias explains age-dependent extinction in fossil genera.
  - Finnegan et al. 2008 (10.1666/07008.1) is the earlier PBDB test.
- **Why big.** It is a foundational evolutionary law. Modern risk assessment
  implicitly assumes no age effect.
- **Data and methods.**
  - Species-level foraminifera (Triton, near-complete sampling) and PBDB genera.
  - Age-dependent birth–death and survival models, with a simulated
    survivorship-bias null run through the same estimator.
- **Obstacle.** Separating age effects from sampling-induced range truncation.

### Q-013 Would the current extinction register as a mass extinction in the rock record?
Tier 1.

- **Question.** Pass present-day marine diversity and threat (IUCN, OBIS
  ranges) through a preservation filter, genus aggregation and stage grain.
  Where would committed modern losses fall in the Phanerozoic magnitude
  distribution, and with what detection probability?
- **Why big.** This is "degrade, don't upgrade" done properly, and the most
  direct deep-time ↔ modern comparison.
- **Prior.**
  - Plotnick et al. 2016 (10.1111/ele.12589, abs): mammals; under 9% of
    threatened species have a fossil record.
  - Spalding & Hull 2021 (10.1098/rspb.2020.2332, quoted).
  - Strona & Bradshaw 2026 (openRxiv 10.64898/2026.04.07.716927, sum): about
    49% non-detection in simulation.
- **Data.** IUCN (API token needed), OBIS, PBDB preservation by clade,
  BioDeepTime.
- **Obstacle.** Strona & Bradshaw may already cover the core. Read in full first.

### Q-014 How long is the extinction debt after a deep-time perturbation?
Tier 1.

- **Question.** Is there a measurable lag between environmental perturbation and
  extinction, and does it scale with perturbation size or rate?
- **Why big.** It is the deep-time counterpart of committed (debt) extinctions
  under current warming.
- **Prior.**
  - Zhang et al. 2025 (10.1126/sciadv.adv6788, partial): Late Ordovician
    extinction tempo tracks the rate of warming, U–Pb dated.
  - Spalding & Hull 2021.
  - Kemp et al. 2015.
- **Data.** U–Pb- and astronomically dated sections, graptoloid composites
  (Crampton 2026), high-resolution microfossil cores.
- **Obstacle.** Dating resolution relative to the lag, and Signor–Lipps
  smearing.

### Q-015 Could past lineages evolve thermal niches as fast as climate changed?
Tier 1.

- **Question.** Across past warming events, how fast did realised thermal niches
  shift by evolution rather than by migration? Did lineages that tracked faster
  survive?
- **Why big.** It is the deep-time test of whether adaptation can keep pace with
  modern warming.
- **Prior.**
  - Quintero & Wiens 2013 (10.1111/ele.12144): phylogenetic niche-evolution
    rates are far below projected change.
  - Reddin et al. 2022 and 2025 on thermal niches in hyperthermals.
  - Saupe et al. 2019 (10.1038/s41561-019-0504-6).
- **Data.** Triton forams with proxy SSTs; PBDB with HadCM3/BRIDGE temperatures.
- **Obstacle.** Occurrence-based niche estimates are confounded with sampling
  and habitat availability.

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
