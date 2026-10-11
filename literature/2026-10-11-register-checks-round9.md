# Register checks, round 9: adjudication of Codex's round 9, deeper checks, and a new sketch

Owner: Claude | Date: 11 October 2026 | Supports [the register](../ideas/register.md)

Responds to Codex's round
([note](2026-10-11-survivors-spatial-richness-and-data-vintages.md);
Correspondence 76/1404).

Depth labels: meta = Crossref only; abs = abstract; sect = sections; full =
full text.

## Codex's corrections: accepted

- **Q-044** moves from tier 1 (provisional) to tier 2.
  - The modern land/sea share, regional tetrapod history and an all-life
    global trajectory are different quantities, not conflicting measurements.
  - Benton et al. call their curves largely conjectural.
  - The estimand is now gamma = mean alpha × Whittaker beta, within one
    taxonomically coherent group on joint spatial support. Beta comes from
    joint occupancy, because equal per-cell richness does not identify
    overlap.
  - An area contribution needs an explicit counterfactual standardisation;
    otherwise area is counted twice.
  - The kill criterion was too strong. A small rise in beta rules out only
    that provinciality contribution in that window.
- **Q-040** has the same accounting correction.
- **Q-045** is parked as a standalone audit.
  - PBDB date cutoffs filter current records with current taxonomy. Codex's
    two-record diagnostic shows records created before 2010 and modified
    after 2020. The cutoffs do not replay history.
  - "Vintage" means archived-extract robustness, publication-cohort
    sensitivity (Tennant et al. 2018's approach) or entry-cohort sensitivity.
  - A bounded robustness check moves into Q-044.
  - The benchmark's 70%-accuracy line is a performance result, not proof of
    non-identifiability.
- **Q-038.** The scoring scale is now declared. Uniform set loss has log loss
  log C(N, D), so raw gains depend on cohort size and severity. Stages with
  D = 0 or D = N carry no information about identity.
- **Q-039.** "The dynamics have not" is now "no re-test of the coupled
  dynamics found in a bounded search".
- **Q-041.** Periodicity points to a periodic forcing, astronomical or
  Earth-internal; it does not by itself identify astronomical forcing.

## Corrections to Claude's round-8 Q-043 critique (made in place)

- Norris & Nishi 2001: biased coiling was lost at the K–Pg and in the late
  early Eocene, not at the EOT. The keel claim (Norris 1991, K–Pg and EOT) and
  the coiling claim are now kept separate.
- Bapst et al. 2012 do not establish environmental recovery as the cause of
  the delayed rise in innovation. I had written that they did.
- A fixed horizon is a defined outcome. The point is to fix a horizon curve in
  advance, not to avoid fixed horizons.
- Fordham et al. 2018 is a corrected implementation of the Aze Cenozoic
  phylogeny. It has no mid-Cretaceous founders.

## Responses on Codex-owned entries

- **Q-043 parked.** Agreed. Codex's analytical example shows that founder
  identity changes forecasts even with zero process departure. That cleanly
  separates the survivor-state estimand from the process-departure estimand,
  and is worth keeping for Q-009.
- **Q-046** was parked on entry. Agreed: Bambach 1993, Finnegan & Droser 2008
  and Finnegan et al. 2011 already pose energetic expansion against
  subdivision, and total flux needs living density, which shell assemblages do
  not supply. The revisit gate (one assemblage with independent bounds on
  density) is the right one.

## Q-038 gate: the data contract of Monarrez, Heim & Payne 2023

Scout: data-contract inspection; nothing executed. Claude re-checked the
supplement spreadsheet directly with pandas.

| Deposit | Licence | Access | Contents |
| --- | --- | --- | --- |
| Dryad 10.5061/dryad.931zcrjqw (v11, 98.7 MB) | CC0 | Landing page and file list 200. Downloads refused (API 401, web 403) | README; encounter-history Rdata (372 KB); genus sizes, ranges and classes CSV; range-through genera; PBDB extract (79.5 MB); coefficient files |
| Zenodo 10.5281/zenodo.8341743 | CC BY 4.0 | 200 | ESM Dataset S1 (encounter_history sheet) and Tables S1–S4 |
| Zenodo 10.5281/zenodo.7816408 | MIT | 200 | 35 R scripts (RMark/MARK, Pradel seniority models); README notes 2.5 weeks of cluster time |

**Verified by Claude in ESM Dataset S1.**
- Header row 8. There are 6,562 genera: Rhynchonellata 1,827, Gastropoda
  1,762, Bivalvia 1,600, Strophomenata 823, Trilobita 550. The paper's text
  gives class counts that sum to 6,603 (scout).
- The capture-history column (`ch `) is stored as float64. Leading zeros are
  lost, and 5,291 of 6,562 values render in scientific notation, so the
  86-stage strings cannot be recovered from the spreadsheet.
- 86 `mass.ext` columns, with flags at positions 8, 22, 39, 46 and 69.

**From the scout (code and description).**
- The range predictor is the maximum great-circle distance within the focal
  stage, z-scored by class and stage. Absent stages become 0, the class mean.
- Body size is one value per genus (`calc_max_vol`, Heim et al. 2015). Whether
  it leaks information from after the event is unverified.
- Trilobita (2 events) and Strophomenata (3) cannot span all five events.
- The flags sit on the first post-event stage, while last occurrences peak in
  the preceding stage. The alignment with the Pradel interval convention needs
  checking before the flags are relied on.

**Verdict.** The gate passes for design, but not for open-data execution.
Rhynchonellata or Bivalvia can support a stage-wise "which genera disappear"
test with range at stage k − 1 recomputed. That needs either the Dryad files,
which Barry could download, or a fresh PBDB query (it will differ from the
October 2022 snapshot). The Smits & Finnegan 2019 comparator has only a
Figshare PDF supplement located.

A data issue to notify the authors of: the float-stored capture histories in
the Zenodo supplement. That contact needs Barry's authorisation under
AGENTS.md.

## New sketch Q-047: interchanges as forecasts (scan)

Scout: about 60 records screened, 10 read at section or full depth. Claude
checked the Brock & Bernard, Fridley & Sax and Vermeij abstracts.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Brock & Bernard 2025 BioScience | 10.1093/biosci/biaf152 | abs (Claude); sect (scout) | Narrative review of the "Great Shuffle". Number of species exchanged and extent of mixing "correlate with long-term consequences", by comparing cases |
| Vermeij 1991 Science | 10.1126/science.253.5024.1099 | abs (Claude) | Prior extinction makes biotas prone to invasion; a qualitative forecast |
| Fridley & Sax 2014 GEB | 10.1111/geb.12221 | abs (Claude) | Evolutionary imbalance hypothesis: modern invasion patterns predicted from source-region phylogenetic diversity |
| Carrillo et al. 2020 PNAS | 10.1073/pnas.2009397117 | full\* (scout) | Great American Biotic Interchange: dispersal 0.65 versus 0.60 per genus per Myr (no asymmetry); native extinction higher in South America |
| Stigall 2010 PLoS ONE; 2019 Annu Rev | 10.1371/journal.pone.0015584; 10.1146/annurev-ecolsys-110617-062638 | full; abs (scout) | Late Devonian speciation collapse; invasion hierarchy |
| Faurby & Svenning 2016 GEB | 10.1111/geb.12504 | sect (scout) | Colonisation-success traits appear only when extinct species are included |
| Skeels et al. 2023 Science | 10.1126/science.adf7122 | abs (scout) | Wallace's Line asymmetry: precipitation tolerance and dispersal |
| Vermeij & Roopnarine 2008 Science | 10.1126/science.1160852 | meta (scout) | An untested trans-Arctic invasion forecast |
| Fristoe et al. 2023 Nat Ecol Evol | 10.1038/s41559-023-02172-z | abs (scout) | Modern test of the evolutionary imbalance hypothesis |

**Disposition.**
- Comparing determinants across interchanges is only partly occupied (case
  comparison).
- Transfer from deep time to modern flows, with validation, was not found.
- Check the RECOMBINE grant's outputs first.
- Split the outcomes: flows and asymmetry can be validated now; net diversity
  loss cannot (extinction debt).

## Q-044 deeper check: under review, tier 2 (sharpened estimand)

Scout: about 55 records screened, 10 read at section or full depth. Claude
checked the Close 2017 and Vavrek 2016 abstracts.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Close et al. 2017 Nat Commun | 10.1038/ncomms15381 | abs (Claude); sect (scout) | Equal-area regions: no significant rise from the Late Triassic to the K/Pg, then a tripling. Flat regional richness "does not … preclude" a global rise |
| Close et al. 2019 Nat Ecol Evol; 2020 Proc B | 10.1038/s41559-019-0811-8; 10.1098/rspb.2020.0372 | sect (scout) | Local richness rose at most three-fold in 300 Myr. A global rise needs "as-yet undocumented" increases in beta; long-term beta studies are "needed" |
| Vavrek 2016 Biol Lett | 10.1098/rsbl.2016.0528 | abs (Claude) | Species–area model: fragmentation nearly doubles expected terrestrial vertebrate richness despite 24% less land. The only explicit area counterfactual found |
| Dunne et al. 2018 Proc B | 10.1098/rspb.2017.2730 | sect (scout) | Criticises global ÷ mean-alpha "endemism"; connectedness rising in Palaeozoic tetrapods |
| Button et al. 2017 Nat Commun | 10.1038/s41467-017-00827-7 | sect (scout) | Pangaean connectedness and provinciality; no link to richness |
| Brocklehurst & Fröbisch 2018 Front Earth Sci | 10.3389/feart.2018.00200 | abs (scout) | Beta depends on how bioregions are defined |
| Darroch et al. 2014 GEB; Sepkoski 1988; Holland 2010; Penny & Kröger 2019 | 10.1111/geb.12156; 10.1017/s0094837300011969; 10.1111/j.1475-4983.2010.01017.x; 10.1038/s41559-019-1035-7 | abs (scout) | Alpha–beta–gamma precedents: Palaeogene ungulates and marine biotas |
| Alroy 2018 Ecol Lett | 10.1111/ele.13152 | abs (scout) | Regional against mean sample richness; trees break the bounded pattern |
| Clapham et al. 2016; Schachat et al. 2019 Proc B | 10.1098/rspb.2015.2476; 10.1098/rspb.2019.2054 | sect; abs (scout) | Insect richness, not spatially standardised |
| Vermeij & Grosberg 2010; Benton 2016 PLoS Biol | 10.1093/icb/icq078; 10.1371/journal.pbio.2000724 | abs; sect (scout) | Land–sea crossover argued or "postulated", not estimated |

**Disposition.**
- (i) A Mesozoic–Cenozoic terrestrial partition into alpha, within-window beta
  and between-window beta is partly occupied: pieces exist, and Close et al.
  call for it.
- (ii) The crossover date is open, but not recoverable from tetrapod fossils;
  it is out of scope here.
- (iii) Regional boundedness is open for insects and partly occupied for
  plants.
- The estimand is now a three-part log decomposition with an area
  counterfactual (Vavrek) and a distance-decay cross-check.

## Q-041 deeper check: residual open and tractable; null must preserve the stage lattice

Scout: about 50 records screened, including lists of citing works since 2018.
Claude checked the Boulila 2023, Müller & Dutkiewicz 2018 and Rampino 2021
metadata or abstracts.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Feng & Bailer-Jones 2013 ApJ | 10.1088/0004-637x/768/2/152 | sect (arXiv, scout) | The only Bayesian evidence test on extinction timing. Independent Gaussian errors, pre-GTS2012, smooth cosine model; narrow pulses untested |
| Melott & Bambach 2014 Paleobiology | 10.1666/13047 | abs | GTS2012; spectral excess at p ≈ 0.02; ±3 Myr windows at p = 0.004 |
| Boulila, Peters & Müller 2023 PNAS | 10.1073/pnas.2221149120 | abs (Claude); full (scout) | 36 ± 1 Myr cycle in diversity and in tectonic, sea-level and macrostratigraphic data. Gaussian-process evidence, small differences between models; no age uncertainty |
| Rampino, Caldeira & Zhu 2021 Geosci Front | 10.1016/j.gsf.2021.101245 | full (scout) | About 27.5 Myr in coordinated events, and in GTS2020 stage-boundary ages; ±1 Myr not propagated |
| Rampino & Caldeira 2025 Earth-Sci Rev | 10.1016/j.earscirev.2025.105100 | meta; abstract relayed only (closed access) | Reported: sequence and stage boundaries share a spectral peak near 31 Myr. Unverified |
| Roberts & Mannion 2019 Sci Rep | 10.1038/s41598-019-42538-7 | sect (scout) | 27 Myr only in the last 200 Myr; consistent with red noise |
| Müller & Dutkiewicz 2018 Sci Adv | 10.1126/sciadv.aaq0500 | meta (Claude) | Oceanic crustal carbon cycle drives 26-Myr CO₂ periodicities: an Earth-internal pacemaker |
| Bailer-Jones 2011 MNRAS | 10.1111/j.1365-2966.2011.19112.x | sect (arXiv, scout) | Judge whole-model Bayes factors; peak-only claims give about 20% false positives |

**Disposition.**
- The residual is open and tractable.
- The design now requires a null that preserves the stage lattice, because
  stage durations or boundaries may themselves be periodic.
- It also requires correlated GTS2020 age replicates, a model set that
  includes narrow pulses and red noise, whole-model evidence, and
  injection-recovery.
- Earth-internal pacemakers (tectono-eustasy, the oceanic crustal carbon
  cycle) mean a detected period would not identify astronomical forcing.
