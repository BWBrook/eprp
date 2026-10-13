# Q-006: what information makes diversification rates identifiable and useful?

Owner: Claude | 11 October 2026; corrected 12 October after
[Codex's source challenge](2026-10-12-q006-target-challenge-codex.md) | Responds to external review F-02 and Codex
76/1529 (Petrucci et al. 2025). The next step is the
[likelihood contract](2026-10-12-q006-likelihood-contract.md).

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
| Extant timetree only | **Fixed, known** present-day sampling fraction | **Piecewise constant**, with at most K breakpoints | λ, μ by piece | Structural | **Identifiable**: distinct models in the class give distinct distributions, given a sufficient tree size condition (n > 8K in the source's notation). That is identification, not precision. Unidentifiable classes can be approximated arbitrarily closely by identifiable ones | Legried & Terhorst 2022, 10.1073/pnas.2119513119 (abs; conditions per Codex's full read) |
| Extant timetree only | Extant | Congruence class | Shared features of the class | Usefulness | Strong trends were shared among the *sampled* congruent models, conditional on recovering the class correctly. That is robustness within a sample, not an invariant of the class | Kopperud, Magee & Höhna 2023, 10.1073/pnas.2208851120 (abs) |
| Extant timetree only | Extant | Congruence class, sampled jointly | Same | Usefulness | **Adverse follow-up.** Sampling speciation and extinction trajectories jointly finds that rapid changes need not be conserved. Uses a time-discretised approximation | Andréoletti & Morlon 2023, 10.1111/2041-210X.14240 (abs) |
| Tree with fossils, sampled ancestors | Fossil sampling ψ(t) > 0, **no removal** | Time-dependent, general | λ(t), μ(t), ψ(t) | Structural | **Identifiable**. The authors note that no finite amount of data guarantees a given precision | Truman et al. 2025, 10.1093/sysbio/syae058 (abs; reviewer). A 2025 correction (10.1093/sysbio/syaf074, meta) was not treated as a reversal |
| Tree with fossils | Removal at sampling with **unknown** probability r(t) ≠ 0 | Time-dependent | λ, μ, ψ, r | Structural | **Not identifiable** (Theorem 7) | Truman et al. 2025 (main text read by Claude, 12 October) |
| Tree with fossils | Removal with a **fixed, known** r(t) ≠ 1 almost everywhere | Time-dependent | λ, μ, ψ | Structural | **Identifiable** (Corollary 8). *Correction:* the first version said that removal breaks identifiability; that holds only when removal is unknown | Truman et al. 2025 (main text read by Claude); Gavryushkina et al. 2014, 10.1371/journal.pcbi.1003919 (register) |
| Stratigraphic ranges with fossil counts, no tree | FBD range process (budding); entirely unsampled species represented | **Constant** (the derivation inspected; a piecewise version was not located) | λ, μ, ψ | Likelihood | Sums over compatible topologies, with latent attachment and death times. **No identifiability theorem** | Stadler et al. 2018, 10.1016/j.jtbi.2018.03.005 (meta; Corollary 6 read by Codex) |
| Same, with incomplete species sampling | FBD range | Constant | Tree-wide λ, μ | Usefulness (simulation) | Performs well when fossil counts are known. Degrades when counts are replaced by sampled-bin presence: underestimated counts bias rates low. Non-uniform preservation fitted as constant also degrades it. **Omitted from the first version** | Warnock, Heath & Stadler 2020, 10.1017/pab.2020.12 (abs; full text read by Codex) |
| **Occurrence histories assigned to lineages, no tree** (PyRate type) | Poisson preservation; each sampled lineage conditioned on at least one occurrence; entirely unsampled species not represented (original formulation) | Piecewise-constant preservation (TPP, 2019) | λ, μ, q per bin | Estimation framework | Joint estimation and simulation recovery; **no structural proof** found (bounded searches, 11 and 12 October). EPRP's Q-026 probe shows a confound in *selected summaries* (moments of range-through counts). It cannot settle identification of the full history | Silvestro et al. 2014, 10.1093/sysbio/syu006; 2019, 10.1017/pab.2019.23 (meta; model sections read by Codex); [Q-026 probe](../data/q026-boundary-observation/README.md) |
| **E1: exact, species-assigned occurrence times with counts, no tree** (EPRP declared experiment) | Common Poisson preservation q(t), no removal; unsampled species latent; conditioned on a non-empty record | Piecewise-constant λ, μ, q (budding) | All bin rates, hence C | Structural | **Identifiable**, edge bins included, from the first-order aggregate occurrence intensity and the same-species pair density (12 October). It is the continuous-time analogue of capture–recapture survival estimation, which is confirmed as conceptually occupied (Liow & Nichols 2010, pp. 84–90; MARK CJS documentation; Codex's [scope check](2026-10-13-q006-cmr-scope-check.md)). Stage-binned counts (E2) are not yet analysed: a binary capture–recapture terminal confound does not automatically transfer to counts | Codex, [E1 note](2026-10-12-q006-e1-observable-identification.md), checked by Claude; CMR precedents in [reply 7](../ideas/2026-10-12-phase2-claude-reply-7.md) |
| Tree with fossils, **trait-dependent** (BiSSE-FBD) | FBD | Two rate classes by binary state | Extinction rate; trait–rate association | Usefulness (simulation) | Fossils improve extinction-rate accuracy, but false associations with neutral traits remain | Petrucci, May & Heath 2025, 10.1098/rstb.2023.0313 (abs) |
| Largely modern tree with fossils, multiple hidden rate classes | FBD; fossils converted to ranges in one variant | Rate heterogeneity across the tree | Rate heterogeneity, turnover, extinction fraction | Usefulness (simulation) | "including fossils rarely outperform analyses that exclude them altogether. At best … improves precision but does not influence bias"; range conversion underestimates turnover. Scope: "given an existing, largely modern tree" | Beaulieu & O'Meara 2022, 10.1093/sysbio/syac049 (abs) |
| Tree **plus information on hidden birth events** (for example, mutations at speciation) | Single-time or through-time sampling | Time-dependent, general | All rates | Structural | **Identifiable**; preprint | Dieselhorst & Stadler 2026, arXiv:2604.17926 (abs) |

## What the table shows

1. **The register's old framing ("fossils versus trees") is the wrong
   axis.**
   - Identifiability turns on three things: the rate class (piecewise
     constant restores it for extant trees), the sampling model (an
     *unknown* removal probability breaks it; a fixed, known one below 1
     does not), and extra observations (fossils without removal; hidden
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
   - *Correction (Codex).* "Occurrences alone" is several different
     experiments, not one cell:
     - all occurrence times assigned to lineages;
     - first and last times plus a count;
     - presence in bins;
     - anonymous ages.
   - Whether entirely unsampled species are represented also differs
     between PyRate and FBD ranges.
   - The [likelihood contract](2026-10-12-q006-likelihood-contract.md)
     declares one experiment.

## Proposed target (current contract, for adjudication)

- **Observations:** occurrence times of lineages, with no tree. Preservation
  is piecewise constant and may change between bins.
- **Target:** one functional, now the *duration-scaled* descriptive
  contrast C defined in the
  [likelihood contract](2026-10-12-q006-likelihood-contract.md).
  - An unscaled difference of integrated hazards is not an event departure
    when interval durations differ (Codex).
  - C is a departure from a local benchmark. Calling it causal event excess
    needs further assumptions.
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
