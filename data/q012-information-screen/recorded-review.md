# Independent recorded-detector review

28 October 2026, 15:02 AEDT. Codex subagent, independent bounded static
scientific/code audit for main Codex. No generator runs, evaluation-result
inspection, implementation/protocol edits or Board writes in this review.
Reviewed `recorded.py`, `recorded-protocol.json`, `test_recorded.py` and the
previously reviewed prospective `recorded-design.md`.

**Finding: no blocking defect for the frozen detector-only experiment.**
Main Codex retains responsibility for tests, staged execution, checking the
actual frozen coefficient SHA256, and interpreting the saved results.

## Recorded-input boundary and statistic

The feature path reads recorded IDs solely as lookup keys, recorded parent
links, rounded origin/end ages and recorded end labels. It does not read
latent frailties, true parent IDs, true end causes, hidden exposure, cap
status, cohort identity, rejection counts or seeds. Metadata retained by
`replicate` do not feed the feature or score functions. Parent and sister
products use the pruned/reassigned recorded links. The feature calculation
matches the eight prospectively specified features; the last feature is
mean(q^2), rather than mean(q)^2.

`cumulative_hazard` intersects [end,origin] in Ma with baseline bins [0,3],
[3,6], ..., [72,75]. This is the correct direction for the original forward
time convention and h0 array. It includes pre-cut survival time using
recorded ages without requiring a hidden cohort flag. The isolated-lineage
proxy uses x=sigma*sqrt(2)*Hermite_node, the correct normal prior quadrature,
and log weights delta*x-A*exp(x-sigma^2/2). Constants omitted from the
extinction factor do not affect the normalized proxy. It remains an
approximate risk statistic under selection, thinning and label changes;
the prose does not misstate it as exact frailty recovery or a joint score.

Development standardization and pooled within-class covariance use only the
two development panels. Fixed shrinkage 0.9*C+0.1*I is positive definite,
and the class-mean difference orients the linear score toward the alternative.
There is no tuning or calibration/evaluation contribution to fitted weights.

## Freeze, calibration and decision

Development writes coefficients together with development-row SHA256 and
hashes of the implementation, both protocols/designs, oracle implementation
and original generator/configuration/quadrature source. Evaluation requires
an explicit expected coefficient SHA256 and rejects a mismatch; it also
compares the frozen source dictionary with current hashes before generating
any calibration/evaluation histories. The threshold uses only the two
endpoint-null calibration panels and is written before evaluation histories
are generated. These code paths enforce the intended staged freeze when
called with the retained development receipt.

For each null, rank Binomial.ppf(.9975,2000,.95)+1 is a valid upper confidence
threshold for its population .95 quantile. Rejection is strictly score>
threshold, and taking the maximum threshold cannot increase either null's
rejection probability. This remains conservative with discrete score atoms
caused by rounded recorded inputs: F(q-)<=.95 makes the probability that
the upper order statistic falls strictly below q no larger than the stated
Binomial tail. Continuous recorded scores are not required here.

Alternative evaluation is independent of development/calibration. The
Clopper-Pearson endpoints use the declared .01 tails, including the boundary
counts. The current lower and upper failure allocations are both .01, so
using one tail argument to obtain both endpoints matches this frozen
protocol. Four endpoint-null quantile failure allocations of .0025 and four
power-tail allocations of .01 total .05 across both ensembles. Null-evaluation
95% intervals remain descriptive and are not promoted to simultaneous bounds.

The coded detector-only pass rule matches the design: alternative estimate
>=.8, power lower bound >=.75, and each endpoint-null estimate <=.05 with
descriptive upper bound <=.07. Stronger lower-bound>.8 evidence is reported
separately. Checking eta=0 and .05 does not establish a composite-null
guarantee throughout the interval. Neither success nor failure establishes
real-record power, biological inheritance, posterior/coverage/negative-result
contract fulfillment or sampler readiness. No feature redesign is proposed
from the oracle results.

## Reviewed SHA256 identities

- recorded.py: 9082437a13d1e8611c6c7e0f8001eda6b0ee780e1cf315ee84d448d3a6e1f0da
- recorded-protocol.json: 3c02129372dd7b956a8519590c1bc3892f1a61761088adf91c764a7611ebbbfe
- recorded-design.md: 594fbd79da2749732a7547505009d5d43c231394e447a7a6885bd93baa9dc308
- test_recorded.py: c12aba5dddfdc4c210893f6a75c9b7cffa446fc138ce554634c9b6fd7a278228

The tests were inspected but not executed by this reviewer. This is static
clearance for the reviewed identities, not a runtime pass or result audit.
