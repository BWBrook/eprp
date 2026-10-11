# Phase 2 portfolio: Claude's first pass at categorising, ranking and planning

Owner: Claude | Date: 11 October 2026 | Status: **first pass, for Codex to challenge**

## Why this document exists

Barry's direction in Claude chat on 11 October 2026, quoted exactly:

> "Ahh, I'm not the one who is going to be critiquing and ranking (yet).
> Eventually, I'll help select the highest priority question to elevate to an
> actual research project, but that is some way off. What I'd like next is for
> you and Codex to work on categorising, ranking/prioritising and diving deeper
> into the current question list, especially with respect to what sort of
> contextual and data-availability work could be done productively by you two
> in phase 2. So let's keep iterating. Your first pass at this: expect a lot of
> back and forth, which is fine and expected. We're not after "an answer" yet!"

This is a starting position, not a decision.
- Scores are my opinions, given so that Codex can disagree with specific
  numbers rather than with an overall impression.
- No register entry's status or tier is changed by this document.

## What the first tranche shows

- **50 entries.** 40 are under review, 4 are sketches and 6 are parked. 36 are
  Claude's, 13 Codex's, and Q-007 is joint.
- **No entry survived at tier 1.** Every candidate first rated tier 1 (Q-007,
  Q-022, Q-027, Q-038, Q-044) dropped to tier 2 after checking. Each time,
  either the broad idea had close precedents, or the first estimand could not
  support the claim.
- **What survived is usually narrower and better specified:** a precise
  estimand, a design and a kill criterion. The register's main asset is
  therefore a set of well-posed, partly open questions, not a set of untouched
  big ideas.
- **The commonest next step is the same kind of task.** Almost every surviving
  entry's next step is one of three:
  - a **data-contract check** (is the needed data openly available, in the
    right form?);
  - an **identifiability or power gate** (can the question be answered at
    realistic sampling and dating resolution?);
  - a **deeper prior-work check** than our bounded scans.

  All three are work we can do ourselves, without new data collection. That
  makes them the natural content of phase 2.

## 1. Categories

Each active entry has one primary theme; cross-links are in the scores table.

| Theme | Entries | The shared question |
| --- | --- | --- |
| **A. Measuring the present against the past** | Q-004, Q-013, Q-017, Q-034, Q-042 (and parked Q-045) | Are the baselines and magnitudes used to compare today with the fossil record sound? |
| **B. Predicting who dies** | Q-012, Q-016, Q-020, Q-022, Q-028, Q-037, Q-038, Q-049 (and parked Q-001, Q-002) | How predictable is which lineages are lost, and from what information? |
| **C. Forcing, response and the Earth system** | Q-003, Q-011, Q-014, Q-015, Q-021, Q-030, Q-031, Q-035, Q-041 | How does extinction scale with the size, rate and type of environmental forcing, and has that changed? |
| **D. Spatial structure of diversity** | Q-008, Q-025, Q-027, Q-029, Q-040, Q-044 | How do local, regional and global diversity relate, and what sets the gradients? |
| **E. Regulation and drivers of diversity** | Q-010, Q-019, Q-023, Q-039 (and parked Q-046) | What limits and drives diversification over long timescales? |
| **F. Recovery, legacies and evolutionary futures** | Q-007, Q-009, Q-026, Q-036, Q-048, Q-050 (and parked Q-043) | What do losses leave behind, and what can evolve afterwards? |
| **G. Biotic mixing and contingency** | Q-033, Q-047 | Do arrival order and biotic interchange shape outcomes predictably? |
| **H. Detection and early warning** | Q-005, Q-006, Q-018, Q-024 (and parked Q-032) | What can the record detect, and can crises be anticipated? |

A cross-cutting tag matters for ranking: **modern transfer**, meaning entries
whose answer changes how a modern conservation or risk number is read. They
are Q-004, Q-013, Q-016, Q-017, Q-024, Q-025, Q-027, Q-028, Q-030, Q-034,
Q-037, Q-038, Q-042, Q-047 and Q-049.

## 2. Ranking rubric (first pass)

Four scores, each from 1 to 3, are given separately rather than summed, so
the reasons stay visible.
- **S, significance.** How much changes if the question is answered: field
  consequence and modern transfer.
- **O, openness after checks.** 3: the residual is clearly open after a bounded
  check. 2: a narrowed residual remains. 1: mostly occupied.
- **D, data readiness.** 3: the open data needed are verified accessible. 2:
  the data exist, but access or form is unverified or needs rebuilding. 1: a
  real data gap.
- **G, gate cost.** 3: a decisive first gate we can run ourselves now
  (simulation, power analysis, analytic note or data-contract check). 2:
  moderate. 1: the gate needs external data, people or long compilation.

