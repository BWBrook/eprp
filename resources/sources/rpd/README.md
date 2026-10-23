---
id: rpd
name: Reading Palaeofire Database (RPD)
kind: compilation
status: frozen
last_update: "2022 (v1b; tables dated 2022-01-11)"
scope:
  taxa: [not taxonomic; sedimentary charcoal records]
  time: "Late Quaternary; Sahul records mostly Holocene (median oldest age 8.7 ka), 37 reach 20 ka"
  space: "global; 181 Sahul entities at 158 sites (Australia 143, New Guinea 24, Torres Strait 14)"
  record_unit: "entity: one charcoal series (a core, or one size class or measure of a core) with samples, dates and age models"
size:
  as_of: "v1b, doi:10.17864/1947.000345"
  entities: 1676
  sites: 1480
  samples: 254763
  sahul_entities: 181
  sahul_samples: 12814
access:
  tier: open
  licence: "CC-BY-4.0 (University of Reading Research Data Archive); contains records derived from the Global Charcoal Database, whose terms say CC BY-NC-ND"
  routes:
    - {type: archive, url: "https://researchdata.reading.ac.uk/345/ (RPDv1b.sql, rpd_csv_files.zip, readme)", state: "v1b, latest", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "two deposited versions with DOIs (v1 2021, v1b 2022); index in versions.tsv. The authors say RPD is not designed as a permanent repository"
mirror:
  path: deep-server:/data/paleodata/rpd
  policy: "latest version (v1b); v1 on demand"
  state: "v1b 2026-10-22T0633Z_url (SQL dump, CSV bundle, readme)"
lineage:
  upstream:
    - "Global Charcoal Database versions 3 and 4 and its web version; PANGAEA, NOAA, Neotoma, EPD, Arctic Data Center; author submissions (840 records new to any GCD version)"
  downstream:
    - "SahulCHAR (2025) did not use RPD's age models"
eprp_questions: []
citation:
  - "Harrison, S. P. et al. (2022). The Reading Palaeofire Database: an expanded global resource to document changes in fire regimes from sedimentary charcoal records. Earth System Science Data 14: 1109-1124. doi:10.5194/essd-14-1109-2022"
  - "data: doi:10.17864/1947.000345 (v1b)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22 (no major findings); findings applied"
---

# Reading Palaeofire Database (RPD)

## Summary

The RPD is a global compilation of sedimentary charcoal records (1,676
entities from 1,480 sites), rebuilt from the Global Charcoal Database and
other archives into a relational schema with standardised units, site
descriptions, original chronologies and new Bacon age models for about half
the entities. Its value is the cleaning and the age models. For Sahul it adds
little beyond the [GCD](../gcd/README.md): 177 of its 181 Sahul entities come
from the GCD at version 4, and 46 have a new age model, although these
include 31 of the 37 records that reach 20 ka. For Sahul fire history, start
with [SahulCHAR](../sahulchar/README.md) and use RPD for its schema, units,
long-record age models and global context.

## Contents

Counts are our own ([profile](profile/rpd_profile.tsv)); the global totals
match the v1b description exactly.

| Table | Rows |
| --- | ---: |
| site | 1,480 |
| entity | 1,676 |
| sample | 254,763 |
| chronology (original ages) | 254,017 |
| age_model (new Bacon models) | 121,720 |
| date_info | 16,432 |
| unit | 202 |

Sahul subset: 181 entities at 158 sites and 151 distinct coordinates
(Australia 143, New Guinea 24, Torres Strait 14), with 12,814 samples and 995
date rows. Entities are series, not places: several sites carry two to four
(different measures or size classes of one core). 146 entities were counted
on pollen slides and 35 sieved; 112 report concentration, 33 pollen-slide
concentration, 25 influx and 11 other measures, in many units (the commonest,
mm² cm⁻³, covers 23 entities). Deposits: bog 105, lake 52, estuarine 7,
fluvial 5, soil 4, marine 2, archaeological 2, unknown 4. The median oldest
original age is 8.7 ka; 37 entities reach 20 ka and 17 reach 50 ka. The date
rows include 54 publication dates used as core-top ages, 27 known core tops
and 37 pollen correlations as well as radiocarbon, AMS, ²¹⁰Pb and U-series
dates.

## Provenance and lineage

Built at the University of Reading (Harrison et al. 2022) from GCD versions
3 and 4 and the GCD web version, plus PANGAEA, NOAA, Neotoma, the European
Pollen Database, the Arctic Data Center and author contributions; 840 records
are not in any GCD version. Sahul content is almost all GCD: the `source`
field names GCD version 4 (the database as released at version 4, not the
version in which a site was first entered) for 177 entities, version 3 for 2,
PANGAEA for one (Native Companion Lagoon) and Neotoma for one (Lake Hordorli).
Version 1 (2021) had 1,681 records; version 1b (2022) is current
([versions.tsv](versions.tsv)).

## Structure

Ten MySQL tables: `site` (basin type and size classes, flow type), `entity`
(measurement method, `TYPE`, unit, source), `sample` (depth, thickness,
charcoal measurement), `date_info` (lab number, radiocarbon and calibrated
ages, whether used), `chronology` (original ages), `age_model` (new Bacon
ages with quantiles), `unit`, `publication`, `entity_link_publication`,
`model_name`. Radiocarbon ages are stored uncalibrated; other ages are cal BP.
Three missing-value codes appear, none defined in the deposit's readme:
-888888 fills `reason_age_not_used` in 12,887 rows (apparently "not
applicable"), -777777 appears 2,537 times (apparently "not reported") and
-999999 2,032 times.

## Access

- **Archive.** `https://researchdata.reading.ac.uk/345/` serves the SQL dump
  (22 MB), a CSV bundle (5 MB) and a readme. No API.
- **Mirror.** `deep-server:/data/paleodata/rpd/raw/2026-10-22T0633Z_url/`
  (read-only, sha256 manifest; the archive publishes no checksums). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- One clean schema with standard units and missing-value codes across all
  sources; the original and new chronologies kept side by side.
- New Bacon age models with quantiles for 829 entities worldwide, including
  31 of the 37 Sahul records that reach 20 ka.
- Fixed, citable versions with DOIs.

## Weaknesses and pitfalls

- **Few new age models for short Sahul records.** 46 of 181 Sahul entities
  have a new Bacon model; most Holocene records carry only their original,
  mixed chronologies.
- **Calibration curve in doubt.** Every Sahul age-model row is labelled
  `BACON_INTCAL20` (globally 119,174 IntCal20 rows and 2,546 IntCal13), and
  the deposit's readme says the models use IntCal20, while the paper (source
  scan) describes SHCal20 south of 15°S and a mixed curve near the equator.
  Southern Hemisphere users should establish which curve was applied before
  using the new ages.
- **Unknown date use.** For 445 of the 995 Sahul date rows `age_used` holds
  -777777, so whether the date entered the chronology is unknown; 68 Sahul
  entities have no `age_used` value on any date.
- **Heterogeneous measures.** Pollen-slide and sieved counts, concentration,
  influx and ratios, in dozens of units; compare within a measure only, or
  standardise (for example z-scores of transformed values).
- **Licence inheritance.** The RPD is CC BY 4.0, but most Sahul records came
  from the GCD, whose terms of use say CC BY-NC-ND. Which terms bind the
  derived records is not resolved.
- **Packaging.** The CSV bundle includes 13 macOS resource-fork and
  `.DS_Store` members, and several CSV headers begin with a byte-order mark;
  read `rpd_csv_files/*.csv` with `utf-8-sig`.
- **Marine cores.** Two Sahul entities are marine sediment (for example ODP
  Site 820 off Queensland); treat them separately from land records.
- **Frozen.** No update since 2022; the authors do not intend it as a
  permanent repository.

## Overlap with other sources

[charcoal_overlap.py](../sahulchar/charcoal_overlap.py) compares Sahul record
locations across SahulCHAR, RPD, GCD and Neotoma. 170 of the 181 RPD entities
lie within about 2 km of a GCD site (its source), and 111 within 2 km of a
SahulCHAR record (141 within about 5 km). Seven places are RPD-only. Neotoma
shares three locations with RPD.

## EPRP relevance

A cleaned, globally consistent charcoal set for fire-regime questions that
need Sahul in global context, with new age models for most long Sahul
records. For Sahul alone, SahulCHAR is fuller.

## Citation and terms

CC BY 4.0. Cite Harrison et al. (2022), the v1b DOI and the original records'
publications (in the `publication` table). Note the GCD terms for records
derived from it.

## Verification log

- 2026-10-22, checked ([rpd_profile.py](rpd_profile.py)): v1b files mirrored;
  table counts match the description (1,676 entities, 1,480 sites, 254,763
  samples); Sahul profile above; sources; new-model coverage overall and for
  long records; age-model labels; missing-value codes; date-use codes;
  packaging clutter.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): versions and
  DOIs, construction and sources, the calibration rules stated in the paper,
  licence, the "not a permanent repository" statement.
- 2026-10-22, independent review (Claude Sonnet subagent): flagged the
  IntCal20 labels, the long-record model coverage, the undocumented codes,
  entities versus places, the meaning of the `source` field, and a
  non-Sahul marine core (Lombok Ridge) admitted by the region box, now
  excluded; all applied.
