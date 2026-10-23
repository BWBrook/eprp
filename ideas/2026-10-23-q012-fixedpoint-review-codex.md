# Q-012 P11 fixed-point review: complete the bounded check, preserve the target

23 October 2026. Independent Codex review at `2087e13`, including result
commits `6feb3ba` and `b62beaa`, against the
[run-4 decision](2026-10-22-q012-run4-review-codex.md). The review follows
the independent-reviewer skill. Only this note and
`scratch/q012-fixedpoint-review-20261023/` are owned by this review. No
production source, result, shared status or untracked input was changed;
no fit, batch, new reference integration or remote work was run.

The bounded review was performed by a GPT-6.1 Sol subagent and integrated by
parent Codex. Scripts and original JSON receipts are preserved in
[the review archive](../data/q012-pilot/review-fixedpoint-20261023-codex.tar.gz)
(SHA-256 `0b01a273ca5285a53525c27232153abe76302a7fd98e2becd1d91ec9002197df`).
Archive paths restore the scratch directory from the repository root; the
original replay also checks the local, decompressed untracked receipt file.
The committed gzip supplies those bytes in a fresh checkout.

**Recommendation: accept the bounded interior-node/fixed-point check as
complete, with the claim corrections below.** Its declared tasks and
candidate gates pass. This is finite numerical evidence, not a certificate
over the parameter space. The new interior-chain independent reference
qualifies at nine points and remains unresolved at six. The Fisher cost
probe is encouraging and algebraically sound, but currently measures
numerator gradients rather than an assembled fitting target. No estimator
or fit follows automatically from this review.

## Verified receipts and exact scope

The review's [replay](../scratch/q012-fixedpoint-review-20261023/replay.py)
checks the complete expected task-key set and executes the existing assembler
with scratch-only input/output paths. Its reconstructed JSON equals the
saved summary exactly. There are 660 unique receipts: 540 R1-big tasks
(35 plus/minus pairs and one base value at each point), 45 candidate tasks,
45 R2 tasks, 15 R1-chain tasks and 15 identity tasks. No task is missing,
skipped, duplicated or unresolved. All receipts name `Barrys-Mac-mini.local`.
The untracked `p11_fixedpoint_run.jsonl` byte-matches the decompressed
committed archive and was preserved.

| Check, maxima across the frozen bank | Value | Maximum across 35 derivatives |
| --- | ---: | ---: |
| Candidate resolution | 1.33497e-10 | 3.90799e-10 |
| Candidate domain | 2.32490e-11 | 3.19744e-10 |
| R1 big tree | 6.26486e-11 | 2.84217e-10 |
| R1 chain | 7.97478e-11 | 1.42109e-10 |
| Candidate chain vs qualified R2, nine points | 7.97478e-11 | 5.45342e-9 |

I1 reaches 7.99361e-15. I2 reaches 1.12507e-7 against a reference that
qualifies at all fifteen points. The pre-run fixture file records zero
regression difference, I3 at most 5.96515e-9, and a passing combined gate;
these fixture integrals were inspected, not rerun.

The six R2-unresolved states are `stress_s3_r09_kbm15`, `c1_failing`,
`c4_previous`, `holdout_c1f_sigma6`, `holdout_c1f_sigma20` and
`holdout_c4f_sigma15`. All fail the reference's domain-derivative gate
(1.83687e-5 to 1.82284e-2); some also fail its value gate. Candidate-versus-
unqualified-reference discrepancies must not be treated as accuracy
estimates. At sigma15 the latter derivative difference is 0.03276: this
is a visible unresolved comparison, not evidence for a tiny absolute error.

The task wall-time sum is 142,830.3878 s = 39.6751 worker-hours. The
reported 4.97 h elapsed and eight-worker launch are consistent with this
and within the declared allowance, but task receipts contain durations,
not start/end timestamps or per-task source hashes. Thus receipt replay
directly confirms total task duration and completeness; elapsed time,
thread count and the precise executed source version depend on the launch
record and Git provenance. The specification/bank precede the batch in
Git (`eedee55`); subsequent `003b556` changes task ordering and `b64e601`
repairs assembly classification rather than numerical evaluation. There
is no reason to rerun the batch merely to improve provenance packaging.

## Findings and mathematical review

