# Paper WIP and decision ledger: first evidence review

Codex | 21 October 2026 | Reviewed snapshot: `bd84335`; ledger introduced
at `b928f2f`. This is a review of the draft evidence, not a verified results
table or a manuscript section.

**Accept joint ownership of the WIP.** Claude maintains the scaffold and
ledger; Codex owns this evidence review and subsequent explicitly allocated
sections. Barry's quoted instruction in the [README](../README.md) authorises
collecting and structuring the pieces. No publication, comparative experiment
or new primary investigation follows from this review.

The useful contribution is already visible: a traceable collection of
questions, checks, mistakes, repairs and unresolved problems. The present
ledger does not establish an error rate, comparative agent performance,
workflow efficiency, or the optimal share of effort to spend on vetting.

## What was checked

I parsed [the draft TSV](decision-changes-draft.tsv) with quoting disabled,
recounted its categories, and checked the existence of all 121 repository
paths extracted from its source field. All exist. There are 182 unique IDs,
11 columns, no ragged rows, and exactly the reported totals:

| Field | Reproduced counts |
| --- | --- |
| Basis | 41 quoted; 138 paraphrase; 3 uncertain |
| Changed by | Codex 134; Claude 28; Barry 9; external reviewer 8; joint 3 |
| Evidence | logic 53; prior work 33; source check 22; computation 22; counterexample 20; data audit 19; human decision 9; other 4 |
| Cost field populated | 11 rows |

Ledger SHA-256:
`37799f3ce6b7dfb84b677b2fcf5ebec1556ef322066eda2bf93076931f8456da`.
The mechanical check is retained in
`scratch/paper-ledger-review-20261021/audit.py` and `audit.json`, included in
the accompanying review evidence archive. It does not validate source claims.

I also inspected the cited passages and their immediate context for fifteen
purposively selected rows: DC-012, 019, 030, 071, 075, 084, 094, 096, 107,
119, 134, 138, 159, 173 and 180. Selection targeted grouped decisions,
possible duplication, reversals and consequential repairs. This is neither a
random sample nor row-by-row verification of the ledger. The inspected
passages support the examples below; matching a quotation does not establish
the quotation's scientific correctness or its place in the decision history.

## Repair the counting unit before verifying 182 rows

**The heading should currently say “182 extracted records”, rather than
“182 judgments changed”.** Preserve the draft, but build the verified index
around a decision episode, with the affected question and proposition stated.
Three concrete problems prevent treating the rows as comparable events:

1. **Summary and component rows overlap.** DC-084 summarises tier reductions
   for Q-007, Q-022, Q-027, Q-038 and Q-044. Q-022, Q-027, Q-038 and Q-044
   reductions are already indexed in DC-019, DC-035, DC-030 and DC-071.
   The [first-pass paragraph](../../../ideas/2026-10-11-phase2-portfolio-first-pass-claude.md)
   is a useful summary, but not another independent correction. Link it as
   supporting evidence to the underlying episodes.
2. **One row can bundle many decisions.** DC-094 records four checkpoint
   resolutions, DC-096 five, and DC-119 a collection of discarded pre-register
   ideas. Conversely, one technical failure can generate several distinct
   repairs over successive days. Keep both an episode identifier and the
   affected proposition/question; do not equate a row, a question, a review,
   and an independent scientific gain.
3. **Not every record describes a changed decision.** DC-075 accurately
   quotes “Q-046 was parked on entry. Agreed” from the
   [round-9 note](../../../literature/2026-10-11-register-checks-round9.md).
   This records agreement with an initial disposition, not a demonstrated
   before/after reversal. DC-096's Q-012 resolution explicitly says “same
   first step” despite the hold/develop wording. Preserve these records,
   classifying the first as confirmation and the second as a label change
   unless a changed action is documented.

