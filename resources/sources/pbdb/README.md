---
id: pbdb
name: Paleobiology Database (PBDB)
kind: database
status: active
last_update: "live; newest record in the extract created 2026-10-21"
scope:
  taxa: ["all fossil groups: invertebrates, vertebrates, plants, microfossils, trace fossils"]
  time: "Archean to Holocene; the extract runs from the Paleoarchean (3,600 Ma interval bound) to the Holocene, 98.6% of occurrences Phanerozoic"
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
  indonesian_box_occurrences: "329 (260 New Guinea, Raja Ampat and Misool; 69 Seram)"
access:
  tier: open
  licence: "CC0 per the API datainfo and service configuration, changed from CC BY 4.0 in a commit of 2025-02-20; the Navigator page, GBIF and re3data still state CC BY 4.0. Record the datainfo licence with each snapshot"
  routes:
    - {type: api, url: "https://paleobiodb.org/data1.2/ (occs, colls, specs, refs, taxa, strata, intervals, timescales, archives)", state: "live; JSON, CSV, TSV; no key", checked: 2026-10-22}
    - {type: web-ui, url: "https://paleobiodb.org/classic/displayDownloadGenerator", state: "download generator builds the same API queries; can request a DOI archive", checked: 2026-10-22}
    - {type: archives, url: "https://paleobiodb.org/data1.2/archives/list.json?public=true", state: "47 DOI archives of stored downloads, all created 2019-05 to 2020-05", checked: 2026-10-22}
    - {type: gbif-dwca, url: "doi:10.15468/jfqhiu (IPT pbdb_paleo)", state: "Darwin Core subset; v1.3 of 2024-04 has 1.31 M of the 1.78 M live occurrences", checked: 2026-10-22}
  api: "REST data service 1.2; filters by country (cc), bounding box, interval (timerule default major), taxon, creation date; show= blocks select columns; pgm= selects palaeocoordinate models"
versioning:
  replay: partial
  notes: "no versioned releases or dumps. occs_created_before returns today's version of surviving records, not the past state. Collection `modified` is uninformative (92.5% share one 2025 timestamp); occurrence `modified` precedes `created` for 17.1%. Classification and interval ages are recomputed from current opinions and time scales. DOI archives (2019-2020 only) and our dated snapshots are the only fixed copies"
mirror:
  path: deep-server:/data/paleodata/pbdb
  policy: "dated regional snapshots kept indefinitely, because PBDB has no archive of its own; plus the interval table"
  state: "au-ng 2026-10-22T0602Z (current); au-png 2026-10-22T0556Z (first pass, AU and PG only); intervals 2026-10-22T0611Z"
lineage:
  upstream:
    - "published literature, entered and taxonomically reconciled by PBDB contributors; ten enterers account for 69% of the extract's occurrences"
  downstream:
    - "EPRP questions Q-006, Q-042, Q-044, Q-045 and Q-049 use the global database"
eprp_questions: [Q-006, Q-042, Q-044, Q-045, Q-049]
citation:
  - "The Paleobiology Database, https://paleobiodb.org, data service 1.2, with the query URL and retrieval date"
  - "Peters, S. E. & McClennen, M. (2016). The Paleobiology Database application programming interface. Paleobiology 42: 1-7. doi:10.1017/pab.2015.39"
  - "Uhen, M. D. et al. (2026). Paleobiology Database User Guide Version 2.0. PaleoBios 43(1): 1-54. doi:10.5070/P9.62178 (Version 1.0: PaleoBios 40(11), 2023, doi:10.5070/P9401160531)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22 (7 major, 30 minor findings); findings applied"
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
something else: almost half is pollen and plant records from a few lake and
swamp sequences, and it complements [FosSahul](../fossahul/README.md) rather
than duplicating it. PBDB is live and unversioned, so every analysis must
snapshot what it used.

## Contents

Counts are our own, from the 2026-10-22 snapshot: the general profile
([pbdb_core.tsv](profile/pbdb_core.tsv)) and targeted checks
([pbdb_checks.tsv](profile/pbdb_checks.tsv), from
[pbdb_checks.py](pbdb_checks.py)). Every CSV reconciles with the provider's
own count for the same query (for example 52,541 occurrences against
`records_found` 52,541).

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

Binning by midpoint hides straddlers: 1,917 occurrences (3.6%) span a period
boundary on PBDB's own time scale, half of them binned as Neogene and a
quarter as Paleogene. The collections column includes the 101 collections with
no occurrences.

