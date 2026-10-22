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
    - {type: website, url: "http://nsb-mfn-berlin.de", state: "no connection from WSL or deep-server", checked: 2026-10-22}
    - {type: postgresql, url: "guest login on the MfN server (Renaudie et al. 2020, p. 25)", state: "not tested; depends on the live server", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: every snapshot ships a PostgreSQL dump, an SQLite copy and denormalised tables
mirror:
  path: deep-server:/data/paleodata/nsb
  policy: all 372 versions (22.5 GB); latest and year-end checkpoints first
  state: latest complete 2026-10-22; remaining versions downloading
lineage:
  upstream: [DSDP Initial Reports range charts (DSDP CD-ROM), ODP and IODP reports and Janus core tables, published range charts, Chronos Neptune (2002-2008)]
  downstream: [Triton (108,339 of 541,846 presence records), Mikrotax occurrence summaries, PBDB query link (Chronos era)]
eprp_questions: [Q-007, Q-016]
citation:
  - "Renaudie, J., Lazarus, D. B. & Diver, P. (2020). NSB (Neptune Sandbox Berlin): an expanded and improved database of marine planktonic microfossil data and deep-sea stratigraphy. Palaeontologia Electronica 23(1): a11. doi:10.26879/1032"
  - "Renaudie, J., Lazarus, D. & Diver, P. Archive of Neptune (NSB) database backups, version <date>. Zenodo. doi:10.5281/zenodo.<record> (cite the version record used)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); paper and ecosystem reads by Claude Sonnet subagents
  reviewed: no
---

# Neptune Sandbox Berlin (NSB)

## Summary

NSB is the main occurrence database for Cenozoic and Cretaceous marine
plankton microfossils from deep-sea drilling. It holds about 784,000 records
of nannofossils, foraminifera, radiolarians, diatoms and dinocysts in about
62,000 samples from 506 DSDP, ODP and IODP holes. Every sample is dated by its
hole's revisable age-depth model, not by the original author's zone
assignment. Reach for it for species-level diversity, origination and
extinction, range and biogeography studies of open-ocean plankton, or to tie
ocean-drilling stratigraphy to a common time scale. Its 372 dated full-database
snapshots on Zenodo make any analysis exactly reproducible, a property PBDB
lacks. The live service is unreachable and the last snapshot is from June 2023,
so treat it as frozen.

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

`DN` is not defined in the paper; its genera (*Impagidinium*, *Spiniferites*,
*Operculodinium*) identify dinocysts. Silicoflagellates and ebridians are filed
under radiolarians with status `I`.

**Time.** Sample ages run from 0 to 151.08 Ma.

| Interval | Occurrences |
| --- | ---: |
| Pleistocene–Holocene | 127,772 |
| Pliocene | 90,430 |
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

**Space.** Pacific 333,169 occurrences, Atlantic 299,438, Indian 124,976,
Southern Ocean (`ANT`) 16,604, Mediterranean 9,800. By present absolute
latitude: 0–30° 367,341, 30–60° 385,644, above 60° 31,002. High latitudes are
thin except for diatoms and radiolarians.

**Drilling programmes.** Of the 506 holes with samples, 171 are DSDP (Legs
3–95), 283 ODP (Legs 104–208) and 52 IODP (Expeditions 303–342). Occurrences: DSDP 307,035, ODP 402,514, IODP 74,438. The hole
table lists 3,818 holes, most without samples.

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

Poor and very poor models date 19.5% of dated samples, matching the paper's
19.3%. 5,181 samples (8.4%) have no age.

**Sources.** 976 datasets with 396 distinct citations. 8,031 samples (13.0%)
and 105,906 occurrences (13.5%) have no recorded source dataset. That is down
from about 22% in 2019 (paper, p. 13).

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
- **2017–2023.** About 120 age models were revised (80 by Lazarus, nearly 40
  Cretaceous models by J. Young), quality ratings were assigned, and data
  sources were back-filled. The project has been unfunded and voluntary since
  2015. Snapshot counts show little growth after 2019: 768,057 occurrences in
  the paper (submitted September 2019) against 783,987 in June 2023 (+2.1%).
  The last age-model revision in the database is dated 2023-01-21.

The 2014-08-16 snapshot (500,756 occurrences, 42,029 samples, 11,777 names in
the old taxonomy table) matches the paper's pre-renovation state (500,622,
42,034, 11,767) to within 0.03%. The Zenodo series therefore spans the whole
Berlin web era.

**Downstream.** Triton (Fenton et al. 2021; 2023 update) takes 108,339 of its
541,846 presence records (20%) directly from Neptune. Mikrotax draws
occurrence summaries from NSB by SQL. See Overlap.

## Structure

Each SQLite snapshot holds the production tables without foreign keys. In the
2023 snapshot there are 21 tables; the key relations, from the paper's
Figure 2 and the NSBcompanion R code, are:

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
  *Chikyu*, M = IODP mission-specific platforms (inferred from leg ranges).
