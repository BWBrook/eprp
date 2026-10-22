---
id: au-fossil-deposits
name: Deposited datasets for Australia's flagship fossil biotas (Ediacaran to Holocene)
kind: deposit
status: active
last_update: 2026-05-15
scope:
  taxa: ["Ediacaran organisms", "Ediacaran assemblages worldwide (co-occurrence)", "Cambrian trilobites", "Permian bryozoans", "Eocene plants", "Quaternary mammals", "kangaroo teeth (microwear, enamel)", "pollen and charcoal"]
  time: "Ediacaran to Holocene"
  space: "Australia (Nilpena and the Flinders Ranges, Kangaroo Island, Riversleigh, Naracoorte, Cloggs Cave, Tasmania and others)"
  record_unit: "varies: a specimen's measurements, a site's taxon counts, a date, a sample's pollen or charcoal"
size:
  as_of: "2026-10-23"
  deposits: 16
  mirror_directories: 17
  mirrored_files: 42
  mirrored_bytes: 5945093
access:
  tier: open
  licence: "per deposit in snapshots.tsv: CC0 (Dryad deposits and their Zenodo copies); CC BY 4.0 (Figshare deposits, the revised Reichgelt record, Gutarra et al.); CC BY with no version stated (thylacine and devil dates)"
  routes:
    - {type: zenodo, url: "https://zenodo.org/api/records/", state: "open; Zenodo copies of Dryad deposits and the Gutarra et al. record; record ids in snapshots.tsv", checked: 2026-10-22}
    - {type: figshare, url: "https://api.figshare.com/v2/articles/", state: "open; Figshare and institutional Figshare articles; ids in snapshots.tsv", checked: 2026-10-22}
    - {type: dryad, url: "https://doi.org/10.5061/dryad.69p8cz9cc", state: "Craffey et al. 2024; mirrored through the Dryad API with a token (index open; downloads redirect to pre-signed storage)", checked: 2026-10-23}
    - {type: dryad, url: "https://doi.org/10.5061/dryad.4j0zpc8nf", state: "Arman et al. 2025; mirrored through the Dryad API with a token (index open; downloads redirect to pre-signed storage)", checked: 2026-10-23}
    - {type: dryad, url: "https://doi.org/10.5061/dryad.4b8gthtmd", state: "Couzens et al. 2026; mirrored through the Dryad API with a token (index open; downloads redirect to pre-signed storage)", checked: 2026-10-23}
  api: "Zenodo, Figshare and Dryad APIs (data_mirror.py)"
versioning:
  replay: exact
  notes: "each deposit is a fixed, DOI-versioned record; the Gutarra et al. file is a plain-URL snapshot of a Zenodo record, held with its sha256"
mirror:
  path: deep-server:/data/paleodata/au-fossil-deposits
  policy: "small open deposits with tabular data; scans, CT data and non-derivative licences documented only"
  state: "16 deposits in 17 directories (the Reichgelt deposit in two versions), 42 files, 5.9 MB, each directory with a manifest"
