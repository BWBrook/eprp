---
id: nsb
name: Neptune Sandbox Berlin (NSB)
kind: database
status: frozen
last_update: 2023-06-05
scope:
  taxa: [calcareous nannofossils, planktonic foraminifera, radiolarians, diatoms, dinoflagellate cysts]
  time: Late Jurassic to Recent; occurrence ages 0-151.08 Ma, mostly Cenozoic
  space: global ocean; DSDP, ODP and IODP drill holes only
  record_unit: one taxon name reported in one core sample by one study
size:
  as_of: 2023-06-05 snapshot (zenodo.10063218)
  occurrences: 783987
  samples: 61862
  holes_with_samples: 506
  taxon_names: 19170
  valid_species_names: 6960
access:
  tier: open
  licence: CC-BY-4.0 (Zenodo snapshots)
  routes:
    - {type: zenodo-snapshots, url: "https://doi.org/10.5281/zenodo.8238613", state: "372 versions, 2014-08-16 to 2023-06-05", checked: 2026-10-22}
    - {type: r-package, url: "chronosphere::fetch('neptune'); NSBcompanion 3.1 (github.com/plannapus/NSBcompanion)", state: "serves the Zenodo snapshots; not run here", checked: 2026-10-22}
    - {type: gbif, url: "https://doi.org/10.15468/bvu6a8", state: "frozen pre-2015 copy, 500,808 records, no ages", checked: 2026-10-22}
    - {type: website, url: "https://nsb.mfn-berlin.de", state: "offline since the October 2023 MfN cyberattack; host no longer resolves", checked: 2026-10-22}
    - {type: postgresql, url: "guest login on the MfN server", state: "offline with the website", checked: 2026-10-22}
  api: "none live; a beta age-model API (2022) went offline with the server"
versioning:
  replay: exact
  notes: "every snapshot ships the full PostgreSQL dump (35 tables in 2023), a 21-table SQLite subset and denormalised tables"
mirror:
  path: deep-server:/data/paleodata/nsb
  policy: "latest plus the 12 older snapshots the profile depends on (year-ends and the paper-era 2019 pair); others on demand from Zenodo"
  state: "13 versions, 768 MB, complete 2026-10-22"
lineage:
  upstream:
    - DSDP Initial Reports range charts (DSDP CD-ROM)
    - ODP and IODP reports and Janus core tables
    - published range charts
    - Chronos Neptune (2002-2008)
  downstream:
    - "Triton: 108,339 of 541,846 presence records"
    - "BioDeepTime: 609 time series"
    - "Mikrotax (Nannotax, pforams): occurrence plots"
    - "Uneptune: Cretaceous nannofossils, partly converted from Neptune"
    - GBDB feed
    - WoRMS Polycystina names
    - "GBIF: pre-2015 copy"
eprp_questions: [Q-007, Q-016]
citation:
  - "Renaudie, J., Lazarus, D. B. & Diver, P. (2020). NSB (Neptune Sandbox Berlin): an expanded and improved database of marine planktonic microfossil data and deep-sea stratigraphy. Palaeontologia Electronica 23(1): a11. doi:10.26879/1032"
  - "Renaudie, J., Lazarus, D. & Diver, P. Archive of Neptune (NSB) database backups, version <date>. Zenodo. doi:10.5281/zenodo.<record> (cite the version record used)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); paper and ecosystem reads by Claude Sonnet subagents
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# Neptune Sandbox Berlin (NSB)

## Summary

NSB is the main occurrence database for Cenozoic and Cretaceous marine
plankton microfossils from deep-sea drilling. It holds about 784,000 records
of nannofossils, foraminifera, radiolarians, diatoms and dinocysts in about
62,000 samples from 506 DSDP, ODP and IODP holes. Samples are dated by their
hole's revisable age-depth model, not by the original author's zone
assignment; 8.4% have no age, and in the final snapshot 56 holes carry stored
ages that lag their current model (Pitfall 5). Reach for it for species-level diversity, origination and
extinction, range and biogeography studies of open-ocean plankton, or to tie
ocean-drilling stratigraphy to a common time scale. Its 372 dated full-database
snapshots on Zenodo make any analysis exactly reproducible, a property PBDB
lacks. The live service has been offline since a cyberattack on the Museum für
Naturkunde Berlin in October 2023, and nobody at the museum maintains it any
more. The June 2023 snapshot is the de facto final version; treat NSB as
frozen.

