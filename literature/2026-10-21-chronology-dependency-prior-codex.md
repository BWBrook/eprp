# Chronology dependencies: bounded prior and consequence review

21 October 2026. Codex subagent review for the whole-consultation assessment.
Scope: card 2 / deep dive B2 of the outside consultation and Claude's assessment.
No age model was run; no raw occurrence compilation was reconstructed. This is
an opportunistic, finite prior check, not a systematic review.

## Ruling

**Retain a bounded claim audit; do not yet promote a general chronology-audit
programme as a distinct biological question.** The principle is established,
including in Cambrian research, and the local SPICE–trilobite ordering problem
already has close empirical prior work. A new contribution would have to show
which specific biological explanation changes when target-derived correlations
are withheld, or give a useful quantitative bound that existing work lacks.

**Correct Claude's statement that fixing biomere synchrony means the chronology
cannot test those boundaries' synchrony with SPICE.** That conflates two targets.
The fixed composite cannot independently test interregional synchrony of the
biomere boundaries that it identifies as common events. It can still compare an
independently located isotope feature with a fossil boundary in one section.
Local order, numerical local duration and interregional synchrony have different
dependencies. B2 itself makes this distinction correctly.

## What Farrell actually fixes

Primary evidence: Farrell et al. (2025), [10.1130/B37919.1](https://doi.org/10.1130/B37919.1),
public supplement [10.1130/GSAB.S.28207634](https://doi.org/10.1130/GSAB.S.28207634),
S2 pp. 5–10 and S4 p. 16; released R scripts and workbook XML inspected on
21 October. Main article access in this review was **abstract only**. This note
therefore establishes the construction of the supplied chronology; it does not
attribute an unverified synchrony claim to the main article.

S2 starts from 61 sections and 614 taxa, using published and unpublished
first/last occurrences. It introduces six unpaired events: the bases of the
Corynexochid, Marjumiid, Pterocephaliid, Ptychapsid and Symphysuriniid biomeres,
and the Drumian boundary. The five biomere bases are expressly treated as
synchronous at the study's scale. They are encoded as event type 4 with allowed
moves 0. The Pterocephaliid boundary is initially recognised in 17 sections.
Further boundary occurrences are inserted above/below actual taxon records,
including outside sampled intervals; the authors explain that only their
relative order, rather than those artificial metre positions, enters this
calculation. These are declared modelling constraints, not independent
observations of synchronicity or evidence of source misconduct.

**SPICE is not among those six fixed CONOP events.** S4 identifies onset and
termination using measured carbon-isotope values and section heights, with
resampling, perturbation and smoothing; the reported onset is 121.9
(+2.7/−1.6) m. The prediction workbook separately records `begin SPICE` at
122.5 m with error 2 m and `base Aphelaspis` at 125 m with error 2 m. Thus the
released package keeps distinct local positions. Their close spacing and
uncertainty also mean that different central heights alone do not establish a
resolved lag. The small difference between the S4 summary and prediction-input
centre should be traced in any numerical reproduction, not silently repaired.

| Target claim | What the fixed biomere construction implies |
| --- | --- |
| The same biomere turnover was synchronous across the correlated sections | Assumed by that representation; cannot be independently demonstrated from its resulting common boundary age |
| SPICE onset lies above/below the local turnover in Smithfield | Not supplied by identifying distant biomere boundaries; local measured ordering survives, subject to horizon uncertainty, preservation and section integrity |
| A numerical Smithfield isotope–turnover lag or SPICE duration | Conditional on the age–depth calibration and its biozone information; evaluate sensitivity rather than declare circularity from the fixed-event list alone |
| SPICE itself was synchronous across regions | Not fixed by those six CONOP events, but requires tracing any isotope matching and age transfers elsewhere in the calibration; this review does not establish their independence |
| A global redox perturbation caused trilobite extinction | Neither carbon onset nor a named biomere boundary alone identifies this; local disappearance, true extinction and distinct redox observations require separate treatment |

If two locally observed signals have inconsistent order between sections, at
least one need not be a globally simultaneous marker, or there is a recording/
identification problem. Such evidence does not alone identify which marker is
diachronous. Likewise, uncertainty after withholding correlations is not
positive evidence of diachroneity.

## Nearest prior work and access depth

All access below is 21 October 2026. Sources describe their own findings;
novelty/consequence rulings in this note are reviewer inference.

| Source and access | Already achieved; implication for the proposal |
| --- | --- |
| Arens & Jahren (2002), *Chemostratigraphic correlation of four fossil-bearing sections in southwestern North Dakota*, [10.1130/0-8137-2361-2.75](https://doi.org/10.1130/0-8137-2361-2.75). [Full PDF](https://static1.1.sqspcdn.com/static/f/1454805/19965897/1345597422027/Arens_and_Jahren_2002.pdf) acquired; introduction and conclusions pp. 75–76, 89–90 inspected | Explicitly identifies circularity when the fossils defining an extinction horizon also document the extinction. Uses carbon-isotope stratigraphy as additional evidence independent of taxonomic extinction to correlate four sections. This directly occupies the general principle and an empirical response; isotope synchrony is a replacement assumption, not universal independence. |
| Maloof et al. (2010), *The earliest Cambrian record of animals and ocean geochemical change*, [10.1130/B30346.1](https://doi.org/10.1130/B30346.1). [Author PDF](https://maloof.princeton.edu/document/157), abstract/introduction pp. 1731–1733 inspected in web PDF text; local download blocked | Maps fossil appearances onto an ash-calibrated isotope framework while deliberately ignoring fossil tie points. Explicitly substitutes isotope-trend synchrony for fossil-appearance synchrony to avoid circular inference. Although published as an invited review, this contains a concrete reconstruction with new geochemical data. Independent-clock reasoning is already explicit in the Cambrian. |
| Crampton et al. (2016), *Southern Ocean phytoplankton turnover in response to stepwise Antarctic cooling over the past 15 million years*, [10.1073/pnas.1600318113](https://doi.org/10.1073/pnas.1600318113). [Full HTML and integrated SI](https://pmc.ncbi.nlm.nih.gov/articles/PMC4922175/) acquired; CONOP age calibration and SI inspected | Constructs composite diatom histories and an age-calibration ensemble. Explicitly excludes polarity observations whose identification relies entirely on diatom data, to avoid circularity. An operational dependency screen is therefore prior practice, beyond a general warning. It does not constitute the proposed Cambrian counterfactual audit. |
| Schiffbauer et al. (2017), [10.1126/sciadv.1602158](https://doi.org/10.1126/sciadv.1602158). [Full main PDF](https://biogeochem.wustl.edu/wp-content/uploads/2013/05/Schiffbauer_SPICE_transgression_SciAdv_2017.pdf), relevant results/discussion pp. 2–5 inspected; numerical SI not acquired | Already compares local isotope–biozone order across Missouri cores, corrects a prior biozone placement, and documents differing SPICE positions relative to trilobite turnover. It also acknowledges weak fossil control and likely time-transgressive lithological correlation in shallower cores. Repeating heterogeneous local order, or merely questioning coupled SPICE/extinction, is insufficient novelty. |
| Pulsipher et al. (2021), *SPICEraq*, [10.1016/j.earscirev.2020.103442](https://doi.org/10.1016/j.earscirev.2020.103442). [Full PDF](https://par.nsf.gov/servlets/purl/10228955) acquired via direct retrieval; §§2, 4.4–4.6 inspected; raw Excel not acquired | Quantifies expression across 78 SPICE-bearing records. It already treats weak/absent excursion candidates separately (SWEETS), discusses wrong age, alteration and missing section, and states isotope-correlation assumptions explicitly. Including absent excursions and preserving facies alternatives are established design elements. It does not provide independent numerical calibration for every record or a target-withheld synchrony bound. |
| Spencer-Cervato et al. (1994), [10.1029/94PA01456](https://doi.org/10.1029/94PA01456). Publisher abstract inspected; author publication listing checked; full methods appeared in third-party search extraction only | Abstract establishes a close quantitative prior: 124 bioevents in 35 holes analysed for synchrony/diachrony using combined biostratigraphic and magnetic evidence. Full independence claims are **not verified** here; extracted discussion acknowledges circularity but regards multi-group information as sufficient. Retain as a prior lead, not as proof that a formal target-withholding audit has already been done. |

A wider systematic extinction-wide provenance audit with the precise B2
ablations was **not found in this finite search**. That is not evidence that
none exists, and it does not make a general audit scientifically distinct.
The occupied components already justify downgrading a claim of conceptual
novelty. Access to Farrell's full raw matrix is a separate feasibility problem.

## Strongest rival, residual question and next test

The strongest rival is that this proposal packages competent stratigraphic
practice as a new programme. Farrell's constraints are explicit, conditional
calibration is legitimate, SPICE heterogeneity is established, and no examined
source has yet been shown to draw a biological conclusion that its own
constraints make untestable. Producing a provenance graph could be useful
infrastructure while changing no scientific inference.

The residual worth testing is narrower: **which proposed extinction mechanisms
are excluded, remain possible, or are unresolved by the joint local loss–carbon–
redox ordering evidence when target-derived correlations are withheld?** A
useful deliverable must identify a mechanistic claim and the temporal ordering
or lag window it needs. Carbon onset is not automatically redox onset. A
universal 0.5 Myr equivalence threshold is a proposed choice, not a demonstrated
biological tolerance, and needs justification for the mechanism being tested.

The cheapest discriminating tranche is a desk-based claim/constraint table,
not simulations or a global chronology build:

1. Select at most three explicit published claims concerning this event and
   name their targets: local ordering, local elapsed time or interregional
   synchrony. Start with Farrell's local lag interpretation and Schiffbauer's
   ordering contrasts; verify exact wording in the main articles before
   declaring a failure.
2. Trace only the inputs supporting those claims, retaining the raw local
   isotope/fossil depths and their uncertainties. Mark direct dates at their
   measured section separately from transfers, maximum depositional ages,
   common fossil events and isotope matches. Record shared calibration.
3. Check whether at least one claimed biological discrimination actually
   relies on a target-derived link. If not, stop the circularity allegation
   and retain a short methods note. If yes, determine whether remaining
   local-order evidence or public independent calibration can discriminate
   its rival before fitting.
4. Proceed to one targeted sensitivity comparison only if that comparison
   can change the mechanistic conclusion or yield a useful resolving bound.
   Stop as **support-limited** if deleting derived constraints leaves no
   informative clock and the inaccessible occurrences are required. That
   outcome is not diachroneity and not a failed novelty test. Stop as
   **prior-occupied/routine** if it only repeats established local-order or
   facies results. A null sensitivity result can still validate a specific
   conclusion, without establishing a new programme target.

Without the raw CONOP inputs, dropping aggregate biozone constraints is a
public-input sensitivity analysis. It cannot isolate the effect of fixed
biomere synchrony, because those aggregates also contain useful nontarget
information. Relabelling a derived age does not remove its ancestry.

A literal public-script reproduction also needs a small disclosed repair:
`Farrell_et_al_model.R` reads sheets `GTS`, `EqD`, `CONOP`, while the downloaded
workbook names them `model 1`, `model 2`, `model 3`. No scripts were run or edited;
package availability is not a successful numerical reproduction.

## Finite search and retained evidence

Search service: web search, no date/language filters; primary papers,
author-hosted PDFs and the source repository were preferred. Search snippets
were discovery aids, with unverified leads labelled above. Search stopped when
exact CONOP constraints were established and multiple direct prior examples
occupied the principle, while no claim-level biological failure had been shown.

The following exact query families were run, alongside direct DOI/source opens:

| Purpose | Queries |
| --- | --- |
| Farrell acquisition and construction | `Farrell 2025 B37919.1 supplement CONOP synchronous biomere boundaries`; `biostratigraphy circularity correlation synchrony leave one out CONOP chronology`; `"Farrell" "B37919.1" pdf`; `"28207634" Farrell`; `"Revising the late Cambrian" "pdf"`; `Farrell Cothren Sundberg Schmitz 2025 Cambrian Bayesian pdf filetype:pdf` |
| Direct circularity/withholding prior | `chronostratigraphy "circularity" extinction correlation`; `"stratigraphic" "circularity" "correlation" "extinction" -astronomy -galaxies -luminosity -paleomagnetic -circular`; `"biostratigraphy" "leave-one-out" synchrony`; `"chronology" "event-free" extinction`; `"biostratigraphy" "circularity" "synchrony"`; `"chronology" "dependency" "extinction" stratigraphy`; `"extinction" "circularity" "age models"`; `"correlation" "circularity" "Cambrian" SPICE`; `"stratigraphic" "circularity" "audit"` |
| Named-prior verification | `"Southern Ocean phytoplankton turnover" 2016 circularity`; `"SPICEraq" "Pulsipher" pdf`; `"Chemostratigraphic correlation of four fossil-bearing sections" Arens Jahren 2002`; `"How synchronous are neogene marine plankton events" magnetostratigraphic`; `"How synchronous" "Spencer-Cervato" filetype:pdf -site:researchgate.net`; `"Arens" "Jahren" "2002" "10.1130" "Chemostratigraphic"`; `"Earliest Cambrian" "Maloof" "2010" "B30346"` |

Access failures: supplement DOI redirect failed through the web tool, but
[Figshare API](https://api.figshare.com/v2/articles/28207634) supplied both source
files. NSF PDF failed in the web tool but direct retrieval succeeded. PMC web
and Europe PMC XML routes failed, while direct PMC HTML succeeded. Main Farrell
full text and Spencer-Cervato full primary-hosted text remain unverified.
An EarthArXiv lead on glacial-deposit circularity was blocked by a bot challenge;
it supplies no supporting claim here. Some broad queries returned irrelevant
material; this is a finite orientation search, without a formal coverage claim.

Downloaded articles are under ignored `scratch/chronology-prior-20261021/`.
Source identities/hashes and the workbook inspection are preserved in
[the joint-review evidence archive](../data/consultation-review-20261021-codex.tar.gz);
the original article PDFs are not redistributed in that archive.
Farrell archive identity:

- `B37919_SuppMat1.pdf`: SHA256 `57e5d15bbe2eb7650f10d0f0c981c27baa44e5f82e38acea9022ebef112ee14b`.
- `B37919_SuppMat2.zip`: SHA256 `87af7495d4fef6d8be78160274194a1440337b9dab0d8f2da4b06e8d7994623c`.

Completed: exact-constraint check and bounded prior/consequence ruling.
Provisional: distinct biological return and availability of an informative
independent calibration. Next owner: parent Codex integrates this assessment;
Claude should respond to the narrowed target before any programme promotion.
