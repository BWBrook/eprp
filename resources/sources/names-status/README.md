---
id: names-status
name: Names, conservation status and species traits for Australian comparisons (APC, EPBC lists, AVONET, COMBINE, PHYLACINE)
kind: compilation
status: active
last_update: "APC export 2026-10-22 (rows modified to 2026-10-21); EPBC species list extracted 2026-08-28; AVONET v7 2022-12-05; COMBINE v4 2021-04-23; PHYLACINE 1.2 2018-19"
scope:
  taxa: ["Australian vascular plants (APC)", "nationally listed threatened species and communities (EPBC)", "all birds (AVONET)", "all mammals that lived since the last interglacial, extinct ones included (PHYLACINE; COMBINE on PHYLACINE and IUCN 2020-2 taxonomies)"]
  time: "modern taxonomy and status; PHYLACINE also covers mammals extinct in prehistory"
  space: "Australia (APC, EPBC); global (AVONET, COMBINE, PHYLACINE)"
  record_unit: "a name (APC), a listed taxon with status (EPBC), a species with traits (AVONET, COMBINE, PHYLACINE)"
size:
  as_of: "2026-10-22"
  apc_rows: 113869
  apc_accepted_species: 26726
  epbc_species_rows: 2222
  epbc_extinct: 102
  avonet_species_birdlife: 11009
  combine_species: 6263
  phylacine_species: 5831
access:
  tier: open
  licence: "APC CC BY 3.0 (every row's licence column); EPBC CC BY 3.0 AU (data.gov.au); AVONET and COMBINE CC BY 4.0 (Figshare); PHYLACINE CC0 (Zenodo)"
  routes:
    - {type: url, url: "https://biodiversity.org.au/nsl/services/export/taxonCsv", state: "APC built on request (about 45 s), no versions", checked: 2026-10-22}
    - {type: url, url: "data.gov.au package ae652011-f39e-4c6c-91b8-1dc2d2dfee8f (CKAN package_show lists the current, date-stamped CSVs)", state: "species list extracted 2026-08-28; communities 2026-03-20", checked: 2026-10-22}
    - {type: figshare, url: "doi:10.6084/m9.figshare.16586228 (AVONET; 7 versions)", state: "v7 latest", checked: 2026-10-22}
    - {type: figshare, url: "doi:10.6084/m9.figshare.13028255 (COMBINE; 4 versions)", state: "v4 latest", checked: 2026-10-22}
    - {type: zenodo, url: "Zenodo record 4954990 (copy of doi:10.5061/dryad.bp26v20, PHYLACINE 1.2)", state: "one version", checked: 2026-10-22}
  api: "none beyond the file routes; the NSL and data.gov.au CKAN serve their files on plain GET"
versioning:
  replay: partial
  notes: "AVONET, COMBINE and PHYLACINE are fixed DOI versions; APC and EPBC are live lists, so every dated snapshot is kept"
mirror:
  path: deep-server:/data/paleodata/names-status
  policy: "latest version of each; keep every APC and EPBC snapshot"
  state: "apc, epbc, avonet, combine, phylacine: one snapshot each (417 MB in all); see snapshots.tsv"
lineage:
  upstream:
    - "APC: Council of Heads of Australasian Herbaria, via the National Species List (NSL)"
    - "EPBC: the federal list under the Environment Protection and Biodiversity Conservation Act 1999"
    - "COMBINE: compiled from PHYLACINE 1.2, IUCN 2020-2 and published trait sources; PHYLACINE: IUCN 2016-3 and its own taxonomy"
  downstream:
    - "AusTraits and ALA follow APC for plants; COMBINE links to PHYLACINE by binomial"
eprp_questions: []
citation:
  - "Australian Plant Census, National Species List export, retrieved 2026-10-22, CC BY 3.0"
  - "EPBC Act List of Threatened Species, data.gov.au package ae652011-f39e-4c6c-91b8-1dc2d2dfee8f, extract of 2026-08-28, CC BY 3.0 AU"
  - "Tobias, J. A. et al. (2022). AVONET: morphological, ecological and geographical data for all birds. Ecology Letters 25: 581-597. doi:10.1111/ele.13898"
  - "Soria, C. D. et al. (2021). COMBINE: a coalesced mammal database of intrinsic and extrinsic traits. Ecology 102: e03344. doi:10.1002/ecy.3344"
  - "Faurby, S. et al. (2018). PHYLACINE 1.2: The Phylogenetic Atlas of Mammal Macroecology. Ecology 99: 2626. doi:10.1002/ecy.2443"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Names, status and species traits

