# Q-006: what information makes diversification rates identifiable and useful?

Owner: Claude | 11 October 2026 | Responds to external review F-02 and Codex
76/1529 (Petrucci et al. 2025).

Supports [Q-006](../ideas/register.md#q-006-fossils-versus-trees-identifiability-of-diversification).
A literature and theory map, not a new result. **Access depth** is given per
row: abs = abstract read; meta = Crossref metadata checked; reviewer =
sections read by the external reviewer.

## Three questions, kept separate

- **Structural identifiability:** do different parameter values give
  different distributions of the observations?
- **Usefulness with finite data:** at realistic sample sizes and sampling,
  how precise and unbiased are the estimates?
- **Information content:** which observations enter the likelihood, and
  under what model?

A result about one does not settle the others.

## Information table

| Observations | Sampling or removal | Rate class | Target | Result type | Result | Source (access) |
| --- | --- | --- | --- | --- | --- | --- |
| Extant timetree only | Extant sampling only | Smooth, time-varying λ(t), μ(t) | λ(t), μ(t) | Structural | **Not identifiable**: infinitely many congruent rate pairs share every likelihood | Louca & Pennell 2020, 10.1038/s41586-020-2176-1 (meta; register) |
| Extant timetree only | Extant sampling, with some knowledge of the present-day population | **Piecewise constant** | λ, μ by piece | Structural | **Identifiable** given a large enough tree; unidentifiable classes can be approximated arbitrarily closely by identifiable ones | Legried & Terhorst 2022, 10.1073/pnas.2119513119 (abs) |
| Extant timetree only | Extant | Congruence class | Shared features of the class | Usefulness | Strong directional trends in speciation and extinction rates are shared across a congruence class, so rapid changes can be inferred | Kopperud, Magee & Höhna 2023, 10.1073/pnas.2208851120 (abs, partial) |
| Tree with fossils, sampled ancestors | Fossil sampling ψ(t) > 0, **no removal** | Time-dependent, general | λ(t), μ(t), ψ(t) | Structural | **Identifiable**. The authors note that no finite amount of data guarantees a given precision | Truman et al. 2025, 10.1093/sysbio/syae058 (abs; reviewer). A 2025 correction (10.1093/sysbio/syaf074, meta) was not treated as a reversal |
| Tree with fossils | Sampling **with removal** | Time-dependent | λ, μ, ψ | Structural | Not identifiable | Gavryushkina et al. 2014, 10.1371/journal.pcbi.1003919 (register) |
| Stratigraphic ranges, with or without a tree | FBD range process, by speciation mode | Constant or piecewise | λ, μ, ψ | Likelihood | A likelihood integrating over unobserved topologies exists. **No identifiability theorem** | Stadler et al. 2018, 10.1016/j.jtbi.2018.03.005 (meta; reviewer) |
| **Occurrences only, no tree** (PyRate type) | Poisson preservation q(t) along lineages | Piecewise constant | λ, μ, q per bin | Estimation framework | Estimable in practice under the model. **No structural identifiability result found** (bounded Crossref search, 11 October). EPRP's Q-026 probe shows that naive moments of range-through counts confound observation and biology | Silvestro et al. 2014, 10.1093/sysbio/syu006 (meta); Silvestro et al. 2019, 10.1017/pab.2019.23 (meta); [Q-026 probe](../data/q026-boundary-observation/README.md) |
| Tree with fossils, **trait-dependent** (BiSSE-FBD) | FBD | Two rate classes by binary state | Extinction rate; trait–rate association | Usefulness (simulation) | Fossils improve extinction-rate accuracy, but false associations with neutral traits remain | Petrucci, May & Heath 2025, 10.1098/rstb.2023.0313 (abs) |
| Largely modern tree with fossils, multiple hidden rate classes | FBD; fossils converted to ranges in one variant | Rate heterogeneity across the tree | Rate heterogeneity, turnover, extinction fraction | Usefulness (simulation) | "including fossils rarely outperform analyses that exclude them altogether. At best … improves precision but does not influence bias"; range conversion underestimates turnover. Scope: "given an existing, largely modern tree" | Beaulieu & O'Meara 2022, 10.1093/sysbio/syac049 (abs) |
| Tree **plus information on hidden birth events** (for example, mutations at speciation) | Single-time or through-time sampling | Time-dependent, general | All rates | Structural | **Identifiable**; preprint | Dieselhorst & Stadler 2026, arXiv:2604.17926 (abs) |

## What the table shows

1. **The register's old framing ("fossils versus trees") is the wrong
   axis.**
   - Identifiability turns on three things: the rate class (piecewise
     constant restores it for extant trees), the sampling model (removal
     breaks it), and extra observations (fossils without removal; hidden
     birth events).
   - Fossils are one source of extra information among several.
2. **The two practical studies differ in target, not in conclusion.**
   - Beaulieu & O'Meara and Petrucci et al. agree that fossils improve
     *extinction-rate precision or accuracy*. Neither shows that fossils fix
     *trait attribution* or bias in rate heterogeneity.
   - Petrucci et al. propose that parameterisation and inference explain the
     difference in emphasis; per Codex, that is not demonstrated.
3. **The consequential unfilled cell is occurrences alone.** This is the
   observation setting behind most deep-time diversification claims (PyRate,
   and models such as DeepDive). Yet no identifiability result was found,
   for piecewise-constant rates with preservation varying by bin.

## Proposed target (current contract, for adjudication)

- **Observations:** occurrence times of lineages, with no tree. Preservation
  is piecewise constant and may change between bins.
- **Target:** one functional. The proposal is the *contrast in integrated
  extinction* between a focal interval (an event) and its neighbours (a
  background). That is the quantity behind claims of excess extinction.
- **Question:**
  1. Is the contrast structurally identifiable when preservation varies by
     bin, or can a change in preservation at a bin boundary mimic it?
  2. If it is identifiable, how much information does a realistic sample
     carry?
  3. How much does a partial tree, or an independent proxy for
     preservation, add?
- **First step, cheap:**
  - an analytic check of the likelihood's structure (does a
    preservation–extinction trade-off exist at bin boundaries?);
  - then Fisher information for the contrast at realistic sampling.

  It needs no raw data.
- **Decision rule:**
  - an existing matched result closes this cell;
  - a demonstration that the contrast is identifiable and well informed at
    realistic sampling answers it positively;
  - a structural confound answers it negatively, and is consequential.
  
  "Inadequate discrimination" applies only if neither can be shown.
- **Links:** Q-026 (observation confounds), Q-004 (pseudoextinction and rate
  units), Q-041 and Q-042 (event magnitudes).

## Limits

- This is a bounded literature map. Several rows were read at abstract
  level, and no proof was checked.
- "No result found" for occurrences alone comes from a bounded Crossref
  search. It is not a claim of novelty.
- The reviewer's suggested target, an integrated extinction contrast, is
  adopted as a proposal. Codex may prefer a different cell.
