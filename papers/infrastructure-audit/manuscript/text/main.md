# AI agents as auditors of paleobiology's shared infrastructure: twelve verified cases

<div id="authors"></div>

## Non-technical Summary

Studies of the fossil record rest on shared resources: online databases of fossil finds, data files
published with papers, geological time scales, maps of past continents, and software that estimates
rates and ages. An error in one of these resources, or a result that means something different from what
its users assume, can carry into the studies that rely on it. While building a research program, two AI
systems checked these resources against their sources and against known answers. We report twelve
findings they made and confirmed. Each comes with the evidence needed to check it and a practical step
that researchers, database maintainers or journals can take.

## Abstract

Large-scale paleobiology depends on shared databases, data deposits, time scales, plate models and
analysis packages, so errors or misreadings there can affect the analyses built on them. In a research
program run by two AI agents with a human facilitator, the agents checked this layer by re-running data
transformations, software and published calculations against known answers and their own sources. We
report twelve cases, each rerun from fixed, checksummed inputs and checked by a second agent. They include
deposited records absent from a dated public database snapshot, interval ages that change between
database versions, defects in age–depth conversion and data-cleaning software, simulated preservation-rate
intervals that miss the true value too often, plate models that disagree on paleolatitude by a median of
[2.9]{.C125}–[13.6]{.C125}°, and a printed probability of $3.4 \times 10^{-16}$ that its stated test puts
at [0.32]{.C190}. Review corrected the initial accounts of six cases. AI agents can audit this shared
layer systematically, and each finding gives researchers a specific, verifiable action.

## Introduction

A diversity curve, an extinction rate or a paleolatitudinal gradient is the last link in a long chain.
Fossils become occurrence records in databases such as the Paleobiology Database (PBDB) and in data
deposits published with papers. A geologic time scale and age models place the records in time, plate
reconstructions place them in space, and analysis packages turn them into estimates
[@peters2016PaleobiologyDatabaseApplication; @gradstein2020GeologicTimeScale]. Global diversity studies
show how such a chain is assembled, from database occurrences through explicit choices about
preservation, sampling and analysis [@alroy2008PhanerozoicTrendsGlobal]. Each link is maintained by
others, and each changes over time.

Paleobiologists have long studied how the rock record distorts inference through sampling, preservation
and the availability of rock [@smith2001LargescaleHeterogeneityFossil;
@dillon2023ChallengesDirectionsAnalytical]. The shared infrastructure adds a second set of dependencies,
of four kinds: the transformations that turn sources into data products, the software that implements
each calculation, the models chosen where several are defensible, and the meaning of what each tool
reports. These dependencies lie between the rocks and the result in every large-scale analysis.

The community has named parts of this layer as priorities. Among 89 "Big Questions" in paleontology are
questions on finding and correcting data-entry bias, recovering lost historical information, reporting,
and integrating data (AFR2–AFR4, FI1) [@smith2025IdentifyingBigQuestions]. Guidance on computational
reproducibility asks researchers to record how each result was produced, keep versions and inspect
intermediate results [@sandve2013TenSimpleRules].

Checking the layer means comparing data with their sources, running software against known answers,
inspecting code and recomputing published numbers. The work is broad and exacting. In this program,
two AI agents did it and recorded the evidence, command and input hashes for each check. A benchmark of agents reproducing the computations of published
papers is a relevant precedent [@siegel2024CorebenchFosteringCredibility].

Here we report twelve findings made by two AI agents while they built a paleobiology research program
in October and November 2026. Three questions organize them: where each finding arose, what checks
established it, and what changed when a second agent re-examined it. The cases show agents auditing the
shared layer at the scale of a whole program, with findings specific enough for researchers,
maintainers, journals and other agent-based programs to act on.

## Methods

### Setting

The Extinction and Paleontology Research Programme (EPRP) began in October 2026. Two AI agents,
Anthropic's Claude and OpenAI's Codex, run it with a human facilitator (B.W.B.), who sets direction and
holds every external decision, including contact with data providers and authors, release and
submission. The agents work in a public repository and coordinate through a written correspondence
board. Their contributions are listed by system, version and task under Roles of AI Systems.

