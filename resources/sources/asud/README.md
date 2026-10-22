---
id: asud
name: Australian Stratigraphic Units Database (ASUD)
kind: database
status: active
last_update: "live; WFS capabilities copyright 2020"
scope:
  taxa: [not taxonomic; stratigraphic units]
  time: "Archean to Holocene"
  space: "Australian states and territories, offshore basins (OFF) and the Australian Antarctic Territory (ATA)"
  record_unit: "one named stratigraphic unit (supergroup to bed) with its hierarchy, lithology, description and age"
size:
  as_of: "WFS snapshot 2026-10-22T0604Z"
  units: 18357
  with_numeric_ages: 16468
  formations_and_beds: 13543
  members: 2351
  groups_and_suites: 1761
access:
  tier: open
  licence: "CC-BY-4.0 (WFS AccessConstraints: Commonwealth of Australia (Geoscience Australia) 2020)"
  routes:
    - {type: wfs, url: "https://services.ga.gov.au/gis/stratunits/ows (stratunit:StratigraphicUnit; also gsmlp:GeologicUnitView and gsmlb:GeologicUnit, same 18,357 units)", state: "live; CSV output, no feature cap", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 (GeoServer); GeoSciML views alongside the native layer"
versioning:
  replay: none
  notes: "live register with no releases; snapshot and record the date"
mirror:
  path: deep-server:/data/paleodata/asud
  policy: "dated snapshots of the native StratigraphicUnit layer"
  state: "snapshot 2026-10-22T0604Z_wfs, row count equals numberMatched"
lineage:
  upstream: ["Geoscience Australia and state geological surveys"]
  downstream: ["used here to check PBDB formation names and ages (pbdb entry)"]
eprp_questions: []
citation:
  - "Geoscience Australia, Australian Stratigraphic Units Database, https://services.ga.gov.au/gis/stratunits/ows, retrieved 2026-10-22, CC BY 4.0"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Australian Stratigraphic Units Database (ASUD)

## Summary

ASUD is Australia's national register of stratigraphic names: 18,357 units,
from supergroups to beds, each with its place in the hierarchy, lithology,
description and age. It holds no fossils. We catalogue it because it is the
authority that fossil databases' formation names should resolve to, and its
ages give an independent check on the ages those databases assign. Reach for it
to normalise and date formation names in [PBDB](../pbdb/README.md) or any
Australian compilation, and to find a unit's group, basin context and
synonymy. It is reliable for names and mostly reliable for ages, with a small
number of clear errors.

## Contents

Counts are our own ([profile](profile/asud_profile.tsv)) from the 2026-10-22
snapshot; the CSV row count equals the server's `numberMatched` (18,357).

| Rank | Units |
| --- | ---: |
| Formation, beds | 13,543 |
| Member, phase | 2,351 |
| Group, Suite | 1,761 |
| Supergroup | 339 |
| Subgroup | 302 |
| Bed | 55 |
| Clan | 5 |
| unknown | 1 |

- *Unit type.* 18,234 lithostratigraphic units and 123 sequence-stratigraphic
  units.
- *Where.* Queensland 3,969, New South Wales 3,858, Western Australia 3,064,
  Victoria 1,483, Northern Territory 1,457, South Australia 1,244, Tasmania 889,
  Australian Antarctic Territory 561, offshore 36, and multi-state units (for
  example "NT, WA" 243); 463 have no state.
- *Ages.* 16,468 units (90%) carry numeric older and younger ages; 16,116 have
  a text age (`GEOLOGICHISTORY`, e.g. "Barremian - Albian"); 15,490 have a
  description.
- *Hierarchy.* Each unit lists its supergroup (3,903), group (8,711), subgroup
  (1,382), formation (15,636), member (2,357) and bed (55) where they apply.

## Provenance and lineage

Geoscience Australia maintains ASUD with the state and territory geological
surveys; every unit is marked "synthesis from multiple sources". Each unit has
a persistent identifier, `http://pid.geoscience.gov.au/geologicFeature/au/SU<STRATNO>`.

## Structure

The native layer `stratunit:StratigraphicUnit` has 34 columns: `STRATNO` (the
key), `NAME`, `RANK`, `DESCRIPTION`, `LITHOLOGY`, `GEOLOGICHISTORY` (text age),
`NUMERICOLDERAGE` and `NUMERICYOUNGERAGE` (Ma), era-level `OLDERAGE`,
`YOUNGERAGE` and `REPRESENTATIVEAGE`, the hierarchy fields `SUPERGROUP`,
`GROUPNAME`, `SUBGROUP`, `FORMATION`, `MEMBER`, `BED`, `STATE`, and GeoSciML
vocabulary URIs. `REPRESENTATIVEAGE_CLASS` is always `era` (or blank), so the
representative age is coarse; use the numeric ages. The two GeoSciML layers
carry the same units with fewer fields.

## Access

- **WFS.** No key, no feature cap; `outputFormat=csv` returns the whole layer
  in one request (14 MB). `data_mirror.py wfs
  https://services.ga.gov.au/gis/stratunits/ows stratunit:StratigraphicUnit
  asud --license ...` takes a dated snapshot and checks the row count.
- **Mirror.** `deep-server:/data/paleodata/asud/raw/2026-10-22T0604Z_wfs/`
  (CSV and schema, read-only, sha256 manifest). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- National coverage under one schema with persistent identifiers.
- Ages are internally consistent for 99.5% of checkable units: of 14,914 units
  whose text age resolves through the PBDB interval table and that have real
  numeric ages, 14,838 have numeric ages that overlap the named interval.
- Names are near-unique (17 duplicated names in 18,357 units), so matching is
  practical; 93.8% of PBDB's named Australian collections find a unit.
- Open licence and a simple, uncapped WFS.

## Weaknesses and pitfalls

- **Some numeric ages contradict the unit's own text age.** 76 units are
  disjoint. Some are typos: the Allaru Mudstone (STRATNO 291) is "Albian" in
  text but 45–44 Ma in numbers, with era "Cenozoic"; the Buchargingah Granite
  reads 6–419.62 Ma; the Jindera Granite 40.4–403.4 Ma. Others follow older
  boundaries: units described as "Cryogenian" carry ages of about 830 Ma,
  older than the period's current base. One is stale text: the Talbragar
  Fossil Fish Bed's text says Early–Middle Jurassic, its numbers 161.5–151 Ma.
- **Inverted and placeholder ages.** 57 units have an older age younger than
  the younger age. 13 units of unknown age carry 0–0 Ma, which reads as Recent
  to any numeric filter.
- **Era fields are derived and coarse.** `OLDERAGE` and `YOUNGERAGE` give the
  era only, and units on era boundaries are labelled inconsistently; do not
  use them to check ages.
- **Gaps in fossiliferous Cenozoic units.** The Fyansford Formation, Muddy
  Creek Marl, Glen Aire Clay and Black Rock Sandstone of Victoria, all classic
  fossil units, are not in the register.
- **Homonyms across states.** "Cave Hill", "Black Rock", "Drummond" and
  "Glenelg" each name unrelated units in different states or eras; match with
  state and age, not name alone.
- **Antarctic units are mixed in.** 561 units belong to the Australian
  Antarctic Territory; filter on `STATE` for continental work.

## Overlap with other sources

ASUD is the reference for PBDB's Australian stratigraphy; the matching and age
comparison are reported in the [PBDB entry](../pbdb/README.md#overlap-with-other-sources).
Macrostrat, PBDB's usual stratigraphic partner, is not yet assessed for
Australia.

## EPRP relevance

ASUD serves any Australian deep-time case study that groups occurrences by
formation or needs independent unit ages: it normalises names, links units to
groups and basins, and flags age disagreements for checking. It has no fossil
content of its own.

## Citation and terms

CC BY 4.0. Cite Geoscience Australia, the service URL and the retrieval date.

## Verification log

- 2026-10-22, checked: WFS capabilities list three layers, each with
  `numberMatched` 18,357; licence text in `AccessConstraints`.
- 2026-10-22, checked: snapshot of `stratunit:StratigraphicUnit`, 18,357 CSV
  rows; profile counts above.
- 2026-10-22, checked: text age against numeric age for every unit, through
  the PBDB interval table; inverted and 0–0 ages; the Allaru, Elcho Island and
  other records read directly.
- 2026-10-22, checked: absence of Fyansford, Muddy Creek, Glen Aire and Black
  Rock Sandstone by name search of the snapshot.
- 2026-10-22, inferred: the "Cryogenian" cases follow older period
  boundaries, from their numeric ages of about 830 Ma.
