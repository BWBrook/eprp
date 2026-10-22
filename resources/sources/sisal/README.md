---
id: sisal
name: SISAL, the Speleothem Isotopes Synthesis and AnaLysis database (version 3)
kind: compilation
status: active
last_update: "2024-02-21 (v3 on Oxford ORA; CSV tables dated 2024-03-04)"
scope:
  taxa: [not taxonomic; speleothem stable isotopes and trace elements]
  time: "global records to 565 ka; Australian records from the present to 99 ka, mostly Holocene"
  space: "global (365 sites); Australia 16 caves, 49 entities; none in New Guinea; Flores and Sulawesi on the Wallacean margin"
  record_unit: "sample: one depth in one speleothem (entity), with d18O, d13C, trace elements and ages under the original and SISAL age models"
size:
  as_of: "v3, doi:10.5287/ora-2nanwp4rk"
  sites: 365
  entities: 902
  samples: 448573
  australian_entities: 49
  australian_samples: 9202
access:
  tier: open
  licence: "CC-BY-4.0 (ORA, DataCite, README); images carry their own licences"
  routes:
    - {type: archive, url: "https://ora.ox.ac.uk/objects/uuid:1e91e2ac-ca9f-46e5-85f3-8d82d4d3cfd4", state: "v3; per-file downloads, no checksums published", checked: 2026-10-22}
    - {type: zenodo, url: "doi:10.5281/zenodo.10726619", state: "v3 age-model ensembles, 2.6 GB", checked: 2026-10-22}
    - {type: neotoma, url: "Neotoma, via GeoJSON loc queries only (SISAL sites carry no geopolitical unit)", state: "28 SISAL sites in a 110-160E, 50S-5N box", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "versions 1 (2018) to 3 (2024) deposited with DOIs; index in versions.tsv"
mirror:
  path: deep-server:/data/paleodata/sisal
  policy: "latest version: database bundle, codes, README, entry workbook, trace elements, and the age ensembles; images and the duplicate whole-package zip not mirrored"
  state: "ora-v3 2026-10-22 (url snapshot); zenodo-ensembles (Zenodo mirror)"
lineage:
  upstream:
    - "published speleothem records and their authors, through the PAGES SISAL working group (versions 1 2018, 2 2020, 3 2024)"
  downstream:
    - "Comas-Bru et al. 2020 and later SISAL syntheses; Australian monsoon and hydroclimate studies citing the underlying records"
eprp_questions: []
citation:
  - "Kaushal, N. et al. (2024). SISALv3: a global speleothem stable isotope and trace element database. Earth System Science Data 16: 1933-1963. doi:10.5194/essd-16-1933-2024"
  - "data: doi:10.5287/ora-2nanwp4rk; also cite Atsawawaranunt et al. 2018 and Comas-Bru et al. 2019, 2020, and each record's publications"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# SISAL version 3

## Summary

SISAL is the community database of speleothem (cave carbonate) records:
oxygen and carbon isotopes, trace elements and U-series or layer-counted
chronologies for 902 speleothems from 365 caves, with each record's original
age model and up to seven standardised SISAL age models. Australia has 16
caves and 49 entities, from the Kimberley (Ball Gown, KNI-51) to the
Flinders Ranges (Mairs), the south-west (Golgotha and others), the Snowy
Mountains (Jersey, Harrie Wood) and Tasmania (Lynds). Reach for it for
precisely dated hydroclimate, especially the Australian monsoon. Most
Australian records cover only the last few thousand years. Glacial coverage
is very thin: eight entities at five caves reach 20 ka, but only five
entities at four caves have samples in the last glacial maximum window
(18–24 ka), three-quarters of them from one stalagmite at Mairs Cave. Nothing
in New Guinea is included.

## Contents

Counts are our own ([profile](profile/sisal_profile.tsv)) and match the v3
description (365 sites, 902 entities).

| Cave | Current entities | Samples (all entities) | Original-chronology span of current entities (BP) |
| --- | ---: | ---: | --- |
| KNI-51 (Kimberley) | 20 | 2,160 | -58 to 20,877 |
| Ball Gown (Kimberley) | 6 | 502 | 8,367 to 39,971 |
| Cape Range | 1 | 1,500 | -60 to 1,439 |
| Cave C126 (Cape Range) | 2 | 312 | 5,676 to 25,640 |
| Chillagoe | 1 | 777 | -53 to 723 |
| Mairs (Flinders Ranges) | 2 | 878 | 14,887 to 23,135 |
| Golgotha (south-west) | 4 | 901 | -61 to 773 |
| Crystal, Moondyne, Labyrinth, Yonderup (south-west) | 4 | 635 | modern to 190 |
| Jersey (Snowy Mountains, flowstone) | 1 | 133 | 34,977 to 98,936 |
| Harrie Wood, Careys (Snowy Mountains); Cathedral (central-west NSW) | 6 | 1,351 | modern to 82 |
| Lynds (Tasmania) | 1 | 53 | 5,081 to 8,888 |

- Australia: 9,202 samples, 9,172 with δ18O and 4,683 with δ13C; Mg/Ca and
  Sr/Ca on 7 entities, Ba/Ca, U/Ca and P/Ca on 4. 421 dating rows (246
  MC-ICP-MS U/Th, 31 TIMS, 42 radiocarbon, 58 "other", 44 events).
- Ball Gown's 502 samples include 30 from its one superseded entity.
- Wallacean margin (not Sahul): Liang Luar on Flores (13 current or partially
  modified entities; 4,636 samples including those of three superseded
  entities; to 90.9 ka) and Gempa Bumi on Sulawesi (to 42.1 ka), both central
  to Indo-Australian monsoon reconstructions.

## Provenance and lineage

Built by the PAGES SISAL working group from records contributed or extracted
from publications; version 1 (2018) and 2 (2020) were deposited at Reading,
version 3 (2024) at Oxford with trace elements and new entities (Kaushal et
al. 2024). Earlier versions are listed in [versions.tsv](versions.tsv).
Australian records come from the Kimberley, Cape Range, the Flinders Ranges,
the south-west, the Snowy Mountains, Chillagoe and Tasmania; their DOIs are in
the `reference` table.

## Structure

Twenty-one relational tables keyed site → entity → sample: isotopes and trace
elements by `sample_id`; `original_chronology` (the published ages) and
`sisal_chronology` (linear interpolation, linear regression, Bchron, Bacon,
OxCal, copRa and StalAge ages, each with 2σ bounds); `dating` (U-series,
radiocarbon and event rows with lab data and use flags); `dating_lamina` for
layer-counted records; `hiatus`, `gap`, `notes`, `reference`. Ages are years
BP (1950); negative values are after 1950. `entity_status` marks current,
partially modified and superseded entities. The ORA bundle holds the SQL dump,
the CSVs, and a second zip of the same CSVs.

## Access

- **ORA.** Per-file downloads from the record page, no login; no checksums are
  published, so ours are in the manifest (they match an independent download
  by the source scan).
- **Zenodo.** Age-model ensembles (2.6 GB) for full age uncertainty.
- **Mirror.** `deep-server:/data/paleodata/sisal/ora-v3/` and
  `sisal/zenodo-ensembles/`. Index: [snapshots.tsv](snapshots.tsv).

## Strengths

- Precise radiometric chronologies (U-series) and annual-layer records, with
  both published and standardised age models.
- Consistent global schema with trace elements and documented metadata
  (mineralogy, cave setting, dripwater).
- Deposited versions with DOIs; ensembles for uncertainty propagation.

## Weaknesses and pitfalls

- **Thin glacial coverage.** By oldest age, 21 of the 48 current Australian
  entities lie within the last 2 ka, 14 reach 2–10 ka, 5 reach 10–20 ka and 8
  reach 20 ka or more (one, Jersey Cave, beyond 40 ka). Only five entities at
  four caves have samples between 18 and 24 ka: 721 samples, 540 of them from
  Mairs Cave stalagmite MC-S2, the rest from Ball Gown, Cave C126 and KNI-51.
  Nothing from New Guinea.
- **Standardised age models are patchy.** 16 current Australian entities have
  no SISAL model at all, and those with models have different subsets of the
  seven. The CSVs carry each model's central age with 2σ bounds; for full
  uncertainty use the ensembles.
- **Aragonite.** All 1,472 Australian aragonite samples, all from KNI-51, are
  flagged as not corrected for mineralogy.
- **Superseded and partially modified entities** coexist with current ones;
  filter on `entity_status` (one Australian entity is superseded; Liang Luar
  has three).
- **Equilibrium unknown.** Most Sahul-margin entities flag oxygen-isotope
  equilibrium with dripwater as "unknown" (source scan).
- **Packaging.** Nested duplicate CSV zip; README still cites "Kaushal et al.
  2023 DOI***".

## Overlap with other sources

Neotoma holds 28 SISAL sites in a 110–160°E, 50°S–5°N box (which includes
Borneo), reachable only through a GeoJSON location query because they carry
no geopolitical unit (see [Neotoma](../neotoma/README.md)). The underlying records are also archived
individually at NOAA's World Data Service for Paleoclimatology. SISAL is the
consolidated, standardised copy.

## EPRP relevance

Hydroclimate and monsoon history for northern and south-western Australia in
Late Quaternary questions (megafauna, people, fire), and Wallacean monsoon
records for the northern Sahul margin. Glacial-age inland hydroclimate needs
other archives.

## Citation and terms

CC BY 4.0. Cite Kaushal et al. (2024) and the earlier SISAL papers as the
README requires, plus each record's own publications.

## Verification log

- 2026-10-22, checked: v3 bundle mirrored; sha256 of the CSV bundle and README
  equal the source scan's independent download; counts above from the CSVs.
- 2026-10-22, checked: Australian and Wallacean entities, samples, dating,
  model coverage, oldest ages and aragonite flags.
- 2026-10-22, checked ([sisal_profile.py](sisal_profile.py)): oldest-age
  classes, samples in the 18–24 ka window by entity, aragonite by cave.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): version
  chain and DOIs, licence and citation requirements, equilibrium flags,
  ensemble record.
- 2026-10-22, independent review (Claude Sonnet subagent): showed that
  "reaching 20 ka" overstated glacial coverage, corrected the Mairs and
  Cathedral locations, the sample scope and the uncertainty wording; all
  applied.
