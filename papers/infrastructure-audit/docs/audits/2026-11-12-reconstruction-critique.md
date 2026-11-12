# Reconstruction steps 1–2: Codex critique

12 November 2026. Review of `2c4cf4a`, requested in Board discussion 160, message 3253.
The reconstruction, manuscript, interpretation specification and claims ledger were read-only.
Two bounded GPT-6.1 Sol delegates independently examined the scientific framing and display-input
availability; main Codex integrated their findings and checked journal policy. This is a critique,
not approval of a submission or a new analysis campaign.

## Recommendation

Keep the agent-centered message, twelve-case design, American spelling, consolidated Limitations,
and *Paleobiology* Research Article target. Revise steps 1–2 before expanding the paper. The numerical
results agree with the ledger; the material problems concern what the sentences claim, the retrospective
expectations, and the claim that every planned panel is already plot-ready.

The strongest contribution is an inspectable demonstration: agents checked consequential dependencies,
found errors and interpretation pitfalls, and corrected their own accounts. It does not need a new
hypothesis test to become a paper.

## 1. Hypotheses: replace retrospective expectations with questions

**R1 — major: the three expectations were formulated after the findings.** Step 1a explicitly records
that they are new. Step 2's “We expected” and the subsequent assessment read as prospective tests.
Selection for consequence and coverage of finding classes also prevents the selected twelve from
estimating where problems concentrate. A dedicated Limitations paragraph cannot supply the missing
temporal ordering or comparison group.

Use three organizing questions: where did the selected findings arise; what checks established them;
and what changed during review? These preserve the intellectual structure without presenting
post hoc expectations as prior predictions.

- **Hand-offs:** a case map is useful, but layer assignment needs a stated rule. A database update, a
  software type error and a reference-frame choice can all be called hand-offs after inspection. There
  is no denominator of checked hand-offs versus core algorithms. The rival explanation is case
  selection plus flexible classification. Describe the selected cases; remove the concentration claim
  from 1a/1b/2 and the claim that Figure 1A demonstrates hypothesis 1.
- **Execution:** verification and discovery differ. Rerunning a result supports a check; it does not
  show that reading could never reveal the issue. Interval semantics, code inspection and printed
  arithmetic need their actual discovery routes recorded. Replace “only when” and “All twelve surfaced
  through re-running” with a description of the checks used. Table 1 should allow mixed routes.
- **Rechecking:** the audit trail supports corrections during replay and wording review. It does not
  isolate the causal benefit of a second actor, model family or independent implementation. Another
  careful pass with better specified inputs is a rival explanation. Describe the observed corrections
  and the actual route for each check.

**R2 — moderate: define the six and its counting unit.** Supplement S3 has six initial replay rows
covering six cases, followed by four later wording-review rows. A row can hold several numerical or
interpretive propositions. Say that initial accounts of six cases were corrected or narrowed during
replay, and identify that tranche. Do not label the six as an exhaustive count of atomic claims or all
review corrections. Earlier qualification of the universal admtools statement also means that not every
listed correction originated in the November replay.

A prospective comparison would need an eligible audit population, fixed classification and matched
review routes. That is a separate study, not a requirement for this case series.

## 2. One-page paper: correct magnitudes, several imprecise subjects

**R3 — major: retain the measured object in the result sentence.** These are definitions, rather than
caveats that need repeating beside every result. The following are targeted repairs for Claude's next
draft, not an invitation to restore qualification-heavy prose.

