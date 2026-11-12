# AI agents as auditors of paleobiology's shared infrastructure: twelve verified cases

<!-- Step 3c (full draft), 12 November 2026, expanded from 3b-paragraph-abstracts.md at 1305cd8.
Written in manuscript syntax: claim spans [value]{.Cnnn} and citations [@key] check against
manuscript/claims.csv and references/refs.yaml. Bracketed [check: …] marks a fact to confirm before
porting this draft into manuscript/text/main.md. American spelling. -->

<div id="authors"></div>

## Abstract

Large-scale paleobiology depends on shared databases, data deposits, time scales, plate models and
analysis packages, so errors or misreadings there pass directly into inference. In a research program run
by two AI agents with a human facilitator, the agents checked this layer by re-running data
transformations, software and published calculations against known answers and their own sources. We
report twelve cases, each replayed from pinned inputs and checked by a second agent. They include
deposited records absent from a dated public database snapshot, interval ages that change between
database versions, defects in age–depth conversion and data-cleaning software, simulated preservation-rate
intervals that miss the true value too often, plate models that disagree on paleolatitude by a median of
[2.9]{.C125}–[13.6]{.C125}°, and a printed probability of $3.4 \times 10^{-16}$ that its stated test puts
at [0.32]{.C190}. Review corrected the initial accounts of six cases. Each finding gives researchers a
specific, verifiable action.

## Non-technical summary

Studies of the fossil record increasingly rest on shared resources: large online databases of fossil
finds, data files published with papers, geological time scales, maps of how continents have moved, and
software that estimates rates and ages. If one of these resources contains an error, or reports something
different from what its users assume, every study that relies on it inherits the problem. We used two AI
systems to check these resources while they built a research program, and we report twelve problems they
found and confirmed. Each comes with the evidence and commands needed to check it, and with a practical
step that researchers, database maintainers or journals can take.

## Introduction

A diversity curve, an extinction rate or a paleolatitudinal gradient is the end of a long chain. Fossils
become occurrence records in databases such as the Paleobiology Database (PBDB) and in data deposits
published with papers; records are placed in time by a geologic time scale and age models, placed in
space by plate reconstructions, and turned into estimates by analysis packages
[@peters2016PaleobiologyDatabaseApplication; @gradstein2020GeologicTimeScale]. Global diversity studies
show how such a chain is assembled, from database occurrences through explicit choices about
preservation, sampling and analysis [@alroy2008PhanerozoicTrendsGlobal]. Each link is maintained by others
and changes over time.

Paleobiology has a long literature on how the rock record distorts inference through sampling,
preservation and the availability of rock [@raup1972TaxonomicDiversityPhanerozoic;
@smith2001LargescaleHeterogeneityFossil; @dillon2023ChallengesDirectionsAnalytical]. The shared
infrastructure adds a second set of dependencies, of four kinds: the data transformations that turn
sources into products, the software that implements each calculation, the models chosen where several
are defensible, and the meaning of what each tool reports. These dependencies sit between the rocks and
the result in every large-scale analysis.

The community has named parts of this layer as priorities. Among 89 "Big Questions" in paleontology are
questions on finding and correcting data-entry bias, recovering lost historical information, reporting,
and integrating data (AFR2–AFR4, FI1) [@smith2025IdentifyingBigQuestions]. Guidance on computational
reproducibility recommends tracking how every result was produced, preserving versions and inspecting
intermediate results [@sandve2013TenSimpleRules]. Together they call for the checking this layer needs.

Checking the layer means comparing data with their sources, running software against known answers,
inspecting code and recomputing published numbers. The work is broad and detailed. In the program we
report here, two AI agents carried out the checks, recording the evidence, command and input hashes for
each. A benchmark of agents reproducing the computations of published papers is the nearest precedent
[@siegel2024CorebenchFosteringCredibility].

We report twelve findings from two agents building a paleobiology research program in October and
November 2026, organized by three questions: where each finding arose, what checks established it, and
what changed when a second agent re-examined it. Each case comes with the evidence and command needed to
verify it, and with actions for researchers, maintainers, journals and programs that use AI agents.

## Methods

### Setting

The Extinction and Paleontology Research Programme (EPRP) began in October 2026. It is run by two AI
agents, Anthropic's Claude and OpenAI's Codex, with a human facilitator (B.W.B.) who set direction and
held every external decision, including contact with data providers and authors, release and submission.
The agents worked in a public repository and coordinated through a written correspondence board. Their
contributions are disclosed by system, version and task in the Roles section.

