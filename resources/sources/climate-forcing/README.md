---
id: climate-forcing
name: Climate-forcing series and event tables — PhanDA, PhanSST, Scotese 2021, Song 2021, CENOGRID, LR04, Rothman 2017 carbon events, Green 2022 LIPs and impacts
kind: compilation
status: active
last_update: "PhanDA head 2026-03-09; PhanSST GitHub head 2023-03-09 (DOI release v0.0.1-beta, 2022-11-03); the others are fixed publications (2005-2022)"
scope:
  taxa: ["not taxonomic: temperature, CO2, benthic isotopes, carbon-cycle events, volcanic provinces, impacts"]
  time: "Phanerozoic (PhanDA 0-486.85 Ma; Scotese 100 intervals; Rothman 0.02-541 Ma); Cenozoic (CENOGRID 0-67.1 Ma); LR04 0-5.32 Ma"
  space: "global"
  record_unit: "varies: a stage slice's GMST and CO2 percentiles; a proxy SST measurement; a dated benthic isotope sample; an event or province"
size:
  as_of: "2026-10-23"
  phanda_stage_slices: 85
  phansst_rows: 151259
  raw_files: 1271
  mirrored_bytes: 659563447
access:
  tier: unclear
  licence: "mixed: Scotese 2021, Song 2021, CENOGRID CC BY 4.0; Rothman 2017 CC BY-NC 4.0; Green et al. 2022 article CC BY-NC-ND 4.0; LR04 NOAA NCEI (no restriction stated); PhanSST's Zenodo release 'other-open'; the PhanDA, PhanSST and Green et al. GitHub repositories state no licence"
  routes:
    - {type: github, url: "https://github.com/EJJudd/PhanDA", state: "head 9f06c0d (2026-03-09), the commit the main project pins; 34 commits indexed", checked: 2026-10-23}
    - {type: github, url: "https://github.com/EJJudd/PhanSST", state: "head 32cc98e (2023-03-09); 30 commits indexed", checked: 2026-10-23}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.7049233", state: "PhanSST DOI releases v0.0.1-alpha and v0.0.1-beta (mirrored)", checked: 2026-10-23}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.8237750", state: "PhanDA HadCM3L priors (version 8237751), 11.4 GB: indexed, not mirrored", checked: 2026-10-23}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.5027293", state: "Song et al. 2021 data and R code", checked: 2026-10-23}
    - {type: zenodo, url: "https://zenodo.org/records/8238875", state: "Scotese et al. 2021 GMST maps, version scotese02a_v21321 (C1)", checked: 2026-10-23}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.917503", state: "CENOGRID collection (27 datasets, Tables S8-S34), as zip; the collection has no text format", checked: 2026-10-23}
    - {type: web, url: "https://www.ncei.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/", state: "LR04 stack; the author's copy (lorraine-lisiecki.com) also mirrored", checked: 2026-10-23}
    - {type: api, url: "https://www.ebi.ac.uk/europepmc/webservices/rest/", state: "Rothman 2017 full text (PMC5606709) and Green et al. 2022 supplement (PMC9499591); PMC itself serves a reCAPTCHA to scripts", checked: 2026-10-23}
    - {type: github, url: "https://github.com/Theodore-Green/LIP-Extinction-Correlations", state: "Green et al.'s code and data tables, head e3038b5 (2023-03-21); 18 commits indexed", checked: 2026-10-23}
  api: "Europe PMC REST; Zenodo; PANGAEA"
versioning:
  replay: exact
  notes: "PhanDA, PhanSST and Green et al.'s code are git repositories (every commit indexed; heads mirrored, PhanDA's being the commit the main project pins); PhanSST also has two Zenodo releases; the rest are fixed deposits or article supplements"
mirror:
  path: deep-server:/data/paleodata/climate-forcing
  policy: "the forcing series and event tables the registers cite; model priors over 5 GB indexed only"
  state: "ten routes mirrored and one indexed; 1,271 files (660 MB), each with a manifest; all verify. Derived: climate-forcing/derived/2026-10-23/"
lineage:
  upstream:
    - "PhanDA: data assimilation of PhanSST proxies with HadCM3L priors (Judd et al. 2024, doi:10.1126/science.adk3705)"
    - "CENOGRID: Westerhold et al. 2020 (Science); LR04: Lisiecki and Raymo 2005 (Paleoceanography); Rothman 2017 (Science Advances); Green, Renne and Keller 2022 (PNAS); Scotese et al. 2021 (Earth-Science Reviews); Song et al. 2021 (Nature Communications)"
  downstream:
    - "the main project's interval crosswalk and PhanDA stage-difference analyses (data/interval-crosswalk, data/phanda-stage-differences), pinned to the same PhanDA files"
