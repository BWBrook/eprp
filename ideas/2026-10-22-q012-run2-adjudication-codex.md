# Q-012 oracle run 2: repair the reference, retain the failed screen

Codex | 22 October 2026 | Result pinned to
`89308904c1acffc63253e3b48a034d4a2c71b6da`; numerical implementation
`8962871`. This follows the [earlier oracle review](2026-10-22-q012-oracle-review-codex.md)
and Claude's handoff in 76/2186. The pool-only change at `a9419ee` does not
change the integrands or numerical rules.

**Decision: proceed with one bounded reference-only repair.** Keep the
evaluator algorithm and target unchanged. The evidence supports this next
step; it does not yet support accepting the oracle or starting the P11
evaluator. No estimator or fit is selected. Preserve the original result:
**33 pass, 4 fail, 8 reference-unresolved** under the frozen rules.

## What the new evidence establishes

The [result JSON](../data/q012-pilot/collapsed_oracle_results_run2.json)
recounts exactly. All 45 evaluator resolution/domain checks pass: maximum
value change **3.55e-15**, maximum derivative change **1.421e-10**. The
decomposition and unit identities pass. All twelve nonpassing rows have
an unqualified tensor reference; five also exceed the derivative accuracy
gate against that reference. Those comparisons cannot locate the error
in the evaluator. Conversely, evaluator self-convergence alone cannot
establish its accuracy. Replace “the repairs fixed the evaluator” with
“the repairs fixed its observed self-convergence failures; the remaining
accuracy checks are unresolved.”

The six affected states are below, in **both T2 and T3**. They are not all
states with sigma at least three: the high-rho hold-outs pass the existing
screen.

| State | Frozen outcome, T2 and T3 | Additional issue |
| --- | --- | --- |
| `stress_s3_r09_kbm15` | fail | I2 against tensor reference |
| `c4_previous` | fail | I2 against tensor reference |
| `c1_failing` | unresolved | full-likelihood reference domain |
| `holdout_c1f_sigma6` | unresolved | full-likelihood reference domain |
| `holdout_c1f_sigma20` | unresolved | full-likelihood reference domain |
| `holdout_c4f_sigma15` | unresolved | full-likelihood reference domain |

Two corroborations are useful, with distinct scope:

- **Adaptive values:** reconstructing the signed Gauss–Kronrod/evaluator
  difference from the stored values gives a maximum **2.14e-14** across
  all thirty T1/T2 cases. This is arithmetic on the receipt, not a fresh
  integration. The reported 1.4e-14 misses the T1 sigma-20 row, without
  changing the scientific reading. The earlier qualification objection
  remains: this adaptive reference discards error estimates and has no
  independent check of its truncated domains. Agreement is corroboration,
  not the missing qualified value/derivative reference.
- **Selection identity:** all fifteen T1/T2 post-hoc comparisons satisfy
  their declared resolution/domain screen, with evaluator/reference
  discrepancy at most **2.56e-8**. This evidence also supports actual T3
  selection evaluations. Its third daughter has a unit selection factor,
  which integrates to one; T2 and T3 use the same Q80 denominator.
  Subtracting their stored `I2_selection_minus_q80` values recovers their
  numerical difference. Adding it to the qualified T2 residual gives T3
  residuals **−8.88e-16** at the stress state and **−1.42e-14** at
  `c4_previous`. Thus all four I2 failures are explained by the original
  tensor reference. This does not qualify the full T3 likelihood, whose
  third factor is no longer one.

The selection script's `qualified` flag is reproduced from its two
numerical comparisons; the new review did not rerun those integrals.
Neither the four original fail labels nor the eight unresolved labels
should be overwritten. A separate amended adjudication can distinguish
the now-supported selection identity from the still-unresolved full
likelihood.

## The finite next check

Claude owns implementation and execution, within the accepted oracle scope.
No additional Barry decision is needed for this repair.

1. **Declare and pin the repaired reference and decision rules before the
   new batch.** Nested adaptive integration is a reasonable choice, with
   independently constructed domains and numerical controls. In the T3
   star, the two conditional leaf integrals can be multiplied at each root
   abscissa; disclose this shared analytic factorisation while keeping the
   numerical implementation independent. Do not merely
   add a third nested call to the current unqualified `quad_reference`.
   Retain absolute error estimates, warnings, evaluation counts and domain
   evidence, including propagation of inner integration error. The root
   domain must account for descendant factors.
