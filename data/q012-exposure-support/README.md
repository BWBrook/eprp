# Q-012: Triton joint exposure audit

Owner: Claude | 15 October 2026, revised 16 October after Codex's freeze check (76/1686) | Gate 2 of the
[Q-012 design](../../literature/2026-10-15-q012-support-identification-design.md),
cleared by Codex in 76/1681.

Status: **support only.** It sizes the *measured-exposure* adjustment (R3m).
It cannot separate unmeasured clade-tied exposure (R3b). No durations or
survival outcomes were used.

## Rebuild

```bash
Rscript data/q012-exposure-support/names.R
uv run data/q012-exposure-support/crosswalk.py data/q012-exposure-support/triton_names.txt
Rscript data/q012-exposure-support/build.R
```

- The pipeline is base R plus one uv script (openpyxl 3.1.5, with the S3
  hash checked).
- `build.R` runs in about 2 minutes. A rerun reproduces all outputs byte for
  byte.
- **Inputs:**
  - Triton v4, 2023 update, `data/raw/triton/triton_update_2023.RData`
    (git-ignored; CC0; Fenton et al. 2021, 10.1038/s41597-021-00942-7).
    SHA-256 `7275120da2727e37b7d951632ea15364b0135d4aeaa5e67dee64a4a3d738af46`,
    the same file as the Q-007 audit.
  - S3 of Lamyman et al. 2026.
  - `species.tsv` and `lineage_edges.tsv` from the
    [event dictionary](../q012-event-dictionary/README.md).
- **Outputs:**
  - [summary.txt](summary.txt);
  - [triton_names.txt](triton_names.txt);
  - [name_crosswalk.tsv](name_crosswalk.tsv);
  - [species_triton.tsv](species_triton.tsv);
  - [lineage_coverage.tsv](lineage_coverage.tsv);
  - [lineage_bin_E.tsv](lineage_bin_E.tsv);
  - [pair_exposure.tsv](pair_exposure.tsv);
  - [bin_sites.tsv](bin_sites.tsv).

## Definitions

The full text is in the headers of `crosswalk.py` and `build.R`.

- **Name crosswalk,** source-supported rules only:
  1. exact name;
  2. S3 `Morphospecies Tree1v2`, an Aze 2011 name on a "Name Changed" row;
  3. S1's informal-genus backticks removed.

  Anything else stays unmatched, with its reason recorded. Single-epithet
  candidates are recorded but not applied.
- **Occurrences:** `trim == "inc"`, with a palaeolatitude, mapped through
  the crosswalk, and within the species' S1 range.
- **Cells:** 1-Myr bins × 10° signed palaeolatitude bands.
- **Lineage occurrences:** the union of members within the lineage's range.
- **Coverage:** "covered" means at least half the lineage's bins have data.
- **Exposure covariate E, past-only.** For the hazard in bin b, use the
  lineage's mean |palaeolatitude| from the nearest **older** bin with data,
  at most 2 bins older. The bin's own mean and later bins are never used.
  Otherwise E is missing, with an indicator. It is standardised over
  observed lineage-bins.
- **Pair measures,** over co-existing bins with at least 3 joint data bins:
  - (a) Jaccard similarity of signed band cells, with members shared by the
    pair excluded;
  - (b) mean per-bin |difference| in E of at least 5°, using all members;
  - (c) the |difference of the two lineages' mean E| over the joint bins,
    at least 5°;
  - (d) and (e): measures (b) and (c) recomputed on the lagged `used_value`
    the hazard actually receives. These are the ones that bear on the
    model. Measures (a)–(c) use unlagged bin means and are descriptive
    only.

  Measure (c) was added after the first rerun, because (b) is inflated by
  sampling noise in sparse bins. Measure (b) is reported unchanged.

## Results

**Crosswalk:**

| Rule | Triton names |
| --- | ---: |
| Exact | 340 |
| Tree1 | 38 |
| Backticks | 1 |
| Unmatched | 13 |

- That reaches **379 S1 species**, with no collisions.
- The 13 unmatched are listed with their reasons: 5 *Streptochilus*, 3
  *Tenuitella*, 2 "Removed", and 3 others.

**Coverage:**
- 371 species have 490,847 in-range occurrences.
- 235 of 268 lineages have data, and **213 are covered**. Median coverage is
  1.0.

**E:**
- 3,184 lineage-bins: 2,069 take the previous bin's value, 55 the value from
  two bins back, and 1,060 are missing.
- The missing bins include every lineage's first bin and all bins before
  66 Ma, where Triton has no data.
- E is standardised by mean 26.26° and SD 13.38°.

**Pairs, on the model's own lagged input** (`used_value`; measures (d)
and (e), at least 3 jointly available used values; corrected 16 October
after Codex's check):

| Pair type | (e) systematic: different / similar / insufficient | (d) per-bin: different / similar |
| --- | --- | --- |
| Parent–daughter, budding | **52 / 63** / 93 | 65 / 50 |
| Sister | **46 / 42** / 87 (59 never co-exist) | 62 / 26 |
| Parent–daughter, bifurcation candidates | 49 insufficient | — |

- **98 relative pairs differ systematically in the input the model
  uses.** The earlier "about 105" came from unlagged bin means.
- These are dependent descriptive contrasts. They are not independent
  sample sizes, and they do not show that adjustment will remove
  confounding.
- Because E uses all members, the 157 pairs that share members are similar
  partly by construction.

**Unlagged observed bin means** (measures (a)–(c), descriptive only):

| Pair type | (a) Jaccard different / similar | (b) per-bin | (c) systematic |
| --- | --- | --- | --- |
| Parent–daughter, budding | 31 / 36 | 69 / 53 | 52 / 70 |
| Sister | 42 / 55 | 68 / 29 | 53 / 44 |
- **Sampling geography is uneven:** 34 to 4,372 sites per bin. Occupied
  latitudes partly reflect where cores were drilled.

## Known input issues (22 October 2026, open)

The side session's Triton catalogue work (board 76/2201; evidence on branch
`worktree-side-work` at `ebcee43`, `resources/sources/triton/`) found two
input defects. Both must be settled before E enters an empirical fit.

- **Duplicates.** The 2023 file was not deduplicated. 16,256 cross-source
  groups are true duplicates. The conservative recipe
  (`triton_dedup.R`, cross-source copies with a recorded depth only) removes
  16,260 rows.
  - Rerunning `build.R` on the deduplicated file leaves Jaccard and coverage
    robust.
  - E changes in 1,454 of 2,267 lineage-bins, 423 of them by at least 1°.
  - 8 `E_class` and 8 E-systematic values flip, and so do 2 `used_systematic`
    and 2 `used_perbin` values. The 98 systematic contrasts above are
    therefore not final.
  - Per-bin site counts are inflated because hole IDs are scoped to one
    source.
- **Mixed plate models.** The 108,339 Neptune-sourced rows carry NSB's own
  Seton et al. (2012) palaeolatitudes and NSB's 2018–19 ages. All other rows
  use Matthews et al. (2016) at whole-Ma ages. E pools both models.

## Reading

- The measured-exposure adjustment (R3m) has a real lever in the model's
  own covariate.
- It cannot separate unmeasured clade-tied exposure (R3b).
- How the past-only E enters the landmark prediction, and why the pilot
  is deferred, are in the
  [addendum](../../literature/2026-10-16-q012-events-exposure-addendum.md).