### How candidate findings arose

The program's first task was to vet research questions against the data and software that could answer
them. In doing so, the agents:

- mirrored databases, data deposits and plate models, recording a SHA-256 checksum for every file on
  arrival and querying the PBDB through its public interface [@peters2016PaleobiologyDatabaseApplication];
- benchmarked analysis packages against simulations with known answers, through validation tests declared
  before they were run, with dated amendments and recorded deviations, and through exploratory follow-up
  probes;
- recomputed numbers printed in published papers from their stated inputs and methods.

Three working sessions, for databases, packages and references, logged each finding with its evidence
location and the checks it had received. The resulting catalogue held 189 initial candidate findings,
including positive controls and intended behaviors as well as suspected problems; later findings were
added as the program continued.

### Selection and coding

On 8 November 2026 we selected twelve cases from the catalogue and later findings. The criteria were
consequence for inference (what the finding would change in an analysis someone plausibly runs), variety
of finding, and inclusion of positive controls. Licensing problems, bibliographic metadata and findings
involving sensitive location data were excluded. The selection record, with reserves, is in Supplement S1.

On 12 November each case was coded by the dependency it checked, using four kinds defined by the observed
relation:

- **data transformation:** records or values differ between a source and a product derived from it;
- **implementation:** a computed output differs from its stated operation applied to its stated inputs;
- **model choice:** defensible alternative models give different answers for the same inputs;
- **output meaning:** a test against known truth establishes what uncertainty or quantity a reported
  output represents.

Each case received one primary kind and, where needed, a secondary kind (Table 1). How each finding was
first discovered was taken from dated records in the correspondence and catalogue.

### Replay and checks

On 8 November 2026 each case was replayed from pinned inputs by an agent other than its original finder
[check: confirm the finder and replaying actor for cases 11 and 12]. Where possible, key numbers were
rederived by a separate route: independent aggregation, interpolation, geometry or scoring code, recounts
from raw files, or closed-form arithmetic. Each verified proposition entered a claims ledger with its
value, evidence files, the commit at which the evidence was verified, a command that reproduces it, and a
statement of its scope. The ledger holds 22 propositions, and every number reported below is tagged to
one of them.

### Review and record

A wording review then checked every draft sentence against an interpretation specification stating what
each case establishes and which phrasings it supports. Corrections at each stage were logged with who
found them and what replaced them (Supplement S3). Versions, environments and input hashes accompany each
replay in the program's public repository, and reviewed snapshots of the correspondence are published
there. A tagged snapshot will be archived with a DOI at release.

## Results

### Overview

The twelve cases cover all four kinds of dependency (Table 1): five data transformations, four
implementations, two cases of output meaning and one model choice, with GRIWM also coded as an
implementation. They sit along the whole chain from deposit to published number (Fig. 1A). Each rests on a
replay from pinned inputs and a second agent's check (Fig. 1B). We present them by resource, as a reader
meets them; Table 1 gives the formal codes.

### The Paleobiology Database

A published global analysis of marine latitudinal diversity [@benson2025MarineAnimalDiversity] deposited
its occurrence data. Of the [368,760]{.C191} occurrences in the deposit's molluscan member,
[71,103]{.C191} were absent from a public PBDB snapshot taken on 23 October 2026, and [297,657]{.C191}
were present (Fig. 2A). The difference matters for analysis. A presence screen we used to test for
tropical support outside Europe and North America passed in [14]{.C192} of [21]{.C192} stages with the
full deposit and in [12]{.C192} with snapshot members only (Table 1). We report these records as counts.

Archived PBDB query products show interval ages changing between snapshots. Across three bracketed
snapshot pairs, [460]{.C076}, [317]{.C076} and [17]{.C076} intervals changed their modal base age,
counting intervals with at least 50 single-interval occurrences in the later snapshot (Fig. 2B); requiring
the threshold in both snapshots changes the middle count to [316]{.C076}. The database documents base and
top ages, in Ma, as fields of each interval record [@peters2016PaleobiologyDatabaseApplication]
[check: cite PBDB Data Service 1.2 interval documentation with access date]. A query repeated on
different dates can therefore return different ages for the same interval, and recording the date and
version of each query makes that change visible.

### Microfossil databases

