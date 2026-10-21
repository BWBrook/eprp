## Proposal ready

The file is a standalone proposal of approximately **12,500 words**, with **22 references**, an assessment of overlap with EPRP, a detailed simulation design, an HPC plan, and explicit criteria for proceeding, narrowing or stopping the project. It is ready to deposit in the repository for consideration.

# Can hybridisation cascades turn environmental change into pulses of species loss?

**The central question is whether weakening one species boundary can cause additional species to lose their evolutionary independence through onward hybridisation.**

Consider a hypothetical radiation containing several distinct, self-maintaining species. An environmental disturbance increases reproductive contact between A and B. Their hybrid descendants might introduce combinations of mating traits, ecological characteristics or compatibility alleles that destabilise the separation between the resulting population and species C—and subsequently D.

Alternatively, those descendants might encounter barriers that contain the process. Hybridisation could occur repeatedly while the species remain distinct.

The proposed research asks **when this process propagates, when it stops, and whether the additional losses exceed what individual species’ exposure and pairwise interactions would predict**.

## Why I think this is worth investigating

The macroevolutionary possibility is that susceptibility to species loss depends on the evolving reproductive relationships within a radiation. A species’ fate could depend on changes occurring in its potential hybridisation partners, even when its own environment and demographic exposure remain similar.

That creates a route to correlated losses of independently evolving lineages. It also raises a distinction between three outcomes:

- **Loss of evolutionary independence:** formerly distinct breeding populations merge.
- **Demographic loss:** organisms and populations disappear.
- **Loss of ancestral genetic material:** pre-disturbance genomic contributions disappear.

