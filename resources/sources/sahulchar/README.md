---
id: sahulchar
name: SahulCHAR, sedimentary charcoal records for Sahul and New Zealand
kind: compilation
status: active
last_update: "2025 (v1); OCTOPUS layers stamped v2.3(1)"
scope:
  taxa: [not taxonomic; sedimentary charcoal and the ages that date it]
  time: "Late Quaternary; Sahul charcoal series mostly Holocene (median oldest charcoal age 8.2 ka), 54 reach 20 ka; Naracoorte cave charcoal to 1.2 Ma"
  space: "Sahul (393 units: Australia 340, New Guinea 42, Torres Strait 11) and New Zealand (142); true coordinates"
  record_unit: "observation: one charcoal measurement or one age at a depth in a core or section (unit)"
size:
  as_of: "OCTOPUS WFS snapshot 2026-10-22T0634Z, v2.3(1)"
  units: 535
  charcoal_records: 687
  metasites: 425
  observations: 48234
  sahul_units: 393
  sahul_observations: 40392
access:
  tier: open
  licence: "CC-BY-4.0 per OCTOPUS documentation and the paper; the data DOI's DataCite record states no rights"
  routes:
    - {type: wfs, url: "http://geoserver.octopusdata.org/geoserver/wfs (be10-denude:sahulchar, sahulchar_units)", state: "live, HTTP only, CSV", checked: 2026-10-22}
    - {type: doi, url: "doi:10.25900/KKDX-XH23 (data); doi:10.25900/Y4E9-R595 (OCTOPUS layer)", state: "resolve to OCTOPUS", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 (GeoServer)"
versioning:
  replay: partial
  notes: "the live layers are the data; snapshot and record DBVERNO (v2.3(1)); the layer DOI's title says v2.2"
mirror:
  path: deep-server:/data/paleodata/sahulchar
  policy: "dated WFS snapshots of both layers"
  state: "octopus-wfs 2026-10-22T0634Z_wfs; counts equal numberMatched"
lineage:
  upstream:
    - "author submissions (141 records, 23 authors); Global Paleofire Database (about a third, 85 of them modified); digitised diagrams (about 46%); Neotoma; PANGAEA; Mooney et al. 2011 compilation"
  downstream:
    - "planned integration into the Global Paleofire Database and Neotoma (paper)"
eprp_questions: []
citation:
  - "Rehn, E. et al. (2025). Earth System Science Data 17: 2681-2692 (the SahulCHAR database). doi:10.5194/essd-17-2681-2025"
  - "data: doi:10.25900/KKDX-XH23, with DBVERNO and retrieval date; Codilean et al. (2022) for OCTOPUS"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# SahulCHAR

## Summary

SahulCHAR is the most complete compilation of sedimentary charcoal for Sahul
and New Zealand: 687 charcoal records from 535 cores and sections at 425
metasites, with their raw ages, assembled from author submissions, digitised
diagrams, the Global Paleofire Database, Neotoma and PANGAEA (Rehn et al.
2025). It lives as two layers in [OCTOPUS](../octopus/README.md). In Sahul it
holds 393 cores and sections, and 170 of the 348 distinct Sahul charcoal places we found
across four sources appear only here. Reach for it first for Late Quaternary
fire history and its relation to megafauna, climate and people. It supplies
dates, not age models: you build the chronologies.

## Contents

Counts are our own ([profile](profile/sahulchar_profile.tsv)); the totals
(687 records, 425 metasites) match the paper.

| | All | Sahul |
| --- | ---: | ---: |
| Units (366 cores, 15 excavations, 12 other in Sahul) | 535 | 393 (Australia 340, New Guinea 42, Torres Strait 11) |
| Charcoal records | 687 | 510 |
| Observations | 48,234 | 40,392 (37,899 charcoal, 2,493 ages) |

- *Deposits.* Lake 201 and bog 195 units overall, then estuarine, alluvial,
  buried organic, fluvial, marine and archaeological; 65 unrecorded.
- *Methods (Sahul charcoal rows).* Sieved 21,236, pollen slide 13,397, sieved
  with image analysis 2,865, hydrogen pyrolysis 290. Leading measures:
  fragments per cm³ (17,644) and fragments per cm² per year (5,002).
- *Data source (Sahul charcoal rows).* Author 17,170, digitised 9,280,
  Paleofire database 10,642 (6,143 of them author-revised), Neotoma 807.
- *Ages (Sahul).* 2,493 ages: conventional radiocarbon 1,019 and AMS 853,
  ²¹⁰Pb 226, OSL 107, U-series 110, pollen correlation 41.
- *Time.* Two measures differ. `MAXAGE` is a unit's oldest dated horizon:
  of 367 Sahul units with one, the median is 7.0 ka, 61 reach 20 ka, 18 reach
  50 ka and 10 exceed 130 ka. The oldest charcoal sample with an estimated age
  is what most uses need: of 268 units with any, the median is 8.2 ka, 54
  reach 20 ka, 26 reach 50 ka and 16 exceed 130 ka. The longest are the
  Naracoorte cave sequences (deposit "Other"): charcoal reaches 1.20 Ma at
  Dead Sheep Cave, 506 ka at Blanche Cave, 421 ka at Specimen Cave, 370 ka at
  Victoria Fossil Cave and 238 ka at Robertson Cave; Alexandra Cave is dated
  to 1.34 Ma but its charcoal stops at 306 ka.

## Provenance and lineage

Compiled by Rehn and colleagues (CABAH and partners) and published in 2025:
141 records were submitted by 23 authors; about a third derive from or also
exist in the Global Paleofire Database (85 of them modified); about 46% of
records (Sahul and New Zealand together) were digitised from diagrams; others came from Neotoma and PANGAEA. It triples
Mooney et al.'s (2011) Australasian compilation. It did not use the RPD's age
models. Integration into the GPD and Neotoma is planned.

## Structure

`sahulchar_units` (one row per core or section: site, metasite, coordinates,
deposit, collection method, maximum age, number of charcoal records,
references, Neotoma site ID) and `sahulchar` (one row per observation: depth,
thickness, `WHATAMI` = `age` or `particles counted`, the age with its error,
type and method, or the charcoal value with method, measure and size class,
and `DATASOURCE`). Missing values appear as `-9999.99`, `ND`, `NA` or blank.
The OCTOPUS geometry is Web Mercator; use `X_WGS84`/`Y_WGS84`.

## Access

- **WFS.** As for other OCTOPUS collections:
  `data_mirror.py wfs http://geoserver.octopusdata.org/geoserver/wfs
  be10-denude:sahulchar,be10-denude:sahulchar_units sahulchar/octopus-wfs`.
- **Mirror.** `deep-server:/data/paleodata/sahulchar/octopus-wfs/raw/2026-10-22T0634Z_wfs/`
  (39 MB, both layers and schemas). Index: [snapshots.tsv](snapshots.tsv).

## Strengths

- The fullest Sahul charcoal coverage, with true coordinates (SahulArch's
  layers, by contrast, are blurred).
- Raw ages with depths for every record that has them, so chronologies can be
  rebuilt consistently.
- Record-level provenance (`DATASOURCE`), so digitised values can be excluded.

## Weaknesses and pitfalls

- **No age models, and no calibration curve recorded.** `CALCURVE` is blank
  for all 2,493 Sahul ages. `EST_AGE` is missing for 9,674 of 37,899 Sahul
  charcoal rows (26%), concentrated in whole records: 116 of the 384 Sahul
  units with charcoal have no estimated age on any row, so their series need
  an age model built from the raw dates.
- **`MAXAGE` is the oldest date, not the oldest charcoal.** Charcoal
  estimated ages run beyond the oldest date in many units (extrapolation) and
  stop short of it in others; use the charcoal rows' own ages.
- **Digitised data.** 9,280 Sahul charcoal values (24% of rows) were read from
  published diagrams; they occur in 136 of the 384 charcoal-bearing units.
- **Not only sediment cores.** Units include 15 excavations and 12 "other"
  units in Sahul, among them the Naracoorte caves (deposit "Other"); 9 Sahul
  units have no charcoal records; filter on `UNITTYPE`, `DEPOSIT` and the
  charcoal rows' ages.
- **Country codes are not reliable.** The independent review found PNG
  mainland units (Caution Bay, Ruisasi) coded as Australia; use coordinates.
- **Mixed measures and units**, as in every charcoal compilation.
- **Licence statement missing** from the data DOI's metadata, and the layer
  DOI's title says v2.2 while the layers say v2.3(1).
- **Duplication with its sources.** Records shared with the GPD may differ
  (85 were modified); do not pool SahulCHAR with GCD or RPD without matching.

## Overlap with other sources

[charcoal_overlap.py](charcoal_overlap.py) reduces SahulCHAR, RPD, GCD and
Neotoma to Sahul record locations and matches them within 0.02° and 0.05°
(about 2 and 5 km). Clustering all locations within 0.02° gives 348 distinct
places: 170 only in SahulCHAR, 82 in SahulCHAR, GCD and RPD, 52 in GCD and RPD
but not SahulCHAR, 15 in SahulCHAR and GCD, 11 in SahulCHAR and Neotoma, and
a handful elsewhere; no place is Neotoma-only. Of RPD's 181 Sahul entities,
141 have a SahulCHAR record within 0.05° and 40 do not, so SahulCHAR does not
contain everything: check RPD and GCD for those places. The clustering is a
greedy, order-dependent heuristic: the independent review found 342 to 352
places at about 2 km depending on method and order, 287 at 5 km and 402 at
1 km, with SahulCHAR-only places about half throughout. Coordinates were
revised for some records.

## EPRP relevance

The primary source for Sahul fire history in megafauna, climate and
human-arrival questions, alongside [FosSahul](../fossahul/README.md),
[SahulArch](../sahularch/README.md) and [Neotoma](../neotoma/README.md).

## Citation and terms

CC BY 4.0 per OCTOPUS and the paper. Cite Rehn et al. (2025), the data DOI
with DBVERNO and retrieval date, and the original record publications.

## Verification log

- 2026-10-22, checked ([sahulchar_profile.py](sahulchar_profile.py)): both
  layers snapshotted (48,234 and 535 features, equal to numberMatched); totals
  match the paper; Sahul profile above, including unit types, charcoal-based
  ages, records without estimated ages, digitised units and the Naracoorte
  sequences.
- 2026-10-22, checked: four-way location overlap with RPD, GCD and Neotoma.
- 2026-10-22, independent review (Claude Sonnet subagent): showed `MAXAGE` is
  the oldest date rather than the oldest charcoal, the concentration of
  missing ages, unit types, country-code errors and the clustering
  sensitivity; all applied.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): authorship,
  provenance shares, DOIs and their metadata, planned integration.