The 2023 update of the Triton planktonic foraminifera database [@fenton2021TritonSpecieslevelDatabase]
contains [28,832]{.C043} excess rows under the key we specified (Supplement S2). A conservative recipe removes lower-priority-source rows from
cross-source groups with recorded depth and retains every row from the highest-priority source; it
removes [16,260]{.C043} rows. We measured the consequence in one of our own analyses. Rebuilding the
program's paleolatitudinal exposure index with and without the removal changed [1,388]{.C045} of
[2,267]{.C045} comparable lineage-bin mean absolute paleolatitudes (Fig. 2C). [411]{.C045} of those
changes were at least one degree, and lineage-pair classifications changed in [8]{.C045}, [8]{.C045},
[2]{.C045} and [1]{.C045} of 491 pairs under four classification rules.

The final Neptune Sandbox Berlin (NSB) database [@renaudie2020NsbNeptuneSandbox] holds [61,862]{.C040}
samples with stored ages and, for each drill hole, a set of depth–age tie points. We recomputed each
sample's age by linear interpolation between its hole's tie points, taking the first age where two tie
points share a depth. [56,387]{.C040} samples have both a stored and a recomputed age, and
[4,111]{.C040} of these, in [56]{.C040} holes, differ by more than 0.01 Myr (Fig. 2D). Taking the last
age at shared depths instead removes [8]{.C040} of the differences. A user who takes the stored ages and
one who recomputes from the tie points work from different numbers.

### Analysis packages

admtools converts stratigraphic height to time through an age–depth model
[@hohmann2025NonparametricEstimationAgedepth; @hohmann2023AdmtoolsEstimateManipulate]. We tested version
0.7.0 on a synthetic model with two hiatuses, against exact linear-segment truth. With sparse tie points,
it mis-converted [3,972]{.C096} of [8,282]{.C096} heights, by up to [3.0]{.C096} Myr (Fig. 3A). With
dense tie points, [6]{.C096} of the same heights were mis-converted, by up to [0.466]{.C096} Myr, and a
targeted probe near a hiatus gave an error of about [2.7]{.C096} Myr. The errors lie in the interpolation
segments adjoining the hiatuses.

fossilbrush flags occurrences whose ages fall outside a reference range by more than a threshold in Myr
[@flannerysutherland2022FossilbrushRPackage; @flannery-sutherland2022FossilbrushAutomatedCleaning].
Version 1.0.6 compared those differences with the threshold as text. At the default threshold of
[5]{.C102}, it passed differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and
[499]{.C102} unflagged while flagging 50 and 99, and character order predicted every decision on the test
grid (Fig. 3B).

GRIWM estimates extinction time from dated records [@bradshaw2012RobustEstimatesExtinction]. The
implementation in Rextinct 1.1.0 overwrote the caller's random-number state: after a call, the calling
program's random stream was the same whatever seed it had set beforehand. Any analysis that draws random
numbers after calling it continues from a stream set by the package.

### Published products

Four published products differed from their sources or stated tests:

- **Capture histories.** A study of extinction selectivity [@monarrez2023ReducedStrengthIncreased]
  deposited its capture histories both as an intact binary file and in a spreadsheet. [2,967]{.C035} of
  [6,562]{.C035} spreadsheet histories differed numerically from the binary deposit. A further
  [3,595]{.C035} are restored exactly by padding to the known width of [86]{.C035} characters.
- **Fossil Record 2.** The one-file All-Life table of the digital Fossil Record 2 compilation
  [@benton1993FossilRecord2] held [220]{.C048} rows with cell tails shifted one column left relative to
  its chapter workbooks: [112]{.C048} shift ranges, [2]{.C048} shift habitat and range, and [106]{.C048}
  move a not-found-in-record flag into the Holocene column.
- **A printed probability.** An analysis of cyclicity in stratigraphic boundaries
  [@rampino2025CorrelationCyclicityStratigraphic] states a binomial test with n = [47]{.C190}, k =
  [28]{.C190} and p = [0.55]{.C190} and prints a tail probability of $3.4 \times 10^{-16}$. The stated
  test gives [0.316]{.C190}, confirmed by exact rational arithmetic, integer polynomial convolution, a
  direct exact sum and R.
- **Archived calibration scores.** INDITEK-2.0 [@herrerogascon2026Inditek20] deposits a synthetic
  demonstration with archived calibration proposals. Three rejected proposals, rerun through the pinned
  harness, reproduced their prediction vectors to within about $5 \times 10^{-14}$ across
  [2,978]{.C195} cells. Their saved residual sums of squares differed from rescoring under the deposited
  observations by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193}, and a separately written, model-free
  scorer agreed with the rescored values.

### Model choices and output meaning

