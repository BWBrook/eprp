# Environmental disruption, susceptibility and cross-scale inference — round 1

Owner: Claude | Critic: Codex (invited) | Date: 7 October 2026 | Status: reconnaissance, not a review

Scope agreed in discussion 76 (message 1106). The aim is to find which consequential
deep-time questions in this area current data and methods can actually answer.
This is an opportunistic reconnaissance, not a systematic review. Novelty of every
candidate is **unverified**.

**Method.** Three bounded parallel sweeps (Sonnet subagents) each screened about
45–55 records and read 7–12 at section or full-text depth. Their sub-questions were:
- the dose–response of extinction;
- selectivity and susceptibility;
- cross-scale rate inference.

Claude integrated the sweeps and checked the load-bearing items:
- Existence of about 30 DOIs, checked via Crossref.
- Exact passages in Song et al. 2021, checked in the full text.
- The scaling exponent in Kemp et al. 2015, checked in the full text.
- The scaling exponent in Spalding & Hull 2021, quoted via a fetched PMC page.

Access depth for each source is in the table at the end. Labels: **[inference]**
marks our own reasoning; everything else is a source claim.

## Revisions after Codex's critique (8 October)

Codex's [source audit](2026-10-08-codex-review-disruption.md) changed these
points. The original text below is kept, and where it conflicts, this section
takes precedence. The reasoning is in Correspondence 77.

- **Bottom line 1 is retracted as stated.**
  - Kemp's magnitude still scales as window^0.10, about 4-fold over six orders
    of magnitude, so magnitude is not window-invariant.
  - An extinction fraction is not rate × duration.
  - Song's arithmetic redundancy among its three thresholds stands. It does not
    show that duration is biologically irrelevant.
  - Which forcing functional predicts extinction across windows is an open
    question to define and test, not an established result: peak, integrated
    anomaly, or rate at a stated window.
- **Bottom line 4 overstated exclusivity.** Stockey 2021 applies physiology
  across three palaeo-configurations, although not as held-out event prediction.
- **Candidate A is reformulated.** Does frozen physiological habitat loss
  improve held-out prediction beyond traits plus thermal exposure and niche
  mismatch (Malanoski 2024; Reddin 2025, 10.1038/s41467-025-56589-0)?
  - The first design is a fixed end-Permian-to-other-event transfer with
    calibration choices frozen. Leave-one-event-out fitting comes later, because
    it needs several training events.
  - The PETM is not a blanket low-extinction control. Deep-sea benthic
    foraminifera are the obvious counterexample, so controls must be specific
    to clade and habitat.
- **Candidates B and C.**
  - B must first fix its estimand: taxon loss, a within-clade selectivity
    coefficient, or a community regime.
  - For C, a design that fails under favourable assumptions shows only that this
    design cannot distinguish the alternatives in practice. It does not show
    structural non-identifiability.
  - C informs B's design but does not gate it.
- **Section 4 is replaced by a crosswalk.** The single stage table gives way to a
  source-native crosswalk, now built in
  [data/interval-crosswalk](../data/interval-crosswalk/README.md).

### Candidate status, 9 October

- **A leads.** The end-Permian calibration fields are deposited (Figshare
  7357193). The calibration is non-unique: 70%/500 m, 80%/1,000 m and about
  95%/4,000 m in 2018, and 50–70% at 500 m in 2022. Other events could test
  transfer and also choose among these calibrations; see the
  [transfer inputs](2026-10-08-transfer-inputs.md). Next step: check the nearest
  prior work.
- **B is parked.** Malanoski et al. 2024 already tested every ΔT × trait
  interaction and all are null, and the leverage is weak; see the
  [B prior-work note](2026-10-09-b-selectivity-prior-work.md). B's question now
  runs through A's mechanism.
- **C stands** as a cheap design diagnostic. It must report detectable effects
  and data requirements, not structural non-identifiability.

## Bottom line

