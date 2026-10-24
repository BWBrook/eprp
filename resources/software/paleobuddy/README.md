---
id: paleobuddy
name: paleobuddy
kind: r-package
domain: fossil-record-forward
languages: [R]
home: https://cran.r-project.org/package=paleobuddy
repo: https://github.com/brpetrucci/paleobuddy
paper: [10.1111/2041-210x.13996]
licence: GPL-3
release: {version: 1.1.0, date: 2025-02-05, checked: 2026-10-23}
maintenance: {state: active, last_commit: 2026-09-04, checked: 2026-10-23}
tier: T2
validated_uses: ["constant-rate birth-death histories (bd.sim)", "piecewise speciation rates, including shift order (bd.sim with lShifts)", "Poisson fossil sampling (sample.clade)"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r, image: "eprp-sw/bench-r:t1 (sha256:926c0052…)", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [Q-004, Q-006, Q-012, Q-045]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
---

# paleobuddy

## Summary

paleobuddy simulates species-level birth–death histories and their fossil
records without building a tree: rates can be constant, functions of time or
of an environmental variable, step functions, or age-dependent (Weibull), and
fossil sampling can vary in time, by species age, or be returned as stratigraphic
ranges in bins. It is the generator behind the 2025 skyline FBD-range study.
Reach for it for rate-estimator benchmarks on occurrence data.

## Method

Event times are drawn per species from (possibly time-varying) exponential
waiting times; time-varying rates are integrated numerically (`rexp.var`).
`bd.sim` returns speciation (`TS`) and extinction (`TE`) times in geological
time (origin at `tMax`, present at 0), parents and extant status;
`sample.clade` draws fossil times per species.

## Install

As FossilSim (same image, [Dockerfile](../bench/env/Dockerfile.r)).

## Validation

| Test | Result |
| --- | --- |
| G1: `bd.sim` (λ 0.3, μ 0.2, 15 Myr, 20,000 runs) against e^{(λ−μ)t} = 4.482 and survival 0.3916 | pass (4.523, z = 0.66; 0.3934, z = 0.51) |
| G2: `sample.clade` (ψ 0.5): total count and dispersion against Poisson(ψL) | pass (z = −0.29; dispersion 0.994 ± 0.030) |
| G3: speciation 0.4 then 0.1 at 7.5 Myr, μ 0.2: mean extant against 2.117 | pass (2.115, z = −0.08) |
| G3b (A2): species alive 7.5 Myr after the origin, against 4.482 (0.472 if the shift order were reversed) | pass (4.569, z = 0.55) |
| G4: against TreeSim and FossilSim | pass (KS p 0.25–0.56; low power, TreeSim 1.0–1.4% higher on all four summaries) |

It also served as truth for E1 (divDyn) and E2 (PyRate); see
[bench/README.md](../bench/README.md).

## Strengths

- General rate forms (time, environment, age, steps) in one interface.
- Fast for constant rates: 0.27 s for a 40-Myr history of 4,218 species,
  under 1 ms for a 15-Myr clade (`bench/results/generators/g3b_timing.json`).
- Independent of FossilSim and TreeSim; KS tests did not distinguish them
  (low power).

## Weaknesses and pitfalls

- Time-varying rates are slow: 1.4 s (an uncommitted first measurement)
  and 3.2 s (`g3b_timing.json`) per 15-Myr history with one speciation
  shift, against under 1 ms with constant rates; our reading is that the
  waiting times are integrated numerically. G3's 20,000 runs
  needed 12 cores.
- `TE` is `NA` for extant species unless `trueExt = TRUE`.
- Times run backwards from `tMax`, but rate shift times (`lShifts`,
  `mShifts`, `rShifts`) are given forward from the origin, and G3b confirms
  that the first rate applies first. Rate vectors are therefore ordered
  oldest first, the reverse of RevBayes' `timeline` convention.
- `nFinal` conditions on the total number of species by rejection; at
  λ 0.3, μ 0.2 over 25 Myr this moves complete-knowledge λ and μ estimates
  by under 4% (`bench/results/e2/e2_attribution.json`).
- `sample.clade` reports species with no fossils only in a message.

## Alternatives and overlap

FossilSim with TreeSim for tree-based simulation; PyRate's simulator; the
DeepDive simulator for spatially structured records.

## EPRP relevance

Default truth generator for the rate benches (tranches 1, 2 and 4), and for
age-dependent extinction rivals in Q-012 (lead L-017).

## Citation and licence

do Rosario Petrucci, B., Januario, M. and Quental, T. (2022). paleobuddy: an
R package for flexible simulations of diversification and fossil sampling.
*Methods in Ecology and Evolution* 13, 2692–2698.
doi:10.1111/2041-210x.13996. GPL-3.

## Verification log

- 2026-10-23 `checked`: CRAN 1.1.0, GitHub release v1.1.0 and activity by
  `landscape.py`.
- 2026-10-23 `checked`: G1–G4 on `deep-server`.
- 2026-10-24 `checked`: G3b and timings (`bench/validate/g3b_timing.R`).
