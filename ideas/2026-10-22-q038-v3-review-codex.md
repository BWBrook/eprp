# Q-038 v3: marked-history closure and primary pilot eligibility

22 October 2026. Independent review of Claude's `1073cd2`, also the live
HEAD at inspection. Scope: the v3 amendment to the
[contract](../data/q038-predictor-contract/contract.md), the complete
[marked-history oracle](../data/q038-predictor-contract/marked_history_oracle.R),
its output and the outstanding findings in the
[v2 review](2026-10-22-q038-v2-contract-review-codex.md). No fit, full design
simulation, empirical analysis, remote job, contract edit or board write.

**Recommendation: proceed to implementation of the primary ε = 1 fitter and
the five S2 datasets, seeds 38001–38005, after the implementation checks below.**
The missing primary predictive law is now supplied. No further conceptual
approval gate is needed. The five datasets measure runtime and convergence;
they cannot qualify recovery or release the larger campaign. The optional
ε = .5 sensitivity needs a corrected oracle and count-conditioned first-capture
initialisation before it is run.

## Verified closure

The pinned R oracle was copied to ignored
`scratch/q038-v3-review-20261022/replay_oracle.R`, changing only its output
directory, and executed with base R. Its output is byte-identical to the
tracked TSV. Source receipts:

| File | SHA256 |
| --- | --- |
| `contract.md` | `923d2f9dd389e75738e9d43819e2daec93350342b4f13a60e7397a4a4f73712f` |
| `marked_history_oracle.R` | `913697b22dd1f583c6901d73ce51a06df8799c1c2a4223e1d1a8255109edfea5` |
| `marked_history_oracle.tsv` | `8bfe7c2860d5ef8e8b9d7294633cb01c7afc2c28450bd1d203cf07168b9bc059` |

The former primary objections are closed:

- Unknown stage-k and later reference counts are integrated, while own-history
  predictors update. O1 reproduces .6686077 rather than the frozen-path .6852245.
- Origin-frozen scaling removes the cross-genus coupling identified in v2.
  The separately implemented joint recursion agrees with products of the
  integrated marginals to 1.1e-16. The restandardised alternative retains a
  1.52e-4 discrepancy and is explicitly excluded.
- Exact path totals and set/count normalisation pass. The 200,000-path Monte
  Carlo result differs from exact q by 0.185 reported standard errors. O4 is a
  useful interface check: realised future rows are discarded before calling
  the predictor. It is not yet a test of a full fold-building implementation.
- Entry before observation, the before-first-record detection intensity and
  reference-count kernel are now explicit. The primary spatial nuisance has
  been removed, avoiding an undefined spatial-mark generator.
- S0 correctly makes event victim probabilities uniform among true members;
  S1 retains biological heterogeneity with zero mean occupancy slope and no
  zero-total-B-gain gate; S2 is the positive control. The previous null/gate
  contradiction is closed. The reported positive-gain example is illustrative,
  rather than a numerical prediction for every S1 dataset.
- The ε < 1 cut is correctly moved to k−1. The primary ε = 1 cut is unchanged.
- The five S2 seeds, main truth values, initial fit budget, diagnostics and
  later Monte Carlo decision conventions are declared. These are design
  choices for a technical benchmark, not estimated biological truths.

## Findings and implementation requirements

### MAJOR for the optional ε = .5 sensitivity — O7 is not a normalised conditional likelihood

`lik_eps_cut` (oracle lines 170–182) divides by the probability of capture at f
but never includes the first-stage emission in its numerator. Summing the
actual function over all later binary histories gives **1.6666667 at ε = 1**
and **1.8066557 at ε = .5**, rather than one, for its stated example. Thus the
reported .09407263 likelihood range is incorrectly scaled.

An independent death-stage enumeration that includes the first emission gives
total one at both ε values. The corrected range for a cut at k is
**.05644358** at ε = .5; a cut at k−1 has range zero. The ε = 1 cut-at-k range
is numerical zero. The substantive masking amendment therefore survives this
oracle bug. Correct O7 and its cited number while implementing the sensitivity;
it does not block primary implementation. Do not reuse this helper as either
fitter's likelihood until its omitted initial emission is corrected.

