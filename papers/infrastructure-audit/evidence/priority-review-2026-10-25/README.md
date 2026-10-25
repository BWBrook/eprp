# Priority receipt audit — 25 October 2026

Independent bounded review by Codex delegate; baseline HEAD `085eaff86a468b632d203ef92083f263a527db5e`.

Existing tracked files were reviewed read-only. The durable audit artifacts are confined to this directory. Reviewed the scaffold, outline, ledger/notes, source README sections, local scripts and committed aggregate/per-case receipts for C001, C031, C069, C076, C077, C040, C043, C045, C096, C102, C107, C110, C111, C119, C123 and C125. No remote compute, provider requests, TDM files, sensitive-location mechanism reconstruction, or release/contact. No existing ledger, scaffold or status file was changed. The untracked Q012 run file was preserved.

Recommendation: continue private paper preparation with corrections and owner replay. This is not gate-2 clearance. Derived-table recalculation checks the summaries of saved outputs; it does not rerun original extraction, reconstruction or estimator fitting.

## Material findings

1. [Detail withheld pending disclosure to the data custodian.]

2. **MAJOR for the declared-test method account: E5's executed design differs from its declaration.** [resources/software/bench/VALIDATION_T2.md:95-97](../../../../resources/software/bench/VALIDATION_T2.md) declares six hiatuses at 3–5, 7–9, 12–14, 17–19, 22–24 and 26–28 Myr in forward time. [resources/software/bench/validate/t2_extinction.R:78](../../../../resources/software/bench/validate/t2_extinction.R) repeats that description, but line 79 implements 2–4, 6–8, 11–13, 16–18, 21–23 and 25–27: all one Myr earlier. No corresponding amendment was found in that declaration. C111's per-case arithmetic remains reproducible for the implemented design, but “as declared” cannot be used without resolving this discrepancy. Preserve the executed results; document the deviation rather than silently changing the declaration. If the declared design matters scientifically, a later authorized owner can rerun it alongside the existing results.

3. **MAJOR for replay status: C045 has no committed differential replay receipt.** The counts 1,454/2,267, 423, 8 and Q007 11–13% are presently documented review observations, not independently replayable from a saved before/after comparison. [data/q012-exposure-support/README.md:130-153](../../../../data/q012-exposure-support/README.md) repeats the Q012 numbers and records further flips (8 E-systematic, 2 used_systematic, 2 used_perbin), demonstrating current project uptake but not an independent data replay. Owner must preserve both build outputs, join keys, thresholds and comparison code. The ledger's “not yet passed to owners” qualifier is stale relative to this current project note.

4. [Detail withheld pending disclosure to the data custodian.]

5. **MINOR precision/denominator repairs:** C096's dense random sample has 6/8,282 errors with maximum **0.465914** Myr; **2.7** Myr is a separate targeted probe, not that sample maximum ([resources/software/bench/results/t2/t2_checks.json:8-12](../../../../resources/software/bench/results/t2/t2_checks.json)). C119's 60.3% agreement and ~3.2° difference describe every 12th eligible collection, 16,599 reconstructed comparisons as given (16,601 after rounding), not every PBDB collection. C125 begins with 300 public collection coordinates but its all-model reconstructable denominator varies 269 to 194 by age. State these denominators.

6. [Detail withheld pending disclosure to the data custodian.]

## Per-claim verdicts and receipts

