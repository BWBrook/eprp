# Step 3b: paragraph abstracts

12 November 2026, expanded from `3a-section-abstracts.md` (revision `283465d`); revised the same day after
Codex's critique (160/3281, `docs/audits/2026-11-12-paragraph-abstracts-critique.md`). For each section: the
paragraph framework as one-sentence summaries, an ordering and coverage check, then each paragraph as 3–4
short sentences. Bracketed comments signpost citations:
- `[cite: key]` gives the bibliography key in `references/refs.yaml`; the source status table at the end
  records what each use rests on.
- Citations were sourced by the References lane (76/3289,
  `resources/library/notes/2026-11-12-infrastructure-audit-citations.md`) and integrated at this revision.

## Introduction (five paragraphs)

**Framework.**
1. Large-scale paleobiology reaches its results through a chain of shared infrastructure.
2. That chain adds a second set of dependencies to the rock-record biases the field already studies.
3. The community has named parts of this layer as priorities, and reproducibility guidance says what
   checking it involves.
4. In this program, two AI agents carried out that checking and recorded the evidence for each check.
5. This paper reports twelve such checks as a case series organized by three questions.

**Check.** The order runs from the problem (1–2), through why it matters now (3) and how it can be
addressed (4), to what we did (5). Everything in the 3a Introduction is covered: the chain, rock-record
bias, the four kinds of dependency, Big Questions, reproducibility guidance, agents, and the three
questions with their deliverables.

**I1. The chain.** A diversity curve, extinction rate or paleolatitudinal gradient is the end of a chain:
occurrence databases, published deposits, time scales, age models, plate reconstructions and analysis
packages. Global diversity studies show how such a chain is built, from database occurrences and explicit
choices about sampling and analysis. Each link is maintained by others and changes over time.
[cite: alroy2008PhanerozoicTrendsGlobal; peters2016PaleobiologyDatabaseApplication; gradstein2020GeologicTimeScale (named reference work only)]

**I2. A second set of dependencies.** Paleobiology has a long literature on how the rock record distorts
inference, through sampling, preservation and rock availability. The shared infrastructure adds a second
set of dependencies: data transformations, software implementations, model choices and the meaning of what
each tool reports. These sit between the rocks and the result in every large-scale analysis.
[cite: dillon2023ChallengesDirectionsAnalytical; raup1972TaxonomicDiversityPhanerozoic (passage pending); smith2001LargescaleHeterogeneityFossil (abstract: rock availability)]

**I3. Why now.** Among the 89 Big Questions in paleontology are questions on data-entry bias, lost
historical information, reporting and data integration. Guidance on computational reproducibility
recommends tracking inputs and procedures, preserving versions and inspecting intermediate results.
Together they ask for exactly the kind of checking this layer needs. [cite:
smith2025IdentifyingBigQuestions (AFR2–AFR4, FI1); sandve2013TenSimpleRules]

**I4. Agents as auditors.** Checking the layer means comparing data with their sources, running software
against known answers, inspecting code and recomputing published numbers. That work is broad and detailed.
In this program, two AI agents carried out the checks reported here, recording the evidence, command and
input hashes for each. A benchmark of agents reproducing published computations is the nearest precedent.
[cite: siegel2024CorebenchFosteringCredibility]

**I5. This study.** We report twelve findings from two agents building a paleobiology research program in
October–November 2026. Three questions organize them: where each finding arose, what checks established it,
and what changed when a second agent re-examined it. Each case comes with the evidence and command needed to verify it, and with actions for researchers,
maintainers, journals and agent-based programs.

## Methods (five paragraphs)

**Framework.**
1. The program, its agents and the facilitator's role.
2. How candidate findings arose.
3. How the twelve cases were selected and coded.
4. How each case was replayed and checked.
5. How wording was reviewed and the record kept.

**Check.** The order is chronological, from setting through discovery, selection and replay to review.
Everything in the 3a Methods is covered: the setting, mirroring, declared tests with amendments,
exploratory probes, recomputation, the 189 candidates, selection on 8 November, retrospective coding on
12 November, discovery routes, replay, separate routes, the ledger, wording review, logging, versions and
disclosure.

