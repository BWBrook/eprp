---
id: austraits
name: AusTraits, a curated plant trait database for the Australian flora, with the AusTraits Plant Dictionary
kind: compilation
status: active
last_update: 2025-06-20
scope:
  taxa: ["Australian vascular plants (native and naturalised)"]
  time: "modern"
  space: "Australia"
  record_unit: "trait observation: one value (raw, mean, minimum, maximum, mode, median or bin) of one trait for one taxon, from one dataset, with location, context and method"
size:
  as_of: "v7.0.0 (Zenodo 15718081)"
  trait_rows: 1798215
  traits: 530
  datasets: 410
  taxa: 33370
access:
  tier: open
  licence: "CC-BY-4.0 (Zenodo; metadata.yml)"
  routes:
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.3568417", state: "concept DOI, resolves to the latest of 14 versions (v7.0.0)", checked: 2026-10-22}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.21782433", state: "AusTraits Plant Dictionary v2.2.0, the latest of 5 versions (2026-08-04)", checked: 2026-10-22}
    - {type: github, url: "https://github.com/traitecoevo/austraits.build", state: "build pipeline; develop branch builds 470 datasets (source scan)", checked: 2026-10-22}
    - {type: r-package, url: "https://github.com/traitecoevo/austraits", state: "v3.1.1, MIT, not on CRAN (source scan); reader and helpers; not run here", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "14 Zenodo versions (0.1.0 in 2019 to 7.0.0 on 2025-06-20), indexed in zenodo-versions.tsv; the plant dictionary's 5 in plant-dictionary-versions.tsv"
mirror:
  path: deep-server:/data/paleodata/austraits
  policy: "latest release and latest plant dictionary; older versions on demand"
  state: "zenodo/raw/v7.0.0_15718081 (5 files, 162 MB); plant-dictionary/raw/2.2.0_21782433 (10 files, 26 MB); md5 verified"
lineage:
  upstream:
    - "410 datasets (dataset_id), each citing its sources in 603 BibTeX entries (sources.bib)"
    - "794 contributors (contributors.csv)"
    - "traits.build pipeline, which harmonises traits, units and taxonomy"
    - "Australian Plant Census (APC) and APNI names, applied through APCalign release 2025-04-15 (metadata.yml)"
  downstream:
    - "AusTraits Plant Dictionary v2.2.0 (the trait vocabulary, mirrored)"
    - "uses in plant-ecology studies and vegetation models: not surveyed"
eprp_questions: []
citation:
  - "Falster, D. et al. (2021). AusTraits, a curated plant trait database for the Australian flora. Scientific Data 8: 254. doi:10.1038/s41597-021-01006-6"
  - "the version DOI used (v7.0.0: doi:10.5281/zenodo.15718081) and the source datasets of the traits used"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent; review fixes by Claude Sonnet 5.5
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# AusTraits

## Summary

AusTraits harmonises plant trait data for the Australian flora from 410
datasets into one table: 1.8 million observations of 530 traits for 33,370
taxa, each tied to its source, location, context and method, with a controlled
trait dictionary and APC-aligned taxonomy. For EPRP's Sahul work its use is
vegetation and fire parameterisation in simulation models. It holds a
categorical resprouting class for 10,930 species, post-fire recruitment,
serotiny, bud-bank location, seed-bank longevity class, growth form, height,
wood density and seed mass. Two cautions govern its use. Value types mean
different things for categorical and numeric traits (below). And the
resprouting class is not one value per species: 12.3% of its taxa carry both
`resprouts` and `fire_killed` (10.9% in separate records), so an aggregation
rule is part of the method. It is modern data: use it to interpret fossil
pollen and charcoal records, not as palaeo evidence.

## Contents

Counts are our own ([profile](profile/austraits_profile.tsv)) from v7.0.0.

| Table | Rows |
| --- | ---: |
| traits | 1,798,215 |
| taxa | 33,370 (species 26,807, subspecies 2,970, genus 2,022, variety 1,326, form 86, blank 71, family 68, series 20) |
| locations | 39,652 |
| contexts | 2,584 |
| methods | 3,996 |
| contributors | 794 |
| excluded data | 5,246 |
| taxonomic updates | 309,795 |
| BibTeX sources | 603 |

- *Traits.* `definitions.yml` defines 532 traits (418 numeric, 114
  categorical); 530 occur in `traits.csv`. The two never recorded are
  `leaf_specific_hydraulic_conductance` and `stem_sapwood_capacitance`. Rows:
  categorical traits 1,007,335 (56.0%), numeric 790,880 (44.0%).
- *Value types.* Across all rows: mode 1,018,686 (56.6%), raw 242,058 (13.5%),
  maximum 209,300, minimum 158,761, mean 137,851, bin 31,286, median 273. That
  pooled split is misleading, because `mode` is the dictionary's value type
  for categorical values (`schema.yml`, source claim). By trait type:

  | Trait type | Rows | Value types |
  | --- | ---: | --- |
  | categorical | 1,007,335 | mode 1,006,362 (99.9%), raw 936, mean 36, maximum 1 |
  | numeric | 790,880 | raw 241,122 (30.5%), maximum 209,299 (26.5%), minimum 158,761 (20.1%), mean 137,815 (17.4%), bin 31,286 (4.0%), mode 12,324 (1.6%), median 273 |

  98.8% of `mode` rows are categorical. Among numeric traits 46.5% of rows are
  a minimum or maximum; for plant height 99.8% of records are. All 936 raw
  categorical rows are resprouting records on individuals. Entity type:
  categorical rows are 93.9% species-level and 5.6% population; numeric rows
  are 51.8% species-level, 40.3% individual and 7.7% population.
- *Basis of record* is multi-valued (7 values, space-separated). Rows holding
  the value: literature 744,099 (41.4%), field 611,515 (34.0%), preserved
  specimen 561,142 (31.2%), laboratory 61,561, field experiment 18,482,
  captive cultivated 11,235, unknown 3,823. 211,330 rows (11.8%) carry two or
  three values, mostly `field literature` (207,508); 3 rows are blank. Rows
  with one value: preserved specimen 561,105, literature 534,276, field
  400,185.
- *Taxa.* `taxonomic_dataset`: APC 32,668, APNI 560, blank 142.
  `establishment_means`: native 26,472, naturalised 3,428, native and
  naturalised 552, blank 2,918.
- *Fire-response traits* (records / taxa / datasets; taxa are distinct
  `taxon_name` at any rank):

  | Trait | Type | Records | Taxa | Datasets |
  | --- | --- | ---: | ---: | ---: |
  | resprouting capacity | categorical | 35,395 | 13,785 | 66 |
  | resprouting capacity, juvenile plants | categorical | 1,326 | 1,294 | 3 |
  | resprouting after disturbance other than fire | categorical | 3,704 | 3,016 | 2 |
  | proportion of individuals resprouting | numeric, means | 438 | 110 | 5 |
  | post- to pre-fire stem ratio | numeric, means | 780 | 52 | 1 |
  | post-fire recruitment | categorical | 9,446 | 5,085 | 21 |
  | serotiny | categorical | 1,632 | 1,356 | 18 |
  | bud-bank location | categorical | 13,234 | 7,113 | 29 |
  | seed-bank longevity class | categorical | 12,806 | 8,546 | 9 |
  | post-fire flowering | categorical | 431 | 387 | 2 |
  | fire exposure level | categorical | 61 | 53 | 3 |
  | bark thickness | numeric, raw 2,175, mean 1,028 | 3,203 | 371 | 13 |
  | time from fire to flowering | numeric | 4,241 | 2,214 | 13 |
  | time from fire to 50% flowering | numeric | 845 | 424 | 5 |
  | time from fire to peak flowering | numeric | 206 | 124 | 4 |
  | time from fire to flowering decline | numeric | 36 | 18 | 2 |
  | time from fire to fruiting | numeric | 635 | 583 | 10 |
  | time from fire to 50% fruiting | numeric | 7 | 7 | 2 |

- *Fire-behaviour traits* (all numeric, all raw values; the dictionary labels
  flame, smoulder and total burn duration as leaf measurements): flame
  duration 1,061 records, smoulder duration 1,063, time to ignition 1,058 and
  total burn duration 1,063, each for the same 39 taxa from 2 datasets; rate
  of spread 145 records, fuel-bed bulk density 145 and fuel consumption 98,
  each for 25 taxa from 1 dataset.
- *Resprouting capacity in detail.* The 35,395 records are resprouts 18,972,
  fire_killed 13,795, partial_resprouting 2,260 and multi-valued 368
  (`fire_killed resprouts` 288, `fire_killed partial_resprouting` 47,
  `partial_resprouting resprouts` 30, all three 3). Counting each value once per
  record, not per token, matters: tokens sum to 35,766 (resprouts 19,293,
  fire_killed 14,133, partial_resprouting 2,340). By entity type: species
  21,924, population 12,400, individual 936 (the raw rows), metapopulation 135.
  The 13,785 taxa are species 10,930, subspecies 1,214, genus 1,109, variety
  460, family 30, form 27, blank 15. Agreement between records:

  | | All ranks | Species |
  | --- | ---: | ---: |
  | taxa with the trait | 13,785 | 10,930 |
  | records from 2 or more datasets | 7,226 (52.4%) | 6,493 (59.4%) |
  | all records carry the same value | 11,556 (83.8%) | 8,908 (81.5%) |
  | records carry different values | 2,229 (16.2%) | 2,022 (18.5%) |
  | tokens `resprouts` and `fire_killed` both present | 1,700 (12.3%) | 1,515 (13.9%) |
  | of these, single-valued records disagree | 1,496 | 1,345 |
  | of those, inside one dataset | 170 | 139 |
  | of those, only between datasets | 1,326 | 1,206 |
  | records differ, but datasets agree on their modal values | 25 | 23 |
  | records differ, strict majority of datasets (one vote each, its modal value) | 1,267 | 1,167 |
  | records differ, no majority | 937 (6.8%) | 832 (7.6%) |

  Counting tokens instead, 2,261 taxa carry more than one value; the 32 beyond
  2,229 hold one multi-valued string on all their records. Of the 1,700 taxa
  with both tokens, 204 lack separate single-valued `resprouts` and
  `fire_killed` records: one token comes from a multi-valued record.
- *Other modelling traits* (records / taxa / datasets): growth form 112,992 /
  31,557 / 104; plant height 69,716 / 22,855 / 83; seed dry mass 40,423 /
  9,971 / 58; leaf mass per area 32,937 / 4,089 / 154; photosynthetic pathway
  15,018 / 9,738 / 26; wood density 13,080 / 2,160 / 58. Value types: plant
  height maximum 52,096, minimum 17,505, mean 115; seed dry mass mean 22,104,
  raw 18,319; leaf mass per area raw 20,426, mean 12,511; wood density raw
  10,290, mean 2,790.
- *Files.* `austraits-7.0.0.zip` (CSV tables, YAML metadata and dictionary,
  BibTeX), `austraits-7.0.0.rds`, flattened `.rds` and `.parquet` versions of
  the whole database (parquet: 1,798,215 rows, 68 columns), and
  `dictionary.html`.

## Provenance and lineage

Built by Falster and colleagues with hundreds of contributors, using the
`traits.build` pipeline (Ecological Informatics 2024; source claim) to
harmonise each dataset's traits, units and taxonomy. `metadata.yml` names
traits.build v2.1.0 as the compiler and APCalign release 2025-04-15 as the
taxonomic source. Versions run from 0.1.0 (2019, 175 datasets; source claim) to
7.0.0 (2025, 410 datasets); v7.0.0 is the first to add flattened parquet and
rds files. The pipeline's development branch now builds 470 datasets (source
scan), so a new release is likely. The AusTraits Plant Dictionary (APD)
publishes the trait definitions as a vocabulary (JSON, RDF, CSV).

