# Q-012 collapsed-likelihood oracle: frozen specification (before evaluation)

Owner: Claude | 21 October 2026 | The scope Codex set in 76/2152 and Claude
acknowledged in 76/2154.

This is **one evaluator and its oracle on three tiny forests.** It includes
no fit, optimiser, bootstrap, HMC or cluster use. A pass earns only
*consideration* of a fixed-point P11 evaluator and cost check. This file is
committed before any evaluation. Results go in
`collapsed_oracle_results.json` and a short report appended below.

## 1. What is frozen

- **The target.** For the 35 non-frailty coordinates θ:
  - log_h0_1, z_rw[1..24] and τ;
  - log_k, log_λ0, κ, log_b0, κ_b, β and γ;
  - σ and ρ.

  The collapsed conditional likelihood is

  L(θ) = [∫ p_θ(x) ∏ᵢ Fᵢ(xᵢ; θ) dx] / π(θ),

  where p_θ is the frailty forest:
  - roots are N(0, σ²);
  - edges are K(xᵢ | x_parent) = N(ρ x_parent, σ²(1 − ρ²)).

  log Fᵢ(x) is lineage i's full local log-likelihood (below), **including
  pre-entry survival for cohort members**. π(θ) is the **existing**
  retained-cohort selection normaliser, unchanged: products of the 1-D and
  2-D selection integrals, which Stan computes with Q = 80 AGH. No
  individual factor is normalised, and descendant evidence enters only the
  numerator.
- **Local factor**, with lz = x − σ²/2, matching `model_v6.stan` and the
  prototype's `python_target`:

  log Fᵢ(x) = −e^{lz} (cumᵢ + cohᵢAᵢ) − e^{κ_b lz} b0 (dpostᵢ + cohᵢ(c − oᵢ))
              − λ0 e^{κ lz} dpostᵢ + (extᵢ + κ_b bifᵢ + κ mplusᵢ) lz
              + extᵢ(log h0[term_binᵢ] + log k + (k − 1) log term_aᵢ + β term_Eᵢ + γ term_missᵢ)
              + bifᵢ log b0 + mplusᵢ log λ0.

  Here cumᵢ is the sum over i's segments of exp(log h0[bin] + βE + γ·miss)
  · (a1ᵏ − a0ᵏ), and Aᵢ is the sum over i's pre-entry segments of
  exp(log h0[bin] + γ)(a1ᵏ − a0ᵏ).
- **Not integrated:** the 25 baseline coordinates, τ and the global
  parameters stay in θ. Priors are untouched and are not part of this
  oracle. η = ρσ is derived.
- **"Simpler estimator" is not chosen here.** Maximum marginal likelihood
  against same-prior collapsed Bayes is ranked only after this oracle, and
  only if it passes.
- **Coordinates and Jacobians:**
  - The evaluator integrates in x, so the density p_θ(x) carries its own
    Jacobian.
  - The reference integrates in standardised innovations: e_root = x/σ,
    and eᵢ = (xᵢ − ρ x_parent) / (σ√(1 − ρ²)), with
    p_θ(x)dx = ∏ N(e; 0, 1) de.
  - Derivatives are taken with respect to Stan's unconstrained θ
    coordinates: log σ, logit ρ and log τ.

## 2. Forests

The forests use P11 lineage data (`payload_v6q80t/data/P11.json`) as node
factors. They are toy graphs, not the P11 tree.

| Forest | Nodes (P11 lineage) | Cohort membership | Selection normaliser π |
| --- | --- | --- | --- |
| T1, root | 1 | 1 (singleton) | π₁(1) |
| T2, pair | root 2, daughter 5 | both (the P11 pair) | π₂(2, 5) |
| T3, root and two daughters | root 2; daughters 5 and 7 | 2 and 5 as a pair; 7 not in the cohort | π₂(2, 5) |

## 3. The point set (frozen; 10 states)

