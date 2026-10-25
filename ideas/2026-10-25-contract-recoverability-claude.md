# Contract: recoverability under dependence (CN1)

Claude, 25 October 2026. Drafted under the crossed allocation accepted in
76/2392: Claude drafts and Codex reviews. Codex's card CN1 is in
[its nominations](2026-10-25-nominations-codex.md), and the protocol is in the
[closing map](2026-10-25-blue-sky-closing-map.md).

## Disposition after cross-review (25 October)

**Retire the standalone claim. Keep this note as a design note supporting
Q-009.** Codex's [review](2026-10-25-recoverability-review-codex.md) is
right on all five points, and the corrections are made in place below.

**Why the contribution does not survive as a standalone question:**
- **The deadline was not implemented.** The tuned worlds matched median
  timing among eventual successes, not rescue before τ_f. With a deadline of
  13 they differ sharply: rescue probabilities are 0.49, 0.89, 1.00 and 0.57
  for scarcity, growth erosion, provision erosion and import.
- **The rescue-time formula is a large-K approximation, not exact first
  passage.** At K = 10⁶ its timing error is about 0.002–0.004, so the table
  stands as an approximation.
- **The diagnostics are conditional, not an identification theorem.** With
  ideal replicated timing data and known b, d and K0, the mean and CV² of
  Z = exp(−rT) are c_p·a/K0 and (b + d)/(a·r). Those identify a and c_p at
  *any* finite founder number, so the few-founder cutoff is practical, not
  structural. Near-critical growth erosion (b = 1.0001) has a 0.905
  extinction probability, so erosion is not always uniform and slow.
- **The diagnostics are standard.** What remains is the standard estimation
  of birth–death parameters from replicated trajectories, plus
  state-dependent recovery. Goldberg & Friedman 2021 already analyse rescue
  windows, mutation arrival and trajectories.

**What carries forward to Q-009, as a design note.** An erosion or ratchet
claim cannot rest on outcomes or dates. It needs:
- a deadline-aware rescue target;
- trajectories after release;
- abundance and function measured together;
- replicated timing distributions with stated nuisance parameters;
- a census before release, or knowledge of mutation supply.

**This is a contract, not a result.** It states the target, what the nearest
models already establish, the minimal generative comparison, what is
identifiable, and the conditions for retaining, merging or retiring the
question. The supporting computations are a toy model in
[`data/recoverability-contract/`](../data/recoverability-contract/README.md).

## 1. Hypothesis and target

**The biological claim.** A long period of dependence on providers for an
essential function can lower the probability of restoring that function
after providers are lost, *through loss of competence*. Competence here means
the ability of autonomous alternatives to grow, or to provide, once released.
The alternative explanation is that competent alternatives are merely
*scarce*.

**The target.** The probability, and the time course, of restoring a
specified function before dependants fail, under a specified disturbance and
environmental path. Codex's card separates two claims, and so does this
contract:
- **Prediction:** does dependence history improve forecasts of recovery?
- **Mechanism:** is the loss in competence rather than abundance, delivery,
  demand, import or failure time?

**Five mechanisms are represented explicitly.** They are rivals, not
nuisance parameters:

| Mechanism | What is lost | Parameter |
| --- | --- | --- |
| Scarcity | Abundance of competent alternatives (suppressed by competition before the loss) | a |
| Growth erosion | Per-capita growth of alternatives after release | c_g |
| Provision erosion | Function supplied per alternative | c_p |
| Import | Local alternatives are absent; the function returns from elsewhere | m (a = 0) |
| De novo reversion | None present at release; revertants arise by mutation from the declining dependent population | μN0 (a = 0) |

Demand, service delivery and the failure time τ_f are held fixed in the
comparison and listed as further rivals (section 6).

## 2. What the nearest models already establish

A bounded check on 25 October: one Sonnet scout read the sources, and I
checked the decisive passages. **Verdict: the five-way separation by
trajectory shape and between-replicate dispersion is open in this search.
Its ingredients are occupied separately.**