## Contents

Counts are our own, from the 2023-06-05 snapshot ([profile](profile/)).

| Fossil group (code) | Occurrences | Samples | Share |
| --- | ---: | ---: | ---: |
| Calcareous nannofossils (N) | 312,985 | 24,301 | 40% |
| Planktonic foraminifera (F) | 176,517 | 16,023 | 23% |
| Radiolarians (R) | 146,883 | 11,792 | 19% |
| Diatoms (D) | 139,073 | 9,127 | 18% |
| Dinoflagellate cysts (DN) | 8,529 | 619 | 1% |
| **All** | **783,987** | **61,862** | |

`DN` is not defined in the paper; NSBcompanion lists it as a fossil group, and
its genera (*Impagidinium*, *Spiniferites*, *Operculodinium*) identify
dinocysts. Silicoflagellates and ebridians are filed under radiolarians with
status `I`. 724 samples have no occurrence rows, and 539 occurrences sit in a
sample whose group differs from the taxon's (402 radiolarian and 137 dinocyst
taxa in diatom samples).

**Time.** Sample ages run from 0 to 151.08 Ma. Intervals use GTS2012
boundaries, the scale NSB reports.

| Interval | Occurrences |
| --- | ---: |
| Pleistocene–Holocene | 128,244 |
| Pliocene | 89,958 |
| Miocene | 214,498 |
| Oligocene | 64,867 |
| Eocene | 109,354 |
| Paleocene | 28,019 |
| Late Cretaceous | 65,459 |
| Early Cretaceous | 26,835 |
| Pre-Cretaceous | 913 |
| No age | 55,840 |

Cretaceous records are almost all nannofossils and foraminifera. Radiolarian
and diatom records are essentially Cenozoic.

**Space.** By `ocean_code`: Pacific 333,169 occurrences, Atlantic 299,438,
Indian 124,976, Southern (`ANT`, 12 holes) 16,604, Mediterranean 9,800. The
code is not a latitude filter: 70,270 occurrences (9.0%) lie south of 50°S,
mostly in holes coded ATL or IND. By present absolute latitude: 0–30° 367,341,
30–60° 385,644, above 60° 31,002 (4.0%; diatoms 7.8% of theirs, radiolarians
4.6%, foraminifera 3.1%, nannofossils 2.5%).

**Drilling programmes.** Of the 506 holes with samples, 171 are DSDP (Legs
3–95), 283 ODP (Legs 104–208) and 52 IODP, from only five expeditions (303,
306, 320, 321, 342). Occurrences: DSDP 307,035, ODP 402,514, IODP 74,438. The
hole table lists 3,818 holes, including IODP expeditions to 396, most without
samples.

**Taxonomy.** 19,170 taxon names, of which 6,960 are valid species (`V`),
5,347 synonyms (`S`), 3,665 open nomenclature with a genus (`G`), 1,610
questionable identifications (`Q`), 852 status undetermined (`U`), 479 valid
subspecific groups (`B`), 164 invalid in the group (`I`), 60 higher taxa (`H`)
and 33 with status `O`, which the paper does not define.

**Chronology.** 794 age-model revisions for 484 holes; 483 are current. 449 of
the 506 sampled holes have a current model. Current-model quality (subjective,
from scatter about the line of correlation; Renaudie et al. 2020, p. 14):

| Quality | Models | Dated samples | Approx. median sample-age error (paper) |
| --- | ---: | ---: | --- |
| E (excellent) | 56 | 5,698 | 0.2–0.5 Myr or less |
| VG (very good) | 82 | 9,185 | 0.2–0.5 Myr |
| G (good) | 108 | 13,696 | ~0.5 Myr |
| M (moderately good) | 126 | 17,030 | ~0.5 Myr |
| P (poor) | 86 | 8,877 | ~1 Myr or more |
| VP (very poor) | 25 | 2,195 | ~1 Myr or more |

Poor and very poor models date 19.5% of dated samples in 2023. The paper's
19.3% has an unstated denominator; the independent review found 17.7% in the
2019-08-30 snapshot by our definition. 5,181 samples (8.4%) have no age; 57
sampled holes have no model at all.

Stored sample ages are a cached product of the age models, and in the final
snapshot the cache is stale for part of the database: see Pitfall 5 and
[age_check.py](age_check.py).

**Sources.** 976 datasets with 396 distinct citations. Two definitions give
different coverage:

