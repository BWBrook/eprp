# Boundary counts under incomplete observation

Owner: Codex. Built and checked 10 October 2026. Synthetic feasibility check
for Q-026; no empirical rates, fossil data or fitted diversification model.
See the [scientific interpretation](../../literature/2026-10-10-boundary-counts-and-incumbency.md).

## Question and construction

True instantaneous richness avoids counting successive names twice within a
bin. Does the same invariance hold for an **observed** boundary count constructed
from first and last fossil occurrences? Can that count be used at its own
boundary in a prediction restricted to information available by then?

Twenty lineages persist throughout twelve unit-length bins. Each has an
independent Poisson fossil process of rate `psi` and a Poisson process of
one-for-one name replacement of rate `a`. A replacement changes the recorded
name, but never branches or removes a biological lineage. Names never recur.
Rates are per lineage per arbitrary time unit, not estimates per million years.

For each internal boundary, the script counts names with an observed first
appearance before it and last appearance after it, anywhere in the twelve-bin
record. This is distinct from an **adjacent two-timer**, which must have fossils
in both immediately adjoining bins. Both are recorded. Sampled-in-bin richness
is the number of distinct names with a fossil in that bin.

## Exact expectation and checks

For a name present at a boundary, the probability of observing it on one side
within available time `s`, before a replacement or the record endpoint, is

`q(s) = psi / (psi + a) * [1 - exp(-(psi + a) * s)]`.

Independence of the two sides gives expected observed count
`20 * q(t) * q(12 - t)` at boundary `t`. An adjacent two-timer has expectation
`20 * q(1)^2`. These are expectations of uncorrected observations, not proposed
estimators of true richness. As fossil sampling becomes complete, both tend
to 20 for finite replacement rate. Finite observation windows also affect
counts even when `a = 0`.

The script checks both expectations against 1,000 independent simulated
records for each of six rate combinations. Standard errors use replicate
means, not correlated boundaries as independent observations. All deviations
were within six Monte Carlo standard errors. It also checks the complete
sampling limit and that two-timer counts never exceed boundary counts.
An independent GPT-6.1 Sol review checked the derivation and reran all six
configurations without writing outputs; the reported numerical metrics
reproduced to displayed precision, with no material correction requested.

A deterministic fixture holds the complete past through `t = 1` fixed:
name A at 0.2 and 0.8. A later fossil at 1.2 of A yields observed boundary
count 1; a later fossil of B yields 0. Thus this retrospective count is not
a function of the prefix alone. Without the later fossil, right-hand support
is unknown: a computed zero is not evidence of biological extinction.

## Results and limits

With `psi = 2`, increasing replacement from 0 to 2 reduces the exact mean
observed boundary count from 19.431 to 4.983 despite true richness remaining
20. The simulations give 19.419 and 5.013. Observed squared adjacent increments
are positive under every configuration, while true count increments are zero.
Those squared increments include edge effects and sampling covariance; they
are not an estimate of branching-plus-extinction rates.

This demonstrates an observation requirement, not a failure of an implemented
correction. Three-timer, capture–recapture and joint sampling/lineage models
were **not fitted or evaluated**. The construction says nothing about the
empirical frequency of one-for-one replacement, taxonomic rank conversions,
or identifiability under a fully specified observation model. It uses exact
ages, uniform fossil sampling, independent lineages and no true birth/death.

## Reproduction and output dictionary

Run from the repository root with Python 3.12 and its standard library:

```bash
python3 data/q026-boundary-observation/probe.py
```

The script regenerates [summary.tsv](summary.tsv); random seeds and replicate
counts are included in every row. No download or external dependency is needed.

| Column | Meaning |
| --- | --- |
| `fossil_rate`, `replacement_rate` | `psi` and `a`, per lineage per time unit |
| `true_standing_count` | Constant number of biological lineages |
| `boundary_mean_exact`, `boundary_mean_simulated` | Analytical/simulated mean of the eleven internal observed boundary counts |
| `boundary_mean_mc_se` | Monte Carlo standard error of the preceding simulated mean |
| `adjacent_two_timer_mean_exact`, `adjacent_two_timer_mean_simulated` | Corresponding means for presence in both adjacent bins |
| `sampled_in_bin_mean` | Mean number of observed distinct names per bin |
| `boundary_increment_mean_square` | Mean squared increment between adjacent observed boundary counts |
| `true_count_increment_mean_square` | Zero by construction |
| `replicates`, `seed` | Independent records simulated and pseudorandom seed |

All table values are generated by this script. No third-party source data are
redistributed; external literature supplies the interpretation and comparison
definitions in the linked note.
