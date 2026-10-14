# Blue-sky ideation: Claude's independent list

Owner: Claude | 14 October 2026 | **Frozen before reading any Codex list.**
Format and mandate are in [register-blue-sky.md](register-blue-sky.md).
Codex's refinements of the format (76/1618) are applied:
- generate first, then ground;
- two extra fields, *understanding changed* and *new capability*;
- overlap with Q entries recorded;
- simulation earns its place through identification, contrast or
  impossibility results, not by reproducing curves.

**Method.**
- I generated about 30 pure deep-time questions and kept 12 for grounding.
  The geography-only candidate became the first worked contrast inside C1.
- Each was given a **target-matched prior check**: three Sonnet subagents
  searched Crossref, OpenAlex, Europe PMC and Semantic Scholar, with
  bounded queries, and were barred from the repository.
- They verified every DOI against Crossref; I re-verified twelve key DOIs.
  Access depth is "abs" (abstract) unless marked "full".
- **"Open" means not found in a bounded search.** OpenAlex rate limits cut
  some searches short (noted where it matters).
- Anchoring: Codex's 76/1618 contained no seeds, and I have read no Codex
  list.

**Ratings:** I = importance, T = demonstrated or plausible tractability,
V = value of the next work, each H, M or L. These are provisional.

---

## C1. Which macroevolutionary hypotheses can the Phanerozoic record actually discriminate?

- **Question.** Run forward eco-evolutionary simulations on reconstructed
  palaeogeography and climate. Pass them through taphonomic and sampling
  filters calibrated to the real record: rock availability from
  Macrostrat, and collection geography and intensity from PBDB. Which major
  hypotheses can the real record distinguish, and which can it not?
  Candidates:
  - global diversity-dependence versus unbounded growth;
  - competitive versus opportunistic clade replacement;
  - pulsed versus continuous turnover;
  - regional versus global limits;
  - geography-and-climate-only models versus diversity-dependent spatial
    models (see the worked contrast below).
- **Understanding changed.** It would replace decades of argument about
  whether a pattern is "real" with an explicit map of what the record *can*
  answer. Several debates would either become decidable or be shown
  undecidable on current data, which is an impossibility result.
- **New capability.** Spatially explicit simulators (gen3sis; the DeepDive
  simulator); open palaeogeography (PALEOMAP PaleoDEMs); Macrostrat; PBDB
  sampling geography; pipelines for stratigraphic filters (StratPal); and
  enough compute (kunanyi) for many full-Phanerozoic replicates.
- **Closest prior; residual.**
  - Estimator benchmarks: DeepDive, Cooper et al. 2024,
    10.1038/s41467-024-48434-7 (full).
  - Single-hypothesis sampling nulls: Dunne et al. 2023,
    10.1038/s41559-023-02128-3 (full); Phillipi et al. 2024,
    10.1017/pab.2024.26.
  - Smiley 2018 (10.1017/pab.2017.28): four hypotheses × six preservation
    scenarios, but one region and one data type.
  - Rineau et al. 2022 (full): their test of diversity dependence has null
    simulations only, with no positive controls, so no power.
  - **Residual: a table of power and false positives across several
    hypotheses, under a Phanerozoic sampling filter. Not found.** A 2025
    review (Allen, Warnock & Dunhill, 10.32942/x2dd1v) lists simulation
    tests of method efficacy as a gap.
- **Worked contrast (absorbs candidate C2).** Do geography-and-climate-only
  models and diversity-dependent spatial models predict different *sampled*
  spatial structure (regional richness, beta between regions, gradient
  shape)? The geography-and-climate-only model is Balembois et al. 2025,
  10.1038/s41467-025-63428-9 (full: no sampling filter; r = 0.73 with
  global curves). The diversity-dependent one is Cermeño et al. 2022,
  10.1038/s41586-022-04932-6 (full: "can be sampled in different ways",
  not done).
- **Overlap.** Q-006, Q-026, Q-039, Q-041 and parked Q-019. The target
  differs: a discriminability atlas across hypotheses. It would directly
  answer why Q-019 was parked (identifiability).
- **Observation model.** Rock availability, facies and collection
  geography; time-averaging; taxonomic resolution and lumping; stage
  binning.
- **Route.** Simulators and deposits (DeepDive Zenodo 10979237; Dunne OSF
  ZGHWB; Balembois figshare 27201498; PALEOMAP Zenodo 5348492); the
  Macrostrat and PBDB APIs; kunanyi once Barry opens the jumpbox. A
  bounded local pilot comes first.
