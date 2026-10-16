# Q-012 pilot: prelaunch package check

Codex | 16 October 2026 | Reviewed `a47eabe`, following seed freeze
`c93ea58` and Claude's evidence in 76/1758. Barry requested cross-checks
before opening the jumpbox. Claude owns implementation; this review changes
only the review record and STATUS.

**Ruling: hold TPAC opening for bounded package repairs.** The current
datasets and checked numerical results reproduce. The remaining problems
are failed-run qualification, incomplete source/build binding, and job
failure handling. No new long laptop fit is needed to resolve them.

## Findings requiring repair

### 1. Major: screening can pass failed, mismatched or incomplete output

In [pilot.py](../data/q012-pilot/pilot.py), lines 344–382 at the reviewed
commit, CSVs and stdout files are paired with `zip`; all CSVs then enter
the statistical calculations. Receipts, exit files, stderr, scenario
identity, hashes, sampler settings and expected draw counts are not checked.
Unequal chains are silently truncated to the shortest length.

Executed isolated fixtures returned `screening_pass=true` for each of:

- No receipt and 2,000 retained draws per chain instead of the declared 4,000.
- A failed P12 receipt presented as R00, stale hashes, a nonzero chain exit
  and a fatal message in stderr.
- Unequal retained chain lengths, with the shortest only 1,500 draws.
- Five CSVs and four stdout files, with a divergence in the fifth CSV.
  Its draws entered R-hat/ESS while its divergence escaped the chain checks.

Require exactly the declared chain IDs and matching files; a successful
receipt for the same scenario, attempt, payload, binary and settings; zero
chain exits; the expected equal retained draw counts; and inspection of
both output streams. Verify the CSV metadata against the declared settings
where it supplies independent evidence. Malformed or inconsistent output
must remain unresolved/failed, even if its numerical diagnostics look good.
Retain any historical-summary mode separately from pilot qualification.

The finite-value guards also need repair. NaN R-hat and NaN ESS already
fail, but fault-injected positive-infinite ESS passes. A fault-injected
NaN upper-endpoint MCSE produces `mcse_target_met=true` through
`max(finite, NaN)` and marks numerical uncertainty false. These are guard
tests, not observed ArviZ failures. Require finite diagnostics/endpoints
and finite, nonnegative MCSE; unavailable MCSE leaves endpoint precision
unresolved. Preserve raw D/X flags separately when their endpoints exist.

### 2. Major: two links in the provenance checks are missing

**Saved states.** [prototype.py](../data/q012-prototype/prototype.py),
lines 579–590, omits the saved CSV banks consumed by the old saved-state
checks, v4 tail selection, benchmarking and saved v3 probes. In an isolated
copy, changing the maximum-sigma v4 state from 2.9932533 to 3.0932533
changed the selected preflight point while `binding(d)` remained unchanged
and matched the archived checks. Bind every consumed bank, or consume
immutable extracted fixtures whose contents and selection are themselves
bound. A source hash recorded in a fixture is insufficient if the next
stage reads a different unverified source file.

**Built binary.** [fit.sh](../data/q012-pilot/payload/pbs/fit.sh), lines
23–30, verifies the current manifest and recorded binary hash, but ignores
the build receipt's `manifest_sha256`. A fixture with a mismatched build
manifest was accepted and completed. Require the build receipt's manifest
to equal the current manifest before execution or resume/skip.

These tests demonstrate gaps in refusal logic, not corruption of the
present payload: its recorded current hashes and all 79 manifest entries
verify. Refresh affected check/manifest receipts after the repairs and
prove that modifying each relevant input invalidates the correct stage.

### 3. Major: the first build/replay failure path is incomplete

- **Runtime environment:** the build loads the declared GCC module, but
  [fit.pbs](../data/q012-pilot/payload/pbs/fit.pbs) and `fit.sh` do not.
  Preflight therefore exercises a different environment from the replay.
  Load the same module for the fit and fail explicitly if it is unavailable.
  A missing/incompatible dynamic-library failure is a conditional risk;
  it has not been observed on kunanyi because no remote job was run.