lineage:
  upstream:
    - "FosSahul (the thylacine and devil dates rate and select its records, keyed by FosSahul ID)"
    - "Riversleigh site richness: Dryad record 'Data from: The use of MSR (Minimum Sample Richness) for sample assemblage comparisons' (doi:10.5061/dryad.p1b6b, 2011-05-20)"
    - "Tasmanian pollen and wildfire: Dryad record 'Data from: Modern pollen from small hollows reflects Athrotaxis cupressoides density across a wildfire gradient in subalpine forests of the Central Plateau, Tasmania, Australia' (doi:10.5061/dryad.1bp06, 2018-05-31)"
    - "Thylacine and devil dates: Figshare record 'Supplementary Table 1 from High-quality fossil dates support a synchronous, Late Holocene extinction of devils and thylacines in mainland Australia' (doi:10.6084/m9.figshare.5746797.v1, 2018-01-02)"
    - "Dickinsonia growth: Dryad record 'Ediacara growing pains: Modular addition and development in Dickinsonia costata' (doi:10.5061/dryad.j9kd51cd4, 2021-08-17)"
    - "Permian bryozoan traits: Dryad record 'Data from: Trophic partitioning and feeding capacity in Permian bryozoan faunas of Gondwana' (doi:10.5061/dryad.fttdz08rt, 2021-05-15)"
    - "Estaingia growth: Figshare record 'Dataset from Complex axial growth patterns in an Early Cambrian trilobite from South Australia' (doi:10.6084/m9.figshare.17113370.v1, 2021-12-02)"
    - "Cloggs Cave mammals: Dryad record 'Interpreting the mammal deposits of Cloggs Cave (SE Australia), GunaiKurnai Aboriginal Country, through community-led partnership research' (doi:10.5061/dryad.kh1893298, 2022-10-19)"
    - "Eocene vegetation proxies: Dryad record and Zenodo record 'Data supplement to: Plant proxy evidence for high rainfall and productivity in the eocene of Australia' (doi:10.5061/dryad.59zw3r294 and doi:10.5281/zenodo.6462287, both 2022-05-02)"
    - "Dickinsonia species: Dryad record 'Data from: Species of Dickinsonia Sprigg from the Ediacaran of South Australia' (doi:10.5061/dryad.4j0zpc8ft, 2023-01-10)"
    - "Eoandromeda: Dryad record 'Data from: Elucidating the morphology and ecology of Eoandromeda octobrachiata from the Ediacaran of South Australia' (doi:10.5061/dryad.2jm63xsvg, 2023-11-14)"
    - "Naracoorte charcoal and pollen: Figshare record 'Cave opening and fossil accumulation in Naracoorte, Australia, through charcoal and pollen in dated speleothems - Supplementary Data 1' (doi:10.25375/uct.20495136.v1, 2024-01-15)"
    - "Tribrachidium: Figshare record 'A new species of the iconic triradial Ediacaran genus Tribrachidium, from Nilpena Ediacara National Park, Flinders Ranges (South Australia)' (doi:10.25909/25341625.v1, 2024-03-05)"
    - "Gutarra et al.: Zenodo record 'Community hydrodynamics created ecological opportunity in Ediacaran shallow marine ecosystems' (Zenodo 17035672, 2025-09-02; source claim, Zenodo record metadata)"
  downstream:
    - "SahulCHAR (its Naracoorte charcoal and age observations cite Weij et al. 2022)"
eprp_questions: []
citation:
  - "each deposit's DOI and its paper (snapshots.tsv; the profile lists files)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent; review fixes by a Claude Sonnet 5.5 subagent
  reviewed: "adversarial review 2026-10-22 (findings D1-D7) applied the same day; not re-reviewed"
---

# Deposited datasets for Australia's flagship fossil biotas

## Summary

Papers on Australia's best-known fossil biotas increasingly deposit their data
in Dryad, Zenodo or Figshare. This entry collects the openly licensed,
tabular ones and records what is missing. The main finding is negative: no
mirrored deposit holds bed-level or occurrence data for the Nilpena Ediacaran
biota or the other pre-Quaternary flagship biotas, and the source scan found
none elsewhere (source claim). There are no Nilpena bed maps or surface
censuses; the Emu Bay Shale, Gogo and Winton deposits the scan found are
phylogenetic matrices, CT scans and morphometrics (source claim). PBDB remains
the open occurrence source for these biotas. What deposits do offer is
specimen-level measurements (Ediacaran, Cambrian), taxon counts by excavation
unit for one Quaternary cave (Cloggs Cave), locality-level species richness
(Riversleigh), Quaternary dates, charcoal and pollen (Naracoorte, Tasmania) and
a thylacine and devil date table, and kangaroo dental microwear and enamel
across living and fossil species. One deposit (Craffey et al.) compiles
Ediacaran occurrences worldwide. We mirror 16 deposits (5.9 MB in all).

## Contents

Our inventory ([profile](profile/deposits_profile.tsv)) of the mirrored
deposits. Row counts are data rows after the header, excluding titles,
captions, footnotes and totals rows; "numeric" means at least half of a
column's filled cells are numbers (rules in
[deposits_profile.py](deposits_profile.py)).

