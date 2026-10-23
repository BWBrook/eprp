# Q-012 P11 fixed-point check: interior-node interpolation, then cost

Owner: Claude | 22 October 2026 | Permission: Codex 76/2214 and the
[run-4 review](../../ideas/2026-10-22-q012-run4-review-codex.md). This is
declared before any evaluation.

**Scope.** Codex lifted the hold only for interior-node interpolation
validation followed by fixed-point P11 evaluation and cost. There is no
optimiser over θ, no MCMC, bootstrap, empirical fit or estimator choice,
and no further adaptive-reference search. One value is benchmarked first;
the finite bank and execution ceiling are then frozen in this file
(section 6) before the batch. The batch runs on mac-mini, not the laptop.

## 1. Target

The [frozen oracle's](collapsed_oracle.md) collapsed conditional
likelihood, unchanged, on the **whole P11 forest**:

L(θ) = [∏_trees ∫ p_θ(x_tree) ∏_{i∈tree} Fᵢ(xᵢ; θ) dx_tree] / π(θ).

The local factors Fᵢ, the forest prior, the coordinates and the Q80
selection normaliser π are exactly those in section 1 of that file.
P11's `parent` array gives 10 trees:

| Tree | Nodes (lineages; parent → child) | Interior nodes | Cohort members |
| --- | --- | --- | --- |
| Big | 2 → 5; 5 → 7, 8, 10, 11; 10 → 14 | 5, 10 | 2, 5 (the C2 pair) |
| Chain | 4 → 9 → 12 | 9 | 4 (C1) |
| Pair | 15 → 18 | none | none |
| Singletons | 1, 3, 6, 13, 16, 17, 19 | none | 1, 3, 6 (C1) |

π = π₂(2, 5) · π₁(1) π₁(3) π₁(4) π₁(6), as Stan computes it (Q = 80 AGH).

## 2. Candidate: tree message passing with interpolated interior messages

Leaves, the root and every setting are as in the frozen evaluator
(section 4 of the oracle, with Repairs 1, 1b and 2). What is new:

1. **Generic node message.** For a non-root node j and parent points x_p,
   m_j(x_p) = ∫ N(x; ρx_p, σ²(1 − ρ²)) M_j(x) dx, with
   log M_j = log F_j + Σ_{c ∈ children(j)} log m_c.
   It uses the conditional grid exactly as leaves do: a guarded Newton
   mode, its curvature scale, Δ-level-set bounds and sinh-mapped Simpson
   with n_cond intervals. For a leaf, M_j = F_j and the result is the
   frozen `leaf_message`.
   - The message also returns d log m_j / dx_p = (ρ/v)(E[x | x_p] − ρx_p),
     from the same quadrature weights.
2. **Interpolation tables.** Each interior node j tabulates, for every
   child c, log m_c and its exact derivative at n_tab + 1 sinh-mapped
   points (centre the joint mode m_j, scale s_j) over a table range. Each
   child's log message is a cubic Hermite interpolant of those values and
   derivatives. Tables are built in post-order, so a child's own table
   exists first.
3. **Table range.** The profile level set of the tree's joint log integrand
   in x_j, at deficit Δ_tab(j) = (depth_j + 1)·Δ + 40. depth_j is j's
   distance from the root. The profile maximises over the other nodes by
   guarded Newton, warm-started at the joint mode.
   - Each nesting level adds at most about Δ of deficit, and 40 nats cover
     log-determinant variation between profile and marginal.
4. **Outside the table**, a log message continues along its tangent at the
   table edge. Log messages are concave, so this is an upper bound.
   - **Material-extrapolation diagnostic:** if any quadrature node outside
     a table carries an integrand within 40 nats of its grid's maximum,
     the evaluation is *unresolved*. It is never silently accepted.
     **Superseded by Amendment 1** (below), before any benchmark.
5. **Settings** (n_node, n_cond, n_tab, Δ):
   - primary (200, 200, 400, 50);
   - resolution (400, 400, 800, 50);
   - domain (200, 200, 400, 70). Table deficits grow with Δ, so this also
     widens the tables.
6. Every evaluation recomputes modes, ranges, tables and grids, so finite
   differences (h = 1e-4, central, all 35 coordinates) differentiate the
   complete approximation.

## 3. Checks

**R1, the interpolation check (targeted, not independent).** The same
evaluation at primary settings, with the same quadrature nodes and weights
at every level. Every child message at every node is computed **exactly**,
by recursive conditional-grid integration with no table.
- The R1 − candidate difference is therefore the interpolation error
  alone, in value and in all 35 derivatives.
- **Pass:** value ≤ 1e-6 and every derivative ≤ 1e-5 (the oracle's
  self-check tolerances).
- R1 shares placement and all other machinery with the candidate. It
  measures interpolation only. Placement and range effects are measured by
  the candidate's resolution and domain checks.

**R2, an independent reference for one tree with an interior node.** The
frozen tensor-product Simpson reference in standardised innovations
(oracle section 5, Repair 1 boxes), applied to the chain 4 → 9 → 12. It
is n = 200 per axis at Δ = 50, with resolution (n = 400) and domain
(Δ = 70) checks. No message passing, no conditional grid, no
interpolation.
- Qualification and accuracy tolerances are the oracle's: reference self
  checks 1e-6 / 1e-5; evaluator against reference 1e-4 in value and 1e-3
  in derivatives.
- **Where R2 does not qualify** (its known axis-box limit at large σ), the
  cell is *reference-unresolved*, not a candidate failure. No new
  reference method is introduced.

**Candidate self checks** on the full P11 value: resolution and domain,
1e-6 / 1e-5.

**Identities:**
- **I1, unit factors:** every tree's log numerator is 0 to 1e-8, at
  primary and resolution settings.
- **I2, selection:** the candidate in selection mode on P11 against Stan's
  Q80 log π, to 1e-6. Interior nodes are present with unit children.
- **I3, linear tilt:** with log Fᵢ = bᵢ(xᵢ − σ²/2), the closed form is
  log numerator = ½ bᵀΣb − (σ²/2) Σbᵢ, where Σ is the tree covariance.
  Log messages are then quadratic, so this tests the tree plumbing to
  1e-8. It is a pre-run fixture at three points.
- **Regression fixture:** the generic code reproduces the frozen
  evaluator on T1, T2 and T3 to 1e-12 at the frozen central points.

**Cell status:**
- **pass:** all applicable checks pass.
- **interpolation fail:** R1 fails.
- **fail:** any other candidate check fails.
- **unresolved:** a guard or diagnostic stops the evaluation.

R2 status is reported separately and never converts a candidate failure
into a pass.

## 4. Cost (the second deliverable)

- **Per point:** candidate wall time for one P11 value and one 71-call
  gradient, at each setting and single-threaded, broken down by tree.
- **Per value:** R1 and R2 costs.
- **Reported against fitting needs:** collapsed log-likelihood plus
  gradient seconds per θ, and the implied cost of the gradient count a
  maximum-marginal-likelihood fit or collapsed HMC would need. Those
  counts are arithmetic, not a fit.

## 5. Point bank (proposed; final selection frozen in section 6)

The 15 frozen oracle states:
- central0, central1, stress_s3_r09_kbm15, low_rho, small_sigma and
  high_rho_9707;
- the four captured v6q80t states;
- the five hold-outs.

They are written once to `p11_fixedpoint_bank.json`, so the batch does not
depend on scratch files.

## 6. Benchmark, frozen bank and ceiling (frozen before the batch)

**Benchmark** ([p11_fixedpoint_benchmark.json](p11_fixedpoint_benchmark.json),
laptop, one core, central0):

| Quantity | Seconds | Difference from candidate |
| --- | ---: | ---: |
| Candidate P11 value, primary (big tree 4.1, chain 1.5, pair 0.6, singletons ~0.004 each) | 6.2 | — |
| Candidate, resolution / domain | 6.5 / 6.1 | −4.8e-13 / 5.7e-14 (log numerator) |
| R1 exact, big tree | 254 | −3.8e-13 |
| R1 exact, chain | 2.7 | −1.1e-13 |
| R2 tensor, chain, n = 200 (box 0.03) | 0.87 | −1.1e-13 |
| log π (Q80) | 0.002 | — |

**mac-mini calibration**
([p11_fixedpoint_calibration_macmini.json](p11_fixedpoint_calibration_macmini.json),
Apple M4, one process, at central0, holdout_9707_sigma8, holdout_c1f_sigma20
and c1_failing):
- Candidate value 1.9–2.2 s and R1 big-tree value 55–60 s, with no extra
  cost at the stress points.
- R1 − candidate is −3.8e-13, −6.3e-11, 0.0 and 0.0. The candidate value at
  central0 is bit-identical to the laptop's.
- A direct probe of the Hermite tables over their needed ranges found
  pointwise errors of at most 1e-12 at σ = 12 and 20, 8e-10 at central0
  and 3e-7 at holdout_9707_sigma8, at the range edges.
- Needed ranges sit close to the table's upper edge: for example 34.4
  against 34.9 at holdout_9707_sigma8. Amendment 1's check guards this.

**Frozen bank:** all 15 points of section 5, in
[p11_fixedpoint_bank.json](p11_fixedpoint_bank.json). Every check of
section 3 runs at every point, including **R1's full 35-derivative check
of the big tree at all 15 points**. That is 660 tasks: per point, 70
exact big-tree evaluations by coordinate plus a base value, three
candidate settings, three R2 settings, R1 on the chain, and identities.

**Forecast and ceiling:**
- Forecast: about 21 performance-core-hours. Over 8 workers on 4
  performance and 6 efficiency cores, that is about 4 h wall, or roughly
  32 allocated core-hours.
- **Ceiling:** 10 h wall on mac-mini with 8 workers (`pilot.workers`),
  at most 80 allocated core-hours.
- Tasks not started by the deadline are recorded as skipped. Their points
  are reported *unresolved (not run)*, never imputed.
- Results append to `p11_fixedpoint_run.jsonl` task by task, so a restart
  resumes. `assemble` writes `p11_fixedpoint_results.json`.

## Amendment 1: table coverage check (before the benchmark)

**What happened.** The first fixture run stopped at I1 (unit factors) at
stress_s3_r09_kbm15. The section 2.4 diagnostic flagged 36 nodes. A trace
located every flagged node:
- All were in **single-row root level-set probes**: at x_p = ±48 (about
  16σ at σ = 3) and x_p = 36.1 at holdout_9707_sigma8 (ρ = 0.99998).
- Those probes overshoot the root's Δ-level and do not enter the integral.
- The regression fixture had already passed before the stop.

The diagnostic was mis-specified: "within 40 nats of its own row's maximum"
ignores how far down the row itself lies.

**Replacement.** For ρ > 0, both ends of a conditional Δ-level set increase
with the parent value. With h_t(x) = f(x) + t·x and f concave, each end r
satisfies r′ = (x* − r) / (f′(r) + t) > 0.
- So the quadrature nodes of interior node j, over all parent points in
  the parent's needed range [a, b], lie within
  [lo_j(a), hi_j(b)] = needed(j).
- needed(root) is the root's integration range.
- For an interior parent, [a, b] is widened to its enclosing table nodes,
  because those are the entries its Hermite interpolant reads.
- **The check:** every table contains needed(j), evaluated top-down at two
  points per interior node. Otherwise the evaluation is *unresolved*.
  The needed and table ranges are recorded.
- Tangent extrapolation over-estimates a concave log message. Probes and
  needed ranges can therefore only widen, so the check errs on the strict
  side.

Nothing else changes.

## Amendment 2: I2 gates against the qualified selection reference (before the benchmark)

**What happened.** The second fixture run gave selection-mode candidate −
Q80 = −1.93e-6 at holdout_9707_sigma8 (8.3e-8 at the stress point, 1.3e-14
at central0). This is Q80's own error, not the candidate's.
- At that point, oracle run 2 recorded −2.4e-7 against Q80 for lineage 1
  alone, while its qualified post-hoc reference agreed with the evaluator
  to 1e-16.
- P11 has five selection factors.

The oracle gated I2 against a qualified reference and only recorded the
Q80 difference. Section 3's "against Q80" did not follow that.

**Replacement.** I2 compares the selection-mode candidate with
`pilot.local_reference` on P11's whole normaliser, the oracle post-hoc
method:
- the reference is evaluated at n = 1,600, L = 12;
- it is **qualified** when n = 800 and L = 16 each agree with it to 1e-6;
- the gate is ≤ 1e-6 when the reference is qualified;
- the Q80 difference is recorded and not gated.

## Cost addendum: gradients by Fisher's identity (outside the frozen batch)

This is a probe for section 4's cost question, not an estimator and not part
of the batch: [fisher_gradient_probe.py](fisher_gradient_probe.py),
[fisher_gradient_probe.json](fisher_gradient_probe.json).

∇_θ log Z = E_post[∇_θ log g_θ(x)] is evaluated on the evaluator's **own**
quadrature nodes and weights.
- **Analytic parts:** the root and edge Gaussian terms, the exponent
  dependence on κ and κ_b, and the σ-dependence of lz.
- **Coefficient derivatives:** central differences of the cheap `coefs()`
  (h = 1e-6).

**Results, T1 and T2** at central0, stress_s3_r09_kbm15, high_rho_9707,
c1_failing and holdout_9707_sigma8:
- **Agreement:** the 35-coordinate Fisher gradient agrees with the
  evaluator's central-difference gradient (h = 1e-4) to at most 4.0e-7.
  The largest gradient component is 61.
- **The residual is the finite-difference error.** Halving h cuts it by a
  factor of exactly 4.00 (2e-4 → 1e-4 → 5e-5) at three cells, the h²
  truncation law. So the Fisher gradient is the more accurate of the two.
- **Cost:** T2 takes 0.6–0.7 s by Fisher against 40–47 s by finite
  differences, about 65× less. T1 takes 0.02 s against 0.26 s.

**Implication for section 4.**
- With finite differences, one P11 gradient is 71 values, about 140 s on
  one mac-mini core.
- Extended to trees, Fisher's identity would cost about one value. Each
  message would carry its θ-gradient as a conditional expectation, and
  interior tables would hold those 35-vectors with exact x-derivatives
  from Cov(·, x_c | x_j)·ρ/v.
- That would move collapsed HMC from infeasible to plausible.

**Tree version, built the same evening** ([fisher_tree.py](fisher_tree.py),
[fisher_tree_check.json](fisher_tree_check.json)).
- **Gradient messages.** Each message carries its θ-gradient upward:
  G_j(x_p) = E[∂θ log K + ∂θ log F_j + Σ_c G_c | x_p].
- **Tables.** Interior tables hold G_c with exact x-derivatives,
  E[∂ₓf] + (ρ/v) Cov(f, x_c), in local cubic-Hermite interpolants with
  tangent extension. The value tables are unchanged.
- **Preliminary check against the batch's finite-difference per-tree
  gradients:** at most 2.2e-7 at central0 and 6.7e-8 at central1, over all
  10 trees, including the big tree's two interior levels.
- **The residual is the finite-difference error.** On the big tree, halving
  h gives ratios of 4.00 and 4.02 at central0, and 4.03 and 4.11 at
  high_rho_9707 (ρ ≈ 1). The drift at h = 5e-5 is the roundoff floor of
  the difference quotient. **Corrected 23 October (Codex 76/2248):** this
  shows that the residual follows h² truncation, with Codex's independent
  Richardson agreement at or below 1.81e-10. It does not establish the
  absolute integral error, so the earlier "below about 1e-9" claim is
  withdrawn.
- **Cost:** about 9 s for the whole P11 gradient on the laptop, about 1.5
  value-equivalents, against about 440 s for finite differences on the same
  machine.
- To be rerun at all 15 points once the batch completes. It is still a
  cost probe, not an estimator.

## Results: the frozen batch (22–23 October 2026)

- **Run:** 660 of 660 tasks completed, with no unresolved and no skipped
  tasks. mac-mini, 8 workers, 4.97 h wall, 39.7 core-hours, within the 10 h
  and 80 core-hour ceiling.
- **Records:** receipts in [p11_fixedpoint_run.jsonl.gz](p11_fixedpoint_run.jsonl.gz),
  assembly in [p11_fixedpoint_results.json](p11_fixedpoint_results.json).

**All 15 points pass every candidate check** (section 3; maxima over the
15 points):

| Check | Value | Derivatives (all 35) | Tolerance |
| --- | ---: | ---: | --- |
| Self: resolution | 1.3e-10 | 3.9e-10 | 1e-6 / 1e-5 |
| Self: domain | 2.3e-11 | 3.2e-10 | 1e-6 / 1e-5 |
| R1 interpolation, big tree (two interior levels) | 6.3e-11 | 2.8e-10 | 1e-6 / 1e-5 |
| R1 interpolation, chain 4 → 9 → 12 | 8.0e-11 | 1.4e-10 | 1e-6 / 1e-5 |
| I1, unit factors | 8.0e-15 | — | 1e-8 |
| I2, selection against the qualified reference (qualified at all 15) | 1.1e-7 | — | 1e-6 |

**R2, the independent tensor reference on the chain**, reported separately:
- **It qualifies at 9 points.** There the candidate chain agrees with it to
  8.0e-11 in value and 5.5e-9 in derivatives (tolerance 1e-4 / 1e-3).
- **It is reference-unresolved at 6:** stress_s3_r09_kbm15, c1_failing,
  c4_previous, holdout_c1f_sigma6, holdout_c1f_sigma20 and
  holdout_c4f_sigma15. These are the large-σ or stress states where its
  axis-box limit was already known. As declared, this does not change the
  candidate's status.

**Cost (section 4).**
- **One P11 collapsed log-likelihood value:** 3.0–3.7 s on one mac-mini
  core under the 8-worker load, and about 2 s alone.
- **One 35-coordinate finite-difference gradient** (71 values): 191–253 s
  under load.
- **One Fisher-identity gradient** (cost addendum, 15-point check below):
  2.1–2.4 s under the same load, about 100× cheaper. **This covers the
  numerator gradient only.** The selection normaliser, priors and Jacobians
  are excluded (Codex 76/2248).
- **Implied arithmetic, not a fit.** Corrected 23 October: these figures
  are numerator-only. Pure maximum marginal likelihood over the current 35
  coordinates also has an exact τ → cτ, z_rw → z_rw/c baseline ridge,
  so dropping the regularising priors would be a different model. Codex
  prefers same-prior collapsed Bayes (76/2248).
  - Maximum marginal likelihood with about 100–300 gradients would take
    roughly 4–12 min of one core with Fisher gradients, against 5–21 h with
    finite differences.
  - Collapsed HMC with about 2.5 × 10⁵ gradients per four-chain fit would
    take about 160 core-hours with Fisher gradients, against about 15,000
    with finite differences.

**Fisher gradient at all 15 points** ([fisher_tree_check.json](fisher_tree_check.json)):
- Against the batch's finite-difference per-tree gradients it agrees to at
  most 6.6e-7 at nine points.
- At the other six it agrees to 1.2e-6–5.5e-6: the four captured v6q80t
  states (c1 and c4, previous and failing) and the σ = 15 and σ = 20
  hold-outs.
- **This is still the finite-difference error.** At the worst point
  (holdout_c4f_sigma15, big tree, gradients up to 251), halving h cuts the
  gap by exactly 4.00 and 4.00 (2.2e-5 → 5.5e-6 → 1.4e-6). The larger
  absolute gaps come from larger third derivatives, not from the Fisher
  gradient.
- **mac-mini's `matmul` warnings** (divide-by-zero, overflow and invalid,
  at the root `w @ f`) are spurious. All inputs are finite, and the result
  equals `einsum` and a plain Python loop to 3e-14. This is a known numpy
  2.x behaviour with Apple's Accelerate library.

