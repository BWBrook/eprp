---
id: timescale
name: Geological time scale — ICS chart releases 2004 to 2020/01 as RDF, ICS chart PDFs 2014-10 to 2024/12, Macrostrat and PBDB interval tables
kind: compilation
status: active
last_update: "ICS chart v2024/12; the RDF series ends at chart v2020/01 (repository last pushed 2021-10-11)"
scope:
  taxa: ["not taxonomic: chronostratigraphic boundaries and intervals"]
  time: "Hadean to Holocene (the RDF to 4,000 Ma; the 2024/12 chart's Phanerozoic base 538.8 Ma)"
  space: "global (Macrostrat adds regional scales, among them 88 New Zealand stages and one epoch)"
  record_unit: "one boundary (base of a stage, series, system or higher unit) with its age and, where given, its uncertainty"
size:
  as_of: "2026-10-23"
  rdf_releases: 16
  chart_pdfs: 12
  pbdb_bases_with_chart_uncertainty: 96
  raw_files: 73
  mirrored_bytes: 43168466
access:
  tier: unclear
  licence: "RDF series and its chart copies: CC0 1.0 (CGI-IUGS repository licence); Macrostrat CC BY 4.0 (the API's licence field); Farrell et al. 2025 CC BY-NC 4.0; the ICS chart PDFs print a copyright line ((c) ICS) and a citation, no licence"
  routes:
    - {type: github, url: "https://github.com/CGI-IUGS/timescale-data", state: "default branch head 2020-10-21 (e7f62800e7), 72 commits indexed; two other branches not mirrored", checked: 2026-10-23}
    - {type: web, url: "https://stratigraphy.org/ICSchart/", state: "ChronostratChart2024-12.pdf and ChronostratChart2020-03.pdf; the repository holds 2014-10 to 2020-01", checked: 2026-10-23}
    - {type: api, url: "https://macrostrat.org/api/v2/defs/intervals?all", state: "1,716 intervals, with the timescales list (timescales?all)", checked: 2026-10-23}
    - {type: figshare, url: "https://doi.org/10.1130/GSAB.S.28207634.v1", state: "Farrell et al. 2025 late Cambrian revision, supplement", checked: 2026-10-23}
  api: "Macrostrat API v2; PBDB intervals (pbdb entry)"
versioning:
  replay: exact
  notes: "each ICS chart release is a fixed document; the RDF keeps sixteen releases (2004 to chart v2020/01) and the PDFs twelve charts (2014-10 to 2024/12). Macrostrat and PBDB are live tables, snapshotted"
mirror:
  path: deep-server:/data/paleodata/timescale
  policy: "every machine-readable ICS release, the 2020/03 and 2024/12 chart PDFs, live interval tables as dated snapshots"
  state: "four routes, 73 files (43.2 MB), each with a manifest; all verify. Derived: timescale/derived/2026-10-23T0844Z/"
lineage:
  upstream:
    - "International Commission on Stratigraphy (chart); Geologic Time Scale 2004, 2012 and 2020 (Gradstein et al.; the books are not open)"
    - "CGI-IUGS (Cox and Richard) RDF encodings of each chart release"
  downstream:
    - "PBDB and Macrostrat interval ages; every dated entry in this catalogue"
eprp_questions: [Q-005, Q-035, Q-041, Q-045]
citation:
  - "Cohen, K. M., Finney, S. C., Gibbard, P. L. & Fan, J.-X. (2013; updated) The ICS International Chronostratigraphic Chart. Episodes 36: 199-204; chart v2024/12"
  - "Cox, S. J. D. & Richard, S. M. A geologic timescale ontology and service (CGI-IUGS timescale-data, GitHub)"
  - "Macrostrat API (macrostrat.org), CC BY 4.0"
  - "Farrell, T. P. et al. (2025) Revising the late Cambrian time scale and the duration of the SPICE event. GSA Bulletin, doi:10.1130/B37919.1"