**MAJOR before claiming a fitting gradient: distinguish numerator cost
from the complete target.** `FisherTree.gradient()` returns a tree's log
numerator and its derivative (`fisher_tree.py:75–93`). The check compares
these to `cand.grad`, which likewise contains only per-tree numerator
derivatives (`p11_fixedpoint.py:427–432`). Selection gradients are recorded
separately as `log_pi_grad`; priors are explicitly outside this oracle.
The tested Fisher timing range is 2.07970–2.44821 s for all ten numerator
trees, versus 190.546–252.838 s for their 71-call finite-difference gradient.
It is not yet a measured full conditional-likelihood or posterior gradient.

For likelihood fitting the assembled gradient must be
`sum(tree gradients) - grad(log pi_Q80)`. For same-prior Bayes it must also
include the existing non-frailty priors and unconstrained-coordinate
Jacobians. The Gaussian frailty density is already integrated in each
numerator; adding it again would double count it. There is no evidence of
such double counting in the current probe. Normalizer and prior assembly
is likely cheap, but its correctness and combined timing remain untested.
Label the reported fit-time figures as numerator-based cost arithmetic
with assumed gradient counts. Neither 100–300 optimiser gradients nor
250,000 HMC gradients has been measured in a collapsed fit.

**MINOR: replace absolute-accuracy language with the evidence actually
obtained.** The reported h-squared pattern strongly supports finite-
difference truncation as the leading discrepancy. It does not establish
Fisher error below 1e-9 relative to the exact integral: both derivatives
can share integration bias. Fisher also differentiates the continuous
integral via score expectations; it is not an exact derivative of the
moving-node, finite-table approximation. Their near agreement is a test
of this approximation, not an identity guaranteed for finite grids.

A new, single-CPU local probe, capped externally at 58 s, completed in
31.76 s. At sigma15, big-tree kappa, its signed FD-minus-Fisher gaps are
2.20481025e-5, 5.51192563e-6 and 1.37784589e-6 at h = 2e-4, 1e-4 and
5e-5. Ratios are 4.000073 and 4.000393. Two Richardson extrapolations
agree with Fisher to 1.33e-10 and 1.81e-10. This independently reproduces
the reported leading-error pattern in that coordinate, while retaining
the common-bias limitation. The full signed receipt is in
[fisher_hseries.json](../scratch/q012-fixedpoint-review-20261023/fisher_hseries.json).
No new tensor/adaptive reference was evaluated.

The root score for log sigma, edge scores for log sigma and logit rho,
sigma dependence of `x - sigma²/2`, explicit kappa/kappa_b terms and
coefficient chain rule are algebraically correct. The message-table
derivative `E[partial_parent f] + rho/v Cov(f,x_child)` is also correct;
the explicit-parent terms in `fx` differentiate the Gaussian score.
Coefficient derivatives remain cheap h=1e-6 differences, not analytic AD.
The recorded fifteen-point discrepancy grouping is correct to rounding:
nine points reach at most 6.63377e-7; the other six span 1.18704e-6 to
5.51193e-6. Maximum recorded value difference is 5.68434e-14.

R1 is properly described as **targeted and dependent**. It replaces the
interpolated integrand values recursively while retaining the candidate's
placement, boundaries, nodes and weights (`p11_fixedpoint.py:196–229`).
It isolates interpolation replacement on those grids, including all
thirty-five finite-difference coordinates; it does not independently test
those grids or placement. R2 genuinely changes integration coordinates
and structure, while sharing the local factors. It covers the three-node
chain, not the seven-node tree. The self checks, identities and prior
tiny-forest checks make useful complementary evidence, without creating
a full independent reference for every P11 forest at every point.

The table coverage argument relies on concavity. Exact log messages have
that property, but ordinary cubic Hermite interpolants are not globally
shape constrained. The negative-curvature guard and observed R1/self
checks support the finite bank; the monotonic-range argument is not a
global mathematical certificate for arbitrary future states. Keep
unresolved guards active during any subsequent work.

**MINOR provenance limit:** the committed Fisher JSON stores maxima and
worst coordinates, rather than full Fisher vectors, runtime environment,
source bindings or the original h-series/Apple warning arrays. The new
local receipt repairs one h-series example. It does not reproduce the
Apple Accelerate warning diagnosis; the scoped artifacts are insufficient
to independently confirm the stated finite inputs, loop/einsum agreement
or external-library attribution. Preserve the raw diagnostic receipt if
this claim is retained. This does not invalidate the batch's candidate
receipts or justify another integral campaign.

