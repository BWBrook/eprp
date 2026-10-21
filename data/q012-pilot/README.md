# Q-012 bounded kunanyi pilot: the package

Owner: Claude | 16–19 October 2026 | Prepared under Codex's rulings 76/1750,
1765, 1774, 1814, 1855, 1895 and 2066.

**Status (19 October 2026):**
- **R00 (v5):** ran (job 820950). It qualified and failed only the E-BFMI
  screen.
- **R00 (v6, partial non-centring):** ran (job 821087). It qualified and
  **passed every screen**. Codex accepted v6 as the technical pilot
  candidate (76/1855).
- **P11 first attempt (job 821265):** failed. It did not qualify
  (non-empty stderr), and its unqualified statistics show one divergence and
  an η upper-endpoint MCSE of 0.0113. P06 was held.
- **Amended P11 (job 821502, Codex 76/1895):** qualified, and **fails the
  screen on two post-warmup divergences** out of 32,000. No sampling
  rejection was logged; every other screen passes, including the η
  endpoint MCSE. Its first 4,000 saved rows per chain are byte-identical
  to the first attempt's; changing f_tol did not remove the same recorded
  chain-1 divergence.
- **Diagnostic replay (jobs 822655–822656, Codex 76/2066):** P11 chain
  IDs 1–2, run under an observation-only sampler patch, **exactly
  replayed the saved path** (6,000 rows × 125 columns plus adaptation,
  both chains). It captured both sampling divergences in full. Each is a
  local integration failure: a single leapfrog step on an excursion into
  σ's upper tail, with coupled κ/log σ and log k/log σ stiffness. Neither
  is a solver failure or a σ → 0 excursion.
  - Q = 64 fails its normaliser gate at one captured preceding state
    (Codex 76/2096).
  - The first attempt's 2.18e-11 Powell rejection is strongly attributed to
    a warmup step (chain 1, transition 102).
- **Remedy allocated (Codex 76/2096):** one bounded trial with Q = 80 and
  adapt_delta 0.999, four chains, after a wider numerical preflight. P06
  and the other ten stay held under every outcome.
- **P06 and the other ten panel datasets remain held.** No power, coverage
  or campaign claim follows from this pilot.

This is a **numerical and cost pilot**. It is not a power, coverage or
robustness experiment, and no campaign claim follows from it.

## What it runs

| Job | What | Gate |
| --- | --- | --- |
| Build (`pbs/build.pbs`) | Build CmdStan 2.38.0 and the model on a compute node, then preflight it (`pbs/preflight.sh`): log density and gradients at three fixed points against local references, plus a four-chain initialisation smoke run | Payload and tarball hashes; any failure stops the replay (afterok) |
| Technical replay R00 (`pbs/fit.pbs`, SCEN=R00) | The v4 cost dataset (seed 20261060, 264 lineages) at 64 nodes: 4 chains, 2,000 warmup + 4,000 draws, adapt_delta 0.995, depth 12, step 0.01, seed 77017, frozen prior-centred starts | Runs only if the build passes |
| Panel P01–P12 (`qsub -J 1-12 pbs/fit.pbs`) | λ₀ ∈ {0.0708, 0.096} × η ∈ {0, 0.05, 0.20} at σ 0.5, two frozen seeds per cell | **Submitted only after Codex reviews the replay.** PBS exit 0 does not release it |

- The seed table, [scenarios.tsv](scenarios.tsv), was committed at
  `c93ea58`, before any panel dataset was generated.
- All 13 datasets generated within the cap and the 120 s timeout (sizes in
  `payload/manifest.json`).
- Every scenario's four starts initialise through Stan's own initialiser.
- Starts are never moved to a scenario's generating values.

## The candidate: the prototype's v5

The [prototype's v5](../q012-prototype/README.md) is v4's model, priors,
Powell solver and guards, with **64-node** fixed AGH. Its checks are in
[checks_v5.json](../q012-prototype/checks_v5.json):
- **Precision gate passes everywhere it is applied:**
  - the old gates;
  - Codex's eight tail states (worst log error 1.25e-5, worst d/dσ error
    1.45e-4);
  - 40 evenly spaced v4 states.
- Actual Stan AD and tight-tolerance stability pass at the central, stress
  and maximum-σ points.
- The 200 probes give no unrecoverable error. Every probe row and its full
  stdout are kept (`probes_v5_stdout.tar.gz`).
- The checks are **hash-bound** to the model source, `prototype.py`,
  `quadrature.py`, the config blocks, the starts and the cost dataset.
  `pilot.py build` refuses stale or failing checks.

## Hash binding and controls

- **Hashing.** `payload/manifest.sha256` covers every payload file; the
  CmdStan tarball is pinned in `cmdstan.sha256`.
- **The prototype checks** are bound to the model source, code, config,
  starts and cost dataset, and to every saved-draw CSV bank they consume
  (v1, v2, v3 and v4 fits).
