# Step 3b: paragraph abstracts

12 November 2026, expanded from `3a-section-abstracts.md` (revision `283465d`). For each section: the
paragraph framework as one-sentence summaries, an ordering and coverage check, then each paragraph as 3–4
short sentences. Bracketed comments signpost citations:
- `[cite: key]` is in the bibliography or verified (status table at the end of 3a);
- `[to source: …]` is still to be found and checked.

## Introduction (five paragraphs)

**Framework.**
1. Large-scale paleobiology reaches its results through a chain of shared infrastructure.
2. That chain adds a second set of dependencies to the rock-record biases the field already studies.
3. The community has named parts of this layer as priorities, and reproducibility guidance says what
   checking it involves.
4. AI agents can now carry out that checking across a research program and record every step.
5. This paper reports twelve such checks as a case series organized by three questions.

**Check.** The order runs from the problem (1–2), through why it matters now (3) and how it can be
addressed (4), to what we did (5). Everything in the 3a Introduction is covered: the chain, rock-record
bias, the four kinds of dependency, Big Questions, reproducibility guidance, agents, and the three
questions with their deliverables.

**I1. The chain.** A diversity curve, extinction rate or paleolatitudinal gradient is the end of a chain:
occurrence databases, published deposits, time scales, age models, plate reconstructions and analysis
packages. Global diversity studies show how such a chain is built, from database occurrences and explicit
choices about sampling and analysis. Each link is maintained by others and changes over time.
[cite: alroy2008] [to source: a PBDB data-model or overview paper; a time-scale paper, e.g. GTS2020]

**I2. A second set of dependencies.** Paleobiology has a long literature on how the rock record distorts
inference, through sampling, preservation and rock availability. The shared infrastructure adds a second
set of dependencies: data transformations, software implementations, model choices and the meaning of what
each tool reports. These sit between the rocks and the result in every large-scale analysis.
[cite: raup1972; smith2001] [to source: one recent sampling-standardization review, e.g. Close et al. or
Benson et al.]

**I3. Why now.** Among the 89 Big Questions in paleontology are questions on data-entry bias, lost
historical information, reporting and data integration. Guidance on computational reproducibility
recommends tracking inputs and procedures, preserving versions and inspecting intermediate results.
Together they ask for exactly the kind of checking this layer needs. [cite:
smith2025IdentifyingBigQuestions (AFR2–AFR4, FI1); sandve2013]

**I4. Agents as auditors.** Checking the layer means comparing data with their sources, running software
against known answers, inspecting code and recomputing published numbers. That work is broad and detailed.
AI agents can now carry it out across a whole research program, keeping a record of each step that others
can rerun. [to source: two or three recent papers on agentic AI in scientific research, preferably with
verification or reproducibility tasks]

**I5. This study.** We report twelve findings from two agents building a paleobiology research program in
October–November 2026. Three questions organize them:
1. Where did each finding arise?
2. What checks established it?
3. What changed when a second agent re-examined it?

Each case comes with the evidence and command needed to verify it, and with actions for researchers,
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
papers and versions in Table S1] [to source: a PBDB API or data-access reference]

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
and what replaced them. Versions, environments and input hashes accompany each replay, in a public
repository with an archived release. [to source: Zenodo DOI at release]

## Results (seven paragraphs)

**Framework.**
1. Overview: twelve cases across four kinds of dependency.
2. Data transformations in the Paleobiology Database: deposit membership and interval re-dating.
3. Data transformations in microfossil databases: excess Triton rows and NSB stored ages.
4. Implementation defects in analysis packages.
5. Published products that differ from their sources or stated tests.
6. Model choices and output meaning.
7. Checks and review.

**Check.** The order follows the four kinds of dependency (1–6), then the second and third questions (7).
The order within data transformations runs from the most widely used database outward. Implementations
split into packages (4) and published products (5), because those audiences differ. Everything in the 3a
Results is covered, including the Triton ≥1° count, which returns here with Table 1 support.

**R1. Overview.** The twelve cases cover four kinds of dependency (Table 1). They sit along the whole chain
from deposit to published number (Fig. 1A). Each rests on a replay from pinned inputs and a second agent's
check (Fig. 1B).

**R2. Paleobiology Database.** Of 368,760 molluscan occurrences in a published deposit, 71,103 were absent
from the public snapshot of 23 October 2026. Keeping only snapshot members cut the stages passing our
regional presence screen from 14 to 12 of 21 (Fig. 2A). Across three archived snapshot pairs, 460, 317 and
17 intervals changed their modal base age (Fig. 2B). [cite: benson2025MarineAnimalDiversity] [to source:
PBDB time-scale documentation]

**R3. Microfossil databases.** Removing 16,260 excess rows from the 2023 Triton update changed 1,388 of
2,267 mean absolute paleolatitudes in our analysis, 411 by at least one degree (Fig. 2C). In Neptune
Sandbox Berlin, 4,111 of 56,387 stored sample ages differed by more than 0.01 Myr from ages interpolated
from the database's tie points (Fig. 2D). [cite: fenton2021TritonSpecieslevelDatabase;
renaudie2020NsbNeptuneSandbox]

**R4. Analysis packages.** admtools 0.7.0 mis-converted 3,972 of 8,282 heights to times in a synthetic
two-hiatus model, by up to 3.0 Myr (Fig. 3A). fossilbrush 1.0.6 compared numbers as text, so at a
threshold of 5 it passed differences of 10, 100 and 499 (Fig. 3B). [to source: admtools paper or CRAN
citation; fossilbrush paper (Flannery-Sutherland et al. 2022?)]