1. **One grain problem runs through forcing, response and diversification.**
   - Measured climate-change rates scale with measurement window as
     window^−0.90±0.03 (Kemp 2015).
   - Genus extinction rates scale as window^−0.6±0.2 (Spalding & Hull 2021).
   - Graptoloid extinction rates also fall with interval length (Crampton 2026).
   - [inference] An exponent near −1 means measured magnitude is almost independent
     of window, so a geological-grain "rate" carries little beyond magnitude ÷ window.
     Magnitude-like quantities are the more transportable estimands. Rate thresholds
     largely restate magnitude at a given grain. For example, Song's three thresholds
     are arithmetically redundant: ΔT >5.2 °C with Δt <0.4 Myr already implies
     R >13 °C/Myr.
2. **Magnitude is a continuum, but mechanism may shift.**
   - Extinction magnitudes show no gap between background and mass extinction
     (Wang 2003; Marshall 2023; Crampton 2026).
   - Selectivity does change in mass extinctions: range protects less, and the sign
     of size selectivity varies (Monarrez 2023; Payne 2023).
   - Those analyses use pre-assigned regime labels and only about 5 mass-extinction
     stages, against 81 background stages.
3. **Warming plus deoxygenation is the best-supported proximate killer in hyperthermals.**
   Direct acidification effects are inconsistent across events (Kiessling 2024;
   Reddin 2021; Payne 2023).
4. **The one mechanistic deep-time-to-modern bridge has a single calibration event.**
   - Penn & Deutsch 2022 project modern ocean extinction with a metabolic-index model
     anchored to the end-Permian (Penn 2018).
   - Neither sweep found a held-out validation on another event. This is absence of
     evidence from a bounded search.
5. **The headline thresholds are contested on identifiability, not just on value.**
   - The ΔT "threshold" differs by definition: 5.2 °C tropical SST (Song), about
     7–9 °C global (Kaiho 2022), about 7 °C local (Malanoski 2024). These are not
     commensurable.
   - Hillebrand 2020 finds that ecological thresholds rarely emerge from noisy
     empirical data.
   - The scout reports that Song's 5.2 °C is cited in IPCC AR6 WGII. This rests on
     OpenAlex citation metadata and has not been checked.

## 1. Evidence by sub-question

### Dose–response of extinction to disruption

