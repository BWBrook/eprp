---
id: biotime
name: BioTIME 2.0, assemblage time series
kind: database
status: active
last_update: "2025-04-15 (Zenodo 15222193)"
scope:
  taxa: ["invertebrates, plants, fish, birds, mammals, amphibians, reptiles, fungi (study-level groups)"]
  time: "1874-2023 (sampling years)"
  space: "global: 708 studies, terrestrial 328, marine 229, freshwater 151"
  record_unit: "a taxon's abundance and/or biomass in one sample of one study in one year"
size:
  as_of: "BioTIME 2.0 (Zenodo 15222193; St Andrews CSV export 2025)"
  records: 11989233
  studies: 708
  names: 56400
access:
  tier: open
  licence: "CC BY 4.0 for the database (Zenodo); each study keeps its own licence (PERMISSIONS): CC BY 369, CC0 or public domain 73, ODC-By 73, ODbL 65, government licences 44, non-commercial 37, citation only 32, others 15"
  routes:
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.10932823", state: "BioTIME 2.0 concept: four versions (2024-04-05, two on 2024-12-18, 2025-04-15); the newest mirrored without its 1.2 GB MySQL dump", checked: 2026-10-24}
    - {type: web, url: "https://biotime.st-andrews.ac.uk/getFullDownload.php", state: "St Andrews site: raw-data CSV zip of the 2025 release (not on Zenodo); mirrored", checked: 2026-10-24}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.1095627", state: "BioTIME 1 concept: six versions (2018); indexed only", checked: 2026-10-24}
    - {type: r-package, url: "https://github.com/bioTIMEHub/BioTIMEr", state: "BioTIMEr: gridding and diversity metrics; not run here", checked: 2026-10-24}
  api: "none; Zenodo REST and the St Andrews download page"
versioning:
  replay: partial
  notes: "Zenodo keeps every release (versions carry no version string, only dates); BioTIME 1 and 2 are separate concepts; studies are added and revised between releases"
mirror:
  path: deep-server:/data/paleodata/biotime
  policy: "the newest 2.0 release (RDS, metadata, references; not the SQL dump) and the St Andrews CSV of the same release; BioTIME 1 indexed"
  state: "zenodo/raw/15222193: 4 files; standrews-csv: 1 file (193 MB); both verify"
lineage:
  upstream:
    - "708 contributed and published monitoring studies, each with its own source and licence, assembled by the BioTIME consortium (Dornelas, Magurran and many co-authors; University of St Andrews)"
  downstream:
    - "syntheses of assemblage change (e.g. Dornelas et al. 2014, Blowes et al. 2019; recall); the BioTIMEr R package"
eprp_questions: [Q-025, Q-028]
citation:
  - "Dornelas, M. et al. (2025) BioTIME 2.0: expanding and improving a database of biodiversity time series. Global Ecology and Biogeography, doi:10.1111/geb.70003"
  - "Dornelas, M. et al. (2018) BioTIME: a database of biodiversity time series for the Anthropocene. Global Ecology and Biogeography 27: 760-786, doi:10.1111/geb.12729"
  - "BioTIME consortium (2025) BioTIME 2.0, Zenodo, doi:10.5281/zenodo.15222193; and each study used (references_biotime_v2_15April25.csv)"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# BioTIME 2.0

## Summary

BioTIME collects assemblage time series: repeated samples of whole
communities, with the abundance or biomass of every taxon recorded. It has
11,989,233 records from 708 studies, 56,400 names, 1874 to 2023. For Q-025
it is the modern local-change data the register names. It records which
species were present in each sample, year after year, at a stated grain, so
local disappearances can be put on the same observation filter as fossil
local losses. For Q-028 it can define "winners" as taxa increasing within
assemblages. Its limits for both are length and grain: the median study
covers 8 sampled years and the median extent is 31 km². Absences are not
recorded, because zero abundances are dropped. Reach for it for local change
in whole assemblages; it is not a source of global outcomes.

## Contents

[Profile](profile/biotime_profile.tsv):
- **Studies:** 708, of which terrestrial 328, marine 229 and freshwater 151.
  By taxa: invertebrates 241, plants 163, fish 131, birds 82, mammals 37,
  multiple 28, amphibians 14, reptiles 9, fungi 3. By climate: temperate
  492, tropical 115, polar 22, mixed and global 79.
- **What is measured:** abundance 495 studies, abundance and biomass 145,
  biomass 68. Abundance is missing on 1,239,675 rows and biomass on
  8,644,306.
- **Records:** 11,989,233, of which marine 5,197,833, terrestrial 5,059,806
  and freshwater 1,731,594. By taxon group: fish 3.19 M, birds 3.11 M, plants
  1.55 M, marine and freshwater invertebrates 0.99 M, other invertebrates
  0.94 M, and smaller groups. Resolution: species 85% of rows, genus 8%,
  coarser or mixed 6%.
- **Series length** (distinct years sampled per study): median 8, quartiles 4
  and 18. 319 studies span 10 or more sampled years, 159 span 20 or more, 75
  span 30 or more.
- **Study extent** (`AREA_SQ_KM`): quartiles 0.02, 31 and 13,500 km²,
  maximum global.
- **Candidate local disappearances.** Take the 319 studies with 10 or more
  sampled years. Of the 25,847 species recorded in a study's first three
  sampled years, 9,203 (36%) are absent from its last three: marine 47%,
  freshwater 30%, terrestrial 23%. Because zeros are not recorded and effort
  varies between years, this is a ceiling on local loss, not an estimate.

