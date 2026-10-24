---
id: agnostic-r
name: agnostic.R (Alroy 2014)
kind: workflow
domain: extinction-timing
languages: [R]
home: http://bio.mq.edu.au/~jalroy/agnostic.R
repo: http://bio.mq.edu.au/~jalroy/agnostic.R
paper: [10.1666/13074]
licence: none stated
release: {version: "single file, sha256 1eb9268f…c8db42", date: unknown, checked: 2026-10-24}
maintenance: {state: dormant, last_commit: unknown, checked: 2026-10-24}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["fails under R >= 4.3 when a total (sampling effort) vector is supplied", "no licence stated"]
related_sources: []
eprp_questions: [Q-013, Q-017, Q-034]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# agnostic.R (Alroy 2014)

## Summary

A single R function, `agnostic(onoff, total, prior, uniform)`, from
Alroy (2014): the posterior probability that a species has gone extinct by
each bin, from presence counts per bin and the sampling effort per bin,
with a prior probability of extinction within the series spread
exponentially (or uniformly) across bins.

## Validation

Characterised only (E4–E6; 1-Myr bins from the first occurrence to the
present, one sampling unit per bin, prior 0.5):

| Score | A | B | C |
| --- | --- | --- | --- |
| first bin with cumulative posterior ≥ 0.95 is at or after the true extinction bin | 0.990 | 0.997 | 0.990 |

Calibration in arm A (posterior decile against the fraction truly extinct
by that bin): 0.1–0.2 → 0.63, 0.3–0.4 → 0.53, 0.5–0.6 → 0.59,
0.7–0.8 → 0.87, 0.8–0.9 → 0.94, 0.9–1 → 0.99. All benchmark species are
extinct, against the default prior of 0.5, so this is not a test of the
method's calibration under its own model.

## Weaknesses and pitfalls

- **Fails under R ≥ 4.3 whenever `total` is supplied**: its first line,
  `if (missing(total) || total == '')`, applies `||` to a vector, now an
  error. Unequal sampling effort, the method's main input, is unusable
  as distributed; `identical(total, '')` would fix it. Queued as
  [CONTACTS](../CONTACTS.md) S2.
- Returns `NA` when fewer than two bins have data, and all zeros when the
  last bin is occupied.
- No licence stated; we fetch it by URL with a pinned sha256 rather than
  redistributing it.

## Citation

Alroy, J. (2014). A simple Bayesian method of inferring extinction.
*Paleobiology* 40, 584–607. doi:10.1666/13074 (checked on Crossref).

## Verification log

- 2026-10-24 `checked`: downloaded and hashed; read in full; E4–E6 on
  `deep-server`.
