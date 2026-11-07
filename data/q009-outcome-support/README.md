# Q-009 outcome and information-window table

**8 November follow-up:** the [counting-noise and precision screen](../q009-noise-precision/README.md)
finds that the specified fixed-six-taxon summed-CV forecast has no defined
outcome in any of its seven prospective evaluation windows. A fixed-scale
variance alternative is defined, but its precision and noise control remain
uncertified. The sparse Walvis source cannot directly replicate the 150-kyr
design. This supersedes immediate development of that summed-CV endpoint;
the table below retains the broader source possibilities and their limits.

7 November 2026. Completed by main Codex under Barry's direct assignment
(76/2964), integrating two bounded GPT-6.1 Sol primary-source audits and
an independent numerical check. References retains the library and original
[K–Pg alignment](../kpg-plankton-alignment/README.md). The old invitation is
superseded by this assignment.

**There is a concrete narrower empirical opportunity: predict genuinely later
Pacific assemblage variability from earlier biological state.** The original
samples have adequate temporal coverage for that comparison. The supplied
published analysis cannot simply be reused as a forecast: taxon selection
uses later observations, the richness baseline is global, and environmental
and age-model joins need explicit construction. The stronger claim about
local ecological memory after richness recovers, controlling environment,
is therefore **not yet an executable test**. No model was fitted here.

El Kef adds actual measured environmental series and two possible later-event
cases. Its chronology, gap and sparse usable windows make it a weaker first
forecasting dataset. The two sites are not established matched perturbation
replicates. These conclusions identify a usable development target and its
precise limits; they do not retire Q-009.

## The completed table

The full machine-readable [outcome-window-table.tsv](outcome-window-table.tsv)
records predictor information, later response, environmental support,
chronology, evaluation blocks and disposition for each route.

| Route | Later outcome and independent information | Window/evaluation support | Disposition |
| --- | --- | --- | --- |
| **Pacific future composition/variability** | Composition or variability calculated entirely within a later window of original percentage observations. A separate measurement family is unnecessary for a valid temporal forecast. | 990 original rows, 53.086199–66.247250 Ma; 24 of 26 fixed landmarks pass the timing census below. Taxonomy/missingness, richness scale and covariate joins remain unresolved. | **Best first development candidate**, with a rebuilt past-only analysis and explicitly narrower predictive claim. Timing support is demonstrated; complete predictor/outcome/environment eligibility is not. |
| **Pacific published ΣCV–carbon comparison** | Published summed CV and carbon-anomaly summaries, including later named disturbances. Fig. 2 workbook has 94 comparison rows, seven with labels. | Taxon selection uses each whole 1-Myr bin; moving-window placement is not stated. Event CIEs combine local/global sources; anomaly summaries include the event interval. | Useful source evidence and a prior result; **not a ready forward test**. Rebuilding the information boundary is necessary. Seven labels are not seven independent disturbances. |
| **Pacific separate process outcome** | Carbon isotopes are separately measured. Neither taxon-derived size/biomass nor Gibbs' recalculated trait percentages supply an independent community response. | Source isotope locations and calibrations must be joined; no verified complete local forcing/process-outcome panel is produced here. | Conditional proxy-forecast alternative. CIEs can reflect biotic feedback and preservation as well as forcing; they are not an exogenous treatment or direct export-efficiency measurement. |
| **El Kef future composition** | Later genus proportions or future-only variability from dominant counts/percentages; raw taxa could support a carefully defined richness proxy. | 186 dated samples. Only 2 of 8 landmarks pass the stated conservative timing rules, in both age models. Counts and percentages are the same observations. | A possible small within-series case, with low replication; weaker first choice than Pacific. Further windows at other horizons are untested, not ruled out. |
| **El Kef separate proxy outcome/environment** | TOC, CaCO₃, carbonate δ¹³C/δ¹⁸O and organic δ¹³C are actually measured and publicly deposited with sample/depth identifiers. | Jones 2023 supplementary Tables A4–A6; depths must be mapped to the revised 2026 age model. No complete joined-window count is asserted. | A genuine source lead. Preserve lab/measurement metadata; future-bracketing interpolation cannot enter a predictor. Proxy change is a narrower outcome than ecosystem function or resilience. |
| **El Kef named-event response** | Early excursion tentatively correlated with Dan-C2; late disturbance speculatively LDE-like. | Early case is one local candidate; late case enters poorly constrained P2 chronology. The Neobiscutum–Futyania change crosses a major hiatus. | Retain descriptive/event sensitivities. No confirmed matched later-disturbance evaluation set is established. |
| **Cross-site recovery/memory comparison** | Two contrasting local histories with different settings, preservation and chronology. | Pacific spans the younger El Kef interval, but no common forcing/outcome design, taxonomic calibration or age-uncertainty distribution is established. | Do not treat the two site trajectories as a controlled memory comparison. They may contextualise a within-site analysis. |

