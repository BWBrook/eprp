# Q-038 replacement contract: independent Codex review

21 October 2026. Review of Claude's `c523389`, inspected at HEAD
`bd84335825142c63a5ac0beb1bdb0c60af6509ad`. Scope: the
[replacement contract](../data/q038-predictor-contract/contract.md), its complete
[check implementation](../data/q038-predictor-contract/contract_checks.R),
tracked outputs, support README, and the preceding
[Codex requirements](2026-10-21-outside-consultations-response-codex.md).
No empirical fit, board write, source-data modification or contract edit.

**Recommendation: approve the conceptual repair, with changes before a finite
synthetic fitting probe.** The prefix-defined risk set, latent membership,
separation of O from B, and detection-only null fix the central previous
mistakes. The supplied checks reproduce. The remaining defects concern a
complete predictive law and implementable masking, rather than the existing
support tables. No empirical analysis is earned.

## Verified evidence

The supplied script was copied to ignored
`scratch/q038-contract-review-20261021/replay_checks.R` with only its output
directory redirected, then run with base R. All three products are byte-identical:

| Output | SHA256 |
| --- | --- |
| `contract_checks.tsv` | `c9548f9a3e51339d813237f74de531ede930fe115eef4162a91c8df8ea6b68f7` |
| `prefix_features_check.tsv` | `0cfb301ea594f83f04edeb9fd1aa1d61d6e271cd7d418192840eeee9f877eb66` |
| `exposure.tsv` | `556bc95177ac58e6d9597648b94b7695ae229acc62628d3ee787f9e1c8b626a0` |

An independent Python enumeration in the same scratch directory compares all
64 detection histories under a seven-stage absorbing-state generator with the
written CJS likelihood: maximum absolute discrepancy `6.94e-18`. For all four
three-stage prefixes, membership π and observed-loss q agree with explicit
latent-state enumeration to `1.11e-16`. Thus the equations in contract lines
143–162 are correct for ε = 1, with parameters and admissible predictors fixed.

Scratch evidence inventory: `replay_checks.R`, `replay.log`, the three replayed
TSVs, `replay_comparison.txt`, `independent_checks.py`,
`independent_checks.txt`, and `artifact_inventory.tsv` (paths and SHA256s). These
are also preserved in the [parent review archive](../data/review-followup-20261021-codex.tar.gz). The tracked source/check outputs and this review retain the
reconstructible scientific record.

E1's retrospective-cohort failure, E2's O gain `0.3752104` with B gain zero,
E3's flat free-detection M = 1 profile, and all 30 deposit feature-invariance
checks replay. The toy M = 3 result is evidence about that toy model only.

## Findings, in severity order

### MAJOR 1 — Severity matching can fail, and the predictive mixture is unspecified

Contract lines 168–180 solve Σq = D_O using event α, then use a Fisher
conditional score. Let `r_i = 1 - Q_i,k+1`. Even with no event deaths,
`q_i,min = 1 - π_i r_i`; α cannot reduce disappearance caused by earlier death
or subsequent nondetection. The scratch counterexample has π = (.2,.4),
r = (.8,.8), giving Σq_min = **1.52**. An observed total D_O = 1 has positive
probability but no severity-matching root. D_O = 0 or N also needs explicit
endpoint treatment.

Further, q odds from the latent mixture are not a common-intercept logistic
model: biological α does not cancel when conditioning on D_O. A fitted
`α(D_O)` can define a normalized conditional discrimination rule if explicitly
specified, including its failure policy; it is not automatically the
conditional predictive distribution of the stated generative model.

Shared event, stage and family effects also make outcomes dependent after
parameter integration. The exact conditional generative score is

`P(S | D, train) = integral P(S | theta, train) dP(theta | train)
                 / integral P(D | theta, train) dP(theta | train)`.

Compute each draw's Bernoulli set probability and its count normalizer before
integration. Equivalently, average draw-conditional set probabilities with
weights proportional to `P(D | theta, train)`. A plain average of conditional
probabilities defines another normalized model; a set law formed from averaged
q defines another again. They need not coincide. The independent example gives
**.79411765, .77472527 and .69417476**, respectively. Averaging log scores is
also different from scoring an averaged predictive distribution.

