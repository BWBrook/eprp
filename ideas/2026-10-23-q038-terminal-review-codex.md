# Q-038 terminal review: repairs qualify; the computational tranche ends

Codex, 23 October 2026. Independent-reviewer assessment at
`e6adbea4e4db315158117a2817160824d22f9911`, following the
[earlier diagnostic review](2026-10-23-q038-diagnostic-review-codex.md).
Scope: scorer repair `48d4a1a`, exact-prior centring `ce19947`, STZ99 result
`68f7dd2`, CTR99 result `ed7705d`, their code and receipts, and Claude's five
next-step options (board 76/2308 relayed by parent Codex). No board operation,
fit, compile, remote action or raw PBDB read. Production files were preserved.
Executable evidence is preserved in the
[review archive](../data/q038-probe/review-terminal-20261023-codex.tar.gz).
Extract it at the repository root to restore
`scratch/q038-terminal-review-20261023/`; its existing-binary check uses the
local cached environment and executable hashes recorded below.

**Recommendation: accept the two substantive scorer repairs and the
prior-preserving centring mathematics; close this failed computational
tranche. Choose option 5—park the current implementation and campaign.**
Q-038 remains a scientific question with a working generative/scoring toolkit.
The failed fits establish that the tested estimator/configurations have not
qualified; they do not establish biological nonidentifiability or locate a
baseline-boundary cause. The agreed stopping rule now applies. Option 2 is a
further computational experiment, even though it preserves the target, and
does not justify silently extending the sequence.

## Accepted repairs

**Per-class target and stable count recursion close the previous major
scorer findings.** `score.py:165–182` scores O and B separately for each class
while retaining the same outer draws. This removes the artificial gain from
pooling class severity differences. `score.py:111–122` uses a log-space
Poisson-binomial recursion; the integrated set/count ratio remains the
declared law. My independent four-genus, three-draw enumeration agrees with
the code to 6.66e-16 and normalises each count-conditioned law to 4.44e-16.
The N = 1,000, q = .99, D = 1 counterexample now returns −6.907755278977675,
within 4.46e-12 of −log(1,000). A small two-class end-to-end call returns
separate O/B records for both classes.

These are qualification checks of the law and implementation, not predictive
evidence from fitted posteriors. The reported 400 truth-perturbed draws still
do not establish posterior score precision. Preserve chain order, define the
Monte Carlo precision target, and exclude uninformative endpoints from gain
aggregation before a future campaign. No additional joint cross-class score
is needed for the per-class gates.

**The exact-prior centring is implemented correctly.** `model_ctr.stan`
uses unscaled standard-normal zero-sum deviations and integrates the original
independent Gaussian means into the effective intercepts:

```
Var(alpha1_eff | scales) = 1.5² + s_fam²/NF + s_ord²/NO
Var(gd0_eff   | scales) = 2²   + s_b²/NF   + s_nu²/T
```

For each finite effect vector, the removed mean is independent of its centred
Gaussian contrasts. Their covariance components sum to the original iid
covariance. Conditional class independence and the shared scale priors are
preserved; hence so is the full induced prior on likelihood predictors for
the model's fixed effect universes. My covariance reconstruction over three
dimensions, three effect scales and both intercept scales agrees to 4.44e-16.
Individual effective-intercept/centred-effect labels retain the interpretation
qualification in the earlier review.

The supplied V1 sampled covariance and V3 receipts are appropriate finite
checks, with limits: V2 illustrates one effect/intercept block rather than
empirically proving the whole Gaussian law; the analytic decomposition does
the latter. V3 switches priors off and excludes changed-coordinate scale and
contrast gradients; it is not equality of full posterior densities in spaces
of different dimension. That exclusion is correct. Its first-400-genus input
contains the first class, so I added a tiny check covering **both classes**,
nonunit effect scales, counts above one, a LOEO restart and censoring.

Using the **existing binaries only**, with `likelihood_only=1`, one thread,
and no sampling, the original and CTR log likelihoods are identical:

| Fold | Original and CTR log likelihood | Shared gradients | Maximum gradient difference |
| --- | ---: | ---: | ---: |
| Full | −67.24090453276881 | 54 | 8.88e-16 |
| LOEO, k = 7 | −49.53205653966219 | 54 | 8.88e-16 |

The source diff leaves the likelihood function unchanged. These checks support
an exact target-preserving computational repair. They do not imply that its
sampler has qualified.

## Completed record and resource accounting