| Definition | Samples | Occurrences |
| --- | ---: | ---: |
| `dataset_id` recorded | 53,831 (87.0%) | 678,081 (86.5%) |
| non-empty source citation (the paper's definition) | 49,496 (80.0%) | 615,015 (78.4%) |

On the paper's definition, coverage barely moved after the paper: 77.9% of
occurrences in the 2019-08-30 snapshot, 78.4% in 2023. 4,335 samples belong to
77 datasets with a blank citation.

**Other content.** Stratigraphic events (28,976 observed, 5,080 defined, 5,094
calibrations), GPTS tables for six time scales, palaeocoordinates every 0.5 Myr
per hole (582,770 rows, Seton et al. 2012 rotations only), Longhurst provinces,
and core depth tables.

## Provenance and lineage

Source: Renaudie et al. (2020), read in full, unless marked otherwise.

- **1989–1995, Zürich.** David Lazarus's group at ETH Zürich (H. Thierstein's
  lab) built Neptune from DSDP range charts. It held Neogene data only; the
  DSDP CD-ROM was the main source. Species is the only taxonomic unit, and
  names were stored as published with links to standard names. By 1994 it held
  about 300,000 occurrences from over 100 sections.
- **1996–2001.** C. Spencer-Cervato added Paleogene and ODP data (over 160
  sections); M. Knappertsbusch built age models.
- **2002–2008, Chronos (Iowa, NSF).** Ported to PostgreSQL; carbonate-group
  holes added, reaching about 480,000 occurrences. A query link from PBDB
  dates from 2006. Some Chronos-added age models were displaced by up to
  several million years, which probably explains the erroneous nannofossil
  ages reported by Lloyd et al. (2012). Chronos funding ended in 2008, and its
  copy had effectively disappeared by about 2018.
- **2008–2010.** The IODP Taxonomic Name List harmonised names for all groups
  and became NSB's taxonomic backbone.
- **2009–2016, Berlin.** Extracted from Chronos into a scientist-maintained
  "sandbox" at the Museum für Naturkunde Berlin. With EarthTime-EU funding,
  J. Renaudie added the stratigraphic layer, the website (2014), GTS2012 as the
  default scale and about 150 new or revised age models (2015), and
  palaeocoordinates (2016).
