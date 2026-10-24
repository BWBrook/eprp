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
release: {version: "1.1.0 (DESCRIPTION dated 2021-06-01; GitHub commit 508d3c9 of 2023-12-04)", date: 2021-06-01, checked: 2026-10-24}
maintenance: {state: dormant, last_commit: 2023-12-04, checked: 2026-10-24}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["not on CRAN; installed from GitHub subdirectory Rextinct/", "griwm reads only a file path of integer dates and errors"]
related_sources: [fossahul]
eprp_questions: [Q-034, Q-013, Q-017]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
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

| Score | A: errors 0.001 Myr | B: hiatuses | C: errors 0.25 Myr (A2 rerun) |
| --- | --- | --- | --- |
| 2.5–97.5% interval covers TE, biased / unbiased | 0.009 / 0.003 | 0.002 / 0.005 | 0.689 / 0.682 |
| biased median (α 0.05) read as a 95% bound (post hoc) | 0.672 | 0.528 | 0.743 |
| unbiased median: median error / median absolute error, as fraction of observed range | −0.049 / 0.117 | −0.145 / 0.211 | −0.028 / 0.134 |
| unbiased median: root-mean-square error (Myr) | 0.914 | 1.568 | 0.919 |

For comparison in arm A, a median-unbiased Strauss–Sadler point,
last + R(2^{1/(n−1)} − 1), has median absolute error 0.123 of the range and
root-mean-square error 0.862 Myr.

## Strengths

- The unbiased GRIWM median has the lowest median scaled absolute error of
  the methods run (0.117 of the observed range in arm A, against 0.149 for
  EDE's Strauss–Sadler estimate). It is no better than a median-unbiased
  Strauss–Sadler point (0.123) and worse on root-mean-square error (0.914
  against 0.862 Myr); 62% of its estimates fall before the truth.
- Handles dating error and radiocarbon calibration in one call.

## Weaknesses and pitfalls

- **Its interval is not a confidence interval for the extinction time.**
  The 2.5–97.5% quantiles are the spread of the estimate across
  resamplings of the dates. With negligible dating error they collapse
  (width about 0.01 Myr) and cover the truth under 1% of the time; with
  0.25-Myr errors, 68–69%. Sampling uncertainty (how far extinction lies
  beyond the last record) is not in the interval. Our reading of the
  method, consistent with these results.
- The biased form at α 0.05, read as a 95% bound, covers 0.67.
- `griwm` reads only a file path (it calls `data.table::fread` on
  `chrono_data`), with dates in years BP and errors as integers; a data
  frame fails.
- **`griwm` calls `set.seed(i_iter)` inside its resampling loop**
  (`R/griwm.R` line 335), which resets the caller's random stream. It
  invalidated our first arm C: dating errors drawn after a `griwm` call in
  the same worker repeated across cases. Draw any random numbers you need
  before calling it, or reseed afterwards.
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