## Summary

Five open lists that let EPRP put Australian species, living and extinct, on
one footing: the **Australian Plant Census** (APC), the accepted names of the
Australian flora; the federal **EPBC threatened species list**, including 102
taxa listed as extinct; **AVONET**, measured morphology and ecology of all
birds; **COMBINE**, intrinsic and extrinsic traits of all mammals; and
**PHYLACINE 1.2**, every mammal species since the last interglacial, extinct
ones included, with body mass, diet, IUCN status and present-natural ranges.
Together they are the modern comparators bundle: the names to resolve fossil
and occurrence data against, the status to compare extinction risk with, and
the traits that models need. Our cross-checks show where they disagree:
PHYLACINE lacks or misspells several Sahul megafauna that FosSahul records,
and EPBC's list lags taxonomy in both directions.

## Contents

Counts are our own ([profile](profile/names_profile.tsv)).

| List (directory) | Version | Content |
| --- | --- | --- |
| APC (`apc`) | export of 2026-10-22; rows modified to 2026-10-21 | 113,869 names: 34,577 accepted (26,726 species, 2,968 subspecies, 1,280 varieties, 81 forms, 3,114 genera, 309 families); 36,202 taxonomic and 24,754 nomenclatural synonyms; 5,254 misapplied and 2,679 pro parte misapplied; 3,759 excluded; 3,650 orthographic variants. 11,040 phrase names |
| EPBC species (`epbc`) | extracted 2026-08-28 | 2,222 listed taxa: Endangered 870, Vulnerable 784, Critically Endangered 458, Extinct 102, Conservation Dependent 7, Extinct in the wild 1. Extinct by class: mammals 39, birds 22, flowering plants 26, ferns and lycophytes 8, frogs 4, reptiles 1, one earthworm and one red alga |
| EPBC communities (`epbc`) | 2026-03-20 | listed ecological communities (111 rows, source scan; not profiled) |
| AVONET (`avonet`) | v7, 2022-12-05 | 11 sheets: 11,009 species on BirdLife taxonomy, 10,661 on eBird and 9,993 on BirdTree; 90,371 rows of raw specimen measurements; taxonomy crosswalks |
| COMBINE (`combine`) | v4, 2021-04-23 | 6,263 species × 60 columns of reported traits (plus imputed values and sources in 18 files); 786 species have Australasia among their realms. Rows cover the union of the two taxonomies: all 5,831 PHYLACINE species appear; 160 rows are IUCN 2020-2 species PHYLACINE does not recognise; 273 have no IUCN 2020-2 name, mostly PHYLACINE's prehistoric species such as *Diprotodon optatum* (inferred from the EP count). COMBINE therefore inherits PHYLACINE's fossil coverage and its `Palorchestes azeal` spelling |
| PHYLACINE 1.2 (`phylacine`) | Zenodo 4954990 | 5,831 species with IUCN status: LC 3,157, DD 777, VU 525, EN 464, NT 350, **EP (extinct in prehistory) 270**, CR 204, EX 82, EW 2; traits (mass, diet, life habit), synonymy tables, two phylogenies (nexus), current and present-natural range rasters |