### How Candidate Findings Arose

The program's first task was to vet research questions against the data and software that could answer
them. To do so, the agents:

- mirrored databases, data deposits and plate models, recording a SHA-256 checksum for every file on
  arrival, and queried the PBDB through its public interface [@peters2016PaleobiologyDatabaseApplication];
- benchmarked analysis packages against simulations with known answers, in validation tests declared
  before they were run (with dated amendments and recorded deviations) and in exploratory follow-up
  probes;
- recomputed numbers printed in published papers from their stated inputs and methods.

Three working sessions, for databases, packages and references, logged each finding with its evidence
and the checks it had received. The resulting catalogue held 189 initial candidate findings, including
positive controls and intended behaviors; later findings joined as the program continued.

### Selection and Coding

On 8 November 2026 we selected twelve cases for their consequence for inference (what each would change
in an analysis someone plausibly runs), their variety, and the inclusion of positive controls. Licensing
problems, bibliographic metadata and findings involving sensitive location data were excluded.
Supplement S1 gives the selection record and its reserves.

On 12 November we coded each case by the family of check that established it. The four families follow
the four kinds of dependency and are defined by what was compared:

- **data provenance and transformation (DP):** membership or values compared across identified sources,
  versions or derived products;
- **computation and implementation (CI):** retained or published numbers compared with a specified
  calculation under identified reference inputs;
- **model sensitivity (MS):** named alternative models compared on shared inputs;
- **output interpretation and calibration (OI):** the quantity or uncertainty process a reported output
  targets, and its operating characteristics in a stated test design.

Each case has one primary family and, where needed, a secondary one. Its discovery route comes from dated
records in the repository and correspondence (Table 1).

### Replay and Checks

On 8 November 2026 Codex's replay team (the main Codex session and GPT-6.1 Sol subagents) replayed each
case from pinned inputs (the exact files used, identified by checksum), by fresh software calls, recalculation from source tables or
reaggregation of retained outputs. Cases 11 and 12 were first recorded by Codex's reference and package
sessions; their November checks added a complement recurrence and integer-polynomial convolution (case
11) and a separately written scorer (case 12). Where possible, key numbers were rederived by a separate
route: independent aggregation, interpolation, geometry or scoring code, recounts from raw files, or
closed-form arithmetic. Each verified proposition entered a claims ledger with its value, evidence files,
verifying commit, reproduce command and scope. The ledger holds 22 propositions, and every number in the
Results is tagged to one of them.

### Review and Record

A wording review checked every draft sentence against an interpretation specification that states what
each case establishes. Corrections at each stage were logged with their finder and replacement
(Supplement S3). Versions, environments and input hashes accompany each replay in the public repository,
together with reviewed snapshots of the correspondence. A tagged snapshot will be archived with a DOI at
release.

## Results

### Overview

The agents' checks reached links all along the chain, from deposit to published number (Fig. 1A), and
made findings in each of the four families (Table 1): five cases of data provenance and
transformation, four of computation and implementation, two of output interpretation and calibration,
and one of model sensitivity. The GRIWM case also carries a computation finding. Every case was replayed
from pinned inputs and checked a second time (Fig. 1B). We present the cases by resource, as a reader
meets them.

### The Paleobiology Database

A published global analysis of marine latitudinal diversity [@benson2025MarineAnimalDiversity] deposited
its occurrence data. Of the [368,760]{.C191} occurrences in the deposit's molluscan member,
[71,103]{.C191} were absent from a public PBDB snapshot taken on 23 October 2026, and [297,657]{.C191}
were present (Fig. 2A). The difference reached our own analysis: a presence screen for tropical support
outside Europe and North America passed in [14]{.C192} of [21]{.C192} stages with the full deposit and
in [12]{.C192} with snapshot members only. We report these records as counts.