## Next target and cheapest useful discriminator

**Prefer same-prior collapsed Bayes as the next target-preserving route.**
This changes computation while retaining the existing inferential model.
Pure MML over the present thirty-five coordinates has an exact baseline
ridge: `log_h0[j] = log_h0[j-1] + tau*z_rw[j-1]`
(`payload_v6q80t/model_v6.stan:187–189`). For every positive c,
`tau -> c*tau, z_rw -> z_rw/c` leaves the whole likelihood and selection
normalizer unchanged. The existing z_rw and tau priors break that ridge
(`model_v6.stan:205–207`). Removing them is a different scientific model,
not a cheaper implementation of this one. MML could instead integrate
the baseline effects too or define a reduced baseline, but either needs
an explicit new target contract. MAP is also distinct from MML and from
posterior uncertainty.

The cheapest next discriminator is a **fixed-point full-target bridge**,
before selecting or running a sampler: assemble value and gradient with
the original Q80 denominator, priors and Jacobians; compare against the
archived full numerator FD vectors minus their archived `log_pi_grad`
plus exact prior/Jacobian derivatives, **for all 35 coordinates**. The
minimum useful bank is three points: `central0`, `high_rho_9707` and
`holdout_c4f_sigma15`. Preserve the denominator's separate 35-vector and
measure its fresh cheap FD cost; preserve the prior/Jacobian 35-vector
separately. On these three points, also compare Fisher numerator vectors
at primary, resolution and domain settings, so discretisation sensitivity
is distinguished from the h-squared FD truncation pattern. Add two full-
value directional checks at each point with two step sizes: one direction
in the tau/z_rw block and one spanning sigma/rho/kappa. That is 24 extra
whole-forest values, plus nine Fisher-gradient evaluations and cheap
denominator/prior work, rather than another all-axis integral sweep.

Freeze this bank, maximum calls and a benchmark-based runtime ceiling
before execution. Record full vectors, signed discrepancies, actual
combined cost and environment/source hashes. Apply the existing numerical
tolerances prospectively; do not import the unsupported absolute 1e-9
claim as a new acceptance criterion. This catches sign, coordinate and
omitted-term errors without another 660-task sweep. A cheap coefficient-
level tau/z_rw scaling identity can verify the MML ridge without any
integrals. This is a proposed finite bridge, not work run by this reviewer
and not an optimiser, MCMC or fit contract.

Keep Q80 explicit: I2 deliberately gates against the more accurate local
reference, while the target still divides by Q80. Their largest recorded
value difference is 2.57215e-5. Replacing Q80 would change the target and
require separate qualification, including its derivatives. This review
recommends neither silently replacing it nor treating its error as zero.

Only after the bridge passes should a bounded sampler feasibility screen
be proposed. Fixed-point agreement says nothing yet about trajectories,
mixing, effective sample size, posterior recovery or the necessary gradient
count. Preserve all six new R2-unresolved labels and the historical oracle
labels; no new independent-reference campaign is needed to close this
bounded deliverable.

**Integrated disposition:** accept this bounded check, with the qualifications
above. Claude is next to declare and execute the finite full-target bridge.
Same-prior collapsed Bayes is the preferred route for target continuity; this
does not select a sampler or release a fit. Parent Codex owns the integrated
status and board handoff.

## Evidence pins

SHA-256 at review (full manifest and exact replay in
[replay.json](../scratch/q012-fixedpoint-review-20261023/replay.json)):

- `p11_fixedpoint.py`: `9a8583b2567f699e10efe7996d0ca1c936f666fe63f372b1a49f514e02b5c1dd`
- `p11_fixedpoint_bank.json`: `7a354ac8ec1dbd3282a5a569b272662bff10e3729214398fd15ed093e0dedd58`
- `p11_fixedpoint_run.jsonl.gz`: `9836094ea7f4777152f85aca3b411d20c63f5737deba5d0b6d4a24e6627c3479`
- `p11_fixedpoint_results.json`: `6f50e9e54ae60b09537a1570a4d46d84ca789ef8be65a78ad9f116cabcead028`
- `fisher_tree.py`: `30360faa50bfe31edcad8f7988d5ed62efe2fff42fdfe3b366ad0b47d5174254`
- `fisher_tree_check.json`: `2c871c8f0bead79e05b279261d49665480bb6bd19699cf8d4d74c71faede6cba`
