---
id: divdyn
name: divDyn
kind: r-package
domain: diversity-rates
languages: [R, C++]
home: https://cran.r-project.org/package=divDyn
repo: https://github.com/divDyn/r-package
paper: [10.1111/2041-210x.13161]
licence: "CC BY 4.0 (CRAN DESCRIPTION); GPL-3.0 (GitHub repository): conflicting"
release: {version: 0.8.3, date: 2024-11-21, checked: 2026-10-23}
maintenance: {state: slow, last_commit: 2025-12-01, checked: 2026-10-23}
tier: T2
validated_uses: ["three-timer, gap-filler and boundary-crosser rates under complete sampling", "corrected three-timer and gap-filler rates under homogeneous Poisson sampling (characterised, no declared tolerance)"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r, image: "eprp-sw/bench-r:t1 (sha256:926c0052…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-038]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# divDyn

## Summary

divDyn computes diversity dynamics from binned occurrence data: richness
counts, origination and extinction rates (proportions, per-capita
boundary-crosser, three-timer and corrected three-timer, gap-filler,
second-for-third), sampling completeness, and subsampling (classical
rarefaction, SQS, by-list and others), plus selectivity tests. Reach for it
for stage-level rates and standardised richness from PBDB-style data.

## Method

Counts of taxa by their sampling pattern around each bin (two-timers,
three-timers, part-timers, gap-fillers) feed the rate formulas of Foote
(2000) and Alroy (2008, 2014, 2015). Rates are per bin, not per Myr. Bins
are integers with higher numbers younger unless `revtime = TRUE`.

## Install

CRAN binary in the shared R image ([Dockerfile](../bench/env/Dockerfile.r)).

## Validation

E1 in [bench/VALIDATION.md](../bench/VALIDATION.md): paleobuddy histories
(λ 0.25, μ 0.2, 100 starting species, 40 Myr, 1-Myr bins, bins 21–38,
200 replicates). Truth is λΔ = 0.25 and μΔ = 0.20 per bin.

| Rate | Complete sampling | Poisson sampling, ψ 0.5 (no tolerance declared) |
| --- | --- | --- |
| `ext3t` / `ori3t` (raw three-timer) | 0.1998 / 0.2501 | +482% / +385% |
| `extC3t` / `oriC3t` (corrected three-timer) | same | +1.2% / −0.3% |
| `extGF` / `oriGF` (gap-filler) | same | +1.5% / +1.0% |
| `extPC` / `oriPC` (boundary-crosser) | same | +7.9% / +0.2% |
| `ext2f3` / `ori2f3` (second-for-third) | same | −36% / −36% |

Under complete sampling every column is within 0.2% of the truth (declared
tolerance 5%): **pass**. The raw three-timer carries the log of the
three-timer sampling probability by design (here about log(1/0.39)); the
corrected form removes it.

## Strengths

- Exact under complete sampling; the corrected three-timer and gap-filler
  rates are within 2% under homogeneous sampling at 39% per-bin sampling
  probability.
- One function returns every standard rate, so estimators can be compared
  on identical counts.

## Weaknesses and pitfalls

- **Second-for-third rates (`ext2f3`, `ori2f3`) were 36% low** under
  homogeneous Poisson sampling. divDyn always substitutes the middle value
  of the three subsequent-sampling counts (`sort(y)[2]`), and its source
  comment notes uncertainty about Alroy's (2015) rule. Not yet checked
  against the paper; do not rely on these columns until it is.
- `ext3t`/`ori3t` are the raw rates; use `extC3t`/`oriC3t` or the
  gap-filler rates for estimates.
- The boundary-crosser extinction rate was 7.9% high under sampling
  (origination +0.2%); our reading is that sampled ranges end early (range
  truncation), which boundary-crosser rates do not correct.
- Licence metadata conflict: CRAN says CC BY 4.0, the repository GPL-3.0.
- Rates are per bin; unequal bin durations need explicit handling.

## Alternatives and overlap

palaeoverse covers preparation and binning but not these rates. PyRate
estimates rates in continuous time with preservation modelled. `squares`
and SQS implementations elsewhere cover richness, not rates.

## EPRP relevance

Stage-level rates for Q-040, Q-042 and Q-038 style analyses; the shared
counting makes it the natural engine for an estimator comparison (lead
N-002). Its SQS subsampling is not yet tested; see lead L-006 on coverage
rarefaction.

## Citation and licence

Kocsis, Á. T., Reddin, C. J., Alroy, J. and Kiessling, W. (2019). The R
package divDyn for quantifying diversity dynamics using fossil sampling data.
*Methods in Ecology and Evolution* 10, 735–743. doi:10.1111/2041-210x.13161
(checked on Crossref).

## Verification log

- 2026-10-23 `checked`: CRAN 0.8.3 (2024-11-21), GitHub activity and the
  licence conflict by `landscape.py`.
- 2026-10-23 `checked`: E1 run on `deep-server`, 200 replicates.
- 2026-10-24 `checked`: second-for-third formula read in
  `R/diversityDynamics.r` (lines 536–546 on GitHub `master`).