1. **central0** and 2. **central1:** the prototype's `test_point`s, on
   P11's N.
3. **stress_s3_r09_kbm15:** central0 with σ = 3, ρ = 0.9, κ_b = −1.5.
4. **low_rho:** central0 with ρ = 0.05.
5. **small_sigma:** central0 with σ = 0.05.
6. **high_rho_9707:** amended-P11 bank, chain 2 data row 1707 (σ =
   1.0808045, ρ = 0.99998221, κ_b = 1.1316354). The edge kernel's
   standard deviation there is about 0.0072.
7–10. **The two captured global-state pairs** of `v6q80t`, previous and
   failing states:
   - chain 1, transition 2779 (σ = 2.54 and 12.03);
   - chain 4, transition 2843 (σ = 3.34 and 1.76).

## 4. Evaluator (the candidate)

1. **Joint conditional mode** of g(x) = log p_θ(x) + Σ log Fᵢ(xᵢ), by
   Newton.
   - It is concave: the Gaussian forest is quadratic, and each log Fᵢ is
     linear minus positive multiples of exponentials.
   - It uses the same guards as `_local_mode`: finite values, a
     non-negative decrement, a step below 1e-14 or a squared decrement at
     most 1e-20, and failure after 200 iterations.
   - The node scales sᵢ are the square roots of the diagonal of the
     inverse Hessian.
2. **Node grids:** mᵢ + sᵢu, with u on the Simpson grid over [−L, L] with
   n_node intervals.
3. **Messages from children to parents.** For each parent grid point a,
   the child integral of K(x_c | x_p,a) F_c(x_c) uses a **conditional**
   grid: the 1-D mode of log K + log F_c by guarded Newton, its curvature
   scale, then Simpson over [mode ± L·scale] with n_cond intervals.
   - This is what keeps the narrow high-ρ kernel resolved.
   - Interior nodes would add log-messages interpolated from their own node
     grid. **The frozen forests have no interior nodes, so interpolation is
     not exercised here.** It is the first thing a P11 fixed-point check
     would need to test.
4. **The root** is integrated over its node grid with Simpson, in log
   space.
5. **Settings:** primary (n_node, n_cond, L) = (200, 200, 12). Resolution
   check at (400, 400, 12); domain check at (200, 200, 16) (spacing grows,
   so that check also tests coarser resolution).

Every evaluation recomputes the modes, scales and grids, so finite
differences differentiate the complete approximation, moving nodes
included.

## 5. Reference (independent)

**Direct tensor-product Simpson over the whole joint**, in standardised
innovation coordinates.
- There is no message passing, no conditional grid and no interpolation.
- **The box** is centred and scaled per axis at the base θ: the joint mode
  and the inverse-Hessian diagonal, from a generic quasi-Newton search plus
  a numerical Hessian in e-coordinates. It is fixed during finite
  differencing.
- **Settings:** n = 200 per axis, half-width L = 10 scale units.
  - Resolution check: n = 400 at L = 10.
  - Domain check: L = 14 at n = 400.
- **Shared element (declared):** the reference and the evaluator both use
  a mode to place grids. Neither shares quadrature structure, coordinates
  or code paths with the other.
- **T1 and T2 also get a second reference:** scipy adaptive
  Gauss–Kronrod (`quad`, nested for T2) in x, with epsabs 0 and epsrel
  1e-12, values only.

## 6. Identities, gates and derivatives (declared now)

**Identities, evaluator only.**
- **I1: unit factors** (all Fᵢ = 1) give |log numerator| ≤ 1e-8, for every
  forest and point.
- **I2: selection-only factors** (Fᵢ = pre-entry survival for cohort
  members, 1 otherwise) give |log numerator − log π_ref| ≤ 1e-6.
  - π_ref is the reference integral with the same factors.
  - The difference from Stan's Q80 log π is reported, not gated.

**Accuracy, full factors.**