## What is newly established from the actual files

The [coverage summary](support-summary.json) is generated by [audit.py](audit.py)
from five pinned source files. The originals remain outside Git. Ages stay on
their supplied clocks; no cross-site age transformation is performed.

| Source product | Rows | Source age range | Interpretation |
| --- | ---: | --- | --- |
| Alvarez original percentages/metadata, Fig. 1 Q:CK | 990 | 53.086199–66.247250 Ma | 979 Site 1209 and 11 Site 1210 rows; median adjacent distinct-age gap 12.152 kyr, maximum 81.312 kyr. This is a local composite, not 990 independent ecosystems. |
| Fig. 1 A/L published variability series | 986 | 53.361510–66.169233 Ma | Approximately 13.003-kyr resampled grid. Interpolation adds no independent observations. |
| Fig. 1 N/O species-richness series | 53 | 53–66 Ma | Exact 250-kyr spacing. Global compiled range-through richness; spreadsheet row position is not a join to the original sample on that row. |
| El Kef dominant table, age model 1 | 186 | 62.350819–66.015840 Ma | Median adjacent gap 5.757 kyr, maximum 501.698 kyr. The small median does not remove the hiatus or age uncertainty. |
| El Kef alternative P0 age column | 186 | 62.350819–66.017573 Ma | Alternative chronology of the same samples; not independent replication. |

The Pacific source-investigator counts remain SA 741, SG 238 and PB 11.
[coverage-by-age.tsv](coverage-by-age.tsv) locates that change in time. Only
752 original rows are nonblank for all four previously selected genus groups
(requiring both Cruciplacolithus size classes). This is a missingness diagnostic,
not a complete compositional panel or a licence to recode blanks as zero.
Missing original integer denominators limits count models, but does not
disqualify all percentage-based forecasting.

**A declared timing census, not a power calculation.** We evaluated absolute
half-Myr landmarks on each source clock. Predictors use original rows in
the older 150-kyr window; outcomes use the younger 150-kyr window. Each needs
at least three rows, both windows must lie in the source range, and a window
cannot intersect an adjacent-source age gap exceeding 100 kyr. Pacific windows
must stay within one investigator code. El Kef windows must remain at or older
than 62.54 Ma because the younger chronology is poorly constrained. These
analyst-chosen rules were used to count timing support, not chosen by forecast
performance. There is no estimated age-error embargo in this census.

- Pacific: **24/26** pass. Landmarks at 56.0 and 66.0 Ma cross investigator
  codes. The passing windows are nonoverlapping by construction, but may still
  be serially dependent and share source procedures.
- El Kef: **2/8** pass in each supplied model, at 63.0 and 64.0 Ma. Source
  limits, sparse windows, large gaps or the young-age restriction exclude the
  others. Two timing pairs do not constitute an informative training/test
  design for a flexible model.

[timing-landmarks.tsv](timing-landmarks.tsv) records every count and exclusion.
These numbers do **not** count complete covariate-supported forecasts,
independent disturbances or effective statistical replicates. Environmental
joint support and taxonomic/missingness eligibility have not been tallied.
Other window lengths or landmark choices could change the timing result.

## The source distinctions that change the design

