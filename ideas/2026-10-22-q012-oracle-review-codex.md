# Q-012 collapsed oracle: independent review of run 1 and declared repairs

22 October 2026. Codex review pinned to repository baseline
`4a9b4bbf65c37e267def60a825d8b1a4c4f7ddfb`. Frozen specification:
`ad09251c6888daa4eaab39eb82b14cf6fbb8a1a7`; run-1 code:
`7ecf5679ac36a0adcdd0dc861d141442f61ddf55`; result/report:
`9ebc27cda05e05994350783da88414265b52cf3e`; repair declaration:
`349dd3da61db91c3cc4c6a97be9a9b52fa76ba42`; repaired implementation:
`8962871211034c165f20bd3bc7adf49a588a1b52`.

**Recommendation:** accept run 1 as a correctly disclosed failed numerical
screen and the repairs as specific, plausible responses. The repaired scalar
case passes a new independent check. A fixed-point P11 evaluator/cost check is
**not yet earned**: run 2 was still running when this audit began, and the
reference/decision issues below need resolution when adjudicating its output.
No optimiser, fit, HMC, bootstrap, cluster job or full oracle replay was run.
Final P11's 2/24,000 divergences and the end of sampler tuning remain settled.

## What is supported

The selected-tree factorisation is correct for the stated working model.
`coefs` includes cohort pre-entry survival once, the full post-entry exposure
and event factors, and the proper powers of frailty. Root and edge Gaussian
densities have their normalising constants; innovation integration correctly
uses standard normal densities without an additional determinant. The
selection denominator stays outside the numerator and descendant messages.
Priors are expressly outside this oracle. The decomposition checks the old
innovation target, not a new unconstrained collapsed posterior: a later Bayes
implementation must retain the global priors and log-scale/logit Jacobians.
Collapsing 19 frailties leaves 35 coordinates; no MML target is selected.

Recounting the immutable [run-1 JSON](../data/q012-pilot/collapsed_oracle_results_run1.json)
reproduces **24 pass, 3 fail, 3 reference-unresolved**, with
`decomposition_pass=true`, `all_pass=false`. Maximum decomposition error is
1.46e-11; unit-factor error 1.97e-15; selection-only discrepancy against the
reference 4.76e-9. Among passing rows, maximum evaluator/reference errors are
5.02e-8 in value and 1.17e-6 in derivatives. The sigma=12 evaluator domain
failures and sigma=3.34 reference derivative failures are already disclosed;
this review does not recast them as new findings.

The sinh Jacobian and Armijo signs are correct on inspection. The pre-run
record candidly distinguishes smoke-tested points from the two fresh
hold-outs. Run 2 is a repair test, not another prospective run 1.

## Findings, ranked

### Major: the independent value check does not affect qualification

In repaired code lines 464–475, `quad_reference_minus_ref` is recorded but
never enters `ref_ok`, `acc_ok` or `status`. An exact control-flow check using
the frozen `task` function, substituting inexpensive deterministic inputs,
returns **pass with a Gauss–Kronrod discrepancy of 0.01**. This is a decision
logic counterexample, not an observed integration error in the scientific
points. Run 1's actual passing T1/T2 discrepancies are at most 4.09e-8.

The adaptive reference also discards QUADPACK's error estimates and uses
finite bounds without its own domain check (lines 323–347). In T2 its outer
box uses the root's local factor without the daughter message; inner bounds
are anchored at the Gaussian mean, rather than the conditional factor's
mode. Those choices may work, but adaptive accuracy inside the box does not
qualify its tails. Calling this the source of “true independence for values”
needs a qualified domain and a disagreement decision. It supplies no
independent derivative check as currently implemented.

**Required adjudication:** incorporate the available independent value
comparison into the qualification decision; retain its error/warning and
domain evidence. A material disagreement makes the reference unresolved
until explained. Apply this first to returned output; do not automatically
launch another full run.

### Major: evaluator exceptions must not become reference-side unresolved

