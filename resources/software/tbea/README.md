---
id: tbea
name: tbea (stratCI)
kind: r-package
domain: extinction-timing
languages: [R]
home: https://cran.r-project.org/package=tbea
repo: https://github.com/gaballench/tbea
paper: []
licence: GPL-3
release: {version: 1.8.0, date: 2026-09-06, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-09-06, checked: 2026-10-24}
tier: T2
validated_uses: ["stratCI Strauss-Sadler (1989) one-endpoint 95% bound under homogeneous sampling"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["Marshall (1994) bracket needs at least 73 fossils at quantile 0.95"]
related_sources: []
eprp_questions: [Q-013, Q-017, Q-034, Q-041]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# tbea (stratCI)

## Summary

tbea's `stratCI` gives confidence intervals on stratigraphic range
endpoints by Strauss & Sadler (1989; one or two endpoints) and by
Marshall's (1994) distribution-free method; only `stratCI` was examined
here.

## Method

Strauss–Sadler one endpoint: the bound extends the observed range R by
R[(1 − C)^{−1/(n−1)} − 1], exact when fossils are uniform over the range.
Marshall 1994: last occurrence plus an order-statistic bracket of the
observed gap sizes at a chosen quantile and confidence.

## Validation

E4 in [bench/VALIDATION_T2.md](../bench/VALIDATION_T2.md), 2,000 species:

| Arm | Strauss–Sadler coverage |
| --- | --- |
| A: homogeneous Poisson fossils | **0.948** (pass; band 0.937–0.962), by fossil count 0.950 / 0.941 / 0.952 |
| B: six 2-Myr hiatuses | 0.884 (0.943 away from hiatuses; 0.829 when the extinction falls in one; 0.838 within 1 Myr after one) |
| C: 0.25-Myr dating error | 0.938 |

Cross-check with EDE's `strauss1989`: identical on the same discretised
input in 97.35% of cases; the rest differ by EDE's use of distinct sighting
times (see [EDE](../ede/README.md)).

## Weaknesses and pitfalls

- **Marshall (1994) returned no bound for any case.** Its upper bracket at
  quantile 0.95 and confidence 0.95 exists only when 0.95^N < 0.025 for N
  gaps (at least 72 gaps); the largest record had 30 fossils. The function
  warns and returns a single value, not an error.
- `endpoint = "first"` is the larger value and `"last"` the smaller: with
  ages (older = larger), `"last"` is the extinction end; with forward time,
  `"first"`.
- Strauss–Sadler assumes uniform recovery; hiatuses near the extinction
  cut coverage to about 0.83.

## Citation and licence

Strauss, D. and Sadler, P. M. (1989). Classical confidence intervals and
Bayesian probability estimates for ends of local taxon ranges.
*Mathematical Geology* 21, 411–427. doi:10.1007/bf00897326 (checked on
Crossref). tbea's own paper not checked here. GPL-3.

## Verification log

- 2026-10-24 `checked`: E4–E6 on `deep-server`; `R/stratCI.R` read on
  GitHub (`master`).
