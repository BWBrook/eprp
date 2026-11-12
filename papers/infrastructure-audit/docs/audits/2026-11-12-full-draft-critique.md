# Step 3c: full-draft critique

12 November 2026. Review of `reconstruction/3c-full-draft.md` at `5577dd8`,
requested in Board 160/3294 and accepted at 3296. Main Codex integrated two
bounded GPT-6.1 Sol scientific/editorial reviews and one mechanical discovery-
route extraction. Draft, manuscript products, bibliography, estimands and
ledger were read-only. Line references below are to this version of 3c.

**Recommendation: targeted revision before porting; retain the lean draft.**
The body has 3,093 whitespace-delimited tokens, Abstract 149 and non-technical
summary 111. The earlier 6,000–7,000 estimate is not a target to fill. Case
detail can stay in Supplement S2, which must be expanded consistently when
porting. The distinct calibration targets, separate admtools controls, GRIWM
interval/RNG properties and INDITEK prediction/score contrast mostly survive
the expansion. Numerical checking passes; several sentences and table cells
still change what those numbers mean.

## The three new choices

### Keep four check families, with definitions that cover the cases

The observed-relation approach is sound. Cases 11 and 12 can sit with
**computation/implementation checks**: comparisons of a published or saved
number with a specified calculation under identified reference inputs.
Reserve “implementation defect” for the demonstrated code failures. For
INDITEK, the reference inputs are the deposited observations; their identity
with the original score-generating inputs is unresolved.

Two other definitions at lines 107–111 need adjustment. PBDB membership and
snapshot-age comparisons do not establish a source→derived-product relation
for every pair being compared. PyRate undercoverage measures operating
characteristics under a simulation design, rather than discovering which
quantity its interval estimates. A workable four-part specification is:

| Family | Observed check |
|---|---|
| Data provenance/transformation | Membership or values compared across identified sources, versions or derived products. |
| Computation/implementation | Retained or published numbers compared with a specified calculation under identified reference inputs. |
| Model sensitivity | Named alternative models compared on shared inputs. |
| Output interpretation/calibration | The target quantity/uncertainty process, and operating characteristics measured in the stated test design. |

These are organizing families of checks. They preserve the current allocation
without adding a fifth class or assigning an unobserved cause. Update labels,
definitions, Table 1 and Figure 1 together; the class counts remain descriptive
of the twelve selected cases.

### Retain the model/interval synthesis, correct the frame attribution

Lines 292–294 accurately describe the uncertainty components in van Hinsbergen
et al., then incorrectly place all of C125's measured spread in the reference-
frame category. C125 compares complete reconstruction models. Use “Our
comparison measures sensitivity to three reconstruction models.” The separate
C123 comparison concerns two routes to a named model. Keep the author's frame
procedure as context without turning it into proof of the archived route's
parameters or the cause of the observed rotations.

### Keep the dedicated Limitations section

Definitions, tested versions, denominators, input objects and conditional
targets belong where they identify a calculation. That is compatible with
Barry's plain-results rule. Keep the scope/generalization limits together.
The explicit cause-open examples at lines 285–286 repeat Limitations and can
be removed; the useful principle that locating a discrepancy differs from
explaining it can stay.

## Required wording repairs

| Location | Problem | Targeted repair |
|---|---|---|
| Abstract 13–16; summary 28–31 | “Pass directly into inference” and “every study … inherits the problem” imply universal downstream effects. “Twelve problems” turns choices and interpretation findings into defects. | Describe findings that **can affect analyses using those resources**; use **twelve findings/cases**. |
| Introduction 45–47, 62 | Raup is still passage-unverified; the broad bias sentence already has a checked review. “Nearest precedent” exceeds the bounded source search. | Use Dillon for the generic context; use Smith only for its supported rock-availability context. Leave Raup's passage in the source queue. Call CORE-Bench **a relevant precedent**. |
| NSB 173–174 | All 61,862 records become samples “with stored ages.” The receipt includes both-undated and recomputation-only records. | **“Contains 61,862 sample records and hole-specific depth–age tie points.”** Keep the correct 56,387 comparable denominator. C040; `data/results/nsb_2023-06-05.json`. |
| fossilbrush 191; Table 1 row 6, 360 | The threshold includes equality; “10–499” asserts an interval of misses contradicted by flagged 50 and 99. | **“At least a threshold.”** List discrete misses **10, 20, 49.9, 100 and 499**, rather than a range. C102 and `software/replay_packages.R:67`. |
| Discussion 274–276 | “A maintainer can reproduce each one” guarantees access/reproduction despite the untested public cold build. | **“A maintainer has a specified check to run.”** Keep access limits in Limitations. |
| Discussion 316–317 | Yesson did not validate names against geographic distributions. | **“Taxonomic checks and coordinate validation against reference distributions.”** The proposed transfer itself is properly labeled. |
| Table 1 rows 10/12, 364/366 | Case 10 loses the predicate of its history count; “scores off” calls disagreement an established scoring error. | State that histories **differ numerically from the intact binary deposit**. State that **saved RSS differs from rescoring under deposited observations**; retain successful vector replay if space permits. C035/C193/C195. |
| Figure 2C/3D captions, 387/393–394 | The plotted objects are underspecified. | Specify full-precision differences among **2,267 comparable lineage-bins**, and the **age-specific cohort reconstructable in all three models**. These define populations, rather than adding caveats. |

