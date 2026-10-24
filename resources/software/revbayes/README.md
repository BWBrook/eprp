---
id: revbayes
name: RevBayes
kind: program
domain: phylogenetic
languages: [C++, Rev]
home: https://revbayes.github.io/
repo: https://github.com/revbayes/revbayes
paper: [10.1093/sysbio/syw021]
licence: GPL-3.0
release: {version: v1.4.1, date: 2026-07-17, checked: 2026-10-23}
maintenance: {state: active, last_commit: 2026-10-22, checked: 2026-10-23}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.revbayes, image: "eprp-sw/bench-revbayes:t1 (sha256:bee72736…)", host: deep-server}
blockers: ["FBD range and FBD speciation processes disabled in every release since 2024-04-15", "dnFBDRMatrix, used by the 2025 skyfbdr study, not registered in v1.4.1"]
related_sources: []
eprp_questions: [Q-006, Q-022, Q-003, Q-005]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
---

# RevBayes

## Summary

RevBayes is a general Bayesian phylogenetics engine in which models are
written in its own language (Rev) as graphical models: tree and tip-dating
models including the fossilized birth–death process, diversification models,
character evolution and biogeography. For EPRP the draw was the treeless
skyline FBD-range model, which would give Q-006 a piecewise likelihood for
stratigraphic ranges. **That model does not run in any current release.**

## Method

Not assessed in this tranche beyond the FBD range process. The range process
(`dnFossilizedBirthDeathRange`, alias `dnFBDRP`) is documented with
piecewise-constant λ, μ and ψ on a `timeline` and marginalisation of
unlisted fossils (`complete = FALSE`).

## Install

Official v1.4.1 Linux tarball in `ubuntu:24.04`
([Dockerfile](../bench/env/Dockerfile.revbayes); tarball sha256
`5d130269…2939650`, recorded in the image). The binary runs; the smoke test
failed at the model, as below.

## Validation

E3 in [bench/VALIDATION.md](../bench/VALIDATION.md) and amendment A1.

- **E3(b), rerun of the skyfbdr study on its inputs: blocked.** In v1.4.1,
  `dnFossilizedBirthDeathRange` throws "FBD range process currently
  disabled due to invalid calculations", as does
  `dnFossilizedBirthDeathSpeciation`. The throw was added by commit
  `02db3b1a2a` ("disabled FBD range model", 15 April 2024) and is in every
  release since. `dnFBDRMatrix`, which the study's script calls, is not a
  registered function. The model is being reworked on the `fbdr` branch,
  181 commits ahead of `development`, with commits through 14 October 2026
  (rewrites of the timeline, origin handling and ρ < 1 sampling).
- **E3(a), coverage from the study's deposited runs** (1,000 prior draws,
  50 million generations each, built with an unrecorded RevBayes version):
  λ 0.932 / 0.945 / 0.954, μ 0.945 / 0.938 / 0.948, ψ 0.941 / 0.903 / 0.944,
  oldest stage first (pooled 0.939); 936/1,000 is the lower 2.5% binomial
  bound for calibrated intervals. The oldest-stage λ and, clearly, the
  middle-stage ψ fall below it, with misses in the tails of the true
  values; MCMC length and burn-in are not the cause (details in
  [bench/README.md](../bench/README.md)). The study's redraw of all
  parameters on its sampled-species rule preserves calibration; its
  fixed-parameter loops (at least five total species; resampling fossils
  until one species is sampled) do not, and are the open candidates. This
  checks the study's own result, not v1.4.1.

## Strengths

- The most complete fossil-aware Bayesian modelling environment found
  (scan C), with active development.
- The deposited skyline FBD-range runs are close to calibrated.

## Weaknesses and pitfalls

- **The documentation does not say the range process is disabled.** Its
  help page lists the function and its arguments; only running it shows
  the error.
- Index conventions: rate vectors on a `timeline` start at the present;
  paleobuddy and the skyfbdr study's true values start at the origin.
- Command-line arguments are positional (`rb script.Rev 1 20000 out`);
  `--args` is passed through literally in v1.4.1.

## Alternatives and overlap

BEAST2 with the SA package implements FBD on trees (not the treeless range
process). PyRate estimates rates from occurrences without modelling
unsampled species. The `fbdr` branch is the route to the treeless range
model.

## EPRP relevance

Q-006 (lead L-001, corrected): the piecewise range likelihood exists in
development code only, and its released implementation was withdrawn as
incorrect. Using it needs a pinned `fbdr` build and our own calibration
test; E3(b) is the ready-made test.

## Citation and licence

Höhna, S., Landis, M. J., Heath, T. A., Boussau, B., Lartillot, N.,
Moore, B. R., Huelsenbeck, J. P. and Ronquist, F. (2016). RevBayes: Bayesian
phylogenetic inference using graphical models and an interactive
model-specification language. *Systematic Biology* 65, 726–736.
doi:10.1093/sysbio/syw021 (checked on Crossref). GPL-3.0.

## Verification log

- 2026-10-23 `checked`: v1.4.1 release assets, repository activity.
- 2026-10-23 `checked`: v1.4.1 error on `dnFossilizedBirthDeathRange`;
  source `src/revlanguage/distributions/phylogenetics/matrix/Dist_FBDRP.cpp`
  and `tree/Dist_FBDSP.cpp`; commit `02db3b1a2a`; `fbdr` branch state
  (re-enabled `createDistribution`, last commit `38b98c3a53`, 14 Oct 2026).
- 2026-10-23 `checked`: E3(a) from `brpetrucci/skyfbdr_simstudy` at
  `950b9bc`.
- 2026-10-24 `checked`: the study's `simulation/sim.R` redraws coverage
  parameters unless 5–50 species are sampled; its README and a code comment
  say 5–20.
