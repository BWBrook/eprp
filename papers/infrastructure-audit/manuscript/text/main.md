# With receipts: twelve checked cases from agent-assisted audits of palaeobiology's data and software

<div id="authors"></div>

## Abstract

Quantitative palaeobiology rests on shared infrastructure: occurrence databases, published data
deposits, time scales, plate models and analysis packages. Problems in these layers can pass into
published inference unnoticed, because auditing them is slow, broad and rarely rewarded. During the first
month of a research programme run by two AI systems (Anthropic's Claude and OpenAI's Codex) with a human
facilitator, agent-assisted audits turned up candidate findings across this infrastructure. We report
twelve of them as a case series. Each was chosen for its consequence for inference, replayed from pinned
inputs, and checked by a different actor along a separate computational route. The cases cover:

- deposited occurrences absent from a dated public database snapshot ([71,103]{.C191} of
  [368,760]{.C191} molluscan records);
- interval ages that change between archived database snapshots;
- excess rows in a database update that changed [1,388]{.C045} of [2,267]{.C045} exposure means in one of
  our own analyses;
- stored sample ages that disagree with their own tie points;
- three implementation defects in analysis packages;
- a calibration failure, alongside two positive controls;
- the semantics of a widely used extinction-time interval;
- model-dependent palaeolatitudes;
- two published spreadsheets that differ from their sources;
- a printed significance value that its stated test does not reproduce ([0.316]{.C190}, not
  $3.4 \times 10^{-16}$);
- archived calibration scores that do not replay.

Every proposition is bounded to the version, design and convention tested. Several original headlines
were narrowed or withdrawn during replay, and we report those corrections. The series does not estimate
how common such problems are, and it does not show that agent-assisted auditing is better than other
auditing. It does show, with receipts anyone can rerun, the kinds of problem that cheap, systematic
replay exposes, and what each one does and does not change for inference.

## 1. Introduction

A palaeobiological result is usually several layers of other people's work deep. An occurrence count
depends on a database query and that database's state on the day of the query. An age depends on a time
scale and an age model. A palaeolatitude depends on a plate model and its reference frame. A rate depends
on an estimator and on the package that implements it. Each layer is maintained by people with too
little time. Each changes, and few users check the layer below the one they work in.

The community knows this. In the recent survey of open questions in palaeontology [@smith2025IdentifyingBigQuestions],
several of the priorities concern exactly this layer: quantifying collecting and preservation biases,
finding and correcting data-entry biases, accounting for data loss, and making data open and combinable.
Audits of the infrastructure answer those calls directly. They are rarely done, because they are tedious,
broad and thankless, and the person best placed to find a problem is usually the person with the least
time to look for it.

Agentic AI systems change the cost of that work. During October and November 2026, the Extinction and
Palaeontology Research Programme (EPRP) used two such systems, with a human facilitator, to vet research
questions against the data that could answer them. Vetting meant mirroring databases and deposits,
benchmarking packages against known truth, and replaying published numbers. That work produced 189
candidate findings about the infrastructure itself.

This paper reports twelve of them as a case series. For each case we state the checked proposition,
the evidence and how it was replayed, what it changes for inference, and what it does not show. We also
report what the auditing agents themselves got wrong. The aim is not a rate or a ranking. It is a set of
inspectable cases, each with a command that reproduces it.

## 2. How the cases were found, chosen and checked

**Finding.** The candidates came from read-only mirrors of databases, deposits and plate models (each
hashed on arrival), benchmark suites declared before they were run, and checks on published numbers made
while vetting research questions. Three working sessions, one each for databases, packages and
references, recorded each finding with its evidence location and the checks it had received.

**Choosing.** From the 189 candidates we chose twelve cases by consequence for inference: what each would
change in an analysis someone plausibly runs. Being a defect was not enough on its own. We also wanted the
selection to cover the kinds of finding in the pool, and we included positive controls, because a series
that only finds faults says nothing about how discriminating the checks were. Licence and
bibliographic-metadata problems were left out as having little bearing on inference. Location data whose
description could itself cause harm were left out entirely. The selection note, with reserves, is in the
repository (Supplement S1).

