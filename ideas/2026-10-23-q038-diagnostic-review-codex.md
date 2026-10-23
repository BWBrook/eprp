# Q-038 diagnostic review: restart closed, scoring repairs and prior choice remain

Codex, 23 October 2026. Independent review at
`2087e13db3ece215af27d4466a223472c8bf8466`, using the independent-reviewer
workflow. Scope: the `de8c84c` restart repair; five-fit pilot and four completed
diagnostics; `core.py`, `run.py`, `score.py`, `checks.py`, constants derivation,
`model_stz.stan`, README and draft redesign. The prior
[implementation review](2026-10-22-q038-implementation-review-codex.md) and
[cost review](2026-10-22-q038-campaign-cost-and-triton-codex.md) supply the
acceptance criteria. A GPT-6.1 Sol subagent performed the bounded review;
parent Codex integrated it and independently checked the pooled-score arithmetic.
Evidence and executable checks are in
[the review archive](../data/q038-probe/review-diagnostics-20261023-codex.tar.gz),
restoring `scratch/q038-diagnostic-review-20261023/` from the repository root.
Archive SHA-256:
`5e93aa9b233072c58a1033509e1f80099826905e9ce9bf6174829b189826a8f1`.
No production source edit, fit,
compilation, remote action, repeated C5 simulation, commit or board write.

**Recommendation: close the LOEO restart defect and retain every pilot and
diagnostic as development evidence. Keep the campaign held.** The pilot has
five completed attempts and zero screen passes. Neither completed diagnostic
variant passes. The sum-to-zero candidate is a changed prior, whose benefit
cannot yet be attributed solely to reparameterisation. Before scoring a
campaign, repair class pooling and numerical underflow. Neither defect affects
the existing full-history fits.

## Verified closures and result boundaries

- **C6 closes the restart defect.** The independent alive/dead recursion gives
  the repaired counterexample suffix exactly: −8.98842587327675. On saved seed
  38001, all **138** LOEO restarts retain full-history feature and detection
  rows exactly; suffix minus full-minus-prefix likelihood differs by at most
  1.42e-14. This is an additional dataset check; the supplied C6's **169**
  restarts are from its different seed/design realisation. A restart conditions
  on capture without erasing the observed feature history.
- **The original pilot remains interpretable as a runtime/convergence
  experiment.** All five datasets regenerate with exactly equal count and
  metadata arrays. All thirty full/forward Stan data dictionaries equal those
  produced by pre-repair `217fa2a`. This compares array contents, rather than
  claiming newly compressed NPZ containers must have identical bytes. All ten
  archived NPZ/truth-file SHA-256 values verify.
- **The constants derivation now replays.** Executing the archived derivation
  with its output redirected to scratch reproduces the constants file byte
  for byte, including 19,426 transitions and class first-record totals
  1,838/1,306. Its raw CSV and stage hashes match the recorded sources. This
  closes missing derivation provenance; full-deposit scales still do not meet
  an empirical prefix-only contract merely because they replay.
- **All five failed screens are correctly retained.** Recomputing the Boolean
  screen and allocation arithmetic from the five JSON receipts gives zero
  successes and allocated core-hours 38.2655, 37.2492, 36.4529, 38.2833 and
  36.9849. The summary matches exactly. These are receipt-level checks:
  raw CmdStan chain files are not in this checkout, so R-hat, ESS,
  divergences, step sizes and correlations were not independently recomputed
  from draws. There is no recovery or reliable posterior-precision result.

The completed diagnostic receipts reproduce:

| Variant | Divergences, 38001 / 38005 | Max R-hat | Min bulk ESS | Min tail ESS |
| --- | --- | --- | --- | --- |
| ad95 | 10 / 12 | 1.01846 / 1.00893 | 341.488 / 345.011 | 475.139 / 616.618 |
| stz95 | 3 / 6 | 1.00708 / 1.00710 | 514.748 / 508.288 | 1044.18 / 858.547 |

STZ95 passes the stated mixing/ESS bounds and fails the divergence rule on
both datasets. Similar occupancy-slope summaries across unsuccessful fits
are reassuring descriptive evidence, not proof of posterior invariance or
of a scientifically innocuous prior change. Associations with saved divergent
states do not locate integrator failure. The already-declared STZ99 pair was
still pending in the supplied record; this review does not infer its result.

## MAJOR — pooled class scoring breaks the class-specific null

`score.py:162–173` pools both classes' risk sets and true members into a
single O/B set score. The contract's section 8 gates are **per class**; S0 is
uniform within class, with different class event severities. A pooled uniform
reference rewards that severity difference even when biological selectivity
is exactly zero within both classes.

An exact four-member counterexample has two members in each class, event-loss
probabilities `(0.2, 0.2, 0.8, 0.8)` and total loss D = 2. Enumerating the six
sets gives expected pooled conditional gain **0.248857705 nats per genus**.
The expected within-class conditional gains are zero. Thus a positive pooled
B gain can exceed the ±0.02 S0 tolerance without any within-class selectivity.
The existing nine-genus normalisation check passes because it tests a
mathematically valid pooled law, not the correct scientific comparison.