**M1. Setting.** The Extinction and Paleontology Research Programme began in October 2026, run by two AI
agents, Anthropic's Claude and OpenAI's Codex, with a human facilitator. The facilitator set direction and
held every external decision: contact with providers, release and submission. Agent contributions are
disclosed by system, version and task. [cite: Paleobiology AI policy, as a statement rather than a
reference]

**M2. How candidates arose.** While vetting research questions, the agents mirrored databases, deposits and
plate models with checksums. They benchmarked packages against simulations with known answers, through
declared validation tests with dated amendments and through exploratory follow-up probes, and they
recomputed published numbers. Three working sessions logged 189 initial candidate findings, including
positive controls and intended behaviors, and later additions joined as the program ran. [cite: package
papers and versions in Table S1; peters2016PaleobiologyDatabaseApplication]

**M3. Selection and coding.** On 8 November 2026 we selected twelve cases for consequence to inference,
variety of finding class and inclusion of positive controls, excluding licensing and bibliographic
metadata. On 12 November each case was coded retrospectively by the dependency checked: data
transformation, implementation, model choice or output meaning, with a secondary kind where needed.
Discovery routes come from dated records.

**M4. Replay and checks.** An agent other than the original finder replayed each case from pinned inputs.
Where possible it rederived key numbers by a separate route: independent aggregation, interpolation,
geometry or scoring code, recounts from raw files, or closed-form arithmetic. Each verified proposition
entered a claims ledger with its value, evidence, verifying commit, reproduce command and limits.

**M5. Review and record.** A second review checked every draft sentence against an interpretation
specification stating what each case licenses. Corrections at each stage were logged with who found them
and what replaced them. Versions, environments and input hashes accompany each replay in the program's public
repository. A tagged snapshot will be archived with a DOI at release.

## Results (seven paragraphs)

**Framework.**
1. Overview: twelve cases across four kinds of dependency.
2. Data transformations in the Paleobiology Database: deposit membership and interval re-dating.
3. Data transformations in microfossil databases: excess Triton rows and NSB stored ages.
4. Analysis packages.
5. Published products that differ from their sources or stated tests.
6. Model choices and output meaning.
7. Checks and review.

**Check.** Paragraphs 2–6 group the cases by resource (databases, packages, published products, models),
because that is how a reader meets them; the formal primary and secondary dependency codes sit in Table 1.
Paragraph 7 answers the second and third questions. The order within databases runs from the most widely
used outward. Everything in the 3a Results is covered, with two additions: the Triton ≥1° count and GRIWM's
random-number finding (C098), omitted from 3a.

**R1. Overview.** The twelve cases cover four kinds of dependency (Table 1). They sit along the whole chain
from deposit to published number (Fig. 1A). Each rests on a replay from pinned inputs and a second agent's
check (Fig. 1B).

**R2. Paleobiology Database.** Of 368,760 molluscan occurrences in a published deposit, 71,103 were absent
from the public snapshot of 23 October 2026 (Fig. 2A). Keeping only snapshot members cut the stages passing
our regional presence screen from 14 to 12 of 21 (Table 1). Across three archived snapshot pairs, 460, 317
and 17 intervals changed their modal base age (Fig. 2B). [cite: benson2025MarineAnimalDiversity; PBDB Data Service 1.2
interval documentation, dated URL in text]

**R3. Microfossil databases.** Removing 16,260 excess rows from the 2023 Triton update changed 1,388 of
2,267 mean absolute paleolatitudes in our analysis (Fig. 2C). 411 of those changes were at least one
degree. In Neptune
Sandbox Berlin, 4,111 of 56,387 stored sample ages differed by more than 0.01 Myr from ages interpolated
from the database's tie points (Fig. 2D). [cite: fenton2021TritonSpecieslevelDatabase;
renaudie2020NsbNeptuneSandbox]