- **Test, informative either way.** For each hypothesis pair, fix in
  advance a minimum useful power (for example 0.8 at a 0.05 false-positive
  rate) at realistic effect sizes. Discriminable pairs then earn empirical
  tests. Non-discriminable pairs are a publishable impossibility result
  that redirects effort.
- **Ratings: I H, T M, V H.** My flagship.

## C3. How much of the Phanerozoic's pulsed turnover is manufactured by stratigraphic architecture?

- **Question.** Forward-simulate occurrences under constant biological
  rates through stratigraphic columns calibrated to Macrostrat
  (unconformities, facies shifts, sea-level cycles). What share of the
  observed clustering of first and last appearances at stage and sequence
  boundaries in PBDB does the architecture alone reproduce?
- **Understanding changed.** It tells us how much of the "pulsed" history
  of origination and extinction is biology. That bears on the reality of
  minor extinction pulses and on the pulsed-versus-continuous debate.
- **New capability.** Macrostrat's Phanerozoic column database, PBDB, and
  StratPal (Hohmann & Jarochowska 2025, 10.1111/2041-210x.14507), which
  makes forward stratigraphic filtering practical at scale.
- **Closest prior; residual.**
  - The mechanism is established at basin scale or for single events:
    Holland & Patzkowsky 2015, 10.1111/pala.12188; Zimmt et al. 2020,
    10.1111/pala.12505; Nawrot et al. 2018, 10.1098/rspb.2018.1191.
  - Phanerozoic-wide *correlations* exist (Peters 2005,
    10.1073/pnas.0502616102).
  - Foote 2005 tests pulsing without architecture.
  - **Residual: a Phanerozoic-wide architectural share from forward
    models, compared with PBDB. Not found.**
- **Overlap.** Q-005, Q-041, Q-035 and Q-023 involve timing artefacts. The
  target differs: the global architectural share of boundary clustering.
- **Observation model.** Macrostrat column completeness and facies; PBDB
  sampling by collection; stage-boundary placement; the age model.
- **Route.** Macrostrat and PBDB APIs (open), with StratPal. Local compute
  is enough for a pilot on one era.
- **Test.** The architecture-only model either reproduces the observed
  clustering within an interval fixed in advance (the architectural share
  is high), or leaves an excess. Both are informative, and the share is
  the reported quantity.
- **Ratings: I M–H, T M–H, V H.**

## C4. Do survivors of mass extinctions occupy predictable refugia, and are refugium environments shared across events?

- **Question.** With detection modelled (so that Lazarus taxa count as
  survivors that went unseen, not as absences), are the environments
  where survivors persist consistent across the Big Five? The candidate
  variables are palaeolatitude, depth, upwelling, oxygenation and
  lithofacies.
- **Understanding changed.** It would show whether persistence through
  crises depends on a generic environmental "safe space" or is
  event-specific. That separates physiological from geographic routes to
  survival.
- **New capability.** Detection-aware occupancy models on PBDB with
  palaeocoordinates; Macrostrat facies; climate-model and oxygenation
  fields (cGENIE, HadCM3).
- **Closest prior; residual.**
  - Wignall & Benton 1999, 10.1144/gsjgs.156.3.0453: a coarse test,
    concluding rarity rather than refugia.
  - Single-event cases: Foster et al. 2023, 10.1029/2023pa004766.
  - Penn et al. 2018, 10.1126/science.aat1327: end-Permian physiological
    biogeography.
  - Monarrez et al. 2023: range selectivity, not environments.
  - **Residual: a cross-event, detection-aware comparison of refugium
    environments. Apparently open, weakly**, given incomplete searches.
- **Overlap.** Q-020, Q-001 and Q-049. The target differs: the
  environments of persistence across events.
- **Observation model.** Lazarus detection, regional sampling gaps and
  palaeocoordinate uncertainty; facies-dependent preservation.
- **Route.** PBDB and Macrostrat (open); climate fields (named); occupancy
  modelling.
- **Test.** A refugium-environment signature that replicates across at
  least three events beyond a detection-null threshold, or event-specific
  signatures. Either outcome is informative.
- **Ratings: I M–H, T M, V M.**

## C5. Do ecosystems reassemble in a repeatable order after crises?

- **Question.** After each major Phanerozoic crisis, do functional groups
  (tiering, motility, feeding) re-emerge in a shared order, beyond what
  recovery of richness alone implies? Is the order bottom-up or top-down?
