---
id: ala-vertebrates
name: Atlas of Living Australia, vertebrate occurrences (species-level counts by period)
kind: database
status: active
last_update: "live; facet snapshots 2026-10-22T1008Z and T1011Z"
scope:
  taxa: ["birds, mammals, reptiles, amphibians, ray-finned fishes, sharks and rays"]
  time: "historical and modern records; 0.34% of vertebrate records predate 1950"
  space: "Australia (ALA country field), including external territories and marine records"
  record_unit: "occurrence record (observation, specimen, survey); mirrored here only as species-level counts"
size:
  as_of: "snapshot 2026-10-22T1011Z"
  vertebrate_records: 128996208
  species_facet_entries: 7985
access:
  tier: open
  licence: "per record: CC0, CC BY or CC BY-NC (source scan: NC about 27% of all ALA records, 9.5% of mammal records); our snapshots hold aggregate counts only"
  routes:
    - {type: api, url: "https://biocache-ws.ala.org.au/ws/occurrences/search (facets=species, flimit=-1)", state: "open; one call per class and period", checked: 2026-10-22}
    - {type: api, url: "biocache occurrence search, record pages", state: "pageSize at most 100; results stop at record 5,000 per query", checked: 2026-10-22}
    - {type: download, url: "ALA offline download", state: "needs an email address or login; not used", checked: 2026-10-22}
    - {type: bulk, url: "GBIF monthly open-data snapshot on AWS (occurrence/2026-10-01/, 288 GB parquet, citable download DOI)", state: "open; ALA publishes to GBIF; not mirrored", checked: 2026-10-22}
  api: "ALA biocache web services (JSON)"
versioning:
  replay: none
  notes: "live database; totals move between calls (the source scan saw ALA's grand total fall by about 25,000 between two probes on 22 October 2026); keep every dated snapshot"
mirror:
  path: deep-server:/data/paleodata/ala-vertebrates
  policy: "species-level facet counts per class and period, as dated snapshots; no records"
  state: "species-facets: 2026-10-22T1008Z_url (all and pre-1950; 12 files) and 2026-10-22T1011Z_url (adds from-1950; 18 files, 2.5 MB)"
lineage:
  upstream:
    - "state and federal agencies, museums (OZCAM), citizen science (eBird, iNaturalist, BirdLife Australia and others); taxonomy from AFD and APC"
  downstream:
    - "GBIF (ALA is Australia's GBIF node); species distribution models and conservation assessments"
eprp_questions: []
citation:
  - "Atlas of Living Australia occurrence search, https://biocache-ws.ala.org.au, species facets retrieved 2026-10-22; cite the data resources behind any records used"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Atlas of Living Australia: vertebrates

## Summary

The Atlas of Living Australia (ALA) aggregates Australian occurrence records
from agencies, museums and citizen science: 129 million vertebrate records,
87% of them birds. For EPRP it is the modern comparator for fossil and
historical ranges, and a check on last records of extinct species. ALA's web
services cap record paging at 5,000 per query, and its bulk download needs an
email address or login, so we mirror species-level counts instead: per class,
how many records each species has in all, before 1950 and from 1950 on. Those
counts already show the main pitfall for extinction work: 21 of the 32 extinct
mammal species on the EPBC list that ALA holds have records dated 1950 or
later. Some are genuine (species lost after 1950); others are subfossil
specimens, taxonomic changes, name collisions or unverified reports. A record's year alone is
not evidence the species was alive then.

## Contents

Our counts ([profile](profile/ala_vertebrates_profile.tsv)), snapshot
2026-10-22T1011Z, `country:Australia`:

| Class | Records | Before 1950 | From 1950 | Undated | Species | With pre-1950 records | No record from 1950 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Aves | 111,991,879 | 281,526 | 108,416,943 | 3,293,410 | 884 | 769 | 9 |
| Mammalia | 6,362,915 | 25,170 | 5,990,342 | 347,403 | 416 | 336 | 14 |
| Actinopterygii | 4,966,455 | 96,535 | 4,725,872 | 144,048 | 4,936 | 2,038 | 116 |
| Reptilia | 2,321,411 | 16,726 | 2,013,225 | 291,460 | 1,153 | 571 | 32 |
| Amphibia | 2,151,126 | 7,201 | 2,055,440 | 88,485 | 258 | 135 | 0 |
| Chondrichthyes | 1,202,422 | 7,226 | 1,190,228 | 4,968 | 338 | 130 | 1 |

"Species" counts facet entries with a species-level name; records identified
only to genus or above are left out.

## Provenance and lineage

ALA is Australia's national biodiversity data infrastructure and its GBIF
node. Records come from museums (through OZCAM), state and federal agencies,
and citizen-science platforms; names are matched to the Australian Faunal
Directory and the Australian Plant Census. Birds dominate because of eBird and
BirdLife Australia surveys (source scan: 94% of bird records are human
observations).