- *Where.* Australia 51,243 occurrences, Papua New Guinea 1,200, Norfolk Island
  56, Christmas Island 33, Cocos (Keeling) 6, Heard Island 3. Australian
  occurrences by state label: Queensland 11,191, New South Wales 9,656,
  Victoria 8,975, Western Australia 8,771, South Australia 7,089, Tasmania
  2,517, Northern Territory 2,001, Australian Capital Territory 300, plus 681
  variant spellings (see the pitfalls). A separate bounding-box query (`_idng`
  files; [profile](profile/pbdb_idng.tsv)) adds 329 occurrences in 70
  collections: 260 from Indonesian New Guinea, Raja Ampat and Misool, and 69
  from 12 collections on Seram, which is in Wallacea, not New Guinea.
- *What.* Brachiopoda 9,791, Mollusca 9,237, Chordata 7,242 (including 1,904
  conodonts), Arthropoda 4,361, angiosperms 4,197, Cnidaria 3,577, Bryozoa
  2,102. Classes with most occurrences: Rhynchonellata 4,506, Strophomenata
  3,658, Bivalvia 3,589, Anthozoa 3,463, Gastropoda 3,190, Mammalia 2,479,
  Conodonta 1,904, Trilobita 1,865. 11,482 distinct accepted names; the taxa
  table holds 16,447 names (6,911 species, 6,135 genera).
- *Identification.* 35,238 occurrences are identified to species, 11,549 to
  genus. 15,425 identified names are genus-level placeholders (`sp.`,
  `indet.`); 4,470 are cf., aff. or queried; 4,576 name a new species (`n.
  sp.`). 1,689 occurrences have no accepted name.
- *Quaternary.* Of 8,898 occurrences (78 of them straddling the Pliocene),
  4,149 were entered by one contributor, almost all of them plant taxa (1,986
  coded as microspores, i.e. pollen and spores, 2,013 with no organ code, a
  few leaves and cuticles), from a few sequences: the
  Stony Creek Basin cores in Victoria (Sniderman 2011, 1,972), Lynch's Crater
  in Queensland (Kershaw 1976 and Kershaw et al. 2007, 1,882), and Regatta
  Point and other Tasmanian sites (Hill and Macphail 1985; Jordan et al.).
  1,307 are corals (two-thirds from Pandolfi 1996 and Greenstein and Pandolfi
  2008), and 2,339 are chordates (Mammalia 1,684, Aves 407, Reptilia 213,
  fishes 23, Amphibia 12). 1,066 occurrences come from caves.
- *Ages.* Ages are interval bounds, not measurements: the median occurrence
  spans 5.0 Myr, 9,787 span more than 10 Myr and 3,421 more than 20 Myr. 1,139
  occurrences carry a direct age, but they come from only 53 collections (14C
  677 occurrences in 13 collections, 608 of them Lynch's Crater; U/Th 225 in
  16; K–Ar 103 in 5; Sr isotope 78 in 8).
- *Specimens and measurements.* 5,310 specimens on 2,389 occurrences (962
  holotypes, 445 paratypes) and 11,897 measurements (length 4,814, width 4,602,
  height 1,994), mainly Permian brachiopods (57% of specimens), plus
  bivalves, insect wings and cephalopods.
- *References.* 2,038, of which 1,817 are journal articles; 1,084 have a DOI.
  Publication years run from 1820 to 2026, peaking in the 1980s–2000s.

## Provenance and lineage

