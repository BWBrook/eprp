---
id: macrostrat
name: Macrostrat, columns, units and gap-bound packages (API v2), global snapshot
kind: database
status: active
last_update: "live; snapshot 2026-10-25T0011Z (API version 2.5.0)"
scope:
  taxa: ["not taxonomic: rock units, with links to PBDB collections"]
  time: "Archean to present (oldest unit base 4,059 Ma); dense for the Phanerozoic of North America"
  space: "North America (1,076 columns), ocean drilling (eODP 1,710 holes; Deep Sea 133 sites), New Zealand (587), North American Ediacaran (218), Caribbean (64), South America (61), Indonesia (25, in process), Africa (2), Australia (1 placeholder)"
  record_unit: "a lithostratigraphic unit in a column (a polygon of crust or a measured section), with ages, thickness, lithology, environment and PBDB links"
size:
  as_of: "snapshot 2026-10-25T0011Z"
  columns_ex_composite: 3878
  units_ex_composite: 133418
  files: 85
  bytes: 419204098
access:
  tier: open
  licence: "CC BY 4.0 (API meta: 'All data are licensed under Creative Commons BY 4.0 International')"
  routes:
    - {type: api, url: "https://macrostrat.org/api/v2", state: "API v2.5.0: columns, units, sections, fossils, measurements, defs and stats, all as JSON or CSV; no bulk download; snapshotted by project and column status", checked: 2026-10-25}
    - {type: web, url: "https://macrostrat.org", state: "map and column browser (not used)", checked: 2026-10-25}
  api: "Macrostrat API v2 (no key)"
versioning:
  replay: partial
  notes: "a live database with no versions or change log by record; each snapshot here is dated and checksummed (sha256). The /changes route serves an HTML changelog page, not data"
mirror:
  path: deep-server:/data/paleodata/macrostrat
  policy: "a dated snapshot of every project's columns, units, sections, PBDB links and measurements, and every definition table; geologic maps not mirrored"
  state: "raw/2026-10-25T0011Z_url: 85 files (419 MB), sha256 recorded; verifies"
lineage:
  upstream:
    - "regional stratigraphic syntheses and measured sections compiled by the Macrostrat team (Peters and colleagues, University of Wisconsin-Madison) and contributors (defs/sources, defs/refs); eODP from ocean-drilling hole data; PBDB collections matched to units"
  downstream:
    - "Macrostrat-based rock-record and diversity studies (e.g. Peters 2005 onwards; recall); the PBDB's stratigraphic context; StratPal and similar filtering tools (B-007 prior)"
eprp_questions: [B-005, B-007, B-008, Q-005, Q-023, Q-035, Q-041]
citation:
  - "Peters, S. E., Husson, J. M. & Czaplewski, J. (2018) Macrostrat: a platform for geological data integration and deep-time Earth crust research. Geochemistry, Geophysics, Geosystems 19: 1393-1409, doi:10.1029/2018GC007467 (details recall; DOI resolves)"
  - "Macrostrat (2026) API v2, https://macrostrat.org/api/v2, accessed 2026-10-25, CC BY 4.0 (the API's citation: 'Peters, S.E. et al. Macrostrat: a platform for geological data integration and deep-time research. https://macrostrat.org, accessed on (date)')"
entry:
  created: 2026-10-25
  updated: 2026-10-25
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# Macrostrat

## Summary

Macrostrat is a database of the rock record. It divides the crust into
columns, each a polygon or a measured section, and stacks in each column its
lithostratigraphic units, with ages, thickness, lithology, depositional
environment and links to PBDB collections. Units are grouped into gap-bound
packages ("sections"). For the blue-sky register it supplies three things:
- **B-005:** the area of marine and non-marine rock through time, the
  classic covariate for sampled diversity.
- **B-007:** the stratigraphic architecture an architecture-only null needs.
- **B-008:** environments through each crisis.

Two findings limit how far it can be used:
- **Coverage is not global.** North America and ocean drilling hold 95% of
  the units. Australia is a one-column placeholder, Africa has 2 columns,
  and Europe and most of Asia have none. The Australian negative recorded in
  the asud and pbdb entries holds globally outside North America, New
  Zealand and the Caribbean.
- **Unit ages follow the same interval conventions as PBDB.** In North
  America 18% of unit tops and bottoms fall exactly on an international
  stage boundary, and only 2% of units have a radiometric date. Codex's
  correction to B-007 ("Macrostrat and PBDB share chronological conventions")
  is measurable here: boundary clustering is partly built into the ages.

Reach for it for North American and New Zealand rock quantity and
architecture. Do not use it as a global record or an independent chronology.

![North American column area with marine and with non-marine units, by stage](profile/macrostrat_stage_area.png)