Priority bands combine the scores by judgement:
- **A:** high S, with an open or narrowed residual and a cheap decisive gate.
  These are phase-2 focus candidates.
- **B:** worth developing context and data contracts; gates are moderate.
- **C:** hold, merge or park candidates.

## 3. Scores and proposed phase-2 action

| ID | Short title | Theme | S | O | D | G | Band | Proposed phase-2 action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q-004 | Pseudoextinction and the background rate | A | 3 | 2 | 2 | 2 | **A** | Data contract for clades with both fossils and trees; a small BDC sensitivity calculation on published rates |
| Q-013 | Would today's extinction register in the rock? | A | 3 | 2 | 1 | 2 | B | Check the IUCN API terms; build the genus-aggregation logic on one well-assessed clade (Codex's crosswalk) |
| Q-017 | Modern and fossil estimators of unseen losses | A | 2 | 3 | 2 | 3 | **A** | Analytic note on equivalence; it needs no data and serves Q-004, Q-026 and Q-034 |
| Q-034 | Island extinction baseline before people | A | 2 | 2 | 2 | 2 | B | Merge into Q-004 as its island branch; data contract for the Rozzi and Cooke deposits |
| Q-042 | Species-level magnitude of mass extinctions | A | 2 | 3 | 2 | 3 | **A** | Simulation of genus-to-species inversion bias; data contract for the Wang and Fan species data |
| Q-012 | Heritable susceptibility versus ageing | B | 2 | 2 | 2 | 2 | B | Prior check against Tikhonov 2026 and Quintero 2025; Triton/Aze lineage data contract |
| Q-016 | Range-based risk criteria over geological time | B | 2 | 2 | 3 | 3 | B | Neptune data contract; possibly the cheapest real pilot in the register (open microfossil data) |
| Q-020 | When range stops insuring against extinction (Codex) | B | 2 | 2 | 1 | 1 | C | Hold until a prediction beyond existing models is specified |
| Q-022 | Phylogenetic diversity lost per extinction | B | 2 | 2 | 1 | 3 | B | Run the designed power calibration on existing trees; find mass-extinction trees with survivors |
| Q-028 | Winners of past and present crises | B | 2 | 2 | 2 | 2 | B | Pair with Q-038; data contract for trait sources |
| Q-037 | Top-down trophic signature | B | 1 | 2 | 2 | 2 | C | Park unless a trophic effect independent of size is plausible; fold into Q-038 |
| Q-038 | How predictable is which genera die? | B | 3 | 2 | 2 | 2 | B (deferred) | Deferred by Barry; keep the gate record |
| Q-049 | Isotherm tracking ratio and extinction | B | 3 | 2 | 2 | 3 | **A−** | Simulation of R separability at PBDB resolution; data contract for the Reddin and Malanoski deposits |
| Q-003 | Threshold versus smooth response, detectability | C | 1 | 2 | 2 | 3 | C | Merge into Q-011 as its power component |
| Q-011 | Size distribution of extinction events | C | 3 | 2 | 2 | 2 | B | Compile a perturbation catalogue chosen independently of extinction (shared with Q-030) |
| Q-014 | Extinction debt after perturbation | C | 1 | 2 | 1 | 1 | C | Park; resolution is the binding limit |
| Q-015 | Thermal-niche evolution keeping pace | C | 2 | 1 | 2 | 2 | B− | First check the Antell & Saupe 2021 overlap, which is still open |
| Q-021 | Lost functions prolonging recovery (Codex) | C | 3 | 2 | 2 | 2 | B | Codex's map of mechanisms and proxies, then distinguishable joint predictions |
| Q-030 | Declining sensitivity to perturbation | C | 3 | 2 | 2 | 2 | **A−** | The gate is a compilation: count post-Jurassic events with independent forcing. Shared catalogue with Q-011 |
| Q-031 | Shrinking per °C | C | 2 | 1 | 3 | 2 | C | The Nätscher Zenodo data are open. Hold unless the PNAS supplement leaves the partition open |
| Q-035 | Land-before-sea lag | C | 1 | 2 | 1 | 1 | C | Park; dating errors are comparable to the lags |
| Q-041 | Periodicity with propagated uncertainty | C | 2 | 2 | 2 | 2 | B | Codex's suggested null fixture: specify the likelihood and exposure contract first |
| Q-008 | Differentiation and recovery (Codex) | D | 2 | 2 | 2 | 2 | B | Training-only bioregion partitions (Codex) |
| Q-025 | Local to global extinction scaling | D | 3 | 2 | 2 | 3 | **A−** | Run the stationary-range sampling null on PBDB geometry; it is decisive and cheap |
| Q-027 | Latitudinal gradient as a climate-state variable | D | 3 | 2 | 3 | 3 | **A** | Jones-style power simulation on the real sampling windows; Benson Dryad and Zenodo data contract |
| Q-029 | Ordering of isolation cycles (Codex) | D | 1 | 1 | 1 | 1 | C | Park |
| Q-040 | Marine alpha–beta history | D | 3 | 1 | 2 | 2 | B | Pair with Q-044; crowded, with scoop risk |
| Q-044 | Land diversity and bounded regional richness | D | 3 | 2 | 3 | 2 | **A** | Data contract for the Close 2019 Dryad deposit; screen joint support (windows × bins) |
| Q-010 | Biological construction of capacity (Codex) | E | 3 | 2 | 2 | 1 | B | Codex: identify one innovation with independent functional evidence |
| Q-019 | Climate versus biotic drivers | E | 2 | 1 | 2 | 2 | C | Keep as context; Rineau 2022 occupies the headline |
| Q-023 | Origination failure versus extinction spikes | E | 2 | 2 | 3 | 3 | B+ | Rerun Bambach's partition with modern rates on the shared PBDB engine |
| Q-039 | Coupling of evolutionary faunas | E | 2 | 2 | 2 | 2 | B− | Identifiability simulation for coupling at about 50–100 bins |
| Q-007 | Biotic legacy given the environmental path (joint) | F | 3 | 2 | 1 | 2 | C | Hold; the Triton gate left only an EOT pilot |
| Q-009 | Ecological memory after recovery (Codex) | F | 2 | 2 | 1 | 2 | B− | Codex: an independently measured outcome first |
| Q-026 | Reversible versus terminal clade decline (Codex) | F | 2 | 2 | 2 | 2 | B | Codex: one cohort with a mapping from latent counts to observations |
| Q-036 | Stasis and geography (Codex) | F | 1 | 1 | 1 | 2 | C | Paused by Codex |
| Q-048 | Predator release and prey persistence (Codex) | F | 2 | 2 | 1 | 1 | C | Hold unless the reframing around predators returning (king crabs) earns it |
| Q-050 | Changing capacity to evolve (Codex) | F | 2 | 2 | 2 | 2 | B | Codex: model recovery at real sample spacing |
| Q-033 | Arrival order and radiation (Codex) | G | 2 | 2 | 1 | 1 | C | Hold until crossed pairs are counted |
| Q-047 | Past interchanges as forecasts | G | 3 | 3 | 2 | 1 | B+ | Outcome and denominator crosswalk on one taxon first |
| Q-005 | Precursors before extinction events | H | 2 | 2 | 2 | 3 | B | Sampling-surrogate pilot on the graptoloid composite |
| Q-006 | Fossils versus trees identifiability | H | 1 | 1 | 3 | 2 | C | Park after a quick check for a published power criterion |
| Q-018 | Plants and mass extinction | H | 2 | 2 | 2 | 2 | B | Watch the McElwain 2026 preprint; it may occupy the question |
| Q-024 | Early-warning calibration on Quaternary transitions | H | 2 | 2 | 3 | 2 | **A−** | Data contract for LegacyPollen and LegacyAge; screen how many transitions survive the length and resolution filters |

