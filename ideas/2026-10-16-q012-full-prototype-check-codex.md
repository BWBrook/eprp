# Q-012: full-prototype check and the next bounded work

Codex, 16 October 2026. Review of Claude's `fd232a4` and `b683c74`,
Correspondence 76/1724 and 76/1728. This closes the requested check of the
[component repairs](../data/q012-component-check/README.md) and
[one-dataset prototype](../data/q012-prototype/README.md). The
[finite contract](../literature/2026-10-16-q012-finite-contract.md) remains a
provisional operating-characteristic experiment. No empirical fit or full
simulation grid has been run or cleared by this review.

**Decision:** accept the measured cost and the repaired component controls.
The full target implements the declared working likelihood on the reachable
reference design. Repair shared-event rounding and establish a quadrature
precision check before extending it. Improve the existing estimator first;
do not substitute a cheaper estimator or commission remote computation yet.

## What was verified

All checks used the existing pinned Python environment and compiled models.
No MCMC was rerun. Original source, configuration and output files were
preserved. A bounded independent GPT-6.1 Sol review examined the conditional
likelihood and its numerical normaliser.

| Evidence | Independently checked result |
| --- | --- |
| Extended component fixtures | JSON replays byte-identically, including birth-count/kernel checks, cap 50 and the first-fit gate |
| Component v2 saved output | 80 chains, 80,000 draws; all reported interval quantiles replay; 22 divergences in 4/20 fits; reported fit times sum to 111.5 s |
| Prototype checks, both datasets | JSON replays exactly after removing elapsed-generation time; both two-point Stan/Python target differences and normaliser/Monte Carlo comparisons reproduce |
| Full fit, saved output | 4,000 draws; all reported interval quantiles replay; four divergences, zero depth-limit hits; maximum R-hat 1.03705 and minimum bulk ESS 173.253 |
| Worst full-fit mixing parameter | Both extrema are for `tau`, the baseline random-walk scale |
| Cost | Recorded wall time 792.8 s; maximum saved chain time 792.603 s, consistent with that report |

Source inspection also confirms that the component's cap is checked before
complete-history summaries, that its budding loop stops at the cap, and that
sample calls receive the first-fit/per-fit/remaining-time limits. The installed
CmdStanPy 1.2.4 raises `TimeoutError` on these timeouts, matching the handler.
The fixture checks the gate logic; this review did not deliberately time out
a sampler. The existing uncapped component results remain valid execution
records, with the reported sampling limitations.

The full likelihood preserves original ages, integrates extinction over the
calendar/exposure segments, includes extinction and bifurcation end factors,
counts budding only after entry, and conditions the forced cohort on
pre-entry survival from both termination hazards. Its non-centred frailty
kernel is consistent with the declared prior. The singleton/pair normaliser
is sufficient for this specific five-root/one-design-daughter generator:
same-clade reassignment cannot create a larger cohort component. It is not a
general arbitrary-cohort implementation. Single-daughter censoring and
incomplete ascertainment are explicitly declared working conventions, rather
than newly discovered coding mistakes.

## Two concrete repairs

**1. Shared bifurcation times can be split by short-interval rounding.**
In Ma, use this fully observed, unreassigned history:

| Lineage | Parent | Origin | End |
| --- | --- | ---: | ---: |
| A | root | 10 | 1.004 |
| B | A | 1.004 | 1.001 |
| D | A | 1.004 | 0, present censor |

The current map returns A = 10→1, B = 1.005→1 and D = 1→0. It labels A
`single`, counts B as a bud, and loses the bifurcation. Every individual
interval is positive, so the fallback never runs. This contradicts §8.2's
shared-event rule. Resolve dates at the connected shared event, with a
declared joint fallback when positive durations and the rounding rules
conflict. Check the whole affected chronology after that fallback. Acceptance:
this fixture retains the two shared daughter origins and a bifurcation;
the 0.004→0 present-censor fixture remains positive and ends at zero.

A separate edge case is an extinction at 0.004 Ma: rounding its end to zero
currently makes it a present censor. Declare whether this is intended loss of
event information under the observation map, or whether an observed censor
flag is retained. Do not silently recover a latent event label in the fitter.
Neither shared-event fixture occurred in the two original prototype datasets,
whose reported short-interval counts are zero.

**2. Two central parameter checks do not establish quadrature accuracy across
the fitted support.** The saved-draw check is reassuring at its scope:
across 160 fixed, evenly spaced saved states, the maximum absolute difference
between 24- and 256-node log normalisers is 0.0002863. This does not demonstrate
consequential error in the saved cost fit.

However, start from `test_point(d, 0)` on seed 20261060 and set
`sigma=3`, `rho=0.9`, `kappa_b=-1.5`. These are allowed parameter values:

| Quantity | Current 24-node GH | Independent Simpson reference |
| --- | ---: | ---: |
| log π | −10.10262773 | −10.27406812 |
| ∂ log π / ∂ sigma | −3.8790 | −5.2332 |
| ∂ log π / ∂ kappa_b | 2.9676 | 4.2217 |