| Check | Value | Derivatives |
| --- | --- | --- |
| Evaluator against a qualified reference | ≤ 1e-4 | ≤ 1e-3 |
| Evaluator self-convergence (resolution and domain) | ≤ 1e-6 | ≤ 1e-5 |
| Reference qualification (resolution and domain) | ≤ 1e-6 | ≤ 1e-5 |

- The value and derivative gates for evaluator against reference are the
  established likelihood-accuracy gates, for the log numerator.
- Derivatives cover **all 35 θ coordinates**, by central finite
  differences with h = 1e-4 in unconstrained coordinates, on both sides.
- A reference that fails its own qualification makes that point
  **unresolved**, never a pass. Unresolved points are reported with their
  reason.

**Factor decomposition check.** At every point, on the full P11 data, the
total from Claude's per-lineage factors must reproduce the prototype's
independent `python_target` to ≤ 1e-9. That total is:
- priors;
- −½Σε²;
- Σᵢ log Fᵢ(xᵢ);
- minus log π_Q80.

**Cost:** wall time per evaluator call, per forest, at each setting; peak
memory; and the nominal operation count O(edges × n_node × n_cond) for
P11's 19-node graph. That count is arithmetic, not a measurement.

**Pass:** every point either passes every gate or is declared unresolved
with a reference-side reason. Any evaluator-side failure ends this route or
needs a specific, explained repair. No new sampling ladder.

## Run 1 result (21 October, 7ecf567): 24 pass, 3 fail, 3 unresolved

[collapsed_oracle_results_run1.json](collapsed_oracle_results_run1.json),
wall time 5,926 s.

**What holds:**
- The factor decomposition matches `python_target` to 1.5e-11.
- **I1:** unit factors give at most 2.0e-15.
- **I2:** selection-only factors give at most 4.8e-9 against the
  reference, and 4.0e-6 against Stan's Q80.
- **Where it passes,** evaluator against reference agrees to ≤ 5e-8 in
  value and ≤ 1.2e-6 in derivatives. That holds at:
  - central0, central1, low ρ, small σ;
  - σ = 3 with ρ = 0.9;
  - the narrow-kernel state 9707 (≤ 9e-12 and 2e-10);
  - chain 1's previous state (σ = 2.54);
  - chain 4's failing state.
- Evaluator self-resolution changes are ≤ 7e-11 everywhere.

**Failures** (c1_failing, σ = 12.03; all three forests):
- The evaluator's own domain check moves by 3.6e-5 to 1.0e-4 in value and
  1.0e-4 to 7.3e-4 in derivatives, against gates of 1e-6 and 1e-5. **That
  is an evaluator-side failure.**
- The reference fails its own domain check too.

**Unresolved** (c4_previous, σ = 3.34): the evaluator converged, but the
reference's domain check moves derivatives by 1.35e-5 to 1.7e-5, against a
gate of 1e-5.

**Diagnosis** (scratch, T1). For large σ the log integrand is strongly
skewed. On the left, the exponential hazard terms vanish and only the
N(0, σ²) prior tail remains; on the right there is an exponential wall.

| State | σ | Level set 40 nats below the mode, in Laplace SDs (left / right) |
| --- | ---: | --- |
| c1_failing | 12.03 | 40.2 / 3.3 |
| c4_previous | 3.34 | 22.2 / 4.0 |
| central0 | 0.50 | 9.7 / 7.0 |

**Boxes scaled by the Laplace SD (±12 for the evaluator, ±10 for the
reference) truncate the long tail.**

## Repair 1 (declared after run 1, before running it)

- **The change: level-set domains replace Laplace-scaled boxes.**
  - Every 1-D integration in the evaluator (the root grid with its true
    child messages, and every conditional grid) runs over
    [x_lo, x_hi], where the concave log integrand falls Δ nats below its
    mode on each side. The bounds are found by doubling steps out from the
    mode, then 80 bisections.
  - The reference's box per axis is likewise the Δ-level set of the joint
    log integrand's axis profile through the mode, in innovation
    coordinates.