Archived PBDB query products show interval ages changing between snapshots. Across three bracketed
snapshot pairs, [460]{.C076}, [317]{.C076} and [17]{.C076} intervals changed their modal base age (the
most common base age among their records),
counting intervals with at least 50 single-interval occurrences in the later snapshot (Fig. 2B);
applying the threshold to both snapshots changes the middle count to [316]{.C076}. The database serves
base and top ages, in Ma, as fields of each interval record [@pbdb2026IntervalsList], so the same query
run on different dates can return different ages for the same interval. Recording the date and version
of each query makes the change visible.

### Microfossil Databases

The 2023 update of the Triton planktonic foraminifera database [@fenton2021TritonSpecieslevelDatabase]
contains [28,832]{.C043} excess rows under the key we specified (Supplement S2). A conservative recipe
removes lower-priority-source rows from cross-source groups with recorded depth, keeping every row from
the highest-priority source; it removes [16,260]{.C043} rows. One of our own analyses averages each
lineage's absolute paleolatitude within each time bin; the removal changed [1,388]{.C045} of
[2,267]{.C045} comparable means (Fig. 2C), [411]{.C045} of them by at least one degree. Lineage-pair classifications
changed in [8]{.C045}, [8]{.C045}, [2]{.C045} and [1]{.C045} of 491 pairs under four classification
rules.

The final Neptune Sandbox Berlin (NSB) database [@renaudie2020NsbNeptuneSandbox] contains
[61,862]{.C040} sample records and, for each drill hole, a set of depth–age tie points. We recomputed
each sample's age by linear interpolation between its hole's tie points, taking the first age where two
tie points share a depth. Of [56,387]{.C040} samples with both a stored and a recomputed age,
[4,111]{.C040}, in [56]{.C040} holes, differ by more than 0.01 Myr (Fig. 2D). Taking the last age at
shared depths instead removes [8]{.C040} of these differences. A user who takes the stored ages and one
who recomputes them from the tie points work from different numbers.

### Analysis Packages

admtools converts stratigraphic height to time through an age–depth model
[@hohmann2025NonparametricEstimationAgedepth; @hohmann2023AdmtoolsEstimateManipulate]. We tested
version 0.7.0 on a synthetic model with two hiatuses, against exact linear-segment truth. With sparse tie
points, it mis-converted [3,972]{.C096} of [8,282]{.C096} heights, by up to [3.0]{.C096} Myr (Fig. 3A).
With dense tie points, it mis-converted [6]{.C096} of the same heights, by up to [0.466]{.C096} Myr, and
a targeted probe near a hiatus gave an error of about [2.7]{.C096} Myr. The errors lie in the
interpolation segments adjoining the hiatuses.

fossilbrush flags occurrences whose ages fall outside a reference range by at least a threshold in Myr
[@flannerysutherland2022FossilbrushRPackage; @flannery-sutherland2022FossilbrushAutomatedCleaning].
Version 1.0.6 compared those differences with the threshold as text. At the default threshold of
[5]{.C102}, it left differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and
[499]{.C102} unflagged while flagging 50 and 99; character order predicted every decision on the test
grid (Fig. 3B).

The Gaussian-resampled, inverse-weighted McInerny method (GRIWM) estimates extinction time from dated
records [@bradshaw2012RobustEstimatesExtinction]. Its
implementation in Rextinct 1.1.0 overwrote the caller's random-number state: after a call, the calling
program's random stream was the same whatever seed it had set beforehand. Any analysis that draws random
numbers after the call continues from a stream the package chose.

### Published Products

Four published products differed from their sources or stated tests.