| Passage in step 2 | Assessment and repair |
|---|---|
| PBDB absence and 14→12 stages | Counts match C191/C192. Identify the regional presence screen as **our** screen; it is a diagnostic, not a published biological conclusion. Keep the snapshot date. |
| PBDB modal ages | 460/317/17 match C076. The full table/caption should identify the three brackets and later-snapshot occurrence threshold. Changed ages need no defect label. |
| Triton “mean exposures” | 16,260, 1,388/2,267 and 411 match C043/C045. Name these as comparable **mean absolute paleolatitudes in our analysis**. The removal recipe and precision convention belong in Methods/table/caption. |
| NSB ages | 4,111/56,387 and >0.01 Myr match C040. The interpolation and exact-tie convention must remain defined in Methods/Limitations. The sentence correctly reports disagreement. |
| admtools | 3,972/8,282 and about 3.0 Myr correctly belong to the same sparse two-hiatus synthetic model (C096). Keep “synthetic”; do not merge the dense-model maximum into this result. |
| fossilbrush | 10, 100 and 499 at threshold 5 match the numeric-as-text probes (C102). The version and older-than-reference test direction belong in the full case/table. |
| PyRate and classical bounds | Both sets of counts match C107/C194. Explicitly name the latter's target as **extinction-time range-end bounds**. Separate groups and “in their own test” avoid a method ranking. Place two-clade dependence, retained-fit scope and the failed E4 agreement gate together in Limitations; the caption must define any displayed uncertainty. |
| GRIWM | Name the **dating-error resampling interval** or its conditional target (C110). “Extinction-time interval” alone risks repeating the interpretation the case corrects. |
| Plate models | Rounded medians match C125. The full caption must state the point cohort; the all-reconstructable cohort changes with age. This is structural model spread. |
| Spreadsheet and FR2 | 2,967/6,562 match C035. For FR2, “220 rows had left-shifted cell tails” identifies the observed object (C048); those rows have different consequences, not all temporal range shifts. |
| Printed probability | 0.32 is a defensible rounding of C190's 0.315864 under the stated standard binomial contract. Keep the test specified in the full case. |
| INDITEK “model scores” | Too broad for C193/C195. These are **saved residual-sum-of-squares scores for three rejected proposals in a synthetic demonstration**. Include the successful forward prediction replay as well as the score disagreement. This is the largest missing positive result in the compressed account. |

**R4 — major: remove unsupported general and causal claims.** “Far less scrutiny” in step 2 and
“have not been systematically replayed” in 1b require literature evidence. Motivate the work with the
dependence of inference on these shared layers until that evidence is assembled. “AI agents made that
checking feasible” asserts an unmeasured counterfactual; say what the agents actually checked. Step 1a's
“cheaply” and the related reading-versus-execution claims should not survive into products.

Keep one Limitations paragraph. It should collect selection, incomplete downstream-study replay,
check-specific independence, two-clade calibration scope, the failed agreement gate, locally held
inputs/public cold-build status, and disclosure status as space permits. “No published analysis was
re-run” needs precision: published calculations and part of a deposited forward model were replayed;
whole downstream biological studies were not. Provider-contact status needs confirmation before release.

The body from the title onward has 623 whitespace-delimited tokens including headings. The scientific
repairs matter more than cutting twenty words blindly. Removing the retrospective expectations and
unsupported feasibility claim frees space for the missing objects and the positive INDITEK result.

## 3. Main message: retain it, widen the explanatory framing

The main sentence in 1c covers the twelve: agents can check the shared infrastructure and find
verifiable errors and pitfalls. Cases 2 and 9 are consequential version/model choices; GRIWM includes
interpretation and random-stream behavior; the classical bounds are positive controls. Classifying these
plainly supports the capability claim. Calling all twelve defects would undermine it.

“Fidelity” alone is a narrower explanation than the collection supports. Different legitimate plate
models can disagree while each implementation is faithful; a conditional interval can be correctly
computed yet answer a narrower question than a user expects. Frame the shared contribution as checking
**data transformations, implementation, model choices and output meaning**. Table 1 can distinguish
these finding classes. Audience actions then follow from the particular cases rather than a universal
instruction to distrust infrastructure. Their effectiveness is a recommendation, not an observed result.

## 4. Displays: feasible from held material, three preparation tasks

No new external data collection is needed. The statement in 1d that Codex has confirmed every panel's
per-item data are already retained is too strong. Source availability was checked; the extractions and
rerun below were **not** executed in this critique.

Here `R` means `evidence/replay-20261108/`, relative to the paper directory.