**Not mirrored.** The Australian Faunal Directory (AFD) has per-taxon CSV
exports but no licence statement of its own, and refuses exports above 1,000
taxa (birds and reptiles) without an email address; a full extract and licence
are queued as [CONTACTS.md](../CONTACTS.md) C17. AFD's extinction flags are
free text (5 mammal species against EPBC's 39 entries; source scan), so it is
not a status source anyway. The BirdLife Australia Working List states no
licence. The IUCN Red List needs registration and forbids redistribution
([BACKLOG.md](../BACKLOG.md)).

## Provenance and lineage

APC is the Council of Heads of Australasian Herbaria's consensus
classification, served by the National Species List as a Darwin Core-style
export built on request. The EPBC list is the statutory list maintained by the
federal environment department and published as date-stamped CSVs on
data.gov.au. AVONET (Tobias et al. 2022) compiles measurements of individual birds
(90,371 raw rows) into species means. COMBINE (Soria et al. 2021) merged published mammal trait sources on
the IUCN 2020-2 and PHYLACINE 1.2 taxonomies, with imputation for gaps.
PHYLACINE 1.2 (Faurby et al. 2018) is the macroecology atlas for "all 5,831
known mammal species that lived since the last interglacial (~130,000 years
ago until present)" (its metadata PDF, mirrored). Extant taxonomy and status
follow IUCN 2016-3, plus its own EP category. Fossil species enter only with a
record from a directly dated site within the last ~130,000 years, and fossil
forms within living lineages are lumped with them, which the authors note
makes extinction counts conservative.

## Structure

- **APC**: one row per name usage: `taxonID`, `nameType`,
  `acceptedNameUsageID` and `acceptedNameUsage`, `taxonomicStatus`,
  `scientificName`, `canonicalName`, `taxonRank`, `created`, `modified`,
  `license`, `ccAttributionIRI` and others. Filter `taxonomicStatus ==
  "accepted"` for the census; follow `acceptedNameUsageID` for synonyms.
- **EPBC**: one row per listed taxon (species or subspecies): scientific and
  common names, current scientific name, national status, state and territory
  occurrence columns, and Kingdom to Species. No listing or extinction dates.
- **AVONET**: workbook sheets per taxonomy, raw measurements, sources and
  crosswalks. No country field: join by name to a national list.
- **COMBINE**: reported and imputed trait tables keyed by
  `iucn2020_binomial` and `phylacine_binomial` (space-separated);
  `biogeographical_realm` can list several realms in one cell.
- **PHYLACINE**: `Trait_data.csv` keyed by `Binomial.1.2` (underscore
  separated); synonymy tables map earlier PHYLACINE, EltonTraits and IUCN
  2016-3 names to it.

## Access

- **Mirror.** `deep-server:/data/paleodata/names-status/<list>/raw/<version>/`
  with manifests; index [snapshots.tsv](snapshots.tsv); version indexes
  [avonet-figshare-versions.tsv](avonet-figshare-versions.tsv) and
  [combine-figshare-versions.tsv](combine-figshare-versions.tsv).
- **APC.** `data_mirror.py url names-status/apc
  "APC-taxon.csv::https://biodiversity.org.au/nsl/services/export/taxonCsv"`;
  the export is rebuilt on each request, so the snapshot time is its version.
- **EPBC.** Resource URLs change with each extract; read the current ones from
  the CKAN `package_show` record (mirrored as `package.json`).

## Strengths

- Open, citable and small: all five fit in 417 MB, and only APC and EPBC
  change between releases.
- PHYLACINE is the only open species-level list that includes prehistoric
  extinctions with status, mass and diet: 270 EP species, the Sahul megafauna
  among them.
- APC's synonym and misapplication rows make it a resolver, not just a
  checklist.

## Weaknesses and pitfalls

- **EPBC has two name columns; use the current one.** Listed and current
  names differ in 117 rows. Under current names, *Perameles myosurus* is *P.
  myosuros*, *Perameles bougainville fasciata* is the species *P. fasciata*,
  and two extinct emus are subspecies of *Dromaius novaehollandiae*.
- **EPBC mixes species and subspecies.** Of 39 extinct mammal entries, 5 are
  subspecies of living species under current names (for example *Bettongia
  gaimardi gaimardi*). Truncating names to binomials marks living species
  extinct.
- **EPBC lags taxonomy.** *Pseudomys gouldii* is listed extinct, yet ALA carries 965 records of *P. gouldii* from
  1950 on ([ala-vertebrates](../ala-vertebrates/README.md)), consistent with
  the two being one living species (recall: Roycroft and colleagues'
  museum-genomics work).
- **PHYLACINE's taxonomy and statuses date from IUCN 2016-3.** Two species EPBC
  lists as extinct, *Nyctophilus howensis* and *Pipistrellus murrayi*, are CR
  there; *Notamacropus greyi* is *Macropus greyi*; and six EPBC extinct
  mammals are absent: *Chaeropus yirratji*, *Perameles fasciata*, *P.
  myosuros*, *P. notina*, *P. papillon* and *Pseudomys auritus* (names that,
  by recall, postdate it).
- **PHYLACINE misspells and omits megafauna.** *Palorchestes azael* appears
  as `Palorchestes_azeal`. Of 64 extinct mammal binomials in FosSahul, 20
  have no exact match in PHYLACINE: one is that misspelling; two have
  same-family, same-epithet candidates under another genus (*Nototherium
  trilobus* and *Zygomaturus trilobus*; *Congruus kitcheneri* and *Wallabia
  kitcheneri*); and 17 have no candidate at all, among them *Palorchestes
  parvus*, *Thylacoleo hilli*, *Protemnodon devisi*, *Sarcophilus laniarius*
  and *Simosthenurus baileyi*. PHYLACINE's inclusion rule (a directly dated
  record within ~130 ka; fossil forms of living lineages lumped) explains
  some of these by design (inferred). Use its EP list as one view of
  megafaunal extinction, not as the Sahul species list.