The shared `Unresolved` handler at lines 476–477 catches evaluator mode,
curvature, line-search and bounds failures as well as reference failures.
An injected evaluator mode failure returns generic **unresolved**, with no
stage. This contradicts the frozen distinction between an evaluator failure
and a reference-side inability to decide accuracy. Separately, `all_pass`
at line 493 omits `decomposition_pass`.

No such exception changes the run-1 count above. For the returned repair,
classify exceptions by the operation that failed, and require decomposition
as well as all row gates. The specification's “passes or is unresolved”
sentence can define a completed report; it cannot define a numerical pass
that earns P11 work. Unresolved remains unresolved.

### Moderate: axis sections are not projected joint level sets

`ref_box`, lines 297–300, holds all other innovation coordinates at the
joint mode. These are axis **sections**, not profiles maximised over the
other axes. Correlated mass can extend far outside their Cartesian box.
For an analytic concave Gaussian with precision
`I + 10^6 * ones((2,2))`, the Delta=50 axis section has half-width 0.010,
while each marginal SD is 0.707. The box contains at most **1.13%** of
the total mass. This example challenges a guarantee from concavity alone;
it is not a newly observed failure of the Q-012 points. The existing domain
check would expose substantial truncation in this particular Gaussian.

Keep resolution and domain checks explicit for every point, especially T3,
which has no second quadrature family. If a point is unresolved, a projected
domain or independent tail bound is an informative repair; do not infer
coverage from a 50-nat axis drop. The shared sinh node placement is disclosed
and weakens independence further, particularly for T1.

### Moderate: tiny-tree arithmetic is not a P11 cost measurement

The 365,619 nominal kernel count is correctly labelled arithmetic. The
repaired root domain search repeatedly calls `hroot`, and each call computes
child integrals; mode finding, bracketing/bisection and finite differences
add work. P11's interior interpolation remains unimplemented and untested.
Run 1 took 5,925.72 s on the laptop; its tiny per-call timings do not make
another large local sweep a cheap probe. An eventual P11 check must measure
actual evaluation cost and interior-message accuracy before choosing any
estimator. It earns no fitting allocation by itself.

## New bounded numerical evidence and next action

The scratch audit extracts functions from the pinned commits rather than
importing a changing oracle. For **T1 only**, central0, c1_failing and
c4_previous were compared against adaptive scalar quadrature with a separate
scalar optimiser and concavity-based tangent tail bounds, without the
evaluator's mode, level-bound routine or sinh nodes. Local coefficients are
shared and declared. Maximum discrepancies were **3.56e-15 in value and
3.56e-11 across all 35 finite-difference derivatives**. Quadrature relative
error estimates are at most 4.36e-13; relative tangent tail bounds at most
8.14e-42. Halving the difference step at c1_failing changes the log-sigma,
kappa_b and log-k derivatives by at most 1.79e-7, below the frozen derivative
gates. This supports the scalar repair; it does not qualify T2 or T3.

The original bounded audit took 8.62 s and reported approximately 1.26 GiB
peak RSS. Its original script/result are preserved separately from the revised
self-contained replay in the [durable review evidence archive](../data/review-oracle-contract-20261022-codex.tar.gz).
The archive includes the two selected full unconstrained state vectors, exact
source paths/transitions, source-line and vector hashes, committed raw-file
manifest hashes, and the pinned source/data snapshots. `audit.py` resolves
inputs relative to its own location and refuses to overwrite an existing
receipt. Its new replay, run once from `/tmp`, took 5.68 s and exactly reproduced
all scientific checks; only runtime/provenance fields differ. No large ignored
fetch trace or Git checkout is needed for replay. See the bundled `README.md`
for the command. This is post-hoc review evidence; it does not replace the
prospective result. No full-bank replay was attempted.

**Next responder: Claude**, after the parent Codex integrates this review.
Finish the already running repair report, distinguish fresh from exposed
hold-outs, and adjudicate its existing rows with the qualification and status
corrections above. Return the unresolved/failure list and the independent
comparison evidence. If every required point then passes with qualified
references, consider one explicitly bounded fixed-point P11 evaluator and
cost check, including an interior-node test. Otherwise retain the failed or
unresolved route and state the one concrete cause; no new sampling ladder.
