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
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
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
| first bin with cumulative posterior ≥ 0.95 is at or after the first bin wholly after the extinction; a posterior that never reaches 0.95 counted as covered | 0.990 | 0.997 | 0.991 |
| cases that never reach 0.95 / return `NA` | 1,288 / 73 | 951 / 103 | 1,281 / 62 |
| coverage among cases that reach 0.95 (number of cases) | 0.970 (639) | 0.986 (218) | 0.973 (657) |
| the same, under the declared wording (bin of the extinction itself allowed) | 0.995 | 0.995 | 0.994 |

The first-absent-bin scoring matches agnostic's likelihood, in which
extinction in bin i means no occurrences from bin i on; the declared wording
was "at or after the bin of TE" (A2 discloses the difference).

Calibration in arm A (posterior decile → mean posterior → fraction truly
extinct by that bin): 0.1–0.2 → 0.16 → 0.63; 0.3–0.4 → 0.36 → 0.53;
0.5–0.6 → 0.54 → 0.59; 0.7–0.8 → 0.75 → 0.87; 0.8–0.9 → 0.86 → 0.945;
0.9–1 → 0.97 → 0.99. The posterior is below the observed fraction in every
decile, which is what a prior of 0.5 should do when every species is in fact
extinct. Pairs of case and bin are dependent and weighted towards long
series, so this is a characterisation, not a calibration test.

## Weaknesses and pitfalls

- **Fails under R ≥ 4.3 whenever `total` is supplied**: its first line,
  `if (missing(total) || total == '')`, applies `||` to a vector, now an
  error. Unequal sampling effort, the method's main input, is unusable
  as distributed; `identical(total, '')` would fix it. Queued as
  CONTACTS (queue held back) S2.
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