## Provenance and lineage

The BioTIME consortium (Dornelas, Magurran and co-authors, St Andrews)
gathers studies from contributors and the literature, standardises them to one
schema and validates names. Release 1 (Dornelas et al. 2018) has six Zenodo
versions (2017 to 2021 per the scoping; the depositor's dates say 2018). Release 2.0 (Dornelas et al. 2025) is a new
Zenodo concept with four versions from April 2024 to April 2025. The St
Andrews site offers the same 2025 release as a raw-data CSV, the form read
here; its 11,989,233 rows equal the paper's record count.

## Structure

The raw-data CSV has one row per taxon per sample: `ID_ALL_RAW_DATA`,
`ABUNDANCE`, `BIOMASS`, `ID_SPECIES`, `SAMPLE_DESC` (encodes date and site),
`LATITUDE`, `LONGITUDE`, `DEPTH`, `DAY`, `MONTH`, `YEAR`, `STUDY_ID`,
`newID`, `valid_name`, `resolution`, `taxon`. The study table (47 columns,
joined by `STUDY_ID`) gives realm, climate, habitat, treatment, protection,
taxa, `AB_BIO` (A, B or AB; 2 studies write "Ab"), years, grain and extent,
methods and `PERMISSIONS`. It also holds contributors' names and e-mail
addresses, which nothing here copies. The RDS on Zenodo is the
same data in BioTIME's query format.

## Access

- **Mirror.** `deep-server:/data/paleodata/biotime/zenodo/raw/15222193/`
  (RDS, study metadata, references, BibTeX; the MySQL dump left out with
  `--files`) and `biotime/standrews-csv/raw/<snapshot>_url/`; BioTIME 1's
  versions in `biotime/v1/versions.tsv`. [snapshots.tsv](snapshots.tsv).
- **Refresh.** [biotime_snapshot.sh](biotime_snapshot.sh) `[zenodo] [csv]
  [v1index]`. [zenodo-versions.tsv](zenodo-versions.tsv) and
  [zenodo-versions-v1.tsv](zenodo-versions-v1.tsv) index both concepts.
- **Profile.** `python3 biotime_profile.py RAWDATA_ZIP METADATA_CSV OUT_TSV`
  (standard library; about five minutes on deep-server).

## Strengths

- Whole-assemblage samples, repeated in time, with abundance or biomass for
  every taxon. That is the structure local-loss and winner analyses need.
- Global, across realms, with study grain and extent recorded.
- Openly released and versioned, with a per-study licence and reference.

## Weaknesses and pitfalls

- **No zeros.** Absent taxa are not recorded, so absence must be inferred
  from the sampling of each study and year.
- **Short series.** The median study has 8 sampled years. Only 159 have 20
  or more, far shorter than fossil time bins.
- **Mixed measures.** Counts, densities, presence/absence and biomass sit in
  the same columns. Check `AB_BIO` and the study methods before comparing.
- **Per-study licences.** 37 studies are non-commercial and 65 ODbL
  (share-alike), and 32 name no licence, only a citation requirement. Private
  mirroring is covered by Barry's universal approval of 23 October 2026. Any
  released derivative must filter by `PERMISSIONS` and cite every study used.
- **Contributor e-mail addresses** are in the study table: never copy them
  into a committed file.
- **Version strings are absent** on Zenodo. Versions are identified by
  record number and date only.

## Overlap with other sources

- **Q-025's other modern data.** Keil et al. (2018) and the IUCN Red List are
  not catalogued here. Antão et al. (2026) analyse population time series,
  not BioTIME assemblages.
- None of the other catalogue sources holds modern assemblage time series.

## EPRP relevance

- **Q-025.** The modern local-loss data the residual names ("Keil 2018's
  datasets, BioTIME, IUCN"). Support counts: 319 studies with 10 or more
  sampled years, and 25,847 species-study pairs that can be followed from a
  study's start to its end. The kill criterion's second obstacle, the time
  grain, is visible here: series last years to decades. BioTIME cannot give
  global outcomes, so C(A) for today still needs IUCN or extinction records.
- **Q-028 (iii).** Pre-defined modern winners: taxa increasing within
  assemblages, with studies in all realms. Human-transport covariates must
  come from elsewhere.
- Cannot support: global extinction, ranges, deep-time comparison on its own.

## Citation and terms

The Zenodo record is CC BY 4.0. BioTIME's usage guidelines say "it is
ultimately your responsibility to consult the actual licence" of each study,
and ask users to cite the database and every study used (scoping, checked on
the site 2026-10-24). Per-study licences are counted under the front
matter's licence.

## Verification log

- 2026-10-24 (Claude, Opus 5.5):
  - *checked*: indexed both Zenodo concepts; mirrored the newest 2.0 version
    without the SQL dump (md5 verified) and the St Andrews CSV (sha256
    recorded);
  - *checked*: profiled the CSV and study table
    ([profile](profile/biotime_profile.tsv)). Rows equal the 11,989,233
    records the 2.0 paper states, and every study in the data is in the
    metadata;
  - *checked*: per-study licences classified from `PERMISSIONS` (non-NC
    ODbL and NC variants separated);
  - *source claim*: the usage-guideline wording and the paper's counts
    (scoping subagent).