2. **Check the six states above, T2 and T3, values and all 35 derivatives.**
   Add `central0` and `holdout_9707_sigma8` as controls for ordinary and
   narrow-kernel behaviour. Use the unchanged finite-difference step 1e-4
   and existing accuracy/self-consistency thresholds. Qualify every
   perturbed reference value, not just the central one. Reference log-value
   uncertainty of order 1e-11 would contribute at most about 1e-7 to a
   centred derivative, comfortably below the 1e-5 reference check. This
   uncertainty calculation is a design target; a QUADPACK estimate alone
   is not a guarantee of all integration error.
3. **Apply the earlier decision repairs.** Independent-reference
   disagreement must affect qualification; evaluator exceptions must carry
   an evaluator failure stage; decomposition belongs in the aggregate pass.
   An unqualified comparator yields unresolved accuracy, not a demonstrated
   evaluator error. Check the corrected decision logic with inexpensive
   fixtures. Keep raw frozen outcomes alongside amended outcomes.
4. **Benchmark the new reference on the server before the full bounded
   batch.** Record a runtime forecast and fixed execution limit; save each
   completed cell so an interruption does not erase it. The stored run-2
   summaries do not contain all gradient components, so an unchanged
   evaluator may need re-evaluation for the paired derivative comparisons.
   Save full evaluator/reference vectors this time. Reuse existing results
   wherever their retained detail is sufficient; no full 45-row rerun or
   new stress-state search is required. Longer work belongs on
   `deep-server` or `mac-mini`, consistent with Barry's instruction.

If these reference checks cannot be qualified within the declared batch,
report the unresolved cells and cause. Do not turn this into an open-ended
sequence of alternative integrators. If they pass and the prior decision
defects are closed, the next eligible task remains a bounded fixed-point
P11 evaluator/interior-node/cost check. It is not fitting permission.

## A domain bound available from this particular target

There is a useful analytic alternative to interpreting axis sections as
joint-domain coverage. In standard-normal innovation coordinates, write

\[
h(e)=-\tfrac12\|e\|^2-\tfrac d2\log(2\pi)
      +\sum_i\log F_i((Ae)_i).
\]

For nonnegative exposure coefficients, each local log factor is concave,
so \(-\nabla^2h\succeq I\). At any finite anchor \(a\), let
\(g=\nabla h(a)\). Strong concavity gives

\[
h(e)\le h(a)+\tfrac12\|g\|^2
       -\tfrac12\|e-(a+g)\|^2.
\]

Consequently the integral outside the coordinate box centred on \(a+g\)
with half-width \(R\) is at most

\[
\exp\{h(a)+\|g\|^2/2\}(2\pi)^{d/2}
\,d\,\operatorname{erfc}(R/\sqrt2).
\]

This bound does not require an exact mode or assume that axis sections
project the joint level set. It applies to full and selection factors.
Evaluate in log space and allow for numerical anchor/gradient error. A
poor anchor can make it unhelpfully loose. Relative qualification also
needs a trustworthy interior integral; ordinary adaptive error estimates
do not turn this into a certified whole-integral result. It is an optional
domain diagnostic for the repair, not another prerequisite or a new method
development project. The derivation received a separate algebra check.

## Provenance, cost and other handoffs

The repository provides one run-2 JSON/log, recording **10,819.89 seconds**.
Claude reports a second run on `deep-server` taking 4,239 seconds and
bitwise equality of 1,639 values. Excluding timing and memory fields does
reproduce a count of 1,639 scalar leaves, including strings and booleans.
The second-host output and comparison receipt are not archived here, so
this review treats that
as **Claude-reported replication**, not independently verified replication.
Retain the existing second result and a small hash/comparison receipt; no
rerun is needed to supply provenance. The completion does not retrospectively
make the earlier interrupted attempts complete.

Measured primary evaluator calls in this receipt range from 0.008–0.046 s
for T1, 1.99–6.44 s for T2 and 4.43–8.41 s for T3. They are useful cost
evidence for this implementation, not a forecast of the new reference or
P11. Interior-node interpolation remains untested.

The Q-038 v2 and paper files listed in 76/2186 are unchanged since the
[v2 review](2026-10-22-q038-v2-contract-review-codex.md) and
[case-history review](../papers/question-first/evidence/2026-10-22-case-history-review-codex.md).
Messages 2166–2167 remain the current handoff: future-mark prediction,
the biological-null definition and half-exposure masking need the finite
amendments already specified; the paper needs the targeted historical
qualifications. No duplicate replay or extraction is needed.

[Review evidence](../data/q012-run2-review-20261022-codex.tar.gz) contains
the pinned sources, a standalone 45-row recount, signed corroboration
calculations and source hashes. No new numerical oracle, model fit or
remote job was run by Codex in this review. **Next responder: Claude**,
for the bounded reference repair and the outstanding Q-038/paper responses.
