---
id: paleoam
name: paleoAM
kind: r-package
domain: fossil-record-forward
languages: [R]
home: https://cran.r-project.org/package=paleoAM
repo: https://github.com/dwbapst/paleoAM
paper: [10.26879/1282]
licence: CC0 (CRAN DESCRIPTION; the repository declares none)
release: {version: 1.0.1, date: 2024-09-17, checked: 2026-10-24}
maintenance: {state: slow, last_commit: 2025-10-16, checked: 2026-10-24}
tier: T2
validated_uses: ["simMixedAssemblageSample: a time-averaged sample is an unbiased mixture of its timesteps"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [Q-005, Q-041, B-007]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# paleoAM

## Summary

paleoAM fits species abundance models (kernel density estimates) along an
environmental gradient and simulates fossil assemblage series through
gradient change, time-averaging, bioturbation, sedimentation rate and
sampling, to ask whether an abrupt environmental change would be
detectable in an assemblage proxy. It ships two example datasets: Gulf of
Alaska benthic foraminifera and Katian–Hirnantian graptolites.

## Validation

| Test | Result |
| --- | --- |
| P1: Gulf of Alaska models; 30 gradient values; 200 replicates of pooled timestep abundances against time-averaged samples of 2,000 specimens | pass (17 species above 1%; max \|z\| = 2.57, declared < 3.5) |

Only the mixing layer is tested. The detectability machinery
(`simulateFossilAssemblageSeries`, bioturbation, sedimentation rate,
`getRecoveredTransitionDuration`) needs its own known-truth design.

## Weaknesses and pitfalls

- The interface is built around its fitted KDE objects
  (`getSpeciesSpecificRescaledKDE`, `getProbOccViaPresAbs`); simulating
  other assemblages means fitting those first.
- Licence: CC0 on CRAN, none declared in the repository.

## EPRP relevance

Time-averaging and bioturbation for Q-005's and Q-041's surrogates (lead
L-011); the 2026 argument that sediment accumulation, not mixing, sets
temporal resolution could be tested with it.

## Citation and licence

Belanger, C. L. and Bapst, D. W. (2023). Simulating our ability to
accurately detect abrupt changes in assemblage-based paleoenvironmental
proxies. *Palaeontologia Electronica*. doi:10.26879/1282 (checked on
Crossref). CC0 per CRAN.

## Verification log

- 2026-10-24 `checked`: P1 on `deep-server`; package datasets and examples
  read in the container.