## Structure

A relational set keyed by `dataset_id`, `observation_id`, `taxon_name`,
`trait_name`, `location_id`, `method_id`: `traits` (26 columns: value, unit,
value type, replicates, basis of record, life stage, entity type, method and
context links), plus `taxa`, `locations`, `contexts`, `methods`,
`contributors`, `excluded_data`, `taxonomic_updates`, `definitions.yml` and
`schema.yml`. Vocabularies, with counts from the profile:

- `value_type`: mode, raw, maximum, minimum, mean, bin, median (counts above).
- `trait_type` (from `definitions.yml`, not a column of `traits`): numeric,
  categorical.
- Categorical values and `basis_of_record` can hold several space-separated
  values. For `resprouting_capacity` the dictionary allows three values
  (`fire_killed`, `partial_resprouting`, `resprouts`); no record falls outside
  them. The dictionary's text defines them by the share of plants resprouting
  after a fire scorching all leaves (fire_killed under 30%, partial_resprouting
  30 to 70%, resprouts over 70%) and, separately, names `fire_killed resprouts`
  as the code for a mixed response (source claim, mirrored `definitions.yml`).
  Intermediate responses are therefore coded two ways, 2,260 records as
  `partial_resprouting` and 288 as `fire_killed resprouts`.
- `taxon_rank`: species 26,807, subspecies 2,970, genus 2,022, variety 1,326,
  form 86, blank 71, family 68, series 20.
