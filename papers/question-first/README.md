# Question first: a methods paper in progress

Status: **work in progress; pieces are collected as the programme runs.** No
manuscript, venue or submission has been decided. Started 21 October 2026.

Barry, Claude chat, 21 October 2026 (exact):

> "this work has been (is) hugely valuable. Too often, people jump quickly
> into new projects, especially with the power of AI workflows behind them.
> But what we've revealed clearly here is that *most* of the time should
> probably be spend ideating, checking, pressure testing, ranking, re-checking,
> etc. the ideas, before any focused project-specific work is done. It's a
> step that's absolutely crucial. There's probably a paper in that idea alone,
> for others thinking of expanding their research portfolio of possibilities
> with frontier AI systems"

and, the same day: "let's start putting together the pieces of the paper in a
separate folder, keeping it very much a WIP at this stage, but building it up
as we go, so that if/when it comes time to write it as a methods
contribution, we'll be well positioned."

## The working thesis

As frontier AI systems cut the cost of *answering* research questions, the
binding constraint moves to *choosing* them. In EPRP, structured adversarial
vetting by two AI agents, with a human facilitator, found most candidate
questions occupied, unanswerable, non-identifiable or under-powered, and
repaired others, before promotion to a primary investigation. Bounded
pilots, such as Q-012's, are part of the vetting. The paper would describe the
method, report what it caught and at what cost, and offer a transferable
template.

This is a hypothesis about our own record, not yet a finding. The outline
lists the evidence each claim needs and what would undercut it.

## What is here

| Path | Contents | Owner |
| --- | --- | --- |
| [outline.md](outline.md) | Section skeleton; each section's claims, evidence pointers and gaps | Joint (Codex 76/2153): Claude maintains the scaffold and ledger; Codex owns evidence review and any section allocated to it |
| [evidence/decision-changes-draft.tsv](evidence/decision-changes-draft.tsv) | Extraction records of changed judgments: 182 from the 21 October sweep, plus later additions (207 at 22 October). They are records, not independent decisions. "Verified" means the source passage was re-read, not that the conclusion is validated. **All 207 rows have now been re-read against their sources** (22 October sweep: 143 verified, 23 corrected; [verdicts](evidence/verification-2026-10-22.tsv)). Read with quoting disabled | Claude (Sonnet sweep, then maintained by Claude); evidence review by Codex |
| [evidence/histories/](evidence/histories/) | **Partial** episode histories for Q-012, Q-038 and the recruitment brief (76/2153). Earlier episodes are not yet verified. Three correction chains have been verified by Codex ([review](evidence/2026-10-22-case-history-review-codex.md)) | Claude; reviewed by Codex |
| [evidence/decision-changes-summary.md](evidence/decision-changes-summary.md) | Counts by type, agent and consequence; current disposition counts; coverage limits; the sweep's own cost, harness-reported to Claude and not independently inspected by Codex | Claude |
| [figures/decision_changes_by_day.png](figures/decision_changes_by_day.png) | **Draft figure:** ledger rows per day, (A) by who changed the judgment and (B) by evidence type. Classes are folded to five per panel; Claude includes the one side-session row. The [TSV](figures/decision_changes_by_day.tsv) is the table view. It is regenerated from the ledger by [the script](figures/decision_changes_by_day.py), with a palette validated for colour-vision deficiency. It shows **records, not a rate**: corrections in Codex's review notes are over-recorded, and Claude's silent self-corrections are under-recorded (summary caveats) | Claude |
| [figures/pipeline_timeline.png](figures/pipeline_timeline.png) | **Draft figure for outline §3:** the pipeline as practised, built from real entries. It shows dated stage events for Q-012 (63), Q-038 (41) and Q-017 (18), marked by event type (entered, artefact, repair, outcome, disposition). The data are in [evidence/pipeline-events.tsv](evidence/pipeline-events.tsv), where every row carries a source pointer. They were extracted on 22 October by a Claude Sonnet 5.5 subagent under Claude Opus 5.5, read-only, in 61 tool calls. Claude spot-checked four rows against their sources. **Extraction caveats:** artefacts are dated by commit, not job date (the Q-012 R00 and P11 runs started a day earlier); the Q-038 deferral and its lift on 11 October are ordered by message ID; Q-017's "develop" is a disposition, while the index shows status "under review" | Claude |

**Related material stays where it lives and is linked, not copied:**
- [ideas/framework-notepad.md](../../ideas/framework-notepad.md): the
  pipeline, roles, failure modes, transfer and seeding sketch;
- the registers ([applied](../../ideas/register.md),
  [blue-sky](../../ideas/register-blue-sky.md));
- the dated `ideas/` and `literature/` notes;
- `STATUS.md`;
- the Correspondence thread `eprp`/76, which Barry is willing to publish
  with the work.

## Rules for building it

- **Evidence-bound.** Every claim points to a dated record, a commit or a
  board message. Agent inference is labelled as inference
  ([docs/evidence.md](../../docs/evidence.md)).
- **Decision changes are recorded in the dated records where they happen**,
  in the four-column form: initial inference, the evidence that changed it,
  the current judgment, and the cost or later check (Codex 76/2138). The
  ledger here indexes them; it does not replace them.
- **Preserve unflattering evidence:** our errors, reversals, dead ends, and
  checks that changed nothing. A methods paper that reports only the catches
  would repeat the failure it describes.
- **AI roles are stated fully,** naming systems and versions (Barry's
  standing instruction):
  - **Claude** (Anthropic), via Claude Code, under the labels Fable and
    Opus. This session is Opus 5.5; earlier sessions' versions are to be
    confirmed from the board's model fields.
  - **Codex** (OpenAI), with GPT-6.1 Sol subagents. The main Codex model
    version is to be confirmed.
  - **GPT-6 Pro**, as external reviewer (11 October) and external
    consultant (21 October).
  - **Sonnet subagents** for bounded searches and sweeps, which must be
    named wherever they contributed.
- **No manuscript drafting yet.** Collect, verify and structure.
  Instrumentation of costs (time, tokens, compute) is an open item, not a
  silent gap.
