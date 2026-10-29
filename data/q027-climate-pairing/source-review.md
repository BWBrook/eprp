# Q-027 held-source climate classification reconnaissance

29 October 2026. Owner: bounded Codex explorer; parent owns scientific choice and support calculation.

## Result

Author stage climate classes exist as **explicit stage-name ranges in deposited R code**, not as a numerical global-temperature threshold. The held accepted manuscript attributes these classes to Scotese et al. (2021), Table S2. No climate download or live API is needed to reconstruct the code-defined classes. **A deposited code discrepancy leaves Thanetian and Ypresian unclassified under `hot_or_cold`, although the interval string implies that both belong to a Hot interval.** Treat literal execution and label-implied intent separately.

Scope remained source/interval metadata only: no occurrence IDs, direct extracts, region-band-overlap support outcomes, estimator fitting, live APIs, acquisition or remote work. Only this scratch note was written. No canonical file edits or commit.

## Exact primary-source references

All paths below are relative to `/home/bwbrook/git/eprp/`.

- `scratch/q027-independent-audit/source/subscripts/define-time-ints.R:12–25`: stages are PBDB scale 1, level 5; `LAD=min_ma`, `FAD=max_ma`, midpoint `(LAD+FAD)/2` and duration `FAD-LAD`. Lines 43–48: `get_bins` sorts by midpoint and selects the inclusive sequence from latest to earliest named stage. Thus ages order the stages; they do not threshold the climate classes.
- Same file, lines 101–114: 13 explicitly named `climate_regime_intervals`; lines 135–141 derive `hot_or_cold` by searching their labels for `Hot`, `Cold`, or `Variable`. No numeric temperature cutoff occurs in this definition.
- Same file, **line 113**: `get_bins(earliest_bin = "Bartonian", latest_bin = "Lutetian")` is labelled `"Thanetian to Bartonian (Hot)"`. Actual membership is only Lutetian and Bartonian. Thanetian and Ypresian match no other regime branch and become NA, not Cold, Variable or Ignore. No subsequent code in this file repairs this.
- Same file, lines 145–158 and 177–183: a distinct `icehouse_and_hothouse_intervals` and derived `icehouse_or_hothouse` uses narrower windows, with default `Ignore`. Among these 21 stages its Hothouse windows are Albian–Santonian and Thanetian–Lutetian; its Icehouse window is Rupelian. These cannot be substituted for `hot_or_cold`.
- `scratch/ranking-primary-check-20261028/benson-aam.txt:671–685`: manuscript says 13 contiguous climate-regime intervals, classes from Scotese et al. (2021; Table S2), also pooled non-contiguously after omitting uncertain/variable intervals for an average warm/cold slope comparison.
- Manuscript lines 1033–1066: the pooled warm/cold comparison concerns diversity–latitude slopes and interactions, including/excluding Europe and North America; lines 1068–1084 and Figure 10 caption, 2342–2352, compare diversity within latitude zones across warm/cold intervals. It is a whole-Phanerozoic pooled design, not a preregistered matched Cretaceous/Paleogene stage-pair design.
- Manuscript Figure 9 caption, 2330–2339, distinguishes **global interval classes** cold/hot/variable from **within-cell SST zones** warm/mid/cold. The latter are separate variables, not stage climates. The held code calls `subscripts/load-gcm-data.R` (`master-script.R:149–150`); that small member is not held here. No within-cell SST threshold should be invented from these stage classes.
- Manuscript bibliography lines 2097–2101: Scotese, Song, Mills & Van der Meer (2021), Phanerozoic paleotemperatures, Earth-Science Reviews 215, 103503. That external paper was not acquired or consulted in this tranche.

## All 21 Cretaceous/Paleogene stages: literal held-code expansion

Ages are original archived PBDB bounds in Ma, not a newly harmonised timescale. `NA` means no matching source case, not an inferred climate. `Ignore` is the narrower source variable's literal default.

