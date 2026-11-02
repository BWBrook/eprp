---
id: names-status
name: Names, conservation status and species traits for Australian comparisons (APC, EPBC lists, AVONET, COMBINE, PHYLACINE)
kind: compilation
status: active
last_update: "APC export 2026-10-22 (rows modified to 2026-10-21); EPBC species list extracted 2026-08-28; AVONET v7 2022-12-05; COMBINE v4 2021-04-23; PHYLACINE 1.2 record 2019-05-11 (paper 2018-10)"
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
  combine_rows: 6263
  phylacine_species: 5831
access:
  tier: open
  licence: "APC CC BY 3.0 (every row's licence column); EPBC CC BY 3.0 AU (data.gov.au); AVONET and COMBINE CC BY 4.0 (Figshare); PHYLACINE CC0 (Zenodo), with the authors' statement that its IUCN-derived parts are transformative derivative works"
  routes:
    - {type: url, url: "https://biodiversity.org.au/nsl/services/export/taxonCsv", state: "APC built on request (about 45 s), no versions", checked: 2026-10-22}
    - {type: url, url: "https://data.gov.au/data/api/3/action/package_show?id=ae652011-f39e-4c6c-91b8-1dc2d2dfee8f", state: "CKAN record listing the current, date-stamped CSVs; species list extracted 2026-08-28, communities 2026-03-20", checked: 2026-10-22}
    - {type: figshare, url: "https://doi.org/10.6084/m9.figshare.16586228", state: "AVONET; 7 versions, v7 latest", checked: 2026-10-22}
    - {type: figshare, url: "https://doi.org/10.6084/m9.figshare.13028255", state: "COMBINE; 4 versions, v4 latest", checked: 2026-10-22}
    - {type: zenodo, url: "https://zenodo.org/records/4954990", state: "PHYLACINE 1.2; the record carries the Dryad DOI 10.5061/dryad.bp26v20; one version", checked: 2026-10-22}
  api: "none beyond the file routes; the NSL and data.gov.au CKAN serve their files on plain GET"
versioning:
  replay: partial
  notes: "AVONET, COMBINE and PHYLACINE are fixed DOI versions; APC and EPBC are live lists, so every dated snapshot is kept"
mirror:
  path: deep-server:/data/paleodata/names-status
  policy: "latest version of each; keep every APC and EPBC snapshot"
  state: "apc, epbc, avonet, combine, phylacine: one snapshot each (417.7 MB in all); see snapshots.tsv"
lineage:
  upstream:
    - "APC: Council of Heads of Australasian Herbaria, via the National Species List (NSL)"
    - "EPBC: the federal list under the Environment Protection and Biodiversity Conservation Act 1999"
    - "COMBINE: compiled from PHYLACINE 1.2, IUCN 2020-2 and published trait sources"
    - "PHYLACINE: IUCN 2016-3 for living species, its own taxonomy for fossil species"
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
  reviewed: "2026-10-22, independent Claude Sonnet subagent; findings applied"
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
the traits that models need. Only COMBINE is itself a compilation; the five
are catalogued as one bundle because they are used together. Our
cross-checks show where they disagree: PHYLACINE misspells, omits and lumps
several extinct Sahul mammals that FosSahul records, and EPBC still lists as
extinct a species resurrected in 2021.

## Contents

Counts are our own ([profile](profile/names_profile.tsv)).