**Checking.** Each case was replayed from pinned inputs on 8 November 2026. A different actor from the
one who made the original finding then rederived each supporting proposition by a separate computational
route: a separate implementation, a recount from raw files, or a closed-form calculation. Each
proposition is a row in one claims ledger, with its value, evidence files, the commit at which the
evidence was verified, a command that regenerates it, and a statement of what it does not show. A row is
marked supported only after that independent check. Where the replay did not reproduce an original
number, the number was withdrawn, and the withdrawal is recorded (Section 4; Supplement S3).

**Classes.** Following the audit design, each case is classified by what kind of finding it is:

- an implementation defect;
- a data inconsistency;
- a calibration failure under a stated model;
- a semantic finding (what a quantity actually estimates);
- an intended version or model choice that users need to know about;
- a replay failure;
- a sensitive access finding.

These classes matter. An intended version change is not an error, and calling it one would be unfair to
the people who maintain the resource.

## 3. The cases

**Table 1.** The twelve cases. Values are from the claims ledger; each row's conditions are in the text.

| # | Case | Class | Checked proposition | Claims |
|--|--------------|----------|----------------------------------|---------|
| 1 | Deposited records absent from a dated public snapshot | sensitive access finding | [71,103]{.C191} of [368,760]{.C191} molluscan occurrences in a published deposit are not in a public snapshot of 23 October 2026 | C191, C192 |
| 2 | Interval ages change between archived snapshots | intended version choice | [460]{.C076}, [317]{.C076} and [17]{.C076} intervals changed modal base age across three snapshot brackets | C076 |
| 3 | Excess rows in a database update | data inconsistency | [28,832]{.C043} excess rows under a specified key; removing [16,260]{.C043} changed [1,388]{.C045} of [2,267]{.C045} exposure means | C043, C045 |
| 4 | Stored ages disagree with their tie points | data inconsistency | [4,111]{.C040} of [61,862]{.C040} samples differ by more than 0.01 Myr | C040 |
| 5 | Age–depth conversion above hiatuses | implementation defect | [3,972]{.C096} of [8,282]{.C096} test points wrong, by up to [0.466]{.C096} Myr | C096 |
| 6 | Numbers compared as text | implementation defect | at a threshold of [5]{.C102}, differences of [10]{.C102} to [499]{.C102} were not flagged | C102 |
| 7 | Preservation-rate calibration, with positive controls | calibration failure | intervals covered the truth in [81]{.C107} of [100]{.C107} and [33]{.C107} of [50]{.C107} replicates; classical bounds near nominal | C107, C194, C196, C105, C111 |
| 8 | What an extinction-time interval estimates | semantic finding and defect | the interval reflects resampled dating error only; the call overwrites the caller's random-number state | C110, C098 |
| 9 | Plate-model palaeolatitudes | intended model choice | median spread among three models from [2.9]{.C125} degrees at 10 Ma to [13.6]{.C125} degrees at 400 Ma | C125, C123 |
| 10 | Published spreadsheets differ from their sources | data inconsistency | [2,967]{.C035} of [6,562]{.C035} capture histories altered; [220]{.C048} rows shifted one column | C035, C048 |
| 11 | A printed probability | arithmetic error in a published claim | the stated binomial test gives [0.316]{.C190}, not $3.4 \times 10^{-16}$ | C190 |
| 12 | Archived calibration scores | replay failure | three saved scores differ from rescored values by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193} | C195, C193 |

### 3.1 Data access and provenance

**Case 1.** A published global analysis of marine latitudinal diversity [@benson2025MarineAnimalDiversity]
deposited its occurrence data. Of the [368,760]{.C191} occurrences in the deposit's molluscan member,
[71,103]{.C191} are not present in a public Paleobiology Database snapshot taken on 23 October 2026[]{.C191}.
That is about one record in five. Absence from a dated snapshot does not by itself establish
why the records are absent; deletion, merging and other database changes can all contribute. It does
mean that a reader who rebuilds the analysis from today's public database cannot obtain the same input.
The consequence showed up in our own work. A cheap screen for outside-Europe and North America tropical
support passed in [14]{.C192} of [21]{.C192} stages with the full deposit, and in [12]{.C192} with
snapshot members only[]{.C192}. We report these records as counts only.

