---
id: neotoma
name: Neotoma Paleoecology Database, with the Indo-Pacific Pollen Database (IPPD)
kind: database
status: active
last_update: "live; IPPD upload still in progress (113 Sahul surface-sample datasets added in 2026)"
scope:
  taxa: ["pollen and spores", "charcoal", "plant macrofossils", "other proxies"]
  time: "Quaternary; Sahul pollen records mostly Holocene (median oldest default age 8.9 ka), 28 reach 20 ka"
  space: "global; mirrored here as every IPPD dataset (Indo-Pacific) plus every dataset in Australia, Papua New Guinea and Indonesian New Guinea"
  record_unit: "dataset: one proxy type from one collection unit (core or section) at a site, with samples, counts and chronologies"
size:
  as_of: "route ippd-sahul snapshot 2026-10-22T0634Z"
  datasets: 611
  sahul_datasets: 502
  sahul_sites: 261
  sahul_pollen_datasets: 167
  sahul_pollen_samples: 5911
access:
  tier: open
  licence: "CC-BY-4.0 (Neotoma data use and embargo policy v.2025); dataset DOIs carry a Local Contexts Open to Collaborate notice"
  routes:
    - {type: api, url: "https://api.neotomadb.org/v2.0/data/ (datasets, sites, downloads, chronologies)", state: "live, no key; default limit 25", checked: 2026-10-22}
    - {type: r-package, url: "neotoma2 1.1.0 (CRAN, 2026-09-15)", state: "API wrapper; not run here", checked: 2026-10-22}
    - {type: db-snapshot, url: "https://www.neotomadb.org/data/db-snapshots", state: "quarterly Postgres dumps; newest linked file 2024-03-18, before most IPPD uploads", checked: 2026-10-22}
    - {type: octopus-wfs, url: "be10-denude:ippd_datasets, ippd_baseline_pollen", state: "flattened copy of IPPD as of August 2024 (v2.2)", checked: 2026-10-22}
  api: "REST v2.0 with OpenAPI spec (https://api.neotomadb.org/swagger.json); filter by geopolitical unit (gpid), constituent database, dataset type, or a GeoJSON polygon"
versioning:
  replay: partial
  notes: "pollen, surface-sample and charcoal datasets have DOIs (10.21233) and a /frozen/{id} record; geochronologic datasets have none. Quarterly database dumps exist but lag. Snapshot what you use"
mirror:
  path: deep-server:/data/paleodata/neotoma
  policy: "dated snapshots of IPPD and Sahul datasets (listings plus full downloads); the OCTOPUS copy for comparison"
  state: "ippd-sahul 2026-10-22T0634Z_url (66 files, 103 MB, all 611 listed datasets downloaded); octopus-wfs 2026-10-22T0634Z_wfs"
lineage:
  upstream:
    - "IPPD: founded 1997 (G. Hope), merged with QUAVIDA 2013, moving into Neotoma since 2021 (Herbert, Haberle); 530 sites compiled, 299 in Neotoma by October 2026"
  downstream:
    - "OCTOPUS IPPD layers (2024 copy); Mariani et al. 2022, 2024; Adeleye et al. 2021, 2023; Cadd et al. 2021"
eprp_questions: []
citation:
  - "Williams, J. W. et al. (2018). The Neotoma Paleoecology Database, a multiproxy, international, community-curated data resource. Quaternary Research 89: 156-177. doi:10.1017/qua.2017.105"
  - "Herbert, A. V. et al. (2024). The Indo-Pacific Pollen Database, a Neotoma constituent database. Climate of the Past 20: 2473-2485. doi:10.5194/cp-20-2473-2024"
  - "each dataset's DOI, with the acknowledgement text in Neotoma's data use policy"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Neotoma, with the Indo-Pacific Pollen Database

## Summary

