---
id: pbdb
name: Paleobiology Database (PBDB)
kind: database
status: active
last_update: "live; global snapshot 2026-10-23T0133Z (records created to 2026-10-22)"
scope:
  taxa: ["all fossil groups: invertebrates, vertebrates, plants, microfossils, trace fossils"]
  time: "Archean to Holocene; 99.9% of occurrences Ediacaran or younger"
  space: "global; with an Australia and New Guinea region cut from the global snapshot"
  record_unit: "occurrence: one taxon identified in one collection (a locality and horizon), dated by its stratigraphic interval"
size:
  as_of: "global snapshot 2026-10-23T0133Z (public records only)"
  occurrences: 1782648
  collections: 278593
  references: 95905
  taxa: 409314
  opinions: 1016149
  specimens: 162604
  measurements: 366107
  region_au_ng_occurrences: 45991
  region_au_ng_collections: 9048
access:
  tier: open
  licence: "CC0 per the API datainfo and service configuration, changed from CC BY 4.0 in a commit of 2025-02-20; the Navigator page, GBIF and re3data still state CC BY 4.0. Record the datainfo licence with each snapshot"
  routes:
    - {type: api, url: "https://paleobiodb.org/data1.2/", state: "[Detail withheld pending disclosure to the data custodian.]", checked: 2026-10-23}
    - {type: web-ui, url: "https://paleobiodb.org/classic/displayDownloadGenerator", state: "download generator builds the same API queries; can request a DOI archive", checked: 2026-10-22}
    - {type: archives, url: "https://paleobiodb.org/data1.2/archives/list.json?public=true", state: "47 DOI archives of stored downloads, all created 2019-05 to 2020-05", checked: 2026-10-22}
    - {type: gbif-dwca, url: "https://doi.org/10.15468/jfqhiu", state: "Darwin Core subset (IPT pbdb_paleo); v1.3 of 2024-04 has 1.31 M of the 1.78 M occurrences", checked: 2026-10-22}
  api: "REST data service 1.2; filters by creation date, taxon, interval (timerule default major), country (cc) and bounding box; show= blocks select columns; pgm= selects palaeocoordinate models"
versioning:
  replay: partial
  notes: "no versioned releases or dumps; our dated global snapshots (and DOI archives of 2019-2020) are the only fixed copies. Creation-date filters return today's version of surviving records. 306,489 occurrences carry one creation stamp, 2025-09-21 22:25 (a bulk import of ocean-drilling microfossils), so created dates are not entry dates"
mirror:
  path: deep-server:/data/paleodata/pbdb
  policy: "dated global snapshots kept indefinitely; regions cut from them by committed code; the interval table"
  state: "[Detail withheld pending disclosure to the data custodian.]"
lineage:
  upstream:
    - "published literature, entered and taxonomically reconciled by PBDB contributors"
    - "since 2025-09-21, IODP shipboard micropalaeontology for 358 holes (306,489 occurrences)"
  downstream:
    - "most EPRP questions (43 of 68 name PBDB or depend on it), e.g. Q-006, Q-023, Q-030, Q-038, Q-042, Q-044, Q-045, Q-049, B-005"
    - "archived vintages: Close et al. 2019 (2017 download), Benson et al. 2025 (2022-05-23), Monarrez et al. 2023 (register-deposits entry)"
eprp_questions: [Q-002, Q-004, Q-006, Q-010, Q-013, Q-016, Q-018, Q-019, Q-020, Q-023, Q-025, Q-026, Q-027, Q-028, Q-029, Q-030, Q-033, Q-037, Q-038, Q-039, Q-040, Q-041, Q-042, Q-044, Q-045, Q-047, Q-049, B-001, B-003, B-005, B-007, B-008, B-009, B-010, B-013, B-014, B-015, B-018]
citation:
  - "The Paleobiology Database, https://paleobiodb.org, data service 1.2, with the query URL and retrieval date"
  - "Peters, S. E. & McClennen, M. (2016). The Paleobiology Database application programming interface. Paleobiology 42: 1-7. doi:10.1017/pab.2015.39"
  - "Uhen, M. D. et al. (2026). Paleobiology Database User Guide Version 2.0. PaleoBios 43(1): 1-54. doi:10.5070/P9.62178 (Version 1.0: PaleoBios 40(11), 2023, doi:10.5070/P9401160531)"
