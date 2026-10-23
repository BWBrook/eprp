---
id: climate-forcing
name: Climate-forcing series and event tables — PhanDA, PhanSST, Scotese 2021, Song 2021, CENOGRID, LR04, Rothman 2017 carbon events, Green 2022 LIPs and impacts
kind: compilation
status: active
last_update: "PhanDA head 2026-03-09; PhanSST v001 (2023-03-09); the others are fixed publications (2005-2022)"
scope:
  taxa: ["not taxonomic: temperature, CO2, benthic isotopes, carbon-cycle events, volcanic provinces, impacts"]
  time: "Phanerozoic (PhanDA 0-486.85 Ma; Scotese 100 intervals; Rothman 0.02-541 Ma); Cenozoic (CENOGRID 0-67.1 Ma); LR04 0-5.32 Ma"
  space: "global"
  record_unit: "varies: a stage slice's GMST and CO2 percentiles; a proxy SST measurement; a dated benthic isotope sample; an event or province"
size:
  as_of: "2026-10-23"
  phanda_stage_slices: 85
  phansst_rows: 151259
  raw_files: 1236
  mirrored_bytes: 656782914
access:
  tier: unclear
  licence: "mixed: Scotese 2021, Song 2021, CENOGRID CC BY 4.0; Rothman 2017 CC BY-NC 4.0; Green et al. 2022 CC BY-NC-ND 4.0; LR04 NOAA NCEI (no restriction stated); PhanDA and PhanSST state no licence"
  routes:
    - {type: github, url: "https://github.com/EJJudd/PhanDA", state: "head 9f06c0d (2026-03-09), the commit the main project pins; 34 commits indexed", checked: 2026-10-23}
    - {type: github, url: "https://github.com/EJJudd/PhanSST", state: "head 32cc98e (2023-03-09); 30 commits indexed", checked: 2026-10-23}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.8237751", state: "PhanDA HadCM3L priors, 11.4 GB: indexed, not mirrored", checked: 2026-10-23}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.5027293", state: "Song et al. 2021 data and R code", checked: 2026-10-23}
    - {type: zenodo, url: "https://zenodo.org/records/8238875", state: "Scotese et al. 2021 GMST maps, version scotese02a_v21321 (C1)", checked: 2026-10-23}
    - {type: pangaea, url: "https://doi.org/10.1594/PANGAEA.917503", state: "CENOGRID collection, as zip (the collection has no text format)", checked: 2026-10-23}
    - {type: web, url: "https://www.ncei.noaa.gov/pub/data/paleo/contributions_by_author/lisiecki2005/", state: "LR04 stack; the author's copy (lorraine-lisiecki.com) also mirrored", checked: 2026-10-23}
    - {type: api, url: "https://www.ebi.ac.uk/europepmc/webservices/rest/", state: "Rothman 2017 full text (PMC5606709) and Green et al. 2022 supplement (PMC9499591); PMC itself serves a reCAPTCHA to scripts", checked: 2026-10-23}
  api: "Europe PMC REST; Zenodo; PANGAEA"
versioning:
  replay: exact
  notes: "PhanDA and PhanSST are git repositories (every commit indexed; the head mirrored, which is the commit the main project pins for PhanDA); the rest are fixed deposits or article supplements"
mirror:
  path: deep-server:/data/paleodata/climate-forcing
  policy: "the forcing series and event tables the registers cite; model priors over 5 GB indexed only"
  state: "eight routes mirrored and one indexed; 1,236 files (657 MB), each with a manifest; all verify. Derived: climate-forcing/derived/2026-10-23/"
lineage:
  upstream:
    - "PhanDA: data assimilation of PhanSST proxies with HadCM3L priors (Judd et al. 2024, doi:10.1126/science.adk3705)"
    - "CENOGRID: Westerhold et al. 2020 (Science); LR04: Lisiecki and Raymo 2005 (Paleoceanography); Rothman 2017 (Science Advances); Green, Renne and Keller 2022 (PNAS); Scotese et al. 2021 (Earth-Science Reviews); Song et al. 2021 (Nature Communications)"
  downstream:
    - "the main project's interval crosswalk and PhanDA stage-difference analyses (data/interval-crosswalk, data/phanda-stage-differences), pinned to the same PhanDA files"
eprp_questions: [Q-003, Q-007, Q-011, Q-019, Q-027, Q-030, Q-050, B-018]
citation:
  - "Judd, E. J. et al. (2024) A 485-million-year history of Earth's surface temperature. Science, doi:10.1126/science.adk3705 (PhanDA)"
  - "Judd, E. J. et al. (2022) PhanSST (Scientific Data; recall)"
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
  reviewed: pending
---

# Climate-forcing series and event tables

## Summary

Most of the unanswered EPRP questions need a forcing series: a temperature,
CO₂ or carbon-cycle record to set against extinction and origination. Q-030
asks for a forcing catalogue outright. This entry gathers the series and event
tables the registers cite:

