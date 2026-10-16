# Q-012 pilot patch: clearance for build and R00

Codex | 16 October 2026 | Reviewed `0df3504`, Claude's reply 76/1771,
and the [prelaunch findings](2026-10-16-q012-pilot-prelaunch-check-codex.md).

**GO for build/preflight plus the R00 technical replay once Barry opens
TPAC.** The execution blockers are closed. Two remaining offline diagnostic
guards, specified below, must be corrected before qualifying R00's results;
they do not affect the frozen remote payload or justify delaying this first
run. Claude owns staging, execution and those small corrections. The panel
still requires a separate review of the actual R00 evidence.

## What was independently checked

| Previous problem | Patch evidence and result |
| --- | --- |
| Stale build could accompany a new manifest | A mismatched build receipt now refuses with exit 2 before an attempt starts. Current payload and binary checks precede resume/skip too |
| Runtime module missing from fit job | Mocked module-load failure refuses; a successful load reaches all four fixture chains. The runner separately rejects an unloaded declared module |
| Interrupted model could survive | Cooperative TERM stops all four fixture models. Four TERM-ignoring models force KILL escalation after five seconds; no survivors remain when the termination receipt is written |
| Failed build could not be fetched | The actual `pack.sh` succeeds with no run directory and includes the failed build receipt, log, PBS output and manifest |
| Build failure could miss the mail wake | Build and fit now request `ae` mail. Actual site delivery remains a first-window runtime check |
| Screening accepted structurally invalid output | Eleven independent negative fixtures now return unqualified/unresolved, with no screening pass: missing/failed/wrong-scenario/stale receipts, extra CSV, missing stdout, failed exit, stderr, wrong CSV metadata, short chain and wrong init |
| Nonfinite MCSE/ESS could pass | NaN/infinite R-hat and ESS fail; NaN MCSE leaves precision unresolved and retains finite raw endpoint flags. A separate nonfinite-endpoint case remains below |
| Saved-state inputs were not bound | All 16 consumed CSV files across four banks are now hashed. Modifying, removing or adding a file in each bank independently invalidates the binding |

Completion, resume/skip and timeout also pass the independent runner
fixtures: resume creates no second attempt, and four chain exits of 124
produce runner timeout exit 4.

The copied **stage → build → preflight → fit → pack → fetch** scripts pass
a local control-path test using transport, scheduler, build and model
stubs. Submission arguments name only the build and R00 with `afterok`.
Fetched evidence includes both receipts and preflight output. This exercises
the script integration; it is not a cluster build or a numerical fit.

A separate actual `pack.sh`/extraction/default-`diagnose` test succeeds with
the expected fetched directory layout, genuine CmdStan header format and
synthetic 4,000-draw chains. Archived real runner CSVs also qualify against
their matching fixture settings. Historical v4 output remains explicitly
labelled as a summary, and still fails the sampling screen.

## Numerical evidence and payload identity

The model, quadrature implementation, configuration, seed table, all 13
datasets and all 52 starts are unchanged from the checked package. The
three preflight reference CSVs have identical numerical content; their
timestamp comments changed. The refreshed checks differ only in bindings
and timing measurements, not in numerical gate or probe outcomes.

All 80 payload manifest entries verify. The checks-file hash, recorded
binding and current binding agree. The current payload manifest SHA-256 is:

```text
9327b837e8caa58b3548b7e4631556c385e8b652a50b898170f0f0eb6eb128ad
```

The archived refreshed smoke run contains exactly four completed chains,
one retained draw each, and no fatal error or rejection. All 200 archived
probe stdout records reproduce their classifications. The output-directory
repair preserves previous smoke output under a superseded name; no mixing
of old and new chains was found in the refreshed record.

Shell syntax, ShellCheck error-level checks and patch whitespace checks
pass. This review ran no real MCMC, compilation, SSH or submission.

## Two offline corrections before result qualification

1. **Require a valid binary hash, not just equality of missing values.**
   In [pilot.py](../data/q012-pilot/pilot.py), lines 248–250 at `0df3504`,
   removing `binary_sha256` from both the build and attempt receipts makes
   `None == None` pass. The healthy synthetic fixture then qualifies and
   screens successfully. Require a nonempty 64-character hexadecimal hash
   in the build receipt, then require the attempt's value to match it.
   Add the missing-both case to the negative fixtures.
2. **Require finite endpoints before declaring endpoint precision met.**
   At lines 318–321, `eta_block(nan, .4, .003, .01, .2)` correctly leaves
   D/X unresolved but incorrectly returns `mcse_target_met=true`. Include
   endpoint validity in that condition, and test the precision result as
   well as D/X. Preserve unresolved precision when either endpoint or MCSE
   is unavailable.

These are real guard defects, but neither was reproduced on the successful
execution path: the build and runner emit binary hashes and refuse missing
or mismatched binaries; the endpoint example is an injected diagnostic
input. Both corrections belong to local post-processing. They require
small fixture checks, not another model build, payload regeneration or fit.
Their closure is due with the R00 diagnostic handoff, before any panel
promotion.

## Next action and limits

Barry can open the jumpbox for Claude to stage the frozen payload and submit
the one-hour build/preflight job plus R00: four single-threaded chains,
2,000 warmup and 4,000 retained iterations each, 64 nodes, six-hour fit cap,
four CPUs and 8 GiB. Retain the declared settings and no-retry policy.

The first cluster build establishes module/library compatibility and the
numerical preflight on kunanyi. Scheduling, mail delivery, elapsed time,
peak memory and sampling quality are not yet observed there. Barry's PBS
mail/wake workflow remains in force, with no background monitor. After the
wake, Claude fetches receipts, raw output and accounting; Codex checks the
actual R00 diagnostics, endpoint precision and cost before the 12-fit panel
is considered. No campaign or empirical-inference clearance is implied.

Evidence is in `scratch/q012-pilot-patch-review-20261016/`:
`binding_evidence.py`/`binding-evidence.json`, `pbs-agent/` runner and
transport-flow fixtures, and `screen-agent/` qualification/statistics
fixtures. Two bounded GPT-6.1 Sol reviews covered the independent PBS and
screening scopes; Codex integrated them with the source/binding checks.
