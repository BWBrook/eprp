# Step 3a: section-abstract critique

12 November 2026. Review of `reconstruction/3a-section-abstracts.md` at `9bf066b`,
requested in Board 160/3269 and accepted at 160/3270. Board 3269 records Barry's
acceptance of steps 1–2 and his direction to continue the reconstruction dialogue
between agents, with his review on the final drafts.

**Recommendation: proceed with targeted revisions before expansion.** The four-kind
structure and organizing questions hold. All four section abstracts meet the hard
300-word cap: Introduction 282, Methods 275, Results 299, Discussion 291, using
whitespace-delimited tokens including list markers and citation placeholders.

Main Codex checked the Introduction, Methods chronology, word counts and integration.
One bounded GPT-6.1 Sol delegate checked Results and Discussion against the ledger and
estimands read-only. No reconstruction, manuscript, ledger, figures or reference files
were changed, and no analyses or builds were run.

## 1. Results balance: settle the architecture now

The four groups answer where findings arose. Lines 95–96 already identify check routes
and six corrected case accounts, so questions 2 and 3 are present. There is no need for
three equally long Results subsections or another analysis campaign.

I recommend making those two answers concrete now, before 3b amplifies the numerical
catalogue. Give one example of a check route and one of a review correction: separate
INDITEK rescoring alongside successful forward replay; or the distinction between PyRate
undercoverage and the earlier interval-width diagnosis. Table 1 can carry the remaining
case-specific routes and changes. Move a few secondary numbers there to create space
within 300 words. This is an editorial recommendation; the current outline already
represents all three questions.

## 2. Introduction: source the context, narrow the reproduction claim

**S1 — major, lines 19–21:** “re-execution as the test” compresses reproducibility,
correctness and validity into one test. Repeating a computation can reproduce an error.
The paper itself uses source comparison, analytic truth, code inspection and arithmetic
as well as execution. Describe what those checks establish, rather than giving execution
exclusive status through an unspecified reproducibility citation.

The gap can rest on the concrete dependency chain and what this case series contributes.
It does not require a claim that earlier researchers neglected this layer, or that AI
performance across a field has already been established.

Source the small context set before expanding the corresponding paragraphs in 3b.
References should return exact source-backed sentences, identifiers and page/section
locations, including what each source does not establish. This can accompany the draft
repairs; it needs no new decision from Barry.

The bounded source check in this review found:

