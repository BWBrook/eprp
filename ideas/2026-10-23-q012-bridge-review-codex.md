# Q-012 full-target bridge: accept the combined finite evidence, retain B1 FAIL

23 October 2026. Independent Codex review at `e6adbea` of declaration
`9a55dc5` and results `b5f1e05`, following the
[fixed-point review](2026-10-23-q012-fixedpoint-review-codex.md). Review
scope: `p11_bridge.py`, benchmark/results/post-hoc JSON, the bridge
declaration/results in `p11_fixedpoint.md`, inherited evaluator sources,
the current Stan target and scientific contract. Only this note and
`scratch/q012-bridge-review-20261023/` were written. No fit, remote run,
batch, new reference integral or production modification was performed.

**Recommendation: close the finite three-point bridge using the combined
evidence. Preserve the declared result exactly: B1 FAIL at sigma15,
`all_pass=false`; B2–B5 pass at all three states.** One coordinate exceeds
B1's threshold. A bounded independent h-halving check closes that coordinate
with a post-hoc Richardson reference; the other thirty-four already meet
the original threshold. This is a development-evidence adjudication, not
a retrospective all-pass claim, absolute integration certificate or fit
authorization. No material target-assembly defect was found.

## Target and all-coordinate receipt audit

The target is the existing Q80 conditional model with the same non-frailty
priors, expressed in the thirty-five Stan unconstrained coordinates, up to
parameter-independent constants. Its implementation has the correct terms:

- The normalized Gaussian frailty forest is integrated in each numerator.
  Integrating the partially non-centred `w` density removes its measure
  transformation; no residual `-a*N*log(sigma)` or frailty prior is added.
- The non-frailty prior terms match `model_v6.stan:205–215`, including the
  scale-0.5 priors on tau and log_k, scale-1 sigma prior, all twenty-four
  standard-normal z_rw terms and uniform rho. The parameters called log_k,
  log_lambda0 and log_b0 are unconstrained Stan parameters themselves, so
  they do not acquire exponentiation Jacobians.
- The remaining Jacobian is `log(tau)+log(sigma)+log(rho)+log(1-rho)`.
  Its analytic gradient, including `1-4*tau²`, `1-sigma²` and `1-2*rho`,
  is correct in log-tau, log-sigma and logit-rho coordinates.
- The denominator is subtracted once: four singleton normalizers for
  lineages 1, 3, 4 and 6, plus one joint normalizer for (2,5), matching
  Stan's C1/C2 loops at lines 230–238. The pair is neither squared nor
  replaced by a product of marginal factors. Pre-entry survival remains
  in the six cohort members' numerator factors once.

The receipt replay (`replay.py` in the archive below)
verifies all eight saved source hashes against this checkout, complete
finite 35-vectors at all three points, and **exactly reconstructs every
entry of `grad_full` and `B1_signed`**, B1 maxima and the sole failed
coordinate from the archived tree gradients and separate denominator and
prior vectors. It reconstructs each B3 Richardson arithmetic/error and
directional prediction (the cross-platform dot-product difference is at
roundoff), and re-evaluates the cheap denominator gradients. Their largest
cross-host difference is 2.22e-11, below B5's 1e-10 tolerance. Separate
component evaluation reproduces each saved normalizer value exactly.
A sentinel substitution confirms four one-dimensional calls, one joint
call, unit coefficients and the negative denominator sign.

Saved full-target value assembly agrees within 2.84e-14; the prior-value
cross-host difference is at most 3.55e-15. B2's resolution/domain vectors
are reduced to maxima in the result file, so those maxima are read from
the saved execution record, not independently reconstructed or rerun here.
Likewise the B3 underlying plus/minus full values are not archived; their
saved directional quotients and subsequent arithmetic are auditable.

| Point | B1 maximum across 35 | B1 disposition | B2 maximum |
| --- | ---: | --- | ---: |
| central0 | 7.26131e-7 | pass | 1.14072e-12 |
| high_rho_9707 | 6.74153e-7 | pass | 2.98155e-10 |
| holdout_c4f_sigma15 | 1.10640e-5, kappa | **FAIL** | 1.37561e-11 |

At sigma15 the next-largest B1 difference is log-sigma, 5.62031e-6;
all other coordinates meet 1e-5. B3's largest discrepancy is 7.18776e-9.
B4's maximum is 1.01503e-15; saved B5 is zero at all three points. The
75.098 s run is within the declared ceiling. Primary Fisher plus measured
denominator-FD time is 2.12917–2.44337 s; analytic prior assembly is
additional cheap arithmetic, not separately timed. Thus 2.2–2.5 s is a
reasonable rounded **assembled-gradient** cost estimate, not a measured
fit cost or prediction of gradient count. No extra numerator value is
needed if the callable returns Fisher's value and gradient together.

## Findings, ranked

**MINOR — retain the failed prospective gate and label the supplementary
reference as post hoc.** The existing disclosure does this correctly.
There is no need to change the threshold or rerun all thirty-five axes.
The original B1 tolerance budget used a per-tree FD discrepancy for a
sum over ten trees; their truncation errors add. Agreement of B5 removes
denominator differences from this B1 comparison, and the common prior
vector cancels, leaving the numerator derivative comparison.

