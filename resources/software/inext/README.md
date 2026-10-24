---
id: inext
name: iNEXT
kind: r-package
domain: diversity-rates
languages: [R, C++]
home: https://cran.r-project.org/package=iNEXT
repo: https://github.com/JohnsonHsieh/iNEXT
paper: [10.1111/2041-210x.12613, 10.1890/13-0133.1, 10.1890/11-1952.1]
licence: GPL (>= 3)
release: {version: 3.0.2, date: 2025-07-30, checked: 2026-10-23}
maintenance: {state: slow, last_commit: 2025-07-30, checked: 2026-10-23}
tier: T2
validated_uses: ["estimateD coverage-standardised richness (incidence, q = 0): unbiased under a 70% fall in sampling effort at constant evenness", "ChaoRichness incidence Chao2 reproduced by an independent implementation"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r4, image: "eprp-sw/bench-r4:t4 (sha256:d0c1c51a…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-027, Q-025, Q-044, B-015]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: not yet}
---

# iNEXT

## Summary

iNEXT interpolates and extrapolates Hill-number diversity (richness, q = 0;
Shannon, q = 1; Simpson, q = 2) by sample size or by sample coverage, from
abundance or incidence data, and gives the Chao asymptotic estimators. In
palaeobiology it is the engine of coverage-standardised richness in the
Benson and Close pipelines and in divvy. Reach for `estimateD(base =
"coverage")` to compare bins at equal coverage when only sampling effort
differs between them.

## Method

Coverage is the estimated fraction of the assemblage's individuals (or
incidences) belonging to species already sampled (Chao and Jost 2012).
`estimateD` rarefies or extrapolates each assemblage to a common coverage,
using the sample-size-based curves of Chao et al. (2014); for q = 0
extrapolation it uses the Chao1 or Chao2 asymptote. With
`datatype = "incidence_freq"` each assemblage is a vector `c(T, Y_1, …)`:
the number of sampling units (here collections) and each species' number
of occupied units. A time bin is treated as one assemblage sampled by
independent units, an assumption to state when collections cluster in
space.

## Install

CRAN 3.0.2 from the Posit snapshot of 2026-10-22 in the tranche-4 R image
([Dockerfile](../bench/env/Dockerfile.r4)).

## Validation

Tranche 4 ([bench/VALIDATION_T4.md](../bench/VALIDATION_T4.md)): records
from an independent generator (paleobuddy birth–death, 8 areas, contiguous
ranges, lognormal abundances, Poisson collections of 40 individuals;
known richness per bin), 20 replicates per scenario. Coverage level 0.6,
q = 0, incidence frequencies per bin. The bias is the log ratio of mean
estimates in the late half (bins 11–20) to the early half, minus the true
log ratio.

| Test | Result |
| --- | --- |
| K2: effort falls 70% at bin 11, evenness fixed (scenario S) | bias **+0.026** (SE 0.016) against ±0.10: **pass**. Post hoc, without replicate 10 (two near-empty bins): +0.019 |
| Evenness falls at bin 11, effort fixed (scenario E; σ of log abundance 0.5 → 2) | bias **−0.76** (SE 0.027): true richness flat, iNEXT reports less than half. Characterisation, no criterion |
| Mass extinction at 50 Ma (scenario M; true drop −0.78 in log richness, bins 11–12 against 9–10) | iNEXT drop −0.67 (SE 0.02): 0.11 too shallow |
| K3: `ChaoRichness` against an independent implementation of its formula, S + (T − 1)/T · f₁²/(2f₂) | equal to 5 × 10⁻⁴ (iNEXT rounds to three decimals) |

## Strengths

- Under a change of sampling effort alone, coverage standardisation did
  what it is designed to do, where raw richness fell 0.37 and Chao2 0.15.
- Interpolation and extrapolation share one framework, with analytical
  and bootstrap intervals.
- Warns when an extrapolation runs past twice the reference sample.

## Weaknesses and pitfalls

- **Coverage standardisation responds to evenness.** With true richness
  flat and only the abundance distribution becoming uneven, the coverage
  estimate fell by 0.76 in log units, more than raw richness (−0.49) or
  Chao2 (−0.31). Equal coverage is not equal completeness of the species
  list when dominance changes. This is the substance of Alroy's (2026)
  critique ([LEADS](../LEADS.md) L-006); do not read coverage-standardised
  values as relative richness where evenness may differ between bins.
- **Extrapolation does not fail; it warns.** In a bin with 4 collections
  (sample coverage 0.20), `estimateD` extrapolated to 18 units (4.5× the
  sample) and returned 281 species from 86 observed, with the warning "the
  results for q = 0 may be subject to large prediction bias". divDyn's SQS
  returns NA in the same bin. Inside `parallel::mclapply` or a loop the
  warning is easily lost: check `t / T` in the output and drop bins beyond
  2.
- `estimateD` returns rows by assemblage name; match on `Assemblage`
  rather than relying on input order.
- The bootstrap (`nboot`, default 50) dominates run time; we used
  `nboot = 0` and did not test the intervals.

## Alternatives and overlap

divDyn's SQS standardises to the same kind of coverage (Good's u, on
occurrences) by subsampling rather than by interpolation; on these data
the two agreed in every scenario (K2 effort: +0.03 for both; evenness:
−0.70 against −0.76). Squares and Chao2 extrapolate to an asymptote
instead; they were less affected by the evenness change but biased by the
effort change. DeepDive targets total richness by simulation-based
inference ([deepdive](../deepdive/README.md)). divvy adds spatial
standardisation before iNEXT.

## EPRP relevance

Coverage-standardised curves underpin Q-040 and Q-042 style comparisons
and the Benson pipeline (Q-027, B-015). The evenness result means any such
comparison across a change in community structure (a mass extinction with
a shift in dominance, a radiation) needs a second estimator that responds
differently, which is what lead N-002 proposes.

## Citation and licence

Hsieh, T. C., Ma, K. H. and Chao, A. (2016). iNEXT: an R package for
rarefaction and extrapolation of species diversity (Hill numbers).
*Methods in Ecology and Evolution* 7, 1451–1456. doi:10.1111/2041-210X.12613.
Chao, A. et al. (2014). Rarefaction and extrapolation with Hill numbers.
*Ecological Monographs* 84, 45–67. doi:10.1890/13-0133.1. Chao, A. and
Jost, L. (2012). Coverage-based rarefaction and extrapolation.
*Ecology* 93, 2533–2547. doi:10.1890/11-1952.1. DOIs as verified in the
landscape scan. GPL (≥ 3).

## Verification log

- 2026-10-23 `checked`: CRAN 3.0.2 (2025-07-30) by `landscape.py`.
- 2026-10-24 `checked`: K2, K3 and the scenario E and M characterisation
  on `deep-server` (`bench/results/t4/`); the extrapolation warning
  reproduced on replicate 10, bin 17 of scenario S.
