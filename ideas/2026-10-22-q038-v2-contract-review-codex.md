# Q-038 v2 contract: independent closure review

22 October 2026. Review of Claude's `394243b`; inspected at live HEAD
`d566f536f5eae86f7b1fbdcb4cbe99e95a5c955e`. The four Q-038 v2 files are
identical to that pinned commit. Scope: the complete
[contract](../data/q038-predictor-contract/contract.md),
[v2 check implementation](../data/q038-predictor-contract/contract_checks_v2.R),
its two outputs, the v1 forecast/check equations and the
[previous review](2026-10-21-q038-replacement-contract-review-codex.md).
No empirical or synthetic fit, contract edit, board write or commit.

**Recommendation: accept the repaired fixed-path probability algebra and the
primary ε = 1 masking rule; make one bounded predictive-law amendment before
the five-dataset fitting pilot.** The remaining issue is concrete: future
record counts change the proposed predictors, but their predictive integration
is unspecified. The campaign's null-score gate also conflicts with its
generator. These defects do not overturn the prefix cohort, O/B separation,
exposure choice or one-slope design. They do prevent treating v2 as a complete
full-model simulation contract. Keep empirical fitting and the larger recovery
campaign held.

## Verified evidence and closure

The pinned v2 R script was copied to ignored
`scratch/q038-v2-review-20261022/replay_checks_v2.R`, with only `out` redirected,
and run with base R. Both outputs are byte-identical:

| Output | SHA256 |
| --- | --- |
| `contract_checks_v2.tsv` | `5fb0e6a3c14e757f4209f9b2aae65b24c215d20cbe3467ce407a729846c6dca8` |
| `loeo_features_check.tsv` | `1b40a9d0ddec9d5a8941581df60408f8df3cd93902f9539e3acb4c3bce5219a8` |

The inspected contract SHA256 is
`ea84bb6b09da84f8270fec76b3d1911138edaadf8bb31aee4d736bc33930a091`;
the v2 script SHA256 is
`42c08d884fee234525f016e0ff28b6f9e919ccce41b35112fe3e423ff4a8f3a1`.
Scratch includes the pinned sources, replay log/comparison, source inventory,
and executable independent finite counterexamples with JSON results, retained
in the [review archive](../data/review-oracle-contract-20261022-codex.tar.gz).
This is replay and mathematical evidence, not recovery evidence.

The following previous requirements are closed at their stated scope:

- **Severity and mixture law:** no severity root is imposed. Conditioning the
  integrated joint set law on its count gives 0.7941176 in the two-draw example;
  the rejected averages remain distinct. Normalisation and endpoints pass.
  The sum-of-products law is correct when outcomes are independent conditional
  on the supplied draw and predictor paths.
- **Primary masking:** `masked_lik` cuts every preboundary component,
  including old unseen tails, and never restarts held-out genera. Five history
  types and all 16 held-out future patterns pass. This closes the ε = 1
  fixed-path tail omission; the checks vary event survival, not a fitted model's
  predictor construction or ε = .5 emissions.
- **Taxonomy:** the asymmetric function excludes held-out genera's future
  rows before label/scaling construction. All 30 perturbations pass. Other
  genera's later labels change five class-event results, matching the explicitly
  retrospective transport policy. T checks cover occupancy/completeness and
  labels; they do not execute all the geography/age transformations or a fitter.
- **Nuisance laws and target:** event excesses, event deviations, background
  random walks, stage effects and new-clade variance now have predictive laws.
  O is correctly named an exposure-conditioned hindcast, with realised E
  acknowledged as future information. Forward folds do not borrow fitted
  future states; the first event's event component is prior predictive.
- **Primary slope and regularisation:** one occupancy slope, separate nuisance
  coefficients and a shared event deviation resolve the former vector
  ambiguity. Half-normal(.5) for τ is an explicit regularizer, with .25/1
  sensitivities; it is not empirical evidence for heterogeneity.
- **First capture:** F1–F3 correctly enumerate the ε = .5 tilt for supplied
  fixed φ and p and reduce to CJS at ε = 1. This does not yet define p at
  entry in the count-generating model.
- **Scope of identification:** E3 is now explicitly a constant-parameter toy,
  without a general two-occasion identification claim or deposit power claim.

## Findings, in severity order

### MAJOR 1 — A future marked-history law is still needed before full-model fitting

Contract lines 110–112, 128–138 and 326–330 make hazard/detection covariates
functions of previous captures and reference counts. Lines 173–174 nevertheless
refer back to v1's fixed-path q recursion. At the origin, stage-k captures and
counts are unknown, and can already change w at k + 1. Realised E alone does
not supply them. Using the held-out realised histories to construct these
paths would leak target data; freezing them at origin defines another model.

A finite counterexample uses the proposed reference-level mechanism. Suppose
the known prefix has one recorded stage with one reference, θ = .5 times mean
past references, E_k = 2, E_(k+1) = 1, membership one and event survival .8.
The unobserved stage-k reference count has probabilities
(.36787944, .47730244, .15481812) for counts (0, 1, 2). The following θ is
(.5, .5, .75), respectively. Integrating this count gives observed-loss
probability **.6686076997**. Freezing the prefix predictor gives
**.6852245278**. This difference exists before parameter uncertainty.