**First-pass A band** (A and A−): Q-004, Q-017, Q-042 (baselines and
magnitudes); Q-027, Q-044, Q-025 (spatial structure); Q-030 and Q-049
(forcing and response); Q-024 (early warning).
- Seven of the nine are mine. That partly reflects ownership: I know my
  entries' gates better.
- Codex should test whether its own Q-010, Q-021 and Q-026 deserve A on
  significance.

## 4. Phase-2 work packages

Most of the value is in shared work that serves several entries at once.

**WP1. Data-contract registry** (Claude to lead, Codex to audit).
- Extend `resources/catalogue.tsv` into a matrix of datasets against the
  entries that use them.
- For each dataset record: the deposit, the licence, whether anonymous
  download works, the fields, the unit of observation, the version and
  whether the predictors are available before the event.
- First rows, all named in entries, several already partly checked:
  - Benson et al. 2025 (Dryad and Zenodo); Close et al. 2019 (Dryad);
  - Monarrez 2023 (Dryad blocked; Zenodo float corruption);
  - Neptune Sandbox Berlin; Triton; the Aze/Fordham lineages; LegacyPollen
    and LegacyAge;
  - the Reddin 2018 and Malanoski 2026 deposits; Rozzi 2023; Cooke 2023;
  - Nätscher 2026 (Zenodo); Tsuboi (Zenodo); the Cantalapiedra trees;
  - PhanDA and PhanSST; GRIIS and GloNAF; NOW; Neotoma.
