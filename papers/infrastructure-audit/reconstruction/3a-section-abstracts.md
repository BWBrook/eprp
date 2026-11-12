# Step 3a: section abstracts (each at most 300 words)

12 November 2026. Barry accepted steps 1–2, including organizing questions in place of post hoc
hypotheses ("Accepted, including the framing of the post-hoc hypothesizes as organising questions").
*Paleobiology* Research Articles follow IMRaD with a short Conclusions section; each section below gets
at most 300 words. `[cite: …]` marks literature still to be sourced and verified.

## Introduction

Large-scale paleobiology works from shared infrastructure rather than from rocks directly. Occurrence
databases such as the Paleobiology Database, published data deposits, geologic time scales, age models,
plate-tectonic reconstructions and analysis packages stand between a fossil and a published rate,
diversity curve or paleolatitudinal gradient [cite: PBDB-era macroevolution, e.g. Alroy et al. 2008].
The field has built a mature literature on how the rock record itself distorts inference, through
sampling, preservation and rock availability [cite: Raup 1972; Smith 2001; Benson et al.]. The
shared layer adds a second set of dependencies, each maintained by others and each changing over time:
data transformations, software implementations, model choices and the meaning of what each tool reports.
The community has named this layer as a priority. Several of the 89 "Big Questions" in paleontology
concern biases, data loss and combinable data [@smith2025IdentifyingBigQuestions]. Reproducibility studies in
neighboring fields establish re-execution as the test of such dependencies [cite: reproducibility
literature].

Checking the layer is broad, detailed work: mirroring sources, running software against known answers,
and recomputing published numbers. AI agents can now carry out such work across a whole research program
and keep a record of every step. Here we report what two agents found while building a paleobiology
research program in October–November 2026. We present twelve cases as a case series organized by three
questions:
1. Where did each finding arise: in a data transformation, an implementation, a model choice or an
   output's meaning?
2. What checks established it?
3. What changed when a second agent re-examined it?

The paper documents each case with the evidence and command needed to verify it, and draws out what
researchers, maintainers, journals and agent-based programs can do with the findings.

## Methods

The setting was the Extinction and Paleontology Research Programme, run from October 2026 by two AI
agents, Anthropic's Claude and OpenAI's Codex, with a human facilitator who set direction and held all
external decisions. While vetting research questions, the agents:
- mirrored databases, deposits and plate models with checksums;
- benchmarked analysis packages against simulations with known answers, declaring tests before running
  them;
- recomputed published numbers.

Three working sessions, for databases, packages and references, logged each finding with its evidence
location and the checks it had received. This produced an initial catalogue of 189 candidate findings,
including positive controls and intended behaviors, and later findings were added as the program
continued.

We selected twelve cases by their consequence for inference, covering every kind of finding and
including positive controls. Licensing and bibliographic-metadata findings were excluded. Each case was
coded by a rule fixed before drawing figures: one primary kind (data transformation, implementation, model
choice or output meaning) and, where needed, a secondary kind. Its discovery route was taken from dated
records.

On 8 November 2026 an agent other than the original finder replayed each case from pinned inputs. Where
possible it rederived key numbers by a separate route: independent aggregation, interpolation, geometry or
scoring code, recounts from raw files, or closed-form arithmetic. Each verified proposition entered a
claims ledger with its value, evidence files, verifying commit, reproduce command and limits. A further
review checked every sentence of the draft against an interpretation specification stating what each case
licenses. Corrections at each stage were logged. Software versions, environments and input hashes are
recorded with each replay. Agent contributions are disclosed in full under journal policy.

## Results

Twelve cases span four kinds of dependency (Table 1; Fig. 1).

**Data transformations (Fig. 2).**
- 71,103 of 368,760 molluscan occurrences in a published deposit were absent from the public
  Paleobiology Database snapshot of 23 October 2026, cutting stages passing our regional screen from 14 to
  12 of 21.
- Across three snapshot pairs, 460, 317 and 17 intervals changed modal base age.
- Removing 16,260 excess Triton rows changed 1,388 of 2,267 mean absolute paleolatitudes in our analysis
  (411 by ≥1°).
- 4,111 of 56,387 stored Neptune Sandbox Berlin sample ages differed by more than 0.01 Myr from ages
  interpolated from its tie points.

**Implementations (Fig. 3A–B).**
- admtools mis-converted 3,972 of 8,282 heights in a synthetic two-hiatus model, by up to 3.0 Myr.
- fossilbrush compared numbers as text: differences of 10, 100 and 499 passed a threshold of 5.
- A deposited spreadsheet altered 2,967 of 6,562 capture histories; Fossil Record 2's one-file table had
  220 rows with left-shifted cells.
- A printed probability of 3.4 × 10⁻¹⁶ is 0.32 under its stated binomial test.
- Three archived INDITEK-2 proposals reproduced their predictions, but their saved scores differed from
  rescoring by up to 42.4.

**Model choices and output meaning (Fig. 3C–D).**
- PyRate's 95% preservation-rate intervals covered the truth in 81 of 100 and 33 of 50 simulated
  datasets; extinction-time range-end bounds covered it in 1,895–1,909 of 2,000 cases in their own test.
- GRIWM's resampling interval measures sensitivity to dating error.
- Three plate models disagreed on paleolatitude by a median of 2.9° at 10 Ma and 13.6° at 400 Ma; two
  routes to one model differed by a near-rigid rotation.

**Checks and review.** Re-execution, recomputation from source, code inspection and arithmetic
established the findings, often combined (Table 1). Replay corrected the initial accounts of six cases.

## Discussion

The twelve cases show that agents can check the four kinds of dependency between rocks and results, and
that each kind can change what a researcher should conclude.
- **Data transformations** alter inputs before any model runs.
- **Implementation defects** alter outputs silently.
- **Model choices** carry structural uncertainty that a single model hides: plate reconstructions
  disagree by degrees.
- **Output meaning** matters as much as correctness. A correctly computed interval can answer a narrower
  question than its label suggests.

These map onto concrete actions (Table 2):
- **Users** record query dates and versions, compare plate models and replay published numbers before
  reuse.
- **Maintainers** version changes and document what outputs measure.
- **Journals and depositors** require machine-readable deposits with scoring code.
- **Agent-based programs** pair each finding with a second check and publish their receipts.

The agents' own record is part of the result: replay corrected six initial accounts, and review corrected
this paper's first draft. Rechecking is integral to agent-based auditing.

The approach generalizes to any field built on community databases and shared code, such as
biodiversity informatics [cite: GBIF-scale data-quality work].

**Limitations.**
- The cases were selected for consequence, so they describe kinds of finding, not their frequency.
- We replayed published calculations and part of one deposited model, not whole downstream studies.
- Independence varies by check, and some checks share inputs or model family.
- Calibration controls rest on two simulated clades, and one declared agreement gate failed.
- Some inputs are held locally, and a cold public rebuild is untested.
- Providers and authors had not been contacted at the time of writing.

Future work could run the same audit on a defined population of dependencies, compare agent and human
auditors, and replay downstream studies.