These outcomes can diverge. Historical whitefish genomics already demonstrates that substantial genomic material from a lost species can persist within surviving species. That establishes the importance of distinguishing species persistence from ancestry retention. [pubmed.ncbi.nlm.nih.gov](https://pubmed.ncbi.nlm.nih.gov/35210577/?utm_source=chatgpt.com)

The proposed contribution is to determine whether losses of independence can **propagate across a species complex**, and what controls their magnitude.

## The novelty claim is specific—and provisional

Several close precedents substantially shaped the proposal.

McDonald and colleagues interpreted three-way ancestry in suckers as evidence of a genetic bridge. A later basin-wide study by Bangs and colleagues found rare three-way hybrids and restricted onward introgression, and judged widespread multispecies collapse improbable in that system. This gives the project both an empirical motivation and an important containment case to explain. [files.cfc.umt.edu](https://files.cfc.umt.edu/cesu/BLM/UWY/McDonald_sucker%20Genetic_frpt.pdf?utm_source=chatgpt.com)

Xiong and Mallet already show that particular intrinsic incompatibilities can erode and that this erosion can spread geographically in a **two-species system**. Their work is an essential mechanistic benchmark. The proposed extension concerns propagation across **different species boundaries**, including additional independently evolving populations. [Wiley Online Library](https://onlinelibrary.wiley.com/doi/10.1111/evo.14626?utm_source=chatgpt.com)

There is also a close ecological alternative: ten Brink’s model shows that environmental change affecting one member of a species flock can trigger wider collapse through shared resources and life-history feedbacks. The experiment therefore needs to establish what onward hybrid transmission contributes. [Wiley Online Library](https://onlinelibrary.wiley.com/doi/full/10.1111/gcb.70239?utm_source=chatgpt.com)

I did not locate the exact controlled experiment proposed here. The file treats that as a plausible research gap, with a further novelty gate before substantial implementation.

## The decisive simulation experiment

The core experiment begins with **three or four species**. That is sufficient to establish whether a change involving A and B causes a further loss involving C.

The model would evolve a stable species complex, save its complete state, and branch it into matched worlds. The main comparisons are:

| Comparison | What it resolves |
| --- | --- |
| Shared environmental forcing, with and without a focal barrier pulse | The total additional effect of perturbing the focal boundary |
| Pulse worlds with onward hybrid transmission permitted or blocked | Whether the response depends on the proposed transmission route |
| Equivalent blocking controls in sham worlds | Whether blocking specifically reduces the pulse’s effect, after accounting for background hybridisation |
| Alternative ways of replacing blocked reproduction | Whether an apparent genetic effect is mainly a consequence of reduced births or replacement genotypes |
| Ecological disturbance controls | Whether ordinary ecological feedback can explain comparable losses |

All intervention policies are assigned before the disturbance. Runs in which hybridisation fails, the focal species remain separate, or no onward transmission occurs remain in the analysis.

The hardest measurement problem is also made explicit: **a connected hybridisation graph cannot be treated as a single species**. Occasional gene exchange can coexist with persistent differentiation. The proposal therefore uses independent breeding-population and genetic estimators, continuous diagnostics, ancestry accounting, and a conservative event ledger.

A convincing result would show persistent loss of an additional independent breeding population, continued reproductive contributions from the participating sources, and a response to the transmission controls. A drop in richness alone would be insufficient.

## How it connects to deep time

The strongest initial scope is **species complexes within reproductively connected parts of a clade**. The process could affect whether episodes of diversification leave durable richness, how losses cluster within radiations, and how species-level disappearance relates to demographic and genetic loss.

The fossil extension would test which of those histories remain distinguishable after preservation, sampling, time averaging, plasticity and taxonomic classification.

Corals offer a useful starting point. Budd and Pandolfi’s Pleistocene Bahamas study provides a concrete example of fossil morphology interpreted in relation to modern species boundaries. Its inference of hybridisation is conditional, however, and it supplies an observation benchmark rather than a resolved extinction-cascade sequence. [Cambridge Core](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/F06C06E64CFF26086B13E70D843B5C3F/S0094837300022612a.pdf/overlapping_species_boundaries_and_hybridization_within_the_montastraea_annularis_reef_coral_complex_in_the_pleistocene_of_the_bahama_islands.pdf?utm_source=chatgpt.com)

**I have not verified a fossil specimen time series that could establish an ancient cascade.** The proposal makes that an explicit empirical gate. The first paper should therefore stand on its biological simulation result; an ancient-event application follows only if suitable observations can constrain it.

This scope is important to the recommendation. The candidate is strongest as a **theory-led macroevolution project with a carefully defined deep-time application**. Its direct empirical palaeobiological component is less secure at present.

## Why it fits your compute and coding-agent opportunity

The expensive work is naturally parallel: independently evolved founder histories, competing genetic architectures, intervention branches, ecological alternatives and synthetic fossil observations.

The proposal uses SLiM and tree-sequence tools as foundations. Modern SLiM supports sophisticated forward eco-evolutionary simulation, including multiple chromosomes, so much of the basic genetic machinery can be reused. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12759289/?utm_source=chatgpt.com)

The opportunity for coding agents lies in integrating that machinery with the difficult scientific interfaces: changing reproductive boundaries, explicit causal interventions, ancestry retention, ecological feedback and fossil observation. Maintaining and checking those interfaces across a large experimental programme is a substantial undertaking for an individual researcher.

Your CPU cluster is the natural main resource. The A100 is optional, potentially useful for a validated emulator or intensive observation-model calculations. The proposal includes staged CPU budgets and transparent runtime arithmetic, while distinguishing planning assumptions from measured performance.

## My recommendation

**Invest first in a bounded causal pilot.** Reproduce a relevant two-species benchmark, implement the three-/four-species experiment, and test whether the result survives defensible species measurement and alternative genetic architectures.

A positive result could establish a mechanism linking local reproductive disruption to additional lineage losses. A strong containment result could explain why hybridisation opportunities often fail to dissolve species complexes. Both would be scientifically useful if they establish general conditions rather than depend on a specially constructed example.

The file also explains where this sits beside EPRP’s Q-029 and other nearby questions. Its justification rests on the specific biological contrast: **whether a disturbance propagates through changing reproductive relationships to remove additional independent lineages, and what prevents that propagation**.
