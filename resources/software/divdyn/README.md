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
validated_uses: ["origination and extinction rates under complete sampling (all rate columns coincide there)", "squares (`indices`) equals Alroy's (2018) formula", "Chao2 (`indices`) equals its own formula, which uses (S - 1)/S where Chao's has (T - 1)/T"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r, image: "eprp-sw/bench-r:t1 (sha256:926c0052…); tranche 4 in eprp-sw/bench-r4:t4 (sha256:d0c1c51a…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-038]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026, findings applied; tranche-4 additions not yet reviewed"}
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
tolerance 5%): **pass**. With no part-timers or gap-fillers, all the
formulas reduce to the same extinction and origination values, so this is
one check of each. The sampled-arm figures are a characterisation (no
tolerance was declared), not a validation. The raw three-timer carries the
log of the three-timer sampling probability by design (here about
log(1/0.39)); the corrected form removes it.

**Richness (tranche 4,
[bench/VALIDATION_T4.md](../bench/VALIDATION_T4.md)).** Spatially
structured records from an independent generator (8 areas, contiguous
ranges, lognormal abundances, Poisson collections of 40 individuals; known
richness per bin), 20 replicates per scenario. Bias is the log ratio of
mean estimates in bins 11–20 to bins 1–10, minus the true log ratio.

| Test | Result |
| --- | --- |
| K1: `indices(method = "squares")` against Alroy's (2018) formula, 1,200 bins | identical (difference 0): **pass** |
| K2: SQS (`subsample(type = "sqs", q = 0.6)`, 100 iterations) when effort falls 70% at constant evenness (scenario S) | **not met as declared**: in one replicate two bins (4 and 7 collections, Good's u 0.16 and 0.54) cannot reach the quorum and return NA, so the declared mean does not exist. Post hoc: **+0.034** (SE 0.014) over the 19 complete replicates, +0.035 using only bins that reach the quorum |
| SQS when only evenness changes (scenario E; σ of log abundance 0.5 → 2) | **−0.70** (SE 0.025): true richness flat, SQS reports half |
| K5 (amendment A5): SQS when collections shrink from 40 to 12 individuals at constant number (scenario C) | **−0.121** (SE 0.014) against ±0.10: **fail** |
| SQS evenness dose–response (A5): late-half σ 0.75, 1.0, 1.5, 2.0 | −0.07, −0.17, −0.41, −0.70 |
| Squares; Chao2 under the collection-size fall; under the evenness doses | −0.12, −0.15; squares −0.01, −0.04, −0.15, −0.31 and Chao2 −0.01, −0.04, −0.16, −0.31 |
| Squares; Chao2 (`indices`) under the effort fall | −0.15, −0.15 (raw richness −0.37, range-through −0.27) |
| Squares; Chao2 under the evenness change | −0.31, −0.31 (raw −0.49) |
| Mass extinction at 50 Ma (true drop −0.78 in log richness, bins 11–12 against 9–10) | squares −0.74, Chao2 −0.74, SQS −0.67, raw −0.68 |
| Squares and Chao2 against true richness (median absolute log error) | 0.17–0.36 against global richness, 0.09–0.18 against richness in the sampled areas; both underestimate (mean log ratio −0.19 to −0.35) |
| K3: `indices` Chao2 against an independent implementation of its formula | equal to 5 × 10⁻¹³; against iNEXT's Chao2, a median −0.2% (range −1.9% to +9.4%) |

## Strengths

- Exact under complete sampling; in our characterisation the corrected
  three-timer and gap-filler rates were within 2% under homogeneous
  sampling at a 39% per-bin sampling probability. With standard errors
  taken across replicates (adjacent bins share data;
  `bench/results/e1/e1_divdyn_se.json`), the corrected three-timer is
  within 1 SE of the truth, while the gap-filler's +1.5% (extinction) and
  +1.0% (origination) are about 2 SE, so a small bias is possible.
- One function returns every standard rate, so estimators can be compared
  on identical counts.

## Weaknesses and pitfalls

- **Second-for-third rates (`ext2f3`, `ori2f3`) were 36% low** under
  homogeneous Poisson sampling in continuous time. divDyn substitutes the
  middle value of the three subsequent-sampling counts (`sort(y)[2]`), and
  its source comment says this follows Alroy's (2015) rule. The cause is
  open; one untested candidate is that continuous turnover within bins and
  constant per-time sampling violate the method's assumptions. Treat these
  columns as unvalidated under such conditions.
- `ext3t`/`ori3t` are the raw rates; use `extC3t`/`oriC3t` or the
  gap-filler rates for estimates.
- The boundary-crosser extinction rate was 7.9% high under sampling
  (origination +0.2%); our reading is that sampled ranges end early (range
  truncation), which boundary-crosser rates do not correct.
- **SQS stops on integer taxon IDs** with "missing value where TRUE/FALSE
  needed" (`subsample(type = "sqs")`); character names work. **`indices()`
  reads a numeric vector as abundances**, so integer taxon IDs passed as
  the occurrence vector give silently wrong values. Pass taxa as character.
- `indices()` returns its columns in its own order (squares before
  chao2) whatever order `method` lists; index the result by name.
- **Chao2 uses (S − 1)/S where Chao's incidence estimator has (T − 1)/T**
  (`Chao2Method`; S observed species, T sampling units). The difference
  from the bias-corrected Chao2 with (T − 1)/T was a median +0.14% here but
  +25% in a bin with 4 collections (Spearman ρ 0.82 with 1/T). It matters
  only for thinly sampled bins.
- SQS returns NA where a bin cannot reach the quorum (`useFailed = FALSE`),
  with no warning or message: safer than a number, but downstream means
  need explicit handling.
- **SQS responds to evenness, by degrees.** Under a pure evenness change
  it halved a flat richness curve (−0.70), as did iNEXT's coverage estimate
  (−0.76), and a modest change (σ 0.5 to 1) already gave −0.17; see
  [inext](../inext/README.md) and lead L-006.
- **SQS corrects fewer collections but not smaller ones**: +0.03 when
  collections fell 70% in number, −0.12 (K5 fail) when they kept their
  number and shrank to a third of their size.
- Licence metadata conflict: CRAN says CC BY 4.0, the repository GPL-3.0.
- Rates are per bin; unequal bin durations need explicit handling.

## Alternatives and overlap

palaeoverse covers preparation and binning but not these rates. PyRate
estimates rates in continuous time with preservation modelled. `squares`
and SQS implementations elsewhere cover richness, not rates.

## EPRP relevance

Stage-level rates for Q-040, Q-042 and Q-038 style analyses; the shared
counting makes it the natural engine for an estimator comparison (lead
N-002). Its SQS absorbed a fall in collection numbers (+0.03) but not a
fall in collection size (−0.12) or an evenness change (−0.70; tranche 4,
lead L-006). Alroy's geometric Weibull did better on all three
([alroy-richness](../alroy-richness/README.md)). Squares and Chao2
recovered 70–83% of global richness on these records (partly a matter of
definition: global richness counts every species alive at any time in a
bin).

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
- 2026-10-24 `checked`: `Chao2Method` and `squaresMethod` read from the
  installed 0.8.3 namespace; tranche-4 K1, K2, K3 and characterisation on
  `deep-server` (`bench/results/t4/`).