| Claim | Local check / verdict | Classification and remaining replay |
|---|---|---|
| C076 | **Supported by whole-table aggregate comparisons and bracket scans.** Full-table `pbdb_chronosphere_checks.tsv` records 460, 317 and 17 changes, plus 1 and 10. HTTP head scans detect fewer affected intervals (135,127,13 for the major steps), as expected from head-only sampling; they date steps, not establish whole-table counts. | Observed timescale/version changes; not all changes are bugs. Whole-table counts are for intervals with ≥50 single-interval rows, not all PBDB intervals. Paibian's precise first bracket is 14→15 February 2024, not an event established on 14 February alone. Gate-2 requires safe public-only source snapshot replay under owner guidance. |
| C077 | **Arithmetic verified from committed profile.** 981,357/1,220,213=80.425%; 67,061/1,764,167=3.801%. | Descriptive among matched occurrences that remain public today. Not a complete partition of all substantive data changes, not evidence that historical records were then restricted, and not proof that name/interval reassignment is unimportant to a specific analysis. Original matching requires snapshots; current turn checked aggregate arithmetic only. |
| C040 | **Summary arithmetic verified, data regeneration outstanding.** 2,475+683+953=4,111; adding agreement, both-undated, cannot-date and newly-dateable classes totals 61,863 samples. `age_check.py` transparently uses current-revision tie points, linear interpolation and no extrapolation. | Stored-versus-current-model inconsistency; “stale” is a plausible mechanism supported by history, rather than all recomputed ages proven true. The latest text receipt exists; the claimed 2019 seven-disagreement output is absent from committed profile files and only reported in README. Need read-only NSB SQLite snapshots and owner replay of 2023, 2019, 2022; reconcile duplicate-depth conventions with the original findAge method. |
| C043 | **Counts partition correctly.** 16,256+6,086=22,342 groups; 16,267+12,565=28,832 excess rows; 28,832/541,846=5.321%. Dedup recipe actually removes 16,260, leaving 525,586, and source drop subtotals 2,282+120+13,858=16,260. | Removal of deduplication is a source/code observation; exact cross-source copies are strongly consistent with duplicated observations. Same-source key collisions are not all duplicates. The seven-row difference between 16,267 excess and 16,260 removals is expected because recipe preserves highest-priority same-source rows rather than force one per group; not an arithmetic defect. Need original v1/v4 RData source replay and source-priority comparison. |
| C045 | **Not locally replayed.** Numbers found in source and project README; no committed before/after differential table/code located. | Consequence for EPRP internal builds, not independently validated published inference. Q012 owners already know; eight class flips alone understate the recorded downstream threshold flips. Owner must replay [data/q012-exposure-support/build.R](../../../../data/q012-exposure-support/build.R) and Q007 support build on original and conservative-dedup inputs and save row-joined diffs. |
| C096 | **Mechanism independently reproduced in base R.** Synthetic seeded times plus `stats::approx(...,ties=list('ordered',min))` reproduce 8,282 retained times, 3,972 wrong and max 2.995777 Myr. Dense inverse reproduces 6 wrong/max0.4659139; dedicated probes give1.8,1.0,2.7,1.5 Myr. Recorded start/end/destroy mode outputs are present. | Strong implementation-defect candidate. Local admtools and StratPal are absent, so no package-runtime or `last_occ` call-path replay this turn. Need original pinned admtools0.7.0/StratPal0.7.1 image, small standalone direct-package reproducer and actual source-version pin. Avoid “above every hiatus” as an unqualified global statement: affected segments are between a hiatus and next tie point; segments farther above can be correct. |
| C102 | **Per-row synthetic output arithmetic independently verified.** 24/100 injected flags, 0/20,000 clean flags; 0/50 old versus24/50 young. All flags predicted by textual comparison of recorded nonmissing differences; numeric comparison catches100/100. Derived reference ranges from clean rows support LAD excess being measured from FAD (remaining ~0.005 rounding of differences). | Strong implementation-type/endpoint-defect candidate. 24% is this injection distribution, not real-world error rate. fossilbrush package/source absent locally: need pinned1.0.6 direct-package reproducer including threshold boundary/negative controls, preserving numeric values before text formatting. |
| C107 | **Per-replicate coverage/bias recomputed.** high: q81/100, lambda95/100, mu95/100; q median+8.9505%, all19 misses below lower bound. low: q33/50,+45.7882%, all17 misses below. All saved ESS exceed299.97. Duration JSON gives stated medians and zero-truncated MLEs; raw fitting logs are not local. | Simulation calibration under this model/setup, not generic PyRate correctness failure. Duration association/known-duration counterfactual supports an attribution hypothesis, not a demonstrated causal mechanism for why durations shorten. Need exact compiled likelihood, priors/chain settings, seeds and raw logs to reproduce ESS/posteriors; do not call high-only declared criterion a prespecified low-arm criterion. |
| C110 | **Per-case results recomputed.** GRIWM biased/unbiased interval coverage A .0085/.003; B .001572/.005503; C .6885/.6825. A biased-median bound .6725. Unbiased scaled absolute-error median .116967; median-unbiased SS .123101; RMSE .914376 vs .862334; fraction before truth .624. | Interval semantics/assumption observation, not itself a bug: dating-error resampling spread need not cover extinction-time sampling uncertainty. “Ideal” actually gives GRIWM sigma=.001Myr, while other methods receive exact ages. State the bound arm explicitly. Minor displayed rounding inconsistencies (.005503 normally .006 to3dp). Need pinned Rextinct source/method-text check and runtime replay, preserving corrected armC and invalid original evidence. |
| C111 | **Per-case/paired arithmetic reproduced.** A SS .9475/.9495; Robson .9545. B tbea .884434, 728/2,000 cases dropped (<3 surviving fossils). Classes: elsewhere598,.943144; hiatus445,.829213; after229,.838428. Same-case A baselines .954849,.921348,.938865. Mean fossils7.617925→4.966195. | Expected limitation under nonhomogeneous sampling, not formula defect. Reconcile E5 declared/executed hiatus locations. Coverage subcriteria pass, but overall E4 is false because SS agreement=.91<.99; retain this failed gate in method/results. Nominal binomial tolerance treats cases independently although they come from only two simulated clades; do not describe it as a general coverage guarantee. |
| C119 | **Source/profile consistency only.** Profile gives Matthews comparison10,004/16,599=60.3%, median3.16° unrounded; rounded10,004/16,601=60.3%, median3.19°. Wright and other-model rounding improves medians; not the fraction within .5°. | Model identity from documentation; numerical model-mismatch observation. Whole-Ma rounding explicitly remains inference. Limit rate to every12th eligible sample and Matthews-reconstructable ages. Need model-index snapshot, rotation/polygon hashes and public collection coordinates to regenerate; the local profile alone is no new reconstruction. |
| C123 | **Independent geometry fit from local public coordinate comparison table.** Own numpy SVD fit gives rotations3.1300,9.5800,2.5100,22.0000,7.0000,28.0000° at ages10,50,100,200,300,400; max residual<.000066°. MERDITH control near-zero rotations. | Strong evidence for rigid frame difference for these sampled points/ages; no frame identified as objectively wrong. Do not universalize to every plate/time from six sampled ages. Need both route source files/request receipts and exact versions to rerun original reconstructions; geometry resummarization alone cannot establish which route has which named frame. |
| C125 | **Independent spread calculation from local comparison rows matches.** Medians2.8852,5.6544,4.3169,5.4947,4.7303,13.5543°; n269,260,255,247,217,194. Fixed194-point medians2.7814,5.6925,4.5029,5.4899,4.7110,13.5543. | Structural model-choice spread, not independent error estimates or uncertainty coverage. Coordinates originate from300 public collections and are reconstructed at six common test ages, not necessarily their fossil ages. Geographic sample and missing reconstructions limit generalisation. Need original point selection seed7 and pinned rotations/layers to regenerate. |

