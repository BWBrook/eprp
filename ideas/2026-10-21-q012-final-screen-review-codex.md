# Q-012: final P11 screen and the estimator handoff

21 October 2026. Independent Codex review of baseline
`bd84335825142c63a5ac0beb1bdb0c60af6509ad`. Scope: the returned
`v6q80t` result and Claude's proposed simpler-estimator comparison. No new
fit, compilation, remote work, prior change or sampler trial was run.

**Recommendation:** accept the failed screen and end the sampler tuning
ladder. P06 and the other ten remain held. Allocate only a bounded local
factorisation/oracle feasibility check before choosing another estimator.
The result establishes a computational failure of this implementation under
the frozen screen; it does not establish statistical nonidentifiability or
failure of calibrated recovery under another implementation.

## Verified result

The [returned diagnostics](../data/q012-pilot/results/P11-v6q80t-20261021/diagnostics.json)
were recomputed with the existing `diagnose(..., write=False)` implementation.
Every field other than the local attempt path agrees exactly. Qualification
and capture pass, as do the non-divergence sampling and precision gates;
the zero-divergence gate fails. The twelve raw chain/log/trace hashes agree
with the [committed manifest](../data/q012-pilot/results/P11-v6q80t-20261021/chain_files.sha256).
The [build receipt](../data/q012-pilot/results/P11-v6q80t-20261021/build_receipt.txt)
records successful mandatory preflight against the reused binary and patch.
The [PBS accounting](../data/q012-pilot/results/P11-v6q80t-20261021/accounting.txt)
has both jobs F/0. These are different claims: job completion does not turn
this failed statistical screen into a pass.

| Quantity | Independent check |
| --- | --- |
| Retained draws | 4 × 6,000 |
| Sampling divergences | Chain 1 transition 2779; chain 4 transition 2843 |
| E-BFMI | 0.845876–0.883542 using the existing sample-variance convention |
| Maximum R-hat | 1.00107494, `w.12` |
| Minimum core bulk ESS | 4,772.363, sigma |
| Eta 90% interval | 0.00473126–0.59008106; truth 0.2 covered |
| Eta endpoint MCSE | 0.00023993 and 0.00771170; target met |
| Allocated core-hours, this sequence | 4 × (58 + 10,615)/3,600 = 11.858889 |
| Tranche total / remaining | 32.576667 / 20.756667 of 53.333333 |

The screen's D and X decisions are false. They remain descriptive outputs of
a failed attempt. The matching divergence *counts* across attempts of
different lengths do not estimate a remedy effect, although the frozen
zero-divergence criterion unambiguously failed again.

## Findings, ranked

### MAJOR: computational geometry is not an identification result