**Recommended repair:** retain conditional O as primary, but specify a
training-only predictive distribution for unknown event severity and integrate
the joint set and count probabilities as above. Do not require Σq = D_O.
Define the unconditional score from that same predictive distribution. Test
small-N probabilities by enumeration, normalization over all sets of each D,
endpoint totals, the no-root example, and shared-effect mixtures. This is a
bounded mathematical/code repair, not a new scientific approval gate.

### MAJOR 2 — Hold out every boundary-crossing likelihood, including unseen tails

Contract lines 204–209 truncate risk-set genera at k*−1 and split genera
“spanning k*”. If spanning means observed on both sides, the rule misses genera
outside W whose last record was long before k* and which never reappear.
Their CJS χ tail still contains the held-out transition. In a seven-stage
example, a genus observed only in stage 1 has likelihood **.1886121719** with
event φ = .9 and **.2413165937** with event φ = .2. It is neither recent-risk
nor observed-spanning, yet informs event survival through non-observations.

**Recommended repair:** censor every history component beginning at/before k*
at the left side of the held-out transition, regardless of subsequent record
presence. Risk-set histories stop at k*−1 as already required; other left
components can stop at k*. Any component with a later record restarts
conditional on its first postboundary detection. No inferred death time, last
observed record or range-through classification decides which χ tail is cut.
The score target remains the prefix risk set. Check the masked likelihood is
invariant to arbitrary φ_k*, β_k* and held-out genus future records. Include
never-reappearing old genera, entrants in k*, and gaps that bridge k*.

Prefix-only taxonomy passes the tested function. The LOEO implementation still
needs a separate fold-wide check: all family/order resolution and standardizing
constants must be recomputed from the actually admissible rows. If other genera's
later records are allowed to resolve a held-out genus's order, label that as
retrospective transport information and test exactly that policy. The current
P check tests a single global prefix, not the proposed asymmetric LOEO mask.

### MAJOR 3 — A forecast needs an explicit law for unknown nuisance quantities

Contract lines 94–102 specify background intercept random walks, but no law for
an unobserved event intercept or its relation to that walk. Lines 164–167 allow
postboundary exposure and background survival. Lines 199–200 transfer background
selectivity to the first event although β_b and β̄_e are distinct model
parameters without a stated relationship. These are incomplete instructions for
forward scoring or synthetic recovery.

Realized future E is useful for an **exposure-conditioned observation hindcast**.
It is future information, and the other-class reference series can itself
respond to the crisis. Calling it only information for “judging the outcome”
does not make it available at the historical origin. This qualification matters
even when it excludes the focal genus's own records.

**Recommended repair:** name primary O as conditional on realized future exposure,
and do not claim a full origin-only forecast. Keep β, severity, postevent
background states and ν in a fully specified predictive distribution learned
from training; use random-walk prediction rather than future fitted states in
forward folds. For the first event, either define a background-transfer
baseline expressly or report a prior-predictive event forecast; do not silently
substitute β_b for β̄_e. LOEO can use permitted later training information, but
must name its retrospective target. A strict origin-only forecast would need a
model for future E; that is unnecessary for this bounded initial probe.

### MAJOR 4 — The full model and simulation gates need an executable specification

E3 fits constant background survival, two detection types and constant
postboundary detection within each type. Three postevent occasions identify
its example. They do not establish identification for a model with changing
prefix covariates, stage detection effects, family effects, random-walk hazards
and event deviations. “At least two post-event occasions” is not a general
sufficiency theorem. Replace contract lines 298–301 with that qualification;
retain the toy result and profile drops as design evidence. The reported
finite-offset profile-derived SEs are illustrative local approximations, not
power calculations for the deposit or the hierarchical model.

Before fitting even synthetic data, specify:

- Whether the primary β is the single occupancy coefficient or a vector.
  A scalar δ_k added to a vector of slopes imposes equal deviations on all
  covariates; that is not innocuous. Recommend one prespecified standardized
  occupancy slope for this first recovery probe, with explicit nuisance terms,
  class-specific means and a shared event deviation for that slope.
- All priors and random-walk initial/innovation distributions, including event
  intercepts and ν; the first-record transition's covariates when no earlier
  genus record exists; and how new/unknown clades retain predictive variance.
  A fixed zero random effect does not retain new-family uncertainty.
- How simulated histories generate prefix occupancy, reference counts and risk
  sets. Do not select histories to force observed risk-set sizes while assuming
  the ordinary CJS likelihood. Generate the histories and apply the frozen W
  rule; match design sizes approximately or state the conditioning explicitly.
- What reference clustering means after stage observations have been collapsed
  to binary presence. A reference-level effect shared across genera/opportunities
  is a meaningful challenge. Repeated rows within an already-collapsed reference
  are not additional binomial trials. A stage effect cannot absorb arbitrary
  within-stage reference dependence.

## Concrete choices and acceptance criteria

**Exposure:** use the other-six-class reference series as the first declared
proxy. Its construction is reproducible and avoids direct focal-class feedback;
it is not an external effort instrument. No better independent opportunity
series has been demonstrated within this review. Retain focal leave-one-out,
collections and a verified all-animal alternative as sensitivities. The
survivor-exposure scenario must change the observation mechanism, not merely
rescale E with a freely offsetting ν; predeclare its strength and the discrepancy
that should reveal it.

**W and M:** retain W = 3 and M = 3 as score-independent operational primaries.
Report stage durations, excluded old-prefix genera and uncertain membership.
W = 1/all and M = all are appropriate sensitivities; three geological stages do
not represent a common number of Myr.

**Final-stage exposure:** ε = 1 is internally coherent. Retain ε = .5 as a
misspecification sensitivity, but derive and enumerate its pair-state likelihood
including conditioning on the first detected stage. When emission depends on
the following death transition, that initial detection can select survival;
one cannot assume the ε = 1 first-capture conditioning is unchanged.

**τ:** half-normal(.5) is a reasonable declared regularizer for a single per-SD
slope, not an evidence-based estimate of heterogeneity from five events. Compare
scales .25/.5/1 and prior versus posterior event variation. With only five
shared event units, report prior sensitivity and class-specific precision.

**Finite probe:** retain null and β = .5 controls plus the two misspecification
scenarios. Freeze generator parameters, number of repetitions, seeds, parameter
of interest, fitting diagnostics and failure accounting before execution.
Recommend 200 attempted datasets per primary correct-model
scenario if the benchmarked cost permits; count failed fits in the denominator
and report all failure types. Smaller diagnostic pilots can test code but cannot
pass a coverage gate. Report binomial Monte Carlo intervals for coverage and
Monte Carlo uncertainty for bias and mean score. Retain 95% interval coverage ≥ .90,
|bias| ≤ .1 and null B gain ± .02 as provisional decision thresholds; distinguish
an unresolved Monte Carlo interval from a pass. β must be defined per class, or
as an explicitly weighted common target, before assessing those gates.

A posterior SD ≤ .5 alone is insufficient: a strong prior can achieve it with
almost no likelihood information. Report contraction relative to each stated
prior and recovery/held-out B gain for β = .5. Treat SD > .5 as an operational
precision hold for the present design, not a universal failure of Q-038.
Likewise, do not park the scientific question because one simulator setting
fails; identify the particular selectivity claim and data design that remain
unsupported. If realistic exposure/clustering misspecification produces false
biological selectivity and the predeclared diagnostics fail to flag it, the B
claim is not earned; O can retain its explicitly observational scope.

## Next bounded task

Claude should amend the four major items and add the score, tail-mask and
full-model deterministic checks. Codex should review that finite amendment.
Then a benchmarked synthetic pilot can establish runtime, convergence and
whether the fixed recovery experiment is worth its cost. Keep empirical fitting
held. This review does not allocate a larger campaign or change the register.
