# Q-038 data contract: Monarrez, Heim & Payne 2023 deposit

Owner: Claude | Built 11 October 2026 | Status: **data contract and diagnostic; not a replication**

Q-038 asks how predictable it is which genera disappear. Given the incoming
cohort and the number of extinctions in a stage, how much do pre-event traits
and clade history improve held-out prediction over Raup's field of bullets
(uniform random loss)? Does that differ in mass extinctions?

The planned base is the deposit of Monarrez, Heim & Payne 2023, "Reduced
strength and increased variability of extinction selectivity during mass
extinctions", R Soc Open Sci (10.1098/rsos.230795). Barry downloaded the
Dryad files, which refuse anonymous download, and lifted Q-038's deferral on
11 October (76/1515).

## Rebuild

```bash
Rscript --vanilla data/q038-monarrez-contract/inspect.R
Rscript --vanilla data/q038-monarrez-contract/flag_diagnostic.R
```

- Both scripts use base R, read the deposit as data only, and take a few
  seconds.
- Inputs (git-ignored) are in `data/raw/monarrez2023/`, extracted from
  `data/raw/dryad-downloads/doi_10_5061_dryad_931zcrjqw__v20230915.zip`
  (sha256 6d78a031a08a84c32331100531b95ca75a1a8272d9652e9aacca82d018ac7391).
- Key members:

  | File | sha256 |
  | --- | --- |
  | `encounter_history_bs_gr_5class_Big5.Rdata` | 1d0787508c568abdeeb132b06cd4659491b235c7081c4ac4f76600aa2b4a43f0 |
  | `pbdb.cleaned.classes.csv` | 239d668aa298337f659a26792b8ff50a18e9640db5a2290d737f363d0a63121d |
  | `genus.sizes.ranges.cleaned.classes.csv` | 1cf3ec5adceed18a065d127618bc590ab42c144beec86977c6efd6b1b36c471c |

- The authors' R code is Zenodo 10.5281/zenodo.7816408 (MIT). Scripts 04 and
  05a were read, not run.
- **Tracked outputs:** [summary.tsv](summary.tsv),
  [flag_alignment.tsv](flag_alignment.tsv) and
  [flag_diagnostic.tsv](flag_diagnostic.tsv).

## Contract

| Item | Finding |
| --- | --- |
| Unit | One row per genus (object `ds`, 6,562 rows × 272 columns). Fields: `genus`, `class`, `ch`, `logvol`, `mass.ext1–86`, `rec.mass1–86`, `range1–87` |
| Capture histories | **Intact in the Rdata**: character strings, all 86 occasions long, 0/1 only. The float corruption is confined to the Zenodo spreadsheet copy (ESM Dataset S1) |
| Occasions | 86 stages, Tremadocian (485.4 Ma) to 1 Ma, ordered oldest first. The occasion index maps to stage bases in the cleaned PBDB file: index 38 is the Changhsingian, 39 the Induan |
| Classes | Bivalvia 1,600; Gastropoda 1,762; Rhynchonellata 1,827; Strophomenata 823 (to occasion 43); Trilobita 550 (to occasion 38) |
| Subgenus duplication | 811 of the 6,562 rows are subgenus-style names, 769 of which also have a base-genus row. Mostly Bivalvia (330) and Gastropoda (394). Effective independent genera are fewer |
| Range covariate | Maximum great-circle distance of palaeocoordinates within the stage, log10, standardised by class and stage. **Aligned with occasions**: non-zero exactly when the genus is present (mean absolute value 0.89 present against 0 absent; misaligned by one occasion it would be 0.51 against 0.02). Range at stage k − 1, a strictly prior predictor, is available directly from these columns |
| Body size | One value per genus (`logvol`); possible use of information from after the event not assessed |
| Order and family | In `genus.sizes.ranges.cleaned.classes.csv`, missing for 8.1% and 5.5% of rows |
| Occurrences | `pbdb.cleaned.classes.csv`: 253,747 rows read, against 284,309 stated in the deposit README (unresolved). Palaeocoordinates come from the `gp_mid` model and are missing for 5.9% |

