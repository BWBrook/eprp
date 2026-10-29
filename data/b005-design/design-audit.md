> This memo preserves the design challenge and later independent audits in
> chronological order. The adopted whole-capacity contract is
> [the main contract](../../ideas/2026-10-29-b005-design-contract-codex.md);
> its definitions supersede the early soft-feedback proposal below.

# B-005: conditional spatial effect and its identification limit

Codex bounded mathematical/design challenge, 29 October 2026. Proposal for
main Codex; no model inspection, literature search or model run. Packages
owns implementation/toggle verification and References owns nearest-prior
checking. This memo derives counterexamples rather than reporting a source's
scientific result. Current instructions and the B-005 register/29 October
response were read; no programme disposition changes.

**Recommendation:** first estimate a paired, fixed-nuisance effect of the
native density-dependent term on a sampled local-richness spatial profile.
Do not call a nonzero map distance historical mechanism discrimination.
Prefer an existing regional expected-richness implementation if its output
semantics and toggle pass Packages' check. Species identities are unnecessary
for this endpoint; beta diversity and global gamma richness are unavailable
from marginal local-richness expectations alone.

**Novelty restriction:** main Codex relays References' early check that
gen3sis already compares ecological limits/no limits through spatial richness
and gradient endpoints. This memo does not independently verify that source
and does not propose profile separation itself as a novel result. The possible
residual is a finite, accuracy-calibrated sampling design for a specified
conditional profile contrast, subject to References' completed prior check.
Describe its endpoint as sampling-induced *change*, rather than assuming
attenuation.

## Two exact counterexamples

Write a simple feedback model as

    dS_i/dt = r_i(t) S_i (1 - S_i/K_i).

For any resulting trajectory S_i^D(t), the density-independent model

    dS_i/dt = a_i(t) S_i,
    a_i(t) = r_i(t) [1 - S_i^D(t)/K_i]

has exactly the same trajectory from the same initial state. Here a_i is
prescribed as a function of time, with no dependence on the alternative
model's live richness. Thus no observation of that trajectory can distinguish
the two parameterisations when an arbitrary regional environmental rate is
allowed. This construction does not prove that a *restricted, independently
specified* temperature-rate function can reproduce feedback. It shows why
flexible arm-specific environmental refitting would destroy the proposed
identification argument. If regional climate/time covariates uniquely index
the observed trajectories, a flexible covariate fit can approach this problem.

An even simpler failure survives fixed intrinsic rates. Set K=(100,50),
S(0)=(10,5), common r=log(2), and evaluate at t=1. The on arm gives
(200/11,100/11); the off arm gives (20,10). Both normalise to (2/3,1/3).
Feedback changes summed local richness, but produces **zero spatial-profile
effect**. K-proportional initial states and common rates preserve this
proportionality at every time. A density-independent common rate
log(20/11) also reproduces the on arm's *absolute endpoint* exactly: even
one recalibrated rate can absorb this endpoint effect. Toy arithmetic checked
with standard-library Python; mathematical Hellinger distance is zero
(floating-point calculation 6.2e-33).

Any common linear aggregation/thinning preserves the proportional-profile
counterexample. A nonlinear observation map need not: changing only overall
richness can then change sampled shape. Normalisation after observation does
not automatically remove this mediation.

## One primary statistic and one domain

Use the existing benchmark's fixed native marine spatial support at **one
predeclared final time**, with eligibility, mask and resolution identical in
both arms. Packages must confirm the domain/output semantics before freezing
the contract. Do not select the endpoint, latitude band or cells by the
largest observed arm difference. Prefer equal-area local supports; otherwise
declare fixed area weights and acknowledge differing native cell support.

Let mu_zi >= 0 be expected sampled local richness in retained cell i under
arm z. Let w_i > 0 be fixed spatial weights summing to one. Define

    M_z = sum_i w_i mu_zi
    q_zi = w_i mu_zi / M_z
    H2 = (1/2) sum_i (sqrt(q_1i) - sqrt(q_0i))^2.

