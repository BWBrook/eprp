---
id: pyrate
name: PyRate
kind: program
domain: diversity-rates
languages: [Python, C++ (optional fastPyRateC)]
home: https://github.com/dsilvestro/PyRate
repo: https://github.com/dsilvestro/PyRate
paper: [10.1093/sysbio/syu006, 10.1017/pab.2019.23]
licence: AGPL-3.0
release: {version: "master 6a27efb (latest tag v3.1.1, 2022-03-09)", date: 2026-10-22, checked: 2026-10-23}
maintenance: {state: active, last_commit: 2026-10-22, checked: 2026-10-23}
tier: T2
validated_uses: ["constant-rate birth-death with homogeneous Poisson preservation (-A 0 -mHPP) at high preservation: no undercoverage detected for lambda and mu (medians about 11% low); q intervals failed"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.pyrate, image: "eprp-sw/bench-pyrate:t1 (sha256:8df17071…)", host: deep-server}
blockers: ["AGPL-3.0: obligations if a modified version is served to users"]
related_sources: []
eprp_questions: [Q-004, Q-006, Q-012, Q-045]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
---

# PyRate

## Summary

PyRate estimates speciation, extinction and preservation rates from fossil
occurrences in a Bayesian framework, jointly inferring each species' times of
origin and extinction. Its family of models covers rate shifts (RJMCMC,
BDMCMC), age-dependent extinction (ADE), diversity- and covariate-dependent
rates, trait-dependent models with neural networks (BDNN), dispersal
(DES), and richness through time (mcmcDivE). Reach for it when rates are the
target and stratigraphic ranges are incomplete.

## Method

The birth–death likelihood is evaluated on the inferred species times; the
preservation likelihood is Poisson along each species' life (homogeneous,
time-binned or non-homogeneous), zero-truncated so that every species is
conditioned on at least one fossil. Our runs used the compiled likelihood
(`pyrate_lib/fastPyRateC/ModulePyrateC/FastPyRateC.cpp`, `PyRateC_HOMPP_lik`,
lines 247–292 at `6a27efb`; the run logs say "Module FastPyRateC was
loaded"), which matches the Python fallback (`PyRate.py` lines 3313–3342)
and excludes the zero age that flags an extant species (both checked). The birth–death likelihood runs over the sampled
species only, so species never sampled are not modelled (recall of the 2014
paper; consistent with the E2 diagnostics).

## Install

`python:3.12-slim`, PyRate cloned at commit `6a27efb`, `pip install -r
requirements.txt` (numpy, scipy, dendropy, pandas, tqdm, matplotlib,
scikit-learn, nlopt); `pip freeze` is stored in the image
([Dockerfile](../bench/env/Dockerfile.pyrate)). The repository ships a
compiled FastPyRateC module for Python 3.12, which loaded without a build
step. The smoke test ran at about 2,000 generations per second for 80
species; the 150 E2 runs of 2 million generations averaged about 18 minutes
each (3 h 50 min as 12 parallel jobs).

## Validation

E2 in [bench/VALIDATION.md](../bench/VALIDATION.md): paleobuddy histories
(λ 0.3, μ 0.2, 25 Myr, 30–150 total species), Poisson fossils, species
without fossils removed, extant species flagged; `-A 0 -mHPP`, 2 million
generations, 20% burn-in, default priors. Every run reached an effective
sample size of at least 100 for λ, μ and q.

| Arm | 95% interval covers truth | Median relative bias |
| --- | --- | --- |
| ψ 1.0, 100 replicates | λ 95, μ 95, **q 81** | λ −11%, μ −12%, q +9% |
| ψ 0.25, 50 replicates | λ 44, μ 40, q 33 | λ +6%, μ −3%, q +46% |

The declared criterion was at least 90 of 100 for each parameter at
ψ 1.0: **E2 fails, on q; λ and μ meet the criterion.** For λ and μ that
means no undercoverage detected (95/100 is compatible with roughly 89–98%),
not calibration: their medians are 11–12% low, about 0.8 posterior sd, and
all five misses of each lie on one side.

The q intervals are about the right width (posterior sd 0.084q against a
spread of medians of 0.078q) but shifted about one posterior sd high; all
19 misses have the truth below the interval. Post hoc diagnostics on the
same histories ([bench/README.md](../bench/README.md)):
- PyRate's inferred durations of sampled species are 8% short at ψ 1.0
  and 31% short at ψ 0.25; singletons 34% and 50% short.
- PyRate's own zero-truncated preservation likelihood, maximised at the
  true durations, gives q within 2% of the truth (1.006; 0.246). At
  PyRate's inferred durations it gives 1.096 and 0.358, matching PyRate's
  posterior medians (1.090; 0.364). The preservation likelihood is sound;
  the bias comes from the durations.
- Our reading, not yet tested: the likelihood divides by the probability
  of being sampled, (1 − e^{−qD}), while the birth–death prior on species'
  times has no matching factor, so short durations are favoured.

## Strengths

- At ψ 1.0, no undercoverage detected for λ and μ despite a −11% median
  bias, because the intervals are wide.
- Active development (commit on 22 October 2026) and a broad model family.
- Fast enough for coverage studies on a modest server.

## Weaknesses and pitfalls

- **Preservation-rate intervals undercover** (81% at ψ 1.0, 66% at ψ 0.25)
  because q is biased high, rising steeply as preservation falls. Any use of
  q as a quantity of interest, or of preservation-corrected richness,
  inherits this.
- At low preservation λ and μ intervals are narrower than the spread of the
  medians and μ is covered only 80% of the time (ψ 0.25).
- The E2 simulations reject records with fewer than 10 sampled species
  (disclosed in A2); this may bind at ψ 0.25.
- The last tagged release (v3.1.1) is from 2022; work from a pinned commit.
- Input is a generated Python file (`data_1=[array(...)]`); extant species
  need a 0 appended to their ages.
- AGPL-3.0.

## Alternatives and overlap

RevBayes' FBD-range process models unsampled species explicitly but is
disabled in releases ([RevBayes entry](../revbayes/README.md)). divDyn gives
binned rates with sampling corrections. DeepDive estimates richness, not
rates.

## EPRP relevance

Rate estimation for Q-006 (as the non-tree alternative), Q-012 (age-dependent
extinction; the survivorship-bias preprint in lead L-007 bears on the ADE
model), Q-045 and Q-004. The q bias matters wherever preservation rates are
compared between intervals or clades.

## Citation and licence

Silvestro, D., Schnitzler, J., Liow, L. H., Antonelli, A. and Salamin, N.
(2014). Bayesian estimation of speciation and extinction from incomplete
fossil occurrence data. *Systematic Biology* 63, 349–367.
doi:10.1093/sysbio/syu006 (checked on Crossref). The 2019 *Paleobiology*
update (doi:10.1017/pab.2019.23) is from the scans and not checked here.
AGPL-3.0.

## Verification log

- 2026-10-23 `checked`: repository, licence and commit by `landscape.py`
  and `gh`.
- 2026-10-23 `checked`: Ursidae example smoke run (20,000 generations in
  10 s); `alpha` fixed at 1 in all logs (no gamma heterogeneity).
- 2026-10-23 `checked`: E2, 150 runs on `deep-server`, 3 h 50 min as 12 jobs.
- 2026-10-24 `checked`: zero-truncated preservation likelihood read in
  `PyRate.py` and `FastPyRateC.cpp`; attribution, duration, interval-width
  and truncated-MLE diagnostics run; ESS recomputed with the standard Geyer
  pairing (no change to coverage; every run above 100).
