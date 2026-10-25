---
id: legacypollen
name: LegacyPollen 1.0 and 2.0 and LegacyAge 1.0, harmonised global late Quaternary pollen with Bacon chronologies (PANGAEA)
kind: compilation
status: active
last_update: 2026-10-25
scope:
  taxa: ["terrestrial pollen and spores, harmonised to genus for woody and major herbaceous taxa and to family for the rest (987 count columns in 1.0)"]
  time: "late Quaternary, mostly the last 30 ka (Bacon chronologies in cal. yr BP)"
  space: "global: 2.0 has Europe 1,446 records, eastern North America 705, Asia 687, western North America 417, South America 185, Africa 159, Indopacific 81 (59 in the Sahul boxes)"
  record_unit: "a pollen sample (one depth in one record) with harmonised counts and a modelled age with its 95% range"
size:
  as_of: "PANGAEA snapshot 2026-10-25T0317Z"
  v1_records: 2831
  v1_count_records: 2676
  v2_records: 3680
  v2_samples: 211167
  legacyage_control_points: 19990
access:
  tier: open
  licence: "CC BY 4.0 (each PANGAEA record)"
  routes:
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.929773", state: "LegacyPollen 1.0 (2021): seven regional zips of count and percentage tables, site metadata, taxa harmonisation table; mirrored", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.933132", state: "LegacyAge 1.0 (2021): control points, prior information, Bacon settings, chronologies (age quantiles per depth), comparison with original chronologies, references, readme; mirrored", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.931920", state: "full age data for the African records (Li et al. 2026): min, max, median and mean age per sample; mirrored. No other region's full age data was found", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.965907", state: "LegacyPollen 2.0 (2025), 'in review' on PANGAEA: review zip, harmonisation table, overview (971802) and seven regional count tables mirrored; percentage tables not mirrored", checked: 2026-10-25}
  api: "PANGAEA (doi.pangaea.de ?format=textfile and metainfo_xml; download.pangaea.de attachments)"
versioning:
  replay: partial
  notes: "LegacyPollen 1.0 and LegacyAge 1.0 are fixed published records; 2.0 is in review and may change before publication, so its snapshot here is dated; the Legacy family's vegetation, REVEALS and climate reconstructions are separate records, not mirrored"
mirror:
  path: deep-server:/data/paleodata/legacypollen
  policy: "1.0, LegacyAge 1.0 with the African full age data, and 2.0's counts and overview"
  state: "v1: 9 files (54 MB); legacyage: 11 files (149 MB); v2: 10 files (230 MB); sha256 recorded; all verify"
lineage:
  upstream:
    - "Neotoma Paleoecology Database records, Cao et al. (2013, 2020) Asian compilations and AWI's own data, harmonised and re-dated by the Herzschuh group (AWI Potsdam)"
  downstream:
    - "the Northern Hemisphere climate reconstruction (PANGAEA 930512), LegacyVegetation and REVEALS reconstructions (PANGAEA 961588, 961699, 974798 and others); BioDeepTime (median ages only, per Q-024)"
eprp_questions: [Q-024]
citation:
  - "Herzschuh, U. et al. (2022) LegacyPollen 1.0: a taxonomically harmonized global late Quaternary pollen dataset of 2831 records with standardized chronologies. Earth System Science Data 14: 3213-3227, doi:10.5194/essd-14-3213-2022 (pages recall)"
  - "Li, C. et al. (2022) Harmonized chronologies of a global late Quaternary pollen dataset (LegacyAge 1.0). Earth System Science Data 14: 1331-1343, doi:10.5194/essd-14-1331-2022 (pages recall)"
  - "Li, C. et al. (2025) LegacyPollen2.0: an updated global taxonomically and temporally standardized fossil pollen dataset of 3680 palynological records. PANGAEA, doi:10.1594/PANGAEA.965907 (in review)"
  - "Herzschuh, U. et al. (2021) LegacyPollen 1.0, PANGAEA, doi:10.1594/PANGAEA.929773; Li, C. et al. (2021) LegacyAge 1.0, PANGAEA, doi:10.1594/PANGAEA.933132"
entry:
  created: 2026-10-25
  updated: 2026-10-25
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# LegacyPollen and LegacyAge

## Summary

The Herzschuh group at AWI Potsdam has harmonised the world's fossil pollen
records to one taxonomy and re-dated every record with Bacon from its
original control points. LegacyPollen 1.0 (2021) holds 2,831 records,
LegacyPollen 2.0 (2025, still "in review" on PANGAEA) holds 3,680, and
LegacyAge 1.0 publishes the chronologies with their inputs. Q-024 asks
whether early-warning indicators work on real Quaternary transitions, and
this is its named data source. It is the only global pollen compilation
with uniform taxonomy and uniform age models. It also ships what is needed
to rebuild age ensembles:
- 19,990 control points;
- the prior information;
- each record's Bacon settings.

