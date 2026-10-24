---
id: register-deposits
name: Deposits named by the EPRP question registers and notes — Dryad, Zenodo, Figshare and PANGAEA (global deep time)
kind: deposit
status: active
last_update: "2026-08-25 (newest deposit, Stigall et al. 2026)"
scope:
  taxa: ["marine invertebrates (molluscs, brachiopods, bryozoans, ostracods, foraminifera, graptoloids, ammonoids)", "terrestrial tetrapods and mammals", "birds (island extinctions)", "Ediacaran biota", "plants and vegetation models", "alien species (modern bridge)"]
  time: "Proterozoic to Recent"
  space: "global"
  record_unit: "varies: a PBDB occurrence download, a genus capture history, a specimen measurement, a trait table, a time series, a phylogeny, Earth-system model code and outputs"
size:
  as_of: "2026-10-23"
  deposits: 78
  mirrored: 73
  indexed_only: 5
  mirrored_versions: 75
  files_listed: 538
  files_on_disk: 536
  mirrored_bytes: 17296912544
access:
  tier: open
  licence: "mixed, per deposit (snapshots.tsv, newest versions): CC0 (27 Dryad, 1 Figshare); CC BY 4.0 (27 Zenodo, 5 Figshare); CC BY-SA 4.0 (1); MIT (5); AGPL-3 (1, recorded by Zenodo as 'apgl-v3'); 'other-open' (5 Zenodo software records); CC BY 3.0 (PANGAEA); the indexed-only records CC0 (2 Dryad), CC BY 4.0 (2) and Apache 2.0 (1)"
  routes:
    - {type: dryad, url: "https://datadryad.org/api/v2/datasets/", state: "index open; downloads with the Dryad API account on deep-server; 27 deposits mirrored, 2 over 5 GB indexed only", checked: 2026-10-23}
    - {type: zenodo, url: "https://zenodo.org/api/records/", state: "open; 39 records mirrored (two of them at two versions), 3 over 5 GB indexed only", checked: 2026-10-23}
    - {type: figshare, url: "https://api.figshare.com/v2/articles/", state: "open; 6 articles, one on the Smithsonian portal (10.25573)", checked: 2026-10-23}
    - {type: pangaea, url: "https://doi.pangaea.de/10.1594/PANGAEA.736778", state: "five IODP U1313 datasets as tab-delimited text", checked: 2026-10-23}
  api: "Dryad API v2, Zenodo REST, Figshare v2, PANGAEA (data_mirror.py dryad, zenodo, figshare, url)"
versioning:
  replay: exact
  notes: "each deposit is a fixed provider version; dryad-versions.tsv (38 versions), zenodo-versions.tsv (161) and figshare-versions.tsv (8) index every version. The newest version of each is mirrored, by the provider's own version order, except Monarrez et al.'s Dryad v10, kept because its files are identical to v11's and the main checkout's copies match it. cgenie.muffin and muffingen are also mirrored at the January 2023 releases the transfer-inputs note names"
mirror:
  path: deep-server:/data/paleodata/register-deposits
  policy: "newest version of every Dryad, Zenodo, Figshare and PANGAEA deposit the registers, ideation notes, literature notes, proposals and data READMEs cite, except those another entry holds; records over 5 GB indexed only"
  state: "73 deposits at 75 versions, 536 files on disk (17.3 GB), each with a manifest; provider checksums verified on download (PANGAEA: sha256 recorded only), and every deposit re-verified on 23 October"
lineage:
  upstream:
    - "supporting data and code of papers 2015-2026"
    - "[Detail withheld pending disclosure to the data custodian.]"
  downstream:
    - "EPRP questions Q-001, Q-002, Q-005, Q-011, Q-012, Q-022, Q-027, Q-031, Q-032, Q-033, Q-034, Q-036, Q-038, Q-044, Q-050 and B-002 (registers); B-009, B-012, B-014, B-016 (14 October ideation notes); Q-008, Q-009, Q-010, Q-020, Q-021, Q-029, B-001, B-003 (literature notes; inferred from the notes' topics); candidate C3 (23 October notes); Q-045 (data vintage, inferred); the 20-21 October proposals and consultations"
eprp_questions: [Q-001, Q-002, Q-005, Q-008, Q-009, Q-010, Q-011, Q-012, Q-020, Q-021, Q-022, Q-027, Q-029, Q-031, Q-032, Q-033, Q-034, Q-036, Q-038, Q-044, Q-045, Q-050, B-001, B-002, B-003, B-009, B-012, B-014, B-016]
citation:
  - "each deposit's DOI (snapshots.tsv) and its paper (below)"
entry:
  created: 2026-10-23
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session); DOIs gathered from the registers and notes, and papers identified, by Claude Sonnet subagents
  reviewed: "2026-10-23, independent Claude Sonnet subagents: the Dryad tranche, then the whole entry (16 findings, including 19 missed deposits); findings applied"
---

# Deposits named by the EPRP question registers and notes

## Summary

The EPRP's question registers, ideation notes, literature notes, proposals
and data READMEs cite 86 open deposits as inputs or close precedents
(counting five PANGAEA datasets from one drill site as one). Two surveys
found them on 23 October, the second prompted by the independent review.
Other entries hold five of them: Triton, the PhanDA priors, Song et al.
2021, CENOGRID and Farrell et al.'s time-scale supplement. Six are next in
the [backlog](../BACKLOG.md): five on Mendeley Data, OSF and Harvard
Dataverse, and PaleoDEM for the palaeogeography entry. This entry holds the
other 75 (Dryad, Zenodo, Figshare and PANGAEA), plus three Zenodo code
records that its Dryad deposits link to: 78 in all.

