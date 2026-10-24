---
id: stratpal
name: StratPal
kind: r-package
domain: fossil-record-forward
languages: [R]
home: https://mindthegap-erc.github.io/StratPal/
repo: https://github.com/MindTheGap-ERC/StratPal
paper: [10.1111/2041-210x.14507]
licence: Apache-2.0
release: {version: 0.7.1, date: 2025-12-06, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-10-08, checked: 2026-10-24}
tier: T2
validated_uses: ["p3: homogeneous Poisson point process", "thin: constant and variable retention"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r2, image: "eprp-sw/bench-r2:t2 (sha256:49f30706…)", host: deep-server}
blockers: ["depends on admtools, whose strat_to_time is wrong above hiatuses"]
related_sources: []
eprp_questions: [B-007, Q-003, Q-005, Q-013, Q-041]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# StratPal

## Summary

StratPal builds stratigraphic palaeobiology pipelines: it simulates
processes in time (trait evolution, occurrences, extinctions), applies
niche and taphonomic filters, and passes the result through an age–depth
model from admtools into the stratigraphic record. It is the only packaged
"stratigraphic filter" simulator found in the landscape (scan A; same
group as admtools).

## Validation

| Test | Result |
| --- | --- |
| S4: `p3(rate = 2, from = 0, to = 10)`, 20,000 draws | pass (mean 19.96; variance ratio 1.001; uniform, KS p = 0.35) |
| S5: `thin` at constant 0.3 and at x/10 retention, 200,000 points | pass (0.2995, z = −0.49; KS p = 0.21) |

Higher-level functions (`strat_filter`, `last_occ`, `range_offset`,
`apply_niche`, `apply_taphonomy`) were not tested in this tranche.

## Weaknesses and pitfalls

- Pipelines that map strat-domain results back to time go through
  admtools' `strat_to_time`, which is wrong above hiatuses
  ([admtools](../admtools/README.md)). Check which direction a pipeline
  converts before trusting its time-domain output.

## EPRP relevance

The natural engine for B-007 (stratigraphic architecture alone) and for
rebuilding Q-005's and Q-041's surrogates (lead L-011), once its higher
functions are tested.

## Citation and licence

Hohmann, N. and Jarochowska, E. (2025). StratPal: an R package for creating
stratigraphic paleobiology modelling pipelines. *Methods in Ecology and
Evolution* 16, 678–686. doi:10.1111/2041-210x.14507 (checked on Crossref).
Apache-2.0.

## Verification log

- 2026-10-24 `checked`: S4, S5 on `deep-server`; exported functions from
  the NAMESPACE.