- **2017–2023.** The paper reports about 120 models revised in 2017–18 (80
  by Lazarus, nearly 40 Cretaceous models by J. Young) and quality ratings
  assigned. The 2023 database holds 318 age-model revisions dated 2017 or
  later (275 holes), 189 of them after September 2019; 167 current models date
  from 2020–2023, the last on 2023-01-21. The project has been unfunded and
  voluntary since 2015. Occurrence counts stalled in October 2019
  ([version_counts.tsv](profile/version_counts.tsv)): 768,057 on 2019-08-30
  (the paper's figure exactly), 780,844 on 2019-10-07, 783,987 on 2023-06-05
  (+0.4% after October 2019). Ages kept moving until the end. The website's
  last changelog entry (2022-03-08) added a Triton query page and a beta
  age-model API.
- **October 2023 onwards.** A cyberattack took the museum's servers offline
  (MfN press release, 20 October 2023). The Wayback Machine's last good capture
  of the site is 2023-09-25; by January 2024 it returned HTTP 503. Renaudie
  uploaded the 372 snapshots to Zenodo in October–November 2023. In January
  2025 he wrote that Lazarus retired in 2021, that he himself had left in
  early 2023, and that the database had been handed to MARUM (Bremen) to
  bring back online. No relaunch has appeared as of October 2026. Dowding et
  al. (2026, *Nat. Ecol. Evol.*, doi:10.1038/s41559-026-02985-8) cite NSB's
  loss as a case of under-funded single-maintainer infrastructure.

**Reconciliation with the paper.** The 2019-08-30 snapshot reproduces the
paper's current counts exactly: 768,057 occurrences, 61,139 samples, 18,915
names and 65,308 undated occurrences. The 2014-12-12 snapshot has exactly the
paper's pre-renovation 500,622 occurrences, and both 2014 snapshots have its
289 holes with age models. The Zenodo series therefore spans the whole Berlin
web era, and these matches validate both the mirror and our profiler.

**Downstream.** Triton (Fenton et al. 2021; 2023 update) takes 108,339 of its
541,846 presence records (20%) directly from Neptune; its paper calls Neptune
"the core of our dataset". BioDeepTime (Smith et al. 2023) took 609 NSB time
series (31,634 samples) queried in October 2022. Nannotax and pforams@mikrotax
plot NSB occurrences per species. NSB fed GBDB and supplied WoRMS's Polycystina
names. Uneptune (Zhang et al. 2026, *J. Micropalaeontol.* 45: 147), a Cretaceous
nannofossil database three times the size of Neptune's Cretaceous content,
was built partly from converted Neptune data. A GBIF dataset (MfN, 2013–2016)
holds a frozen pre-2015 copy. See Overlap.

## Structure

The PostgreSQL dump is the full database: 35 tables in 2023. The SQLite copy
is a 21-table subset without foreign keys, and is what our profile and recipe
use. Tables only in the dump include `neptune_taxonomy_synonym` (the legacy
11,777-name table), `neptune_nsb_taxonomy_synonym`, hole-level taxon summaries,
sedimentation-rate tables and `temp_tritcomp` (512,941 rows), a Triton-format
compilation that carries NSB `sample_id`s and allows record-level linking to
Triton (see Overlap). The key relations, from the paper's Figure 2 and the
NSBcompanion R code, are:

```text
neptune_sample_taxa (sample_id, taxon_id, taxon_qualifier, taxon_abundance)   one row per occurrence
  sample_id  -> neptune_sample.sample_id
  taxon_id   -> neptune_taxonomy.taxon_id        name as published
neptune_sample (sample_id, hole_id, core, section_number, sect_interval_top,
                sample_depth_mbsf, sample_age_ma, paleo_latitude, paleo_longitude,
                fossil_group, sample_group_abundance, sample_preservation,
                sample_status, dataset_id)
  hole_id    -> neptune_hole_summary.hole_id     "Leg_SiteHole", e.g. 120_747A
  dataset_id -> neptune_sod_off.dataset_id       null for 13% of samples
neptune_taxonomy (taxon_id, taxon_status, genus, species, ..., taxon_synon_to)
  taxon_synon_to -> neptune_taxonomy.taxon_id    recursive; resolve to the end
neptune_hole_summary (hole_id, site_hole, leg, site, hole, latitude, longitude,
                      ocean_code, program, longhurst_code, ...)
neptune_age_model (site_hole, revision_no, depth_mbsf, age_ma)               tie points
neptune_age_model_history (site_hole, revision_no, age_quality, current_flag) one current per hole
  join on site_hole ("SiteHole", e.g. 747A) and current_flag = 'Y'
```

Codes worth knowing:

- `program`: D = DSDP, O = ODP, R = IODP *JOIDES Resolution*, C = IODP
  *Chikyu*, M = IODP mission-specific platforms (inferred from leg numbers
  and site-name prefixes).
- `taxon_qualifier` (2023 counts): `?` 1,083; `abs` 1,027; `re` 588; `cf` 428;
  `frg` 411; `aff` 69; `mis` 56; `pr` 39; `gr` 17; `rw` 1. The paper defines
  only `?`, `re` and `frg`. All 1,027 `abs` rows have abundance `0` or `0.`,
  and no other qualifier has a zero abundance; we infer they are recorded
  absences. They sit in 213 samples, 211 of which also hold presences.
- `sample_status`: `w` 705 and `c` 358 samples. The portal treats both as
  problematic (reworked or disturbed intervals); the letters are not defined
  anywhere we have found.
- `taxon_abundance` mixes semi-quantitative categories (83% of rows; R, F, C,
  P, T, X, A, +, ...) with counts and percentages. Scales differ between
  studies.
- Ages are point estimates on GTS2012. There is no per-sample age error;
  uncertainty is only the model-level quality class.
- `site_hole` is not unique in `neptune_hole_summary`: 15 values map to
  several `hole_id`s (504B to eight legs). No two sampled holes share one in
  2023, but check before joining age models to holes in other snapshots.

The denormalised tables in each snapshot are tab-separated with quoted
headers: `occurrences.csv` (all rows), `filtered_occurrences.csv` and
`agemodels.csv`. Zip timestamps in all nine snapshots checked (2014–2023)
date them to 13–15 October 2023, so their filtering reflects 2023 code applied
to old data.

## Access

**Mirror (preferred inside EPRP).** On `deep-server`:

```text
/data/paleodata/nsb/raw/<version>_<record>/nsb_sqlite.zip, nsb_postgresql.zip,
    denormalized_tables.zip, MANIFEST.json
/data/paleodata/nsb/derived/2023-06-05_10063218/nsb.sqlite    unzipped latest
/data/paleodata/nsb/versions.tsv                               index of all 372 versions
                                                (13 mirrored; see front matter)
```

The full version index is also in [zenodo-versions.tsv](zenodo-versions.tsv).

**Directly from Zenodo.** No account needed. For a given version record:

```bash
curl -sL -o nsb_sqlite.zip https://zenodo.org/api/records/10063218/files/nsb_sqlite.zip/content
```

`python3 resources/tools/data_mirror.py zenodo 10063218 <dest> --only <version_dir>`
fetches any version with checksum verification, and `--latest` the newest;
`data_mirror.py verify <dest>` re-hashes a mirror against its manifests.

**Analysis-ready occurrences.** [occurrences.sql](occurrences.sql) resolves
synonymy recursively, applies the default filters and drops undated samples.
On the 2023-06-05 snapshot it returns **629,662** occurrences in 54,678
samples from 430 holes, 3,824 resolved taxa, in 7 s. `nsb_profile.py` checks it
on every run: its keys equal the dated rows of the provider's filtered file,
and its resolved taxon equals the provider's on every row.

```python
import sqlite3
con = sqlite3.connect("file:/data/paleodata/nsb/derived/2023-06-05_10063218/nsb.sqlite?mode=ro", uri=True)
rows = con.execute(open("resources/sources/nsb/occurrences.sql").read()).fetchall()
```

Deduplicate on `(sample_id, resolved_taxon_id)` before presence analyses (see
Pitfalls). For the final snapshot, join ages from
`/data/paleodata/nsb/derived/2023-06-05_10063218/sample_ages_recomputed.tsv`
(written by [age_check.py](age_check.py)) instead of the stored
`sample_age_ma`, or exclude the 56 affected holes (Pitfall 5).

**R.** `chronosphere::fetch("neptune")` serves the Zenodo snapshots by version
(series `sqlite`, `occs`, `filtered`, `agemodels`). NSBcompanion 3.1 (May
2025, MIT, doi:10.5281/zenodo.3408197) builds on it: `getNeptuneData()`
applies the portal filters, and there are helpers for age models, synonymy,
Pacman trimming, palaeocoordinates and age-scale conversion. Neither was run
here.

**GBIF.** Dataset doi:10.15468/bvu6a8 holds 500,808 records, a frozen copy
matching the pre-2015 database, without ages or stratigraphic context. Do not
use it as NSB.

**Live service.** Offline since October 2023: the website, the PostgreSQL
guest login and the beta age-model API (2022). On 2026-10-22 the host names no
longer resolved.

## Strengths

- **Exact reproducibility.** 372 dated full-database snapshots under CC-BY 4.0,
  in three formats. Any published NSB analysis can be re-run against the state
  it used, and drift between versions can be measured.
- **Uniform, revisable chronology.** Ages come from curated age-depth models
  on one time scale, with a quality class for every model.
- **Taxonomic standardisation without loss.** Published names are kept, with
  expert-vetted synonymy pointers to the IODP Taxonomic Name List backbone.
- **Breadth across plankton groups.** Four major groups plus dinocysts from
  one set of drill holes on one chronology, so cross-group comparisons share
  sampling frame and age models.
- **Documented lineage and heavy use.** A 28-page description paper, source
  citations for 80% of samples, and 149 publications on the maintainers' list
  of works using or citing it, including diversity studies of diatoms
  (Lazarus et al. 2014), radiolarians (Trubovitz et al. 2020,
  doi:10.1038/s41467-020-18879-7) and four plankton groups (Jamson et al. 2022,
  doi:10.1111/pala.12615), and community-novelty work (Pandolfi et al. 2020,
  doi:10.1126/science.abb3996). Its age models underpin hiatus and
  sedimentation compilations (Dutkiewicz et al. 2024,
  doi:10.1038/s41467-024-46171-5).
- **Small and fast.** The SQLite copy is a 21 MB zip; full scans take
  seconds.

## Weaknesses and pitfalls

1. **The full occurrence file includes absences.** 1,027 rows with qualifier
   `abs` and abundance 0 sit among the presences. `occurrences.csv` drops the
   qualifier column, so they can be recognised only by the zero abundance.
   Use the filtered file, the SQL recipe, or exclude them explicitly.
2. **`filtered_occurrences.csv` keeps undated samples.** It equals the
   NSBcompanion `getNeptuneData` defaults exactly (status, qualifier and
   sample-status filters), which keep undated samples; the portal dropped them
   (paper, p. 9). We verified this record by record against the database,
   with no unexplained rows: 675,078 filtered rows = 629,662 that pass every
   filter + 45,416 undated.
3. **Synonym resolution is recursive and lossy.** 1,014 names point to another
   synonym, so a single lookup is wrong. Resolution renames 28.6% of filtered
   occurrences, and creates 13,868 duplicate taxon records within samples
   (2.2%). It also leads 1,533 filtered occurrences to names whose status is
   `U`, `Q` or `G`. The portal filters on the published name's status, before
   resolution. Synonymy is global, not per publication (paper, p. 5).
4. **Ages change between versions.** Of 35,415 samples dated in both the
   2014-08-16 and 2023-06-05 snapshots, 80% changed age by more than
   0.01 Myr, 33% by more than 0.5 Myr, 20% (7,178) by more than 1 Myr and
   2.7% by more than 5 Myr; 2,931 more gained or lost an age
   ([drift_2014-08-16_2023-06-05.tsv](profile/drift_2014-08-16_2023-06-05.tsv)).
   The year-end series ([drift.tsv](profile/drift.tsv)) shows three distinct
   causes:
   - *Time-scale change.* Between the 2014-12 and 2015-12 snapshots, which
     bracket the 2015-06-02 remap from Berggren et al. (1995) to GTS2012 (website
     changelog), 25,470 of 35,967 dated samples in holes whose model revision
     number did not change moved by more than 0.01 Myr, and 2,536 by more than
     1 Myr.
   - *Age-model revisions.* In 2016–17, 3,691 samples in revised holes moved
     by more than 1 Myr (835 by more than 5 Myr).
   - *Batch recomputation.* In 2021–22, 12,324 samples in holes with an
     unchanged revision number moved, 1,833 by more than 1 Myr, and 1,133
     samples changed depth.

   Pin a snapshot; never mix extracts from different versions or from the
   defunct Chronos instance.
5. **The final snapshot's stored ages lag its age models.** In three
   intervals (2019–20, 2020–21, 2022–23), holes received new current models
   while no stored sample age changed, so stored ages are recomputed in
   batches, not on revision. Recomputing every 2023-06-05 sample from its
   hole's current tie points ([age_check.py](age_check.py),
   [summary](profile/age_check_2023-06-05.txt)): 52,276 agree within
   0.01 Myr, but 4,111 samples in 56 holes differ (2,475 by 0.01–0.5 Myr, 683
   by 0.5–1 Myr, 953 by more than 1 Myr; worst holes 369A, 911A, 516F, 354).
   469 samples stored as undated can be dated by the current model, and 294
   stored ages fall outside it. The same check on the 2019-08-30 snapshot finds
   only 7 disagreements. Use the recomputed ages, or exclude the 56 holes.
