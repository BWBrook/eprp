---
id: legacypollen
name: LegacyPollen 1.0 and 2.0 and LegacyAge 1.0, harmonised global late Quaternary pollen with Bacon chronologies (PANGAEA)
kind: compilation
status: active
last_update: 2025-07-15
scope:
  taxa: ["pollen taxa harmonised to genus (woody and major herbaceous taxa) or family (other herbs); spores, Sphagnum, aquatics such as Typha and Potamogeton, and algae are deleted by the harmonisation table; 987 count columns in 1.0, incl. Indeterminable"]
  time: "late Quaternary, mostly the last 30 ka (chronologies in cal. yr BP)"
  space: "global: 2.0 has Europe 1,446 records, eastern North America 705, Asia 687, western North America 417, South America 185, Africa 159, Indopacific 81 (59 in the Sahul boxes)"
  record_unit: "a pollen sample (one depth in one record) with harmonised counts and a modelled age with its 95% range"
size:
  as_of: "PANGAEA snapshot 2026-10-25T0317Z"
  v1_records: 2831
  v1_count_records: 2676
  v2_records: 3680
  v2_records_with_ages: 3074
  v2_samples: 211167
  legacyage_control_points: 19990
access:
  tier: open
  licence: "CC BY 4.0 (each PANGAEA record)"
  routes:
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.929773", state: "LegacyPollen 1.0 (2021): seven regional zips of count and percentage tables, site metadata, taxa harmonisation table; mirrored", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.933132", state: "LegacyAge 1.0 (2021): control points, prior information, Bacon settings, chronologies (age quantiles per 1-cm depth), comparison with original chronologies, references, readme; mirrored", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.931920", state: "full age data for 46 African records (Li et al. 2026): age quantiles at 1-cm model depths; mirrored. One PANGAEA search found no other region's table", checked: 2026-10-25}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.965907", state: "LegacyPollen 2.0 (published 2025-02-05, modified 2025-07-15): overview (971802) and seven regional count tables mirrored, with the superseded review zip; percentage tables not mirrored", checked: 2026-10-25}
  api: "PANGAEA (doi.pangaea.de ?format=textfile and metainfo_xml; download.pangaea.de attachments)"
versioning:
  replay: exact
  notes: "1.0, LegacyAge 1.0 and 2.0 are fixed published PANGAEA records, mirrored as dated snapshots; 2.0's review zip is an earlier state (3,728 records, per the review); the family's vegetation, REVEALS and climate reconstructions are separate records, not mirrored"
mirror:
  path: deep-server:/data/paleodata/legacypollen
  policy: "1.0, LegacyAge 1.0 with the African full age data, and 2.0's counts and overview"
  state: "v1: 9 files (54 MB); legacyage: 11 files (149 MB); v2: 10 files (230 MB); sha256 recorded (no provider checksums); all verify"
lineage:
  upstream:
    - "Neotoma Paleoecology Database records, the Asian compilations of Cao et al. (2013, 2020) and AWI's own data, harmonised and re-dated by the Herzschuh group (AWI Potsdam)"
  downstream:
    - "the Northern Hemisphere climate reconstruction (PANGAEA 930512), LegacyVegetation and REVEALS reconstructions (PANGAEA 961588, 961699, 974798 and others); BioDeepTime (median ages only, per Q-024)"
eprp_questions: [Q-024]
citation:
  - "Herzschuh, U. et al. (2022) LegacyPollen 1.0: a taxonomically harmonized global late Quaternary pollen dataset of 2831 records with standardized chronologies. Earth System Science Data 14: 3213-3227, doi:10.5194/essd-14-3213-2022 (pages recall)"
  - "Li, C. et al. (2022) Harmonized chronologies of a global late Quaternary pollen dataset (LegacyAge 1.0). Earth System Science Data 14: 1331-1343, doi:10.5194/essd-14-1331-2022 (pages recall)"
  - "Li, C. et al. (2025) LegacyPollen2.0: an updated global taxonomically and temporally standardized fossil pollen dataset of 3680 palynological records. PANGAEA, doi:10.1594/PANGAEA.965907; supplement to Li et al. (2025), Climate of the Past 21: 1001-1024 (per PANGAEA, via the review)"
  - "Herzschuh, U. et al. (2021) LegacyPollen 1.0, PANGAEA, doi:10.1594/PANGAEA.929773; Li, C. et al. (2021) LegacyAge 1.0, PANGAEA, doi:10.1594/PANGAEA.933132"