- **Phanerozoic temperature:**
  - PhanDA, the data-assimilated GMST and CO₂ by stage;
  - PhanSST, its proxy database;
  - Scotese et al. 2021, GMST maps for 100 intervals;
  - Song et al. 2021, temperature thresholds for mass extinctions.
- **Cenozoic and Plio-Pleistocene benthic isotopes:** CENOGRID and LR04.
- **Event tables:**
  - Rothman's 31 carbon-isotope events;
  - Green, Renne and Keller's tables of stage-boundary extinction magnitudes,
    large igneous provinces and impacts.

The main project already uses PhanDA and Song 2021. Our PhanDA files are
byte-identical to the pins in `data/interval-crosswalk/sources.tsv`, and so is
Song's extinction-rate script. The two event tables existed only as an article
table and a PDF appendix; we extracted both and count-checked them.

## Contents

From [profile/climate_forcing_profile.tsv](profile/climate_forcing_profile.tsv).

| Route | What | Size |
| --- | --- | ---: |
| `phanda` | PhanDA repository at 9f06c0d: GMST and CO₂ percentiles for 85 stage slices (0–486.85 Ma), the GMST ensemble (`.mat`), 85 per-stage surface-temperature gradient files, code | 1,218 files, 517 MB |
| `phansst` | PhanSST v001: 151,259 proxy rows from 1,247 sites and 635 publications, with a 663-row reference list | 4 files, 43 MB |
| `phanda-hadcm3l-priors` | PhanDA's model priors: indexed only | (11.4 GB) |
| `song2021-temperature-thresholds` | Database S1 (Excel) and two R scripts | 3 files, 1.3 MB |
| `scotese2021-gmst` | GMST for 100 Phanerozoic intervals, as grids, lists and netCDF, with a methods PDF | 5 files, 91 MB |
| `cenogrid` | Westerhold et al. 2020, 27 member tables, including the splice (24,321 samples, 0–67.1 Ma) and the binned record (23,629 rows) | 1 zip, 1.8 MB |
| `lr04` | LR04 stack, 2,115 rows (0–5,320 ka), from NOAA and from the author's site | 2 files, 0.4 MB |
| `rothman2017-carbon-events` | the article's full text, whose Table 1 lists the 31 carbon-isotope events (0.02–541 Ma) | 0.2 MB |
| `green2022-lips` | the supplementary files (SI appendix PDF and figures) and the full text | 2 files, 2.3 MB |

- **PhanDA.**
  - The median GMST ranges from 11.4 °C (Upper Pleistocene) to 35.6 °C
    (Turonian).
  - The median CO₂ ranges from 239 ppm (Chibanian) to 3,326 ppm (Floian).
- **PhanSST proxies.**
  - By type:

    | Proxy type | Rows |
    | --- | ---: |
    | Carbonate δ¹⁸O (`d18c`) | 81,709 |
    | Alkenone U^K'_37 (`uk`) | 35,360 |
    | TEX86 (`tex`) | 14,091 |
    | Mg/Ca (`mg`) | 13,249 |
    | Phosphate δ¹⁸O (`d18p`) | 6,379 |
    | `d18a` | 471 |

  - The ages are heavily Cenozoic: 63,089 Quaternary and 41,721 Neogene rows,
    against 92 Cambrian. The median age is 3.6 Ma.
- **Derived** (`climate-forcing/derived/2026-10-23/`):
  - `rothman2017_events.tsv`: event, abbreviation, date, δ₁ before and after,
    Δr, τ_env, φ, M.
  - `green2022_table_S1.tsv`: 102 stage boundaries with age, 1σ, and Muscente
    et al.'s corrected diversity and extinction rates.
  - `green2022_table_S2.tsv`: 35 LIPs with start and end ages and their 1σ,
    duration, volume and eruption rate (25 have a rate). The two column blocks
    are joined on the row number.
  - `green2022_table_S3.tsv`: 24 impacts of 20 km or more, with ages and 1σ.

## Provenance and lineage

- **PhanDA, PhanSST and the priors.** PhanDA assimilates PhanSST proxies into
  HadCM3L model priors, stage by stage (Judd et al. 2024). The priors are
  Zenodo 8237751. PhanDA's stages are merged where proxies are sparse: the
  main project's notes describe merged slices, and the gradient files are
  named e.g. `Anisian&Olenekian`.
- **Scotese et al. (2021).** HadCM3L simulations adjusted to δ¹⁸O proxies;
  version scotese02a_v21321 (C1) is the newest of two Zenodo versions.
- **Song et al. (2021).** Database S1 and the R code behind its thresholds of
  temperature change.
- **CENOGRID.** The astronomically tuned Cenozoic benthic δ¹³C and δ¹⁸O
  reference (Westerhold et al. 2020). PANGAEA serves the collection only as a
  zip.
- **LR04.** NOAA's file holds the stack and further blocks (sedimentation
  rates, age-model notes). Its stack block is identical to the author's file
  at all 2,115 rows.