entry:
  created: 2026-10-23
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-23, independent Claude Sonnet subagent; findings applied"
---

# Geological time scale

## Summary

Every dated record in this catalogue rests on a time scale. Q-041
(periodicity) needs boundary ages with their uncertainties, and Q-045 needs
to know how far the ages themselves have moved.

The ICS chart is published as a PDF. The GTS books and the TimeScale Creator
datapack are not open (CONTACTS C9 f). We therefore assembled the open,
machine-readable pieces and checked them against each other:

- **CGI-IUGS RDF.** The CGI-IUGS RDF encoding of sixteen ICS chart releases,
  from 2004 to chart v2020/01, under CC0, with the PDFs of the charts from
  2014-10 to 2020-01.
- **Recent chart PDFs.** The ICS chart PDFs of 2020/03 and 2024/12.
- **Interval tables.** Macrostrat's and PBDB's interval tables.
- **Late Cambrian revision.** The supplement to Farrell et al.'s 2025 revision
  of the late Cambrian.

**Findings:**
- **The RDF's last release is chart v2020/01, a pre-GTS2020 chart.** Its
  Phanerozoic base is 541 Ma. Of 156 boundaries it shares by name with PBDB,
  90 differ from PBDB's values.
- **A boundary table with uncertainties.** Matching the ages printed on the
  2024/12 chart to PBDB's stage bases gives `ics2024_pbdb_bases.tsv`.
  - 166 of PBDB's 171 interval rows match (114 distinct ages).
  - 96 rows carry a ± uncertainty (63 distinct ages).
- **PBDB differs from the 2024/12 chart at three boundaries,** which
  Macrostrat prints as the chart does.

## Contents

- **RDF series** (`isc-rdf`, the repository at its last commit on the default
  branch).
  - We read one Turtle file per release: 2004, 2005, 2006, 2008, 2009, 2010,
    2012, 2013, 2014, 2016-10, 2016-12, 2017, 2018, a second 2018 file
    (`isc2018-1`), 2019 and 2020.
  - Boundaries are keyed by URI, and named by every "Base of" label and
    alias. Ages come in both vocabularies (the older `tm:`/`thors:` and the
    newer `time:`/`gts:`).
  - Positions in years before present are converted to Ma. These are the late
    Quaternary boundaries from `isc2018-1` on, where the RDF gives each one
    position in each system.
  - The releases hold 106–125 boundaries (116 distinct ages in the last
    three, which carry synonym pairs such as Upper and Late Pleistocene).
    55–80 of them have uncertainties, and the 2006–2010 releases include four
    uncertainties of 0.
  - The `isc2020` file's version tag is `gts2020:2020-01-13`, and the
    repository's newest change log calls v2020/01 the actual chart. So this
    release is chart v2020/01, not the GTS2020 book.
  - The repository also holds the chart PDFs for 2014-10, 2015-01, 2016-04,
    2016-10, 2016-12, 2017-02, 2018-08, 2019-05 and 2020-01, with the ICS
    change logs.
  - `isc_boundaries_by_version.tsv` (derived) gives each boundary's labels,
    and its age and uncertainty in every release.
- **ICS charts** (`ics-chart`). The 2024/12 and 2020/03 charts, as PDFs.
- **Macrostrat** (`macrostrat`). `intervals?all` holds 1,716 intervals,
  among them 170 "international intervals" and the New Zealand scale (88
  stages, one epoch); `timescales?all` lists the scales.
- **Farrell et al. 2025** (`farrell2025-late-cambrian`). The GSA Bulletin
  supplement: a 4.1 MB PDF, and a zip of R files with the SPICE data of
  Cothren et al. 2022.
- **PBDB intervals** are in the [pbdb](../pbdb/README.md) entry
  (`pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv`).

## Findings

All from [profile/timescale_profile.tsv](profile/timescale_profile.tsv).

