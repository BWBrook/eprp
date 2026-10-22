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
  sahul_datasets: "502 (336 proxy, 166 geochronologic)"
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
  - "Herbert, A. V. et al. (2024). Climate of the Past 20: 2473-2485 (the Indo-Pacific Pollen Database in Neotoma). doi:10.5194/cp-20-2473-2024"
  - "each dataset's DOI, with the acknowledgement text in Neotoma's data use policy"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# Neotoma, with the Indo-Pacific Pollen Database

## Summary

Neotoma is the main community database for Quaternary palaeoecology; its
Australasian content is the Indo-Pacific Pollen Database (IPPD), now being
moved into it. We hold every IPPD dataset plus every other dataset in
Australia and New Guinea: 611 datasets, 502 of them in Sahul at 261 sites (336
proxy datasets and 166 geochronologic ones that carry their dates), including
167 fossil-pollen sequences, 141 modern surface samples and 17 charcoal
records, each with its samples, counts and chronologies. Reach for it for
vegetation history, pollen-based climate or land-cover reconstruction, and as
the vegetation side of megafauna, fire and human-arrival questions. It is
open (CC BY 4.0) and well structured, but the upload is unfinished and the
chronologies are uneven: choose each record's chronology deliberately, and do
not use ages beyond its oldest dating control.

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
  Vanuatu, Tonga, Norfolk Island, Indonesia west of New Guinea).
- *Pollen.* 167 datasets at 144 sites, 5,911 samples, median 46 taxa per
  dataset. 151 are raw counts (NISP); 8 are percentages; 4 were digitised
  from diagrams (3 as percentages, 1 as counts); 4 mix units.
- *Time.* Under each dataset's preferred default chronology (below), 163
  datasets have ages: the oldest age has a median of 8.9 ka; 28 reach 20 ka
  and 12 reach 40 ka.
- *Upload history.* 77 of the 167 Sahul pollen datasets (46%) were added in
  2024, more than in any other year; all 113 Sahul surface-sample datasets
  created this year were added in 2026, and 28 in 2024.

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
group, units, value). Chronologies belong to the collection unit; one default
may be flagged per age type, and 16 Sahul pollen datasets flag several. Each
chronology lists its controls: dating controls (radiocarbon, Pb-210, U-series,
"other dating methods") and tie-points (core tops, interpolations, settlement
horizons, biostratigraphic events). 137 of the 502 Sahul datasets sit on
polygon sites (lake outlines); use their centres for point work. Age types in
use: calibrated radiocarbon BP, radiocarbon BP, calendar BP and calendar
AD/BC.

## Access

- **API.** `datasets?gpid=303` (Australia), `3361` (Papua New Guinea) and
  `2026` (Indonesian New Guinea) list datasets; `datasets/db?database=...`
  lists a constituent database; `downloads/{id,id,...}` returns full
  datasets. The tested script is [neotoma_snapshot.sh](neotoma_snapshot.sh).
  Set `limit` explicitly (default 25). A `loc=` filter given as WKT is
  silently ignored and returns global data; only GeoJSON polygons work. SISAL
  speleothem sites carry no geopolitical unit, so they appear only through a
  polygon query (the source scan found 28 in a 110–160°E, 50°S–5°N box).
- **Mirror.** `deep-server:/data/paleodata/neotoma/ippd-sahul/raw/2026-10-22T0634Z_url/`
  (four listings and 62 download batches; every listed dataset downloaded
  once) and `neotoma/octopus-wfs/` (the OCTOPUS copy). Index:
  [snapshots.tsv](snapshots.tsv).

## Strengths

- Raw counts for 151 of 167 Sahul pollen sequences, so taxa can be
  re-harmonised and re-analysed, not just replotted.
- Full chronologies with their controls; Bacon models for 146 of the 167
  preferred defaults (102 name SHCal13 or SHCal20; 43 say only "Bacon").
- 141 modern surface samples for calibration, absent from other copies.
- Open licence, DOIs per dataset, a documented API with an R client.

## Weaknesses and pitfalls

- **Unfinished transfer.** 299 of the IPPD's 530 sites are in Neotoma; the
  rest exist only in the IPPD's earlier forms.
- **The API's default chronology is not always the calibrated one.** For 20
  Sahul pollen datasets the first flagged default is in radiocarbon years;
  15 of these also flag a calibrated default. Only 5 have no calibrated
  chronology (Lake George, Lynch's Crater dataset 1683, Bega Swamp, Blue Lake,
  Yarlington Tier). Our profile prefers a flagged calibrated or calendar
  chronology; do the same.
- **Thinly dated chronologies.** 65 of 167 preferred defaults rest on fewer
  than five dating controls, 41 on fewer than three, and 7 on none.
- **Ages beyond the dated range.** In 12 datasets the default ages run more
  than 20% beyond the oldest dating control, into the glacial or beyond:
  Lynch's Crater dataset 52582 to 203 ka on controls ending at 37.9 ka, Lake
  George to 117 ka on controls ending at 18.6 ka, Lake Selina to 79 ka on
  52 ka, Lake Hordorli to 68 ka on 32 ka, Old Lake Coomboo Depression to
  495 ka on 225 ka. These are model extrapolations, not dates; for Lynch's
  Crater use dataset 1683, whose 26 dating controls reach 210 ka. Eight
  datasets also label ages beyond 50 ka as radiocarbon or calibrated
  radiocarbon years, which they cannot be.
- **Model labels are free text.** 16 distinct labels among the preferred
  defaults of Sahul pollen datasets ("Bacon SHCal20", "SHCal20 Bacon", "Bacon
  and SHCal13", "linear interpolation", "Linear Interpolation"), 23 across the
  snapshot.
- **Several datasets per site.** 20 sites carry more than one pollen dataset;
  17 of them are separate cores, 3 share a collection unit. Lynch's Crater's
  two datasets (1683 and 52582) come from different collection units with
  different chronologies.
- **Geochronologic datasets have no DOIs** (all 166 in Sahul), so the ages
  behind a chronology cannot be cited separately; dataset DOIs include
  case-variant duplicates (570 strings, 532 distinct ignoring case).
- **API traps** as above (WKT ignored, default limit 25, sites as polygons).

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
- **Charcoal.** 16 of Neotoma's 17 Sahul charcoal datasets lie within about
  2 km of a SahulCHAR record; Ijomba, in central New Guinea, does not, but it
  is in the GCD and RPD. Neotoma adds no charcoal place missing from all
  three other sources.

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
  listed dataset downloaded once; counts above from
  [neotoma_profile.py](neotoma_profile.py).
- 2026-10-22, checked: flagged defaults per dataset, API and preferred default
  age types, dating controls and tie-points, ages beyond the oldest dating
  control, model labels, units, upload years, DOI strings.
- 2026-10-22, checked: OCTOPUS copy (311 datasets, 155,952 baseline rows)
  joined by Neotoma site ID; PBDB Quaternary plant collections within 5 km;
  charcoal locations against SahulCHAR, RPD and GCD.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent, URLs in its
  report): licence and attribution policy, IPPD history and size, API
  behaviour (WKT, limits, rate limit), neotoma2 version, database dumps, the
  SISAL sites seen through a polygon query.
- 2026-10-22, independent review (Claude Sonnet subagent): showed the
  radiocarbon-default count was an artefact of picking the first flagged
  default, that the long ages are extrapolations, the Ijomba exception, the
  label-count scope and a polygon-centre bias (closing vertex counted twice);
  all corrected. Ijomba's 9 km distance is the reviewer's figure.
