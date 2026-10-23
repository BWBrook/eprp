---
id: register-deposits
name: Dryad deposits named by the EPRP question registers (global deep time)
kind: deposit
status: active
last_update: "2026-08-25 (newest deposit, Stigall et al. 2026)"
scope:
  taxa: ["marine invertebrates (molluscs, brachiopods, bryozoans, ostracods, foraminifera, graptoloids, ammonoids)", "terrestrial tetrapods", "mammals (phylogenies)"]
  time: "Cambrian to Recent"
  space: "global"
  record_unit: "varies: a PBDB occurrence download, a genus capture history, a specimen measurement, a time series, a phylogeny, model outputs"
size:
  as_of: "2026-10-23"
  deposits: 15
  files_on_disk: 91
  mirrored_bytes: 544988629
access:
  tier: open
  licence: "CC0 (every deposit, per Dryad)"
  routes:
    - {type: dryad, url: "https://datadryad.org/api/v2/datasets/", state: "index open; downloads with the Dryad API account on deep-server; DOIs in snapshots.tsv", checked: 2026-10-23}
  api: "Dryad API v2 (data_mirror.py dryad)"
versioning:
  replay: exact
  notes: "each deposit is a fixed Dryad version; four have earlier versions (21 versions indexed in dryad-versions.tsv). The newest file-bearing version of each is mirrored; Monarrez et al.'s current v11 is a metadata revision of the mirrored v10 with identical files"
mirror:
  path: deep-server:/data/paleodata/register-deposits
  policy: "newest version of every Dryad deposit the registers or their ideation notes cite; Zenodo and Figshare deposits to follow"
  state: "15 deposits, 91 files (545 MB), each with a manifest; Dryad checksums verified on download (sha256 for 77 listed files, md5 for 16)"
lineage:
  upstream:
    - "supporting data of papers 2015-2026 (Proc. R. Soc. B, PNAS, Science, Nature Ecology & Evolution, Paleobiology, Palaeontology, American Naturalist, Palaeogeography Palaeoclimatology Palaeoecology, Royal Society Open Science)"
    - "several deposits embed dated PBDB downloads (Close et al., about 2017; Benson et al., 2022-05-23; Monarrez et al., about 2023)"
  downstream:
    - "EPRP questions Q-002, Q-005, Q-011, Q-012, Q-022, Q-027, Q-036, Q-038, Q-044, Q-050 and B-002 (registers); B-009, B-012, B-014, B-016 (14 October ideation notes); Q-045 (data vintage, inferred)"
eprp_questions: [Q-002, Q-005, Q-011, Q-012, Q-022, Q-027, Q-036, Q-038, Q-044, Q-045, Q-050, B-002, B-009, B-012, B-014, B-016]
citation:
  - "each deposit's Dryad DOI (snapshots.tsv) and its paper (below)"
entry:
  created: 2026-10-23
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session); DOIs gathered from the registers by a Claude Sonnet subagent
  reviewed: "2026-10-23, independent Claude Sonnet subagent; findings applied"
---

# Dryad deposits named by the EPRP question registers

## Summary

The EPRP question registers and their ideation notes cite fifteen Dryad
deposits as inputs; until now the project held five of them, as files Barry
downloaded by hand. With the Dryad API account on deep-server they are now
mirrored at their newest file-bearing versions, with Dryad's checksums
verified. They feed questions in development and on hold: Monarrez et al.'s
genus capture histories (Q-038), Walton and Korn's ammonoid conch ontogenies
(B-002), Crampton et al.'s graptoloid extinction-rate spectrum (Q-005,
Q-011), Cantalapiedra et al.'s mammal phylogenies (Q-012, Q-022), and the
tetrapod and marine PBDB downloads behind Close et al. and Benson et al.
(Q-044, Q-027). Three deposits embed dated PBDB downloads, which matter
because PBDB cannot replay a past state.

## Contents

Our inventory ([profile](profile/register_deposits_profile.tsv)). Questions
are cited in `ideas/register.md` and `ideas/register-blue-sky.md` of the main
checkout, except B-009, B-012, B-014 and B-016, which cite them in the 14
October blue-sky ideation notes (`ideas/2026-10-14-blue-sky-ideation-*.md`).
Tables are listed by the paper's first author; directory names follow the
Dryad depositor.