**Case 2.** Archived query products from the Paleobiology Database show interval base ages changing
between consecutive snapshots. Across three main brackets, [460]{.C076}, [317]{.C076} and [17]{.C076}
intervals with at least 50 single-interval occurrences changed their modal base age[]{.C076}. If the
50-occurrence threshold must hold in both snapshots, the middle count is [316]{.C076}. A query repeated on
different dates can therefore return different ages for the same interval. We have not shown whether the
database keeps historical versions accessible, and we make no comparison here with the international
chronostratigraphic chart. This is a version change, and the point for users is to record the date and
version of every query.

**Case 3.** The 2023 update of the Triton planktonic-foraminifera database [@fenton2021TritonSpecieslevelDatabase]
contains [28,832]{.C043} excess rows under the key we specified. A conservative recipe that keeps one row
per key by source priority removes [16,260]{.C043} of them[]{.C043}. Rows that share a key are not
necessarily repeated physical observations, so we call them excess rows under that key, not duplicates.
The consequence is measured in one of our own analyses. Rebuilding EPRP's exposure index with and without
the removal changed [1,388]{.C045} of [2,267]{.C045} comparable lineage-bin means, [411]{.C045} of them by
at least one degree. Of 491 lineage-pair rows, [8]{.C045}, [8]{.C045}, [2]{.C045} and [1]{.C045} changed their
classification under four different classification rules[]{.C045}. An earlier internal report of 1,454 and 423 changed means did not
reproduce under the pinned recipe and is withdrawn (Supplement S3).

**Case 4.** The final snapshot of the Neptune Sandbox Berlin database [@renaudie2020NsbNeptuneSandbox]
stores an age for each sample. We recomputed each age from its hole's current tie points by linear
interpolation. Of [61,862]{.C040} samples, [4,111]{.C040} in [56]{.C040} holes differ from the stored value
by more than 0.01 Myr[]{.C040}. The recomputation takes the first age where two tie points share a
depth; with the other choice, [8]{.C040} of the differences disappear. Neither set of ages is thereby
shown to be right. A user who takes the stored ages and one who recomputes from the tie points will be
working from different numbers.

### 3.2 Software correctness

**Case 5.** admtools 0.7.0 converts stratigraphic height to time. On a synthetic age–depth model with two
hiatuses, [3,972]{.C096} of [8,282]{.C096} random query points received wrong times, by up to
[0.466]{.C096} Myr, against exact linear-segment truth; a targeted probe gave an error of about
[2.7]{.C096} Myr[]{.C096}. The errors fall in affected interpolation segments. Later segments can be
correct, so the error does not apply to every point above a hiatus.

**Case 6.** fossilbrush 1.0.6 flags occurrences whose ages differ from a reference range by more than a
threshold. It compares the differences with the threshold as text. At a threshold of [5]{.C102}, it failed
to flag differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and [499]{.C102}. A character
comparison predicts every flag on the test grid, which identifies the mechanism[]{.C102}. This is a
tested mechanism on a deterministic grid, not a measured rate of misflagged records in real data.

**Case 8.** The GRIWM estimator of extinction time [@bradshaw2012RobustEstimatesExtinction], as
implemented in Rextinct 1.1.0, reports an interval whose width comes only from resampling the input dating
errors. With zero dating error, the interval collapses to a point[]{.C110}. It is therefore not an
interval for the extinction time given the sampling of the record, and it should not be reported as one.
The same implementation also overwrites the calling program's random-number state[]{.C098}. Any
analysis that draws random numbers after calling it inherits a stream it did not choose. We have not
quantified the effect of either finding on any published study.

### 3.3 Calibration, with positive controls

**Case 7.** We simulated fossil records under a declared design and asked whether PyRate's
[@silvestro2014PyrateProgramEstimate] 95% intervals for the preservation rate covered the true value. They
covered it in [81]{.C107} of [100]{.C107} replicates in one arm and [33]{.C107} of [50]{.C107} in a
lower-preservation arm, and the posterior medians sat above the truth (median relative bias
[0.0895]{.C107} and [0.458]{.C107})[]{.C107}. The intervals are not too narrow: every miss lies below
the lower endpoint, which points to location bias rather than understated spread.