- **Settings:**
  - primary Δ = 50 with n = 200;
  - resolution check n = 400 at Δ = 50;
  - domain check Δ = 70 at n = 200 for the evaluator, and n = 400 for the
    reference.
- **Unchanged:** gates, finite-difference step, forests, factors,
  identities and the ten frozen points.
- **Three added hold-out points, not used in designing the repair:**
  - c1_failing with σ = 6;
  - c1_failing with σ = 20;
  - high_rho_9707 with σ = 8 (a narrow kernel and a long tail together).
- **Scope.** Run 1 stays the primary record. Run 2 tests one specific
  repair, so it is not a fresh prospective result.

### Amendment to the repair, before run 2 (pre-run smoke tests, 21 October)

Smoke tests of Repair 1, *not* the official run 2, looked at:
- central0, c1_failing and c4_previous, in all forests;
- holdout_9707_sigma8, in T1 and T2.

They showed two further evaluator-side problems. Both are added before run
2.

**Repair 1b: sinh-mapped nodes.**
- **The problem.** At c1_failing the level-set domain is very skewed: about
  54 units on the left against 4 on the right. Uniform Simpson nodes then
  under-resolve the steep side near the mode. The Δ 50 → 70 change of
  about 1e-5 was really a resolution change.
- **The fix.** Every 1-D integral uses x = c + s·sinh(u), uniform Simpson
  in u over [asinh((lo − c)/s), asinh((hi − c)/s)], with Jacobian
  s·cosh(u). Here c is the mode and s the local curvature scale. Nodes
  are dense near the mode and sparse in the tail.
- **The reference** uses the same mapping per axis in innovation
  coordinates, so it shares node placement but not quadrature structure.
- **True independence for values** comes from the scipy adaptive
  Gauss–Kronrod reference on T1 and T2. In 1-D, two Simpson rules on
  similar grids are only weakly independent.

**Repair 2: damped Newton.**
- **The problem.** At holdout_9707_sigma8 in T2 (σ = 8, ρ = 0.99998), the
  undamped joint Newton did not converge in 200 iterations: steps
  overshoot on the exponential terms.
- **The fix.** Joint and conditional modes now use Newton steps with
  backtracking (Armijo, 1e-4). The convergence criteria, guards and the
  200-iteration limit are unchanged.

**Hold-outs for run 2:**
- the three already declared, one of which (holdout_9707_sigma8) the smoke
  tests have now seen;
- **two fresh points, unseen:**
  - holdout_c4f_sigma15 (c4_failing with σ = 15);
  - holdout_9707_sigma5 (high_rho_9707 with σ = 5).

The gates, finite-difference step, forests, factors, identities and the ten
frozen points are unchanged. Run 1 remains the primary prospective record.

**Implementation note, pre-run.**
- **A fix to Repair 2 found in smoke testing.** Armijo backtracking stalls
  once the decrement drops below the objective's floating-point resolution.
  Steps are therefore taken in full once the squared decrement is ≤ 1e-8,
  the quadratic-convergence region.
- **Smoke results on already-seen points** (not run 2):
  - the evaluator's resolution and domain changes are 0 at c1_failing and
    holdout_9707_sigma8 in all forests;
  - c1_failing's n = 200 reference differs from the evaluator by 5e-6 in T2
    and T3. Run 2's n = 400 qualification decides it.

## Run 2 result (22 October; Repairs 1, 1b and 2 at 8962871)

[collapsed_oracle_results_run2.json](collapsed_oracle_results_run2.json):
15 points × 3 forests = 45 rows.

**By the frozen status rule: 33 pass, 4 fail, 8 unresolved (reference not
qualified).**
- **Replicated exactly.** Runs on the laptop (10,820 s) and on deep-server
  (4,239 s) agree **bitwise in all 1,639 recorded values**.
