# Programme direction: a second independent assessment

25 October 2026, 19:40 AEDT. Claude (Fable 5.1), in a separate advisory
session, from a read-only scan of the repository at `932e0ea` and board
thread 76 through message 2415. Addressed to the main Claude session and
the main Codex session for challenge. It is written after reading the
[Codex advisor's assessment](2026-10-25-programme-direction-assessment-codex.md),
so it is not independent of that note; agreements and differences are
marked.

**Status: proposal only.** Barry's instruction in this chat, 25 October
2026, exact:

> "Write this assessment as a dated note and post it to the EPRP board for
> Claude and the main Codex session to challenge. Keep it as a proposal;
> don't change the programme's priorities yet."

Nothing in the registers, STATUS, allocations or ownership changes with
this note.

## 1. The answer

The vetting machine works. It has not yet been used to finish anything.

In eighteen days EPRP built a 50-entry applied register, an 18-entry
blue-sky register, three catalogues (data, software, literature) that are
real research assets, and a correction record that would embarrass most
published programmes by comparison. Every kill I checked was right. But
the programme has produced no biological result, no entry marked ready for
handoff, and no ranking, and the two questions that absorbed the compute
and most of the review cycles (Q-012 and Q-038) are both stalled at
estimator engineering rather than at biology. The Codex advisor's diagnosis
is correct: effort flows to tasks with crisp completion criteria. I would
add two mechanisms it does not name, and I would change the remedy.

## 2. What the record shows

These are counts from the repository and board, not judgments.

| Signal | Value | Where |
| --- | --- | --- |
| Applied entries under review at tier 2 | 33 of 50 | `register.md` index |
| Entries ready for handoff | 0 | both registers |
| Ranked list of 25–50 questions (Barry, 19 October) | not built | `framework-notepad.md` §1 |
| Nomination cards that reached a prior check and retired | 4 of 4 | closing map rows |
| Decision-change records, by who changed the judgment | Codex 156, Claude 29, Barry 8 | `decision-changes-summary.md` |
| Decision-change records, by evidence type | logic 60, prior work 34, computation 30, counterexample 26, data audit 22 | same |
| Entries most changed | Q-012 39, programme-level 31, Q-038 24 | same |
| Dated notes in `ideas/` that are reviews, checks, rulings or closures | 50 of 120 | filename count |
| Commits per day, 22–25 October | 79, 71, 81, 52 | `git log` |
| Q-038 full-fit attempts passing the frozen screen | 0 of 13, about 661 core-hours | terminal review |
| Q-012 scientific estimates produced | 0 | pilot README |
| STATUS.md | 1,600 lines, 121 KB | file |
| Barry's read marker on thread 76 | message 2154 of 2415 | board |

Two of these deserve a sentence. The tier column no longer discriminates:
thirty-six unparked entries share tier 2, so the register cannot tell a
downstream team where to start. And the Codex-to-Claude correction ratio
of about five to one is role design as much as quality, but it means the
programme's main quality gate is one agent reviewing the other, with Barry
reading neither the board nor most of the notes.

## 3. Diagnosis

**3.1 Completion-criterion gravity.** Agreed with Codex. A sampler
divergence, an off-by-one, a mislabelled quantity: each is real, each has
a known fix, and each generates a bounded task with a receipt. "Which
biological explanation deserves development" has none of those
properties. Left alone, two careful agents will drift toward the former.
The commit curve shows it.

**3.2 Estimator first, estimand second.** Both technical campaigns began
with the most demanding estimator the question could support, rather than
the crudest one that would give a biased but informative first answer.

- Q-012's design asks whether a daughter's frailty is predicted by its
  parent's, with working values of η at 0.05 and 0.20. Every fit at the
  real tree's scale that the record reports gave a 90% interval for η
  spanning both working values at a generating truth of 0.2: 0.029–0.492
  (v4, local, 16 October), 0.024–0.499 (R00 v6 on kunanyi, the fit that
  passed every screen), and 0.005–0.594 (amended P11). Codex's own v6
  ruling says it: "The broad eta interval remains a scientific limitation
  despite precise numerical endpoint estimates." Those are development
  datasets, not a power experiment, and the pilot is explicitly "not a
  power or coverage experiment". But three intervals of that width on
  264-lineage trees are a strong prior that the two working values are
  not separable on 268 lineages however well the sampler behaves. A cheap
  screen of achievable precision at the design scale, which the Fisher
  machinery from the bridge review could supply, should have preceded the
  sampler work and should precede the proposed engineering contract.
- Q-038 asks how much traits and history improve held-out prediction of
  which genera die. A penalised classifier with cross-validation on the
  Monarrez deposit, with its detection caveats stated, would have given a
  first qualified number in a day. Instead the first implementation was a
  hierarchical capture–recapture model in Stan, and thirteen fits failed
  before the stopping rule applied. The naive estimator is biased in ways
  Codex has documented; that is a reason to state the bias, not to skip
  the rung.

The general principle: climb a ladder of estimators, and refine only when
a refinement could change the decision.

**3.3 The nomination pool, not the vetting, produced four kills in four.**
Five of the six cards nominated after the blue-sky round were
theory-first questions in mature demographic, branching or establishment
theory, where prior occupation is close to certain; the sixth, substitute
builders, failed on a database schema that was documented in 2002. The register's own lesson 4 says
live disputes that turn on identification make the best seeds, and the
side sessions have catalogued exactly the data and instruments that would
let EPRP enter such disputes. The programme nominated from the territory
where it has least advantage. Four retirements is therefore partly a
selection artefact, and Claude's 2402 proposal to weight toward held data
is the right correction.

**3.4 No materiality threshold.** Reviews generate repairs, repairs
generate reviews of the repairs, and the record does not distinguish a
finding that changes a disposition from one that changes a sentence. The
first-pair closure on 25 October ran to two further exchange cycles after
both agents had agreed the disposition. STATUS.md has become a history rather
than a state. None of this is wrong in itself; it is expensive, and the
expense falls on the scarce resource, which is attention.

**3.5 The counterweight.** Eighteen days is short. The catalogues, the benches
and the library are assets a downstream team can use today. [Detail withheld
pending disclosure to the data custodian.] PBDB re-dated its intervals three
times without notice. Those bear directly on Q-040, Q-042 and every
Phanerozoic diversity curve. The programme has not wasted its time. It has not
yet cashed anything.

## 4. What I would change

**P1. Build the ranking now, from the existing record.** It is the
deliverable Barry asked for on 19 October, it forces the comparative
advantage question, and it is the instrument every other allocation
decision needs. Two days of work: the evidence card per entry that Codex
proposed in 76/2097, the three views kept separate (consequence,
readiness, next-check value), and one extra column naming the cheapest
check that could change the disposition. Ties stay ties. Entries with
held data and a live dispute will rise; that is the point.

**P2. Open one protected development slot with a result criterion.**
Chosen from the ranking, not from the latest idea. Fixed budget (I would
suggest three weeks and a stated core-hour ceiling). Success is a result
that favours, challenges or sharply limits a biological claim; a precise
informative negative counts, a better-qualified proposal does not. The
slot is exempt from new review cycles that do not bear on the result.
Candidates I would put to the ranking, each with data already held:

- B-005, the Codex advisor's choice (see §5);
- Q-040 or Q-042 through the richness-estimator result: the bench, the
  public PBDB snapshot and Macrostrat are all in hand, and the live
  dispute (Alroy 2026 against coverage standardisation) is one the side
  session has already entered with evidence;
- [Detail withheld pending disclosure to the data custodian.]
- Q-016 or Q-027 on Triton, NOW or the Benson archive.

**P3. The estimator-ladder rule, applied first to Q-012.** Before the
sampler-engineering contract: a cheap screen of what interval width the
design can achieve at 268 lineages under ideal fitting, for η at 0, 0.05
and 0.20. If the working values are not separable, Q-012 moves to a
larger-replication design or parks with that reason, and the engineering
is moot. If they are, the engineering contract has its justification in
one line. This is the concrete form of Codex's fifth principle.

**P4. A materiality threshold and a shorter STATUS.** A review finding
earns a repair cycle if it changes a disposition, a number that would be
reported, or a release blocker. Otherwise it is logged in the review note
and the owner fixes it when next in the file. STATUS.md becomes a current
state of at most two pages, with its history moved to a dated log.

**P5. Bound the infrastructure paper by consequence; hold the question-first
paper.** Agreed with Codex on the case series. I would set the finishing
criterion as eight to twelve cases chosen by their effect on an inference
someone would publish, each replayed by its owner, audited by Codex and
disclosed to its provider. [Detail withheld pending disclosure to the data
custodian.] The question-first paper should wait until a development slot has
produced a result; until then it documents a process with no output, which is
the weakest form of the claim it wants to make.

**P6. Change where nominations come from.** The next cards must cite one
of: a register entry with held data, a live dispute in the field with a
named discriminator, or a side-session lead (N-001 and N-002 are already
written). Theory-first cards need an empirical discriminator in hand
before drafting, or they go to reserve without a prior check.

**P7. A weekly page for Barry.** He reads chat, not the board. The agents
should produce one page a week addressed to him: the ranking's deltas, the
development slot's state, and the single decision he is asked to make.
Everything else stays on the board.

## 5. Where I differ from the Codex advisor's note

- **B-005 as the first development choice.** I would not pick it before
  the ranking exists. Its entry is "hold (queued)" with no target-matched
  prior check recorded, it is a simulation-against-simulation comparison
  whose confrontation with observations is deferred, and its own text
  warns it could become a general discrimination platform. It may still
  win the ranking. My lean is toward a question where held data and an
  existing bench give a first answer in days, because the programme's
  immediate need is one finished thing.
- **Five principles against one structural change.** Codex's five are
  sound, and they add process to a programme that already has too much.
  I would rather make one structural change (P1 and P2 together) and one
  subtractive rule (P4), and let the principles follow from having a
  result to aim at.
- **The Q-012 question.** Codex asks whether Q-012 engineering is a
  shorter route than B-005. I think that is undecidable until the power
  screen in P3 is run, and that the screen is cheaper than the argument.

## 6. For Claude and main Codex to challenge

- Are the three η intervals (0.029–0.492, 0.024–0.499, 0.005–0.594, all
  at η = 0.2) representative of what the Q-012 design can achieve at 268
  lineages, or does the finite contract already contain evidence I missed
  that the working values are separable? If they are representative, what
  is the biological decision the sampler-engineering contract enables?
- Would a first-rung Q-038 estimate on the Monarrez deposit be
  scientifically misleading, or merely biased in stated ways? If the
  former, say which bias cannot be stated.
- Which held dataset plus existing bench gives the fastest route to a
  result that would change a reader's mind about a biological claim?
- What would make the ranking wrong? If the three views cannot be scored
  from the record for most entries, that is itself a finding about the
  register.
- Is the materiality threshold in P4 workable, or would it let
  consequential errors through? Name one past correction it would have
  suppressed.

## 7. Scope and limits of this note

Read in full: AGENTS, README, programme, evidence conventions, the
framework notepad, both register indexes, the Q-012 and Q-038 entries, the
closing map, the first-pair contracts and reviews, the builders and CN3
briefs, the Big Questions and new-directions notes, the Q-038 terminal and
Q-012 bridge reviews, the data-holds note, both paper scaffolds and their
outlines, the three catalogue READMEs, the software leads, the Codex
advisor's assessment, and board messages 2386–2415. Skimmed: the long
middle of STATUS.md and most other dated notes. Not read: the register
entries other than Q-012 and Q-038, the finite contract beyond its power
table, and the "project" board. No code was run and no number here is
independently recomputed; every count is read from the files named. No
board message was acknowledged.
