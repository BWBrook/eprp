# Cases 7 and 12: retained posterior calibration and archived scoring

8 November 2026. Bounded Codex delegate, GPT-6.1 Sol. New files only in this
directory; no catalogue/source edits, fits, new simulation campaign or contacts.

The numerical claims below reproduce. Their scope is narrower than the case
selection's broad titles. Case 7 combines posterior-log reaggregation,
per-case estimator-output checks and analytic moment checks. Case 12 includes
three **fresh forward implementation calls** plus a separate saved-vector
score calculation. The source ZIP and the complete 150 retained PyRate logs,
truth records and generated inputs were available. No source-access blocker
was encountered. Large source payloads remain in their source stores.

## Case 7

[pyrate_raw_check.py](pyrate_raw_check.py) parses all 150 original posterior logs
with CSV, recomputes equal-tailed quantiles by explicitly sorting and linearly
interpolating, and calculates Geyer initial-positive-pair ESS from **direct
lag products**, separately from the original NumPy quantile/FFT summarizer.
It checks all 1,001 logged generations per run (0 to 2,000,000 by 2,000), drops
the first 200, and retains 801. Every original stdout identifies PyRate
v3.1.3 (20260823) and the compiled FastPyRateC module. All recomputed interval
endpoints, medians and ESS match the six-significant-digit retained TSV;
all 450 coverage decisions match. [Raw receipt](pyrate_raw.json),
[full derived replicate summaries](pyrate_raw_per_replicate.json).

| Arm | Quantity | Covered | Wilson 95% coverage interval | Median relative bias |
| --- | --- | ---: | --- | ---: |
| psi 1.0 | lambda | 95/100 | 0.8882–0.9785 | -0.112818 |
| psi 1.0 | mu | 95/100 | 0.8882–0.9785 | -0.116635 |
| psi 1.0 | q | 81/100 | 0.7222–0.8749 | +0.089504 |
| psi 0.25 | lambda | 44/50 | 0.7620–0.9438 | +0.062140 |
| psi 0.25 | mu | 40/50 | 0.6696–0.8876 | -0.029236 |
| psi 0.25 | q | 33/50 | 0.5215–0.7756 | +0.457883 |

Fresh posterior-width calculations distinguish undercoverage from a width
defect. For q, **mean posterior SD divided by truth** is 0.084974 (high) and
0.307244 (low), versus **across-replicate SD of posterior medians divided by
truth** of 0.077881 and 0.290381. Median posterior SD/truth is 0.083488 and
0.281239. Mean posterior SD slightly exceeds the across-record median spread
in both arms. The intervals are shifted high; these results do **not** support
calling them "too narrow". Median bias divided by each run's posterior SD is
+1.119 (high) and +1.483 (low). These width/spread comparisons are descriptive
across the retained simulation design; they do not identify the cause of the
shift or prove calibration of widths independently of interval location.

Every q miss has truth below the lower endpoint (19 and 17). Minimum ESS over
all parameters/runs is 299.970291. The high-preservation E2 criterion fails
on q; the low arm had no declared pass criterion. Coverage Monte Carlo SEs
and exact hashes of the logs, inputs and truth records are in the receipt.
These are sampling-error summaries across independently seeded simulated
records, conditional on the implemented design. ESS is a single-chain mixing
summary, not a convergence proof or guarantee of posterior correctness.

[classical_reaggregate.py](classical_reaggregate.py) uses scalar arithmetic on
the three retained per-case estimator tables. In ideal arm A, Strauss–Sadler
covers 1,895/2,000 (tbea) and 1,899/2,000 (EDE); Robson–Whitlock covers
1,909/2,000. Rebuilding the continuous Strauss–Sadler upper bound from each
row's fossil count, range and last occurrence agrees to at most 1.14e-13 Myr.
This is an independent analytic mechanism check beyond copying coverage
counts; it does not rerun the packages from individual fossil ages.
[Receipt](classical_reaggregate.json).

The nominal 99% binomial band is independently computed from binomial
probabilities as [0.937, 0.962]. Both Strauss–Sadler coverage subcriteria pass,
but their bounds agree within 0.02 Myr for only **91.0%**, below the declared
99%. **Overall E4 fails.** Discretising the tbea input yields 97.35% agreement
within 1e-6, still short of complete agreement.

Arm B drops 728/2,000 cases. Its retained Strauss–Sadler coverage is
1,125/1,272 (0.884434), versus the same species' ideal-arm baseline recorded
in the receipt. E5's executed hiatuses are **2–4, 6–8, 11–13, 16–18, 21–23
and 25–27 Myr forward time**; the declaration instead lists 3–5, 7–9,
12–14, 17–19, 22–24 and 26–28. Results belong to the executed design;
"as declared" is not justified. The 2,000 species come from only **two
simulated clades** (seeds 50001/50002). Casewise Wilson intervals and Monte
Carlo SEs are descriptive calculations under independent-case assumptions,
not independently replicated clade-level uncertainty or general calibration
certificates. The positive control is limited to observed near-nominal
coverage under this homogeneous-sampling design.

