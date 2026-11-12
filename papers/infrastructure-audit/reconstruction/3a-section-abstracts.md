# Step 3a: section abstracts (each at most 300 words)

12 November 2026; revised the same day after Codex's critique (160/3272,
`docs/audits/2026-11-12-section-abstracts-critique.md`). Barry accepted steps 1–2, including organizing
questions in place of post hoc hypotheses ("Accepted, including the framing of the post-hoc hypothesizes
as organising questions"). *Paleobiology* Research Articles follow IMRaD; each section below gets at most
300 words. Citation status is listed at the end.

## Introduction

Large-scale paleobiology works from shared infrastructure rather than from rocks directly. Occurrence
databases such as the Paleobiology Database, published data deposits, geologic time scales, age models,
plate-tectonic reconstructions and analysis packages stand between a fossil and a published diversity
curve, rate or paleolatitudinal gradient. Global diversity analyses illustrate the chain: they combine
database occurrences with explicit choices about preservation, sampling and analysis [@alroy2008]. The
field has a long literature on how the rock record distorts such inference [@raup1972; @smith2001]. The
shared layer adds a second set of dependencies, each maintained by others and each changing over time:
data transformations, software implementations, model choices and the meaning of what each tool reports.
The community has named parts of this layer as priorities. Among the 89 "Big Questions" in paleontology are
questions on data-entry bias, lost historical information, reporting and data integration (AFR2–AFR4, FI1)
[@smith2025IdentifyingBigQuestions]. Guidance on computational reproducibility recommends tracking inputs
and procedures, preserving versions and inspecting intermediate results [@sandve2013].

Checking this layer means comparing data with their sources, running software against known answers,
inspecting code and recomputing published numbers. AI agents can now do that work across a whole research
program and record every step. Here we report what two agents found while building a paleobiology
research program in October–November 2026. We present twelve cases as a case series, organized by three
questions:
1. Where did each finding arise: in a data transformation, an implementation, a model choice or an
   output's meaning?
2. What checks established it?
3. What changed when a second agent re-examined it?

Each case is documented with the evidence and command needed to verify it, and the paper draws out what
researchers, maintainers, journals and agent-based programs can do with the findings.

## Methods

The setting was the Extinction and Paleontology Research Programme, run from October 2026 by two AI agents,
Anthropic's Claude and OpenAI's Codex, with a human facilitator who set direction and held all external
decisions. While vetting research questions, the agents:
- mirrored databases, deposits and plate models with checksums;
- benchmarked analysis packages against simulations with known answers, through declared validation tests
  (with dated amendments and recorded deviations) and exploratory follow-up probes;
- recomputed published numbers.

Three working sessions, for databases, packages and references, logged each finding with its evidence and
checks: 189 initial candidate findings, including positive controls and intended behaviors, and later
additions.

On 8 November 2026 we selected twelve cases for consequence to inference, variety of finding class and
inclusion of positive controls, excluding licensing and bibliographic metadata. On 12 November each case
was coded retrospectively by the dependency checked: one primary kind (data transformation,
implementation, model choice or output meaning), with a secondary kind where needed. Discovery routes were
taken from dated records.

On 8 November an agent other than the original finder replayed each case from pinned inputs. Where
possible, it rederived key numbers by a separate route: independent aggregation, interpolation, geometry or
scoring code, recounts from raw files, or closed-form arithmetic. Each verified proposition entered a
claims ledger with its value, evidence, verifying commit, reproduce command and limits. A wording review
then checked every draft sentence against an interpretation specification. Corrections were logged at each
stage. Versions, environments and input hashes are recorded with each replay, and agent contributions are
disclosed in full.

## Results

Twelve cases span four kinds of dependency (Table 1; Fig. 1).

**Data transformations (Fig. 2).**
- 71,103 of 368,760 molluscan occurrences in a published deposit were absent from the public Paleobiology
  Database snapshot of 23 October 2026, cutting stages passing our regional screen from 14 to 12 of 21.
- Across three snapshot pairs, 460, 317 and 17 intervals changed modal base age.
- Removing 16,260 excess Triton rows changed 1,388 of 2,267 mean absolute paleolatitudes in our analysis.
- 4,111 of 56,387 stored Neptune Sandbox Berlin ages differed by over 0.01 Myr from interpolated ages.

**Implementations (Fig. 3A–B).**
- admtools mis-converted 3,972 of 8,282 heights in a synthetic two-hiatus model.
- fossilbrush compared numbers as text: differences of 10, 100 and 499 passed a threshold of 5.
- 2,967 of 6,562 spreadsheet capture histories differed numerically from the intact binary deposit.
- A printed probability of 3.4 × 10⁻¹⁶ is 0.32 under its stated binomial test.
- Three archived rejected proposals in INDITEK-2's synthetic demonstration reproduced their predictions;
  their saved residual-sum-of-squares scores differed from rescoring by up to 42.4.

**Model choices and output meaning (Fig. 3C–D).**
- PyRate's 95% preservation-rate intervals covered the truth in 81 of 100 and 33 of 50 simulated datasets;
  extinction-time range-end bounds covered it in 1,895–1,909 of 2,000 cases in their own test.
- GRIWM's resampling interval measures sensitivity to dating error.
- Three plate models disagreed on paleolatitude by a median of 2.9° at 10 Ma and 13.6° at 400 Ma; two
  routes to one model differed by age-specific near-rigid rotations.

**Checks and review.** Each finding rests on its own mix of checks (Table 1); INDITEK's paired forward
replay with separately written rescoring. Replay corrected six cases' initial accounts; PyRate's moved from
"too narrow" to "shifted high".

## Discussion

The twelve cases show agents checking four kinds of dependency between rocks and results, with findings
that change what researchers should record, test or interpret.
- **Data transformations** altered inputs before any model ran: deposited records, interval ages, row
  counts and stored ages.
- **Implementations** produced incorrect conversions, flag decisions and numbers.
- **Model choices** carry structural spread: plate reconstructions disagree by degrees.
- **Output meaning** determines which uncertainty a reported interval represents. GRIWM's interval
  captures dating error.

These map onto actions (Table 2):
- **Users** record query dates and versions, compare plate models and replay published numbers before
  reuse.
- **Maintainers** version changes and document what outputs measure.
- **Journals and depositors** require machine-readable deposits with scoring code.
- **Agent-based programs** pair each finding with a second check, as the corrections here motivate, and
  publish their receipts.

The agents' own record is part of the result: replay corrected six initial accounts, and review corrected
this paper's first draft.

Source comparison and known-answer checks of the kind used here could be applied in other fields built on
community databases and shared code, such as biodiversity informatics. That is a proposal for future work.

**Limitations.**
- Cases were selected for consequence, so they describe kinds of finding, not their frequency.
- We replayed published calculations and part of one deposited model, not whole downstream studies.
- Independence varies by check, and some checks share inputs or model family.
- Calibration controls rest on two simulated clades, and one declared agreement gate failed.
- Some inputs are held locally, and a cold public rebuild is untested.
- Providers and authors had not been contacted at the time of writing.

Future work could audit a defined population of dependencies, compare agent and human auditors, and replay
downstream studies.

## Citation status

| Key | Work | Status |
|---|---|---|
| `alroy2008` | Alroy et al. 2008, *Science* 321:97, 10.1126/science.1156963 | Identity verified (Crossref); text checked by Codex (160/3272) for the illustrative use |
| `raup1972` | Raup 1972, *Science* 177:1065, 10.1126/science.177.4054.1065 | Identity verified (Crossref); content use from the standard literature, source check pending |
| `smith2001` | Smith 2001, *Phil. Trans. R. Soc. B* 356:351, 10.1098/rstb.2000.0768 | Identity verified (Crossref); source check pending |
| `smith2025IdentifyingBigQuestions` | Smith et al. 2025, *Paleobiology*, 10.1017/pab.2025.10042 | In the bibliography; AFR2–AFR4 and FI1 checked by Codex |
| `sandve2013` | Sandve et al. 2013, *PLoS Comput. Biol.*, 10.1371/journal.pcbi.1003285 | Identity verified; Rules 1, 3 and 8 checked by Codex |

The GBIF placeholder is dropped: the Discussion now presents wider application as a proposal.