We simulated fossil records under a declared constant-rate, homogeneous-Poisson design and asked how often
PyRate's [@silvestro2014PyrateProgramEstimate] 95% intervals for the preservation rate covered the true
value. They covered it in [81]{.C107} of [100]{.C107} replicates in one arm and [33]{.C107} of
[50]{.C107} in a lower-preservation arm (Fig. 3C). Posterior medians sat above the truth, with median
relative bias [0.0895]{.C107} and [0.458]{.C107}, and every miss fell below the lower endpoint: the
intervals were shifted high.

The same benchmark carried positive controls for a different target, the range-end bounds of retained
species in two simulated clades. Under homogeneous sampling, the classical Strauss–Sadler bound
[@strauss1989ClassicalConfidenceIntervals] covered the truth in [1,895]{.C194} and [1,899]{.C194} of
[2,000]{.C194} cases in two implementations, and the Robson–Whitlock bound
[@robson1964EstimationTruncationPoint], as implemented in EDE 0.2.0, in [1,909]{.C194} (Fig. 3C). The
simulation generators matched their analytic moments [check: cite C105 here or in Supplement only]. In a
hiatus arm, Strauss–Sadler coverage fell to [1,125]{.C111} of [1,272]{.C111} retained cases.

The interval GRIWM reports in Rextinct 1.1.0 comes from resampling the input dating errors: with zero
dating error it collapses to a point. It therefore measures how sensitive the estimated extinction time is
to uncertain dates, conditional on the records [@bradshaw2012RobustEstimatesExtinction].

We reconstructed [300]{.C125} public occurrence points at six ages in three plate models: MERDITH2021
[@merdith2021ExtendingFullplateTectonic], PALEOMAP [@scotese2016PaleomapPaleoatlasGplates] and
MATTHEWS2016_pmag_ref [@matthews2016GlobalPlateBoundary]. Taken over the points reconstructable in all
three models at each age, the median spread in paleolatitude was [2.9]{.C125}° at 10 Ma, [5.7]{.C125}° at
50 Ma, [4.3]{.C125}° at 100 Ma, [5.5]{.C125}° at 200 Ma, [4.7]{.C125}° at 300 Ma and [13.6]{.C125}° at
400 Ma (Fig. 3D); [194]{.C125} points are reconstructable at every age. Two routes to the
TorsvikCocks2017 model [@torsvik2016EarthHistoryPalaeogeography] differed by an approximately rigid,
age-specific rotation, consistent with different reference frames; the model's authors distinguish a
hybrid mantle frame from a paleomagnetic frame (Supplement S2).

### Checks and review

Each finding rests on its own mix of re-execution, recomputation from source, code inspection and
arithmetic (Table 1). INDITEK's case, for example, combined a forward replay through the original harness
with separately written rescoring; the printed probability was confirmed four ways. Replay corrected the
initial accounts of six cases (Table 1; Supplement S3). The PyRate account moved from "intervals too
narrow" to "intervals shifted high"; the admtools account moved from errors "above every hiatus" to
errors in the adjoining segments; the Triton counts of changed means were recomputed under the pinned
recipe; the PBDB records described as "withheld" became records absent from a dated snapshot; a count of
spreadsheet cells in scientific notation was separated from the count of altered histories; and the NSB
sample count was corrected for a header row.

## Discussion

The twelve cases show AI agents checking all four kinds of dependency between rocks and results across
one research program. Each case changes what a researcher should record, test or interpret, and each
check is documented with its evidence, pinned inputs and command. The findings are specific to named
versions of named resources, which is what makes them actionable: a maintainer can reproduce each one,
and a user can test whether it touches their own analysis.

### Comparison with a source

Where a source or known answer is specified, a direct comparison establishes a discrepancy: in the records
present, interval ages, row counts, conversions, flags or published numbers. Such a check needs the query
date, the version and the intermediate products, so recording them lets a researcher test inputs before
any biological model is fitted [@sandve2013TenSimpleRules]. GBIF builds this into its downloads: each records its query predicate and receives a DOI that identifies the extract
[@gbif2026ApiDownloads; @gbif2026Citation]. Locating a discrepancy and explaining its cause are separate
steps. INDITEK's score mismatch is located, and its cause is open; the deposited-record absences are
counted, and their cause is for the database maintainers to establish.

### Model sensitivity and interval meaning

