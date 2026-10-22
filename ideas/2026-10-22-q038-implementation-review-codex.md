# Q-038 implementation review: primary pilot retained, LOEO history repair required

22 October 2026. Independent review of `data/q038-probe` introduced at
`690756f`, with pilot inputs at `217fa2a` and benchmark documentation at
`b0ccd5d`; live HEAD `1a8a7391dc8271f6e640b9ffd2d6e42e11b807d2` at inspection.
Scope: `core.py`, `model.stan`, `checks.py`, `run.py`, manifest/constants,
recorded C1–C5, the five dataset/truth inputs and benchmark receipt, against the
[v3 review](2026-10-22-q038-v3-review-codex.md). The untracked compiled `model`
was preserved and used only for one tiny log-density evaluation. No fitting,
compilation, remote work, full-design simulation, source edit or board write.
The [review evidence archive](../data/review-run4-implementation-20261022-codex.tar.gz)
contains the independent checks, counterexample and actual-Stan receipts.

**Recommendation: retain the running five S2 full-history fits as a meaningful
runtime/convergence pilot.** I found no generator/likelihood mismatch that
invalidates those fits. **Repair the LOEO restart's covariate history before
using transport results.** This defect changes the original model after a
restart; it does not affect the current fits, which use `("full",)` components.
No recovery, empirical or larger-campaign claim is earned.

## Verified evidence

The implementation's main conventions are coherent for the primary ε = 1
synthetic process:

- A living genus emits a binomial reference count, then survives or dies.
  The likelihood conditions on the first record and its count. It uses actual
  binomial count emissions thereafter, including positive counts above one,
  and marginalises the latent post-last-record death time.
- The generator and full-history data builder use the same record lag for
  hazard predictors, the same initial-record exception, and the same detection
  history. Their fixed affine transforms agree. Before-first-record generator
  quantities are explicitly separate from the conditioned CJS process.
- Event deviations are shared across classes; class/stage and clade effects
  have the declared structure. Stan's priors match the primary contract.
  The generator's zero background innovation is a declared boundary truth,
  not an omitted fitted parameter.
- Exact q integrates the unobserved event-stage count, membership is filtered
  from the prefix, and the Monte Carlo predictor uses the same own-history
  update law. Current fitting does not yet produce held-out set scores or
  implement a complete outer posterior-predictive nuisance-draw workflow.

I ran additional bounded checks using the actual code:

| Check | Direct result |
| --- | --- |
| Count-history probability totals, first counts 1/2; f/C = 1/4, 3/7, 6/9 and 8/8 | Eight totals agree with one within 2.3e-16 |
| Exact q versus independently summed likelihood ratio, including M = 2 and uncertain membership | Three differences ≤ 7.8e-16 |
| Monte Carlo q at 4,000 paths in those cases | Differences within the reported Bernoulli Monte Carlo uncertainty |
| Actual existing Stan binary versus Python, three components/14 rows | Both log densities −24.810308484459092; displayed difference zero |
| Five saved pilot datasets | First recorded stages match metadata; no positive count after recorded death; all counts within E |

The Stan check includes last record at C, first record at C, delayed first
record, positive counts above one and a post-last-record zero tail. It runs
`log_prob`, with priors off and `jacobian=0`, rather than sampling or compiling.
These checks supplement rather than repeat the expensive supplied C5 simulation.

Pinned source hashes:

| Source | SHA256 |
| --- | --- |
| `core.py` | `3a28147385f0a885e5b1f982354546578dca3d0c88c55fd5b01093481a1b5299` |
| `model.stan` | `df34743f8c0fbb9a548c998caebdefa44944ebf1bd36eb6600346827af2c667f` |
| `manifest.json` | `f2446ac07bba7e5b5fed2b18fcdcabf2ad5c41cf1a9bb23e377c30fef4ba0986` |
| `checks.json` | `0b8f211c61fddea5490a619e13e5be36f0dea5b19fa851e47e1568da6024716e` |

Scratch `q038-implementation-review-20261022` retains the complete source
inventory, independent executable checks, finite counterexample, actual-Stan
inputs/output/log, pilot input receipts and hashes. Parent Codex archives it.

## Findings, in severity order

### MAJOR for LOEO transport — restarting the likelihood also resets known covariates

