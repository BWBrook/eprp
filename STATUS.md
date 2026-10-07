# EPRP current status

Updated: 7 October 2026, Australia/Hobart. Maintainer of this snapshot: Codex;
Claude updated the critique row, next responder and Claude cursor.

**Stage:** foundation complete; scientific orientation proposed. No primary
investigative project is selected or underway.

**Current objective:** obtain Claude's independent critique and agree the first
bounded orientation tasks. The foundation has 14 files, checked local navigation,
four source records with verification limits, and shared operating instructions.

## Work and ownership

| Work | Owner | State | Completion evidence / next action |
| --- | --- | --- | --- |
| Foundation, shared instructions and seed resource register | Codex | Complete | Local links, TSV integrity, ignore rules and source-access notes checked; bundled foundation commit |
| Independent critique and first orientation framing | Claude | Posted; counter-proposal awaiting Codex | Critique in discussion 76; framing in [ideas/2026-10-07-claude-first-framing.md](ideas/2026-10-07-claude-first-framing.md). Proposes splitting work by question family, not by literature/data function |
| Initial resource/data-contract audit | Unassigned | Proposed | Select a small question-relevant slice after the orientation exchange |
| Primary project selection | Barry, informed by both agents | Deferred | Receive a short comparative brief after evidence and feasibility checks |

## Current findings and limits

- Four seed resources cover fossil occurrences, palaeoecological records,
  geological context and preparation software. See [the catalogue](resources/README.md).
- PBDB documentation, the Neotoma API specification and the Macrostrat API
  root returned HTTP 200 from WSL. This is documentation/metadata access, not
  a tested extraction or evidence of adequate scientific coverage.
- No literature synthesis, novelty assessment or representative data audit
  has been completed. No datasets or third-party papers have been imported.
- An independent Codex reviewer challenged the structure; those suggestions
  informed the promotion boundary, evidence labels and limits on active work.
  Claude has not yet reviewed or accepted the proposed division of work.

## Next useful tranche

Recommendation: pair a small biological-question literature map with an audit
of the observations needed to discriminate its competing explanations. Begin
with two contrasting question families, not a bulk database download. Each
agent should first offer their own framing before converging on a joint shortlist.
The [roadmap](docs/programme.md) defines the proposed deliverable and stopping point.

**Next responder:** Codex on discussion 76, to accept, revise or counter
Claude's allocation proposal and offer its own independent framing. No immediate Barry decision is
needed for the foundation or routine orientation. If Claude is unavailable on
a later wake, Codex can take an unowned bounded task and record it; do not claim
mutual agreement or edit work already accepted by Claude.

## Repository and correspondence state

- Verified checkout: `/home/bwbrook/git/eprp`; no remote configured at launch.
- Correspondence project: `eprp` (active); foundation discussion: `76`.
- Source of authority: Barry's launch message in Codex chat, 7 October 2026.
- Additional instruction: future Codex subagents use GPT-6.1 Sol with effort
  matched to the task; recorded in `AGENTS.md`.
- Codex bootstrap task, project inbox `next_after`: `1101`.
- Codex bootstrap task, discussion 76 `next_after`: `1101`.
- Last complete message read and explicitly acknowledged in discussion 76: `1101`.
- Claude onboarding task: read and acknowledged discussion 76 through `1102`;
  Claude's critique follows that message.
- The final committed handoff follows that cursor in discussion 76; read it on
  the next catch-up for the commit hash and receipt. Keeping the earlier cursor
  ensures it is retrieved without a self-referential status commit.
- Other agents must keep their own task cursors and recover the substantive
  context even when the configured participant's shared read marker is newer.

Detailed activity and consequential rationale belong in
[the launch log](logs/2026-10-07-foundation.md), not repeated status prose.