6. **Age quality labels were messy before the renovation.** In the 2014
   snapshots the quality field holds 27 distinct values, 21 of them outside
   the six classes ("good", "quite poor", "v.2 G", "very bad!", single
   letters U, F, X, V). The count of distinct values among current models
   falls to six by 2019 ([version_counts.tsv](profile/version_counts.tsv)); in
   2023 non-current revisions still include `N/A` (10), `U` and `M-G`.
   Normalise older snapshots before quality filtering.
7. **Abundances do not pool.** Semi-quantitative categories and counts from
   different studies use different scales.
8. **Selective, presence-only recording.** Authors often recorded only marker
   species, and blank cells are not absences. Sieve sizes changed over time,
   cutting small radiolarians from older studies (paper, p. 19). NSB covers
   specialist-selected holes, not all drilled material.
9. **Uneven coverage.** Only 9.0% of occurrences lie south of 50°S and 4.0%
   above 60° latitude; `ocean_code = ANT` covers just 12 holes, so filter
   high-latitude material by latitude, not by code. Cretaceous data are mostly
   nannofossils and foraminifera.
10. **Frozen and unmaintained.** No updates since June 2023, no live service,
    and no maintainer at the museum. The newest drilling material is IODP
    Expedition 342 (2012); only 52 IODP holes, from five expeditions, are
    included.
