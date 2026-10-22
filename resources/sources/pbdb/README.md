---
id: pbdb
name: Paleobiology Database (PBDB)
kind: database
status: active
last_update: "live; newest Australian records created 2026-10"
scope:
  taxa: [all fossil groups; invertebrates, vertebrates, plants, microfossils, trace fossils]
  time: "Archean to Holocene; the Australian extract runs from 3,400 Ma to the Holocene, almost all of it Phanerozoic"
  space: "global; mirrored here as an Australia and New Guinea extract (route au-ng) with Australia's external territories"
  record_unit: "occurrence: one taxon identified in one collection (a locality and horizon), dated by its stratigraphic interval"
size:
  as_of: "route au-ng snapshot 2026-10-22T0602Z (core: cc=AU,PG,NF,CX,CC,HM)"
  occurrences: 52541
  collections: 9048
  references: 2038
  taxa: 16447
  specimens: 5310
  measurements: 11897
  strata: 1139
  indonesian_new_guinea_occurrences: 329
access:
  tier: open
  licence: "CC0 per the API's datainfo block (data_license Creative Commons CC0)"
  routes:
    - {type: api, url: "https://paleobiodb.org/data1.2/ (occs, colls, specs, refs, taxa, strata, intervals)", state: "live; JSON, CSV, TSV; no key", checked: 2026-10-22}
    - {type: web-ui, url: "https://paleobiodb.org/classic/displayDownloadGenerator", state: "download generator builds the same API queries", checked: 2026-10-22}
  api: "REST data service 1.2; filters by country (cc), bounding box, interval, taxon; show= blocks select columns; pgm= selects palaeocoordinate models"
versioning:
  replay: partial
  notes: "no versioned releases. Records carry created timestamps, but `modified` was bulk-overwritten (2025-02-22 for 93% of Australian collections), so a past state cannot be rebuilt. Our dated snapshots are the only fixed copies"
mirror:
  path: deep-server:/data/paleodata/pbdb
  policy: "dated regional snapshots kept indefinitely, because PBDB has no archive of its own; plus the interval table"
  state: "au-ng 2026-10-22T0602Z (current); au-png 2026-10-22T0556Z (first pass, AU and PG only); intervals 2026-10-22T0611Z"
lineage:
  upstream:
    - "published literature, entered and taxonomically reconciled by PBDB contributors; ten enterers account for 69% of Australian occurrences"
  downstream:
    - "most global Phanerozoic diversity analyses; EPRP questions Q-006, Q-042, Q-044, Q-045 and Q-049 use the global database"
eprp_questions: [Q-006, Q-042, Q-044, Q-045, Q-049]
citation:
  - "The Paleobiology Database, https://paleobiodb.org, data service 1.2, with the query URL and retrieval date"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Paleobiology Database (PBDB)

## Summary

PBDB is the main global database of fossil occurrences: a taxon recorded in a
collection (a fossil locality and horizon), dated by the stratigraphic interval
it was found in, tied to the publication it came from and to a maintained
taxonomy. This entry describes PBDB through its Australian and New Guinean
extract, the first part of it we have mirrored: 52,541 occurrences in 9,048
collections from 2,038 references, plus specimens, measurements, taxa and
strata, with palaeocoordinates under three plate models. Reach for it for deep
time: Australia's Palaeozoic marine faunas (Permian brachiopods, Devonian reefs,
Cambrian shelly faunas), Mesozoic and Cenozoic vertebrates and plants, and
anything that needs occurrences in a global context. Its Quaternary content is
something else: about half is pollen counts from a few lake cores, and it is a
complement to [FosSahul](../fossahul/README.md), not a substitute. PBDB is live
and unversioned, so every analysis must snapshot what it used.

## Contents

Counts are our own ([profile](profile/pbdb_core.tsv)) from the 2026-10-22
snapshot. Every CSV reconciles with the provider's own count for the same
query (for example 52,541 occurrences against `records_found` 52,541).