Of these, 73 are mirrored at their newest versions (two also at an older
release a note names). The providers' checksums were verified for every
deposit but the PANGAEA tables, whose sha256 was recorded on download. Five
records over 5 GB are indexed only. Between them they hold:

- [Detail withheld pending disclosure to the data custodian.]
- **Trait, body-size and functional tables.** Inputs to Q-031, Q-034, Q-036,
  Q-050 and B-003.
- **Earth-system and ecological model code and outputs.** cGENIE (the model
  and runs), CESM end-Permian and FOAM Late Ordovician fields, TREED, INDITEK,
  DeepDive and others, for the transfer and recovery work.
- **Compilations.** BioDeepTime, SInAS, Currano et al.'s fossil-leaf
  herbivory matrices and Lamyman et al.'s planktonic foraminiferal phylogeny
  with its relational database.

## Contents

Our inventory ([profile](profile/register_deposits_profile.tsv)). "Cited in"
gives the register question where a register cites the deposit. Otherwise it
names the citing note, with the note's question where the note is about one
(inferred). Notes in the main checkout, by short name:

- *register expansion*: `literature/2026-10-09-register-expansion.md`, about
  Q-008 to Q-010, Q-020 and Q-021;
- *disruption susceptibility*, *recovery contingency*, *recovery contracts*,
  *transfer inputs*, *Penn calibration*, *interchange transfer*: the
  `literature/2026-10-*` notes of those names;
- *route review*, *prior check*, *reassembly contract*, *escalation
  evidence*, *source inventory*: the Q-021, Q-010, B-001 and B-003 notes in
  `literature/`;
- *prediction units* (Q-029) and *evolvability note* (Q-050): the 10 and 11
  October notes in `literature/`;
- *C3 attenuation check* and *23 October Alroy notes*:
  `data/c3-attenuation-check/` and the `ideas/2026-10-23-alroy-*` notes, on
  candidate C3;
- *model-contract audit*: `data/model-contract-audit/`;
- *snowball proposal*, *recruitment proposal*, *hybridisation proposal*: the
  20 October proposals under `docs/review/2026-10-21-gpt6pro-proposals/`;
- *Ediacaran consultation* and *Ediacaran assessments*: the 21 October
  consultation under `docs/review/2026-10-21-gpt6pro-blind-ediacaran/` and
  the responses to it in `ideas/`;
- *14 October ideation*: `ideas/2026-10-14-blue-sky-ideation-codex.md`.

Tables are listed by the paper's first author. Directory names follow the
depositor, and are in [snapshots.tsv](snapshots.tsv).

### Dryad (15 deposits, 545 MB)

Crampton et al. and Malanoski et al. 2024 reach their questions through their
papers, which the registers cite; the deposits themselves are cited in the
disruption-susceptibility note and `resources/capability-inventory.md`.

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

### Occurrence compilations built on PBDB downloads (Zenodo)

| Deposit (directory) | Cited in | Content | Size |
| --- | --- | --- | ---: |
| Kocsis et al. 2018, biogeographical imprint of mass extinctions (`kocsis2018-biogeographic-imprint`) | register expansion | PBDB downloads of 2017-07-07 (folder name) for eight marine groups (648,458 occurrences × 117 columns; bivalves 176,682, brachiopods 164,946, gastropods 139,859), a Fossilworks collection table of 2017-07-10 (95,047 rows), stage tables, shapefiles and R code | 185.7 MB |
| Benson et al. 2025, code and data (`close2025-marine-latitudinal-diversity-code`; Zenodo lists Close first) | Q-027 | the Dryad deposit's PBDB download of 2022-05-23 (Animalia minus Chordata, 712,947 × 126, and 32 group files), PaleoReefs downloads (4,332 reefs), plate-model reconstructions (99,852 rows), climate-model fields (`gcm_data_df.rda`, 241 MB), analysis code with a bundled `renv` R library (46,914 zip members in all) | 1,549.3 MB |
| Gavirneni et al. 2025, bivalve metabolic rate and extinction (`gavirneni2025-bivalve-metabolic-rate`) | disruption susceptibility | PBDB occurrences with sea-surface temperatures (838,280 rows × 137 columns, a 1.16 GB CSV), a 222-cell trait table (124,786 rows), genus sizes and ranges (9,404 rows), a stage table, R script and supplement | 1,168.9 MB |
| Carrillo et al. 2020, South American mammals and the interchange (`carrillo2020-south-american-mammals`) | Q-033 | Datasets S1 to S4: 100 occurrence tables of American fossil mammals (S1) and 100 permutation tables (S4), drawn from 15,637 distinct PBDB occurrences; PyRate dispersal and diversification logs; R scripts | 129.5 MB |
| Al Aswad et al. 2025, end-Permian homogenisation (`alaswad2024-end-permian-homogenization`) | register expansion; disruption susceptibility; recovery contingency | a GitHub release: a PBDB extract (4,340 occurrences × 14 columns) and Quarto analysis code (AGPL-3) | 2.4 MB |
| Monarrez et al. 2023, code (`monarrez2023-selectivity-code`) and electronic supplement (`monarrez2023-selectivity-zenodo`) | Q-038 | 35 R scripts (MIT); five workbooks: encounter histories (6,562 rows) and the AIC tables S1 to S4 | 0.2 and 5.9 MB |

### Traits, body size, phylogenies and other compilations (Zenodo, Figshare)