- **Event tables.**
  - Rothman (2017) compiled 31 Phanerozoic carbon-isotope excursions.
  - Green et al. (2022) compiled LIPs and impacts against PBDB-derived
    extinction magnitudes (Muscente et al.). Their Table S1 gives boundary
    ages on GTS2012 unless noted ([timescale](../timescale/README.md)).
  - Their Table S4 applies Rothman's method to the LIPs.

## Access

- **Terms.**
  - Scotese 2021, Song 2021 and CENOGRID are CC BY 4.0.
  - Rothman 2017 is CC BY-NC 4.0, and Green et al. 2022 CC BY-NC-ND 4.0 (the
    articles' licences).
  - LR04 comes from NOAA's World Data Service, with no restriction stated.
  - **PhanDA and PhanSST state no licence** (GitHub). We hold private copies,
    as the main project does, on the rationale of Barry's 23 October approval
    for unlicensed sources ("We're not making this public, although we might
    publish a public registry at some point, but that would point everything
    back to original locations"). The approval itself named FR2 and Sepkoski.
- **PMC.** It now answers scripted requests with a reCAPTCHA. Europe PMC's
  REST API (`fullTextXML`, `supplementaryFiles`) serves the same files openly.
- **Rebuild.** On deep-server, in a login shell:

  ```sh
  climate_forcing_snapshot.sh [phanda] [phansst] [priors] [song] [scotese] [cenogrid] [lr04] [rothman] [green]
  uv run climate_forcing_profile.py /data/paleodata/climate-forcing /data/paleodata/climate-forcing/derived/2026-10-23 \
      profile/climate_forcing_profile.tsv
  ```

  PhanDA is fetched file by file from GitHub (1,218 files) and takes about two
  hours. The profiler needs `pdftotext`.

## Strengths

- **The forcing series behind the registers, at fixed versions.** PhanDA's
  files match the main project's pins byte for byte.
- **Machine-readable event tables.** The LIP, impact and carbon-event tables
  were PDF or HTML only; they are now TSVs, checked for row numbering and age
  order.

## Weaknesses and pitfalls

- **PhanDA's stages are not independent.** It assimilates each stage
  separately, so there is no joint temporal posterior (the main project's
  `data/phanda-stage-differences` treats this). Some slices merge stages.
- **PhanSST is Cenozoic-heavy.** 69% of its rows are Neogene or younger, and
  the Palaeozoic is thin, which matters for any proxy-level
  reanalysis.
- **Time scales differ.**
  - Green et al. use GTS2012, and PhanDA and PhanSST their own stage ages.
  - CENOGRID and LR04 have astronomically tuned age models.
  - Rothman's dates are the events' own.
  - Put them on one scale before comparing ([timescale](../timescale/README.md)).
- **The Green tables are parsed from layout text.**
  - The checks hold: consecutive row numbers, readable ages, and no LIP that
    ends before it starts.
  - Cells are assigned by column position, and spot checks matched the PDF.
    The S1 comment column holds fragments (such as "1σ") that look cut off at
    the page edge in the PDF itself.
- **The priors are not mirrored.** At about 0.3 MB/s, fetching the 11.4 GB
  would take most of a day; fetch them on demand with `data_mirror.py zenodo
  8237751`.

## Overlap with other sources

- **Main project.**
  - `data/interval-crosswalk/sources.tsv` pins SHA-256 values for PhanDA's
    percentile and ensemble files and Song's extinction-rate script. The files
    here match those pins. The main project's copies themselves are git-ignored
    and were not compared.
- **Time scale.**
  - Green et al.'s Table S1 boundaries are GTS2012 and can be compared with
    the RDF release of 2012 ([timescale](../timescale/README.md)).
- **Australia.**
  - Green et al. list five Australian LIPs: Whitsunday, Bunbury, Gascoyne
    Margin, and the Kalkarindji volcanics and sills.
  - They also list the Tookoonooka impact (Queensland, 55 km, 125 ± 1 Ma).

## EPRP relevance

- **Q-030 (forcing catalogue):** PhanDA, Song 2021, Rothman's events and
  Green's LIPs, which are its named inputs.
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
  [climate_forcing_snapshot.sh](climate_forcing_snapshot.sh) (the CENOGRID leg
  rerun as a zip after the text format was refused). All 1,236 files
  re-verify. Indexes: [snapshots.tsv](snapshots.tsv) and
  [versions.tsv](versions.tsv) (PhanDA 34 commits, PhanSST 30, and the Zenodo
  versions).
- 2026-10-23, checked: [climate_forcing_profile.py](climate_forcing_profile.py)
  ([output](profile/climate_forcing_profile.tsv)), run on deep-server. The
  PhanDA percentile and ensemble files and Song's extinction-rate script match
  the main project's SHA-256 pins.
- 2026-10-23, source claim: the articles' licences (from the full-text XML);
  PANGAEA's refusal of text format for collections; the Zenodo priors' size.
- 2026-10-23, recall: the PhanSST paper citation; that PhanDA's inputs are
  PhanSST.