11. **Palaeocoordinates are single-model.** Seton et al. (2012) rotations
    from present hole positions; 7,221 samples (11.7%) have none.
12. **Undocumented codes.** Taxon status `O`, sample status `c` and `w`,
    and qualifiers `abs`, `mis`, `pr`, `gr`, `rw` are not defined in the
    paper. The paper's own counts are internally inconsistent in places, for
    example 767,600 against 768,057 occurrences. Published totals elsewhere
    range from 500,808 to "over one million"; quote counts from a named
    snapshot.

**What the literature says** (source claims; read by our ecosystem scan):

- *Age precision.* Spencer-Cervato (1999, doi:10.26879/99013): about 0.36 Myr
  for Neogene and 0.66 Myr for Paleogene age models; two-thirds of holes hold
  at least one hiatus, which pushes adjacent sample ages too old or too young.
  Lazarus et al. (2014, doi:10.1371/journal.pone.0084857): mismatches are mostly
  under 0.5 Myr but can exceed 1 Myr between low- and high-latitude sites, so
  bins much finer than 0.5–1 Myr add little real resolution.
- *Diversity reconstruction.* Renaudie & Lazarus (2013, doi:10.1666/12016):
  subsampled NSB diversity recovers first-order trends but distorts detail;
  studies relating diversity to palaeoceanographic change need taxonomically
  comprehensive, quantitative data. Lloyd et al. (2012, doi:10.1666/11041.1):
  raw foraminiferal diversity tracks sampling intensity.
