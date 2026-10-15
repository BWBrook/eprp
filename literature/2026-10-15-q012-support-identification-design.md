# Q-012 (with D1): support count and identification design

Owner: Claude | 15 October 2026 | The next decision in Q-012's
[current contract](../ideas/register.md#q-012-heritable-susceptibility-versus-intrinsic-ageing-in-extinction-risk),
after the [prior check](2026-10-14-q012-prior-check.md). It folds in Codex's
blue-sky D1: speciation as a reset of vulnerability, or its transmission. It
carries the lessons of B-001 and B-003:
- definitions come before counting;
- planning numbers are not information bounds;
- a power gate needs false-decision and coverage criteria.

Status: **a support count and design contract.** Relative pairs were counted.
No durations were compared between relatives, and no model was fitted.

## 1. Data

- **Source:** Lamyman, Fordham & Pearson 2026, supplementary data, latest
  version: Zenodo record 21414007 (concept 10.5281/zenodo.18854730), CC BY
  4.0, 17 July 2026.
  - The archive is 1,162,702,765 bytes, with provider MD5
    `45350e95…3b3c3c`.
  - An earlier version is record 18854731 (March 2026, 1,098,100,706 bytes). The latest is used.
- **Retrieval:** four small members were taken from the remote archive by
  HTTP range requests, checked against the zip's own CRCs. The archive was
  not downloaded whole. They are git-ignored in `data/raw/lamyman2026/`:

  | Member | sha256 |
  | --- | --- |
  | S1, Morphospecies Key Information.xlsx | `88cd9b0a…f05d84` |
  | S3, Supporting Data.xlsx | `2412991d…a7366b` |
  | S6, All_Species_Lineages.nex | `e8bb5da6…38ad95` |
  | S6, All_Species_Morphospecies.nex | `3a0867e0…09ce3` |

- **S1 has 482 morphospecies.** Each row has its ancestor, the ancestry
  evidence (406 significant, 9 strong, 67 speculative), start and end ages
  (GTS2020) with references, a morphogroup and ecogroups.
- **Reconciliation needed.** S3's summary reports 480 Cenozoic
  morphospecies and 268 lineages in "this study", against 339 and 210 in Aze
  et al. 2011. S1's 482 rows need reconciling with that figure before
  analysis.
- **Durations are compiled ranges, not occurrence-based ranges.** Triton is
  a later, independent check of range ends (section 5).

## 2. Support (counted on 15 October; no outcome comparison)

| Unit | Count |
| --- | ---: |
| Parent–daughter pairs (ancestor present in the table) | 471 |
| … with the parent persisting after the daughter appears (budding) | 453 |
| … with the parent ending exactly at the daughter's start (anagenetic naming or bifurcation) | 18 |
| … both members extinct | 365 (333 with non-speculative ancestry) |
| Sister pairs | 323, from 107 sibships |
| … both members extinct | 249 (214 non-speculative) |
| Extant morphospecies (right-censored, kept) | 73 |
| Relatives in *different* dominant ecogroups | 134 of 323 sister pairs; 150 of 471 parent–daughter pairs |

- Sibship sizes:

  | Daughters | 2 | 3 | 4 | 5 | 6 | 7 |
  | --- | ---: | ---: | ---: | ---: | ---: | ---: |
  | Sibships | 63 | 24 | 11 | 5 | 2 | 2 |

  178 parents have one daughter.
- The median duration of extinct morphospecies is 6.2 Myr.
- **Pairs are not independent replicates.** They nest within sibships and
  the tree. The unit of replication is the tree structure, so inference
  must be tree-structured, not built on counts of pairs.
- Even so, support is an order of magnitude beyond B-001's or B-003's.

## 3. Estimand

**Inherited frailty along the tree.**
- Each morphospecies i has a hazard h_i(a, t) = z_i h₀(t, e_i) g(a), where:
  - a is the species' age;
  - t is calendar time;
  - e_i is its ecogroup;
  - z_i is its frailty.
- Log frailty is inherited: log z_d = ρ log z_p + √(1 − ρ²) ε, with
  ρ ∈ [0, 1).
- **Primary estimand: ρ.** ρ = 0 is "reset" in D1's terms: susceptibility is
  renewed at budding. ρ > 0 is transmission.

**Two internal consistency checks follow from vertical inheritance:**
- sisters' frailty correlation should be about ρ², given that each inherits
  independently from the parent;
- the correlation should not decay with the gap between relatives'
  origination times.

**Secondary estimand: held-out predictive skill.** This is the gain in
log-score from the inherited model over the non-inherited one, when whole
sibships or clades are held out of the fit.

**D1's event-level signature: parent age at budding.**
- With inherited frailty and survivorship, parents that are old when they bud
  are selected for low frailty, so their daughters should last **longer**.
- An inherited ageing clock predicts the opposite sign.
- A reset predicts no association.
- Calendar-time exposure is absorbed by h₀.

## 4. Rivals, matched on marginal durations, and how they are separated

| Rival | Mechanism | Signature |
| --- | --- | --- |
| R0. Intrinsic ageing | g(a) varies; no frailty | No relative dependence beyond h₀ |
| R1. Frailty, not inherited | z drawn independently | The same marginal decline in hazard with age (the Gamma-frailty equivalence); no relative dependence |
| R2. Inherited frailty | ρ > 0 | Relative dependence that survives a different ecogroup and a long origination gap; sisters ≈ ρ²; positive parent-age signature |
| R3. Shared exposure | Variation in h₀ by time, ecogroup and finer habitat; no inheritance | Dependence that decays with origination gap and vanishes across ecogroups; time-matched non-relatives show it too |

**Separating them.** Survival curves alone cannot separate R0 from R1. The
relatives can, through four levers:
1. a baseline h₀ by calendar time and ecogroup;
2. the 134 sister and 150 parent–daughter pairs that differ in ecogroup;
3. **decay with origination gap**: shared exposure decays as relatives'
   start times separate, and inheritance does not;
4. **time-matched non-relative controls**: pairs originating in the same
   window and ecogroup, in different clades. They estimate the residual
   shared exposure, and inheritance must exceed it.

**Selection from parents surviving to bud.**
- A parent is known to have survived to its last budding event.
- The likelihood therefore treats each lineage's duration as left-truncated
  at its last observed budding. The simulation applies the same
  conditioning.
- Ancestry is inferred partly from stratigraphic order, so long-ranging
  species may be likelier to be named ancestors. The generator must include
  a rule for assigning ancestors, and the "speculative" ancestry links are a
  sensitivity subset.

## 5. Observation model

- **Range ends:** compiled from the literature, with age uncertainty. Triton
  (held in the repository) is a later check, through occurrence density near
  range ends.
- **Morphospecies against lineages:**
  - the 18 parent-ends-at-daughter-start pairs are D1's "naming" class.
    Their parent end is treated as a pseudo-extinction, so censored, not
    extinction;
  - the lineage tree (S6) is the sensitivity analysis.
- **Ancestry evidence:** results are reported with speculative links
  included and excluded.
- **Extant species** are right-censored at 0 Ma.

## 6. Discrimination check, before ρ is estimated

1. **Freeze everything first:**
   - the priors;
   - the working values ρ₀ = 0.1 (negligible) and ρ₁ = 0.4 (consequential:
     a parent's frailty explains at least 16% of its daughter's);
   - the baseline structure;
   - the truncation and ancestor rules.

   These are working scenarios. Codex may challenge them.
2. **Simulate on the actual topology and budding times** under R0, R1, R3,
   R2 at ρ₀, R2 at ρ₁, and R2 at 0.7. Durations are simulated conditional on
   each parent surviving to its last budding.
3. **Proceed only if all of these hold**, each with Monte Carlo uncertainty:
   - **Power:** P(lo > ρ₀ | ρ₁) ≥ 0.8, and P(hi < ρ₁ | R1) ≥ 0.8;
   - **False decisions:** P(lo > ρ₀) ≤ 0.05 under R0, R1, R3 and R2 at ρ₀.
     R3 is the decisive control;
   - **Coverage** close to nominal across the grid.

   The grid is finite, so it is not a uniform bound.
4. **Compute.** The check is local and moderate: a tree of about 480 tips and
   hundreds of replicates. It fits on this machine or on deep-server.

## 7. Outcomes

- **Inheritance supported:**
  - lo > ρ₀;
  - with dependence surviving both the ecogroup and origination-gap levers;
  - and held-out skill above the non-inherited model.
- **Informative negative:** hi < ρ₁. No consequential inherited
  susceptibility is detected beyond shared exposure, which is D1's reset
  answer at this grain.
- **Inadequate:** the interval spans both values, or the check fails. Q-012
  then parks at this grain.
- **D1's sign** is reported descriptively, with its interval.

## 8. Next steps

- Codex reviews this design once.
- Then, in order:
  1. reconcile the 482 and 480 counts;
  2. freeze the section 6 inputs;
  3. run the discrimination check.
- No estimation of ρ, and no comparison of relatives' durations, before the
  check passes.