| Stage | FAD Ma | LAD Ma | Literal regime label | `hot_or_cold` | Narrow `icehouse_and_hothouse_intervals` |
| --- | ---: | ---: | --- | --- | --- |
| Berriasian | 145 | 139.8 | Aalenian to Hauterivian (Cold) | Cold | Ignore |
| Valanginian | 139.8 | 132.9 | Aalenian to Hauterivian (Cold) | Cold | Ignore |
| Hauterivian | 132.9 | 129.4 | Aalenian to Hauterivian (Cold) | Cold | Ignore |
| Barremian | 129.4 | 125 | Barremian to Santonian (Hot) | Hot | Ignore |
| Aptian | 125 | 113 | Barremian to Santonian (Hot) | Hot | Ignore |
| Albian | 113 | 100.5 | Barremian to Santonian (Hot) | Hot | Albian to Santonian Hothouse |
| Cenomanian | 100.5 | 93.9 | Barremian to Santonian (Hot) | Hot | Albian to Santonian Hothouse |
| Turonian | 93.9 | 89.8 | Barremian to Santonian (Hot) | Hot | Albian to Santonian Hothouse |
| Coniacian | 89.8 | 86.3 | Barremian to Santonian (Hot) | Hot | Albian to Santonian Hothouse |
| Santonian | 86.3 | 83.6 | Barremian to Santonian (Hot) | Hot | Albian to Santonian Hothouse |
| Campanian | 83.6 | 72.1 | Campanian to Selandian (Cold) | Cold | Ignore |
| Maastrichtian | 72.1 | 66 | Campanian to Selandian (Cold) | Cold | Ignore |
| Danian | 66 | 61.6 | Campanian to Selandian (Cold) | Cold | Ignore |
| Selandian | 61.6 | 59.2 | Campanian to Selandian (Cold) | Cold | Ignore |
| Thanetian | 59.2 | 56 | NA | NA | Thanetian to Lutetian Hothouse |
| Ypresian | 56 | 47.8 | NA | NA | Thanetian to Lutetian Hothouse |
| Lutetian | 47.8 | 41.3 | Thanetian to Bartonian (Hot) | Hot | Thanetian to Lutetian Hothouse |
| Bartonian | 41.3 | 38 | Thanetian to Bartonian (Hot) | Hot | Ignore |
| Priabonian | 38 | 33.9 | Priabonian to Holocene (Cold) | Cold | Ignore |
| Rupelian | 33.9 | 28.1 | Priabonian to Holocene (Cold) | Cold | Rupelian Icehouse |
| Chattian | 28.1 | 23.03 | Priabonian to Holocene (Cold) | Cold | Ignore |

Literal target total: 9 Hot, 10 Cold, 2 NA. The **label-implied** Thanetian–Bartonian interval would instead give 11 Hot and 10 Cold. That is an interpretation/repair, not execution of this held source.

The 13 literal regime labels are Fortunian–Darriwilian Hot; Sandbian–Homerian Cold; Gorstian–Givetian Variable; Frasnian–Famennian Hot; Tournaisian–Changhsingian Cold; Induan–Hettangian Hot; Sinemurian–Pliensbachian Cold; Toarcian Hot; Aalenian–Hauterivian Cold; Barremian–Santonian Hot; Campanian–Selandian Cold; the inconsistent label Thanetian–Bartonian Hot; Priabonian–Holocene Cold. Labels include source categories called cool/warm in nearby comments; they are not evidence of ice presence or a numerical global-temperature cutoff.

## Which variable feeds the reported latitude-gradient comparison?

The held plotting source uses **`hot_or_cold`**, not the narrower icehouse/hothouse variable, for the directly relevant pooled contrast:

1. `master-script.R:70` sources `define-time-ints.R`, which constructs the explicit interval metadata. A held plotting preparation route joins `grid_cell_intervals` onto `grid_cell_plotting_data` (`load-shiny-data-for-plotting-figures.R:6–7`).
2. `plot-main-LGB-figures.R:49–58` puts `climate_regime_intervals` and `hot_or_cold` in its active facet-variable vector; **neither narrow icehouse/hothouse variable is in that vector**. Lines 135 and 148 use the selected variable for panel/grouping; line 219 fits the within-panel log-richness slope. Lines 479–482 write `Table X hot_or_cold model_tidy.csv` for the 1000 km, no-high/cold-exclusion version.
3. The explicit slope-difference path filters stage data with `facet_var == "hot_or_cold"` (`plot-main-LGB-figures.R:514–520`), removes Variable at 552–555, log-transforms richness at 559–562, and fits the predictor-by-facet interaction at 564, with `na.action="na.omit"`. It obtains contrasts at 570–578. This is the direct code-level basis for a primary author-Hot/Cold rule; an extreme Icehouse/Hothouse analysis would be a separate choice.
4. The corresponding manuscript locators are 1033–1066 and Figure 9 caption 2330–2339; they identify pooled warm/cold classes, latitude slopes and the climate interaction. The latitude-zone richness comparison uses the same broad class: `plot-main-LGB-figures.R:1813,1823–1834`, corresponding to manuscript 1068–1084 and Figure 10.

