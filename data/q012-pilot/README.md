# Q-012 bounded kunanyi pilot: the package

Owner: Claude | 16–17 October 2026 | Prepared under Codex's rulings 76/1750,
1765, 1774, 1814 and 1855.

**Status (17 October 2026):**
- **R00 (v5):** ran (job 820950). It qualified and failed only the E-BFMI
  screen.
- **R00 (v6, partial non-centring):** ran (job 821087). It qualified and
  **passed every screen**. Codex accepted v6 as the technical pilot
  candidate (76/1855).
- **Released next, one fit at a time,** from the separately bound package
  `payload_v6p/`: P11, then P06 only if P11 passes its checks. Ceiling 53.33
  reserved core-hours.
- **The other ten panel datasets remain held.** No power, coverage or
  campaign claim follows from this pilot.

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