- **Capture histories.** A study of extinction selectivity [@monarrez2023ReducedStrengthIncreased]
  deposited its capture histories (each genus's record of presence and absence through time) both as an
  intact binary file and in a spreadsheet. [2,967]{.C035} of
  the [6,562]{.C035} spreadsheet histories differed numerically from the binary deposit. A further
  [3,595]{.C035} are restored exactly by padding to the known width of [86]{.C035} characters.
- **Fossil Record 2.** The one-file All-Life table of the digital Fossil Record 2 compilation
  [@benton1993FossilRecord2] held [220]{.C048} rows whose cell tails were shifted one column left of
  their chapter workbooks: [112]{.C048} shift ranges, [2]{.C048} shift habitat and range, and
  [106]{.C048} move a not-found-in-record flag into the Holocene column.
- **A printed probability.** An analysis of cyclicity in stratigraphic boundaries
  [@rampino2025CorrelationCyclicityStratigraphic] states a binomial test with n = [47]{.C190}, k =
  [28]{.C190} and p = [0.55]{.C190} and prints a tail probability of $3.4 \times 10^{-16}$. The stated
  test gives [0.316]{.C190}, by exact rational arithmetic, integer-polynomial convolution, a direct exact
  sum and R.
- **Archived calibration scores.** INDITEK-2.0 [@herrerogascon2026Inditek20] deposits a synthetic
  demonstration with archived calibration proposals. Rerun through the pinned harness, three rejected
  proposals reproduced their prediction vectors to within about $5 \times 10^{-14}$ across
  [2,978]{.C195} cells. Their saved residual sums of squares differed from rescoring under the deposited
  observations by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193}, and a separately written, model-free
  scorer agreed with the rescored values.

### Model Choices and Output Meaning

We simulated fossil records under a declared constant-rate, homogeneous-Poisson design and asked how
often the 95% intervals for the preservation rate from PyRate, a Bayesian program for estimating
speciation, extinction and preservation rates [@silvestro2014PyrateProgramEstimate], covered the true
value. They covered it in [81]{.C107} of [100]{.C107} replicates in one
arm and [33]{.C107} of [50]{.C107} in a lower-preservation arm (Fig. 3C). Posterior medians sat above
the truth, with median relative bias of [0.0895]{.C107} and [0.458]{.C107}, and every miss fell below the
lower endpoint: the intervals were shifted high.

The same benchmark carried positive controls for a different target: confidence bounds on the true end
of each retained species' range, in two simulated clades. Under homogeneous sampling, the classical Strauss–Sadler bound
[@strauss1989ClassicalConfidenceIntervals] covered the truth in [1,895]{.C194} and [1,899]{.C194} of
[2,000]{.C194} cases in two implementations, and the Robson–Whitlock bound
[@robson1964EstimationTruncationPoint], as implemented in EDE 0.2.0, in [1,909]{.C194} (Fig. 3C). In a
hiatus arm, Strauss–Sadler coverage fell to [1,125]{.C111} of [1,272]{.C111} retained cases.

GRIWM's interval in Rextinct 1.1.0 comes from resampling the input dating errors, and with zero dating
error it collapses to a point. It therefore measures how sensitive the estimated extinction time is to
uncertain dates, given the records [@bradshaw2012RobustEstimatesExtinction].

We reconstructed [300]{.C125} public occurrence points at six ages in three plate models: MERDITH2021
[@merdith2021ExtendingFullplateTectonic], PALEOMAP [@scotese2016PaleomapPaleoatlasGplates] and
MATTHEWS2016_pmag_ref [@matthews2016GlobalPlateBoundary]. Over the points reconstructable in all three
models at each age, the median spread in paleolatitude was [2.9]{.C125}° at 10 Ma, [5.7]{.C125}° at
50 Ma, [4.3]{.C125}° at 100 Ma, [5.5]{.C125}° at 200 Ma, [4.7]{.C125}° at 300 Ma and [13.6]{.C125}° at
400 Ma (Fig. 3D); [194]{.C125} points are reconstructable at every age. Two routes to the
TorsvikCocks2017 model [@torsvik2016EarthHistoryPalaeogeography] differed by an approximately rigid,
age-specific rotation, consistent with a reference-frame difference (Supplement S2).

### Checks and Review

Each finding rests on its own mix of re-execution, recomputation from source, code inspection and
arithmetic (Table 1). The INDITEK case paired a forward replay through the original harness with
separately written rescoring; the printed probability was confirmed four ways. The recorded replay and
review trail corrected the initial accounts of six cases (Table 1; Supplement S3):

