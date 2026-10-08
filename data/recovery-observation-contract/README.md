# Minimal checks of the recovery observation contract

Owner: Codex. Date: 9 October 2026. These are deterministic mathematical
counterexamples, not fitted biological models or estimates from fossil data.
They address the proposed instantaneous-environment versus finite-rate recovery
comparison in Correspondence 82/1177.

Run `python3 data/recovery-observation-contract/probe.py` from the repository
root. The standard-library script regenerates [summary.tsv](summary.tsv).
All quantities and parameter values are artificial.

## Richness does not determine a subsampling distribution

Two input pools each contain ten genera and 100 occurrences. One has ten
occurrences per genus; the other has 91 of one genus and one of each remaining
genus. Expected richness in ten draws without replacement is

`sum_i [1 - choose(N-n_i, m) / choose(N, m)]`.

The expectations are **6.6952** and **1.9000**, respectively. Thus richness and
total effort do not determine even ordinary rarefaction. This is not a numerical
implementation of shareholder quorum subsampling. It demonstrates that a scalar
richness model requires extra taxon-frequency information before an actual
subsampling estimator can be applied. Collection-based procedures require the
corresponding collection structure too.

## Environmental levels still require temporal coupling

Let richness start at 100 and evolve logistically over two unit intervals.
Within each interval K is constant, and `exp(-r*dt)=0.5`. At each time separately,
K is equally likely to be 80 or 120. Three joint distributions preserve those
same marginals: aligned low/low or high/high; opposed low/high or high/low;
or all four independent combinations.

| Coupling of K levels | Final richness mean | Final richness variance |
| --- | --- | --- |
| Aligned | 99.2481 | 226.1292 |
| Opposed | 97.2177 | 24.1079 |
| Independent | 98.2329 | 126.1493 |

The instantaneous model `S=K` has the same endpoint distribution in all three
cases. The dynamic model does not. This exact enumeration shows that marginal
uncertainty in levels is insufficient for a dynamic response distribution.
It neither estimates PhanDA dependence nor prefers any of these couplings.

## Loss-dependent recovery already follows from ordinary logistic dynamics

With constant K, positive r, and a one-off fractional loss d from equilibrium,

```
S(t) = K / [1 + d/(1-d) * exp(-r*t)]
D(t)/K = d*exp(-r*t) / [1-d+d*exp(-r*t)]
t_half = log((2-d)/(1-d)) / r
```

Here D is the deficit relative to the undisturbed equilibrium trajectory.
At r=1, loss fractions 0.1, 0.5 and 0.9 give deficit half-times **0.7472**, **1.0986**
and **2.3979**. The script checks the endpoint deficit against d/2.
Nonlinear scaling with loss therefore does not by itself establish additional
historical dependence. These monotone recovery results require constant K and
the specified initial condition; a changing environment does not inherit that
guarantee. Time units here are arbitrary, not geological Myr.

These checks identify missing parts of the proposed comparison. They do not
establish what fossil evidence can identify or whether a study would be novel.