entry:
  created: 2026-10-22
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "the 2026-10-22 regional entry was reviewed (Claude Sonnet subagent; findings applied); this global revision is not yet reviewed"
---

# Paleobiology Database (PBDB)

## Summary

PBDB is the main global database of fossil occurrences: a taxon recorded in a
collection (a fossil locality and horizon), dated by the stratigraphic interval
it was found in, tied to the publication it came from and to a maintained
taxonomy. We now hold the whole public database: 1,782,648 occurrences in
278,593 collections from 95,905 references, with 409,314 taxa, 1,016,149
taxonomic opinions, 162,604 specimens and 366,107 measurements, and
palaeocoordinates under three plate models, pulled in creation-date
partitions that each reconcile exactly with PBDB's own counts. An Australia
and New Guinea region (45,991 occurrences) is cut from it by committed code.

[Detail withheld pending disclosure to the data custodian.]

## Contents

Counts are our own, from the global snapshot of 2026-10-23
([pbdb_global.tsv](profile/pbdb_global.tsv), from
[pbdb_global_profile.py](pbdb_global_profile.py)). Every occurrence and
collection partition, and the specimen, measurement, reference and taxon
tables, equal PBDB's `records_found` for the same query; the datainfo counts
before and after the pull agree (1,782,648).

| Period (interval midpoint) | Occurrences |
| --- | ---: |
| Quaternary | 233,121 |
| Neogene | 298,491 |
| Paleogene | 247,676 |
| Cretaceous | 232,839 |
| Jurassic | 154,825 |
| Triassic | 100,372 |
| Permian | 145,999 |
| Carboniferous | 76,700 |
| Devonian | 83,641 |
| Silurian | 54,412 |
| Ordovician | 112,925 |
| Cambrian | 37,722 |
| Ediacaran | 2,162 |
| Older or outside the table | 1,763 |
| **Total** | **1,782,648** |

- *Where (by the collection's country code and PBDB's continent table).*
  North America 542,595; Europe 462,554; Asia 240,893; South America 72,550;
  Africa 71,753; Australia 45,186; Oceania 22,219; Antarctica 10,105; Indian
  Ocean territories 5,386; no continent 309,407 (ocean-drilling and other
  marine codes, among them the whole 2025 import).
- *What.* Mollusca 418,562; Chordata 291,410; Foraminifera 188,578;
  Brachiopoda 178,841; Arthropoda 152,474; Haptophyta (coccolithophores)
  110,422; Radiozoa 57,487; Cnidaria 47,736. Accepted at species rank 854,985,
  genus 736,507; no accepted name 44,802.
- *Ages.* Median interval span 4.5 Myr (deciles 1.1 to 11.4 Myr).
- *Context.* 61% of occurrences have a formation on their collection; GPlates
  palaeolatitudes exist for 83%, Scotese 79%, Seton 51%.
- *Taxonomy.* 409,314 taxon names (166,595 accepted species and 95,771
  accepted genera) and 1,016,149 opinions.
- *The 2025 import.* 306,489 occurrences in 31,701 collections, all created
  2025-09-21 22:25, citing 162 references that are IODP expedition site
  reports (Site U1338 alone 9,244 occurrences): coccolithophores 79,508,
  diatoms 30,353, radiolarians 21,577, foraminifera (three classes) 30,230,
  and 132,919 with no class assigned; ages mostly Pleistocene to Miocene.
  Collections are named by expedition, hole, core and section (for example
  `363-U1482A-1H-CC`).

