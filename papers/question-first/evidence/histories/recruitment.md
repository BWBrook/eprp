# Case history: the recruitment-failure brief (an outside idea)

WIP | Claude | 21 October 2026. One of the three complete histories (Codex
76/2153). The idea came from a GPT-6 Pro brief commissioned by Barry and
filed in `docs/review/2026-10-21-gpt6pro-proposals/recruitment/`.

| Episode | Date | Initial judgment (owner) | Evidence that changed it (by) | Current judgment | Rows | Source | Verified |
| --- | --- | --- | --- | --- | --- | --- | --- |
| E1: intake | 21 Oct | The brief claims weak K–Pg developmental selectivity (17/28 against 14/23) as a puzzle (GPT-6 Pro) | Recalculation: 95% interval about ±25 points (Claude; reproduced by Codex) | The hook is a power problem, not established equivalence | — (agreement, not a change) | `ideas/2026-10-21-gpt6pro-proposals-assessment-claude.md` | yes |
| E2: Claude's analytic gate | 21 Oct | D* ≈ ln N_A/μ means larval-only failure cannot extinguish widespread species, **"so R_L should be small"** (Claude) | Exact birth–death and pulse-breeding counterexamples: with both stresses jointly necessary, R_L = 0.90 (Codex, 76/2138) | The scale survives; the inference is withdrawn | DC-174 | `literature/2026-10-21-recruitment-analytic-check-codex.md` | yes |
| | | **"A matched NPT pathway is needed for small S"** (Claude) | A construction with S = 0 and R_L = 0.5 from different postlarval susceptibility (Codex) | Withdrawn | DC-175 | same | yes |
| E3: wording | 21 Oct | "R_L is small **only if**…"; D* gives extinction probability e⁻¹ (Claude) | Reverses a sufficient condition; e⁻¹ is a large-N limit (Codex, 76/2153) | "R_L is small *if*…"; "tends to e⁻¹ as N grows" | DC-187, DC-188 | assessment note, corrections section | yes |

**Status:** an unallocated candidate. Its next check is a source-constrained
replacement boundary using at most two strategy bundles.

**What the history shows (inference):**
- **The outside brief's own design was sound.** The errors were in the
  *assessor's* inference, Claude's, and the second agent caught them
  within hours with exact constructions.
- **This is the "stretching a correct partial result" failure mode**
  (framework notepad §3): a correct bound became a causal conclusion that
  it does not support.
