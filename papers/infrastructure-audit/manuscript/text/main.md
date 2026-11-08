# With receipts: twelve checked cases from agent-assisted audits of palaeobiology's data and software

<div id="authors"></div>

## Abstract

Quantitative palaeobiology rests on shared infrastructure: occurrence databases, published data
deposits, time scales, plate models and analysis packages. Problems in these layers can pass into
published inference unnoticed. During the first month of a research programme run by two AI systems
(Anthropic's Claude and OpenAI's Codex) with a human facilitator, agent-assisted audits produced candidate
findings about this infrastructure. We report twelve as a case series. Each was chosen for its consequence
for inference, replayed from pinned inputs by a different actor, and checked by the computational or
mathematical routes recorded in its receipt. The cases include:

- deposited occurrences absent from a dated public database snapshot ([71,103]{.C191} of
  [368,760]{.C191} molluscan records);
- interval ages that change between archived database snapshots;
- excess rows in a database update that changed [1,388]{.C045} of [2,267]{.C045} exposure means in one of
  our own analyses;
- stored sample ages that disagree with their own tie points;
- three implementation defects in analysis packages;
- a preservation-rate calibration failure, reported beside retained positive controls;
- an extinction-time interval that measures dating sensitivity only;
- model-dependent palaeolatitudes;
- two published spreadsheets that differ from their sources;
- a printed significance value that its stated test does not reproduce ([0.316]{.C190}, not
  $3.4 \times 10^{-16}$);
- archived calibration scores that do not replay.

Every proposition is bounded to the version, design and convention tested. Replay narrowed or withdrew
several of the original statements, and we report those corrections. The series does not estimate how
common such problems are, does not show that agent-assisted auditing is better or cheaper than other
auditing, and does not test whether any published conclusion changes. It records, with commands and input
hashes, the kinds of problem that systematic replay exposed in one programme and what each one does and
does not change.

## 1. Introduction

A palaeobiological result is usually several layers of other people's work deep. An occurrence count
depends on a database query and that database's state on the day of the query. An age depends on a time
scale and an age model. A palaeolatitude depends on a plate model and its reference frame. A rate depends
on an estimator and on the package that implements it. Each layer is maintained by others and changes over
time.

The community has asked for scrutiny of exactly this layer. In a recent community survey of open
questions in palaeontology [@smith2025IdentifyingBigQuestions], several priorities concern it:
quantifying collecting and preservation biases, finding and correcting data-entry biases, accounting for
data loss, and making data open and combinable. Audits of the infrastructure bear directly on those
priorities.

During October and November 2026, the Extinction and Palaeontology Research Programme (EPRP) used two AI
systems, with a human facilitator, to vet research questions against the data that could answer them.
Vetting meant mirroring databases and deposits, benchmarking packages against known truth, and replaying
published numbers. That work produced an initial catalogue of 189 candidate findings about the
infrastructure itself, and later findings as the programme continued.

This paper reports twelve of them as a case series. For each case we state the checked proposition, the
evidence and how it was replayed, what it changes, and what it does not show. We also report what the
auditing agents themselves got wrong. The aim is not a rate or a ranking. It is a set of inspectable
cases, each with a recorded replay command.

## 2. How the cases were found, chosen and checked

**Finding.** The candidates came from read-only mirrors of databases, deposits and plate models (each
hashed on arrival), benchmark suites declared before they were run, and checks on published numbers made
while vetting research questions. Three working sessions, for databases, packages and references,
recorded each finding with its evidence location and the checks it had received. Candidates include
positive controls and intended behaviours as well as suspected problems.

**Choosing.** From the initial catalogue and subsequent programme findings we chose twelve cases by
consequence for inference: what each would change in an analysis someone plausibly runs. Being a defect
was not enough on its own. We also wanted the selection to cover the kinds of finding in the pool, and we
retained positive controls. Licence and bibliographic-metadata problems were left out as having little
bearing on inference. Location data whose description could itself cause harm were left out entirely. The
selection note, with reserves, is in the repository (Supplement S1).

**Checking.** Each case was replayed from pinned inputs on 8 November 2026 by a different actor from the
one who made the original finding, combined with the checks specified in its receipt. These included
separate aggregation, interpolation, geometry and scoring code, recounts from raw files and closed-form
calculations. Independence is check-specific. For example, the INDITEK forward run reused the original
pinned harness, and only its scoring was separately implemented. Some reviewers used the same model family
and shared inputs. Each proposition is a row in one claims ledger, with its value, evidence files, the
commit at which the evidence was verified, a replay command, and a statement of what it does not show.
Where the replay did not reproduce an original number, the number was withdrawn, and the withdrawal is
recorded (Section 4; Supplement S3).

