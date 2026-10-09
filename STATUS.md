# EPRP current status

Updated: 9 October 2026, Australia/Hobart. Maintainer of this snapshot: Codex.

**Stage:** continuous ideation. Barry (9 October): the programme's output is a
growing, continuously revised [question register](ideas/register.md) of big,
well-posed questions for other teams, not a single target. Deep time has
particular interest.

**Current objective:** grow and refine the register. Every round both narrows
(prior-work and feasibility checks; park or reject with reasons) and expands
(new sketches). Map consequential questions, nearest prior work and usable
evidence together. Develop competing explanations and discover
what existing data and modern inference/simulation can genuinely distinguish.
Do not organise the programme around Barry's previous specialisms.

## Work and ownership

| Work | Owner | State / next action |
| --- | --- | --- |
| Foundation and private GitHub remote | Codex | Complete; private `BWBrook/eprp`, `origin` configured; commit/push evidence in discussion 76 |
| First independent framing | Claude | Reviewed by Codex; [original framing](ideas/2026-10-07-claude-first-framing.md) preserved |
| Environmental disruption, susceptibility and cross-scale inference | Claude | Register round 1 done ([checks](literature/2026-10-09-register-checks-round1.md)). Q-011 and Q-015 under review at tier 2; Q-012 (reframed) and Q-013 promising at tier 2; Q-014 at tier 3. Q-007 Cenozoic support is inadequate across events; an Eocene–Oligocene pilot only, gated on the full Triton site table. Added Q-022 to Q-025. Claude next: the Triton gate on deep-server; prior-work checks for Q-022 and Q-023 |
| Recovery, historical contingency and regulation of deep-time diversity | Codex | Expanded Q-008–Q-010 and added Q-020–Q-021: [source synthesis](literature/2026-10-09-register-expansion.md). All five under review, tier 2; generic versions substantially occupied. Retains PBDB regional-support preparation, with a concrete support check next; Claude to challenge formulations and Q-007/Q-015 objections |
| Downstream investigation handoffs | Barry and future project teams, informed by both agents | The hub continuously develops a portfolio. No single programme target selected; no entry yet ready for handoff |

Each scientific area includes literature, data and methods end to end. These
are starting areas for exploration, not an exclusive two-topic agenda. The
previous proposed Codex Late Quaternary assignment is superseded. The revised
division was accepted in messages 1106 and 1127: selectivity and rate-estimator
methods sit with Claude; consequences, recovery and diversity regulation with
Codex. Shared dependencies are coordinated through Correspondence.

## Evidence and unresolved points

- Four infrastructure seeds remain in the [catalogue](resources/README.md).
  Their checks establish documentation/metadata access, not data suitability.
- Claude's initial literature leads were checked at metadata/abstract depth.
  Codex has now inspected selected primary-text sections for several leads
  and competing deep-time models; precise access depth is in the response note.
- Song et al. explicitly acknowledge temporal-resolution limits, so a proposed
  contribution cannot rest on claiming they overlooked them. Their joint
  magnitude/rate argument needs a more careful critique than rate exceedance alone.
- INDITEK carries richness on geological particles; SNCI redraws niches in each
  environmental snapshot. Neither carries identifiable fossil lineages. Source
  inspection found calibration-driver and connectivity issues requiring checks
  before reuse; effects on published results remain untested. Shared source
  families do not establish identical calibration targets.
- Instantaneous environmental tracking, finite-rate state dynamics and additional
  history dependence are distinct hypotheses. A small synthetic probe shows
  that shared observation errors and smoothing can create apparent delayed
  rebound even with constant true richness; it is not an empirical bias estimate.
- The physiology-transfer candidate needs a thermal-exposure comparator and
  frozen calibration choices. Magnitude is not automatically portable across
  observation windows. A failed simulation fit is not proof of structural
  nonidentifiability.
- The [PhanDA source audit](literature/2026-10-08-phanda-ensemble-contract.md)
  confirms pooled fits, filtering and resampling. Matching member positions do
  not certify temporal trajectories; independence is a sensitivity assumption,
  not a general uncertainty bound. The interval crosswalk remains descriptive.
- Claude's original full-independence sampler selected older scenarios by block,
  producing incorrect marginal weights. The independent corrected diagnostic
  gives 10 sign-resolved pairs rather than 9; the other three chosen couplings
  stand. Four signs have separate >95% lower bounds under every coupling of the
  deposited empirical marginals. This does not identify a temporal posterior.
- The original end-Permian temperature/O2 deposit was located through Penn
  2018's data statement. The earlier missing-source inference is withdrawn.
  Units, physical depths, geometry and distinct 2018/2022 calibration assumptions
  still need a reproduction contract; other-event forcing remains unresolved.
- Alroy 2010 does not report the proposed regional holdout test. Close 2020's
  standardised spatial samples are not continuous fixed-region trajectories.
  This narrows the next feasibility check without establishing novelty.
- No candidate's novelty is established. No primary empirical analysis, climate
  simulation or full occurrence-data extraction has started. Only bounded source
  inspections and small synthetic/deterministic probes have been run.
- The register now has 21 entries. New Codex directions concern failure of
  geographic insurance and biological control of Earth-system recovery. Close
  precedents are recorded; discriminating predictions, not broad themes, need
  further evaluation.
- Functional/taxonomic recovery decoupling and global bioregional turnover are
  established. Q-008/Q-009 now ask whether these states predict subsequent
  behaviour. Q-010 retires an either/or capacity-versus-dynamics framing.
- CENOGRID's composite proxy path does not alone establish local environmental
  exposure or continuous fossil support. Susceptibility traits may affect both
  loss and recovery. These are constraints for Claude's accepted support check.

## Next exchange

**Next scientific responder: Codex**, on discussion 76 (Claude's critique of Q-008 to
Q-010, Q-020 and Q-021; register round 1) and 82 (Cenozoic audit result: support
inadequate across events). Both agents keep narrowing and expanding the register
without returning routine choices to Barry.

## Shared checkout and decisions

- Checkout: `/home/bwbrook/git/eprp`.
- Private remote: [BWBrook/eprp](https://github.com/BWBrook/eprp).
- Correspondence: active project `eprp`; foundation/division in `76`, disruption
  review in `77`, with the recovery orientation handed off in a separate discussion.
- Authority: Barry's launch and follow-up decisions in Codex chat, 7 October
  2026; the hosting/deep-time steer is relayed in message 1104.
- Codex subagents: GPT-6.1 Sol, effort commensurate with the task.
- Compute (Barry in Claude chat, 8 October): TPAC `kunanyi` allocation permits
  a 48-node × 28-CPU PBS job. Barry must open the TPAC authorisation jumpbox
  before agents probe it. Operational rules: `~/work/nectar/docs/machines/kunanyi.md`.
- Stage owned paths only and inspect the whole Git index before committing.
- Runtime restored on 8 October after Barry changed permissions. Codex verified
  both shell probes and a clean local checkout matching remote bfda1c7 at 16:46
  AEDT. Claude had already safely incorporated the earlier GitHub-written notes.
- Routine process-document expansion is frozen. Operational read cursors stay
  in task-local state; recover substantive context before acknowledging messages.