- **Refusals.** The build verifies both hashes before building. Every fit
  refuses (exit 2) unless all of these hold:
  - the build receipt is `ok` **and was produced for the current payload
    manifest**;
  - the binary matches the receipt's hash;
  - the declared module (the build's GCC 12.3 stack) is loaded, which
    `fit.pbs` does before starting;
  - `ldd` finds every shared library on the compute node.
- **Attempts.** Each fit writes `runs/<id>/attempt<n>/` with per-chain
  CSV, stdout, stderr, exit code and GNU `time` peak memory, plus a
  key=value receipt. Earlier attempts are never overwritten.
- **Resume and signals.** A complete receipt under the same manifest and
  binary makes a rerun a no-op (resume/skip). Each chain runs in its own
  process group within the job's session. On TERM or INT the groups get
  TERM, then KILL after 5 s. The `terminated_*` receipt is written only
  after the groups are gone, and it records whether escalation was needed
  and whether anything survived.
- **No retries.** Nothing retries, lengthens a run or replaces a dataset.

`pilot.py selftest` exercises every one of these controls with cheap
fixtures, using the frozen-seed dataset and the local binary. It includes a
model that ignores TERM, a build receipt for another manifest, an unloaded
module, retrieval after a failed build with no run directory (`pbs/pack.sh`),
and a mutated saved-draw bank. Results: [selftest.json](selftest.json).

## Screening (`pilot.py diagnose`)

**Qualification comes first.** A fit is screened only if every structural
check passes:
- its receipt names the same scenario and attempt, status `complete`, the
  current manifest, the built binary and the declared settings;
- the build receipt names the same manifest;
- the attempt holds exactly `chain1`–`chain4` `.csv`, `.stdout`,
  `.stderr` and `.exit`, and nothing else;
- every exit is 0, stderr is empty and stdout shows no fatal message;
- each CSV header matches the declared settings, data file and start file;
- every chain has exactly the declared number of retained draws.

Otherwise the fit is `unresolved`, with the reasons, and no statistics are
computed. Nothing is truncated or paired by position.

**Pass rules** (Codex's thresholds; screening, not proof of unbiased
inference):
- four complete chains;
- zero post-warmup divergences;
- no fatal or sampling-phase numerical failure;
- E-BFMI ≥ 0.3 per chain;
- R̂ < 1.01 for every non-diagnostic column, including lp__ and the latent
  x;
- bulk and tail ESS ≥ 400 for the core parameters.

**Reported:**
- depth-limit hits and rejections by phase and cause;
- η's 5% and 95% endpoints at full precision, with chain-preserving
  quantile MCSE (ArviZ 0.20.0) against a target of 0.01;
- the raw D and X flags, with a separate flag when an endpoint ± 2 MCSE
  crosses 0.05 or 0.20.

**Finite guards.** Non-finite R̂ or ESS fails. Non-finite endpoints or
MCSE leave the affected flags and the precision status `unresolved`; they
are never passed. E-BFMI follows CmdStan's `diagnose` definition.

`pilot.py summarise DIR` gives the same statistics for historical output
such as the v4 fit, labelled as not pilot qualification. On v4 it
reproduces R̂, ESS and the η endpoints, and fails v4 on divergences,
E-BFMI, R̂ and ESS.

Every attempted dataset, cap, timeout and failed fit stays in the
denominator: report [s/n, (s+u)/n].

## Amendments to Codex's package (accepted, 76/1765)

1. **The per-fit cap is raised from 2 h to 6 h** (walltime 06:10:00).
   - **Basis:**
     - v4 chains took 831–891 s for 2,000 iterations here;
     - the pilot runs three times as many iterations, at adapt_delta
       0.995;
     - 64-node gradients cost 1.7–2.8 times v4's at identical points
       (three benchmark runs);
     - the smoke warmup adapted step sizes near 0.0057.
   - **Projection:** about 1.6–2.7 h per fit on this laptop. kunanyi's
     per-core speed is unmeasured.
   - **Ceiling:** 13 × 6 h × 4 CPUs = 312 core-hours for the fits, plus
     8.7 for job overhead and 4 for the build. These are ceilings, not
     measured cost.
   - **Scope of Codex's acceptance:** the cap is accepted for the R00
     technical replay. The panel's resources are reconsidered from R00's
     measured cost and diagnostics, and the ceiling is not a release of
     the panel.
2. **The local smoke budget for v5 is 300 s, not 60 s.** It was declared
   after the 60 s run timed out on cost alone: 1 of 4 chains complete, no
   fatal error, no rejection. That record is kept as
   `checks_v5_smoke60.json`. The 300 s rerun completed all four chains in
   70 s. The cluster preflight smoke allows 600 s.

## Staging record (16 October 2026)

- **The first four builds failed in seconds at the module load.** Each
  stopped its R00 by `afterok`. They are kept on kunanyi under tags `r00`,
  `r00b`, `r00c` and `r00d`:

  | Build | Cause | Repair in the next attempt |
  | --- | --- | --- |
  | 820938 (manifest 9327b837…, as cleared) | `module: command not found` | `#!/bin/bash -l` |
  | 820943 | the same | source `/etc/profile.d/lmod.sh` |
  | 820945 | that file reads `SLURM_NODELIST`, which aborts under `set -u` before a receipt | relax `set -u` around Lmod only, and add an EXIT trap that writes a failed receipt |
  | 820947 | **`/etc/profile.d/lmod.sh` returns early whenever `PBS_NODEFILE` is set**, so batch jobs never get `module` | initialise Lmod directly in the PBS scripts: the site `MODULEPATH`, then `/opt/ohpc/admin/lmod/lmod/init/bash` |

  The cause is a recent "optimised", warewulf-managed site init. It also
  affects other projects' PBS scripts that rely on `module`.
- **Running:** build/preflight `820949.kunanyi-ohpc` (GCC 12.3.0 loaded,
  GNU Make 3.82), then R00 `820950.kunanyi-ohpc` with `afterok:820949`.
  - Queue `normal`; 1 node, 4 CPUs, 8 GiB, walltime 06:10:00.
  - Mail points `ae` on both.
  - Tag `r00e`; payload manifest feaf5ce8….
- **Build 820949 passed (exit 0):**
  - stanc3 v2.38.0, GCC 12.3.0, Make 3.82;
  - binary sha256 87f90015…;
  - preflight log density and gradients match the laptop references within
    1e-6 at all three points;
  - the four-chain smoke check passed;
  - 18 min wall time, 11 min CPU, peak memory 2.5 GB.
- **R00 820950 started at 11:38 UTC** on n011. The first gradient took
  14.0–17.6 ms per chain, against 11.1–11.8 ms in the laptop's v5 smoke
  check, so kunanyi is about 1.2–1.6× slower per core. The projected fit
  time is roughly 2–4.3 h, inside the 6 h cap.
- **Payload:** Codex cleared manifest 9327b837… (76/1774). The only changes
  since are the PBS scripts' shell and Lmod initialisation above; data,
  starts, model and run settings are byte-identical. Each tarball was
  verified by hash on kunanyi before submission.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261016-r00e`.
  - `/scratch/bwbrook` is at its 8 TiB quota ("Disk quota exceeded").
  - Home holds the 20 TiB allocation (TPAC, per X-ray Cavities' log of 21
    August).
  - Barry directed: do not use scratch. The scripts now default to
    `/u/bwbrook/codex_kunanyi`.
- **Transfer:** uses scp's legacy protocol (`-O`). kunanyi's SFTP path
  reported the scratch quota failure only as "close remote: Failure",
  leaving a 0-byte file. The empty directory
  `/scratch/bwbrook/q012-pilot-20261016-r00` from that attempt remains
  (0 bytes).
- **Host key:** this laptop's stale `kunanyi` pin (`c/CENudr…` and ECDSA)
  was replaced with Barry's authorisation. The new key, ED25519
  `IzXcim01EZc9FMqnrbDIfX9WfFSrK1RMwFq5McL4zpI`, is the one accepted on 30
  June and already held by the Mac mini. A backup is at
  `~/.ssh/known_hosts.bak-20261016-kunanyi`.

## Execution, when Codex has checked the package

```bash
uv run --python 3.12 data/q012-pilot/pilot.py build
uv run --python 3.12 data/q012-pilot/pilot.py selftest
```

```bash
KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/stage.sh
```

`stage.sh` runs only while Barry has the jumpbox window open. It uploads
the payload and the tarball, verifies hashes on kunanyi, submits the build
and then the replay with `afterok`, and prints `qstat -f` to show the mail
and dependency settings. Barry receives PBS mail when the replay ends or
either job aborts. Then:

```bash
KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/fetch.sh TAG R00
```

`fetch.sh` runs `pbs/pack.sh` on kunanyi. It archives whatever evidence
exists (submission record, PBS accounting, build directory, the run's
attempts and PBS output files), so a failed build is retrievable too.

```bash
uv run --python 3.12 data/q012-pilot/pilot.py diagnose scratch/q012-pilot/fetch-TAG/runs/R00/attempt1 R00
```

The replay's receipts and diagnostics go to Codex. The panel is a separate
decision and a separate jumpbox window.

## R00 technical replay: result (job 820950, 16 October 2026)

Evidence: [results/R00-20261016-r00e/](results/R00-20261016-r00e/). It holds
the receipts, PBS accounting, `diagnostics.json` and hashes of every chain
file. The 102 MB of chain output stay on kunanyi and in scratch.

**Run:**
- **Completed** in 2 h 50 min wall time (10,196 s), inside the 6 h cap.
- 11 h 13 min CPU; peak memory 77 MB (from PBS accounting; GNU `time` is
  not installed on the compute node, so the per-chain fields are blank).
- **Per chain:** warmup 2,715–3,031 s, sampling 7,152–7,265 s. Adapted
  step sizes 0.0137–0.0168. Median tree depth 8 (255 leapfrog steps),
  maximum 9, no depth-limit hits.

**Qualified:** the receipt, manifest (feaf5ce8…), binary, settings, file
set, exits, stderr, CSV headers and 4,000 draws per chain all match.

| Screen | R00 | Threshold | Pass |
| --- | --- | --- | --- |
| Post-warmup divergences | 0 | 0 | yes |
| Fatal or sampling-phase failures | 0 | 0 | yes |
| Max R̂, all 590 columns | 1.004 (σ) | < 1.01 | yes |
| Minimum core ESS, bulk / tail | 725 / 1,433 (σ) | ≥ 400 | yes |
| **E-BFMI per chain** | **0.289, 0.268, 0.315, 0.290** | ≥ 0.3 | **no** |

**Screening fails on E-BFMI alone, so the panel is not promoted.**

**η, reported only:**
- 90% interval 0.0264–0.5109 (truth 0.2);
- endpoint MCSE 0.0013 / 0.0058, so the 0.01 target is met;
- raw D = no, X = no; neither is numerically uncertain.

**Interpreting the low E-BFMI** (revised after Codex's review, 76/1814;
the first wording was too causal):
- **Correlations, post-warmup draws:**
  - the energy correlates with log σ (−0.78), log k (−0.74) and κ (−0.54);
  - those three are strongly correlated with one another (0.69–0.87).
- This is *consistent with* a frailty-versus-ageing trade-off, but does not
  establish it as the source.
- **Codex's energy calculation is the sharper account.** For any fixed
  Gaussian metric, the stationary exact-Hamiltonian limit of CmdStan's
  E-BFMI is d / (Var(U) + d/2), with d = 299.
  - R00's Var(U) of 789–938 predicts 0.275–0.319, which matches the
    observed values.
  - A dense metric, or any affine change of coordinates, leaves Var(U)
    unchanged. My proposed `dense_e` remedy was therefore withdrawn.
  - A nonlinear reparameterisation can reduce Var(U): see the v6
    candidate below.
- E-BFMI barely changed from v4 (0.258–0.326), despite stricter adaptation
  and three times as many iterations.

## v6 R00 comparison: staging record (17 October 2026)

- **Submitted:** build/preflight `821085.kunanyi-ohpc` (running on n008,
  GCC 12.3.0 loaded), then the v6 R00 comparison `821087.kunanyi-ohpc`
  with `afterok:821085`.
  - Queue `normal`; 4 CPUs, 8 GiB, walltime 06:10:00; `ae` mail.
- **Payload:** `payload_v6/`, manifest 936c2a56…; tarball d4e5ba03….
  Both tarballs verified by hash on kunanyi.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261017-v6r00`.
- **Next:** fetch with `fetch.sh 20261017-v6r00 R00`, then `pilot.py
  diagnose` (with `active_candidate` v6), the comparison with R00, and
  Q = 64 checks on any new tails.

## v6 R00 comparison: result (job 821087, 17 October 2026)

Evidence: [results/R00-v6-20261017-v6r00/](results/R00-v6-20261017-v6r00/).
It holds the receipts, accounting, `diagnostics.json`,
`comparison_with_R00.json` and hashes of every chain file. The 147 MB of
chain output stay on kunanyi and in scratch.

**Run:**
- **Completed:** build 821085 (20 min, preflight passed on n008), then the
  fit in 4 h 40 min wall time (16,825 s), inside the 6 h cap. 11 h 45 min
  CPU; peak memory 72 MB (PBS).
- **Qualified:** receipt, manifest 936c2a56…, binary 1a7bc6f9…, settings,
  files, exits, stderr, CSV headers and 4,000 draws per chain all match.

**Screening: passes on every criterion, the first full pass.**

| Screen | v6 | R00 (v5) |
| --- | --- | --- |
| E-BFMI per chain | **0.751, 0.732, 0.768, 0.780** | 0.289, 0.268, 0.315, 0.290 |
| Divergences / fatal / depth hits | 0 / 0 / 0 | 0 / 0 / 0 |
| Max R̂, all columns | 1.0016 (τ) | 1.004 (σ) |
| Minimum core ESS, bulk / tail | 1,125 / 2,298 (σ) | 725 / 1,433 (σ) |
| η 90% interval (truth 0.2) | 0.0240–0.4993 | 0.0264–0.5109 |
| η endpoint MCSE | 0.0014 / 0.0049 (met) | 0.0013 / 0.0058 (met) |
| Raw D / X | no / no; not numerically uncertain | no / no |

The E-BFMI values fall inside Codex's ideal-limit proxy for v6, 0.72–0.78.

**Comparison with R00** (`pilot.py compare`):
- **MCSE-scaled differences (descriptive):** across the 11 core
  parameters' mean, 5% and 95% quantiles, the largest is |z| = 1.69; η's
  endpoints differ by z = −1.23 and −1.53.
  - *Convention:* z = (v6 − R00) / √(MCSE₁² + MCSE₂²) assumes zero
    covariance between the two fits' Monte Carlo errors.
  - The fits share seeds and chain IDs, so this is **not a calibrated
    equality test** (Codex, 76/1855).
  - Source/AD equivalence and v6's own diagnostics are the stronger
    evidence.
- **Quadrature at v6's joint states (corrected):**
  - The first version of this section claimed that v6 stayed inside
    R00's marginal ranges, so R00's checks covered it. That is invalid:
    marginal ranges do not bound joint-state quadrature error, the
    shortcut tested no points, and maximum ρ in fact rose from 0.730 to
    0.813.
  - `compare` now checks selected v6 joint states directly: the six
    highest σ, largest |κ_b|, smallest and largest ρ, and 40 evenly spaced
    states, with domain-safe finite-difference steps.
  - **All 49 pass at Q = 64:** maximum log error 2.42e-5, maximum
    derivative error 8.38e-5. Doubling the reference grid at the worst
    point changes the result by 1.3e-15 and 1.7e-11.
  - These reproduce Codex's independent check exactly.
- **σ's lower tail, per chain:**

  | | Range across chains |
  | --- | --- |
  | 0.1% quantile | 0.198–0.220 |
  | 1% quantile | 0.281–0.316 |
  | Minimum | 0.156–0.187 |
  | Mass below 0.1 | none |

  This posterior is well away from σ = 0, so the near-zero concern
  remains **incompletely tested**. P11, the weak-data tree, is next for
  that reason.

**Cost.** Adaptation differed widely between chains:

| Chain | Step size | Median tree depth | Mean leapfrog steps | Sampling time |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0.0097 | 9 | 511 | 13,714 s |
| 2 | 0.0192 | 8 | 255 | 7,082 s |
| 3 | 0.0333 | 7 | 127 | 3,526 s |
| 4 | 0.0139 | 8 | 255 | 6,914 s |

The fit's wall time is the slowest chain's: 4.67 h at N = 264.
- **Seconds per leapfrog step are similar across chains** (0.0067–0.0069),
  so the spread comes mainly from adapted trajectory length.
- **Against R00 (v5):** CPU rose about 4.7%, wall time about 65%, and
  nominal allocation from 11.33 to 18.70 core-hours.
- *Withdrawn:* an earlier version of this section predicted that the
  largest panel trees would probably exceed 6 h. Per-step cost is not a
  function of N alone. In unadapted local probes (20 draws, step 0.002,
  depth capped at 6, so not posterior or cluster estimates), P05 (N = 49),
  P06 (N = 84) and P07 (N = 385) cost 3.06, 3.90 and 2.21 times R00 per
  leapfrog step, while P12 (N = 649) cost 1.26 times. Codex kept the 6 h
  cap; P06 is the deliberate cost test in the next tranche.

## Next tranche: P11, then P06 (Codex 76/1855–1856)

- **Package:** `payload_v6p/` (candidate `v6p`, manifest 592a1ce3…).
  - **R00** serves only as the build/preflight reference.
  - **The permitted fits are P11 and P06**, listed in `fits.txt`.
  - Data are byte-identical to the frozen originals. The starts are exact
    a = 0.2 mappings of the original panel starts, and all initialise.
- **Tranche preflight** ([tranche_preflight_v6p.json](tranche_preflight_v6p.json),
  all pass), at P11's and P06's mapped starts and at σ = 0.01 and 0.001:
  - actual-Stan v5/v6 identity, worst 7.5e-13 (log) and 8.0e-15 (scaled
    gradient), all finite;
  - Q = 64 against the reference, worst log error 2.9e-15, derivative
    error 1.2e-11.
- **Dispatch** ([dispatch_test_v6p.json](dispatch_test_v6p.json), local
  fixture with fake transport and qsub, all pass):
  - `FIT_SCEN=P11 stage.sh` submits only the build, then
    `-v SCEN=P11 -W depend=afterok:<build>`;
  - a missing scenario and R00 are refused, and no array is submitted;
  - `submit_fit.sh TAG P06` is refused without a successful build for the
    same manifest. Once the build has succeeded, it submits only
    `-v SCEN=P06`.
- **Order:**
  1. stage `PAYLOAD_DIR=payload_v6p FIT_SCEN=P11`;
  2. after P11's mail: fetch, then `diagnose`, then `pilot.py joint` (49
     direct joint states, plus σ's lower tail);
  3. only if P11 qualifies and passes the sampling, endpoint-MCSE and
     joint checks: `submit_fit.sh TAG P06`.
- **Budget:** one fit at a time, 4 CPUs, 8 GiB, a 6 h runner cap (6:10 in
  PBS); at most 53.33 reserved core-hours. No retry, cap raise,
  replacement or search.

### Tranche staging record (17 October 2026)

- **Submitted:** build/preflight `821264.kunanyi-ohpc` (running on n001,
  GCC 12.3.0), then **P11** `821265.kunanyi-ohpc` with `afterok:821264`.
  - Queue `normal`; 4 CPUs, 8 GiB, 06:10:00; `ae` mail.
  - Nothing else was submitted.
- **Payload:** `payload_v6p`, manifest 592a1ce3…; tarball c29c4630…. Both
  verified on kunanyi.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261017-v6p`.
- **P06** is not queued. It waits on P11's qualification, its sampling and
  endpoint-MCSE screens, and the joint checks; then
  `submit_fit.sh 20261017-v6p P06`.

### P11 result (job 821265, 17 October 2026): fails; P06 not submitted

Evidence: [results/P11-20261017-v6p/](results/P11-20261017-v6p/). It holds
the receipts, accounting, the qualification record, the stderr files, the
unqualified statistics, the joint checks and the chain-file hashes.

**Run.** It completed (exit 0) in 1 h 02 min (3,723 s), using 3.9 CPU-hours
and 62 MB. The build/preflight (821264, n001) passed.

**Qualification fails, as the rule is written: chains 1–3 have non-empty
stderr.**
- The content is four labelled domain rejections in total:

  | Chain | Rejection |
  | --- | --- |
  | 1 | Powell residual 2.18e-11 against the 1e-11 tolerance |
  | 2 | a Powell residual of 1.9e11 |
  | 2 | `Q012 input failure`, with A = inf |
  | 3 | `Q012 input failure` on the initial score |

- Stan writes these through `logger.error`
  (`base_hamiltonian.hpp:83–87`), which goes to stderr.
- `fit.sh` separates the two streams, so these messages cannot be assigned
  to a phase from the files.
- The rule was frozen before the run, so it was not relaxed after seeing
  the result.

**Even unqualified, the statistics fail the screen** (historical mode;
information only):

| Screen | P11 | Pass |
| --- | --- | --- |
| Post-warmup divergences | **1** (chain 1, at σ = 0.79, ρ = 0.10) | no |
| E-BFMI | 0.862, 0.906, 0.863, 0.871 | yes |
| Max R̂ | 1.0016 (σ) | yes |
| Minimum core ESS, bulk / tail | 2,983 / 3,979 (σ) | yes |
| η endpoint MCSE | 0.00036 / **0.0113** | target **not met** (0.01) |

**η and the decision flags:**
- 90% interval 0.0047–0.594 (truth 0.2); raw D = no, X = no.

**The near-zero concern is now genuinely tested:**
- σ's posterior reaches down to σ = 4e-5, with **16.7% of draws below 0.1
  and 1.9% below 0.01** in every chain.
- *Corrected (Codex, 76/1895):* the saved divergent row (σ = 0.79) is the
  state selected from the trajectory, not the failed proposal. It cannot
  exclude a near-zero excursion. Likewise, the historical
  `no_fatal_or_sampling_phase_failures` field read stdout only, so the four
  stderr rejections have **unknown phase**; it is not an observed zero.
- **Direct joint-state checks pass at all 49 states:** maximum log error
  8.0e-6, derivative error 3.9e-5; reference convergence 4e-16 / 1e-11.

**Stop rule applied:** P11 does not pass, so P06 was **not** submitted.
The evidence goes to Codex.

## Amended P11 attempt: preparation (Codex 76/1895)

- **Package:** `payload_v6p2/` (candidate `v6p2`, manifest d2ecaddb…).
  - **P11 is the only permitted fit**; R00 is the build/preflight
    reference.
  - **The sole data change is `solver_f_tol` 1e-11 → 1e-10**, asserted
    field by field against the frozen originals. `rel_tol` (1e-12),
    `max_steps` (200), `check_tol` (1e-8), Q = 64, a = 0.2, priors, starts,
    seed and chain IDs are unchanged.
  - **Run settings:** 2,000 warmup plus a fixed 8,000 retained draws;
    `refresh=1`; log format `combined`.
- **Runner** (`payload_v6p2/pbs/fit.sh`): each chain writes one ordered
  `chain<k>.log`, with stdout and stderr on the same open file. It refuses
  unless `run.env` declares the combined format and the refresh setting,
  and the receipt's settings line records both.
- **Qualification** (`parse_log`, fail-closed). The only recognised line
  types are:
  - the CmdStan config echo and the gradient-timing block;
  - the low-warmup warning;
  - sequential `Iteration:` markers 1…N, labelled Warmup up to the warmup
    count and Sampling after;
  - complete rejection envelopes, whether initial-value or Metropolis;
  - the elapsed-time block.

  **Classification:**
  - Rejections are attributed to init, step-size initialisation, warmup
    (with transition) or sampling.
  - Recognised causes in init, step-size and warmup are recorded; any
    sampling rejection fails the screen.
  - Unknown text or causes, orphan exceptions, incomplete envelopes,
    missing, repeated or mislabelled markers, and a missing completion
    block all fail qualification.
  - Old separate-stream attempts are still read as before. A non-empty
    stderr now leaves the sampling-failure criterion *unknown*.
- **Numerical checks:**
  - **Reference convergence is signed:** the references are compared
    directly at 1,600 against 3,200 intervals, and are unconverged above
    1e-6 in value or 1e-5 in derivatives.
  - **Disputed points use a local-mode reference:** where the coarse
    reference is unconverged, a chunked Simpson rule centred at each
    Newton mode is used, with its own resolution and domain checks.
  - **Fail-safe:** a state with no converged reference is unresolved,
    never passed.
- **Amended preflight** ([amended_preflight_v6p2.json](amended_preflight_v6p2.json),
  all pass):
  - data and starts as above;
  - v5/v6 identities at P11's starts and σ = 0.01 / 0.001;
  - **1e-11 against 1e-10: identical log density and AD gradients at 60
    accepted states.** These are P11's starts, small σ, and the first P11
    fit's 49 joint states, divergent state and per-chain minimum-σ states.
  - **Controls:** p75 is accepted at 1e-10 and rejected at 1e-11 (on R00
    and P11, with finite values); p53 is rejected at both. AD agrees with
    finite differences at p75 (scaled errors 3.6e-8).
  - **Q = 64:** worst error 1.5e-11. p75 is classified with the
    local-mode reference, since the coarse reference is unconverged there
    (it shifts 0.245 when the grid doubles).
  - For P11-mapped p53, cmdstanpy reports only a generic failure, so that
    rejection's cause is unconfirmed. For R00 the build asserts the Powell
    residual message.
- **Cluster preflight:** adds p75 as a log-density control and p53 as a
  reject control, which must fail with the Powell residual message.
- **Controls tested:**
  - [selftest.json](selftest.json): all pass, including 13 parser cases
    and the end-to-end sampling rejection (qualified, then fails the
    screen).
  - [dispatch_test_v6p2.json](dispatch_test_v6p2.json): only build plus
    P11 (afterok); R00 refused; P06 refused even after a successful build.

### Amended P11 staging record (18 October 2026)

- **Submitted:** build/preflight `821501.kunanyi-ohpc` (running on n017,
  GCC 12.3.0), then the **amended P11** `821502.kunanyi-ohpc` with
  `afterok:821501`.
  - Queue `normal`; 4 CPUs, 8 GiB, 06:10:00; `ae` mail.
  - Nothing else was submitted.
- **Payload:** `payload_v6p2`, manifest d2ecaddb…; tarball 5bdc5967….
  Both verified on kunanyi.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261018-v6p2`.

### Amended P11 result (job 821502, 18 October 2026): fails on divergences

Evidence: [results/P11-amended-20261018-v6p2/](results/P11-amended-20261018-v6p2/).
It holds the receipts, PBS accounting, the qualification and screening
record (`diagnostics.json`), the combined chain logs (gzipped), the joint
checks, the cross-attempt comparison and the chain-file hashes.

**Run.** The build/preflight (821501, n017, 19 min) passed, including both
controls: p75 accepted, p53 rejected with a Powell residual of 2.62e-10
against 1e-10. The fit completed (all chains exit 0) in 1 h 55 min
(6,896 s in the runner), using 7.0 CPU-hours and 63 MB.

**Accounting.** (0:19:10 + 1:55:00) × 4 CPUs = **8.94 core-hours** of the
28.67 released. The P11/P06 tranche total is now 6.06 + 8.94 = **15.00 of
its 53.33 ceiling** (this excludes the earlier R00 jobs).

**Qualification passes.** All four combined logs parse completely under
the fail-closed parser. The only logged rejections are in warmup:

| Chain | Transition | Cause |
| --- | --- | --- |
| 2 | 252 (warmup) | Powell residual 1.86e11 |
| 2 | 452 (warmup) | `Q012 input failure`, A = inf |
| 3 | 252 (warmup) | `Q012 input failure`, initial score |

All three fall two transitions after the metric updates at 250 and 450.
Chains 1 and 4 log nothing, and **no chain logs any sampling-phase
rejection**.

**Screening fails on one criterion:**

| Screen | Amended P11 | Pass |
| --- | --- | --- |
| Post-warmup divergences | **2 of 32,000** (chain 1 transition 4,426; chain 2 transition 6,652) | **no** |
| Fatal or sampling-phase failures | none | yes |
| E-BFMI | 0.870, 0.898, 0.869, 0.874 | yes |
| Max R̂ | 1.0004 (`z_rw.17`); core max 1.0002 (γ) | yes |
| Minimum core ESS, bulk / tail | 6,209 / 8,530 (σ) | yes |
| η endpoint MCSE | 0.00022 / 0.0076 | yes (target 0.01) |

η's 90% interval is 0.0050–0.594 (truth 0.2); raw D = no, X = no, neither
numerically uncertain.

**The first 4,000 saved rows per chain are byte-identical to the first
attempt's** (all 125 columns, every chain), and so is the adaptation output
(step sizes and metrics). The model source, seed, starts and settings are
the same; the rebuilt binaries differ in hash.

*Corrected (Codex 76/2066).* An earlier version of this section drew
stronger conclusions than the evidence supports. The saved rows are
finite-precision records (eight significant digits); intermediate leapfrog
states and momenta were not saved. Identical saved prefixes therefore do not
prove that every unsaved trajectory was unchanged, that the tolerance
change affected no proposal, or that the first attempt's 2.18e-11 rejected
proposal later exceeded the energy threshold. The supported statements are:
- **Intervention result:** changing f_tol from 1e-11 to 1e-10 did not remove
  the same recorded chain-1 divergence (transition 4,426). Where the old
  2.18e-11 rejection occurred is not known.
- **Phases:** the amended logs directly phase this attempt's three
  remaining messages (all warmup). That the first attempt's matching
  messages had the same phases is an inference from determinism, not an
  observation.
- **New evidence:** draws 4,001–8,000 per chain, 16,000 further
  transitions, with one new divergence (chain 2, transition 6,652).

**Neither divergence has a logged rejection.** Stan 2.38's `base_nuts.hpp`
flags a divergence when the *signed* energy change H − H0 exceeds 1,000,
after converting a NaN H to infinity; it does not test the absolute error.
So each is a positive energy change above 1,000, or a non-finite H that
raised no exception. The start state (the previous draw) and the saved
state are not the divergent step, so the opposite σ tails below cannot
exclude an excursion toward zero in either trajectory:

| Divergence | Start σ (pooled percentile) | Saved σ | Step size |
| --- | --- | --- | --- |
| chain 1, 4,426 | 1.38 (97th) | 0.79 | 0.040 |
| chain 2, 6,652 | 0.030 (5th) | 1.03 | 0.047 |

**Lower σ tail (all 8,000 draws):**

| Chain | 0.1% quantile | 1% quantile | Minimum | Below 0.1 | Below 0.01 |
| --- | --- | --- | --- | --- | --- |
| 1 | 3.7e-4 | 6.3e-3 | 4.9e-5 | 16.0% | 1.7% |
| 2 | 3.4e-4 | 3.1e-3 | 4.2e-5 | 17.4% | 2.1% |
| 3 | 1.6e-3 | 6.8e-3 | 3.8e-4 | 16.3% | 1.6% |
| 4 | 9.2e-4 | 5.4e-3 | 4.6e-5 | 16.6% | 1.8% |

**Direct joint-state checks pass at all 49 states**, each with a converged
reference: maximum log error 8.0e-6, derivative error 3.9e-5, reference
convergence 4e-16 / 1e-11. These equal the first attempt's maxima, as the
shared prefix implies.

**Stop rule applied.** The amended P11 does not pass. Nothing else was
submitted; P06 and the other ten remain held. The evidence goes to Codex.

## Diagnostic replay package (Codex 76/2066)

Codex's review (`ideas/2026-10-19-q012-amended-p11-review-codex.md`)
allocated a passive capture of the failing leapfrog steps before any
remedy is chosen. It is an **instrumented diagnostic attempt**: not a
qualification attempt and not a dataset replicate. P06 and the other ten
stay held in every outcome.

**Package** `payload_v6d/` (candidate `v6d`).
- **Inputs:** data, starts, preflight points and model source are
  identical to `payload_v6p2/` (build() asserts it; reference CSVs are
  compared on their data lines).
- **Settings:** a = 0.2, Q = 64, f_tol 1e-10, all guards and priors, seed
  77017, diag_e, adapt_delta 0.995, depth 12, initial step 0.01 and 2,000
  warmup are all unchanged. Retained draws are fixed at 6,000 per chain, so
  both known events (transitions 4,426 and 6,652) fall inside the horizon.
  Logs are combined at refresh 1.
- **Chains:** chain IDs 1 and 2 only (`CHAINS=2`), with their original
  starts.
- **Resources:**
  - build/preflight: 4 CPUs, 8 GiB, 1 h;
  - fit: 2 CPUs, 8 GiB, 3:10 PBS (3 h runner).
  - At most 10.3333 core-hours, within the 38.3322 left of the tranche's
    53.3333.
- **Not permitted:** arrays, chains 3–4, any other scenario, retries and
  extensions.

**The sampler patch** (`patch_v6d/base_nuts.hpp`, applied over the pinned
original eb646717… by `build.pbs`, which verifies both hashes):
- It is observation only, and active only when `Q012_TRACE_FILE` is set.
- **What it copies:**
  - the transition-initial state, after momentum and gradient
    initialisation;
  - the state before each leapfrog.
- **Where it writes:** one JSON line at the existing divergence branch
  (`H − H0 > 1000`, after NaN → ∞) to a per-chain sidecar,
  `chain<k>.trace.jsonl`. The combined CmdStan log keeps its strict
  grammar.
- **What each full record holds**, at 17 significant digits:
  - chain, transition, phase and tree depth;
  - initial, previous and failing q, p, V and grad V (Stan's `g`, the
    gradient of the potential, flagged as possibly stale when V is not
    finite);
  - the signed step size, H0, raw and effective H, and the inverse metric.
- **Caps:** full records are capped per phase (16 warmup, 64 sampling).
  Later events in a phase get short records, so warmup cannot use up the
  sampling capture. A summary line gives the counts and the write status.
- **Phase:** warmup when the transition count is at most the declared
  `num_warmup`. Init and step-size-search leapfrogs never enter
  `build_tree`.
- **What it does not add:** no log-density, gradient or Hamiltonian
  evaluation, no RNG call, and no change to any arithmetic, threshold or
  decision. The added lines are audited for calls into the sampler
  machinery.

**Repairs (Codex 76/2066):**
- **Parser:** the startup header must equal the exact CmdStan 2.38 echo of
  the runner's command line, so arbitrary identifiers or assignments now
  fail. Rejection causes follow an exact grammar:
  - each labelled `reject()` statement, with its declared value form and
    its own source line;
  - the Powell residual message, with the payload's tolerance;
  - the Powell step-limit message, with the payload's limit.
  - Keyword matches such as `newton` are gone. Regression fixtures cover
    each case.
- **Runner:** `fit.sh` itself refuses array dispatch, any scenario not in
  `fits.txt`, missing trace settings and an uninstrumented binary.

**After the run:**
- `pilot.py diagnose` reports structural qualification, descriptive
  two-chain screening and capture validity (`trace_structure`).
- `pilot.py prefix-compare` compares all 6,000 saved rows and 125
  columns, plus the adaptation output, with the hash-verified v6p2 bank,
  and reports the first mismatch. Only an exact match permits calling it a
  replay of the old saved path.
- `pilot.py trace-check` takes every full record, using the model's own
  `log_prob`, and checks:
  - the recorded V and gradient;
  - one leapfrog from the previous state, reproducing the failing state and
    H;
  - two half steps from the same previous q, p and metric;
  - actual-LP finite differences against AD;
  - the Q = 64 normaliser against a converged reference, at the failing
    state (or the previous state if the failing one is not finite);
  - the potential and kinetic split of the energy change.

### Diagnostic replay staging record (19 October 2026)

- **Submitted:** build/preflight `822655.kunanyi-ohpc` (running), then the
  **P11 diagnostic replay** `822656.kunanyi-ohpc` with `afterok:822655`,
  held until the build passes.
  - Build: 4 CPUs, 8 GiB, 01:00:00. Fit: 2 CPUs, 8 GiB, 03:10:00. Queue
    `normal`; `ae` mail.
  - Nothing else was submitted.
- **Payload:** `payload_v6d`, manifest 31038b84…; tarball c7dee063….
  Both verified on kunanyi.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261019-v6d`.
- **Comparison binary:** the v6p2 binary is present and its hash verifies
  (ff9861c5…).

### Diagnostic replay result (jobs 822655, 822656, 19 October 2026)

Evidence: [results/P11-diagnostic-20261019-v6d/](results/P11-diagnostic-20261019-v6d/).
It holds:
- the receipts, PBS accounting and build output;
- `diagnostics.json`;
- the combined logs and the divergence traces (gzipped), plus the
  preflight exercise traces;
- `prefix_comparison.json` and `trace_check.json`;
- the tolerance localisation and the initial-state check, with their
  scripts in `scripts/`;
- the chain-file hashes.

**Run.** The build/preflight (822655, n146, 28 min) passed every check:
- LP/AD points and the p75/p53 controls;
- the smoke run;
- both capture exercises, each with 12 of 12 events matching the CSV;
- the trace-on/off gate;
- `preflight_compare_old_binary=identical`, so the instrumented binary
  reproduced the v6p2 binary's output.

The fit (822656, n001) completed with both chains at exit 0 and complete
traces, in 1 h 55 min (6,877 s in the runner).

*Cosmetic:* `build_job_output.txt` shows three "Broken pipe" messages.
These come from `grep -q` and `head` closing pipes inside the preflight
checks. The checks' exit statuses are unaffected. A later package should
silence them.

**Accounting.** (0:28:23 × 4) + (1:54:44 × 2) = 1.892 + 3.824 = **5.717
core-hours** of the 10.333 released. The P11/P06 tranche total is now
15.001 + 5.717 = **20.718 of 53.333**, leaving 32.616.

**Qualification and capture.** Both combined logs pass the strict parser.
The only logged rejections are chain 2's warmup 252 (Powell) and 452
(input), as before. Capture is valid for both chains:
- each has 10 warmup and 1 sampling divergence, all recorded in full;
- nothing was dropped;
- `write_ok` is true.

The two-chain screening is descriptive only, and not a qualification:
- 1 divergence per chain;
- E-BFMI 0.861 and 0.885;
- max R̂ 1.0010;
- minimum core ESS 2,122 bulk / 2,513 tail (σ).

**Exact replay of the saved path.** All 6,000 saved rows and 125 columns
of both chains, and their adaptation output, are byte-identical to the
hash-verified v6p2 bank. Each traced transition-initial state equals the
previous saved draw to 3.5e-8 relative, which is the CSV's precision. So
the captured sampling events are the two original divergences: chain 1
transition 4,426 and chain 2 transition 6,652.

**Every full record is reproduced from the trace alone,** using the local
GCC 13 build of the same source and patch (`trace_check.json`, 22
records):
- the recorded V and grad V at the previous and failing states are
  bitwise identical to `log_prob`;
- one leapfrog from the previous q, p and metric reproduces the failing
  q, p and H bitwise.

**The two sampling divergences:**

| | Chain 1, transition 4,426 | Chain 2, transition 6,652 |
| --- | --- | --- |
| Tree depth, leapfrog count | 6, 97 | 7, 161 |
| Step size (signed) | +0.0396 | −0.0475 |
| σ: initial → previous → failing | 1.38 → 1.91 → **6.20** | 0.030 → **3.57** → 1.59 |
| V: previous → failing | 199.9 → 7,957 | 165.3 → 692.3 |
| H − H0 at the failing step | **1.08 × 10⁷** | **1,911** |
| Of which kinetic / potential | 1.08 × 10⁷ / 7,840 | 1,336 / 576 |
| Largest momentum changes | κ 3,843; σ 2,201; log λ0 149 | log k 138; σ 39; log h0 14 |
| Two half steps, same start: H − H0 | 111, then 146 | 92, then 116 |
| H − H0 already at the previous leaf (Codex) | 113.82 | 75.79 |
| Local energy increment from the previous leaf, step split into n = 1/2/4/8/16/32 (Codex) | 1.08e7 / 31.68 / 2.06 / 0.355 / 0.080 / 0.0195 | 1,835 / 40.69 / 6.40 / 1.305 / 0.308 / 0.0759 |
| AD against actual-LP finite differences (scaled) | ≤ 3.1e-7 | ≤ 4.6e-9 |
| Q = 64 normaliser against a converged reference, failing state | log 9.0e-6, d/dσ 3.0e-4: pass | log 1.5e-10: pass |
| Same check at the previous leaf (Codex) | pass | **fails: log error 1.36e-4 > 1e-4** |
| Solver or guard message | none | none |

- **Where:** both failing steps sit in σ's upper tail. Across all 32,000
  saved v6p2 draws, σ's 99.9% quantile is 2.37 and its maximum is 3.03.
  Chain 1's failing step reached σ = 6.20. Chain 2's previous leaf was at
  σ = 3.57, and its trajectory had started from σ = 0.030.
  - *Corrected (Codex 76/2096):* the saved maximum is not a bound on the
    posterior's support.
  - Earlier, uncaptured parts of these trajectories remain unknown.
- **What:** in each case a single leapfrog step blew up the energy, mainly
  through the kinetic term, in a region where the gradients are very
  large. At chain 1's failing state, dV/d(log σ) is about 1.1 × 10⁵.
- **Why it is the integrator:** the local energy increment from the
  previous leaf collapses as the step is subdivided: from 1.08e7 and 1,835
  at the full step to 31.7 and 40.7 at half. An earlier version of this
  section read the H − H0 of about 100 after two half steps as residual
  local error.
  - *Corrected (Codex 76/2096):* most of that is inherited from the
    previous leaf (113.8 and 75.8).
  - The full step is too large for the coupled κ/log σ and log k/log σ
    curvature there.
- **What the evidence rules out** for these two events:
  - solver failure (no message; every evaluation finite);
  - gradient error at the checked states (AD agrees with actual-LP finite
    differences, on all 54 coordinates in Codex's check);
  - a σ → 0 excursion at the failing steps.
- **What it does not rule out:** normaliser error.
  - *Corrected (Codex 76/2096):* Q = 64 fails the 1e-4 value gate at chain
    2's previous leaf (log error 1.36e-4). I had checked only the failing
    states.
  - The error is small beside the catastrophic local energy error, but the
    earlier blanket exclusion was wrong.
  - Fixed Q = 80, 96 and 128 pass at all four previous and failing
    points.
- **Not established:** how often such excursions occur, or which remedy
  works.

**The first attempt's 2.18e-11 rejection: a strongly supported attribution.** Every captured
previous and failing state (44 states) was evaluated under both data
files. The two files differ only in `solver_f_tol`
(`ftol_1e-11_at_captured_states.json`):
- **Exactly one state changes between the tolerances:** the failing step
  of chain 1, warmup transition 102. It is rejected at 1e-11 and finite at
  1e-10. It is the first leapfrog (tree depth 0) after the metric update at
  transition 100.
- **The residual matches:** it is 2.18243e-11, the same six digits as the
  first attempt's chain-1 stderr.
- **At 1e-10** the same step is finite, but H − H0 = 7.5 × 10¹⁷. It
  diverges at either tolerance.
- **The other 43 states.** *Corrected (Codex 76/2096):*
  - 41 are finite, with identical log density and gradients at both
    tolerances.
  - 2 are rejected at both: chain 2's warmup failing steps at 252 and 452.
- **Caveat:** this rests on the replayed path matching the first
  attempt's, which the byte-identical saved rows across all three runs
  support. The residual match strongly supports it, but it does not turn
  the old, unphased stderr stream into direct phase evidence.
- **Consequence:** the first attempt's sampling divergence (4,426) was
  never associated with a solver rejection.

**Warmup divergences** (20 in all, descriptive): 16 fall in the two
transitions just after a metric update and step-size reset (101–102,
151–152, 252, 452, 852, 1951–1952). Nine of those fail on the very first
leapfrog, and they include chain 2's two logged rejections. The other
four are chain 1 at 386–387 and chain 2 at transition 1 and at 630.

**Stop rule applied.** Nothing else was submitted. P06 and the other ten
remain held. The evidence goes to Codex for the mechanism and remedy
review; no remedy (adapt_delta 0.999, reparameterisation, prior, seed or
fit) is chosen here.

## Remedy trial package: Q = 80 and adapt_delta 0.999 (Codex 76/2096)

One bounded remedy, allocated by Codex after the captured-failure review
(`ideas/2026-10-19-q012-captured-failure-review-codex.md`). Barry approved,
in Claude chat on 19 October, one bounded fix and then a simpler estimator
if it fails. A P11 pass does not release P06 or the other ten, which stay
held under every outcome.

**Package** `payload_v6q80/` (candidate `v6q80`).
- **Data:** the only change from v6p2 is Q = 80, with its exact
  Gauss–Hermite nodes and weights (numpy `hermgauss(80)`; the weights sum to
  √π). build() asserts that no other field differs. Starts and preflight
  points are byte-identical; the order-dependent reference CSVs are
  regenerated at Q = 80.
- **Sampler:** adapt_delta 0.999. Four chains (IDs 1–4, original starts),
  2,000 warmup plus exactly 6,000 retained draws each. Everything else is
  unchanged: a = 0.2, diag_e, depth 12, initial step 0.01, seed 77017,
  solver settings and guards.
- **Binary:** the verified v6d instrumented binary (5e9842cb…) is reused;
  because Q is data, it is not recompiled. The cluster job is
  preflight-only (`build.pbs`). It verifies:
  - the v6d build receipt against its pinned hash (15fb01b6…);
  - that the receipt records the same binary, `binary_instrumented=yes`,
    and this payload's patch and pinned original;
  - that the copied binary matches the receipt.
  It then runs `preflight.sh`: LP/AD at the fixed points against the
  Q = 80 references, the p75/p53 controls, a smoke run, and the two capture
  exercises. Trace-on/off identity is a property of the binary,
  established by its v6d preflight.
- **Resources:**
  - preflight job: 4 CPUs, 8 GiB, 1 h;
  - fit: 4 CPUs, 8 GiB, 6 h runner (6:10 PBS).
  - At most 28.6667 core-hours, leaving at least 3.9489 of the tranche.
- **Not permitted:** restart, extension, seed replacement or a passing
  prefix.

### v6q80: finite bank failed on a reference defect; candidate revised to v6q80t (Codex 76/2107–2111)

- **The failed v6q80 bank** is sealed in three files:
  - `order_preflight_v6q80.json`;
  - `order_reference_diagnosis_v6q80.json`;
  - `order_local_reference_whatif_v6q80.json`.
  Three of Codex's 48 stress states failed (σ = 0.001, log h0 + 10). The
  fixed-innovation reference was resolution-stable but truncated by its
  ±12 box. Q = 64–128 and the mode-centred reference agreed to 1e-10.
  Nothing was staged.
- **Codex's rulings (76/2111):**
  - (a) The reference repair is approved. The local-mode reference becomes
    primary, qualified on resolution (800 → 1,600 intervals) and domain
    (L 12 → 16) for the value and every axis, with explicitly converged
    modes. The fixed-innovation reference is a cross-check only once it
    qualifies on resolution (1,600 → 3,200) *and* domain (±12 → ±24).
    Unexplained disagreement is unresolved.
  - (b) The remedy keeps Q = 80 and adapt_delta 0.999, and sets
    **term_buffer = 500** (init_buffer 75, window 25 and total warmup 2,000
    unchanged).
- **Candidate `v6q80t`, payload `payload_v6q80t/`.** Data are identical to
  v6q80. term_buffer is bound in run.env, the runner command (which refuses
  if it is missing), the receipt settings line, the strict expected header
  and the CSV metadata check. Selftest fixtures check that a wrong or
  omitted value fails qualification. Old runs parse with their own
  environment (default 50).
- **Mode convergence, an implementation note for Codex's check.**
  - The first bank under the repaired rule left one state unresolved:
    amended-P11 state 9707, with ρ = 0.99998. My step criterion (a Newton
    step below 1e-14) cannot be met when the pair precision is that
    ill-conditioned; steps stall at 6e-13.
  - The criterion now also accepts a squared Newton decrement g'P⁻¹g ≤
    1e-20. It is affine-invariant in exact arithmetic; the local quadratic
    predicts *half* of it (5e-21) as the remaining log-integrand gain, which
    is not a bound on the integral (corrected per Codex 76/2121).
  - Codex approved the criterion in 76/2121 after independent checks. Its
    requested guards are in `_local_mode`: every iteration rejects a
    non-finite gradient, curvature, step or decrement, and a negative
    decrement, before either stopping test can accept. The 200-iteration
    and positive-definite checks are kept. The selftest's
    `reference_mode_guards` fixture covers the invalid-value cases.
  - That run is kept as `order_preflight_v6q80t_step_criterion.json`.

### v6q80t staging record (21 October 2026)

- **Staged** with `stage.sh 20261021-v6q80t`, with `FIT_SCEN=P11`, after
  Barry opened the jumpbox.
- **Remote:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261021-v6q80t`. Payload
  sha `bb62811b…`; manifest `d4ed5408…` and the CmdStan hash were verified on
  kunanyi.
- **Jobs:**
  - preflight-only build **839387**;
  - the one P11 fit **839388**, `afterok`.
- 4 CPUs and 8 GB each; 1:00:00 and 6:10:00.

### v6q80t result (jobs 839387, 839388, 21 October 2026): fails the frozen screen on divergences

Evidence: `results/P11-v6q80t-20261021/`. It holds receipts, accounting,
the four combined logs and traces (gz), `diagnostics.json`,
`trace_check.json.gz`, `joint_checks.json`, chain-file hashes, and the fetch
archive hash (`e634487e…`).

**Cluster preflight passed.** The reused binary `5e9842cb…` was bound to
the receipt and patch. Passing:
- the LP/AD points;
- the controls;
- the smoke run;
- both capture exercises (12 of 12 events each).

**The fit completed.** All four chains, 2,000 warmup (term_buffer 500) and
6,000 draws each.
- Wall time 2:56:55; chains 9,583–10,612 s.
- The planning projection (1.7–3.1 h) held. The 6-hour cap was not
  approached.
- Qualified, and capture valid in all chains.

**Screen** (frozen; Codex 76/2111):

| Criterion | Result |
| --- | --- |
| Zero post-warmup divergences | **fails: 2 of 24,000** (chain 1 transition 2779; chain 4 transition 2843) |
| No fatal or sampling-phase failures | pass |
| E-BFMI, each chain | pass (0.846–0.884) |
| R-hat, all quantities | pass (max 1.0011, w.12) |
| Bulk and tail ESS, core | pass (minimum σ bulk 4,772) |

- **η:** 90% interval 0.0047–0.5901, which covers the truth 0.2; D and X
  are false; the MCSE target is met.
- **Adapted step sizes:** 0.0325–0.0369. Mean acceptance 0.992–0.995,
  against a target of 0.999. Tree depth ≤ 7, with no depth hits.
- **Comparison:** the amended v6p2 attempt (Q64, 0.995, term_buffer 50)
  had 2 divergences in 32,000 draws. **The remedy did not reduce the
  divergence count.**

**The two divergences, replayed** (`trace_check.json.gz`):
- **Both leapfrogs reproduce exactly:** q and p are identical, and H has a
  relative error of about 1e-16. V and grad V are rechecked at the
  previous and failing states.
- **Both are single-step energy blow-ups.**

| | Chain 1 | Chain 4 |
| --- | --- | --- |
| σ, previous → failing | 2.54 → 12.03 | 3.34 → 1.76 |
| ΔH | 2,676 | 1,761 |
| ΔH with the step halved | 333 and 351 | 104 and 75 |
| Largest momentum changes | κ, σ, log_k | log_k, σ |

  Halving the step still leaves large errors. The stiffness sits in the
  joint σ–(log_k, κ) geometry, not in the lineage frailties.
- **AD against finite differences at the failing states:** scaled errors
  ≤ 4e-8.
- **The Q80 normaliser passes the repaired gate at both failing states.**
  Log errors are 6.7e-11 and 5.0e-11, with both references qualified.
  **Normaliser accuracy is excluded as the cause.**

**Joint-state checks** (`joint_checks.json`): 49 of 49 selected states
pass, with no state unresolved. The maximum log error is 3.9e-6 and the
maximum derivative error 2.3e-5.

**The divergences sit where η's upper tail lives.**
- In the retained draws, corr(σ, η) = 0.645 and corr(σ, log_k) = 0.454.
- P(σ > 2) is 0.37% posterior, against 4.6% prior.
- The 88 draws with σ > 2 have an η median of 0.65 and a q95 of 1.79,
  against 0.11 and 0.59 overall.
- Unreliable exploration of the σ > 2.5 region therefore bears directly on
  the upper η quantile. The zero-divergence screen guards something real.

**Accounting.** (0:00:58 × 4) + (2:56:55 × 4) = 0.064 + 11.794 =
**11.859 core-hours**, within the 28.667 released. The tranche total is now
20.718 + 11.859 = **32.577 of 53.333**, leaving 20.756.

**Disposition, under the agreed stop rules:**
- This attempt **fails**: no retry, extension, seed change or selection of
  a passing prefix.
- **Sampler tuning ends.**
- P06 and the other ten stay held.
- The next step is the simpler-estimator discussion with Codex. Barry
  approved stepping back on 19 October.