## Replay artifacts and next-owner requirements

- [reaggregate.py](reaggregate.py) recalculates T2 coverage/paired effects, PyRate per-replicate coverage/bias, fossilbrush synthetic flags, and C123/C125 geometry. [reaggregate.json](reaggregate.json) records its numerical output. [inputs.json](inputs.json) lists the six source-table SHA256 hashes, sizes, row counts, material descriptions, runtime and output hash. No APIs are called; the script reads only the six synthetic/public tables named inside it. The identifier-bearing PBDB receipt is excluded and was not reopened or hashed during artifact preparation.

  From the repository root:

  ```bash
  uv run --python 3.12 papers/infrastructure-audit/evidence/priority-review-2026-10-25/reaggregate.py
  ```

  The script also works with an absolute script path from another working directory. Its PEP 723 specification pins Python 3.12 and NumPy 2.1.3. `uv` may fetch that dependency once; no system environment is modified. The script writes its own JSON outputs beside itself.

  Counts and ordinary scalar summaries should reproduce exactly on this runtime. Numerical SVD results can vary with BLAS/CPU: compare fitted angles within 0.00001 degrees and residuals within 0.00000001 degrees; use absolute tolerance 0.0000000001 for other floating results. Near-zero MERDITH rotation angles are numerically unstable at about a few millionths of a degree and should be judged against that absolute angular tolerance.

  Final verification used CPython 3.12.3 and NumPy 2.1.3 in the uv environment. Two executions, including one from `/tmp`, reproduced both numerical JSON and manifest byte for byte. All 155 numerical scalars also matched the earlier local mechanical check exactly. The documented tolerances allow for other BLAS/CPU implementations. This verifies reaggregation, not original package fitting or input extraction.