- **Notification:** [build.pbs](../data/q012-pilot/payload/pbs/build.pbs)
  requests only `-m a`. PBS distinguishes an abort by the batch system from
  a job ending; an ordinary nonzero build-script exit does not reliably
  trigger abort mail. With the replay blocked by `afterok`, the agreed
  mail-driven wake can be missed. Use `-m ae` for the build too. This follows
  the documented mail-point distinction in the
  [PBS Professional User's Guide, section 2.5.1.1](https://2021.help.altair.com/2021.1/PBSProfessional/PBSUserGuide2021.1.pdf)
  (primary documentation inspected 16 October 2026); actual site delivery
  remains a runtime check.
- **Retrieval:** [fetch.sh](../data/q012-pilot/fetch.sh), lines 24–25,
  requires `runs/R00` in both tar attempts. A failed build can leave that
  directory absent because R00 never starts. The exact archive commands
  then return exit 2. Archive the existing evidence paths, retaining build
  logs, receipts and accounting even when no run directory exists. Test
  this earliest failure case locally.

### 4. Moderate: interruption can leave the model running

`fit.sh`, lines 77–83, kills by a command-line regular expression, waits
two seconds and writes a termination receipt without checking descendants.
A TERM-ignoring fixture left both its model and timeout process alive
after `terminated_TERM` was recorded; the timing wrapper had exited 143.
Track the launched processes/groups, use bounded TERM/KILL escalation,
and wait for their termination before completing the receipt. Test a
TERM-ignoring child, not only the cooperative success case. The review
fixture descendants were explicitly cleaned up.

## Evidence that passes, and accepted amendments

- All 13 datasets regenerate exactly from the frozen table, and all 52
  starts match the frozen prior-centred rule. R00 retains 264 lineages;
  panel sizes are 71, 83, 82, 45, 49, 84, 385, 315, 556, 75, 19 and 649.
  The small P11 remains in the panel; seeds are not replaced.
- The archived Codex fixtures match the previous independent outputs.
  The eight selected tail states and 40 evenly spaced v4 states match the
  saved CSVs. Recomputing the latter gate reproduces the reported maxima:
  log error 3.53058e-7 and largest derivative error 7.12855e-7.
- All 200 archived probe stdout records reproduce the recorded outcomes.
  The old gates, actual AD and tight-tolerance evidence remain the existing
  checks; this review did not rerun every numerical check or any MCMC.
- Amendment 2 correctly restricts nominal equal-tail coverage to interior
  eta, retaining raw structurally zero boundary coverage and existing D/X
  endpoints. No prior change is required.
- Claude's E-BFMI correction is accepted. CmdStan's sample-variance
  convention gives 0.27736, 0.25790, 0.32371 and 0.32542 for v4; the earlier
  Codex population-variance values were higher by 1000/999. Two chains
  remain below 0.3, so the previous sampling ruling is unchanged.
- Accept the declared 300 s local and 600 s cluster smoke limits, preserving
  the failed 60 s record. Accept a six-hour cap for the first technical
  replay: the increased node count and sampling length justify headroom,
  while kunanyi throughput remains unmeasured. The 312 core-hour fit ceiling
  covers all 13 proposed fits; it is not a measured cost or a release of
  the 12-fit panel. Reconsider panel resources from the actual R00 evidence.

Shell syntax and ShellCheck error-level checks pass. The CmdStan make
target is valid. These checks do not cover the control failures above.
No compilation, MCMC, SSH, submission or background monitoring occurred.

## Closure and next owner

Claude should repair these bounded controls, preserve the numerical/source
evidence, refresh affected bindings and demonstrate refusal/cleanup on the
listed cheap fixtures. Codex then checks that patch before Barry opens TPAC.
The next remote tranche remains build/preflight plus R00 only. The panel
requires the separate review of R00's receipts, diagnostics, endpoint MCSE
and measured resources already specified in the package.

Generation outcomes and run attempts are retained, but the all-attempt
denominator and `[s/n, (s+u)/n]` remain a reporting contract, not an implemented
aggregation command. This is work for panel reporting, not an extra R00
launch blocker. No power, coverage or empirical-inference claim follows
from the present numerical package.

Local review evidence: `scratch/q012-pilot-review-20261016/`, including
`numerical_replay.py` and `numerical-replay.json`; the `pbs-agent/` control
and fetch fixtures; and the `screen-agent/` screening, nonfinite and
binding fixtures. Two bounded GPT-6.1 Sol reviews covered independent
PBS and screening/provenance scopes; Codex integrated their evidence.
