# B-003: evidence and trait contract for escalation

Owner: Claude | 15 October 2026 | The first bounded product for
[B-003](../ideas/register-blue-sky.md#b-003-did-prey-defences-track-independent-predator-capability-through-the-phanerozoic).
It applies Codex's correction from cross-critique: drilling and repair
frequencies are interaction outcomes, not predator capability. It also
carries the lessons of B-001: support is defined before counting, and no
planning number is treated as an information bound.

Status: **a design contract, amended once** after
[Codex's single review](../ideas/2026-10-15-blue-sky-specification-and-escalation-review-codex.md);
section 9 records the changes. Its
[source inventory](2026-10-15-b003-source-inventory.md) led to a
**practical hold on support** (section 10). No data were compiled, measured
or analysed.

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
| Kosnik et al. 2011, 10.1666/10022.1 (full) | None (narrative) | Reinforcement (ribs, folds, spines) and size in the most common genera, which make up 40% of occurrences per bin. **One static mean per genus is applied in every bin** (p. 321, "Genus Values As Averages"), so the series changes only through composition | Global; 48 bins; 1,002 genera of brachiopods, bivalves and gastropods | "Increases in shell durability hypothesized to be the result of increased predation in the late Mesozoic are not evident in the common genera". The gastropod reinforcement rise is Permo-Triassic or earlier |
| Aberhan, Kiessling & Fürsich 2006, 10.1666/05028.1 (full) | None (narrative) | Life habit, mobility, cementation, size, ornament | Jurassic; about 22,000 occurrences | Infaunalisation and mobility rise; ornament "remained fairly constant"; tested only against abiotic series |
| Klompmaker et al. 2017, 10.1126/science.aam7468 (main text) | Drill-hole diameter, calibrated to predator size (556 modern pairs, slope 0.94) | Prey size (shell area); mobility and infaunality only qualitatively (supplementary figs) | Global; 362 occurrences; molluscs and brachiopods | Predator-to-prey size ratio "67-fold increase … directional trend". The authors favour an energetic driver |
| Kelley 1989, 10.1080/08912968909386497 (abstract) | Naticid predation intensity (an outcome) | Shell thickness, internal volume | Miocene Chesapeake Group; 5 bivalve genera; about 3 Myr | Thickness rose 8–157% in all five genera; "Improvement of predator capabilities apparently did not keep pace" |
| Kelley 1992, 10.1017/s0022336000020801 (abstract) | **Predator body-fossil morphology**: globosity, aperture, thickness and size of two naticids | (Kelley 1989's prey) | Same system | **Heterogeneous.** Most putative efficiency characters show stasis. Euspira's aperture height fell 9% and its thickness rose 63%. Neverita's thickness fell 37% and its height rose 60%. That size rise permits coevolution; escape from cannibalism is a rival, and neither is eliminated |
| Dietl, Alexander & Bien 2000, 10.1666/0094-8373(2000)026<0215:eilcep>2.0.co;2 (abstract) | Repair frequency (an outcome, used as "independent evidence of the action of a selective agent") | Commissural shelves, thickness, ornament | Late Cretaceous to early Paleocene gryphaeid oysters; over 1,600 valves | Escalation supported; adaptation "by the enhancement of existing traits" |
| Dietl 2003, 10.1046/j.1095-8312.2003.00255.x (abstract) | Attack success and position (outcomes); whelk size (morphology) | Mercenaria size | Plio-Pleistocene Florida | Reciprocal; "predator adaptation has outpaced prey antipredatory adaptation" |
| Signor & Brett 1984, 10.1017/s0094837300008174 (abstract) | Mid-Palaeozoic durophagous fish radiation | Spinose and sculptured genera | Mid-Palaeozoic | Defence frequency rose through three routes: extinction of undefended genera, the radiation of productids, and change "within established clades" of crinoids. All three sit in a predation-driven account, so sorting can itself be a predation route |

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
- The one directly measured local predator series (Kelley 1992) is
  **heterogeneous**: mostly stasis in characters thought to affect
  efficiency, with some changes in size and thickness. Whether that is
  coevolution or escape from cannibalism is unresolved.
- Prey adapting while the measured predator capability is unchanged does
  not refute predation as the selective agent.

**Residual, narrowed.** Does prey defence change *within lineages* follow
independently measured, mechanically relevant change in predators, once a
common-cause comparison (energetics, abiotic change) is in place? And can
such local results be related to global composition? This bounded search
found no such test. Whether the published local systems can support one is
the next gate's question.

## 2. Which predator measures are admissible

| Measure | What it records | Admissible as capability? |
| --- | --- | --- |
| Repair-scar frequency | Attacks × failure × survival × preservation | **No.** It indicates a selective agent at most |
| Drilling frequency, incomplete drilling, attack success, prey effectiveness | Interaction outcomes | **No** |
| Drill-hole diameter (Klompmaker's calibration) | Predator size, but only for *successful* attacks. If prey thicken, only larger drillers succeed, so part of the series is caused by prey defence | **Not without a stated observation and selection model.** Conditioning on thickness and counting incomplete holes is not enough: unattempted prey and attacks leaving no trace are still missing, and conditioning on the defence changes the target |
| Predator body-fossil morphology (Kelley 1992's characters; claw dimensions; crushing dentition) | Measured on the predator, independently of the prey | **Candidate capability.** Admitted only with a recorded functional mapping from trait to attack performance, with its uncertainty, per system |
| Predator body size from body fossils (for example the Heim et al. 2015 compilation, 10.1126/science.1260065; contents and deposit not checked) | Size, for size-limited modes | **Candidate capability**, with the same mapping requirement |
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

## 4. Target and estimands

**Level A: matched systems (the primary target, narrowed).**
- **Hypothesis:** *within-lineage* change in a prey defence follows
  independently measured, mechanically relevant change in a predator.
- **A system pairs:**
  - one predator mode;
  - a candidate-capability series P(t) for that predator, with its
    functional mapping;
  - a prey defence D(t) from that mode's row.

  Both sides come from the same habitat, region and lineages, across
  stratigraphic horizons t.
- **The estimand** is the directional association between changes in P and
  D at declared lags, with measurement variances. It is interpreted only
  beside a **common-cause comparison**: energetic and abiotic covariates at
  the same resolution, specified before the association is computed.
  Differencing alone does not remove time-varying common causes or shared
  observation error.
- **Lag-pattern categories are descriptive only:**
  - prey after predator;
  - predator after prey;
  - reciprocal;
  - prey change with no measured predator change;
  - neither.

  None of them is by itself an attribution of cause.

**Level B: relating local results to global composition (held).**
- A Price-equation split (Price 1970, 10.1038/227520a0) of a global defence
  trait into sorting and within-lineage change needs *time-resolved* traits
  of lineages that persist.
- Kosnik et al. 2011 apply one static mean per genus in every bin. Their
  within-genus component is therefore zero by construction, and they are
  not evidence for this estimand. They still describe **composition**.
- **Level B is held** unless time-resolved lineage traits are recovered.
  Even then:
  - a genus is not automatically a lineage, since species replace one
    another within it;
  - occurrence weights are not abundance or selection;
  - the decomposition is an identity, not a causal attribution.

## 5. Rivals and what can separate them

| Rival | Prediction |
| --- | --- |
| R0. Sampling and shared trend | Association disappears under common sampling and detrending (Madin et al.'s design) |
| R1. Shared energetics (Bambach 1993, 10.1017/S0094837300000336) | Predator and prey traits both follow productivity or metabolic indices. Finnegan et al. 2011 (10.1666/09066.1) give an independent Meso-Cenozoic gastropod metabolic-rate series |
| R2. Abiotic calcification (temperature, carbonate saturation, aragonite and calcite seas) | Thickness and ornament follow the cost of calcification |
| R3. Escalation | Within-lineage defence change, in the predator mode's row, follows candidate-capability change, *and* survives the common-cause comparison |

**Mode matching is a mechanistic prediction, not an exclusive test.**
Energetic and abiotic change can also act on both actors, and can produce
mode-specific responses. Mode matching sharpens what R3 predicts. It does
not by itself exclude R1 or R2.

**Sorting is not a rival to escalation by itself.** Signor & Brett place
extinction of undefended genera, radiation and within-clade change all in a
predation-driven account. A dominant sorting term cannot separate escalation
from non-escalation without evidence about what caused the sorting. Level A
therefore concerns the within-lineage route only.

## 6. Observation model

**Compositional confounding in compilations.** Re-tabulating Klompmaker's
open Database 2 (10.6084/m9.figshare.5046964; CC BY 4.0):
- Palaeozoic rows: 133 of 141 are brachiopods, 131 epifaunal and 123
  stationary;
- Paleocene–Pleistocene rows: 139 of 147 are molluscs.

This *demonstrates* compositional confounding. It does not measure how much
of any particular trait trend the shift explains.

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

## 7. Outcomes

**Level A, per system:**
- **Within-lineage tracking supported:**
  - a matched-row defence follows candidate-capability change at the
    declared lag;
  - beyond R0;
  - and it survives the common-cause comparison.
- **Descriptive coupling only:** the association is present, but the
  common-cause comparison is absent or cannot separate the causes.
- **Informative negative:** a precise null association with adequate
  support. Prey change with no measured predator change is recorded as
  that pattern. It does not refute predation as the selective agent.
- **Inadequate:** anything else.

**Across systems:**
- The summary is the share of systems in each class.
- Thresholds are fixed only after the inventory. A discrimination benchmark
  on the actual supported design, labelled as a benchmark, decides whether
  the cross-system route is informative.

## 8. Next gate: a published-source and support inventory

**Definitions, frozen on 15 October 2026 before the inventory:**
- **Candidate predator series:** body-fossil morphology or size of the
  predator mode in that system, with the trait-to-performance mapping and
  its source recorded. Drill-hole size enters only with a stated observation
  and selection model.
- **Matched prey series:** a trait in that mode's row, measured on prey
  lineages exposed in the same habitat and region.
- **Inventory screen**, for workflow only and not as evidence of adequate
  information:
  - at least 4 horizons with both series;
  - at least 10 specimens per horizon per side;
  - identification to lineage level;
  - data deposited or recoverable from published tables.

  Systems that fail the screen stay in the inventory, with reasons. Failure
  is not evidence of biological absence.
- **What each system's row records:**
  - joint horizon support;
  - age uncertainty;
  - measurement variances or specimen values, where available;
  - collection clustering;
  - lineage continuity;
  - reuse of samples across papers;
  - the number of usable lag pairs. Four horizons give three first
    differences and at most two lag-one pairs.

**Order and stopping rule:**
1. **Start with the Kelley pair** (Chesapeake Group naticids and bivalves:
   Kelley 1989, 1992, and the reappraisal by Dietl, Kelley & Handley,
   10.1017/s2475262200012156, probably a meeting abstract). Add a
   **contrasting mechanical mode**:
   - crushing, in Dietl et al. 2000's gryphaeid oysters;
   - apertural chipping, in Dietl 2003's whelks and Mercenaria.
2. **Then finish the nominated source families**, with one compact row each,
   including failures and inaccessible material:
   - Kelley et al. 2001 (10.1016/s0031-0182(00)00207-8);
   - Kelley & Hansen 2006 (10.1016/j.palaeo.2005.11.012);
   - Signor & Brett 1984;
   - Syverson et al. 2018 (10.1017/pab.2017.38, crinoid spinosity).
3. **For Level B, record only:**
   - whether Kosnik's supplement holds time-resolved values (the static
     definition in the main text stands regardless);
   - whether Finnegan et al.'s and Heim et al.'s data are available.
4. **No search beyond the nominated families.** No new specimen
   measurement, fit or author contact.
5. **Stopping rule.** If these sources do not jointly support the narrowed
   Level A target, report a practical hold, and move to Q-012/D1. The
   planning figure of about 3 systems governs workflow only.

**Overlap.** Q-048 and Q-037. B-011 also uses energetics. B-001's coding
gaps (fishes and sharks barely coded) also limit any predator-side series
based on Knope.

## 9. Amendment record (15 October 2026)

All of the following come from
[Codex's single review](../ideas/2026-10-15-blue-sky-specification-and-escalation-review-codex.md).
All were accepted.

| Review point | Change |
| --- | --- |
| Kosnik et al. apply static genus means (p. 321), so within-genus change is zero by construction | Level B is held. Kosnik's scores are kept for composition only, and the genus-as-lineage and identity-not-cause caveats are added |
| Kelley 1992 was over-read as uniform stasis | Restated as heterogeneous, with coevolution and cannibalism unresolved. Prey change without measured predator change does not refute predation |
| Sorting can be a predation route (Signor & Brett) | Replacement is removed as a rival in itself. Level A is narrowed to within-lineage tracking |
| Mode matching and lags do not exclude energetic or abiotic common causes | A common-cause comparison is required. Mode matching is a prediction, not an exclusive test. Lag categories are descriptive |
| Morphology needs a functional mapping; drill-hole selection is not repaired by conditioning | Both are now "candidate capability"; drill-hole size needs a stated selection model |
| Four horizons and ten specimens are screens, not information | Relabelled as an inventory screen. The extra recording fields and the lag-pair arithmetic are added |
| The Database 2 shift shows confounding but not its share | Qualified |

## 10. Inventory result (15 October 2026): practical hold

[Inventory](2026-10-15-b003-source-inventory.md), under the section 8
definitions frozen at `29367db`.

**What passed:**
- One system passes the horizon and sample-count part of the screen (its
  lineage continuity is unverified): Dietl 2003, Florida whelks and
  Mercenaria, apertural chipping. It falls short of the candidate-capability
  requirement:
  - the predator series is a sample maximum, with n of 16–36 that doubles
    across horizons;
  - the mapping is qualitative;
  - no variances;
  - one locality per horizon, except three in the Caloosahatchee;
  - at most 2 lag-one pairs.
- The Chesapeake naticid–bivalve pair cannot be scored, because its full
  texts were inaccessible.

**What failed:** every other family has no candidate predator series,
outcomes only, or genus composition.

**Level B:** Kosnik's and Heim's data are static per genus.

**Under the stopping rule agreed in 76/1668:**
- B-003 holds on support, and the question is kept.
- This is not evidence against escalation.
- Reopening terms are in the inventory.
