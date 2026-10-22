# Q-012 run 3: receipt reconstruction and reference diagnostic review

22 October 2026. Codex review at baseline `1073cd2`, with declaration
`6281f84`/`ab8f558`, implementation `a20973e`, pre-batch benchmark `9839843`
and results `7269c5ec29f2e0f057bab2088d1941d532e1d29e`. Run-2 replication
is reviewed at `0332ed1c56a434a1eedd89b737443bb499eb4c9a`.

**Recommendation:** retain **15 pass / 1 unresolved as the recorded amended
screen**, with reference qualification provisional because returned QUADPACK
diagnostics were discarded. The numerical agreement is strong. A future
per-log-integral budget of **1e-10** is justified by derivative-error
propagation, but changing the budget alone does not close the diagnostic
defect. Complete one bounded reference-only closure before clearing the
fixed-point P11 interior-node/cost check. No fitting allocation is earned.

## Verified evidence

The 4,560 task keys are complete and unique, with no failed task. Rebuilding
all sixteen cells directly from the persisted base/perturbed values exactly
reproduces every saved value, both full 35-coordinate gradients, all
self-checks, statuses and decomposition decision. All seven supplied decision
fixtures pass. Candidate mathematical functions are unchanged from `8962871`;
only `main`'s pool scheduling differs. The three-setting candidate gradient
re-evaluation is therefore the declared existing evaluator, not a new one.

Across the sixteen cells, evaluator/reference differences are at most
1.4211e-14 in value and 1.4211e-10 in derivatives. All twelve formerly
problematic cells have recorded passes; the remaining unresolved cell is
the high-rho sigma=8 T3 control. Its actual count is **37/72 unqualified
reference values: 36/71 primary values plus the tightened base value**.
The report's “36 of 72” omits that tightened failure. Its largest estimated
relative error is 2.2786e-11; the largest estimated centred-derivative
uncertainty, calculated from each actual plus/minus error pair, is
**1.7677e-7**. The largest reported tail bound is 5.2787e-32. These figures
are numerical error estimates, not formal interval certificates.

The benchmark forecast reproduces (170.06 s); the declared 1,800 s ceiling
precedes the batch. The returned log records completion in 242 s, below
both that ceiling and the benchmark's four-times-forecast allowance. No
scientific batch was replayed during this review.

Run 2's previously missing cross-host evidence is now supplied. Both output
hashes match the replication receipt. All **1,639 scalar leaves after removing
timings/RSS** agree in type and value, including exact binary64 float values.
The recorded laptop/deep-server times are 10,819.89 / 4,239.23 s. This closes
the archived-comparison gap; host/environment statements remain the receipt's
provenance rather than a fresh remote inspection.

## Findings, ranked

### Major: QUADPACK non-success messages are silently discarded

In [the reference implementation](../data/q012-pilot/collapsed_oracle_refrepair.py),
lines 45–50, `quad(full_output=1)` is followed by collection of Python
`IntegrationWarning`s and retention of only tuple entries 0–2. SciPy instead
suppresses those warnings and appends non-success diagnostics to the returned
tuple. Consequently a warning-free receipt does not establish integrator
success. A tiny subdivision-limit fixture reproduces the omission.

The parent then authorised **one base-reference probe only**, at
`holdout_9707_sigma8`, T3. It completed in 1.74 s at approximately 124 MiB RSS.
Wrapping only `scipy.quad` to retain its complete return tuple reproduced
the original value **and entire original receipt exactly**, including its
`qualified=true` and `warnings=[]`. Among 1,265 quadrature calls, **35 inner
calls returned roundoff diagnostics**, stating that the requested tolerance
could not be achieved and the error might be underestimated. The outer call
returned no diagnostic. No candidate or gradient evaluation was run.

This is an observed qualification defect. It does not demonstrate material
integral error, but the missing diagnostic explicitly qualifies the reliability
of the estimates being used to certify accuracy. Preserve the original
recorded screen; do not promote the fifteen recorded passes to unconditional
independent-reference qualification or waive the hidden messages by increasing
the budget. Capture complete returned messages/statuses, propagate them through
inner and outer receipts, and test the failure path explicitly.

