# Pacific variability: counting noise and precision feasibility

8 November 2026. Completed main-Codex response to Claude's Board 144/2970
assessment forwarded by Barry. This is the next bounded tranche after the
[outcome/window table](../q009-outcome-support/README.md). Main integrated two
bounded GPT-6.1 Sol contributions: an independent methods audit and a Walvis
source check. The [protocol](PROTOCOL.md) fixes the diagnostic choices and
records the training-only inspection that preceded them.

**Decision: do not build or fit the proposed fixed-taxon summed-CV forecast.**
The endpoint is undefined in **all seven prospective evaluation windows**.
Counting noise is a substantial rival for a better-behaved variance endpoint,
and the precision check does not certify a consequential forecast increment.
The Walvis data exist but cannot directly replicate the 150-kyr design.
These results close this specific endpoint/design; they do not establish
absence of ecological predictability or a universal information limit.

## Original-sample endpoint check

We restrict the original workbook to Site 1209 and investigator SA, retaining
19 half-Myr landmarks from 65.5 to 56.5 Ma. Each uses older and younger
150-kyr windows of original percentages, with no interpolation. All selected
fields are numeric in every retained row; no missing row or zero is replaced.

Taxa were selected using 420 older samples at 60.15–65.9 Ma: explicit values
throughout training, positive in >65% of rows, mean abundance >=1%, excluding
the aggregate remainder and calcisphere fragments. All six qualifying fields
are retained: Zeugrhabdotus, Coccolithus, small and large Cruciplacolithus,
Ericsonia and Toweius. This is a fixed training-only diagnostic set, not a
reproduction of the source's changing million-year taxon sets. The source's
reported [500–1,000 liths/sample](https://doi.org/10.1038/s41586-019-1590-8),
accepted-manuscript Methods lines 314–318, defines the primary counting range;
exact sample totals are not supplied in the percentage workbook.

For each taxon, sample CV divides its within-window SD by its within-window
mean. When a selected taxon is zero in every sample, that ratio is 0/0. We
preserve the undefined result rather than selecting different taxa from the
future or declaring its CV zero.

| Domain | Windows | Earlier summed CV defined | Later summed CV defined |
| --- | ---: | ---: | ---: |
| Older training landmarks, >=60.5 Ma | 11 | 9 | 8 |
| Reserved separation at 60 Ma | 1 | 0 | 0 |
| Prospective evaluation landmarks, <=59.5 Ma | 7 | 0 | 0 |
| All diagnostic windows | 19 | 9 | 8 |

The seven evaluation windows are an announced possible split, not a completed
forecast test. This endpoint failure is specific to the frozen six-taxon
selection. Other taxon maps or statistics would be different designs; none is
silently substituted to obtain a positive result. The source's whole-Myr taxon
reselections are not a forecasting-safe remedy.

The predeclared companion is
`V = sum_j sample_variance(P_j) / a_j^2`, with positive `a_j` fixed to training
mean proportions. V is defined in all 19 earlier and later windows. It avoids
the random near-zero denominator, but still includes counting variation and
weights taxa relative to their training abundances.

## Counting-noise scenarios

The marginal multinomial population CV is
`sqrt((1-p)/(N*p))`. It is not the expected finite-window CV, and subtracting
such CVs does not isolate ecological variability. We simulated **4,000 joint
multinomial or Dirichlet-multinomial windows** per source window/scenario/null,
retaining the actual later sample count, selected taxa and a residual other
category. This gives 912,000 simulated windows across six scenarios and two
composition nulls, using seed 20261108. It is a conditional observation model,
not a claim to have recovered sample counts or the latent proportions.

The first null holds the **earlier** window's mean composition constant across
the future window. It is available at the forecast origin, conditional on
the assumed observation design. The second holds the **later observed mean**
constant and is an offline diagnostic; it must never enter a predictor.
Neither simulates ecological changes within a window, preservation bias,
age uncertainty or dependence among separately counted samples.

For the fixed-scale variance, the expected counting term under each frozen
composition p is `D/N * sum_j p_j(1-p_j)/a_j^2`. Marginal observation variance
is additive in sample variance under independent unbiased counting errors;
that identity does not identify its ecological and measurement components
from the supplied percentages.

| Counting scenario | Earlier-mean null: median expected counting V / observed later V | Later-mean diagnostic: median ratio |
| --- | ---: | ---: |
| N=500, multinomial | 0.548 | 0.499 |
| N=1,000, multinomial | 0.274 | 0.250 |
| N=250, stress scenario | 1.095 | 0.999 |
| N=2,000, stress scenario | 0.137 | 0.125 |
| N=500, design effect 2 | 1.095 | 0.999 |
| N=1,000, design effect 2 | 0.548 | 0.499 |

These are **scenario noise-to-observed ratios**, not estimates or certified
bounds on a biological variance share. They can exceed one. Unknown sample
totals, nonstationary composition and field-of-view clustering remain. Design
effect 2 is a deliberately hypothetical overdispersion stress, not estimated
from these samples. The selected proportions fit a residual-category simplex
arithmetically; this does not independently verify the source denominator.

The [complete scenario table](counting-scenarios.tsv) also retains summed-CV
null summaries. Their comparisons use only the **eight observed-defined
later windows**, and within each window only **defined simulated CVs**. Thus
the nominal 2.5–97.5% quantiles are conditional on simulated definedness, not
an unconditional 95% acceptance band. At N=500, the earlier-mean null has
8.98% undefined simulations on average across those eight comparable windows,
with one as high as 71.43%; the later-mean diagnostic averages 0.266%, with
maximum 2.125%. Reporting the average over all 19 windows would mix structural
absence with finite-count undefinedness. Those rates are separately labelled
in the table. The between-window ratios for summed CV are also conditional
descriptions; they are not an additive decomposition or a forecast gain.

The counting rival therefore needs explicit control. It does not explain away
all observed ecological variation, and it supplies no scalar ecological-noise
fraction to subtract. The endpoint's zero-denominator failure is already a
sufficient reason to stop the present summed-CV design.

## Dependence and the detectable increment

Across consecutive defined future windows, lag-1 response correlations are
0.953 for summed CV (seven pairs) and 0.915 for V (18 pairs). Finite AR(1)
mean-precision heuristics give effective counts about 1.13 and 1.63. Earlier
V has correlation 0.617 and a heuristic effective count about 5.03. Trends,
regimes, few pairs and estimation uncertainty make these weak descriptive
summaries; they are **not the effective sample size of an added predictor's
forecast score**.

For squared-error losses the paired gain is `D=L_baseline-L_enriched`.
Precision depends on the covariance of D, not merely the covariance of the
response. It is unknown before predictions are generated. We therefore report
a transparent conditional grid, rather than convert response autocorrelation
into an asserted universal power floor. The declared illustrative target is
**10% reduction in baseline MSE**, an analyst's pilot criterion rather than a
known biological threshold.

With two-sided alpha=.05, target power .8, known paired-loss covariance and
the usual normal approximation, detectable mean gain is approximately
`(z(.975)+z(.8))*SD(D)/sqrt(n_effective)`. The finite covariance calculation
uses actual half-Myr spacings. It excludes fitted-model uncertainty,
covariance-estimation uncertainty and departures from its Gaussian/AR(1)
working model. It is not actual power for this fossil record.

| Assumed paired-loss correlation | Conditional effective n for seven evaluation windows | Detectable relative MSE gain if SD(D)/baseline MSE =0.25 | Largest SD(D)/baseline MSE compatible with a 10% target |
| --- | ---: | ---: | ---: |
| 0 | 7.00 | 26.5% | 0.0944 |
| 0.25 | 4.55 | 32.8% | 0.0761 |
| 0.50 | 2.88 | 41.3% | 0.0605 |
| 0.75 | 1.74 | 53.1% | 0.0470 |
| 0.90 | 1.25 | 62.6% | 0.0400 |

[precision-sensitivity.tsv](precision-sensitivity.tsv) includes all 19
diagnostic windows, the 11 older training windows and the seven possible
evaluation windows, with four paired-loss scale assumptions. The smallest
detectable increment across the **declared grid** is already above 10% for
the evaluation set. That is conditional on the scale assumptions. No result
here proves that every possible method must have such a large paired-loss
SD; it could be smaller. Response ESS alone cannot settle that unknown.

## Walvis check and next decision

There is a genuine separate-sediment Walvis ODP1262 abundance series in
[Gibbs et al. 2020](https://doi.org/10.1126/sciadv.abc9123), Data S1 rows
791–816. It supplies **26 converted cell-percentage observations**, spanning
63.594–66.009 Ma, with median age gap 94.515 kyr and maximum 294.210 kyr.
None of five half-Myr landmarks has three observations in both adjacent
150-kyr windows, before further gap/range/age restrictions. Both Walvis and
Pacific 1209 were counted by the same analyst using related taxonomy and
chronology. Distinct sediment samples offer geographic evidence, but not
independent observer, trait-conversion or age-model errors.

The exact [Birch 2016 supplement](https://doi.org/10.1130/2016088) supplies
55 dated isotope rows, 60.97–66.46 Ma, with paired measurements for 11 taxa.
It is an actual separate proxy lead, not the source of the new Danian
nannofossil counts. Neither source supplies exact raw lith denominators for
the Gibbs Walvis cell percentages. A wider-horizon comparison may be possible;
it has not been designed or given a power guarantee here. See
[walvis-summary.json](walvis-summary.json) and [the source note](walvis-sources.md).

**Stop before the joined table and a fitted forecast under this design.**
The summed-CV endpoint fails outright; V is a possible replacement but not
noise-free, and its score precision is unestablished. The exact Walvis source
does not repair the seven-window evaluation design at this horizon.

The smallest remaining pilot option is a **development-only** V comparison
on the older windows to estimate paired-loss variability, with counting,
persistence and time baselines. Its value would be deciding whether any
later test could be informative; it could not itself establish the 10% gain.
That is a recommendation for scientific allocation, not a fit already run or
an automatic rescue of the current endpoint. Alternatively, seek a coarser
multisite comparison with genuinely adequate abundance support. The evidence
does not warrant promising a result from the full Q-009 ecological-memory
question on the current series.

## Reproduction and verification

```bash
uv run --python 3.12 data/q009-noise-precision/screen.py ORIGINAL_FIG1_WORKBOOK --private-output PRIVATE_OUTPUT_DIRECTORY
uv run --python 3.12 --with numpy==2.1.3 --with scipy==1.15.3 python -m unittest discover -s data/q009-noise-precision -p 'test_*.py'
python3 data/q009-noise-precision/walvis_audit.py GIBBS_DATA_S1_WORKBOOK
```

The main script pins its original workbook hash, parser, protocol, versions
and seed. [summary.json](summary.json) records these and hashes of private
window/simulation summaries. Original source rows, per-window vectors and
simulation payloads remain ignored. Public outputs are aggregate scientific
diagnostics and code; source licences remain those of the providers.

Four controls cover joint multinomial variance/covariance, Dirichlet-
multinomial overdispersion and zero categories, undefined CV versus defined
V, and finite covariance under irregular spacing. Independent R calculations
reproduced the precision examples and design effect; an independent source
closure check covered all 741 SA rows. Finite-simulation V means agree with
their analytic expectations within about 1.4% in the audited scenarios.
Reporting was corrected to expose both levels of conditioning for CV;
the seeded private numerical results remained unchanged. This is numerical
and methodological verification, not latent-ecology identification.