The same benchmark showed that the checks can tell good from bad. In the ideal arm, the classical
Strauss–Sadler range-end bound [@strauss1989ClassicalConfidenceIntervals] covered the truth in
[1,895]{.C194} and [1,899]{.C194} of [2,000]{.C194} cases in two independent implementations, and the
Robson–Whitlock bound in [1,909]{.C194}[]{.C194}. The simulation generators matched their analytic
moments[]{.C105}. Two qualifications travel with these controls:

- **A declared gate failed.** The pre-declared overall agreement gate required 99% of paired bounds to
  agree within [0.02]{.C196} Myr; [0.91]{.C196} did[]{.C196}. We report the failure.
- **The hiatus arm deviated from its declaration.** Its executed windows were shifted one Myr from the
  declared design. In that arm, Strauss–Sadler coverage fell to [1,125]{.C111} of [1,272]{.C111} retained
  cases, with [728]{.C111} cases dropped[]{.C111}.

### 3.4 Spatial models

**Case 9.** Three widely used plate models [@merdith2021ExtendingFullplateTectonic; @matthews2016GlobalPlateBoundary]
place the same [300]{.C125} public points at different palaeolatitudes. The median spread among them is
[2.9]{.C125} degrees at 10 Ma, [5.7]{.C125} at 50 Ma and [13.6]{.C125} at 400 Ma[]{.C125}. This is
structural disagreement among models, not calibrated error. A diversity gradient analysed in latitude
bands of 20 degrees will move points between bands depending on the model chosen. Separately, two routes
to reconstructing the same named model differ by an approximately rigid, age-specific rotation. That is
consistent with their using different absolute reference frames[]{.C123}. We do not identify either
frame as correct. The practical point is that a model name alone does not fix the coordinates.

### 3.5 Published deposits and published numbers

**Case 10.** The electronic supplement of a study of extinction selectivity [@monarrez2023ReducedStrengthIncreased]
provides capture histories in a spreadsheet as well as an intact binary file. Comparing the two, we found
[2,967]{.C035} of [6,562]{.C035} histories in the spreadsheet with altered values. [3,595]{.C035} more can
be restored exactly by padding to the known width of [86]{.C035} characters[]{.C035}. The pattern is consistent with spreadsheet software converting long digit
strings to numbers, though we did not establish how the file was produced. Separately,
the one-file All-Life table of the Fossil Record 2 compilation has [220]{.C048} rows shifted one column
left relative to its chapter workbooks. In [112]{.C048} rows this moves a family's range by one interval[]{.C048}.
We did not rerun either study's analysis, and we make no claim about its conclusions.

**Case 11.** A recent analysis of cyclicity in stratigraphic boundaries [@rampino2025CorrelationCyclicityStratigraphic]
states a binomial test with n = [47]{.C190}, k = [28]{.C190} and p = [0.55]{.C190}, and prints a tail
probability of $3.4 \times 10^{-16}$. The stated test gives [0.316]{.C190}[]{.C190}. We confirmed this by
exact rational arithmetic, by integer polynomial convolution, by a direct exact sum and in R. This does
not bear on the paper's separate spectral analysis, which we did not rerun.

**Case 12.** The INDITEK-2 model of Phanerozoic marine diversity [@cermeno2022PostextinctionRecoveryPhanerozoic]
archives its calibration runs. We reran three archived proposals from the pinned archive. Their
predictions replay exactly, to [2,978]{.C195} cells[]{.C195}. Their saved residual sums of squares,
however, differ from the rescored values by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193}, and a separate,
model-free rescoring agrees with ours[]{.C193}. All three are rejected proposals, not accepted draws.
The cause of the disagreement is unresolved, and we make no claim about the published conclusions.

## 4. What the auditing agents got wrong

The agents' own errors are part of the record. Replay withdrew or narrowed several of the original
findings:

- **Case 3.** The changed-mean counts of 1,454 and 423 did not reproduce under the pinned recipe, and an
  11–13% sample inflation figure was withdrawn.
- **Case 4.** A sample count that included a header row was corrected to [61,862]{.C040}.
- **Case 5.** "Wrong above every hiatus" was false; the error is confined to affected segments.
- **Case 7.** "Too narrow" intervals were not supported.
- **Case 10.** A count of 5,291 cells in scientific notation had been read as a count of damaged
  histories.