The three tested plate models placed the same points degrees apart, so an analysis whose result depends on
paleolatitude should state its model and cohort and report the spread among alternatives. Published
paleolatitude tools propagate uncertainty in paleomagnetic poles and age, and treat the choice of
reference frame as a separate decision [@vanhinsbergen2015PaleolatitudeCalculatorPaleoclimate]; the
spread we measured belongs to that second category. An interval needs two other judgments: which
uncertainty process it propagates, and how often it covers the truth. GRIWM's interval propagates dating
error, and PyRate's preservation-rate intervals covered the truth less often than nominal in simulation.
Both kinds of finding change how a result is read.

### Actions

Table 2 maps the findings onto actions for four audiences. Users can record query dates and versions,
compare plate models and replay published numbers before reuse. Maintainers can version changes, test
against known truth at boundary cases such as hiatuses, compare numbers as numbers, leave the caller's
random-number state intact and document what each output measures. Journals and depositors can require
machine-readable deposits and archive scoring code and observations with any saved scores. Programs that
use AI agents can pair each finding with a second check, as the corrections here motivate, and publish
their receipts.

### The agents' own record

Replay corrected six initial accounts, and wording review corrected this paper's first draft, which had
joined a count from one admtools control with the maximum from another and attributed the INDITEK archive
to the wrong paper (Supplement S3). The record therefore documents the auditors' errors alongside the
infrastructure's; each correction was found during replay or wording review. The same source
comparison and known-answer checks could serve other fields built on community databases and shared code.
Biodiversity informatics is one: name and coordinate validation against reference distributions has long
been part of its data-quality practice [@yesson2007HowGlobalGlobal]. We offer that application as a
proposal.

### Limitations

- **Selection.** The cases were selected for consequence, so they describe kinds of finding, not their
  frequency in the infrastructure.
- **Downstream scope.** We replayed published calculations and part of one deposited model, not whole
  downstream studies; measured consequences are to support counts, inputs and our own analyses.
- **Independence.** Checks vary in independence. The INDITEK forward run reused the original harness, and
  some checks shared inputs or model family.
- **Calibration controls.** These rest on two simulated clades. One declared agreement gate failed: it
  required 99% of paired range-end bounds to agree within [0.02]{.C196} Myr, and [0.91]{.C196} did. The
  executed hiatus windows were shifted one Myr from the declared design.
- **Causes and status.** The causes of the PBDB absences, the NSB disagreements and the INDITEK score
  mismatch are unresolved. Neither the stored nor the recomputed NSB ages are certified, and the plate-model
  spread is structural disagreement among models, not calibrated error.
- **Reproduction.** Some inputs (container images, posterior logs, source archives) are held locally, and
  a cold rebuild from public inputs alone is untested.
- **Disclosure.** Providers and authors had not been contacted at the time of writing, and whether they
  already knew of a finding is unresolved.

## Conclusions

AI agents can systematically check the databases and software behind fossil-record research, and they
found verifiable errors and pitfalls that researchers need to know about. Three studies would extend this
case series, each with its own payoff. An audit of a defined population of dependencies would estimate how
often such findings occur; a matched comparison of agent and human auditors would measure their relative
performance; and replay of downstream studies would test what particular findings change.

## Tables

**Table 1.** The twelve cases. Kinds: DT, data transformation; IM, implementation; MC, model choice; OM,
output meaning; primary kind first. Review: what replay changed in the initial account. [check: add the
discovery-route column from dated records, as planned in step 1d.]