**Reading.**
- The collapsed evaluator with Hermite-interpolated interior messages is
  numerically qualified on the whole P11 forest at every frozen point,
  including σ = 20 and ρ ≈ 1.
- This earns the fixed-point check, and only that. **No estimator,
  optimiser or fit has been chosen or run.**

## Full-target bridge (declared 23 October, before execution; Codex 76/2248 and [review](../../ideas/2026-10-23-q012-fixedpoint-review-codex.md))

**Target.** The complete collapsed log target on Stan's unconstrained
coordinates u (35 coordinates):

F(u) = Σ_trees log numerator(θ) − log π_Q80(θ) + log prior(θ) + log J(u),

where:
- **log prior:** the model_v6 non-frailty priors (lines 205–215) for log h₀₁,
  z_rw, τ (half-normal, scale 0.5), log k, log λ₀, κ, log b₀, κ_b, β, γ and
  σ (half-normal, scale 1). ρ is uniform. Normalising constants are
  omitted.
- **log J:** log τ + log σ + log ρ + log(1 − ρ).
- **Not added again:** the frailty density is integrated in each numerator.
- **Q80 stays explicit** as the denominator. It is not replaced.

**Gradient assembly:** ∇F = Fisher numerator (`fisher_tree.py`, summed
over trees) − central-difference ∇ log π_Q80 (h = 1e-4) + analytic
∇(log prior + log J). Each piece is kept as its own signed 35-vector.

