# Frozen complete-data information screen

Frozen 28 October 2026, before evaluating either hypothesis. Machine-readable
settings and seed ranges are in [protocol.json](protocol.json). Main Codex
reviewed the ensemble and likelihood-ratio construction before evaluation.

The estimand is eta = rho sigma. The simple hypotheses are eta = 0.05 and
0.20 with sigma = 0.5, hence rho = 0.1 and 0.4. These are deliberately easy
fixed-nuisance comparisons. They do not test identifiability with unknown
nuisances. All other generator parameters and root origin times remain those
of the primary [generator](../q012-prototype/prototype.py) and
[configuration](../q012-prototype/config.json).

## Ensembles and observation

Use two declared repeated-history ensembles: the original marginal-rate
reference (lambda0 = 0.0708) and the previous size-calibrated generator
(lambda0 = 0.096). Neither selects histories with 268 recorded lineages.
The latter historically had approximately 45% recorded present-day censors,
against approximately 19% in the compiled record. Matching median size does
not match the historical design. No statement here estimates real-data power.

Each replicate follows the original generator, including rejection until the
five early roots and forced daughter survive to the K-Pg cut, all later
births and terminations, administrative censoring at 0 Ma and the 3000-lineage
cap. Every outcome is retained. The cap stops expansion before adding a batch
of daughters that would exceed it; existing lineages already have histories
through termination or the horizon, but some have not yet had offspring
generated. Thus a capped output is a stopped computational history, not a
complete uncapped biological tree. Both the oracle and any later recorded
test refer to this computational experiment. Capped outputs must not silently
be discarded or treated as uncapped trees. Report cap frequency and retain
its indicator. The original observation map is applied to the generated output
only for descriptive size, event, censoring and link summaries. It does not
enter the oracle score. Observation seeds are deterministic distinct offsets
from each replicate seed; panels and ensembles have disjoint generator seeds.

Oracle data X contain accepted latent frailties, every generated parent edge,
origin/end/cause, E histories, true budding counts, and the cap/stopping
information. They exclude rejected cohort proposals, rejection-attempt counts
and Gaussian/RNG innovations. Those implementation artifacts are not a
recorded-data information bound for this accepted-history experiment.

## Likelihood-ratio ordering

For every generated daughter, including the forced pre-boundary daughter,

    x_d | x_p ~ Normal(rho x_p, sigma^2 (1-rho^2)).

Let K_rho be the product of those densities and Z_rho be the probability that
the initial forced cohort survives to the cut under its unselected prior.
The accepted joint density factors as

    f_rho(X) = K_rho(X) A(X) / Z_rho,

where A includes the common independent Normal(0,sigma^2) root densities,
E laws, conditional event-process densities, cohort survival indicator,
censoring and deterministic cap/stopping factors. Budding and bifurcation
can depend on x, but their conditional laws are identical across the two
hypotheses because their nuisance parameters and sigma are fixed. The
selection probability is a constant for each hypothesis and does not depend
on the accepted history. Consequently

    log(f_1/f_0) = sum_edges log(phi_1/phi_0) + log(Z_0/Z_1).

The score is the edge sum, an exact likelihood-ratio *ordering*, not a
normalized numerical joint log ratio. The omitted constant is harmless for
calibration. Omitting a true edge, changing the innovation variance, or using
frailty innovations themselves as observed data would invalidate it. Random
tree size is retained; its likelihood contribution is already represented by
the stopped-history factors and edge product. There is no assumption that
edges are independent marginally or that realized cohort variance is sigma^2.

## Independent calibration, evaluation and uncertainty

Per ensemble use 2000 null calibration histories, 2000 independent null
evaluation histories and 2000 independent alternative evaluation histories.
Seed base plus panel offset through base + offset + 1999 defines each range.
No seed selection or repeat until a convenient size is permitted. Smoke seeds
are separate and have no inferential role.

The nominal threshold is calibration order statistic ceil(0.95(n+1)), with
rejection for score strictly greater. Its finite-sample unconditional null
size is at most 0.05 for continuous scores. Independent null evaluation
reports its realized size with a descriptive exact 95% binomial interval.

To bound optimal power at *population* size 0.05, bracket the population
0.95 quantile using exact Binomial(n,0.95) rank tails, allowing infinite
endpoints. At each bracket endpoint count independent alternative rejections.
One-sided Clopper-Pearson bounds give a lower bound at the upper threshold
and an upper bound at the lower threshold. Each ensemble spends 0.005 on
quantile-bracket failure and 0.01 on each power bound. The union bound over
both ensembles is 0.05. Thus both optimal-power intervals simultaneously cover
with at least 95% confidence, including calibration and power Monte Carlo
uncertainty. The continuous score law is ensured by the forced daughter edge
and continuous accepted frailties, up to probability-zero equalities.

Only an upper bound below 0.8 excludes target recorded-data power for its
declared ensemble, by the Neyman-Pearson lemma and data processing. A lower
bound above 0.8 permits developing a cheap recorded-data test on fresh seeds.
A straddling interval is inconclusive. Failure of an approximate test never
establishes impossibility. This screen does not evaluate the contract's full
composite-null, eta=0 informative-negative, interval-coverage or prediction
requirements, and it provides no sampler-restart or biological-inheritance
clearance.
