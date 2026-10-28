# K–Pg plankton: source alignment and observation limits

Codex, 28 October 2026. A preliminary, reproducible alignment for the
[extinction/recovery synthesis](../../literature/2026-10-28-extinction-recovery-disagreements-codex.md).
This establishes what can be joined; it does not estimate recovery, test
mechanisms, harmonise age models or equate the two sites' environments.

## Deposits and custody

Downloaded 28 October 2026 directly from PANGAEA as provider TSVs, including
metadata headers. The exact files, SHA-256 and private derived tables are at
`deep-server:/data/codex/artifacts/eprp/kpg-plankton-alignment-20261028/`.
Destination input hashes were verified. `raw/` retains the five PANGAEA files
and the original Nature source workbook; `aligned/` retains the initial
derivation, `aligned-v2/` adds the weathering flags, and `aligned-v3/` also
contains the original Pacific percentages joined to sample metadata.
Raw or derived rows are not checked
into Git. PANGAEA declares **CC BY-NC-ND 3.0** on the two Alvarez tables and
**CC BY 4.0** on the three Jones tables. Respect the individual terms, including
any restriction on distributing adaptations; the aggregate checks below are not
a grant of permission to redistribute the joined material.

| Deposit | What was used | Licence as stated by provider |
| --- | --- | --- |
| [Alvarez Table A](https://doi.org/10.1594/PANGAEA.893899) | selected taxon percentages, interpolated at 13-kyr spacing | CC BY-NC-ND 3.0 |
| [Alvarez Table E](https://doi.org/10.1594/PANGAEA.893919) | individual sample labels, depths and ages, not raw species counts | CC BY-NC-ND 3.0 |
| [Alvarez Figure 1 source workbook](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41586-019-1590-8/MediaObjects/41586_2019_1590_MOESM2_ESM.xlsx) | original sample-level percentages and metadata | no reuse licence established in the workbook; private copy |
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
  hole E cores 3 and 4. [Jones et al. (2026), section 2.3](https://doi.org/10.1029/2026PA005729),
  exclude nannofossil samples in the weathered top of hole E above 51.32 mcd
  and hole C above 17.47 mcd because of downhole contamination and poor
  preservation. All 13 unmatched samples fall in the hole-E interval at
  49.32–51.27 mcd; none of the 186 matched samples is in either stated interval.
  This exact match supports the published quality exclusion as the explanation;
  it is an inference from the depth rule, not a sample-by-sample author receipt.
  They remain in the private alignment with a quality flag, missing ages and
  dominant-category percentages, not zeroes, and are not valid substitutes
  for the published analysis samples.
- Jones's count and percentage columns match to rounding under their stated
  row totals (maximum absolute discrepancy less than 0.000001 percentage
  points for nonblank cells). This checks the tabular arithmetic, not whether
  the categories capture the same organisms or sampling effort as the Pacific.
- Both published Jones age columns are kept: they differ for 105/186 dated
  samples, by a median absolute 0.890 kyr and maximum 15.167 kyr. These are
  differences between the two supplied model outputs, not age uncertainty
  intervals. No age is assigned to the 13 raw-only rows.
- The two age columns do not describe all stratigraphic uncertainty. Jones
  et al. report an unconformity exceeding approximately 500 kyr with unknown
  missing duration, and describe ages younger than 62.54 Ma as poorly
  constrained. Those limitations must accompany any comparison of event times;
  the 15.167-kyr maximum column difference is not a full uncertainty bound.
- Alvarez Table A has 997 interpolated time points and 25 reported categories,
  not 997 independent samples. Table E has 990 distinct sample labels: 979
  from holes at Site 1209 and **11 from Site 1210**. The Nature Figure 1
  workbook supplies 990 original sample records, with 60 abundance columns,
  and joins one-to-one to Table E. Its original rows retain 31,159 blank cells
  and 15,867 explicit zeroes across those columns; blanks are not recoded as
  zero. Depths agree within the provider's 0.005-m rounding and ages within
  0.5 kyr, with a 1e-8 numerical allowance for Excel floating-point artefacts.
  Those checks establish correspondence, not age-model accuracy.
- The workbook contains percentages, not the original integer counts or
  denominators. Alvarez et al.'s accepted manuscript reports counts of 500–1,000
  liths per sample and genus/morphogroup identifications; reconstructing counts
  from rounded percentages and unknown denominators would add assumptions.
  The manuscript describes 981 samples for the figure/series, whereas the
  source workbook and Table E contain 990 rows; the difference is unresolved.
  Workbook contributor codes cover 741, 238 and 11 samples, spanning different
  time intervals; investigator and time are therefore potentially confounded.
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
python3 data/kpg-plankton-alignment/align_pacific.py INPUT_DIR/41586_2019_1590_MOESM2_ESM.xlsx INPUT_DIR/pangaea-893919.txt OUTPUT_DIR
python3 -m unittest discover -s data/kpg-plankton-alignment -p 'test_*.py' -v
```

The input directory must contain the five original `pangaea-<id>.txt` files.
The script requires unique Jones sample keys, checks that dated count and
percentage keys and ages agree, tests the count/percentage arithmetic, retains
unmatched raw keys, and writes a private table for each site plus aggregate
summary. `align_pacific.py` reads the fixed source workbook using the Python
standard library and matches original samples to Table E. It retains the raw
workbook values and Excel row numbers, normalises a leading `U` in the site
code and tiny floating-point artefacts in centimetre labels for matching only,
and checks sample uniqueness and depth/age agreement. The
[El Kef summary](summary.json) and [Pacific summary](pacific-original-summary.json)
give hashes and aggregate checks; tests cover missing versus zero values,
unmatched or duplicate keys and inconsistent depths or ages.

The next scientific step is to resolve the sample-count discrepancy and, if
integer counts are needed, locate their source, then establish a defensible
common taxonomy and age alignment and an independently measured outcome. The
current tables do not establish comparable independent perturbations and
should not be fitted as a test of ecological memory.