| Deposit (directory) | Content | Licence |
| --- | --- | --- |
| Dickinsonia species, Nilpena (`dickinsonia-species`) | 304 specimen rows (303 distinct IDs; one ID appears twice), 27 columns: five labels (specimen, old ID, type, type notes, new ID) and 22 mostly numeric columns (measurements, counts and 0/1 codes; `--` marks a missing value) | CC0 |
| Dickinsonia growth (`dickinsonia-growth`) | a ReadMe sheet and five data sheets: length and width measurements for 55, 11 and 60 specimens in three (total and AMU dimensions, module counts; the 60-specimen sheet has AMU only), and module-by-module measurements in two wide sheets (41 and 61 rows, specimens side by side) | CC0 |
| Eoandromeda (`eoandromeda`) | 95 specimens' arm width, arm length and centroid size; four landmark (TPS) files holding 7, 74, 10 and 4 specimens; a landmark relabelling file (per the deposit's README) | CC0 |
| Tribrachidium (`tribrachidium`) | 46 and 57 specimens of two species (two CSVs), a specimen ID and 9 numeric variables each | CC BY 4.0 |
| Estaingia bilobata growth, Emu Bay Shale area (`estaingia-growth`) | 234 specimens: 19 length variables (CEL, TRL, PYL, FAL, PGL, ORL, LTS1 to LTS13) and `degree`, an ordinal stage code rather than a length (inferred from its name and integer values) | CC BY 4.0 |
| Gutarra et al. simulated communities (`gutarra-simulated-communities`) | four workbooks, 15 sheets, each a simulated community with x, y and a size: diameter for FUN5 (three simulations of 1,604 rows and three `Density900` sheets of 240 rows; one adds a height column) and Funisia clusters (24, 25 and 50 rows); length, width and orientation for DS (5 or 6 rows a sheet); KS adds a taxon column (6 or 7 taxa a sheet; 17 to 19 rows) | CC BY 4.0 |
| Permian bryozoan traits (`permian-bryozoan-traits`) | Permian: 204 data rows, of which 203 carry a taxon name (199 distinct) and one has none (it holds method citations in the diameter columns); modern: 67 rows (66 distinct taxa). Mouth, lophophore and tentacle-crown diameters (mm), with sources | CC0 |
| Eocene Australian vegetation proxies, Reichgelt et al. (`reichgelt-eocene-dryad`, `-revised`) | a README sheet and seven tables: S1 leaf physiognomy (111 rows, 25 columns), S2 calibration scores and climate (112 rows, 30 columns), S3 northern calibration sites (110 rows), S4 and S5 leaf size and margin by site (8 and 10 rows), S6 taxa at fossil sites with modern niches (90 taxon-site rows), S7 DeepMIP climate (108 rows, 26 columns); Dryad copy and revised version | CC0, CC BY 4.0 |
| Riversleigh site richness (`riversleigh-richness`) | Appendix 2: 84 Riversleigh localities (site ID with faunal zone, name, sampled species richness); Appendix 1: 167 Quercy and Limagne (French) localities in the same layout; Appendix 3 (.doc) not parsed | CC0 |
| Cloggs Cave mammals (`cloggs-cave-mammals`) | 38 taxon or category rows by 56 excavation units, and the same rows by 22 stratigraphic units; counts are NISP (sheet captions), 4,886 in total in each sheet. 24 rows are identified to species (4 of them `cf.`); 14 are indeterminate groups, five of them not mammals (three reptile groups, a frog group and birds), so the deposit is not mammals only | CC0 |
| Naracoorte charcoal and pollen, Weij et al. (`naracoorte-charcoal-pollen`) | Table 1 speleothem U-Th data (70 samples); Table 2 U-Pb isochron data (155 rows for 14 samples); Table 3 U-Th or U-Pb age with charcoal and pollen concentrations (70 samples; 65 with charcoal concentrations, the other five giving a U-Pb age only) | CC BY 4.0 |
| Tasmanian pollen and wildfire (`tasmania-pollen-fire`) | 50 modern surface samples with burn code and index (66 columns) and a 49-sample core with depths and ages (66 columns), plus R and MATLAB code | CC0 |
| Thylacine and devil dates (`thylacine-devil-dates`) | 277 date rows: 234 linked to FosSahul IDs and 43 new dates with none; 102 marked Accepted and 175 Rejected | CC BY (no version stated) |
| Ediacaran co-occurrence, Craffey et al. 2024 (`craffey-ediacaran-cooccurrence`) | a zip of data, results and R code: 1,540 occurrence rows (29 columns, PBDB-style: collection number, genus, coordinates, formation, lithology) in 415 collections and 278 genera worldwide, 340 of them (77 collections) in Australia, mostly the Rawnsley Quartzite (321); site-by-genus matrices for the Avalon, White Sea and Nama assemblages; co-occurrence results | CC0 |
| Kangaroo dental microwear, Arman et al. 2025 (`arman-kangaroo-microwear`) | S1: 2,650 microwear rows for 960 specimens (genus, species, tooth facet and position, macrowear stage, ecoregion, island, age, texture parameters), an ANOVA subset (937 rows) and test summaries; S2: model-selection tables per texture parameter | CC0 |
| Kangaroo enamel, Couzens et al. 2026 (`couzens-kangaroo-enamel`) | a zip of data and R code: 282 enamel measurement rows for 246 specimens of 76 macropodoid taxa (157 fossil, 125 modern rows; estimated ages 0 to 24.1 Ma; 42 assemblage labels), per-taxon summaries (68 taxa), enamel maps, body-mass compilations, a 2,408-row marsupial herbivore occurrence table and PBDB genus extracts; paper in Science 392: 488-492 (per its README) | CC0 |

