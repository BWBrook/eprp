---
id: pbdb-chronosphere
name: PBDB dated downloads archived by chronosphere — 1,178 global occurrence tables, November 2019 to October 2026 (one Zenodo concept)
kind: deposit
status: active
last_update: "newest version 20261018 (Zenodo 23468334); versions indexed 2026-10-24"
scope:
  taxa: ["all PBDB occurrences returned by the archive's API call (see Structure)"]
  time: "Ediacaran to Holocene until February 2026; all records since (the call changed to all_records on 2026-02-27)"
  space: "global"
  record_unit: "a PBDB occurrence row (its current identification at download), with collection, location, stratigraphy, environment and reference fields"
size:
  as_of: "2026-10-24"
  versions: 1178
  versions_mirrored_tables: 12
  versions_mirrored_metadata: 1178
  zenodo_bytes_all_versions: 492117258496
access:
  tier: open
  licence: "CC BY 4.0 on every Zenodo version; PBDB's own datainfo header says CC BY in downloads to 2025-02-17 and CC0 from 2025-02-24"
  routes:
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.7808071", state: "concept record: 1,178 versions, each one PBDB download as pbdb_occs.rds, pbdb_parquet.zip, pbdb_csv.zip and metadata.txt (taxon tables too since 2026-07-05)", checked: 2026-10-24}
    - {type: registry, url: "https://github.com/chronosphere-info/chrono_arch_2/raw/main/users/public/master.csv", state: "chronosphere's public registry: 1,171 occurrence versions and 16 taxon versions, each with its Zenodo DOI (resources/software/chronosphere/pbdb_versions.tsv)", checked: 2026-10-23}
    - {type: r-package, url: "https://cran.r-project.org/package=chronosphere", state: "chronosphere::fetch(src='pbdb', ser=..., ver=...) serves the registry's versions; not run here", checked: 2026-10-24}
  api: "Zenodo REST API (versions of record 7808072); chronosphere R client"
versioning:
  replay: partial
  notes: "[Detail withheld pending disclosure to the data custodian.]"
mirror:
  path: deep-server:/data/paleodata/pbdb-chronosphere
  policy: "metadata of every version; the CSV table of a sample of 12 versions (first of each year, each change of API call, one anomalously small archive, the newest); further versions on demand"
  state: "metadata route: 1,178 versions, 1,194 files (1.2 MB); tables route: 12 versions, 25 files (1.76 GB); each version with a manifest; all verify"
lineage:
  upstream:
    - "The Paleobiology Database data service (occs/list, taxa/list), downloaded and archived by Ádám T. Kocsis for the chronosphere project"
  downstream:
    - "chronosphere::fetch('pbdb'); fossilx (Kocsis) post-processing; chronosphere-info/case_pbdbRT (range-through diversity over all versions to September 2020)"
eprp_questions: [Q-045, Q-044, Q-040]
citation:
  - "The Paleobiology Database Community (2019-2026) Denormalized occurrence table of the Paleobiology Database, version YYYYMMDD. Zenodo, concept doi:10.5281/zenodo.7808071 (cite the version DOI used); archived by Á. T. Kocsis for the chronosphere project"
  - "Kocsis, Á. T. & Raja, N. B. (2023) chronosphere: Evolving Earth System Variables. R package version 0.6.1, CRAN, doi:10.32614/CRAN.package.chronosphere"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-24, independent Claude Sonnet subagent; findings applied"
---

# PBDB dated downloads archived by chronosphere

## Summary

Q-045 asks how robust headline macroevolutionary estimates are to future
data, and its strongest form, archived-extract robustness, needs PBDB as it
actually stood on past dates: the identifications, interval assignments and
ages then served. No query of today's PBDB can supply that. chronosphere has
archived it: 1,178 whole-database downloads from 22 November 2019 to 18
October 2026, on 118 to 313 days a year from 2020 to 2024 and weekly in
2026, each a dated, checksummed Zenodo version under CC BY 4.0.

[Detail withheld pending disclosure to the data custodian.]

The 2026 Quaternary share is diluted by the 2025 IODP import. A filtered
version is therefore a *public-data vintage*: that day's records as far as
they are public today. It is not the full input the version's users saw,
and its era composition shifts differently in each vintage.

**The vintages differ in substance.** Take the occurrences public today and
compare each one's then-current values with today's:

| Version | Accepted name changed | Early interval changed | Same intervals, new age (time scale) |
| --- | ---: | ---: | ---: |
| 2019-11-22 | 9.6% | 5.9% | 80.4% |
| 2023-01-04 | 4.9% | 2.7% | 83.0% |
| 2025-01-02 | 2.3% | 1.1% | 48.1% |
| 2026-02-27 | 0.8% | 0.3% | 3.8% |

PBDB re-dated its intervals in at least three steps, each between two
sampled versions (modal `max_ma` of single-interval rows):

| Step | Intervals changed | Examples |
| --- | ---: | --- |
| 2024-01-07 to 2025-01-02 | 462 | Kungurian 279.3 → 283.5; Wuchiapingian 259.9 → 259.51; Priabonian 38.0 → 37.71; Late Pleistocene 0.126 → 0.129 |
| 2025-01-02 to 2026-02-27 | 327 | Kungurian 283.5 → 283.3; Roadian 273.01 → 274.4; Olenekian 251.2 → 249.9; Anisian 247.2 → 246.7; Maastrichtian 72.1 → 72.2 |
| 2026-02-27 to 2026-10-18 | 17 | Wuchiapingian 259.51 → 259.857; Olenekian 249.9 → 250.8; Anisian 246.7 → 247.0; Middle Oxfordian 161.5 → 159.0 |

So the first two steps brought several boundaries onto ICS chart values,
and the third moved three of them (Olenekian, Anisian, Wuchiapingian) back
off the chart, to the values queried in [CONTACTS.md](../CONTACTS.md) C10
(i). A vintage comparison must separate these changes of time scale from
reassignment of occurrences to intervals.

**Verdict for Q-045: usable as public-data vintages, under the rule.**
Three cautions apply:
- One sampled archive is cut at its tail. 2023-12-28 holds 1,344,110 rows
  where its own metadata reports 1,595,282, and the registry omits it.
- The call excluded pre-Ediacaran records until February 2026.
- The rule's era skew (above) must be carried into any comparison.

[Detail withheld pending disclosure to the data custodian.]

## Contents

| Route | Content | Files | Size |
| --- | --- | ---: | ---: |
| `metadata` | every version's `metadata.txt` (PBDB's `datainfo`: call, access time, records found and returned, stated licence), and `metadata_taxa.txt` for the 16 versions with taxon tables | 1,194 | 1.2 MB |
| `tables` | `pbdb_csv.zip` and the metadata for 12 versions: the first of each year, each change of API call, the one archive much smaller than its neighbours (2023-12-28), and the newest | 25 | 1.76 GB |

[zenodo-versions.tsv](zenodo-versions.tsv) lists all 1,178 versions with
their files, sizes and checksums. [The series](profile/pbdb_chronosphere_series.tsv)
gives each version's call, access time, records found and stated licence.
The three formats of all versions total 492 GB, and the CSV zips alone 182
GB. A version is mirrored when an analysis needs it.

## Provenance and lineage

Ádám Kocsis (FAU Erlangen) downloads the whole PBDB occurrence table through
the public API and deposits each download as a new version of one Zenodo
record. The Zenodo creator is "The Paleobiology Database Community", and
each version's description quotes the API call it used. chronosphere's
public registry (`chrono_arch_2`) lists 1,171 of the 1,178 versions with
their DOIs, and the `chronosphere` R package fetches them by date. Seven
versions are on Zenodo but not in the registry:
- five between December 2021 and March 2022, each within a day of a
  registry version;
- the truncated 2023-12-28 version (10437013);
- a second 2024-04-06 version (10991647), the same size as the listed one.

Each download is PBDB as served that day: current
identifications, current interval ages and palaeocoordinates, and current
collection fields. A version therefore records the database's state on that
date, which no query of today's PBDB can reproduce
([pbdb](../pbdb/README.md), Weaknesses: creation and modification dates do
not reconstruct past states).

## Structure

Each version holds the same table in three formats: `pbdb_occs.rds` (R),
`pbdb_parquet.zip` and `pbdb_csv.zip` (one `pbdb_occs.csv`, written by R,
with `NA` for missing values and R's renaming of repeated columns, such as
`formation.1`). It also holds `metadata.txt`: PBDB's `datainfo` header,
with the call, access time, records found and records returned, and the
licence PBDB stated. Versions since 5 July 2026 add the taxon table in the
same three formats, plus `metadata_taxa.txt`. One row is one occurrence
under its identification at the time of download; reidentified occurrences
appear once (rows equal distinct occurrence numbers in every sampled
version). The API call changed three times (see Weaknesses). Among the
sampled tables, the CSV has 72 columns in 2019, 80 from September 2020, 144
from May 2021, 147 by December 2023, 150 by January 2025 and 152 in 2026.

