# Audit of the main checkout's `data/raw` against the catalogue

[Detail withheld pending disclosure to the data custodian.]

## Result

- **Provenance.** `data/raw` holds 192 files (2.95 GB) in 13 holdings.
  Every data file is in the catalogue's mirror byte for byte: 184 files,
  matched by sha256 against the mirror's manifests and zip members. That
  count includes Knope et al. 2015's supplement, which the audit found
  uncatalogued and mirrored. The other eight files are the main agents' own
  retrieval records (four), three publication copies, and a PBDB intervals
  download whose content matches the catalogue's intervals snapshot. All 192
  files are accounted for.
- **Licences.** The data are open (CC0, CC BY 4.0) except the PhanDA and
  PhanSST repositories, which state none. The three publication copies are
  one CC BY 4.0 article (Lamyman et al. 2026) and Walton and Korn's Wiley
  article page. The main agents' notes agree with the catalogue's licences,
  with three small differences (below).
- [Detail withheld pending disclosure to the data custodian.]
- **One missing input.** `data/q021-shangsi-support/build.py` reads
  `data/raw/cao2022/41561_2022_1009_MOESM2_ESM.xlsx`, which is not in
  `data/raw`. It is the only path that tracked files name under `data/raw`
  and that does not exist. The catalogue now holds that workbook and its
  supplementary PDF (below). Both match the sha256 values Codex pinned.
- [Detail withheld pending disclosure to the data custodian.]

## Holdings

Matched means the file's sha256 equals a file or zip member in the mirror
([raw_join.tsv](profile/raw_join.tsv)).

| Holding | Files | MB | In the mirror | Catalogue entry | Licence (catalogue) | Main agents' note |
| --- | ---: | ---: | --- | --- | --- | --- |
| `ammonoid-growth-walton-korn-2018` | 6 | 0.9 | the workbook | register-deposits `walton2018-ammonoid-ontogeny` | CC0 | `ammonoid-growth-support/` (CC0) |
| `benson2025` | 4 | 1,125.6 | 4/4: the occurrence file (= the Dryad and Zenodo copies) and three members of the Zenodo code record | `benson2025-marine-latitudinal-diversity` (Dryad), `close2025-marine-latitudinal-diversity-code` (Zenodo 15269137) | CC0; CC BY 4.0 | `q027-joint-support/`, `q027-support-audit/`, `q044-joint-support/` (CC BY 4.0) |
| `cantalapiedra2019` | 10 | 9.5 | 10/10, as members of the Dryad zip | `cantalapiedra2019-phylogenetic-diversity` | CC0 | `q022-premortem/` (CC BY 4.0, from the PNAS supplement) |
| `close2019` | 138 | 778.7 | 138/138: the zip and its extracted tree | `close2019-tetrapod-local-richness` | CC0 | `q044-joint-support/`, `q044-support-audit/` (no licence stated) |
| `dryad-downloads` | 4 | 251.3 | the Brombacher workbook; all 373 members of the three Dryad download zips (Monarrez, Benson, Close) | `brombacher2017-foram-allometry` and the three above | CC0 | `q050-sample-crosswalk/`, `q038-monarrez-contract/`, `q044-joint-support/build.py` (the Close zip); the Benson zip is named nowhere |
| `knope2015` | 1 | 3.9 | yes, after this audit | `knope2015-guild-coding` (new) | CC BY 4.0 | `b001-support/` (CC BY 4.0) |
| `lamyman2026` | 6 | 3.3 | the four data files | `lamyman2026-pforam-phylogeny` | CC BY 4.0 | `q012-source-support/` and others (CC BY 4.0) |
| `monarrez2023` | 10 | 98.7 | 10/10 | `monarrez2023-selectivity` | CC0 | `q038-*` (extracted from the Dryad zip) |
| `pbdb` | 1 | 0.02 | content only (below) | pbdb `intervals` | CC BY 4.0 | `interval-crosswalk/`, `q042-crosswalk/` and others |
| `phanda` | 4 | 20.4 | 4/4 | climate-forcing `phanda` | none stated | `interval-crosswalk/` (terms recorded), `phanda-*` |
| `phansst` | 1 | 42.5 | 1/1 | climate-forcing `phansst` | none stated | `triton-event-support/` (paper CC BY, no repository licence) |
| `song2021` | 3 | 1.3 | 3/3 | climate-forcing `song2021-temperature-thresholds` | CC BY 4.0 | `interval-crosswalk/` |
| `triton` | 4 | 614.5 | 4/4: `Triton.zip` and its readme; the two loose `.RData` files are byte-identical members of that zip | triton | CC0 | `triton-event-support/`, `q012-exposure-support/` (CC0) |