*Summed area of North American columns with a marine unit and with a
non-marine unit spanning each international stage's midpoint
([series](profile/macrostrat_stage_area.tsv), drawn by
[plot_stage_area.py](plot_stage_area.py)).*

## Contents

By project ([profile](profile/macrostrat_profile.tsv); project 14, "core
columns", composites the others and is left out of totals):

| Project | Columns (active / in process / obsolete) | Units | Gap-bound sections | PBDB collections linked |
| --- | --- | ---: | ---: | ---: |
| 1 North America | 1,076 (949 / 6 / 121) | 27,034 | 8,208 | 48,696 |
| 3 eODP (drilling holes) | 1,710 sections | 92,451 | 2,029 | 0 |
| 4 Deep Sea (drilling sites) | 133 | 7,356 | 389 | 0 |
| 5 New Zealand | 587 (329 / 258 / 0) | 2,871 | 1,096 | 328 |
| 10 North American Ediacaran | 218 | 1,372 | 648 | 0 |
| 8 South America | 61 | 1,238 | 469 | 0 |
| 7 Caribbean | 64 | 798 | 243 | 897 |
| 12 Indonesia | 25 (in process) | 212 | 64 | 0 |
| 9 Africa | 2 | 41 | 11 | 0 |
| 6 Australia | 1 (placeholder, no ages) | 32 | 4 | 0 |
| 11 North American Cretaceous | 1 (no ages) | 13 | 2 | 0 |
| 13 Northern Eurasia | 0 | 0 | 0 | 0 |

North America's units: 24,141 have a numeric base age, ranging back to
4,059 Ma. By environment class, 19,471 are marine, 3,845 non-marine, 928 both
and 2,790 have none. There are 1,086,577 measurement rows (geochemistry
mostly: Ba, Cu, Fe, Cr, Sr, major oxides; plus U–Pb dates), against the
1,222,193 measurements the stats route reports. The definition tables hold
1,716 intervals, 214 lithologies, 87 environments (43 marine, 44
non-marine), 124 measurement types, and the stratigraphic-name lexicon and
concepts (51 MB of JSON).

## Provenance and lineage

The Macrostrat team at the University of Wisconsin–Madison (Peters,
Czaplewski, Quinn, Husson and others) compiles columns from regional
syntheses and measured sections, each unit sourced in `defs/sources` and
`defs/refs`. eODP turns ocean-drilling holes into section columns; Deep Sea
composites drilling sites. PBDB collections are matched to units by
stratigraphic name and position, which gives the `fossils` route and the
units' PBDB counts. The API is at version 2.5.0, and nothing is versioned by
record, so each snapshot here is dated.

## Structure

- **Columns** (GeoJSON): `col_id`, polygon, `col_area` (km²), project,
  `col_type` (column or section), `status_code` (active, in process,
  obsolete), age range, and summary lithology and environment.
- **Units** (CSV, `response=long`): `unit_id`, `section_id` (the gap-bound
  package), `col_id`, names (`Mbr`, `Fm`, `Gp`, `SGp`, `strat_name_id`),
  `t_age`/`b_age`, `t_int_name`/`b_int_name` with `t_prop`/`b_prop` (the
  position within the top and bottom intervals, 0 to 1), thickness,
  `lith`, `environ` and `econ` (each "name type class ~ proportion",
  separated by `|`), `pbdb_collections`, `pbdb_occurrences`, centroid and
  palaeo-coordinates (`t_plat`, `b_plat`).
- **Sections:** gap-bound packages with their age range, thickness,
  lithology and environment mixes.
- **Fossils:** PBDB collections matched to units, with `pbdb_occs`, unit
  and column.
- **Measurements** (`response=long&show_values`): value, error, method,
  sample, lithology and the unit it belongs to.
- **Definitions:** intervals and timescales, lithologies and attributes,
  environments, economic types, measurement types, stratigraphic names and
  concepts, sources, references, projects, column groups, drilling sites,
  minerals, structures, plates.

An empty project returns a two-byte CSV. The age-model route
(`age_model?col_id=`) returned nothing for the column tried and is not
mirrored.

## Access

- **Mirror.** `deep-server:/data/paleodata/macrostrat/raw/2026-10-25T0011Z_url/`:
  `columns__pNN.geojson`, `units__pNN.csv`, `sections__pNN.csv`,
  `fossils__pNN.csv`, `measurements__pNN.csv` per project, `defs__*.json`,
  `stats.csv`, and the manifest. [snapshots.tsv](snapshots.tsv).
- **Refresh.** [macrostrat_snapshot.sh](macrostrat_snapshot.sh), with
  [macrostrat_specs.py](macrostrat_specs.py) listing the requests (85 in all,
  one a second; about six minutes). Each run is a new dated snapshot.
- **Profile.** `python3 macrostrat_profile.py SNAPSHOT_DIR PBDB_GLOBAL_RAW
  OUT_TSV SERIES_TSV` ([profiler](macrostrat_profile.py)). It writes the
  [profile](profile/macrostrat_profile.tsv) and the
  [stage-area series](profile/macrostrat_stage_area.tsv).
- **Check against the provider.** Units per project in the snapshot equal
  the stats route's counts for every project.

## Strengths

- The standard quantitative description of the North American rock record,
  with gap-bound packages, column areas and environments, ready for
  rock-quantity covariates and architecture nulls.
- Openly licensed with a documented API, and linked to PBDB collections.
- Ocean drilling as continuous section columns (eODP, Deep Sea).

## Weaknesses and pitfalls

- **Not global.** See Contents. Outside North America, New Zealand and the
  Caribbean, coverage is thin or absent. A "global" rock-quantity curve from
  Macrostrat is a North American curve.
- **Ages are interval-derived.** In North America 9,676 of 54,068 unit tops
  and bottoms (17.9%) equal an international stage boundary, and 12,887
  (23.8%) sit on the edge of their interval (`t_prop` or `b_prop` 0 or 1).
  Only 515 units (1.9%) have a radiometric measurement (units of Ma). The
  shares on stage boundaries are 40% in the Caribbean, 23% in South America
  and 75% in Indonesia. Unit boundaries cluster at stage boundaries by
  construction, so B-007's architecture-only null must model age assignment
  separately, or use the dated units and eODP's own age models.
- [Detail withheld pending disclosure to the data custodian.]
  - Caribbean: 215 of 897 collections, 6,937 beyond;
  - New Zealand: 107 of 328 collections, 1,567 beyond.

  These are counts, not records, but any occurrences-per-unit covariate
  inherits them. Recount from public PBDB data under the main project's PBDB
  hold ([pbdb](../pbdb/README.md)). Queued for both providers
  ([CONTACTS.md](../CONTACTS.md) C10 (k), C34).
- **Project 14 duplicates.** "Core columns" composites other projects
  (39,338 units); never add it to their totals.
- **Areas need care.** eODP holes have no area. Column areas sum to more
  than a region when obsolete columns are kept (121 in North America).
  Filter on `status_code`.
- **Environment is not always given.** 2,790 North American units (10%)
  have none, and the North American Ediacaran has none for 771 of 1,372.

## Overlap with other sources

- **[pbdb](../pbdb/README.md).** Macrostrat links 48,696 PBDB collections in
  North America, 897 in the Caribbean and 328 in New Zealand. It shares
  PBDB's interval conventions.
- **[timescale](../timescale/README.md).** Holds Macrostrat's interval
  table (1,716 intervals) from an earlier snapshot. The same table is here
  in `defs__intervals.json`.
- **[asud](../asud/README.md).** Macrostrat's name lexicon took 12,279
  Australian names from ASUD in 2015, but there are no Australian columns.
- **[nsb](../nsb/README.md), [triton](../triton/README.md).** Ocean-drilling
  microfossil data; eODP gives the holes' lithostratigraphy for the same
  sites.

## EPRP relevance

- **B-005.** The rock-quantity covariate: marine and non-marine column area
  by stage for North America and the other land projects
  ([series](profile/macrostrat_stage_area.tsv)). That is the sampling side
  of "sampled diversity structure". Global comparisons cannot use it.
- **B-007.** Units and gap-bound packages give the architecture. Unit ages
  are interval-derived (above), so the "section and age-support audit with
  independent chronology" gate starts from 515 dated units in North America
  and eODP's own age models. Sequence surfaces are not stage boundaries,
  but Macrostrat's ages put many unit boundaries on stage boundaries.
- **B-008.** Environment classes of units through crises, as exposure
  denominators, in North America (and New Zealand for the Cenozoic).
- **Q-005, Q-023, Q-035, Q-041.** Stratigraphic context for completeness,
  gaps and boundary questions, with the same limits.
- Cannot support: a global rock record, an age model independent of
  interval assignments, Australia.

## Citation and terms

CC BY 4.0. Cite Peters et al. (2018) and the API with its access date (the
API's own citation is in the front matter). For individual units, cite the
sources in `defs__sources.json` and `defs__refs.json`.

## Verification log

- 2026-10-25 (Claude, Opus 5.5):
  - *checked*: snapshotted the API by project and status (85 requests); units
    per project equal the stats route's counts; sha256 recorded and
    verified;
  - *checked*: profiled every project ([profile](profile/macrostrat_profile.tsv)):
    columns, units, sections, age support, environments, PBDB links against
    our public PBDB snapshot of 2026-10-23, measurements; the stage-area
    series;
  - *source claim*: the licence, citation, API version and funding (API
    meta); project descriptions (defs/projects);
  - *recall*: the 2018 paper's details beyond its DOI.