- `taxon_qualifier` (2023 counts): `?` 1,083; `abs` 1,027; `re` 588; `cf` 428;
  `frg` 411; `aff` 69; `mis` 56; `pr` 39; `gr` 17; `rw` 1. The paper defines
  only `?`, `re` and `frg`. `abs` rows all have abundance 0 and are recorded
  absences.
- `sample_status`: `w` 705 and `c` 358 samples. The portal treats both as
  problematic (reworked or disturbed intervals); the letters are not defined
  anywhere we have found.
- `taxon_abundance` mixes semi-quantitative categories (83% of rows; R, F, C,
  P, T, X, A, +, ...) with counts and percentages. Scales differ between
  studies.
- Ages are point estimates on GTS2012. There is no per-sample age error;
  uncertainty is only the model-level quality class.

The denormalised tables in each snapshot are tab-separated with quoted
headers: `occurrences.csv` (all rows), `filtered_occurrences.csv` and
`agemodels.csv`. Their zip timestamps show they were generated in October 2023
for every snapshot, so their filtering reflects 2023 code applied to old data.

## Access

**Mirror (preferred inside EPRP).** On `deep-server`:

```text
/data/paleodata/nsb/raw/<version>_<record>/nsb_sqlite.zip, nsb_postgresql.zip,
    denormalized_tables.zip, MANIFEST.json
/data/paleodata/nsb/derived/2023-06-05_10063218/nsb.sqlite    unzipped latest
/data/paleodata/nsb/versions.tsv                               all 372 versions
```

The full version index is also in [zenodo-versions.tsv](zenodo-versions.tsv).

**Directly from Zenodo.** No account needed. For a given version record:

```bash
curl -sL -o nsb_sqlite.zip https://zenodo.org/api/records/10063218/files/nsb_sqlite.zip/content
```

`resources/tools/zenodo_mirror.py 10063218 <dest> --only <version_dir>`
fetches one version with checksum verification.

**Analysis-ready occurrences.** [occurrences.sql](occurrences.sql) resolves
synonymy recursively, applies the portal's default filters and drops undated
samples. On the 2023-06-05 snapshot it returns **629,662** occurrences in
54,678 samples from 430 holes, 3,824 resolved taxa, in 7 s:

```python
import sqlite3
con = sqlite3.connect("file:/data/paleodata/nsb/derived/2023-06-05_10063218/nsb.sqlite?mode=ro", uri=True)
rows = con.execute(open("resources/sources/nsb/occurrences.sql").read()).fetchall()
```

Deduplicate on `(sample_id, resolved_taxon_id)` before presence analyses (see
Pitfalls). The R package NSBcompanion (github.com/plannapus/NSBcompanion)
implements the same filters but expects a PostgreSQL connection, so it needs
the dump restored locally while the live server is down.

**Live service.** The website and its SQL guest login did not respond on
2026-10-22. No API has ever existed.

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
- **Documented lineage.** A 28-page description paper and source citations
  for 87% of samples.
- **Small and fast.** The whole database is a 21 MB zip; full scans take
  seconds.

## Weaknesses and pitfalls

1. **The full occurrence file includes absences.** 1,027 rows with qualifier
   `abs` and abundance 0 sit among the presences. `occurrences.csv` drops the
   qualifier column, so they can be recognised only by the zero abundance.
   Use the filtered file, the SQL recipe, or exclude them explicitly.
2. **`filtered_occurrences.csv` keeps undated samples.** It reproduces the
   portal's defaults exactly, with one exception: the 45,416 undated
   occurrences the portal would drop are retained. We verified this
   record-by-record against the database, with no unexplained rows: 675,078
   filtered rows = 629,662 that pass every default + 45,416 undated.
3. **Synonym resolution is recursive and lossy.** 1,014 names point to another
   synonym, so a single lookup is wrong. Resolution renames 28.6% of filtered
   occurrences, and creates 13,868 duplicate taxon records within samples
   (2.2%). It also leads 1,533 filtered occurrences to names whose status is
   `U`, `Q` or `G`. The portal filters on the published name's status, before
   resolution. Synonymy is global, not per publication (paper, p. 5).
4. **Ages change between versions.** Ages are recomputed whenever a hole's
   age model is revised. Between the 2014-08-16 and 2023-06-05 snapshots,
   of 41,314 samples present in both, 28,397 (69%) changed age by more than
   0.01 Myr, 11,671 (28%) by more than 0.5 Myr, 7,178 (17%) by more than
   1 Myr and 948 (2.3%) by more than 5 Myr; 2,931 gained or lost an age
   ([drift.tsv](profile/drift.tsv)). Some of this may reflect the 2015
   adoption of GTS2012 as the default scale (inference); the year-end
   snapshots will separate scale changes from model revisions. Pin a snapshot; never mix extracts from different versions or
   from the defunct Chronos instance.
