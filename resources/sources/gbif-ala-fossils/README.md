---
id: gbif-ala-fossils
name: GBIF and ALA fossil-specimen records for Australia and Papua New Guinea
kind: database
status: active
last_update: "live; harvest of 2026-10-22T1013Z-1028Z; basis check 2026-10-22"
scope:
  taxa: ["all fossil taxa recorded as FOSSIL_SPECIMEN: mammals, birds, invertebrates, plants, microfossils"]
  time: "Precambrian to Holocene, as recorded by each collection"
  space: "GBIF country AU and PG only; Australian external territories (NF, CX, CC, HM), Indonesia and Timor-Leste carry their own codes and are not included"
  record_unit: "a fossil specimen or lot in a museum collection; 3% of Australian records are PANGAEA data-publication rows (drill-core descriptions and paper tables), not specimens"
size:
  as_of: "harvest 2026-10-22T1013Z"
  au_harvested: 40453
  pg_harvested: 2329
  au_reported: 66252
  au_neptune_excluded: 25799
  pg_reported: 6176
  pg_neptune_excluded: 3847
access:
  tier: open
  licence: "per record: CC0, CC BY 4.0 or CC BY-NC 4.0 (each dataset's licence in its mirrored dataset__*.json); 5.8% of the Australian harvest and 33 Papua New Guinea records are CC BY-NC"
  routes:
    - {type: api, url: "https://api.gbif.org/v1/occurrence/search?basisOfRecord=FOSSIL_SPECIMEN&country=AU", state: "open; slow beyond an offset of about 10,000, so harvested in partitions of 9,000 or fewer", checked: 2026-10-22}
    - {type: download, url: "https://api.gbif.org/v1/occurrence/download/request", state: "needs a GBIF account; not used (source claim)"}
    - {type: bulk, url: "https://gbif-open-data-ap-southeast-2.s3.ap-southeast-2.amazonaws.com/?list-type=2&prefix=occurrence/", state: "monthly open-data snapshot (occurrence/2026-10-01/, 288 GB parquet, citable download DOI); not mirrored", checked: 2026-10-22}
    - {type: api, url: "https://biocache-ws.ala.org.au/ws/occurrences/search?q=*:*&fq=basis_of_record:FossilSpecimen", state: "open; a subset of GBIF's records; documented only", checked: 2026-10-22}
  api: "GBIF occurrence search (JSON); ALA biocache (JSON)"
versioning:
  replay: none
  notes: "live aggregator with no releases; keep every dated harvest; GBIF's monthly AWS snapshots are the citable alternative"
mirror:
  path: deep-server:/data/paleodata/gbif-ala-fossils
  policy: "dated GBIF harvests of AU and PG fossil specimens, Neptune excluded (NSB's old copy; see nsb); a basis-of-record check; ALA documented only"
  state: "gbif/raw/2026-10-22T1013Z_url: 396 JSON files (265 result pages, counts, dataset facets, 127 dataset records), 205 MB; basis-check/raw/: 14 count queries"
lineage:
  upstream:
    - "museum collections publishing to GBIF (49 organisations for Australia, per the review): Natural History Museum London, UC Museum of Paleontology, Swedish Museum of Natural History, Smithsonian NMNH and others"
    - "PANGAEA data publications (33 Australian datasets)"
    - "the Neptune microfossil database (GBIF's copy of NSB, modified 2016; excluded)"
  downstream:
    - "ALA re-serves the NHM London, UCMP and MCZ datasets as copies of GBIF's (source scan)"
eprp_questions: []
citation:
  - "GBIF.org occurrence search, basisOfRecord FOSSIL_SPECIMEN, country AU and PG, retrieved 2026-10-22; cite the datasets of the records used (their DOIs are in the dataset records). For publication, cite a GBIF download DOI or the AWS snapshot's DOI"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "2026-10-22, independent Claude Sonnet subagent; findings applied"
---

# GBIF and ALA fossil specimens: Australia and Papua New Guinea