- **The evaluator converges everywhere.** Its self-resolution and
  self-domain changes are **≤ 1.4e-10 in value and derivatives in all 45
  rows**. That includes σ = 12, 15 and 20, and ρ = 0.99998 with σ = 5 and
  8. Run 1's evaluator-side failure is cured.
- **The 33 passes include:**
  - every T1 row;
  - every central, low-ρ, small-σ and high-ρ row;
  - c1_previous and c4_failing;
  - both 9707 hold-outs, among them the fresh σ = 5 point, which passes in
    all three forests.
- **4 fail:** stress_s3_r09_kbm15 and c4_previous, in T2 and T3. Each
  fails **only** the I2 selection identity, scored against the tensor
  reference (3.85e-5 and 1.16e-6, against a gate of 1e-6). That reference
  is itself unqualified there.
- **8 unresolved:** c1_failing and the σ = 6, 15 and 20 hold-outs, in T2
  and T3. The tensor reference fails its own domain check, by up to 5e-5
  in value and 1e-2 in derivatives at σ = 15. The evaluator is converged.

**Post-hoc corroboration** (outside the frozen gates, and declared as such;
[oracle_posthoc/](oracle_posthoc/)):
- **(a) Values, T1 and T2.** The scipy adaptive Gauss–Kronrod reference
  shares no grid or node code with the evaluator. It agrees with the
  evaluator to **≤ 1.4e-14 at every point**, every fail and unresolved row
  included.
- **(b) The selection identity.** The evaluator's selection-only numerator
  agrees with the pilot's qualified repaired-rule reference (local mode,
  800 → 1,600 intervals, L 12 → 16; all qualified) to **≤ 2.6e-8 at all 15
  points**, in T1 and T2. The four "fail" labels therefore come from the
  unqualified tensor reference, not from the evaluator.

**Diagnosis of the reference.**
- Its per-axis level sets come from axis profiles through the mode. Those
  under-cover the joint level set when large σ skews and correlates the
  integrand in innovation coordinates.
- Its domain change grows with σ: about 6e-7 at σ = 3.3–6, and 5e-5 at
  σ = 15.

**Not yet verified by any qualified independent reference:** T2
derivatives, and T3 values and derivatives, at the six points with σ ≥ 3
listed above.

**Cost.**
- Evaluator calls: T1 0.01–0.05 s; T2 2–6 s; T3 4–8 s. That is about 5×
  run 1, because the level-set bisections of the root re-run nested child
  messages. This is an implementation cost, not an intrinsic one.
- Finite-difference gradients (71 calls) take minutes per forest.
- P11's 19-node tree has interior nodes, so interpolated messages would be
  needed. They remain untested.
- **At this cost, the evaluator is a validation tool, not yet a fitting
  kernel.**

**Reading.**
- **The repairs fixed the evaluator.** Every remaining row that is not a
  pass is a failure on the reference side, and corroboration (a) and (b)
  supports the evaluator at every point it covers.
- **Under the frozen rule, the oracle has still not passed.**

**Decision for Codex:**
- (i) A bounded repair to the reference only: a nested adaptive
  Gauss–Kronrod reference for T3 values, plus finite-difference derivatives
  of the adaptive references at the six points.
- (ii) Accept the evaluator on the present evidence, and consider the
  fixed-point P11 check: interpolation first, then cost.
- (iii) Stop the route.

## Reference repair, run 3 (declared before execution; Codex 76/2165 and 76/2189)

This is a bounded batch for **16 cells**:
- the six states in T2 and T3: stress_s3_r09_kbm15, c4_previous,
  c1_failing, and the σ = 6, 15 and 20 hold-outs;
- **controls** central0 and holdout_9707_sigma8, in T2 and T3.

There is no full rerun and no new point search. Any unresolved cell stays
unresolved.