entry:
  created: 2026-10-25
  updated: 2026-10-25
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-25, independent Claude Sonnet subagent; findings applied"
---

# LegacyPollen and LegacyAge

## Summary

The Herzschuh group at AWI Potsdam harmonised the world's fossil pollen
records to one taxonomy and, for most of them, built new Bacon age-depth
models from the original control points. LegacyPollen 1.0 (2021) holds
2,831 records and LegacyPollen 2.0 (published 2025) holds 3,680. LegacyAge
1.0 publishes the chronologies of 1.0 with their inputs. For Q-024, which
asks whether early-warning indicators work on real Quaternary transitions,
this is the named data source. Three facts set its limits.

**Fewer long, dated series than the headline counts suggest.**
- 606 of 2.0's 3,680 records carry no ages in the count tables. These are
  the records whose chronologies come from other sources (Zhou et al.,
  ACER, Neotoma originals; review).
- With ages, 2.0 has 345 records of 100 or more samples, and 259 of those
  have a median gap of 100 years or less between samples (202 by mean gap).
- Only 8 records reach 450 samples, the length above which Dakos et al.
  2008 found strong signals.

**Age uncertainty is large relative to sampling.** The 95% age range
averages a median of 949 years per record, about six times the median
sample gap of 150 years. Q-024's age-model ensembles must therefore drive
the analysis, not decorate it.

**No ensembles, and the inputs cover only 1.0.**
- Only age quantiles are published.
- Ensembles must be rebuilt with Bacon from LegacyAge's control points (S1)
  and settings (S3). Those exist for 1.0's records only.
- Of the 259 well-sampled 2.0 records, 204 have them, and the other 55 have
  no published Bacon inputs.

It is thin for the Sahul region: 59 records in 2.0, against 167 Sahul pollen
datasets in Neotoma.

## Contents

[Profile](profile/legacypollen_profile.tsv); per record and version in
[the records table](profile/legacypollen_records.tsv).

| | LegacyPollen 1.0 | LegacyPollen 2.0 |
| --- | ---: | ---: |
| records | 2,831 (2,676 with counts; 155 percentages only, all Asian, 154 from Cao et al.) | 3,680 (3,074 with ages) |
| samples in the count tables | 148,431 | 211,167 |
| median samples per record (quartiles) | 43 (27–68) | 43 (25–69) |
| records with 50 / 100 / 450+ samples, with ages | 1,132 / 305 / 5 | 1,313 / 345 / 8 |
| 100+ samples and median gap ≤ 100 yr (mean gap ≤ 100 yr) | 210 (157) | 259 (202) |
| 100+ samples and median gap ≤ 200 yr | 264 | 320 |
| 450+ samples and median gap ≤ 50 yr | 4 | 8 |
| median gap between sample ages (median over records) | 165 yr | 150 yr |
| median sum of all count columns per sample (incl. Indeterminable) | 384 | 361 |
| Sahul region (100+ samples) | 21 (5) | 59 (7) |

Gaps are taken between successive median ages. 2.0's ages are rounded to
0.01 ka, and a few records repeat depths (review); neither changes the
classes materially.

**From 1.0 to 2.0.**
- Of all 2,831 records in 1.0, 2,789 are kept, 42 are dropped and 2.0 adds
  891.
- 146 of the 155 percentage-only records have counts in 2.0.
- Ages are carried over. In the 2,643 shared count records, 133,920 of
  134,308 samples matched by depth (99.7%) have the same median age, and
  only 8 records have a matched sample that moved by more than 0.5 kyr.
- Coordinates changed for 83 shared records by more than 1 km, and for 3 by
  more than 100 km. For example, id 788 (Elikchan 4) moves from north-east
  Siberia to the Urals, and id 336 (Candelabra Lake) from Yukon to Quebec
  (review).

**LegacyAge 1.0.**
- **Control points:** 19,990 for all 2,831 records. By method: radiocarbon
  17,215, prior information 1,705, ²¹⁰Pb 999, luminescence 50, U-series 17,
  Ar–Ar 3, cosmogenic 1.
- **Measured dates per record** (prior information excluded): median 5,
  quartiles 3–8; 429 records have fewer than 3.
- **Bacon settings:** for 2,823 records.
- **New chronologies:** AWI Bacon chronologies for 2,742 records. The other
  89 keep their original chronologies (Neotoma 71 and others, Cao et al. 18)
  and are not in the chronology table.
- **Chronology table:** age quantiles at 1,483,815 depths (1-cm steps).
  The width of the 95% age range, averaged over each record's depths, has a
  median of 949 years (quartiles 632–1,405).