| Deposit (directory) | Questions | Content | Size |
| --- | --- | --- | ---: |
| Monarrez et al. 2023, extinction selectivity (`monarrez2023-selectivity`) | Q-038 | cleaned PBDB occurrences (253,747 rows × 40 columns), genus sizes and ranges (6,707 rows), range-through genus table, encounter histories and Pradel model coefficients for the Big Five and other partitions | 98.7 MB |
| Walton and Korn 2017, ammonoid conch ontogeny (`walton2018-ammonoid-ontogeny`) | B-002 | one workbook: 179 species rows, with conch parameters along ontogeny in parallel sheets | 0.2 MB |
| Close et al. 2019, tetrapod local richness (`close2019-tetrapod-local-richness`) | Q-044 | code and inputs: PBDB downloads (157,847 tetrapodomorph and 106,147 mammaliamorph occurrences × 135 columns; 168,713 collection rows; 32,189 taxa), dated 2017-12-13 by the zip members' timestamps (inferred) | 72.2 MB |
| Brombacher et al. 2017, foraminiferal allometry (`brombacher2017-foram-allometry`) | Q-050 | 12,633 specimen measurements × 12 columns | 0.8 MB |
| Hunt et al. 2015, trait evolution and stasis (`hunt2015-trait-stasis`) | Q-036 | paleoTS time series (771 files in a zip, plus 164 macOS resource-fork entries; also as RData), a 771-row summary and references | 0.8 MB |
| Cantalapiedra et al. 2019, phylogenetic diversity (`cantalapiedra2019-phylogenetic-diversity`) | Q-012, Q-022 | ten phylogenetic datasets (Nexus trees) in a zip | 4.0 MB |
| Slattery et al. 2025, nuculid stasis (`slattery2025-nuculid-stasis`) | Q-036 | 1,106 *Nucula* specimen measurements and two summary tables | 0.2 MB |
| Benson et al. 2025, marine latitudinal diversity (`benson2025-marine-latitudinal-diversity`) | Q-027 | PBDB downloads of 2022-05-23 (712,947 non-chordate animal occurrences × 126 columns, with group files such as Mollusca 368,760 and Brachiopoda 146,281) and analysis code | 79.5 MB |
| Franeck and Liow 2019, Ordovician radiation (`franeck2018-ordovician-radiation`) | B-009 | code archive (7z, not parsed) and supplement PDF | 4.4 MB |
| Stigall et al. 2026, Ordovician species dynamics (`stigall2026-ordovician-species`) | B-009 | small character and occurrence tables (17 to 23 rows), trees as TIFF, supplements | 14.3 MB |
| Leventhal and Samuels-Fair 2025, bryozoan larval brooding (`leventhal2025-bryozoan-brooding`) | B-012 | a 14,826-row main table (`alldata.csv`, 7 columns), 796 brooding records, WoRMS name matching (1,100 rows), mark-recapture outputs | 8.3 MB |
| Lidgard et al. 2021, cheilostome and cyclostome assemblages (`liow2021-cheilostome-cyclostome`) | B-014 | bryozoan fossil occurrences (25,756 rows), taxa by locality (36,155 rows), synonym tables, stage table, PyRate output (109 MB RData) | 184.6 MB |
| Martins et al. 2020, ostracod sexual dimorphism (`hunt2020-ostracod-dimorphism`) | B-016 | three tables (168, 71 and 43 rows) and a supplement | 0.5 MB |
| Crampton et al. 2026, spectrum of extinction rates (`crampton2026-extinction-spectrum`) | Q-005, Q-011 | R scripts and inputs: randomised graptoloid range-slope files (up to 648,522 rows) for Ordovician and Silurian, with phyletic sensitivity tests | 25.5 MB |
| Malanoski et al. 2024, climate and extinction risk (`malanoski2024-climate-extinction-risk`) | Q-002 | extracted climate-model values (462,854 rows), intrinsic and extrinsic variables (22,221 rows), genus body sizes (9,460 rows) | 51.0 MB |

## Provenance and lineage

Each deposit is the supporting data of one paper; the paper DOIs come from the
deposits' Dryad records (primary article) and were checked against Crossref
for first author, year and journal. The registers' data-gate notes record
which questions use which deposit; three had been blocked because Dryad
refuses downloads without an account. The embedded PBDB downloads were made by
the authors with PBDB's download tools; they are the only route to those past
states. Several deposits link further Zenodo records (code or supplements):
Benson et al. 10.5281/zenodo.15269137, Monarrez et al. 10.5281/zenodo.7816408
and 8341743, Leventhal and Samuels-Fair 14104269 and 14918283, Lidgard et al.
5394385, Malanoski et al. 10541354 (from the Dryad records, via the review);
they are not mirrored yet.

## Structure

As deposited: CSV and Excel tables, R scripts and RData, Nexus trees, zips
and a 7z archive. The profile lists every file and, for tables, rows,
columns, headers and numeric columns. Zip members are inventoried; macOS
resource-fork entries are skipped and counted.

## Access

- **Mirror.** `deep-server:/data/paleodata/register-deposits/<deposit>/raw/<version>/`
  with manifests. Indexes: [snapshots.tsv](snapshots.tsv) (mirrored
  versions) and [dryad-versions.tsv](dryad-versions.tsv) (all 21 versions).
  Dryad lists 93 files; Hunt et al. 2015 lists two pairs of identically named
  README files, which land as one file each, so 91 are on disk.