- **Understanding changed.** It would settle whether recovery follows
  assembly rules (a deterministic ecological succession on macro
  timescales) or contingent histories. The best end-Permian accounts
  conflict:
  - Chen & Benton 2012 (10.1038/ngeo1475) describe a bottom-up recovery;
  - Song, Wignall & Dunhill 2018 (10.1126/sciadv.aat5091) describe a
    top-down one.
- **New capability.** Ecospace coding over PBDB at Phanerozoic scale;
  simulators of ecospace assembly (the CRAN `ecospace` package); sampling
  nulls for when a guild first reappears.
- **Closest prior; residual.**
  - Foster & Twitchett 2014 (10.1038/ngeo2079), Edie, Jablonski & Valentine
    2018 (10.1073/pnas.1717636115), Cribb et al. 2023
    (10.1098/rspb.2023.2232) and Dunhill et al. 2024
    (10.1038/s41467-024-53000-2) cover single events or two realms.
  - **Residual: a sampling-aware test of a shared order across three or
    more events. Not found.**
- **Overlap.** Q-009 and Q-007. The target differs: a shared reassembly
  order across events.
- **Observation model.** Guild detection depends on sampling and on how
  preservable the guild is (soft-bodied predators). Time-averaging can
  blur the order.
- **Route.** PBDB with ecospace coding; the Dunhill Zenodo deposit
  11400588; simulation of the detection null.
- **Test.** A rank concordance of re-emergence order across events,
  compared with a sampling null that accounts for detection. High
  concordance supports assembly rules; concordance no better than the null
  supports contingency.
- **Ratings: I H, T M, V M–H.**

## C6. How common is competitive displacement between clades, with calibrated error?

- **Question.** Across many Phanerozoic clade pairs with overlapping
  ecology, how often do diversity dynamics support competitive
  displacement (one clade's rates depend on the other's diversity) rather
  than independent or opportunistic replacement? False-positive rates are
  to be calibrated by simulation.
- **Understanding changed.** It would turn "double-wedge" anecdotes into a
  prevalence estimate of whether biotic interactions drive macroevolution.
- **New capability.** Multiple-clade diversity-dependence (MCDD) and
  stochastic-differential-equation (SDE) frameworks; PBDB; simulation for
  calibration.
- **Closest prior; residual.**
  - Silvestro et al. 2015, 10.1073/pnas.1502803112.
  - Liow, Reitan & Harnik 2015, 10.1111/ele.12485.
  - Pires et al. 2017, 10.1111/evo.13269 (22 carnivoran families).
  - Lidgard et al. 2021, 10.1098/rspb.2021.1632.
  - Song et al. 2026 (10.1038/s41559-026-03134-x): 12 clades, on extinction
    rather than paired dependence.
  - **Residual: a Phanerozoic-wide, multi-order census of pairs with
    calibrated false positives. Not found.**
- **Overlap.** Q-039 and Q-033. The target differs: prevalence with
  calibrated error.
- **Observation model.** Shared sampling between paired clades
  (correlated detection) can mimic coupling, as can shared environmental
  forcing.
- **Route.** PBDB, PyRate MCDD, and the Lidgard Dryad deposit
  (10.5061/dryad.zpc866t6s).
- **Test.** A prevalence estimate with an interval, after calibration
  against null pairs simulated under shared sampling and forcing.
- **Ratings: I M–H, T M, V M.**

## C7. Are "living fossils" statistically exceptional?

- **Question.** Under birth–death and trait-evolution models with rates
  that vary among lineages, and with fossil sampling included, how often
  should lineages combining very long persistence with low rates arise?
  Are the observed ones more frequent than that?
- **Understanding changed.** It would show whether bradytely needs a
  special explanation (constraint, stable niches) or is the expected tail
  of heterogeneous rates.
- **New capability.** Simulation of trait evolution together with
  birth–death and sampling (FossilSim and related tools).
- **Closest prior; residual.**
  - Bennett et al. 2016, 10.1017/pab.2016.36: extant trees only.
  - Budd & Mann 2025, 10.1093/sysbio/syaf020: analytic, extant data.
  - Cascini et al. 2026 bioRxiv, 10.64898/2026.10.03.756400 (full): an
    empirical contrast with sister groups.
  - **Residual: a fossil-sampled simulation null for how often living
    fossils occur. Not found.**
- **Overlap.** Loosely Q-012. The target differs.
- **Observation model.** Morphological rate estimated from fossil
  morphology; how long a lineage persists depends on its sampling.
- **Route.** FossilSim and RevBayes; published matrices of living-fossil
  clades.
- **Test.** Observed counts compared with the null's predictive interval,
  for a definition of "living fossil" fixed in advance.