Earlier in the programme, the two agents corrected each other's scientific reasoning repeatedly. One
agent's proposed rule, for example, was refuted by the other's counterexample, and a predicted outcome of
a screening test was wrong. The full correspondence record is available. These errors were caught because
each finding was rechecked by a different actor along a different route. We do not claim that this
arrangement catches more errors than any other; the series contains no comparison that could show it.

## 5. Recommendations

- **For database providers:** expose versions and change logs for interval ages and records; say in query
  results when records have been removed or merged.
- **For package authors:** test against known truth, including hiatuses and boundary cases; compare
  numbers as numbers; never reset the caller's random-number state.
- **For authors of deposits:** deposit identifiers and histories as text in machine-readable formats, not
  in spreadsheets; archive the scorer and observations with any saved calibration scores.
- **For users:** record the date and version of every query; rerun spatial analyses under more than one
  plate model and state the reference frame; replay a published number before building on it.
- **For programmes that use AI agents:** declare tests before running them, keep failed gates, have a
  different actor recheck each finding by a different route, and publish the correspondence.

## 6. Discussion

### 6.1 What follows

Each case is small on its own. Together they show that the layer beneath published palaeobiology holds
problems of several distinct kinds: version changes users need to know about, inconsistencies within a
resource, implementation defects, estimators whose output is easy to misdescribe, and published numbers
that do not survive replay. None of these problems needed new data or new theory to find. They needed
someone to take the time to replay each layer against known truth or against its own source.

### 6.2 Which conclusions depend on which assumptions

**Table 2.** Dependence of the main conclusions on their assumptions.

| Conclusion | Rests on | Fails if |
|----------------|----------------|----------------|
| Each case's proposition holds for the version tested | Pinned inputs and the stated convention | A different input version, convention or design is substituted |
| The consequence for inference is real | The downstream calculation named in the case | The downstream use differs from the one tested |
| The independent check adds information | A different actor and computational route | The routes share an error (e.g. a common input misread) |
| Third-party findings are not already known | Our search of changelogs and issue trackers (incomplete) | A provider documented the behaviour before our audit |

### 6.3 What would sharpen the answer

- **Disclosure responses.** Providers' and authors' replies would establish which findings are already
  known, intended or fixed.
- **A controlled comparison.** The same audit run by experienced human auditors would allow the cost and
  yield of agent-assisted auditing to be compared, which this series cannot do.
- **Downstream replays.** Rerunning one or more published analyses that use the affected layers would
  measure consequence directly, rather than by the proxy analyses used here.

## 7. Conclusions

Cheap, systematic replay of palaeobiology's shared infrastructure exposes problems of several kinds. The
twelve cases here are each bounded, reproducible and checked by a second route. They are a sample of what
one programme found, not a measure of how often such problems occur. Their value is that anyone can rerun
them, and that providers, authors and users can act on them.

## Methods in brief

Supplement S1 gives the case selection and its rules. S2 gives the replay and independent check for each
case, with commands. S3 is the audit trail of withdrawn and narrowed statements.

## Roles of AI systems and humans

- **Codex (OpenAI GPT-6, with GPT-6.1 Sol delegates)**
  - took over the programme's database, reference and package work from 28 October;
  - replayed all twelve cases;
  - built the claims ledger;
  - made the independent checks.
- **Claude (Anthropic)**, Opus 5.5 in the main session and Claude Sonnet subagents:
  - ran the database, package and reference sessions that produced most of the original findings,
    before 28 October;
  - compiled the 189-row candidate ledger;
  - chose the twelve cases;
  - wrote the interpretation specification and drafted this paper.
- **Barry W. Brook** facilitated the programme, approved the paper on 25 October 2026, chose this case
  series for development on 8 November 2026, and holds decisions on provider contact, submission and
  release.

The two AI systems reviewed each other's work throughout. Their correspondence is published in the
repository as reviewed snapshots (`docs/correspondence/`).

## Data and code

The repository is public at <https://github.com/BWBrook/eprp>; code is MIT-licensed and text, figures and
data are CC BY-SA 4.0. The claims ledger (`papers/infrastructure-audit/manuscript/claims.csv`) gives, for
each proposition, the evidence files, the commit at which they were verified and the command that
regenerates them. Third-party sources keep their own licences and are not redistributed. Records absent
from public database snapshots are reported as counts only.

## References