- It is low risk, high value and entirely within our capabilities. It also
  turns many "data unverified" notes into facts.

**WP2. A shared engine for PBDB and chronology** (Codex to lead, since it
already holds PBDB preparation).
- One documented pipeline: occurrence extraction with a recorded query and
  date, taxonomy cleaning, spatial standardisation (divvy or MST windows),
  coverage standardisation, and three-timer or gap-filler rates.
- A GTS2020 Monte Carlo chronology with shared boundaries.
- It serves Q-011, Q-019, Q-023, Q-025, Q-027, Q-030, Q-038, Q-039, Q-040,
  Q-041, Q-044 and Q-049.
- It is not a research result. It removes the most-repeated setup cost, and
  it fixes the data vintage of record (a Q-045 lesson).

**WP3. A battery of cheap identifiability and power gates.**
- Each fixture decides whether an entry can be answered at realistic
  resolution, before any empirical fit.
- In rough order of cost:
  1. Q-042 genus-to-species inversion bias (pure simulation).
  2. Q-049 separability of R at PBDB resolution.
  3. Q-027 recovery of the climate–slope coefficient on real sampling windows
     (Jones-style).
  4. Q-025 stationary-range null.
  5. Q-022 power calibration (already designed).
  6. Q-005 sampling surrogate.
  7. Q-041 null fixture (after Codex's exposure contract).
  8. Q-039 identifiability of coupling.
- Reuse existing simulators before building new ones: PyRate's simulator, the
  DeepDive spatial simulator (Cooper et al. 2024), and gen3sis for spatial
  eco-evolution. Each needs a capability check first.
- Runtime is small (laptop scale), apart from any spatial simulation sweeps,
  which could use kunanyi once Barry opens the jumpbox.

**WP4. Deep prior-work reviews for the A band.**
- Our checks so far were bounded scans, typically 30–60 records with 5–12
  read closely. Before Barry chooses, the top candidates need systematic
  searches with a documented strategy and stated recall limits.
- One review per A-band entry, perhaps three or four in parallel, with Codex
  auditing each other's.

**WP5. Theory and methods notes that serve several entries.**
- (a) Equivalence of estimators of unseen extinction: Q-017, Q-026, Q-034,
  Q-004.
- (b) Price-type partition into within-unit and among-unit change: Q-030,
  Q-031, Q-036, Q-050.
- (c) A hierarchical diversity-accounting identity with area counterfactuals:
  Q-025, Q-040, Q-044. Codex's weighted identity is the start.
- (d) Generative nulls on an irregular stage grid: Q-041, Q-003, Q-011.

These are short documents, with no data needed and checkable algebra. They
prevent each entry from re-deriving the same machinery.

**WP6. Consolidation.**
- Proposed merges or pairings:
  - Q-003 into Q-011.
  - Q-034 into Q-004.
  - Q-037 into Q-038.
  - Q-040 and Q-044 run as twins.
  - Q-016 and Q-038 as a "predictive extinction" pair (Q-016 is the
    open-data pilot).
  - Q-005 and Q-024 as siblings in deep and Quaternary time.
- Proposed parks: Q-014, Q-029, Q-035, Q-006, and possibly Q-036 and Q-020.

The register would then hold about 40 active entries with sharper boundaries.

## 5. A proposed division of labour, for discussion

- **Claude:** WP1 (registry), WP5 (a) and (c), WP3 fixtures for Claude-owned
  A-band entries, and a WP4 review of one A-band entry.
- **Codex:** WP2 (PBDB and chronology engine), WP5 (b) and (d), WP3 fixtures
  for Q-041's exposure contract and its own entries, a WP4 audit, and
  adversarial review of all of the above.
- Both: argue the scores. Every change of band should be recorded with a
  reason, as tier changes are now.

## 6. Questions for Codex

1. Is the rubric right? Should "modern transfer" be a separate score, or
   should G (gate cost) carry less weight than S? I may be over-rewarding
   cheapness.
2. Which of your entries do you think are under-scored? Q-010, Q-021 and
   Q-026 are candidates for higher S.
3. Do you agree with the proposed merges and parks (WP6)? Which do you
   reject?
4. WP2: is a shared engine premature before WP1 confirms which datasets each
   A-band entry needs? I lean towards WP1 first and WP2 in parallel only for
   the PBDB core.
5. WP3: should the fixtures share one simulator? DeepDive's spatial simulator
   is the candidate. Or does that hide entry-specific assumptions?
6. Is anything missing from the A band that a downstream team would most
   regret not having been told about?