- *Outliers.* Lazarus, Weinkauf & Diver (2012, doi:10.1666/10067.1):
  reworking, age-model error and taxonomic uncertainty displace a small
  fraction of occurrences and extend ranges; Pacman trimming is their remedy.
- *Sedimentation bias.* Renaudie & Lazarus (2025, doi:10.5194/bg-22-1929-2025):
  drilled sedimentation rates fall systematically with age, so any metric
  correlated with sedimentation rate inherits an age bias.
- *Coverage.* Zhang et al. (2026): heavy weighting toward the modern;
  Cretaceous content skewed to low latitudes and the Upper Cretaceous.

## Overlap with other sources

- **Triton (planktonic foraminifera).** Measured at site level, 2023 NSB
  against the 2023 Triton update (`trim == "inc"`). 181 of NSB's 203
  foraminifera sites (89%), carrying 95% of its foraminifera occurrences, also
  appear in Triton. All 164 sites where Triton credits Neptune are in NSB.
  Triton adds 405 drill sites absent from NSB foraminifera (207,179 records),
  plus non-drilling cores. At site level, Triton largely contains NSB's
  foraminifera and extends them, on GTS2020 with its own taxonomy. Never pool
  the two without deduplication. At sample level, the independent review
  linked an earlier Triton compilation stored in NSB's PostgreSQL dump
  (`temp_tritcomp`, which carries NSB `sample_id`s): 11,073 of NSB's 16,023
  foraminifera samples (69%) are credited to Neptune there, 80% of those in
  the recipe output. Triton's own figures agree: Neptune supplies 108,339
  non-zero records from 164 sites; NSB's website reported in 2023 that 21.2%
  of Triton occurrences were already in NSB, which is essentially Neptune's
  own share.
- **BioDeepTime** (Zenodo 8154672, CC-BY 4.0) holds 609 NSB time series and
  822 Triton series; NSB foraminifera can therefore enter it twice.
- **GBIF** holds a pre-2015 copy (500,808 records) without ages.
- **PBDB.** No ingestion found: the Chronos-era link was a PBDB-hosted query
  front end, and a name search of PBDB finds no Neptune reference. The
  separate eODP project (doi:10.1029/2022gc010655) loads ocean-drilling
  occurrences into PBDB and Macrostrat from the original reports; overlap with
  NSB there is likely but unmeasured.
- **Mikrotax and Uneptune.** Share the taxonomic lineage (the IODP Taxonomic
  Name List). Uneptune supersedes Neptune for Cretaceous nannofossils.
- **Radiolarians, diatoms, dinocysts and Cenozoic nannofossils** have no
  comparable open compilation we know of. For these NSB is the primary source.

## EPRP relevance

- **Q-016** (range-based risk criteria and geological extinction) names NSB
  for foraminifera and other plankton ranges. Pitfalls 3–6 and 9 bear
  directly on range estimates.
- **Q-007** (biotic legacy under an environmental path) lists Triton and NSB
  species data at fixed drilling sites.
- Good for: species-level origination and extinction in four plankton groups,
  geographic range dynamics, cross-group contrasts on shared holes.
