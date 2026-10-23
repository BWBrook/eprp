---
id: timescale
name: Geological time scale — ICS chart releases 2004-2020 as RDF, the current ICS chart, Macrostrat and PBDB interval tables
kind: compilation
status: active
last_update: "ICS chart v2024/12; RDF series to the 2020/03 chart (repository last pushed 2021-10-11)"
scope:
  taxa: ["not taxonomic: chronostratigraphic boundaries and intervals"]
  time: "Hadean to Holocene (the RDF to 4,000 Ma; the chart's Phanerozoic base 538.8 Ma)"
  space: "global (Macrostrat adds regional scales, among them 89 New Zealand stages)"
  record_unit: "one boundary (base of a stage, series, system or higher unit) with its age and, where given, its uncertainty"
size:
  as_of: "2026-10-23"
  rdf_releases: 15
  current_bases_with_uncertainty: 94
  raw_files: 73
  mirrored_bytes: 43168466
access:
  tier: open
  licence: "RDF series CC0 1.0 (CGI-IUGS); Macrostrat CC BY 4.0; Farrell et al. 2025 CC BY-NC 4.0; the ICS chart PDFs state no licence (cite Cohen et al. 2013, updated)"
  routes:
    - {type: github, url: "https://github.com/CGI-IUGS/timescale-data", state: "head 2020-10-21 (e7f62800e7); 72 commits indexed", checked: 2026-10-23}
    - {type: web, url: "https://stratigraphy.org/ICSchart/", state: "ChronostratChart2024-12.pdf (current) and ChronostratChart2020-03.pdf", checked: 2026-10-23}
    - {type: api, url: "https://macrostrat.org/api/v2/defs/intervals?all", state: "1,716 intervals, with the timescales list (timescales?all)", checked: 2026-10-23}
    - {type: figshare, url: "https://doi.org/10.1130/GSAB.S.28207634.v1", state: "Farrell et al. 2025 late Cambrian revision, supplement", checked: 2026-10-23}
  api: "Macrostrat API v2; PBDB intervals (pbdb entry)"
versioning:
  replay: exact
  notes: "each ICS chart release is a fixed document; the RDF series keeps fifteen of them (2004-2020). Macrostrat and PBDB are live tables, snapshotted"
mirror:
  path: deep-server:/data/paleodata/timescale
  policy: "every machine-readable ICS release, the current and GTS2020-era charts, live interval tables as dated snapshots"
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
  reviewed: pending
---

# Geological time scale

## Summary

Every dated record in this catalogue rests on a time scale. Q-041
(periodicity) needs boundary ages with their uncertainties, and Q-045 needs
to know how far the ages themselves have moved.

The ICS chart is published only as a PDF. The GTS books and the
TimeScale Creator datapack are not open (CONTACTS C9 f). We therefore
assembled the open, machine-readable pieces and checked them against each
other:

- **CGI-IUGS RDF.** The CGI-IUGS RDF encoding of fifteen ICS chart releases,
  2004 to 2020, under CC0, with ages and uncertainties.
- **ICS chart PDFs.** The current ICS chart (v2024/12) and the 2020/03 chart.
- **Interval tables.** Macrostrat's and PBDB's interval tables.
- **Late Cambrian revision.** The supplement to Farrell et al.'s 2025 revision
  of the late Cambrian.

**Findings:**
- **The RDF release labelled 2020 is the ICS 2020/03 chart, not GTS2020.** Its
  Phanerozoic base is 541 Ma, and 62 of the 106 stage bases it shares with
  PBDB differ from the current values.
- **A current boundary table with uncertainties.** Matching the numbers
  printed on the 2024/12 chart to PBDB's current stage bases gives
  `ics2024_pbdb_bases.tsv`: 144 of PBDB's 171 bases, 94 of them with a ±
  uncertainty.
- **PBDB lags the current chart at three boundaries,** where Macrostrat
  follows it: the Olenekian, Anisian and Wuchiapingian bases.

## Contents

- **RDF series** (`isc-rdf`, the repository at its last commit).
  - We read one Turtle file per release, in two vocabularies (the older
    `tm:`/`thors:` and the newer `time:`/`gts:`).
  - The releases are 2004, 2005, 2006, 2008, 2009, 2010, 2012, 2013, 2014,
    2016-12, 2017, 2018, a second 2018 file (`isc2018-1`), 2019 and 2020.
  - They hold 106–125 boundaries each, with uncertainties for 55–80.
  - `isc_boundaries_by_version.tsv` (derived) gives every boundary's age and
    uncertainty in every release.
- **ICS charts** (`ics-chart`). The current v2024/12 chart and the 2020/03
  chart, as PDFs.
- **Macrostrat** (`macrostrat`). `intervals?all` holds 1,716 intervals,
  among them 170 "international intervals" and 89 New Zealand stages;
  `timescales?all` lists the scales.
- **Farrell et al. 2025** (`farrell2025-late-cambrian`). The GSA Bulletin
  supplement: a 4.1 MB PDF, and a zip of R files with the SPICE carbon-isotope
  data of Cothren et al. 2022.
