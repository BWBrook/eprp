# Life-history contract: finite-horizon demographic controls

These are illustrative calculations for the
[Codex contract](../../ideas/2026-10-25-contract-life-history-codex.md), not
fitted biological models or new demographic theory. The
[primary-source check](prior-check.md) records the close existing literature.

Run `python data/life-history-contract/compare.py` from the repository root.
It writes [comparison.json](comparison.json), using only the Python standard
library. The 144 comparisons and four order controls take less than a second.
There is no Monte Carlo approximation or random seed.

## Model and exact outcome

At each census an individual is juvenile J or adult A. A juvenile remains
juvenile with probability p, matures with probability g, or dies. An adult
survives with probability s and independently produces Poisson(f) newborn
juveniles. Reproduction can occur in the interval in which that adult dies;
this timing convention is part of the model. Offspring and individuals are
independent. There is no density dependence, environmental stochasticity,
immigration, dormancy, sex limitation or adaptation.

The mean projection matrix is `[[p, f], [g, s]]`. The individual offspring
probability-generating functions are

```
F_J(z_J,z_A) = 1-p-g + p*z_J + g*z_A
F_A(z_J,z_A) = (1-s+s*z_A) * exp(f*(z_J-1)).
```

Starting from `(z_J,z_A)=(0,0)` at the final census, compose these functions
backward through the prescribed schedule. With initial counts `(J0,A0)`, the
probability of extinction by that census is `z_J**J0 * z_A**A0`. Zero is
absorbing, so this is also the probability of having become extinct at any
earlier census. Expected abundance is calculated separately by matrix products.

Two invented strategies share juvenile survival 0.8 and baseline dominant
eigenvalue 1. Set `p=0.8*(1-gamma)`, `g=0.8*gamma`, and
`f=(1-s)*(1-p)/g`. Generation time, the mean parental age of offspring in
this stationary model, is `1/(1-p)+1/(1-s)`.

| Strategy | Maturation gamma | Adult survival s | Fecundity f | Generation time |
| --- | ---: | ---: | ---: | ---: |
| Fast | 0.8 | 0.5 | 0.65625 | 3.19048 |
| Slow | 0.2 | 0.95 | 0.11250 | 22.77778 |

Both processes are critical: eventual extinction is certain. Their
**finite-horizon persistence** is the target. Baseline equality of mean growth
does not equalise demographic variance or finite-horizon extinction risk.
The strategies bundle several traits; these are not isolated interventions
on generation time.

## Comparisons and controls

Each population begins with 40 individuals, either rounded stable stage
proportions (fast 18 J / 22 A; slow 10 J / 30 A) or the common allocation
20 J / 20 A. The disturbance multiplies either fecundity (successful
recruitment into the juvenile class) or adult survival. Duration is 1, 4 or
16 steps; the post-disturbance observation window is 0, 8 or 32 steps.

Two exposure conventions are retained: a fixed multiplier 0.2, and a fixed
sum of negative log multipliers, giving `0.2**(1/duration)` at each step.
The latter fixes a rate-scale budget; it does **not** match lost births,
deaths, reproductive value or biological severity across strategies/routes.
For example, the fixed adult-survival multiplier changes death probability
from 0.05 to 0.81 for the slow strategy and from 0.5 to 0.9 for the fast one.

Every disturbed result has an undisturbed control with the same strategy,
initial counts and total horizon. Output includes persistence, excess
extinction probability, expected abundance relative to that control, and
minimum expected abundance. Minimum expected abundance is not a
quasi-extinction probability.

Selected fixed-intensity, rounded-stable results with eight subsequent steps:

| Disturbance | Duration | Fast persistence | Slow persistence | Fast / slow mean abundance relative to respective controls |
| --- | ---: | ---: | ---: | --- |
| Recruitment suppression | 4 | 0.918038 | >0.999999 | 0.2224 / 0.8609 |
| Adult-survival reduction | 4 | 0.980850 | 0.877395 | 0.3621 / 0.0751 |
| Recruitment suppression | 16 | 0.017925 | >0.999999 | 0.0017 / 0.5365 |
| Adult-survival reduction | 16 | 0.160405 | 0.018466 | 0.0179 / 0.0007 |

These establish conditional counterexamples to a universal duration rule,
not predictions for named extinction events. At duration one, adult-survival
loss leaves the fast strategy with more expected individuals but slightly
lower persistence than the slow strategy. Abundance is not extinction risk.

The order control swaps one recruitment and one adult-survival interval.
Ordinary stage structure produces non-commuting projections and different
outcomes; no acquired biological memory was added.

## Verification

The script checks one-step extinction probabilities, the empty population,
zero mortality, an independent no-birth survival identity, baseline unit
eigenvalues and stationary expected abundance. A separate Codex reviewer
replayed all outputs and checked the backward PGF and generation-time
derivations. These checks establish the calculations under the stated model;
they do not qualify novelty, historical forcing or fossil proxies.

## Cross-review closure follow-up

Claude replayed the model and agreed to retire the standalone novelty claim.
The [updated source check](prior-check.md) records the full Valentine–Jablonski
paper and Murray's verified 2026 citation dates; [source-followup.json](source-followup.json)
preserves source access and hash details.

Run `python data/life-history-contract/closure-check.py` to regenerate
[closure-checks.json](closure-checks.json). It uses standard-library pooled
and Fisher tests on integer counts implied by the source's rounded size
summary, and extracts four archived model cells that contradict a universal
fixed-sign-by-route interpretation. The original unpublished source data/test
remain unavailable; the printed significance is unreproduced, not silently
replaced. Changing disturbance duration in these selected cells changes dose
and horizon too. This follow-up does not refit or modify `comparison.json`.
