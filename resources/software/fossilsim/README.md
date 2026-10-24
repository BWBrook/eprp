---
id: fossilsim
name: FossilSim
kind: r-package
domain: fossil-record-forward
languages: [R]
home: https://cran.r-project.org/package=FossilSim
repo: https://github.com/fossilsim/fossilsim
paper: [10.1111/2041-210x.13170]
licence: GPL-3 (CRAN DESCRIPTION; the GitHub repository declares none)
release: {version: 2.4.4, date: 2026-02-26, checked: 2026-10-23}
maintenance: {state: active, last_commit: 2026-10-06, checked: 2026-10-23}
tier: T3
validated_uses: ["Poisson fossil sampling on complete trees (sim.fossils.poisson)", "morphotaxonomy and pseudoextinction on complete trees (sim.taxonomy)", "with TreeSim sim.bd.age, constant-rate birth-death histories, cross-checked against paleobuddy"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r, image: "eprp-sw/bench-r:t1 (sha256:926c0052…)", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [Q-004, Q-006, Q-045]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# FossilSim

## Summary

FossilSim simulates fossil records on phylogenies: Poisson and
interval-structured fossil sampling, morphotaxonomy (budding, bifurcating and
anagenetic species on a lineage tree), extant sampling, trait values, and
conversion to BEAST2, PyRate and paleotree formats. Reach for it when you need
a fossil record with known truth on a tree, or species that differ from
lineages (pseudoextinction). Tree generation comes from TreeSim or ape; in
tranche 1 we validated it with TreeSim `sim.bd.age`.

## Method

Fossils are a Poisson process along branches (`sim.fossils.poisson`) or in
intervals with their own rates. `sim.taxonomy` overlays species on a complete
tree: at each speciation event, with probability β the parent species ends
and both daughters are new (bifurcating, "symmetric"), otherwise one daughter
continues the parent (budding); anagenetic species changes occur at rate λa
along branches. This follows the FBD-range framework of Stadler et al. (2018).

## Install

CRAN binary from the Posit snapshot of 2026-10-22 in a `rocker/r-ver:4.6.1`
image ([Dockerfile](../bench/env/Dockerfile.r)). The binaries for its
dependency chain need `libuv1` (for `fs`) and `libglpk40` (for `igraph`) at
run time; the first two builds failed without them.

## Validation

Tests declared in [bench/VALIDATION.md](../bench/VALIDATION.md); results in
[bench/README.md](../bench/README.md) and `bench/results/generators/`.

| Test | Result |
| --- | --- |
| G1: TreeSim `sim.bd.age` (λ 0.3, μ 0.2, 15 Myr, 20,000 clades) against e^{(λ−μ)t} and the survival probability | pass (z = 1.95, 1.06) |
| G2: `sim.fossils.poisson` (ψ 0.5) on 7,895 surviving trees: total count and dispersion against Poisson(ψL) | pass (z = −0.48; dispersion 0.990 ± 0.048) |
| G4: distributions of extant count, species, total duration and fossils against paleobuddy | pass (KS p 0.25–0.56) |
| G5: `sim.taxonomy` (β 0.5, λa 0.1) on 2,000 trees: originations and terminations against their tree-conditional expectations | pass (z = −1.27 each) |

Under survival conditioning, morphospecies originations and terminations per
unit species time were 0.571 and 0.439, against the unconditional 0.55 and
0.45; the conditional test removes that difference, which is the survival
bias of the tree, not of the taxonomy layer.

## Strengths

- Independent of paleobuddy and agrees with it; both meet analytic truth.
- The only package found that layers budding, bifurcating and anagenetic
  species on a tree, which Q-004 (pseudoextinction) needs.
- Exports to the main inference tools (BEAST2, PyRate, paleotree).

## Weaknesses and pitfalls

- Slow per tree: about 0.08 s for `sim.fossils.poisson` and 0.1 s for
  `sim.taxonomy` on 15-Myr trees, so large studies need parallel workers.
- `sim.taxonomy` output has one row per species per edge; a species' end is
  the minimum `end` over its rows.
- TreeSim's `sim.bd.age` returns `0` for an extinct clade and `1` for a
  single surviving lineage with no extinct tips, not a tree; summaries must
  handle both.
- Time-varying rates on age-conditioned trees need another generator
  (TreeSim's rate-shift functions condition on tip number).

## Alternatives and overlap

paleobuddy simulates birth–death histories and fossils without a tree
object, with time- and environment-dependent rates. paleotree's
`simFossilRecord` covers morphotaxa and sampling. PyRate ships its own
simulator, which is not independent of PyRate.

## EPRP relevance

Truth generator for any rate or range estimator; Q-004's pseudoextinction
correction can be tested on synthetic taxonomies before real rates (lead
L-004). Not a source of empirical data.

## Citation and licence

Barido-Sottani, J., Pett, W., O'Reilly, J. and Warnock, R. (2019).
FossilSim: an R package for simulating fossil occurrence data under mechanistic
models of preservation and recovery. *Methods in Ecology and Evolution*
10, 835–840. doi:10.1111/2041-210x.13170 (checked on Crossref). GPL-3 per
CRAN.

## Verification log

- 2026-10-23 `checked`: CRAN 2.4.4 (2026-02-26) and GitHub activity by
  `landscape.py`.
- 2026-10-23 `checked`: G1, G2, G4, G5 run on `deep-server` in
  `eprp-sw/bench-r:t1`, 12 cores, 62 min including paleobuddy tests.
- 2026-10-23 `checked`: exported functions read from the NAMESPACE.