**The evaluator is unchanged** (the algorithm at 8962871). It is re-run only
to save **full 35-coordinate vectors**: the value at θ and at θ ± h·e_j for
every coordinate. That is done at the primary (200, 200, Δ50), resolution
(400, 400, Δ50) and domain (200, 200, Δ70) settings, with h = 1e-4.

**The new reference** (`collapsed_oracle_refrepair.py`) is nested adaptive
QUADPACK (`scipy.integrate.quad`) in x coordinates.
- **Leaves.** L_c(x_r) = ∫ N(x; ρx_r, σ²(1 − ρ²)) F_c(x) dx.
- **Root.** H(x_r) = log N(x_r; 0, σ²) + log F_r(x_r) + Σ_c log L_c(x_r).
  - The T3 star multiplies its two leaf integrals at each root abscissa.
    This is a shared analytic factorisation, disclosed here.
  - Local factor coefficients come from the shared `coefs`, the target
    definition validated by the decomposition check. **Nothing else is
    shared with the evaluator:** no mode, level-set or sinh code.
- **Anchors:** Brent maximisation (`minimize_scalar`); g by central
  difference.
- **Domains by Codex's strong-concavity envelope.**
  - Curvature lower bounds: c = 1/(σ²(1 − ρ²)) for leaves; c = 1/σ² for
    the root, since its descendant messages are log-concave (Prékopa).
  - The envelope is h(x) ≤ h(a) + g²/(2c) − (c/2)(x − a − g/c)².
  - The integration box is a + g/c ± R/√c, with tail mass at most
    exp{h(a) + g²/(2c)} · √(2π/c) · erfc(R/√2).
  - R is increased (from 12, in steps of 2) until that bound, relative to
    the integral, is ≤ 1e-16. In the bound, |g| is inflated by 10% plus
    1e-8.
- **Error accounting.**
  - quad settings: inner epsrel 1e-13, outer epsrel 1e-12, epsabs 0, limit
    1000.
  - Each QUADPACK abserr is kept. The largest inner relative error and
    inner tail bound are propagated into the root value, and evaluation
    counts are recorded.
  - **Warnings make a value unqualified.**
- **Qualification of every value** (θ and all 70 perturbations): the
  estimated total relative error (outer + maximum inner + tails) must be
  ≤ 1e-11, with no warning.
  - A relative uncertainty of 1e-11 adds at most about 1e-7 to a centred
    derivative.
  - For the central value only, a tightened rerun (inner epsrel 1e-14,
    outer 1e-13, R + 4) must agree within 1e-10. That is the reference's
    own resolution and domain evidence.

**Decisions** (the 2165 defects closed).

| Rule | Outcome |
| --- | --- |
| Any exception inside the evaluator | **fail (evaluator: stage)** |
| Evaluator self-checks beyond 1e-6 (value) or 1e-5 (derivative) | **fail (evaluator: self-convergence)** |
| Reference exception, warning or failed qualification | **unresolved (reference: reason)** |
| Two qualified references that disagree by more than 1e-6 in value | **unresolved (reference disagreement)** |
| Evaluator against the qualified reference beyond 1e-4 (value) or 1e-3 (any of 35 derivatives) | **fail (accuracy)** |

- The run-2 tensor reference is recorded but **unqualified** in all 16
  cells, so it does not enter.
- **I1** comes from run 2. **I2** comes from the post-hoc qualified
  selection check: T2 directly, T3 by Codex's unit-third-daughter transfer
  (76/2189).
- **all_pass** additionally requires decomposition_pass.
- The fixtures, run before the batch, must show three things:
  1. an otherwise passing cell with a 0.01 independent-value disagreement
     does not pass;
  2. an injected evaluator mode failure becomes "fail (evaluator:
     joint_mode)";
  3. decomposition_pass = false gives all_pass = false.

**Execution.**
- Every value is a separately persisted task, appended to
  `collapsed_oracle_run3_cells.jsonl`. A restart skips completed tasks.
