# Q-027: independent support audit

Owner: Codex | 11 October 2026. Independently checked with a bounded subagent; parent integrated the evidence. Scope: cached Benson CSVs and selected deposited R source; no Benson pipeline execution, climate download, fit or power calculation. Originals untouched. All numerical findings below are direct local observations unless explicitly described as inference or proposed work.

## Decision

Keep the 27/95 result as the output of a stated conservative presence screen. Do not use it to fix a Benson-style power design or to conclude that the tropical-dip test is possible only in the listed warm stages. Reconstruct the intended estimator's sampling windows first: age allocation, palaeocoordinates, grid, country/region exclusion, richness eligibility, latitude bands, and dependent sampling units. The bounded next task is a support/estimator contract, not the complete climate-analysis pipeline.

## Verified and corrected

- `probe.py` imports the original builder, redirects outputs to this scratch directory and disables fetching. Both tracked TSVs reproduce byte-for-byte: 382,266 occurrences, 95 represented stages, k3/k10/k20 passes 74/27/4.
- Independent interval containment checks find 100 source ICS stages, 382,266 uniquely contained records, 271,806 uncontained records, no multiply contained records, no invalid ages/coordinates, no lost valid interval candidates. Five unrepresented stages are Stage 2, Stage 4, Paibian, Jiangshanian and Stage 10. Thus 95 is the represented-stage denominator, not every ICS stage.
- There are no duplicate occurrence IDs in the download; retained collections do not occur in multiple cells within a stage or in multiple stages. This establishes row/collection integrity, not independence of references, formations or successive stage samples.
- **Era bug:** original `build.py:150` uses 251.902 Ma, whereas the archived PBDB interval table uses 252.17 Ma. It assigns Induan (252.17–251.2 Ma) to the Palaeozoic. Corrected source-consistent breakdowns are k3: 28/43, 28/30, 18/22; k10: 12/43, 10/30, 5/22; k20: 3/43, 1/30, 0/22. Global counts remain 74/27/4.

## Country join and spatial meaning

- Every Europe/North America name in the supplied region table joins to an ISO code. UK is handled. Russia is Asia, Turkey Asia, Georgia and Cyprus Europe, Mexico North America, Greenland and Svalbard/Jan Mayen Rest of World: these are the source table's definitions, not a geographic judgement by the audit.
- The source explicitly recodes PBDB AA to AQ and FA to FK for country lookup and back again (`source/subscripts/define-regions.R:16`). AA's 1,426 retained records are Antarctica, appropriately outside EU/NAm; they are not an unknown modern country.
- Original pandas parsing turns Namibia's literal `NA` code (40 retained records) into missing. It remains correctly classified outside EU/NAm in this binary screen, but the identity must be preserved for a general region join.
- Another **822 retained records have an actually empty country code** and are classified outside EU/NAm by the boolean complement. Excluding them changes k10 support 27→26: Ypresian changes 30/10/12 to 28/9/12 cells across the three bands. Treat unknown country separately; do not silently call it outside. `known-country-support.tsv` preserves this sensitivity (287 point-age records are omitted in the age-comparison script; the k10 baseline remains 27).
- Cells are geographic grid IDs, not genus records, regional replicates or SQS-ready samples. Both hemispheres are pooled through absolute latitude. At k10 only 3 stages pass using the north alone and 4 using the south alone, versus 27 pooled. Pooling is a modelling choice requiring a symmetry/region-confounding check, not an automatic error.
- 66 stage×cell IDs contain both EU/NAm and outside occurrences. The original binary cell sets therefore overlap: `cells_eu_na_share` is the proportion of cells having any EU/NAm occurrence, not a partition of spatial coverage. There are 3,721 occupied outside stage×cells, including these 66 overlaps. Excluding EU/NAm occurrence rows does not create geographic or bibliographic independence.
- Benson's deposited source excludes **whole cells by their modal collection-level region** (`compute-clade-agnostic-env-vars.R:103`; `explore-eu-nam-peak-latitudinal-richness.R:48`), unlike the screen's occurrence-row exclusion. Use the intended approach explicitly in the estimator contract.
- Original 5° grid latitude boundaries mostly coincide with the four bands. Exact negative boundary latitudes can put the same cell in adjacent absolute-latitude bands. Assigning each cell by its midpoint leaves all three threshold totals unchanged. Shifted/coarser grid probes can also split one cell across occurrence-defined bands; their counts are sensitivity illustrations, not a faithful dggridR result or a usable upper/lower bound.

## Age allocation changes the claimed windows

Source `subscripts/assign-occurrences-using-bin-schemes.R:41` assigns an occurrence to the unique stage with **strictly more than 50% of its age-range overlap**, rather than demanding containment. It also joins precomputed palaeocoordinates at the bin's reconstruction age. Source zero-duration ranges cannot satisfy the strict overlap rule; 287 such records were included in the original containment output.

`assignment_compare.py` applies the source's >50% rule while holding the other screen choices fixed (original downloaded Scotese coordinates, 555 km grid, simple lithification filter). This is a one-choice sensitivity, not a source replication. It admits 209,088 spanning-age records and removes the 287 contained point-age records: 591,067 occurrences in 99 stages. k3/k10/k20 passes become **83/46/14**. All original k10 stages remain, and 19 further stages pass. The extra windows include Turonian, Lutetian, Toarcian and Campanian.

