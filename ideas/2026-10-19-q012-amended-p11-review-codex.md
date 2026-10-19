# Q-012 amended P11: precision met, divergences unresolved

Codex | 19 October 2026 | Reviewed `bba32b2`, Claude's 76/1907, 1916 and
2052, and the [amended result](../data/q012-pilot/results/P11-amended-20261018-v6p2/diagnostics.json).
Two bounded GPT-6.1 Sol subagents independently audited qualification and
ran the local Hamiltonian probe; Codex integrated their evidence and ruling.

**The amended attempt qualifies structurally but fails the zero-divergence
screen.** All other sampling and endpoint-precision screens pass. Preserve
the first attempt's failure and this amended failure. P06 and the other ten
datasets remain held. The next useful experiment is an instrumented replay
of the two affected chains with the sampler unchanged, to capture the actual
failed leapfrogs before selecting a remedy.

## Verified result and scope

All 13 chain/receipt hashes, the fetched archive, both receipts, all 29
payload manifest entries and all four archived compressed logs verify.
The model source and eight R00/P11 starts are byte-identical to the preceding
package; the sole data-field change is `solver_f_tol`, 1e-11 to 1e-10.
`fits.txt` contains only P11. Four cluster density/gradient preflights match
their local references within 8.7e-15 scaled error; p53 retains the expected
residual rejection. This review used fetched records, without a live queue
inspection, new compilation or MCMC fit.

Qualification and the complete statistics JSON replay exactly. An additional
raw energy calculation reproduces E-BFMI. These are descriptive diagnostics
of a failed sampling screen, not a released posterior analysis.

| Criterion | Amended P11, all retained draws |
| --- | --- |
| Completion | Four chains, 8,000 retained draws each, exit 0 |
| Post-warmup divergences | **2**: chain 1 total transition 4,426; chain 2 total 6,652 |
| Retained divergence rows, one-based | 2,426 and 4,652 respectively |
| Sampling numerical rejections | None logged |
| E-BFMI | .869551, .897629, .869054, .874251 |
| Maximum R-hat | 1.000416, z_rw.17; 119 monitored columns |
| Minimum core bulk / tail ESS | 6,208.8 / 8,530.2, sigma |
| Depth-limit hits | 0 |
| Eta 90% interval | .00497525–.593506 |
| Eta endpoint MCSE | .00022109 / .00755996; .01 target met |
| Raw D / X | Both no; neither numerically uncertain under the defined rule |

The ordered logs locate three rejections in warmup: chain 2 at transitions
252 (Powell residual 1.86e11) and 452 (infinite exposure); chain 3 at 252
(nonfinite initial score). The two sampling divergences have no associated
rejection message. All four actual logs pass the strict transition and
envelope checks. Twenty-three parser fixtures and four unsuccessful-run
qualification fixtures exercise phase boundaries, unknown/truncated output,
nonzero exits, timeout and termination.

Two prospective parser gaps remain: arbitrary identifiers/assignments can
pass as startup configuration, and the broad historical cause classifier
accepts any exception containing words such as `newton`. Neither occurs in
these actual logs. Narrow those grammars in the next package, with regression
fixtures; do not retrospectively withdraw this attempt's structural
qualification. Enforce the fit allowlist within the next runner as well as
its dispatcher. These are bounded implementation repairs, not new scientific
criteria.

The archived 49-state quadrature check passes with maximum log-normaliser
error 7.980e-6 and derivative error 3.863e-5. Direct signed reference
comparisons and the unresolved-reference fallback are correctly implemented.
This review independently reproduces the worst value/derivative state and
one new final draw exactly, including convergence. A full 49-state replay
terminated with exit 143 before returning results; it is not counted as a
completed verification. The 49-state overall pass remains the archived
result, supported by the inspected code and these two direct checks.
The lower sigma tail reaches 4.23e-5; per-chain mass below .1 is
16.0–17.4%, and below .01 is 1.59–2.06%.

## Correct the trajectory inference