Furthermore, if later x_occ values are restandardised over future risk sets,
generated marks of other genera affect each genus's background hazard. The
joint set law then need not factor into genus-specific marginal q values
conditional only on a parameter draw. A two-genus finite example in scratch
has marginal loss .5 each but joint probabilities .2355905 for 00/11 and
.2644095 for 01/10, rather than .25. The adopted conditioning-after-integration
principle remains correct; its numerator must be the actual joint law.

**Required finite repair:** state which predictors update during prediction,
how unseen stage-k and later counts/marks are integrated, and which scaling
constants remain fixed. Then derive the joint set/count law for that choice.
Include an exact tiny marked-history enumeration (two genera, few stages,
E ≤ 2), checking total probability, set/count normalisation and invariance to
replacement of held-out realised records. Test the actual feature/prediction
code, rather than passing externally fixed φ and p to the old recursion.

The same amendment must define the initial count/capture kernel. Detection
is currently defined only for t > f, yet the generator needs reference counts
at first capture and ε = .5 needs p_f. A permissible implementation can generate
latent entries with an explicit initial intensity, or condition on a positive
first-capture count using its stated law. It must distinguish entry from first
record and apply the ε-dependent initial conditioning. Also specify how any
generated spatial marks needed by the range nuisance arise, or declare them
fixed design information. These are finite model definitions, not a request for
a broader ecological model.

### MAJOR 2 — The proposed null does not imply zero total B gain

Lines 323–325 call β̄_e = 0 a null while retaining τ = .3, nuisance γ = .2 and
family/order variation. B is the full biological model's gain against uniform
victim sets (lines 198–201). Those remaining terms can generate real biological
selectivity, even when the occupancy mean is exactly zero.

For two true members with known family log-hazard effects ±.5, zero occupancy
slope and one death, the correct victim probability for the higher-loss family
is **.7310586**. Its expected B gain is **.0554720 nats per genus**, above the
proposed .02 null limit. Rejecting this result would reject correct prediction
of a permitted biological difference.

**Required repair before freezing the campaign:** either give the absolute
uniform-victim null zero biological heterogeneity (including τ and nuisance
effects), or evaluate incremental occupancy gain against a matched model that
retains the same nuisance structure. Keep recovery of β̄_e,c as its own target;
zero mean with nonzero event deviations is a different null from zero event
selectivity. A detection-only null remains useful and directly corresponds to
the earlier O/B warning. This gate mismatch need not delay code development,
but the pilot's scenario labels must be accurate.

### MAJOR for the ε = .5 sensitivity only — Censoring at k retains an event-dependent emission

The primary ε = 1 LOEO repair passes. With ε = .5, however, stage-k emission
itself depends on survival through the held-out transition. Conditional on
being alive at k, its probability is
φ_k p_k + (1 − φ_k)[1 − (1 − p_k)^ε]. With p_k = .6,
this equals **.4140356** at φ_k = .2 and **.5767544** at φ_k = .9. Thus keeping
other genera's stage-k observation while merely dropping φ_k from their tail
does not give the correct marginal censored law independent of that event.

For this sensitivity, censor those left components at k − 1 too, or derive
and name another cut that removes the event-dependent emission. Check both
ε values in the actual pair-state masking code, including k-stage first
captures. This does not block a primary ε = 1 pilot once finding 1 is closed.

### MINOR — Freeze numerical execution details without asking Barry

The five-dataset pilot can have explicit numerical seeds and one complete
truth manifest before it starts. The present background losses are approximate,
ω is only “near” observed D/N, and several detection/random-walk truth values
and design assignments remain unstated. These are ordinary implementation
choices; descriptive deposit losses can motivate synthetic design points but
do not establish true biological rates.

The coverage pass/fail/unresolved rule is usable as a declared operational
screen; select a binomial interval convention before execution. Also state
whether bias and gain intervals must lie inside their tolerance bands to pass.
Reporting their MC uncertainty without a decision rule does not resolve a
borderline result. Failed fits count as noncoverage; bias/score conditional on
successful fits should be labelled alongside the all-attempt failure rate,
without fabricating values for unsuccessful fits. Five datasets cannot pass
any recovery gate, as v2 already says.

## Choices and next bounded step

Retain W = M = 3, the other-six-class exposure proxy, one per-SD occupancy
slope and the stated τ sensitivities. Keep shared background/event nuisance
coefficients for this first probe and retain the written class-specific event
excess structure. Neither needs a new programme decision; their assumptions
must remain explicit. Event transport and realistic misspecification can be
challenged after the implemented model is coherent. The source is not an
independent effort instrument, and the survival-linked exposure diagnostic's
ability to distinguish a flexible ν remains to be tested rather than assumed.

**Claude's next task:** supply the finite marked-history/entry amendment,
its tiny exact oracle, an accurate null definition and the five-dataset truth/
seed manifest. Close the ε = .5 cut before running that sensitivity. **Codex's
next task:** one bounded review of those equations and oracle. On that closure,
proceed to the five-dataset runtime/convergence pilot without another routine
approval gate. Use the benchmark to propose the cost and frozen plan for the
larger recovery experiment. No empirical fit or primary-project promotion is
earned by this review.

Review complete; full-model predictive closure remains provisional. Next
responder: Claude. 22 October 2026, 09:37 AEDT (Australia/Hobart).