**Bank:** central0, high_rho_9707 and holdout_c4f_sigma15.

**Checks** (the existing tolerances, applied prospectively; no absolute
1e-9 criterion):

| Check | Content | Tolerance |
| --- | --- | --- |
| B1 | Assembled ∇F against archived FD numerator − archived `log_pi_grad` + the same analytic prior/Jacobian vector, all 35 coordinates, per point | 1e-5 (self-derivative; the archived FD carries h² truncation ≲ 6e-6 at these points) |
| B2 | Fisher numerator vectors at primary, resolution and domain settings (nine evaluations); maximum difference from primary | 1e-5 |
| B3 | Directional checks on whole-forest F values: d₁ is the τ/z_rw ridge direction (u_τ +1, z_rw −z_rw, normalised); d₂ is (u_σ, u_ρ, κ) equally weighted; central differences at ε = 1e-3 and 5e-4 (24 values). The gate uses their Richardson combination (4D(ε/2) − D(ε))/3 against ∇F·d; both raw values are reported. d₁ is tangent to the curved τ/z_rw ridge, so the numerator and log π are invariant to first order along it, and ∇(numerator)·d₁ ≈ 0 is reported too (wording corrected, Codex 76/2329) | relative 1e-4, or 1e-5 absolute |
| B4 | Coefficient-level ridge identity: `coefs` and log π_Q80 unchanged under τ → cτ, z_rw → z_rw/c for c = 0.5 and 2 | 1e-12 |
| B5 | Fresh FD log π against archived `log_pi_grad` (same h) | 1e-10 |

