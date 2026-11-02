---
id: alien-first-records
name: "FirstRecords: a global dataset of first records of non-native species (the Alien Species First Records Database), v4.0 and v3.1"
kind: compilation
status: active
last_update: "2026-02-25 (v4.0)"
scope:
  taxa: ["all alien taxa with a dated first record: vascular plants 62% of rows, insects 15%, birds, fishes, molluscs, crustaceans, fungi and others"]
  time: "first records from 7000 BCE to 2023; 90% from 1800 on"
  space: "global: 268 recipient locations (countries, islands, sub-national regions); 4,633 rows have none"
  record_unit: "the first record of an alien taxon in a recipient location (year, confidence, status)"
size:
  as_of: "v4.0 (Zenodo 18759840)"
  records: 90023
  taxa: 28823
  locations: 268
access:
  tier: open
  licence: "CC BY 4.0 (Zenodo, v3.1 and v4.0); public files omit records without sharing permission"
  routes:
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.3690741", state: "concept: v1.1, v1.2 (2020-02-28) and v2 (2021-03-22) restricted (no files listed); v3.1 (2023-10-25, free-data workbook) and v4.0 (2026-02-25) open, both mirrored", checked: 2026-10-24}
  api: "none; Zenodo REST"
versioning:
  replay: partial
  notes: "each version is a dated release, but the versions behind the 2017 and 2018 papers (1.1 to 2) are restricted on Zenodo, and every public release omits records not cleared for sharing"
mirror:
  path: deep-server:/data/paleodata/alien-first-records
  policy: "v4.0 (newest) and v3.1 (the version SInAS 3.x harmonises); all versions indexed"
  state: "two versions, 6 files (58 MB) with manifests; both verify"
lineage:
  upstream:
    - "national and regional inventories, databases and literature (DAISIE, NOBANIS, GISD, AquaNIS, GAVIA, Simpson et al. 2018 for the USA, and others; FirstRecords_dataset_sources_v4.0.csv), compiled by Hanno Seebens and colleagues (Senckenberg)"
  downstream:
    - "Seebens et al. 2017 and 2018 (the papers on accumulating first records); SInAS 3.x (Gómez-Suárez et al. 2025), which harmonises v3.1 with GRIIS and GloNAF"
eprp_questions: [Q-047, Q-028]
citation:
  - "Seebens, H. & Renard Truong, T. (2026) FirstRecords: A global dataset of first records of non-native species, version 4.0. Zenodo, doi:10.5281/zenodo.18759840 (a data paper is under review, per the scoping; not checked)"
  - "Seebens, H. et al. (2017) No saturation in the accumulation of alien species worldwide. Nature Communications 8: 14435, doi:10.1038/ncomms14435"
  - "Seebens, H. et al. (2018) Global rise in emerging alien species results from increased accessibility of new source pools. PNAS 115: E2264-E2273, doi:10.1073/pnas.1719429115 (recall)"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-24, independent Claude Sonnet subagent; findings applied"
---

# Alien Species First Records Database

## Summary

The First Records Database gives, for each alien taxon and recipient
location, the year it was first recorded there: 90,023 records of 28,823 taxa
in 268 locations in v4.0 (February 2026). It is the only one of the three
global alien-species sources here with *timing*, so for Q-047 it is the
modern side of a flow: what reached where, and when. It does not say where a
species came from (no source region or route). Its early versions, behind the
much-cited 2017 paper, are now restricted, and the public files leave out
records whose providers have not cleared them for sharing. Reach for it for
the timing of arrivals by recipient region. GRIIS and GloNAF give status, and
SInAS gives native ranges.

## Contents

| Version | Files | Records |
| --- | --- | ---: |
| v4.0 (2026-02-25) | records (semicolon-separated CSV), location table, taxonomy table (GBIF-matched), sources table, raw workbook | 90,023 |
| v3.1 (2023-10-25) | free-data workbook (ReadMe, FirstRecords, References sheets) | 77,375 |

v4.0 in numbers ([profile](profile/first_records_profile.tsv)):
- **Taxa:** vascular plants 56,028 rows (62%), insects 13,563, birds 4,225,
  fishes 3,792, molluscs 2,099, crustaceans 2,017, worms 1,254, mammals 1,209,
  fungi 875.
- **Recipient continents:** Europe 38,388 rows (43%), Oceania 13,816, Asia
  11,828, North America 11,482, Africa 6,771, South America 2,035,
  Antarctica 1,070; 4,633 rows have no continent.