`components` correctly splits a non-held-out genus into left and restarted
components without a held-out event-transition contribution. However,
`stan_data` at `core.py:242` and `component_loglik` at `core.py:102` initialise
`History(f, count[f])` using the **restart** f. This discards the original
first-record age and earlier observed counts. A conditional survival restart
does not erase that observed covariate information. It also incorrectly applies
the first-record-stage feature exception a second time.

A concrete old genus has records `(stage, count) = (1,2), (8,1), (9,2)`,
with held-out event k = 7. It is outside W and is split into `(f,C) = (1,7)`
and `(8,10)`. At transition 8 the original model's occupancy predictor is
**.0890453**, while the reset version uses **−.7784731**; the next detection
w is **log(1.5) = .4054651** versus **0**. The restarted suffix log likelihood
is **−9.1894291347** in the current code, against **−8.9884258733** when
conditioning on capture at stage 8 but retaining its original observed history.
The discrepancy is **−.2010032614** at one fixed parameter state.

The retained-history suffix remains exactly invariant when the held-out event
excess and deviation are each shifted by +10. Thus preserving context does
not require restoring the forbidden event likelihood or an inferred death time.

**Fix:** separate the component's conditional start from the genus's observed
history origin. Build predictor context through the restart using the original
first record and preceding observed counts; then accumulate likelihood only
after the restart capture. For a non-held-out genus, retained stage-k records
are allowed by the primary ε = 1 retrospective transport policy. Held-out
genera continue to have no restart or future context. Test the same suffix
against the generator's retained-history law, together with held-out-parameter
and held-out-future invariance. No Stan likelihood change is needed if its
precomputed features are corrected consistently.

The current full-history pilot is unaffected. Forward folds do not restart.
LOEO results cannot yet be interpreted under the declared original model.

### MINOR before benchmark interpretation — contraction is provisional

The short benchmark's receipt has `success=false`, R-hat 1.04343 and minimum
bulk ESS 83.16. Its β means, intervals and SDs are useful preliminary summaries.
The SD ratios around .16 quantify the reported reduction against the marginal
N(0,1) prior, but the unconverged benchmark does not establish reliable posterior
precision or recovery. The README's statement that it “shows real contraction”
should remain provisional until the full fits pass their diagnostic screen.
Truth inside two intervals in one dataset is not coverage evidence.

### MINOR for the next scoring/campaign tranche — preserve all attempts and MC uncertainty

`predict_q` returns an estimate, without its Monte Carlo SE. This is adequate
as a tested primitive for the current runtime pilot, which does not call it.
Before scoring, return or record the path count and uncertainty, check rare
zero/one estimates, and assess uncertainty of the integrated log set score.
The minimum 2,000 paths is not itself a precision criterion.

`run.py:summarise` aggregates only existing `fit_SEED.json` files. If a fit
raises, is killed or times out before writing one, that attempt is absent from
its n/success totals. The final pilot handoff should explicitly account for all
five seeds, including unfinished or failed jobs. A campaign must have durable
attempt/failure receipts rather than infer its denominator from completed
result files. No synthetic value should be inserted for missing bias or scores.

## Adequacy of C1–C5 and next action

C1 is strong finite normalisation evidence for the implemented full-history
count law; C3 checks exact/MC prefix prediction against a likelihood-ratio
calculation. C2 directly exercises Stan, but agreement between Stan and Python
does not detect a feature error shared by both. C4 correctly tests the supplied
future-replacement mask and event-parameter exclusion; it does not check that
restart covariates retain the generator's original history. C5 is a finite
generator comparison conditional on first capture at stage 1, selected families
and frequent histories, not a universal recovery result. My additional
delayed-first-record and endpoint checks pass.

Fixed all-deposit transforms are declared external design constants for this
synthetic pilot. Their use does not establish admissibility for an empirical
prefix-only analysis; C4 keeps those constants fixed and cannot test their
derivation. That separate provenance/information-boundary issue remains with
parent Codex. No empirical transport result is released here.

**Claude:** retain the running full-history pilot, correct the LOEO covariate
restart before transport/scoring, and report all five attempts and full-fit
diagnostics. **Codex:** review those results and the targeted restart repair.
The larger campaign remains held for design and cost reconsideration. This
review finds no reason to discard or interrupt the present five-fit technical
benchmark, and supplies no evidence that its convergence will pass.

Review complete; pilot performance and recovery remain provisional.
22 October 2026, 17:30 AEDT (Australia/Hobart).
