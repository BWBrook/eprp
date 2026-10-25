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
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
---

# richness (Alroy)

## Summary

John Alroy's R package of species-abundance distributions and richness
estimators: the compound exponential-geometric series (CEGS; `cegsML`,
`cegsB`, `cegsLD`), Chao 1 and 2, jackknives, the discrete Weibull, the
Poisson log normal, SQS, rarefaction, Fisher's α and random generators. We
take its v.3.x CEGS to be the "geometric Weibull" that Alroy (2026) found
more accurate than coverage-based rarefaction; that is our inference. On
the tranche-4 records, `cegsML` fitted to a bin's occurrence frequencies
had the lowest absolute error of the estimators we ran, with a trend
bias inside ±0.10 except under the strongest evenness change. Use it
alongside an estimator that fails differently, not alone.

## Method

Each species' count is geometric, and its mean varies among species. In
the 2024 preprint and in v.3.0 the mean is (E/λ + 1)^(1/γ) − 1 with E
exponential; v.3.2 uses E^γ/λ, which is a Weibull variate, so v.3.2's
model is a geometric series with Weibull-distributed means. That fits the
2026 paper's name, and the paper's abstract lists the geometric Weibull
beside a separate discretised Weibull, as the package has both; the 2026
paper's own code was not seen. The two parameters are fitted by maximum
likelihood (`cegsML`, `stats4::mle`, integrating over E), by a Bayesian
grid with an exponential prior that weights each grid cell by its
likelihood (`cegsB`), or by a grid without a prior that weights each cell
by the product of absolute differences between neighbouring likelihoods,
a gradient-style weight (`cegsLD`). Richness is the observed count over the
fitted probability of being seen at least once, S / (1 − P(X = 0)).

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
(`bench/results/t4/t4_gw_k4.json`). The criterion is on the median only,
and on counts only; there is no occurrence-frequency analogue.

| (λ, γ) | Species observed | `cegsML` median log(R̂/R) (IQR) | `cegsLD` | Failed fits |
| --- | --- | --- | --- | --- |
| (1, 2) | 38% | −0.026 (0.37) | +0.037 (0.33) | 0 |
| (0.1, 1) | 79% | −0.010 (0.07) | −0.008 (0.07) | 0 |

**On the tranche-4 records (characterisation, no criterion).** Records
from an independent generator with lognormal abundances, a different
family from the model's own, in eight areas; 20 replicates per scenario,
23–100 collections per bin. Bias is the error in the log ratio of the late
half to the early half (0 is perfect); the mass-extinction column is the
error in the drop at 50 Ma.

| `cegsML` input | Fewer collections (S) | Smaller collections (C) | Late evenness σ 0.75, 1, 1.5, 2 (early 0.5) | Mass extinction | Median abs. log error: sampled-area; global richness |
| --- | --- | --- | --- | --- | --- |
| occurrence frequencies (collections per species) | +0.03 | +0.09 | −0.01, −0.02, −0.06, −0.12 | −0.01 | 0.04–0.08; 0.06–0.10 |
| individual counts pooled per bin | +0.06 | +0.11 | +0.03, +0.07, +0.21, +0.46 | −0.05 | –; 0.06–0.15 |

For comparison, at the same σ steps SQS moved −0.07, −0.17, −0.41, −0.70
and Chao2 −0.01, −0.04, −0.16, −0.31; Chao2's errors were 0.06–0.15
against sampled-area and 0.14–0.31 against global richness. `cegsLD` gave
the same picture where run (S, E, M).