- **Ratings: I M, T M, V M.**

## C8. Does origination follow the kinetic (metabolic) temperature prediction across the Phanerozoic?

- **Question.** Is per-capita origination Arrhenius-like in temperature,
  with E near 0.65 eV, once sampling, diversity dependence and the
  uncertainty in temperature reconstruction (the PhanDA ensemble) are
  modelled jointly?
- **Understanding changed.** It is a direct test of a quantitative
  theory: that metabolism sets the tempo of evolution.
- **New capability.** The PhanDA ensemble with its uncertainty;
  capture–recapture rates from PBDB.
- **Closest prior; residual.** This one is the most occupied of the list.
  - Allen et al. 2006 (10.1073/pnas.0603587103): forams, 30 Myr.
  - Mayhew et al. 2008 and 2012.
  - Rineau et al. 2022 (full): taxon-specific.
  - Wilson, Reitan & Liow 2024 (10.1098/rspb.2024.0165, full): an SDE
    with Scotese temperatures; origination link p = 0.052, not
    significant after correction.
  - Signs conflict (Zhang et al. 2025, 10.1126/sciadv.adv2549).
  - **Residual: the specific test of kinetic form, with PhanDA
    uncertainty. Narrow.**
- **Overlap.** Q-015 and parked Q-019. The target differs: a theory's
  functional form.
- **Observation model.** Covariance between sampling and temperature;
  the age model; PhanDA's bin-level dependence.
- **Route.** PBDB; PhanDA (held); Wilson's OSF deposit (5JAFU).
- **Test.** The posterior for E, against 0.65 eV and against 0.
- **Ratings: I M–H, T M, V L–M.** Hold unless a sharper contrast appears.

## C9. What sets the lag between disparity and diversity, and do mass extinctions reset it?

- **Question.** Across many fossil clades, estimate the lag between the
  peak of morphological disparity and the peak of taxonomic diversity.
  Regress it on extinction bottlenecks, selectivity and clade age, and
  test its sensitivity to the disparity metric and to sampling.
- **Understanding changed.** It would show when, and why, form and number
  decouple: the macroevolutionary architecture of innovation.
- **New capability.** Compiled morphological matrices; disparity tooling
  (dispRity); PBDB diversity.
- **Closest prior; residual.**
  - Hughes, Gerber & Wills 2013 (10.1073/pnas.1302642110, full) use 98
    clades but a shape summary, not a lag.
  - Puttick et al. 2020 (10.1111/evo.14078, full) show that the choice of
    metric changes inference.
  - Single-clade decoupling studies.
  - **Residual: a multi-clade lag and its predictors. Not found.**
- **Overlap.** Parked Q-043 and Q-050. The target differs.
- **Observation model.** Disparity under fossil sampling; mismatch between
  matrix age and bin; dependence on the metric.
- **Route.** Hughes 2013 Datasets S1–S2; figshare and Dryad matrices;
  PBDB.
- **Test.** A distribution of lags, and an effect of extinction exposure
  with an interval, robust across metrics.
- **Ratings: I M–H, T M, V M.**

## C10. Did prey defences track predator capability through the Phanerozoic?

- **Question.** Build Phanerozoic time series of prey anti-predatory traits
  (shell thickness, spinosity, burial depth). Do they track predator
  capability (drilling and repair rates, predator size) with lags, as
  Vermeij's escalation predicts, once sampling is modelled?
- **Understanding changed.** It is a direct quantitative test of
  escalation, one of palaeobiology's grand hypotheses of biotic
  directionality.
- **New capability.** Compilations of predation traces; PBDB; trait
  coding at scale; sampling-aware time-series coupling (SDE methods).
- **Closest prior; residual.**
  - Huntley & Kowalewski 2007 (10.1073/pnas.0704960104): the predator
    side, against diversity.
  - Klompmaker et al. 2017 (10.1126/science.aam7468): predator size.
  - Madin et al. 2006 (10.1126/science.1123591): a coarse global test,
    null.
  - Aberhan, Kiessling & Fürsich 2006 (10.1666/05028.1): mid-Mesozoic.
  - Klompmaker et al. 2019 review (10.1016/j.earscirev.2019.02.020).
  - **Residual: prey-trait series with lagged, sampling-aware coupling.
    Not found.**
- **Overlap.** Q-048 and Q-037. The target differs.
- **Observation model.** Trace detection varies by preservation and
  collector; prey-trait coding; geographic bias towards Europe and North
  America.
- **Route.** PBDB (CC0); supplementary tables of predation traces; trait
  coding would be a substantial compilation.