| Item | Readiness and source | Required decision or preparation |
|---|---|---|
| Figure 1A | Editorial schematic from ledger and estimands. | Define layer/hand-off coding; present as a map of selected cases. |
| Figure 1B | Catalogue, selection record, ledger and supplement S3 retained. | Label 189 candidate findings, twelve cases and 22 propositions as different units; later additions have no stated total. Use a workflow, not an attrition-rate funnel. Define the six-case correction tranche. |
| Figure 2A | **Ready:** `R/main/case01.json`: 297,657 present, 71,103 absent, 368,760 total. | Counts already committed; no new extraction required. |
| Figure 2B | **Ready:** `R/data/results/pbdb.json`: bracket counts 1, 460, 0, 317, 10, 0, 17; the three large brackets are selected in the text. | Label brackets and ≥50 later-snapshot threshold. These are counts, without comparable-interval denominators for rates. |
| Figure 2C | Paired `R/data/results/{before,after}/q012/lineage_bin_E.tsv` retained at three decimals; full source projection and removal indices also held. | **Recompute full-precision per-bin means** for a plot consistent with 1,388 changes. Rounded tables give 1,385 changed means; both give 411 shifts ≥1°. Account separately for four newly missing bins. |
| Figure 2D | Aggregate `R/data/results/nsb_2023-06-05.json` and source SQLite retained. | **Extract signed per-sample differences** using the recorded interpolation rule; receipt keeps absolute-difference classes only. Histogram denominator is 56,387 comparable samples. Mark both −0.01 and +0.01 Myr, or plot absolute differences. |
| Figure 3A | `R/software/case05_admtools.json` holds ten signed sparse-model height probes plus aggregate grid results. | **Rerun the pinned synthetic conversion** for a full curve; the inspected receipts retain grid summaries, not the 8,282 per-point values. Hiatuses occur at heights 8 and 14 with zero height span: mark boundaries rather than shading fictitious thickness. Label affected interpolation segments separately if shaded. |
| Figure 3B | **Ready:** `R/software/case06_fossilbrush.json` older/younger probes and retained flag grid. | Label numeric truth, text-order result, test direction and threshold. |
| Figure 3C | **Ready counts:** `R/calibration/pyrate_raw.json` and `classical_reaggregate.json`. | Distinct targets in distinct groups. Casewise binomial intervals describe conditional case counts; two generating clades do not supply independent clade replication. Prefer observed coverage plus the nominal line, or label retained intervals explicitly as descriptive. The positive controls do not reverse failed E4. |
| Figure 3D | **Ready:** `R/software/case09_plate_models.json`, three-model age summaries and fixed 194-point cohort. | Choose all reconstructable points with age-specific n, or the fixed cohort. Both are retained. The median pattern is not monotonic. |
| Tables 1–2 | Ledger, estimands and dated discovery/review records support synthesis. | Discovery route and second-check changes require editorial extraction, not inference from the fact that replay succeeded. Table 2 contains recommended actions. |

Supplementary receipts support GRIWM, the two damaged deposits, binomial arithmetic, INDITEK scores,
reference-frame geometry, classical controls and the shifted hiatus arm. Raw bulk files need not be
redistributed to show their recorded aggregate results. The exact cold-reproduction package remains a
separate preparation task.

## 5. Venue, authorship and inquiry

No objection to Barry's chosen first target. The current [author instructions](https://www.cambridge.org/core/journals/paleobiology/information/author-instructions/preparing-your-materials)
allow Research Articles up to 8,500 words and 15 figures/tables, require American English, and welcome
scope inquiries with a title page and abstract. They exclude AI tools from authorship and require
disclosure of substantive AI use: analysis in Methods, generated text in acknowledgments, generated
visual content in captions. Human-only authorship with specific, accurate agent contributions is appropriate.
Describe the actual figure-production role, including agent-written plotting code where used.

**Editorial judgment:** the [journal's scope](https://www.cambridge.org/core/journals/paleobiology/information/about-this-journal)
emphasizes biological processes and patterns. This methodological case series could be useful to that
readership, but its contribution is infrastructure verification rather than a new biological pattern.
A scope inquiry after revising the short draft is worthwhile before expansion. Explain that contribution
directly; adding retrospective hypotheses will not solve a scope mismatch. No inquiry was sent.

The instructions also require reproducibility material accessible in review and a stable public
repository at publication. The held-input and cold-build limitations therefore need a release plan.
The 149-word working abstract is a reconstruction constraint; this review did not establish it as a
journal word limit. The proposed three figures and two tables fit the stated Research Article allowance.

## Handoff and verification

Claude owns the reconstruction. The next bounded tranche is to revise 1a/1b/1d/2 around descriptive
questions, precise result subjects and the corrected display-readiness plan, then return the short
paper for review before step 3. Keep the adopted writing rule and the main message. The three display
preparations can be assigned separately once that plan is agreed.

Verification here comprised ledger/estimand comparison, retained-receipt and source-availability
inspection, the dated correction trail, and current primary journal policy. No fresh fitting, biological
validation, public cold rebuild, figure production or manuscript build was performed. The old four
wording residuals were separately closed in `5f41279`; this review concerns the new reconstruction.

Next: Claude — revise reconstruction steps 1–2 and the display plan.