**Australia and New Guinea region** ([pbdb_core.tsv](profile/pbdb_core.tsv),
[pbdb_checks.tsv](profile/pbdb_checks.tsv), [pbdb_idng.tsv](profile/pbdb_idng.tsv)),
cut by [pbdb_region.py](pbdb_region.py) from the global snapshot: collections
coded AU, PG, NF, CX, CC or HM (core), and a box over Indonesian New Guinea
(`_idng`).

| Period (interval midpoint) | Occurrences | Collections |
| --- | ---: | ---: |
| Quaternary | 7,694 | 716 |
| Neogene | 4,047 | 535 |
| Paleogene | 3,188 | 464 |
| Cretaceous | 2,578 | 664 |
| Jurassic | 305 | 92 |
| Triassic | 1,004 | 166 |
| Permian | 9,819 | 2,843 |
| Carboniferous | 2,267 | 324 |
| Devonian | 5,654 | 1,360 |
| Silurian | 1,245 | 266 |
| Ordovician | 2,325 | 502 |
| Cambrian | 5,136 | 968 |
| Ediacaran | 287 | 64 |
| Older | 442 | 84 |
| **Total** | **45,991** | **9,048** |

[Detail withheld pending disclosure to the data custodian.]

- *Where.* Australia 45,186 occurrences, Papua New Guinea 707, Norfolk Island
  56, Christmas Island 33, Cocos (Keeling) 6, Heard Island 3. Australian
  occurrences by state label: Queensland 10,353, New South Wales 8,550,
  Western Australia 7,803, Victoria 7,780, South Australia 5,962, Tasmania
  2,446, Northern Territory 1,280, Australian Capital Territory 300, plus 662
  variant spellings. The Indonesian box adds 239 occurrences in 70
  collections: 204 from Indonesian New Guinea, Raja Ampat and Misool, and 35
  from Seram, which is in Wallacea, not New Guinea.
- *What.* Brachiopoda 9,618, Mollusca 8,129, Chordata 6,037 (799 conodonts),
  Arthropoda 4,261, angiosperms 4,124, Cnidaria 1,990, Bryozoa 1,988.
  Classes: Rhynchonellata 4,433, Strophomenata 3,658, Bivalvia 3,102,
  Gastropoda 2,611, Mammalia 2,468, Anthozoa 1,884, Trilobita 1,862. 10,470
  distinct accepted names.
- *Identification.* 29,996 occurrences are identified to species, 10,620 to
  genus. 14,362 identified names are genus-level placeholders (`sp.`,
  `indet.`); 4,048 are cf., aff. or queried; 4,325 name a new species. 1,438
  have no accepted name.
- *Quaternary.* Of 7,694 occurrences (78 straddling the Pliocene), 4,149
  were entered by one contributor, almost all plant taxa (1,986 coded as
  microspores, i.e. pollen and spores, 2,013 with no organ code), from a few
  sequences: the Stony Creek Basin cores in Victoria (Sniderman 2011, 1,972),
  Lynch's Crater in Queensland (Kershaw et al. 2007 and Kershaw 1976, 1,882),
  and Regatta Point and other Tasmanian sites. 2,339 are chordates (Mammalia
  1,684, Aves 407, Reptilia 213); 195 are corals; 1,160 come from caves,
  fissure fills and sinkholes.
