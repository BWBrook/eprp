# Tranche 1 validation: declared tests

Declared by Claude (Opus 5.5) on 23 October 2026, before any of these tests
was run. Results go in `results/`; this file is not edited after the runs
except to append dated amendments at the end, each saying what changed and
why. Rates are per lineage per Myr unless stated.

Environments: Docker images built by `env/build.sh` on `deep-server`
(`eprp-sw/bench-r:t1`: R 4.6.1 with CRAN packages from the Posit snapshot of
2026-10-22; `eprp-sw/bench-pyrate:t1`: PyRate commit `6a27efb`;
`eprp-sw/bench-revbayes:t1`: RevBayes v1.4.1 Linux release). Image ids,
package versions and seeds are written into each result file.

## Generators

**G1. Constant-rate birth–death moments.** λ = 0.3, μ = 0.2, one starting
lineage, t = 15 Myr, 20,000 unconditioned replicates per generator.
Truth: E[N(t)] = e^{(λ−μ)t} = 4.4817; P(survival) = (λ−μ)/(λ − μ e^{−(λ−μ)t})
= 0.39158. Generators: paleobuddy `bd.sim`, and TreeSim `sim.bd.age`
(the tree generator FossilSim's workflows use; `complete = TRUE`,
`mrca = FALSE`). Pass: mean extant count within 3 standard errors of the
truth, and the surviving proportion within 3 binomial standard errors.

**G2. Poisson fossil sampling.** On the G1 histories, ψ = 0.5. Truth: given
total lineage duration L, the fossil count K is Poisson(ψL). Generators:
paleobuddy `sample.clade` and FossilSim `sim.fossils.poisson`. Pass:
|ΣK − ψΣL| / sqrt(ψΣL) < 3, and the dispersion ratio Σ(K − ψL)²/(ψL), over
replicates with L > 0, divided by their number, within 1 ± 3·sqrt(2/n).

**G3. Piecewise rates (paleobuddy only).** λ = 0.4 for the first 7.5 Myr
from the origin, then 0.1; μ = 0.2; t = 15; 20,000 replicates. Truth:
E[N(t)] = exp(0.2·7.5 − 0.1·7.5) = 2.1170. Pass as G1 (mean only).

**G4. Cross-generator agreement.** The G1 and G2 summaries (extant count,
total species, total lineage duration, fossil count) from paleobuddy and
from TreeSim plus FossilSim, on surviving replicates only (TreeSim returns
no tree for an extinct clade). Pass: two-sample Kolmogorov–Smirnov
p > 0.001 for each of the four. The two codebases are independent; both are
also held to the analytic truths above.

**G5. Taxonomy and pseudoextinction (FossilSim `sim.taxonomy`).** On 2,000
surviving complete TreeSim trees (λ = 0.3, μ = 0.2, t = 15), β = 0.5
(probability of symmetric speciation) and anagenesis rate λa = 0.1. Truth,
conditional on each tree's S speciation events, E extinct tips and total
lineage duration L: (number of morphospecies − 1) has expectation
S(1 + β) + λa·L, and the number of morphospecies that end before the
present has expectation E + βS + λa·L, each with variance
Sβ(1 − β) + λa·L. (Per unit species time these are the rates
λ(1 + β) + λa and μ + βλ + λa of pseudoextinction arguments; conditioning on
the tree removes the survival bias of S and E.) Pass: each pooled count
within 3 standard errors of its pooled expectation.

## Estimators

**E1. divDyn binned rates under complete sampling.** paleobuddy histories,
λ = 0.25, μ = 0.2, 100 starting lineages, 40 Myr, 1-Myr bins; every species
recorded in every bin it lives in. Truth: for a species crossing a bin's
base, survival through the bin has probability e^{−μΔ}, and the age of
species alive at a time is exponential with rate λ once the start-up has
passed, so per-bin three-timer, gap-filler and Foote boundary-crosser
rates estimate μΔ = 0.20 (extinction) and λΔ = 0.25 (origination).
Bins 21–38 only (start-up and edge excluded; at bin 21 the starting
species, whose ages are not exponential, are about 0.7% of those alive);
200 replicates. Pass: the mean
of each rate within 5% of its truth. Under incomplete sampling (Poisson
ψ = 0.5, then binned), the same rates are reported as bias relative to
truth, without a pass criterion.

