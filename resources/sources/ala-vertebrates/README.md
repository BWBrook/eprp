---
id: ala-vertebrates
name: Atlas of Living Australia, vertebrate occurrences (species-level counts by period)
kind: database
status: active
last_update: "live; facet snapshots 2026-10-22T1008Z, T1011Z and T1044Z"
scope:
  taxa: ["six vertebrate classes: birds, mammals, reptiles, amphibians, ray-finned fishes, sharks and rays"]
  time: "historical and modern records; 0.34% of the six classes' records predate 1950"
  space: "Australia (ALA country field), including external territories and marine records; records without a country are excluded"
  record_unit: "occurrence record (observation, specimen, survey); mirrored here only as species-level counts"
size:
  as_of: "snapshot 2026-10-22T1011Z"
  vertebrate_records_six_classes: 128996208
  species_facet_entries: 7985
access:
  tier: open
  licence: "per record: mostly CC0, CC BY or CC BY-NC, also CC BY-SA, CC BY-NC-SA, CC BY-NC-ND and unspecified (source scan and review: NC about 27% of all ALA records, 9.6% of mammal, 28.5% of bird and 61% of amphibian records); our snapshots hold aggregate counts only, hence tier open"
  routes:
    - {type: api, url: "https://biocache-ws.ala.org.au/ws/occurrences/search", state: "open; species facets (flimit=-1) in one call per class and period", checked: 2026-10-22}
    - {type: api, url: "https://biocache-ws.ala.org.au/ws/occurrences/search", state: "record pages: pageSize at most 100, results stop at record 5,000 per query (source scan and review)", checked: 2026-10-22}
    - {type: download, url: "https://biocache-ws.ala.org.au/ws/occurrences/offline/download", state: "needs an email address or login; not tested, not used (source claim)"}
    - {type: bulk, url: "https://gbif-open-data-ap-southeast-2.s3.ap-southeast-2.amazonaws.com/?list-type=2&prefix=occurrence/", state: "GBIF monthly open-data snapshot (occurrence/2026-10-01/, 288 GB parquet, citable download DOI); ALA publishes to GBIF; not mirrored", checked: 2026-10-22}
  api: "ALA biocache web services (JSON)"
versioning:
  replay: none
  notes: "live database; totals move between calls (the source scan saw ALA's grand total fall by about 25,000 between two probes on 22 October 2026); keep every dated snapshot"
mirror:
  path: deep-server:/data/paleodata/ala-vertebrates
  policy: "species-level facet counts per class and period, and facets for EPBC extinct species with records from 1950 on, as dated snapshots; no records"
  state: "species-facets: 2026-10-22T1008Z_url (all and pre-1950; 12 files) and 2026-10-22T1011Z_url (adds from-1950; 18 files, 2.5 MB); extinct-since1950: 2026-10-22T1044Z_url (31 files, 0.1 MB)"
lineage:
  upstream:
    - "museums, mostly through OZCAM"
    - "state and federal agencies (BioNet, Fauna Atlas NT, Natural Values Atlas, WildNet and others)"
    - "citizen science (eBird, BirdLife Australia Birdata, iNaturalist and others)"
    - "taxonomy from the Australian Faunal Directory and the Australian Plant Census"
  downstream:
    - "GBIF (ALA is Australia's GBIF node)"
    - "species distribution models and conservation assessments"
eprp_questions: []
citation:
  - "Atlas of Living Australia occurrence search, https://biocache-ws.ala.org.au, species facets retrieved 2026-10-22; cite the data resources behind any records used"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "2026-10-22, independent Claude Sonnet subagent; findings applied"
---

# Atlas of Living Australia: vertebrates

## Summary

The Atlas of Living Australia (ALA) aggregates Australian occurrence records
from agencies, museums and citizen science: 129 million records in six
vertebrate classes, 87% of them birds. For EPRP it is the modern comparator
for fossil and historical ranges, and a check on last records of extinct
species. ALA's web services cap record paging at 5,000 per query, and its bulk
download needs an email address or login, so we mirror species-level counts
instead: per class, each species' records in all, before 1950 and from 1950
on; and, for the EPBC-listed extinct species with records from 1950 on, where
those records come from. The counts show the main pitfall for extinction
work. 21 of the 32 extinct mammal species on the EPBC list that ALA holds have
records dated 1950 or later, 4,993 in all, and only 3 of them are fossil
specimens. Most come from one agency's recent use of a name for a different
animal, a taxonomic resurrection, a museum's misdated batch, and historical
sighting reports; a minority are genuine records of species lost after 1950.
A record's year alone is not evidence the species was alive then.

## Contents

Our counts ([profile](profile/ala_vertebrates_profile.tsv)), snapshot
2026-10-22T1011Z, `country:Australia`:

| Class | Records | Before 1950 | From 1950 | Undated | Not to species | Species-rank names | With pre-1950 records | No dated record from 1950 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Aves | 111,991,879 | 281,526 | 108,416,943 | 3,293,410 | 1,788,388 | 880 | 769 | 9 |
| Mammalia | 6,362,915 | 25,170 | 5,990,342 | 347,403 | 402,213 | 416 | 336 | 14 |
| Actinopterygii | 4,966,455 | 96,535 | 4,725,872 | 144,048 | 885,059 | 4,932 | 2,038 | 116 |
| Reptilia | 2,321,411 | 16,726 | 2,013,225 | 291,460 | 101,190 | 1,153 | 571 | 32 |
| Amphibia | 2,151,126 | 7,201 | 2,055,440 | 88,485 | 43,132 | 258 | 135 | 0 |
| Chondrichthyes | 1,202,422 | 7,226 | 1,190,228 | 4,968 | 25,583 | 338 | 130 | 1 |

The species facet also holds eight hybrid or infraspecific labels (four
birds, four fishes), listed in the profile. Chordata as a whole has more
records (lungfish, tunicates and class-less records; review).

**Extinct species' records from 1950 on** (snapshot 2026-10-22T1044Z; one
query per EPBC extinct species with such records, built by
[ala_extinct_specs.py](ala_extinct_specs.py)). For the 21 mammal species,
4,993 records: by data resource, NSW BioNet Atlas 3,376, AWC Ecological
Monitoring Surveys 812, Queen Victoria Museum 247, Fauna Atlas NT 152,
Tasmanian Natural Values Atlas 148, AMNH 147, others 111; by basis, human
observation 3,855, machine observation 492, preserved specimen 476,
observation 150, image and other records 17, fossil specimen 3; by decade,
2020s 4,110 and 1950s–2010s 883.

## Provenance and lineage

ALA is Australia's national biodiversity data infrastructure and its GBIF
node. Records come from museums (largely through OZCAM), state and federal
agencies, and citizen-science platforms; names are matched to the Australian
Faunal Directory and the Australian Plant Census. Birds dominate because of
eBird and BirdLife Australia surveys (source scan: 94% of bird records are
human observations).

## Structure

Each species-facet snapshot holds one JSON per class and period, the response
of
`/ws/occurrences/search?q=*:*&fq=country:Australia&fq=class:<Class>[&fq=year:...]&pageSize=0&facets=species&flimit=-1`:
`totalRecords` plus `{label, count}` per species, and "Not supplied" for
records without a species. The extinct-species snapshot holds one JSON per
species with facets for basis of record, data resource, decade, state, year
and raw name, plus BioNet's yearly counts of *Perameles fasciata* and *P.
nasuta*.

## Access

