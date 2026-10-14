# Phase 2 checkpoint: reconciling the two independent passes

Drafted by Claude, 13 October 2026. Revised 14 October to include Codex's
[final check](2026-10-14-phase2-checkpoint-final-check-codex.md)
(76/1607); all its corrections are accepted. Compares:
- [Claude's pass](2026-10-13-phase2-checkpoint-claude.md), frozen at
  `81a7347`; see the erratum appended there;
- [Codex's pass](2026-10-13-phase2-checkpoint-codex.md), frozen at `561862d`.

Each pass was frozen before the other was read. A mechanical check confirms
that both tables cover all 50 IDs once each. The **work dispositions** agree
for 37 entries and differ for 13. That is agreement on dispositions, not on
every score, gate or piece of evidence.

## Corrections accepted

- **Coverage.** 13 register bodies changed and 37 did not, counted as
  changed or unchanged bodies, not as "substantial" revision. Unchanged text
  does not mean no work.
- **Observation problems.** Their recurrence in the deep dives is a lesson
  from selected cases, not a frequency across the portfolio.
- **Q-006 wording.** "Deprioritised; exact E2 identification unresolved".
  Reference reuse describes shared publication labels. It is not by itself a
  conditional-Poisson test, nor proof that a mixture model is needed.

## Where the passes agree (37 of 50)

- **Develop:** Q-004, Q-016, Q-025, Q-030, Q-038.
- **Merge a component:**
  - Q-003 into Q-011;
  - Q-006's observation component into Q-038, with Q-006's rate contrast
    kept distinct.
- **Park-category dispositions:**
  - **new parks:** Q-014, Q-019, Q-029;
  - **retained parks:** Q-001, Q-002, Q-032, Q-043, Q-046. Q-001 and Q-002
    were already parked; my first draft wrongly counted them as new.
- **Hold, with the stated gates:** Q-005, Q-007, Q-008, Q-009, Q-011,
  Q-015, Q-020, Q-021, Q-026, Q-027, Q-028, Q-031, Q-033, Q-036, Q-037,
  Q-039, Q-040, Q-041, Q-044, Q-047, Q-048, Q-049.

## The 13 disagreements and their resolution

| ID | Claude | Codex | Resolution |
| --- | --- | --- | --- |
| Q-010 | Hold | Develop | **Develop** (Codex). Its contrast table, with a stop if capacity is only the fitted richness curve, is the check that settles Claude's tractability doubt |
| Q-012 | Hold, prior check | Develop | **Develop as a prior check** (same first step) |
| Q-017 | Hold, prior check | Develop | **Develop as a prior check** |
| Q-018 | Hold (trigger) | Develop | **Develop as a prior check** (read the near-occupant) |
| Q-024 | Hold, prior check | Develop (reserve) | **Develop as a prior check; reserve** |
| Q-023 | Develop | Hold | **Hold** (Codex). It needs a decision target: which event's interpretation would flip? |
| Q-013 | Develop | Hold | **Hold.** Both require an enumerated species–genus cohort and a recognition criterion. The importance difference (Claude H, Codex 2) stays visible |
| Q-034 | Develop | Hold | **Hold.** Its island estimand is kept separate from Q-004's |
| Q-042 | Develop | Hold | **Hold.** Reopen on a genuine start cohort, with genus-size and retention information and explicit regional-to-global transport |
| Q-050 | Develop narrowly | Hold | **Hold, with joint support unresolved.** A bounded audit of coordinates, sieve selection and depth/age joins may be scheduled after the checkpoint. Workbook access does not pass the gate. Keep the bivariate phenotypic target; P is not G |
| Q-022 | One gate, then decide | Hold | **Hold.** The pre-mortem limits the residual and motivates the hold, but the power calibration was never run, so the power of an incremental event effect remains uncalibrated. No calibration is requested now |
| Q-035 | Park | Hold | **Hold.** It is equivalent in action, with an external trigger (paired chronology) and the outcome-neutral rule |
| Q-045 | Parked | Merge a component into Q-044 | **Q-045 stays parked as a standalone question**; its archived-extract component lives in Q-044 |

**Importance differences, left visible:**
- Q-013: Claude H, Codex 2.
- Q-008, Q-009, Q-020: Codex 3, Claude M.
- Q-016: Claude M–H, Codex 2.

None changes an action now.

## The reconciled portfolio

| Work disposition | Count | Entries |
| --- | --- | --- |
| Develop (bounded first checks) | 10 | Q-004, Q-010, Q-012, Q-016, Q-017, Q-018, Q-024, Q-025, Q-030, Q-038 |
| Hold, with gate or trigger | 29 | All others not listed here |
| Park category | 8 | New: Q-014, Q-019, Q-029. Retained: Q-001, Q-002, Q-032, Q-043, Q-046 |
| Merge a component | 3 | Q-003 into Q-011; Q-006 into Q-038; Q-045 into Q-044 |

Work dispositions are not register statuses. If the changes below were
applied, **nine** register entries would be parked: the eight above plus
Q-045.

**Proposed register changes, for Barry's approval** (each owner applies its
own):
1. Park Q-014, Q-019 and Q-029, keeping their reasons and reopening
   triggers.
2. Annotate Q-003's component in Q-011, Q-006's observation requirements in
   Q-038, and Q-045's existing component in Q-044. Every ID and distinct
   target is kept, and no recipient's gates are retired automatically.
3. Describe Q-006 as "deprioritised; exact E2 identification unresolved".
4. Raise Q-016 from tier 3 to tier 2 for its scientific consequence. Its
   open archive does not demonstrate that forecasting is feasible.

## Queue (two active at a time; conditional beyond the first step)

1. **A bounded sweep of target-matched prior checks**, with **Q-010 (Codex)
   and Q-012 (Claude) first**.
   - Then Claude takes Q-015, Q-017, Q-023 and Q-031; Codex takes Q-018 and
     Q-024.
   - Each product names the closest target-matched prior, the remaining
     contrast, its joint-support gate and a disposition.
   - The sweep is a queue, not a barrier: a candidate's next useful check
     may proceed when its prior check clears.
2. **Conditional next options:**
   - Q-030's outcome-independent forcing catalogue;
   - Q-010's contrast table, whose prior check forms its first part;
   - then Q-025 (one taxon's nested-grain baseline, then a stationary-range
     null) and Q-038 (a prospective predictor contract carrying Q-006's
     observation component).
3. **Retained later options, all conditional:**
   - Q-004 (one clade's matched baseline);
   - Q-016 (one microfossil landmark cohort);
   - Q-012's design step;
   - Q-050's support audit;
   - Q-024 as a reserve.
   None is an automatic commitment.

**Guardrails:**
- a target-matched prior check before modelling, with small access checks
  allowed alongside it;
- two substantive exchanges per question by default, with an exception
  when the next check could change a stated decision;
- each tranche ends with a recorded disposition and reason, and a retained
  hold counts;
- no forced status changes;
- a portfolio checkpoint after roughly six exchanges, as a planning
  reminder, not a hard stop.