- **Recorded:** full vectors, signed discrepancies, per-piece timings, and
  source and environment hashes.
- **Host:** mac-mini, one process.
- **Ceiling:** about 9 Fisher evaluations and 30 whole-forest values per
  run, plus cheap log π and coefficient work. Frozen after a one-value
  benchmark: no more than 45 min wall.
- **Not in scope:** any fit, optimiser or sampler.

### Bridge results (23 October; mac-mini, 75 s wall against a 45-minute ceiling)

Files: [p11_bridge_results.json](p11_bridge_results.json),
[p11_bridge_benchmark.json](p11_bridge_benchmark.json) and the post-hoc
[p11_bridge_posthoc.json](p11_bridge_posthoc.json). Full signed vectors and
source hashes are inside.

| Check | central0 | high_rho_9707 | holdout_c4f_sigma15 | Tolerance |
| --- | --- | --- | --- | --- |
| B1: assembled ∇F against archived FD reference (max over 35) | 7.3e-7 pass | 6.7e-7 pass | **1.106e-5 FAIL** | 1e-5 |
| B2: Fisher, resolution and domain against primary | 1.1e-12 | 3.0e-10 | 1.4e-11 | 1e-5 |
| B3, d₁ (τ/z_rw ridge): Richardson FD of F against ∇F·d₁ | 2.8e-10 | 8.1e-10 | 1.9e-9 | relative 1e-4 / absolute 1e-5 |
| B3, d₂ (σ, ρ, κ) | 5.6e-10 (∇F·d = −0.642) | 7.2e-9 (0.415) | 3.3e-10 (−543.9) | same |
| B4: ridge identity (coefficients, log π) | 0.0 | 9.8e-16 | 1.0e-15 | 1e-12 |
| B5: fresh FD log π against archived | 0.0 | 0.0 | 0.0 | 1e-10 |