5. **Age quality labels were messy before the renovation.** In the 2014-08-16
   snapshot the quality field holds about 30 free-text variants ("good",
   "quite poor", "v.2 G", "very bad!"). The 2023 snapshot uses only the six
   classes. Older snapshots need normalising before quality filtering.
6. **Abundances do not pool.** Semi-quantitative categories and counts from
   different studies use different scales.
7. **Selective, presence-only recording.** Authors often recorded only marker
   species, and blank cells are not absences. Sieve sizes changed over time,
   cutting small radiolarians from older studies (paper, p. 19). NSB covers
   specialist-selected holes, not all drilled material.
8. **Uneven coverage.** Southern Ocean (2%) and high-latitude (above 60°,
   4%) material is thin; Cretaceous data are mostly nannofossils and
   foraminifera.
9. **Frozen and unfunded.** No updates since June 2023 and no reachable
   service. The newest drilling material is IODP Expedition 342 (2012);
   only 52 IODP holes are included.
10. **Palaeocoordinates are single-model.** Seton et al. (2012) rotations
    from present hole positions; 7,221 samples (11.7%) have none.
11. **Undocumented codes.** Taxon status `O`, sample status `c` and `w`,
    and qualifiers `abs`, `mis`, `pr`, `gr`, `rw` are not defined in the
    paper. The paper's own counts are internally inconsistent in places, for
    example 767,600 against 768,057 occurrences.

## Overlap with other sources

- **Triton (planktonic foraminifera).** Measured at site level, 2023 NSB
  against the 2023 Triton update (`trim == "inc"`). 181 of NSB's 203
  foraminifera sites (89%), carrying 95% of its foraminifera occurrences, also
  appear in Triton. All 164 sites where Triton credits Neptune are in NSB.
  Triton adds 405 drill sites absent from NSB foraminifera (207,179 records),
  plus non-drilling cores. For foraminifera Triton largely contains NSB and
  extends it, on GTS2020 with its own taxonomy. Never pool the two without
  deduplication. Record-level identity was not tested.
- **PBDB.** No bulk ingestion is documented; the link was a query page from
  the Chronos era. Not measured.
- **Mikrotax.** Shares the taxonomic lineage (the IODP Taxonomic Name List)
  and shows NSB occurrence summaries.
- **Nannofossils, radiolarians, diatoms and dinocysts** have no comparable
  open compilation we know of. For these groups NSB is the primary source.

## EPRP relevance

- **Q-016** (range-based risk criteria and geological extinction) names NSB
  for foraminifera and other plankton ranges. Pitfalls 3–5 and 8 bear
  directly on range estimates.
- **Q-007** (biotic legacy under an environmental path) lists Triton and NSB
  species data at fixed drilling sites.
- Good for: species-level origination and extinction in four plankton groups,
  geographic range dynamics, cross-group contrasts on shared holes.
- Not good for: abundance-based ecology without per-study recoding;
  analyses needing per-sample age uncertainty; post-2015 IODP material;
  shelf or land sections.

## Citation and terms

Cite the paper and the specific Zenodo version record used (front matter).
The Zenodo snapshots are CC-BY 4.0. The paper itself is CC BY-NC-SA 4.0; the
website footer in 2019 screenshots showed CC BY-SA. Neither applies to the
deposited snapshots, which carry their own licence.

## Verification log

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | Zenodo API: 372 versions under concept 8238613, all CC-BY-4.0, 22.5 GB, uploaded October–November 2023 | checked |
| 2026-10-22 | `nsb.mfn-berlin.de` and `nsb-mfn-berlin.de`: no connection from WSL | checked |
| 2026-10-22 | Mirrored 2023-06-05 and 2014-08-16 with md5 verification; sha256 in each MANIFEST | checked |
| 2026-10-22 | Profiled both snapshots; counts above from `profile.py` | checked |
| 2026-10-22 | `filtered_occurrences.csv` = portal defaults minus the age filter, record-by-record, 0 unexplained rows | checked |
| 2026-10-22 | `occurrences.sql` returns 629,662 rows, equal to the predicted portal-default set | checked |
| 2026-10-22 | 2014 snapshot matches the paper's pre-renovation counts; 2019 paper counts vs 2023 snapshot | checked |
| 2026-10-22 | Sample-age drift 2014-08-16 → 2023-06-05 | checked |
| 2026-10-22 | Triton source composition and site-level overlap, from EPRP's held Triton copy | checked |
| 2026-10-22 | History, schema relations, filter definitions, quality classes, limitations | source claim (Renaudie et al. 2020, read in full) |
| 2026-10-22 | `DN` = dinocysts; `program` codes C, M, R | checked (inferred from genera and leg ranges) |
