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