- **`Uncertainty_Record.mean`:** not that mean width but about 0.28 of it.
  The readme does not say how it is computed.
- **Against the original chronologies:** the original lies within the new
  95% range for 1,011 records, partly or wholly outside it for 914, and 906
  had no original calibrated chronology.

## Provenance and lineage

The records come from the Neotoma Paleoecology Database, the Asian
compilations of Cao et al. (2013, 2020) and AWI's own data (LegacyAge
readme). The group harmonised the taxa and recalibrated the control points
(mostly IntCal20). It then ran Bacon with predefined settings (Li et al.
2022; Bacon 2.5.3 per the paper, source claim not verified here). 2.0 adds
records and Neotoma DOIs and carries 1.0's ages over. PANGAEA lists it as a
supplement to Li et al. (2025) in *Climate of the Past*. The family
continues into LegacyVegetation, REVEALS and climate reconstructions, which
are separate PANGAEA records.

## Structure

- **1.0 regional zips:** `pollen_counts_<region>.csv` and
  `pollen_percentages_<region>.csv`, each with a `.txt` twin. One row is one
  sample: `Event`, `Data_Source`, `Site_ID`, `Dataset_ID`, `Site_Name`,
  coordinates, `Continent`, `AgeModel_Source` (AWI 2,604, Neotoma 71, Cao
  et al. 1 among count records), the minimum, maximum, median and mean age
  (cal. ka BP), `Depth (m)`, then one `Taxon (#)` column per harmonised
  taxon. The ".csv" files are tab-separated with quoted fields.
- **1.0 metadata:** one row per record, with archive type, site
  description, and up to eight publications and DOIs. The taxa
  harmonisation table is comma-separated and maps each original name to a
  harmonised name or "Delete".
- **LegacyAge:**
  - S1, the control points: laboratory code, method, material, raw and
    calibrated ages with errors, depth, thickness;
  - S2, prior information (category codes and free text);
  - S3, the Bacon settings: memory, resolution, starting age, accumulation
    mean, hiatuses, added ages. No calibration curve, Bacon version or seed
    is recorded;
  - S4, the original chronologies;
  - S5, the chronology: `Age_Minimum`, `Age_Maximum`, `Age_Median`,
    `Age_Mean`, and `Uncertainty_Each.depth`, which equals maximum minus
    minimum;
  - S6, the comparison and each record's chronology source;
  - S7, the references.

  The tables are tab-separated. The Bacon parameter description is
  semicolon-separated, as the readme says of all files. PANGAEA table 933132
  summarises each record.
- **2.0 regional count tables:** PANGAEA tab format (a `/* … */` header,
  then one row per sample with `Sample label`, Neotoma DOI, coordinates,
  ages, depth and taxa). They hold 28,987 literal replacement characters
  (U+FFFD) in site and taxon text, so join on ids, not names.
- **2.0 overview (971802):** 3,404 rows, so 276 records are missing from
  it. Its Age and Time-res headers say [ka], but the values are in years
  (review).
- **`ReviewVersion.zip`:** the superseded version used in the article's
  review, a 47 MB tar holding 3,728 records (review).
- **African full age data (931920):** age quantiles for 46 records at 1-cm
  model depths (41,041 rows; review). S5 already gives every depth for every
  1.0 record.

## Access

- **Mirror.** `deep-server:/data/paleodata/legacypollen/{v1,legacyage,v2}/raw/2026-10-25T0317Z_url/`
  with manifests. The plain-URL route records sha256 only, because PANGAEA
  gives no checksums. [snapshots.tsv](snapshots.tsv).
- **Refresh.** [legacypollen_snapshot.sh](legacypollen_snapshot.sh) `[v1]
  [age] [v2]`.
- **Profile.** `python3 legacypollen_profile.py V1_DIR AGE_DIR V2_DIR
  OUT_TSV RECORDS_TSV` ([profiler](legacypollen_profile.py)).
- **Rebuilding age ensembles.** Rerun Bacon (R package `rbacon`) per record
  from S1 (dates) and S3 (settings), choosing the calibration curve and a
  seed, which S3 does not record. This covers the 2,823 records with
  settings, all from 1.0. `rbacon` is not installed on deep-server (review),
  and nothing was run here.

## Strengths

- One taxonomy, and one age-modelling procedure for 2,742 records, with its
  inputs published.
- Q-024's screening classes are populated: 345 dated records of 100+ samples
  in 2.0, 259 with a median gap of 100 years or less.