**Call-path limit:** this is static source tracing, not proof that this exact definition produced the published coefficients. `load-shiny-data-for-plotting-figures.R:4` loads a dated saved-output script, `./output/marine_inverts/2022-07-12-13-05-12-including-almost-everything/source-me-to-load-shiny-data.R`. That output path is absent from the cached archive manifest. A complete publication replay or a retained author stage-definition output could supersede the suspect line; neither was found among the held source/metadata/manuscript candidates. No saved output was executed or acquired.

## Table availability and exact missing members

The code supplies an explicit table-generation route: `subscripts/plotting-scripts/plot-main-LGB-figures.R:438–456` selects stage, period, climate-regime interval and Hot/Cold/Variable, joins equal-length bins, and writes **`{folder.name}/lbg-tables/Table S1.html`**. The held manuscript calls the definitions **Table S2**, so numbering differs between held code and manuscript. Do not assert that the uninspected published supplement agrees with either version.

A filtered inspection of the complete cached ZIP central-directory list (`scratch/q027-independent-audit/archive-members.tsv`, excluding bundled `renv`) found no output directory or Table S1/S2 member, and no standalone climate-class table. Thus no exact deposited Table S2 archive member can be named from this manifest. The climate-definition member itself is already held:

`marine-lbg-ms-code-submission-2025-04-22 2/subscripts/define-time-ints.R` (manifest line 55399, 13,525 uncompressed bytes, 2,963 compressed).

If the distinct within-cell temperature zones are needed later, the exact unheld small member is:

`marine-lbg-ms-code-submission-2025-04-22 2/subscripts/load-gcm-data.R` (manifest line 55401, 4,029 uncompressed bytes, 1,389 compressed).

The archive also contains `marine-lbg-ms-code-submission-2025-04-22 2/input/gcm_data_df.rda` (line 2358, 240,732,239 uncompressed bytes) and `input/PaleoDEMS netcdf/stages_scotese_lookup_table.csv` (line 2543, 5,597 bytes). Neither is required to expand the explicit stage classes, and neither was acquired/read here.

## Mechanical verification and provenance

- Python standard library independently parsed the literal climate case lines and expanded inclusive ranges using the archived PBDB stage ordering. Assertions: 21 target stages; all 100 source stages covered except exactly Thanetian and Ypresian; 98 assigned broad classes. No occurrence table was opened.
- A separate base-R interval-only check reproduced the crucial line-113 membership as `Lutetian, Bartonian`; replacing only its boundaries with the label-implied endpoints would return `Bartonian, Lutetian, Ypresian, Thanetian`. This was no estimator/pipeline execution.
- Code source: immutable Zenodo record 15269137, held via earlier bounded ZIP member retrieval and CRC verification, documented in `data/q027-support-audit/README.md`. The locally recomputed climate-source SHA256 agrees with `scratch/q027-independent-audit/source-member-checksums.tsv`.
- Archived PBDB interval metadata source and date: source `README.txt:3–4,65–66` specifies the occurrence-associated interval download of 23 May 2022; `make-intervals.R:11` reads `./input/pbdb_time_int.csv`. This audit used `data/raw/benson2025/pbdb_time_int.csv` only.
- Accepted manuscript provenance: `scratch/ranking-primary-check-20261028/receipt.json` records Bristol CC BY accepted manuscript, retrieved 28 October 2026, visible editorial comments, not Version of Record, URL `https://research-information.bris.ac.uk/ws/files/459336927/Phanerozoic_LBG_11Nov2024_ES_RJW-SZS-DJL.pdf`; receipt PDF SHA256 `ea6896715b06a5b242dadbbfc1661c9e807dbc44b735b80ac0132f41a1a607e8`.

Locally recomputed file hashes:

- `scratch/q027-independent-audit/source/subscripts/define-time-ints.R`: `57d45a486d945029c21415ca679b94e3ce0d8b9cc91d2e8b74f62c5d9ba95958`
- `data/raw/benson2025/pbdb_time_int.csv`: `023c31855b30247b324a2fb2c2edeb493eef84f898c082c359d647da3c3f9765`
- `scratch/ranking-primary-check-20261028/benson-aam.txt`: `9cbe82aa3ca6ccfe5b907601b79b63c37d4aa9d01ab2665ec0028a1f4c81e590`

## Handoff