**Documented, not mirrored** (source claims from the source scan unless
stated):

- *Non-derivative licences* (CC BY-NC-ND): Kimberella from Nilpena, Perth
  Basin Permian-Triassic invertebrates, Winton palynology, Talbragar and
  Koonwarra teleosts, among others.
- *Matrices, scans and CT data*: Emu Bay Shale chelicerates and radiodonts,
  Gogo fishes (MorphoSource media mostly restricted), Riversleigh and Winton
  matrices, Lightning Ridge CT data (1.1 GB), Trilophosuchus (937 MB),
  Pallimnarchus (660 MB), and the 38.5 GB set of Ediacaran fluid-dynamics
  simulations (the size is also in the Zenodo record metadata, read
  2026-10-22).
- *Code*: Ediacaran biomass networks (GitHub, GPL-3.0), which hold the only
  per-square-metre abundances for a Nilpena bed, inside the source code.

## Provenance and lineage

Supporting data of papers in palaeontology and Quaternary science. The
mirrored records were published from 2011-05-20 (Riversleigh) to 2024-03-05
(Tribrachidium) by their manifests (checked, profile), and the Gutarra et al.
Zenodo record on 2025-09-02 (Zenodo record metadata, read 2026-10-22; the mirror holds an
undated URL snapshot). Most Dryad deposits have an open copy on Zenodo carrying
the Dryad DOI (50 of 58, source scan), which is how we mirror them; the copies
matched Dryad's stored size in 38 of 40 comparable cases (source scan).

The thylacine and devil dates are keyed to FosSahul IDs, so FosSahul is their
upstream; SahulCHAR's Naracoorte charcoal and age observations cite the Weij et
al. paper, so SahulCHAR is downstream of that deposit (see Overlap).

**The Reichgelt deposit, two records.** The Dryad copy on Zenodo (record
6511559; carries the Dryad DOI 10.5061/dryad.59zw3r294; `supplementary_tables.xlsx`
and a README; CC0) and a Zenodo record (6462287; concept DOI
10.5281/zenodo.6462286; `supplementary_tables_revised.xlsx`; CC BY 4.0). Both
show publication date 2022-05-02. The Zenodo API lists one version for each
(checked, [reichgelt-zenodo-versions.tsv](reichgelt-zenodo-versions.tsv)), so
the concept record holds no other versions. The record 6462287 metadata lists
the Dryad DOI as the source it derives from (source claim, Zenodo record
metadata). The sheet-by-sheet differences are in Weaknesses.

