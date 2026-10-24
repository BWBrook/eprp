---
id: palaeoverse
name: palaeoverse
kind: r-package
domain: data-access
languages: [R]
home: https://palaeoverse.org
repo: https://github.com/palaeoverse/palaeoverse
paper: [10.1111/2041-210x.14099]
licence: GPL (>= 3)
release: {version: 1.5.0, date: 2026-06-11, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-10-23, checked: 2026-10-24}
tier: T2
validated_uses: ["bin_time: mid, majority, random and point (uniform) methods, for continuous ages away from bin boundaries", "tax_range_time (to its three-decimal rounding)", "palaeorotate point method for MERDITH2021, PALEOMAP and MATTHEWS2016_pmag_ref, consistent with pyGPlates on the mirrored model files (same GPlates software, so a consistency check)", "palaeorotate grid method, to its grid resolution"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r3, image: "eprp-sw/bench-r3:t3 (sha256:44432c89…)", host: deep-server}
blockers: ["point method needs the GPlates Web Service online; grid method downloads about 45 MB per model"]
related_sources: [pbdb, palaeogeography, timescale]
eprp_questions: [Q-040, Q-041, Q-045, Q-027, Q-049, Q-016, Q-038]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagent, 24 Oct 2026; findings applied"}
---

# palaeoverse

## Summary

palaeoverse is the community data-preparation package for palaeobiology:
time and space binning, palaeocoordinates (`palaeorotate`), taxonomic
checks and ranges, latitudinal bins, geological time axes, and GTS2012 and
GTS2020 tables. Reach for it to prepare PBDB-style occurrence data
consistently; scan A ranked it first among the landscape's data tools.

## Validation

Tests in [bench/VALIDATION_T3.md](../bench/VALIDATION_T3.md); results in
[bench/README.md](../bench/README.md) (tranche 3).

| Test | Result |
| --- | --- |
| V1: `bin_time` "mid" and "majority" against independently computed bins, 20,000 occurrences | pass (mid 20,000 of 20,000; majority 19,983 of 19,983, 17 exact ties excluded) |
| V2: "random" draws equally among overlapped bins, 200 replicates, 10,273 multi-bin occurrences | pass (χ² p = 0.40) |
| V3: "point" (uniform) draws in proportion to overlap | pass (χ² p = 0.51) |
| V4: `tax_range_time` FAD and LAD | fail at the declared 1e−9 (differences up to 0.0005); the function rounds to three decimals (its source) |
| V5: `GTS2020` stage bases against ICS charts | 59 of the 60 stages in the v2020/01 table equal it (Priabonian 37.71 against 37.8); 61 of 97 stages with printed v2024/12 values differ by more than 0.001 Myr |
| V6: `palaeorotate` against pyGPlates, 300 public PBDB collections × 6 ages, four models | pass for MERDITH2021, PALEOMAP and MATTHEWS2016_pmag_ref (all within 0.0001°); fail for TorsvikCocks2017 (see below) |

## Strengths

- `bin_time`'s four methods do what the documentation says for continuous
  ages, including the length-weighted "point" draw and the length-blind
  "random" draw.
- The point method reproduces an offline pyGPlates reconstruction on the
  same models to 0.00007° (same GPlates software, so a consistency check);
  the grid method's error is the distance from a point to its cell centre
  (median 0.38°), which rotation preserves.

## Weaknesses and pitfalls

- **Bin boundaries** (`bench/validate/t3_checks.R`): `mid` returns `NA`
  with a warning when the midpoint falls exactly on a boundary; a zero-width
  occurrence lying on a boundary makes `majority` and `random` stop with an
  error; an exact two-bin tie goes to the older bin under `majority`.
- **TorsvikCocks2017 is in a different absolute frame on the Web Service
  than in the GPlates Plate Model Manager's files.** One rigid rotation per
  age maps one onto the other with residual at most 0.00007° (3.1° at
  10 Ma, 22.0° at 200 Ma, 28.0° at 400 Ma), so relative plate motions are
  identical. The point and grid methods share the Web Service's frame. Which
  frame suits a question (palaeomagnetic, mantle or hybrid) has to be
  decided; results named "TorsvikCocks2017" are not comparable across
  routes without it.
- The grid method is far off near plate boundaries (2% of returned values
  more than 1° away, up to 56°) and returns no value for 2.6–3.6% of
  point–ages the point method reconstructs.
- `tax_range_time` rounds FAD, LAD and range to three decimals.
- **The `GTS2020` table is chart v2020/03, not the GTS2020 book** (its
  documentation says so). Its Fortunian base is 541 Ma; chart v2024/12
  gives 538.8 Ma. Use a current chart for boundary-sensitive work.
- Model choice matters (leads L-010, L-024): across MERDITH2021, PALEOMAP
  and MATTHEWS2016_pmag_ref the same collections' palaeolatitudes spread by
  a median 2.9° at 10 Ma, 4.3–5.7° from 50 to 300 Ma and 13.6° at 400 Ma
  (`bench/results/t3/t3_checks.json`).

## Citation and licence

Jones, L. A., Gearty, W., Allen, B. J., Eichenseer, K., Dean, C. D. et al.
(2023). palaeoverse: a community-driven R package to support palaeobiological
analysis. *Methods in Ecology and Evolution* 14, 2205–2215.
doi:10.1111/2041-210x.14099. Grids: Jones, L. A. and Domeier, M. (2024).
*Scientific Data* 11. doi:10.1038/s41597-024-03468-w. Both checked on
Crossref. GPL (≥ 3).

## Verification log

- 2026-10-24 `checked`: V1–V6 on `deep-server`; `R/tax_range_time.R` (line
  186, rounding) and `R/data.R` (GTS2020 source) read on GitHub (`main`).
- 2026-10-24 `checked` (after the independent review): boundary cases, the
  TorsvikCocks2017 frame fit, the three-model spread and grid omissions
  (`t3_checks.R`, `t3_checks.py`).
