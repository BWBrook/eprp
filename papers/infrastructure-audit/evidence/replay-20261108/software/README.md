# Fixed-input software replay, 8 November 2026

Cases 5, 6, 8 and 9 now have fresh implementation runs, with separately coded
mathematical or control routes. These receipts support bounded propositions;
main Codex and Claude still own ledger integration and scientific review.
Nothing was staged or committed by this delegate. Only this directory was
edited. No population-wide defect rate is estimated.

| Case | Fresh observation | Separate check | Boundary |
| --- | --- | --- | --- |
| 5, C096 | admtools 0.7.0 gives 3,972 wrong inverse times among 8,282 deposited times in the specified sparse model. A 0.01-Myr tie-point model gives six wrong times, maximum 0.465914 Myr. | Explicit linear-segment algebra checks the forward mapping, deposition mask and inverse truth. Positive controls later in the section agree exactly. | Errors affect interpolation segments adjacent to repeated heights; the wording “every point above every hiatus” is false. The separate near-hiatus probes give errors up to 2.7 Myr, not the random-sample maximum. StratPal wrappers were not run. |
| 6, C102 | fossilbrush 1.0.6 misses older-than-reference differences 10, 20, 49.9, 100 and 499 at threshold 5, while flagging 5, 5.1, 6, 9, 9.9, 50, 99 and 500. | Numeric subtraction and thresholding disagree with the package; character comparison predicts every flag on the grid. Younger-than-LAD differences additionally include the taxon's 20-Myr reference duration. | A deterministic synthetic grid establishes the mechanism; this does not replay the historical 100 injected occurrences or estimate real-world prevalence. |
| 8, C110/C098 | Rextinct 1.1.0 at commit `508d3c90698b88efcb8c2f1c17a6837a42fd7691` collapses the dating-error interval to a point at zero input dating uncertainty; nonzero dating uncertainty restores a spread. Different caller seeds give identical subsequent uniforms. | Closed-form weighted-prefix estimates reproduce every one of 100 saved resamples for each estimator variant. An explicit final-iteration RNG state predicts all five subsequent uniforms exactly; without the call the caller seeds differ. | This is evidence about conditional resampling semantics and RNG state, not a new population-coverage experiment or a claim that the method is generally invalid. The original benchmark's “ideal dating” used sigma 0.001 Myr, not zero. |
| 9, C125/C123 | pyGPlates 1.0.0 reconstructs all 7,200 fixed point-age-model rows from raw ZIPs, exactly reproducing retained coordinates and missingness. Three-model median latitude spread is 2.885, 5.654, 4.317, 5.495, 4.730 and 13.554 degrees at 10, 50, 100, 200, 300 and 400 Ma. | Plain-Python spread aggregation includes both changing and fixed 194-point cohorts. An oriented two-point basis, with no SVD/least-squares fit, maps TorsvikCocks2017 routes by rotations 3.13, 9.58, 2.51, 22, 7 and 28 degrees; maximum residual 0.000117 degrees. All-pair dot products remain nearly invariant. Synthetic rigid and distorted controls discriminate; MERDITH2021 is near identity. | Raw local reconstructions were rerun; the comparison route is the retained web-service response, not a new API request. This establishes a near-rigid discrepancy at sampled points and ages, not the correctness of either frame or globally identical relative motions. Structural model-choice spread is not calibrated error. |

`case05_admtools.json`, `case06_fossilbrush.json`, `case08_griwm.json` and
`case09_plate_models.json` contain observations and limits. The independent
frame construction uses only two well-separated point vectors to determine
the rotation, then checks all remaining vectors and every pairwise inner
product; it does not optimise the old SVD objective. Its residuals need not
equal the historical least-squares residuals. The distorted synthetic control
has a 10-degree maximum residual, versus approximately 4e-15 degrees for a
known rigid rotation.

For GRIWM, sorted dates `a[1] < ... < a[j]` in years BP yield prefix estimates
`a[1] + (a[j]-a[1]+1)*log(alpha)/j` for the biased variant and
`a[1] - (a[j]-a[1]+1)/j` for the unbiased variant. The separate implementation
uses weights `1/(a[j]-a[1])` and rounds the weighted average. This algebraic
implementation matches the package's saved dating-error resamples exactly;
it does not independently establish the estimator's sampling assumptions.

## Reproduction and provenance

Use a machine with Docker, the two retained content-addressed images recorded
in `provenance.json`, and the mirrored plate-model ZIPs. Create an output
directory first, then run from the repository root:

```bash
bash papers/infrastructure-audit/evidence/replay-20261108/software/run.sh \
  "$PWD" "$RAW_MODEL_DIR" "$OUTPUT_DIR"
```

The unchanged `run.sh` wrapper was subsequently executed end to end and
exited successfully in a fresh output directory on the same data host.
Its minimal staged source tree held shallow Git metadata for the exact
workspace revision; all 15 source/input hashes matched the workspace before
transfer and again on the execution host. All five scientific/environment
JSON outputs equal the earlier direct-run receipts. `provenance.json`
records the command, successful exit and complete staged-input hashes.
The wrapper pins image content IDs rather than mutable tags,
mounts the repository and raw models read-only, and writes results only to
the requested output directory. Paths to hosts and the private data store
are deliberately omitted; ZIP basenames and hashes identify the inputs.
The remote scratch directory was new; retained source resources were read-only.

The package environment is R 4.6.1, admtools 0.7.0, fossilbrush 1.0.6 and
Rextinct 1.1.0. Python is 3.12.15 with pyGPlates 1.0.0 and NumPy 2.5.4.
`package_environment.json` records locale, RNG kinds and hashes of deparsed
package functions. CRAN installations do not retain an upstream Git SHA;
the exact image ID plus package version and function hash identify tested
implementations. The source revision and script hashes are in
`provenance.json`; replay scripts were new/uncommitted at execution. The R
input hash is SHA-256 of a `jsonlite::toJSON(auto_unbox=TRUE, digits=15)`
representation followed by a newline; the exact synthetic construction is in
the hashed R script. Plate inputs include ZIP, point table and retained
response hashes. No third-party full text or private collection identifiers
are copied into these receipts.

The runner stops on a failed assertion. The existing large simulations,
coverage rates and live-service behaviour were not re-evaluated. These are
implementation replay and mathematical/control checks of the named versions
and frozen inputs, not independent empirical validation of the models.

## Independent review of case 11

`review_case11.py` executes both the References direct exact sum and main
Codex's complement recurrence/R check, then uses a third calculation:
47-fold integer polynomial convolution of `(9 + 11*x)`, summing coefficients
from degree 28 upward and dividing by `20^47`. All three exact routes have
identical reduced rational numerators and denominators, giving
**0.31586402602507185**. R 4.6.2 gives **0.3158640260250713**, a difference of
about 5.55e-16 from the exact-decimal result. This rounding difference has no
scientific consequence. The reviewer receipt is `case11_reviewer.json`.

```bash
python3 papers/infrastructure-audit/evidence/replay-20261108/software/review_case11.py \
  "$PWD" "$OUTPUT_DIR"
```

This review checks the stated binomial calculation, including `P(X >= 28)`;
it does not re-review the source PDF, select a geological null or assess the
paper's separate spectral evidence.