**Under the declared rule the bridge does not pass:** B1 fails at
holdout_c4f_sigma15. The label stands.

**Post-hoc attribution (labelled post hoc; not a re-run of the gate):**
- At that point the archived FD numerator (h = 1e-4) differs from the
  Fisher numerator by 1.106e-5. A fresh FD at h = 5e-5 differs by 2.77e-6,
  a ratio of 4.0006, the h² truncation law.
- **The Richardson-corrected reference agrees with the Fisher numerator to
  8.7e-9.**
- The B1 tolerance was mis-set by me. I sized it to the largest single
  tree's FD truncation (5.5e-6), but the reference is a sum over ten trees.
  The independent B3 check at the same point agrees to 3.3e-10 on a
  directional derivative of −543.9.
- **So the evidence locates the B1 discrepancy in the reference, not the
  assembled gradient.** That reading is post hoc, and Codex should judge
  it.

**Other findings:**
- **The ridge holds:** along d₁, which is *tangent* to the curved ridge,
  the numerator's directional derivative is 3e-10 to 1.8e-9. The exact
  finite scaling τ → cτ, z_rw → z_rw/c leaves the coefficients and log π
  invariant to 1e-15 (B4).
- **The prior/Jacobian gradient matches its own central difference** to
  ≤ 1.5e-7, the largest at ρ ≈ 0.99998. That gap comes from rounding in the
  constrained subtraction 1 − ρ, not from curvature (Codex 76/2329). A future
  callable should use the stable unconstrained form
  log ρ + log(1 − ρ) = −softplus(−u) − softplus(u).
- **Cost of the complete target gradient** (corrects the numerator-only
  figure): Fisher numerator 2.1–2.4 s (primary setting; 2.7–3.0 s at
  resolution) plus 0.03 s for the 70-call FD log π, plus the analytic prior.
  That is about 2.2–2.5 s per point on one mac-mini core. One whole-forest
  value costs 1.9 s.
- **Not in scope:** no fit, optimiser or sampler was run or selected.
