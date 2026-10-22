---
id: gbif-ala-fossils
name: GBIF and ALA fossil-specimen records for Australia and Papua New Guinea
kind: database
status: active
last_update: "live; harvest of 2026-10-22T1013Z-1028Z"
scope:
  taxa: ["all fossil taxa held as museum specimens: mammals, birds, invertebrates, plants, microfossils"]
  time: "Precambrian to Holocene, as recorded by each collection"
  space: "Australia and Papua New Guinea (GBIF country field)"
  record_unit: "fossil specimen or lot (basisOfRecord FOSSIL_SPECIMEN) in a museum collection"
size:
  as_of: "harvest 2026-10-22T1013Z"
  au_reported: 66252
  au_neptune_excluded: 25799
  au_harvested: 40453
  pg_reported: 6176
  pg_neptune_excluded: 3847
  pg_harvested: 2329
access:
  tier: open
  licence: "per record: CC0, CC BY 4.0 or CC BY-NC 4.0 (each dataset's licence in its mirrored dataset__*.json); 5.8% of the Australian harvest is CC BY-NC"
  routes:
    - {type: api, url: "https://api.gbif.org/v1/occurrence/search?basisOfRecord=FOSSIL_SPECIMEN&country=AU", state: "open; slow beyond an offset of about 10,000, so harvested in partitions of 9,000 or fewer", checked: 2026-10-22}
    - {type: download, url: "GBIF occurrence download API", state: "needs a GBIF account; not used", checked: 2026-10-22}
    - {type: bulk, url: "GBIF monthly open-data snapshot on AWS (occurrence/2026-10-01/, 288 GB parquet, citable download DOI)", state: "open; not mirrored (source scan)", checked: 2026-10-22}
    - {type: api, url: "https://biocache-ws.ala.org.au/ws/occurrences/search?fq=basis_of_record:FossilSpecimen", state: "open; a subset of GBIF's records; documented only", checked: 2026-10-22}
  api: "GBIF occurrence search (JSON); ALA biocache (JSON)"
versioning:
  replay: none
  notes: "live aggregator with no releases; keep every dated harvest; GBIF's monthly AWS snapshots are the citable alternative"
mirror:
  path: deep-server:/data/paleodata/gbif-ala-fossils
  policy: "dated GBIF harvests of AU and PG fossil specimens, Neptune excluded (it is NSB's old copy; see nsb); ALA documented only"
  state: "gbif/raw/2026-10-22T1013Z_url: 396 JSON files (265 result pages, counts, dataset facets, 127 dataset records), 205 MB"
lineage:
  upstream:
    - "museum collections publishing to GBIF: Natural History Museum London, UC Museum of Paleontology, Swedish Museum of Natural History, Smithsonian NMNH and over 120 others; the Neptune microfossil database (NSB's 2016 copy)"
  downstream:
    - "ALA re-serves the NHM London, UCMP and MCZ datasets as copies of GBIF's (source scan)"
eprp_questions: []
citation:
  - "GBIF.org occurrence search, basisOfRecord FOSSIL_SPECIMEN, country AU and PG, retrieved 2026-10-22; cite the datasets of the records used (their DOIs are in the dataset records). For publication, cite a GBIF download DOI or the AWS snapshot's DOI"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# GBIF and ALA fossil specimens: Australia and Papua New Guinea

## Summary