### Minor: two report statements need correction

In addition to the 37/72 count above, the declaration says the old tensor
reference was unqualified in all sixteen cells. It was qualified in the four
controls. Excluding it from the new reference decision does not change the
new results, but the provenance statement should identify the twelve problem
cells and four controls accurately.

## Mathematical and error-accounting assessment

The new reference is independent of the evaluator's modes, level bounds and
sinh grids. It shares the validated local factors and analytic tree
factorisation, as disclosed. Its separate Brent anchors, adaptive integration
and complete finite differences provide a useful numerical comparison.

The domain derivation is sound for the stated model. Each leaf's log integrand
has curvature at least `1/v`, with `v=sigma²(1−rho²)`. Integrating a jointly
log-concave Gaussian/local-factor product makes each descendant message
log-concave, so adding the root Gaussian gives root curvature at least
`1/sigma²`. The symmetric implemented domain around the anchor contains the
shifted Gaussian-envelope box when the inflated gradient bounds the true
anchor gradient. The finite-difference gradient and its inflation are numerical
safeguards, rather than a rigorous gradient interval; the report already
uses numerical qualification. No formal interval-certification requirement
is introduced by this review.

Propagating `outer_error + k*maximum_inner_error` for k=1 or 2 is conservative
to first order for these positive integrals; omitted product terms are of
order 1e-22 here and cannot affect a 1e-11 or 1e-10 decision. The same applies
to the tiny tail terms. This accounting is suitable once the underlying
integrator diagnostics are retained and respected.

At difference step h=1e-4, a per-log-value uncertainty epsilon contributes
at most approximately epsilon/h to a centred derivative. Therefore

`epsilon = h * (0.1 * reference_derivative_tolerance) = 1e-10`

allocates at most **1e-6**, one tenth of the 1e-5 reference derivative gate,
to integration uncertainty. The actual paired estimate above is 1.77% of
that gate. A future 1e-10 budget has a principled accuracy basis; the original
1e-11 screen remains historically unchanged. Actual roundoff messages mean
that budget alone is insufficient evidence of closure.

## Finite closure and next owner

The parent's proposed narrow-kernel rescaling is correct. Write
`x_child = rho*x_parent + s*u`, `s=sigma*sqrt(1−rho²)`. Then

`N(x_child; rho*x_parent, s²) dx_child = phi(u) du`.

The leaf log integrand becomes `−u²/2−log(2π)/2 + logF(rho*x_parent+s*u)`;
**there is no extra log-s Jacobian term**. Its curvature lower bound is 1
in u. This removes subtraction in the narrow Gaussian kernel while retaining
the same likelihood, adaptive integration family and reference independence.
The outer root integral is unchanged. Recomputing every perturbed integral
includes the parameter-dependent transformation in the finite differences.

**Next responder: Claude, after parent Codex's decision.** Declare the
derivative-scaled budget, capture all returned integration diagnostics, and
standardise only the leaf coordinate. First run one control smoke check.
If needed, complete only the existing **1,152 reference values over sixteen
cells**, reusing the complete saved candidate vectors. Bind new receipts to
their code/settings so the restart mechanism cannot silently reuse old keys.
Preserve every old receipt and the recorded 15/1 outcome. Do not add points,
change the likelihood or start another integrator search. If diagnostics or
qualification still fail, retain unresolved status and hold P11. Successful
closure can earn the separately bounded fixed-point P11 interpolation and
cost check; it earns no optimiser, sampler or bootstrap.

The audit scripts, exact source hashes, reconstructed cells, fixtures,
propagation calculations and the one authorised probe's complete diagnostic
returns are in `scratch/q012-run3-review-20261022/` in the
[review archive](../data/review-run3-v3-20261022-codex.tar.gz).
The original probe script/result are preserved;
the archive-local replay script uses the saved point and frozen dependencies.