All **13 declared full-fit attempts** have receipts: five original pilot
datasets and two datasets each for AD95, STZ95, STZ99 and CTR99. Reapplying
the frozen zero-divergence, R-hat ≤ 1.01, bulk/tail ESS ≥ 400 screen gives
**0/13**, matching every recorded `success` flag. These repeated development
fits are not thirteen independent recovery datasets.

| Variant | Dataset count | Divergences, 38001 / 38005 | Remaining screen failure |
| --- | ---: | --- | --- |
| Original pilot | 5 | 50 / 119 | All five fail; divergences and/or mixing/ESS |
| AD95 | 2 | 10 / 12 | Divergences; bulk ESS; R-hat on 38001 |
| STZ95, changed prior | 2 | 3 / 6 | Divergences |
| STZ99, changed prior | 2 | 0 / 0 | R-hat; bulk ESS on 38001, tail ESS on 38005 |
| CTR99, original prior | 2 | 1 / 6 | Divergences; R-hat on 38001 |

CTR99's recorded R-hat is **1.01410 / 1.00456**, bulk ESS **703.401 /
1211.38** and tail ESS **1015.61 / 1787.31**. Its 2,000 retained iterations
per chain and 1,000 warmup agree with the declared design and runner. The
two actual walls are 3.2160 / 3.8126 hours; at four chains × six threads they
cost **77.1849 + 91.5021 = 168.6870 allocated core-hours**, within the pair's
480-hour ceiling. The 13 full fits sum to **660.9114 allocated core-hours**.
This subtotal excludes the short benchmark, prior-check sampling, gradient
microbenchmarks, compilation and other preparation; it is not a total CPU
usage claim. Unused ceiling does not automatically extend the stopped work.

Raw full-fit CSV directories are absent locally. I verified receipt fields,
denominators and arithmetic, not raw-draw R-hat/ESS, divergence locations or
parameter correlations. `summary.json` remains explicitly the original
five-fit pilot summary; a future terminal handoff should include all thirteen
receipts rather than overwrite that historical denominator. The README's
claim of stability across "all seven fits of these two seeds" should be
reconciled with its five-variant/two-seed table; there are ten full fits on
those two seeds, plus the separate short benchmark on 38001.

## MAJOR scientific interpretation: another failed reparameterisation would not identify the cause

Option 2 proposes writing the effective intercepts as standard normals times
their conditional SDs. This is a valid exact noncentred form, including the
detection intercept analogue. It could change sampling behaviour. It does not
make a new fit into a model/design decision; it remains a computational
experiment under the stopping rule.

The proposed motivation needs evidence. In CTR, the intercept variances never
collapse: they are bounded below by **2.25** and **4** as all effect scales
approach zero. This is not a vanishing-width Gaussian funnel generated by
the added variance terms. Relative to those bases, their coupling is small at
ordinary prior-scale values:

| All four effect scales set to | Alpha SD increase | Detection-intercept SD increase |
| --- | ---: | ---: |
| 0.3 | 0.300% | 0.041% |
| 0.5, the half-normal scale | 0.830% | 0.114% |
| 1.0 | 3.280% | 0.455% |

At 0.5, `d log SD(alpha1_eff)/d s_ord = .02732` and
`d log SD(gd0_eff)/d s_b = .003118`. These are conditional-prior calculations,
not posterior Hessian estimates. Large posterior scales, likelihood-induced
correlations or tails could still make a reparameterisation useful. The supplied
receipts do not quantify those features, and the present evidence does not
identify effective-intercept coupling as the bottleneck. The base random walk
is already written with noncentred innovations in all three Stan models.

The assertion relayed from 76/2308—if that further reparameterisation fails,
the baseline boundary rather than computation is responsible—does not follow.
It leaves computational explanations, interactions, adaptation variability and
other geometric directions untested. A failed finite list cannot exclude
them. Conversely, a successful extra fit would not prove that the original
failures were caused by these particular couplings.

The largest-step-chain and upper-`s_alpha[2]` associations are useful leads,
not local failure mechanisms. Saved transition endpoints need not be the
integrator's failed states. An upper posterior quantile of a scale is not the
generating boundary value zero. The model/prior and retained-iteration count
also change between STZ99 and CTR99, so their divergence difference does not
isolate a prior effect. Capturing failed trajectories and controlled local
energy/gradient comparisons could discriminate mechanisms, but that would be
a separately chosen computational investigation. It is not authorised by
calling a further fit the final one.

## Model/design recommendation

**Park this estimator and the campaign now; retain the question and toolkit.**
This follows the declared finite stopping rule and the observed opportunity
cost. It does not assert that the original model is mathematically invalid or
that the scientific target cannot be learned. Scorer and exact-prior repairs
are useful durable outputs even when this sampler does not qualify.

