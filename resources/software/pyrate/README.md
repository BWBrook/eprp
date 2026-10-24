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
validated_uses: ["constant-rate birth-death with homogeneous Poisson preservation (-A 0 -mHPP): lambda and mu intervals calibrated at high preservation; q intervals not calibrated"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.pyrate, image: "eprp-sw/bench-pyrate:t1 (sha256:8df17071…)", host: deep-server}
blockers: ["AGPL-3.0: obligations if a modified version is served to users"]
related_sources: []
eprp_questions: [Q-004, Q-006, Q-012, Q-045]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
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
conditioned on at least one fossil (`PyRate.py` lines 3266–3342 at
`6a27efb`, checked). The birth–death likelihood runs over the sampled
species only, so species never sampled are not modelled (recall of the 2014
paper; consistent with the E2 diagnostics).

## Install

`python:3.12-slim`, PyRate cloned at commit `6a27efb`, `pip install -r
requirements.txt` (numpy, scipy, dendropy, pandas, tqdm, matplotlib,
scikit-learn, nlopt); `pip freeze` is stored in the image
([Dockerfile](../bench/env/Dockerfile.pyrate)). The optional compiled
`fastPyRateC` was not built. About 2,000 generations per second for 80
species; 2 million generations took 15–17 minutes.

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
ψ 1.0: **λ and μ pass, q fails.**

Post hoc diagnostics on the same histories ([bench/README.md](../bench/README.md)):
- PyRate's inferred durations of sampled species are 8% short at ψ 1.0
  and 31% short at ψ 0.25; singletons 34% and 50% short.
- With known durations, sampled species alone give q at +6.5% and +43%;
  PyRate's posterior median sits at that value (1.089 against 1.065;
  0.364 against 0.356). The shortening and the zero truncation roughly
  cancel.
- Our reading, not yet tested: the birth–death prior on each species'
  times is not conditioned on that species being sampled, while sampled
  species are biased towards long durations.

## Strengths

- λ and μ intervals calibrated at ψ 1.0 despite a −11% median bias.
- Active development (commit on 22 October 2026) and a broad model family.
- Fast enough for coverage studies on a modest server.

## Weaknesses and pitfalls

- **Preservation-rate intervals undercover** (81% at ψ 1.0, 66% at ψ 0.25)
  and q is biased high, rising steeply as preservation falls. Any use of q
  as a quantity of interest, or of preservation-corrected richness, inherits
  this.
- λ and μ calibration degrades at low preservation (μ covered 80% at
  ψ 0.25).
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
  `PyRate.py`; attribution and duration diagnostics run.