- **PBDB intervals** are in the [pbdb](../pbdb/README.md) entry
  (`pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv`).

## Findings

All from [profile/timescale_profile.tsv](profile/timescale_profile.tsv).

- **How the chart has moved, release to release.**
  - 2010 → 2012 (GTS2012) moved 85 of 110 shared boundaries, by up to 11.5
    Myr (Norian 216.5 → 228).
  - 2008 settled the Ediacaran base at 635 Ma; it was 600 in 2004 and 630 in
    2005.
  - 2009 moved the Quaternary base from 1.806 to 2.588 Ma.
  - 2016-12 moved the Cryogenian base from 850 to 720 Ma.
  - Smaller moves in most other releases are listed in the profile.
- **The "2020" release is the 2020/03 chart.**
  - The GTS2020 book's ages (538.8 Ma for the base of the Cambrian, 125.77 for
    the Barremian, and so on) entered the chart after 2020.
  - Against PBDB's current bases, 62 of 106 shared names differ. The same 62
    differ against Macrostrat.
  - Seventy-four values printed on the 2024/12 chart are not on the 2020/03
    chart, and 66 on 2020/03 are gone.
- **Unit errors in the RDF.**
  - The second 2018 file (`isc2018-1`) and the 2019 release give four late
    Quaternary boundaries in years, not Ma: Holocene 11,700, Northgrippian 8,276, and Late and Upper
    Pleistocene 126,000.
  - The 2020 release repairs three of them but keeps "Upper Pleistocene" at
    129,000 beside a correct "Late Pleistocene" 0.129.
  - Filter ages over 4,600 Ma before use; the profile lists them.
- **The current boundaries with uncertainties** (`ics2024_pbdb_bases.tsv`,
  derived). For each of PBDB's 171 scale-1 intervals, the table gives:
  - its base age;
  - the chart's printed value at that age, where there is one (144);
  - the chart's ± uncertainty (94) or its "~" approximation flag (14).

  Three chart values have no PBDB base: 246.7, 249.9 and 259.51 ± 0.21 (see
  the next point).
- **PBDB vs Macrostrat.** They agree on 165 of 170 shared bases. The five
  that differ are three boundaries, where the 2024/12 chart prints
  Macrostrat's value:

  | Boundary | PBDB | Macrostrat and the 2024/12 chart |
  | --- | ---: | ---: |
  | Olenekian base | 250.8 | 249.9 |
  | Anisian (Middle Triassic) base | 247 | 246.7 |
  | Wuchiapingian (Lopingian) base | 259.857 | 259.51 ± 0.21 |

  PBDB's interval table lags the chart here (queued as CONTACTS C10 i).

## Access

- **Terms.** The RDF is CC0 and Macrostrat CC BY 4.0. Farrell et al.'s
  supplement is CC BY-NC 4.0. The ICS chart PDFs print a citation but no
  licence, so derived values stay on deep-server.
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

- **Open and versioned.** Fifteen releases of the chart are machine-readable
  under CC0, so analyses can be rerun on the time scale of their day.
- **Uncertainties.** The current chart's printed uncertainties, attached to
  PBDB's interval names, are the uncertainties Q-041's age model needs for 94
  boundaries.

## Weaknesses and pitfalls

- **No machine-readable current chart.** The RDF stops at 2020/03, and the
  ICS site's interactive chart loads its data from a script bundle we did not
  reverse-engineer. The 2024/12 values here come from the PDF's text layer,
  matched to PBDB names by value. A boundary whose chart value matches no
  PBDB base stays unlabelled (three, all named above).
- **GTS2020 itself is not open.** The book's tables (and their uncertainty
  models) are under copyright. The TimeScale Creator datapack's licence
  conflicts with its record (C9 f).
- **Approximate ages.** Fourteen current boundaries are printed as "~"
  (mostly Cambrian and early Ordovician): treat them as undefined in
  uncertainty, not as exact.
- **Units.** See the RDF unit errors above.

## Overlap with other sources

- **PBDB.** PBDB's intervals follow the current chart, except at the three
  boundaries above. PBDB occurrence ages (`max_ma`, `min_ma`) inherit them.
- **Other entries' time scales.** The classic compendia use Harland et al.
  (1990) ages (FR2) and the package's stage ages (Sepkoski). Green et al.'s
  (2022) LIP and extinction tables use GTS2012 unless noted. NSB and Triton
  use their own age models.

## EPRP relevance

- **Q-041 (periodicity).** The boundary uncertainties for its age model, and
  the release series to test how much a claimed period depends on the time
  scale's vintage.
- **Q-045 (data vintage).** The time scale is itself a vintage; fifteen are
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
  ([output](profile/timescale_profile.tsv)), run on deep-server; identical
  to a local run.
- 2026-10-23, source claim: the ICS chart's citation line; that the GTS books
  are not openly licensed; that the site's interactive chart is built from
  ICS OWL data (search result, not verified).