Neotoma is the main community database for Quaternary palaeoecology; its
Australasian content is the Indo-Pacific Pollen Database (IPPD), now being
moved into it. We hold every IPPD dataset plus every other dataset in
Australia and New Guinea: 611 datasets, 502 of them in Sahul at 261 sites,
including 167 fossil-pollen sequences, 141 modern surface samples and 17
charcoal records, each with its samples, counts and chronologies. Reach for it
for vegetation history, pollen-based climate or land-cover reconstruction, and
as the vegetation side of megafauna, fire and human-arrival questions. It is
open (CC BY 4.0) and well structured, but the upload is unfinished and the
chronologies are uneven: check each record's age model before using its ages.

## Contents

Counts are our own ([profile](profile/neotoma_profile.tsv); one row per
dataset in [neotoma_datasets.tsv](profile/neotoma_datasets.tsv)). Regions are
assigned from coordinates, as in the other Sahul entries.

| Dataset type | Australia | New Guinea | Torres Strait |
| --- | ---: | ---: | ---: |
| pollen | 138 | 19 | 10 |
| pollen surface sample | 117 | 13 | 11 |
| geochronologic | 140 | 16 | 10 |
| charcoal | 15 | 2 | 0 |
| other (loss on ignition, macrofossil, pollen trap, cladocera, XRF, geochemistry, isotope) | 11 | 0 | 0 |

- The snapshot's 611 datasets are 610 IPPD and one Neotoma surface sample;
  109 lie outside Sahul (New Zealand, Fiji, New Caledonia, French Polynesia,
  Vanuatu, Indonesia west of New Guinea).
- *Pollen.* 167 datasets at 144 sites (20 sites have more than one), 5,911
  samples, median 46 taxa per dataset. 151 datasets are raw counts (NISP); 11
  are percentages, 4 of them digitised from diagrams.
- *Time.* The default chronology's oldest age has a median of 8.9 ka; 28
  datasets reach 20 ka and 12 reach 40 ka.
- *Upload history.* Most Sahul pollen datasets were added in 2024; all 113
  Sahul surface-sample datasets created this year were added in 2026 (source
  scan).

## Provenance and lineage

The IPPD was founded in 1997 by Geoff Hope, merged with Colin Prentice's
QUAVIDA database in 2013, and since 2021 has been moving into Neotoma as
constituent database 4, led by Annika Herbert and Simon Haberle, with more than
400 pollen taxa added to Neotoma's taxonomy and checked against the Australian
Plant Name Index (Herbert et al. 2024). The IPPD paper describes 530 sites;
299 were in Neotoma on 22 October 2026, so the transfer is unfinished.
OCTOPUS mirrors an August 2024 state as flattened layers. Kershaw's
south-eastern Australian pollen database is related but separate.

## Structure

Site (point or lake polygon, altitude, geopolitical units) → collection unit
(core, depositional environment) → dataset (type, constituent database, PI,
DOIs) → sample (depth, ages under each chronology) → datum (taxon, ecological
group, units, value). Chronologies belong to the collection unit, one flagged
default, each with its model, age type and controls. 137 of the 502 Sahul
datasets sit on polygon sites; use centroids for point work. Age types in use:
calibrated radiocarbon BP, radiocarbon BP, calendar BP and calendar AD/BC.

## Access

- **API.** `datasets?gpid=303` (Australia), `3361` (Papua New Guinea) and
  `2026` (Indonesian New Guinea) list datasets; `datasets/db?database=...`
  lists a constituent database; `downloads/{id,id,...}` returns full
  datasets. The tested script is [neotoma_snapshot.sh](neotoma_snapshot.sh).
  Set `limit` explicitly (default 25). A `loc=` filter given as WKT is
  silently ignored and returns global data; only GeoJSON polygons work, and
  SISAL speleothem sites carry no gpid, so they appear only through `loc`.
- **Mirror.** `deep-server:/data/paleodata/neotoma/ippd-sahul/raw/2026-10-22T0634Z_url/`
  (four listings and 62 download batches; every listed dataset downloaded
  once) and `neotoma/octopus-wfs/` (the OCTOPUS copy). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- Raw counts for 151 of 167 Sahul pollen sequences, so taxa can be
  re-harmonised and re-analysed, not just replotted.