PBDB is a community database for quantitative palaeobiology, run by an
Executive Committee (which also approves DOI archives). Contributors enter
records from the literature, each tied to a reference and an authorizer; the
classification shown for a record is computed from the current taxonomic
opinions, not stored with it (Peters and McClennen 2016). The data service and
its documentation are described by Peters and McClennen (2016) and the User
Guide (Uhen et al. 2023; version 2.0, 2026). The extract's data were entered
mostly in 2004–2016 (peak 2015, with 8,643 occurrences, 1,972 of them on one
day, 27 August 2015: the Stony Creek Basin pollen), and entry continues: 1,621
occurrences were created in 2025 and 1,106 so far in 2026. Ten enterers account
for 36,414 occurrences (69%); M. Clapham alone entered 11,485 (22%, mostly
Permian brachiopods), and C. Jaramillo 6,486 (including all 4,149 of the
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
  preservation and method fields, `n_occs` (a cached count that can lag), and
  palaeocoordinates.
- `specimens` (`specimen_no`, `occurrence_no`) and `measurements`
  (`measurement_no`, `specimen_no`).
- `references`, `taxa` (one row per taxon in the selected occurrences, with
  first and last appearances and ecological attributes), `strata` (one row per
  group/formation/member combination with occurrence counts).

Code vocabularies we found, with the traps:

- `difference` (accepted vs identified name), all 13 codes: blank 37,915;
  `species not entered` 7,760; `recombined as` 4,237; `taxon not entered`
  1,689; `rank change, species not entered` 366; `variant of` 324; and seven
  rarer misspelling, correction and reassignment codes (250 in all).
- `latlng_precision` mixes two vocabularies: `minutes` 2,420, `seconds` 2,339
  and `degrees` 478, beside decimal-place counts `1`–`8` (3,811 collections).
- `latlng_basis`: `based on nearby landmark` 3,785, `estimated from map` 2,865,
  `stated in text` 1,416, `based on political unit` 382, blank 593.
- `lithology1` values in literal quotes (`"limestone"` 2,150, `"siliciclastic"`
  1,531, `"shale"` 363) are PBDB's generic lithologies, distinct from the
  unquoted specific ones; the quotes are part of the value, and some
  `formation` values carry them too.
- `state` holds provinces for Papua New Guinea (Morobe, East New Britain) and
  is blank for the external territories.
- Palaeocoordinates: requesting `pgm=gplates,scotese,seton` adds numbered
  column sets (`paleomodel`, `paleolat`; `paleomodel2`, `paleolat2`; ...).
  `gplates` is Wright et al. (2013), `scotese` the PALEOMAP atlas (Scotese
  2021) and `seton` Seton et al. (2012), rotated by Macrostrat's service at
  the collection's age midpoint; `gplates` is the default. `geoplate` 801
  (Australia) for 8,401 collections and 800 (Papua New Guinea) for 83; where
  a model cannot compute, the column holds the text "not computable using
  this model".
- `max_ma` and `min_ma` are boundaries on PBDB's current time scales, which
  use GTS2020-era values: 11.63 Ma for the Late Miocene base appears 2,330
  times and the older 11.608 never; likewise 143.1, 419.62, 538.8 and 251.902
  appear and their predecessors do not. 90% of `max_ma` values equal a
  boundary of PBDB's international scale; the rest are regional stage and zone
  ages, mainly Australian Cambrian and Ordovician stages. (User Guide 2.0 still
  describes the scales as mostly Gradstein et al. 2012; the data have moved
  on, and a 2019 DOI archive still carries the older 11.608.)
- `updated`, `updater` and `updater_no` are blank in every row.

## Access

- **API.** No key. One request per table, filtered by country code; a
  bounding box picks up Indonesian New Guinea, where PBDB has no province
  filter (the box also catches Seram; filter on coordinates). The tested
  extraction script is [pbdb_snapshot.sh](pbdb_snapshot.sh): it requests every
  table with `vocab=pbdb` (full field names), the `show` blocks for full
  collection, ecology, taphonomy, abundance, stratigraphy, lithology,
  palaeolocation and entry history (`crmod,ent,entname`), all three plate
  models, and a `limit=0&rowcount` count for each table. The datainfo block
  records the defaults applied (`timerule` major, `taxon_status` all).
- **Mirror.** `deep-server:/data/paleodata/pbdb/`:
  `au-ng/raw/2026-10-22T0602Z_url/` (28 files, 150 MB, current),
  `au-png/raw/2026-10-22T0556Z_url/` (first pass: AU and PG only, without
  specimens, entry history or extra plate models) and
  `intervals/raw/2026-10-22T0611Z_url/` (the interval table, 1,909 rows, used
  to read ASUD's text ages). Index: [snapshots.tsv](snapshots.tsv). All raw
  files read-only with sha256 manifests.
- **DOI archives.** A download can be archived with a DOI on request, after
  Executive Committee approval; `archives/retrieve.csv?archive_id=N` returns
  the stored file, not a re-run. Only 47 exist, all from 2019–2020.
- **GBIF.** A Darwin Core subset (doi:10.15468/jfqhiu) is refreshed rarely;
  version 1.3 (April 2024) holds 1.31 million of 1.78 million occurrences.
- **Endpoint that fails.** `occs/opinions` returns HTTP 500 for the continent
  (it works for PNG alone); taxonomic opinions are global, so fetch them by
  taxon when needed.

## Strengths

- Breadth: every period, every fossil group, 9,048 collections across the
  continent, in one consistent schema with a maintained taxonomy.
- Every occurrence traces to a reference (2,038, 53% with DOI) and an enterer.
- The API is open, fast and documented; a full continental extract takes
  minutes, reconciles exactly with the provider's counts, and two extracts six
  minutes apart were identical.
- Formation names are mostly real and correctly dated: 77% of named Australian
  collections match a unit in Geoscience Australia's register
  ([ASUD](../asud/README.md)) exactly and another 17% on the core name, and
  95% of unique matches agree on age, against 12% for random units from the
  same state (see Overlap).
- Palaeocoordinates under three plate models, so model sensitivity can be
  tested without leaving the data service.
- Specimen measurements (11,897) for size studies, mainly Permian brachiopods.

## Weaknesses and pitfalls

- **No versions, and no replay.** The record a query returns today will differ
  tomorrow. `occs_created_before` keeps today's version of each surviving
  record, not the past state: a 2019 archive held 270 occurrences of
  *Carcharocles megalodon*, while the same creation-date filter now returns
  240. Timestamps do not help: 8,369 of 9,048 collections (92.5%) carry one
  `modified` timestamp (2025-02-22 15:12:02, a bulk update), and occurrence
  `modified` precedes `created` for 8,993 occurrences (17.1%), almost all
  created in 2010–2013, where `created` may record a migration rather than
  first entry. Classifications and interval ages are recomputed from current
  opinions and time scales. Snapshot and cite the query URL and date; our
  snapshots are the only fixed copies.
- **The licence statement depends on where you look.** The API and User
  Guide say CC0 (changed from CC BY 4.0 in the service code on 20 February
  2025, with no announcement found); the Navigator page, the GBIF dataset and
  re3data still say CC BY 4.0, and the IPT page also links CC BY-NC. Record
  the `datainfo` licence and access time with every download; data taken
  before 2025 were released under CC BY 4.0.
- **Ages are coarse.** Median span 5 Myr per occurrence; 19% span more than
  10 Myr; 3.6% straddle a period boundary. Time-binning choices drive results.
  Across PBDB, Flannery-Sutherland et al. (2022) find stratigraphically
  suspect occurrences in often more than 30% of genera in major groups.
- **Accepted names hide species.** For 7,283 occurrences identified at species
  rank (21% of species identifications; 7,606 counting compound codes), the
  species is not in PBDB's taxonomy, so `accepted_name` falls back to the
  genus (`species not entered`). Species-level work must use
  `identified_name` and reconcile it.
- **Placeholder classes.** `NO_CLASS_SPECIFIED` 8,127 occurrences (mostly
  plants and pollen), `NO_PHYLUM_SPECIFIED` 1,138 and blank phylum 1,771
  (mostly microfossils and Cambrian–Ordovician animals). Filter by taxon name,
  not class, for those groups.
- **State labels are free text.** Of 51,243 Australian occurrences, 681 carry
  misspelt or variant state names ("New south wales" 544, a leading space 26,
  "Queenslandd" 23, "Northern Teritorry" 19, "New South Whales"), 26 a
  sub-state place name (Yorke Peninsula, Kimberley), 31 "Macquarie Island";
  only 5 are blank. The other 1,030 blank labels are Papua New Guinea and the
  external territories. Use coordinates, after checking them (next item).
- **Coordinates are often approximate, and some are wrong.** 3,785 collections
  are placed from a nearby landmark and 382 from a political unit; 478 are
  precise only to a degree. One Australian collection has a negative
  longitude and two Papua New Guinea collections a northern latitude.
- **Palaeocoordinates are model-dependent and incomplete.** GPlates and
  Scotese palaeolatitudes differ by more than 10° for 2,537 collections, but
  93% of them are Cambrian to Carboniferous (median differences 12–16°); the
  Cretaceous differs by a median 7°, the Permian by 2°, and nothing from the
  Paleogene onwards differs by more than 10°. No model computes positions
  older than about 534 Ma (Macrostrat's service states 550 Ma); Seton stops
  at about 200 Ma, with one Induan collection as an exception. Nothing is
  computed for collections younger than about 0.39 Ma, for reasons PBDB does
  not document: 4,274 of the 8,898 Quaternary occurrences, including every
  occurrence younger than 0.39 Ma, lack palaeocoordinates, so filtering on a
  non-missing `paleolat` silently drops half the Quaternary. Wright et al.
  (2013) found the Early Devonian (Emsian) of south-eastern Australia poorly
  described by their model.
- **Formation names vary.** 68 normalised formation names appear under two or
  more raw spellings ("Parara" and "Parara Limestone"; "Miria", "Miria
  Calcarenite" and "Miria Marl"), and 1,642 Australian collections have no
  formation. Normalise names before counting formations.
- **Host-rock names on cave deposits.** In at least two collections
  Quaternary fossils carry the name of the host rock (a Chillagoe fissure
  fill under the Silurian–Devonian Chillagoe Formation; Wee Jasper under the
  Taemas Limestone member), so formation ages can contradict the fossils'
  ages by hundreds of millions of years. Most cave collections leave the
  formation blank.
- **Duplicated CSV columns.** Overlapping `show` blocks repeat 44 column names
  in the occurrences file (17 in collections). The duplicates hold identical
  values, but readers rename or drop them differently (pandas appends `.1`, R
  `make.unique`, a Python `DictReader` keeps the last).
- **Pseudo-collections.** 101 collections have `n_occs` 0, and 11 are "Extant
  Distribution" records of living species placed in the Holocene; 9
  occurrences are "Pseudofossil indet.".
- **Coverage follows projects.** One enterer supplied 22% of the extract's
  occurrences, and the Quaternary is dominated by two pollen projects. Any
  Australian richness or sampling analysis inherits that structure. Global
  studies find PBDB sampling especially limited in the Southern Hemisphere
  (Close et al. 2020) and concentrated in high-income countries (Raja et al.
  2022); we found no published assessment of PBDB's Australian coverage
  against an Australian compilation. The Australasian fossil mammal checklist
  (Jackson et al. 2024) is a candidate comparator.

## Overlap with other sources

- **ASUD (formation names and ages).** [pbdb_asud_match.py](pbdb_asud_match.py)
  matches each Australian collection's formation, group and member to ASUD:
  exactly (case, punctuation, trailing rank words and the spellings
  Harbor/Harbour and Mt/Mount folded), then on a core name with lithology
  words also dropped, preferring units in the collection's state. Of 7,208
  Australian collections with a formation, 5,573 (77.3%) match exactly and
  1,192 (16.5%) on the core name; 48 match only units in other states (likely
  homonyms); 10 are ambiguous; 385 do not match. Among the largest unmatched
  names, Muddy Creek, Fyansford, Glen Aire and Wataepoolan are Victorian
  Cenozoic units absent from ASUD's WFS names; Tambo and Lockup Well are
  other gaps. Of the 6,765 unique matches, 25 have no ASUD
  age; of the other 6,740, 6,414 (95.2%) overlap ASUD's age range (exact
  matches 95.8%, core-name matches 92.2%), against 12% when each collection is
  paired with a random dated ASUD unit from its state. 178 miss by up to
  5 Myr, 120 by 5–20 Myr and 28 by more
  ([examples](profile/pbdb_asud_examples.tsv)); 24 of those 28 are one ASUD
  error, the Allaru Mudstone (45–44 Ma in ASUD's numbers but Albian in its own
  text), and the rest are Chillagoe, Rouge, Frere and Elcho Island. At group
  and member level the large misses include a homonym (Glenelg, 27
  collections) and the Taemas Limestone host-rock case. Groups match at 92%
  and members at 68% of named collections; most unmatched members are
  informal ("Upper", "Unit 3").
- **FosSahul (Late Quaternary vertebrates).**
  [pbdb_fossahul_overlap.py](pbdb_fossahul_overlap.py) compares PBDB's 414
  Quaternary tetrapod collections with FosSahul's 438 distinct coordinate
  sites. Only 78 PBDB collections lie within 5 km of a FosSahul site, and 245
  lie more than 25 km from any; FosSahul sites lie a median 26 km from the
  nearest PBDB collection. Where they coincide, coverage is bimodal: 39 of the
  78 collections have all their genera in FosSahul nearby, 17 share none, and
  overall 372 of 613 collection-genus records (61%) are shared. PBDB holds 279
  tetrapod genera and FosSahul 219, sharing 131; PBDB's extras are mostly
  birds (96 genera). 25 of FosSahul's 31 megafauna genera (counting a
  pseudo-genus) occur in PBDB, in 282 collections, some only for *Macropus*.
  The two are largely complementary: FosSahul holds dated, quality-rated
  records, while PBDB holds occurrences, many undated beyond their interval,
  mostly at other localities. (The 414 include 10 Norfolk Island collections.)
- **Neotoma.** PBDB's Quaternary plant records overlap Neotoma only at Lynch's
  Crater (22 collections, 1,863 occurrences within 5 km of a Neotoma pollen
  site); the Stony Creek Basin and Tasmanian records are PBDB-only
  ([Neotoma](../neotoma/README.md)).
- **Macrostrat.** PBDB's usual stratigraphic partner has no Australian
  columns (a placeholder project). Its name lexicon includes 12,279 names
  imported from ASUD (2015), but links no PBDB collections to the Australian
  names tested (Gogo, Wallumbilla). No PBDB–ASUD crosswalk exists apart from
  the matching above.
- **NSB and Triton.** Negligible: PBDB's Australian extract is onshore outcrop
  and cores; four collections name ocean-drilling sites (ODP Leg 194, Marion
  Plateau; Sites 823 and 824 on the Queensland Plateau).

## EPRP relevance

The global PBDB feeds Q-006, Q-042, Q-044, Q-045 and Q-049. Three findings
here bear on them. Neither `created` filtering nor timestamps reconstruct a
past state: collection `modified` is a bulk timestamp, occurrence `modified`
precedes `created` for 17% of rows, and classifications and interval ages
are recomputed (Q-045's creation-date filter and any replication of an older
download). Interval boundaries now follow GTS2020-era values, so ages from a
download made before the change differ from today's for the same records.
And plate-model choice matters most for the early Palaeozoic: in this extract
GPlates and Scotese palaeolatitudes differ by more than 10° for nearly all
Cambrian and most Silurian to Carboniferous collections, but little after the
Permian (the global fraction is unmeasured). For Australian case studies the
extract supports Palaeozoic marine diversity and turnover, Cenozoic
vertebrate and plant records, and size studies of Permian brachiopods. It
cannot support Late Quaternary extinction chronologies (use FosSahul) or
anything needing ages finer than the stratigraphic interval.

## Citation and terms

CC0 per the API (`data_license`) since 2025; CC BY 4.0 from December 2013
until then. Cite PBDB with the data-service query URL and retrieval date
(Peters and McClennen 2016 for the service), and the primary references for
the records used. Citing PBDB also satisfies the older CC BY terms.

## Verification log

- 2026-10-22, checked: API probes for AU,PG counts (occurrences 52,443;
  collections 9,005) and the datainfo licence string; first snapshot
  (`au-png`) reconciled.
- 2026-10-22, checked: second snapshot (`au-ng`) adding NF, CX, CC, HM, an
  Indonesian box, specimens, measurements, entry history and three plate
  models; every table's row count equals its `records_found`.
- 2026-10-22, checked ([pbdb_profile.py](pbdb_profile.py)): duplicated column
  names hold identical values; profile counts above.
- 2026-10-22, checked ([pbdb_checks.py](pbdb_checks.py)): the two snapshots
  return the same 52,443 AU and PG occurrences with identical values in all
  135 shared columns; state-label partition; Quaternary composition by
  enterer, reference and organ; plate-model coverage and palaeolatitude
  differences by period; time-scale boundary values; timestamps; direct ages
  by collection; identification qualifiers and `species not entered` by rank;
  all difference codes; ocean-drilling collections; the Seram collections in
  the Indonesian box; coordinate sanity.
- 2026-10-22, checked: ASUD formation matching, age agreement and the
  random-unit null; FosSahul site and genus overlap; Neotoma overlap.
- 2026-10-22, checked (not stored): `occs/opinions` HTTP 500 for AU,PG;
  `timescales/list` works.
- 2026-10-22, source claim (documentation scan, Claude Sonnet subagent, URLs
  in its report): licence change commit of 2025-02-20 and the pages still
  stating CC BY 4.0; DOI archives (47, 2019–2020) and the 270-versus-240
  replay test; GBIF DwC-A versions; plate-model identities and Macrostrat's
  stated limits; `timerule`; Macrostrat's Australian holdings; the cited
  critiques; the User Guide's statement on time scales (contradicted by the
  data, as noted).
- 2026-10-22, independent review (Claude Sonnet subagent): recomputed the
  numbers above with its own code; corrected the scope of the `modified`,
  palaeolatitude and state-label claims, the time-scale claim, the Seram
  records, the FosSahul genus overlap and several counts.
- 2026-10-22, inferred: Australian coverage reflects contributor projects,
  from the enterer and reference concentration.