## Structure

Each snapshot holds one JSON per class and period, the response of
`/ws/occurrences/search?q=*:*&fq=country:Australia&fq=class:<Class>[&fq=year:...]&pageSize=0&facets=species&flimit=-1`:
`totalRecords` plus a `fieldResult` list of `{label, count}` per species
(and "Not supplied" for records without a species).

## Access

- **Mirror.** `deep-server:/data/paleodata/ala-vertebrates/species-facets/raw/<snapshot>/`
  with manifests. Index: [snapshots.tsv](snapshots.tsv). The first snapshot
  lacks the from-1950 files; the profile reads the second.
- **Records.** For record-level work, take the GBIF open-data snapshot on AWS
  (anonymous, monthly, with a download DOI) and filter it to Australia and to
  CC0 or CC BY on deep-server. ALA's own download route needs an email
  address and is not used by agents.

## Strengths

- National coverage, all vertebrate classes, with specimen, survey and
  observation records under one taxonomy.
- Species-level counts by period are cheap (one call per class and period)
  and reproducible as dated snapshots.

## Weaknesses and pitfalls

- **A record's year is not a sighting of a living animal.** Of EPBC's 34
  extinct mammal species (under EPBC's current names), ALA holds 32; 21 have
  records from 1950 on, among them *Perameles fasciata* (3,356), *Pseudomys
  gouldii* (965), *Notamacropus greyi* (245), *Thylacinus cynocephalus*
  (156), *Leporillus apicalis* (71) and *Notomys amplus* (26). Four different
  things produce such records. Some species were lost after
  1950, so their records are genuine (by recall, *Melomys rubicola* and
  *Pipistrellus murrayi* were last seen around 2009). *P. gouldii*'s records
  are consistent with its synonymy with the living Shark Bay mouse (recall:
  Roycroft and colleagues' museum-genomics work). For species lost before
  1950, specimens collected from caves and owl-pellet deposits later, and
  unverified reports, are the likely sources (inferred, not checked record by
  record). And one name may mean different taxa in different systems: all
  3,356 *P. fasciata* records come from the NSW BioNet Atlas under that raw
  name, while EPBC uses it for an extinct bandicoot; which animal BioNet means
  is queued for the provider ([CONTACTS.md](../CONTACTS.md) C19). Only 11 of
  the 32 have no record from 1950 on. For birds, 4 of EPBC's 7 extinct
  species have none; *Psephotellus pulcherrimus* (5), *Porphyrio albus* (2)
  and *Zosterops albogularis* (2) have later records.
- **Match on EPBC's current names.** EPBC carries a listed and a current name
  (they differ in 117 rows). Matching on listed names misses *Perameles
  myosuros* (listed as *P. myosurus*) and counts two extinct emus as species
  (EPBC now treats them as subspecies of *Dromaius novaehollandiae*).
- **Undated records are not rare.** 5.5% of mammal and 12.6% of reptile
  records have no year, more than have years before 1950.
- **Licences are mixed.** Per the source scan, about 27% of ALA records
  carry non-commercial licences (9.5% of mammal records, 60% of amphibian
  records); filter by licence before reuse.
- **Paging is shallow.** Search stops at record 5,000 and pages hold at most
  100 records, so record-level harvesting needs partitions or the GBIF
  snapshot.
- **The country field includes external territories and marine records**
  (Christmas Island species such as *Rattus macleari* and *Emoia
  nativitatis*; Weddell seal).

## Overlap with other sources

- **EPBC** ([names-status](../names-status/README.md)): matched as above by
  [ala_vertebrates_profile.py](ala_vertebrates_profile.py), species-level
  entries only.
- **GBIF**: ALA publishes to GBIF; its fossil-specimen records are a subset of
  GBIF's ([gbif-ala-fossils](../gbif-ala-fossils/README.md)).
- **AVONET, COMBINE, PHYLACINE**: species traits to pair with these counts,
  joined by name.

## EPRP relevance

Modern range and abundance comparators for Sahul fossil records; screening
last-record dates of extinct and declining species, with the caveats above;
choosing comparator species with adequate records.

## Citation and terms

Cite ALA and the data resources of any records used; check each record's
licence. The mirrored snapshots are aggregate counts.

## Verification log

- 2026-10-22, checked ([ala_vertebrates_profile.py](ala_vertebrates_profile.py),
  [output](profile/ala_vertebrates_profile.tsv)): counts by class and period,
  species counts, species with no record from 1950, and the EPBC extinct
  cross-check, from the second snapshot.
- 2026-10-22, observed (one-off ALA facet query, not mirrored): the 3,356
  *Perameles fasciata* records from 1950 on are all NSW BioNet Atlas records
  from New South Wales with that raw name.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): paging
  limits (`pageSize` 100, results stop at 5,000), licence shares, record
  types, ALA's grand-total drift, the GBIF AWS snapshot's size and download
  DOI.
