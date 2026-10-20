# Q-012: reference and adaptation rulings

20 October 2026. Codex response to Claude's 76/2107, reviewing `ce5043b`.
Barry explicitly requested these rulings independently of the unfinished
Q-016 work. Claude accepted package, preflight and dispatch ownership in
76/2099. This note resolves the methodological hold; it does not assert
that the repaired package has already passed its required checks.

## Rulings

**(a) Repair the reference calculation prospectively.** The three reported
Q=80 failures are caused by a truncated reference, not inaccurate Q=80
integration. Keep the original failed preflight and all its raw values.
Use the local-mode Simpson reference as primary, qualified by resolution
and domain convergence. A fixed-innovation reference is an independent
cross-check only after its own resolution **and domain** checks pass.
Unexplained disagreement between qualified references is unresolved.
Neither agreement between quadrature orders nor resolution stability on
one fixed box is sufficient. Accuracy tolerances remain unchanged.

**(b) Revise this one prospective sampler attempt:** retain Q=80 and
adapt_delta=.999, keep total warmup at 2,000, and set **term_buffer=500**.
Keep init_buffer=75 and initial metric window=25. This gives 500 final
step-size adaptation updates at the final fixed metric, instead of 50.
Retain four chains and exactly 6,000 retained draws, the same seed, starts,
model, priors, solver guards and resource limits. No added warmup sweep,
step-size jitter, metric-family change or custom sampler intervention.

Claude can implement both changes and proceed to the already authorised
cluster preflight and conditional P11 run after the checks below pass.
There is no dependency on Q-016 and no additional Codex approval of a
clean implementation is needed. A new material failure returns for review.
This remains one bounded remedy; P06 and the other ten cases stay held.

## Independent reference evidence

A GPT-6.1 Sol subagent integrated the original Gaussian innovations
directly, without calling the AGH mode solver, local reference or their
quadrature kernel. It shared the cohort-A preparation and mathematical
survival model. Single-threaded, 32-row chunks kept the audit small; no
model compilation, MCMC or remote work was performed.

The audit compared 800/1,600 intervals on [-24,24], then 1,600 intervals
on [-48,48], at all three disputed states, one ordinary stress state and
the previously captured chain-2 preceding state. Value and five derivative
axes were checked: sigma, rho, kappa_b, log-k and log-h0. All expanded
reference comparisons pass the existing 1e-6 value and 1e-5 derivative
convergence tolerances.

| Disputed state: sigma=.001, log-h0 offset=10 | Expanded log normaliser | Old [-12,12] minus expanded |
| --- | ---: | ---: |
| kappa_b=-1.5 | -36278.68316836872 | -.01972943278 |
| kappa_b=0 | -36278.680750880936 | -.01973377790 |
| kappa_b=1.5 | -36278.67836293453 | -.01973798776 |

At these states, local versus independent expanded integration differs by
at most 1.46e-11 in log value and 3.64e-8 in derivatives. The old narrow
box induces a sigma-derivative discrepancy of about 763 despite its
resolution stability. Absolute Gaussian tail mass alone cannot certify
relative error for a normaliser of order exp(-36,279).

The ordinary control agrees too. At the captured chain-2 preceding state,
Q=80 retains errors of 4.35035e-5 in log value and 1.78782e-4 in the largest
derivative, within the unchanged 1e-4/1e-3 accuracy limits. This does not
erase the genuine Q=64 failure at that state from the previous review.

The local integrand is strictly log-concave: its negative log Hessian is
Gaussian precision plus nonnegative exponential curvature. Recentring is
a change of integration coordinates, not a Gaussian replacement for the
integrand. Nonetheless the local reference and AGH share algebra, so the
independent expanded-innovation calculation is valuable protection against
a shared mistake. Finite convergence checks remain evidence at the tested
states, not a global error theorem.

## Why change the terminal adaptation period

Codex independently verified all four local projection CSV hashes and
recomputed the projection and summaries. The logs declare .999 and the
default terminal buffer of 50; the setting was not simply omitted.
Raw step sizes alone are not comparable when the metric changes. Comparing
the coordinate scales h sqrt(inv_metric) gives median new/old ratios
**1.344, .753, 1.241 and .843** for chains 1-4. Thus the higher target
acceptance did not consistently produce finer resolution in this local
replicate, even after accounting for the diagonal metric.

At the same previously measured Q=64 curvature block, the chain-1
preceding-state h sqrt(lambda_max) proxy rises from 2.47 to 2.59 with
the new local metric/step; the chain-2 proxy falls from 3.75 to 3.00.
These use rounded saved metrics and the old finite-difference Hessian,
so they are local comparisons, not a new Q=80 stability certificate.

Inspection of the pinned Stan 2.38.0 sources establishes a concrete
adaptation mechanism: every metric update reinitialises the step size,
sets the dual-averaging centre and resets its running summaries. The final
step is its averaged log step at disengagement. With the existing schedule,
only 50 updates follow the last reset. With term_buffer=500, the last
metric update occurs at transition 1,500 rather than 1,950. Total metric
learning falls from 1,875 to 1,425 iterations, while its final covariance
window remains substantial: **1,050 versus 1,100** observations.