| List (directory) | Version | Content |
| --- | --- | --- |
| APC (`apc`) | export of 2026-10-22; rows modified to 2026-10-21 | 113,869 name usages in 19 `taxonomicStatus` values: 34,577 accepted, 36,202 taxonomic and 24,754 nomenclatural synonyms, 5,254 misapplied and 2,679 pro parte misapplied, 3,759 excluded (names APC excludes from the census; see `taxonRemarks`), 3,650 orthographic variants, 1,284 basionyms and smaller classes. Accepted by rank: 26,726 species, 3,114 genera, 2,968 subspecies, 1,280 varieties, 309 families, 81 forms and 99 at other ranks. The 26,726 accepted species include 1,683 phrase names and 520 hybrids or intergrades (24,523 plain scientific names). 34,487 accepted rows carry `taxonDistribution` (state occurrence) |
| EPBC species (`epbc`) | extracted 2026-08-28 | 2,222 listed taxa: Endangered 870, Vulnerable 784, Critically Endangered 458, Extinct 102, Conservation Dependent 7, Extinct in the wild 1. Extinct by class: mammals 39, birds 22, flowering plants 26, ferns and lycophytes 8, frogs 4, reptiles 1, one earthworm and one red alga. Occurrence in 17 state, territory and marine-area columns, coded "Yes" or "-" |
| EPBC communities (`epbc`) | 2026-03-20 | 111 listed ecological communities |
| AVONET (`avonet`) | v7, 2022-12-05 | 11 sheets: 11,009 species on BirdLife taxonomy, 10,661 on eBird and 9,993 on BirdTree; raw data for 90,020 measured individuals (75,843 museum specimens, 14,177 live birds), matching the paper, plus 351 gap-species placeholder rows; taxonomy crosswalks |
| COMBINE (`combine`) | v4, 2021-04-23 | 6,263 rows × 60 columns (54 traits and 6 identifiers) in `trait_data_reported.csv`, one of 18 files with imputed values, sources and validation. The paper reports 6,234 species. Rows are not species: all 5,831 PHYLACINE species appear, 163 of them in several rows (up to 10) because IUCN 2020-2 splits what PHYLACINE lumps, and 160 rows are IUCN species PHYLACINE does not recognise. 273 rows have no IUCN 2020-2 name: 268 are PHYLACINE's prehistoric (EP) species, such as *Diprotodon optatum*, plus five others (among them *Homo sapiens*). 809 rows (808 IUCN species) list Australasia among their realms; 798 of them link to 785 PHYLACINE species and 11 have no PHYLACINE name (for example *Pseudomys auritus*, *Rattus detentus*) |
| PHYLACINE 1.2 (`phylacine`) | Zenodo 4954990 | 5,831 species with IUCN status: LC 3,157, DD 777, VU 525, EN 464, NT 350, **EP (extinct in prehistory) 270**, CR 204, EX 82, EW 2; traits (mass, diet, life habit), synonymy tables (with 48 names listed as not accepted), two phylogenies (nexus), current and present-natural range rasters |

**Not mirrored.** The Australian Faunal Directory (AFD) has per-taxon CSV
exports but no licence statement of its own, and refuses exports above 1,000
taxa (birds and reptiles) without an email address; a full extract and licence
are queued as CONTACTS.md (queue held back) C17. AFD's extinction flags are
free text (5 mammal species against EPBC's 39 entries; source scan), so it is
not a status source anyway. The BirdLife Australia Working List states no
licence. The IUCN Red List needs registration and forbids redistribution
([BACKLOG.md](../BACKLOG.md)).

## Provenance and lineage

APC is the Council of Heads of Australasian Herbaria's consensus
classification, served by the National Species List as a Darwin Core-style
export built on request. The EPBC list is the statutory list maintained by the
federal environment department and published as date-stamped CSVs on
data.gov.au. AVONET (Tobias et al. 2022) compiles measurements of individual
birds into species means. COMBINE (Soria et al. 2021) merged published mammal
trait sources on the IUCN 2020-2 and PHYLACINE 1.2 taxonomies, with
imputation for gaps. PHYLACINE 1.2 (Faurby et al. 2018) is the macroecology
atlas for "all 5,831 known mammal species that lived since the last
interglacial (~130,000 years ago until present)" (its metadata PDF,
mirrored). Extant taxonomy and status follow IUCN 2016-3, plus its own EP
category. Fossil species enter only with a record from a directly dated site
within the last ~130,000 years, and fossil forms within living lineages are
lumped with them, which the authors note makes extinction counts
conservative.

## Structure

- **APC**: one row per name usage: `taxonID`, `nameType`,
  `acceptedNameUsageID` and `acceptedNameUsage`, `taxonomicStatus`,
  `scientificName`, `canonicalName`, `taxonRank`, `taxonDistribution`,
  `taxonRemarks`, `created`, `modified`, `license`, `ccAttributionIRI` and
  others. Filter `taxonomicStatus == "accepted"` for the census; follow
  `acceptedNameUsageID` for synonyms. The profile lists every status, rank and
  name type.
- **EPBC**: one row per listed taxon (species or subspecies): listed and
  current scientific names, common name, national status, 17 occurrence
  columns ("Yes" or "-"), SPRAT taxon IDs, and Kingdom to Species. No listing
  or extinction dates.
- **AVONET**: workbook sheets per taxonomy (species means, range centroid,
  latitude limits and range size, no country), raw measurements per
  individual with `Data.type` (1 museum specimen, 2 live bird), `Locality`
  and `Country_WRI` (filled for 77,245 rows, 4,343 of them Australia; the
  `Country` column is empty), sources and crosswalks.
