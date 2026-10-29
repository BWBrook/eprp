# B-005 affinity critique: independent bounded check

Codex, 29 October 2026. Scope: parent-supplied claim from Claude's critique,
the already checked fixed-profile observer and its saved numerical receipts.
No remote model call, literature campaign, parameter sweep or parent-file
edit. This memo owns only its stated scratch path.

**Verdict:** the constructive affinity argument is correct. It establishes
that the two frozen profiles can meet the declared size/power targets under
the specified independent-incidence observer. The earlier upper power bound
of one was correctly labelled inconclusive, but it did not exhaust what
affinity establishes. There is no reason to leave this observer's feasibility
unresolved or run a detector campaign merely to establish it.

## Independent proof, with the threshold convention explicit

Let P0 and P1 be the two multinomial count laws at fixed detected total N,
with known probability profiles p0 and p1. Define the likelihood ratio
Lambda(y)=P1(y)/P0(y). Reject the null when Lambda>1; equivalently, reject
when the previously defined **log** likelihood ratio L>0, not L>1.
Assign equal-likelihood outcomes to the null for definiteness. Then

    alpha_N = sum_{P1>P0} P0(y)
    beta_N  = sum_{P1<=P0} P1(y)
    alpha_N + beta_N = sum_y min(P0(y),P1(y))
                      <= sum_y sqrt(P0(y)P1(y)) = a^N,
    a = sum_i sqrt(p0_i p1_i).

The last equality is the multinomial expansion. This is a fixed ratio-one
rule minimising the sum of the two errors; it is not a fitted threshold or
an assertion that its size equals .05. Since both errors are nonnegative,
each is at most a^N, so its power is at least 1-a^N. The size-.05 NP test
could also attain at least this power whenever the ratio-one rule has size
at most .05; the exact optimal power need not be computed for this certificate.

On a one-sided support point, P0=0<P1 means reject at no false-positive cost;
P1=0<P0 means accept. Both-zero outcomes have probability zero under both
models and are outside their joint support, not an infinity-minus-infinity
calculation. Equal-likelihood outcomes can instead be randomised arbitrarily
without changing the error sum. Thus the proof covers zeros and ties without
pseudocounts. At N=0 the count laws coincide and the bound is one; the strict
rule has size zero and power zero. For a=1 the bound supplies no separation;
for a=0 disjoint supports separate perfectly at every N>=1.

## Independent arithmetic and the finite 4–26 bracket

Using saved a=0.8873956068630543, standard-library Decimal arithmetic at
60-digit precision gives:

| N | a^N: upper bound on error sum and each error | Guaranteed power lower bound |
| --- | ---: | ---: |
| 25 | 0.0504582122463792676 | 0.9495417877536207324 |
| 26 | 0.0447763958776005285 | 0.9552236041223994715 |
| 100 | 0.00000648227478532093985 | 0.9999935177252146791 |

At N=26, size is therefore at most .0447764 and power at least .9552236.
At N=100, size and false-negative probability are each at most 6.4823e-6.
These are model-law guarantees on operating characteristics. They are not
empirical estimates, observed error frequencies or a guarantee that every
realised data set produces the correct decision. Exact attained size/power
remain uncomputed, but their bounds already certify the declared target.

For size<=.05 and power>=.8, this particular sufficient certificate requires

    a^N <= min(.05, 1-.8) = .05,
    N >= ceil(log(.05)/log(a)) = ceil(25.07636173411391) = 26.

Twenty-six is the smallest N *certified by this sufficient inequality*.
It is not the exact minimum N at which this test or the optimal size-.05
test succeeds: failure of the inequality at 25 proves neither test fails.
The prior any-test upper bound independently requires

    N >= ceil(log[1-(.8-.05)^2]/[2 log(a)])
      = ceil(3.459937178301602) = 4.

Consequently the unknown minimum feasible integer budget lies in [4,26]
for these two simple laws. No sharper optimum is needed for the present
decision. The ratio-one rule need not have size<=.05 at small N for an
arbitrary pair of profiles; its certified error bound is what establishes
that property here at N>=26.