The full numerical sentences and the table cells must receive the same semantic
check. In particular, the numeric validator accepts the fossilbrush endpoints
while missing the false range they form.

## Disposition of the five factual checks

1. **Finder/replaying actor, lines 118–119 — replace the universal claim.**
   The [provenance appendix](2026-11-12-full-draft-provenance.md) identifies
   original Codex References/Packages records for cases 11/12 and subsequent
   main/delegated Codex checking roles. Name those roles/routes. Distinguish
   fresh calls from reaggregation of retained fits; retain the original-harness
   reuse for INDITEK. A provider name alone is not an independence argument.

2. **PBDB interval reference, lines 157–158 — resolved.** Add a dated official
   manual entry for [Data Service 1.2, interval RESPONSE](https://paleobiodb.org/data1.2/intervals/list_doc.html#RESPONSE),
   accessed 12 November 2026, as already checked in source slot S01. It defines
   base/top fields and Ma units; C076 supplies the historical modal differences.
   The Peters–McClennen paper is overview context, not the live field citation.

3. **Generator moments, line 241 — move C105 detail to Supplement S2.**
   The main positive-control coverage results already do the interpretive work.
   If retained, name **retained G1/G2 moment checks** rather than implying that
   every generator property was validated. Keep the failed E4 agreement gate
   in Limitations. Express its observed/required agreement in the same units
   (0.91 versus 0.99, or 91% versus 99%).

4. **Discovery column, lines 350–351 — prepared.** The appendix provides twelve
   route entries with dated public records. It distinguishes probes, smoke
   runs, benchmark discovery, review additions and later replay. Some first-
   finder identities remain unestablished; do not infer them from lane labels.
   Keep the six-case account-correction tally distinct from first discovery.

5. **Byline/disclosure and human declarations, lines 396–410 — split the facts.**
   Journal policy resolves the byline/placement part: AI tools are excluded
   from authorship; analytical use belongs in Methods, text generation in an
   acknowledgment/footnote, and visual generation in captions. Include known
   system/version/date/task details; do not impute missing main-model IDs.
   **Current `manuscript/authors.yaml:6` still lists the AI systems as an author,**
   and the build profiles consume that file. Correct it when porting; moving
   the Roles section alone will not fix the emitted byline. Barry's actual
   acknowledgment, funding and interest declarations can remain placeholders
   for his final review. No request for them is needed now.

   Roles should say Barry **endorsed developing the paper idea** on 25 October,
   consistent with the quoted launch decision in the paper README; do not
   imply approval of this unwritten manuscript. Figure-specific AI roles should
   remain prospective until the scripts are linked; this review did not verify
   the draft's claim that the planned figure code has already been written.

The [current author instructions](https://www.cambridge.org/core/journals/paleobiology/information/author-instructions/preparing-your-materials)
support that disclosure disposition. The [current style guide](https://www.cambridge.org/core/services/aop-file-manager/file/699609d0284ce28ed1a44a53/PAB-Paleobiology-style-guide.pdf),
“Abstract Page,” requires the non-technical summary **before** the abstract,
each at most 300 words. Both draft lengths comply; reverse their order on port.

## Editing and porting recommendation

Do not add bulk to reach the old estimate. Table 2 already carries the actions;
replace most of lines 301–307 with a short introduction to that table. Keep
the agents' own drafting-error examples, but remove the repeated assertion
that each correction was found during the already named review stages.
Keep substantive case definitions and distinct controls; these are useful
detail, not overwriting.

Then port the revised main text together with its updated Supplement S2/S3
and author metadata. The present supplement is not yet the full per-case
procedure implied by the new draft. The three display preparations remain
outstanding: exact Triton means, signed NSB differences and the admtools curve.
Captions currently specify future figures; this review did not inspect plots.

Verification run: standalone `claims.py check` reports 22 supported/cited,
zero errors/warnings; Pandoc citeproc resolves the 32 actual citation keys
without warnings. The check markers and discovery records were read; word
counts, source boundaries and actor routes were checked. No source analysis,
replay, build or figure was rerun. The canonical makedoc checkout differs from
the locked revision (`1178639a` versus `3d1934ca`); resolve that deliberately
with the port/build tranche, rather than changing the lock in this review.

Next: Claude — repair the listed semantics and integrate the factual checks before porting.
