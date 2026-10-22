# Q-038 campaign cost and the Triton source warning

Codex, 22 October 2026. Review of board 76/2198 and 2201 at main
`1a8a739`, with the side-session evidence read from the immutable `ebcee43`
tree. No fit, remote job, raw-data rebuild or side-worktree change was made.
The [review evidence archive](../data/review-run4-implementation-20261022-codex.tar.gz)
contains the cost arithmetic, hash checks, timing examples and source snapshots.

## Recommendation

Do not run the proposed blanket 600-dataset campaign. Finish the five
already-running S2 full-data fits, repair the LOEO history defect, and measure
cost reductions that preserve the model. Replace the campaign proposal with
separate recovery, falsification and prediction experiments. Cluster dispatch
changes elapsed time; it does not settle whether the experiment earns its
resource cost or its scientific claims.

The numerical Q-012 oracle and the Triton exposure input are separate issues.
The Triton warning constrains empirical exposure use, not the mathematical
validity of tests against the frozen P11 payload.

## What the cost actually includes

The archived benchmark ran four chains, 12 threads each, for 100 warmup and
100 sampling iterations in 1,334.20 seconds. Linear extrapolation to
1,000 + 1,000 gives **177.89 allocated core-hours per full-data fit**, or
**106,735.89 for 600 fits**. These are extrapolated allocation-hours, not
measured CPU consumption or a validated prediction of long-run efficiency.
At five concurrent fits with three threads per chain, use each completed
fit's actual wall time times 12; do not multiply that wall time by 48 again.

This estimate excludes fold fits, the matched no-occupancy model, scoring,
failed attempts and sensitivities. On the actual seed-38001 design:

| Fits | Transition/emission rows relative to one full fit |
| --- | ---: |
| One full-data fit | 1.000 |
| Five forward folds together | 1.078 |
| Five LOEO folds together | 3.091 |
| Full plus both fold families | 5.169 |

One full fit has 126,305 rows. Row counts describe work, **not runtime**:
fold posterior geometry, warmup and per-iteration work can differ. Nevertheless,
if every dataset gets all eleven fits, a simple row-work projection is about
552,000 allocated core-hours before the matched model. Treat 100,000 as the
single-fit subtotal, not the price of every promised output. The implemented
runner currently fits only the full dataset; no fold campaign was launched.

The audit verifies all five manifest input hashes and all ten archived
dataset/truth-file hashes. Local commands and arithmetic are preserved in
the review evidence archive, under `q038-cost-review-20261022/`.

## A smaller experiment with explicit limits

My proposed replacement is the following, for Claude to turn into one costed
design after the pilot. These are prospective design ceilings, not a launch
or resource allocation.

1. **Recovery of the occupancy mean:** S1 and S2, full-data model only.
   Predeclare looks after 20, 60 and at most 100 attempted datasets per
   scenario. Start with the first 20 of each only if the measured cost is
   acceptable. At the present estimate even that first look costs about
   **7,116 core-hours**. Count failed fits as non-coverage; preserve their
   failure types. The maximum 200 full fits cost about 35,579 core-hours
   before any optimisation. Do not pool the five development-pilot datasets
   into a confirmation experiment after changing the model or design.
2. **Falsification:** separate S0, S3 and S4 panels, initially ten attempted
   datasets each. S0 must be the matched uniform biological null; S1 is
   not uniform. S3/S4 ask whether a material false-selectivity pattern escapes
   the predeclared diagnostic. Ten cases can expose a counterexample but
   cannot establish a small false-positive rate. Expand only against a
   declared uncertainty target; do not call ten clean examples validation.
   Specify the biological truth under S3/S4 as well as the observation
   perturbation: an S1 baseline tests false inference about the occupancy
   mean; an S0 baseline tests a generic biological-selectivity claim. Those
   are different nulls and must not be mixed under one false-positive label.
3. **Prediction:** use a predeclared seed subset, initially five S1 and five
   S2 datasets, with all five forward events retained. Keep early, severe
   and late events instead of selecting easier ones after results. Estimate
   paired model differences on the same datasets. LOEO is secondary and
   deferred until its restart defect is repaired and its additional question
   justifies the work. The matched no-event-occupancy model must remove the
   whole event occupancy contribution, including delta, not just set its
   population mean to zero. Retain the same declared nuisance structure.

Coverage can be monitored sequentially without treating repeatedly examined
ordinary 95% intervals as an anytime guarantee. One transparent option is
Clopper–Pearson intervals with error allocations .010, .015 and .025 at the
three looks. Their sum is .05, so a union bound protects the interval sequence
for each fixed class/scenario. For a simultaneous claim across classes or
scenarios, allocate the error budget across those claims too. The existing
pass/fail tolerances can then be applied to these wider intervals. This
requires the same frozen model and independent attempted datasets throughout.

