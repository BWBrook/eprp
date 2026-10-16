# Q-012 bounded kunanyi pilot: the package

Owner: Claude | 16 October 2026 | Prepared under Codex's ruling 76/1750
([note](../../ideas/2026-10-16-q012-v4-check-and-pilot-codex.md)). **Nothing
has been submitted.** Codex checks this package before Barry opens TPAC.

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

- **Submitted:** build/preflight `820938.kunanyi-ohpc`, then R00
  `820939.kunanyi-ohpc` with `afterok:820938`.
  - Queue `normal`; 1 node, 4 CPUs, 8 GiB, walltime 06:10:00.
  - Mail points `ae` on both.
- **Payload:** manifest 9327b837…, the tarball 67adbed3…, as Codex cleared
  (76/1774). Both tarballs verified by hash on kunanyi before submission.
- **Remote root:** `/u/bwbrook/codex_kunanyi/q012-pilot-20261016-r00`.
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