GBIF aggregates museum fossil specimens worldwide; ALA re-serves part of
GBIF's Australian set. For Australia, GBIF reports 66,252 fossil specimens,
but 39% are the Neptune microfossil database (NSB's old copy, catalogued in
[nsb](../nsb/README.md)), and almost all the rest sit in foreign museums:
London, Berkeley, Stockholm, Washington and over a hundred others. Only 278
records come from an Australian publisher (CSIRO's ANWC subfossils), and no
state museum or geological survey palaeontology collection is in either
aggregator. We harvested every non-Neptune record for Australia (40,453) and
Papua New Guinea (2,329), reconciled exactly with GBIF's counts. The set's
distinctive value is specimen-level access to Australian material held
abroad, above all UCMP's 2,862 Quaternary mammal specimens and its Cenozoic
Lake Eyre Basin faunas. For occurrence analysis, PBDB remains the primary
source; this set is a complement and a pointer to physical specimens.

## Contents

Our counts ([profile](profile/gbif_fossil_profile.tsv)), non-Neptune records:

| | Australia | Papua New Guinea |
| --- | ---: | ---: |
| GBIF's reported total | 66,252 | 6,176 |
| Neptune, excluded | 25,799 | 3,847 |
| Harvested, unique | 40,453 | 2,329 |
| Datasets | 126 | 18 |
| Species-level names (incl. subspecies, varieties) | 15,540 (38%) | 1,018 (44%) |
| No match to the GBIF backbone (no kingdom) | 6,106 (15%) | 175 |
| Coordinates | 14,096 (35%) | 1,082 (46%) |
| Any chronostratigraphic field | 30,575 (76%) | 1,680 (72%) |
| Formation, group, member or bed | 18,728 (46%) | 1,536 (66%) |
| Collection year | 10,866 (27%) | 1,394 (60%) |
| Quaternary mammals | 3,318 | 313 |

- *Datasets (Australia).* NHM London 9,018; UC Museum of Paleontology 7,987;
  Swedish Museum of Natural History palaeobotany 7,527 and palaeozoology 826;
  Smithsonian NMNH 2,359; UT Austin 1,496; Condon (Oregon) 1,437; Florida
  1,250; MNHN Paris 1,232; International Fossil Shell Museum 1,010. The top
  three hold 61%. Papua New Guinea: NHM 1,071, Swedish palaeozoology 715,
  UCMP 333.
- *Publishers' countries (Australia).* US 17,768; GB 9,018; SE 8,353; DE
  1,618; NL 1,451; FR 1,276; JP 345; AU 278.
- *Licences (Australia).* CC BY 4.0 22,354; CC0 15,749; CC BY-NC 4.0 2,350.
- *Taxa (Australia).* Animalia 22,668, Chromista 5,991 (foraminifera and
  diatoms), Plantae 5,535. Classes: mammals 7,139, globothalamid foraminifera
  3,335, gastropods 2,354, echinoids 1,234, ostracods 1,217, bivalves 1,087,
  birds 875, conifers 855.
- *Time (Australia, earliest period).* Neogene 5,364, Quaternary 5,242,
  Permian 3,633, Triassic 2,653, Cretaceous 2,250, Paleogene 1,567, Cambrian
  1,187, Devonian 1,057; none 15,440.
- *Quaternary mammals* (a Quaternary period or a Pleistocene or Holocene
  epoch): Australia 3,318, of which UCMP 2,862, NHM 214, Royal Ontario Museum
  93, MCZ 58; Papua New Guinea 313, all but one UCMP. A further 1,118
  Australian mammal specimens carry no chronostratigraphy.

**ALA (documented, not mirrored; source scan).** ALA serves 17,531 fossil
specimens (NHM 8,877, UCMP 7,983, MCZ 385, ANWC 279, others 7). Its NHM, UCMP
and MCZ resources are registered as copies of GBIF's datasets, and nine of
nine sampled record IDs were found in GBIF. ANWC's 279 subfossil records
(mammals 206, birds 47; caves in New South Wales, Lord Howe and Norfolk
islands) are native to ALA and also in GBIF. All 27 ALA collections with
palaeontology, fossil or geology in their names, including the Australian,
Queensland, South Australian and Western Australian museums and the state
geological surveys, return zero records.

## Provenance and lineage

Each record is published to GBIF by its holding museum, usually through an
IPT or a collection-management system export, and interpreted by GBIF
against its taxonomic backbone and geological-time vocabulary. The large
Australian holdings abroad reflect historical exchange and expeditions:
UCMP's Lake Eyre Basin and cave collections, the Swedish Museum's Permian and
Triassic plants, NHM London's wide collections (inferred from the datasets'
content). GBIF's Neptune dataset is a 2016 copy of NSB, a third smaller than
NSB's final release and without ages ([nsb](../nsb/README.md)).

## Structure

Darwin Core occurrence records as GBIF's JSON: taxon (verbatim and
interpreted, with backbone keys), `datasetKey`, `institutionCode`,
`catalogNumber`, `license`, coordinates and GADM areas, `locality`, `year`,
geological context (`earliestEraOrLowestErathem` to
`latestAgeOrHighestStage`, `formation`, `group`, `member`, `bed`,
`lithostratigraphicTerms`), and GBIF's `issues` flags. Records also carry
collector and identifier names, which our profile does not read.

## Access

- **Mirror.** `deep-server:/data/paleodata/gbif-ala-fossils/gbif/raw/2026-10-22T1013Z_url/`
  with manifest: `{AU,PG}__count.json`, `{AU,PG}__datasets.json`,
  `dataset__<key>.json` and result pages `<cc>__<datasetKey>__p<part>__<offset>.json`.
  Index: [snapshots.tsv](snapshots.tsv).
- **Refresh (about 15 minutes).** [gbif_fossil_specs.py](gbif_fossil_specs.py)
  writes the page list, splitting any dataset over 9,000 records by latitude
  bisection plus its records without coordinates and skipping Neptune; then
  `data_mirror.py url gbif-ala-fossils/gbif ... $(cat specs)` fetches it.
  Reconcile `unique_records` with `reported_count − neptune_skipped` in the
  profile.