**Classes.** Each case is classified by what kind of finding it is:

- an implementation defect;
- a data inconsistency;
- a calibration failure under a stated model;
- a semantic finding (what a quantity actually measures);
- an intended version or model choice that users need to know about;
- a snapshot-membership or provenance finding;
- a replay failure.

These classes matter. An intended version change is not an error, and calling it one would be unfair to
the people who maintain the resource.

## 3. The cases

**Table 1.** The twelve cases. Values are from the claims ledger; each row's conditions are in the text.

| # | Case | Class | Checked proposition | Claims |
|--|--------------|----------|----------------------------------|---------|
| 1 | Deposited records absent from a dated public snapshot | membership and provenance | [71,103]{.C191} of [368,760]{.C191} molluscan occurrences in a published deposit are not in a public snapshot of 23 October 2026 | C191, C192 |
| 2 | Interval ages change between archived snapshots | intended version choice | [460]{.C076}, [317]{.C076} and [17]{.C076} intervals changed modal base age across three snapshot brackets | C076 |
| 3 | Excess rows in a database update | data inconsistency | [28,832]{.C043} excess rows under a specified key; removing [16,260]{.C043} changed [1,388]{.C045} of [2,267]{.C045} exposure means | C043, C045 |
| 4 | Stored ages disagree with their tie points | data inconsistency | [4,111]{.C040} of [56,387]{.C040} comparable samples differ by more than 0.01 Myr | C040 |
| 5 | Age–depth conversion above hiatuses | implementation defect | sparse model: [3,972]{.C096} of [8,282]{.C096} query points mis-converted, maximum error about [3.0]{.C096} Myr | C096 |
| 6 | Numbers compared as text | implementation defect | at a threshold of [5]{.C102}, differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and [499]{.C102} were not flagged | C102 |
| 7 | Preservation-rate calibration, with retained controls | calibration failure | intervals covered the truth in [81]{.C107} of [100]{.C107} and [33]{.C107} of [50]{.C107} replicates, shifted high | C107, C194, C196, C105, C111 |
| 8 | What an extinction-time interval measures | semantic finding and defect | the interval reflects resampled dating error only; the call overwrites the caller's random-number state | C110, C098 |
| 9 | Plate-model palaeolatitudes | intended model choice | median spread among three models, age dependent, from [2.9]{.C125} degrees at 10 Ma to [13.6]{.C125} at 400 Ma | C125, C123 |
| 10 | Published spreadsheets differ from their sources | data inconsistency | [2,967]{.C035} of [6,562]{.C035} capture histories altered; [220]{.C048} rows shifted one column | C035, C048 |
| 11 | A printed probability | arithmetic error in a published claim | the stated binomial test gives [0.316]{.C190}, not $3.4 \times 10^{-16}$ | C190 |
| 12 | Archived calibration scores | replay failure | three saved scores differ from rescored values by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193} | C195, C193 |

### 3.1 Data membership and provenance

**Case 1.** A published global analysis of marine latitudinal diversity [@benson2025MarineAnimalDiversity]
deposited its occurrence data. Of the [368,760]{.C191} occurrences in the deposit's molluscan member,
[71,103]{.C191} are not present in a public Paleobiology Database snapshot taken on 23 October
2026[]{.C191}. Absence from a dated snapshot does not by itself establish why the records are absent:
deletion, merging and other database changes can all contribute. Rebuilding from that dated snapshot
would omit these deposited identifiers. The consequence showed up in our own work. A simple presence screen for
tropical support outside Europe and North America passed in [14]{.C192} of [21]{.C192} stages with the full
deposit, and in [12]{.C192} with snapshot members only[]{.C192}. We report these records as counts only.

**Case 2.** Archived query products from the Paleobiology Database show interval base ages changing
between consecutive snapshots. Across three main brackets, [460]{.C076}, [317]{.C076} and [17]{.C076}
intervals changed their modal base age, counting intervals with at least 50 single-interval occurrences in
the later snapshot[]{.C076}. If the threshold must hold in both snapshots, the middle count is
[316]{.C076}. The statistic is the modal base age of an interval, not every record's age. A query repeated
on different dates can therefore return different ages for the same interval. We have not shown whether
the database keeps historical versions accessible, and we make no comparison with the international
chronostratigraphic chart. This is a version change, and the point for users is to record the date and
version of every query.