Parent Codex owns the frozen choice of climate definition and candidate stage pairs **before** inspecting support outcomes. The literal broad source classes permit a reproducible support-only check while excluding the two NA stages; a label-implied sensitivity needs explicit identification as a repair. No statement here establishes a pair's sampling support, estimator feasibility or scientific validity. No occurrence identifiers or support outcomes were used to choose a classification.

## Independent pair/support verification after declared evaluation

29 October 2026. Parent explicitly authorised outcome inspection after declaration and evaluation. This check imported neither `check.py` nor the support builder. It reused this explorer's previously reconstructed, Python-expanded and base-R-checked 21-stage source table, then independently formed Cartesian opposite-class pairs within periods. It recomputed stage region sets directly from `support.tsv`: region qualifies only when both 0–20 and 20–40 rows have `cells_ge2_within_region_band >= 1`, excluding EU/NAm/UNKNOWN. It never used `region-band-overlap.tsv` or its flags, opened occurrence data/IDs, or ran an estimator.

**All checks pass:** all 21 declared class rows (including numeric source bounds), all 103 unique candidate pairs, all 42 stage-region rows, and every field of all 206 unique result rows agree. Summary pass counts, plan/script hashes and saved declaration/output hashes also agree. Candidate counts by scenario are literal 45 (35 Cretaceous, 10 Paleogene), label-implied 55 (35 Cretaceous, 20 Paleogene), and strict 3 (all Paleogene).

| Class scenario | Dated public members: passing pairs | Original deposit: passing pairs |
| --- | ---: | ---: |
| Literal author Hot/Cold | 3 | 7 |
| Label-implied sensitivity | 3 | 9 |
| Strict source Icehouse/Hothouse | 0 | 2 |

All three primary dated-public passes are Cretaceous: Albian–Campanian (AF, AS, SA); Albian–Maastrichtian (AS, SA); Barremian–Campanian (AF, SA). Exact stage-region sets and shared sets match the parent outputs.

**Interpretation:** the observed pass permits a next estimator-specific eligibility check, not a richness comparison, power claim or independent regional replication. This screen's collection-age palaeocoordinates, 555-km approximate grid, occurrence-row region assignment and containment rule differ from the author stage-to-map reconstruction lookup, dggridR, modal-region cell exclusion, majority-overlap allocation and incidence coverage rules. Their joint changes are non-nested: a support-screen failure is not an upper bound on author-estimator support, and a pass need not survive author eligibility. Even the age-only difference has a point-range exception: the strict >50% source rule cannot assign zero-duration records retained by containment.

The literal/label discrepancy remains: Thanetian and Ypresian stay NA in the primary rule and become Hot only in the labelled repair sensitivity. The equal dated-member pass count after repair does not resolve author intent. The prior support-informed focal choice is disclosed in `plan.json`; the complete within-period enumeration avoids omission of other declared pairs but does not turn that focal choice into a blind test. Board declaration timing itself was not independently replayed in this aggregate audit.

SHA256 at verification:

- `data/q027-regional-support/support.tsv`: `8f253a64ddd2dfb2230df35e1be02fb8da5b818e1c8a7dfdc95adfaddeab3459`
- `data/q027-climate-pairing/check.py`: `983bbdb3d845c538fa62f99e854a09b8fc84da243b5d73ec70e28a61d850b78a`
- `data/q027-climate-pairing/declaration/source-classes.tsv`: `0355db594c18d7bd228dd694f90130b020b09240fd0b33b46d5067a3496228e8`
- `data/q027-climate-pairing/declaration/candidate-pairs.tsv`: `c33be34bc46cd7dd1eb67664f43a2451fed050d6ca7274d7b346c6399b3a0d1e`
- `data/q027-climate-pairing/declaration/plan.json`: `2c260e83de596acad4f59d7c562bf71bb5eafe119b875e746b6619c17fcdce84`
- `data/q027-climate-pairing/results/pair-results.tsv`: `a14c64b481a1e8716c0a72a1ff692453dc43c66dd9e87393b79955f6a252e039`
- `data/q027-climate-pairing/results/stage-regions.tsv`: `2baf3f3755770e663b4b764a666abb06e570d14fa937a24a3588d34b4667c157`
- `data/q027-climate-pairing/results/summary.json`: `e60697eacc0bc05c23151565097a96af9ea5d461891ef6ab727323a79f7352f3`

Parent integration clarification: the complementary full-archive inspection
resolved stage coordinates as the author stage-to-map lookup, not general
midpoint rounding. That wording is corrected above; classes and pair results
are unchanged. See `estimator-contract.md` for the exact source path.
