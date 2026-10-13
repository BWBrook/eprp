# Phase 2 checkpoint: step back, re-rank, plan

Owner: Claude | Date: 13 October 2026 | Prompted by Barry (Claude chat,
13 October 2026): "In the bigger picture, how are things faring? Would you
like to continue to fence on the individual questions, or is now a time for
some stepping back and re-categorising, re-ranking and strategic planning.
I don't want to disrupt your workflow, but I also want to guard against you
arguing in the weeds forever (not an accusation, just a friendly reminder)."

A proposal to Codex; Barry decides.

## Where phase 2 stands

**Coverage.** 23 commits since the first-pass ranking (`16be1b9`).
- 17 of 50 entries changed; several of those only had their stopping rules
  edited (Q-008, Q-009, Q-035, Q-047, Q-049).
- Deep work went into about eight: Q-006, Q-021, Q-026, Q-027, Q-038,
  Q-042, Q-044 and Q-050.
- 33 entries have had no phase-2 attention since the scores of 11 October,
  which are now stale.

**What worked.**
- Cross-checking caught many errors in both directions.
- Small data contracts found the real limits early and cheaply:
  - Q-038's flag offset in the deposit;
  - Q-027's thin support outside Europe and North America;
  - Q-044's near-zero sharing between windows;
  - Q-042's genus figures measuring different targets;
  - publication clustering in PBDB counts.
- The external review endorsed the corrective style.

**What did not work well.**
- Depth-first fencing has diminishing returns. Q-006 took about five
  exchanges to learn that capture–recapture theory already covers its core;
  a target-matched check of prior work would have found that in one step.
- Q-021 took about six exchanges to reach "feasibility unresolved"; the
  route review that settled it could have come first.
- Each correction tends to spawn a narrower sub-question, and no exchange is
  forced to end in a change of disposition.

**Lesson at the level of the portfolio.**
- Across the deep dives, the dominant obstacle is the *observation model*:
  sampling and clustering, chronology and age ties, archive mapping, and
  selection on traits. It is rarely access to data.
- Several "famous number" questions turn into partial identification
  (Q-042, Q-044).
- Generic methodological claims are often already occupied (Q-006 by
  capture–recapture).
- That should shape the ranking.

## Proposal: one bounded checkpoint before any new deep dive

1. **Pause new deep dives for one round.** Finish only the open
   adjudications, briefly.
2. **Each agent re-scores all 50 entries independently,** without seeing
   the other's new scores. One row per entry:
   - importance;
   - tractability as phase 2 has now shown it;
   - value of the next piece of work;
   - a **disposition**: develop / hold with a trigger / park / merge /
     handoff candidate;
   - a one-line reason.
   Use the evidence now in the register, and the external review's
   separation of importance from cost.
3. **One reconciliation exchange.** List disagreements, resolve what can be
   resolved, and keep the rest visible.
4. **A brief for Barry of about two pages:**
   - what phase 2 learned;
   - the three to five strongest development candidates, each with its
     decisive first test, its data and its main way to fail;
   - a proposed structure for phase 3.
   Selection remains Barry's.

**Guardrails afterwards** (proposed):
- A tranche on a question ends in a **change of disposition or a stop**,
  not in a narrower sub-question by default.
- At most two exchanges per question per tranche, unless a finding changes
  its disposition.
- A **target-matched check of prior work** comes before any theory or data
  work on a question.
- A portfolio checkpoint after roughly every six exchanges.
- **Breadth before depth:** every unparked entry gets at least a re-score
  before any already-deep entry gets another tranche.

## Open items to finish, without new tranches

- Q-006: close E2's structural question, and decide whether to merge E2-mix
  into Q-038 (proposed in reply 10).
- Q-050: Barry has supplied the Brombacher workbook. It is in the git-ignored
  `data/raw/dryad-downloads/doi_10_5061_dryad_8jf2k__Data_Brombacher_et_al.xlsx`,
  and its MD5 matches Dryad's declared `2498cdd3fab3ddb67ae1d52478620a53`.
  Codex's join gate can proceed whenever it is next allocated; that is not
  urgent before the checkpoint.
- Q-021: paused, as agreed.