| Stage | Containment: outside cells 0–20 / 20–40 / ≥40° | Majority overlap: same screen |
| --- | --- | --- |
| Turonian | 15 / 8 / 7 | 31 / 18 / 18 |
| Lutetian | 24 / 7 / 7 | 31 / 13 / 14 |
| Coniacian | 10 / 7 / 10 | 17 / 9 / 15 |
| Santonian | 6 / 6 / 12 | 9 / 11 / 21 |
| Aptian | 10 / 12 / 27 | 22 / 25 / 41 |

Inference: the count 27 is neither a ceiling nor a source-faithful set of potentially usable stages. Choosing full containment may be scientifically defensible, but it deliberately changes the support and temporal-precision contract; it does not establish impossibility in stages it removes.

## Presence support cannot determine power

Source uses hexagonal/pentagonal dggridR grids (`compute-dggridr-cells.R:37`), cell-centre latitude, and iNEXT incidence-frequency richness at quorum 0.9 with extrapolation capped at twice the collection sample (`functions/run_SQS_iNEXT_simple.R:57`). Main plots omit missing SQS values (`plot-main-LGB-figures.R:30`). A deposited plotting preparation route imposes at least 10 clade-agnostic collections per cell and multiton ratio ≥0.3 (`load-shiny-data-for-plotting-figures.R:10`); the main revised plotting file calls a separately defined quality function, whose definition was not traced in this bounded audit. Exact intended eligibility still needs to be pinned.

On the original 555 km screen, requiring merely at least 2, 5 or 10 distinct **outside** collections per cell changes k10 passing stages from 27 to **14, 4 or 1**. These are arbitrary diagnostic thresholds, not Benson's filters (the source counts clade-agnostic collections, may include EU/NAm rows in modal-outside cells, and uses a different grid/age rule). They demonstrate why occupancy alone gives no usable-richness count. A further exploratory filter requiring ≥3 genera with at least one repeated collection incidence gives 6 k10 stages, also not a Benson eligibility result.

A 9° approximately 1000 km rectangular grid gives 24 k10 stages at one origin and 20 at a shifted origin under occurrence-defined bands. This is not dggridR and cells may straddle bands; do not substitute those totals for the source's 1000 km design. Coarsening can merge observations but also improve coverage/richness eligibility. There is no justified conversion from 555 km occupancy k to a number of usable 1000 km SQS observations.

Power also requires the exact latitude positions and region identity (to separate latitude from region), per-cell incidence and reference/collection structure, uncertainty and dependence, temporal durations and climate contrasts, and an explicit effect/estimator. Two datasets with identical cell counts can have all-singleton versus repeated genus incidences and entirely different coverage eligibility. Excluding source regions supplies a robustness subset; it does not certify independent source data or random-effects identification.

## Evidence and reproducibility

- Reproduce original/sensitivity checks: `uv run --offline data/q027-support-audit/probe.py` and `uv run --offline data/q027-support-audit/assignment_compare.py` (pandas and numpy pinned to 2.3.3). All generated files stay under ignored `scratch/q027-independent-audit/`. The scripts import the original support builder; this audit records its state at commit `b208a6a`. Later changes to that builder require rechecking the baseline. Runs used selected columns and modest matrix checks; peak RSS was not instrumented. No heavy remote compute.
- Cached raw source: `data/raw/benson2025/`, occurrence member SHA256 c5da9359fced2285e0d50f20626a1ab562738d80ff12cece2bb0af530746670d (original contract; actual read reproduction).
- Selected code members fetched from the [immutable Zenodo record 15269137](https://doi.org/10.5281/zenodo.15269137) by bounded ZIP range requests, with zipfile CRC verification. Exact full archive paths are the prefix `marine-lbg-ms-code-submission-2025-04-22 2/` plus paths in `source-member-checksums.tsv`; no complete 1.55 GB download. Run `uv run data/q027-support-audit/fetch_sources.py` to retrieve/check the pinned code members under `scratch/q027-independent-audit/source/`.
- Primary [publisher page](https://onlinelibrary.wiley.com/doi/10.1111/pala.70006) verified abstract and supporting-table descriptions on 11 October 2026; Tables S3/S4 describe 1000 km SQS regressions. Publisher full text and Bristol accepted manuscript retrieval returned 403; these are access limits. No detailed paper-method claim relies on those inaccessible texts.
- Tracked result tables: `corrected-era-summary.tsv`, `majority-support.tsv`, `known-country-support.tsv`, `5deg-min{2,5,10}collections-support.tsv`, and hemisphere columns in `5deg-support.tsv`. The original `summary.tsv` and `per_stage.tsv` remain in [Claude's screen](../q027-joint-support/README.md). Other exploratory tables and logs remain in scratch.

Parent Codex owns integration and reply to Claude. Suggested next owner: Claude for the estimator-faithful support contract; Codex challenges the power/discrimination design before any empirical gradient fit. Status remains provisional feasibility.