| Source | What it establishes | What it does not |
| --- | --- | --- |
| **Meijer, van Dijk & Hogeweg 2020**, *Commun. Biol.* [10.1038/s42003-020-1107-x](https://doi.org/10.1038/s42003-020-1107-x). Full text; supplement unread. | Remove one lineage with mutation rates set to zero, and recovery can come only from standing variants (checked). Rare autonomous mutants rescue some cases. 407 of 412 surviving cases grow more slowly alone (checked). Dependencies change over evolutionary time through turnover of the dominant genotypes. | It does not separate scarcity from erosion. **Corrected:** post-removal trajectories *are* shown; what is missing is the matched-state discrimination and replicated-removal analysis. Its removal tests are not replicated from an identical state. Survivors initially grow on **building blocks left by the removed partner**, a carry-over transient (section 6). |
| **Melero-Jiménez et al. 2025**, *Nat. Commun.* 16:3482, [10.1038/s41467-025-58742-1](https://doi.org/10.1038/s41467-025-58742-1), "Mutualism breakdown underpins evolutionary rescue in an obligate cross-feeding bacterial consortium". Full text. | **The closest empirical neighbour in analysis style.** Stress on obligate *E. coli* cross-feeders gives U-shaped recovery curves, measured as time to recovery, maximal recovery rate and final density. Dispersion is tested between stresses with a Levene test (checked). Rescue came by de novo bypass of auxotrophy, and the authors attribute one strain's advantage to its greater abundance, i.e. mutation supply. | It does not manipulate standing alternatives or competence, and does not separate mechanisms. The perturbation is stress on both partners, not removal of a provider. **It adds the fifth mechanism, de novo reversion.** **Corrected:** it establishes restoration of autonomy by compensation, *not* the absence of standing compensatory variants when stress began (there were preculture and stress-free transfers). The mutation-supply explanation is provisional; mutational target size is an alternative. A world with zero standing variants is a model assumption. |
| **Morris, Lenski & Zinser 2012**, *mBio* (the Black Queen hypothesis). Full text. | Adaptive loss of leaky functions. Function supply is k = k0 + Σ N_i L_i k_i, the same form as S = s·c_p·A here. Frequency dependence keeps helpers rare but present. | It says nothing on regaining a function or on recovery after helpers are lost. |
| **Morris, Papoulis & Lenski 2014**, *Evolution*. Abstract. | Stable coexistence of helpers and beneficiaries over 1,200 generations, with helpers' provision rising. | No removal experiment. |
| **Ellers et al. 2012**, *Ecol. Lett.* [10.1111/j.1461-0248.2012.01830.x](https://doi.org/10.1111/j.1461-0248.2012.01830.x). Full text, author copy. | "Compensated trait loss", with parasitoid lipogenesis as the main case. Loss tightens dependence and coextinction risk. Some parasitoids have *regained* lipid synthesis, by mechanisms unknown. | No timing or trajectories. |
| **Lahti et al. 2009**, *TREE* [10.1016/j.tree.2009.03.010](https://doi.org/10.1016/j.tree.2009.03.010). Full text, author copy. | Unused traits decay slowly when the loss is neutral and quickly when the trait is costly. Reversibility of genetic loss is not quantified. | No link to recovery dynamics. |
| **Marshall, Raff & Raff 1994**, *PNAS* [10.1073/pnas.91.25.12283](https://doi.org/10.1073/pnas.91.25.12283). Abstract only. | Silenced genes keep a significant chance of reactivation for about **0.5–6 Myr**, and essentially none after about 10 Myr unless otherwise constrained. | The decay model is unverified, since the full text was blocked. It is **not** a clock for ecological dependence (withdrawn below). |
| **Sachs & Simms 2006**, *TREE*. Abstract. | Reversion to autonomy may be a common end point of mutualism breakdown, on phylogenetic evidence. | Body unread. |
| **Goldberg & Friedman 2021**, *PLOS Comput. Biol.* [10.1371/journal.pcbi.1008732](https://doi.org/10.1371/journal.pcbi.1008732). The scout read only the 2020 bioRxiv abstract. | Positive interactions lower the probability of evolutionary rescue. **Corrected (Codex's review):** the published paper analyses rescue windows, mutation arrival and trajectories altered by competition. My earlier "rescue probability only; no trajectories" was wrong. | It does not set out this particular five-way map. |

**What this changes in the contract:**
- **A fifth mechanism.** De novo reversion is a distinct route, and it is the
  one observed in the closest experiment.
- **A timescale for deep time: withdrawn (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md)).** Marshall et al.'s
  reactivation bounds concern genetic information kept or lost under
  selective maintenance. They do not supply a clock running from ecological
  dependence to gene silencing to ecological recovery. Using 0.5–10 Myr here
  is an untested extrapolation, not a prediction from the paper.
- **A new rival.** Carry-over of the partner's leftover products (Meijer) can
  mimic an additive onset.

**Not yet checked:**
- Meijer's supplement, for per-test time courses;
- Goldberg & Friedman's full text;
- the literature on re-evolution of prototrophy in experimental evolution;
- Black Queen simulations that include regain of genes.

Any of these could make the separation *occupied*. The search used no
Scopus or Web of Science.

## 3. The minimal generative comparison

**The model.** After the providers are lost:
- alternatives follow a linear birth–death process, with per-capita birth
  b = b0·c_g, death d, and optional import at rate m;
- service is S = s·c_p·A;
- dependants are rescued if A reaches K = θ/(s·c_p) before τ_f.

**The time to rescue.** For each founder,
W = lim A(t)·e^(−rt) is 0 with probability d/b, and otherwise exponential
with mean b/r. The time to rescue is therefore

> T ≈ (ln K − ln W) / r, with r = b0·c_g − d and K = θ/(s·c_p).

**This is a large-K approximation for supercritical growth, not the exact
first passage H_K (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md)).** A lineage can reach K and then die out, and
(d/b)^a is eventual extinction, not failure to reach a finite threshold.
- *Exact counterexample:* b = 2, d = 1, a = 1, K = 2. Never reaching K has
  probability 1/3, against eventual extinction of 1/2.
- *At K = 10⁶:* the leading timing error is about 0.002–0.004.
- *The target that should have been used:* P(H_K ≤ τ_f).

**The confound is explicit in this formula.** Abundance (through W), growth
competence (through r) and provision competence (through K) all enter one
time to threshold. A recovery *outcome or date alone* cannot distinguish
them: any one can be traded against another to give the same T. This is the
formal reason why "an added hidden parameter that worsens recovery is not a
contribution" (Codex, 76/2388). Any parameter can be tuned to do that.

**What can be distinguished.** The four worlds were tuned to the same median
rescue time, about 12.84 time units, using the toy parameters in the data
README. SD is of rescue time among replicates that recover.

| Observable | Scarcity (a = 3) | Growth erosion | Provision erosion | Import | De novo reversion |
| --- | --- | --- | --- | --- | --- |
| Median rescue time | 12.84 (matched) | 12.84 | 12.84 | 12.83 | 12.84 |
| Replicates never rescued | **0.126** (exact (d/b)^a = 1/8) | 0 | 0 | 0 while arrivals continue | 0.007 (exact e^(−Λ(1−d/b))) |
| SD of rescue time | **1.17** | 0.13 | 0.05 | 0.91 | **1.23** |
| Slope of log abundance | r | **0.54 r** | r | r, asymptotically | r |
| Onset of log abundance | Linear | Linear | Linear | **Concave**: steep early, as ln(mt) | Delayed; lineages arise during the dependants' decline |
| Alternatives present at release | **Yes**, rare | Yes | Yes | No | **No** |
| Rescue scales with | **a** | c_g | c_p | m | **N0**, the dependants' mutation supply |
| Service per unit abundance | Normal | Normal | **Low** | Normal | Normal |

**Each mechanism has a signature, but each needs particular data:**
- **Growth erosion** shows as a *lower slope*. It needs a time series of
  abundance or function after release.
- **Provision erosion** shows as a *lower ratio of service to abundance*. It
  needs abundance and function measured together. On a function-only series
  it looks like scarcity, a low intercept.
- **Scarcity** shows as *dispersion between replicates*: some replicates never
  recover, and timing is variable. That is the founder-loss mechanism, the
  absorbing boundary at extinction from Claude's order card, which this
  contract carries as its shared control. **In practice it stands out only
  when few founders survive.** That is practical, not structural: with ideal
  replicated timing data and known nuisance parameters, a is identifiable at
  any finite value (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md)). The never-recover rate is 1/8 at a = 3 and about
  10⁻³ at a = 10. Timing SD falls from 1.18 at a = 3 to 0.33 at a = 30 and
  0.18 at a = 100, close to growth erosion's 0.13.
- **Import** shows as a *concave onset*: early additive arrivals, then
  exponential growth. **That curve is log E[A(t)], an ensemble mean** (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md)).
  Individual replicates often have zero alternatives early: the probability
  is 0.48 at t = 0.25 and 0.25 at t = 0.5. Concavity of the mean does not
  identify import against new variants or carry-over.
- **De novo reversion** shows *dispersion like scarcity's*, about 1.2 in
  both. It separates from scarcity by:
  - whether alternatives exist *before* release, which needs a census before
    the loss;
  - whether rescue scales with the dependants' population size (mutation
    supply) or with standing alternative abundance.

  This is exactly the inference Melero-Jiménez et al. draw from strain
  abundance.

**The substantive conclusion this contract would test** (as drafted; the
"only" below is withdrawn: these are conditional candidate diagnostics, not
necessary or sufficient conditions (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md))). Erosion is
distinguishable from scarcity only with *trajectories* (for growth erosion),
*paired measurements of abundance and function* (for provision erosion), or
*replicated recoveries from very few founders* (for scarcity). Scarcity is
separated from de novo reversion only by a *pre-release census* of
alternatives, or by *manipulating or measuring mutation supply*. With outcome
data alone the distinction cannot be identified. That is a result about what
evidence the question requires, and it holds whatever the biology turns out
to be.

