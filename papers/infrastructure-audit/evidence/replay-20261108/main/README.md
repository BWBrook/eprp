# Counts-only membership and published probability checks

Main Codex, 8 November 2026. These checks rederive findings from the Databases
and References sessions respectively. They do not reopen restricted extracts
or change the scientific questions those sessions own.

## Case 1: dated public membership

The offline production builder in `data/q027-regional-support/build.py` is
rerun on its original checksum-pinned deposit, public snapshot and static
tables. The separate `check_case01.py` reads the taxon member and snapshot
with the standard-library CSV parser, takes their set difference, and derives
the regional threshold from the rebuilt support table. It imports no builder
functions. The fresh table must match the committed table byte for byte.

The claim concerns **absence from a dated public snapshot**. Neither the set
difference nor the original deposit alone establishes why each record is
absent, whether it is currently restricted, or whether any live query fails.
The fresh rebuild reproduces all 1,638 support rows byte for byte. It finds
71,103 absent members among 368,760 deposited molluscan occurrences and
reproduces 14 versus 12 qualifying stages out of 21. The broader
withheld-record finding is not re-established here. Counts-only
output contains no occurrence, collection or reference identifiers.

With the retained inputs mounted and a fresh output directory, run:

```sh
python3 data/q027-regional-support/build.py "$ARCHIVE" "$PUBLIC_SNAPSHOT" "$STATIC" "$NEW_OUTPUT"
python3 papers/infrastructure-audit/evidence/replay-20261108/main/check_case01.py \
  "$ARCHIVE" "$PUBLIC_SNAPSHOT" "$NEW_OUTPUT/support.tsv" \
  data/q027-regional-support/support.tsv
```

`case01.json` records counts and hashes, with filesystem locations omitted.
The support threshold is the original inexpensive presence diagnostic,
using approximate cells and deposited collection-age palaeocoordinates.
It is not a result from the later Q-027 richness estimator.

## Case 11: the stated binomial contract

The author-hosted PDF has SHA256
`7ba178cce4c5359152e474f027171faae2d317b931e124ba9ddef5e63c20fc71`,
matching References' source. Main visually rechecked printed page 4:
the prose states 47 trials, 28 matches, probability 0.55 and result
3.4 × 10⁻¹⁶. Source: [author's public copy and publication record](https://ciunit.org/publications/rampino-2025-sequence-stage-boundaries.html),
DOI `10.1016/j.earscirev.2025.105100`. No PDF or page image is redistributed.

`check_case11.py` uses an exact rational recurrence for the **complement**
of the lower binomial tail, unlike the References script's direct exact
upper-tail sum. It also calls R's `pbinom`. All routes give approximately
0.315864026025072. The small final-digit difference between exact decimal
0.55 and R's binary floating-point argument has no inferential consequence.
`case11.json` retains both values and the exact fraction. Run:

```sh
python3 papers/infrastructure-audit/evidence/replay-20261108/main/check_case11.py
```

The typeset equation's combinatorial coefficient differs from the standard
binomial sum described in its prose. This check states the mathematical
contract it evaluates. It does not validate a replacement geological null,
rerun the separate spectral analysis, or refute periodicity. Main's recurrence
and R calculation are independent implementations of the arithmetic; they are
not independent geological evidence.

## Parent reviews of delegated data results

`nsb_count_review.json` records a separate SQLite `count(*)` on both the
sample table and its hole-summary join: each has 61,862 rows. The older
61,863 count included an exported header. The duplicate-depth sensitivity
in the data receipt addresses samples exactly at tied depths, not every
possible age-depth interpolation model.

`check_triton_display.py` independently joins paired TSVs and compares
displayed values with exact decimal arithmetic. It confirms 1,385 changes
among 2,267 comparable displayed means, 411 of at least one degree, four
newly missing means, and pair-class flips of 8/8/2/1. These displayed counts
are separate from the full-precision mean calculation in the data replay.
Run from the repository root:

```sh
python3 papers/infrastructure-audit/evidence/replay-20261108/main/check_triton_display.py \
  papers/infrastructure-audit/evidence/replay-20261108/data/results
```