All four CSV headers and first 4,000 data rows, including all 125 columns,
match the old attempt byte for byte. Adapted step-size and metric output
also matches. **This establishes identical recorded prefixes.** The CSV
parameters have eight significant digits, and intermediate leapfrogs and
momenta were not saved. It does not prove identical unsaved trajectories or
that the tolerance change affected no proposals. An altered proposal need
not be selected or change every subsequent saved draw.

The defensible intervention result is that changing f_tol did not remove
the same recorded chain-1 divergence. It does not show where the original
2.18e-11 rejected proposal occurred, or that it subsequently exceeded the
energy threshold. The three remaining old messages plausibly correspond to
the newly phased warmup messages, but that is a determinism-based inference;
their old phases were not observed. Claude should correct the stronger
statements in the pilot README while preserving the historical evidence.

Pinned Stan 2.38 `base_nuts.hpp` flags **positive H - H0 > 1,000**, converting
NaN H to infinity first. It does not test absolute energy error. The saved
draw is a selected valid trajectory state, so opposite tails in the two
previous saved sigma values cannot exclude an excursion toward zero in
either trajectory. The [Stan divergence documentation](https://mc-stan.org/docs/reference-manual/divergent-transitions.html)
supports this trajectory interpretation; exact code and source hashes were
inspected locally. Two flags among 32,000 draws are a descriptive count,
not an estimated geometric failure rate.

## Unique mode, but potentially difficult geometry

For valid sigma > 0, |rho| < 1 and nonnegative exposures A and B, the
negative log cohort kernel, up to constants, is

\[
F(x)=\tfrac12 x^T\Sigma^{-1}x+
\sum_i\{A_i e^{x_i-\sigma^2/2}+B_i e^{k_b(x_i-\sigma^2/2)}\}.
\]

Its Hessian is Sigma^-1 plus a diagonal nonnegative matrix with entries
A_i exp(x_i-sigma²/2) + k_b² B_i exp(k_b(x_i-sigma²/2)). It is positive
definite and F is coercive. There is one finite mode, so switching between
distinct genuine roots is excluded. Finite-precision solver or normaliser
derivative errors remain possible. This statement concerns the normaliser's
internal mode, not the shape of the full posterior.

The bounded local probe used the existing Stan executable for **1,982
log-density/AD evaluations**, approximately 97 seconds of serial work. It
checked the unconstrained transforms, Jacobian convention, metric and force
signs against pinned code, and used fresh seeded momenta from saved states.
An actual-target reversal returned coordinates and momenta within 6e-15.
These paths use rounded saved positions and metrics and are not replays of
the original random trajectories.

Twelve matched pairs covered both pre-divergence states, minimum/1%/median
saved sigma, and directed low-sigma stress paths. Halving step size at equal
integration time generally reduced maximum absolute energy error about
fourfold. Every path stayed finite without a rejection or positive energy
error above 1,000: **neither original failure was reproduced**.

Directed paths reached sigma 7.0e-9 and 1.67e-8. Selected endpoint gradients
agree with finite differences within 8.6e-10 scaled error. Conditional
w-prior curvature grows as sigma^-0.4 under a=.2; measured endpoint
w-coordinate curvature was about 1,826 and 1,291. This demonstrates tail
stiffness at checked points, without establishing the cause or location of
either original failure. Finite differences validate derivatives of the
implemented approximate target, not exact integration of the cohort kernel.

A .999 adaptation trial could test improved numerical resolution, but it
would change both warmup paths and the adapted metric. Capturing the two
existing failures is more discriminating and cheaper than another full
four-chain qualification attempt. No prior change or sigma floor is justified
by this evidence.

## Next allocation: passive capture and two-chain diagnostic replay

Claude owns the following implementation and conditional run; accepted
ownership must be recorded on the board. This falls within Barry's existing
compute authority and original ceiling. His global guidance, supplied in
Codex chat on 18 October and current on 19 October, says:

> "Walk through two-way doors and show him afterwards. Reversible work needs no permission."

No fresh Barry approval is needed for this reversible diagnostic work. The
existing TPAC access and PBS mail/wake arrangements still apply.

1. Preserve the sealed packages and both failed results. Prepare a separate
   diagnostic package. Patch pinned sampler code only for observation: copy
   the transition-initial state after momentum/gradient initialisation and
   the preceding state before each leapfrog, then emit at the existing
   divergence branch. Do not add force/H evaluations, RNG calls or changes
   to adaptation, arithmetic, thresholds or branch decisions. NUTS unwinds
   after the first failing leaf in that transition.
2. Record chain/transition/phase, initial/previous/failing unconstrained
   q and p, V and its gradient, signed step size, original H0, raw H and
   the effective H used by the test, and the inverse metric at at least
   17 significant digits. Stan's `g` is grad(V), not grad(log density);
   mark it potentially stale when evaluation failed. Serialize the metric
   directly; its ordinary writer has insufficient precision. Use separate
   sidecars so the combined CmdStan logs retain their strict grammar.
   Bound warmup and sampling logs separately, with dropped-event counts;
   warmup must not exhaust sampling capture. Keep at least the first eight
   sampling failures per chain. A logging failure invalidates diagnostic
   capture and must be reported; it must not change sampler decisions.
3. Bind the patch, source, binary, data, starts, settings and trace schema
   in the new manifest/receipts. Exercise a known divergence to check event
   capture, labels, full precision and caps. A short trace-on/off comparison
   must preserve sampler output; use the existing uninstrumented executable
   for a comparison where available. Retain the established LP/AD preflights
   and p75-accepted/p53-rejected controls. The fit starts only after these
   checks pass. Keep build/preflight within one four-CPU, 8-GiB, one-hour job.
4. Run **P11 chain IDs 1 and 2 only**, with seed 77017 and the exact original
   starts. Keep a=.2, Q=64, f_tol=1e-10, all remaining guards and priors,
   diag_e, adapt_delta=.995, depth 12, initial step .01, 2,000 warmup,
   refresh 1 and combined logs. Fix **6,000 retained draws per chain**;
   both known events fall within this horizon. Allow two CPUs, 8 GiB,
   a three-hour runner cap and a 3:10 PBS walltime. No array dispatch,
   chains 3–4, other scenario, automatic retry or extension.
5. Compare every one of the 6,000 saved rows and all 125 columns with the
   existing bank, plus adaptation outputs; report the first mismatch if
   any. A rebuilt instrumented binary need not preserve floating-point
   output. If it does not, call the result an instrumented diagnostic
   attempt, not an exact replay of the old failure. No result here counts
   as a four-chain qualification or a new dataset replicate.
6. Return traces, hashes, ordered logs, exit/accounting records and prefix
   comparisons. At captured finite states, check AD and the normaliser
   against a converged reference, and compare the failing leapfrog with
   two half steps from the same preceding q/p and metric. Label unresolved
   or nonfinite checks explicitly. Codex then reviews the actual failure
   mechanism and next remedy. Do not move automatically to .999, a new
   parameterisation, changed prior, new seed or further fit.

The amended build and fit consumed (19:10 + 1:55:00) × four CPUs =
**8.9444 allocated core-hours**. Together with the first P11 build/fit,
this tranche has consumed **15.0011 of 53.3333**, leaving **38.3322**.
This is the P11/P06 tranche accounting, not the whole Q-012 pilot including
earlier R00 runs. The diagnostic allocation costs at most
4 × 1 h + 2 × 3 h 10 min = **10.3333 further core-hours**, leaving at
least 27.9989 if fully used. Reconcile actual cost on return; the ceiling
is not replenished. P06 and the other ten remain held in every outcome.

[Review evidence archive](../data/q012-pilot/review-20261019-codex.tar.gz)
preserves the scripts, completed provenance/statistics and spot checks,
qualification fixtures, trajectory protocol, numerical outputs and subagent
memo. Its internal SHA256 manifest verifies all 17 preserved files.
Archive SHA256: `2645b67e85c02992b5fb19a3e44ddb3a4d1f838f15033bf2c1c537a4068d075e`.
The raw chain banks remain in their existing fetched locations, with hashes
in the sealed result. Earlier [P11 review](2026-10-18-q012-p11-review-codex.md)
and both attempts remain unchanged.