- **How the chart has moved** (RDF, boundaries matched by URI).
  - 2010 → 2012 (GTS2012) moved 87 of 112 shared boundaries, by up to 11.5
    Myr (Norian 216.5 → 228).
  - 2008 settled the Ediacaran base at 635 Ma; it was 600 in 2004 and 630 in
    2005.
  - 2009 moved the Quaternary base from 1.806 to 2.588 Ma.
  - Between the 2014 and 2016-10 files the Cryogenian base moved from 850 to
    720 Ma (the change log dates it to chart 2015/01).
  - Smaller moves in most releases are listed in the profile.
- **Chart to chart** (PDF text, by printed value).
  - From 2014-10 to 2020-03 each release changed one to four printed values.
  - 2020-03 to 2024-12 changed 68 of about 122 (new 68, gone 68).
- **Chart v2020/01 against PBDB** (by name, aliases included).
  - 156 boundaries are shared and 90 differ:

    | PBDB type | Shared | Differing |
    | --- | ---: | ---: |
    | Ages | 94 | 61 |
    | Epochs | 28 | 18 |
    | Periods | 22 | 8 |
    | Eras | 9 | 1 |
    | Eons | 3 | 2 |

  - 15 PBDB names have no RDF label, among them Wuliuan, Stage 2–4 and 10,
    Series 2, Greenlandian and Ludfordian.
  - So any analysis on the RDF's last release is on pre-GTS2020 ages.
    Inferred: the chart took most GTS2020 ages after 2020/03. The 2024/12
    chart says most of its ages are from GTS2020.
- **The boundary table with uncertainties** (`ics2024_pbdb_bases.tsv`,
  derived). For each of PBDB's 171 scale-1 interval rows, it gives:
  - the base age;
  - the 2024/12 chart's printed value at that age, where there is one (166
    rows, 22 of them matched through integer ages such as 635 and 720);
  - the chart's ± uncertainty (96 rows, 63 distinct ages) or its "~" flag (18
    rows, 14 distinct ages).
  - A PBDB age is its own base, so a stage and the epoch or period it starts
    share a row value. The row counts therefore exceed the boundary counts.
- **PBDB vs Macrostrat and the 2024/12 chart.** They agree on 165 of 170
  shared names. The five that differ are three boundaries, where the 2024/12
  chart prints Macrostrat's value:

  | Boundary | PBDB | Macrostrat and the 2024/12 chart |
  | --- | ---: | ---: |
  | Olenekian base | 250.8 | 249.9 |
  | Anisian (Middle Triassic) base | 247 | 246.7 |
  | Wuchiapingian (Lopingian) base | 259.857 | 259.51 ± 0.21 |

  PBDB's three values appear on no chart release we hold, so we cannot say
  where they come from (queued as CONTACTS C10 i).

## Access

