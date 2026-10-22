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

## 6. Benchmark, frozen bank and ceiling

(Filled in after the one-value benchmark, before the batch.)