- **Stage-scale extinction rises with temperature change** (Song 2021, 45 bins,
  ρ ≈ 0.6). The relation survives dropping the Big Five (ρ = 0.54 for ΔT, n = 40).
  Warming is not significantly steeper than cooling (p = 0.12).
  - Song defines ΔT as the maximum change within a bin, over spans of 0.05–6.5 Myr.
  - The authors cite Kemp 2015 and state that decadal-to-millennial peak rates are
    unrecoverable. Claude checked this in the full text.
  - They test neither a threshold against a smooth monotone relation nor out-of-sample
    prediction (scout's reading).
- **Malanoski 2024**: local ΔT, from stage-to-stage HadCM3 snapshot differences,
  plus physiological traits predicts genus extinction. Selectivity is weaker in
  mass-extinction intervals (SI). The model includes no O₂ or pH terms.
- **Background state modulates sensitivity, but none of these is tested on an
  empirical event-level dose–response:**
  - O₂ (Stockey 2021, cGENIE: loss nonlinear below about 40% PAL);
  - climate legacy (Mathes 2021);
  - Pangean configuration (Kiessling 2024, hypothesis);
  - palaeogeography (Pohl 2023; Malanoski 2026).
- **An explicit duration framework exists for the carbon cycle**: Rothman 2017 finds
  a critical rate at long timescales and a critical size at short ones, across 31
  carbon-isotope events. Neither sweep found an empirical extinction dose–response
  over magnitude × duration.

### Susceptibility and selectivity

- **Settled enough:**
  - Narrow geographic range raises background extinction risk.
  - Abundance adds little once range is known (Harnik 2012; Finnegan 2024).
  - Clade identity carries large risk differences (Finnegan 2015).
  - Models trained on past stages predict the next stage with AUC ≈ 0.76
    (Finnegan 2024) and 70–80% skill (Smits & Finnegan 2019).
- **Key disanalogy:** modern marine threat is biased towards large bodies, unlike
  past events (Payne 2016).
- **Mechanism:**
  - Temperature-dependent hypoxia explains end-Permian magnitude, its latitudinal
    gradient (Penn 2018) and class-level selectivity (Marquez 2026).
  - It also explains post-extinction homogenisation (Al Aswad 2025), which is
    relevant to Codex's area.
  - Penn 2018 pools traits from 61 modern species and 26 Φcrit values across phyla.
    It predicts biogeography, not taxon identity.
- **Contested:**
  - Whether selectivity is a regime switch or an intensification.
  - Whether selectivity transfers between events (Foster 2023 against the Reddin
    2023 reply).
  - Whether acidification selects; it switches sign across events.
  - Primary physiological versus secondary ecological extinction.
- **Range is entangled with detection and geography.**
  - Range is estimated from occurrences.
  - Range combined with sampling dominates graptoloid risk; range alone explains
    under 5% (Boyle 2016).
  - Occupancy-detection modelling shows detection is driven by outcrop area
    (Dean 2025).
  - Range can itself arise from palaeogeography (Pohl 2023).
  - So a range coefficient is not a causal trait effect.

### Cross-scale inference and identifiability

- **Extant timetrees cannot identify λ(t) and μ(t) separately** (Louca & Pennell
  2020). Priors or piecewise models restore partial identifiability (Morlon 2022;
  Legried & Terhorst 2022; Kopperud 2023).
- **The fossilised birth–death model is identifiable** when sampled ancestors are
  observable (Truman 2025), but most fossil datasets cannot recognise them
  [inference]. A preprint claims bias without them (Beaulieu & O'Meara 2026).
- **Fossil and phylogenetic rates target different estimands.** Fossil μ\* includes
  pseudoextinction, and only λ\*−λ = μ\*−μ is identified (Silvestro 2018, 9 clades).
  Modern IUCN counts are terminal losses, so the modern/background ratio may be
  mis-stated [inference].
- **Comparing modern and fossil rates:**
  - Spalding & Hull 2021 fit E|t = E₀(t/Myr)^−γ with γ ≈ 0.6 ± 0.2. If all
    threatened mammals went extinct, about 500 E/MGY would reach only the upper
    edge of the bounds; in their words, "it is unclear how anomalous the present is".
  - Cowie 2022 identifies the numerator problem: invertebrates are undercounted.
  - Wiens & Saban 2025 question the sixth-extinction framing (unread). Hatfield
    2025 argues the current event exceeds most Cenozoic events (abstract only).
- **Apparent timescaling has rival explanations.**
  - Reijenga & Close 2025 find that the clade-duration scaling of fossil
    diversification rates vanishes after sampling correction.
  - [inference] Window scaling and clade-age scaling are distinct effects and are
    often conflated.
- **Detectability:** a preprint reports that simulated mass extinctions go
  undetected in about 49% of scenarios (Strona & Bradshaw 2026; summary depth only).
- **Precursors:** only abiotic early-warning claims exist (Sudakow 2026, AR(1) on
  δ¹³C/δ¹⁸O over 20-Myr windows). Alroy 2008 found no rate autocorrelation at
  stage scale.

## 2. What present data cannot identify

[inference, partly sourced]

- **Peak forcing.** True peak ΔT and rate for events shorter than about 0.1–1 Myr
  (Kemp 2015). PhanDA is stage-resolved only.
- **Replicates.** Clean replicates of "same dose, different state". Triggers (CO₂,
  SO₂, Hg, O₂, pH, sea level) co-vary across about 10–15 events. O₂ and climate
  legacy also trend with faunal age (Foster 2023).
- **Mass-extinction regime.** Regime is estimated from about 5 stages and is
  pre-labelled, which conflates regime with intensity.
- **Causal trait effects.** Range, size, latitude, clade, physiology and
  preservation are collinear. PBDB ecology fields are coded at higher-taxon level
  and inherited.
- **Event dynamics.** Pulse versus press, and primary versus cascade extinction, at
  genus level and stage grain.
- **Extinction timing.** True extinction time versus last appearance
  (Signor–Lipps). Rate resolution is capped by age-model resolution.
- **A common cross-scale unit.** No dataset spans 10²–10⁶ yr with one taxonomic unit
  and one sampling design. BioDeepTime gives local turnover, not global extinction.

## 3. Candidate questions, ranked

These are for critique, not selection. Each needs a full-text nearest-prior-work
check before it becomes a brief.

**A. Does the end-Permian-calibrated physiology model transfer to other events?**
- *Why big:* it is the only mechanistic bridge underpinning a modern
  mass-extinction projection (Penn & Deutsch 2022). Out-of-sample success would be
  the strongest deep-time-to-modern transfer result available. Failure would remove
  that projection's palaeo-validation.
- *Newly tractable:*
  - cGENIE and HadCM3 runs exist for several events (Stockey 2021; Pohl 2023;
    Ying 2026; Malanoski deposits).
  - Class-level physiology is now available (Marquez 2026).
  - PBDB supplies genus occurrences.
- *Test:* leave-one-event-out genus-level prediction, comparing:
  - (a) clade + range + size + age;
  - (b) (a) plus modelled habitat loss in each genus's occupied cells;
  - (c) habitat loss alone.

  Score within-clade spatial variation and held-out magnitude. Use the end-Triassic
  and Toarcian as tests, and the PETM as a low-extinction control.
- *Kill if:*
  - physiological parameters cannot be assigned below class;
  - ESM uncertainty swamps the signal outside the end-Permian;
  - the Penn/Deutsch/Payne network has already done it (Payne 2023 lists it as a
    next step).

**B. Is the "mass-extinction regime" a switch, or a continuous function of dose?**
- Both the dose–response and selectivity sweeps proposed this independently. The
  sweeps are not independent evidence, since they share a model and a brief.
- *Why big:* it decides whether background-calibrated selectivity can extrapolate
  to the current crisis, and it reframes the old Jablonski regime debate.
- *Newly tractable:*
  - stage-level forcing with propagated uncertainty (PhanDA ensembles; Malanoski
    HadCM3 extractions);
  - capture–mark–recapture selectivity estimates (Monarrez 2023, code deposited).
- *Test:* regress hierarchical selectivity coefficients (range, thermal niche, size)
  on continuous forcing. Compare a smooth model with a two-state mixture out of
  sample, and check whether cross-clade variance scales with forcing.
- *Kill if:*
  - per-stage selectivity is too noisy;
  - ~5 high-dose stages give no power, in which case "not identifiable" is the
    result;
  - Malanoski 2024 SI or 2026 already covers it.

**C. Threshold or smooth? An identifiability audit of the warming–extinction relation.**
- *Why:* a widely cited 5.2 °C figure rests on rank correlation and the placement of
  the Big Five. A robust limit result would itself be useful.
- *Cheap and gating:* this is a one-sided simulation test.
  - Simulate smooth, threshold and state-dependent kill curves.
  - Alias the forcing with Kemp scaling and degrade the response to stage grain with
    PBDB-like sampling.
  - Ask whether n ≈ 45 can separate the curves.
  - If not, under favourable assumptions, the threshold claim is unidentifiable.
- *Nearest prior work:* Song 2021, Kaiho 2022, Hillebrand 2020, Kemp 2015,
  Kiessling 2024.
- *Kill if:* the Kiessling/Reddin group already holds the result.

**D. A pseudoextinction-corrected background rate for modern comparisons.**
- *Approach:* take μ = μ\* − (λ\* − λ) per clade for groups that have both
  well-sampled fossils and large extant trees, and propagate it to E/MSY baselines.
- *Kill if:*
  - extant-tree μ is congruence-dependent, leaving intervals unbounded;
  - the correction only matters for borderline claims.

**E. Precursor hindcast with false-positive control (high value, high artefact risk).**
- *Approach:* preregister indicators (rate variance, AR(1), cohort range
  contraction). Score them against Signor–Lipps and sampling-preserving surrogates
  on unbinned composite records, for example graptoloids with about 16 secondary
  events.
- *Kill if:* range truncation and ordering artefacts mimic decline, or dating error
  exceeds the lead time.

A, B and C share infrastructure, and C gates B. Candidates C1 (a window-explicit
extinction spectrum) and C4 (simulation-based inference over identifiable
functionals) from the cross-scale sweep are parked. Spalding & Hull already did
most of C1. C4 is a method in search of a question until A, B or D needs it.

## 4. Shared infrastructure these imply

A reusable **stage-level forcing–response table** would serve A–C, and matches
Barry's wish to get the datasets in order first. Its contents:
- for each stage, GMST, ΔT and baseline with uncertainty (PhanDA ensembles);
- local ΔT where available (Malanoski deposits);
- genus extinction and origination with sampling-corrected estimators (PBDB);
- selectivity covariates (range, size, PBDB ecology codings, class physiology);
- explicit age-model and interval-mapping provenance.

The first probe is small: align the PhanDA stage slices, Song's bins and PBDB
intervals, and record the losses from mapping between them. This is a proposal
only; it needs Codex critique before any build.

## 5. Data and software capability

Deposit existence was reported by the scouts. Nothing was downloaded or run.
"No licence" on GitHub means no reuse grant; it does not mean the data are free to
redistribute.

| Resource | Location | Licence / state |
| --- | --- | --- |
| Song 2021 data and R scripts | Zenodo 10.5281/zenodo.5027293; GitHub haijunsong/Thresholds-of-temperature | CC-BY-4.0 (Zenodo); GitHub no licence |
| PhanDA outputs and DASH code | GitHub EJJudd/PhanDA; HadCM3L priors Zenodo 10.5281/zenodo.8237751 | GitHub no licence; priors CC-BY-4.0. Spatial fields need assimilation re-run |
| Malanoski 2024 | Dryad 10.5061/dryad.1ns1rn91g | Licence unclear |
| Malanoski 2026 | Dryad 10.5061/dryad.9ghx3ffts (~289 MB, Rmd) | Dryad terms |
| Monarrez 2023 (CMR selectivity) | Dryad 10.5061/dryad.931zcrjqw; code Zenodo 10.5281/zenodo.7816408 | Not checked |
| Stockey 2021 cGENIE; Ying 2026 cGENIE | Zenodo 10.5281/zenodo.5519730; Zenodo 10.5281/zenodo.17742290 + GitHub ruiying-ocean | Not checked |
| Gavirneni 2025; Al Aswad 2025 | Zenodo 10.5281/zenodo.11321797; 10.5281/zenodo.11522106 | Not checked |
| Crampton 2026 graptoloids | Dryad 10.5061/dryad.vx0k6dk71 | Not checked |
| BioDeepTime | Zenodo 10.5281/zenodo.8154672 v1.0 (2023) | CC-BY-4.0; no later release seen |
| NSB microfossils | Renaudie 2020, 10.26879/1032 | Maintenance unchecked |
| PyRate | GitHub | AGPL-3.0; last release 2022, master active (Sept 2026) |
| DeepDive | Zenodo 10979237 | LGPL-2.1; v1.0.28 (Feb 2026); estimates richness, not rates |
| RevBayes / BEAST2 (+ sampled ancestors) | — | GPL-3.0 v1.4.1 (Jul 2026) / LGPL-2.1 v2.7.8 |
| FossilSim | CRAN/GitHub | GPL-3; v2.4.4, active |
| Penn 2018; Penn & Deutsch 2022 | No deposit found (not exhaustive) | — |

## 6. Hand-offs to Codex's area

- Al Aswad 2025: metabolic-index habitat expansion explains post-end-Permian
  homogenisation. This bears on recovery and contingency.
- Pohl 2023 and Malanoski 2026: palaeogeography generates range and susceptibility.
  This bears on what regulates diversity.
- Reijenga & Close 2025: an apparent rate scaling turns out to be a sampling
  artefact. This is relevant to any diversity-dynamics estimator.
- Crampton 2026: graptoloid pulses are finer than stages, and the magnitude
  spectrum is continuous.

## 7. Next steps (Claude)

1. Close-read the nearest prior work for A–C:
   - Payne 2023 future-directions section;
   - Monarrez 2023 in full;
   - Malanoski 2024 and 2026 SI;
   - Penn & Deutsch 2022 calibration (paywalled; record the access limit);
   - Kiessling 2024 open questions.
2. Run the PhanDA–Song–PBDB interval-alignment probe as a capability check.
3. Re-rank A–C after Codex critique, and kill or promote each to an idea brief.

## Sources relied on

Access depth: **full** = full text; **sect** = named sections; **abs** = abstract;
**sum** = WebFetch model summary; **meta** = existence only. The depth is the
scout's unless marked "C", meaning Claude also checked the passage. All DOIs below
resolve. Claude checked about 30 via Crossref; the rest were checked by the scouts.

| Source | DOI | Depth | Used for |
| --- | --- | --- | --- |
| Song et al. 2021 Nat Commun | 10.1038/s41467-021-25019-2 | full, C | Thresholds, bins, resolution caveat |
| Kemp et al. 2015 Nat Commun | 10.1038/ncomms9890 | full, C | Rate ∝ window^−0.90±0.03 |
| Spalding & Hull 2021 Proc B | 10.1098/rspb.2020.2332 | sum, C (quoted) | γ ≈ 0.6 ± 0.2; anomaly unclear |
| Malanoski et al. 2024 Science | 10.1126/science.adj5763 | full (accepted manuscript) | Local ΔT + traits; weaker selectivity in mass extinctions |
| Malanoski et al. 2026 Science | 10.1126/science.adv2627 | abs | Palaeogeography and selectivity |
| Judd et al. 2024 Science | 10.1126/science.adk3705 | sect | PhanDA, stage grain |
| Kiessling et al. 2024 Paleobiology | 10.1017/pab.2024.20 | sect | Warming + deoxygenation; open questions |
| Kaiho 2022 Biogeosciences | 10.5194/bg-19-3369-2022 | sect | Global ΔT threshold; event selection |
| Hillebrand et al. 2020 Nat Ecol Evol | 10.1038/s41559-020-1256-9 | abs | Thresholds rarely detectable |
| Rothman 2017 Sci Adv | 10.1126/sciadv.1700906 | full | Rate versus size criticality by timescale |
| Stockey et al. 2021 PNAS | 10.1073/pnas.2101900118 | sum | O₂ modulates warming vulnerability |
| Wang 2003 Paleobiology | 10.1666/0094-8373(2003)029<0455:OTCOBA>2.0.CO;2 | abs | Magnitude continuum |
| Marshall 2023 Camb Prisms Extinction | 10.1017/ext.2022.4 | full | Big Five not statistically distinct |
| Crampton et al. 2026 Paleobiology | 10.1017/pab.2026.10107 | sect | Continuous spectrum; sub-stage pulses |
| Payne et al. 2023 Camb Prisms Extinction | 10.1017/ext.2023.10 | full | Selectivity review; open problems |
| Monarrez, Heim & Payne 2023 RSOS | 10.1098/rsos.230795 | sect | Selectivity weakens/varies in mass extinctions |
| Finnegan et al. 2024 Annu Rev Mar Sci | 10.1146/annurev-marine-021723-095235 | sect | Range consistency; forecast skill |
| Finnegan et al. 2015 Science | 10.1126/science.aaa6635 | abs | Clade + range intrinsic risk |
| Harnik et al. 2012 Proc B | 10.1098/rspb.2012.1902 | abs | Range > abundance |
| Payne et al. 2016 Science | 10.1126/science.aaf2416 | abs | Modern large-body bias |
| Smits & Finnegan 2019 Phil Trans B | 10.1098/rstb.2019.0392 | abs | Forecast skill; human impacts may break link |
| Penn et al. 2018 Science | 10.1126/science.aat1327 | sect (author PDF) | Metabolic index, end-Permian |
| Penn & Deutsch 2022 Science | 10.1126/science.abe9039 | abs | Modern projection; calibration not inspected |
| Marquez et al. 2026 PNAS | 10.1073/pnas.2533086123 | abs | Class physiology explains P–Tr faunal shift |
| Al Aswad et al. 2025 Sci Adv | 10.1126/sciadv.adr4199 | sect | Post-extinction homogenisation |
| Pohl et al. 2023 Sci Adv | 10.1126/sciadv.adg7679 | abs | Early-Palaeozoic proneness from palaeogeography |
| Gavirneni et al. 2025 Paleobiology | 10.1017/pab.2025.10041 | sect | Metabolic rate selectivity (size-confounded) |
| Ying et al. 2026 Nature | 10.1038/s41586-026-10541-4 | sect | K–Pg darkness/size model (sufficiency only) |
| Reddin et al. 2021 GCB | 10.1111/gcb.15434 | abs | Hyperthermal selectivity; buffering not worse |
| Boyle et al. 2016 Paleobiology | 10.1017/pab.2016.33 | abs | Range × sampling dominates |
| Dean et al. 2025 Curr Biol | 10.1016/j.cub.2025.03.025 | sect | Occupancy-detection; outcrop-driven detection |
| Louca & Pennell 2020 Nature | 10.1038/s41586-020-2176-1 | abs | Extant-tree congruence |
| Truman et al. 2025 Syst Biol | 10.1093/sysbio/syae058 | sum | FBD identifiability conditions |
| Silvestro et al. 2018 Nat Commun | 10.1038/s41467-018-07622-y | full | Palaeo versus neo estimands |
| Reijenga & Close 2025 Curr Biol | 10.1016/j.cub.2024.12.038 | full (preprint version) | Timescaling as sampling artefact |
| Cowie et al. 2022 Biol Rev | 10.1111/brv.12816 | sect (§V) | Numerator problem |
| Hatfield et al. 2025 GCB; Wiens & Saban 2025 TREE | 10.1111/gcb.70476; 10.1016/j.tree.2025.01.002 | abs; meta | Sixth-extinction debate |
| Strona & Bradshaw 2026 (openRxiv preprint) | 10.64898/2026.04.07.716927 | sum | Mass extinction undetected in ~49% of simulations |
| Sudakow et al. 2026 Nat Commun | 10.1038/s41467-026-75655-9 | sect | Abiotic early-warning near regime transitions |
| Cooper et al. 2024 Nat Commun (DeepDive) | 10.1038/s41467-024-48434-7 | sect | Simulation-trained richness inference |
| Smith et al. 2023 GEB (BioDeepTime) | 10.1111/geb.13735 | abs | Cross-timescale assemblage series |

Further sources were screened at abstract or metadata depth and not relied on.
Their DOIs are in the subagent reports, which are retained only in session
scratch: for example Foote 1994/2000/2005, Alroy 2008/2014/2015, Jablonski
1986/2005, Payne & Finnegan 2007, Clapham & Payne 2011, Knoll 2007, Mayhew
2008/2012, Morlon 2022 and Du 2025.

## Search log and limits

Sweeps ran on 7 October 2026. Services:
- OpenAlex, keyless. Its free daily budget **ran out from this machine mid-session**,
  so later checks went through other services.
- Crossref and Europe PMC REST. No email address was sent.
- Zenodo API, `gh api` metadata, WebSearch and WebFetch.

Stopping rule: each sweep stopped when new searches only resurfaced known
clusters:
- Song/Kaiho;
- Kiessling/Reddin/Kocsis;
- Stockey/Penn/Deutsch;
- Payne/Finnegan/Saupe;
- Silvestro/Morlon.

Paywalls limited depth for Penn 2018 (an author PDF was used), Penn & Deutsch 2022,
Wang 2003 and the Foote/Alroy methods papers. The Royal Society blocks PMC XML
download. Searches for PhanDA combined with extinction late in the session used
WebSearch only, so "none found" there is weak.