- `taxonomic_status`: accepted 30,453, genus accepted 2,001, unplaced 547,
  excluded 117, unknown 77, blank 68, family accepted 68, genus unplaced by APC
  12, nomenclatural synonym 9, genus excluded 9, taxonomic synonym 8,
  misapplied 1.
- `taxonomic_dataset`: APC 32,668, APNI 560, blank 142.
- `establishment_means`: native, naturalised, native and naturalised, blank
  (counts above).
- `entity_type`: species, individual, population, metapopulation, unknown
  (counts by trait type in the profile).

## Access

- **Zenodo.** Concept DOI 10.5281/zenodo.3568417 resolves to the latest
  version; [zenodo-versions.tsv](zenodo-versions.tsv) lists all 14.
- **R.** The `austraits` package (GitHub, not CRAN) loads the rds and joins
  tables.
- **Mirror.** `deep-server:/data/paleodata/austraits/zenodo/raw/v7.0.0_15718081/`
  and `plant-dictionary/raw/2.2.0_21782433/`. Index:
  [snapshots.tsv](snapshots.tsv).
- **Reading `traits.csv`.** Not valid UTF-8 as shipped (see Weaknesses). Decode
  line by line, UTF-8 first and Windows-1252 if that fails; no invalid row also
  holds valid non-ASCII UTF-8, so this loses nothing.