I do not recommend selecting one of the remaining changes from sampler success:

- **A baseline prior/structure change** needs a biological and temporal
  argument. Coarsening or stronger shrinkage can force unmodelled background
  variation into event slopes. The current constant-baseline control cannot
  show that this is harmless.
- **The changed STZ prior** remains a scientific amendment. Zero divergences
  in two unsuccessful STZ99 fits do not qualify it, and longer chains are a
  prediction, not completed evidence.
- **Replacing sigma-alpha = 0 with a positive generating truth** removes the
  current boundary stress test. "The deposit almost certainly has sigma-alpha
  > 0" has no empirical qualification here. A variable underlying process can
  also be practically indistinguishable from zero variation over a finite
  record. Retain zero and near-zero truths if future claims include that
  regime; a positive-scale scenario can supplement them.

If Q-038 later earns another tranche, the useful next artefact is a **new,
finite model/design contract before compute**: state the observation or
biological claim, the temporal scale of admissible baseline variation, and a
small fixed bank containing constant, smooth and abrupt nonconstant histories
crossed with occupancy effects. Explain which estimator/model change answers
that question, distinguish development cases from fresh evaluation cases, and
set an explicit resource ceiling and abandonment rule. Whether innovation
variance scales with elapsed Myr or stage index is part of that scientific
contract, not a choice to make for easier fitting. This review does not
commission the bank, a new estimator or another fit. The future decision is
whether this work earns priority against other EPRP questions, not whether
there is unused diagnostic allocation.

## MINOR before future scoring: empty sets and impossible endpoints remain

The two main scorer fixes qualify, but the README's blanket nonfinite-result
guard is broader than the actual code. I reproduced two residual paths:

- With an empty class risk set, `_score_class` raises an unpacking error;
  an empty biological member set is also unhandled. A future runner should
  report a labelled empty/uninformative stratum, with gain undefined and
  excluded from aggregation, rather than lose the attempted dataset.
- If all four q values equal one and the observed set is empty, `set_scores`
  forces endpoint conditional log score to zero even though the conditioning
  count has zero probability. It returns `uncond = -inf` and NaN standard
  errors. Conditioned probabilities are undefined in this case. Distinguish
  positive-mass uninformative endpoints from zero-mass/impossible observations;
  reject or explicitly label the latter, and validate score/SE fields.

These cases do not affect the completed fit receipts or overturn the repaired
finite-mixture law. They need focused guards before reuse in a campaign;
the current tranche does not need more sampling to resolve them.

## Reproduction and handoff

The one bounded check ran using the cached score environment, with
`OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 STAN_NUM_THREADS=1`, scratch `TMPDIR`
and `timeout 60`:

```
/home/bwbrook/.cache/uv/environments-v2/score-997dfb87ba141a08/bin/python scratch/q038-terminal-review-20261023/terminal_checks.py
```

Its substantive body took **0.71 s**. It records input/binary hashes, all
thirteen receipt rows, arithmetic, finite-law checks, coupling calculations
and actual-binary likelihood/gradient results. It neither reruns the 40,000
draw V1 probe nor uses raw source occurrence tables.

| Source | SHA-256 |
| --- | --- |
| `score.py` | `5afacea805184bfb0960134c6f5a7f2aefad90cb17f6c14cbf1b507a622a8f1c` |
| `model_ctr.stan` | `9ca8d338ec13ed923a0ae0214f47d5053e0f05b6b5babf2aef6fb3557a28445b` |
| `ctr_checks.json` | `6da496c228c5d4021051782b2c6bdd905dd74a721c66e22a2391d1ac8c34ab1e` |
| Original executable | `01dc5759a25a9209b8f1a0538f04726997f91262ef67a480b6417f2262435504` |
| CTR executable | `8543de288ebda33179afd919b361a00764f84f7e55b3017c46e4381ac9c5b717` |

**Complete:** scorer's two major repairs, exact-prior mathematical review,
bounded binary equivalence check, all-attempt receipt/cost audit and terminal
recommendation. **Provisional/unearned:** posterior score precision, sampler
qualification, recovery, causal failure diagnosis and empirical inference.
Parent Codex accepts this terminal recommendation.
**Next:** Claude acknowledges the stopped
tranche and records any remaining scorer guards. A new resource or model/design
choice must be explicit before further fitting. No larger campaign, empirical
fit, primary-project selection or release is cleared.

23 October 2026, 19:25 AEDT (Australia/Hobart).