## Access

- **Mirror.** `deep-server:/data/paleodata/pbdb-chronosphere/<route>/raw/<version>/`
  with manifests. The `metadata` route holds every version's metadata file.
  The `tables` route holds `pbdb_csv.zip` and the metadata of the sampled
  versions. [snapshots.tsv](snapshots.tsv) lists them.
- **Refresh.** [pbdb_chronosphere_snapshot.sh](pbdb_chronosphere_snapshot.sh)
  `[metadata] [tables]`. To add a version, add its version directory to the
  `tables` list; each version is about 0.5 GB in its three formats and
  0.1-0.2 GB as CSV alone. Zenodo serves each connection at 0.1-0.3 MB/s, so
  the routes fetch in parallel (`--jobs`).
- [Detail withheld pending disclosure to the data custodian.]
- **Zenodo.** Any version by its record number:
  `python3 data_mirror.py zenodo 7808072 DEST --only <version>_<record>
  --files pbdb_csv.zip 'metadata*.txt'` (the version directories are listed
  in each route's `versions.tsv`). `--latest` follows Zenodo's version
  index, which is broken for this record (see Weaknesses); the tool refuses
  it if the newest index is shared.
- **R.** `chronosphere::fetch(src = "pbdb", ser = "occs3", ver = "20240107")`
  downloads a version from Zenodo through the registry (series as in
  [pbdb_versions.tsv](../../software/chronosphere/pbdb_versions.tsv); not
  run here).

## Strengths

- The only dense series of whole-PBDB states we know of: 1,178 versions over
  seven years, each with a DOI, checksums and the exact API call.
- Each table carries the identification, intervals, ages, palaeocoordinates
  and collection context of its day, so a past analysis can be rerun on the
  data its authors could have seen, or, after the rule, on the part of it
  that is public today.
- Eleven of the 12 sampled tables hold exactly the records their metadata
  reports.
- [Detail withheld pending disclosure to the data custodian.]

## Weaknesses and pitfalls

- [Detail withheld pending disclosure to the data custodian.]
- **One archive cut at its tail.** Version 2023-12-28 (Zenodo 10437013)
  holds 1,344,110 rows, and its metadata reports 1,595,282 records found.
  The table is in occurrence-number order and stops at 1,382,650, partway
  through a row, with no final newline (the profiler counts that partial
  row). Of the 231,346 occurrences that are
  public today, were created before its access time and are missing, 230,769
  are numbered above that point. The rds and parquet files are probably cut
  too: their bytes per record are about a fifth below the neighbouring
  versions' (inferred from Zenodo's file sizes). The registry omits this
  version. Check every table's rows against its metadata before use (the
  profiler flags a mismatch). A screen of bytes per record over all 1,178
  versions flags no other version (review, 2026-10-24), so no other archive
  has lost more than about 5% of its records.
- **The API call changed three times.**
  - 2020-09-09: 16 to 18 show blocks (`refattr`, `entname`).
  - 2021-05-18: 18 to 34 entries (`refattr` listed twice), adding
    abundance, ecospace, taphonomy, preservation, `geo`, `methods` and
    others.
  - 2026-02-27: `interval=Ediacaran,Holocene` replaced by `all_records`.
  Until then the interval filter excluded records. Take the occurrences
  public today, created before a download and missing from it (complete
  tables only; [checks](profile/pbdb_chronosphere_checks.tsv)):
  - 649 to 2,061 per version from 2020 to 2025, 9 in February 2026 and
    none in October 2026.
  - In January 2024, 1,278 of the 2,061 lie wholly before the Ediacaran
    (`min_ma` of at least 635 Ma).
  - From 2020 to 2024, each version misses another 520 to 730, about 470 of
    them in three regional or broad intervals (Westphalian B, Sarka,
    Neoproterozoic). They are gone once the call changed, so we infer the
    interval filter excluded them.
  - In November 2019, 6,589 of the 7,875 missing were created in the six
    weeks before that download (mostly Eocene). The February 2020 version
    has them, and why the November download missed them is unknown.
- **Ages change with the time scale.** PBDB re-dated its intervals in at
  least three steps between January 2024 and October 2026 (Summary). Before
  comparing ages across versions, either re-date each version's intervals
  on one time scale, or compare interval assignments rather than ages.
  The 2026 versions are weekly, so dating the third step needs only about
  four more tables. The first two (daily 2024 versions, 71 in 2025) need
  about four each.
