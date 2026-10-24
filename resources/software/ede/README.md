---
id: ede
name: EDE
kind: r-package
domain: extinction-timing
languages: [R]
home: https://cran.r-project.org/package=EDE
repo: https://github.com/rodrigosqrt3/EDE
paper: [10.1007/bf00897326, 10.1038/426245a, 10.2307/1940821]
licence: GPL (>= 3)
release: {version: 0.2.0, date: 2026-09-21, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-09-23, checked: 2026-10-24}
tier: T2
validated_uses: ["strauss1989 one-sided 95% bound under homogeneous sampling"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [Q-013, Q-017, Q-034, Q-041]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# EDE

## Summary

EDE (new on CRAN in 2026) estimates extinction dates from sighting
records: eleven procedures under one interface, including Strauss & Sadler
(1989), Robson & Whitlock (1964), optimal linear estimation (Roberts &
Solow 2003), Solow (1993, 2005), McInerny et al. (2006), Burgman et al.
(1995) and reliability-adjusted variants. Input is a table of sighting
counts per time unit in forward time.

## Validation

E4–E6 in [bench/VALIDATION_T2.md](../bench/VALIDATION_T2.md), 2,000 species,
sightings in 0.01-Myr units, the present as `test_year`. Coverage of the
true extinction time:

| Method | A: ideal | B: hiatuses | C: dating error |
| --- | --- | --- | --- |
| `strauss1989` (one-sided 95%) | **0.950** (pass) | 0.886 | 0.939 |
| `robson1964` (one-sided 95%) | 0.955 | 0.921 | 0.946 |
| `ole` (two-sided 95%) | 0.610 | 0.496 | 0.591 |
| `solow1993` estimate as a bound, scored cases / post hoc with missing estimates as "not inferred extinct" | 0.933 / 0.950 | 0.831 / 0.886 | 0.918 / 0.939 |
| `mcinerny2006`, same | 0.866 / 0.886 | 0.701 | 0.849 |
| `burgman1995`, same | 0.752 / 0.850 | 0.523 | 0.754 |

Missing estimates for the three persistence tests come from species whose
last fossil is close to the present (median 1.4–3.2 Myr, against
8.5–10.8 Myr for scored cases): the test never rejects persistence before
`test_year`.

## Strengths

- One interface over many methods; fast (pure R).
- Strauss–Sadler, Robson–Whitlock and (read correctly) Solow 1993 are
  calibrated under homogeneous sampling.

## Weaknesses and pitfalls

- **OLE's 95% interval undercovers badly** on records of 3–30 fossils:
  0.42 with 3–5 fossils, 0.81 with 6–10, 0.89 above 10.
- McInerny and Burgman estimates, read as α = 0.05 inference dates, are
  anti-conservative (0.87, 0.75 in arm A).
- **`strauss1989` counts distinct sighting times** (`unique()` in its
  source), so sightings sharing a time unit count once. That makes the
  bound wider than the sighting-count formula when units are coarse; on
  our 0.01-Myr units it changed 53 of 2,000 bounds against `tbea`.
- A persistence test that never rejects before `test_year` returns `NA`
  with a warning, not a bound beyond the present.
- New package (repository created July 2026); no published validation
  found.

## Citation and licence

Cite the methods' original papers (for example Strauss & Sadler 1989,
doi:10.1007/bf00897326; Roberts & Solow 2003, doi:10.1038/426245a; Solow
1993, doi:10.2307/1940821; all checked on Crossref). GPL (≥ 3).

## Verification log

- 2026-10-24 `checked`: E4–E6 on `deep-server`; `R/strauss1989.R` read on
  GitHub (`main`); README examples.
