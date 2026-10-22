---
id: rpd
name: Reading Palaeofire Database (RPD)
kind: compilation
status: frozen
last_update: "2022 (v1b; tables dated 2022-01-11)"
scope:
  taxa: [not taxonomic; sedimentary charcoal records]
  time: "Late Quaternary; Sahul records mostly Holocene (median oldest age 8.9 ka), 38 reach 20 ka"
  space: "global; 182 Sahul entities at 159 sites (Australia 144, New Guinea 24, Torres Strait 14)"
  record_unit: "entity: one charcoal series (a core, or one size class of a core) with samples, dates and age models"
size:
  as_of: "v1b, doi:10.17864/1947.000345"
  entities: 1676
  sites: 1480
  samples: 254763
  sahul_entities: 182
  sahul_samples: 12949
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
  reviewed: "not yet"
---

# Reading Palaeofire Database (RPD)

## Summary

The RPD is a global compilation of sedimentary charcoal records (1,676
entities from 1,480 sites), rebuilt from the Global Charcoal Database and
other archives into a relational schema with standardised units, site
descriptions, original chronologies and new Bacon age models for about half
the entities. Its value is the cleaning and the age models; for Sahul it adds
little beyond the [GCD](../gcd/README.md): 178 of its 182 Sahul entities come
from GCD version 4, and only 47 received a new age model. For Sahul fire
history, start with [SahulCHAR](../sahulchar/README.md) and use RPD for its
schema, units and global context.

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

Sahul subset: 182 entities at 159 sites (Australia 144, New Guinea 24, Torres
Strait 14) with 12,949 samples and 1,001 dates. 147 entities were counted on
pollen slides and 35 sieved; 112 report concentration, 34 pollen-slide
concentration, 25 influx and 11 other measures, in many units (the commonest,
mm² cm⁻³, covers only 23 entities). Deposits: bog 105, lake 53, estuarine 7,
fluvial 5, soil 4, marine 2, archaeological 2, unknown 4. The median oldest
original age is 8.9 ka; 38 entities reach 20 ka and 18 reach 50 ka.

## Provenance and lineage

Built at the University of Reading (Harrison et al. 2022) from GCD versions
3 and 4 and the GCD web version, plus PANGAEA, NOAA, Neotoma, the European
Pollen Database, the Arctic Data Center and author contributions; 840 records
are not in any GCD version. Sahul content is almost all GCD: 178 entities from
GCD version 4, 2 from version 3, one from PANGAEA (Native Companion Lagoon)
and one from Neotoma (Lake Hordorli). Version 1 (2021) had 1,681 records;
version 1b (2022) is current ([versions.tsv](versions.tsv)).

## Structure

Ten MySQL tables: `site` (basin type and size classes, flow type), `entity`
(measurement method, `TYPE`, unit, source), `sample` (depth, thickness,
charcoal measurement), `date_info` (lab number, radiocarbon and calibrated
ages, whether used), `chronology` (original ages), `age_model` (new Bacon
ages with quantiles), `unit`, `publication`, `entity_link_publication`,
`model_name`. Radiocarbon ages are stored uncalibrated; other ages are cal BP.
Missing values are coded -999999, -777777 and -888888. New age models use
SHCal20 south of 15°S and a 50:50 mix of curves between 15°N and 15°S, which
covers northern Australia and New Guinea.

## Access

- **Archive.** `https://researchdata.reading.ac.uk/345/` serves the SQL dump
  (22 MB), a CSV bundle (5 MB) and a readme. No API.
- **Mirror.** `deep-server:/data/paleodata/rpd/raw/2026-10-22T0633Z_url/`
  (read-only, sha256 manifest; the archive publishes no checksums). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- One clean schema with standard units and missing-value codes across all
  sources; the original and new chronologies kept side by side.
- New Bacon age models with quantiles for 829 entities worldwide.
- Fixed, citable versions with DOIs.

## Weaknesses and pitfalls

- **Few new age models in Sahul.** 47 of 182 Sahul entities have a new Bacon
  model; the rest carry only their original, mixed chronologies.
- **Unknown date use.** For 445 of the 1,001 Sahul dates, `age_used` is the
  missing code, so whether a date entered the chronology is unknown; 56 have
  no date type.
- **Heterogeneous measures.** Pollen-slide and sieved counts, concentration,
  influx and ratios, in dozens of units; compare within a measure only, or
  standardise (for example z-scores of transformed values).
- **Licence inheritance.** The RPD is CC BY 4.0, but most Sahul records came
  from the GCD, whose terms of use say CC BY-NC-ND. Which terms bind the
  derived records is not resolved.
- **Packaging.** The CSV bundle includes 13 macOS resource-fork and
  `.DS_Store` members, and several CSV headers begin with a byte-order mark;
  read `rpd_csv_files/*.csv` with `utf-8-sig`.
- **Frozen.** No update since 2022; the authors do not intend it as a
  permanent repository.

## Overlap with other sources

[charcoal_overlap.py](../sahulchar/charcoal_overlap.py) compares Sahul record
locations across SahulCHAR, RPD, GCD and Neotoma. 171 of the 182 RPD entities
lie within about 2 km of a GCD site (its source), and 111 within 2 km of a
SahulCHAR record (141 within 5 km). Seven places are RPD-only. Neotoma shares
three locations with RPD.

## EPRP relevance

A cleaned, globally consistent charcoal set for fire-regime questions that
need Sahul in global context. For Sahul alone, SahulCHAR is fuller.

## Citation and terms

CC BY 4.0. Cite Harrison et al. (2022), the v1b DOI and the original records'
publications (in the `publication` table). Note the GCD terms for records
derived from it.

## Verification log

- 2026-10-22, checked: v1b files mirrored; table counts match the description
  (1,676 entities, 1,480 sites, 254,763 samples); Sahul profile above.
- 2026-10-22, checked: Sahul sources, new-model coverage, date-use codes,
  packaging clutter.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): versions and
  DOIs, construction and sources, calibration rules, licence, the "not a
  permanent repository" statement.