- **COMBINE**: reported and imputed trait tables keyed by
  `iucn2020_binomial` and `phylacine_binomial` (space-separated; "Not
  recognised" where a taxonomy lacks the species); `biogeographical_realm`
  can list several realms in one cell, and is the literal "NA" for 514 rows.
- **PHYLACINE**: `Trait_data.csv` keyed by `Binomial.1.2` (underscore
  separated); synonymy tables map earlier PHYLACINE, EltonTraits and IUCN
  2016-3 names to it, and list names it does not accept.

## Access

- **Mirror.** `deep-server:/data/paleodata/names-status/<list>/raw/<version>/`
  with manifests; index [snapshots.tsv](snapshots.tsv); version indexes
  [avonet-figshare-versions.tsv](avonet-figshare-versions.tsv) and
  [combine-figshare-versions.tsv](combine-figshare-versions.tsv).
- **APC.** `python3 resources/tools/data_mirror.py url names-status/apc
  --license "CC BY 3.0 (per-row licence column of the NSL export)"
  "APC-taxon.csv::https://biodiversity.org.au/nsl/services/export/taxonCsv"`;
  the export is rebuilt on each request, so the snapshot time is its version.
- **EPBC.** Resource URLs change with each extract; read the current ones from
  the CKAN `package_show` record (mirrored as `package.json`).
- **Profile.** `uv run names_profile.py /data/paleodata/names-status
  <FosSahul_updated_March2021.csv> names_profile.tsv`.

## Strengths

- Open, citable and small: all five fit in 418 MB, and only APC and EPBC
  change between releases.
- PHYLACINE is the only open species-level list we found that includes
  prehistoric extinctions with status, mass and diet: 270 EP species, the
  Sahul megafauna among them.
- APC's synonym and misapplication rows make it a resolver, not just a
  checklist, and `taxonDistribution` gives state occurrence.
- AVONET's raw sheet allows specimen-level work, including 4,343 individuals
  measured from Australia.

## Weaknesses and pitfalls

- **EPBC has two name columns; use the current one.** Listed and current
  names differ in 117 rows. Under current names, *Perameles myosurus* is *P.
  myosuros*, *Perameles bougainville fasciata* is the species *P. fasciata*,
  and the two extinct emus listed under species names (*Dromaius ater*, *D.
  baudinianus*) are subspecies of *D. novaehollandiae*.
- **EPBC mixes species and subspecies.** Of 39 extinct mammal entries, 5 are
  subspecies of living species under current names (for example *Bettongia
  gaimardi gaimardi*); of 22 extinct bird entries, 15 are subspecies.
  Truncating names to binomials marks living species extinct.
- **EPBC lags a resurrection.** It lists *Pseudomys gouldii* as Extinct and
  *P. fieldi* (Shark Bay mouse) as Vulnerable, but Roycroft et al. (2021,
  PNAS 118: e2021390118) showed that Gould's mouse survives as the Shark Bay
  population and resurrected the name (their abstract, via Crossref). ALA
  already holds 965 records of *P. gouldii* from 1950 on, 957 of them from
  Western Australia ([ala-vertebrates](../ala-vertebrates/README.md)).
- **PHYLACINE's taxonomy and statuses date from IUCN 2016-3.** Two species EPBC
  lists as extinct, *Nyctophilus howensis* and *Pipistrellus murrayi*, are CR
  there. *Pseudomys auritus* is on PHYLACINE's list of names it does not
  accept. Six EPBC extinct mammals have no PHYLACINE match: *Notamacropus
  greyi* (PHYLACINE's *Macropus greyi*), *Chaeropus yirratji* and *Perameles
  papillon* (described after IUCN 2016-3, recall), and *P. fasciata*, *P.
  myosuros* and *P. notina* (older names recognised at species rank later,
  recall).
- **PHYLACINE misspells, omits and lumps extinct Sahul mammals.**
  *Palorchestes azael* appears as `Palorchestes_azeal`. Of 64 extinct mammal
  binomials in FosSahul, 20 have no exact match: one is that misspelling; one
  is *Pseudomys auritus*, not accepted; two have same-family, same-epithet
  names under another genus (*Nototherium trilobus* and *Zygomaturus
  trilobus*; *Congruus kitcheneri* and *Wallabia kitcheneri*); 16 have no
  similarly spelled name, though PHYLACINE holds the genus of 12. The
  inclusion rule explains most: 11 of the 20 have no FosSahul record dated
  within 130 ka, against 1 of the 44 matched species (*Propleopus
  oscillans*). *Sarcophilus laniarius*, which has such dates, is lumped with
  *S. harrisii* by design (inferred from the lumping rule). Use the EP list as
  one view of megafaunal extinction, not as the Sahul species list.
- **COMBINE's fossil species are names only.** All 270 EP rows have realm
  "NA", so realm cannot select Sahul megafauna; 215 of them carry 4 of 54
  trait values, though 257 have adult mass.
- **FosSahul's status column is row-level.** 9 of its 64 extinct mammal
  binomials also have non-Extinct rows (*Dasyurus viverrinus* Extant 89,
  Extinct 5; *Sarcophilus laniarius* Extinct 38, Extant 2), and three are
  living species (*D. viverrinus* EN, *Dendrolagus goodfellowi* EN, *Macropus
  dorsalis* LC). The column also holds "?" for 3,035 rows, "Extinct/Extant"
  for 280 and the misspelling "Exinct" for 17. The binomial filter drops 439
  of 1,970 extinct mammal rows, mostly indeterminate (*Diprotodon* species
  indet. 180) plus *Macropus giganteus titan* (17).
- **COMBINE's realm field is multi-valued** ("Indomalayan, Palearctic").
- **APC is plants only.** Animal names need AFD, whose terms are unsettled.

## Overlap with other sources

[names_profile.py](names_profile.py) matches names exactly, then through
PHYLACINE's synonymy table (no match used it), then against the names
PHYLACINE does not accept, and lists same-genus near-spellings and
same-family same-epithet names as candidates only.

- **EPBC extinct mammals in PHYLACINE.** 34 species under EPBC's current
  names: 27 exact matches (25 EX, 2 CR), 1 not accepted, 6 unmatched (one
  with a candidate).
- **FosSahul extinct mammals in PHYLACINE.** 64 binomials (FosSahul 2.0,
  March 2021 file): 44 exact matches (EP 33, EX 8, EN 2, LC 1), 1 not
  accepted, 19 unmatched (3 with candidates).
- **COMBINE and PHYLACINE.** COMBINE's PHYLACINE names are exactly
  PHYLACINE's 5,831; 785 PHYLACINE species are Australasian in COMBINE.
- **AusTraits** follows APC for plant names; **ALA** follows APC and AFD.

## EPRP relevance

Name resolution for fossil and occurrence data (FosSahul, PBDB, ALA, GBIF);
extinction-risk comparisons between prehistoric, historical and current
losses; and species traits (mass, diet, morphology) for Sahul megafauna and
modern comparator models. What the bundle cannot support: animal name
resolution beyond mammals and birds (AFD is not mirrored), selecting fossil
species by realm, or plant native status beyond APC's `taxonDistribution`.

## Citation and terms

APC CC BY 3.0, EPBC CC BY 3.0 AU, AVONET and COMBINE CC BY 4.0, PHYLACINE
CC0. PHYLACINE's authors state that its IUCN-derived parts are transformative
derivative works freely distributable under IUCN's terms, that "IUCN was
notified", and that use requires citing both PHYLACINE and the underlying
datasets (metadata PDF); this sits beside the IUCN Red List's own
no-redistribution terms. COMBINE carries IUCN-derived columns too. Cite the
papers and version DOIs in the front matter, and give APC and EPBC with their
retrieval or extract dates.

## Verification log

- 2026-10-22, checked ([names_profile.py](names_profile.py),
  [output](profile/names_profile.tsv)): mirrors with provider checksums
  (Figshare, Zenodo) or sha256 (APC, EPBC); APC counts by every status, rank
  and name type, accepted species by name type, `taxonDistribution`; EPBC
  counts by status, extinct class, place columns, the two *Pseudomys*
  listings and community rows; AVONET sheet rows, raw rows by data type,
  gap-species rows and country fields; COMBINE rows by taxonomy, Australasian
  rows and EP rows; PHYLACINE statuses and not-accepted names; the EPBC and
  FosSahul matches, FosSahul filter exclusions, mixed-status species and
  dating within 130 ka.
- 2026-10-22, checked: AVONET (7) and COMBINE (4) version indexes; citations
  and first authors checked against Crossref.
- 2026-10-22, source claim: PHYLACINE 1.2 metadata PDF (mirrored) for its
  scope, IUCN 2016-3 taxonomy, inclusion rule and IUCN derivative-works
  statement; the Roycroft et al. (2021) abstract (Crossref) for the
  resurrection of *P. gouldii*; the AVONET and COMBINE papers (via the
  review's Crossref reading) for 90,020 individuals and 6,234 species.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): AFD export
  limits, licence position and extinction flags; BirdLife Australia Working
  List licence.
- 2026-10-22, reviewed by an independent Claude Sonnet subagent; its findings
  (COMBINE placeholder counts, PHYLACINE's rejected names, AVONET individuals
  and country fields, FosSahul filters and dating, APC vocabularies, licence
  notes) are applied above.