The captured failures and replay show a step-size/curvature problem for the
current target and coordinates. That is consistent with the
[Stan reference manual's description of divergences](https://mc-stan.org/docs/reference-manual/divergent-transitions.html)
(primary software documentation; relevant section inspected 21 October).
It does not distinguish a weak likelihood ridge from a strongly identified
but sharply curved region, hierarchical coordinate coupling, or a combination.
The evidence cannot support “inference is failing at the edge of frailty–ageing
identification itself” as an established statistical conclusion.

The largest **raw momentum changes** occur in sigma, log_k and sometimes
kappa. They locate the observed kick; they neither give a curvature
eigendecomposition in the adapted metric nor exclude coupling to the
lineage frailties. In these coordinates, every x depends on sigma and w,
and log z additionally contains −sigma²/2
([model](../data/q012-pilot/payload_v6q80t/model_v6.stan), lines 183–202).
Integrating out x could change that geometry even when global-coordinate
kicks are largest. It could also leave difficult marginal geometry.
Neither outcome has been tested.

The retained-draw tail calculation reproduces 88/24,000 draws with sigma > 2
(0.3667%), correlations 0.64493 for sigma/eta and 0.45442 for sigma/log_k,
and eta median/q95 0.65647/1.80504 within that tail. Overall eta median/q95
are 0.11164/0.59008. These show association in the available draws. A sample
that fails exploration diagnostics cannot certify the mass of its own
poorly explored region or the sign/size of upper-quantile bias. They justify
retaining the gate; they do not quantify lost posterior mass or prove that
eta's 95th percentile is wrong.

**Required qualification:** report failed computational screening; reserve
identification/recovery conclusions for a valid likelihood or posterior,
then calibration/support evidence. A same-target collapsed calculation is
an informative next comparison, not a promised cure.

### MAJOR: step-halving errors include inherited energy error

The [stored replay](../data/q012-pilot/results/P11-v6q80t-20261021/trace_check.json.gz)
and `pilot.py` lines 1411–1415 report each half-step's H minus the original
trajectory H0. They do not subtract H at the preceding leaf. Independent
replay reproduces full-step q and p exactly and H to relative error
1.61e-16 / 1.20e-16. Subtracting the inherited offsets gives:

| H difference | Chain 1 | Chain 4 |
| --- | --- | --- |
| Preceding leaf − H0 | +221.90499 | +85.62040 |
| Full failing leaf − preceding leaf | +2,453.62124 | +1,675.03429 |
| First half step − preceding leaf | +110.79764 | +18.68887 |
| Two half steps − preceding leaf | +129.47888 | −11.08681 |

Halving sharply reduces local error. Chain 1 still has a substantial local
error, but the 333/351 and 104/75 figures cannot be interpreted as entirely
new error from the halved offending step. This particularly changes the
interpretation of chain 4. It does not reopen tuning or change the screen.

### MAJOR: numerical exclusion must be scoped to tested states/axes

Claude's replay checks finite differences on sigma, rho, kappa_b and one w
coordinate, and the normaliser only at each finite failing state
(`pilot.py` lines 1419–1435). The two failing-state normaliser log errors
6.66e-11 / 5.03e-11 are supported by the archived qualified references;
they alone do not check the preceding leaves.

This review closes that particular gap with the existing repaired gate:

| Previous endpoint | Q80 log error | Maximum derivative error, sigma/rho/kappa_b/log_k |
| --- | --- | --- |
| Chain 1 | 2.74146e-7 | 1.87082e-6 |
| Chain 4 | 2.14763e-5 | 9.44878e-5 |

Both pass the unchanged gates, with qualified primary and fixed-innovation
references. Actual-Stan AD/FD was also checked on **all 54 unconstrained
coordinates at both previous and failing states**. Maximum scaled errors
are 2.23e-8 / 2.24e-7 for chain 1 and 2.45e-8 / 6.88e-8 for chain 4.
For log_k/kappa specifically all four states are within 4.2e-9. The larger
maxima occur among random-walk derivatives with small magnitudes.

This substantially strengthens a local integrator attribution. No checked
value/gradient discrepancy is remotely commensurate with the observed
energy blow-ups. “No material normaliser error at the checked endpoints and
axes” is defensible. A blanket exclusion over unsaved trajectories, all
parameter axes or a future collapsed numerator is not established. No
additional numerical chase is needed to apply the agreed stopping rule.

### MAJOR: a new estimator needs an explicit target before comparison

The current working likelihood already integrates x formally
([finite contract](../literature/2026-10-16-q012-finite-contract.md), §8.1).
A tree sum-product evaluator is an alternative numerical representation of
that likelihood; maximisation and Bayesian sampling are separate decisions.
The existing target has **54 free coordinates for P11: 19 frailty coordinates
and 35 others**. Integrating the 19 leaves 35. Integrating the 25 baseline
coordinates as well leaves 10, conditional on an explicit hyperparameter
and prior contract. Eta is derived, not another free coordinate.

Write theta for the other parameters and F_i(x_i; theta) for all local
post-entry event/exposure factors **times pre-entry survival for cohort
members**. The model implies independent root N(0,sigma²) densities and edge
kernels K(x_i|x_parent)=N(rho x_parent,sigma²(1−rho²)). Its conditional
likelihood is

L(theta) = [ integral p_theta(x_forest) product_i F_i(x_i;theta) dx ] / pi(theta).

A correct child-to-parent message is

M_i(x_parent) = integral K(x_i|x_parent) F_i(x_i) product_child M_child(x_i) dx_i.

Integrate each root against its root Gaussian, multiply root results, then
divide by pi(theta). Pi is the **existing retained-cohort selection
normaliser** (four singleton factors and one pair for this P11). Do not drop
it, put it inside a frailty-dependent denominator, or substitute separately
normalised node factors. Descendant evidence belongs in the numerator's
messages; it does not redefine this design-selection probability.

On reusable one-dimensional node grids, dense edge contractions have nominal
O(N G²) cost. This is a derivation for the frozen working graph, not a proof
that any particular G is accurate. Near rho=1 the kernel narrows, and
large sigma, tilted event factors and several daughters can move/concentrate
numerator mass. Q80 accuracy for the tiny selection integral does not certify
full-tree numerator accuracy. A parameter-dependent quadrature/interpolation
scheme must differentiate its complete approximation, including moving nodes
and scales, and verify value and gradient convergence.

The conditional x log-integrand here is concave: the Gaussian forest term
is quadratic; each local log factor is linear in x minus positive multiples
of exponentials of linear x. This supports a conditional-mode numerical
oracle for small trees. It says nothing equivalent about concavity or
identification in theta after integration.

For an MML proposal, state exactly which terms are integrated and which are
optimised. The 25 log-baseline variables have a Gaussian **prior/law**
conditional on tau; their observed-data integrand is not Gaussian because
hazards are exponentiated. Integrating them is another 25-dimensional task;
a Laplace approximation would need its own error checks. Optimising them
with a random-walk penalty is penalised frailty-marginal likelihood, and
retaining all global priors for optimisation gives a posterior-mode target.
Neither can silently inherit same-prior Bayesian interval interpretation.
A bootstrap must replicate the frozen generator, observation/selection rules,
nuisance fitting and any smoothing selection. Boundary conventions matter:
at sigma=0 rho drops out and eta=0 is not a regular interior case. P11 also
has zero bifurcation terminal events, so an unconstrained ML interior optimum
for b0/kappa_b cannot simply be presumed.

## Small next task that would earn further work

**Proposed next scope for Claude: a local feasibility note and a tiny-tree
oracle, followed by Codex's review; no new fit or cluster allocation.** Use one shared collapsed
likelihood before ranking MML versus same-prior collapsed Bayes.

1. Freeze the formula above, the treatment of baseline/tau/global priors,
   integration coordinates and Jacobians, and what “simpler estimator” means.
   Retain the original eta target, cohort conditioning and all data rules.
2. Implement only evaluation on three toy forests: one root, one pair and
   one root with two daughters. Verify unit local factors integrate to one;
   with only selection-survival factors, numerator/pi equals one; then check
   event-weighted messages against independent low-dimensional integration.
3. Use a finite, declared point set spanning central and high-sigma states,
   low/high rho, and the two captured global-state pairs. Check domain and
   grid-resolution convergence separately, values and all active derivatives,
   with declared tolerances before evaluation. Include the narrowed-kernel
   high-rho case. Report runtime/memory, failures and unresolved references.
4. Stop after that one bounded evaluator/oracle report. A successful check
   earns consideration of a fixed-point P11 evaluator/cost check. It does not
   release optimisation, HMC, parameter bootstraps or campaign fitting.

No profile or bootstrap can presently decide identification because its
validated evaluation and nuisance-target contract do not yet exist. Reducing
kappa or other scientific structure may change the question; it is not a
numerical substitute for this comparison. A failure of the tiny oracle should
end that implementation route or produce a specific explained repair, not a
new hidden sampling ladder.

## Reproduction and evidence limits

Local scripts and detailed receipts are in
`scratch/q012-final-review-20261021/`: `review_checks.py`, `checks.json`,
`requalify.py` and `diagnostics_recomputed.json`, preserved in the
[parent review archive](../data/review-followup-20261021-codex.tar.gz). Reproduction uses
`uv run --python 3.12 --script` on the two scripts, the existing local
instrumented binary and the hash-verified returned files. No binary was
rebuilt. Existing archived joint-state results (49/49 pass, maximum value
3.93897e-6 and derivative 2.26725e-5) were inspected, not recomputed in full.
The two newly checked preceding-state gates are separate post-hoc review
evidence and do not amend the frozen screen. The referenced memory was used
only to orient to the earlier conditional P11 ruling; conclusions above were
checked against current files.

**Next responder: Claude**, after the parent Codex communicates the bounded
allocation and integrates this review. No Barry-only decision is needed for
the local evaluator feasibility check; estimator choice and any changed
scientific target remain explicit subsequent decisions.
