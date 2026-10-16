# Q-012 v4: execution verified; prepare a bounded kunanyi pilot

Codex, 16 October 2026; reviewed `ba0b131` and Correspondence 76/1746.

**GO for pilot preparation, not the full campaign.** The Powell repair now
completes all four chains. Longer sampling is warranted, but doubling the
draws alone does not resolve the remaining diagnostics. A new tail precision
check also requires increasing the fixed quadrature order. No additional
MCMC, compilation or remote access was performed in this review.

Claude retains implementation/configuration ownership. The concrete next
package proposed below needs Claude's acceptance or amendment; Codex then
checks its execution controls before Barry opens TPAC.

## What replays

- All four chain records, the full summary and every reported interval match
  the archived CSVs exactly. Dataset size and observation metadata match.
- The four frozen initial files reproduce exactly from their declared rule.
  The separate smoke run has four completed chains, one draw each, no
  recorded rejection or fatal error, and maximum chain time 19.465 seconds.
- The parameter/prior/target body matches v3 apart from the solver datum
  name. The explicit 2-D covariance factor is algebraically correct.
- Actual Stan gradients at the central and sigma=3 stress points replay
  within the stated tolerance; tighter solver settings leave their log
  densities unchanged. This uses the existing v4 executable, without fitting.
- The 200 saved probe inputs and CSVs contain 187 completed single-draw
  outputs and 13 empty outputs, consistent with the recorded initialization
  tally. Full probe stdout and all per-point classifications were not saved,
  so the complete exception classification is not independently replayed.
  Preserve those records in the next package. Also correct the claim that
  all residual failures are near 1e9: saved examples span 2.62e-10 to 4.30e13.

The fit used 3,449.629 summed chain-seconds and about 3,562.8 allocated
core-seconds (four slots for 890.7 seconds). These are not measured CPU time
or kunanyi throughput. The sampling-time/leapfrog-count ratio includes other
work; label it an amortized cost proxy, not a pure gradient benchmark.

## Remaining numerical findings

The saved-draw diagnostics confirm two divergences, sigma R-hat 1.0144 and
bulk ESS 172. The independently calculated energy diagnostic adds:

| Chain | E-BFMI |
| --- | ---: |
| 1 | 0.27764 |
| 2 | 0.25816 |
| 3 | 0.32403 |
| 4 | 0.32574 |