**Robustness (amendment A6, declared; 20 replicates per condition,
scenario S's effort fall).** Abundances from gamma(0.25), log-uniform or
Pareto distributions, or lognormal with variable collection sizes, at
about 77 or 30 collections per bin early (`bench/results/t4/t4_rob.json`):

| Condition | Median abs. log error vs sampled-area: `cegsML`; Chao2 | `cegsML` closer than Chao2 | `cegsML` trend bias | Failed `cegsML` fits (of 400 bins) |
| --- | --- | --- | --- | --- |
| lognormal (S itself) | 0.064; 0.143 | 77% | +0.03 | 4 |
| lognormal, low effort | 0.091; 0.211 | 69% | −0.05 | 112 |
| variable collection sizes | 0.068; 0.142 | 72% | +0.06 | 12 |
| variable sizes, low effort | 0.111; 0.239 | 66% | +0.04 | 124 |
| gamma(0.25) | 0.403; 0.575 | 99% | −0.10 | 1 |
| gamma, low effort | 0.428; 0.662 | 98% | −0.11 | 103 |
| log-uniform | 0.139; 0.318 | 97% | −0.11 | 2 |
| log-uniform, low effort | 0.195; 0.432 | 95% | −0.10 | 87 |
| Pareto (α = 1) | 0.185; 0.200 | 52% | +0.04 | 9 |
| Pareto, low effort | 0.215; 0.313 | 61% | **−0.47** | 97 |

## Strengths

- Among estimators run in every scenario, the only one whose trend bias
  stayed within ±0.12; within the declared ±0.10 everywhere except the
  strongest evenness change (−0.118, SE 0.021).
- The lowest absolute error against sampled-area richness on the main
  scenarios (0.036–0.077, closer than Chao2 in 49–80% of bins), lower than
  Chao2's in all ten robustness conditions, and it tracked a 54%
  mass-extinction drop to within 0.015 log units.
- Fast enough for per-bin use: about 1.6 s per bin for `cegsML`, 13 s for
  `cegsLD` (`cegsB` not timed on these records).

## Weaknesses and pitfalls

- **Overshoots the identifiable target.** Its 90–98% recovery of global
  richness comes partly from overshooting richness in the sampled areas by
  3–10%; global richness here includes 9–11% of species living only in
  unsampled areas.
- **Pooled individual counts overshoot when evenness falls**: +0.46 at
  σ 2 (late-half median ratio 1.38). One candidate cause, untested, is
  that pooling counts across spatially clumped collections violates the
  single-community model; it is a stress test, not the method's intended
  use.
- **Imprecise when most species are unseen**: in K4, with 38% of species
  observed, the interquartile range of log(R̂/R) was 0.37.
- **Fits fail silently in thin bins.** `cegsML` returns NA when a sample
  has fewer than three distinct counts or the fit reaches its parameter
  bounds: 4 of the 400 bins of scenario S, all with 14 or fewer
  collections, and 22–31% of bins at about 9 collections (A6). `cegsLD`
  failed none in our run.
- **Accuracy depends on the abundance distribution.** Under
  log-series-like (gamma 0.25) abundances it underestimated sampled-area
  richness by about a third (median log ratio −0.40; Chao2 −0.58), under
  Pareto abundances it overestimated it (+0.18, where Chao2 was −0.20),
  and under Pareto abundances at low effort its trend bias was −0.47.
- Occurrence frequencies are bounded by the number of collections and
  saturate for common species; using them as counts is a heuristic we have
  not validated beyond these records.
- Licence metadata conflict (CC0-1.0 against GPL-2 | GPL-3), and the
  DESCRIPTION version (3.1) lags the tag (v.3.2). Not on CRAN; pin the
  commit.

## Alternatives and overlap

divDyn and iNEXT give Chao2, squares and coverage-standardised richness
([divdyn](../divdyn/README.md), [inext](../inext/README.md)); this package
offers those too (`chao2`, `sqs`), untested here. `ecodive` and `tabula`
implement squares. DeepDive estimates total richness by simulation-based
inference ([deepdive](../deepdive/README.md)). Alroy's older scripts
(`sqs.R`, `fitDistributions.R`; landscape row `alroy-scripts`) predate
CEGS.

## EPRP relevance

A strong per-bin richness candidate for Q-040 and Q-042 analyses when used
on occurrence frequencies, beside an estimator that fails differently
(lead N-002), and with its fit failures reported. These results are not a
test of Alroy's (2026) method as published: the input that worked is not
the paper's, and which variant the paper used is unknown (CONTACTS S2).
Next: an occurrence-frequency analogue of K4 with heterogeneous
collection sizes and a fit-adequacy check.

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
  DESCRIPTION through the GitHub API; `cegsML.R`, `cegsLD.R`, `cegsB.R` and
  `rcegs.R` read at tag v.3.2 (and `cegsML.R` at v.3.0 by the reviewer);
  the 2024 preprint's methods read.
- 2026-10-24 `checked`: K4 and the tranche-4 characterisation on
  `deep-server` (`bench/results/t4/`); headline numbers recomputed
  independently by the reviewer.
- 2026-10-24 `inferred`: CEGS v.3.x is the 2026 paper's geometric Weibull.