- Full chronologies with their controls, and new Bacon models (SHCal13 or
  SHCal20) for most records.
- 141 modern surface samples for calibration, absent from other copies.
- Open licence, DOIs per dataset, a documented API with an R client.

## Weaknesses and pitfalls

- **Unfinished transfer.** 299 of the IPPD's 530 sites are in Neotoma; the
  rest exist only in the IPPD's earlier forms.
- **Uncalibrated and thin chronologies.** The default chronology of 20 Sahul
  pollen datasets is in radiocarbon years, and 52 rest on fewer than five
  controls. Default model labels are inconsistent (25 variants such as "Bacon
  SHCal20", "SHCal20 Bacon", "linear interpolation", "Linear Interpolation").
- **Labels that cannot be right.** Five datasets label default ages beyond the
  radiocarbon range as calibrated radiocarbon years: Lynch's Crater 203 ka,
  Old Lake Coomboo Depression 495 ka, Lake Selina 79 ka, Kosipe 61 ka, Egg
  Lagoon 56 ka. These long records rest on other dating; treat the age type
  as wrong, not the ages.
- **Duplicates per site.** 20 sites carry more than one pollen dataset (Blue
  Lake three, Lynch's Crater two); choose deliberately.
- **Geochronologic datasets have no DOIs** (all 166 in Sahul), so the ages
  behind a chronology cannot be cited separately.
- **Digitised percentages.** 4 datasets were digitised from published diagrams,
  with their precision.
- **API traps** as above (WKT ignored, default limit 25, sites as polygons,
  case-variant duplicate DOIs).

## Overlap with other sources

[neotoma_overlap.py](neotoma_overlap.py) and the charcoal comparison in
[SahulCHAR](../sahulchar/README.md):

- **OCTOPUS IPPD layers.** A flattened copy of the same records (identical
  counts and chronology identifiers where tested in the source scan), frozen
  in August 2024: 311 datasets, of which 120 pollen. 84 of Neotoma's 144
  Sahul pollen sites are in it; 60 are not, and it holds 2 surface samples
  against Neotoma's 141. Use Neotoma.
- **PBDB.** PBDB holds 4,044 Quaternary plant occurrences in 68 Australian
  collections; the 22 Lynch's Crater collections (1,863 occurrences) duplicate
  a Neotoma pollen site, while the Stony Creek Basin cores (Sniderman 2011)
  and the Tasmanian records are only in PBDB.
- **Charcoal.** Neotoma's 17 Sahul charcoal datasets all fall within 5 km of a
  SahulCHAR record (16 within 2 km); Neotoma adds no charcoal places of its
  own.

## EPRP relevance

Supplies vegetation history for Late Quaternary Sahul questions: megafauna
decline and vegetation change (with [FosSahul](../fossahul/README.md)), fire
and human arrival (with [SahulArch](../sahularch/README.md) and the charcoal
sources), and pollen-based climate inputs for simulation. It does not cover
vertebrates, insects or ancient DNA in Sahul.

## Citation and terms

CC BY 4.0. Neotoma asks for three levels of attribution: Neotoma (Williams et
al. 2018), the constituent database (Herbert et al. 2024 for the IPPD), and
the primary publications, with a table of dataset DOIs. The DOI records carry
a Local Contexts "Open to Collaborate" notice, relevant to Indigenous data
governance.

## Verification log

- 2026-10-22, checked: snapshot of 611 datasets in 62 download batches; every
  listed dataset downloaded once; counts above from the snapshot.
- 2026-10-22, checked: age types, model labels, control counts and oldest
  default ages per dataset; datasets without DOIs.
- 2026-10-22, checked: OCTOPUS copy (311 datasets, 155,952 baseline rows)
  joined by Neotoma site ID; PBDB Quaternary plant collections within 5 km.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent, URLs in its
  report): licence and attribution policy, IPPD history and size, API
  behaviour (WKT, limits, rate limit), neotoma2 version, database dumps, upload
  dates.