| Deposit (directory) | Cited in | Content | Size |
| --- | --- | --- | ---: |
| Lamyman et al. 2026, Cenozoic planktonic foraminiferal phylogeny (`lamyman2026-pforam-phylogeny`) | Q-012 (source-support audit); 14 October ideation | one zip: a morphospecies key (482 morphospecies with ancestors and ranges), 1,072 dated first and last appearances on GTS2020, datums and synonymies, Nexus trees, TimeScale Creator datapacks, and the relational database behind them (Access, 1.13 GB) | 1,162.7 MB |
| Nätscher et al. 2026, marine ectotherm body size in hyperthermals (`natscher2025-ectotherm-body-size`) | Q-031 | 8,883 body-size change records × 45 columns, RData and R code | 6.2 MB |
| Cooke et al. 2023, undiscovered bird extinctions (`cooke2023-extinct-birds`) | Q-034 | GitHub release v.1.1.2: 662 extinct island bird species with extinction dates, human arrival dates for 88 archipelagos, island and climate predictors, R code | 12.8 MB |
| Currano et al. 2021, fossil-leaf herbivory (`swain2022-palaeoherbivory-review`) | Q-032 | damage-type matrices for 63 floras (72,440 leaf rows; Willershausen 7,491 and Messel 5,499 the largest), network and herbivory metrics, R code | 1.9 MB |
| Tsuboi et al. 2024, paradox of predictability (`tsuboi2024-paradox-of-predictability`) | Q-050 | R code and 28 trait time series, each in two forms, Brombacher et al.'s foraminifera among them | 0.2 MB |
| Edie et al. 2025, K–Pg functional diversity of bivalves (`edie2025-kpg-functional-diversity`) | register expansion | Dataset S1: 1,711 bivalve genera × 24 columns (functional traits and stratigraphic bounds), 224 species-level assignments, a 43-field key and a family phylogeny; R code | 0.4 MB |
| Klompmaker et al. 2017, predator–prey size ratios (`klompmaker2017-external-database-2`) | B-003 (escalation evidence) | External Database 2: 364 literature records of predation traces × 36 columns (producer, prey taxonomy, sizes, ages) | 0.1 MB |
| Cribb et al. 2026, ecosystem engineers (`cribb2026-ecosystem-engineers`) | Q-010 (prior check); register expansion | R code, cleaned Phanerozoic occurrences and reef and bioturbator data (RData), effect-size outputs | 100.1 MB |
| Cribb et al. 2023, end-Triassic ecospace (`cribb2023-ete-ecospace`) | B-001 (reassembly contract) | R code and marine and terrestrial ecospace data (RData) | 3.7 MB |
| Dunhill et al. 2024, Toarcian food webs (`beckerman2024-toarcian-secondary-extinction`) | B-001 (reassembly contract); register expansion; recovery contingency | four guild tables (21 to 48 guilds × 14 columns: guild, clade and 12 trait columns), feeding rules, network metrics, R code | 0.2 MB |
| Foster et al. 2023, Permian–Triassic siliceous organisms of Spitsbergen (`foster2023-siliceous-permian-triassic`) | Q-021 (route review) | 237 specimens × 17 columns and an abundance table | 0.04 MB |
| Smith et al. 2023, BioDeepTime (`smith2023-biodeeptime`) | disruption susceptibility | the database (7,437,847 rows as CSV; also Parquet, SQLite and RDS) and its compilation bundle, with source exports from BioTIME, Neotoma, Triton and others and 5,496 BibTeX files | 1,527.5 MB |
| Gómez-Suárez et al. 2025, SInAS 3.2 (`seebens2026-sinas`) | interchange transfer | 391,234 species–region records of native and alien ranges, location shapefiles, workflow inputs and outputs (GloNAF, WCVP and others), manual | 472.8 MB |
| Craffey et al. 2024, the journal's copy (`craffey2024-ediacaran-cooccurrence-figshare`) | Ediacaran assessments (21 October) | the Dryad deposit's data and code plus a trait table (117 genera × 23 columns); see pitfalls | 0.2 MB |
| Wang et al. 2025, trace-fossil trajectories (`wang2025-trace-fossil-trajectories`) | Ediacaran consultation | MATLAB and R code, two example trajectories, and a Windows executable (see pitfalls) | 60.8 MB |
| Tang et al. 2024, Proterozoic eukaryote diversity (`tang2024-proterozoic-eukaryotes`) | snowball proposal | Data S3: a ready-to-run CONOP bundle (a Windows CONOP executable, its configuration, and event, section and load files: 3,058 events in 278 sections) and R code; the occurrence data are the Dryad deposit below | 0.2 MB |
| Padfield et al. 2016, metabolic traits of *Chlorella* (`padfield2016-metabolic-traits`) | snowball proposal | thermal performance curves (974 rows), growth curves (324 rows), metadata | 0.2 MB |
| Qvarnström et al. 2024, digestive contents and the dinosaur radiation (`qvarnstrom2024-supplementary-figures`) | 14 October ideation | the supplementary figures (one PDF) | 11.9 MB |
| Leventhal and Samuels-Fair 2025, supplement (`leventhal2025-bryozoan-brooding-supplement`) | recruitment proposal | supplementary text, three tables (Word) and three figures (TIFF) | 6.9 MB |

### Earth-system, climate and ecological models (Zenodo, Figshare)