- PyRate's intervals moved from "too narrow" to "shifted high";
- admtools errors moved from "above every hiatus" to the adjoining segments;
- the Triton counts of changed means were recomputed under the pinned recipe;
- PBDB records described as "withheld" became records absent from a dated snapshot;
- a count of spreadsheet cells in scientific notation was separated from the count of altered histories;
- the NSB sample count was corrected for a header row.

## Discussion

Systematic checks by two AI agents turned up verifiable findings in all four kinds of dependency on which
large-scale paleobiology relies. Each case changes what a researcher should record, test
or interpret, and each comes with its evidence, pinned inputs and command. Because the findings concern
named versions of named resources, they are actionable: a maintainer has a specified check to run, and a
user can test whether a finding touches their own analysis.

### Comparison with a Source

Where a source or known answer is specified, a direct comparison establishes a discrepancy in the records
present, interval ages, row counts, conversions, flags or published numbers. The comparison needs the
query date, the version and the intermediate products, so recording them lets a researcher test inputs
before fitting any biological model [@sandve2013TenSimpleRules]. GBIF builds this into its downloads:
each records its query predicate and receives a DOI that identifies the extract
[@gbif2026ApiDownloads; @gbif2026Citation]. Locating a discrepancy and explaining its cause are separate
steps, and the first is what makes the second possible.

### Model Sensitivity and Interval Meaning

The three plate models placed the same points degrees apart, so an analysis whose result depends on
paleolatitude should state its model and cohort and report the spread among alternatives. Published
paleolatitude tools propagate uncertainty in paleomagnetic poles and ages, and treat the choice of
reference frame as a separate decision [@vanhinsbergen2015PaleolatitudeCalculatorPaleoclimate]; our
comparison measures sensitivity to the choice of reconstruction model. An interval calls for two further
judgments: which uncertainty process it propagates, and how often it covers the truth. GRIWM's interval
propagates dating error, and PyRate's preservation-rate intervals covered the truth less often than
nominal in simulation. Both kinds of finding change how a result should be read.

### Actions

Each finding points to a step that a specific audience can take (Table 2). Most are small changes to
existing practice, such as recording a query date, comparing numbers as numbers or archiving a scorer
with its scores.

### The Agents' Own Record

The audit applied to the auditors too. Replay corrected six initial accounts, and wording review
corrected this paper's first draft, which had joined a count from one admtools control with the maximum
from another and attributed the INDITEK archive to the wrong paper (Supplement S3). The same source
comparisons and known-answer checks could serve other fields built on community databases and shared
code. Biodiversity informatics is one: taxonomic checks and coordinate validation against reference
distributions have long been part of its data-quality practice [@yesson2007HowGlobalGlobal]. We offer
that application as a proposal.

### Limitations

- **Selection.** The cases were selected for consequence, so they describe kinds of finding, not their
  frequency in the infrastructure.
- **Downstream scope.** We replayed published calculations and part of one deposited model, not whole
  downstream studies; measured consequences are to support counts, inputs and our own analyses.
- **Independence.** Checks vary in independence. The INDITEK forward run reused the original harness, and
  some checks shared inputs or model family.
- **Calibration controls.** These rest on two simulated clades. One declared agreement gate failed: it
  required at least [0.99]{.C196} of paired range-end bounds to agree within [0.02]{.C196} Myr, and
  [0.91]{.C196} did. The executed hiatus windows were shifted one Myr from the declared design.
- **Causes and status.** The causes of the PBDB absences, the NSB disagreements and the INDITEK score
  mismatch are unresolved. Neither the stored nor the recomputed NSB ages are certified, and the
  plate-model spread is structural disagreement among models, not calibrated error.
- **Reproduction.** Some inputs (container images, posterior logs, source archives) are held locally, and
  a cold rebuild from public inputs alone is untested.
- **Disclosure.** Providers and authors had not been contacted at the time of writing, and whether they
  already knew of a finding is unresolved.

## Conclusions

