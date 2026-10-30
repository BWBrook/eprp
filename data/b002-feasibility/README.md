# B-002: coupling and physical support in the held sources

30 October 2026. Completed bounded tranche following Claude's critique in
Correspondence 96/2581 and Barry's instruction to assess it and proceed.
Main Codex integrated two bounded GPT-6.1 Sol audits and performed the
workbook calculation and independent numerical checks. The
[response](../../ideas/2026-10-30-b002-critique-response-codex.md) gives the
allocation decision; [PROTOCOL.md](PROTOCOL.md) defines this calculation's scope.

**Result: the held tables cannot identify a through-growth buoyancy map or
the proposed route-connectivity test.** They support descriptive size-pair
associations, a within-specimen volume-proportion diagnostic and three
reconstruction-conditional endpoint loading calculations. They supply neither
the proposed thickness series nor a complete physical animal at each growth
stage. Park this held-table shortcut; B-002's broader theoretical question
remains provisional. No route search or empirical barrier test was run.

Claude's warning about imposed coupling is sound. His automatic stop rules
based on weak association, failure to reject isometry, complete decoupling or
one-coordinate monotonicity are not valid in general. The
[mathematical check](mathematical-check.md) gives corrected conditions and
counterexamples. This support failure does not establish that development
is unconstrained or that an earlier-stage physical barrier is absent.

## 1. What the workbook can describe

