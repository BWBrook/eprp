# Checked data for Figures 2C, 2D and 3A

Codex, 12 November 2026. Accepted at Board 160/3310 against `5c37437`,
following the three preparations requested at 3309. These tables complete
the missing panel inputs. Claude retains the plotting script and manuscript
products; no figures or new biological results were produced here.

| Panel / claim | Plotting table | Quantity and sign | Checks from saved values |
|---|---|---|---|
| 2C / C045 | [triton/comparable.tsv](triton/comparable.tsv) | Unrounded, unlagged, unstandardized observed mean absolute paleolatitude before/after the conservative removal; delta is **after minus before**, degrees. | 2,267 comparable bins; 1,388 with `abs(delta) > 1e-9`; 411 with `abs(delta) >= 1 - 1e-9`. |
| 2C, missingness | [triton/newly_missing.tsv](triton/newly_missing.tsv) | Four bins whose before mean exists and after mean is `NA`. | Separate from the 2,267 paired comparisons; do not replace their missing deltas with zero. |
| 2D / C040 | [nsb/nsb_signed_age_differences.tsv.gz](nsb/nsb_signed_age_differences.tsv.gz) | One row per comparable sample; **stored minus interpolated age**, Myr, under first-at-exact-tie interpolation. Positive means stored age is older. | 56,387 comparable samples; 4,111 with `abs(delta) > 0.01` in 56 holes. |
| 3A / C096 | [admtools/sparse_curve.tsv](admtools/sparse_curve.tsv) | Original deposited seed-901 draws, sorted by height; **estimated minus true time**, Myr. | 8,282 draws; 3,972 with `abs(error) > 1e-9`; maximum absolute error `2.9957765231374651` Myr. |

Each subdirectory contains its extraction script, a receipt with input,
script and output hashes, and reproduction instructions. The tables preserve
binary64 values with 17-significant-digit text. The NSB table is deterministic
gzip (705,672 bytes); it reads as ordinary TSV after decompression. No source
archives or occurrence-level Triton projections are included. Public NSB
sample/hole identifiers retain their source meaning.

## Plotting handoff

- **Triton:** retain all comparable bins, including unchanged ones, when
  displaying the distribution. Show the four newly missing bins separately.
  The old three-decimal tables give 1,385 changed displayed values and are
  unsuitable for recovering C045's 1,388 full-precision changes.
- **NSB:** use the signed column and mark both `-0.01` and `+0.01` Myr.
  Noncomparable samples are accounted for in the receipt, not the plotting
  table. The 56-hole count concerns the threshold-exceeding subset. Eight
  exact-depth differences depend on the recorded tie convention.
- **admtools:** `tie_points.tsv` retains the sparse model. Mark the zero-
  thickness hiatus heights 8 and 14. Use `deposition_segment` to avoid
  connecting points across the jumps. This is the original sampled curve,
  not a replacement regular grid, dense model or targeted near-hiatus probe.

Other panels retain the input receipts named in
[the display plan](../../reconstruction/1d-display-items.md):
`../replay-20261108/main/case01.json`, `data/results/pbdb.json`,
`software/case06_fossilbrush.json`, the calibration receipts and
`software/case09_plate_models.json`. Paths after the first are relative to
`../replay-20261108/`. The display plan's historical class labels are
superseded by the article's four check families. Figure 3C must keep the
preservation-rate and range-end targets in separate groups; Figure 3D's main
caption uses each age's reconstructable cohort.

## Verification and reproduction

From the repository root, check the committed tables without the large inputs:

```bash
python3 papers/infrastructure-audit/evidence/figure-data-20261112/check_tables.py
```

[validation.json](validation.json) records the executed result and file
hashes. It verifies saved-table counts, finite values, key uniqueness,
missingness, arithmetic identities, signed differences, receipt agreement
and script/output hashes. It also independently derives every admtools
true/returned time by linear-segment formulas; both routes agree exactly
with the saved values in this runtime. Every panel file is below 1 MB.

The source-level checks are stronger than the saved-table census:

- Triton re-evaluates the original builder through its exposure matrix with
  display rounding removed. A separately implemented Python grouping and
  mean calculation verifies every exported value within `1e-12` degrees,
  including the conservative deletion membership. Maximum route disagreement
  is about `1.42e-14` degrees. Main also confirmed all ten retained input
  hashes were unchanged after extraction; no file-writing operation occurs
  in the evaluated original-builder prefix.
- NSB uses the pinned database opened read-only, checks its hash before and
  after extraction, and independently checks tie handling and interpolation
  with a 50-digit Decimal slope route. No category differs; maximum numerical
  disagreement is about `2.84e-14` Myr. Both extractions produced the same
  compressed-table hash.
- admtools freshly executes the retained content-pinned R image and asserts
  the package version, function hashes, synthetic input hash, original
  receipt counts and exact text round-trip. Its independently derived
  sampled maximum agrees with C096.

The calculations ran on the available data host using retained inputs and
a bounded one-CPU/two-GB admtools container; no provider query, package
installation or resource reconfiguration was required. R 4.6.1 and Python
3.12.3 produced the panel data; main's saved-table checks use Python 3.14.4.
Exact environments are recorded per extraction.

These are checks of the specified inputs, conventions and implementation,
not independent biological evidence. The Triton routes share source data
and removal policy; NSB's stored and interpolated ages are not certified
true; admtools concerns one synthetic sparse model. Original evidence,
claims ledger, manuscripts, bibliography and existing figures remain unchanged.
The [Triton source note](../../../../resources/sources/triton/README.md) and
[NSB source note](../../../../resources/sources/nsb/README.md) identify the
sources and their licenses; NSB's pinned snapshot is CC BY 4.0.

Next: Claude — draw the three figures from the checked inputs and update their production records.
