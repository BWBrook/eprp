# Q-012 run 4: stop the adaptive repair and accept the combined finite evidence

22 October 2026. Independent Codex review of result
`b6be66540770d1051c3afbbcf96e844c6b5f91f4`, implementation
`0fe89610f690658c5366328fb6551b6340e0f36d` and prospective declaration
`f863277a3f834841331fc81fb931774ffccbed4a`, at checkout `1a8a739`.
This follows the [run-3 review](2026-10-22-q012-run3-review-codex.md).
The [review evidence archive](../data/review-run4-implementation-20261022-codex.tar.gz)
contains the pinned inputs, reconstruction and fixture results.

**Adopted disposition:** preserve run 4 as **14 pass / 2 reference-unresolved**
and stop this adaptive-reference repair. Accept the finite tiny-forest
evidence using **qualified references across the declared methods**. That
clears the separately bounded P11 interior-node and fixed-point cost
check; it does not earn fitting or estimator selection. The two adaptive
warnings remain failures of that method's qualification. They do not erase
the earlier independently qualified tensor checks at those same controls.

## Receipt and implementation checks

The 1,152 reference tasks are complete, unique and version-bound. Rebuilding
all sixteen cells from them and the unchanged run-3 candidate tasks reproduces
every saved reference gradient, discrepancy, tightened change and decision
exactly. All five supplied fixtures pass, including preservation of returned
QUADPACK messages and their propagation into qualification. This review ran
only those small fixtures, including two central0 reference calls; no candidate
evaluation, new parameter-point investigation, batch or remote job was run.

The revised leaf substitution is correct: the Gaussian density and Jacobian
cancel in standardised coordinates; no log-s term is missing. Curvature 1
in the leaf coordinate and `1/sigma²` at the root are appropriate. The error
sum and prospective 1e-10 budget match the declared policy. Diagnostics are
now captured and cannot be overridden by a small estimated error.

The fourteen passing cells have no inner or outer diagnostic, and agree with
the candidate within 1.4211e-14 in value and 1.4211e-10 over all 35 derivatives.
The two sigma=8/high-rho controls have **58/72 diagnostic-bearing values in
T2 and 67/72 in T3**. All diagnostics are inner roundoff messages; none is an
outer diagnostic. All values meet the estimated-error budget, with overall
maximum 2.1478e-11 and maximum reported tail bound 5.2787e-32. A warning's
possibility of underestimated error prevents these estimates from clearing
the adaptive reference's own gate. The code correctly retains unresolved
status. No further numerical defect was found in this bounded review.

The full reference batch did run **after the negative 1.9 s smoke check**:
1,152 additional reference values took 70 s, within the declared 900 s limit.
This was disclosed before execution and established which other cells cleared
the corrected diagnostics. It incurred that extra cost, without repeating
candidate evaluations. Its result is now sufficient to stop the repair;
there is no reason to repeat it or search for another integrator.

## Why the two existing tensor checks remain usable

At `holdout_9707_sigma8`, both T2 and T3 already passed the frozen run-2
tensor-reference qualification. These were **full derivative checks**, not
central-value comparisons:

| Check, both controls | Value discrepancy | Maximum over 35 derivatives |
|---|---:|---:|
| Tensor resolution, 200 to 400 intervals | 0 | 3.5527e-11 |
| Tensor domain, Delta 50 to 70 | 0 | 3.5527e-11 |
| Candidate versus qualified tensor | 0 | 3.5527e-11 |
| Candidate self-resolution/domain | 0 | 3.5527e-11 |

The frozen code differentiates all 35 unconstrained coordinates at h=1e-4
for each setting. Run 2 retains the maximum across each complete vector and
the worst-coordinate pair, rather than the full tensor gradient vectors.
Consequently this review verifies their coverage through the audited code
and recorded reductions, not a fresh per-coordinate tensor replay. The
candidate algorithm, points and settings are unchanged; both saved central
values and saved worst-coordinate candidate derivatives match the run-3
vectors exactly. Reconstructing the full run-3 vectors also reproduces the
same candidate self-check maxima.

The tensor and message evaluators use different integration coordinates and
quadrature structures. They share local factors and mode-based/sinh placement
ideas, as disclosed. The known axis-section truncation concern means the
resolution/domain checks are **finite empirical numerical qualification**,
not an interval proof of omitted mass. At these controls those tests pass,
including every derivative. The adaptive method adds descriptive agreement:
zero value difference and at most 7.1055e-11 derivative difference. Its
warnings prevent qualification, but supply no contradictory numerical result.
Neither agreement nor method diversity supplies mathematical certification.

The original accuracy criterion requires comparison with **a qualified
independent reference**. It does not require every attempted numerical method
to qualify. Here the method is selected by its own convergence qualification,
then the candidate comparison is checked. No warning is waived, tolerance
softened or favourable central value substituted for a failed gradient test.
A new qualified-reference disagreement would reopen the issue; none is present.

## Exact combined scope and disposition

This is a combined development-evidence adjudication, not a retrospective
claim that one prospective run passed all 45 rows.

- **Twenty-nine cells outside run 4** retain their qualified run-2 passes:
  all fifteen T1 cells, and T2/T3 at `central1`, `low_rho`, `small_sigma`,
  `high_rho_9707`, `c1_previous`, `c4_failing` and `holdout_9707_sigma5`.
  Their recorded unit-factor and selection identities also passed.
- **Fourteen cells** have the clean run-4 adaptive reference: the six
  named problem states in T2/T3 plus central0 in T2/T3.
- **Two cells**, sigma=8/high-rho T2/T3, retain the qualified tensor
  reference above; the adaptive screen remains unresolved.

For the sixteen repaired/control cells, I1 is inherited from run 2. I2 is
supported by the declared qualified selection post-hoc check. In particular,
the four historical I2 failures at stress_s3_r09_kbm15 and c4_previous remain
historical failures against the old selection tensor reference; they are
closed by the qualified pair reference and unit-third-daughter transfer.
The actual stored T3/T2 selection difference was checked in the earlier
review: those four residuals are at most 1.6e-14, and the transfer across
all fifteen points is within 2.56e-8. This evidence is explicitly post hoc.
Decomposition also remains passed. Thus each of the 45 finite cells has
usable qualified-reference and identity evidence across this documented
sequence, while every individual run's labels and limitations remain intact.

**Parent Codex adopts this combined adjudication. Next owner: Claude.**
The hold is lifted **only** for
interior-node interpolation validation followed by fixed-point P11 cost.
Freeze a finite bank and execution ceiling before that work; benchmark first
and use it to size the check. Do not prescribe another large all-axis sweep
before knowing its cost. Benchmark one value first; freeze the finite bank
and resource ceiling using that measured cost before the batch. Use an
appropriate always-on host under the compute control-plane rules; no long
laptop run. There is no optimiser, MCMC, bootstrap, empirical
fit or estimator choice in this permission. The adaptive-reference sequence
ends here, with the two warnings preserved.

Pinned inputs, hashes, exact reconstruction, all supplied fixtures and the
two controls' detailed tensor/candidate comparison are in
`scratch/q012-run4-review-20261022/` for the parent's review archive. Existing
code/results, other agents' files and the Q-038 executable were untouched.
