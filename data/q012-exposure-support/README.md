# Q-012: Triton joint exposure audit

Owner: Claude | 15 October 2026 | Gate 2 of the
[Q-012 design](../../literature/2026-10-15-q012-support-identification-design.md),
cleared by Codex in 76/1681.

Status: **support only.** It sizes the *measured-exposure* adjustment (R3m).
It cannot separate unmeasured clade-tied exposure (R3b). No durations or
survival outcomes were used.

## Rebuild

```bash
Rscript data/q012-exposure-support/build.R
```

- Base R; it runs in about 60 s, and a rerun reproduces all five outputs
  byte for byte.
- **Inputs:**
  - Triton v4, 2023 update, `data/raw/triton/triton_update_2023.RData`
    (git-ignored; CC0; Fenton et al. 2021, 10.1038/s41597-021-00942-7).
    SHA-256 `7275120da2727e37b7d951632ea15364b0135d4aeaa5e67dee64a4a3d738af46`,
    the same file as the Q-007 audit.
  - `species.tsv` and `lineage_edges.tsv` from the
    [event dictionary](../q012-event-dictionary/README.md).
- **Outputs:**
  - [summary.txt](summary.txt);
  - [species_triton.tsv](species_triton.tsv);
  - [lineage_coverage.tsv](lineage_coverage.tsv);
  - [pair_exposure.tsv](pair_exposure.tsv);
  - [bin_sites.tsv](bin_sites.tsv).

## Definitions (fixed before the first run; also in the script header)

- **Occurrences** are Triton `triton.pres` records with:
  - `trim == "inc"`;
  - a palaeolatitude;
  - an exact name match to an in-scope S1 morphospecies, after stripping
    outer whitespace;
  - an age within that species' S1 range.
- **Cells:** 1-Myr bins × 10° signed palaeolatitude bands.
- **Lineage occurrences:** the union of member species' occurrences within
  the lineage's own range.
- **Shared members.** Membership is many-to-many, so members shared by both
  lineages of a pair are excluded from both sides of that comparison.
- **Coverage:** the share of a lineage's 1-Myr bins with at least one
  occurrence; "covered" means at least 0.5.
- **Pair classes**, by the Jaccard similarity of occupied cells, over bins
  where both lineages exist and both have data:

  | Class | Rule |
  | --- | --- |
  | No co-existence | The lineages never exist together |
  | Insufficient | Fewer than 3 joint data bins |
  | Different | J < 0.5 |
  | Similar | J ≥ 0.5 |

## Results

**Matching and coverage:**
- 340 of 480 in-scope S1 species match Triton's 395 names exactly.
  - 332 have occurrences within their S1 ranges, 420,490 occurrences in all.
  - The article reports its own matching to all 480 (pp. 6–7). That
    crosswalk is not in the supplement, so the 140 species without an exact
    match are a mapping gap, not an absence. The S3 synonym tables are the
    route to closing it.
- 211 of 268 lineages have data; 190 are covered (coverage at least 0.5).
  Median coverage is 0.99.

**Relative pairs:**

| Pair type | Different | Similar | Insufficient | No co-existence |
| --- | ---: | ---: | ---: | ---: |
| Parent–daughter, budding (overlap) | 31 | 30 | 147 | 0 |
| Parent–daughter, bifurcation candidate (boundary) | 0 | 0 | 49 | 0 |
| Sister | 42 | 48 | 85 | 59 |

- **73 relative pairs have observably different palaeolatitude occupancy**
  while co-existing, with a median difference in mean |palaeolatitude| of
  9.95°. 78 are similar (median 4.84°).
- **Bifurcation candidates cannot be compared** on co-existence by
  definition. The parent's last bins against the daughter's first bins
  would need a separate rule.
- **Shared members.** 157 pairs had shared members excluded. That moves
  many budding pairs into "insufficient".
- **Sampling geography is uneven.** The number of sites with matched
  occurrences per 1-Myr bin ranges from 34 to 4,372 (median 81.5), so
  occupied bands partly reflect where cores were drilled.

## Reading

- **There is a measured-exposure lever:** about 70 pairs of relatives that
  lived together in different palaeolatitude bands. That is enough for the
  calibration's R3m control to be meaningful. Whether it gives adequate
  power is for calibration to decide, not this audit.
- **Even so, this cannot separate unmeasured exposure that shares the tree's
  correlation (R3b).** A positive result stays "residual phylogenetic
  dependence after adjustment for measured exposure".
- **Possible extensions, none allocated:**
  - closing the 140-species name gap through the S3 synonym tables;
  - a rule for comparing across bifurcations;
  - a control for site sampling, such as occupancy relative to sampled
    bands.
