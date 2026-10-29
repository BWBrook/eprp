# B-005: a fixed spatial-profile contrast and its scientific limit

29 October 2026. Main Codex integrates the accepted Packages and References
contributions and the parallel Q-027 support check. Barry authorised this
bounded design task in main chat, quoted in Correspondence 76/2508. This is
a completed design and viability check, not selection of a primary project.

**Recommendation:** the native INDITEK-2 comparison is executable and changes
spatial shape, so B-005 has a concrete technical starting point. Its present
scientific payoff is limited: logistic/exponential and spatial comparisons
already exist, and the proposed incidence observer is an idealised diagnostic.
Seek Claude's focused judgement on whether a domain-specific observation
question merits the next development tranche. Do not commission a parameter
ensemble or present the current comparison as a new biological mechanism test.
Q-027 remains a competing development option with newly quantified, uneven
regional support. Q-012's sampler remains queued.

## One intervention, domain and endpoint

**Question:** at a fixed deposited parameter vector and forcing history, does
removing the entire finite-capacity mechanism redistribute predicted local
richness across the present-day shelf, after discarding a uniform multiplier?
Could a specified independent-incidence observer distinguish those two fixed
profiles? The first question has now been checked; attained discrimination
power has not been evaluated.

Use the pinned Zenodo INDITEK-2.0 archive and its native `proof` and `expo`
branches. The [Packages contract](../resources/software/reviews/2026-10-29-b005-design/README.md)
records source/input hashes, environment, equations and execution receipts.
The intervention removes both `rho D (1-D/K)` suppression and every hard K
cap, including caps during capacity changes, colonisation and forced-extinction
updates. The uncapped branch retains environmental rate forcing, the initial
and lower-floor value D0=1, activation/neighbour rules and extinction schedule.
It is a whole-capacity contrast, not soft-feedback-only, nor abiotic versus
all biotic effects. Capacity also mediates one effect of food supply.

Hold `[161,19,0.035,0.002,2]`, the full deposited 541–0 Ma history, food and
temperature, geography, particle ordering, initial states, numerical time
support and imposed extinction history fixed. These are conditional reference
settings, not independently known biological parameters. Do not fit either
arm, initialise it at its own equilibrium, stop it at a richness target or
shorten the horizon to repair overflow. The native branches use different
analytic logistic/exponential updates; a large-finite-K fixture checks their
limiting agreement. Passing infinity to the bounded code produces NaNs and
is not the off switch. Uncapped positive growth has no finite equilibrium,
but a finite-horizon prediction can be well defined.

The domain is **all 2,978 common native supported shelf cells at 0 Ma**, on the
360 × 720 half-degree grid. This present-day endpoint is a viability domain;
no fossil time window has been chosen. Require equal masks and coordinates,
no infinities and no negative values. Do not choose cells by arm difference
or form separate complete-case masks. Native excluded/empty cells remain
outside support. A future zero-richness or missing-data convention must be
declared explicitly; the present supported maps are strictly positive.

Let D_zi be continuous predicted local genus richness. Set a_i proportional
to the spherical area of each native half-degree bin, normalized over the
supported domain, and e_i=1 everywhere. The source grids by fixed latitude
edges; use the centre of those bins for cos(latitude) weights, independently
of supplied coordinate labels. This is an area-weighted profile of native
local-richness predictions, not a reconstruction of richness at a new spatial
grain. Define

    B_z = sum_i a_i e_i D_zi
    p_zi = a_i e_i D_zi / B_z
    H² = 0.5 sum_i (sqrt(p_1i) - sqrt(p_0i))².

The single primary map statistic H² is invariant to a positive scalar change
in either richness field. Report B_z alongside it. Neither B_z nor the sum of
local richness is global taxonomic gamma diversity. Normalisation discards
scale; it does not show incremental evidence conditional on true global
richness. Species identities and emergent taxonomic beta diversity are absent.

## A named observation experiment, not yet a fossil observation model

The preliminary observer is Y | z,N ~ Multinomial(N,p_z): independent sampled
cell-incidences with replacement, conditional on **N=100 detected incidences**.
Set `expo` as the null, `proof` as the alternative, size alpha=0.05 and target
power 0.8. The budget is a convenient fixed benchmark, not an estimate of
available fossil effort. Holding N fixed discards yield information and does
not equalise raw collecting effort when B differs between arms. Y_i is not
unique-taxon richness. Repeated taxa, collection clustering, preservation,
age uncertainty and regional dependence are not represented.

For these two simple hypotheses the log likelihood ratio is

    L(Y) = sum_i Y_i log(p_1i / p_0i).

The most-powerful size-alpha test rejects for large L with boundary
randomisation when necessary. An exact likelihood expression does not provide
an exact computational threshold by itself. An exchangeable null-rank test
can control size; attained power still requires independent alternative
evaluation. An estimated numerical threshold needs independent size and power
checks with uncertainty; do not label it an exact guarantee.
Outside-model observations and one-sided zero support need explicit handling.

The single-draw affinity a=sum_i sqrt(p_0i p_1i)=1-H² gives count-law affinity
a^N by the multinomial expansion. Cauchy–Schwarz bounds total variation by
sqrt(1-a^(2N)), hence

    power(any size <= alpha test) <= min(1, alpha + sqrt(1-a^(2N))).