- **Zenodo's version index is broken for this record.** 157 versions share
  index 741, nine other indices repeat, and in 16 places a later version
  has a lower index ([zenodo-survey.tsv](zenodo-survey.tsv)). The newest
  value (983) is unique today, so `data_mirror.py --latest` picks
  2026-10-18, but the order cannot be trusted. Use the version strings,
  which are download dates, as the profiler does. One version string
  repeats (20240406, two records).
- **Gaps.** The longest are 127 days (February to June 2020), 87 days
  (November 2019 to February 2020), 87 days (January to April 2023), 73 days
  (December 2025 to February 2026), 42 days (June to August 2020) and 40
  days (May to June 2022).
- **The 2025 IODP import shows as a step.** Records found rose by 307,950
  between the 18 and 29 September 2025 downloads: PBDB's import of 306,489
  IODP occurrences created on 21 September 2025 ([pbdb](../pbdb/README.md)).
  Treat it explicitly in any series spanning that date.
- **Licence statements differ.** Zenodo says CC BY 4.0 for every version.
  PBDB's own header said CC BY in downloads up to 17 February 2025 and CC0
  from 24 February 2025, which dates the change queried in
  [CONTACTS.md](../CONTACTS.md) C10 (a).
- **The CSV is R's.** Missing values are the string `NA`, repeated column
  names are suffixed (`formation.1`), and the columns differ by period
  (Structure).
- **Size.** Every version in every format is 492 GB; mirror only the
  versions an analysis uses.

## Overlap with other sources

- **[pbdb](../pbdb/README.md).** Our public snapshot of 23 October 2026 is
  the reference for "public today". The 18 October 2026 version holds
  1,782,350 of its 1,782,649 occurrences; the other 299 were created in
  between.
- [Detail withheld pending disclosure to the data custodian.]
- **[Software catalogue](../../software/chronosphere/pbdb_versions.tsv).**
  The registry listing came from the Packages session (lead L-005, board
  76/2350). chronosphere-info/case_pbdbRT computed range-through diversity
  for every version to September 2020: an earlier small vintage analysis.

## EPRP relevance

- **Q-045 (parked), and the archived-extract component the checkpoint moved
  into Q-044.** This is the input for archived-extract robustness. A
  workable design: pick versions at the dates a target analysis used,
  apply the rule, re-date intervals on one time scale, and separate
  additions, deletions, reidentifications and interval reassignments.
- **Q-040.** Time-scale versions are a source of age uncertainty that
  ordinary analyses never see.
- **Under the PBDB hold.** STATUS.md requires "a bounded public-data
  contract" for any rebuild. The rule above is a candidate. It needs, for
  each version used:
  - rows equal to the metadata's records found;
  - rows dropped whose collection has occurrences but none public in a
    dated public snapshot;
  - [Detail withheld pending disclosure to the data custodian.]
  - the snapshot date recorded with the result.

  Whether to adopt the rule is the main agents' call. Nothing here is a
  biological estimate.

## Citation and terms

[Detail withheld pending disclosure to the data custodian.]

## Verification log

- 2026-10-24 (Claude, Opus 5.5):
  - *checked*: indexed all 1,178 Zenodo versions ([zenodo_survey.py](zenodo_survey.py),
    with Zenodo's version index) and mirrored every metadata file (1,194
    files) and 12 tables (1.76 GB); all verify.
  - [Detail withheld pending disclosure to the data custodian.]
  - *checked*: [pbdb_chronosphere_checks.py](pbdb_chronosphere_checks.py)
    gives the registry comparison, gaps, Zenodo index, interval-age steps,
    era shares, missing public records and table tails
    ([output](profile/pbdb_chronosphere_checks.tsv)).
  - *checked*: the age drift is a time-scale change. On 20191122, 981,357 of
    the 1,220,213 rows public today keep both intervals but have a new
    `max_ma`, and each interval maps to one old and one new value.
  - [Detail withheld pending disclosure to the data custodian.]
  - *source claim*: the API calls (Zenodo descriptions and the datainfo
    headers), PBDB's stated licences.
  - Independent review (Claude Sonnet subagent), findings applied:
    - the third re-dating step and its link to C10 (i);
    - the era skew and "public-data vintage";
    - the tail cut;
    - the licence wording in the front matter;
    - the contract wording;
    - committed checks for the numbers;
    - a `data_mirror.py` regression when a record has no files.