## Strengths

- National coverage under one schema, with provenance for every value and a
  published dictionary.
- Resprouting class for 10,930 species, with records from a second dataset for
  59.4% of them, so conflicts can be measured.
- Versioned on Zenodo with DOIs; the flattened parquet carries the whole
  table for use outside R (mind the encoding note).

## Weaknesses and pitfalls

- **Value types differ by trait type.** Categorical rows (56.0% of the table)
  are almost all `mode`, which is the normal label, and 93.9% are
  species-level assignments. Numeric rows mix raw values (30.5%), minima and maxima (46.5%),
  means (17.4%) and bins (4.0%). Plant height is 99.8% minimum or maximum, so
  there is no raw height to pool. Choose the value type per trait before
  pooling or fitting.
- **Resprouting is a conflicted species-level class.** Of 10,930 species,
  18.5% have records with different values, 13.9% carry both `resprouts` and
  `fire_killed`, and 40.6% rest on one dataset. 13,785 is a count of taxa at
  all ranks (2,855 of them not species). The dictionary says the values
  describe mature plants after a fire that scorches all leaves, with fire
  severity an important context (source claim), so disagreement between
  datasets may be real variation between populations as well as error
  (inferred). A rule is needed before any model sees one class per species. A
  defensible one (inferred): keep species rank only; treat each multi-valued string as its own
  class, not as two votes; reduce each dataset to its modal value for the
  species; call a species resprouter or fire-killed only with a strict
  majority of datasets; carry the 832 species with no majority (7.6%), and
  those with a 30-70% response (`partial_resprouting` or `fire_killed
  resprouts`), as an explicit "variable" class or draw them in proportion to
  votes. The conflict rate of the other fire traits (recruitment, serotiny,
  bud bank) is not measured here.
- **Fire-behaviour traits cover 25 to 39 taxa.** Flame and smoulder duration,
  time to ignition and burn duration are 39 taxa from 2 datasets (1,058 to 1,063
  records each); rate of spread, fuel consumption and fuel-bed bulk density are
  25 taxa from 1 dataset (145, 98 and 145 records). They cannot parameterise
  fire behaviour across the flora. Bark thickness covers 371 taxa.
  Quantitative resprouting measures cover 110 taxa (proportion resprouting)
  and 52 (stem ratio).