The unchanged [Walton–Korn source](../ammonoid-growth-support/README.md)
contains 179 series and 2,643 jointly measured diameter/CWI/UWI/WER positions.
It lacks row-linked maturity and evolutionary transitions. Its source study
selected mainly pachyconic/globular late-growth forms, generally CWI 0.60–1.10
and UWI 0.00–0.30, with exceptions. This restricts late-shape variation before
any correlation is calculated. The study uses typical/best-preserved examples;
these rows are not a random sample of possible developmental programmes.
[Walton & Korn 2017, Material and method](https://doi.org/10.1111/pala.12308).

We calculated ratios at two fixed pairs of **native diameter values**, using
log-diameter interpolation with a maximum twofold bracket and no extrapolation.
Neither pair is labelled juvenile/adult. The original workbook does not state
diameter units; its values and metadata remain unchanged. Each early ratio is
regressed descriptively on all three late ratios with an intercept. These
in-sample R² values have no coupling threshold, p-value or inferential interval.

| Native diameter pair | Eligible source rows | Original family labels | CWI R² | UWI R² | WER R² |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2 → 10 | 178 | 41 | 0.3762 | 0.2147 | 0.1937 |
| 5 → 20 | 124 | 37 | 0.5741 | 0.4793 | 0.3805 |

The first pair excludes one row lacking joint lower-size coverage; the second
excludes 55 lacking upper-size coverage. All source diameter sequences pass
the monotonicity check. These are different size references **and different
row sets**, so their R² difference does not isolate a developmental-stage
effect. The 302 paired records reuse series across the two comparisons and
are not 302 independent specimens. Repeated taxon labels are retained.

[workbook_size_pairs.tsv](workbook_size_pairs.tsv) contains derived values,
source-row identities, bracket cell locators and interpolation weights;
[workbook_eligibility.tsv](workbook_eligibility.tsv) records every inclusion
and exclusion. [workbook_summary.json](workbook_summary.json) also retains
same-ratio correlations, coefficients, ranks and ranges.

This answers a descriptive question about the held proxies. It cannot identify
which combinations of early and late geometry are developmentally possible,
heritable, physically viable or connected by evolutionary change. A nonlinear
deterministic relation can have zero linear R², and even statistical independence
of measured summaries would not establish independent control of the underlying
growth programme. Strong association is likewise compatible with selection,
phylogeny or common measurement structure. Neither result is a barrier test.

## 2. Physical observables and the missing map

| Source and checked locator | What the held material supplies | Limitation for the proposed calculation |
| --- | --- | --- |
| [Naglik et al. 2015](https://doi.org/10.1111/let.12085), Tables 2–4 pp. 32–35, Methods/Data set pp. 35–36 | Chamber and septum **volumes**, diameters, aperture heights and septal spacing through three individuals | No tabulated wall-thickness series or septal surface areas. Authors did not measure body-chamber volumes. Labelled outer-wall segments are not tabulated. Reconstruction and segmentation errors are not a fitted uncertainty distribution. |
| [Naglik, Rikhtegar & Klug 2016](https://doi.org/10.1111/let.12125), Methods/Table 1 pp. 4–5, Table 2 p. 8, buoyancy p. 9 | Endpoint shell-plus-septa, living-chamber, siphuncle and gas-space volumes, with assigned densities | Same three specimens as 2015. Two body chambers reconstructed by removing 5 and 16 terminal septa using other specimens/literature. Endpoint reconstruction does not identify earlier living-chamber geometry. |
| [Tajika et al. 2014/2015](https://doi.org/10.1080/08912963.2013.872097), author text Methods pp. 2–4, Table 1/buoyancy pp. 5–6 | One mature Normannites reconstruction, separating outer shell, septa and lappets; endpoint comparison with lappets removed | Terminal component volumes are not a thickness trajectory. Conch thickness in the text means whole-conch width. No numerical extraction was made without an accessible table image. |
| [De Baets et al. 2012](https://doi.org/10.1111/j.1558-5646.2011.01567.x), Results on initial chamber/coiling, Fig. 10 and developmental-constraint discussion | Distinct histories of embryonic and post-embryonic coiling | Challenges a universal one-to-one coiling rule; does not identify unrestricted recombination, mutation controls or a feasible bypass. The authors retain morphogenetic and soft-part limitations. |

Thickness is not volume. A septum's volume also depends on its area, curvature
and thickness distribution. Fitting log volume against log diameter would
estimate a different quantity, with isometric exponent **3**, not the
thickness exponent **1**. The table does not identify an independent thickness
uncertainty model. Fitting three endpoint species as though they were a single
ontogenetic trajectory would add another error.

For an actual stagewise mass balance we still need the outer-shell material,
water-excluding displaced region, living chamber and soft-tissue/mantle-cavity
occupation at each stage, linked to septa and siphuncle geometry. Retained
internal chambers cannot simply be truncated at a septum and called the living
animal at that time. Stage-specific legitimate liquid-loading limits and the
ecological reason to require neutral buoyancy are also unestablished. Dynamics
would additionally require a fluid history; stability requires the same
allocation's mass centres. These missing quantities prevent evaluating the
margin field on which component labelling would operate.

## 3. Two physical calculations that the sources do support

**Volume proportions.** Six spaced post-10-mm chambers of the Fidelites
specimen were selected for a small illustrative calculation, avoiding the
most resolution-limited early measurements. This is a source replay, not a
representative or exhaustive allometry analysis. All displayed source precision
is retained in [the input table](naglik2015-fidelites-selected.csv).

| Chamber | Diameter (mm) | Chamber volume (mm³) | Septum volume (mm³) | Septum/chamber volume |
| ---: | ---: | ---: | ---: | ---: |
| 45 | 11.12 | 34.415 | 2.82 | 0.08194 |
| 50 | 15.2 | 98.7 | 7.06 | 0.07153 |
| 55 | 20.7 | 224.95 | 13.2 | 0.05868 |
| 60 | 29.16 | 547.82 | 21.735 | 0.03968 |
| 65 | 39.35 | 1191.62 | 42.18 | 0.03540 |
| 69 | 49.47 | 2281.69 | 67.92 | 0.02977 |

The ratio falls **63.67%** across these selected reconstructed points. Half-unit
intervals at the last printed digit cannot make the six ratios equal; those
are rounding checks, not reconstruction-error confidence intervals. Thus an
exact fixed septum/chamber proportion does not describe these tabulated points.
The source already reports differing chamber/septum scaling. This does not
identify wall allometry, total shell fraction or the sign of the juvenile
buoyancy margin. [Derived proportions and rounding bounds](volume-proportions.csv).

**Endpoint loading.** With the literal 2016 component model, write shell-plus-
septa, living-chamber, siphuncle and gas-space volumes as `Vs,Vb,Vy,Vp`. For
the source's assigned densities and zero gas mass:

```
V  = Vs + Vb + Vy + Vp
M0 = 2.62 Vs + 1.055 Vb + 1.055 Vy
q  = (1.026 V - M0) / (1.013 Vp)
```

Here `q` is the liquid fraction needed for static neutral buoyancy if the entire
gas-space volume were continuously loadable. This is a mathematical capacity
envelope, not an observed physiological loading range. The table's living-
chamber region is used as supplied; its soft-body/mantle-cavity separation is
not independently reconstructed here.

| Reconstructed endpoint | Component volume (cm³) | Recomputed gas-only mass (g) | Required q |
| --- | ---: | ---: | ---: |
| Fidelites clariondi | 51.205 | 47.612740 | 0.37910 |
| Diallagites lenticulifer | 11.393 | 10.459045 | 0.35498 |
| Goniatites multiliratus | 8.335 | 8.030360 | 0.31324 |

Crossing source-discussed shell density {2.62, 2.66} with fluid density
{1.013, 1.026} gives q ranges 0.36046–0.37910, 0.33556–0.35498 and
0.29456–0.31324 respectively. They are scenario ranges, not probability
intervals or comprehensive uncertainty bounds. All three endpoints fit the
idealised capacity interval. Their gas-only orientations are not thereby
validated under an unspecified liquid distribution.

The [input](naglik2016-endpoints.csv), [endpoint replay](endpoint-loading.csv)
and [density scenarios](endpoint-density-sensitivity.csv) preserve the source
totals alongside recalculation. Fidelites' printed total mass 47.617 equals
the sum of its displayed rounded component masses; the displayed volumes
times densities give 47.612740, consistent with the text's 47.613. This is
retained as a rounding/order-of-calculation distinction, not a demonstrated
source defect. No source total is silently replaced.

Under exact similarity of **all** component regions, fixed densities and
coherently scaled capacity, the common length-cubed factor cancels from q.
The changing septum/chamber ratio shows why that full null should not simply
be assumed. It does not determine q's trajectory: the other stage components
remain missing. A confidence interval covering an isometric exponent would
not establish equality or negligible physical effect either.

## Reproduction, verification and custody

Run from the repository root:

```bash
uv run --python 3.12 data/b002-feasibility/workbook_diagnostic.py
uv run --python 3.12 --with numpy==2.1.3 --with openpyxl==3.1.5 python -m unittest discover -s data/b002-feasibility -p 'test_*.py'
python3 data/b002-feasibility/physical_diagnostic.py
```

The workbook script pins Python 3.12, NumPy 2.1.3 and openpyxl 3.1.5, refuses
an unexpected source hash and checks schema/row order. Execution used Python
3.12.13. The physical script uses standard-library Decimal arithmetic;
source-table and script hashes are in [diagnostic-summary.json](diagnostic-summary.json).
No system environment, raw workbook or original PDF was changed.

[Verification receipt](verification.json), including the separate R fit results:

- Five controls cover exact zero retention, log interpolation, extrapolation,
  large gaps and empty coverage.
- Independent ZIP/XML extraction reproduced all 1,812 derived ratios in
  302 paired rows; maximum absolute difference 4.44e-16.
- Separate R `lm` fits reproduced all six R²/correlation summaries; maximum
  absolute difference 5.00e-16. These are numerical agreement, not biological
  validation or independent specimens.
- The physical-source delegate checked original table images and independently
  reproduced the three endpoint q values in R to <1e-12 and the ratio decline
  to <1e-10. Main Codex then checked the consequential table images and replayed
  the retained Decimal calculation.
- Mathematical claims were independently checked by a separate GPT-6.1 Sol
  delegate; main integrated the proofs and counterexamples. No empirical
  applicability follows merely from agreement.

The two held publisher PDFs remain in ignored
`scratch/blue-sky-codex/priors-20261015/`, SHA256
`794cbb7c47d4b285689e892b0a0d901efee54df6142b559c080cc4f91365f21f`
(2015) and
`1f05e487d091d84a77418983aece1c08367e7ac633c391af15fed6a7d9b2bc0f`
(2016). Primary numerical tables and relevant methods were reread. Tajika was
read as author-uploaded article text; PDF routes failed with 404/403, so no
fresh numerical transcription is claimed. De Baets and Walton–Korn were read
in relevant publisher sections. No TDM text, new specimen request or broad
source campaign was used. B-002's Bayer/Urdy prior gaps remain open.

Main Codex owns these results. Q-009's finite later-response support check was
invited from the existing References owner in 76/2583; acceptance is pending.
This source-support result changes the proposed next allocation, without
selecting a primary project or changing the original question registers.