## Structure

Spreadsheets and CSVs, one or a few per deposit, with READMEs; the profile
lists each file's sheets, data rows, columns, numeric columns and headers, and
distinct IDs or taxa where a column holds them. Files not parsed: the
Riversleigh Appendix 3 (.doc) and the Tribrachidium README (.docx). The
Riversleigh Appendix 1 (.xls) is read with xlrd.

## Access

- **Mirror.** `deep-server:/data/paleodata/au-fossil-deposits/<deposit>/raw/`
  with manifests; versions indexed per deposit. Index:
  [snapshots.tsv](snapshots.tsv). Rebuild the profile with `uv run
  deposits_profile.py DIR profile/deposits_profile.tsv`; the overlap script's
  usage line names its inputs.
- **Dryad.** `data_mirror.py dryad DOI DEST --index-only` indexes any Dryad
  deposit without a token ([dryad-versions.tsv](dryad-versions.tsv));
  `data_mirror.py dryad DOI DEST --latest` downloads it with the Dryad API
  account on deep-server (credentials outside the repository; see the
  catalogue README), verifying Dryad's sha256 for each file.

## Strengths

- Specimen-level measurements for Ediacaran and Cambrian taxa, ready for
  morphometric and ontogenetic analysis.
- Dated Quaternary series: Naracoorte (U-Th and U-Pb ages with charcoal and
  pollen) and the Tasmanian core (ages). Cloggs Cave counts are by excavation
  and stratigraphic unit, with no ages in the file.
- Fixed, citable versions; small enough to mirror whole.

## Weaknesses and pitfalls

- **No bed-level or occurrence data for the flagship biotas.** Bed-level
  Nilpena data exist only as simulations, as code, or with their authors. The
  Cloggs Cave counts are the one occurrence-type table, and Quaternary.
- **Heterogeneous formats.** Each deposit has its own layout; several put
  their README inside a spreadsheet sheet or in a .docx. Missing values are
  written `--`, `n/a`, `N/A`, `NA` or left blank, depending on the deposit.
- **Sheet dimensions are not row counts.** Totals, captions, one-cell cave
  headings and a method-notes row sit inside the data blocks (Cloggs: 41 rows,
  38 taxa; Naracoorte Table 1: 70 samples among 19 one-cell rows). Naracoorte
  Table 2 gives the cave and sample ID on the first row of each sample only (14
  filled in 155 rows). Wide sheets (Dickinsonia module data) put specimens side
  by side.
- **Thylacine and devil "Accepted" and "Rejected" follows FosSahul's quality
  categories, not a separate test.** Accepted is QR category A or A* (58 A, 44
  A*); rejected is B (38) and C (129), plus eight A-rated rows, all U-series
  dates on indirectly associated material, with no reason in the sheet. The
  sheet covers 234 of FosSahul's 370 *Thylacinus* and *Sarcophilus* records plus
  43 new dates (Overlap).
- **FosSahul IDs in that sheet are not guaranteed.** ID 8261 points at a
  different record in the current FosSahul (Overlap), and the deposit's AgeID or
  coordinates differ from FosSahul's for other rows.
- **The two Reichgelt records carry the same numbers.** Compared sheet by sheet
  (checked, [overlap output](profile/deposits_overlap.tsv)): the README sheet
  and S2, S3, S4, S5 and S7 are identical cell for cell. S6 holds the same 90
  taxon-site rows with the same values in a different order; its GBIF download
  DOIs are bare in the Dryad copy and carry a `https://doi.org/` prefix in the
  revised file (88 cells with one prefix, 2 with it doubled). S1 gains a
  `geographic area` column in its fossil-site block (8 values: South Australia
  4, Victoria 2, Queensland 1, New South Wales 1), which shifts that block's
  other columns right. No other cell differs in value. We found no reason to prefer
  one record on content: use the one that matches the paper's citation, and note
  the licence (CC0 for the Dryad copy, CC BY 4.0 for the revised record).