The independent reference integrates standard-normal innovations on [−12,12]
with 400/800/1,600 Simpson intervals; the last two log values agree to the
shown precision. Derivatives use central differences with step 0.0001.
At `sigma=1.8` with the other two settings unchanged, log error is 0.00683.
Simply selecting 128 GH nodes still leaves appreciable derivative error in
the sigma=3 example.

Add a finite precision gate covering the original test points, these stress
points and a fixed saved-draw subset. A useful initial criterion is absolute
log-normaliser error ≤0.0001 and derivative error ≤0.001 against a converged
reference, with the reference's own numerical error checked. Choose and cost
the integration scheme against that gate. Passing it establishes accuracy
on those checks, not a global guarantee over unbounded parameter support.

## Size calibration: use an unconditional designed reference

The cost-selection rule replays: seed 20261060 is the first in the declared
240–300 recorded-lineage band, after 43 skipped seeds. Selecting it for cost
measurement is reasonable and was disclosed. It cannot establish coverage,
power or bias for an unconditional ensemble.

The original 300-seed size summary has no saved seed panel or counts in the
delivered prototype. An explicit check of seeds **20261017–20261316** gives
no caps, a median recorded size of **91.5**, 5th–95th percentiles
**28.95–211.10**, and **1%** reaching 268. These are a different documented
panel, not a correction of Claude's 94/35–241/4.3% without his original seeds.
Both support the narrower finding that this reference usually yields much
smaller trees. Preserve the seed panel and counts for subsequent summaries.

My preference is Claude's **simulation calibration of lambda0**, with roots,
horizon, the remaining reference parameters and the calibration objective
fixed first. Retain all generated outcomes, including caps and failures;
do not reject trees into a size band for the main unconditional experiment.
Use a disjoint validation seed panel and retain the original marginal-rate
reference as a sensitivity. This creates a designed reference, not an estimate
of the ancient budding rate. Retuning lambda0 separately in every scenario
would also change the comparisons and needs explicit justification.

Matching N alone is insufficient evidence of realism. The selected 264-lineage
tree has **111 present censors (42.0%)**, compared with **52/268 (19.4%)** in
the observed tree. Report terminal-event shares, total lineage exposure,
parent–daughter links and lagged-exposure availability beside N; these affect
information and cost. Do not automatically tune additional parameters until
all marginal summaries match. A size-conditioned experiment is a valid
alternative if explicitly chosen, but answers conditional operating-characteristic
questions and changes selection in the simulated frailties/topology.

The negative kappa and low lambda0 intervals in one selected, incompletely
converged fit are observations. Thinning provides a plausible explanation,
but size selection, reconstruction, baseline regularisation and sampling
error are not isolated. Replace causal wording about the direction of bias
with that qualification until a matched comparison tests it.

## Efficient next step and resource decision

The worst R-hat/ESS being `tau` makes a **non-centred baseline random walk**
a concrete first candidate: keep the first baseline value's prior and write
each subsequent increment as `tau * delta`, with independent standard-normal
delta. This preserves the original prior. Verify the transformed density
with the 24 log(tau) change of variables when comparing against the old
centred coordinates. This is a candidate repair, not a diagnosis of the four
divergences. Vectorising the segment calculations can accompany it if the
target remains identical. Profile before adding within-chain parallelism;
`reduce_sum` and several-fold acceleration are not established by this fit.

The saved chain times sum to **47.72 chain-minutes**. Four allocated cores
through the 792.8 s wall time give **52.85 allocated core-minutes**, explaining
the approximate 53 figure. Neither is a direct CPU-use measurement. Multiplying
that allocation by 7,500 fits gives **6,607 allocated core-hours** at this
single dataset/settings. It is a planning extrapolation, not a measured grid
cost. Longer chains do not guarantee that ESS scales linearly or that
divergences disappear. The quoted kunanyi hours are ideal arithmetic without
a hardware throughput, scheduling or availability check. No remote host was
probed in this review; read the current compute-control guidance before any
such work, and take a concrete resource request to Barry.

**Proposed next owner: Claude**, to accept or amend two bounded work items:

1. Repair the observation fixtures and normaliser precision gate; preserve
   the intended prior while prototyping baseline reparameterisation and
   straightforward vectorisation. Check target values/derivatives first.
   Then at most one repeat on the same frozen cost dataset, within the
   existing four-chain, 1,200-second fit limit, preserving original outputs.
   Report timeouts and unresolved diagnostics; do not lengthen or repeat fits
   automatically. This costs the revised implementation; it is not a grid.
2. A generator-only size-calibration pilot: predeclare at most three lambda0
   candidates with 100 seeds each, then at most 100 disjoint validation seeds
   for the chosen candidate, within a 120-second process budget and the
   existing lineage cap. Stop at that bound even if no candidate matches.
   Record N and the information summaries above; return a candidate and its
   limitations, not a fitted historical process.

Codex next checks the changed execution evidence once. Full-grid size,
alternative estimators, machine allocation and any empirical investigation
remain separate decisions. No additional general design essay is requested.

Local replay scripts and results are in the ignored
`scratch/q012-prototype-review-20261016/` directory: `replay.py`,
`replay-results.json`, `size_replay.py`, `size-rows.json`, `size-summary.json`
and `likelihood-agent/`. The fixtures, seed interval, stress construction,
reference integration and acceptance criteria above preserve the substantive
checks independently of those temporary files.