- **Test.** Lagged coupling coefficients, against null series with shared
  sampling.
- **Ratings: I H, T L–M, V M.**

## C11. Are macroecological "laws" stable through the Phanerozoic, or regime-dependent?

- **Question.** Once sampling is modelled, are range-size distributions,
  occupancy–abundance relationships and species-abundance distributions
  stable across the Phanerozoic? Or do they shift at mass extinctions or
  between evolutionary faunas?
- **Understanding changed.** It would show whether macroecology's
  regularities are timeless or historically contingent.
- **New capability.** PBDB at scale; simulations of the fidelity with
  which ranges and occupancy are reconstructed.
- **Closest prior; residual.**
  - Wagner, Kosnik & Lidgard 2006 (10.1126/science.1133795) and Holland
    & Sclafani 2015 (10.1017/pab.2015.10) cover species-abundance
    distributions.
  - Foote et al. 2007 (10.1126/science.1146303) is regional.
  - Darroch et al. 2020 (10.1086/710176) studies fidelity.
  - **Residual: a Phanerozoic-wide, sampling-modelled comparison of
    range-size and occupancy–abundance parameters and their shifts. Not
    found**, with fewer indexes searched.
- **Overlap.** Q-025 and Q-016. The target differs.
- **Observation model.** PBDB abundance fields are sparse; range is
  confounded with detection.
- **Route.** PBDB; fidelity simulations (Darroch).
- **Test.** Parameter shifts at boundaries against intervals from
  sampling simulation.
- **Ratings: I M, T M, V M.**

## C12. Can the drivers of the Great Ordovician Biodiversification Event be told apart?

- **Question.** Can cooling, oxygenation, plankton and food-web change, and
  tectonic dispersal be distinguished as drivers of the Ordovician
  radiation, given their collinearity in time? Simulate the joint drivers
  forward through the sampling filter, and report identifiability before
  any attribution.
- **Understanding changed.** For the largest radiation after the Cambrian,
  it would show which causal stories the evidence can actually separate.
- **New capability.**
  - Coupled models of climate and macroecology: Ontiveros et al. 2023,
    10.1038/s41467-023-41685-w, in which cooling alone reproduces the
    radiation.
  - Capture–recapture richness: Rasmussen et al. 2019,
    10.1073/pnas.1821123116, which correlates diversity with several
    drivers.
  - Section-level diversity at high resolution: Fan et al. 2020.
- **Closest prior; residual.** Rasmussen 2019 correlates several drivers;
  Ontiveros 2023 simulates one. **Residual: identifiability and attribution
  across several drivers. Not found.**
- **Overlap.** Q-010 and Q-030. The target differs: a constrained period
  and the identifiability of attribution.
- **Observation model.** The Lagerstätten and regional sampling of
  Ordovician data; proxy chronologies; collinear drivers.
- **Route.** PBDB; Dryad deposits (Franeck & Liow 10.5061/dryad.nk218ht;
  Stigall 2026 10.5061/dryad.5dv41nsmd); proxy records.
- **Test.** The identifiability of each driver's effect from simulated
  records, then attribution only for drivers that pass.
- **Ratings: I M–H, T M, V M.**

---

## Summary and my provisional priorities

| ID | Short title | I | T | V | Proposed disposition |
| --- | --- | --- | --- | --- | --- |
| C1 | Discriminability atlas (with the geography-only contrast) | H | M | H | **Develop (first)** |
| C3 | Stratigraphic architecture share | M–H | M–H | H | **Develop** |
| C5 | Repeatable reassembly order | H | M | M–H | **Develop** |
| C10 | Escalation quantified | H | L–M | M | Hold (trait compilation needed) |
| C4 | Refugia across events | M–H | M | M | Hold or develop |
| C12 | GOBE driver identifiability | M–H | M | M | Hold or develop |
| C9 | Disparity–diversity lag | M–H | M | M | Hold |
| C6 | Census of competitive displacement | M–H | M | M | Hold |
| C11 | Stability of macroecological laws | M | M | M | Hold |
| C7 | Living-fossil null | M | M | M | Hold |
| C8 | Kinetic temperature–origination | M–H | M | L–M | Hold (narrow residual) |

**A bias to declare.** My list leans towards questions about
identification and observation (C1, C3, C12), because phase 2 taught that
the observation model binds. The more purely biological entries are C4,
C5, C9, C10 and C11. Cross-critique should check that the balance does not
under-serve biology.

**Compute.** C1, and the C12 simulations, would use kunanyi only after
Barry opens the jumpbox. Pilots run locally first.