- **Not Australian throughout.** The Riversleigh deposit's Appendix 1 lists 167
  Quercy and Limagne (French) localities (checked). The source scan reports that
  the Gutarra simulations include Russian surfaces; the mirrored files carry
  only coordinates and sizes, so this cannot be checked from them (source claim).

## Overlap with other sources

[deposits_overlap.py](deposits_overlap.py) ([output](profile/deposits_overlap.tsv)),
all checked unless marked:

- **FosSahul, links.** All 234 thylacine and devil rows with a FosSahul ID are
  in the March 2021 CSV, with the same genus in 234 of 234. The AgeID is the
  same in 211; it is NA in the deposit for 21 (FosSahul also NA for 4) and a
  different code for two: ID 8214 (GaK-3814 against GaK-3888, same place) and
  ID 8261 (Wk-36184 in New South Wales against Y-1367 in Papua New Guinea's
  Eastern Highlands). Coordinates agree within 0.05 degrees for 213, differ for
  20 and are not numeric for one. So the IDs resolve, but the deposit's
  AgeIDs and coordinates differ from FosSahul's current ones for some rows, and
  ID 8261 points at a different record.
- **FosSahul, the accept or reject decision.** Against FosSahul's current
  Quality, the 59 accepted linked records are A 47, B 6, C 6 and the 175
  rejected are A 8, B 61, C 106. The deposit's own QR category is A or A* for
  every accepted row (58 A, 44 A*) and B, C or A for the rejected ones (38, 129,
  8); it equals FosSahul's current Quality for 155 of the 234 linked rows (C to
  B 44, B to C 21, A to B 6, A to C 6, C to A 1, A* to C 1 differ). The 43 new
  dates are all A*, from Western Australia (28), Victoria (14) and New South
  Wales (1).
- **FosSahul, authorship.** Saltré and Bradshaw are creators of both the
  deposit's Figshare record and the FosSahul 2.0 record (record creator lists in
  the mirror manifests: 4 and 8 creators); paper authorship was not checked.
- **FosSahul, coverage.** FosSahul holds 370 *Thylacinus* and *Sarcophilus*
  records. 234 are linked by ID. The deposit's 43 new dates are all in FosSahul
  too, found by AgeID (IDs 9303 to 9345, all publication year 2018). The
  remaining 93 are not in the deposit: Tasmania 19; Papua New Guinea (Nombe
  Rockshelter, Simbu) 30; Kangaroo Island 32 (Kelly Hill Cave and Seton
  Rockshelter; 2013 and 2015; Quality A 8, B 22, C 2); and 12 from Kudjal
  Yolgah Cave in Western Australia (2016, all B, IDs 9715 to 9857). The first
  three groups fall outside "mainland Australia"; the deposit does not say why
  the Kudjal Yolgah records are absent, and their IDs lie above every ID the
  deposit links (inferred: added to FosSahul later).
- **Cloggs Cave.** FosSahul holds 20 dated records from the site and PBDB one
  collection; SahulCHAR has no unit there. The mirrored sources hold no
  excavation-unit counts other than this deposit (inferred; the PBDB collection's
  occurrences were not examined).
- **SahulCHAR and Naracoorte.** Six SahulCHAR units cite Weij et al. 2022
  (doi:10.1038/s43247-022-00538-y): Alexandra, Blanche, Dead Sheep, New,
  Specimen and Victoria Fossil caves. 113 observation rows cite it (57 charcoal
  counts and 56 ages, on 60 samples), and they include four rows for a seventh
  unit, Robertson Cave, whose unit record is not among the six. All 57 SahulCHAR
  charcoal values occur among the deposit's 65 charcoal concentrations (matched
  by value, not sample by sample); 8 of the deposit's values are not in
  SahulCHAR, and the rows citing the paper are ages and charcoal counts only, so
  its pollen concentrations are not in SahulCHAR.
- **PBDB.** Craffey et al.'s Ediacaran occurrences carry PBDB-style
  collection numbers and fields; they were compiled from PBDB and the
  literature (source claim). Of their 77 Australian collections, 36 match a
  collection in our PBDB Australian extract; the other 41 are presumably
  literature compilations or collections changed since (inferred, not
  checked).