eprp_questions: [Q-003, Q-007, Q-011, Q-019, Q-027, Q-030, Q-050, B-018]
citation:
  - "Judd, E. J. et al. (2024) A 485-million-year history of Earth's surface temperature. Science, doi:10.1126/science.adk3705 (PhanDA)"
  - "Judd, E. J. et al. (2022) PhanSST. Scientific Data, doi:10.1038/s41597-022-01826-0"
  - "Scotese, C. R., Song, H., Mills, B. J. W. & van der Meer, D. G. (2021) Phanerozoic paleotemperatures. Earth-Science Reviews 215: 103503"
  - "Song, H. et al. (2021) Thresholds of temperature change for mass extinctions. Nature Communications, doi:10.1038/s41467-021-25019-2"
  - "Westerhold, T. et al. (2020) An astronomically dated record of Earth's climate and its predictability over the last 66 million years. Science (CENOGRID; PANGAEA doi:10.1594/PANGAEA.917503)"
  - "Lisiecki, L. E. & Raymo, M. E. (2005) A Pliocene-Pleistocene stack of 57 globally distributed benthic d18O records. Paleoceanography 20: PA1003, doi:10.1029/2004PA001071"
  - "Rothman, D. H. (2017) Thresholds of catastrophe in the Earth system. Science Advances 3: e1700906, doi:10.1126/sciadv.1700906"
  - "Green, T., Renne, P. R. & Keller, C. B. (2022) Continental flood basalts drive Phanerozoic extinctions. PNAS 119: e2120441119, doi:10.1073/pnas.2120441119"
entry:
  created: 2026-10-23
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-23, independent Claude Sonnet subagent; findings applied"
---

# Climate-forcing series and event tables

## Summary

Many EPRP questions, including several no source yet serves, need a forcing
series: a temperature, CO₂ or carbon-cycle record to set against extinction
and origination. This entry gathers the series and event tables the registers
cite:

- **Phanerozoic temperature:**
  - PhanDA, the data-assimilated GMST and CO₂ by stage;
  - PhanSST, the proxy database it assimilates;
  - Scotese et al. 2021, GMST maps for 100 intervals;
  - Song et al. 2021, temperature thresholds for mass extinctions.
- **Cenozoic and Plio-Pleistocene benthic isotopes:** CENOGRID and LR04.
- **Event tables:**
  - Rothman's 31 carbon-isotope events;
  - Green, Renne and Keller's tables of stage-boundary extinction magnitudes,
    large igneous provinces, impacts, Rothman-method CO₂ calculations and
    predicted extinction magnitudes.

The main project already uses PhanDA and Song 2021. Our PhanDA files match the
SHA-256 pins in `data/interval-crosswalk/sources.tsv`, and so does Song's
extinction-rate script.

Green et al.'s tables come from two places: their SI appendix (PDF) and their
own data repository. We parsed the PDF and checked the parse against the
repository: 102 of 102 boundaries, 33 of 35 LIPs (two not found by name, none
differing) and 24 of 24 impacts agree.

## Contents

From [profile/climate_forcing_profile.tsv](profile/climate_forcing_profile.tsv).

| Route | What | Size |
| --- | --- | ---: |
| `phanda` | PhanDA repository at 9f06c0d: GMST and CO₂ percentiles for 85 slices (0–486.85 Ma), the GMST ensemble (`.mat`), 85 slice files of surface-temperature gradients, code | 1,218 files, 517 MB |
| `phansst` | PhanSST at its GitHub head: `PhanSST_v001.csv` (151,259 proxy rows), a 663-row reference list, a template | 4 files, 43 MB |
| `phansst-zenodo` | PhanSST's DOI release v0.0.1-beta (150,691 rows) | 1 zip, 2.6 MB |
| `phanda-hadcm3l-priors` | PhanDA's model priors: indexed only | (11.4 GB) |
| `song2021-temperature-thresholds` | Database S1 (Excel) and two R scripts | 3 files, 1.3 MB |
| `scotese2021-gmst` | GMST for 100 Phanerozoic intervals, as grids, lists and netCDF, with a methods PDF | 5 files, 91 MB |
| `cenogrid` | Westerhold et al. 2020: the PANGAEA collection's 27 tables (S8–S34), including the splice (24,321 samples, 0–67.1 Ma, Table S33) and the binned and smoothed series (Table S34, 23,629 rows) | 1 zip, 1.8 MB |
| `lr04` | LR04 stack, 2,115 rows (0–5,320 ka, at 1–5 kyr steps), from NOAA and from the author's site | 2 files, 0.4 MB |
| `rothman2017-carbon-events` | the article's full text; its Table 1 lists the 31 carbon-isotope events (0.02–541 Ma) | 0.2 MB |
| `green2022-lips` | the supplementary files (SI appendix PDF and figures) and the full text | 2 files, 2.3 MB |
| `green2022-code` | the authors' repository: Julia code, `data/` tables (LIPs with and without oceanic provinces, boundaries, impacts) and results | 34 files, 0.15 MB |