| Deposit (directory) | Cited in | Content | Size |
| --- | --- | --- | ---: |
| Penn et al. 2018, end-Permian climate (`penn2018-end-permian-climate`) | Q-001 | one netCDF of Community Earth System Model (CESM) monthly climatologies of ocean temperature and oxygen, 3° × 3°, for the Permian and Triassic states (`Permian_temp`, `Permian_o2`, `Triassic_temp`, `Triassic_o2`) | 145.6 MB |
| Penn and Deutsch 2022, avoiding ocean mass extinction (`penn2022-metabolic-index-extinction`) | transfer inputs; Penn calibration | MATLAB code and model output | 0.4 MB |
| Penn and Deutsch 2024, aerobic traits from OBIS (`penn2023-mi-traits-obis`) | transfer inputs | MATLAB code and outputs: OBIS-derived trait fields (a 17,690-row table) and metabolic-rate data for 22 species | 32.8 MB |
| Stockey et al. 2021, cGENIE and the metabolic index (`stockey2021-cgenie-metabolic-index`) | transfer inputs; disruption susceptibility | cGENIE configurations, outputs and analysis code | 39.4 MB |
| Ying et al. 2026, cGENIE runs for the K–Pg (`rui2026-cgenie-kpg`) | recruitment proposal; transfer inputs; disruption susceptibility | nine cGENIE (muffin) experiment archives: main, no extinction, size effect, CO₂, forced PAR, solar and others | 927.0 MB |
| Balembois et al. 2025, drivers of Phanerozoic marine biodiversity (`balembois2025-marine-biodiversity-drivers`) | model-contract audit; recovery contracts; recovery contingency | 193 netCDF fields (monthly sea-surface temperature by time slice, cGENIE output), MATLAB code | 271.1 MB |
| Cermeño et al. 2022, INDITEK (`garciacomas2022-inditek`) | model-contract audit; recovery contracts | the MATLAB model, gridded inputs (point ages, food and temperature; 127 MB) and fossil diversity series | 119.1 MB |
| Rogger et al. 2024, LIP climate sensitivity (`rogger2024-lip-climate-sensitivity`) | register expansion | model code and outputs (182 netCDF files, RDS summaries) and the temperature-proxy analysis (MATLAB, Stan) | 2,816.0 MB |
| Rogger et al. 2026, TREED v1.0 (`rogger2026-treed-vegetation-model`) | register expansion | Julia model source and three case studies (present-day validation, PETM, eco-evolutionary lags) | 1,389.5 MB |
| Minsky et al. 2026, Sturtian snowball limit cycles (`minsky2026-snowball-limit-cycle`) | snowball proposal | Python model and notebooks, a 10,000-run parameter sweep | 4.5 MB |
| Gibbs et al. 2020, MCM plankton model (`ward2020-mcm-model`) | recruitment proposal | MATLAB model code | 0.02 MB |

### Companion code for the Dryad deposits (Zenodo)

| Deposit (directory) | Cited in | Content | Size |
| --- | --- | --- | ---: |
| Lidgard et al. 2021 (`liow2021-cheilostome-cyclostome-code`) | with B-014 | R and R Markdown analysis (MIT) | 0.2 MB |
| Malanoski et al. 2024 (`malanoski2024-climate-extinction-risk-code`) | with Q-002 | four R Markdown analyses | 0.04 MB |
| Leventhal and Samuels-Fair 2025 (`leventhal2025-bryozoan-brooding-code`) | with B-012 | one R Markdown analysis (CC BY-SA 4.0) | 0.05 MB |

Benson et al.'s and Monarrez et al.'s companion records are listed with the
PBDB downloads above.

### Found by the second survey (Dryad and Zenodo)

