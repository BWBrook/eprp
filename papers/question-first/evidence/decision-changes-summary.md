# Decision-change ledger: summary (draft, updated 22 October 2026)

**Rows:** 207 in `decision-changes-draft.tsv`, dated 7–22 October. Basis: 44 quoted, 163 paraphrase. **Every row has now been re-read against its source** (see "Verification sweep" below). 204 rows are changes; 2 are duplicates and 1 is a confirmation.

**By evidence_type:** logic 60, prior-work 34, computation 30, counterexample 26, source-check 22, data-audit 22, human-decision 8, other 5, replication 0.

**By changed_by:** Codex 156, Claude 29, Barry 8, external (GPT-6 Pro review) 7, joint 6, Claude side session 1.

**22 October additions (DC-195 to DC-207):**
- Q-038 oracle corrections (O7, O6b).
- The LOEO restart defect, caught by Codex before any LOEO fit.
- The provisional benchmark contraction.
- The fivefold campaign-cost correction and the withdrawn blanket campaign.
- The scaling-unit reconciliation.
- The pilot's 0/5 convergence screen.
- Q-012:
  - the run-3 reference diagnostics and the run-4 adjudication;
  - two P11 declaration amendments, each found by a pre-benchmark fixture;
  - the side session's Triton finding, which makes the 98 exposure contrasts historical.
- These rows were drafted by Claude from sources read the same day, with no subagent sweep. Two are Claude's own pre-benchmark self-corrections, a class the first sweep under-recorded.

**By consequence** (182 rows of 21 October; classed from the leading phrase, approximate): claim narrowed or corrected 55; design, rule or contract repaired 48; claim, rule or inference withdrawn or rejected 42; disposition change (park, hold, develop, merge, defer) 19; tier, score or priority change 18.

**Most-changed entries** (counted 22 October by the entry's leading label): Q-012 39, programme-level 31, Q-038 24, Q-006 9, Q-021 9, B-001 7, Q-022 and B-003 5 each.

**Reversals inside the ledger:** Q-006 tier 3 then 2 (DC-042, DC-063); Q-016 tier 3 then 2 (DC-043, DC-108); Q-038 deferral lifted (DC-080); Q-012 hold then develop (DC-096).

**Current disposition counts**

| Register | Counts | Counted from |
| --- | --- | --- |
| Applied | under review 38, parked 9, sketch 3 (unparked: 36 tier 2, 5 tier 3) | `ideas/register.md:104-153` |
| Blue-sky | develop 1 (B-002), hold 17 (3 "hold (support)", 1 queued, 1 low), park 0 | `ideas/register-blue-sky.md:103-120`, tally `:122` |
| Checkpoint work dispositions, 14 Oct (no "merged" status exists) | 10 develop, 29 hold, 8 park-category, 3 component merges | `ideas/2026-10-13-phase2-checkpoint-reconciliation.md:68-73` |

**Caveats and coverage**
- Codex dominates changed_by because corrections sit in its review notes and Claude's acceptance tables. Claude's silent self-corrections are under-recorded.
- Initial judgments are mostly reconstructed from the correcting note, hence the paraphrase share.
- Not reliably recorded: board messages absent from the repository; edits visible only in git history; score changes beyond those discussed; minor wording fixes; some repeat steps in the Q-012 pilot.
- Costs are stated for only 11 rows; time and tokens were not instrumented.
- Read in full: STATUS.md, `ideas/framework-notepad.md`, most Codex review notes. Read only at grep-targeted passages: `ideas/register.md`, `ideas/register-blue-sky.md`, other literature and data READMEs. Not covered: `docs/`, `resources/`, raw data, tarballs, and commits after `13f6ae4` (including the untracked P11 v6q80t result). No file was unreadable.
- Quotes are snapped to the record text (markdown emphasis removed, inner double quotes shown as single). Read the TSV with quoting disabled (`csv.QUOTE_NONE`).

**Provenance and verification (Claude, 21 October 2026).**
- **The sweep:** drafted by a Claude Sonnet subagent under Claude Opus 5.5.
- **Its recorded cost:** about 689,000 subagent tokens, 295 tool calls and
  37 minutes. This is the first instrumented cost in the record.
- **Spot check:** Claude checked five randomly sampled rows against their
  cited sources. Each quoted span or paraphrase matches the text at the
  cited lines: DC-003, DC-081, DC-104, DC-140, DC-149.
- **Still to do:** verify every row individually, add a later-reversal
  column, and add costs where the record allows.

**Codex review, 21 October (76/2153;
[2026-10-21-ledger-review-codex.md](2026-10-21-ledger-review-codex.md)).**
- The counts reproduce. The 182 rows are **records, not 182 independent
  decisions**:
  - DC-084 repeats tier changes already recorded in DC-019, 030, 035 and
    071;
  - DC-094 and DC-096 group four or five decisions;
  - DC-075 confirms a status that was parked on entry;
  - DC-096 restates Q-012's "same first step".
- **Repair before exhaustive verification:**
  - add episode, question and proposition IDs;
  - add links for duplication, acceptance, reversal and verification;
  - then build three complete histories first: Q-012, Q-038 and the
    recruitment brief.
- The counts by agent do not compare performance: there is no denominator
  and no counterfactual.
- **The sweep's cost** (689,140 subagent tokens, 295 tool uses,
  2,196,553 ms) comes from the harness's task-notification usage block for
  that subagent, not from the subagent's own report. It is visible to
  Claude, not to Codex. Treat it as scoped to that one sweep.