That matters because only age quantiles are published: no ensemble draws.
Screening against the register's thresholds, 2.0 has 446 records with 100
or more samples (259 of them sampled every 100 years or finer). Only 15
reach 450 samples, the length above which Dakos et al. 2008 found strong
signals. The ≥30-transition kill criterion therefore looks reachable only
with the 100-sample class. Reach for it for the Northern Hemisphere and for
calibration studies; it is thin for the Sahul region (59 records, against
167 Sahul pollen datasets in Neotoma).

## Contents

[Profile](profile/legacypollen_profile.tsv); per record and version in
[the records table](profile/legacypollen_records.tsv).

| | LegacyPollen 1.0 | LegacyPollen 2.0 |
| --- | ---: | ---: |
| records | 2,831 (2,676 with counts; 155 percentages only) | 3,680 |
| samples in the count tables | 148,431 | 211,167 |
| median samples per record (quartiles) | 43 (27–68) | 43 (25–69) |
| records with 50 / 100 / 450+ samples | 1,132 / 305 / 5 | 1,555 / 446 / 15 |
| 100+ samples and median spacing ≤ 100 yr / ≤ 200 yr | 210 / 264 | 259 / 320 |
| 450+ samples and spacing ≤ 50 yr | 4 | 8 |
| median spacing between samples (median over records) | 165 yr | 150 yr |
| median pollen sum per sample (median over records) | 384 | 361 |
| Sahul region (100+ samples) | 21 (5) | 59 (7) |

1.0 has records from Europe (1,075 with counts), eastern North America
(670), western North America (362), Asia (333), South America (150), Africa
(54) and the Indopacific (32). Of the 1.0 records with counts, 2,643 are in
2.0 under the same dataset id, 33 are not, and 2.0 adds 1,037.

LegacyAge 1.0 holds:
- **Control points:** 19,990 for all 2,831 records, by method radiocarbon
  17,215, prior information 1,705, ²¹⁰Pb 999, luminescence 50, U-series 17,
  Ar–Ar 3, cosmogenic 1. A record has a median of 5 dates (quartiles 4–8);
  277 have fewer than 3.
- **Bacon settings:** for 2,823 records.
- **Chronology table:** age quantiles at 1,483,815 depths in 2,742 records.
  The median record-mean width of the 95% age range is 280 yr (quartiles
  178–396).
- **Comparison with the original chronologies:** within the new 95% range
  for 1,011 records, partly or wholly outside it for 914, and no original
  calibrated chronology for 906.

## Provenance and lineage

The records come from the Neotoma Paleoecology Database, the Asian
compilations of Cao et al. (2013, 2020) and AWI's own data (LegacyAge
readme). The group harmonised the taxa to 987 count columns, recalibrated
the control points (mostly IntCal20) and ran Bacon 2.5.3 with predefined
settings (Li et al. 2022, source claim). 2.0 adds records and Neotoma DOIs
and re-estimates chronologies. For the 2,643 records in both versions the
oldest median age moved by more than 0.5 kyr in only 43, and by 0.003 kyr at
the median. The family continues into LegacyVegetation, REVEALS and
LegacyClimate reconstructions, which are separate PANGAEA records.

## Structure

- **1.0 regional zips:** `pollen_counts_<region>.csv` and
  `pollen_percentages_<region>.csv`, each with a `.txt` twin. One row is one
  sample: `Event`, `Data_Source`, `Site_ID`, `Dataset_ID`, `Site_Name`,
  coordinates, `Continent`, `AgeModel_Source`, the minimum, maximum, median
  and mean age (cal. ka BP), `Depth (m)`, then one `Taxon (#)` column per
  harmonised taxon. The ".csv" files are **tab**-separated with quoted
  fields.
- **1.0 metadata table:** one row per record with archive type, site
  description and up to eight publications and DOIs.
- **LegacyAge tables (S1–S7, tab-separated; the readme says semicolons):**
  - S1, the control points: laboratory code, method, material, raw and
    calibrated ages with errors, depth, thickness;
  - S2, prior information;
  - S3, the Bacon settings: memory, resolution, starting age, accumulation
    mean, hiatuses, and added ages;
  - S4, the original chronologies;
  - S5, the chronology: `Age_Minimum`, `Age_Maximum`, `Age_Median`,
    `Age_Mean` and `Uncertainty_Each.depth`, all over the 95% range in
    cal. yr BP;
  - S6, the comparison with the original chronologies;
  - S7, the references.
  The PANGAEA table 933132 summarises each record.