**Minimal repair:** return O/B scores separately for each class, retaining a
single shared outer draw for event effects. Any optional cross-class joint
score needs an explicitly different target and baseline. If jointly conditioning
on the two class counts, integrate the **product of the two class set laws**
and the **product of their count laws**, then take their ratio; summing
separately integrated scores generally differs because shared effects couple
classes. Add the two-class uniform-null counterexample and endpoint checks.
Preserve uninformative endpoint labels when aggregating gains. The current
`informative` flag is useful, but no campaign consumer yet enforces exclusion.

## MAJOR before campaign scoring — the count DP can return impossible log scores

`score.py:111–121` runs its Poisson-binomial recursion in probability space
and takes the logarithm afterwards. This underflows for valid low-probability
counts. For N = 1,000, all q = 0.99 and D = 1, the current `set_scores` returns
**+infinity** as the conditional log probability; the exact answer is
**−log(1,000) = −6.907755279**. Its Monte Carlo SE is also unusable. This does
not require q = 0 or 1, and all draws can be identical.

The ordinary small-set law is correct: my separate three-genus enumeration
normalises to within 2.22e-16. The defect is numerical dynamic range, not
conditioning-before-integration. Use a log-space or rigorously rescaled count
DP and preserve log normalisation. Reject nonfinite outputs and conditional
log probabilities materially above zero. Test rare counts as well as small
central ones; endpoints D = 0/N should return exactly zero conditional log
score when the conditioning event has positive probability. This repair is
needed before using score precision as a decision gate; no existing fit is
invalidated.

## MAJOR for model adoption — STZ changes contrasts as well as means

The README openly labels the prior change; that is appropriate. Its additional
claim that the parameterisation moves mixing rather than the estimand needs
the distinction below. Let one class's original random effects be
`u ~ N(0, s² I_N)`. Write `P = I_N − 11'/N`. Then:

- Original centred contrasts have covariance `s² P`, marginal variance
  `s²(1 − 1/N)`, and pairwise-difference variance `2s²`.
- The candidate's marginal-SD-preserving constrained prior has covariance
  `s² N/(N−1) P`, covariance `−s²/(N−1)` between different effects and
  pairwise-difference variance `2s² N/(N−1)`.

Consequently STZ increases contrast variance by **14.29% for eight orders**,
**2.56% for forty families** and **1.16% for 87 stages**, conditional on the
same scales. It also removes the independent random means while leaving
`alpha1 ~ N(logit(.1),1.5²)` and `gd0 ~ N(log(.01),2²)` unchanged. Original
likelihood-intercept variances conditional on scales contain extra
`s_fam²/40 + s_ord²/8` and `s_b²/40 + s_nu²/87`, respectively. Those terms
are absent from STZ. The original S2 generator draws iid effects, so it is
not a generator from the candidate's constrained effect distribution.

**An exact prior-preserving option exists.** Use zero-sum deviations with
unscaled standard-normal density, giving covariance `s²P`; integrate the
independent Gaussian effect means into the effective intercepts. Conditional
on the original hierarchical scales, set

```
alpha1_eff,c ~ N(logit(.1), sqrt(1.5² + s_fam²/40 + s_ord²/8))
gd0_eff,c   ~ N(log(.01), sqrt(2² + s_b²/40 + s_nu²/T))
```

Keep the random-walk innovations, scale priors and all other priors unchanged.
The two classes retain independent effective-intercept draws conditional on
the shared scales. This exactly preserves the induced joint prior on all
likelihood predictors: the means and deviations of an iid Gaussian vector
are independent; adding its removed mean to the intercept preserves its
entire common covariance component. The check reconstructs `P + 11'/N = I`
exactly for N = 8, 40 and 87. Direct centring of an existing truth draw and
moving its means into the intercepts changes the tested suffix likelihood
by only 1.78e-15.

These effective intercepts and centred effects have different interpretations
from the original individual nuisance components. Recovering those components
requires the conditional Gaussian decomposition; occupancy slopes and the
predictive law retain their original target exactly. Retaining explicit
independent Gaussian means instead is another exact representation, but
retains the redundant directions that motivated the change.

**Recommendation:** prefer the exact prior-preserving formulation for a
computational repair. Adopting the current STZ prior is possible as an explicit
scientific model amendment, but stable beta summaries and better mixing on two
selected datasets do not justify claiming equivalence. Freeze either choice
before fresh confirmation datasets; preserve the five original pilot cases
as development data.

## Cost and redesign audit

The 24 saved per-gradient receipts reproduce the timing formula and efficiency
curve. At grain 1, three threads retain **93.31%** and twelve **79.72%** of
single-thread efficiency. At grain 50, twelve threads retain **68.76%**.
Thus the original 178 allocated-core-hour linear extrapolation was a valid
calculation from its short benchmark, but a poor predictor of completed fits;
the blanket assertion that `reduce_sum` scales poorly to twelve threads is
withdrawn correctly. The reported early-warmup explanation is plausible,
but **725 leapfrogs is inferred**, not independently reconstructed here from
warmup draws. One short timing per configuration supports this measured curve,
not a universal throughput law. The under-load 0.047 s/gradient remains an
estimate. A future fit's declared grain should be recorded; `run.py:86` still
uses `stan_data`'s default grain 50 despite the README's grain-1 recommendation.