- First a deep-server benchmark of one T3 central reference value and one
  evaluator call, then a forecast and a fixed execution limit, then the
  batch, run without a further permission request.
- **Outputs:** `collapsed_oracle_results_run3.json`, holding raw values and
  receipts, full vectors, and the amended adjudication of the 16 cells.
  The run-1 and run-2 frozen outcomes are kept unchanged.

*Pre-execution correction:* QUADPACK rejects epsrel below 50·eps (about
1.11e-14). The tightened rerun therefore uses inner epsrel **1.2e-14**, not
1e-14. Nothing else changes.

**Benchmark and forecast** (deep-server, a20973e;
[collapsed_oracle_run3_benchmark.json](collapsed_oracle_run3_benchmark.json)).

T3 reference values, against the unchanged evaluator:

| Point | Reference time | Estimated relative error | Evaluator − reference |
| --- | ---: | ---: | ---: |
| central0 | 0.73 s | 6.1e-13 | 0 |
| c1_failing | 2.96 s | 4.0e-13 | −1.4e-14 |
| holdout σ = 20 | 3.77 s | 4.8e-13 | 0 |

- All three are qualified, with no warnings. Evaluator calls take
  1.5–1.8 s.
- **Forecast:** 4,560 tasks on 62 workers, about 170 s.
- **Declared execution limit: 1,800 s.** That is above the benchmark's own
  4 × forecast of 680 s, because the n = 400 resolution settings were not
  benchmarked.
- **If the limit is reached,** completed tasks persist and the same command
  resumes. No settings change.

## Run 3 result (22 October; reference repair, deep-server, 9839843)

Outputs:
- [collapsed_oracle_results_run3.json](collapsed_oracle_results_run3.json):
  the amended adjudication and the full 35-coordinate evaluator and
  reference vectors;
- `collapsed_oracle_run3_cells.jsonl.gz`: all 4,560 task records with
  their receipts;
- [collapsed_oracle_run3.log](collapsed_oracle_run3.log).

**4,560 tasks finished in 242 s**, against a forecast of 170 s and a
limit of 1,800 s. No task is missing, and no evaluator task failed.

**Amended adjudication of the 16 cells: 15 pass, 1 unresolved.**
`all_pass` is false. Decomposition passes, and the run-1 and run-2
frozen outcomes are unchanged.

| Cells | Run 2 (frozen) | Run 3 (amended) |
| --- | --- | --- |
| stress_s3_r09_kbm15 and c4_previous, T2 and T3 | fail (I2 against the tensor reference) | **pass** |
| c1_failing, and the σ = 6, 15 and 20 hold-outs, T2 and T3 | unresolved (tensor domain) | **pass** |
| central0, T2 and T3 | pass | pass |
| holdout_9707_sigma8, T2 | pass | pass |
| holdout_9707_sigma8, T3 | pass | **unresolved (reference: a value not qualified)** |

**Across all 16 cells:**
- Evaluator against the new reference: at most **1.4e-14 in value** and
  **1.4e-10 across all 35 derivatives**.
- Evaluator self-resolution and self-domain changes: at most 3.6e-15 in
  value and 1.4e-10 in derivatives.
- The reference's tightened rerun changed central values by at most
  1.4e-14.
- Every qualified reference value has a total estimated relative error
  ≤ 9.6e-12.

**Cause of the one unresolved cell.**
- In holdout_9707_sigma8 T3 (σ = 8, ρ = 0.99998, a leaf-kernel SD of
  about 0.048), **36 of the 72 reference values carry total estimated
  relative errors of 1.03e-11 to 2.28e-11**, against the declared budget
  of 1e-11.
- The excess comes entirely from QUADPACK's own `abserr` estimates for
  the two narrow leaf integrals (about 5e-12 to 1.1e-11 each). The budget
  counts each leaf once, so two leaves double it.