- **Mirror.** `deep-server:/data/paleodata/ala-vertebrates/{species-facets,extinct-since1950}/raw/<snapshot>/`
  with manifests. Index: [snapshots.tsv](snapshots.tsv). The first
  species-facet snapshot lacks the from-1950 files (its other 12 files are
  identical to the second's); the profile reads the second.
- **Refresh.** `data_mirror.py url ala-vertebrates/species-facets --license
  "..." "species_<Class>_<period>.json::<URL>" ...` (the URL pattern above),
  then [ala_extinct_specs.py](ala_extinct_specs.py) and a second
  `data_mirror.py url` for the extinct-species facets; then
  `python3 ala_vertebrates_profile.py SPECIES_FACETS EXTINCT EPBC_CSV OUT`.
- **Records.** For record-level work, take the GBIF open-data snapshot on AWS
  (anonymous, monthly, with a download DOI) and filter it to Australia and to
  CC0 or CC BY on deep-server. ALA's own download route needs an email
  address and is not used by agents.

## Strengths

- National coverage, all vertebrate classes, with specimen, survey and
  observation records under one taxonomy.
- Species-level counts by period, and provenance facets for any species, are
  cheap (one call each) and reproducible as dated snapshots.

## Weaknesses and pitfalls

- **A record's year is not a living animal.** Of EPBC's 34 extinct mammal
  species (under EPBC's current names), ALA holds 32 (not *Bettongia pusilla*
  or *Conilurus capricornensis*); 21 have records from 1950 on. Five things
  produce them:
  1. *One agency's name for another animal.* All 3,356 *Perameles fasciata*
     records are NSW BioNet human observations from New South Wales, dated
     2023 to 2026 (33, 705, 1,921, 697), under that raw name; EPBC uses the
     name for an extinct bandicoot. Over the same years BioNet's *P. nasuta*
     records fell from 3,387 (2024) to 818 (2025) and 76 (2026 so far),
     which suggests a recent name or concept change in BioNet (inferred;
     queued as [CONTACTS.md](../CONTACTS.md) C19).
  2. *A resurrection.* *Pseudomys gouldii* (965 records, 957 in Western
     Australia; 812 from AWC monitoring, 738 dated in the 2020s) is the living
     Shark Bay mouse under its resurrected name (Roycroft et al. 2021; see
     [names-status](../names-status/README.md)).
  3. *Data artefacts.* All 245 *Notamacropus greyi* records are Queen
     Victoria Museum preserved specimens filed as *Macropus greyi*, dated in
     the 1970s and placed in Tasmania, outside the species' known South
     Australian and Victorian range (recall), so the date and place are
     probably cataloguing artefacts (inferred). Ten image records (EoL Flickr
     group) are dated by photograph or upload.
  4. *Historical reports.* Fauna Atlas NT holds 152 human observations from
     the 1960s to the 1990s of arid-zone species (for example *Leporillus
     apicalis* 56, *Onychogalea lunata* 22, *Perameles eremiana* 21, *Notomys
     amplus* 15, *Chaeropus yirratji* 14), and the Tasmanian Natural Values
     Atlas 148 thylacine observations from the 1950s to the 1970s. Their
     evidential standard is not recorded here.
  5. *Genuine late records.* Some species were lost after 1950: *Pipistrellus
     murrayi* (29 specimens from Christmas Island in the 1980s), *Melomys
     rubicola* (2 specimens, 1980s and 1990s), and outside mammals the four
     extinct frogs (*Taudactylus acutirostris* 525, *T. diurnus* 309,
     *Rheobatrachus silus* 98, *R. vitellinus* 44) and *Emoia nativitatis*
     (121) (losses after 1950 by recall).
  Only 3 of the 4,993 mammal records are fossil specimens (*Chaeropus
  ecaudatus*, NHM London).
- **"No dated record from 1950" is not "no record".** All 11 extinct mammal
  species with no dated record from 1950 have undated records (104 in all;
  *Perameles papillon* 39 of 42, *Caloprymnus campestris* 32 of 42, *Rattus
  macleari* 9 of 9), and so do the 4 such birds. Last-record dates need the
  undated records checked.
- **Match on EPBC's current names.** EPBC carries a listed and a current name
  (they differ in 117 rows). Matching on listed names misses *Perameles
  fasciata* (listed as *P. bougainville fasciata*) and *P. myosuros* (listed
  as *P. myosurus*), and counts two extinct emus as species. Of EPBC's 22
  extinct bird entries, 7 are species under current names; ALA holds all 7,
  and 3 have records from 1950 on (*Psephotellus pulcherrimus* 5, *Porphyrio
  albus* 2, *Zosterops albogularis* 2).
- **Undated and unidentified records are not rare.** 5.5% of mammal and
  12.6% of reptile records have no year, more than have years before 1950;
  6.3% of mammal and 17.8% of fish records are not identified to species.
- **Licences are mixed.** About 27% of ALA records carry non-commercial
  licences (source scan; mammals 9.6%, amphibians 61%); filter by licence
  before reuse.
- **Paging is shallow.** Search stops at record 5,000 and pages hold at most
  100 records, so record-level harvesting needs partitions or the GBIF
  snapshot.
- **The country field is broad and incomplete.** It includes external
  territories (Christmas Island species such as *Rattus macleari*,
  *Pipistrellus murrayi* and *Emoia nativitatis*) and vagrants (four Weddell
  seal records), and records without a country are excluded (about 100,000
  mammal records, most with an Australian state; review).

## Overlap with other sources

- **EPBC** ([names-status](../names-status/README.md)): matched as above by
  [ala_vertebrates_profile.py](ala_vertebrates_profile.py), species-level
  entries under current names.
- **GBIF**: ALA publishes to GBIF; its fossil-specimen records are a subset of
  GBIF's ([gbif-ala-fossils](../gbif-ala-fossils/README.md)).
- **AVONET, COMBINE, PHYLACINE**: species traits to pair with these counts,
  joined by name.

## EPRP relevance

Modern range and abundance comparators for Sahul fossil records; screening
last-record dates of extinct and declining species; choosing comparator
species with adequate records. What it cannot support without record-level
checks: last-record dates (undated records, misdated batches, name
collisions), or presence claims from single historical observations.

## Citation and terms

Cite ALA and the data resources of any records used; check each record's
licence. The mirrored snapshots are aggregate counts.

## Verification log

- 2026-10-22, checked ([ala_vertebrates_profile.py](ala_vertebrates_profile.py),
  [output](profile/ala_vertebrates_profile.tsv)): counts by class and period,
  undated and unidentified records, species-rank names, species with no dated
  record from 1950; the EPBC extinct cross-check with dated and undated
  records; the provenance, basis, decade, state and raw-name facets of the
  extinct species' records from 1950 on; BioNet's yearly *Perameles* counts.
- 2026-10-22, checked: per-species queries built by
  [ala_extinct_specs.py](ala_extinct_specs.py) and fetched with
  `data_mirror.py url` (sha256 manifests).
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): paging
  limits, licence shares, record types, ALA's grand-total drift, the GBIF AWS
  snapshot's size and download DOI. The review reproduced these live and
  added the fuller licence list, the records without a country and the
  Weddell seal records' states.
- 2026-10-22, reviewed by an independent Claude Sonnet subagent; its findings
  (undated records, provenance of post-1950 records, licence list, facet
  labels, scope) are applied above.
