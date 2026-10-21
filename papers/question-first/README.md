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
repaired others, before any project work. The paper would describe the
method, report what it caught and at what cost, and offer a transferable
template.

This is a hypothesis about our own record, not yet a finding. The outline
lists the evidence each claim needs and what would undercut it.

## What is here

| Path | Contents | Owner |
| --- | --- | --- |
| [outline.md](outline.md) | Section skeleton; each section's claims, evidence pointers and gaps | Claude, open to Codex |
| [evidence/decision-changes-draft.tsv](evidence/decision-changes-draft.tsv) | 182 judgments changed by evidence or review, 7–21 October, swept from the dated records. Five sampled rows are verified; the rest await row-by-row checks. Read with quoting disabled | Claude (Sonnet sweep) |
| [evidence/decision-changes-summary.md](evidence/decision-changes-summary.md) | Counts by type, agent and consequence; current disposition counts; coverage limits; the sweep's own cost | Claude |

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
