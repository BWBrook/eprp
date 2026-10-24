---
id: fossilbrush
name: fossilbrush
kind: r-package
domain: data-access
languages: [R]
home: https://cran.r-project.org/package=fossilbrush
repo: https://github.com/jf15558/fossilbrush
paper: [10.1111/2041-210x.13966]
licence: GPL (>= 3)
release: {version: 1.0.6, date: 2025-06-05, checked: 2026-10-24}
maintenance: {state: slow, last_commit: 2025-06-03, checked: 2026-10-24}
tier: T2
validated_uses: ["check_taxonomy: conflicting higher classifications and non-letter characters (recall 1.0, no false flags)"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r3, image: "eprp-sw/bench-r3:t3 (sha256:44432c89…)", host: deep-server}
blockers: ["flag_ranges compares differences with its thresholds as text, and measures LAD excesses from the reference FAD"]
related_sources: [pbdb, classic-compendia]
eprp_questions: [Q-040, Q-038, Q-042]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# fossilbrush

## Summary

fossilbrush detects and resolves anomalies in palaeontological occurrence
data: taxonomic formatting, spelling and classification conflicts
(`check_taxonomy`), stratigraphic ranges out of line with a reference
(`flag_ranges`, `revise_ranges`), and GTS2020 interval ages. It is the
cleaning step of the 2025 "ten simple rules" workflow (scan A).

## Validation

Tests in [bench/VALIDATION_T3.md](../bench/VALIDATION_T3.md), on a synthetic
taxonomy (400 genera, 5,000 occurrences) with injected errors:

| Test | Result |
| --- | --- |
| F1: `check_taxonomy` | conflicting families: recall 1.0 (30 of 30), no false flags; non-letter characters: 1.0 (10 of 10), none false; **misspellings: 0.87 (26 of 30), with 11 synonym pairs reported among clean names** (F1 fails on the declared 0.9) |
| F2: `flag_ranges` with `flag.diff = 5`, 100 injected outliers 10–30 Myr beyond their taxon's range among 20,000 valid occurrences | **fail**: 24 of 100 flagged (none of the 50 older than the FAD; 24 of the 50 younger than the LAD); no false flags |

## Weaknesses and pitfalls

- **`flag_ranges` compares as text.** Its `fad_diff` and `lad_diff` start
  as copies of the character status vector, so `fad_diff >= flag.diff` is a
  string comparison: 18.72 is "less than" "5" and goes unflagged, 55.65 is
  flagged. The text-comparison prediction matches all 100 injected flags.
- **`flag_ranges` measures occurrences beyond the LAD from the reference
  FAD** (`yr$max[mt] - v$min` in the "R00", "1R0" and "0R0" branches; the
  per-taxon summary correctly uses `yr$min[mt]`). The returned LAD
  difference equals the true excess plus the taxon's whole range, to
  0.005 Myr.
- Reading the returned differences numerically (`as.numeric`) and
  comparing them yourself recovers all 100 outliers with no false flags,
  but the LAD values themselves are wrong.
- Spell-checking misses some one-letter substitutions and pairs distinct
  names; review its synonym list rather than applying it.
- Queued for the authors as [CONTACTS](../CONTACTS.md) S10.

## Citation and licence

Flannery-Sutherland, J. T., Raja, N. B., Kocsis, Á. T. and Kiessling, W.
(2022). fossilbrush: an R package for automated detection and resolution of
anomalies in palaeontological occurrence data. *Methods in Ecology and
Evolution* 13, 2404–2418. doi:10.1111/2041-210x.13966 (checked on
Crossref). GPL (≥ 3).

## Verification log

- 2026-10-24 `checked`: F1, F2 on `deep-server`; `R/flag_ranges.R` read on
  GitHub (`master`); text-comparison and LAD-offset predictions checked
  against all injected rows.