| Period (interval midpoint) | Occurrences | Collections |
| --- | ---: | ---: |
| Quaternary | 8,898 | 716 |
| Neogene | 5,452 | 535 |
| Paleogene | 3,519 | 464 |
| Cretaceous | 4,017 | 664 |
| Jurassic | 305 | 92 |
| Triassic | 1,004 | 166 |
| Permian | 9,822 | 2,843 |
| Carboniferous | 2,305 | 324 |
| Devonian | 6,835 | 1,360 |
| Silurian | 1,689 | 266 |
| Ordovician | 2,444 | 502 |
| Cambrian | 5,522 | 968 |
| Ediacaran | 287 | 64 |
| Older | 442 | 84 |
| **Total** | **52,541** | **9,048** |

- *Where.* Australia 51,243 occurrences, Papua New Guinea 1,200, Norfolk Island
  56, Christmas Island 33, Cocos (Keeling) 6, Heard Island 3. By state:
  Queensland 11,191, New South Wales 9,656, Victoria 8,975, Western Australia
  8,771, South Australia 7,089, Tasmania 2,517, Northern Territory 2,001 (raw
  labels; see the pitfalls). A separate bounding-box query
  (`_idng` files; [profile](profile/pbdb_idng.tsv)) adds 329 occurrences in 70
  collections from Indonesian New Guinea, Raja Ampat and Misool: mostly Neogene,
  Triassic and Permian.
- *What.* Brachiopoda 9,791, Mollusca 9,237, Chordata 7,242, Arthropoda 4,361,
  angiosperms 4,197, Cnidaria 3,577, Bryozoa 2,102. Classes with most
  occurrences: Rhynchonellata 4,506, Strophomenata 3,658, Bivalvia 3,589,
  Anthozoa 3,463, Gastropoda 3,190, Mammalia 2,479, Conodonta 1,904, Trilobita
  1,865. 11,482 distinct accepted names; the taxa table holds 16,447 names
  (6,911 species, 6,135 genera).
- *Identification.* 35,238 occurrences are identified to species, 11,549 to
  genus; 20,349 identified names contain a qualifier (cf., aff., ?, sp.,
  indet.). 1,689 occurrences have no accepted name.
- *Quaternary.* Of 8,898 occurrences, 4,149 are plant records, mostly pollen
  and spores, entered by one contributor from a few sequences: the Stony Creek
  Basin cores in Victoria (Sniderman 2011, 1,972), Lynch's Crater in Queensland
  (Kershaw 1976 and Kershaw et al. 2007, 1,882), and Regatta Point and other
  Tasmanian sites (Hill and Macphail 1985; Jordan et al.). 1,307 are corals
  (Pandolfi 1996, Greenstein and Pandolfi 2008), and 2,304 are vertebrates
  (Mammalia 1,684, Aves 407, Reptilia 213). Caves supply 1,066 occurrences.
- *Ages.* Ages are interval bounds, not measurements: the median occurrence
  spans 5.0 Myr, 9,787 span more than 10 Myr and 3,421 more than 20 Myr. 1,139
  occurrences also carry a direct age (14C 677, U/Th 225, K–Ar 103, Sr isotope
  78).
- *Specimens and measurements.* 5,310 specimens on 2,389 occurrences (962
  holotypes, 445 paratypes) and 11,897 measurements (length 4,814, width 4,602,
  height 1,994), overwhelmingly Permian brachiopods, plus bivalves, insect wings
  and cephalopods.
- *References.* 2,038, of which 1,817 are journal articles; 1,084 have a DOI.
  Publication years run from 1820 to 2026, peaking in the 1980s–2000s.

## Provenance and lineage