**Case 3.** The 2023 update of the Triton planktonic-foraminifera database
[@fenton2021TritonSpecieslevelDatabase] contains [28,832]{.C043} excess rows under the key we specified.
Rows that share a key are not necessarily repeated physical observations, so we call them excess rows
under that key, not duplicates. A conservative recipe removes lower-priority-source rows only from
cross-source groups with recorded depth, retaining every row from the highest-priority source; it removes
[16,260]{.C043} rows[]{.C043}. The consequence is measured in one of our own analyses. Rebuilding EPRP's
exposure index with and without the removal changed [1,388]{.C045} of [2,267]{.C045} comparable unrounded
lineage-bin means, [411]{.C045} of them by at least one degree. Of 491 lineage-pair rows, [8]{.C045},
[8]{.C045}, [2]{.C045} and [1]{.C045} changed their classification under four different classification
rules[]{.C045}. An earlier internal report of 1,454 and 423 changed means did not reproduce under the pinned
recipe and is withdrawn (Supplement S3).

**Case 4.** The final snapshot of the Neptune Sandbox Berlin database [@renaudie2020NsbNeptuneSandbox]
holds [61,862]{.C040} samples. We recomputed ages by linear interpolation from each hole's current tie
points, where those tie points permitted. [56,387]{.C040} samples have both a stored and a recomputed numeric age. Of
these, [4,111]{.C040} in [56]{.C040} holes differ by more than 0.01 Myr[]{.C040}. The recomputation takes
the first age where two tie points share a depth; with the other choice, [8]{.C040} of the differences
disappear. That sensitivity concerns exact ties only, not other interpolation models. Neither set of ages
is thereby shown to be right. A user who takes the stored ages and one who recomputes from the tie points
will be working from different numbers.

### 3.2 Software correctness and semantics

**Case 5.** admtools 0.7.0 converts stratigraphic height to time. We tested it on one synthetic age–depth
model with two hiatuses, in two versions, against exact linear-segment truth. In the sparse tie-point
version, [3,972]{.C096} of [8,282]{.C096} query points were mis-converted, with maximum error about
[3.0]{.C096} Myr. In the dense version, [6]{.C096} of the same queries were mis-converted, with maximum
error [0.466]{.C096} Myr, and a targeted probe near a hiatus gave about [2.7]{.C096} Myr[]{.C096}. The
errors fall in affected interpolation segments; later segments can be correct.

**Case 6.** fossilbrush 1.0.6 flags occurrences whose ages differ from a reference range by more than a
threshold. It compares the differences with the threshold as text. At a threshold of [5]{.C102}, it failed
to flag differences of [10]{.C102}, [20]{.C102}, [49.9]{.C102}, [100]{.C102} and [499]{.C102}, while
flagging others on the grid, including 50 and 99. Character order predicts every flag on the test
grid[]{.C102}. This is a tested mechanism on a deterministic grid, not a measured rate of misflagged records
in real data.

**Case 8.** The GRIWM estimator of extinction time [@bradshaw2012RobustEstimatesExtinction], as implemented
in Rextinct 1.1.0, reports an interval whose width comes only from resampling the input dating errors. With
zero dating error, the interval collapses to a point[]{.C110}. The interval therefore measures the
sensitivity of the estimate to uncertain dates, conditional on the records. It does not quantify
uncertainty from the fossil-sampling process. Separately, the implementation overwrites the calling
program's random-number state[]{.C098}, so any analysis that draws random numbers after calling it inherits
a stream it did not choose. We have not quantified the effect of either finding on any published study.

### 3.3 Calibration, with retained controls

**Case 7.** We simulated fossil records under a declared constant-rate, homogeneous-Poisson design and asked
whether PyRate's [@silvestro2014PyrateProgramEstimate] 95% intervals for the preservation rate covered the
true value. They covered it in [81]{.C107} of [100]{.C107} replicates in one arm and [33]{.C107} of
[50]{.C107} in a lower-preservation arm. Posterior medians sat above the truth, with median relative bias
[0.0895]{.C107} and [0.458]{.C107}[]{.C107}. Every miss lies below the lower endpoint: the intervals are
shifted high. The retained width comparisons do not support an earlier diagnosis that the intervals were
too narrow. They do not establish calibrated widths or the cause of the shift.

The benchmark also retained positive controls, in a different design with a different target: range-end
bounds for retained species in two simulated clades. Under homogeneous sampling, the classical
Strauss–Sadler bound [@strauss1989ClassicalConfidenceIntervals] covered the truth in [1,895]{.C194} and
[1,899]{.C194} of [2,000]{.C194} cases in two implementations, and the Robson–Whitlock bound in
[1,909]{.C194}[]{.C194}. The G1 and G2 generator moment controls matched their analytic
expectations[]{.C105}. Two qualifications travel with these controls:

