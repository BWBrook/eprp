---
id: alroy-richness
name: richness (Alroy)
kind: r-package
domain: diversity-rates
languages: [R]
home: https://github.com/johnalroy/richness
repo: https://github.com/johnalroy/richness
paper: [10.22541/au.173279215.54394439/v1, 10.1002/oik.11607]
licence: "CC0-1.0 (repository LICENSE); GPL-2 | GPL-3 (DESCRIPTION): conflicting"
release: {version: "v.3.2 (commit 5dd4506; DESCRIPTION says 3.1)", date: 2025-06-14, checked: 2026-10-24}
maintenance: {state: slow, last_commit: 2025-06-14, checked: 2026-10-24}
tier: T2
validated_uses: ["cegsML and cegsLD recover richness on counts drawn from their own model (K4)"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r4gw, image: "eprp-sw/bench-r4gw:t4 (sha256:51a21c04…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-044, B-015]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: not yet}
---

# richness (Alroy)

## Summary

John Alroy's R package of species-abundance distributions and richness
estimators: the compound exponential-geometric series (CEGS; `cegsML`,
`cegsB`, `cegsLD`), Chao 1 and 2, jackknives, the discrete Weibull, the
Poisson log normal, SQS, rarefaction, Fisher's α and random generators.
CEGS is, on our reading, the "geometric Weibull" that Alroy (2026) found
more accurate than coverage-based rarefaction. Reach for `cegsML` on a
bin's occurrence frequencies when absolute richness, or a trend that
survives changes in evenness, is the target. On the tranche-4 records it
was the most accurate estimator we ran.

## Method

Each species' count is geometric with p = 1 / (E^γ / λ + 1), E
exponential: a geometric series whose mean, E^γ/λ, is a Weibull variate.
The two parameters are fitted to the observed counts by maximum likelihood
(`cegsML`, `stats4::mle`, integrating over E), by a Bayesian grid with an
exponential prior (`cegsB`) or by a likelihood-weighted grid without a
prior (`cegsLD`). Richness is the observed count divided by the fitted
probability of being seen at least once, S / (1 − P(X = 0)). The 2024
preprint parameterises the mean as E/λ raised to 1/γ; v.3.2 uses
(−ln U)^γ/λ. That this is the 2026 paper's geometric Weibull is our
inference from the code and the abstract's list of tested distributions;
the 2026 paper's own code was not seen.

## Install

Not on CRAN. `remotes::install_github("johnalroy/richness", ref =
"5dd45069370378620e6c7843bfe49a8dc91b02ba")` (tag v.3.2) with minpack.lm,
poilog and sads from CRAN, on top of the tranche-4 R image
([Dockerfile](../bench/env/Dockerfile.r4gw)). The functions call
`library(stats4)` internally, so they attach it.

## Validation

[bench/VALIDATION_T4.md](../bench/VALIDATION_T4.md), amendment A5, declared
before running.

**K4: the package under its own model (pass).** 300 species with counts
from `rcegs`; 100 draws per parameter set
(`bench/results/t4/t4_gw_k4.json`).

| (λ, γ) | Species observed | `cegsML` median log(R̂/R) (IQR) | `cegsLD` | Failed fits |
| --- | --- | --- | --- | --- |
| (1, 2) | 38% | −0.026 (0.37) | +0.037 (0.33) | 0 |
| (0.1, 1) | 79% | −0.010 (0.07) | −0.008 (0.07) | 0 |

**On the tranche-4 records (characterisation, no criterion).** Records
from an independent generator with lognormal abundances, a different
family from the model's own, in eight areas; 20 replicates per scenario.
Bias is the error in the log ratio of the late half to the early half (0
is perfect); the mass-extinction column is the error in the drop at
50 Ma.

| `cegsML` input | Fewer collections (S) | Smaller collections (C) | Evenness σ 0.5 → 0.75, 1, 1.5, 2 | Mass extinction | Median absolute log error against global richness |
| --- | --- | --- | --- | --- | --- |
| occurrence frequencies (collections per species) | +0.03 | +0.09 | −0.01, −0.02, −0.06, −0.12 | −0.02 | 0.06–0.10 |
| individual counts pooled per bin | +0.06 | +0.11 | +0.03, +0.07, +0.21, +0.46 | −0.05 | 0.06–0.15 |

For comparison, under the same σ steps SQS moved −0.07, −0.17, −0.41,
−0.70 and Chao2 −0.01, −0.04, −0.16, −0.31; Chao2's absolute error was
0.14–0.31. `cegsLD` gave the same picture where run (S, E, M).

## Strengths

- On occurrence frequencies, it was the only estimator within ±0.12 in
  every scenario, and it recovered 90–98% of global richness (mean log
  ratio −0.02 to −0.10 across the seven scenarios), where Chao2 and squares
  recovered 70–85%.
- It tracked a 54% mass-extinction drop to within 0.02 log units.
- Fits are fast enough for per-bin use: about 1–2 s per bin for
  `cegsML`, 8–15 s for `cegsLD` or `cegsB`.

## Weaknesses and pitfalls

- **Pooled individual counts overshoot when evenness falls**: +0.46 at
  σ 2, against −0.12 on occurrence frequencies of the same records. One
  candidate cause, untested, is that pooling counts across spatially
  clumped collections violates the single-community model.
- **Imprecise when most species are unseen**: in K4, with 38% of species
  observed, the interquartile range of log(R̂/R) was 0.37.
- `cegsML` returns NA when a sample has fewer than three distinct counts
  or the fit reaches its parameter bounds, without a warning: 4 of 400
  bins in scenario S (the thinnest). `cegsLD` failed none.
- Licence metadata conflict (CC0-1.0 against GPL-2 | GPL-3), and the
  DESCRIPTION version (3.1) lags the tag (v.3.2). Not on CRAN; pin the
  commit.
- One generator family was tested. The result supports Alroy's (2026)
  recommendation on known truth, but does not show the method's accuracy
  on records whose structure differs from ours.

## Alternatives and overlap

divDyn and iNEXT give Chao2, squares and coverage-standardised richness
([divdyn](../divdyn/README.md), [inext](../inext/README.md)); this package
offers those too (`chao2`, `sqs`), untested here. `ecodive` and `tabula`
implement squares. DeepDive estimates total richness by simulation-based
inference ([deepdive](../deepdive/README.md)). Alroy's older scripts
(`sqs.R`, `fitDistributions.R`; landscape row `alroy-scripts`) predate
CEGS.

## EPRP relevance

The strongest single-estimator candidate for per-bin richness in Q-040 and
Q-042 analyses, used on occurrence frequencies and alongside an estimator
that fails differently (lead N-002). Lead L-006: the comparison with
coverage rarefaction now runs both ways on known truth.

## Citation and licence

Alroy, J. (2024). Species richness and abundance can be predicted
accurately. Preprint, Authorea. doi:10.22541/au.173279215.54394439/v1.
Alroy, J. (2026). Coverage-based rarefaction fails to quantify relative
species richness. *Oikos*. doi:10.1002/oik.11607 (both checked on
Crossref, 24 October 2026; the 2026 article was read in abstract only).
Code: CC0-1.0 per the repository's LICENSE; GPL-2 | GPL-3 per its
DESCRIPTION.

## Verification log

- 2026-10-24 `checked`: repository, releases, licence files and
  DESCRIPTION through the GitHub API; `cegsML.R`, `cegsLD.R`, `rcegs.R` read
  at tag v.3.2; the 2024 preprint's methods read.
- 2026-10-24 `checked`: K4 and the tranche-4 characterisation on
  `deep-server` (`bench/results/t4/`).
- 2026-10-24 `inferred`: CEGS v.3.x is the 2026 paper's geometric Weibull.