The draft's **103.2 first-stage / 263.2 maximum full-fit equivalents** give
**3,818.4 / 9,738.4 allocated core-hours** at c = 37, consistent with its
rounded totals. These remain row-work projections from an unconverged model;
do not convert idle-host gradient speed into validated fold or campaign cost.
The separation of recovery, falsification and prediction, the exclusion of
development seeds, attempted-fit denominators and per-claim error spending
are sound. Freeze a terminal bias rule if stopping earlier than 100: assessing
bias at a coverage-dependent random terminal look does not give an ordinary
fixed-sample confidence interval a repeated-look guarantee. Descriptive bias
and its Monte Carlo SE may still be reported as such.

C7's scenario paths implement the stated choices: S0 removes biological
nuisance and clade terms globally at events while retaining background
occupancy/detection heterogeneity; S1 keeps the other biological selectivity;
S3 scales post-event opportunity by the **target**, not realised, survivor
fraction; S4 draws shared reference/stage effects before generating counts.
All five S2 arrays replay unchanged. I inspected the supplied S0/S1
calibration and S3/S4 mean checks without rerunning their 60,000-genus probes.
Those checks do not validate a falsification diagnostic. Because observed
marks feed future hazard covariates, observation perturbations can also alter
realised biological trajectories under the same structural coefficients.
Freeze the baseline and diagnostic statistic, tail direction, calibration
distribution and flag threshold before generating the panel. Genus counts
alone do not retain direct reference-level co-occurrence; a between-stage
count-dispersion diagnostic must be assessed against the fitted stage and
family detection heterogeneity that can absorb part of S4.

**MINOR:** `redesign.md:120–123` contains a literal `EOF` and an appended
Git commit/push command. Remove this drafting residue in the owner's next
edit. It is documentation content and was not executed by this review.

## Bounded next action and stopping rule

1. **Claude reports the already-running STZ99 pair**, including every failed
   attempt, under the unchanged divergence/mixing/precision screen. Its result
   is evidence about the declared changed-prior candidate, not clearance of
   the original model or a campaign.
2. **Choose one model route**, preferably exact prior-preserving centring.
   First validate joint-prior covariance and fixed-point likelihood/gradient
   equivalence. Any implementation and resource allowance must be specified
   before a new fit; this review launches none. Do not cycle through successively
   higher adaptation settings or scale priors until the two chosen cases pass.
3. **Repair and qualify the scorer** with per-class, rare-count and endpoint
   checks; retain posterior chain structure and require a predeclared score
   Monte Carlo precision target. The present delta-method batch formula is
   appropriate for regular, sufficiently long batches, but a reported SE from
   400 truth-perturbed stand-in draws is not posterior precision evidence.
4. If one finite centring evaluation still fails the screen, **stop sampler
   tuning and return a model/design decision or park this implementation**.
   Reducing baseline-walk flexibility or changing its scale prior is a
   scientific model change: the present constant-baseline S2 truth cannot
   establish that it is harmless. The costed campaign stays a draft until a
   qualified model, complete scoring/diagnostic contract and measured resource
   budget are available.

No Barry-only decision is needed to record these findings or fix the scorer.
Claude is the next responder on model choice and the completed diagnostic;
parent Codex accepts the closures and bounded repair recommendations above.
No empirical
fit, larger campaign, primary-project promotion or release is cleared.

## Reproduction receipts

Both commands set `OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1`, use the existing
cached score environment and are bounded by `timeout 60`:

```
/home/bwbrook/.cache/uv/environments-v2/score-997dfb87ba141a08/bin/python scratch/q038-diagnostic-review-20261023/review_checks.py
/home/bwbrook/.cache/uv/environments-v2/score-997dfb87ba141a08/bin/python scratch/q038-diagnostic-review-20261023/replay_structural.py
```

The substantive check bodies took 0.09 s and 18.57 s respectively. Scratch
JSON records source hashes, receipt arithmetic, covariance checks, numerical
counterexamples, all regeneration/fold comparisons and derivation output.

| Pinned source | SHA-256 |
| --- | --- |
| `core.py` | `cc69927cca62cc7eae6941810457ffd3ce32d5a3f6e4a9bdcd9af345f5605b5e` |
| `score.py` | `7ef0ab079948fbe379a159b83627fa0b438599b257d78b8e5c0005c601d1f858` |
| `model.stan` | `df34743f8c0fbb9a548c998caebdefa44944ebf1bd36eb6600346827af2c667f` |
| `model_stz.stan` | `e59d283f00bc91c4e2b98e42b3fc4db3ee8d6c5d551a38258c9e071d6e77af31` |
| `checks.json` | `2aab564f055845f289ad36ab4c4384502229f72ddf1a2405991da42113df0a40` |

Review complete. Candidate convergence, predictive precision and scientific
recovery remain unqualified. Claude responds next.
23 October 2026, 12:24 AEDT (Australia/Hobart).