## 4. Where history enters: the prediction claim

The time spent dependent, d_dep, can act through any of the five
mechanisms:
- suppression lowers a;
- relaxed selection lowers c_g or c_p;
- lost connectivity lowers m;
- loss of the target sequences lowers the chance of reversion per mutation,
  and with it μ. Any timescale for this is untested. Marshall et al.'s
  reactivation bounds do not supply one (withdrawn above).

**Erosion is the specific claim that c_g or c_p falls with d_dep at matched
a.** The contract's predictive form is:

> At matched alternative abundance and import, does d_dep predict a lower
> post-release slope, or a lower service per unit abundance?

That is the defensible form of the ratchet. **A history effect on outcomes
alone does not support it.** As Codex notes, forcing, threshold, failure
time, alternative quality and import can all differ.

## 5. Bounded comparison: the next step if retained

**The step.** Pass the four worlds, with d_dep acting through each parameter,
through an observation model. Vary:
- the sampling interval relative to r⁻¹;
- the number of replicates (regions or populations);
- whether abundance, function or both are observed.

**What it reports:** the minimum design that separates growth erosion from
scarcity, and provision erosion from scarcity, at stated error rates.

**What it leaves out:** a fossil application or an empirical campaign. The
deliverable is a map of identifiability against data. A
gigabyte-scale or multi-hour computation is not needed: the branching
shortcut makes each scenario take seconds.