- **Paging.** The search API allows `limit` up to 300 and offsets to 100,000,
  but pages beyond an offset of about 10,000 took 5 to 6 minutes each in the
  source scan's tests; partitioning keeps every query under that.

## Strengths

- Complete, reconciled harvest of every non-Neptune fossil specimen GBIF
  holds for Australia and Papua New Guinea, refreshable in minutes.
- Specimen-level records with catalogue numbers: a finding aid for Australian
  material in foreign museums, including Quaternary mammals that PBDB and
  FosSahul record only as literature occurrences.
- Geological context on three-quarters of records; open licences on 94%.

## Weaknesses and pitfalls

- **Foreign museums only.** Australian state museums and surveys publish no
  fossil specimens to GBIF or ALA; 278 Australian-published records
  (ANWC) are the exception. Coverage reflects which overseas collections
  digitised, not the Australian record.
- **Neptune dominates the raw count.** Filter it out (39% of Australian and
  62% of Papua New Guinea fossil specimens) and use NSB instead.
- **Thin geography.** 35% of Australian records have coordinates; 962 of
  those fall outside the Australian mainland and Tasmania box used across the
  catalogue (external territories, offshore sites or errors; not separated).
- **Names.** 15% of Australian records match nothing in GBIF's backbone and
  28% (11,284) match only at a higher rank, so genus and species counts
  undercount.
- **Basis of record hides fossils.** UCMP holds 1,354 more Australian records
  as preserved specimens, most with geological periods (source scan); a
  FOSSIL_SPECIMEN filter misses them.
- **Facets double count.** GBIF's geological-time facets include ancestor
  terms (the period facet sums to more than the record count; source scan);
  count from records, as the profile does.
- **Papua New Guinea flags.** 878 records carry
  `CONTINENT_COUNTRY_MISMATCH` and 728 `TYPE_STATUS_INVALID`.
- **Collector names.** Raw records hold personal names in `recordedBy` and
  `identifiedBy`; keep them out of derived outputs.

## Overlap with other sources

- **PBDB.** PBDB's GBIF dataset is typed MATERIAL_CITATION (42,333 Australian
  records; source scan), so a FOSSIL_SPECIMEN filter does not double count
  it. By genus name: GBIF's Australian set has 3,026 genera and PBDB's
  Australian occurrences 6,161; they share 1,439, and 1,587 GBIF genera are
  absent from PBDB's Australian set (name-level only; unmatched spellings and
  microfossil genera presumably account for many). Papua New Guinea: 271 and
  362 genera, 45 shared.
- **FosSahul.** GBIF's Australian fossil mammals span 143 genera, FosSahul's
  131; 65 are shared, and 66 FosSahul genera have no GBIF specimen. GBIF's
  mammal genera include Cenozoic taxa outside FosSahul's scope.
- **NSB.** GBIF's Neptune dataset is NSB's 2016 copy; excluded here.
- **ALA.** A subset of GBIF's records, plus the same ANWC records.

## EPRP relevance

A finding aid for specimen-based checks of Australian fossil records held
abroad (re-dating, re-identification, morphometrics), especially UCMP's
Quaternary mammals; a negative result on Australian institutional data
mobilisation; and a reconciled, refreshable harvest for the PBDB Australian
pilot's deduplication.

## Citation and terms

Cite GBIF.org with the query and retrieval date, and the datasets of the
records used; for publication, cite a GBIF download DOI or the AWS snapshot's
DOI. Respect CC BY-NC on the 2,350 Australian records that carry it.

## Verification log

- 2026-10-22, checked ([gbif_fossil_profile.py](gbif_fossil_profile.py),
  [output](profile/gbif_fossil_profile.tsv)): harvest reconciled with GBIF's
  counts (Australia 40,453 = 66,252 − 25,799; Papua New Guinea 2,329 = 6,176 −
  3,847); counts by dataset, publisher country, licence, taxon, rank,
  institution, geological time and issue; completeness; Quaternary mammals;
  genus overlap with PBDB and FosSahul.
- 2026-10-22, checked: harvest specs written by
  [gbif_fossil_specs.py](gbif_fossil_specs.py) (sha256 matches the deployed
  copy), fetched by `data_mirror.py url` with sha256 manifests.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): ALA
  figures and its copies of GBIF datasets; state museum collections returning
  zero; UCMP's preserved-specimen fossils; PBDB's MATERIAL_CITATION dataset;
  paging timings; facet double counting; the AWS snapshot.