- **2.0:** regional count tables in PANGAEA's tab format (a `/* … */`
  header, then one row per sample with `Sample label`, Neotoma DOI,
  coordinates, ages, depth and taxa). There is an overview with one row per
  record (sample count, datings, age span, resolution, source). The
  `ReviewVersion.zip` holds a 47 MB tar of the review files.
- **African full age data (931920):** min, max, median and mean age for
  41,041 samples.

## Access

- **Mirror.** `deep-server:/data/paleodata/legacypollen/{v1,legacyage,v2}/raw/2026-10-25T0317Z_url/`
  with manifests; [snapshots.tsv](snapshots.tsv).
- **Refresh.** [legacypollen_snapshot.sh](legacypollen_snapshot.sh) `[v1]
  [age] [v2]`. 2.0 should be re-snapshotted when PANGAEA publishes it.
- **Profile.** `python3 legacypollen_profile.py V1_DIR AGE_DIR V2_DIR
  OUT_TSV RECORDS_TSV` ([profiler](legacypollen_profile.py)).
- **Rebuilding age ensembles.** Rerun Bacon (R package `rbacon`) per record
  from S1 (dates), S2 (priors) and S3 (settings). LegacyAge's own R code is
  described in the readme. Not run here.

## Strengths

- One taxonomy and one age-modelling procedure across thousands of records,
  with every input published.
- Q-024's screening classes are well populated: 446 records of 100+ samples
  in 2.0, 259 of them at 100-year spacing or finer.
- Open (CC BY 4.0) and versioned on PANGAEA.

## Weaknesses and pitfalls

- **No ensembles.** Only age quantiles per depth are published (min, max,
  median and mean of the 95% range). Q-024's age-model ensembles must be
  regenerated with Bacon from the published inputs (not run here).
- **Few long series.** 15 records in 2.0 (5 in 1.0) have 450 or more
  samples. Indicator calibration with Dakos-length series rests on very few
  sites.
- **2.0 is in review.** Its tables may change before publication; cite the
  snapshot date.
- **Counts versus percentages.** 155 records in 1.0, mainly from the Asian
  compilations (inferred from the sources), exist only as percentages.
  Analyses needing counts lose them.
- **Format traps.** The ".csv" files are tab-separated, and the readme's
  "semicolon" is wrong for these copies. PANGAEA tab files start with a
  long `/* … */` header.
- **Sahul is thin.** 59 records in 2.0 fall in the Australia and New Guinea
  boxes, 7 of them with 100+ samples. Neotoma's Sahul holdings
  ([neotoma](../neotoma/README.md)) are the fuller source there.
- **Harmonisation loses resolution.** Herbaceous taxa are merged to family.

## Overlap with other sources

- **[neotoma](../neotoma/README.md).** Most records come from Neotoma; 2.0
  carries Neotoma DOIs. For Sahul, Neotoma has 167 pollen datasets against
  59 here.
- **[register-deposits](../register-deposits/README.md).** BioDeepTime
  (Smith et al. 2023) carries pollen series with median ages only (per the
  Q-024 entry).

## EPRP relevance

- **Q-024.** This is the data source the register names. Support counts
  for its screening:
  - 446 records (2.0) with 100+ samples, 259 of them with median spacing of
    100 years or less;
  - 15 records with 450+ samples;
  - complete Bacon inputs for regenerating age ensembles.
  Whether 30 transitions survive screening depends on the transition
  definition, which is not tested here.
- Cannot support: ensemble ages without rerunning Bacon, or Sahul analyses
  needing many long records.

## Citation and terms

CC BY 4.0 on every PANGAEA record. Cite the ESSD papers (Herzschuh et al.
2022; Li et al. 2022), the PANGAEA DOIs of the versions used, and the
original records' publications (1.0 metadata table, LegacyAge S7).

## Verification log

- 2026-10-25 (Claude, Opus 5.5):
  - *checked*: read PANGAEA's metadata for the family; mirrored 1.0, LegacyAge
    1.0 with the African full age data, and 2.0's counts, overview and review
    zip; all verify;
  - *checked*: profiled all three ([profile](profile/legacypollen_profile.tsv)):
    record and sample counts, screening classes, spacing, pollen sums,
    LegacyAge dates, settings and uncertainties, the 1.0-to-2.0 overlap, the
    Sahul counts, and the field delimiters;
  - *source claim*: Bacon 2.5.3 and IntCal20 (Li et al. 2022); 2.0's review
    status and record count (PANGAEA);
  - *inferred*: that the percentage-only records are the Asian
    compilations'.