- **Encoding errors.** 898 lines of `traits.csv` are invalid UTF-8. All are
  rows of one dataset, `Wenk_2022` (898 of its 60,257 rows), all in
  `measurement_remarks`, and all are Windows-1252 bytes: 0x96 (900
  occurrences, an en dash, in citation page ranges such as "187–251") and 0x92
  (6, a right single quotation mark). Strict UTF-8 decoding fails, and the
  flattened parquet holds the same bytes (898 cells identical to the CSV; the
  pyarrow reader raises on the column), so the parquet is not a fix. The rds
  files were not read. Decoding the whole file as Windows-1252 would corrupt
  the 71,826 other rows with valid non-ASCII UTF-8 (two of them in
  `Wenk_2022`'s `taxon_name`), so decode line by line, UTF-8 first. No other CSV
  in the release has an invalid line.
- **Multi-valued fields.** `value` (categorical traits) and `basis_of_record`
  hold space-separated values: 211,330 rows for basis of record, 368 for
  resprouting. Split before counting, and count records, not tokens.
- **Blanks and ranks.** `establishment_means` is blank for 2,918 taxa,
  `taxonomic_dataset` for 142 and `taxon_rank` for 71; 6,563 taxa are not
  species. Records at genus or family rank are not species-level values.
- **Uneven trait coverage.** Recruitment, serotiny, bud-bank and
  seed-bank class traits come from 9 to 29 datasets; fire-timing traits are
  minima, maxima, means or bins (value types per trait are in the profile).
- **Dictionary and data.** The dictionary defines 532 traits and the data
  hold 530. Check a trait's allowed values in `definitions.yml`, not only its
  label.
- **Modern only.** No fossil or palaeo content; mapping traits onto pollen
  types needs a taxonomic crosswalk at genus or family level.

## Overlap with other sources

- **Neotoma and the charcoal sources.** AusTraits supplies the traits of the
  taxa behind pollen types (for example *Eucalyptus*, *Casuarina*,
  Poaceae) and the fire responses that shape charcoal records
  ([neotoma](../neotoma/README.md)); the overlap is thematic and not measured.
- **Names and status lists.** AusTraits taxonomy is aligned to the APC
  (`taxonomic_dataset` APC for 32,668 of 33,370 taxa); the APC export is
  profiled in [names-status](../names-status/README.md).

## EPRP relevance

Vegetation and fire parameterisation for Sahul simulations, interpretation of
pollen and charcoal records, and modern comparators for vegetation change.
What it supports: a resprouter, intermediate or fire-killed class for 10,930
species (81.5% with unanimous records, so 8,908 uncontested before any
aggregation), and single-class recruitment, serotiny, bud-bank and seed-bank
traits for 1,356 to 8,546 taxa, with the uncertainty carried. What it cannot
support: a rate or probability of resprouting (quantitative measures cover 110
and 52 taxa), fire behaviour across the flora (25 to 39 taxa), fire regimes,
or anything before the modern flora. Taxon-level classes are not site-level
outcomes.

## Citation and terms

CC BY 4.0 (`metadata.yml`, checked). Cite Falster et al. (2021), the version
DOI, and the source datasets for the traits used (listed in the bundled
BibTeX). The APC's own terms are CC BY 3.0 (every row's licence column in the
APC export, see [names-status](../names-status/README.md)). That AusTraits'
taxonomy is released under them is a source claim: the mirrored AusTraits
files state no APC licence (no mention of CC BY 3.0 in `metadata.yml`,
`schema.yml`, `definitions.yml` or `build_info.md`).

## Verification log

- 2026-10-22, checked ([austraits_profile.py](austraits_profile.py), output
  [profile/austraits_profile.tsv](profile/austraits_profile.tsv)): table
  counts; 532 defined and 530 present traits; value types by trait type and
  entity type; basis of record by token and combination; records, taxa,
  datasets and value types of each fire-response and modelling trait;
  resprouting values, taxa by rank, agreement, conflicts and the dataset vote;
  taxa vocabularies; 603 BibTeX entries; release metadata (version, date,
  CC-BY-4.0, APCalign release) and the absence of CC BY 3.0 from the four
  metadata files. Run on deep-server in about 50 s: `uv run
  austraits_profile.py <mirror>/austraits-7.0.0.zip
  <mirror>/austraits-7.0.0-flattened.parquet profile/austraits_profile.tsv`.
- 2026-10-22, checked (same script): encoding. 898 invalid lines, one dataset,
  one column, bytes 0x96 and 0x92 and their Windows-1252 characters; the
  parquet holds identical bytes; no invalid line in the other CSVs.
- 2026-10-22, checked: mirror md5 verification of v7.0.0 and APD v2.2.0; version
  indexes (14 AusTraits, 5 APD versions).
- 2026-10-22, source claim (mirrored `definitions.yml` and `schema.yml`): the
  resprouting value thresholds, the `fire_killed resprouts` code for a mixed
  response, the definition's mature plants, full leaf scorch and fire-severity
  context, and `mode` as the value type for categorical values.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): papers and
  DOIs, the 175 datasets of v0.1.0, the development branch's dataset count,
  the R package version and licence, the pipeline paper. The APC's CC BY 3.0
  licence is checked in the names-status entry; its application to AusTraits'
  taxonomy is a source claim.
- 2026-10-22, inferred: the resprouting aggregation rule and its reading of
  disagreement as possible real variation; that the fire-behaviour traits
  cannot parameterise fire behaviour across the flora; that decoding line by
  line loses nothing (from the checked absence of rows holding both invalid
  bytes and valid non-ASCII UTF-8).
- Not checked: the rds files; how R, DuckDB or polars handle the invalid
  bytes; conflict rates of traits other than resprouting capacity.
- 2026-10-22, independent adversarial review (Claude Sonnet subagent):
  findings A1 to A5 applied (value types by trait type, fire-behaviour
  counts, resprouting counts and conflicts, encoding, taxonomy licence and
  complete vocabularies).
