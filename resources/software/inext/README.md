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
validated_uses: ["estimateD coverage-standardised richness (incidence, q = 0): within ±0.10 (+0.026) of the truth's trend when collections fall 70% at constant evenness", "ChaoRichness incidence Chao2 reproduced by an independent implementation"]
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
| K5 (amendment A5): collections keep their number but shrink from 40 to 12 individuals at bin 11 (scenario C) | bias **−0.125** (SE 0.015) against ±0.10: **fail** |
| Evenness dose–response (A5): late-half σ 0.75, 1.0, 1.5, 2.0 | −0.08, −0.19, −0.45, −0.76 |
| Mass extinction at 50 Ma (scenario M; true drop −0.78 in log richness, bins 11–12 against 9–10) | iNEXT drop −0.67 (SE 0.02): 0.11 too shallow |
| K3: `ChaoRichness` against an independent implementation of its formula, S + (T − 1)/T · f₁²/(2f₂) | equal to 5 × 10⁻⁴ (iNEXT rounds to three decimals) |

## Strengths

- When the number of collections fell 70% at constant evenness, the
  coverage estimate moved +0.03, where raw richness fell 0.37 and Chao2
  0.15.
- Interpolation and extrapolation share one framework, with analytical
  and bootstrap intervals.
- Warns when an extrapolation runs past twice the reference sample.

## Weaknesses and pitfalls

- **Coverage standardisation responds to evenness.** With true richness
  flat and only the abundance distribution becoming uneven, the coverage
  estimate fell by 0.76 in log units, more than raw richness (−0.49) or
  Chao2 (−0.31). The dose–response is a slope, not a cliff: −0.08, −0.19,
  −0.45 and −0.76 as the late-half σ rose from the early 0.5 to 0.75, 1,
  1.5 and 2, so a modest change in dominance already exceeds ±0.10. This is
  at coverage 0.6, a strong rarefaction of samples with native coverage
  0.85–0.97. At 0.8 (A6) it was smaller but of the same kind (−0.05, −0.14,
  −0.35, −0.63), and a no-change control stayed within 0.01 (K6 pass). Equal coverage is not equal completeness of the
  species list when dominance changes. Alroy (2026; [LEADS](../LEADS.md)
  L-006) concludes from different tests (excluding dominants, pooling,
  singleton-matched pairs) that coverage-based rarefaction does not track
  richness; this result is consistent with that conclusion. Do not read
  coverage-standardised values as relative richness where evenness may
  differ between bins.
- **The effort correction depends on how effort falls.** Fewer
  collections of the same size: +0.03. The same number of collections,
  each a third the size: −0.13 (K5 fail, about 1.5 SE beyond ±0.10,
  still removing about 60% of raw richness's −0.33; −0.08 at coverage 0.8,
  where low-effort bins then extrapolate). Our reading, untested: smaller
  collections change the shape of the incidence-frequency distribution,
  not only its total.
  Lower preservation was not tested.
- **Extrapolation does not fail; it warns.** In a bin with 4 collections
  (sample coverage 0.20), `estimateD` extrapolated to 18 units (4.5× the
  sample) and returned 281 species from 86 observed, with the warning "the
  results for q = 0 may be subject to large prediction bias". divDyn's SQS
  returns NA in the same bin, with no warning. Inside `parallel::mclapply` or a loop the
  warning is easily lost: check `t / T` in the output and drop bins beyond
  2.
- `estimateD` returns rows by assemblage name; match on `Assemblage`
  rather than relying on input order.
- The bootstrap (`nboot`, default 50) dominates run time; we used
  `nboot = 0` and did not test the intervals.

## Alternatives and overlap

divDyn's SQS standardises to the same kind of coverage (Good's u, on
occurrences) by subsampling rather than by interpolation. On these data
SQS ran 2–5% below iNEXT on average, except in the uneven late bins of
scenario E (1% above), and the two responded alike to effort (+0.03 each) and to
evenness (−0.70 against −0.76). Alroy's geometric Weibull (his CEGS
model, on our inference), which he prefers to both, moved −0.12 under the
strongest evenness change and +0.09 under the collection-size fall when
fitted to the same occurrence frequencies, on this generator
([alroy-richness](../alroy-richness/README.md)). Squares and Chao2 extrapolate to an asymptote
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