| Deposit (directory) | Cited in | Content | Size |
| --- | --- | --- | ---: |
| Malanoski et al. 2026, palaeogeography and extinction risk (`malanoski2026-paleogeography-extinction-risk`) | disruption susceptibility | [Detail withheld pending disclosure to the data custodian.] | 289.4 MB |
| Dunhill et al. 2018, Late Triassic functional diversity (`dunhill2018-late-triassic-functional-diversity`) | B-001 (reassembly contract) | PBDB occurrence data with ecological traits (55,428 rows × 38 columns), ranged-through genera (2,838 rows), references, supporting information | 10.2 MB |
| Tang et al. 2024, Proterozoic eukaryote data (`tang2024-proterozoic-eukaryotes-dryad`) | snowball proposal | Data S1 (8,743 section rows and a table of contents) and Data S2 (figure source data); the companion of the CONOP bundle above | 3.7 MB |
| Holstad et al. 2024, evolvability and macroevolution (`holstad2024-evolvability-macroevolution`) | Q-050 (evolvability note) | fossil and contemporary trait data, grid-search results and metadata (tab-delimited text) | 4.8 MB |
| Saupe et al. 2019, range size and niche breadth (`saupe2019-range-size-niche-breadth`) | register expansion | eight data tables (1.33 million rows; the largest 834,695) | 75.4 MB |
| Syverson et al. 2018, crinoid spinosity and predation (`syverson2017-crinoid-spinosity`) | B-003 (source inventory) | spine measurements: eucladid calyces (1,031 rows) and anal sacs (458), *Gennaeocrinus* (176), and supplement B (1,064 rows) | 0.1 MB |
| Freitas et al. 2024, patch biogeography under intermittent barriers (`freitas2026-patch-biogeography-simulations`) | Q-029 (prediction units) | simulation materials in a tar.gz (not inventoried) and a README | 0.1 MB |
| Holland and Patzkowsky 2015, stratigraphy of mass extinction (`holland2016-stratigraphy-mass-extinction`) | recruitment proposal | R code and sedflux model inputs | 0.2 MB |
| Kerr et al. 2025, regional databases against field data (`kerr2025-regional-databases`) | C3 attenuation check; 23 October Alroy notes | 1,516 field-collected bivalve records and site metadata | 0.2 MB |
| Alroy 2026, coverage-based rarefaction (`alroy2026-coverage-rarefaction`) | 23 October Alroy notes | data files (tar.gz, not inventoried) and R code | 0.3 MB |
| Kontopoulos et al. 2020, phytoplankton thermal responses (`kontopoulos2020-phytoplankton-thermal`) | snowball proposal | growth rates (7,708 rows), thermal-performance parameters, a calibrated tree, R and Python code | 1.3 MB |
| Xiong and Mallet 2022, collapse of hybrid incompatibilities (`xiong2022-hybrid-incompatibilities`) | hybridisation proposal | SLiM simulation output (one zip of 791,281 files) | 3,261.6 MB |
| Cooper et al. 2024, DeepDive (`cooper2024-deepdive`) | 14 October ideation (Claude); disruption susceptibility | the DeepDive software, worked marine and proboscidean analyses with trained models, and the simulations and analyses (613 tables, 9.9 million rows) | 234.9 MB |
| Ontiveros et al. 2023 set-up, Late Ordovician FOAM simulation (`pohl2024-late-ordovician-foam`) | transfer inputs | three netCDF climate fields for 440 Ma (Hirnantian), deposited by Pohl | 173.5 MB |
| Liu, Penn and Deutsch 2026, Phanerozoic productivity and oxygenation (`liu2026-phanerozoic-productivity-oxygen`) | transfer inputs | six MATLAB figure-data files; no paper found (Crossref, 23 October) | 7.6 MB |
| cGENIE.muffin (`ridgwell-cgenie-muffin`) | transfer inputs | the Earth-system model's code: v0.9.78 (16 October 2026, MIT) and v0.9.35 (January 2023, 'other-open'; the release the note names, archived for Pohl et al. 2023) | 210.8 + 97.1 MB |
| muffingen (`ridgwell-muffingen`) | transfer inputs | cGENIE's boundary-condition generator (MATLAB): v0.24-574-NSF (2024, CC BY 4.0) and v0.9.24 (January 2023, the record the note names) | 112.2 + 112.1 MB |

### PANGAEA: IODP Site U1313 (Q-050)

Five datasets from IODP Site U1313 (North Atlantic), the Q-050 sample
crosswalk's inputs (`pangaea-u1313`, 0.1 MB, CC BY 3.0), as tab-delimited text
with PANGAEA's metadata header:

| Dataset | Paper | Content | Rows |
| --- | --- | --- | ---: |
| PANGAEA.736778 | Naafs et al. 2010 | alkenone sea-surface temperature by depth and age | 375 |
| PANGAEA.761442 | Bolton et al. 2010 | benthic *C. wuellerstorfi* δ18O | 409 |
| PANGAEA.761443 | Bolton et al. 2010 | planktic *G. ruber* δ13C and δ18O | 440 |
| PANGAEA.892803 | Bolton et al. 2018 | *G. crassaformis* Mg/Ca, temperature and δ18O | 652 |
| PANGAEA.892804 | Bolton et al. 2018 | *N. atlantica* counts | 132 |

### Indexed only: records over 5 GB

| Deposit (directory) | Cited in | Content (from the record) | Size |
| --- | --- | --- | ---: |
| Gutarra et al. 2024, Ediacaran animal forests (`rahman2024-ediacaran-animal-forests`) | Ediacaran consultation | flow-simulation data and a 0.3 MB zip of simulated communities (CC BY 4.0) | 37.8 GB |
| Gutarra et al. 2025, community hydrodynamics (`rahman2025-ediacaran-hydrodynamics`) | Ediacaran consultation | flow-simulation data and a 0.3 MB zip of simulated communities (CC BY 4.0); the zip is mirrored in [au-fossil-deposits](../au-fossil-deposits/README.md) | 38.5 GB |
| Rogger et al. 2025, PETM vegetation (`rogger2025-petm-vegetation`) | register expansion | model code and outputs (Apache 2.0) | 15.6 GB |
| Kagawa and Seehausen 2020, admixture and adaptive radiation (`kagawa2020-admixture-radiation`) | hybridisation proposal | Dryad data (CC0) | 8.0 GB |
| Shum et al. 2026, dark land surfaces as refugia (`shum2026-dark-land-refugia`) | snowball proposal | climate simulations (Dryad, CC0) | 106.1 GB |

## [Detail withheld pending disclosure to the data custodian.]

[Detail withheld pending disclosure to the data custodian.]
- Kocsis, Gavirneni, Carrillo and Couzens et al. kept no query, so their
  route is unknown.

[Detail withheld pending disclosure to the data custodian.]

## Provenance and lineage

Each deposit is the supporting data, code or model of one paper, or a
compilation with its own data paper. The DOIs were gathered from the
registers and notes by a Claude Sonnet survey on 23 October. The
independent review and a second survey, matching every citation form,
found 19 more. A second Sonnet subagent identified the first set's Zenodo,
Figshare and PANGAEA papers and checked them on Crossref; the second set's
were checked the same way. The Dryad papers come from the Dryad records'
primary-article links, checked on Crossref (one link is wrong; see
pitfalls). The embedded PBDB downloads were
made by the authors with PBDB's download tools; they are the only route to
those past states. Several deposits pair a Dryad data record with a Zenodo
code record (Benson and Close, Monarrez, Leventhal and Samuels-Fair, Lidgard
and Liow, Malanoski). All seven companion records, for those five deposits,
are now mirrored.

