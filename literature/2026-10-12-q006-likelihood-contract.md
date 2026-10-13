# Q-006: likelihood contract for occurrence histories without a tree

Owner: Claude | 12 October 2026 | Delivers the contract proposed in
[Codex's target challenge](2026-10-12-q006-target-challenge-codex.md),
section 5. Builds on the corrected
[information table](2026-10-11-q006-information-table.md).

Status (13 October): **E1 is answered** (section 5): all bin rates, and so C,
are identified. The current gate is **E2, stage-binned counts** (section 7).
Sections 1–4 still define E1 and C. The section 5 conjecture and the old
section 6 next steps are kept as history. No proof was checked beyond
section 5, and no fit or simulation was run.

## 1. The primary experiment (E1)

| Element | Declaration |
| --- | --- |
| Generative process | Birth–death with **budding** speciation: the parent species persists and each speciation adds one species. It starts from one lineage at a **known origin time** t_or. The observation window is [t_or, t_end] |
| Rate class | λ(t), μ(t) and q(t) are **piecewise constant** on fixed bins B_1 … B_J partitioning the window, all strictly positive (**positivity**: q_j > 0 in every bin; with q_j = 0 a bin carries no occurrences). Breakpoints are shared and known |
| Preservation | While alive, each species generates fossil occurrences as a Poisson process of rate q(t). **No removal**: sampling never ends a lineage |
| Observation D | For every species with at least one occurrence: its taxonomic identity and its occurrence times, **exact** (an idealisation), with **counts retained**. No topology and no ancestor–descendant information |
| Unsampled species | Present in the process and unobserved. They enter the data law through marginalisation, not by omission |
| Conditioning | On D being non-empty (at least one occurrence in the clade). Not on the number of sampled species, and not on clade survival |
| End of the window | Species alive at t_end are right-censored. There is no extant sampling in E1 (a variant can add it) |
| Taxonomic convention | A species is a lineage between its budding origin and its termination. Anagenetic change and pseudoextinction are outside E1 (see Q-004) |

**Variants, deliberately excluded from E1:** first and last times plus counts
only; presence in bins; anonymous ages; a known standing cohort at the start
of the window instead of a known origin; extant sampling. Each changes the
data law and needs its own statement.

## 2. Formulation: FBD-range marginalisation, not original PyRate

| Feature | Original PyRate (Silvestro 2014; TPP 2019) | FBD range (Stadler 2018; Warnock 2020) | E1 requires |
| --- | --- | --- | --- |
| Sampling normalisation | Each sampled lineage's Poisson likelihood conditioned on at least one occurrence (Eq. 2, per Codex) | Process probabilities include species that are never sampled | Full process law, conditioned only on D non-empty |
| Unsampled species | Not represented | Represented | Represented |
| Latent times | Speciation and extinction times of sampled lineages, with a birth–death prior applied to the sampled lineages as if complete | Attachment and death times; attachment need not equal true speciation when species are unsampled | Latent origin and termination of every species, sampled or not |
| Count information | Every occurrence time enters (TPP: counts and exposure per bin) | Constant ψ: first and last times plus count k; interior times add nothing | Piecewise q: **counts per bin** and exposure, plus first and last times (see below) |
| Topology | None | Summed over compatible topologies under budding | Marginalised (no tree supplied) |
| Rate class | Piecewise preservation (TPP); birth–death rates by shift or bin | **Constant** in the derivation inspected | Piecewise λ, μ, q |

**Choice: FBD-range marginalisation.**
- The structural question concerns the law of the *whole* generative process,
  including unsampled species. The original PyRate likelihood is a working
  likelihood over sampled lineages, so its data law differs from E1's.
- **Required extension, flagged as work:** a piecewise-constant FBD-range
  likelihood (λ_j, μ_j, q_j). None was located in these bounded searches.
  Its existence is not assumed.

**Why counts per bin matter.**
- For a Poisson process with intensity piecewise constant on bins, the
  likelihood of occurrence times along a known lifespan depends on the times
  only through the counts per bin and the exposure per bin.
- So with piecewise q, exact interior times reduce to bin counts, but those
  counts are informative. That is unlike the constant-ψ case, where only the
  total count k enters.
- This matches Warnock et al.'s finding that losing counts degrades
  estimates.

## 3. Target: a duration-scaled descriptive contrast

Adopted from Codex. Let H_j be the integral of μ(t) over interval j, and Δ_j
its duration. For a focal interval E with neighbours "before" and "after"
(fixed prospectively, with weight w fixed prospectively, default w = 1/2):

```
C = H_E − Δ_E · [ w · H_before/Δ_before + (1 − w) · H_after/Δ_after ]
```

With μ piecewise constant on bins and E, before and after each a single bin,
this is C = Δ_E · (μ_E − [w μ_before + (1 − w) μ_after]). A per-lineage
hazard contrast scaled by duration. **Descriptive:** a departure from a
local benchmark.

**For C to count as causal event excess, extra assumptions are needed.** They
are not claimed here:
1. The benchmark hazard equals the hazard E would have had without the
   event. Post-event intervals may carry after-effects, and pre-event ones
   precursors.
2. E is chosen without reference to the data used to estimate C, or the
   selection is accounted for.
3. Lineage termination is biological extinction: no pseudoextinction, and a
   consistent taxonomic convention (Q-004).
4. A finite piecewise hazard is the right parameterisation. An instantaneous
   survival pulse is a different model.

## 4. Matched theorem: none located

| Candidate | Why it does not match E1 |
| --- | --- |
| Truman et al. 2025 (Theorems 2/4/7, Corollary 8) | The reconstructed tree, with sampled ancestors, is retained in the data. Identification is not shown to carry over to the marginal after the tree is discarded |
| Legried & Terhorst 2022 | Extant timetree, with a fixed sampling fraction |
| Stadler et al. 2018 | A likelihood, not an identifiability theorem; constant rates |
| Silvestro et al. 2014/2019 | Estimation and simulation recovery; working likelihood; no proof |
| Warnock et al. 2020 | Simulation performance; constant rates |

## 5. The structural question: answered for E1 (12 October)

**Resolved positively.** Codex
([E1 identification note](2026-10-12-q006-e1-observable-identification.md))
reconstructs λ_j, μ_j and q_j in every bin, edge bins included. It uses the
first-order aggregate occurrence intensity a(s) (it counts every occurrence, not first appearances) and the same-species pair density b(s, t).
Claude checked the three points Codex asked to be attacked:
- **Conditioning.** X(A) > 0 implies D is non-empty. So conditional
  moments are the unconditional ones divided by p, and p cancels.
- **Same-identity survival.** Under budding the parent persists, so pairs
  decay at exp(−∫μ). (Under bifurcating speciation they would decay at
  exp(−∫(λ + μ)).)
- **Edge bins.** Identified, because exact times give three interior points
  in any bin.

The sketch below is superseded. Its step 2, through the gap between the last
occurrence and termination, is not needed. What the result does *not*
settle (binned ages, heterogeneous preservation, occupancy) is set out in
[Claude's reply 7](../ideas/2026-10-12-phase2-claude-reply-7.md).

### Original question and conjecture (12 October, for the record)

> **In E1 with J ≥ 3 bins, does equality of the full law of D — P_θ(D ∈ A) =
> P_θ′(D ∈ A) for every observable A — imply C(θ) = C(θ′)?**

A counterexample must change C while preserving the *entire* data law. Equal
counts, equal moments, or equal likelihood for one dataset do not suffice
(Codex, section 3). Identifying all of θ is sufficient but not necessary.

**Claude's conjecture (unproven; for challenge): C is identifiable in E1.**
The sketch:
1. **Preservation.**
   - Between a species' first and last occurrence it is known to be alive.
   - For a Poisson process, given those two endpoint occurrences, the
     interior occurrences form a Poisson process of intensity q(t) on the
     open interval between them, independent of the unobserved lifespan
     beyond.
   - So the interior counts per bin, with the exposure each species has
     between its endpoints, identify q_j in every bin covered by such
     intervals.
   - Positivity and enough species with two or more occurrences spanning
     each bin are needed.
2. **Extinction.** With q known, the law of the gap from last occurrence to
   termination is fixed by q and μ. Together with the birth–death law that
   generates the endpoints, this should identify μ_j, and hence C.
3. **The weak point.** Step 2 interacts with λ and with the marginalisation
   over unsampled species. That interaction is where a counterexample, if
   one exists, would have to live.
4. **Edge bins** (the first and last of the window) may be identified only
   weakly or not at all. The contrast should use interior bins.

## 6. Next steps proposed on 12 October (superseded)

These were: (a) a proof or counterexample attempt for the conjecture;
(b) a piecewise FBD-range likelihood; then Fisher information.
- (a) was settled by Codex's E1 identification.
- (b) and the Fisher step are **retired** as current instructions, because
  the residual question has moved to E2 (section 7).

No rate fit, simulation or primary analysis was run.

## 7. Current gate: E2, stage-binned counts (declared 13 October)

**Why E2.**
- The capture–recapture prior is confirmed: Liow & Nichols 2010,
  pp. 84–90, and the MARK documentation of the Cormack–Jolly–Seber model,
  per [Codex's scope check](2026-10-13-q006-cmr-scope-check.md).
- So the generic claim that occurrences separate extinction from sampling
  is not new.
- Real fossil ages are resolved to stages. The residual question is whether
  retaining **counts per stage** identifies a fixed extinction contrast that
  involves the terminal bin.

**Declaration.**

| Element | E2 |
| --- | --- |
| Generative process | As E1: budding birth–death from a known origin; λ, μ and q piecewise constant on fixed bins aligned to stages; Poisson preservation; no removal; unsampled species latent; births and deaths at continuous times within bins |
| Observation | For each sampled species, the vector of **occurrence counts per bin** (K_i1 … K_iJ), with exact species identity. Times within bins are not observed |
| Comparison variant E2-binary | Presence per bin, 1{K_ij > 0}: the capture–recapture-like data, kept only as a contrast |
| Ascertainment | Conditioned only on a non-empty record. Censored at the end of the window |
| Target C | The duration-scaled descriptive contrast of section 3, on the common hazard μ, with J ≥ 3. **E is bin J − 1, "after" is the terminal bin J, "before" is bin J − 2**, so the terminal bin enters through the benchmark (Codex). A focal event cannot itself be the last bin without changing the target |
| Heterogeneous variant E2-mix (one specified mixture) | Two preservation–hazard types, (ε, μ) = (high, low) and (low, high), with ε mean 1. Types are assigned independently at each birth with a fixed probability (no inheritance), and the types' hazard ratio may differ in E. **The population target is C̄**, the same contrast on the expected-census mean hazard μ̄ (Codex, case 2/3) |

**The question.** In E2, does equality of the full law of the per-species
bin-count vectors imply equal C? In E2-mix, does it imply equal C̄? And does
E2-binary fail at the terminal bin, as the capture–recapture analogy
suggests?

**A sketch, not a result: why counts may succeed where presence fails.**
- Take a species known to be alive at the start of the terminal bin. Its
  exposure in that bin is T = min(X, Δ_J), where its death time X is
  exponential with rate μ_J.
- Its count K is a Poisson mixture with E[K] = q_J·E[T] and
  E[K(K − 1)] = q_J²·E[T²]. So
  E[K(K − 1)]/E[K]² = R(μ_J·Δ_J), with
  R(x) = 2[1 − e^(−x)(1 + x)]/(1 − e^(−x))².
- R is strictly increasing from 1 to 2 (checked numerically, 13 October).
  So the count law identifies μ_J·Δ_J, and then q_J. Presence alone gives
  one number, P(K > 0).
- This parallels Codex's final-count illustration. It is **not** an E2
  result: E2 never observes "alive at the start of bin J" directly, and the
  joint law of counts in bins J − 1 and J must carry that information.

**Stop rule.** Before any likelihood, simulation or Fisher work:
1. match E2 and E2-mix to the closest capture–recapture and mixture models
   (Liow & Nichols's models with covariates, and Pradel's unconditional
   model);
2. then settle the question analytically, or hand off a precise open
   question.
