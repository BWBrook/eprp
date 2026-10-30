# What the proposed topology and coupling checks establish

30 October 2026. Independent GPT-6.1 Sol mathematical audit, integrated by
main Codex, of Correspondence 96/2581 against the
[15 October specification](../../literature/2026-10-15-b002-paper-specification.md).
These are proofs and constructed counterexamples, not ammonoid reconstructions.

## Strict obstruction and path components

For continuous finite margins `J<=A`, all-stage feasible endpoints and all
continuous admissible paths, `B_A>0` is equivalent to a connecting path in
`{A>0}`. Positive continuity along a compact path gives a positive minimum.
`B_J<0` excludes a path in `{J>=0}`. Its converse requires additional
regularity: distinct feasible path components alone do not guarantee a
strict negative best bottleneck.

For example, take `Theta=[-2,2] × [0,1)`, `A=1`,
`J=min(1,x²+y−1)` and endpoints `(−2,0),(2,0)`. Every path crosses `x=0`
with negative margin. Yet paths across `y=1−epsilon` have bottleneck
`−epsilon`; hence `B_J=0`. This domain is bounded, as the existing
specification requires, but not closed. On compact domains, continuous
margins can still have connected but non-path-connected zero sets. For a
compact domain with locally path-connected feasible set, such as a compact
semialgebraic model, the converse can be recovered: a sequence of paths
with minimum margins approaching zero has a compact connected limit in the
feasible set containing both endpoints; local path connectivity supplies
a feasible path. Any restricted route family needs its own admissibility check.

The practical rule remains the original sufficient certificate: both
endpoints feasible, `B_A>0`, `B_J<0`. A zero bottleneck needs a separate
argument. Numerical component labels alone do not certify these signs.

## Convexity supplies a valid conditional bypass

At stage s, let
`m_s(theta)=max_{z in Z_s(theta)} min_k f_sk(theta,z)`.
If the **joint admissible graph** of `(theta,z)` is convex, every slack is
jointly quasi-concave, maxima exist, and straight programme interpolation is
allowed, then the projection of each joint superlevel set is convex.
Intersections across stages are convex, so A and J are quasi-concave.
For either X, straight interpolation stays above the lesser endpoint margin;
endpoints bound every route from above. Thus `B_X=min(X0,X1)` and
`H_A=H_J=0`. The endpoint margins, and therefore `B_A−B_J`, can still differ.

The same feasible allocation must satisfy simultaneous constraints. The
specification permits different quasistatic allocations at different growth
stages; a single whole fluid history requires its own convex admissible domain.
Convex slack formulas do not rescue a nonconvex allocation graph or excluded
geometry. A homeomorphism preserves the route result only when the complete
domain, constraints and routes are transformed with it.

## One monotone coordinate and full decoupling are insufficient

**Monotone coordinate.** Let `Theta=[−2,2] × [0,1/2]`, `A=4`,
`J=x²+y−1`, and endpoints `(−2,0),(2,0)`. J is strictly increasing in y,
and both endpoints have margin 3. Every path crosses x=0, with margin at
most −1/2; the path along the upper edge achieves it. Thus `B_A=4`,
`B_J=−1/2`. The chart `(x,y) -> (x,w=x²+y−1)` makes the constraint simply
`w>=0`, but transforms the domain into a curved strip. It does not remove
the obstruction. A monotone compensation coordinate needs a demonstrated
feasible connecting face or another complete bypass argument.

**Decoupled stages.** Let juvenile and terminal controls be independent,
`Theta=[−2,2] × [0,1]`, `A=1`, `J=min(j²−1,1)`, with endpoints
`(−2,0),(2,1)`. Every path crosses juvenile control j=0, so `B_J=−1`
although terminal feasibility is unrestricted. A terminal performance equal
to the second coordinate can improve at the same time. The juvenile feasible
factor has two components: a product space alone supplies no bypass.
Juvenile-first/terminal-second adjustment works if both factors have the
necessary feasible paths and their recombinations are admissible. It is
particularly simple when both endpoints share a viable juvenile programme
that can remain fixed along a terminal-feasible route.

Partial coupling and nonevolvable thickness allometry are therefore not
general necessary conditions for an obstruction. Nor are they sufficient.
An evolvable but bounded compensator can still fail to overcome a physical
separator; other component proportions or justified stage targets can also
break the isometry null. Which instance is biologically defensible is an
empirical/physical question.

## Statistical proxies cannot supply those conditions

If adult proxy U is symmetric on [−1,1] and juvenile proxy V=U², their
linear correlation and linear R² are zero despite exact deterministic
dependence. A nonlinear fit would recover that example. More generally,
prediction performance depends on representation, coverage, selection and
measurement error; it does not identify which developmental interventions
are possible. Even true statistical independence of two summaries would not
establish unrestricted recombination of complete growth programmes.

Likewise, failure to reject a unit thickness exponent does not establish
isometry. Exact similarity of all material regions, densities and loading
rules makes q size invariant; thickness similarity alone does not. A useful
equivalence result would propagate supported deviations into physical margins
and show that they cannot bind over the declared domain. The held tables
cannot fit the proposed thickness model in the first place.

## A certified grid path is a useful exit

For a polygonal path entirely in the admissible domain, suppose node estimates
have certified lower bounds `J_i>=hat J_i−epsilon_i` and a uniform Lipschitz
constant L applies along its edges in the same coordinate norm. Then

`min_i(hat J_i−epsilon_i) − L * maximum_edge_length / 2 > 0`

certifies a positive-margin bypass. The error allowance must cover numerical
evaluation, unsampled growth stages, allocation feasibility and any uncertainty
domain included in the claim. A continuous stage grid needs its own
interpolation bound; positive sampled nodes alone do not cover all growth.
The same feasible allocation must satisfy simultaneous constraints along
each edge. Theta-dependent allocation domains need regularity before an
optimized envelope inherits a Lipschitz constant.

Such a bypass rejects the obstruction for its declared endpoints and scenario.
Failure to find it supplies no global exclusion certificate. Here the physical
margin map is unprovided, so neither grid direction is currently applicable.