- **Year of first record:** before 1500, 777 rows; 1500–1799, 7,854;
  1800–1899, 19,191; 1900–1949, 20,210; 1950–1999, 32,070; from 2000, 9,921.
  The range runs from 7000 BCE to 2023.
- **Confidence:** high 77,064, medium-high 7,087, medium 355, medium-low 125,
  low 5,392.
- **Status:** present 85,208, uncertain 4,332, absent 429, present but not in
  the wild 54. `degreeOfEstablishment` is blank on 60,361 rows; established
  25,693, casual 3,119, invasive 550, extinct 231.
- **Pathway:** given on 2,010 rows (2.2%).
- **Largest sources:** DAISIE (10,771 rows), Robeck et al. 2024 (8,990), GISD
  (6,185), NOBANIS (5,296), GAVIA (3,159), Simpson et al. 2018 (3,142).

## Provenance and lineage

Hanno Seebens and colleagues assemble first records from regional
inventories, national databases and the literature. The sources table lists
each one with its data-usage terms. Seebens et al. (2017) analysed the records
from 1500 on of an early version (45,813 records, 16,926 species, 282
regions, as the paper states);
v2 and v3.1 grew it (source claim, scoping), and v4.0 moved to Darwin Core
field names and added prehistoric and extinct records. Zenodo keeps
v1.1, v1.2 and v2 as restricted records: their files are not listed or
served. SInAS 3.x harmonises v3.1 with GRIIS and GloNAF.

## Structure

v4.0's records table has Darwin Core columns: `locationID`, `location`,
`verbatimLocation`, `taxonID`, `taxon`, `habitat`, `firstRecordEvent` (a
year; negative for BCE), `verbatimFirstRecordEvent`,
`confidenceFirstRecordEvent`, `occurrenceStatus`, `establishmentMeans`,
`degreeOfEstablishment`, `pathway`, `datasetName`, `bibliographicCitation`,
`accessRights`. It joins to the taxonomy table (GBIF match status, rank and
classification) by `taxonID`, and to the location table (`region`,
`continent`) by `locationID`. The location table has 557 rows for 268
identifiers, one per verbatim name (up to 57 per identifier), so take one row
per identifier before joining or the records multiply. Vocabularies are as
counted under Contents; `habitat` is blank on 94% of rows. `accessRights` is
"Free" (89,306) or "Free with proper credit/citation" (717). The records file
is not valid UTF-8 (679 undecodable bytes, the first at offset 8,164,937):
read it with replacement, as the profiler does.

## Access

- **Mirror.** `deep-server:/data/paleodata/alien-first-records/raw/{4.0_18759840,3.1_10039630}/`
  with manifests; [snapshots.tsv](snapshots.tsv).
- **Refresh.** [first_records_snapshot.sh](first_records_snapshot.sh) (newest
  plus v3.1); [zenodo-versions.tsv](zenodo-versions.tsv) indexes all five.
- **Profile.** `python3 first_records_profile.py V4_DIR V31_XLSX OUT_TSV`.
- **Crosswalk.** `python3 crosswalk_plants.py GLONAF_DIR FR_V4_DIR GRIIS_RAW
  GRIIS_DATASETS_TSV GRIIS_COMPENDIUM_CSV OUT_TSV` (see Overlap).

## Strengths

- Dated first records for nearly 29,000 taxa, with a confidence grade on
  every row.
- Darwin Core fields and a GBIF-matched taxonomy table make joins practical.
- Sources are attributed per record.

## Weaknesses and pitfalls

- **Some years are resolved from ranges, by an undocumented rule.** Every row
  has a year, but on 13,858 rows (15%) it differs from the verbatim first
  record, which is a range or text. v3.1 drew years at random within ranges
  of up to 20 years (scoping, from v3.1's `FirstRecord` and
  `FirstRecord_orig`), but 1,571 of v4.0's 3,281 verbatim ranges written
  YYYY-YYYY span more than 20 years, so that cannot be v4.0's
  rule, and v4.0 does not state one. Use `verbatimFirstRecordEvent` and the
  confidence grade where precision matters.
- **A first record is not an arrival.** Detection effort drives first
  records, and it rose steeply after 1950.
- **Restricted early versions.** v1.1 to v2, behind the 2017 and 2018 papers,
  are restricted on Zenodo, so those analyses cannot be replayed from public
  data. Records without sharing permission are left out of every public file.
  Both are queued for the compilers (CONTACTS.md (queue held back) C32).