## Structure

As deposited: CSV and Excel tables, R scripts and RData, netCDF model output,
MATLAB, Julia, Python and Fortran (cGENIE) model code, Nexus trees,
TimeScale Creator datapacks, an Access database, zips, tar.gz archives and a
7z archive. The profile lists every
file and, for tables, rows, columns, headers and numeric columns. Zip members
are inventoried; macOS resource-fork entries are skipped and counted;
tar.gz and 7z archives are not opened. The committed profile is compacted by
[compact_profile.py](compact_profile.py): zips of more than 250 members are
summarised by extension, and the rows for Benson et al.'s bundled R package
library (890 rows) are dropped, leaving 16,510 rows (2.8 MB). The full
profile (1,762,569 rows, 450 MB, most of them the 791,281 files of Xiong and
Mallet's simulation zip) is in the mirror at
`derived/2026-10-23/register_deposits_profile_full.tsv`.

## Access

- **Mirror.** `deep-server:/data/paleodata/register-deposits/<deposit>/raw/<version>/`
  with manifests. Indexes: [snapshots.tsv](snapshots.tsv) (mirrored
  versions, with provider, DOI, licence, files and bytes),
  [dryad-versions.tsv](dryad-versions.tsv),
  [zenodo-versions.tsv](zenodo-versions.tsv) and
  [figshare-versions.tsv](figshare-versions.tsv) (every version). Dryad
  lists 153 files for the mirrored versions. Hunt et al. 2015 lists two pairs
  of identically named README files, which land as one file each, so 151 are
  on disk.
- **Refresh.** [register_deposits_snapshot.sh](register_deposits_snapshot.sh)
  `[dryad] [zenodo] [figshare] [pangaea] [index]` runs `data_mirror.py` for
  each deposit (Dryad with the API account on deep-server; Zenodo four at a
  time, since Zenodo serves about 0.3 MB/s per connection). `--latest` takes
  the provider's own newest version. Zenodo uses its version index and Dryad
  its version number, because depositors set the publication dates. A
  refresh will take Monarrez et al.'s Dryad v11, whose ten files are
  identical to v10's (sha256, 23 October).
- **The five indexed-only records** (206 GB together): fetch on demand with
  `data_mirror.py zenodo RECORD DEST --latest` or `data_mirror.py dryad DOI
  DEST --latest`.
- **Main checkout copies.** Barry's hand-supplied files for Close, Benson,
  Monarrez and Brombacher and the Walton and Korn workbook are identical, file
  by file, to the mirror (sha256). The main checkout also holds
  Cantalapiedra et al.'s Nexus files (not compared).

## Strengths

- One place for the deposits the project's questions and notes cite, at fixed
  versions with checksums, so analyses can cite exactly what they used.
- Seven archived PBDB downloads with occurrence numbers, from July 2017 to
  2024, and at least three more without them, for data-vintage work (Q-045)
  and for reproducing published analyses.
- Code alongside data for most papers, sometimes with a pinned environment
  (Benson et al.'s code record ships an `renv` library).

## Weaknesses and pitfalls

- [Detail withheld pending disclosure to the data custodian.]
- **Two copies can differ.** Craffey et al.'s journal copy (Figshare) and
  Dryad v8 ([au-fossil-deposits](../au-fossil-deposits/README.md)) hold the
  same 1,540 occurrences (the Figshare file adds one row of three `NA`s). Four
  `stratgroup` cells differ only in character encoding (`Bambuí` against a
  replacement character), blanks are coded `NA` on Dryad and empty on
  Figshare, the main R script differs (79,991 against 76,355 bytes), and only
  the journal copy has a trait table
  (`ED Trait Table Master.csv`). Cite the copy used.
- **Heterogeneous and code-heavy.** Many deposits are analysis bundles (code,
  RData, intermediate outputs, model runs) rather than clean tables. The 7z
  archive and the Access database are not inventoried below file level.
- **Executables.** Wang et al. 2025 deposit `Free_software.exe` (61 MB) and
  Tang et al.'s Data S3 holds a CONOP executable (0.2 MB), both Windows
  programs. They are mirrored as deposited and must not be run.
- **Licences can disagree inside a record.** Zenodo gives TREED v1.0 as CC BY
  4.0; its `LICENSE.txt` and the paper say Apache 2.0. Al Aswad et al.'s code
  is AGPL-3 (Zenodo's "apgl-v3"), which binds derived code.
- **A deposit can be a fragment.** Tang et al.'s Zenodo record holds only
  Data S3; the occurrence data are in their Dryad deposit. Qvarnström et
  al.'s record is the supplementary figures only.
- **Slugs follow the depositor, not the paper.** Swain deposited Currano et
  al.'s code, Beckerman Dunhill et al.'s, García-Comas Cermeño et al.'s and
  Ward Gibbs et al.'s; Zenodo lists Close before Benson.
- **Different deposits, same download.** Benson et al.'s Zenodo code record
  carries the PBDB download in their Dryad record, occurrence for occurrence.
  Do not count them as two vintages.
- **A provider's paper link can be wrong.** Kerr et al.'s Dryad record
  names Kerr and Alroy 2023 (*Frontiers of Biogeography*) as its primary
  article; the deposit's title and data belong to Kerr et al. 2025
  (*Ecography*), cited below. Liu, Penn and Deutsch's Zenodo record has no
  paper that Crossref finds.
- **Not every cited deposit is here.** Five are in other entries (above).
  Five on Mendeley Data, OSF and Harvard Dataverse, and PaleoDEM (Zenodo
  5348492, for the palaeogeography entry), are next in
  [BACKLOG.md](../BACKLOG.md).

## Overlap with other sources

- **PBDB** ([pbdb](../pbdb/README.md)): past PBDB downloads here (seven
  with occurrence numbers, from 2017 to 2024, and Malanoski et al.'s of 2025
  without); the catalogue's global snapshot is the current public one.
- **Climate forcing** ([climate-forcing](../climate-forcing/README.md)) holds
  the PhanDA priors (indexed), Song et al. 2021 and CENOGRID, which the same
  notes cite. Penn et al. 2018's CESM fields, the FOAM Late Ordovician
  simulation, and cGENIE (code, boundary-condition generator and runs) here
  complement them.
- **Time scale** ([timescale](../timescale/README.md)) holds Farrell et al.'s
  late Cambrian supplement.
- **Triton** ([triton](../triton/README.md)) and **Neotoma**
  ([neotoma](../neotoma/README.md)): BioDeepTime's compilation bundles a 2023
  Triton update and a 2022 Neotoma export.
- **Australian deposits** ([au-fossil-deposits](../au-fossil-deposits/README.md)):
  Craffey et al., as above, and the simulated-communities zip of Gutarra et
  al. 2025 (`gutarra-simulated-communities`), whose full record is indexed
  here.
- **Main checkout `data/raw/`**: identical copies of five Dryad deposits, as
  above.

## EPRP relevance

Direct inputs to the questions listed above, including Q-038 and B-002, both
in development (STATUS.md lists B-002 with B-001 as the first blue-sky
development pair). Q-012's source-support audit cites Lamyman et al. 2026
by its concept record (Zenodo 18854730), which resolves to the newest
version, mirrored here (21414007, July 2026).

## Citation and terms

Mixed licences, per deposit in [snapshots.tsv](snapshots.tsv). Cite each
deposit's DOI and its paper.

Dryad deposits: Monarrez et al. 2023 (R. Soc. Open Sci.,
doi:10.1098/rsos.230795); Walton and Korn 2017 (Palaeontology,
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

Zenodo and Figshare deposits (the companion records cite their Dryad
deposit's paper, above): Al Aswad et al. 2025 (Sci. Adv.,
doi:10.1126/sciadv.adr4199; deposit 2024); Balembois et al. 2025 (Nat.
Commun., doi:10.1038/s41467-025-63428-9); Dunhill et al. 2024 (Nat. Commun.,
doi:10.1038/s41467-024-53000-2; code deposited by Beckerman); Carrillo et al.
2020 (PNAS, doi:10.1073/pnas.2009397117); Cooke et al. 2023 (Nat. Commun.,
doi:10.1038/s41467-023-43445-2); Craffey et al. 2024 (Proc. R. Soc. B,
doi:10.1098/rspb.2024.2029); Cribb et al. 2023 (Proc. R. Soc. B,
doi:10.1098/rspb.2023.2232); Cribb et al. 2026 (Nat. Commun.,
doi:10.1038/s41467-026-73628-6); Edie et al. 2025 (Sci. Adv.,
doi:10.1126/sciadv.adv1171); Foster et al. 2023 (Paleoceanogr.
Paleoclimatol., doi:10.1029/2023PA004766); Cermeño et al. 2022 (Nature,
doi:10.1038/s41586-022-04932-6; INDITEK code by García-Comas); Gavirneni et
al. 2025 (Paleobiology, doi:10.1017/pab.2025.10041); Klompmaker et al. 2017
(Science, doi:10.1126/science.aam7468); Kocsis et al. 2018 (Proc. R. Soc.
B, doi:10.1098/rspb.2018.0232); Lamyman et al. 2026 (J. Syst. Palaeontol.,
doi:10.1080/14772019.2026.2669255); Minsky et al. 2026 (PNAS,
doi:10.1073/pnas.2525919123); Nätscher et al. 2026 (PNAS,
doi:10.1073/pnas.2505564123; the deposit points to the bioRxiv preprint,
doi:10.1101/2025.07.25.666730); Padfield et al. 2016 (Ecol. Lett.,
doi:10.1111/ele.12545; online 26 November 2015); Penn et al. 2018 (Science,
doi:10.1126/science.aat1327); Penn and Deutsch 2022 (Science,
doi:10.1126/science.abe9039); Penn and Deutsch 2024 (Phil. Trans. R. Soc. B,
doi:10.1098/rstb.2022.0487; deposit 2023); Qvarnström et al. 2024 (Nature,
doi:10.1038/s41586-024-08265-4); Rogger et al. 2024 (Science,
doi:10.1126/science.adn3450); Rogger et al. 2026 (Geosci. Model Dev.,
doi:10.5194/gmd-19-4931-2026); Ying et al. 2026 (Nature,
doi:10.1038/s41586-026-10541-4; Zenodo lists the depositor as "Rui, Ying";
Crossref gives the surname as Ying); Gómez-Suárez et al. 2025 (Sci. Data,
doi:10.1038/s41597-025-06379-6; the mirrored v3.2 postdates it); Smith et al.
2023 (Glob. Ecol. Biogeogr., doi:10.1111/geb.13735); Stockey et al. 2021
(PNAS, doi:10.1073/pnas.2101900118); Currano et al. 2021 (Palaeogeogr.
Palaeoclimatol. Palaeoecol., doi:10.1016/j.palaeo.2021.110636; code
deposited by Swain); Tang et al. 2024 (Science, doi:10.1126/science.adm9137);
Tsuboi et al. 2024 (J. Evol. Biol., doi:10.1093/jeb/voae103); Wang et al.
2025 (Proc. R. Soc. B, doi:10.1098/rspb.2025.0889); Gibbs et al. 2020 (Sci.
Adv., doi:10.1126/sciadv.abc9123; MCM model code deposited by Ward).

Indexed only: Gutarra et al. 2024 (Curr. Biol.,
doi:10.1016/j.cub.2024.04.059); Gutarra et al. 2025 (PNAS Nexus,
doi:10.1093/pnasnexus/pgaf346); Rogger et al. 2025 (Nat. Commun.,
doi:10.1038/s41467-025-66390-8); Kagawa and Seehausen 2020 (Proc. R. Soc. B,
doi:10.1098/rspb.2020.0941); Shum et al. 2026 (J. Geophys. Res. Atmos.,
doi:10.1029/2025jd044833).

Found by the second survey: Malanoski et al. 2026 (Science,
doi:10.1126/science.adv2627); Dunhill et al. 2018 (Palaeontology 61,
doi:10.1111/pala.12332; online 2017); Tang et al. 2024 (above); Holstad et
al. 2024 (Science, doi:10.1126/science.adi8722); Saupe et al. 2019 (Glob.
Ecol. Biogeogr., doi:10.1111/geb.12904); Syverson et al. 2018 (Paleobiology,
doi:10.1017/pab.2017.38; deposit 2017); Freitas et al. 2024 (J. Evol. Biol.,
doi:10.1093/jeb/voae035; deposit version of 2026); Holland and Patzkowsky
2015 (Palaeontology, doi:10.1111/pala.12188; deposit 2016); Kerr et al. 2025
(Ecography, doi:10.1111/ecog.07355); Alroy 2026 (Oikos,
doi:10.1002/oik.11607); Kontopoulos et al. 2020 (Evolution,
doi:10.1111/evo.13946); Xiong and Mallet 2022 (Evolution,
doi:10.1111/evo.14626); Cooper et al. 2024 (Nat. Commun.,
doi:10.1038/s41467-024-48434-7); Ontiveros et al. 2023 (Nat. Commun.,
doi:10.1038/s41467-023-41685-w; the FOAM set-up the simulation reuses);
Pohl et al. 2023 (Sci. Adv., doi:10.1126/sciadv.adg7679; cGENIE.muffin
v0.9.35 was archived for it). cGENIE.muffin, muffingen and the Liu, Penn and
Deutsch figure data are cited by their Zenodo DOIs (snapshots.tsv).

PANGAEA (CC BY 3.0): Naafs et al. 2010 (Earth Planet. Sci. Lett.,
doi:10.1016/j.epsl.2010.08.023; PANGAEA.736778); Bolton et al. 2010
(Paleoceanography, doi:10.1029/2010PA001951; PANGAEA.761442 and 761443);
Bolton et al. 2018 (Paleoceanogr. Paleoclimatol., doi:10.1029/2018PA003412;
PANGAEA.892803 and 892804).

## Verification log

- 2026-10-23, checked: 27 Dryad deposits mirrored with
  [register_deposits_snapshot.sh](register_deposits_snapshot.sh), each listed
  file verified against Dryad's checksum (sha256 for 130, md5 for 23); two
  over 5 GB indexed only; versions indexed
  ([dryad-versions.tsv](dryad-versions.tsv)).
- 2026-10-23, checked: 39 Zenodo records (two at two versions), 6 Figshare
  articles and 5 PANGAEA datasets mirrored with the same script; Zenodo and
  Figshare files verified against the providers' md5, PANGAEA's recorded by
  sha256 only; three Zenodo records over 5 GB indexed only. `data_mirror.py
  verify` passes on every deposit (0 failures).
- 2026-10-23, checked: a second survey of `ideas/`, `literature/`, `docs/`,
  `data/` and `papers/`, and of the files new on main, for every citation
  form (DOIs, record URLs, "Zenodo 1234567", Figshare portal prefixes),
  found the 19 deposits the first survey missed; all are now held. Every
  other match is held here, held by another entry, or listed in the
  backlog.
- [Detail withheld pending disclosure to the data custodian.]
- 2026-10-23, checked: profiled with the deposits profiler
  ([../au-fossil-deposits/deposits_profile.py](../au-fossil-deposits/deposits_profile.py),
  [output](profile/register_deposits_profile.tsv)).
- [Detail withheld pending disclosure to the data custodian.]
- 2026-10-23, checked (not committed code): Craffey et al.'s Figshare and
  Dryad zips compared member by member and row by row.
- 2026-10-23, checked (sha256, not committed code): the main checkout's
  hand-supplied copies match the mirror file for file.
- 2026-10-23, source claim: Dryad paper DOIs from the records'
  primary-article links; Zenodo, Figshare and PANGAEA papers from the
  records, the citing notes and Crossref (Claude Sonnet subagent); question
  links from the registers and notes.
- 2026-10-23, reviewed (Dryad tranche) by an independent Claude Sonnet
  subagent; its findings are applied above.
- 2026-10-23, reviewed (whole entry) by a second independent Claude Sonnet
  subagent. Its 16 findings are applied above: the missed deposits; the
  Monarrez and Al Aswad download dates and query routes; the descriptions of
  Tang, Currano, Tsuboi, Dunhill and Penn et al.; the checksum and Gutarra
  wording; and the Figshare and Zenodo version handling in
  `data_mirror.py`.
