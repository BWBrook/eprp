# Q-050: what the covariance archive actually supplies

Owner: Codex. Inspected 11 October 2026. A bounded data-support check for
[Q-050](../../ideas/register.md#q-050-how-does-the-capacity-to-evolve-change-during-environmental-upheaval),
supporting the [phase-2 response](../../ideas/2026-10-11-phase2-response-codex.md).
This inspects two deposited series; it does not fit an evolutionary model.

## Finding and consequence

The archive supplies two complete numerical series of means, phenotypic
covariance matrices and specimen counts on the same 75-point elapsed-time
grid. It is sufficient to construct a sampling-design fixture. It does not
yet supply the verified joint environmental, chronological and population
support needed to distinguish Q-050's mechanisms.

| Deposited taxon label | Samples | Traits | Specimens summed across samples | Specimens per sample: min / median / max |
| --- | --- | --- | --- | --- |
| `Globoconella_puncticulata` | 75 | 2 | 6,575 | 3 / 86 / 182 |
| `Truncorotalia_crassaformis` | 75 | 2 | 6,058 | 17 / 79 / 139 |

Both grids span **474.57 kyr**. Adjacent spacings range from **4.72 to 10.07
kyr**, with median **6.18 kyr**. These are derived from the stored coordinates;
they are not age uncertainties or estimates of effective temporal resolution.
All mean/covariance values are finite. Every covariance matrix is symmetric
and positive definite at the numerical tolerances in the script. Dimensions,
sample counts and trait labels agree internally. Two samples in each series
have fewer than 20 specimens; that descriptive threshold is not a power rule.
In particular, a numerically valid covariance matrix based on three specimens
does not establish adequate precision.

**Time-field correction.** The source README describes `tt` as "time lapse
between steps", which our first-tranche note rendered as time increments.
The inspected objects instead contain an increasing elapsed-time coordinate,
starting at zero. Source `code/check_TS.R`, lines 19–23, checks that `tt`
starts at zero and strictly increases; `code/analysis.R`, line 143 (also
164, 187 and 206), uses `max(tt)` for the series duration. Thus use
`diff(tt)` for adjacent spacings in these objects. Summing their stored `tt`
would incorrectly give 18.38922 Myr instead of 0.47457 Myr. This corrects
our reading of the field; it is not a finding that the published analysis
summed it. Source values have not been changed.

## Joint support still missing from this check

Each inspected object has exactly ten fields: `nsamp`, `nvar`, `M`, `S`,
`nn`, `tt`, `time.units`, `taxon`, `sex`, `reference`. There are no explicit
absolute ages, core/depth/sample identifiers, environmental measurements,
age-error ensembles, or specimen-level observations in these objects. The
covariance dimnames identify `Area` and `Aspect_ratio`; `M` has no column
names. The README describes log-transformed traits. The original measurement
and ordering crosswalk still requires the source data and methods.

Absence of fields here is not absence of those data elsewhere. The
[original Dryad deposit](https://doi.org/10.5061/dryad.8jf2k) remains a lead
for the sample/age crosswalk, not an inspected spreadsheet in this audit.
Identical stored grids are verified; they do not independently establish
replicated populations, independent climatic perturbations or independent
dating errors. The two species are not two independent environmental
experiments merely because they occupy separate R objects.

**13 October follow-up:** the [source/support audit](../q050-sample-crosswalk/README.md)
retrieved five local environmental tables and identified shared LR04 chronology,
depth-scale and time-averaging dependencies. Scripted workbook downloads failed;
Barry subsequently supplied the file, whose size and MD5 Codex verified during
the portfolio checkpoint. The numerical crosswalk remains open and is deferred
until allocated after that checkpoint.

**Next decision:** establish a one-to-one crosswalk to original samples and
absolute ages, environmental observations, and chronology/time-averaging
provenance. Preserve shared age errors. Then specify constrained competing
models and an observation model before a recovery experiment. Until then,
simulations on this grid can test hypothetical resolution, not show that the
real data distinguish inherited constraint, selection and feedback. No model
recovery, genetic covariance inference or novelty assessment was performed.

## Source and reproduction

- Tsuboi et al. 2024 supplementary archive,
  [Zenodo record 13294509, v1.0.1](https://doi.org/10.5281/zenodo.13294509),
  associated with [10.1093/jeb/voae103](https://doi.org/10.1093/jeb/voae103).
- Retrieved anonymously through the Zenodo API on 11 October 2026. Browser
  access failed; the API metadata and file download succeeded. Access depth:
  metadata, README, selected source-code lines and the two numerical RData
  objects. The author's analysis and environment activation were not run.
- File: `NiklasHohmann/paradox_of_predictability-v1.0.1.zip`, 242,575 bytes.
  Independently computed MD5 matches the deposited checksum:
  `ab026931157f5734790be0ed732dc94b`.
  SHA-256: `46f28ed0df66333a63a7455e0321e61a7de9a06d0b8704197e8348d7876206ad`.
- Source metadata records CC BY 4.0; the bundle README names Apache 2.0.
  The scope of these statements and original dataset terms have not been
  reconciled for redistribution. The ZIP and extracted objects remain in
  ignored scratch storage; this directory contains our inspection script
  and descriptive audit output, not the deposited numerical series.

From the repository root, download the immutable version and run the base-R
inspection (checked with R 4.6.1; no additional packages):

```bash
mkdir -p scratch/q050-archive
curl --fail --location 'https://zenodo.org/api/records/13294509/files/NiklasHohmann/paradox_of_predictability-v1.0.1.zip/content' --output scratch/q050-archive/source.zip
Rscript --vanilla data/q050-covariance-support/inspect.R scratch/q050-archive/source.zip
```

[inspect.R](inspect.R) checks the pinned MD5, loads only the two named
objects into isolated R environments and writes [summary.tsv](summary.tsv).
An optional second argument writes the summary elsewhere. No source values
are repaired or rescaled in the archive. Spacings and elapsed span are
converted from Myr to kyr in the summary; the table above rounds spacings
to two decimal places. `specimen_sum` sums stored `nn`, not unique specimen
identifiers checked against the original workbook. `samples_n_lt_20` counts
thin samples; the final two fields report exact grid identity and the
specified numerical checks. These checks establish internal consistency,
not correspondence to the original specimens or scientific suitability.
An independent GPT-6.1 Sol check reran the script to a temporary output,
reproduced the tracked TSV exactly and checked both archive hashes and the
cited source-code passages. It did not validate the original measurements.