**Primary endpoint is H2 between the paired maps.** It lies in [0,1], is
unchanged by a positive scalar multiplier of either input map, accepts
continuous expected richness, and requires no pseudocounts. Zero-richness
cells have q=0 and remain included. If either M is zero, report the pair as
non-evaluable for spatial shape and report the extinction separately; never
drop it silently, replace it by a uniform profile or add epsilon. A missing
value in a required cell fails the declared map evaluation; do not form an
arm-specific complete-case mask. Cells known unavailable before simulation
are excluded by the common frozen observation mask.

M is an area-weighted local-richness quantity. Even its unweighted sum counts
species incidences across cells; neither is global gamma richness. H2 tests
redistribution of this local-richness mass, not turnover of species identities.
It does not remove environmental-rate confounding. A change in where warm
cells occur can produce the same profile as feedback.

**Sampling need not attenuate this statistic.** For full profiles
q0=(.9,.05,.05) and q1=(.9,.1,0), H2=.0292893. Mask the common first cell
and renormalise: the retained profiles become (.5,.5) and (1,0), giving
H2=.292893, ten times larger. A common mass-preserving observation kernel
contracts Hellinger distance, but conditioning on detection discards the
non-detection category and loses that guarantee. Finite sampling also adds
noise and can inflate a plug-in distance. Therefore neither a larger nor a
smaller expected sampled profile distance alone establishes better or worse
single-map discrimination. Retained observation mass/coverage must accompany
any comparison across sampling designs, and held-out false-support/power
calibration is required to make an accuracy claim.

## What the comparison must freeze

- The exact source/configuration and coefficient to toggle, beta=0 versus
  one declared native beta>0 value. All other terms retain their meanings;
  turning feedback off must not also change dispersal, environmental response
  or speciation rules. Packages supplies the actual equation/code locations.
- Forcing history, land/sea geometry, temperature-to-rate mapping, area and
  habitat masks, initial states, dispersal, other birth/death parameters,
  numerical resolution and stopping time. Do not initialise each arm at its
  own fitted equilibrium or stop each at a target richness.
- A single nuisance vector fixed before the contrast. Native fitted values
  can define a conditional benchmark, but do not make them independently
  known. Any later arm-specific recalibration is a separate question.
- One observation operator, coverage/effort map and noise law, fixed across
  arms. Start with a known linear operator if possible: common thinning and
  aggregation make the scalar invariance interpretable. If a nonlinear native
  operator is necessary, use a scalar-only control: rescale the off map to
  match the on map's pre-observation weighted local-richness mass, then apply
  the same operator. This
  artificial diagnostic tests whether total-change mediation alone can explain
  the sampled-profile effect; it is not a second mechanistic simulation.
- Shared exogenous randomness where practicable, and independent replicate
  landscapes for uncertainty. A shared seed alone does not guarantee matched
  event histories when the toggle changes the random-call sequence. Do not
  regard spatially correlated cells, latitude bands or time slices as
  independent replication. No latitude/SST residual fitting by arm.

## Finite controls and optional held-out calibration

Before interpreting the paired endpoint, require a null toggle beta=0 versus
beta=0 with identical deterministic inputs; a scalar-only map change giving
H2=0 under the linear observation operator; and a known nonproportional
redistribution at fixed M that survives the common mask/operator. For example,
equal-weight two-cell profiles (1/2,1/2) versus (3/4,1/4) give
H2=1-(sqrt(3)+1)/(2 sqrt(2))=0.03407417. Place the positive control inside
observable support. Its passage demonstrates sensitivity to that imposed
redistribution, not to every possible density-dependent mechanism.

If the implementation is deterministic and returns only expected maps, H2
alone has no empirical power interpretation. Main Codex subsequently proposed
the following exact named-observer gate. It is preferable to the initially
suggested template-distance detector because it needs no learned classifier
and supplies a bound on *every* test under its specified measurement law.

## Exact fixed-profile multinomial observer: valid, conditional, useful

Freeze two nonnegative continuous expected local-richness profiles D_zi,
common eligible cells, fixed spatial weights a_i and observation weights
e_i >= 0. Define b_zi=e_i a_i D_zi, B_z=sum_i b_zi, and

    p_zi = b_zi/B_z,
    Y | z,N ~ Multinomial(N, p_z).