**Repair in progress (22 October).** The ledger now has 194 rows (DC-183 to
DC-194 were added after the sweep), and four new columns:
- `episode`: assigned for the three complete histories (Q012-E1 to E11,
  Q038-E1 to E6, REC-E2 and E3);
- `relation`: change, duplicate, grouped or confirmation. Codex's flagged
  rows are marked: DC-084 duplicate, DC-094 and DC-096 grouped, DC-075 a
  confirmation;
- `relation_to`;
- `verified`: rows re-read for the histories, plus the five spot checks.

All other rows are still unrepaired and unverified.

**Verification sweep (Claude, 22 October 2026).**
- **Scope:** the 166 rows still marked "no", split across four parallel
  Claude Sonnet 5.5 subagents under Claude Opus 5.5. They were read-only and
  wrote only verdict tables, with 343 tool calls and about 826,000 subagent
  tokens between them.
- **Checks:** each row was checked against its cited passage for verbatim
  quotes, faithful paraphrase, changed_by, evidence_type and date.
- **Result:** 143 verified, 23 corrected, 0 unverifiable. The verdicts and
  the evidence read for each are in `verification-2026-10-22.tsv`.
- **Claude's review before merging:**
  - Claude spot-checked three verdicts against the sources (DC-012,
    DC-068, DC-148) and two structural ones (DC-117, DC-121). All held.
  - Rationale stays in the verification file, not in the ledger fields.
  - Hand-written values replaced four proposals whose text mixed values
    with advice (DC-082, DC-099, DC-117, DC-121).
- **Corrections that change attribution:**
  - DC-019 and DC-084 → joint;
  - DC-033 and DC-068 → Codex (DC-068 was the GPT-6 Pro review's general
    finding, but Codex's own audit fixed Q-008 and Q-009);
  - DC-099 → joint, as "other": Barry asked a question; he did not decide;
  - DC-117 → a confirmation, not a change: Codex's own list already placed
    D1 within Q-012.
- **Corrections of substance:**
  - DC-012: Q-014 went from tier 1 to tier 3 as posed, not to tier 2;
  - DC-121: the baseline change was Claude's own fix, not Codex's;
  - DC-148: the 160-state check stood as reassuring at its scope.
- **Basis:** three "uncertain" basis values became "paraphrase" (DC-027,
  DC-043, DC-076).
- **What "verified" means:** the passage was re-read and the row matches
  it. It does not validate the scientific conclusion. Board messages are
  not in the repository, so rows were settled from files.
- **Not re-examined:** DC-039 and DC-040 were flagged as possible
  duplicates. They record tier changes that followed premise changes
  (DC-036, DC-037), a different judgment, so they stay as changes.
