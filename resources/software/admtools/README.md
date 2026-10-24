---
id: admtools
name: admtools
kind: r-package
domain: fossil-record-forward
languages: [R]
home: https://cran.r-project.org/package=admtools
repo: https://github.com/MindTheGap-ERC/admtools
paper: [10.5194/gchron-7-427-2025]
licence: GPL (>= 3)
release: {version: 0.7.0, date: 2026-10-08, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-10-08, checked: 2026-10-24}
tier: T2
validated_uses: ["time_to_strat: time to height, including hiatus removal (destructive = TRUE)", "get_completeness and get_hiat_duration"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["strat_to_time returns wrong times above each hiatus (S1)"]
related_sources: []
eprp_questions: [B-007, Q-003, Q-005, Q-041]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# admtools

## Summary

admtools builds and manipulates age–depth models (from tie points, from
sediment accumulation curves, or nonparametrically from sedimentological
information) and transforms data between the time and stratigraphic
domains. It is the transformation engine under StratPal. Reach for it to
pass simulated events through a stratigraphic column, or to estimate
age–depth models with uncertainty.

## Method

An age–depth model is a monotone map from time to height, with flat
segments for hiatuses. `time_to_strat` maps times to heights (`NA` for
times in a hiatus when `destructive = TRUE`); `strat_to_time` maps
heights back to times through `get_time`.

## Install

CRAN 0.7.0 in the tranche-2 image ([Dockerfile](../bench/env/Dockerfile.r2)).

## Validation

Tests in [bench/VALIDATION_T2.md](../bench/VALIDATION_T2.md); results in
[bench/README.md](../bench/README.md) (tranche 2).

| Test | Result |
| --- | --- |
| S1: round trip `strat_to_time(time_to_strat(t))` on a model with hiatuses at 4–6 and 12–15 Myr | **fail**: 3,972 of 8,282 deposited times wrong, by up to 2.0 and 3.0 Myr |
| S2: fraction of times lost to hiatuses; `get_completeness`, `get_hiat_duration` | pass |
| S3: constant accumulation | pass (exact) |

## Weaknesses and pitfalls

- **`strat_to_time` is wrong for every height between a hiatus and the
  next tie point.** `get_time.adm` (unchanged since 2023) interpolates with
  `stats::approx(x = h, y = t, ties = list("ordered", min))`. The two tie
  points that share a hiatus height collapse to the hiatus start before
  interpolation, so heights above the surface are interpolated from the
  hiatus start, not its end. The error is up to the hiatus duration. On
  the S1 model, 48% of deposited times came back wrong. `hiat_mode =
  "end"` has the mirror error below a hiatus, and `"destroy"` sets to `NA`
  every height where the two modes differ, which removes valid data on
  both sides.
- Dense age–depth models (tie points every 0.01 Myr) shrink the affected
  interval to one spacing above each hiatus, but not the size of the error
  (0.47 Myr maximum in S1).
- Until fixed, do not use `strat_to_time` (or functions that call it) on
  models with hiatuses; invert `time_to_strat` directly instead. Queued
  for the authors as [CONTACTS](../CONTACTS.md) S1.
- Data come first and the model second: `time_to_strat(times, adm)`,
  `strat_to_time(heights, adm)`; passing the model first fails with "no
  applicable method".

## Alternatives and overlap

StratPal wraps it. CarboKitten.jl (Julia) and CarboCAT (MATLAB) model the
stratigraphy itself; neither runs on our hosts.

## EPRP relevance

The stratigraphic-filter arm of the extinction benchmark used
`time_to_strat` (correct) to remove fossils in hiatuses. B-007, Q-005 and
Q-041 pipelines that convert strat-domain data back to time must avoid
`strat_to_time` until it is fixed.

## Citation and licence

Hohmann, N., De Vleeschouwer, D., Batenburg, S. and Jarochowska, E. (2025).
Nonparametric estimation of age–depth models from sedimentological and
stratigraphic information. *Geochronology* 7, 427–448.
doi:10.5194/gchron-7-427-2025 (checked on Crossref). GPL (≥ 3).

## Verification log

- 2026-10-24 `checked`: S1–S3 on `deep-server`; `R/get_time.adm.R` read
  on GitHub (`main`) and its commit history (last change 2023-12-18).