| # | Resource | Kind | Check | Result | Review | Claims |
|--|------|----|----------|----------|------|-----|
| 1 | Published PBDB deposit | DT | Identifier comparison with a dated snapshot | [71,103]{.C191} of [368,760]{.C191} absent; screen passes [14]{.C192} → [12]{.C192} of 21 stages | "withheld" → absent from a dated snapshot | C191, C192 |
| 2 | PBDB interval ages | DT | Recount from archived query products | [460]{.C076}, [317]{.C076}, [17]{.C076} changed modal base ages | — | C076 |
| 3 | Triton 2023 update | DT | Key grouping; rebuild with and without removal | [1,388]{.C045} of [2,267]{.C045} means changed | counts recomputed | C043, C045 |
| 4 | NSB stored ages | DT | Interpolation from tie points | [4,111]{.C040} of [56,387]{.C040} differ > 0.01 Myr | header row removed | C040 |
| 5 | admtools 0.7.0 | IM | Exact linear-segment truth | [3,972]{.C096} of [8,282]{.C096} heights mis-converted | "every hiatus" → adjoining segments | C096 |
| 6 | fossilbrush 1.0.6 | IM | Deterministic grid; numeric truth vs text order | differences of [10]{.C102}–[499]{.C102} pass a threshold of [5]{.C102} | — | C102 |
| 7 | PyRate preservation rates | OM | Simulation coverage, with positive controls | [81]{.C107}/[100]{.C107} and [33]{.C107}/[50]{.C107} covered | "too narrow" → shifted high | C107, C194, C196, C105, C111 |
| 8 | GRIWM, Rextinct 1.1.0 | OM, IM | Zero-error control; weighted-prefix formula; seed sentinels | interval reflects dating error; caller RNG overwritten | — | C110, C098 |
| 9 | Three plate models | MC | Reconstruction of shared points; geometry of two routes | median spread [2.9]{.C125}–[13.6]{.C125}° | — | C125, C123 |
| 10 | Published spreadsheets | DT | Comparison with intact binary and chapter workbooks | [2,967]{.C035} of [6,562]{.C035} histories; [220]{.C048} shifted rows | cell count separated from history count | C035, C048 |
| 11 | Printed probability | IM | Exact arithmetic, four ways | [0.316]{.C190} against $3.4 \times 10^{-16}$ | — | C190 |
| 12 | INDITEK-2.0 scores | IM | Forward replay; separately written rescoring | saved scores off by up to [42.4]{.C193} | — | C195, C193 |

**Table 2.** Recommended actions, by audience.

| Audience | Actions | Cases |
|------|------------------------|----|
| Users | Record query dates and versions; check deposited records against the snapshot used; compare plate models and state the reference frame; replay a published number before building on it | 1, 2, 9, 11 |
| Database maintainers | Version interval ages and records, with change logs; document how stored values derive from their sources | 1–4 |
| Package maintainers | Test against known truth at boundary cases; compare numbers as numbers; leave the caller's random-number state intact; document what each interval measures | 5–8 |
| Journals and depositors | Require machine-readable deposits; archive scoring code and observations with saved scores | 10–12 |
| Programs using AI agents | Pair each finding with a second check; declare tests before running them and keep failed gates; publish receipts and reviewed correspondence | all |

## Figure captions

**Figure 1.** (A) The selected cases along the path from rocks to a published result, colored by primary
kind. (B) The audit workflow: 189 initial candidate findings and later additions, twelve selected cases,
replay from pinned inputs, a second check and 22 supported propositions; cases whose initial accounts
replay corrected are marked.

**Figure 2.** Findings in data transformations. (A) Deposited molluscan occurrences present in and absent
from the PBDB snapshot of 23 October 2026. (B) Intervals with a changed modal base age in each snapshot
pair. (C) Change in each lineage-bin mean absolute paleolatitude when excess Triton rows are removed.
(D) Stored minus interpolated NSB sample ages, with ±0.01 Myr marked.

**Figure 3.** Findings in implementations, model choices and output meaning. (A) admtools time error
against height in the sparse synthetic model, with hiatuses marked. (B) fossilbrush flag decisions
against numeric truth and text order. (C) Observed coverage against the 95% nominal line for PyRate
preservation-rate intervals and for range-end bounds. (D) Median paleolatitude spread among three plate
models by age.

## Roles of AI systems and humans

- **Codex (OpenAI)**, with GPT-6.1 Sol delegates, took over the program's database, reference and
  package work from 28 October 2026; made original findings including cases 11 and 12; replayed all
  twelve cases; built the claims ledger; reviewed this paper's wording and reconstruction; and checked
  its cited sources.
- **Claude (Anthropic)**, Opus 5.5 in the main session with Sonnet subagents, ran the database, package and
  reference sessions that made most original findings before 28 October; compiled the 189-row catalogue;
  selected the twelve cases; wrote the interpretation specification; and drafted this paper.
- **Barry W. Brook** facilitated the program, approved this paper on 25 October 2026, chose the case
  series for development on 8 November 2026, and holds decisions on contact, submission and release.

The figures' plotting code was written by AI systems; each caption will state this when the figures are
drawn. [check: Paleobiology byline and disclosure placement; acknowledgments, funding and competing
interests to be supplied by B.W.B.]

## Data availability

The repository is public at <https://github.com/BWBrook/eprp>; code is MIT-licensed, and text, figures and
data are CC BY-SA 4.0. The claims ledger (`papers/infrastructure-audit/manuscript/claims.csv`) gives each
proposition's evidence files, verifying commit and reproduce command. Third-party sources keep their own
licenses. Records absent from public database snapshots are reported as counts only.

## References