| Context | Evidence checked and drafting consequence |
|---|---|
| Shared-data dependence and sampling | [Alroy et al. (2008)](https://doi.org/10.1126/science.1156963), first-page text, uses PBDB collection/occurrence data and discusses preservation, sampling and analytical choices. It is a concrete illustration, rather than evidence for every dependency listed or a survey of infrastructure scrutiny. An [author-hosted copy](https://people.ucsc.edu/~mclapham/papers/AlroyEtAl2008.pdf) was read after the Smithsonian PDF route failed. |
| Community priorities | [Smith et al. (2025)](https://doi.org/10.1017/pab.2025.10042), Table 3, AFR2–AFR4 (p. 416), and Table 12, FI1 (p. 422), address entry bias, historical information loss, reporting and data integration. The cited priority is real. Name the relevant questions rather than implying that the community specifically endorsed this agent-audit design. The version-of-record PDF was checked against the existing local question extraction. |
| Computational reproducibility | [Sandve et al. (2013)](https://doi.org/10.1371/journal.pcbi.1003285), opening discussion and Rules 1, 3 and 8, support tracking inputs/procedures, preserving versions and inspecting intermediate results. This is methodological guidance, not an empirical demonstration that re-execution alone tests all four dependency kinds. Relevant sections were read from the publisher HTML after browser retrieval failures. |
| Remaining placeholders | The intended Raup/Smith/Benson references were not resolved as a complete source set here. The GBIF placeholder was not checked. Source a precise sampling-bias review where needed; do not attach a GBIF data-quality citation as evidence that this particular agent workflow has transferred successfully. |

This was a targeted citation check on 12 November, using publisher, institutional and
author sources; it was not a literature search establishing novelty or completeness.
Reference and library ownership remains unchanged.

## 3. Discussion: retain recommendations, label prospective applications

**S2 — moderate, lines 117–120:** “Rechecking is integral” is defensible as a
recommendation motivated by the corrections. Put that force in the agent-program action
already listed. The observed result is that replay and wording review corrected the
accounts; there was no comparison isolating the benefit of another actor or model family.

“The approach generalizes to any field” is a universal application claim. Describe
biodiversity informatics as a proposed application of source comparisons and known-answer
checks. A data-quality paper can motivate that application; it cannot demonstrate its
performance. Keep the proposal in Discussion or Future work. Neither statement needs to
be buried in Limitations merely because it is a recommendation or extrapolation.

**S3 — moderate, lines 100–107:** remove the unsupported amplifications:

- “Implementation defects alter outputs silently” implies an unmeasured property across
  the cases. Name the demonstrated incorrect conversions and flag decisions instead.
- “Output meaning matters as much as correctness” asserts an unmeasured comparison.
  “Than its label suggests” adds an assumption about labeling or interpretation. State
  that output meaning determines which uncertainty an interval represents, using the
  dating-error resampling example.
- Tie the opening implication to what researchers should record, test or interpret.
  The series measured inputs, diagnostic support and our own analysis outputs, alongside
  published numerical contracts; it did not measure changes in downstream biological
  conclusions.

These are affirmative, precise statements. They preserve Barry's plain-results rule.

## 4. Methods chronology: distinguish selection from later classification

**S4 — moderate, lines 51–55:** the 8 November selection sought consequence, a variety
of finding classes and positive controls. The specific four-kind coding rule was adopted
on 12 November during reconstruction. State both dates and call the classification
retrospective. “Fixed before drawing figures” is true but leaves its relationship to
selection and the known results unclear. Avoid implying that these exact four classes
were the prospective selection strata, or that “every kind” exhausts possible findings.

Coding should identify the dependency being checked, rather than assign an unestablished
cause. In particular, placing INDITEK under Implementations cannot establish why its
scores disagree: observations, scoring and source-version alternatives remain open.

**S5 — moderate, lines 41–44:** distinguish declared benchmarks from exploratory probes.
`resources/software/bench/README.md` records fossilbrush follow-up shifts chosen after a
smoke run exposed the bug; the calibration replay records an executed hiatus schedule
that differed from its declaration. Existing `VALIDATION_T2.md`, `VALIDATION_T3.md` and
`VALIDATION_T5.md` support the declared-benchmark route. A short statement can name both
routes now; the full Methods/supplement should retain amendments and executed deviations.
The entire discovery program should not acquire a blanket prospective status.

## 5. Result sentences: restore defining objects

**S6 — major:** three compressed results need targeted repairs. Their numerical
magnitudes agree with the ledger; their subjects or relations have broadened.

| Lines in 3a | Evidence and minimal repair |
|---|---|
| 85–86, INDITEK | C193/C195 concern **three archived rejected proposals in a synthetic demonstration**, their prediction vectors and saved **residual-sum-of-squares** scores. Restore these objects so the 42.4 has a defined meaning. Keep the successful forward replay; its reported numerical tolerance belongs in the full case. |
| 92–93, plate-model routes | C123 supports **age-specific near-rigid rotations** at the tested ages. The singular unqualified rotation can suggest one transformation across time. Restore “age-specific.” |
| 82–83, capture histories | C035 is a comparison with the intact binary deposit. Prefer “2,967 of 6,562 spreadsheet capture histories differed numerically from the intact binary deposit.” This states the measured comparison without assigning a damage mechanism. |

The dated PBDB count, our regional screen, Triton means, comparable NSB denominator,
synthetic admtools model, separate PyRate/range-end targets and conditional GRIWM meaning
remain appropriately bounded at this outline stage. Keep their detailed conventions in
Methods, tables/captions and the dedicated Limitations. The latter already retains the
two-clade scope and failed agreement gate. Moving constraints there did not invalidate
these result sentences. The repairs above concern the objects measured, not a demand to
reattach caveats to every result.

## Handoff

Claude should make these targeted repairs, complete the small source-to-sentence check
for the Introduction, and expand from the balanced outline. No full restructuring of
Results, fresh modeling, or further Barry approval is needed for this drafting tranche.
Formal inquiry, disclosure and release retain their existing boundaries.

Verification: read the full new Board messages; compared 3a with the 22 supported ledger
rows, estimands, correction trail, selection note and dated benchmark records; counted
section tokens; and checked the primary-source passages identified above. No fresh
empirical derivations, figure preparation, cold rebuild or manuscript build was performed.

Next: Claude — revise step 3a and source its Introduction before the next expansion.
