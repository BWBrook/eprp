# Q-050: specimen, chronology and environmental support

Owner: Codex. Bounded source audit, 13 October 2026. Supports
[reply 10](../../ideas/2026-10-13-phase2-codex-reply-10.md) and extends the
[two-object numerical inspection](../q050-covariance-support/README.md).

**Finding:** a concrete same-site environmental route exists, but the numerical
specimen-to-sample crosswalk remains incomplete. Initial scripted workbook
downloads returned HTTP 401/403. Barry subsequently supplied the workbook;
Codex verified its identity during the portfolio checkpoint below. Five
environmental tables were retrieved and inventoried. No phenotype/environment
join, model fit or recovery simulation was performed. Joint support remains
unresolved; neither the earlier access failure nor the present support limit
establishes that the scientific question fails.

## Original phenotype data and coordinate contract

[Brombacher et al. 2017](https://www.journals.uchicago.edu/doi/full/10.1086/692570),
Methods: Material/Analysis, Figure 1 and Appendix A1, describes two thermocline
species from the **same Site U1313 primary shipboard splice**. There are 75
samples approximately 30 cm apart over the reported 2.4–2.9 Ma interval,
split into phases of 20/30/25 samples at 2.72 and 2.54 Ma. Both species therefore share one environmental trajectory
and chronology. They provide contrasting responses, not independent climatic
replicates. Individual cycles and phases are nested within this record.

The original measured traits are edge-view projected area and height/width.
The paper describes size sieving, species selection and unit-variance scaling
for its phenotypic covariance analysis. The Tsuboi archive README instead
describes natural-log traits. These are separate coordinate choices: the
archive's two means and covariance matrices must be reproduced from specimens
before treating them as the original paper's scaled matrices. Appendix A1's
average repeat-measurement error percentages do not supply an error covariance
model for every sample.

Dryad [dataset 10.5061/dryad.8jf2k](https://doi.org/10.5061/dryad.8jf2k),
dataset ID 3031, version 3046, has one listed file:

- `Data Brombacher et al.xlsx`, file 19832, 845,521 bytes.
- Declared MD5: `2498cdd3fab3ddb67ae1d52478620a53`, **now locally verified**
  on the supplied workbook; it was unverified at the initial source audit.
- Metadata describe specimen measurements, sample IDs and ages after Bolton
  2010; licence CC0. Published 17 March 2017; modified 21 September 2019.
- [Dataset API](https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.8jf2k)
  and [file-list API](https://datadryad.org/api/v2/versions/3046/files) succeeded;
  list `count = total = 1`, with no further file page.
- API download returned 401; public `downloads/file_stream/19832` and legacy
  `stash/downloads/file_stream/19832` returned 403, including a cookie-session
  attempt. No verified alternate workbook source was found in the bounded
  DOI/title/filename search. Metadata are not inspection of workbook contents.

**Checkpoint receipt, 13 October:** Barry supplied
`data/raw/dryad-downloads/doi_10_5061_dryad_8jf2k__Data_Brombacher_et_al.xlsx`.
Codex independently verified 845,521 bytes, the declared MD5 above and SHA-256
`195e15b36f599e9f8c064be046a1d08df58d2dbdb625688407d1d1fcb28b311f`.
The file is ignored by Git. This resolves access and byte identity; no workbook
values, specimen aggregation or joins were inspected during the checkpoint.
The earlier HTTP failures remain retrieval history, not a current blocker.

Required first join: original specimen ID and taxon → original sample/interval
→ source depth and age → each Tsuboi sample index. Preserve source labels,
interval endpoints, exclusions and repeated measurements. Confirm counts,
trait order, log/scaling rules, means, covariance divisor and time direction.
The earlier totals (6,575 and 6,058 specimens) remain sums of archived `nn`,
not counts independently checked against this workbook. Do not reconstruct
absolute ages by attaching a guessed endpoint to the elapsed `tt` grid.

## What the chronology establishes

[Bolton et al. 2010](https://doi.org/10.1029/2010PA001951), §§3.1–3.4,
Figures 2–4 and §3.6, aligns local benthic δ18O manually to LR04 with ties
at glacial–interglacial transition midpoints. Brombacher uses this chronology
and regresses morphological first differences against **global LR04**. These
are shared dating dependencies; LR04 is neither an independent local
thermocline exposure nor independent validation of isotope–morphology timing.
This does not invalidate every association: within-core depth order can be
informative, and common age offsets may cancel in relative comparisons.

The reported 6 kyr uncertainty is for the LR04 age model at 3–1 Ma, not a
Gaussian standard deviation to assign independently to each sample. Alternative
LB10 tuning covers only MIS 101–95; the MIS 100 onset differs by approximately
7 kyr. Numerical tie coordinates with a joint uncertainty model were not
recovered from the inspected public tables. Any future test must retain shared
ties and distinguish common offsets, local stretching and relative proxy
phase. Sample spacing is not effective resolution.

Brombacher cites 2–3 cm as average bioturbation depth when arguing against
mixing between 30 cm samples. The cited
[IODP lithostratigraphy](https://publications.iodp.org/proceedings/303_306/112/112_3.htm),
Unit I, describes **burrows up to 2–3 cm in size**, not a measured average
mixing depth. Unit II says uniform colour makes bioturbation difficult to
estimate. This does not establish the morphology samples' mixing kernel or
absence of within-sample time averaging. Original slice bounds and a
defensible mixing envelope remain required; burrow size alone is insufficient.

## Environmental tables actually inspected

These are whole-export row counts and age bounds, **not matched morphology
sample counts**. Ages are the source's ka BP; numerical bounds do not certify
coverage between them. All five exports carry CC BY 3.0.

| PANGAEA table | Rows; age range (ka BP) | Verified support and limitation |
| --- | --- | --- |
| [761442](https://doi.org/10.1594/PANGAEA.761442), Bolton benthic isotopes | 409; 2413.84–3331.68 | Sample labels, primary mcd, ages, δ18O and +0.64‰ corrected values. Local chronological reference, not direct thermocline temperature |
| [761443](https://doi.org/10.1594/PANGAEA.761443), Bolton planktonic isotopes | 440; 2413.84–2597.59 | Primary mcd, ages, *G. ruber* δ13C/δ18O. Only the younger part of the reported morphology interval |
| [736778](https://doi.org/10.1594/PANGAEA.736778), Naafs alkenones | 375; 2459.36–3681.98 | Sample/lab labels, sediment depth, **adjusted** mcd, annual SST and alkenones. 373 distinct sample labels; conversion to primary mcd remains unresolved |
| [892803](https://doi.org/10.1594/PANGAEA.892803), Bolton 2018 geochemistry | 652; 2413.836–2832.315 | Primary mcd, ages, crassaformis Mg/Ca/TWT and ruber Mg/Ca/SST/isotopes. 623 nonempty thermocline temperatures, 588 SSTs; 649 distinct depth values |
| [892804](https://doi.org/10.1594/PANGAEA.892804), Bolton 2018 assemblage counts | 132; 2431.576416–2828.803955 | Primary mcd, ages, *N. atlantica*/other-foram counts and concentration. Candidate context for changing assemblages; not identification of immigrant morphology populations |

One repeated Naafs sample label has separate laboratory IDs; the other,
`306-1313C-15H-5,20-22`, repeats lab ID `60020232` and all other fields except
SST (20.04 versus 21.00°C, at 3131.34 ka BP, outside the reported morphology
interval). Its provenance is unresolved. Bolton 892803 repeats
depths 116.560, 116.580 and 122.680 mcd; some accompanying ages differ slightly.
Preserve these source rows pending provenance adjudication.
Neither silently collapsing them nor merging on rounded age is justified.
Primary and adjusted composite depths are distinct coordinates even when their
values are close. The primary-depth isotope/geochemistry path is the first
candidate join, conditional on recovering the phenotype sample identities.

The 2018 export explicitly reuses Bolton 2010 and Friedrich 2013 measurements
and averages selected laboratory replicates. These are not independent source
replications. Its thermocline and surface temperatures use different proxy
calibrations; derived seawater isotopes include non-ice-volume-corrected and
ice-volume-corrected fields. They must not become independent observations of
temperature, salinity and ice volume in a likelihood without their common
measurement/calibration dependencies. The original source labels
*Globorotalia crassaformis* and *Truncorotalia crassaformis* are retained;
the numerical taxon/assay crosswalk is not verified here.

[Friedrich et al. 2013](https://doi.org/10.1002/palo.20029), §§2.1–2.2,
describes paired isotope/Mg/Ca assays from split *G. ruber* tests. This is
geochemical assay pairing, not pairing to the morphology individuals. Its
summer surface interpretation also differs from the annual alkenone proxy.
The 2018 temperature record does not cover the oldest portion of the reported
morphology series; extrapolating over that gap would add an assumption.

## Next gate and scientific limit

When next allocated after the portfolio checkpoint, verify the specimen
aggregation and same-primary-depth join, retaining unmatched samples, repeated
keys and the chronology dependency.
Do not substitute nearest-age matches without a supported depth/age contract.
Fix common trait coordinates and represent finite specimen counts, measurement
error and time averaging before constructing a joint mean/covariance fixture.

Even a successful join supplies phenotypic **P**, not genetic **G**, and an
environmental proxy, not a measured selection gradient. Plasticity, persistent
selection, immigration and size-dependent sampling remain rival explanations.
Only specified models with independently justified restrictions warrant a
bounded recovery comparison. An alignment regression or temporal ordering
alone cannot identify inherited constraint, selection and feedback. Novelty
and empirical mechanism discrimination remain unverified.

**Checkpoint observation clarification:** recover the actual sieve/fraction
protocol and its consistency across samples. Filtering shell geometry need not
be a hard projected-area cutoff, and retained lower tails alone do not identify
the excluded fraction. Treat selection as a modelled rival, not as a diagnosed
cause of covariance change. Restrict the candidate to bivariate phenotypic
mean/covariance dynamics in common trait coordinates. One proposed summary is
directional variance `u' P_t u` for predeclared directions; leading-axis
orientation requires resolved eigenvalue separation. Neither is genetic
evolvability. [Reply 11](../../ideas/2026-10-13-phase2-codex-reply-11.md)
records this qualification; no new fit or simulation is commissioned.

## Provenance and reproduction

Source access was on 13 October 2026. Search was restricted to Brombacher's
original deposit, its central chronological references and same-site proxy
archives; this was not a systematic resource or novelty review. A bounded
GPT-6.1 Sol source check inspected the primary methods/citation chain. Parent
Codex independently inventoried the retrieved tables and integrated the limits.
The delegate then reproduced the inventory byte-for-byte and caught the
repeated-laboratory-ID SST conflict during a focused source check.

Access depth: Brombacher publisher full-text methods/appendix; Bolton 2010
full-text methods/chronology; IODP lithostratigraphy; Friedrich 2013 methods;
PANGAEA full exports and descriptive/calibration headers. Bolton 2018's broader
mechanistic interpretation and Naafs's full analysis were not revalidated.
The [LR04 author table](https://lorraine-lisiecki.com/LR04stack.txt) was also
retrieved; its stack standard error is not age error or local habitat variance.
No original author was contacted.

Raw exports and Dryad API metadata remain in ignored
`scratch/q050-sample-crosswalk/`; publisher captures are retained there too.
[inventory.json](inventory.json) records exact download URLs, byte counts,
SHA-256 hashes, field completeness, ranges and repeated keys for the five
exports. [inspect.py](inspect.py) checks those hashes and rectangular schemas
and regenerates the inventory with Python 3.12 standard libraries:

```bash
python3 data/q050-sample-crosswalk/inspect.py scratch/q050-sample-crosswalk/sources
```

For a fresh checkout, download each `download_url` from the inventory to its
`filename` in that directory before running the script. A changed export fails
the hash check; inspect the change rather than replacing the pinned checksum
silently. The script never joins, repairs, drops or interpolates source rows.
Its summaries are audit metadata, not a prepared analysis dataset.