- **FosSahul and PBDB, kangaroos.** Couzens et al.'s 76 macropodoid taxa
  span 43 genera, 24 of them in FosSahul; their deposit also bundles PBDB
  genus extracts and a 2,408-row marsupial herbivore occurrence table.

## EPRP relevance

Morphometric data for Ediacaran and Cambrian questions; dated Quaternary
records (megafauna, fire, vegetation) that complement FosSahul, SahulCHAR and
Neotoma; and an inventory of where Australian occurrence data are missing.

## Citation and terms

Cite each deposit's DOI and its paper; CC0 and CC BY terms as listed. For
Reichgelt et al., cite the record you used; the Dryad copy is CC0 and the
revised record CC BY 4.0.

## Verification log

- 2026-10-22, checked ([deposits_profile.py](deposits_profile.py),
  [output](profile/deposits_profile.tsv)): 17 mirror directories holding 42
  files and 5,945,093 bytes; each manifest's title, DOI, publication date and
  licence; per sheet or table, data rows, columns, numeric columns and distinct
  IDs or taxa; .xls files (xlrd) and the .xlsx members of the Gutarra zip read;
  the .doc and .docx files reported as not parsed; authors' email addresses
  redacted from echoed text.
- 2026-10-22, checked (`data_mirror.py verify` on each deposit directory,
  [output](profile/mirror_verify.txt), rerun 2026-10-23): 42 of 42 files re-hash to the sha256 in
  their manifests. The tool records that hash after comparing the provider's size
  and checksum at download (tool documentation).
- 2026-10-22, checked ([deposits_overlap.py](deposits_overlap.py),
  [output](profile/deposits_overlap.tsv)): thylacine and devil rows against
  FosSahul (ID, genus, AgeID, coordinates, QR category, current Quality,
  coverage, AgeID match of the new dates, shared record creators); Cloggs Cave
  taxon rows and totals, and the site against FosSahul, PBDB and SahulCHAR;
  SahulCHAR units and observations citing Weij et al. 2022 against the Naracoorte
  Table 3 charcoal values; the two Reichgelt versions sheet by sheet.
- 2026-10-22, checked (`data_mirror.py zenodo RECORD DEST --index-only` on
  records 6462287 and 6511559, [reichgelt-zenodo-versions.tsv](reichgelt-zenodo-versions.tsv)):
  one version each. `data_mirror.py dryad DOI DEST --index-only` on the three
  Dryad-only DOIs ([dryad-versions.tsv](dryad-versions.tsv)): one version each,
  with file names, sizes and sha256.
- 2026-10-23, checked: the three Dryad deposits mirrored with
  `data_mirror.py dryad DOI DEST --latest` (Dryad API account), each file
  matching Dryad's sha256; all seven files are byte-identical to Barry's
  hand-downloaded copies. Profiled by [deposits_profile.py](deposits_profile.py)
  (now reading CSV members of zips); Craffey and Couzens counts and overlaps
  by [deposits_overlap.py](deposits_overlap.py).
- 2026-10-22, source claim (Zenodo record metadata, open GET, not committed):
  Gutarra et al. record 17035672 published 2025-09-02, with the 300,730-byte
  communities zip and a 38,496,573,147-byte CFD zip; record 6462287 lists the
  Dryad DOI as the source it derives from.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): the search
  for occurrence and census deposits across Dryad, Zenodo, Figshare, DataCite,
  PANGAEA and OSF; the 50 of 58 Dryad deposits with Zenodo copies and the 38 of
  40 size matches; the contents and licences of the documented-not-mirrored
  deposits; Russian surfaces in the Gutarra simulations; Craffey et al.'s
  compilation from PBDB.
- 2026-10-22, inferred: `degree` in the Estaingia file is an ordinal stage code;
  the Kudjal Yolgah records were added to FosSahul after the deposit; no
  excavation-unit counts for Cloggs Cave exist in the other mirrored sources.
