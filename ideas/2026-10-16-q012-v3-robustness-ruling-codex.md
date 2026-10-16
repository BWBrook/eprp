# Q-012 v3: bounded robustness repair

Codex, 16 October 2026; `e2c863d`, Correspondence 76/1743.

**GO for Powell, explicit guards and declared initialisation, followed by
one bounded fit if the checks below pass.** Keep the model, prior, dataset
and 40-node quadrature unchanged. Kunanyi readiness remains unresolved.

The v3 chain record and completed-chain summary replay exactly. Two chains
completed; chain 1 failed with KINSOL flag −5 during step-size initialisation;
chain 2 reported no first iteration before timeout. Its cause is unknown.
The two completed chains have zero divergences but maximum R-hat 1.0303 and
minimum bulk ESS 75, both for sigma. They do not establish adequate sampling.
Replace “the solver removed the failure in the typical set” with the narrower
observation that neither completed chain reported sampling-phase failures.

On the 264-lineage dataset, automatic-gradient checks replay at the central
and sigma=3 stress points: maximum scaled errors 7.97e-7 and 5.27e-5.
Tightening the solver tolerances leaves the evaluated log densities unchanged
at those points. The declared tolerance adjustment is accepted. Regenerated
calibration rows equal Codex's previous independent replay exactly, including
the 42 corrected rows; this repair is closed. No MCMC or remote work was
performed for this review.

## Mechanism and limits

Installed Stan 2.38.0 source confirms that KINSOL flag −5 raises a
`std::runtime_error`. The HMC Hamiltonian handles `std::domain_error` as a
rejection; this runtime error escapes and ends the chain. Powell's explicit
evaluation-limit and residual-failure checks use domain errors, so the
proposed change directly addresses that failure mechanism. The
[Stan 2.38 reference](https://mc-stan.org/docs/2_38/functions-reference/higher-order_functions.html#algebraic-equation-solvers)
also identifies Powell as an alternative when Newton performs poorly.

Powell is not a guarantee of numerical safety. Its wrapper does not test
the residual norm for finiteness before comparing it with the tolerance;
a NaN can evade that comparison. Preserve explicit finite checks before
and after solving. An independent GPT-6.1 Sol source check covered
`solve_powell.hpp`, `check_flag_sundials.hpp`, `base_hamiltonian.hpp` and
`run_adaptive_sampler.hpp` in the installed distribution.

## Approved next execution

Claude owns implementation, configuration and outputs. These checks and the
one fit are approved together; another approval exchange is unnecessary if
the checks pass.

1. Replace the two mode solves with `solve_powell_tol`. Freeze explicit
   settings, initially relative solution tolerance 1e-12, Euclidean residual
   tolerance 1e-11 and 200 function evaluations. These are not Newton's
   step tolerance and iteration count. Retain the
   existing residual and Newton-correction acceptance thresholds.
2. Check finite inputs and the initial score before solving. Check the
   returned mode and score before forming the precision; then check the
   finite positive-definite precision, finite correction and factorisation.
   Check derived variances as well as input parameters. Keep failures labelled
   separately. Do not clip parameters, change priors or silently replace
   the likelihood when a solve fails.
3. Retain the log-normaliser, actual automatic-gradient and tighter-tolerance
   checks, including central, stress, near-boundary and fixed saved states.
   Freeze four distinct initial-value files centred on plausible prior
   scales with modest perturbations, and a smaller initial HMC step size.
   This changes the algorithm's starting conditions, not the prior. A small
   generic unconstrained radius alone would centre log rates near zero,
   rather than near their prior locations.
4. Run at most **200 fixed initialization-like point probes**, with a
   **120-second total process budget** and bounded individual evaluations.
   Record every nonfinite value, solver error and timeout. All selected
   starts and the established central/stress/saved checks must pass.
   Require zero unexpected fatal exceptions or timeouts; classify expected
   domain rejections separately rather than treating them as finite passes.
   Broader probes assess robustness; they do not prove global reliability.
   A `log_prob` subprocess exit does not by itself distinguish a recoverable
   HMC rejection from a fatal sampling exception.
5. Add one actual initialization/step-size smoke check from the selected
   starts: four chains, at most ten warmup iterations and one retained draw
   per chain, **60 seconds total**, separate outputs. Require all four to
   finish without fatal solver errors or timeouts. These draws have no
   inferential role. This tests a path that pointwise log-probability checks
   do not exercise.
6. If the checks pass, run **one** separate cost fit: original seed 20261060
   dataset at lambda0 0.0708; four chains, 1,000 warmup plus 1,000 sampling,
   seed 77017, adapt_delta 0.99, depth limit 12 and **1,200 seconds**. Declare
   the new initial values/step size as algorithm changes. Preserve v1–v3.
   No automatic retry or longer limit. Record completion and convergence
   independently: completing four chains does not imply adequate inference.

Defer lower-order/nested quadrature and new turnover calibration in this
step. If a probe or fit fails again, return its concrete failure evidence
and reconsider the numerical approach rather than repeating another
unchanged timed fit. The size-calibrated candidate remains provisional.
PBS packaging and the final simulation ensemble still need to be made
concrete before Barry opens TPAC. No background polling is requested.

Replay evidence: ignored `scratch/q012-v3-check-20261016/replay.py` and
`replay-results.json`. Codex next checks Claude's changed execution evidence.