An upper bound below 0.8 rules out the target **for this fixed observer and
budget**. A bound at or above 0.8 is inconclusive. For 0<a<1 a necessary
sample budget is

    N >= ceil(log(1-(0.8-0.05)²) / (2 log(a))).

This is not a sufficient sample-size calculation. Identical profiles imply
power at most alpha for every N; disjoint supports separate at N=1. These are
standard mathematical properties, not a novelty claim. The
[design evidence](../data/b005-design/README.md) contains executable small
controls and the numerical receipts.

## What the bounded checks established

Packages declared its fixture and two-call supplement before execution.
Both full-history calls completed in 27.488 seconds total on one `deep` CPU,
with identical native coordinates and finite masks, and no infinity. No further
simulator calls were made. Main Codex declared the profile weighting and
observer budget in 76/2527 before computing the profile. Existence, ranges
and support of the maps were already known: this is a design smoke, not an
untouched confirmatory experiment.

| Quantity | Result |
| --- | ---: |
| Supported cells per arm | 2,978 |
| Weighted mean local richness, bounded / uncapped | 10.9148 / 52.4650 |
| Squared Hellinger profile distance | 0.1126044 |
| Single-incidence affinity | 0.8873956 |
| Any-test power ceiling at N=100, size 0.05 | 1.0 — inconclusive |
| Necessary N lower bound for power 0.8 | 4 — not sufficient |

The finite-capacity intervention changes spatial shape at this reference
state, not only overall magnitude. The power ceiling supplies no useful
exclusion at N=100; **attained power remains unmeasured**. Neither conclusion
establishes real-record discrimination or historical mechanism attribution.

The implementation checks cover selected static-point ordinary/extinction
updates, zero growth, a large-K limit and gridding. They do not independently
validate full palaeogeographic activation/colonisation paths or the inverse
chains. Separately, 16 observer fixtures cover scalar-only changes, imposed
redistribution, masking, zero counts and disjoint supports. Independent ordered
sequence enumeration reproduces the small count-vector calculations. The
large-N count-vector enumeration is neither run nor claimed feasible.

## Strongest objections and what would answer them

**Occupied question.** The [References brief](../literature/2026-10-29-b005-prior-check-references-codex.md)
finds existing logistic/exponential regional predictions in Cermeño et al.,
spatial ecological-limit comparisons in Hagen et al., and related diagnostic
patterns in Etienne and Hurlbert–Stegen. Balembois et al. also demonstrate why
a change in global species counting can leave spatial richness unchanged.
The possible residual is an observation-conditioned discrimination envelope
for a justified domain; generic shape separation and the mathematical bound
are not that advance. The present observer does not yet meet the richer
fossil-observation residual or a beyond-gamma-richness comparison.

**Environmental confounding.** For any feedback trajectory D_i(t), a prescribed
time-varying density-independent rate rho_i(t)[1-D_i(t)/K_i(t)] reproduces
the same trajectory. This is a constructive counterexample when that much
regional rate flexibility is allowed, not a claim about every restricted
climate model. Fixed nuisance settings give an intervention effect; they do
not identify its cause from a real map. A later predictive comparison would
need independently constrained nuisance settings or training-only calibration
of explicit alternatives. That is a separate design.

**Sampling can amplify apparent separation.** A common retained-cell mask
followed by renormalisation can increase H²; the synthetic control increases
it tenfold. Conditioning on detected N changes the experiment. Do not assume
sampling always attenuates a profile difference, equate a plug-in map distance
with classification accuracy, or regard spatial cells as independent biological
replicates. Any later mask needs retained mass reported for each arm and an
explicit observation law.

The next worthwhile extension therefore needs a named biological comparison,
an admitted regional/time domain and an observation process tied to data.
More parameter sweeps of this idealisation would not answer those objections.

## Q-027 support and the next critique

Databases completed the [finite support table](../data/q027-regional-support/README.md)
and its independent raw-source reaggregation. Under the dated public-member
subset, 60,103 selected occurrence rows occupy 1,068 stage-cells, of which
726 have at least two distinct collections somewhere in the stage-cell.
The stricter within-region-band counts must be used for regional overlap.
Twelve of 21 stages have three outside-Europe/North-America regions with
qualifying tropical cells. Only Albian has three such regions each spanning
all three bands (Africa, Asia, South America); Campanian and Maastrichtian
have two. Unknown countries remain separate. Region labels are sampling
partitions, not demonstrated independent palaeobiogeographic replicates.

[Detail withheld pending disclosure to the data custodian.]

**Claude's requested critique:** (1) does a specific observation-conditioned
B-005 question have enough biological payoff after the prior check, or should
this remain reusable support work; (2) is the whole-capacity intervention and
fixed-nuisance interpretation scientifically useful, with a credible route from
the incidence observer to a real comparison; (3) does Q-027's new overlap favour
one bounded estimator-specific check instead? Recommend one concrete next
tranche, preserving disagreement. No further code or source legwork is asked
of Claude. Main Codex retains implementation; Barry retains consequential
programme and primary-project decisions. Registers and frozen results are
unchanged.
