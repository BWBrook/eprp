# B-003: evidence and trait contract for escalation

Owner: Claude | 15 October 2026 | The first bounded product for
[B-003](../ideas/register-blue-sky.md#b-003-did-prey-defences-track-independent-predator-capability-through-the-phanerozoic).
It applies Codex's correction from cross-critique: drilling and repair
frequencies are interaction outcomes, not predator capability. It also
carries the lessons of B-001: support is defined before counting, and no
planning number is treated as an information bound.

Status: **a design contract.** No data were compiled, measured or analysed.

**Sources and access:**
- A Sonnet subagent extracted:
  - Klompmaker et al. 2017 (main text; the supplement was inaccessible);
  - Huntley & Kowalewski 2007, Madin et al. 2006, Aberhan et al. 2006,
    Kosnik et al. 2011 and Bush & Bambach 2011 (full text, through
    University of Tasmania access where paywalled);
  - the others by abstract.
- Claude read the matched-system abstracts (Kelley 1989, 1992; Dietl et al.
  2000; Dietl 2003) through OpenAlex.
- Claude re-tabulated Klompmaker's open Database 2.
- All DOIs were checked against Crossref.
- **Corrections to my earlier citations:**
  - Bambach 1993 is 10.1017/S0094837300000336;
  - Klompmaker 2017's fourth author is Finnegan.

## 1. What the closest work measured: a gap between scales

| Work | Predator side | Prey side | Scale | Result |
| --- | --- | --- | --- | --- |
| Madin et al. 2006, 10.1126/science.1123591 (full) | Share of carnivorous genera and occurrences | Shares of infaunal or mobile life habits | Global PBDB; bins of about 11 Myr; differenced; lags up to ±3 bins | "none are significant after a Bonferroni correction"; "no evidence that escalation drives macroecological trends at global and million-year time scales" |
| Kosnik et al. 2011, 10.1666/10022.1 (full) | None (narrative) | Reinforcement (ribs, folds, spines) and size in the most common genera, which make up 40% of occurrences per bin | Global; 48 bins; 1,002 genera of brachiopods, bivalves and gastropods | "Increases in shell durability hypothesized to be the result of increased predation in the late Mesozoic are not evident in the common genera". The gastropod reinforcement rise is Permo-Triassic or earlier |
| Aberhan, Kiessling & Fürsich 2006, 10.1666/05028.1 (full) | None (narrative) | Life habit, mobility, cementation, size, ornament | Jurassic; about 22,000 occurrences | Infaunalisation and mobility rise; ornament "remained fairly constant"; tested only against abiotic series |
| Klompmaker et al. 2017, 10.1126/science.aam7468 (main text) | Drill-hole diameter, calibrated to predator size (556 modern pairs, slope 0.94) | Prey size (shell area); mobility and infaunality only qualitatively (supplementary figs) | Global; 362 occurrences; molluscs and brachiopods | Predator-to-prey size ratio "67-fold increase … directional trend". The authors favour an energetic driver |
| Kelley 1989, 10.1080/08912968909386497 (abstract) | Naticid predation intensity (an outcome) | Shell thickness, internal volume | Miocene Chesapeake Group; 5 bivalve genera; about 3 Myr | Thickness rose 8–157% in all five genera; "Improvement of predator capabilities apparently did not keep pace" |
| Kelley 1992, 10.1017/s0022336000020801 (abstract) | **Predator body-fossil morphology**: globosity, aperture, thickness and size of two naticids | (Kelley 1989's prey) | Same system | Stasis in most characters thought to affect efficiency; a size rise in one predator could be coevolution or escape from cannibalism |
| Dietl, Alexander & Bien 2000, 10.1666/0094-8373(2000)026<0215:eilcep>2.0.co;2 (abstract) | Repair frequency (an outcome, used as "independent evidence of the action of a selective agent") | Commissural shelves, thickness, ornament | Late Cretaceous to early Paleocene gryphaeid oysters; over 1,600 valves | Escalation supported; adaptation "by the enhancement of existing traits" |
| Dietl 2003, 10.1046/j.1095-8312.2003.00255.x (abstract) | Attack success and position (outcomes); whelk size (morphology) | Mercenaria size | Plio-Pleistocene Florida | Reciprocal; "predator adaptation has outpaced prey antipredatory adaptation" |
| Signor & Brett 1984, 10.1017/s0094837300008174 (abstract) | Mid-Palaeozoic durophagous fish radiation | Spinose and sculptured genera | Mid-Palaeozoic | Some prey changed by extinction of undefended forms, crinoids "through evolution within established clades" |

Also: Huntley & Kowalewski 2007 (10.1073/pnas.0704960104) tracks
trace frequency against diversity. Trace frequencies are outcomes, and
the paper pools drilling with repair.

**Inference: there is a gap between scales.**
- Matched local systems often show prey defences changing directionally
  over a few million years (Kelley 1989; Dietl et al. 2000; Dietl 2003).
- Global tests find no coupling (Madin et al.) or no late-Mesozoic rise in
  durability (Kosnik et al.).
- Neither level measures both sides properly:
  - global tests use carnivore share and life-habit shares;
  - local tests mostly measure the predator side through outcomes.
- The one admissible local predator series (Kelley 1992) shows **predator
  stasis while prey thickened**. That is the opposite of predator-driven
  tracking.

**Residual.** Does matched local escalation add up to global trends in
prey defence? If so, through within-lineage change or through sorting
among lineages, once predator capability is measured independently and the
energetic and abiotic rivals are included? This bounded search found no
such test.

## 2. Which predator measures are admissible

| Measure | What it records | Admissible as capability? |
| --- | --- | --- |
| Repair-scar frequency | Attacks × failure × survival × preservation | **No.** It indicates a selective agent at most |
| Drilling frequency, incomplete drilling, attack success, prey effectiveness | Interaction outcomes | **No** |
| Drill-hole diameter (Klompmaker's calibration) | Predator size, but only for *successful* attacks. If prey thicken, only larger drillers succeed, so part of the series is caused by prey defence | **Conditionally.** Only with prey thickness conditioned on, and incomplete holes included |
| Predator body-fossil morphology (Kelley 1992's characters; claw dimensions; crushing dentition) | Capability, measured on the predator | **Yes** |
| Predator body size from body fossils (for example the Heim et al. 2015 compilation, 10.1126/science.1260065; contents and deposit not checked) | Size-limited capability | **Yes**, for size-limited modes |
| Predator diversity or share (Madin et al.; Bambach 2002) | Pressure at most | **No.** Reported only as a weak pressure covariate |

**PBDB's durophage diet coding is negligible.** The subagent found it on 1
of 1,397 chondrichthyan genera and 0 of 2,061 decapods. This bounded search
found no compiled time series of bite force or jaw mechanics.

## 3. Mechanical matching: which defence answers which predator

| Predator mode (examples) | Mechanically relevant prey defences |
| --- | --- |
| Drilling (naticids, muricids, octopods) | Shell thickness (drilling time), size refuge, burrowing depth, mobility |
| Crushing (decapods, durophagous fishes and reptiles) | Thickness and strength, ornament and spines, size refuge, globose or tightly coiled form, cementation |
| Apertural peeling or chipping (calappid crabs, busyconine whelks) | Apertural thickening or constriction, narrow apertures, size (Dietl 2003) |
| Whole-body ingestion (fishes) | Size, burrowing depth, spines |

A prey trait counts as a response to a predator mode only if it sits in that
mode's row.

## 4. Target and estimands at two levels

**Level A: matched systems.**
- A system pairs one predator mode, an admissible series of predator
  capability P(t), and a prey defence D(t) from that mode's row, in the
  same habitat, region and lineages, across stratigraphic horizons t.
- The estimand is the **directional coupling** between first differences of
  P and D at declared lags, with measurement error taken from specimen
  counts. Each system is classed as one of:
  - prey-follows-predator (escalation);
  - predator-follows-prey;
  - reciprocal;
  - prey change with predator stasis (the Kelley pattern);
  - neither.

**Level B: bridging the scales.**
- A Price-equation decomposition (Price 1970, 10.1038/227520a0) splits the
  change in a global mean defence trait between bins into two parts:
  - **sorting** among lineages, which is the replacement rival;
  - **within-lineage change.**
- Predator-driven escalation predicts that within-lineage change dominates
  and is timed to rises in admissible predator capability *of the matching
  mode*.
- Kosnik et al. 2011's genus-level reinforcement scores are the candidate
  trait series.

## 5. Rivals

| Rival | Prediction |
| --- | --- |
| R0. Sampling and shared trend | Coupling disappears after differencing, under common sampling (Madin et al.'s design) |
| R1. Shared energetics (Bambach 1993, 10.1017/S0094837300000336) | Defences change with productivity or metabolic indices, whatever the predator mode. Finnegan et al. 2011 (10.1666/09066.1) give an independent Meso-Cenozoic gastropod metabolic-rate series as a covariate |
| R2. Abiotic calcification (temperature, carbonate saturation, aragonite and calcite seas) | Thickness and ornament follow the cost of calcification, not predators |
| R3. Taxonomic replacement | The sorting term dominates (Madin et al.'s aragonite case; Signor & Brett's bellerophontids) |
| R4. Escalation | Within-lineage defence change, in the predator mode's row, follows an admissible rise in predator capability at the declared lag |

**Key discriminator: specificity to predator mode.**
- R1 and R2 predict defence change regardless of which predator mode is
  rising.
- R4 predicts *matched* change: a rise in drilling capability should be
  followed by thickness or burrowing, and a rise in crushing capability by
  ornament, strength or apertural defence.

Like B-001's test of refilling by different clades, this narrows the rivals
but does not by itself identify cause.

## 6. Observation model

**Clade confounding in compilations.** Re-tabulating Klompmaker's open
Database 2 (10.6084/m9.figshare.5046964; CC BY 4.0):
- Palaeozoic rows: 133 of 141 are brachiopods, 131 epifaunal and 123
  stationary;
- Paleocene–Pleistocene rows: 139 of 147 are molluscs.

Any global trend in prey traits there is largely a change of clade.

**Taphonomy:**
- thin and delicate shells preserve and get collected less;
- lithification affects recovery. Database 2 records lithification state;
- an apparent thickening through a section can therefore be taphonomic, so
  fragmentation and preservation controls are needed.

**Other biases:**
- **Geography:** the record is mainly the Cenozoic of Europe and North
  America (Klompmaker et al. 2019, 10.1016/j.earscirev.2019.02.020,
  abstract).
- **Selection of genera:** Kosnik et al. score only the most common
  genera.
- **Resolution:** local sections are time-averaged, and global bins are
  about 11 Myr. The declared lags must exceed the resolution.

## 7. Outcomes, informative either way

**Level A, per system:**
- **Escalation supported:** a defence in the matched row follows an
  admissible predator change at the declared lag, beyond R0, within
  lineages.
- **Informative negative:** precise null coupling, or prey change with
  documented predator stasis.
- **Inadequate:** anything else.

**Across systems:**
- The summary is the share of systems in each class.
- Thresholds are fixed only after the support audit. A discrimination
  benchmark on the actual supported design, labelled as a benchmark, decides
  whether the cross-system route is informative.

**Level B:**
- The quantity is the within-lineage share of defence change, with an
  interval, and its timing against predator-capability series of the
  matching mode.
- A dominant sorting share with no mode matching is an informative result
  for R3, R1 or R2. It is not a disproof of escalation at local scales.

## 8. Next gate: a source and support audit, with definitions fixed first

**Definitions, proposed now and fixed before counting:**
- **Admissible predator series:** body-fossil morphology or size of the
  predator mode in that system. Drill-hole size counts only if prey
  thickness is conditioned on and incomplete holes are counted.
- **Matched prey series:** a trait in that mode's row, measured on the
  prey lineages exposed in the same habitat and region.
- **Supported system:**
  - at least 4 horizons with both series;
  - at least 10 specimens per horizon per side;
  - lineage-level identification;
  - data deposited or recoverable from published tables.

**Audit steps:**
1. **Matched-system inventory.** Read the primary papers, then record for
   each system:
   - the predator measure and whether it is admissible;
   - the prey measure and its mechanical match;
   - horizons and specimens;
   - lineage resolution;
   - data availability.

   The systems:
   - Kelley 1989 and 1992;
   - the reappraisal by Dietl, Kelley & Handley (10.1017/s2475262200012156,
     probably a meeting abstract);
   - Kelley et al. 2001 (10.1016/s0031-0182(00)00207-8);
   - Kelley & Hansen 2006 (10.1016/j.palaeo.2005.11.012);
   - Dietl et al. 2000; Dietl 2003;
   - Signor & Brett 1984;
   - Syverson et al. 2018 (10.1017/pab.2017.38, crinoid spinosity).

   A bounded search should look for further systems: decapod and gastropod
   systems, and Palaeozoic crinoids and fishes.
2. **Support for bridging the scales:**
   - Kosnik et al.'s appendices (10.1666/10022.s1): whether scores per genus
     per bin are available for a decomposition;
   - Klompmaker's Database 1 and 2 (open);
   - the availability of Finnegan et al.'s and Heim et al.'s data.
3. **No new compilation or specimen measurement before the audit.** No
   author contact without Barry's authorisation.

**Planning target, not an information bound:** about 3 supported systems
with admissible predator series, plus genus-level scores for Level B.
- If the audit finds fewer, Level A parks.
- Level B is judged separately on its own support.

**Overlap.** Q-048 and Q-037. B-011 also uses energetics. B-001's coding
gaps (fishes and sharks barely coded) also limit any predator-side series
based on Knope.
