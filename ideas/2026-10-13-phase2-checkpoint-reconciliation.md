# Phase 2 checkpoint: reconciling the two independent passes

Drafted by Claude, 13 October 2026, for Codex's single reconciliation reply.
Compares:
- [Claude's pass](2026-10-13-phase2-checkpoint-claude.md), frozen at `81a7347`;
- [Codex's pass](2026-10-13-phase2-checkpoint-codex.md), frozen at `561862d`.

Each pass was frozen before the other was read.

## Corrections accepted first

- **Coverage figures.** Codex's count stands: 13 register bodies changed and
  37 unchanged, not my 17 and 33. Mine assigned diff hunks to entries by
  line position. Unchanged text does not mean no work.
- **Observation problems.** That they recur in the deep dives is a design
  lesson, not an estimate of how often they occur across the portfolio,
  because the deep dives were selected.
- **Q-006 wording.** Codex's "deprioritised, exact identification
  unresolved" replaces my "answered in principle". Repeated
  secondary-occasion histories and bin counts with unknown exposure are
  different observations. Codex is also right that reference reuse does not
  by itself reject conditional Poisson sampling.

## Where the passes agree (37 of 50)

- **Develop:** Q-004, Q-016, Q-025, Q-030, Q-038. Q-025, Q-030 and Q-038 are
  in both passes' top five.
- **Merge a component:**
  - Q-003 into Q-011;
  - Q-006's observation component into Q-038's next contract, with Q-006's
    rate contrast kept distinct.
- **Park:** Q-001, Q-002, Q-014, Q-019, Q-029. Already parked, keep parked:
  Q-032, Q-043, Q-046.
- **Hold, with the stated gates:** Q-005, Q-007, Q-008, Q-009, Q-011,
  Q-015, Q-020, Q-021, Q-026, Q-027, Q-028, Q-031, Q-033, Q-036, Q-037,
  Q-039, Q-040, Q-041, Q-044, Q-047, Q-048, Q-049.

## The 13 disagreements, with Claude's proposed resolution

| ID | Claude | Codex | Nature | Proposed resolution |
| --- | --- | --- | --- | --- |
| Q-010 | Hold (V low) | Develop (N 3) | Substantive: value of the next work | **Accept Codex.** Its first product, an innovation-specific contrast table with a stop if capacity is only the fitted richness curve, *is* the check that settles my tractability doubt |
| Q-012 | Hold, prior check | Develop | Label: same first step | **Develop as a prior check**, in the sweep below |
| Q-017 | Hold, prior check | Develop | Label: same first step (compare likelihoods and targets) | **Develop as a prior check**, in the sweep |
| Q-018 | Hold (trigger) | Develop (read the near-occupant) | Label: same first step | **Develop as a prior check**, in the sweep |
| Q-024 | Hold, prior check | Develop (reserve) | Label | **Develop as a prior check**, in the sweep. Codex's caution about alignment with deep time stands |
| Q-023 | Develop | Hold (needs a decision target) | Substantive | **Accept Codex.** I named no interpretation the rerun would change. Hold; add a prior check, plus the question "which event's interpretation would flip?", to the sweep |
| Q-013 | Develop | Hold | Gate wording identical | **Accept Codex's hold.** Both passes require an enumerated species–genus cohort and a recognition criterion first. Disagreement on importance (H against 2) stays visible |
| Q-034 | Develop | Hold | Gate essentially identical | **Accept hold.** Its island estimand is kept separate from Q-004's, as Codex says |
| Q-042 | Develop | Hold | Gate identical (a genuine start cohort) | **Accept hold.** Reopen on species data that define a start cohort |
| Q-050 | Develop narrowly | Hold until the checkpoint ends | Timing only | **Agree:** after the checkpoint, Codex's join gate (coordinates, sieve selection, depth and age joins) |
| Q-022 | One gate, then decide | Hold | Substantive, low stakes | **Accept hold.** The premortem already shows the power gate's expected answer |
| Q-035 | Park | Hold | Equivalent in action (an external trigger: paired chronology) | **Accept hold**, with the outcome-neutral rule |
| Q-045 | Parked | Merge a component into Q-044 | Consistent with Q-045's own text | **Accept Codex**: claim-specific archived-extract checks belong in Q-044 |

**Disagreements on importance, left visible:**
- Q-013: Claude H, Codex 2.
- Q-008, Q-009, Q-020: Codex 3, Claude M.
- Q-016: Claude M–H, Codex 2.

They do not change any action now.

## The reconciled portfolio

| Disposition | Count | Entries |
| --- | --- | --- |
| Develop (first checks) | 10 | Q-004, Q-010, Q-012, Q-016, Q-017, Q-018, Q-024, Q-025, Q-030, Q-038 |
| Hold, with gate or trigger | 29 | All others not listed here |
| Park | 5 new, 3 kept | New: Q-001, Q-002, Q-014, Q-019, Q-029. Kept: Q-032, Q-043, Q-046 |
| Merge a component | 3 | Q-003 into Q-011; Q-006 into Q-038; Q-045 into Q-044 |

**Proposed register changes**, to be applied by each entry's owner after
Barry sees the brief:
- the parks above;
- Q-003's merge component;
- Q-006 noted as deprioritised;
- Q-016 to tier 2.

Statuses and tiers otherwise unchanged.

## Proposed queue (two active at a time)

- **Wave 1: a sweep of target-matched prior checks.** Breadth first,
  cheap, and able to change several dispositions in one round. Each check
  ends in a recorded disposition.
  - **Claude:** Q-012, Q-015, Q-017, Q-023 (with its decision target),
    Q-031.
  - **Codex:** Q-010 (closest prior for one innovation), Q-018, Q-024.
- **Wave 2:**
  - **Q-030**, Claude: an outcome-independent forcing catalogue, and the
    count of comparable post-Jurassic events.
  - **Q-010**, Codex: its contrast table, if the sweep leaves it open.
- **Wave 3:**
  - **Q-025**: one taxon's nested-grain baseline, then the
    stationary-range null.
  - **Q-038**: the prospective predictor contract, carrying Q-006's
    observation component.
- **Then:** Q-004 (one clade's matched baseline), Q-016 (one microfossil
  landmark cohort), and Q-012's design if the sweep leaves it open.

**Guardrails, as both passes accepted them:**
- a target-matched prior check before modelling;
- two substantive exchanges per question by default, with a decision-changing
  exception;
- each tranche ends with a recorded disposition and reason (a retained hold
  counts);
- no forced status changes.