- **PhanDA.**
  - The 85 slices are 78 single stages, 6 merged pairs (Selandian/Danian,
    Sinemurian/Hettangian, Anisian/Olenekian, Capitanian/Wordian,
    Pragian/Lochkovian, Aeronian/Rhuddanian) and the PETM.
  - The median GMST ranges from 11.4 °C (Upper Pleistocene) to 35.6 °C
    (Turonian).
  - The median CO₂ ranges from 239 ppm (Chibanian) to 3,326 ppm (Floian).
- **PhanSST** (proxy codes as the PhanSST ReadMe defines them):

  | Proxy | Code | Rows |
  | --- | --- | ---: |
  | Calcite δ¹⁸O | `d18c` | 81,709 |
  | Alkenone U^K'_37 | `uk` | 35,360 |
  | TEX86 | `tex` | 14,091 |
  | Planktonic-foraminiferal Mg/Ca | `mg` | 13,249 |
  | Conodont phosphate δ¹⁸O | `d18p` | 6,379 |
  | Aragonite δ¹⁸O | `d18a` | 471 |

  - **Sources.** 1,247 site names (1,396 with the hole), 635 lead-author-year
    pairs, 662 DOIs (469 rows lack one), and 663 references in the list.
  - **Ages.** Heavily Cenozoic: 63,089 Quaternary and 41,721 Neogene rows
    against 92 Cambrian; median 3.6 Ma. Ages are on GTS2020 (ReadMe).
    - 38,834 rows have ages from relative information (AgeFlag 1 or 2).
    - Four ages are slightly negative.
  - **Flags.**
    - The diagenesis flag is empty in 52,358 rows (35%).
    - The value type is blank in 5,438.
  - **Versions.** The GitHub head (2023-03-09) has 568 more rows than the DOI
    release v0.0.1-beta (2022-11-03).
- **Derived** (`climate-forcing/derived/2026-10-23/`):
  - `rothman2017_events.tsv`: event, abbreviation, date, δ1 at the start and
    after τ_env, Δr, τ_env, φ, M.
  - `green2022_table_S1.tsv` to `S5.tsv`. Tables in two column blocks are
    joined on the row number.
    - **S1:** 102 stage boundaries with age, 1σ, and Muscente et al.'s
      corrected diversity and extinction rates.
    - **S2:** 35 LIPs with start and end ages and their 1σ, duration, volume
      and eruption rate (25 have a rate).
    - **S3:** 24 impacts of 20 km or more.
    - **S4:** 26 rows: the LIPs, the present and the SSP scenarios. Each has
      τ_env, dimensionless duration T, volume, CO₂ mass change Δm and
      dimensionless M at two CO₂ contents.
    - **S5:** 13 LIPs with predicted and observed extinction magnitudes.

## Provenance and lineage