- The base-R standalone check used the declared eight tie points, seed901, 10,000 uniform times, removed open hiatus interiors, then inverted height with `stats::approx(...,ties=list('ordered',min))`; it independently matches the committed sparse/dense results. This is a mechanism replay, not execution of unavailable packages.
- **Databases owner:** NSB mirror paths and command are in [resources/sources/nsb/README.md:302-336](../../../../resources/sources/nsb/README.md); Triton RData paths in [resources/sources/triton/README.md:285-317](../../../../resources/sources/triton/README.md); palaeogeography source routes/command in its README:137-147. Need exact manifests/hash pins before replay. Do not execute current embedded/chronosphere PBDB profilers unchanged: they mix restricted-record handling and live requests. A counts-only, offline-safe replay path must be specified within Barry's hold.
- **Packages owner:** pinned environment receipts are [resources/software/bench/env/Dockerfile.r2](../../../../resources/software/bench/env/Dockerfile.r2), `VALIDATION_T2.md`, `VALIDATION_T3.md` and original run scripts. Reuse existing image on an authorized host later; this task did not start Docker or jobs. PyRate fitting logs are absent locally; `pyrate_summary.py` and `pyrate_durations.py` cannot fully replay from the committed TSV/JSON summaries alone.
- **Main Q007/Q012 owners:** save before/after builds and a standalone comparison so C045 moves from a documented review observation to replayable evidence. Q012 build accepts source arguments (`build.R`) and owns the modelling consequences.
- **Parent:** assess central method/novelty/prior-disclosure claims separately; reconcile evidence status before editing Claude's ledger. No claim here is provider-confirmed or release-cleared.

## Ledger units and AI-method inference

- Recomputed **189 rows**, categories19 data-access,54 provenance-deposit,20 timescale,13 software-correctness,7 software-calibration,14 spatial-model,24 coverage,9 library-metadata,29 process-receipt. Owners143 Databases,30 Packages,14 References,2 joint.
- These are catalogue claims, not189 independent defects, tests, datasets, discoveries, or papers. Some rows combine many propositions; others repeat the same mechanism at different layers or document a positive control. C001/C031/C069 share the PBDB access mechanism. C043/C045 share Triton data; C110/C111 share T2 cases; C123/C125 share V6 points. The29 process receipts include corrections, logistics, reviews and human decisions.
- Separate implementation defects (C096/C102 candidates), data inconsistencies (C040/C043), calibration failures under specified models (C107), violated assumptions/semantic findings (C110/C111), intentional/version/model choices (C076/C077/C119/C123/C125), sensitive access findings and internal downstream effects. A common “silent failure” denominator is indefensible.
- Recorded agent errors and later corrections establish that this workflow found and repaired particular problems. They do not establish that second-model review is necessary or sufficient, that agents generally improve science over human auditing, or that AI lowers cost. Those claims need counterfactual/baseline evidence and inclusion of searches that found no issue, corrections, human time and compute. Source agreement alone is not an independent replay.

## Standalone interpolation-mechanism check

The initial audit executed this small base-R check. It uses synthetic tie points only and reproduces the recorded admtools interpolation mechanism without loading admtools or StratPal. This demonstrates the numerical mechanism; package call-path clearance remains outstanding.