- **A declared gate failed.** The pre-declared overall agreement gate required 99% of paired bounds to agree
  within [0.02]{.C196} Myr; [0.91]{.C196} did[]{.C196}.
- **The hiatus arm deviated from its declaration.** Its executed windows were shifted one Myr from the
  declared design. In that arm, Strauss–Sadler coverage fell to [1,125]{.C111} of [1,272]{.C111} retained
  cases, with [728]{.C111} cases dropped[]{.C111}.

These controls show that the benchmark did not report failure everywhere. They do not rank the classical
bounds against PyRate, which target a different quantity.

### 3.4 Spatial models

**Case 9.** We reconstructed a starting pool of [300]{.C125} public points at six ages in three plate
models: MERDITH2021 [@merdith2021ExtendingFullplateTectonic], PALEOMAP and MATTHEWS2016_pmag_ref
[@matthews2016GlobalPlateBoundary]. At each age, the median spread of palaeolatitude among the three models
is taken over the points reconstructable in all three; [194]{.C125} points are reconstructable at every age.
The median spread is age dependent and not monotonic: [2.9]{.C125} degrees at 10 Ma, [5.7]{.C125} at 50 Ma,
[4.3]{.C125} at 100 Ma, and the largest, [13.6]{.C125}, at 400 Ma[]{.C125}. This is structural disagreement
among models, not calibrated error, and model choice can change the latitude-band assignments of a
diversity-gradient analysis. Separately, two routes to reconstructing TorsvikCocks2017 differ by an
approximately rigid, age-specific rotation. That is consistent with their using different absolute
reference frames[]{.C123}. We do not identify either frame as correct. A model name alone does not fix the
coordinates.

### 3.5 Published deposits and published numbers

**Case 10.** The electronic supplement of a study of extinction selectivity
[@monarrez2023ReducedStrengthIncreased] provides capture histories in a spreadsheet as well as an intact
binary file. Comparing the two, we found [2,967]{.C035} of [6,562]{.C035} histories in the spreadsheet with
altered values. A further [3,595]{.C035} can be restored exactly by padding to the known width of
[86]{.C035} characters[]{.C035}. We did not establish how the spreadsheet was produced. Separately, the
one-file All-Life table of the Fossil Record 2 compilation has [220]{.C048} rows shifted one column left
relative to its chapter workbooks. Of these, [112]{.C048} shift ranges only, [2]{.C048} shift habitat and
range, and [106]{.C048} move a not-found-in-record flag[]{.C048}. We did not rerun either study's analysis,
and we make no claim about its conclusions.

**Case 11.** A recent analysis of cyclicity in stratigraphic boundaries
[@rampino2025CorrelationCyclicityStratigraphic] states a binomial test with n = [47]{.C190}, k =
[28]{.C190} and p = [0.55]{.C190}, and prints a tail probability of $3.4 \times 10^{-16}$. The stated test
gives [0.316]{.C190}[]{.C190}. We confirmed this by exact rational arithmetic, by integer polynomial
convolution, by a direct exact sum and in R. This does not bear on the paper's separate spectral analysis,
which we did not rerun.

**Case 12.** INDITEK-2.0 [@herrerogascon2026Inditek20] deposits a proof example that uses synthetic
observations, with archived calibration proposals. We reran three archived rejected proposals with the
original pinned harness. Their prediction vectors reproduce within about $5 \times 10^{-14}$ across
[2,978]{.C195} cells[]{.C195}. Their saved residual sums of squares, however, differ from rescoring under
the deposited observations and scorer by [42.4]{.C193}, [17.5]{.C193} and [11.9]{.C193}, and a separately
implemented, model-free scorer agrees with the rescored values[]{.C193}. These are rejected proposals, not
accepted draws. The cause, and any connection to published figures, are unresolved.

## 4. What the auditing agents got wrong

The agents' own errors are part of the record. Replay withdrew or narrowed several original statements:

- **Case 3.** The changed-mean counts of 1,454 and 423 did not reproduce under the pinned recipe, and an
  11–13% sample inflation figure was withdrawn.
- **Case 4.** A sample count that included a header row was corrected to [61,862]{.C040}.
- **Case 5.** "Wrong above every hiatus" was false; the error is confined to affected segments.
- **Case 7.** The "too narrow" diagnosis of PyRate's intervals was not supported.
- **Case 10.** A count of 5,291 cells in scientific notation had been read as a count of damaged
  histories.

The draft of this paper was itself corrected in review. Among other things, the first draft joined the
admtools count from one control with the maximum from another, and attributed the INDITEK archive to the
wrong paper.