The new independent check evaluated **two** whole-forest numerator values
at kappa ±5e-5, using one CPU and a 58 s external timeout; it completed
in 13.48 s. Its full per-tree values are preserved in
`kappa_halfstep.json` in the review archive.
Against the already saved Fisher value, it exactly reproduces the reported
post-hoc gaps and ratio:

| Quantity, sigma15 kappa numerator derivative | Result |
| --- | ---: |
| Archived FD at h=1e-4 | 87.09480039255979 |
| New FD at h=5e-5 | 87.09479209414894 |
| Saved Fisher | 87.09478932855316 |
| Gap ratio | 4.000587036217418 |
| Richardson minus Fisher | -5.41178e-10 |

This independently supports h-squared reference truncation for the sole
failed coordinate. The committed post-hoc file additionally reports an
all-coordinate Richardson maximum of 8.67207e-9, but contains only seven
summary scalars, without half-step/Richardson vectors or generating script.
That full-vector maximum is **reported, not independently reconstructed**.
It is unnecessary to the present closure: the thirty-four original passes
and the reproduced kappa supplement cover all thirty-five coordinates at
the original tolerance. Do not promote the post-hoc maximum into an
absolute error bound for the exact integral.

**MINOR — describe d1 as a tangent direction.** The finite ridge
transformation is `u_tau -> u_tau+log(c), z -> z/c`. B3 instead follows a
straight line tangent to that curved path; its numerator derivative is
zero at the base point, but its finite displacements do not preserve the
numerator exactly. B4 checks the actual finite transformation. Both tests
are sensible; the prose saying the target is invariant "along d1" should
say that its likelihood directional derivative vanishes at the base.
The prior supplies the nonzero posterior derivative. This preserves the
reason to prefer same-prior collapsed Bayes over pure MML in the current
coordinates; it does not imply a Bayesian posterior identification failure.

**MINOR — correct the prior-FD discrepancy explanation.** The recorded
1.50568e-7 prior/Jacobian FD discrepancy near rho=1 is not evidence of
steep curvature in the unconstrained logit-rho coordinate. There,
`d²(log(rho*(1-rho)))/du_rho² = -2*rho*(1-rho)` is small. A stable direct
log-Jacobian expression using two log-sum-exp terms is identical in value
at these points; its FD derivative agrees with the analytic formula much
more closely. Subtraction in `1-rho` and constrained-coordinate rounding
are the relevant numerical concerns. Use stable unconstrained expressions
in any future sampler callable and retain explicit invalid-state guards;
the current fixed-point evidence needs no rerun or source repair for this.

## What this earns next

The inherited six unresolved interior-chain references remain unresolved.
This bridge assembles the existing **Q80 numerical target**; it does not
replace Q80 by the exact selection integral or prove global quadrature
accuracy. B2 tests Fisher discretization sensitivity; it does not prove
that the score-based vector is exactly the derivative of the moving-node,
Hermite-table numerical value everywhere. Finite agreements do not establish
smoothness across table/guard changes, trajectory stability, stationary
sampling, mixing, effective sample size or the scientific simulation
contract's operating characteristics.

The next useful route is a **bounded sampler-engineering feasibility
contract for same-prior collapsed Bayes**, not another reference-repair
campaign and not a fit. The cheapest substantive screen would expose a
deterministic joint value/gradient callable, verify stable coordinates and
explicit invalid-state behavior, then run a frozen small set of short
forward/reverse leapfrog maps from fixed states. Record round-trip error,
Hamiltonian error, actual gradient counts/time and failure handling; freeze
the states, step sizes, path lengths and ceiling first. This can distinguish
an integration/regularity problem from the historical latent-frailty solver
failure without adaptation or posterior draws. An acceptance-corrected
sampler must use the declared numerical target value; an uncorrected
approximate-gradient trajectory is not posterior evidence.

This is a proposed next contract for parent Codex and Claude to adjudicate.
No sampler or optimiser has been selected or run by this review, and the
no-fit boundary remains. Parent Codex integrates the disposition and hands
the next scoped work to Claude.

## Evidence pins

SHA-256 at review:

- `p11_bridge.py`: `3f390f7b0ee164c048fa49bf304027441594fa7af96c3b0fa1d718ee2b0b29c3`
- `p11_bridge_results.json`: `6c2bb247e9392f91b92eddfa5c1691d709a8daec9fe3471ffd3fbca3bda27801`
- `p11_fixedpoint_run.jsonl.gz`: `9836094ea7f4777152f85aca3b411d20c63f5737deba5d0b6d4a24e6627c3479`

Exact reconstruction, normalizer components, source pins and the new
two-value receipt are preserved in the
[review archive](../data/q012-pilot/review-bridge-20261023-codex.tar.gz).
Extract it at the repository root to restore
`scratch/q012-bridge-review-20261023/`; the scripts resolve that layout.
The preserved untracked raw P11 JSONL was not modified.

Parent Codex accepts the combined-evidence closure and recommends the finite
engineering contract above as Claude's next proposal. No fit is selected.