```r
tp_t <- c(0, 4, 6, 12, 15, 21, 24, 30)
tp_h <- c(0, 8, 8, 14, 14, 26, 32, 38)
set.seed(901)
times <- runif(10000, 0, 30)
kept <- times[!(times > 4 & times < 6 | times > 12 & times < 15)]
height <- approx(tp_t, tp_h, xout = kept)$y
back <- approx(tp_h, tp_t, xout = height, ties = list("ordered", min))$y
c(kept = length(kept), wrong = sum(abs(back - kept) > 1e-9),
  max_error = max(abs(back - kept)))
dt <- seq(0, 30, 0.01)
dh <- approx(tp_t, tp_h, xout = dt)$y
back_dense <- approx(dh, dt, xout = height, ties = list("ordered", min))$y
probe <- c(6.001, 6.005, 15.001, 15.005)
hp <- approx(tp_t, tp_h, xout = probe)$y
c(wrong = sum(abs(back_dense - kept) > 1e-9),
  max_error = max(abs(back_dense - kept)))
abs(approx(dh, dt, xout = hp, ties = list("ordered", min))$y - probe)
```

Observed: sparse `kept=8282`, `wrong=3972`, `max_error=2.995777` Myr; dense `wrong=6`, `max_error=0.4659139` Myr; probe errors `1.8, 1.0, 2.7, 1.5` Myr.

## Receipt index

These files support the individual verdicts above. A link identifies the evidence inspected; it does not certify the claim or authorize a restricted replay.

| Claims | Repository receipts and implementation |
|---|---|
| C076, C077 | [Detail withheld pending disclosure to the data custodian.] |
| C040 | [Latest age-comparison summary](../../../../resources/sources/nsb/profile/age_check_2023-06-05.txt), [age recomputation](../../../../resources/sources/nsb/age_check.py). |
| C043, C045 | [Triton counts](../../../../resources/sources/triton/profile/checks.tsv), [deduplication summary](../../../../resources/sources/triton/profile/dedup_v4.txt), [recipe](../../../../resources/sources/triton/triton_dedup.R), [Q012 build](../../../../data/q012-exposure-support/build.R), [Q012 known-issues account](../../../../data/q012-exposure-support/README.md). |
| C096 | [Sparse test output](../../../../resources/software/bench/results/t2/t2_strat.json), [dense/probe/modes output](../../../../resources/software/bench/results/t2/t2_checks.json), [original test](../../../../resources/software/bench/validate/t2_strat.R), [follow-up test](../../../../resources/software/bench/validate/t2_checks.R). |
| C102 | [Synthetic per-row output](../../../../resources/software/bench/results/t3/t3_flag_ranges.tsv), [test implementation](../../../../resources/software/bench/validate/t3_palaeoverse.R), [source account](../../../../resources/software/fossilbrush/README.md). |
| C107 | [Per-replicate summaries](../../../../resources/software/bench/results/e2/e2_pyrate_reps.tsv), [duration diagnostics](../../../../resources/software/bench/results/e2/e2_durations.json), [posterior summarizer](../../../../resources/software/bench/validate/pyrate_summary.py), [duration summarizer](../../../../resources/software/bench/validate/pyrate_durations.py). |
| C110, C111 | [Arm A](../../../../resources/software/bench/results/t2/t2_extinction_A.tsv), [Arm B](../../../../resources/software/bench/results/t2/t2_extinction_B.tsv), [corrected Arm C](../../../../resources/software/bench/results/t2/t2_extinction_C.tsv), [summary](../../../../resources/software/bench/results/t2/t2_extinction_summary.json), [test implementation](../../../../resources/software/bench/validate/t2_extinction.R), [scoring](../../../../resources/software/bench/validate/t2_summary.R), [declaration](../../../../resources/software/bench/VALIDATION_T2.md). |
| C119 | [Palaeogeography aggregate profile](../../../../resources/sources/palaeogeography/profile/palaeogeography_profile.tsv), [profiler](../../../../resources/sources/palaeogeography/palaeogeography_profile.py), [source account](../../../../resources/sources/palaeogeography/README.md). |
| C123, C125 | [Public-coordinate route comparisons](../../../../resources/software/bench/results/t3/v6_merged.tsv), [original geometric checks](../../../../resources/software/bench/validate/t3_checks.py), [original aggregate output](../../../../resources/software/bench/results/t3/t3_checks.json). |