- **Refresh.** [register_deposits_snapshot.sh](register_deposits_snapshot.sh)
  runs `data_mirror.py dryad DOI DEST --latest` for each DOI with the Dryad
  API account on deep-server. `--latest` now takes the highest version
  number (Dryad's publication dates are not monotonic in version, which is
  why Monarrez et al. v10 was taken rather than v11).
- **Main checkout copies.** Barry's hand-supplied files for Close, Benson,
  Monarrez and Brombacher and the Walton and Korn workbook are identical, file
  by file, to the mirror (sha256). The main checkout also holds
  Cantalapiedra et al.'s Nexus files (not compared).

## Strengths

- One place for the register's Dryad deposits, at fixed versions with
  checksums, so analyses can cite exactly what they used.
- Three archived PBDB states for data-vintage work and for reproducing
  published analyses.

## Weaknesses and pitfalls

- **Heterogeneous and code-heavy.** Several deposits are analysis bundles
  (code, RData, intermediate outputs) rather than clean tables; the 7z
  archive is not inventoried.
- [Detail withheld pending disclosure to the data custodian.]
- **Not every register deposit is on Dryad.** Zenodo and Figshare deposits
  the registers cite (Lamyman 2026, PhanDA priors, Song 2021, Rozzi 2023,
  Cooke 2023 and others) are the next tranche ([BACKLOG.md](../BACKLOG.md)).

## Overlap with other sources

- **PBDB** ([pbdb](../pbdb/README.md)): the Close, Benson and Monarrez
  deposits hold past PBDB states; the catalogue's global snapshot is the
  current public one.
- **Main checkout `data/raw/`**: identical copies of five deposits, as above.

## EPRP relevance

Direct inputs to the questions listed above, including Q-038 and B-002, both
in development (STATUS.md lists B-002 with B-001 as the first blue-sky
development pair).

## Citation and terms

CC0. Cite each deposit's DOI and its paper: Monarrez et al. 2023 (R. Soc. Open
Sci., doi:10.1098/rsos.230795); Walton and Korn 2017 (Palaeontology,
doi:10.1111/pala.12308; deposit 2018); Close et al. 2019 (Nat. Ecol. Evol.,
doi:10.1038/s41559-019-0811-8); Brombacher et al. 2017 (Am. Nat.,
doi:10.1086/692570); Hunt et al. 2015 (PNAS, doi:10.1073/pnas.1403662111);
Cantalapiedra et al. 2019 (Proc. R. Soc. B, doi:10.1098/rspb.2018.2896);
Slattery et al. 2025 (Paleobiology, doi:10.1017/pab.2025.10046); Benson et
al. 2025 (Palaeontology, doi:10.1111/pala.70006); Franeck and Liow 2019
(Paleobiology, doi:10.1017/pab.2019.4; deposit 2018); Stigall et al. 2026
(Palaeogeogr. Palaeoclimatol. Palaeoecol., doi:10.1016/j.palaeo.2026.114134);
Leventhal and Samuels-Fair 2025 (Paleobiology, doi:10.1017/pab.2024.63);
Lidgard et al. 2021 (Proc. R. Soc. B, doi:10.1098/rspb.2021.1632); Martins
et al. 2020 (Proc. R. Soc. B, doi:10.1098/rspb.2020.0730); Crampton et al.
2026 (Paleobiology, doi:10.1017/pab.2026.10107); Malanoski et al. 2024
(Science, doi:10.1126/science.adj5763).

## Verification log

- 2026-10-23, checked: all fifteen deposits mirrored with
  [register_deposits_snapshot.sh](register_deposits_snapshot.sh), each listed
  file verified against Dryad's checksum (sha256 for 77, md5 for 16);
  versions indexed ([dryad-versions.tsv](dryad-versions.tsv)).
- 2026-10-23, checked: profiled with the deposits profiler
  ([../au-fossil-deposits/deposits_profile.py](../au-fossil-deposits/deposits_profile.py),
  [output](profile/register_deposits_profile.tsv)).
- 2026-10-23, checked (sha256, not committed code): the main checkout's
  hand-supplied copies match the mirror file for file.
- 2026-10-23, source claim: paper DOIs from the Dryad records' primary-article
  links; first authors, years and journals from Crossref; question links from
  the registers and ideation notes via the Claude Sonnet survey of 23
  October; Monarrez et al. v11 is a metadata-only revision (the review's
  comparison of Dryad's file listings for both versions).
- 2026-10-23, reviewed by an independent Claude Sonnet subagent; its findings
  (version choice, file and version counts, checksum types, attributions,
  question links, related records) are applied above.