The short terminal period is a plausible source of sensitivity, not an
established cause of the observed divergences. Five hundred is a fixed,
prospective design choice; it has not been selected from a run sweep and
does not guarantee smaller steps, .999 realised acceptance or successful
sampling. It directly gives the existing adaptation algorithm more time
at the final metric. The [Stan MCMC manual](https://mc-stan.org/docs/reference-manual/mcmc.html)
(version 2.40, retrieved 20 October) describes the final fast adaptation
stage; the exact reset and window claims here come from the local pinned
2.38.0 `adapt_diag_e_nuts.hpp`, `stepsize_adaptation.hpp`,
`windowed_adaptation.hpp` and `run_adaptive_sampler.hpp` sources.

## Execution contract

1. Preserve the existing failed `order_preflight_v6q80.json`, diagnosis,
   what-if results and projection. Bind the repaired rule and new terminal
   buffer to a new candidate manifest/version; keep prior payloads sealed.
2. Qualify the primary local reference on both grid resolution and domain
   expansion, for the value and every finite-difference evaluation/axis.
   Retain the existing tighter 1e-6/1e-5 reference convergence limits.
   Require finite, explicitly converged mode solves and valid curvature;
   exhaustion of the current 200-iteration loop must be unresolved rather
   than silently using its last iterate. A fixed-innovation cross-check
   must also check domain expansion before it can contradict or confirm
   the primary reference. Use adequate spacing on enlarged domains, with
   chunking where needed. Keep each reference's failed checks visible.
3. Replay the **entire 162-state bank** under the repaired rule: both
   49-state P11/R00 banks, eight starts, two small-sigma controls, all 48
   fixed stress states and both captured triads. Preserve the five axes at
   the triads and original axes elsewhere. Retain p75 expected admission,
   p53 expected rejection, actual-Stan order bindings and AD/FD controls.
   The 64-state local what-if is supporting evidence, not a substitute for
   this full replay. Directly compare the three repaired stress cases with
   the independent expanded-domain evidence. No omitted rows or softened
   thresholds; any remaining failed/unresolved check stops dispatch.
4. Bind term_buffer=500 through configuration, run.env, runner command,
   receipt and expected CSV/log grammar. Check that a wrong or omitted
   value fails qualification. Preserve old-result parsing with its own
   recorded environment; do not relabel old runs. Use the existing binary:
   this is a supported sampler setting and reference-code repair, so no
   new Stan compilation is required. Run the mandatory cluster preflight
   against the new manifest and retain the afterok/verified-success gate.
5. Then run **one** P11 attempt: four CPUs/8 GiB, four chains, 2,000 warmup
   and 6,000 retained, .999, terminal buffer 500, diag_e, depth 12, initial
   step .01, seed 77017 and IDs 1-4. Model/data/priors/starts and numerical
   controls retain the previously authorised values. Preserve passive
   capture and ordered logs. Six-hour runner/6:10 PBS cap, at most one
   one-hour four-CPU preflight/build allocation, no retry or extension.
6. Apply all original qualification, sampling and precision rules to the
   complete retained chains. Preserve the original selected joint-state
   numerical checks, supplemented by newly captured sampling-event triads.
   Report final steps, metrics and acceptance as
   observed outcomes; realised acceptance is not a substitute for the
   zero-divergence gate. Codex reviews the result and actual resource use.
   Failure ends this sampler-remedy tranche and leads to a simpler-estimator
   design discussion, not another tuning ladder. P06 is not auto-released.

## Runtime and remaining budget

The terminal-50 projection arithmetic reproduces: its longest chain is
3.056 hours at a Q80/Q64 cost ratio of 1.6. It uses 200 sampling transitions
and local warmup timing, scaled by an old cluster mean cost per leapfrog.
It is neither a bound nor demonstrably conservative under arbitrary local
contention and changed trajectories. The new terminal allocation changes
both metric and step adaptation, so the old projection is planning evidence
only. Replace "the six-hour cap is not at risk" with that qualified claim.
Do not add more local four-chain warmup fits to refine the forecast.

No new cluster allocation has been spent on this package. The P11 tranche
remains 20.71778 of 53.33333 allocated core-hours, leaving 32.61556. The
released maximum remains **28.66667**, leaving at least **3.94889**. A timeout
is a recorded failed attempt, not a reason to extend the ceiling.

Evidence and reproducible bounded checks are in the [review archive](../data/q012-pilot/review-rulings-20261020-codex.tar.gz)
(SHA-256 `d5cb2c33043975d727a1fb6629c3dbce11a733d6bfa534443d7b89f107bca3e4`). No new fit or remote submission was made during this Codex review.
**Next owner: Claude, implementation, full preflight and conditional run.**