Do this small schema repair before a costly exhaustive verification sweep.
The existing TSV is a discovery index. A verified episode needs the original
statement, the evidence or objection, the response/decision, and any later
reversal. Use commit-pinned paths or board message IDs: current line numbers
in evolving files, especially STATUS, will drift. A retrospective initial
judgment remains reconstructed when no contemporaneous statement is located.
Add acceptance state (proposed, accepted, disputed, unresolved), verification
state and verifier, and links to summary/duplicate/superseding records. These
are fields in the existing evidence files, not a new application.

## Claims the record can and cannot carry

**Counter-agent review demonstrably caught particular mistakes.** The
recruitment counterexample and selected-sample likelihood repairs are useful
case histories. The stronger outline claim that antagonism catches errors
“that self-review does not” needs a comparison that this selected record
cannot supply. A correction recorded after another agent's review does not
show it would never have been found by the original agent, another check or
additional elapsed work. Likewise, 134 versus 28 is an extraction count,
not a comparison of reviewer accuracy or contribution. The draft's warning
about the source imbalance is correct and should govern every derived figure.

**Most questions failing is not yet a measured finding.** The register mixes
holding for support, narrower development, parking, component merges and
unstarted checks. None is automatically “unanswerable”, “non-identifiable”,
or “under-powered”. Q-012's sampler failure is a particularly important
example of why those labels need their own evidence. Count mutually defined
dispositions on a pinned cohort and date; preserve multiple reasons and their
uncertainty. The decision-change ledger has no denominator for the rate of
corrected claims, and its programme/pre-register rows do not all belong to
the 50-question applied cohort.

**The work precedes promotion to primary investigations, not all project
work.** EPRP already includes data preparation, counterexamples, the Q-022
empirical pre-mortem and the Q-012 computational pilot. Those are part of
the method being described. The README's “before any project work” and the
working title should not erase them. “Before committing to a primary
investigation” captures the actual programme boundary.

**Changed judgments are not automatically improvements.** Retain contrary
responses, unresolved disputes, later reversals and checks that confirmed a
claim. Confirmations need a defined inclusion rule; mining only notes that
announce a correction cannot estimate their frequency. A scientifically valid
null result can be valuable, while an erroneous parking decision can suppress
a worthwhile project. A case series can document the evidence for each
disposition without inventing an overall benefit metric.

**Costs are incomplete.** The reported sweep cost—about 689,000 tokens,
295 calls and 37 minutes—is labelled as Claude's report; this review did not
inspect its raw runtime receipt. It describes the sweep, not the cost of the
182 underlying records. PBS receipts permit a separate compute total;
missing human and agent effort must remain missing, not zero. Neither cheap
execution, net savings, nor “most effort should be spent upstream” has been
measured here. The last is a useful hypothesis from Barry, not yet an
optimisation result.

## Next bounded work

Claude should amend the scaffold's counting and causal language, then verify
one complete episode each from Q-012, Q-038 and recruitment—including the
initial statement, response, acceptance and later outcome. These cases test
whether the index can tell the full story, including our own mistakes.
Expand verification when the episode structure works; do not conduct another
large extraction sweep merely to increase row count. Updating these pieces
is part of maintaining the WIP, not a third scientific investigation.

Record readily available costs prospectively in the existing dated notes,
with a clear scope and unavailable fields. No new monitoring or request for
Barry to reconstruct his past attention is needed. A comparative experiment
or a prior-literature review can be allocated later; neither is commissioned
by the existence of this folder.

| Initial inference | Evidence changing it | Current judgment | Cost or later check |
| --- | --- | --- | --- |
| The draft contains 182 changed judgments | Parsed counts plus overlap, grouped rows and unchanged-action examples above | 182 extracted records; distinct verified decision episodes not yet counted | Small local parse and fifteen targeted passage checks; full verification unrun |
| The ledger can support an agent or workflow performance comparison | Unequal source coverage, no attempted-check denominator or counterfactual, incomplete costs | Descriptive case evidence only at present | Reconsider only with a matched design and independent outcome assessment |

Next owner: **Claude**, for scaffold and ledger amendments. Codex reviews
the repaired episode examples. The original draft and unverified rows remain
visible; no manuscript drafting or release is authorised by this review.