- **PhanDA, PhanSST and the priors.**
  - PhanDA assimilates PhanSST proxies into HadCM3L model priors, slice by
    slice (Judd et al. 2024). The PhanDA README cites PhanSST.
  - The priors are Zenodo concept 8237750 (version 8237751).
  - PhanDA's slice boundaries and PhanSST's ages are on GTS2020 (PhanSST
    ReadMe; the main project's PhanDA notes).
- **Scotese et al. (2021).** HadCM3L simulations adjusted to δ¹⁸O proxies.
  Version scotese02a_v21321 (C1) is the newer of two Zenodo versions; only the
  netCDF zip differs between them.
- **Song et al. (2021).** Database S1 and the R code behind its thresholds of
  temperature change.
- **CENOGRID.** The astronomically tuned Cenozoic benthic δ¹³C and δ¹⁸O
  reference (Westerhold et al. 2020). The PANGAEA collection holds 27
  datasets, Tables S8–S34; Tables S1–S7 are not on PANGAEA. PANGAEA serves
  the collection only as a zip.
- **LR04.** NOAA's file holds the stack, then sedimentation rates and the
  conversion tables between earlier age models and LR04. Its stack block is
  identical to the author's file at all 2,115 rows.
- **Event tables.**
  - Rothman (2017) compiled 31 Phanerozoic carbon-isotope excursions, dated
    on an older scale (the K–Pg at 65.50 Ma).
  - Green et al. (2022) compiled LIPs and impacts against PBDB-derived
    extinction magnitudes (Muscente et al.). Their data availability
    statement names the SI tables and the GitHub repository, and their Table
    S1 gives boundary ages on GTS2012 unless noted.

## Access

- **Terms.**
  - Scotese 2021, Song 2021 and CENOGRID are CC BY 4.0.
  - Rothman 2017 is CC BY-NC 4.0, and the Green et al. 2022 article CC
    BY-NC-ND 4.0 (from the full-text XML).
  - LR04 comes from NOAA's World Data Service, with no restriction stated.
  - PhanSST's Zenodo releases say "other-open", without naming the licence.
  - **The PhanDA, PhanSST and Green et al. GitHub repositories state no
    licence.** We hold private copies under Barry's universal approval of 23
    October 2026: "Licence overrides confirmed, universally for the EPRP.
    Mirroring locally is always okay for us: we're not hosting anything here
    for public use, except perhaps later for the frameworks, but not the
    actual source files." The licence questions for reuse are queued as
    CONTACTS C29 and C30.
- **PMC.** It now answers scripted requests with a reCAPTCHA. Europe PMC's
  REST API (`fullTextXML`, `supplementaryFiles`) serves the same files openly.
- **Rebuild.** On deep-server, in a login shell. The tools are deployed as
  `/data/paleodata/_tools/climate-forcing_climate_forcing_snapshot.sh` and
  `climate-forcing_climate_forcing_profile.py`:

  ```sh
  climate_forcing_snapshot.sh [phanda] [phansst] [phansst-zenodo] [greencode] [priors] [song] [scotese] [cenogrid] [lr04] [rothman] [green]
  uv run climate_forcing_profile.py /data/paleodata/climate-forcing /data/paleodata/climate-forcing/derived/2026-10-23 \
      profile/climate_forcing_profile.tsv
  ```

  PhanDA is fetched from GitHub file by file (1,218 files); here it took
  about half an hour (observed, file times). The profiler needs `pdftotext`.

## Strengths

- **The forcing series behind the registers, at fixed versions.** PhanDA's
  files match the main project's pins byte for byte.
- **Machine-readable event tables, independently checked.** The LIP, impact,
  boundary, carbon-event and CO₂ tables were PDF or HTML in the papers. They
  are now TSVs, checked against the authors' own data tables where those
  exist.

## Weaknesses and pitfalls

- **PhanDA's slices are not independent.**
  - It assimilates each slice separately, so there is no joint temporal
    posterior (the main project's `data/phanda-stage-differences` treats
    this).
  - Six slices merge two stages, and one is the PETM.
- **Some of Green et al.'s σ are not uncertainties.** In 18 boundaries of
  Table S1 (rows 2–16 and 20–22: the Quaternary and Neogene) the comment
  column says "1σ is least significant digit". Those σ values (0.0001–0.01
  Myr) record rounding, not measurement uncertainty.
- **PhanSST is Cenozoic-heavy.**
  - 69% of its rows are Neogene or younger.
  - A quarter of ages come from relative information.
  - A third of rows have no diagenesis flag.
- **Time scales differ.**
  - Green et al. use GTS2012, and PhanDA and PhanSST GTS2020.
  - CENOGRID and LR04 have astronomically tuned age models.
  - Rothman's dates use an older scale.
  - Put them on one scale before comparing ([timescale](../timescale/README.md)).
- **Green's S2 names differ from the repository.**
  - Two LIPs in the SI are not under the same names in the repository's
    tables: Viluy (Yakutsk), and Central Iapetus (Baltoscandian, Egersund).
  - Use the repository tables (they add continental or oceanic, locations
    and coordinates) and keep the SI parse as a cross-check.
- **The priors are not mirrored.** At Zenodo's 0.2–0.3 MB/s per connection
  (catalogue lessons), the 11.4 GB would take ten hours or more. Fetch them on
  demand with `data_mirror.py zenodo 8237751`.
- **Rothman's table header** uses the article's symbols (δ1, τ_env, φ, M);
  see the article for definitions.

## Overlap with other sources

- **Main project.** `data/interval-crosswalk/sources.tsv` pins SHA-256 values
  for PhanDA's percentile and ensemble files and Song's extinction-rate
  script. The files here match those pins. The main project's copies are
  git-ignored and were not compared.
- **Time scale.** Green et al.'s Table S1 boundaries are GTS2012 and can be
  compared with the RDF release of 2012 ([timescale](../timescale/README.md)).
- **Australia.**
  - Green et al.'s Table S2 lists six Australian provinces in seven rows:
    Whitsunday, Bunbury, Gascoyne Margin, Kennedy–Connors–Auburn, and the
    Kalkarindji volcanics and sills. That Kennedy–Connors–Auburn is in north
    Queensland is recall.
  - Their Table S3 lists the Tookoonooka impact (Queensland, 55 km,
    125 ± 1 Ma).

## EPRP relevance

- **Q-030.**
  - Its data line lists "LIP eruptive rates and CO₂ estimates from the Green
    2022 supplement". These are Tables S2, S4 and S5 here.
  - The 13–14 October checkpoint notes call for an outcome-independent
    forcing catalogue, which this entry starts.
  - PhanDA and Rothman's events are named in the register. Song 2021 appears
    under its forcing proxies.
- **Q-003 (threshold or smooth response):** PhanDA and Song 2021.
- **Q-011:** Song 2021 and the event tables.
- **Q-027 and Q-019:** PhanDA (and CENOGRID for Q-027).
- **Q-007:** PhanSST and CENOGRID.
- **Q-050:** LR04.
- **B-018:** PhanDA.
- **Unserved questions, inferred:** the same series serve Q-015 (thermal
  niches), Q-021 (Earth-system recovery) and Q-035 (land–sea lags).

## Citation and terms

Cite each source as listed in the front matter, and the deposits by DOI.
Rothman's and Green et al.'s tables are non-commercial; Green et al.'s also
no-derivatives. Use the derived TSVs for analysis, not for redistribution.

## Verification log

- 2026-10-23, checked: mirrored with
  [climate_forcing_snapshot.sh](climate_forcing_snapshot.sh). The CENOGRID
  leg was rerun as a zip after the text format was refused. All 1,271 files
  re-verify. Indexes: [snapshots.tsv](snapshots.tsv) and
  [versions.tsv](versions.tsv): PhanDA 34 commits, PhanSST 30 and two Zenodo
  releases, Green et al. 18 commits, and the Zenodo versions.
- 2026-10-23, checked: [climate_forcing_profile.py](climate_forcing_profile.py)
  ([output](profile/climate_forcing_profile.tsv)), run on deep-server.
  - The PhanDA files and Song's script match the main project's SHA-256 pins.
  - The Green S1–S3 parses agree with the authors' repository tables.
- 2026-10-23, source claim: the articles' licences (from the full-text XML);
  the PhanSST ReadMe's code definitions and time scale; the CENOGRID
  collection's 27 datasets; PANGAEA's refusal of text format for collections.
- 2026-10-23, recall: the location of the Kennedy–Connors–Auburn province.
- 2026-10-23, reviewed by an independent Claude Sonnet subagent, and all its
  findings are applied above:
  - PhanDA's merged slices;
  - the S1 "least significant digit" σ;
  - the sixth Australian LIP;
  - PhanSST's Zenodo release, codes and counts;
  - Green et al.'s repository, and Tables S4 and S5;
  - the Q-030 wording;
  - the time scales;
  - the scope of the approval (since made universal by Barry);
  - smaller points.

  It also re-ran the parses and found every Green and Rothman row correct.
- 2026-10-24, GitHub Copilot's review of BWBrook/eprp#2, applied: the
  profiler takes each route's newest mirrored version in `versions.tsv`
  order (a name sort would pick Scotese's superseded release if both were
  mirrored), and a missing or differing S1 boundary, S2 age or S3 impact
  against Green et al.'s repository now fails the run. Re-run: profile
  unchanged, summary ok.