Independent finite check: separately enumerated all 13,842 ordered sequences
in the four prior fixtures at N=0,1,4,8, using rational probabilities and
strict P1>P0 comparison, without importing either parent implementation.
All 16 cases satisfy the exact rational identity
alpha_N+beta_N=sum min(P0,P1), the affinity upper bound, and the product
affinity formula. Identical and disjoint profiles, one-sided zeros and ties
were included. This check differs from the saved randomized size-.05 NP
enumeration; the strict ratio-one rule deliberately has its own size.

Numerical inputs inspected:

- `map-check.json` SHA-256:
  `b16be17b30d0e364bbd9db3687de457cf24fb12e5a7a21bacf79e5f1128ad809`
- `observer-check.json` SHA-256:
  `b2b5593d23dda6fb844f959ed88ddbe4b7aabec5046bbc7425b41ef157b6c93e`

## Scientific interpretation and stopping recommendation

N counts **independent sampled incidences**, with replacement, allocated to
cells. It does not mean N distinct cells, genera, specimens, fossil collections
or independent biological replicates. Cells can be visited repeatedly.
The observer was introduced as an idealised measurement law; continuous
expected local richness alone does not imply that law. Fixed detected N
conditions away total yield and does not equalise raw collecting effort.

Recommend closing **this fixed-profile idealised observer tranche** as
reusable support. It has now demonstrated executable conditional shape
separation and analytically certified observer feasibility. Extra simulations
to establish the already certified target, or work to sharpen the exact
optimal N, would not change that decision. Its limited scientific payoff
comes from the artificial observer and occupied generic question, not a
failure of richness predictions to carry signal. It does not show that
richness-only predictions are universally uninformative or unsuitable for
a scientifically justified future observation model. It also does not
establish incremental information conditional on true global gamma richness,
historical attribution or adequacy across nuisance settings and parameter
states. Any new biological comparison needs its own named domain, observation
law and scientific rationale; that is a distinct tranche.

Finally, the density-feedback trajectory can be reproduced exactly by a
density-independent model allowed an arbitrary prescribed regional rate
rho_i(t)[1-D_i(t)/K_i(t)]. This is a counterexample for that flexible family,
not a proof that a common global rate or the native restricted environmental
parameter family reproduces the actual two maps. The proportional two-cell
toy admits a single-rate endpoint mimic only in its special construction.
Neither argument establishes that every environmental alternative is
indistinguishable from feedback. Preserve this boundary when closing the
idealised exercise.

## Final assessment review: ready

Reviewed the B-005 closure/Q-027 pairing assessment, climate-pairing README,
saved pairing summary, source delegate's climate-class and independent-pair
audit, and completed estimator contract against the affinity proof above.
No new numerical reconstruction, source search or estimator/model call.

**Ready: no blocking or material correction identified.** The B-005 closure
accepts the constructive guarantee while preserving the broader research
question and the limits of the idealised observer. It correctly distinguishes
independent incidences from cells, sufficient from optimal N, gamma richness
from local-richness mass, the arbitrary regional-rate counterexample from
restricted environmental alternatives, and a native intervention from any
alleged defect in published code.

The Q-027 recommendation uses the source's actual broad-class caller,
preserves literal Thanetian/Ypresian NAs, separates narrow extreme-state
results, discloses the support-informed focal choice, and keeps the passing
presence screen distinct from estimator eligibility. Its three reported
primary pairs and scenario counts agree with the saved summary and source
delegate's independent audit. Non-nested preparation rules explicitly block
the proposed universal negative interpretation. The named next action is a
finite Albian–Campanian eligibility build with prerequisite environment and
input-join controls, not an empirical gradient fit. Q-012 remains separately
justified work rather than an automatic fallback. Independent raw support
verification belongs to the source delegates; it was not repeated here.

Reviewed SHA-256 values:

- Main closure/pairing assessment:
  `7352e51c245040a10cd3a91133c48ae0f1187e784158e959ba16a3bd0ea6ba33`
- Climate-pairing README:
  `997294edb1ccc8387f4d5407f31e5af813ac3dfb7510d3e3ead64f421b4d281e`
- Saved pairing summary:
  `e60697eacc0bc05c23151565097a96af9ea5d461891ef6ab727323a79f7352f3`
- Source review (scratch predecessor of planned canonical source-review.md):
  `4c5b841e80c5529a722c97750274b2b6afdb5fe1d73d1de73d839971ee9a6a92`
- Completed estimator contract:
  `945a0c884e94c8972f43b9950c53367c2cfd90e69f4f2afa8c2e7033747262f9`