**R4. Analysis packages.** admtools 0.7.0 mis-converted 3,972 of 8,282 heights to times in a synthetic
two-hiatus model, by up to 3.0 Myr (Fig. 3A). fossilbrush 1.0.6 compared numbers as text, so at a
threshold of 5 it passed differences of 10, 100 and 499 (Fig. 3B). GRIWM in Rextinct 1.1.0 overwrote the
caller's random-number state. [cite: hohmann2025NonparametricEstimationAgedepth;
hohmann2023AdmtoolsEstimateManipulate; flannerysutherland2022FossilbrushRPackage;
flannery-sutherland2022FossilbrushAutomatedCleaning; bradshaw2012RobustEstimatesExtinction; tested versions in
Table S1]

**R5. Published products.**
- 2,967 of 6,562 capture histories in a published spreadsheet differed numerically from the intact
  binary deposit.
- The one-file Fossil Record 2 table held 220 rows with left-shifted cells.
- A printed probability of 3.4 × 10⁻¹⁶ is 0.32 under the paper's stated binomial test.
- Three archived rejected proposals in INDITEK-2's synthetic demonstration reproduced their predictions,
  while their saved residual-sum-of-squares scores differed from rescoring by up to 42.4.

[cite: monarrez2023ReducedStrengthIncreased; rampino2025CorrelationCyclicityStratigraphic;
herrerogascon2026Inditek20; benton1993FossilRecord2]

**R6. Model choices and output meaning.** PyRate's 95% preservation-rate intervals covered the true value
in 81 of 100 and 33 of 50 simulated datasets, while extinction-time range-end bounds covered it in
1,895–1,909 of 2,000 cases in their own test (Fig. 3C). GRIWM's resampling interval measures sensitivity
to dating error. Three plate models disagreed on paleolatitude by a median of 2.9° at 10 Ma and 13.6° at
400 Ma (Fig. 3D), and two routes to one model differed by age-specific near-rigid rotations. [cite:
silvestro2014PyrateProgramEstimate; strauss1989ClassicalConfidenceIntervals;
bradshaw2012RobustEstimatesExtinction; robson1964EstimationTruncationPoint (as implemented in EDE 0.2.0);
merdith2021ExtendingFullplateTectonic; matthews2016GlobalPlateBoundary;
scotese2016PaleomapPaleoatlasGplates; torsvik2016EarthHistoryPalaeogeography (model label TorsvikCocks2017)]

**R7. Checks and review.** Each finding rests on its own mix of re-execution, recomputation from source,
code inspection and arithmetic (Table 1). INDITEK, for example, combined a forward replay with separately
written rescoring. Replay corrected the initial accounts of six cases. PyRate's, for example, moved from
"intervals too narrow" to "intervals shifted high" (Table S3).

## Discussion (six paragraphs) and Conclusions (one)

**Framework.**
1. The principal finding: agents checked four kinds of dependency, with consequences for what researchers
   record, test and interpret.
2. Discrepancies against a specified source or known answer: what direct comparison establishes, and what
   makes it possible.
3. Model sensitivity and interval meaning: two different judgments a researcher has to make.
4. Actions for each audience.
5. The agents' own record, and the proposal for other fields.
6. Limitations.
7. Conclusions: the main message and future work.

**Check.** The order runs from the principal finding (1), through interpretation by kind (2–3), to use (4),
method (5), limits (6) and close (7). Everything in the 3a Discussion is covered, including the separate
future-work sentence, which moves to Conclusions.

**D1. Principal finding.** Agents checked all four kinds of dependency between rocks and results across one
research program. Every case changes what a researcher should record, test or interpret. Each check is
documented with its evidence, pinned inputs and command.

**D2. Comparison with a source.** Where a source or known answer is specified, a direct comparison
establishes a discrepancy: in records present, interval ages, row counts, conversions, flags or published
numbers. Such a check is possible only when the query date, version and intermediate products are kept, so
recording them lets a researcher test inputs before any biological model is fitted. Locating a
discrepancy and explaining its cause are separate steps; INDITEK's score mismatch, for one, is located and
its cause open. [cite: sandve2013TenSimpleRules; gbif2026ApiDownloads; gbif2026Citation]