- **Terms.**
  - The RDF repository is CC0, and Macrostrat CC BY 4.0 (the API's own
    licence field).
  - Farrell et al.'s supplement is CC BY-NC 4.0.
  - The ICS chart PDFs print "(c) International Commission on Stratigraphy"
    and a citation, with no licence. By the catalogue's tier rules they are
    `unclear`; we hold them as a private copy under Barry's universal
    approval of 23 October 2026 ("Licence overrides confirmed, universally
    for the EPRP. Mirroring locally is always okay for us"). Derived values
    stay on deep-server.
- **Rebuild.** On deep-server, in a login shell, with `$P` =
  `/data/paleodata/timescale`:

  ```sh
  timescale_snapshot.sh [isc] [ics] [macrostrat] [farrell]
  uv run timescale_profile.py $P/isc-rdf/raw/2020-10-21_e7f62800e7 $P/ics-chart/raw/2026-10-23T0844Z_url \
      $P/macrostrat/raw/2026-10-23T0844Z_url /data/paleodata/pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv \
      $P/farrell2025-late-cambrian/raw/<version_dir> $P/derived/2026-10-23T0844Z profile/timescale_profile.tsv
  ```

  The profiler needs `pdftotext`, and Python below 3.14 for rdflib 7.1.

## Strengths

- **Open and versioned.** Sixteen releases of the chart are machine-readable
  under CC0, so analyses can be rerun on the time scale of their day.
- **Uncertainties.** The 2024/12 chart's printed uncertainties, attached to
  PBDB's interval names, give Q-041's age model uncertainties for 63 distinct
  boundaries.

## Weaknesses and pitfalls

- **No machine-readable recent chart.**
  - The RDF stops at v2020/01. The 2024/12 values come from the PDF's text
    layer, matched to PBDB names by value.
  - A printed number that equals a PBDB base by chance would be mislabelled.
    An independent check of the 144 decimal matches against the chart's
    geometry found none.
- **Approximate ages.**
  - The 2024/12 chart prints 14 values as "~": nine Cambrian boundaries, the
    Rhaetian, Norian and Carnian, and the Ediacaran and Cryogenian bases.
  - Treat them as undefined in uncertainty, not as exact.
- **Boundary names change.**
  - Labels drift between releases. Examples: "Cambrian Stage 9" became
    Jiangshanian, "Middle Pleistocene" became Chibanian, and there are
    misspellings ("Creataceous", "Darriwillian").
  - Join releases by URI, as the derived table does, and match names through
    all labels.
- **GTS2020 itself is not open.** The book's tables (and their uncertainty
  models) are under copyright. The TimeScale Creator datapack's licence
  conflicts with its record (C9 f).

## Overlap with other sources

- **PBDB.** PBDB's intervals agree with the 2024/12 chart except at the three
  boundaries above. Its occurrence ages (`max_ma`, `min_ma`) inherit them.
- **Other entries' time scales:**
  - **NSB and Triton:** GTS2012 ([nsb](../nsb/README.md),
    [triton](../triton/README.md)).
  - **Classic compendia:** FR2 uses Harland et al. (1990), and the Sepkoski
    package uses its own stage ages.
  - **Green et al.'s (2022) event tables:** GTS2012 unless noted (their Table
    S1's comment column; [climate-forcing](../climate-forcing/README.md)).

## EPRP relevance

- **Q-041 (periodicity).** The boundary uncertainties for its age model, and
  the release series to test how much a claimed period depends on the time
  scale's vintage.
- **Q-045 (data vintage).** The time scale is itself a vintage; sixteen are
  here.
- **Q-005 and Q-035 (inferred).** Precursors and land–sea lags turn on
  stage-level timing.

## Citation and terms

Cite the ICS chart as Cohen et al. (2013; updated), v2024/12, and the RDF
encodings as CGI-IUGS timescale-data. Cite Macrostrat (CC BY 4.0) and
Farrell et al. (2025).

## Verification log

- 2026-10-23, checked: four routes mirrored with
  [timescale_snapshot.sh](timescale_snapshot.sh) (the RDF leg rerun after a
  `data_mirror.py` fix for zero-length files, commit 3757575). All 73 files
  re-verify. Index: [snapshots.tsv](snapshots.tsv).
- 2026-10-23, checked: [timescale_profile.py](timescale_profile.py)
  ([output](profile/timescale_profile.tsv)), run on deep-server.
- 2026-10-23, source claim: the chart's citation and copyright lines; that the
  GTS books are not openly licensed; the change logs' dating of releases.
- 2026-10-23, reviewed by an independent Claude Sonnet subagent, and all its
  findings are applied above:
  - **The "unit errors" were a profiler bug.** The late Quaternary positions
    are declared years before present.
  - **Release labels:** the last release is chart v2020/01, and the 2016-10
    release had been skipped.
  - **Matching:** boundaries are now keyed by URI with all labels, and
    integer chart ages are parsed.
  - **Counts** are now given by rows and by distinct ages.
  - **Cross-entry time scales and licence statements** are corrected.

  The reviewer's geometry check confirmed every ± and "~" assignment and the
  three-boundary difference.
