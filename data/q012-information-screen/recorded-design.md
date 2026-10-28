# Prospective recorded-data detector

Prepared 28 October 2026 without viewing full oracle evaluation results. After
both oracle ensembles cleared their power lower-bound criterion, main Codex
reviewed and accepted this design. It is now implemented unchanged in
[recorded.py](recorded.py) and frozen in
[recorded-protocol.json](recorded-protocol.json), before production development,
calibration or evaluation. Six independent controls and a separate 20-history
timing panel pass; those timing histories have no inferential role. Freeze the
development coefficients separately before calibration and evaluation.

## Scientific statistic

Use a fixed, small vector built only from the original observation map's
recorded origins, ends, end labels and recorded parent links. The central
signal is agreement in mortality-risk proxies between recorded relatives.
Known nuisance settings may be used because this remains a fixed-nuisance
information screen. No true parents, true end causes, latent frailties,
exposure values hidden by the map, rejection counts, innovations, or cap
indicator enter the detector. Cap status remains descriptive metadata.

For each recorded lineage compute cumulative baseline extinction hazard A
from its rounded origin to rounded end using the fixed 3-Myr h0 bins. Include
the pre-cut survival time for cohort lineages. Let delta be 1 for recorded
label `ext` and 0 for the other labels, and set

    q_i = E[x_i / sigma | delta_i, A_i]
        = integral (x/sigma) exp(delta*x - A*exp(x-sigma^2/2)) phi_sigma(x) dx
          / integral exp(delta*x - A*exp(x-sigma^2/2)) phi_sigma(x) dx.

Use fixed 40-node Gauss-Hermite quadrature and log-sum-exp stabilization,
checking 80-node agreement on predeclared synthetic durations and labels.
This is an isolated-lineage risk proxy, not a recovered latent frailty or
the exact joint posterior. Misclassified terminal events, thinning,
reassignment, selection and inherited birth structure can bias it; simulation
calibration evaluates the resulting detector without declaring the proxy
unbiased. Including pre-cut hazard acknowledges cohort survival selection.

The product q_parent*q_daughter is motivated by the derivative of a bivariate
Gaussian inheritance density at rho=0: its conditional expectation under
independent node likelihoods is the product of standardized posterior means.
Sibling products target the weaker shared-parent signal. This motivation
does not promote the proposed statistic to an exact observed-data score.

Prespecify these eight features, with no feature selection:

1. Sum of recorded parent-daughter q products divided by sqrt(1 + edge count).
2. Sum of parent-daughter products after centering q by the tree's mean,
   divided by sqrt(1 + edge count).
3. Sum of q products over unordered recorded sisters (same recorded parent),
   divided by sqrt(1 + sister-pair count).
4. log(1 + recorded lineage count).
5. Recorded present-day censor fraction.
6. Recorded extinction-label fraction.
7. Tree mean q.
8. Tree mean q squared (second moment, not square of the mean).

Empty pair sets contribute zero. A zero-lineage history has zeros except
log(1+N), also zero. Sister products use the algebraic pair-sum identity,
avoiding quadratic expansion. Features 4-8 allow the detector to use any
recorded distributional differences in this declared generator, including
informative random tree size; their coefficients are not causal effects.

Fit one regularized linear discriminant separately for each ensemble using
1000 new null and 1000 new alternative development histories. Standardize
features using the pooled development mean and SD, setting constant-feature
SD to 1. Use pooled within-class covariance C and fixed covariance
0.9*C + 0.1*I; coefficients are its inverse times the standardized class-mean
difference. No tuning, model comparison, nonlinear classifier or revision
after evaluation. Save all development features and fitted coefficients.

## Independent calibration and evaluation

Use entirely new seed families, bases 283000000 and 284000000 for the two
ensembles. Proposed offsets and panels, each contiguous from its start:

| Offset | Panel | n |
| --- | --- | --- |
| 10000 | Development eta=0.05 | 1000 |
| 20000 | Development eta=0.20 | 1000 |
| 30000 | Calibration eta=0.05 | 2000 |
| 40000 | Calibration eta=0 | 2000 |
| 50000 | Evaluation eta=0.05 | 2000 |
| 60000 | Evaluation eta=0 | 2000 |
| 70000 | Evaluation eta=0.20 | 2000 |

With the development coefficients fixed, calibrate a threshold on each null
calibration panel. Use an upper confidence endpoint for each population
0.95 quantile with failure probability 0.0025 per null. Take the maximum of
these thresholds, giving size at most 0.05 for both declared endpoint nulls
except with probability at most 0.005 per ensemble. Report independent null
evaluation proportions and exact 95% descriptive binomial intervals. Bound
alternative power by independent one-sided exact binomial intervals, spending
0.01 on each lower and upper endpoint per ensemble. The union bound gives
at least 95% simultaneous coverage for both endpoint-null calibration
statements and both ensembles' alternative-power intervals. Preserve all
history outcomes and cap/censor summaries.

This is 24,000 histories across both ensembles, about six minutes by the
oracle's small WSL timing; route it to deep-server as a small single-process
job. A separate small timing/control panel, seeds starting 280910000, has no
inferential role. Freeze the final machine-readable design and coefficient
file before calibration/evaluation.

## Decision boundary

A passing detector needs observed positive power at least 0.8 and the
contract's Monte Carlo lower bound at least 0.75, plus endpoint-null false
support at most 0.05 with upper bound at most 0.07. Also report whether its
power lower bound exceeds 0.8, the stronger evidence criterion. Null
calibration and evaluation must both be reported; a discrepancy is a result,
not a reason to change the threshold. No interpolation to all eta <= 0.05
is established by checking only eta=0 and 0.05. A detector failure says only
that this fixed cheap statistic did not pass. It never excludes an optimal
observed-data test. Success shows information survives this simulator's
observation map and supports planning a cheap recovery method; it supplies no
interval coverage, informative-negative, prediction, unknown-nuisance,
real-record power or biological-inheritance claim, and no automatic sampler
restart.