PBDB began in 1998 as a community database for quantitative palaeobiology and
is governed by an executive committee; records are entered by contributors from
the literature, each tied to a reference and an authorizer. Australian data
were entered mostly in 2004–2016 (peak 2015, with 8,643 occurrences), and entry
continues: 1,621 occurrences were created in 2025 and 1,106 so far in 2026. Ten
enterers account for 36,414 occurrences (69%); M. Clapham alone entered 11,485
(22%, mostly Permian brachiopods), and C. Jaramillo 6,486 (including all 4,149
Quaternary plant records). The emphasis of Australian coverage reflects those
projects, not the Australian fossil record.

## Structure

The data service returns flat tables, one per endpoint, keyed by integers:

- `occurrences`: `occurrence_no`, `collection_no`, `reid_no` (a
  reidentification, 750 rows), identified and accepted names and ranks with
  the `difference` between them, classification (phylum to genus), interval
  names and `max_ma`/`min_ma`, abundance, then the full collection context
  repeated on every row.
- `collections`: `collection_no`, coordinates with `latlng_basis` and
  `latlng_precision`, geography (`cc`, `state`, `county`), stratigraphy
  (`formation`, `geological_group`, `member`, `zone`), lithology, environment,
  preservation and method fields, `n_occs`, and palaeocoordinates.
- `specimens` (`specimen_no`, `occurrence_no`) and `measurements`
  (`measurement_no`, `specimen_no`).
- `references`, `taxa` (one row per taxon in the selected occurrences, with
  first and last appearances and ecological attributes), `strata` (one row per
  group/formation/member combination with occurrence counts).

Code vocabularies we found, with the traps:

- `difference` (accepted vs identified name): blank 37,915; `species not
  entered` 7,760; `recombined as` 4,237; `taxon not entered` 1,689; `rank
  change, species not entered` 366; `variant of` 324; misspelling and
  correction codes 199.
- `latlng_precision` mixes two vocabularies: `minutes` 2,420, `seconds` 2,339
  and `degrees` 478, beside decimal-place counts `1`–`8` (3,811 collections).
- `latlng_basis`: `based on nearby landmark` 3,785, `estimated from map` 2,865,
  `stated in text` 1,416, `based on political unit` 382, blank 593.
- `lithology1` values in literal quotes (`"limestone"` 2,150, `"siliciclastic"`
  1,531, `"shale"` 363) are PBDB's generic lithologies, distinct from the
  unquoted specific ones; the quotes are part of the value.
- Palaeocoordinates: requesting `pgm=gplates,scotese,seton` adds numbered
  column sets (`paleomodel`, `paleolat`; `paleomodel2`, `paleolat2`; ...).
  `geoplate` 801 (Australia) for 8,401 collections, 800 for 83.

## Access

- **API.** No key. One request per table, filtered by country code; a
  bounding box picks up Indonesian New Guinea, where PBDB has no province
  filter. The tested extraction script is [pbdb_snapshot.sh](pbdb_snapshot.sh):
  it requests every table with `vocab=pbdb` (full field names), the `show`
  blocks for full collection, ecology, taphonomy, abundance, stratigraphy,
  lithology, palaeolocation and entry history (`crmod,ent,entname`), all three
  plate models, and a `limit=0&rowcount` count for each table.
