---
id: asud
name: Australian Stratigraphic Units Database (ASUD)
kind: database
status: active
last_update: "updated daily (Geoscience Australia); snapshot 2026-10-22"
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
  licence: "CC-BY-4.0 (WFS AccessConstraints and the eCat record; copyright Geoscience Australia and the Geological Society of Australia)"
  routes:
    - {type: wfs, url: "https://services.ga.gov.au/gis/stratunits/ows (stratunit:StratigraphicUnit; also gsmlp:GeologicUnitView and gsmlb:GeologicUnit, same 18,357 units)", state: "live; CSV output, no feature cap", checked: 2026-10-22}
    - {type: web-ui, url: "https://asud.ga.gov.au/", state: "search interface; per-state, Antarctic and offshore zips of pipe-delimited text behind /search-state (names, definitions, references)", checked: 2026-10-22}
    - {type: catalogue, url: "eCat a05f7892-8ca9-7506-e044-00144fdd4fa6; https://pid.geoscience.gov.au/dataset/ga/21884", state: "metadata only; no DOI", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 (GeoServer); GeoSciML views alongside the native layer"
versioning:
  replay: none
  notes: "live register updated daily, with no releases; snapshot and record the date. The WFS warns that some attribute names have changed"
mirror:
  path: deep-server:/data/paleodata/asud
  policy: "dated snapshots of the native StratigraphicUnit layer"
  state: "snapshot 2026-10-22T0604Z_wfs, row count equals numberMatched"
lineage:
  upstream: ["National Register of Stratigraphic Names (from 1949); Australian Stratigraphy Commission and its state subcommissions"]
  downstream: ["Macrostrat name lexicon (12,279 names, 2015 import)", "Wikidata property P2367 (5,955 items)", "used here to check PBDB formation names and ages (pbdb entry)"]
eprp_questions: []
citation:
  - "Geoscience Australia, Australian Stratigraphic Units Database, https://services.ga.gov.au/gis/stratunits/ows, retrieved 2026-10-22, CC BY 4.0"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
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

ASUD began in 1949 as the National Register of Stratigraphic Names and is
the national standard for Australian geological names. Geoscience Australia
maintains it with the Australian Stratigraphy Commission, a standing
committee of the Geological Society of Australia: new names are reserved,
defined on a unit definition form and approved by a state or territory
subcommission. Card files ran to 1979, and some legacy information still
exists only on cards. GA states about 17,500 current names, 36,000 name
variations and 16,000 references, and daily updates. Every unit in the WFS is
marked "synthesis from multiple sources", and each has a persistent
identifier, `http://pid.geoscience.gov.au/geologicFeature/au/SU<STRATNO>`.
Macrostrat imported 12,279 ASUD names in 2015, and Wikidata links 5,955
items to ASUD identifiers.

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
- **Bulk text.** The search site offers per-state, Antarctic and offshore
  zips of pipe-delimited text with definitions and references, which the WFS
  lacks; not yet mirrored.
- **Mirror.** `deep-server:/data/paleodata/asud/raw/2026-10-22T0604Z_wfs/`
  (CSV and schema, read-only, sha256 manifest). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- National coverage under one schema with persistent identifiers.
- Ages are internally consistent for most units. Of 15,643 units with a real
  numeric age and a text age we can resolve (PBDB's interval table plus
  "Late Permian"-style series names; inverted ranges swapped), 14,662 (93.7%)
  lie within the named interval widened by 5% or 1 Myr, 923 (5.9%) overlap it
  but extend beyond, and 58 (0.4%) are disjoint.
- Full names are near-unique (17 duplicated in 18,357 units); folded names
  collide more (the independent review found 100 groups after dropping rank
  words), but with state and age the matching works: 93.9% of PBDB's named
  Australian collections find a unit, 77.3% exactly.
- Open licence and a simple, uncapped WFS.

## Weaknesses and pitfalls

- **Some numeric ages contradict the unit's own text age.** 58 units are
  disjoint from their text age; 36 of them by 5 Myr or less (scale and
  boundary differences), 22 by more. The clear errors include the Allaru
  Mudstone (STRATNO 291: "Albian" in text, 45–44 Ma in numbers, era
  "Cenozoic"), the Lagoon River Quartzite ("Neoproterozoic", 1,462–1,315 Ma),
  the Cundaline Formation and the Copper Hills Porphyry (Archean eras that
  disagree by 120–180 Myr). Six units described as "Cryogenian" carry ages of
  735–1,147 Ma, several older than the period's current base, which suggests
  older boundary definitions.
- **Inverted ranges.** 57 units have an older age younger than the younger
  age, among them the Buchargingah Granite (6 and 419.62 Ma), the Jindera
  Granite (40.4 and 403.4) and the Talbragar Fossil Fish Bed (151 and 161.5).
  Swap them before any age test; some, like Buchargingah's 6 Ma, are garbled
  as well as swapped.
- **Placeholder ages.** 337 units carry an older age of 4,031 Ma (313) or
  4,567 Ma (24), the base of the eon named in a vague text age ("Archean",
  "Precambrian"); 13 units of unknown age carry 0–0 Ma. A numeric filter reads
  the first as Hadean rocks and the second as Recent.
- **Era fields follow the numbers.** `OLDERAGE` and `YOUNGERAGE` give the era
  of the numeric ages, so they inherit numeric errors (the Allaru Mudstone is
  "Cenozoic"), and the convention at boundaries varies: an older age of 66 Ma
  is labelled Cenozoic (272 units), but 251.902 Ma and 538.8 Ma are labelled
  Paleozoic (261 and 433) and 2,500 Ma Neoarchean (674). Do not use them to
  check ages.
- **Untested units.** 351 units have numeric ages but no text age, and 124
  have a text age we could not resolve; 1,889 have no numeric age.
- **Gaps in fossiliferous Cenozoic units.** The Fyansford Formation, Muddy
  Creek Marl, Glen Aire Clay, Wataepoolan limestone and Black Rock Sandstone
  of Victoria, all classic fossil units, are not among the WFS layer's names
  or descriptions. GA lists about 36,000 name variations that the WFS does not
  carry, so some may exist as synonyms.
- **Homonyms.** "Cave Hill" (a Victorian sandstone and a Western Australian
  member) and "Black Rock" (a New South Wales subgroup and a Western Australian
  granodiorite) name unrelated units in different states; PBDB's "Glenelg" and
  "Drummond" match unrelated ASUD units of the same name. Match with state and
  age, not name alone.
- **Antarctic units are mixed in.** 561 units belong to the Australian
  Antarctic Territory; filter on `STATE` for continental work.

## Overlap with other sources

ASUD is the reference for PBDB's Australian stratigraphy; the matching and age
comparison are reported in the [PBDB entry](../pbdb/README.md#overlap-with-other-sources).
Macrostrat, PBDB's usual stratigraphic partner, has no Australian columns,
only ASUD-derived names from 2015, so ASUD is the live authority.

## EPRP relevance

ASUD serves any Australian deep-time case study that groups occurrences by
formation or needs independent unit ages: it normalises names, links units to
groups and basins, and flags age disagreements for checking. It has no fossil
content of its own.

## Citation and terms

CC BY 4.0. Cite Geoscience Australia, the service URL and the retrieval date.

## Verification log

- 2026-10-22, checked (not stored): WFS capabilities list three layers, each
  with `numberMatched` 18,357; licence text in `AccessConstraints`.
- 2026-10-22, checked: snapshot of `stratunit:StratigraphicUnit`, 18,357 CSV
  rows (the manifest records numberMatched 18,357); profile counts above.
- 2026-10-22, checked ([asud_profile.py](asud_profile.py)): text age against
  numeric age for the 15,643 units where both are usable, after swapping
  inverted ranges; placeholder, 0–0 and inverted ages; era labels at
  boundaries; the Allaru, Elcho Island and other records read directly.
- 2026-10-22, checked: absence of Fyansford, Muddy Creek, Glen Aire,
  Wataepoolan and Black Rock Sandstone by name search of the snapshot.
- 2026-10-22, inferred: the "Cryogenian" cases follow older period
  boundaries, from their numeric ages.
- 2026-10-22, independent review (Claude Sonnet subagent): found the first
  version of the age check counted inverted ranges as disagreements (76
  reported; 58 after the fix) and missed the placeholder ages; both corrected.
- 2026-10-22, source claim (documentation scan, Claude Sonnet subagent, URLs
  in its report): history from 1949, custodianship and naming procedure, the
  name and reference counts, daily updates, eCat and PID records with no DOI,
  the bulk zips, Macrostrat and Wikidata uses. No peer-reviewed assessment of
  ASUD's ages or names was found.