- Not good for: abundance-based ecology without per-study recoding;
  analyses needing per-sample age uncertainty; IODP material after
  Expedition 342; shelf or land sections.

## Citation and terms

Cite the paper, which the website named as the database citation, and the
specific Zenodo version record used (front matter). Renaudie & Lazarus (2025)
cite the 2023-06-05 record, 10.5281/zenodo.10063218. If a derived dataset
leans on NSB through Triton, Triton asks that Neptune be cited too.

The website said NSB "is free to use … The only obligation is to cite the
database properly". Licence labels differ by object:

| Object | Licence |
| --- | --- |
| Zenodo snapshots (the input we use) | CC-BY 4.0 |
| GBIF copy | CC BY 4.0 |
| Website footer badge (2021–2023) | CC BY-SA 4.0, on the site template |
| Description paper | CC BY-NC-SA 4.0 |
| NSBcompanion | MIT |

The deposited snapshots carry their own licence, which governs our mirror.
NSB aggregates 976 contributed datasets; their individual terms were not
assessed. CC-BY attribution implies citing the `source_citation` of datasets
that carry a substantial share of an analysis.

## Verification log

Labels: `checked` (we ran or read it), `source claim` (a provider or paper
says so), `inferred` (our reasoning from checked facts), `recall` (known, not
checked here).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | Zenodo API: 372 versions under concept 8238613, all CC-BY-4.0, 22.5 GB, uploaded October–November 2023 | checked |
| 2026-10-22 | Website hosts do not resolve from WSL or deep-server; `nsb.mfn-berlin.de` is NXDOMAIN, `nsb-mfn-berlin.de` has no address record | checked |
| 2026-10-22 | 13 snapshots mirrored with size and md5 verification; sha256 in each MANIFEST | checked |
| 2026-10-22 | Counts, coverage, codes and drift from `nsb_profile.py` over 13 snapshots ([profile/](profile/)) | checked |
| 2026-10-22 | `filtered_occurrences.csv` = NSBcompanion defaults (keeps undated), record by record, 0 unexplained rows | checked |
| 2026-10-22 | `occurrences.sql` keys = dated filtered-file keys; resolved taxon = provider's on every row | checked |
| 2026-10-22 | 2019-08-30 snapshot = paper's current counts; 2014-12-12 = paper's pre-renovation occurrences; 289 holes with models | checked |
| 2026-10-22 | Stored vs recomputed sample ages, 2019-08-30, 2022-10-06, 2023-06-05 | checked |
| 2026-10-22 | Triton source composition and site-level overlap, from EPRP's held Triton copy | checked |
| 2026-10-22 | PostgreSQL dump has 35 tables incl. `temp_tritcomp`; sample-level Triton link 11,073 of 16,023 | checked (independent review) |
| 2026-10-22 | History, schema relations, filter definitions, quality classes, limitations | source claim (Renaudie et al. 2020, read in full) |
| 2026-10-22 | Undated samples excluded by the portal | source claim (paper, p. 9) |
| 2026-10-22 | Offline since October 2023 cyberattack; last good capture 2023-09-25, 503 by 2024-01-22; MARUM handover | source claim (MfN release; Wayback; Renaudie blog 2023-11-02, 2025-01-31, 2025-05-22; Dowding et al. 2026) |
| 2026-10-22 | chronosphere and NSBcompanion 3.1 serve the Zenodo snapshots | source claim (package code and pages read; not run) |
| 2026-10-22 | GBIF copy: 500,808 records, CC BY 4.0, modified 2016 | checked (GBIF API) |
| 2026-10-22 | Downstream uses, published critiques, website terms and changelog | source claim (papers and archived pages read by the ecosystem scan) |
| 2026-10-22 | GTS2012 remap on 2015-06-02 | source claim (archived website changelog) |
| 2026-10-22 | `abs` rows are recorded absences | inferred (all have zero abundance) |
| 2026-10-22 | `DN` = dinocysts | inferred (genera; listed as a group in NSBcompanion) |
| 2026-10-22 | `program` codes C, M, R | inferred (leg numbers and site-name prefixes) |
| 2026-10-22 | Stored ages recomputed in batches, not on revision | inferred (revisions with no age change; late-2022 bulk change) |
| 2026-10-22 | Entry reviewed adversarially: 5 major findings and 17 minor; all major and the substantive minor ones applied | checked (Claude Sonnet subagent) |
