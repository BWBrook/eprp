# K–Pg plankton: source alignment and observation limits

Codex, 28 October 2026. A preliminary, reproducible alignment for the
[extinction/recovery synthesis](../../literature/2026-10-28-extinction-recovery-disagreements-codex.md).
This establishes what can be joined; it does not estimate recovery, test
mechanisms, harmonise age models or equate the two sites' environments.

## Deposits and custody

Downloaded 28 October 2026 directly from PANGAEA as provider TSVs, including
metadata headers. The exact files, SHA-256 and private derived tables are at
`deep-server:/data/codex/artifacts/eprp/kpg-plankton-alignment-20261028/`.
Destination input hashes were verified. `raw/` is unchanged; `aligned/` contains
private derived tables and `summary.json`. Raw or derived rows are not checked
into Git. PANGAEA declares **CC BY-NC-ND 3.0** on the two Alvarez tables and
**CC BY 4.0** on the three Jones tables. Respect the individual terms, including
any restriction on distributing adaptations; the aggregate checks below are not
a grant of permission to redistribute the joined material.

| Deposit | What was used | Licence as stated by provider |
| --- | --- | --- |
| [Alvarez Table A](https://doi.org/10.1594/PANGAEA.893899) | selected taxon percentages, interpolated at 13-kyr spacing | CC BY-NC-ND 3.0 |
| [Alvarez Table E](https://doi.org/10.1594/PANGAEA.893919) | individual sample labels, depths and ages, not raw species counts | CC BY-NC-ND 3.0 |
| [Jones all taxa](https://doi.org/10.1594/PANGAEA.997794) | raw count table, no age fields | CC BY 4.0 |
| [Jones dominant counts](https://doi.org/10.1594/PANGAEA.997781) | dominant categories, two age columns | CC BY 4.0 |
| [Jones dominant percentages](https://doi.org/10.1594/PANGAEA.997793) | the corresponding published percentages | CC BY 4.0 |

The published studies are [Alvarez et al. 2019](https://doi.org/10.1038/s41586-019-1590-8)
and [Jones et al. 2026](https://doi.org/10.1029/2026PA005729). The PANGAEA
records cite the original papers and need citation in downstream work.

## What aligns, and what does not

- Jones's raw table contains **199 distinct hole × core × within-section depth
  keys**. Both dominant tables contain the same 186 keys, all present in the
  raw file. The other 13 are not empty: all have nonzero counts and lie in
  hole E cores 3 and 4. Why they were excluded from the dated tables is not
  established; they remain in the private alignment with missing ages and
  dominant-category percentages, not zeroes.
- Jones's count and percentage columns match to rounding under their stated
  row totals (maximum absolute discrepancy less than 0.000001 percentage
  points for nonblank cells). This checks the tabular arithmetic, not whether
  the categories capture the same organisms or sampling effort as the Pacific.
- Both published Jones age columns are kept: they differ for 105/186 dated
  samples, by a median absolute 0.890 kyr and maximum 15.167 kyr. These are
  differences between the two supplied model outputs, not age uncertainty
  intervals. No age is assigned to the 13 raw-only rows.
- Alvarez Table A has 997 interpolated time points and 25 reported categories,
  not 997 independent samples. Table E has 990 distinct sample labels: 979
  from holes at Site 1209 and **11 from Site 1210**. It is a sample/depth/age
  index, not a full raw abundance matrix. The full underlying taxon counts
  have not been located in this check.
- Four labels are selected for the preliminary table: *Neobiscutum*,
  *Praeprinsius*, *Cruciplacolithus* and *Coccolithus*. For Alvarez only,
  the reported small and large *Cruciplacolithus* percentages are summed when
  both are present. This is a transparent working crosswalk, not an assertion
  that species concepts or detection are identical. The Alvarez values are
  percentages of an assemblage but only selected taxa are listed, so they
  need not sum to 100; Jones's dominant categories include an “other” class.
- Source ages remain in their supplied units: Alvarez `ka BP`, Jones `Ma`.
  The alignment does not silently assume the same time origin or equate
  samples across the two sites. The settings are also confounded with location,
  water depth, chronology, preservation and investigator/sampling differences.

## Reproduce and verify

```bash
python3 data/kpg-plankton-alignment/align.py INPUT_DIR OUTPUT_DIR
python3 -m unittest discover -s data/kpg-plankton-alignment -p 'test_align.py' -v
```

The input directory must contain the five original `pangaea-<id>.txt` files.
The script requires unique Jones sample keys, checks that dated count and
percentage keys and ages agree, tests the count/percentage arithmetic, retains
unmatched raw keys, and writes a private table for each site plus aggregate
summary. Its [checked summary](summary.json) includes hashes and outcomes;
the tests exercise unmatched rows, incompatible percentages and duplicate keys.

The next scientific step is to establish the 13 excluded samples' role in the
core splice, the raw Pacific abundance and observation protocol, a defensible
common taxonomy and age alignment, and an independently measured outcome. The
current tables do not establish comparable independent perturbations and
should not be fitted as a test of ecological memory.