Require B_0,B_1>0. This is an **additional idealised measurement law**:
N independent sampled cell-incidences, with replacement, conditional on
their total. A continuous expected-richness field does not by itself imply
this law. No species identity is needed to compute it, but Y_i is a sampled
cell-incidence count, not observed unique local taxon richness or a literal
fossil-occurrence sample. For example, independent Poisson cell counts with
means c*b_zi yield this law conditional on their sum N; that construction
illustrates the assumption rather than validating it for fossils. Spatially
clustered collections, repeated identities and sampling without replacement
need not obey it.

Holding detected N fixed deliberately discards B_z and total-yield evidence.
It is a conditional information budget, **not equal raw survey effort**:
equal c in the Poisson construction gives different expected N when B differs.
The relationship between local support, cell area and a_i must be fixed to
avoid changing the meaning of richness when spatial resolution changes.

For the two simple hypotheses, the multinomial coefficient cancels and the
likelihood ratio is

    L(Y) = log[P_1(Y)/P_0(Y)] = sum_i Y_i log(p_1i/p_0i).

The most-powerful size-alpha test rejects for large L. Because counts are
discrete, choose c with P0(L>c)<=alpha<=P0(L>=c), and randomise ties at c
with probability [alpha-P0(L>c)]/P0(L=c) when needed. Exact LR does not mean
its null quantile is computationally available without calculation: an
approximate Monte Carlo quantile must not be called an exact size guarantee.
An exchangeable null Monte Carlo rank test is an alternative finite-sample
valid calibration. No fitting or tuning to evaluation counts is needed.

**Support conventions:** a category with p0=p1=0 is impossible in both arms
and omitted; a positive observed count there is an off-model observation.
Evaluate the two likelihood supports before summing logarithms. If P0(Y)=0
and P1(Y)>0, reject at no null-size cost; if P1(Y)=0 and P0(Y)>0, accept.
If both likelihoods vanish, flag outside both models, rather than assigning
an arbitrary value to infinity-minus-infinity. Zero counts contribute zero,
including in categories having zero probability. If either B_z=0, fixed
positive-N sampling is undefined, not a discriminating shape observation.
N=0 carries no discrimination; identical profiles do not become informative
through an arbitrary pseudocount.

Let a=sum_i sqrt(p0_i*p1_i). The affinity of the *count-vector* laws is
exactly A_N=a^N: summing sqrt[P0(Y)P1(Y)] over all count vectors with total
N gives the multinomial expansion of (sum_i sqrt(p0_i*p1_i))^N. Also

    TV(P0,P1) <= sqrt(1-A_N^2) = sqrt(1-a^(2N)),
    power(any size<=alpha test) <= min(1, alpha+sqrt(1-a^(2N))).

The TV inequality follows directly by Cauchy-Schwarz applied to
|P0-P1|=|sqrt(P0)-sqrt(P1)|*(sqrt(P0)+sqrt(P1)); its two squared factors
sum to 2-2*A_N and 2+2*A_N. The power bound follows from the definition
of total variation, including randomised tests. Here a=1-H2 for the two
probability profiles, so the existing shape endpoint supplies the bound.

**Cheap finite gate:** freeze one N, alpha and target power before examining
the result. If the upper bound is below target, no detector can meet target
under this observer at that budget. If it exceeds target, it is inconclusive:
compute the fixed NP test's operating characteristics rather than equating
an upper bound with attainable power. For 0<a<1 and 0<pi-alpha<1, attaining
target power pi necessarily requires

    N >= ceil(log[1-(pi-alpha)^2] / [2*log(a)]).

This is a necessary budget lower bound, not a sufficient design. If a=1,
the laws coincide and power cannot exceed alpha at any N. If a=0, supports
are disjoint and one draw suffices for perfect separation. The earlier
proportional logistic toy gives a=1 exactly. A known redistributed profile
provides the positive control. No simulations are needed to establish these
mathematical conclusions; any later implementation still needs numerical and
support checks.