## Flag alignment: an apparent offset of one interval

**What the deposit and code show.**
- Script 04 sets `mass.ext` = 1 on the columns whose stage *base* ages are
  443.4, 372.2, 252.17, 201.3 and 66 Ma. These are the Rhuddanian, Famennian,
  Induan, Hettangian and Danian: occasions 8, 22, 39, 46 and 69, each the
  **first stage after** its extinction.
- Script 05a fits RMark `Pradsen` models with `Phi ~ time + range * mass.ext`
  (and variants), using `process.data` defaults.

**How RMark matches the flag** (current CRAN source, 3.1.0).
- In `inst/parameters.txt`, `Pradsen Phi` has `begin = 0`, an
  interval-type parameter.
- `compute.design.data.R` labels such parameters from the starting occasion
  (lines 236–242).
- The `make.mark.model` documentation says: "survival is labeled based on the
  beginning of the time interval ... so the variables should be named
  appropriately for the parameter model in which they will be used".
- The flag on occasion 39 therefore enters Phi for the interval from occasion
  39 to 40 (Induan to Olenekian). The end-Permian extinction interval,
  Changhsingian to Induan (Phi from occasion 38), carries `mass.ext` = 0.

**What the data say about where the extinctions are.** Last occurrences peak
in the stage *before* each flag:

| Flagged occasion | Last occurrences at k − 1 | at k | at k + 1 |
| --- | --- | --- | --- |
| 8 | 87 | 25 | 28 |
| 22 | 129 | 83 | 73 |
| 39 | 305 | 51 | 7 |
| 46 | 108 | 8 | 11 |
| 69 | 180 | 72 | 15 |

**Diagnostic** ([flag_diagnostic.R](flag_diagnostic.R)).
- Setup: per class and interval, a logistic regression of "last occurrence at
  k" on range at k, among genera present at k. It ignores imperfect detection,
  so it is not the published model.
- The flagged intervals hold small cohorts with few losses; the true
  extinction intervals hold most of them. End-Permian Rhynchonellata: 99 last
  occurrences among 119 genera in the Changhsingian, against 15 of 23 in the
  Induan. End-Permian Strophomenata: 120 of 139 against 19 of 20.
- Range slopes at the true extinction intervals are often weaker than the
  background median (about −0.7 to −0.8 log-odds per SD). Examples: Bivalvia
  at the K–Pg, −0.24 (SE 0.11); Gastropoda at the K–Pg, +0.19 (0.19).
- Some are strong: Strophomenata at the end-Permian, −1.57 (0.54);
  Rhynchonellata at the Late Devonian, −0.84 (0.21), and at the end-Permian,
  −0.80 (0.34).

**Status of this finding.**
- On the deposited code and RMark's documented convention, the published
  "mass extinction" Phi coefficients appear to describe survival *out of* the
  first post-extinction stage. The extinction intervals themselves appear to
  be pooled with background.
- This has not been confirmed by refitting the CMR models, which need the
  external MARK program and, per the authors' code, about 96 hours per class.
  Whether the paper's conclusion of reduced range selectivity changes is
  therefore unknown.
- The recovery flags (`rec.mass` at occasions 9, 23, 40, 47 and 70, on Gamma
  with the same labelling) may have a similar issue. Not assessed.
- Any contact with the authors needs Barry's authorisation (AGENTS.md).

## Consequences for Q-038

- **Data access is resolved.** The capture histories are intact, the range
  covariate is aligned, and range at k − 1 is available from the deposited
  columns.
- **Event intervals must be redefined.** Define each event as the interval
  ending at the boundary (start occasions 7, 21, 38, 45 and 68). Do not reuse
  the deposited `mass.ext` flags.
- **Collapse subgenus duplicates** to base genera, or treat them explicitly.
- Rhynchonellata and Bivalvia remain the candidates spanning all five events.
  Strophomenata spans the first three and Trilobita the first two.
- The cleaned file's row count disagrees with the README. Audit it before
  using the file for anything beyond palaeocoordinates.