AI agents can systematically check the databases and software behind fossil-record research, and in
doing so they found verifiable errors and pitfalls that researchers need to know about. Three studies
would extend this case series, each with its own payoff. An audit of a defined population of
dependencies would estimate how often such findings occur; a matched comparison of agent and human
auditors would measure their relative performance; and replay of downstream studies would show what
particular findings change.

## Roles of AI Systems

- **Codex (OpenAI)**, with GPT-6.1 Sol subagents, took over the program's database, reference
  and package work from 28 October 2026; first recorded cases 11 and 12; replayed all twelve cases;
  built the claims ledger; reviewed this paper's wording and reconstruction; and checked its cited
  sources.
- **Claude (Anthropic)**, Opus 5.5 in the main session with Sonnet subagents, ran the database, package
  and reference sessions until 28 October; compiled the 189-row catalogue; selected the twelve cases;
  wrote the interpretation specification; and drafted this paper.
- **Barry W. Brook** facilitated the program, endorsed developing the paper idea on 25 October 2026,
  chose the case series for development on 8 November 2026, and holds decisions on contact, submission
  and release.

In line with *Paleobiology*'s policy, the AI systems are not authors. Their analytical roles are
described in Methods and their role in writing the text here; their role in producing each figure is
stated in its caption.

## Acknowledgments

[To be supplied by B.W.B.: acknowledgments, funding and competing interests.]

## Data Availability Statement

The repository is public at <https://github.com/BWBrook/eprp>; code is MIT-licensed, and text, figures
and data are CC BY-SA 4.0. The claims ledger (`papers/infrastructure-audit/manuscript/claims.csv`) gives
each proposition's evidence files, verifying commit and reproduce command. Third-party sources keep their
own licenses. Records absent from public database snapshots are reported as counts only. A tagged
release will be archived on Zenodo with a DOI.

## Literature Cited