- *Ages.* Median span 4.8 Myr; 8,520 span more than 10 Myr and 3,363 more
  than 20 Myr. 837 occurrences carry a direct age, from 30 collections (14C
  677 in 13, 608 of them Lynch's Crater; K–Ar 103 in 5).
- *Specimens and measurements.* 5,309 specimens on 2,388 occurrences (961
  holotypes, 445 paratypes) and 11,895 measurements (length 4,813, width
  4,601, height 1,994), mainly Permian brachiopods, plus bivalves, insect
  wings and cephalopods.
- *References.* 2,103 cited by the region's records, 1,870 of them journal
  articles; 1,112 have a DOI. Years 1825 to 2026.

## Provenance and lineage

PBDB is a community database for quantitative palaeobiology, run by an
Executive Committee (which also approves DOI archives). Contributors enter
records from the literature, each tied to a reference and an authorizer; the
classification shown for a record is computed from the current taxonomic
opinions, not stored with it (Peters and McClennen 2016). The data service and
its documentation are described by Peters and McClennen (2016) and the User
Guide (Uhen et al. 2023; version 2.0, 2026). Entry peaked in 2002–2013
(created years); 2025 is the largest year because of the IODP import.

In the Australian region, entry peaked in 2015 (8,177 occurrences, 1,970 of
them modified on one day, 27 August 2015: the Stony Creek Basin pollen), and
continues: 1,529 occurrences were created in 2025 and 1,105 so far in 2026.
Ten enterers account for 32,783 occurrences (71%); M. Clapham alone entered
11,484 (25%, mostly Permian brachiopods), and C. Jaramillo 6,477 (including
the 4,149 Quaternary plant records). Australian coverage reflects those
projects, not the Australian fossil record (inferred).

## Structure

The data service returns flat tables, one per endpoint, keyed by integers:

- [Detail withheld pending disclosure to the data custodian.]
- `collections`: coordinates with `latlng_basis` and `latlng_precision`,
  geography (`cc`, `state`, `county`), stratigraphy (`formation`,
  `geological_group`, `member`, `zone`), lithology, environment, preservation
  and methods, `n_occs`, palaeocoordinates.
- `specimens` and `measurements`; `references`; `taxa` (all names, with
  first and last appearances and `n_occs`); `opinions`; `intervals`.

Vocabularies and traps (counts for the region unless stated):

- `difference` (accepted vs identified name): blank 33,462; `species not
  entered` 6,684; `recombined as` 3,571; `taxon not entered` 1,438; `rank
  change, species not entered` 325; `variant of` 316; and rarer misspelling,
  correction and reassignment codes.
- `latlng_precision` mixes two vocabularies (`minutes`, `seconds`, `degrees`
  beside decimal-place counts); `latlng_basis` records how coordinates were
  placed (nearby landmark, map, text, political unit).
- `lithology1` values in literal quotes (`"limestone"`) are PBDB's generic
  lithologies; the quotes are part of the value.
- `taxon_rank` is blank in every row of the taxa table (`accepted_rank` is
  filled).
- Palaeocoordinates: `pgm=gplates,scotese,seton` adds numbered column sets
  (`paleolat`, `paleolat2`, `paleolat3`); `gplates` is Wright et al. (2013),
  `scotese` the PALEOMAP atlas and `seton` Seton et al. (2012); where a model
  cannot compute, the column holds the text "not computable using this model".
- `max_ma` and `min_ma` use GTS2020-era boundaries (11.63 Ma for the Late
  Miocene base appears 1,659 times in the region, the older 11.608 never);
  89% of region `max_ma` values equal a boundary of PBDB's international
  scale. User Guide 2.0 still describes the scales as mostly Gradstein et al.
  2012.
- `updated`, `updater` and `updater_no` are blank in every row.

## Access

- [Detail withheld pending disclosure to the data custodian.]
- **Regions.** [pbdb_region.py](pbdb_region.py) selects collections by `cc`
  or coordinates in the global collections table, which respects access, and
  takes their public occurrences, specimens, measurements, references and
  taxa.
- [Detail withheld pending disclosure to the data custodian.]
- **Mirror.** `deep-server:/data/paleodata/pbdb/`; index
  [snapshots.tsv](snapshots.tsv); raw files read-only with sha256 manifests.
- **DOI archives.** A download can be archived with a DOI on request, after
  Executive Committee approval; only 47 exist, all from 2019–2020.
- **GBIF.** A Darwin Core subset (doi:10.15468/jfqhiu) is refreshed rarely;
  version 1.3 (April 2024) holds 1.31 million of 1.78 million occurrences.

## Strengths

- Breadth: every period and fossil group, worldwide, in one schema with a
  maintained taxonomy and its opinions; a complete public snapshot takes half
  an hour and reconciles exactly with the provider's counts.
- Every occurrence traces to a reference and an enterer.
- Formation names are mostly real and correctly dated in Australia: 77% of
  named Australian collections match a unit in Geoscience Australia's
  register ([ASUD](../asud/README.md)) exactly and another 17% on the core
  name, and 95% of unique matches agree on age, against 12% for random units
  from the same state.
- Palaeocoordinates under three plate models.
- Specimen measurements (366,107 globally) for size studies.

## Weaknesses and pitfalls

- [Detail withheld pending disclosure to the data custodian.]
- **No versions, and no replay.** `occs_created_before` returns today's
  version of each surviving record, not the past state: a 2019 archive held
  270 occurrences of *Carcharocles megalodon*, while the same creation-date
  filter now returns 240 (documentation scan). Created dates are not entry
  dates: 306,489 occurrences carry one stamp from 2025, `modified` precedes
  `created` for 206,708 (12%), and 8,369 of 9,048 Australian collections
  (92.5%) share one `modified` timestamp (2025-02-22 15:12:02). Snapshot and
  cite the query URL and date; dated snapshots are the only fixed copies.
- **One import is 17% of the database.** The 2025 IODP microfossil import
  changes Cenozoic marine counts and diversity curves; filter by reference or
  collection-name pattern when it should be excluded or treated separately
  (see Overlap: NSB).
- **The licence statement depends on where you look.** The API and User
  Guide say CC0 (changed from CC BY 4.0 in the service code on 20 February
  2025); the Navigator page, the GBIF dataset and re3data still say CC BY 4.0.
  Record the `datainfo` licence with every download.
- **Ages are coarse.** Median span 4.5 Myr globally; time-binning choices drive
  results. Flannery-Sutherland et al. (2022) find stratigraphically suspect
  occurrences in often more than 30% of genera in major groups.
- **Accepted names hide species.** In the region, for 6,219 occurrences
  identified at species rank (21% of species identifications; 6,476 counting
  compound codes), the species is not in PBDB's taxonomy, so `accepted_name`
  falls back to the genus. Species-level work must use `identified_name`.
- **Placeholder classes.** Globally `NO_CLASS_SPECIFIED` 260,741 occurrences
  and `NO_PHYLUM_SPECIFIED` 23,536 (in the region 7,510 and 1,092; mostly
  plants, pollen and microfossils). Filter by taxon name for those groups.
- **State labels are free text.** Of 45,186 Australian occurrences, 662 carry
  misspelt or variant state names ("New south wales" 544, a leading space 26,
  "Queenslandd" 23), 14 a sub-state place name, 31 "Macquarie Island", 5 are
  blank. Use coordinates, after checking them.
- **Coordinates are often approximate, and some are wrong.** Many Australian
  collections are placed from a nearby landmark or a political unit; one has a
  negative longitude and two Papua New Guinea collections a northern
  latitude.
- **Palaeocoordinates are model-dependent and incomplete.** In the region,
  GPlates and Scotese palaeolatitudes differ by more than 10° mainly for
  Cambrian to Carboniferous collections (medians 12–16°), by a median 7° in
  the Cretaceous and 2° in the Permian. No model computes positions older
  than about 534 Ma, Seton stops at about 251 Ma, and nothing is computed
  younger than about 0.39 Ma: 3,070 of the region's 7,694 Quaternary
  occurrences, including all 2,725 younger than 0.39 Ma, lack
  palaeocoordinates.
- **Formation names vary, and caves borrow host-rock names.** Normalise
  formation names before counting; in at least two Australian collections
  Quaternary fossils carry the name of a Palaeozoic host rock.
- **Duplicated CSV columns.** Overlapping show blocks repeat column names (17
  in collections); readers rename or drop them differently.
- [Detail withheld pending disclosure to the data custodian.]
- **Coverage follows projects.** One enterer supplied 25% of the region's
  occurrences; global studies find PBDB sampling especially limited in the
  Southern Hemisphere (Close et al. 2020) and concentrated in high-income
  countries (Raja et al. 2022).

## Overlap with other sources

- **NSB.** [pbdb_nsb_overlap.py](pbdb_nsb_overlap.py)
  ([output](profile/pbdb_nsb.tsv)) parses the drilling collections' names to
  NSB's hole keys. All 358 holes in the 2025 import are NSB holes, but only
  5,008 of its 31,676 parsed collections (59,024 of 306,358 occurrences) lie
  at a core NSB sampled, and NSB holds 4,294 samples in those holes. The
  import is new, denser shipboard data rather than a copy of NSB; combining
  the two needs sample-level reconciliation, and analyses of Cenozoic
  plankton in PBDB now include IODP data that NSB-based work (and Triton) may
  also hold.
- [Detail withheld pending disclosure to the data custodian.]
- **FosSahul (Late Quaternary vertebrates).**
  [pbdb_fossahul_overlap.py](pbdb_fossahul_overlap.py)
  ([output](profile/pbdb_fossahul.tsv)): of PBDB's 414 Quaternary tetrapod
  collections, only 78 lie within 5 km of a FosSahul site and 245 more than
  25 km from any; PBDB holds 279 tetrapod genera and FosSahul 219, sharing
  131. The two are largely complementary.
- **Neotoma.** PBDB's Quaternary plant records overlap Neotoma only at
  Lynch's Crater ([Neotoma](../neotoma/README.md)).
- **Macrostrat.** No Australian columns; its name lexicon holds 12,279 names
  imported from ASUD (2015).
- **Archived PBDB vintages.** Close et al. 2019, Benson et al. 2025 and
  Monarrez et al. 2023 deposit PBDB downloads of 2017, 2022 and about 2023
  ([register-deposits](../register-deposits/README.md)); with our dated
  snapshots they support data-vintage work (Q-045).

## EPRP relevance

PBDB is the most-needed source in the EPRP registers (43 of 68 questions).
[Detail withheld pending disclosure to the data custodian.] The Australian
region supports Palaeozoic marine diversity and turnover, Cenozoic vertebrate
and plant records, and Permian brachiopod size studies; it cannot support Late
Quaternary extinction chronologies (use FosSahul) or ages finer than the
stratigraphic interval.

## Citation and terms

CC0 per the API (`data_license`) since 2025; CC BY 4.0 from December 2013
until then. Cite PBDB with the data-service query URL and retrieval date
(Peters and McClennen 2016 for the service), and the primary references for
the records used.

## Verification log

- 2026-10-23, checked ([pbdb_global_profile.py](pbdb_global_profile.py),
  [output](profile/pbdb_global.tsv)): every occurrence and collection
  partition and the specimen, measurement, reference and taxon tables equal
  their rowcounts; creation times inside each window; no duplicates; datainfo
  1,782,648 before and after. A first public pull 30 minutes earlier gave the
  same counts but for one occurrence's classification.
- [Detail withheld pending disclosure to the data custodian.]
- 2026-10-23, checked ([pbdb_profile.py](pbdb_profile.py),
  [pbdb_checks.py](pbdb_checks.py), on the region from
  [pbdb_region.py](pbdb_region.py)): the regional counts above; region tables
  equal the region builder's counts.
- 2026-10-23, checked ([pbdb_nsb_overlap.py](pbdb_nsb_overlap.py)): the IODP
  import against NSB's 2023 SQLite.
- 2026-10-22, checked: ASUD formation matching, age agreement and the
  random-unit null; FosSahul site and genus overlap; Neotoma overlap
  (collection-level; rerun on the region with identical results).
- 2026-10-22, source claim (documentation scan, Claude Sonnet subagent):
  licence change commit of 2025-02-20 and the pages still stating CC BY 4.0;
  DOI archives and the 270-versus-240 replay test; GBIF DwC-A versions;
  plate-model identities and Macrostrat's limits; the cited critiques.
- 2026-10-22, independent review of the regional entry (Claude Sonnet
  subagent); its corrections carried into this revision.