Conditional sampling weights can amplify or erase the *profile* contrast,
as the missing-cell toy above shows. This does not violate data processing:
the guarantee applies to a common mass-preserving channel on a fixed
experiment, whereas renormalising to a chosen detected N conditions on a
selection event and changes the experiment. Report B_z/retention alongside
any comparison across e_i designs.

**Claim limit:** the gate is exact for fixed endpoint profiles and this
independent-incidence observer. It marginalises neither nuisance uncertainty
nor the stochastic process generating D. A negative bound is a named-observer
information limit; it is not a limit for real fossil records, absolute yields,
other endpoints or all density-dependent mechanisms. A positive result is
separability of two specified predictions, not historical attribution, and
does not settle whether the nearest priors already cover this contribution.

**Stopping interpretation:** if valid controls pass but the paired shape
effect is negligible or absent, the selected implementation, parameter state,
time, domain and observation operator do not express a useful redistribution
signal. That does not establish observational equivalence across all settings,
an information bound, absence of real diversity dependence, or failure of
temporal/absolute-richness/species-compositional endpoints. A positive effect
establishes a conditional model prediction; flexible environmental alternatives
and nuisance uncertainty remain untested. Main Codex integrates this memo
after Packages and References return their non-overlapping checks.

## Independent implementation receipt, 29 October 2026 14:17 AEDT

Read-only review of main Codex's `data/b005-design/observer_check.py` and
`observer-check.json`; neither was edited or executed. A separate temporary
calculation enumerated ordered categorical sequences rather than multinomial
count vectors, using rational probabilities, rational likelihood-ratio tie
groups and exact rational allocation of size 1/20. Across all 16 saved
fixtures/budgets, 13,842 ordered sequences independently reproduced saved
NP power, null/alternative unit mass, and the count-support cardinalities.
Maximum power discrepancy was 8.33e-17. Summing sequence affinities confirmed
A_N=a^N (maximum discrepancy 5.56e-17), independently calculated TV satisfied
the affinity bound, and saved power ceilings agreed within 1.12e-16.

Checks include N=0, identical profiles, disjoint support, and outcomes
impossible under both models. The parent routine's allocation within an
equal-LR group need not be uniform: arbitrary boundary allocation at that
same ratio is also NP-optimal. It correctly accepts alternative-zero outcomes
unless unused size is spent there, and admits null-zero/alternative-positive
outcomes at no size cost. Both-zero outcomes are excluded from the possible
outcome enumeration; this routine is not an empirical data classifier.
No material issue found for the declared small fixtures. Its floating-point
enumeration is not a validated large-N solver, and these receipts establish
no INDITEK/gen3sis result or empirical observation-law validity.

Reviewed SHA-256 values:

- `observer_check.py`: `8763af2fd7415ed7772ce74cc53bc38c83a26c2ab4728e20f3783a2ed3b7b917`
- `observer-check.json`: `b2b5593d23dda6fb844f959ed88ddbe4b7aabec5046bbc7425b41ef157b6c93e`

## Independent native-map receipt, 29 October 2026

Read current control-plane access guidance and verified `ssh deep`
reachability. Read the two frozen raw NPZ files directly with the existing
Python environment on deep; no model invocation, installation or parent
script import. Used the exact spherical band-area expression

    area_row = [sin(lat_upper)-sin(lat_lower)] * longitude_width_radians

with the source's fixed half-degree edges, then normalised over retained
cells. This independently reproduces the main script's cosine-centre weights:
for a fixed angular band width they are exactly proportional mathematically.
The source assigns point richness using `digitize` against fixed `lat_edges`
and `lon_edges`; X/Y are meshgrid labels supplied from input vectors, not
the indexing rule. In these actual raw maps, every label equals its native
bin centre exactly (Y range -89.75 to 89.75, X -179.75 to 179.75).

Both maps have shape 360 by 720 with exactly equal finite masks and exactly
equal, everywhere finite X/Y coordinates. Each has 2,978 strictly positive
finite diversity cells, 256,222 NaNs and no infinities. Recomputed extrema
and sums agree with Packages' receipt. Raw hashes match the frozen design:

- proof: `81769f0be286176c871897953c9ada70bdf359fc2e5adfcf53fa8082f2718611`
- expo: `a55f64a8ae01b598510bfca0e8f8d9242d229e94d6efaa3d0b2d76a3a25d4a0d`
- Remote and local gridding source both:
  `f9ab162de611897aa5f87c5e136b27c92053a939aa763d2292b414300e7b1e59`

Independent results:

| Quantity | Recomputed value |
| --- | ---: |
| Supported area, steradians | 0.15821931512644422 |
| Weighted mean local richness, expo | 52.46502491650207 |
| Weighted mean local richness, proof | 10.914797158464722 |
| Squared Hellinger distance | 0.11260439313694572 |
| Single-incidence affinity | 0.8873956068630542 |
| N=100 product affinity | 6.482274785320857e-6 |
| N=100 power upper bound, alpha=.05 | 1 |
| Necessary continuous N for power .8 | 3.459937178301598 |
| Necessary integer N lower bound | 4 |

All reported map-check values reproduce to floating-point precision. The
integer bound is only necessary, never sufficient. The N=100 bound is
inconclusive; attained power has not been evaluated. Retained mass fraction
one means all of the *declared native support* is retained; it does not mean
complete global shelf coverage or an empirically complete fossil record.
This compares a whole-capacity mechanism against uncapped growth at one
fixed parameter/forcing history and endpoint. It neither isolates only the
soft feedback factor nor attributes historical richness patterns to capacity.
No consequential scientific overclaim was found in the frozen design/result
manifests; the draft narrative remains subject to a separate bounded check.

Reviewed local SHA-256 values:

- design JSON: `e95e0bc823beafe14cc35a84c6170acad2a244dd528d3142173df04a434254ba`
- map-check script: `a9b7c7626ef331f90ac0e1eeae1299a266f94be0f431c36c6882d390338ebda3`
- map-check result: `b16be17b30d0e364bbd9db3687de457cf24fb12e5a7a21bacf79e5f1128ad809`

## Final bounded scientific-claims review, 29 October 2026

Reviewed main Codex's contract and design README against the direct raw-map
and mathematical checks above, Packages' completed native-capacity note and
References' completed closest-prior brief. Q-027 table verification remains
main Codex's separate work and is not covered by this receipt.

No material inconsistency found in the current numerical conclusions,
intervention definition, stopping interpretation or programme recommendation.
The text correctly identifies the whole-capacity intervention, fixed-nuisance
and finite-horizon scope, native gridding/integrator limitations, loss of
absolute yield information, absence of global-gamma conditioning and taxon
identities, occupied generic spatial question, and lack of a justified fossil
observation law. It explicitly leaves attained power unmeasured, interprets
the N=100 ceiling as inconclusive, and labels N>=4 necessary rather than
sufficient. Seeking bounded scientific judgement before an ensemble is
consistent with the limited residual in the References brief.

One narrow wording correction was sent to main Codex: the sentence offering
independent evaluation *or* an exchangeable null-rank procedure to establish
"size and power" should separate those guarantees. An exchangeable null-rank
test controls null size; its alternative power still needs independent
evaluation. Estimated numerical thresholds require separate held-out size
and power checks with uncertainty. This does not change any current result:
no attained-power or calibrated-test claim is made in this tranche.

Reviewed hashes before that wording correction:

- Contract: `cf1d11b267e280a9ca736430d859e2e72924f813c8319e4521bea6a720db8137`
- Design README: `a9ae1a13af2d1550fd818d23b02cf23347b8e345e4dfe1396cc16ee641292e4e`
- Packages README: `d83d223cbd83e695818c310cca206d95e1ef28642537fa266001fa44dd251d4e`
- References brief: `b4aa47e12b31bc5c7b22aff023bda8e9f6366e49f523059ec891c38a87a8d8fb`

## Main Codex integration receipt

The null-rank wording correction above is applied: the contract separates
null-size control from independent alternative-power evaluation. Final corrected
contract SHA-256: `8cfbd373aa06ae73b634044a8dd28e0e4848b8db02740c780e716bdfa4b72a61`.
No numerical results changed.
