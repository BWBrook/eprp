# Triton Fig. 2C values (C045)

`comparable.tsv` retains all 2,267 lineage–bin pairs with an observed mean
absolute palaeolatitude before and after the conservative cross-source removal,
including unchanged values. `newly_missing.tsv` holds the four bins that lose
their last eligible occurrence; their after values and deltas are `NA`.
All means are in degrees. The signed delta is **after minus before**.
These are unlagged, unstandardised observed means, rather than the lagged
`used_value` covariate. Each bin is the integer floor of age in Ma.

The extraction evaluates the pinned original Q-012 builder only through its
`emat` construction, using the same wrapper transformations as
`../../replay-20261108/data/raw_mean_check.R`. It replaces `round(obs, 3)`
and `round(used, 3)` with the unrounded values before evaluation. It does not
read the rounded three-decimal output tables. Values are explicitly formatted
with `sprintf("%.17g", value)` so that their binary64 precision survives TSV
serialization. Rows are sorted by lineage and ascending bin.

The conservative removal uses matching species, abundance, sample depth and
three-decimal location keys, only for cross-source groups with nonmissing
sample depth, retaining the highest-priority represented source. Priority is
ForCenS, IODP, Neptune, Pangaea, Lloydetal2012, Fentonetal2016. It removes
16,260 of 541,846 presence rows. A key collision does not prove duplication of
a physical observation. This is a descriptive EPRP support comparison, not a
fitted biological outcome or a correction of an external published analysis.

## Reproduce

From this directory, with the retained replay directory and fixed Triton v4
RData supplied as positional arguments:

```sh
python3 reproduce.py "$RETAINED_REPLAY_DIR" "$TRITON_V4_RDATA" .
```

Requires base R and Python's standard library; no packages or installations.
The retained replay directory must contain `inputs/{species,lineage_edges,
name_crosswalk}.tsv`, `scripts/{q012_original,raw_mean_check,triton_prepare}.R`,
`scripts/triton_independent.py`, `projection.tsv.gz`, and `drop_rows.txt`.
All retained source inputs are read-only. Run on a data/compute host with the
retained inputs available; only the output directory is written. No raw
occurrence identifiers or access details are exported.

The Python route independently rebuilds the deletion set, applies the
species/lineage/range/bin selection and computes the means with
`statistics.fmean` from the retained 17-significant-digit projection. It checks
every exported value and missingness state at a tolerance of 1e-12 degrees,
and verifies the expected key sets. It shares the raw projection, support
tables and priority policy with the R route; it independently implements the
grouping and calculations.

`receipt.json` records input/script/output SHA256 values, software versions,
counts, predicates, and observed route disagreement. `r_summary.tsv` supplies
the full builder/missingness accounting. Outputs contain no timestamps or
compressed files and can be compared byte for byte in the recorded runtime.
The table predicates are `abs(delta) > 1e-9` (1,388 bins) and
`abs(delta) >= 1 - 1e-9` (411 bins); the maximum absolute change is 26.89925
degrees. The four newly missing bins are excluded from those 2,267 paired
comparisons.