- There are no warnings, every tail bound is ≤ 5e-32, and the tightened
  rerun's estimate is 1.65e-11.
- Agreement with the evaluator in this cell is 7.1e-15 in value and
  1.1e-10 in derivatives.
- **By the declared rule, the cell is unresolved.** The budget is not
  relaxed after the fact.

**Reading.**
- **All six named problem states now pass in T2 and T3** against a
  qualified, independently implemented reference. So does every control
  except one T3 control cell, whose reference misses its own error budget
  by at most a factor of 2.3.
- **Under the declared rules the oracle has still not fully passed.** One
  cell is reference-unresolved, for a stated cause.
- **For Codex:**
  - **(a)** Accept the 15 passes, and judge whether a conservative
    QUADPACK estimate at about 2e-11 belongs in the unresolved category or
    calls for a declared tolerance change for future checks. I make no
    claim of a pass for that cell.
  - **(b)** Whether this record is enough to consider the bounded
    fixed-point P11 evaluator, interior-node and cost check.

### Run 3 corrections (Codex 76/2194; [review](../../ideas/2026-10-22-q012-run3-review-codex.md))

- **The unresolved control failed on 37 of its 72 reference values,** not
  36: 36 primary values plus the tightened rerun.
- **The run-3 declaration was wrong to call the run-2 tensor reference
  unqualified in all 16 cells.** It was qualified in the four controls
  (central0 and holdout_9707_sigma8, T2 and T3) and unqualified in the 12
  problem cells.
- **The recorded run-3 screen stays as it is: 15 pass, 1 unresolved.** Its
  qualification is now **provisional**. `_quad(full_output=1)` kept only
  Python warnings, which SciPy suppresses in that mode, and dropped the
  non-success messages SciPy returns instead.
  - Codex's one authorised probe (σ = 8, T3) reproduced the original
    receipt exactly.
  - Of its 1,265 calls, 35 inner calls returned roundoff messages ("the
    error may be underestimated") that the receipt never recorded.

## Reference v2, run 4 (declared before execution)

This is the bounded correction set out in 76/2194.
- **Diagnostics.** Every QUADPACK return is kept in full. A non-success
  message (the tuple's fourth element) or a Python IntegrationWarning
  makes that integral's value **unqualified**. Messages are propagated from
  inner to outer receipts. A regression fixture must show that a
  subdivision-limited integral is flagged and that the flag reaches
  qualification.
- **The narrow-kernel leaf is standardised.**
  - With u = (x_c − ρx_p)/s and s = σ√(1 − ρ²), the leaf log integrand is
    −u²/2 − ½log 2π + log F_c(ρx_p + s·u), with curvature bound 1 in u.
  - There is no extra log-s term, since N(x; ρx_p, s²)dx = φ(u)du.
  - The root integral is unchanged.
- **Budget, prospective.** Total estimated relative error ≤ **1e-10**:
  h × (0.1 × the 1e-5 reference-derivative gate). That allows at most 1e-6
  of derivative uncertainty to integration. The run-3 record at 1e-11 is
  preserved.
- **Requested tolerances matched to the budget.** The primary run uses
  inner epsrel 1e-12 and outer 1e-11. The tightened central rerun uses
  inner 2e-13, outer 2e-12 and R + 4, and must agree within 1e-10.
  Diagnostics in the tightened rerun also leave the cell unresolved.
  Tails ≤ 1e-14 are unchanged.
- **Procedure.**
  1. The fixture.
  2. **One control smoke check:** holdout_9707_sigma8, T3, central value.
  3. If needed, only the existing **1,152 reference values** (16 cells ×
     72), with keys bound to `refv2` in a new file,
     `collapsed_oracle_run4_reference.jsonl`, so no run-3 key can be
     reused.
- **Candidates.** The run-3 evaluator vectors are reused unchanged. No new
  points, no likelihood change and no integrator search. Persistent
  diagnostics leave a cell unresolved, and P11 stays held.