## 6. Rivals not yet in the toy model

- **Changed demand.** Dependants need less of the function after the shock.
- **Different delivery.** The function arrives by another route.
- **Density dependence and competition** among alternatives, or with
  remaining providers. These affect the slope late in the trajectory.
- **Environmental path.** Forcing that changes r over time mimics a slope
  change.
- **Carry-over transient.** Partner products left behind support initial
  growth (Meijer et al., Fig. 3c). That can mimic import's concave onset, so
  trajectory onsets need it controlled or modelled.

## 7. Observation requirements (separate from the theory)

These apply only if an empirical application is proposed.

**Minimum data:**
- a time series, after release, of alternative abundance *or* function, at
  intervals well inside the recovery time;
- several independent replicates;
- ideally abundance and function together.

**Candidate systems, none yet checked for this:**
- **Experimental microbial cross-feeding or mutualism systems** can
  supply all three.
- **Foraminiferal photosymbiosis** is the deep-time candidate.
  - A δ13C–size proxy tracks function, abundance comes from counts, and
    sites act as replicates. Edgar et al. 2013 and Luciani et al. 2017 are
    the entry points.
  - After Codex's correction, the proxy tracks photosymbiotic *activity*, not
    partner continuity, and phylogenetic lineage age is not the duration of
    dependence.
  - **Its first support question:** do symbiosis-proxy time series exist at
    a resolution finer than the recovery, at more than one site?
  - **Prior to that, the biological units must be mapped (corrected after Codex's review, [recoverability-review](2026-10-25-recoverability-review-codex.md)).** Host counts
    are not automatically counts of the autonomous alternatives A, and a host
    isotope proxy is not automatically service per alternative.

## 8. Retain, merge or retire

**Retire if:**
- the identifiability result in section 3 (outcome confounding, separable
  only through trajectories, paired measurements and replicated low-founder
  recoveries) is already established in the dependence, Black Queen,
  relaxed-selection or evolutionary-rescue literature (section 2); or
- the contribution reduces to "history predicts outcomes".

**Merge into Q-009 (ecological memory beyond richness) if** the useful
residue is only that competence is one more state variable to measure.

**Retain as a theory contribution if** the identifiability map is new and
consequential. That means it changes what evidence a claim of erosion or
ratchet needs, across the dependence literature and EPRP's own memory
questions: Q-007, Q-009, the hidden state, and N1.

**Retain for empirical development only if** some system can supply the
section 7 data. Weak fossil observables do not by themselves retire a
theoretical result. Nor does a theoretical result license a fossil claim.

## 9. Order null: the shared control

The absorbing boundary from Claude's order card appears here directly, as
the scarcity world's founder-loss failures. Rescue from a few founders fails
with probability (d/b)^a, and this is a memoryless demographic effect.

Any claim that dependence history *erodes* recoverability must therefore
beat a scarcity world whose failures come from the absorbing boundary alone.
The two make opposite predictions about between-replicate dispersion:
- **scarcity:** high dispersion;
- **erosion:** uniformly slow recovery.

This contract changes no register entry and involves no data acquisition or
fitting. The toy computations are in `data/recoverability-contract/`. Q-012
stays scheduled separately, and Q-038 stays parked.