- Open (CC BY 4.0), with fixed published versions on PANGAEA.

## Weaknesses and pitfalls

- **Missing ages in 2.0.** 606 records carry no ages in the count tables,
  among them 101 with 100+ samples and 7 with 450+. Of these 606, 174 have
  ages in 1.0 (review).
- **No ensembles; inputs for 1.0 only.** See Summary. A 2.0-wide ensemble
  analysis would need control points for the 563 dated records outside
  LegacyAge.
- **Age uncertainty exceeds spacing.** A 949-year median 95% range against
  a 150-year median gap.
- **Few long series.** 8 dated records with 450+ samples in 2.0.
- **Not every record has a new chronology.** 89 records keep their original
  chronologies.
- **Format traps.**
  - The ".csv" files are tab-separated, and only the Bacon parameter
    description uses the readme's semicolons.
  - PANGAEA tab files start with a long `/* … */` header.
  - The 2.0 overview's [ka] headers hold years.
  - The 2.0 tables carry U+FFFD characters.
- **Shared ids can move.** 3 records' coordinates changed by more than 100
  km between versions; check coordinates when joining versions.
- **Sahul is thin.** 59 records in 2.0, 7 with 100+ samples. Neotoma
  ([neotoma](../neotoma/README.md)) is the fuller source there.
- **Harmonisation drops taxa.** Spores, Sphagnum, aquatics and algae are
  deleted, and herbaceous taxa are merged to family.

## Overlap with other sources

- **[neotoma](../neotoma/README.md).** Most records come from Neotoma, and
  2.0 carries Neotoma DOIs. For Sahul, Neotoma has 167 pollen datasets
  against 59 here.
- **[register-deposits](../register-deposits/README.md).** BioDeepTime
  (Smith et al. 2023) carries pollen series with median ages only (per the
  Q-024 entry).

## EPRP relevance

- **Q-024.** This is the data source the register names. Support counts for
  its screening:
  - 345 dated records (2.0) with 100+ samples, 259 of them with a median
    gap of 100 years or less (202 by mean gap);
  - 8 with 450+ samples;
  - Bacon inputs for regenerating age ensembles for 1.0's records, which
    cover 204 of the 259.

  The age uncertainty (median 95% range 949 years) is wide relative to the
  sampling, so ensemble propagation is essential. Whether 30 transitions
  survive screening depends on the transition definition, which is not
  tested here.
- Cannot support: ensemble ages without rerunning Bacon, ensembles for
  2.0-only records, or Sahul analyses needing many long records.

## Citation and terms

CC BY 4.0 on every PANGAEA record. Cite the ESSD papers (Herzschuh et al.
2022; Li et al. 2022), the *Climate of the Past* paper for 2.0, the PANGAEA
DOIs of the versions used, and the original records' publications (the 1.0
metadata table and LegacyAge S7). Queued for the compilers:
[CONTACTS.md](../CONTACTS.md) C35.

## Verification log

- 2026-10-25 (Claude, Opus 5.5):
  - *checked*: read PANGAEA's metadata for the family; mirrored 1.0,
    LegacyAge 1.0 with the African full age data, and 2.0's counts,
    overview and review zip; all verify.
  - *checked*: profiled all three ([profile](profile/legacypollen_profile.tsv)).
    It covers record and sample counts, aged records, screening classes by
    median and mean gap, LegacyAge dates (measured and prior), the
    95%-range widths, chronology sources, and LegacyAge coverage of 2.0. It
    also covers the depth-matched comparison of 1.0 and 2.0 ages,
    coordinate shifts, the percentage-only records, the overview's
    coverage, replacement characters and delimiters.
  - *source claim*: Bacon 2.5.3 and IntCal20 (Li et al. 2022); 2.0's
    publication dates and the *Climate of the Past* paper (PANGAEA).
  - Independent review (Claude Sonnet subagent), findings applied:
    - the 95%-range width (`Uncertainty_Record.mean` is not it);
    - records without ages in 2.0;
    - 2.0 is published, not in review (the "in review" flag belonged to a
      related paper in PANGAEA's metadata);
    - not every record was re-dated, and 2.0 carries ages over;
    - Bacon inputs cover 1.0 only;
    - the percentage-only records are Asian (Cao et al.);
    - scope (deleted taxa);
    - the overview and African table descriptions;
    - median against mean gap;
    - measured dates;
    - formats;
    - a contact row.

    Figures marked "(review)" come from the review's scripts.