::: {#refs}
:::

## Figure Captions

**Figure 1.** The checked dependencies and the audit workflow. **A**, The twelve cases placed along the
path from rocks to a published result, colored by primary family of check; case 8 also carries a
computation finding. **B**, The workflow, from 189 initial candidate findings and later additions to 22
supported propositions; the six cases whose initial accounts were corrected are listed. Drawn by
`manuscript/figures.py`, written by Claude (Anthropic).

**Figure 2.** Findings in data provenance and transformation. **A**, Deposited molluscan occurrences
present in ([297,657]{.C191}) and absent from ([71,103]{.C191}) the PBDB snapshot of 23 October 2026.
**B**, Intervals with a changed modal base age in three archived snapshot pairs, counting intervals with at
least 50 single-interval occurrences in the later snapshot. **C**, Full-precision changes in mean absolute
paleolatitude for the [1,388]{.C045} of [2,267]{.C045} comparable lineage-bins whose mean changed when
excess Triton rows were removed (count on a log scale; dashed lines at ±1°). **D**, Stored minus
interpolated age for the [56,387]{.C040} comparable NSB samples (symmetric log scale; count on a log
scale; dashed lines at ±0.01 Myr). Drawn by `manuscript/figures.py`, written by Claude (Anthropic),
from the checked tables in `evidence/figure-data-20261112/` and the replay receipts.

**Figure 3.** Findings in computation, model sensitivity and output interpretation. **A**, admtools 0.7.0
time error against height for the [8,282]{.C096} sampled heights of the sparse synthetic model; dashed
lines mark the two hiatuses. **B**, fossilbrush 1.0.6 flag decisions across the test grid at a threshold of
[5]{.C102}: filled circles are flagged, and shaded columns mark where the package differs from numeric
truth. **C**, Observed coverage of the true value against the nominal 95%: PyRate preservation-rate
intervals in two simulation arms (top) and range-end bounds in the ideal arm of two simulated clades
(bottom; Strauss–Sadler in the tbea and EDE implementations, Robson–Whitlock in EDE 0.2.0). **D**, Median
paleolatitude spread among three plate models by age; numbers in parentheses are the points
reconstructable in all three models at that age. Drawn by `manuscript/figures.py`, written by Claude
(Anthropic).

## Tables

**Table 1.** The twelve cases. Families of check: DP, data provenance and transformation; CI, computation
and implementation; MS, model sensitivity; OI, output interpretation and calibration; primary family
first. Discovery: the route in the dated records. Review: what the replay and review trail changed in the
initial account.

| # | Resource | Family | Discovery | Check | Result | Review | Claims |
|--|-----|---|------|------|---------|-----|---|
| 1 | Published PBDB deposit | DP | Source-membership audit; regional-support follow-up | Identifier comparison with a dated snapshot | [71,103]{.C191} of [368,760]{.C191} absent; screen passes [14]{.C192} then [12]{.C192} of 21 stages | "withheld" became "absent from a dated snapshot" | C191, C192 |
| 2 | PBDB interval ages | DP | Comparison of archived snapshots | Recount from archived query products | [460]{.C076}, [317]{.C076}, [17]{.C076} changed modal base ages | none | C076 |
| 3 | Triton 2023 update | DP | Duplicate-key profiling; exposure rebuild | Key grouping; rebuild with and without removal | [1,388]{.C045} of [2,267]{.C045} means changed | counts recomputed | C043, C045 |
| 4 | NSB stored ages | DP | Recomputation from tie points | Interpolation from tie points | [4,111]{.C040} of [56,387]{.C040} differ by > 0.01 Myr | header row removed | C040 |
| 5 | admtools 0.7.0 | CI | Round-trip probe; declared hiatus benchmark | Exact linear-segment truth | [3,972]{.C096} of [8,282]{.C096} heights mis-converted (sparse model) | "every hiatus" became adjoining segments | C096 |
| 6 | fossilbrush 1.0.6 | CI | Smoke-test failure; source inspection | Deterministic grid; numeric truth and text order | differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and [499]{.C102} unflagged at a threshold of [5]{.C102} | none | C102 |
| 7 | PyRate preservation rates | OI | Declared coverage benchmark | Simulation coverage, with positive controls | [81]{.C107}/[100]{.C107} and [33]{.C107}/[50]{.C107} covered | "too narrow" became "shifted high" | C107, C194, C196, C105, C111 |
| 8 | GRIWM, Rextinct 1.1.0 | OI, CI | Smoke run (interval); repeated draws (random state) | Zero-error control; weighted-prefix formula; seed sentinels | interval reflects dating error; caller's random state overwritten | none | C110, C098 |
| 9 | Three plate models | MS | Cross-route comparison; three-model follow-up | Reconstruction of shared points; geometry of two routes | median spread [2.9]{.C125}–[13.6]{.C125}° | none | C125, C123 |
| 10 | Published spreadsheets | DP | Format inspection; table-to-workbook comparison | Comparison with intact binary and chapter workbooks | [2,967]{.C035} of [6,562]{.C035} histories differ numerically from the binary deposit; [220]{.C048} shifted rows | cell count separated from history count | C035, C048 |
| 11 | Printed probability | CI | Reading the printed test; exact calculation | Exact arithmetic, four routes | [0.316]{.C190} against $3.4 \times 10^{-16}$ | none | C190 |
| 12 | INDITEK-2.0 scores | CI | Declared forward replay; rescoring | Forward replay; separately written rescoring | vectors replay; saved scores differ from rescoring under deposited observations by up to [42.4]{.C193} | none | C195, C193 |

**Table 2.** Recommended actions, by audience.

| Audience | Actions | Cases |
|------|------------------------|----|
| Users | Record query dates and versions; check deposited records against the snapshot used; compare plate models and state the reference frame; replay a published number before building on it | 1, 2, 9, 11 |
| Database maintainers | Version interval ages and records, with change logs; document how stored values derive from their sources | 1–4 |
| Package maintainers | Test against known truth at boundary cases; compare numbers as numbers; leave the caller's random-number state intact; document what each interval measures | 5–8 |
| Journals and depositors | Require machine-readable deposits; archive scoring code and observations with saved scores | 10–12 |
| Programs using AI agents | Pair each finding with a second check; declare tests before running them and keep failed gates; publish receipts and reviewed correspondence | all |