For C105, [generator_reaggregate.py](generator_reaggregate.py) separately
checks G1 birth–death mean/survival and G2 Poisson-sampling moments from the
retained 20,000-row tables against analytic expectations. Both generator arms
pass these stated moment checks; the paleobuddy and FossilSim dispersions
are 0.9942762 and 0.9903592. [Receipt](generator_reaggregate.json). **No fresh
generator run** was made; G3, G3b, G4's KS p values and G5's taxonomy
checks are not newly verified by this tranche. C105 as a whole remains
broader than the verified subset.

The original PyRate fits used commit
`6a27efb78c487a9d284d727558b7bd26ff674592`, `-A 0 -mHPP`, default priors,
2,000,000 generations, interval 2,000 and seed equal to replicate suffix.
The immutable existing image ID, its current inspected package versions,
original metadata and source-script revisions/hashes are in
[provenance.json](provenance.json). This task reaggregates those retained fits;
it does not reproduce the simulator or re-estimate the posterior. It does
not newly verify the duration-based causal attribution, other PyRate models,
or downstream preservation-corrected diversity results.

## Case 12

The checksum-verified INDITEK-2.0 archive from Zenodo record 22079167 was
extracted into separate scratch storage. Its existing locked environment was
reconstructed offline; the original benchmark
[t5_inditek_forward_replay.py](../../../../../resources/software/bench/validate/t5_inditek_forward_replay.py)
was run unchanged at the same three preselected proposal states.
[Fresh forward receipt](inditek_forward.json) records all input/model hashes,
versions, parameters, acceptance flags, masks and numerical errors.

| Chain (zero based), iteration | Saved RSS | Fresh RSS | Saved minus fresh |
| --- | ---: | ---: | ---: |
| 0, 50 | 3347.632514158171 | 3305.272872634216 | 42.359641523955 |
| 0, 500 | 2860.316351960297 | 2842.847905656028 | 17.468446304269 |
| 5, 5000 | 2732.960823664541 | 2721.024013909283 | 11.936809755258 |

Every vector contains 2,978 predictions. Maximum saved-versus-fresh prediction
error is below 5e-14; all finite-cell masks agree. All three combined F2
prediction-and-score gates fail; independent F3 scoring gates pass.

A second route, [inditek_saved_score.py](inditek_saved_score.py), opens the
NPZ members **directly from the ZIP**, imports no model/scorer, and sums
squared scalar residuals divided by four with `math.fsum`. It reproduces the
fresh RSS values to the displayed precision.
[Independent score receipt](inditek_saved_score.json). Every chosen state
has acceptance flag zero and differs from the next accepted parameter state.
They are **rejected proposals**, not accepted posterior draws. Three calls
are not three proposal variants or three independent calibration datasets.

The supported finding is a saved-score/deposited-observation-and-scorer
inconsistency for these three proposals, alongside successful forward-vector
replay. Different observations, scoring implementations or generating source
versions remain unresolved alternatives. This check does not identify the
cause, establish that these outputs generated the article's figures, or
refute the article's conclusions. Previously reported chain diagnostics were
not recomputed here. "The archived calibration does not replay" needs this
qualification; "the model is unreproducible" or "the code is wrong" is not
licensed.

This delegate is a different actor and wrote separate aggregation/scoring
code, but uses the **same Codex model family** as the original main review.
The fresh forward call deliberately reuses the original replay script; that
call alone is not a separate-route check. The direct ZIP score calculation
and analytic range-bound calculation supply separate computational routes,
not independent empirical data or cross-model scientific validation.

## Reproduce

Run from the repository root. `E2_RAW`, `INDITEK_ZIP`, `INDITEK_ROOT` and
`INDITEK_PYTHON` identify the retained source root, pinned ZIP, extracted
archive root and the environment built from
`resources/software/inditek-2/env/{pyproject.toml,uv.lock}`. Reconstruct that
environment in separate scratch storage with `uv sync --frozen --offline`.
No network request or fit is needed. `SRC` identifies these scripts; set `OUT`
to this directory or a fresh scratch comparison directory.
`OPENBLAS_NUM_THREADS=1` was used for model/scoring calls.

```bash
SRC=papers/infrastructure-audit/evidence/replay-20261108/calibration
mkdir -p "$OUT"
python3 "$SRC/pyrate_raw_check.py" "$E2_RAW" "$OUT/pyrate_raw.json"
python3 "$SRC/classical_reaggregate.py" resources/software/bench/results/t2 "$OUT/classical_reaggregate.json"
python3 "$SRC/generator_reaggregate.py" resources/software/bench/results/generators "$OUT/generator_reaggregate.json"
OPENBLAS_NUM_THREADS=1 "$INDITEK_PYTHON" resources/software/bench/validate/t5_inditek_forward_replay.py "$INDITEK_ROOT" > "$OUT/inditek_forward.json"
OPENBLAS_NUM_THREADS=1 "$INDITEK_PYTHON" "$SRC/inditek_saved_score.py" "$INDITEK_ZIP" "$OUT/inditek_saved_score.json"
```

The forward receipt includes elapsed wall times; those fields need not match.
Raw-derived and scalar numerical receipts otherwise have deterministic
content for fixed versions and inputs. [Suggested narrow claims](suggested-claims.md)
are for main's integration and review, not ledger edits by this delegate.