## Summary

GBIF aggregates fossil specimens worldwide; ALA re-serves part of GBIF's
Australian set. For Australia, GBIF reports 66,252 fossil-specimen records,
but 39% are the Neptune microfossil database (GBIF's copy of NSB, catalogued
in [nsb](../nsb/README.md)), and almost all the rest sit in foreign museums:
London, Berkeley, Stockholm, Washington and some 45 others, plus PANGAEA
drill-core and table data. Only 278 records come from an Australian publisher
(CSIRO's ANWC subfossils), and no state museum or geological survey
palaeontology collection is in either aggregator. We harvested every
non-Neptune record for Australia (40,453) and Papua New Guinea (2,329),
reconciled exactly with GBIF's counts. The set is a finding aid for Australian
material held abroad, notably UCMP's 2,862 Quaternary mammal records and its
Cenozoic faunas, but it is thin as data: none of UCMP's Quaternary mammals has
coordinates, 24% are named to species, and the records are lots. For
occurrence analysis, PBDB remains the primary source.

## Contents

Our counts ([profile](profile/gbif_fossil_profile.tsv)), non-Neptune records:

| | Australia | Papua New Guinea |
| --- | ---: | ---: |
| GBIF's reported total | 66,252 | 6,176 |
| Neptune, excluded | 25,799 | 3,847 |
| Harvested, unique (rows fetched, no duplicates) | 40,453 | 2,329 |
| Datasets | 126 (33 PANGAEA) | 18 |
| Species-level names (incl. subspecies, varieties) | 15,540 (38%) | 1,018 (44%) |
| No kingdom after GBIF interpretation | 6,106 (15%) | 175 (7.5%) |
| Coordinates (of which placeholder −9, −9) | 14,096 (30) | 1,082 (12) |
| An `earliest*` time field | 30,575 (76%) | 1,680 (72%) |
| Any `earliest*` or `latest*` time field | 31,977 (79%) | 1,729 (74%) |
| Formation, group, member or bed | 13,022 (32%) | 799 (34%) |
| ... or `lithostratigraphicTerms` | 18,728 (46%) | 1,536 (66%) |
| Collection year | 10,866 (27%) | 1,394 (60%) |
| Quaternary mammals | 3,318 | 313 |

- *Datasets (Australia).* NHM London 9,018; UC Museum of Paleontology 7,987;
  Swedish Museum of Natural History palaeobotany 7,527 and palaeozoology 826;
  Smithsonian NMNH 2,359; UT Austin 1,496; Condon (Oregon) 1,437; Florida
  1,250; MNHN Paris 1,232; International Fossil Shell Museum 1,010. The top
  three hold 61%. PANGAEA: 1,189 records in 33 datasets (diatoms 697, 259
  "Arachnida" that the review traced to coral labels interpreted as a spider
  genus, 196 without class). Papua New Guinea: NHM 1,071, Swedish
  palaeozoology 715, UCMP 333.
- *Publishers' countries (Australia).* US 17,768; GB 9,018; SE 8,353; DE
  1,618; NL 1,451; FR 1,276; JP 345; AU 278.
- *Licences (Australia).* CC BY 4.0 22,354; CC0 15,749; CC BY-NC 4.0 2,350.
- *Taxa (Australia).* Animalia 22,668, Chromista 5,991 (foraminifera and
  diatoms), Plantae 5,535. Classes: none 13,542, mammals 7,139, globothalamid
  foraminifera 3,335, gastropods 2,354, echinoids 1,234, ostracods 1,217,
  bivalves 1,087, tubothalamid foraminifera 900, rhynchonelliform
  brachiopods 895, birds 875.
- *Time (Australia, earliest period).* Neogene 5,364, Quaternary 5,242,
  Permian 3,633, Triassic 2,653, Cretaceous 2,250, Paleogene 1,567, Cambrian
  1,187, Devonian 1,057; none 15,440.
- *Quaternary mammals* (mammals with Quaternary as earliest period, or
  Pleistocene or Holocene as earliest or latest epoch; 52 qualify only by
  latest epoch): Australia 3,318, of which UCMP 2,862, NHM 214, Royal Ontario
  Museum 93, MCZ 58. Only 25 have coordinates (none of UCMP's) and 950 a
  formation (Katipiri Sands 490, Mampuwordu Sands 444, Chinchilla Sands 12).
  Ranks: species 1,014 (31%), genus 1,134, family 967, order or class 203.
  States: New South Wales 1,481, South Australia 1,100, Queensland 370,
  Victoria 204, Western Australia 87. UCMP's 2,862 records give 4,461
  individuals where a count is stated (542 records state none). Four are
  human remains (*Homo sapiens*; 11 in the whole harvest). Papua New Guinea:
  313, all but one UCMP's, all from the Otibanda Formation, 13 to species.
  A further 1,074 Australian mammal records carry no time field at all (NHM
  738, ANWC's subfossils 205, MCZ 44).
- *UCMP's Australian collection.* South Australia 4,159, New South Wales
  1,602, Northern Territory 1,182, Western Australia 426, Victoria 316,
  Queensland 251. Formations: Katipiri Sands 1,311 (103 queried), Waite
  1,179, Wipajiri 1,015, Etadunna 965, Mampuwordu Sands 485, Blina Shale 264,
  Namba 84. Katipiri, Wipajiri, Etadunna, Mampuwordu, Namba and Tirari are
  Lake Eyre Basin units, while Waite is in the Northern Territory and the
  Blina Shale in Western Australia (recall).

**Basis of record does not hide fossils** (basis check,
[gbif_basis_specs.py](gbif_basis_specs.py)). GBIF holds 3,018 further
Australian records with basis PRESERVED_SPECIMEN and the period Quaternary
(UCMP 1,344, Paleontological Research Institution 1,291, International Fossil
Shell Museum 382, MCZ 1). Their classes are gastropods 2,203, bivalves 613,
chitons 118 and corals 58 (class names for GBIF's keys from the review), none
are mammals, and the review found them to be living species from modern
localities: Recent comparative material with a blanket period, not missed
fossils. Only 21 older-period records sit under that basis.

**ALA (documented, not mirrored; source scan, confirmed by the review).** ALA
serves 17,531 fossil specimens (NHM 8,877, UCMP 7,983, MCZ 385, ANWC 279,
others 7). Its NHM, UCMP and MCZ resources are registered as copies of GBIF's
datasets, and nine of nine sampled record IDs were found in GBIF. ANWC's 279
subfossil records (mammals 206, birds 47; New South Wales including Lord Howe
Island 257, ACT 11, Norfolk Island 10) are native to ALA and also in GBIF.
ALA collections with palaeontology, fossil or geology in their names,
including the Australian, Queensland, South Australian and Western Australian
museums and the state geological surveys, return no fossil records.

## Provenance and lineage

Each record is published to GBIF by its holding institution (protocols in
the records: EML-described archives, Darwin Core archives, BioCASE; review)
and interpreted by GBIF against its taxonomic backbone and geological-time
vocabulary. PANGAEA's datasets are tables from drill-core and paper data
publications rather than specimen catalogues. GBIF's Neptune dataset is the
pre-2015 copy of NSB, modified in 2016, a third smaller than NSB's final
release and without ages ([nsb](../nsb/README.md)).

## Structure

Darwin Core occurrence records as GBIF's JSON: taxon (verbatim and
interpreted, with backbone keys), `datasetKey`, `institutionCode`,
`catalogNumber`, `individualCount`, `license`, coordinates and GADM areas,
`locality`, `year`, geological context (`earliestEraOrLowestErathem` to
`latestAgeOrHighestStage`, `formation`, `group`, `member`, `bed`,
`lithostratigraphicTerms`), and GBIF's `issues` flags (the profile lists the
15 commonest per country). Records also carry collector and identifier
names, which our profile does not read.

## Access

- **Mirror.** `deep-server:/data/paleodata/gbif-ala-fossils/gbif/raw/2026-10-22T1013Z_url/`
  with manifest: `{AU,PG}__count.json`, `{AU,PG}__datasets.json`,
  `dataset__<key>.json` and result pages `<cc>__<datasetKey>__p<part>__<offset>.json`;
  `basis-check/raw/<snapshot>/`. Index: [snapshots.tsv](snapshots.tsv).
- **Refresh.** On deep-server, in `/data/paleodata`:
  `python3 _tools/gbif-ala-fossils_gbif_fossil_specs.py specs.txt AU PG`
  (a few minutes of count and dataset queries), then
  `mapfile -t S < specs.txt; python3 _tools/data_mirror.py url gbif-ala-fossils/gbif --license "per record: CC0, CC BY 4.0 or CC BY-NC 4.0 (see each dataset__*.json)" "${S[@]}"`
  (about 15 minutes), then
  `python3 gbif_fossil_profile.py <harvest> <basis-check> <PBDB snapshot> <FosSahul CSV> out.tsv`,
  which exits with status 1 unless each country's unique records equal
  GBIF's count minus Neptune.
- **Partitioning.** The spec builder splits any dataset over 9,000 records
  into its records with coordinates (bisected by latitude if still over 9,000)
  and those without. Only NHM needed it this time (1,808 with coordinates,
  7,210 without, per the review), so the bisection branch has not run on real data. GBIF's
  latitude ranges include both ends, so records on a split latitude would be
  fetched twice (the profile dedupes by key); the part without coordinates is
  never split, so NHM's would need another partition above 9,000.
- **Paging.** The search API allows `limit` up to 300 and offsets to 100,000,
  but pages beyond an offset of about 10,000 took 5 to 6 minutes each in the
  source scan's tests.

## Strengths

- Complete, reconciled harvest of every non-Neptune fossil-specimen record
  GBIF holds for Australia and Papua New Guinea, refreshable in under half an
  hour.
- A finding aid for Australian material in foreign museums, with catalogue
  numbers: Quaternary mammals that PBDB records only as literature
  occurrences (PBDB's specimen table holds no Australian mammals; review),
  and UCMP's Cenozoic collections.
- Geological context on three-quarters of records; open licences on 94%.

## Weaknesses and pitfalls

- **Foreign museums only.** Australian state museums and surveys publish no
  fossil specimens to GBIF or ALA; ANWC's 278 records are the exception.
  Coverage reflects which overseas collections digitised, not the Australian
  record.
- **Neptune dominates the raw count.** Filter it out (39% of Australian and
  62% of Papua New Guinea fossil-specimen records) and use NSB instead.
- **Quaternary mammals are hard to use as data.** No coordinates for UCMP's
  2,862, formations for a third, species names for a quarter, and records are
  lots. Use them to find specimens, not as occurrences. Human remains are
  among them and need appropriate handling.
- **Thin and noisy geography.** 35% of Australian records have coordinates.
  953 of those fall outside the Australian region used across the catalogue
  (mainland and Tasmania plus Torres Strait); 883 of them carry GBIF's
  COUNTRY_DERIVED_FROM_COORDINATES flag, mostly offshore cores and net
  samples (NHM 646, NMNH 186, a PANGAEA ODP table 62), and 30 are Oslo's
  placeholder (−9, −9). Papua New Guinea has 12 more placeholders.
- **Interpreted names mislead both ways.** 15% of Australian records have no
  kingdom after interpretation and 28% (11,284) match only at a higher rank,
  so genus and species counts undercount; and interpretation also invents
  names (the review found Hyrachyus, Aelurodon, Mammuthus and Elephas on
  Australian records, and PANGAEA coral labels read as a spider genus).
- **PANGAEA rows are not specimens.** 1,189 Australian records in 33 datasets
  come from drill-core descriptions and paper tables.
- **Scope stops at the country code.** Records coded to the external
  territories, Indonesia or Timor-Leste are outside the harvest (the review
  counted 318 NF, 441 CX, 1,665 CC and 7,621 HM fossil specimens, and 534 ID
  and 122 TL records inside the Australian box).
- **Collector names.** Raw records hold personal names in `recordedBy` and
  `identifiedBy`; keep them out of derived outputs.

## Overlap with other sources

- **PBDB** (snapshot au-ng 2026-10-22T0602Z). PBDB's GBIF dataset is typed
  MATERIAL_CITATION (42,333 Australian records; source scan, confirmed by the
  review), so a FOSSIL_SPECIMEN filter does not double count it. By genus
  name: GBIF's Australian set has 3,026 genera and PBDB's Australian
  occurrences 6,161; they share 1,439. Widening both sides to all name first
  words (GBIF `genericName` and scientific names; PBDB accepted and
  identified names) gives 1,777 of 3,560, so the strict figure is a lower
  bound at name level. Papua New Guinea: 271 and 362 genera, 45 shared.
- **FosSahul** (March 2021 file). FosSahul mammal genera with rows in the
  Australian region number 97 (single names only); 63 have GBIF Australian
  specimens and 53 have Quaternary-labelled ones. The 34 without include
  extinct genera (*Bohra*, *Congruus*, *Metasthenurus*, *Warendja*,
  *Invictokoala*) and many living ones (*Pteropus*, *Nyctophilus*,
  *Planigale*, *Zyzomys*, *Dugong*). Of GBIF's 143 Australian mammal genera,
  only 71 carry a Quaternary label.
- **NSB.** GBIF's Neptune dataset is NSB's pre-2015 copy; excluded here.
- **ALA.** A subset of GBIF's records, plus the same ANWC records.

## EPRP relevance

A finding aid for specimen-based checks of Australian fossil records held
abroad (re-identification, morphometrics, and dating where material
allows), especially UCMP's Quaternary mammals and Cenozoic faunas; a
negative result on Australian institutional data mobilisation; and a
reconciled, refreshable harvest for the PBDB Australian pilot's
deduplication. It cannot serve as an occurrence dataset for spatial or
temporal analysis without georeferencing and re-identification.

## Citation and terms

Cite GBIF.org with the query and retrieval date, and the datasets of the
records used; for publication, cite a GBIF download DOI or the AWS snapshot's
DOI. Respect CC BY-NC on the 2,350 Australian and 33 Papua New Guinea records
that carry it.

## Verification log

- 2026-10-22, checked ([gbif_fossil_profile.py](gbif_fossil_profile.py),
  [output](profile/gbif_fossil_profile.tsv)): harvest reconciled with GBIF's
  counts and free of duplicates (Australia 40,453 = 66,252 − 25,799; Papua
  New Guinea 2,329 = 6,176 − 3,847); counts by dataset, publisher country,
  licence, taxon, rank, institution, geological time, lithostratigraphy and
  issue; PANGAEA rows; coordinates, placeholders and records outside the
  region; Quaternary mammals and UCMP's share; UCMP by state and formation;
  the basis-of-record check; genus overlaps with PBDB (strict and widened)
  and FosSahul (Australian region).
- 2026-10-22, checked: harvest specs written by
  [gbif_fossil_specs.py](gbif_fossil_specs.py) and basis-check specs by
  [gbif_basis_specs.py](gbif_basis_specs.py), fetched by `data_mirror.py url`
  with sha256 manifests.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): ALA
  figures and its copies of GBIF datasets; state museum collections returning
  zero; PBDB's MATERIAL_CITATION dataset; paging timings; the AWS snapshot.
  The review reproduced these live.
- 2026-10-22, reviewed by an independent Claude Sonnet subagent; its findings
  (basis of record, Quaternary-mammal caveats, PANGAEA, FosSahul like for
  like, field definitions, region, partitioning, scope) are applied above.
  Its API-only observations are labelled where quoted.