Earlier in the programme, the two agents corrected each other's scientific reasoning repeatedly. One
agent's proposed rule, for example, was refuted by the other's counterexample, and a predicted outcome of a
screening test was wrong. These errors were identified during rechecking by a different actor. The series
contains no comparison that could show whether this arrangement catches more errors than any other.

## 5. Recommendations

- **For database providers:** expose versions and change logs for interval ages and records, and say in
  query results when records have been removed or merged.
- **For package authors:** test against known truth, including hiatuses and boundary cases; compare numbers
  as numbers; do not reset the caller's random-number state; document what each reported interval
  measures.
- **For authors of deposits:** deposit identifiers and histories as text in machine-readable formats, not
  in spreadsheets; archive the scorer and observations with any saved calibration scores.
- **For users:** record the date and version of every query; rerun spatial analyses under more than one
  plate model and state the reference frame; replay a published number before building on it.
- **For programmes that use AI agents:** declare tests before running them, keep failed gates, have a
  different actor recheck each finding, and publish reviewed correspondence.

## 6. Discussion

### 6.1 What follows

Each case is small on its own. Together they show problems of several distinct kinds in the layer beneath
published palaeobiology: version changes users need to know about, inconsistencies within a resource,
implementation defects, intervals whose meaning is narrower than their label suggests, and published
numbers that do not survive replay. None needed new data or new theory to find. Each needed a layer to be
replayed against known truth or against its own source.

### 6.2 Which conclusions depend on which assumptions

**Table 2.** Dependence of the main conclusions on their assumptions.

| Conclusion | Rests on | Fails or narrows if |
|----------------|----------------|----------------|
| Each case's proposition holds for the version tested | Pinned inputs and the stated convention | The replay is wrong for those inputs; another version only restricts scope |
| The measured changes are real | The support counts, inputs and EPRP analyses named in each case | The named downstream calculation was misreplayed; effects on published conclusions were not tested |
| The checks add information | A different actor and the routes recorded in each receipt | The routes share an error, such as a common input misread |
| Provider knowledge | Not established | Open: providers may already have documented a behaviour |

### 6.3 What would sharpen the answer

- **Disclosure responses.** Providers' and authors' replies would establish which findings are already
  known, intended or fixed.
- **A controlled comparison.** The same audit run by experienced human auditors would allow the cost and
  yield of agent-assisted auditing to be compared, which this series cannot do.
- **Downstream replays.** Rerunning published analyses that use the affected layers would measure
  consequence for published conclusions directly.
- **A cold public rebuild.** Rebuilding every case from public inputs alone would test how far the
  recorded commands suffice without locally retained images and archives.

## 7. Conclusions

Systematic replay of palaeobiology's shared infrastructure, in one programme, exposed problems of several
kinds. The twelve cases here are each bounded and recorded with a replay command, required inputs and
their hashes, and each was rechecked by a different actor. They are a sample of what one programme found,
not a measure of how often such problems occur. Providers, authors and users can act on them.

## Methods in brief

Supplement S1 gives the case selection and its rules. S2 gives the replay and checks for each case, with
commands. S3 is the audit trail of withdrawn and narrowed statements.

## Roles of AI systems and humans

- **Codex (OpenAI), with GPT-6.1 Sol delegates**
  - took over the programme's database, reference and package work from 28 October;
  - made some original findings, including cases 11 and 12;
  - replayed all twelve cases, built the claims ledger and reviewed this paper's wording.
- **Claude (Anthropic)**, Opus 5.5 in the main session and Claude Sonnet subagents:
  - ran the database, package and reference sessions that made most of the original findings, before
    28 October;
  - compiled the initial 189-row candidate catalogue;
  - chose the twelve cases;
  - wrote the interpretation specification and drafted this paper.
- **Barry W. Brook** facilitated the programme, approved the paper on 25 October 2026, chose this case
  series for development on 8 November 2026, and holds decisions on provider contact, submission and
  release.

The two AI systems reviewed each other's work throughout. Reviewed snapshots of their correspondence are
published in the repository (`docs/correspondence/`), with withheld messages left as placeholders.

## Data and code

The repository is public at <https://github.com/BWBrook/eprp>; code is MIT-licensed and text, figures and
data are CC BY-SA 4.0. The claims ledger (`papers/infrastructure-audit/manuscript/claims.csv`) gives, for
each proposition, the evidence files, the commit at which they were verified and the replay command. Each
replay record names its required inputs and their hashes; some are retained locally (container images,
posterior logs, source archives) and are not redistributed. Third-party sources keep their own licences.
Records absent from public database snapshots are reported as counts only.

## References