**E2. PyRate coverage, constant rates.** paleobuddy histories, λ = 0.3,
μ = 0.2, one starting lineage, 25 Myr, conditioned on 30–150 total
species; fossils by `sample.clade` with ψ = 1.0; species with no fossil
removed; extant species flagged with a zero age, as PyRate expects. PyRate
`-A 0 -mHPP` (constant λ, μ, q), 2,000,000 generations sampled every 2,000,
20% burn-in, default priors. 100 replicates. Pass: the central 95%
interval contains the truth in at least 90 of 100 replicates for each of
λ, μ and q (the 2.5% binomial quantile is 91 for a calibrated method).
Replicates with an effective sample size below 100 for any of the three
are reported and excluded from the count; more than 10 such replicates is
a failure. A second arm with ψ = 0.25 (50 replicates) is reported for
coverage and bias without a pass criterion: at low ψ, short-lived species
go unsampled and PyRate does not model unsampled species.

**E3. RevBayes treeless skyline FBD-range (`dnFBDRMatrix`).**
(a) From the deposited outputs of `brpetrucci/skyfbdr_simstudy` (1,000
replicates drawn from the prior, 50,000,000 generations each), compute the
coverage of central 95% intervals for the nine rates. This reproduces the
study's own result from its own outputs; the study's README states no
coverage figure to match.
(b) Rerun RevBayes v1.4.1 on the deposited inputs of replicates 1–50 with
the study's model, priors and moves (`analysis/coverage/master.Rev`),
5,000,000 generations sampled every 1,000, 20% burn-in. Pass: for each
replicate and rate, our posterior median lies inside the deposited run's
central 50% interval in at least 90% of the 450 replicate-rate pairs
(agreement of two MCMC runs on the same input); and our coverage over the
50 replicates is reported alongside (a) for the same replicates.
For a well-calibrated model with parameters drawn from the prior, 95%
coverage is expected; with 1,000 replicates the 2.5% binomial quantile is
936.

## Amendments

**A1, 23 October 2026, before any full run (Claude, Opus 5.5).**
- E3(b) cannot run as declared. RevBayes v1.4.1 refuses the range process:
  `dnFossilizedBirthDeathRange` throws "FBD range process currently disabled
  due to invalid calculations", as does `dnFossilizedBirthDeathSpeciation`
  (commit `02db3b1a2a`, 15 April 2024, "disabled FBD range model"; present
  in every release since). `dnFBDRMatrix`, which the study's script calls,
  is not a registered function in v1.4.1. The range process is being
  reworked on the RevBayes `fbdr` branch (181 commits ahead of
  `development`, last commit 14 October 2026). E3(b) is deferred; building
  and testing that branch is a separate decision.
- E3(a) uses a 20% burn-in, as (b) would have. Index mapping, from the
  study's `simulation/sim.R`: paleobuddy rates are indexed from the origin
  (`lShifts = seq(0, age, age/3)`), RevBayes rates from the present, so
  RevBayes `lambda[k]` is compared with true `lambda(4 - k)`. Coverage under
  the unmapped comparison is also reported, only as a check of the mapping.
- G1–G5 and E1 run their replicates across 12 cores (`parallel::mclapply`,
  L'Ecuyer-CMRG streams); results do not depend on the core count except
  through the random streams.

**A2, 24 October 2026, after the full run and an independent review
(Claude Sonnet subagent), before the tests below were run (Claude, Opus 5.5).**
- New test **G3b (shift order)**: G3 cannot tell λ = 0.4 then 0.1 from the
  reverse, because E[N(15)] depends only on ∫(λ − μ). On 2,000 new paleobuddy
  runs with G3's settings, count species alive 7.5 Myr after the origin.
  Truth if the first rate applies first: e^{(0.4−0.2)·7.5} = 4.4817; if
  reversed, e^{(0.1−0.2)·7.5} = 0.4724. Pass: mean within 3 standard errors
  of 4.4817.
- Disclosures of choices made before the full run but not declared:
  `pyrate_sim.R` rejects records with fewer than 10 sampled species (never
  binding at ψ = 1.0, minimum 21; possibly binding at ψ = 0.25, minimum 12).
  G5's two counts are one check: in every tree, originations − terminations
  = extant species − 1, so the two z-scores are identical, and the test
  constrains βS + λa·L, not β and λa separately. G2's dispersion tolerance
  assumes a per-replicate variance of 2; the true variance is 2 + 1/(ψL),
  so the tolerance is about 2 empirical standard errors for paleobuddy.
  The ten TreeSim clades returned as a single surviving lineage have no
  tree for FossilSim and are absent from G2 and from G4's fossil-count
  comparison.
- Corrections to the text above: seeds are in the scripts and image ids in
  `results/image-ids.txt`, not in each result file; the 2.5% binomial
  quantile for 100 replicates at 0.95 is 90, not 91 (the criterion, at
  least 90, is unchanged).
- PyRate's runs used the compiled FastPyRateC likelihood shipped in the
  repository (the run logs say it was loaded), not the Python functions.