The eight files that are not data:

- `ammonoid-growth-walton-korn-2018/`: `dataset-metadata.json`,
  `files-metadata.json`, `retrieval-log.json` and
  `walton-korn-2017-retrieval-20261015.json` are Codex's retrieval records.
  `walton-korn-2017-publisher.html` is the Wiley article page (Wiley terms).
  The literature library holds the article through Wiley's TDM route
  (mining only).
- `lamyman2026/article/`: the article as PDF and EPUB. Crossref records CC BY
  4.0 for the version of record. No tracked note records where this copy came
  from: `q012-source-support/README.md` says full-text access returned 403.
  The literature library's fetch also got 403 on all five routes, so this
  copy (PDF sha256 `bf479249…7579`) is the project's only one.
- `pbdb/intervals_scale1.json`: PBDB's scale-1 intervals, downloaded 8
  October. All 171 intervals match the catalogue's intervals snapshot of 22
  October in name and both ages ([intervals_compare.txt](profile/intervals_compare.txt)).

### Differences between the main agents' notes and the catalogue

- **Cantalapiedra et al. 2019.** `q022-premortem` records the inputs as CC BY
  4.0 from the PNAS supplement, because Dryad refused unauthenticated
  downloads. The ten files are byte-identical to members of the Dryad
  deposit, which is CC0. Both are open.
- **Close et al. 2019.** `q044-joint-support` notes that the zip has no
  licence file, which is true of the zip. The Dryad record states CC0.
- **Benson et al. 2025.** `q027-joint-support` says the companion Dryad
  deposit was not used because anonymous downloads return 401. `data/raw`
  nevertheless holds that deposit's download zip in `dryad-downloads`. Its
  occurrence file is byte-identical to the Zenodo member the note uses, so
  the difference does not affect any result.

### Stated checksums

[stated_hashes.py](stated_hashes.py) took every sha256 in the tracked
`data/` files that name `data/raw` (58) and looked each up among the raw
files and zip members ([stated_hashes.tsv](profile/stated_hashes.tsv)). 39
match. The 19 that do not are:

- the deleted B-001, Q-042 and Q-006 PBDB extracts (six values, stated 11
  times in four files);
- four ammonoid PDFs that the ammonoid pilot inventories in scratch;
- the Cao et al. 2022 workbook (`q021-shangsi-support/build.py`), absent from
  `data/raw` (above);
- the RMark source archive cited by `q038-flag-audit`;
- two PhanDA audit hashes: the original build script's, and the optional
  `data/derived/phanda-stage-differences/stage_differences.tsv`, which has
  since been rewritten (sha256 `321541e9…`). The note expects this: the
  comparison is skipped and labelled when the file has changed.

## [Detail withheld pending disclosure to the data custodian.]