**R5. Published products.**
- 2,967 of 6,562 capture histories in a published spreadsheet differed numerically from the intact
  binary deposit.
- The one-file Fossil Record 2 table held 220 rows with left-shifted cells.
- A printed probability of 3.4 × 10⁻¹⁶ is 0.32 under the paper's stated binomial test.
- Three archived rejected proposals in INDITEK-2's synthetic demonstration reproduced their predictions,
  while their saved residual-sum-of-squares scores differed from rescoring by up to 42.4.

[cite: monarrez2023ReducedStrengthIncreased; rampino2025CorrelationCyclicityStratigraphic;
herrerogascon2026Inditek20] [to source: Fossil Record 2 (Benton 1993)]

**R6. Model choices and output meaning.** PyRate's 95% preservation-rate intervals covered the true value
in 81 of 100 and 33 of 50 simulated datasets, while extinction-time range-end bounds covered it in
1,895–1,909 of 2,000 cases in their own test (Fig. 3C). GRIWM's resampling interval measures sensitivity
to dating error. Three plate models disagreed on paleolatitude by a median of 2.9° at 10 Ma and 13.6° at
400 Ma (Fig. 3D), and two routes to one model differed by age-specific near-rigid rotations. [cite:
silvestro2014PyrateProgramEstimate; strauss1989ClassicalConfidenceIntervals;
bradshaw2012RobustEstimatesExtinction; merdith2021ExtendingFullplateTectonic;
matthews2016GlobalPlateBoundary] [to source: Robson & Whitlock 1964; PALEOMAP (Scotese); Torsvik & Cocks
2017]

**R7. Checks and review.** Each finding rests on its own mix of re-execution, recomputation from source,
code inspection and arithmetic (Table 1). INDITEK, for example, combined a forward replay with separately
written rescoring. Replay corrected the initial accounts of six cases. PyRate's, for example, moved from
"intervals too narrow" to "intervals shifted high" (Table S3).

## Discussion (six paragraphs) and Conclusions (one)

**Framework.**
1. The principal finding: agents checked four kinds of dependency, with consequences for what researchers
   record, test and interpret.
2. Data transformations and implementations: inputs and outputs change before and during analysis.
3. Model choices and output meaning: structural spread and what an interval represents.
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

**D2. Inputs and code.** Data transformations altered the inputs to analysis before any model ran: which
records are present, what age an interval carries, how many rows a sample contributes. Implementation
defects altered conversions, flags and published numbers. Both were found by comparing a result with its
source or with a known answer, and by inspecting intermediate results as reproducibility guidance
recommends. [cite: sandve2013]
[to source: data-versioning practice in large databases, e.g. GBIF or PBDB download citation guidance]

**D3. Models and meaning.** Plate reconstructions disagree by degrees of paleolatitude, so model choice is
a source of structural spread in any latitudinal analysis. Output meaning determines which uncertainty an
interval represents: GRIWM's interval represents dating error. Both are legitimate features of the tools,
and both need stating when results are reported. [to source: a paleolatitude-uncertainty study (e.g.
Buffan et al. or Jones et al.); an extinction-time estimation review (e.g. Saltré et al. or Marshall)]

**D4. Actions.** Users can record query dates and versions, compare plate models and replay published
numbers before reuse. Maintainers can version changes and document what outputs measure. Journals and
depositors can require machine-readable deposits with scoring code. Agent-based programs can pair each
finding with a second check, as the corrections here motivate, and publish their receipts (Table 2).

**D5. The agents' record.** Replay corrected six initial accounts, and wording review corrected this
paper's first draft, so the record documents the auditors' errors as well as the infrastructure's. The
same source comparison and known-answer checks could serve other fields built on community databases and
shared code, such as biodiversity informatics. We offer that as a proposal for future work. [to source: one
biodiversity-informatics data-quality paper, as motivation only]

**D6. Limitations.** The cases were selected for consequence, so they describe kinds of finding, not their
frequency. We replayed published calculations and part of one deposited model, not whole downstream
studies. Checks vary in independence, some share inputs or model family, and the calibration controls rest
on two simulated clades with one failed agreement gate. Some inputs are held locally, a cold public rebuild
is untested, and providers and authors had not been contacted at the time of writing.

**C1. Conclusions.** AI agents can systematically check the databases and software behind fossil-record
research, and they found verifiable errors and pitfalls that researchers need to know about. Future work
could audit a defined population of dependencies, compare agent and human auditors, and replay downstream
studies. Each step would turn this case series into estimates.

## Citations still to source before 3c

The list is also in the paragraph comments above:
- a PBDB overview or data-access reference;
- a time-scale reference (GTS2020);
- a recent sampling-standardization review;
- two or three agentic-AI-in-research papers;
- the admtools and fossilbrush papers;
- Fossil Record 2 (Benton 1993);
- Robson & Whitlock 1964;
- PALEOMAP;
- Torsvik & Cocks 2017;
- a paleolatitude-uncertainty study;
- an extinction-time estimation review;
- a data-versioning or download-citation reference;
- one biodiversity-informatics data-quality paper.

These suit a References-lane source check: identities from DOI metadata, and passage locations for each
use.