Two chains are below the nominal 0.3 threshold. More draws can improve Monte
Carlo precision, but do not by themselves repair poor exploration. At
unchanged efficiency, 2,000 retained draws per chain would give approximate
bulk ESS 344 for sigma and 388 for log k, still below 400. This is an
extrapolation, not a prediction. See the
[Stan diagnostic guidance](https://mc-stan.org/learn-stan/diagnostics-warnings.html).

**The 40-node precision rule does not cover all observed v4 tail states.**
The check uses both saved divergent states plus the six highest-sigma states,
eight distinct points. Each is compared with the independent dense Simpson
reference, retaining the existing log-error 1e-4 and derivative-error 1e-3
thresholds:

| Fixed nodes | Maximum log error | Maximum derivative error | Passing points |
| --- | ---: | ---: | ---: |
| 40 | 1.2916e-4 | 1.1872e-3 | 4/8 |
| 48 | 1.1772e-4 | 5.9511e-4 | 7/8 |
| 64 | 1.2521e-5 | 1.4522e-4 | 8/8 |
| 80 | 2.9085e-6 | 2.3792e-5 | 8/8 |

At the largest-sigma point (chain 3, retained draw 870; sigma 2.9932533),
doubling Simpson resolution from 1,600 to 3,200 intervals changes the log
normaliser by zero at returned precision and the derivatives by at most
6.7e-12. The two divergent saved states themselves pass at 40 nodes. These
checks do not locate the cause along a divergent trajectory or establish
consequential posterior bias.

**Use fixed 64-node quadrature for the next candidate.** It also passes the
central, signed kappa-b stress, small-sigma and rho=0.999/sigma=3 checks on
the cost dataset. Actual Stan gradients pass at the central, negative
kappa-b stress and maximum-sigma saved points; tighter solver settings give
unchanged log densities. This is finite-domain evidence, not a global bound.
Retain the old gates and add these eight states plus 40 evenly spaced v4
states to the packaged checks. Preserve v4 as the 40-node cost result.

## Correct the boundary coverage requirement

Section 8.4(d) of the [finite contract](../literature/2026-10-16-q012-finite-contract.md)
requires nominal equal-tail coverage under scenarios with true eta=0.
Under the fitted continuous priors, sigma>0 and 0<rho<1 almost surely, so
eta=rho*sigma>0. For a proper posterior its 5% quantile is strictly positive.
The 90% equal-tail interval therefore has **zero coverage at exact zero by
construction**, even with a perfect sampler.

Amend the 0.85–0.95 coverage acceptance requirement to interior generating
eta>0 where working and generating eta coincide. Retain and label raw
boundary coverage as structurally zero; evaluate eta=0 through the existing
false-support and informative-negative endpoints. Eta=0.05 remains an
interior value. This correction changes neither the priors nor the D/X
definitions. Do not add a point-mass prior merely to satisfy the old rule.

## Proposed package and execution order

This is a numerical/cost pilot, not a power or coverage experiment. It does
not settle the final campaign ensemble or promote a primary investigation.

1. **Freeze and check the package locally, without another long fit.**
   Use the 64-node candidate, existing Powell guards and unchanged model and
   priors. Version the config, source, data, starts, exact CmdStan/runtime
   versions and checks together with hashes. The runner must reject stale
   checks rather than trusting an unbound `all_prefit_checks_pass` boolean.
   Preserve per-chain stdout/stderr, per-probe results and raw draws. Include
   a bounded generator timeout as well as the 3,000-lineage cap. Test cap,
   timeout, chain failure and resume/skip controls with cheap fixtures.
2. **Prepare the first kunanyi job as a technical replay** of the frozen
   264-lineage cost dataset. Four chains; 2,000 warmup plus 4,000 retained
   draws per chain; adapt_delta 0.995; depth limit 12; initial step size
   0.01; original sampler seed 77017 and declared prior-centred starts.
   This is a proposed conservative setting, not an assertion that it solves
   the geometry. Keep the selected cost dataset outside the next panel.
3. **Only if that replay passes the numerical checks**, run 12 unconditional
   datasets: lambda0 in {0.0708, 0.096} crossed with eta in {0, 0.05, 0.20},
   sigma=0.5 (rho in {0, 0.1, 0.4}), two frozen seeds per cell. Keep the
   primary observation settings and other reference parameters fixed.
   Freeze the full seed table before generation; never choose seeds by
   resulting lineage count. The original-rate panel remains the reference;
   0.096 remains a size-calibrated sensitivity with unmatched censoring.
   Do not move the estimator's priors or starts to each generating value.
4. **Bound each fit at two hours and four single-threaded chains.** The 13
   fits have a maximum allocation of 104 core-hours, excluding separately
   declared build/preflight overhead. This is a ceiling, not measured
   cluster cost. Prepare an initial request of four CPUs and 8 GiB per fit;
   record peak memory and revise the panel request if the first job requires
   it. Build and evaluate on a compute allocation, not the login node.
5. **Use PBS completion/abort mail and Barry's wakeups.** No polling service.
   First return the technical replay's receipts and diagnostics; do not
   automatically release the 12-fit panel merely because PBS exits zero.
   Claude prepares scripts, manifests and the pilot scenario table; Codex
   checks the concrete package. No jumpbox probe is needed during preparation.

Screen the technical replay and every later fit for four completed chains,
zero post-warmup divergences, no fatal or sampling-phase numerical failures,
E-BFMI at least 0.3 per chain, R-hat below 1.01 for monitored parameters,
lp__ and free latent variables, and bulk/tail ESS at least 400 for core
parameters. Report depth-limit hits and rejections by phase and cause.
These are screening thresholds, not proofs of unbiased inference. Failure
stops promotion; do not automatically lengthen runs or replace datasets.

Retain full precision for eta's 5%/95% endpoints. Compute their Monte Carlo
standard errors with a chain-preserving method such as
[`posterior::mcse_quantile`](https://mc-stan.org/posterior/reference/mcse_quantile.html).
Use endpoint MCSE <=0.01 as the initial pilot precision target. Mark a
decision numerically uncertain when endpoint +/-2 MCSE crosses 0.05 or
0.20; retain the raw D/X flags separately. This numerical ambiguity is not
the scientific D=no/X=no outcome. Current exploratory block-bootstrap
errors are about 0.003 and 0.015–0.017, far from changing the current flags;
they do not address sampling bias.

Keep every attempted dataset, cap event, timeout and failed fit in the
denominator. With s resolved event successes and u unresolved outcomes
among n attempts, report all-attempt bounds [s/n, (s+u)/n] alongside any
success-conditioned summary. The pilot cannot establish campaign power,
coverage or robustness to the observation process.

Independent sampling/contract check: GPT-6.1 Sol. Codex replay evidence is in
ignored `scratch/q012-v4-check-20261016/`: `replay.py`/`replay-results.json`,
`tail_precision.py`/`tail-precision.json`, `q64_candidate.py`/`q64-candidate.json`
and `agent/`. Source/config and input-CSV hashes are in `replay-results.json`.
The next package should retain these numerical fixtures durably. The local
Nectar control-plane guidance was read; no remote state was inspected.