[csv_occurrence_ids.py](csv_occurrence_ids.py) reads every `.csv`, `.tsv` and
`.txt` file and zip member with an `occurrence_no` column (the
register-deposits check's rule). [rbin_scan.py](rbin_scan.py) with
[rdata_occurrence_ids.R](rdata_occurrence_ids.R) reads the R binaries,
including those inside zips. [Detail withheld pending disclosure to the data
custodian.] The scan read the main agents' files themselves; their hashes
already showed them identical to the mirror copies checked on 23 October, and
the counts agree.

[Detail withheld pending disclosure to the data custodian.]

No other holding has occurrence numbers. Triton, the Close et al. `geoMST`
workspace and Monarrez et al.'s encounter histories were read and hold none.
The main checkout's `scratch/` (3.6 GB) has no table with an
`occurrence_no` column and no R binary with one; its only PBDB records are
two in an 831-byte Q-045 check (`scratch/q045-vintage/`).

[Detail withheld pending disclosure to the data custodian.]

## R binaries across the mirror

Because the register-deposits check skips R binaries, the same scan ran over
the whole mirror: 412 R binaries (`.RData`, `.rda`, `.rds`, loose and in
zips) in 24 entries and deposits. About 7,000 package internals were
skipped, mostly the `renv` library in Benson and Close's code record
([rbin_mirror_files.tsv](profile/rbin_mirror_files.tsv),
[rbin_mirror_check.tsv](profile/rbin_mirror_check.tsv)):

[Detail withheld pending disclosure to the data custodian.]

[Detail withheld pending disclosure to the data custodian.] The
register-deposits entry now flags them, its counts read eleven downloads in
twelve deposits, and Carrillo et al.'s download date and query, which their
script records, replace "not stated". The other 19 holdings' binaries have no
occurrence-number column. Two gaps remain, each recorded per file: AusTraits
7.0.0's full `.rds` has 603 lists nested deeper than 40 levels that the walk
skips (a plant-trait database, not PBDB), and a `tidytree` object in two Penn
et al. 2023 binaries could not be read without that package.

## Changes to the catalogue

- **Knope et al. 2015, Supplementary Data 1** (`register-deposits/knope2015-guild-coding`):
  B-001's guild coding, 18,317 genera, CC BY 4.0. Mirrored from Springer
  Nature's static ESM link, byte-identical to `data/raw/knope2015/`. A
  second run of the new `esm` route took a second, identical snapshot; the
  mirror rule keeps both.
- **Cao et al. 2022, Table S1 and supplementary PDF**
  (`register-deposits/cao2022-reverse-weathering-esm`): the input Q-021's
  Shangsi build expects at `data/raw/cao2022/`. Springer Nature TDM licence,
  not open access; held privately under Barry's 23 October decision:
  "Mirroring locally is always okay for us".
- [Detail withheld pending disclosure to the data custodian.]

## For the main agents and the other side sessions

The audit changes nothing outside this worktree and the mirror. Open items:

1. Restore `data/raw/cao2022/` from
   `deep-server:/data/paleodata/register-deposits/cao2022-reverse-weathering-esm/raw/2026-10-25T0547Z_url/`,
   or point `q021-shangsi-support/build.py` there.
2. [Detail withheld pending disclosure to the data custodian.]
3. Record where `data/raw/lamyman2026/article/` came from. The References
   session can add this CC BY 4.0 copy to the literature library, which has
   none.
4. Note the CC0 Dryad licence in `q044-joint-support` and, optionally, the
   Dryad source in `q022-premortem`.

## Reproducing

[run_audit.sh](run_audit.sh) runs every step: inventory and sha256 join,
intervals comparison, occurrence numbers and the public-snapshot check, and
the mirror-wide R-binary scan. `bash run_audit.sh /path/to/main/data/raw WORK`
writes to `WORK` and copies the outputs to [profile/](profile/). Local steps
read only the given `data/raw`; deep-server steps read `/data/paleodata` and
write under `/data/codex/scratch/eprp-paleodata/raw-audit`. The public
snapshot, the sample size (12) and the seed (20261025) are fixed in the
script. [Detail withheld pending disclosure to the data custodian.]

| File | What it does |
| --- | --- |
| [raw_inventory.py](raw_inventory.py) | files, sizes and sha256 per holding |
| [zip_members.py](zip_members.py) | sha256 of every zip member, nested zips one level down |
| [raw_join.py](raw_join.py) | joins the inventory and members against the mirror's manifests and zip members |
| [stated_hashes.py](stated_hashes.py) | checks the sha256 values tracked notes state |
| [intervals_compare.py](intervals_compare.py) | PBDB intervals download against the catalogue snapshot |
| [csv_occurrence_ids.py](csv_occurrence_ids.py) | occurrence numbers in text files and zip members |
| [rbin_scan.py](rbin_scan.py), [rdata_occurrence_ids.R](rdata_occurrence_ids.R) | occurrence numbers in R binaries, loose and in zips |
| [Detail withheld pending disclosure to the data custodian.] | [Detail withheld pending disclosure to the data custodian.] |

Review: REVIEW_PLACEHOLDER