- **FosSahul's status column is not a species status.** Three of its
  "Extinct" mammals are living species (*Dasyurus viverrinus* EN,
  *Dendrolagus goodfellowi* EN, *Macropus dorsalis* LC), presumably regional
  losses or errors; the column also holds "?" for 3,035 rows,
  "Extinct/Extant" for 280 and the misspelling "Exinct" for 17.
- **COMBINE's realm field is multi-valued** ("Indomalayan, Palearctic"), and
  514 species have none.
- **APC is plants only.** Animal names need AFD, whose terms are unsettled.

## Overlap with other sources

[names_profile.py](names_profile.py) matches names exactly, then through
PHYLACINE's synonymy table (no match used it), and lists same-genus
near-spellings and same-family same-epithet names as candidates only.

- **EPBC extinct mammals in PHYLACINE.** 34 species under EPBC's current
  names: 27 exact matches (25 EX, 2 CR), 7 unmatched (one with a candidate).
- **FosSahul extinct mammals in PHYLACINE.** 64 binomials (FosSahul 2.0,
  March 2021 file): 44 exact matches (EP 33, EX 8, EN 2, LC 1), 20 unmatched
  (3 with candidates).
- **COMBINE and PHYLACINE.** 785 of COMBINE's 786 Australasian species carry
  a `phylacine_binomial` found in PHYLACINE.
- **AusTraits** follows APC for plant names; **ALA** follows APC and AFD.

## EPRP relevance

Name resolution for fossil and occurrence data (FosSahul, PBDB, ALA, GBIF);
extinction-risk comparisons between prehistoric, historical and current
losses; and species traits (mass, diet, morphology) for Sahul megafauna and
modern comparator models.

## Citation and terms

APC CC BY 3.0, EPBC CC BY 3.0 AU, AVONET and COMBINE CC BY 4.0, PHYLACINE
CC0. Cite the papers and version DOIs in the front matter, and give APC and
EPBC with their retrieval or extract dates.

## Verification log

- 2026-10-22, checked ([names_profile.py](names_profile.py),
  [output](profile/names_profile.tsv)): mirrors with provider checksums
  (Figshare, Zenodo) or sha256 (APC, EPBC); APC counts by status, rank, name
  type and licence; EPBC counts by status and extinct class; AVONET sheet
  rows; COMBINE rows, columns and realms; PHYLACINE statuses; the EPBC,
  FosSahul and COMBINE cross-checks.
- 2026-10-22, checked: AVONET (7) and COMBINE (4) version indexes; citations
  checked against Crossref.
- 2026-10-22, source claim (PHYLACINE 1.2 metadata PDF, mirrored): scope,
  IUCN 2016-3 taxonomy and inclusion rule for fossil species.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): EPBC
  communities row count; AFD export limits, licence position and extinction
  flags; BirdLife Australia Working List licence.