**Pacific variability and richness.** Alvarez's Methods (accepted manuscript
lines 335–353) resample at about 13 kyr and select eight abundant taxa present
in more than 65% of samples within each 1-Myr bin, then calculate summed CV
over a moving 150-kyr window. The whole-bin selection can use information from
after a proposed cutoff. Window centering/trailing placement is not explicitly
specified. The source also supplies 250-kyr global range-through richness
for the full record and a separate 100-kyr Danian version. Neither should be
silently called local sample richness. [Alvarez et al. 2019](https://doi.org/10.1038/s41586-019-1590-8).

The [literal Fig. 2 comparison rows](published-comparison-rows.tsv) retain
labels I2, I1, `HI`, PETM, ELPE and two LDE entries. These are representative
comparison rows, not a cleaned onset catalogue. Extended Data Table 2 supplies
the actual event/tie-point reference, with additional events and different
dates. The intended source age framework includes the Westerhold updates;
the differences do not by themselves prove incompatible clocks. Their mapping
must be resolved before using event dates to count pre/post samples.

**Gibbs is related evidence, not a new Pacific replicate.** Its Site 1209
percentages reuse Alvarez, with specified taxonomic updates and interpolation.
Its summed inferred mixotroph fraction and biovolume derive from community
abundance/trait assumptions. They may motivate a state variable, but cannot
be presented as an independently measured ecosystem response. The source
also uses carbon-isotope/XRF ties to correlate Pacific and Walvis Ridge.
[Gibbs et al. 2020](https://doi.org/10.1126/sciadv.abc9123).

**El Kef has real environmental data.** The
[Jones 2023 supplement](https://doi.org/10.1130/GSAB.S.21445755.v1), Data1,
Tables A4–A6 provides the five measured sediment/isotope series above; A1–A3
provides depth/splice information. Data2 includes older competing age models,
which do not embody the 2026 revision. The 2026 analysis interpolates between
bracketing geochemical samples. A younger bracket can leak information into
a putatively earlier predictor; carry measured support distances through the
join. The revised record retains an approximately half-Myr or larger hiatus
and poorly constrained ages younger than about 62.54 Ma.
[Jones et al. 2026, §§2.3–2.4, 3.1, 4.1](https://doi.org/10.1029/2026PA005729).

## Recommended next development product

Use **one Pacific continuous-series forecast** as the candidate, with future-only
assemblage variability as its outcome. Its scientific question is whether
earlier biological state adds predictive information about later observed
behaviour. It does not require a label of independent disturbance at every
forecast origin. This is a narrower test than ecological memory specifically
after local richness has recovered.

The concrete preparation should produce one joined analysis table and a
frozen, simple forecast comparison:

1. Resolve the original 981-versus-990 sample/splice discrepancy, blank versus
   zero conventions, common taxon treatment and age/event correspondence.
   Inspect existing source code before inventing replacements. Select a
   contiguous investigator-consistent segment; do not treat holes as independent
   validation sites. Keep disputed samples in explicit sensitivities.
2. Choose and name the richness target honestly. Global range-through richness
   is available; local recorded morphogroup richness would need a justified
   observation/missingness treatment and is not species richness. The main
   Q-009 claim cannot use one in place of the other without stating the change.
3. Rebuild taxa/ordination/scaling and variability from training/past information.
   Use a future-only window and an age-uncertainty buffer. Join measured
   environmental information with no future bracketing; count the resulting
   complete cases. If a joint environment panel is unavailable, reduce the
   stated claim rather than interpreting unmeasured environment as memory.
4. Compare richness, time since K–Pg, available environment, sampling metadata
   and past variability/persistence with the same baseline plus one fixed,
   interpretable biological-state summary. A strong persistence baseline is
   essential. Test on younger held-out blocks, purging training outcomes that
   overlap a test information window. Fix a consequential score increment and
   uncertainty target before fitting; the 24 timing landmarks do not establish
   precision for it.

A small predictor that improves a genuinely later forecast would be a positive
empirical result at that declared observational level. An informative negligible
increment could also be useful. Neither would establish biological causation,
direct ecosystem function or that the omitted state is uniquely identified.
The published recovery ordering and same-window correlations are already prior
results and are not the new payoff. This table recommends the preparation;
it does not select a primary investigation or claim the fit is already ready.

## Evidence, reproduction and remaining limits

Reproduce the aggregate source and timing counts with standard-library Python:

```bash
python3 data/q009-outcome-support/audit.py INPUT_DIRECTORY
```

`INPUT_DIRECTORY` contains the five hash-pinned files named in the script:
original Fig. 1 workbook, Fig. 2 workbook renamed `alvarez-fig2.xlsx`, and
PANGAEA tables 893899, 893919 and 997781. The 893899 interpolated table is
retained as a provenance check; original samples drive the timing census.
Source hashes and the script hash are in the summary. The calculation does
not query the restricted library, alter the existing alignment or export
raw/derived source rows.

Public primary-source methods, supplementary fields and representative tables
were inspected on 7 November. Alvarez's accepted manuscript and its event
table were checked beyond the abstract; Jones 2026 full methods/results and
the 2023 supplement were read; Gibbs article and supplement/data were inspected.
[sources.tsv](sources.tsv) records identifiers, URLs and access depth.
The source audits used legitimate public copies. Original PDFs/workbooks
remain in ignored scratch; their own licences apply. PANGAEA's Alvarez
NC/ND terms and the workbook's unestablished redistribution terms are not
replaced by this repository's content licence.

The independent verification receipt is [verification.json](verification.json).
This verifies extraction and arithmetic, not statistical power, age models,
functional trait truth or ecological causation. Chronology uncertainties,
local richness, complete covariate joins, matched-event replication and
precision of added predictive value remain open. The decisive advance here
is the completed, source-linked table and a concrete narrower candidate,
rather than a claim that data density alone establishes readiness.