- **Locations are mixed units, and 5% have none.** Countries, islands and
  sub-national regions. 4,633 rows have a blank location identifier, with
  verbatim locations such as "USACanada" (2,854), "Channel Is" (636),
  "European part of Russia" (260) and "Aegean Sea" (190); they fall out of
  any join by location.
- **No source region or pathway** for 98% of rows. Q-047 needs flows; this
  gives only arrivals.
- **Recent decades are incomplete** (2000 on: 9,921 rows, against 32,070 for
  1950–1999), a reporting lag.

## Overlap with other sources

**A naive plant crosswalk** ([crosswalk_plants.py](crosswalk_plants.py),
[output](profile/crosswalk_plants.tsv)). It covers plant species by country:
- **First Records:** records marked present, at locations matched by name to
  a country (217 of 268, with seven aliases).
- **GloNAF:** regions whose code is a country code.
- **GRIIS:** 218 checklists. Protected-area lists, the GISD and nested units
  are left out, and territories keep their own codes.

Names are the first two words of the accepted name (GRIIS's
`acceptedNameUsage` where given). In the 138 countries all three cover:

| | Pairs |
| --- | ---: |
| GloNAF | 38,553 |
| First Records | 38,939 |
| GRIIS | 59,805 |
| GloNAF and GRIIS | 24,802 |
| GloNAF and First Records | 17,585 |
| First Records and GRIIS | 24,445 |
| all three | 13,181 |
| GloNAF only; First Records only; GRIIS only | 9,347; 10,090; 23,739 |

Of the pairs found in all three, First Records grades 10,469 high
confidence, 1,400 medium-high and 1,276 low. Australia (2,403), Japan
(1,070), Sweden (867), South Africa (769) and Norway (714) contribute most.

Three reasons keep this from being a complete crosswalk:
- **Exact names and country units** make every overlap a lower bound.
  First Records plant rows at sub-national or unmatched locations are left
  out (about 20,000 before the aliases were added, by the review's count).
- **The inclusion rules differ.** GloNAF lists naturalized or invasive
  taxa, GRIIS present aliens, and First Records first records of any
  establishment. A pair missing from one source is not necessarily a missed
  match.
- **It counts coverage, not outcomes.** There are no denominators here.

SInAS harmonises names and units properly
([register-deposits](../register-deposits/README.md); SInAS 3.2 holds v3.1's
free-data workbook).

## EPRP relevance

- **Q-047.** The timing side of modern flows by recipient region. Codex's
  first gate (76/1420) asks for a crosswalk of outcomes and denominators
  within one taxon. For plants, the crosswalk above shows that the three
  modern sources cover 13,181 of the same species-by-country pairs, 10,469 of
  them with a high-confidence first record. That is coverage on which a
  modern outcome could be defined. It is not yet an outcome with a
  denominator, and it says nothing about the gate's fossil half. Source
  pools and routes still need SInAS or native-range data.
- **Q-028 (iii).** Successful invaders (established or invasive) as one
  definition of modern winners, but `degreeOfEstablishment` is blank on 67%
  of rows, so most records carry no establishment outcome.
- Cannot support: transport routes, source regions, abundance or impact.

## Citation and terms

Zenodo licence CC BY 4.0. The records table's `bibliographicCitation` and
the sources table give each record's origin; 717 rows ask for "proper
credit/citation". Cite the version used and Seebens et al. (2017).

## Verification log

- 2026-10-24 (Claude, Opus 5.5):
  - *checked*: indexed the five Zenodo versions (three restricted, no files)
    and mirrored v4.0 and v3.1 (md5 verified);
  - *checked*: profiled v4.0 and counted v3.1's records sheet
    ([profile](profile/first_records_profile.tsv));
  - *checked*: the plant crosswalk with GloNAF and GRIIS (Overlap);
  - *source claim*: the 2017 paper's counts; the v3.1 range-resolution rule
    (scoping); the data paper under review (scoping).
  - Independent review (Claude Sonnet subagent), findings applied:
    - the blank location identifier (not a missing table row);
    - the location table's repeated identifiers;
    - the file encoding;
    - the Zenodo title and creators;
    - ranges wider than 20 years;
    - the 2017 paper's post-1500 subset;
    - the crosswalk's names, units, aliases and inclusion rules, which raise
      the count found in all three from 12,480 to 13,181;
    - softer Q-047 and Q-028 claims.