The same sensitivity must condition on the **observed first reference count**
when that count is retained. The positivity-only tilt checked in O6 is correct
for the event “count > 0”, but death and survival have different count laws.
At O6's parameters, survival after a first count of one is **.77650894**;
after a first count of two it is **.88529686**. Conditioning only on positivity
gives **.79581058**. Consequently, the unconditional positive-count law is a
mixture of the survival/death zero-truncated binomials at ε < 1. Use that marked
kernel in the pair-state initialisation. At primary ε = 1 the two count laws
coincide, so this distinction vanishes.

### Implementation acceptance — use the declared count law and one feature convention

The v3 oracle supplies a coherent primary forward marked process. Implement it
directly, retaining CJS marginalisation of latent alive/dead states:

- For stages after the conditioned first capture, a living genus's observed
  reference-count emission is Binomial(E_t, 1−exp(−θ_t)); a dead genus emits
  zero. A binary-only presence likelihood does not become the marked-data
  likelihood merely by using earlier observed counts as covariates. The
  count emission is a direct consequence of v3, not an additional model.
  Conditioning on the initial observed count is permissible for the primary
  CJS likelihood; state that convention explicitly.
- Use one declared covariate and scaling convention across the generator,
  fitted likelihood and predictive code. In particular, origin-frozen means
  and SDs in the forecast must not silently differ from per-stage generator
  or training z-scores while retaining the same numerical slope. Record the
  constants and transformations, the first-record-stage exception and
  zero-variance handling in the implementation manifest. A fold-specific
  transformation must carry its coefficient interpretation consistently.
- Shared future event, class-stage and clade effects belong in the outer
  predictive draw, shared across the affected genera. Integrate each genus's
  own future marks conditionally on that draw; preserve the v2 integration of
  joint set and count probabilities before conditioning on D.

Test the actual fitter/filter and predictive functions against a tiny exact
count-history law, including positive counts larger than one, zeros after
last capture, first-capture conditioning and a masked old tail. Check total
probability, the likelihood and posterior-predictive q using the same features
as the generator. Extend the future-row replacement check to the implemented
fold builder. These are ordinary implementation checks within the authorised
work, not another standalone contract-review tranche.

Two remaining numerical details can be completed by the implementer without
asking Barry: record the ten event-excess values and their deterministic design
calibration before generating datasets, and archive the generated true δ/clade/
stage-effect draws and seeds. Calibrating synthetic truth is distinct from
severity matching on held-out observed outcomes, which remains excluded from
scoring. Monte Carlo q precision should be measured if predictive scoring is
timed; 2,000 paths is a minimum budget, not evidence that every log set score
is sufficiently precise. No recovery decision rests on these five datasets.

### MINOR for the later campaign — distinguish a matched S0 from event-only removal

S0's event-uniform target is now correctly labelled, but its phrase
“background ... heterogeneity kept” needs one restriction before that scenario
is generated. The fitted nuisance and family/order effects are shared between
background and event hazards. Removing those effects only at events while
retaining them in background truth puts S0 outside that fitted model. The
simplest matched S0 sets the shared biological γ and family/order effects to
zero at **all** stages, as well as β̄_e and event deviations at events. It can
retain the distinct background occupancy slope, background intercept variation
and detection heterogeneity. Alternatively, label event-only removal as an
explicit misspecification stress. No additional hierarchy is needed, and this
does not affect the S2 benchmark.

## Handoff

Primary ε = 1 implementation and the five-dataset benchmark are eligible.
Keep empirical fitting, the larger recovery campaign and the ε = .5 run held
until their respective implementation/benchmark requirements are met. The
contract's scientific claims remain unchanged: O is an exposure-conditioned
observation hindcast; B needs recovery and misspecification evidence.

Scratch contains pinned sources, replay receipts, a source-hash inventory and
`independent_checks.R`/`independent_checks.tsv` reproducing the O7 defect,
corrected cut result and first-count tilts. Parent Codex retains the review
archive at [review-run3-v3-20261022-codex.tar.gz](../data/review-run3-v3-20261022-codex.tar.gz).
Claude implements next; Codex reviews the implementation evidence and
benchmark results. Review complete; fitting performance remains untested.

22 October 2026, 14:35 AEDT (Australia/Hobart).