**D3. Models and meaning.** The three tested plate models placed the same points degrees apart, so an
analysis whose result depends on paleolatitude should state its model and cohort and report the spread
among alternatives. An interval needs two other judgments: which uncertainty process it propagates, and how
often it covers the truth. GRIWM's interval propagates dating error, and PyRate's preservation-rate intervals
covered the truth less often than nominal in simulation. Both kinds of finding change how a result is read.
[cite: vanhinsbergen2015PaleolatitudeCalculatorPaleoclimate; bradshaw2012RobustEstimatesExtinction]

**D4. Actions.** Users can record query dates and versions, compare plate models and replay published
numbers before reuse. Maintainers can version changes and document what outputs measure. Journals and
depositors can require machine-readable deposits with scoring code. Agent-based programs can pair each
finding with a second check, as the corrections here motivate, and publish their receipts (Table 2).

**D5. The agents' record.** Replay corrected six initial accounts, and wording review corrected this
paper's first draft, so the record documents the auditors' errors as well as the infrastructure's. The
same source comparison and known-answer checks could serve other fields built on community databases and
shared code, such as biodiversity informatics. We offer that as a proposal for future work. [cite:
yesson2007HowGlobalGlobal, as motivation]

**D6. Limitations.** The cases were selected for consequence, so they describe kinds of finding, not their
frequency. We replayed published calculations and part of one deposited model, not whole downstream
studies. Checks vary in independence, some share inputs or model family, and the calibration controls rest
on two simulated clades with one failed agreement gate. Some inputs are held locally, a cold public rebuild
is untested, and providers and authors had not been contacted at the time of writing.

**C1. Conclusions.** AI agents can systematically check the databases and software behind fossil-record
research, and they found verifiable errors and pitfalls that researchers need to know about. Three
studies would extend it, each with its own payoff. An audit of a defined population of dependencies would
estimate how often such findings occur; a matched comparison of agent and human auditors would measure
their relative performance; and replay of downstream studies would test what particular findings change.

## Source status

Every citation key above is in `references/refs.yaml`, built from registered metadata (Crossref; DataCite
for PALEOMAP; arXiv for CORE-Bench; publisher catalogue and ISBN for the two books; official pages for
GBIF). Passage support comes from the References return (76/3289) and the step 3a review (160/3272).

| Use | Source | Passage status and limit |
|---|---|---|
| I1 chain | Alroy 2008; Peters & McClennen 2016 | Read. Data model and API structure; not EPRP's mirroring |
| I1 time scale | GTS2020 (Gradstein et al., eds) | Identity only; cite as the named reference work, with no chapter claims |
| I2 rock-record bias | Dillon et al. 2023 | Read; carries the generic bias sentence |
| I2 history | Raup 1972; Smith 2001 | Raup identity only, passage pending. Smith: abstract, rock availability only |
| I3 | Smith et al. 2025; Sandve et al. 2013 | Read (160/3272) |
| I4 precedent | Siegel et al. 2024 (CORE-Bench) | Read. Agents reproduce supplied computations; context only |
| R2 interval fields | PBDB Data Service 1.2 documentation | Read 12 Nov 2026; current documentation, not a frozen October schema |
| R4 packages | Hohmann et al. 2025; Flannery-Sutherland et al. 2022; CRAN package DOIs | Method and manual read; tested versions 0.7.0 and 1.0.6 named separately |
| R5 FR2 | Benton 1993 (ed.) | Book identity and official Bristol digital-product pages |
| R6 range-end bound | Robson & Whitlock 1964 | Original identity only; EDE 0.2.0 implementation read |
| R6 plate models | Scotese 2016 v3; Torsvik & Cocks 2016 | Registry match to the tested models; book chapters unread |
| D2 versioning | Sandve et al. 2013; GBIF documentation | Read |
| D3 | van Hinsbergen et al. 2015; Bradshaw et al. 2012 | Read. Propagated versus frame uncertainty; GRIWM process |
| D5 | Yesson et al. 2007 | Read; motivation for a proposed application |

Open before submission: the Raup 1972 passage, a GTS2020 chapter passage if a specific claim is drawn from
it, and the original Robson–Whitlock passage. Solow et al. 2006 (`10.1073/pnas.0509480103`) is checked and
held in reserve for D3.
