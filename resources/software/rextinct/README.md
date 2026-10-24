---
id: rextinct
name: Rextinct (GRIWM, CRIWM)
kind: r-package
domain: extinction-timing
languages: [R]
home: https://github.com/FredSaltre/CRIWM
repo: https://github.com/FredSaltre/CRIWM
paper: [10.1016/j.quascirev.2011.11.021, 10.1016/j.quageo.2023.101489]
licence: MIT
release: {version: "1.1.0 (DESCRIPTION; GitHub commit 508d3c9)", date: 2023-12-04, checked: 2026-10-24}
maintenance: {state: dormant, last_commit: 2023-12-04, checked: 2026-10-24}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["not on CRAN; installed from GitHub subdirectory Rextinct/", "griwm reads only a file path of integer dates and errors"]
related_sources: [fossahul]
eprp_questions: [Q-034, Q-013, Q-017]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# Rextinct (GRIWM and CRIWM)

## Summary

Rextinct implements GRIWM (Bradshaw et al. 2012), which estimates
extinction (or arrival) time from dated records with dating errors by
resampling each date from its error distribution and applying an
inverse-weighted McInerny estimator, and CRIWM, its extension with
radiocarbon calibration (Herrando-Pérez & Saltré 2024). It is aimed at
Quaternary chronologies. Barry Brook is a co-author of the 2012 paper.

## Install

`remotes::install_github("FredSaltre/CRIWM", subdir = "Rextinct", ref =
"508d3c9")` (imports data.table, moments, rcarbon).

## Validation

Characterised, no declared pass criteria (E4–E6), 2,000 species, calendar
dates (`radiocarbon = 0`), `resample = 1000`:

| Score | A: errors 0.001 Myr | B: hiatuses | C: errors 0.25 Myr |
| --- | --- | --- | --- |
| 2.5–97.5% interval covers TE, biased / unbiased | 0.008 / 0.003 | 0.002 / 0.006 | 0.706 / 0.682 |
| biased median (α 0.05) read as a 95% bound (post hoc) | 0.672 | 0.528 | 0.706 |
| unbiased median: median error / median absolute error, as fraction of observed range | −0.049 / 0.117 | −0.145 / 0.211 | −0.050 / 0.126 |

## Strengths

- **The unbiased GRIWM median is the most accurate point estimator in the
  benchmark**: median absolute error 0.117 of the observed range under
  ideal sampling, against 0.149 for the Strauss–Sadler estimate and 0.166
  for Robson–Whitlock.
- Handles dating error and radiocarbon calibration in one call.

## Weaknesses and pitfalls

- **Its interval is not a confidence interval for the extinction time.**
  The 2.5–97.5% quantiles are the spread of the estimate across
  resamplings of the dates. With negligible dating error they collapse
  (width about 0.01 Myr) and cover the truth under 1% of the time; with
  0.25-Myr errors, about 70%. Sampling uncertainty (how far extinction lies
  beyond the last record) is not in the interval. Our reading of the
  method, consistent with these results.
- The biased form at α 0.05, read as a 95% bound, covers 0.67.
- `griwm` reads only a file path (it calls `data.table::fread` on
  `chrono_data`), with dates in years BP and errors as integers; a data
  frame fails.
- Prints a progress bar per resampling run.
- Not on CRAN; last commit December 2023.

## Alternatives and overlap

EDE (Strauss–Sadler, Robson–Whitlock and Solow give calibrated bounds
under homogeneous sampling, but ignore dating error); `tbea`.

## EPRP relevance

Q-034 (island and regional extinction chronologies), with FosSahul-style
quality-rated ages. For a defensible bound, pair the GRIWM point estimate
with a sampling-based bound, or extend the resampling to include sampling
uncertainty.

## Citation and licence

Bradshaw, C. J. A., Cooper, A., Turney, C. S. M. and Brook, B. W. (2012).
Robust estimates of extinction time in the geological record. *Quaternary
Science Reviews* 33, 14–19. doi:10.1016/j.quascirev.2011.11.021.
Herrando-Pérez, S. and Saltré, F. (2024). Estimating extinction time using
radiocarbon dates. *Quaternary Geochronology* 79, 101489.
doi:10.1016/j.quageo.2023.101489. Both checked on Crossref. MIT.

## Verification log

- 2026-10-24 `checked`: E4–E6 on `deep-server`; `man/griwm.Rd` and
  DESCRIPTION read at `508d3c9`.