- **Mirror.** `deep-server:/data/paleodata/pbdb/`:
  `au-ng/raw/2026-10-22T0602Z_url/` (28 files, 150 MB, current),
  `au-png/raw/2026-10-22T0556Z_url/` (first pass: AU and PG only, without
  specimens, entry history or extra plate models) and
  `intervals/raw/2026-10-22T0611Z_url/` (the interval table, 1,909 rows, used
  to read ASUD's text ages). Index: [snapshots.tsv](snapshots.tsv). All raw
  files read-only with sha256 manifests.
- **Endpoints that fail.** `occs/opinions` returns HTTP 500 for the continent
  (it works for PNG alone); taxonomic opinions are global, so fetch them by
  taxon when needed. `scales/list` returns 404.

## Strengths

- Breadth: every period, every fossil group, 9,048 collections across the
  continent, in one consistent schema with a maintained taxonomy.
- Every occurrence traces to a reference (2,038, 53% with DOI) and an enterer.
- The API is open, fast and documented; a full continental extract takes
  minutes and reconciles exactly with the provider's counts.
- Formation names are mostly real: 93.8% of named Australian collections
  match a unit in Geoscience Australia's register ([ASUD](../asud/README.md)),
  and 95.2% of the unique matches with ASUD ages agree on age (see Overlap).
- Palaeocoordinates under three plate models, so model sensitivity can be
  tested without leaving the data service.
- Specimen measurements (11,897) for size studies, mainly Permian brachiopods.

## Weaknesses and pitfalls

- **No versions, and no replay.** The record a query returns today will differ
  tomorrow. `created` dates survive, but filtering on them keeps today's
  version of each record, not the past state. `modified` cannot identify
  changes: 8,369 of 9,048 Australian collections (93%) carry
  `modified` 2025-02-22, a bulk update. Snapshot and cite the query URL and
  date; our snapshots are the only fixed copies.
- **Ages are coarse.** Median span 5 Myr per occurrence; 19% span more than
  10 Myr. Time-binning choices drive results.
- **Accepted names hide species.** For 7,760 occurrences identified to species
  (22% of species identifications), the species is not in PBDB's taxonomy, so
  `accepted_name` falls back to the genus (`species not entered`). Species-level
  work must use `identified_name` and reconcile it.
- **Placeholder classes.** `NO_CLASS_SPECIFIED` 8,127 occurrences,
  `NO_PHYLUM_SPECIFIED` 1,138, blank phylum 1,771: mostly plants and pollen.
  Filter by taxon name, not class, for those groups.
- **State labels are free text.** Beyond the canonical names, at least 697
  occurrences carry misspelt or variant labels ("Queenslandd", "New South
  Whales", "Northern Teritorry", "New south wales" 544, a leading space) and
  1,035 have none. Use coordinates.
- **Coordinates are often approximate.** 3,785 collections are placed from a
  nearby landmark and 382 from a political unit; 478 are precise only to a
  degree.
- **Palaeocoordinates are model-dependent and incomplete.** GPlates and
  Scotese palaeolatitudes differ by a median of 4.9° and by more than 10° for
  2,537 collections (the Cambrian Ranken Limestone sits at 7.6° under GPlates,
  26.1° under Scotese). No model computes positions older than about 534 Ma;
  Seton stops at about 251 Ma. Nothing is computed for collections younger
  than about 0.39 Ma (381 of 716 Quaternary collections), so filtering on a
  non-missing `paleolat` silently drops half the Late Quaternary.
- **Formation names vary.** 66 formations appear under two or more raw names
  ("Parara" and "Parara Limestone"; "Miria", "Miria Calcarenite" and "Miria
  Marl"), and 1,642 Australian collections have no formation. Normalise names
  before counting formations.
- **Cave and fissure fills take their host rock's name.** Quaternary bones
  are entered under the Silurian–Devonian Taemas Limestone or Chillagoe
  Formation, so formation ages can contradict the fossils' ages by hundreds of
  millions of years.
- **Duplicated CSV columns.** Overlapping `show` blocks repeat 44 column names
  in the occurrences file (17 in collections). The duplicates hold identical
  values, but readers rename or drop them differently (pandas appends `.1`, R
  `make.unique`, a Python `DictReader` keeps the last).
- **Collections without occurrences.** 101 collections have `n_occs` 0.
- **Coverage follows projects.** One enterer supplied 22% of Australian
  occurrences, and the Quaternary is dominated by two pollen projects. Any
  Australian richness or sampling analysis inherits that structure.

## Overlap with other sources

- **ASUD (formation names and ages).** [pbdb_asud_match.py](pbdb_asud_match.py)
  matches each Australian collection's formation, group and member to ASUD:
  exactly (case, punctuation and trailing rank words folded), then on a core
  name with lithology words also dropped, preferring units in the collection's
  state. Of 7,208 Australian collections with a formation, 5,569 match exactly
  and 1,192 on the core name (93.8% together); 48 match only units in other
  states (likely homonyms); 10 are ambiguous; 389 do not match. The largest
  unmatched names by occurrences are Tambo, Muddy Creek, Fyansford, Macquarie
  Harbor and Lockup Well limestone; several of these Victorian Cenozoic units
  are absent from ASUD. Of the 6,761 unique matches, 25 have no ASUD age; of
  the other 6,736, 6,410 (95.2%) overlap ASUD's age range, 178 miss by up to
  5 Myr, 120 by 5–20 Myr and 28 by more
  ([examples](profile/pbdb_asud_examples.tsv)): homonyms (Glenelg), cave fills
  dated by host rock (Taemas, Chillagoe) and one ASUD error (the Allaru
  Mudstone, dated 45–44 Ma in ASUD but Albian in ASUD's own text field). Groups
  match at 92% and members at 68% of named collections; most unmatched members
  are informal ("Upper", "Unit 3").
- **FosSahul (Late Quaternary vertebrates).**
  [pbdb_fossahul_overlap.py](pbdb_fossahul_overlap.py) compares PBDB's 414
  Quaternary tetrapod collections with FosSahul's 438 coordinate sites. Only 78
  PBDB collections lie within 5 km of a FosSahul site, and 245 lie more than
  25 km from any; FosSahul sites lie a median 26 km from the nearest PBDB
  collection. Where they do coincide, PBDB's genera are almost all in FosSahul
  nearby (median 98%). PBDB holds 279 tetrapod genera and FosSahul 219, sharing
  131; PBDB's extras are mostly birds (96 genera). 25 of FosSahul's 31
  megafauna genera occur in PBDB, in 282 collections. The two are largely
  complementary: FosSahul holds dated, quality-rated records, while PBDB holds
  occurrences, many undated beyond their interval, at different localities.
- **NSB and Triton.** Negligible: PBDB's Australian extract is onshore
  outcrop and cores; one collection names an ocean-drilling site (ODP Leg 194,
  Marion Plateau).
- **Neotoma.** PBDB's Quaternary pollen (Lynch's Crater and others) overlaps
  Neotoma's Indo-Pacific pollen holdings; to be measured with the Neotoma entry.

## EPRP relevance

The global PBDB feeds Q-006, Q-042, Q-044, Q-045 and Q-049. Two findings here
bear on them directly: `modified` dates cannot identify records changed after a
cutoff (Q-045's creation-date filter), and palaeolatitudes differ between
models by more than 10° for over a quarter of collections (any latitudinal
analysis). For Australian case studies the extract supports Palaeozoic marine
diversity and turnover, Cenozoic vertebrate and plant records, and size
studies of Permian brachiopods. It cannot support Late Quaternary extinction
chronologies (use FosSahul) or anything needing ages finer than the
stratigraphic interval.

## Citation and terms

CC0 per the API (`data_license`). Cite PBDB with the data-service query URL
and retrieval date, and the primary references for the records used.

## Verification log

- 2026-10-22, checked: API probes for AU,PG counts (occurrences 52,443;
  collections 9,005) and the datainfo licence string; first snapshot
  (`au-png`) reconciled.
- 2026-10-22, checked: second snapshot (`au-ng`) adding NF, CX, CC, HM, an
  Indonesian New Guinea box, specimens, measurements, entry history and three
  plate models; every table's row count equals its `records_found`.
- 2026-10-22, checked: duplicated column names hold identical values (0
  mismatches across 52,541 rows).
- 2026-10-22, checked: profile counts above; Quaternary composition by
  reference and enterer; plate-model coverage by age.
- 2026-10-22, checked: ASUD formation matching and age agreement; FosSahul
  site and genus overlap.
- 2026-10-22, checked: `occs/opinions` HTTP 500 for AU,PG; `scales/list` 404.
- 2026-10-22, inferred: Australian coverage reflects contributor projects,
  from the enterer and reference concentration.