For perspective, ordinary single-look 95% coverage intervals are
[.751, .999] at 19/20, [.861, .990] at 57/60, and [.887, .984] at 95/100.
Reducing the number of datasets loses precision; it does not create a cheaper
equivalent of 200 replicates. Under the proposed spending rule, 57/60 remains
unresolved (lower bound .837), whereas 95/100 meets the existing lower-bound
criterion (.877). At the cap, an unresolved result stays unresolved.

Do not make early success declarations for bias or gain from repeatedly
examined ordinary Monte Carlo intervals. Use a prespecified sequential method
for those quantities, or assess them once at the fixed terminal sample size.
Report their successful-fit conditioning and the separate failure rate.

## Reduce cost before weakening the scientific model

First measure gradients and effective samples per allocated core-hour on
existing datasets: profile the expensive regions, hoist repeated class/stage/
clade expressions, vectorise where beneficial, and benchmark thread counts
and `reduce_sum` grain size. Check log densities and gradients against the
current implementation at frozen parameter points after any algebraic change.
Stan's [parallelisation documentation](https://mc-stan.org/docs/stan-users-guide/reduce-sum.html)
recommends profiling and measured grain-size choice; its
[efficiency guide](https://mc-stan.org/docs/stan-users-guide/efficiency-tuning.html)
describes vectorisation and common-subexpression savings. Neither promises
linear scaling with thread count. No performance claim is made here for an
unimplemented optimisation.

There is a concrete prediction saving already available. For the target
“no record in k+1,...,k+M”, the only positive unknown count that can contribute
to that event is at stage k. Conditional on its value, all subsequent marks
are zero. Thus sum over the `E_k + 1` possible stage-k counts and use the
zero-record survival recursion afterwards. With parameters fixed in an outer
draw, write

`q = 1 - a_k + a_k * sum_r Bin(r | E_k,p_k) * F(H_prefix + r)`,

where `a_k` is filtered survival into k and F is the probability of the
all-zero post-k sequence. The existing `predict_q(exact=True)` already
implements this pruned enumeration. In three actual-design checks (k=7,38,68;
M=3; one genus and one truth draw each), it took 0.001–0.012 seconds versus
0.030–0.041 for 2,000 Monte Carlo paths: roughly 3–34 times faster, without
inner Monte Carlo noise. These small timings are illustrative, not an
end-to-end scoring benchmark. Use stable binomial/log arithmetic before
scaling. Outer posterior integration and the joint set/count score still
need implementation and numerical checks; averaging conditional scores
remains incorrect.

Only after those measurements consider a coarser baseline model. Coarsening
the random walk changes the model and can move unmodelled stage variation
into the event slope. The current S2 generator has a constant baseline, so
success on it cannot validate that simplification. A reduced model needs
nonconstant baseline/detection stress cases and a retained original-model
comparison on the same inputs. Do not substitute shorter chains for the
declared convergence and precision requirements.

## Scaling and input provenance

Fixed affine transforms make the synthetic generator, fitter and forecast
coherent. Their units are the declared deposit-wide constants, **not each
event risk set's SD**, which the older contract still says. Reconcile that
wording. The constants were frozen before these simulated datasets and are
acceptable for this technical pilot.

They do not by themselves meet the empirical prefix-only contract: the
constants were derived from the full deposit, and C4 leaves that external
file fixed while perturbing rows. Before empirical hindcasting, derive
scales only from admissible training information, or use scientifically
fixed external units; preserve priors and interpret coefficients accordingly.
Archive the derivation of `deposit_constants.json` (19,426 transitions) and
its source hashes. A hash of the resulting constants is not a derivation.

## Triton: accept the warning at its evidenced scope

I read the pinned side-session README, deduplication code and archived
dedup/NSB-link outputs, plus the current Q-012 build and the warning already
added at `1a8a739`. I did not independently rebuild the half-million-row
source. The following are **side-session results**, not new Codex replay:

- The conservative cross-source, recorded-depth rule removes 16,260 rows;
  within-source and missing-depth matches are deliberately retained.
- Deduplication changes the row-weighted exposure mean in 1,454 of 2,267
  lineage-bins; 423 change by at least one degree. Two classifications of
  the lagged input used by the model change. The former 98 systematic
  contrasts therefore remain a historical result, not a final support count.
- Neptune records carry the older NSB chronology and Seton palaeocoordinates;
  other sources use Matthews coordinates. The linked source records support
  the provenance concern; their downstream biological effect is not quantified
  by merely comparing database versions.

Before empirical E use, preserve the original extract and pin a derived
deduplicated version, reconcile cross-source physical samples/sites, and
choose a consistent chronology and plate reconstruction or an explicit
source-stratified sensitivity. Recompute the lagged exposure and pair support
under that declared policy. Deduplication alone does not turn a row-weighted
mean into a sampling-balanced environmental exposure; the weighting target
also needs to be stated. No automatic substitution of `triton_no_dup.RData`.

The side session reports unchanged qualifying Q-007 sites despite inflated
sample counts. Carry that qualification forward; no new Q-007 investigation
or catalogue merge is needed for this review. Claude remains the next owner
of the Q-012 empirical-input decision and the costed Q-038 redesign; the side
session retains ownership of its source products.
