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
- That would move collapsed HMC from infeasible to plausible. **The tree
  version is not built or tested here.** The batch's per-tree candidate
  gradients at all 15 points would be its validation data.
