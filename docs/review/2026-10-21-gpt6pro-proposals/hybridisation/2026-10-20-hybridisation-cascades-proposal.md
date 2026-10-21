# Can hybridisation cascades turn environmental change into pulses of species loss?

## A simulation-led proposal on the collective stability of species boundaries

**Prepared for:** Barry W. Brook and the Claude/Codex research agents working in EPRP  
**Date:** 20 October 2026  
**Status:** First research proposal; suitable for a bounded theory pilot, with novelty and empirical feasibility gates  
**Portfolio position:** A mechanism-specific offshoot adjacent to Q-029; no new register identifier assigned  
**Primary domain:** Macroevolution of sexually reproducing species complexes, with a conditional Cenozoic fossil application  
**Working short name:** Hybridisation cascades

> **The question:** Can a temporary weakening of one species boundary cause other species to lose their evolutionary independence, even though those other boundaries would usually persist under the same environmental disturbance?
>
> **The proposed contribution:** Establish when such losses propagate across different species boundaries, when genetic and ecological barriers contain them, and whether the resulting histories can be distinguished from demographic extinction after fossil preservation and sampling.

This is a proposal for research, not a report of simulated results. Numerical settings, precision targets and resource budgets below are proposed design choices unless explicitly attributed to a source. No simulation performance, empirical parameter fit or ancient cascade is claimed.

## Contents

1. [Executive proposal](#1-executive-proposal)
2. [Why this is a macroevolution question](#2-why-this-is-a-macroevolution-question)
3. [Relationship to EPRP](#3-relationship-to-eprp)
4. [What is already known, and the residual novelty](#4-what-is-already-known-and-the-residual-novelty)
5. [Definitions and falsifiable hypotheses](#5-definitions-and-falsifiable-hypotheses)
6. [The simulation model](#6-the-simulation-model)
7. [Causal experiments and estimands](#7-causal-experiments-and-estimands)
8. [Simulation campaign and analysis](#8-simulation-campaign-and-analysis)
9. [Fossil observation and empirical feasibility](#9-fossil-observation-and-empirical-feasibility)
10. [Implementation and HPC plan](#10-implementation-and-hpc-plan)
11. [Work packages, decision gates and stopping rules](#11-work-packages-decision-gates-and-stopping-rules)
12. [Expected scientific products](#12-expected-scientific-products)
13. [Risks and questions for independent review](#13-risks-and-questions-for-independent-review)
14. [Evidence and search audit](#14-evidence-and-search-audit)
15. [References](#15-references)

---

## 1. Executive proposal

I recommend investigating **the collective stability of species boundaries in young or partially interfertile radiations**.

Imagine a region containing several recognisably distinct, self-maintaining species. Their reproductive barriers are strong enough to preserve differentiated breeding populations, but occasional hybridisation remains possible. Environmental change brings two species into greater reproductive contact or weakens a barrier between them. Their hybrids might merely disappear, exchange a few alleles, rescue a declining population, form a new species, or cause the original pair to merge.

The proposed question begins at the next step. Could descendants of that initial hybridisation alter compatibility, mating behaviour or reproductive encounter rates sufficiently to destabilise **additional** species? A local disturbance might then remove more independently evolving lineages than its direct effects predict. Conversely, multilocus incompatibilities, ecological differentiation or spatial separation might make such propagation exceptionally difficult.

Both answers would matter. A robust propagation regime would identify a route from environmental change to clustered species loss. A robust containment result would explain why widespread hybridisation need not imply wholesale dissolution of species complexes.

The central experiment is possible only in a model: evolve a stable multispecies system; save its complete state; branch it into matched worlds; perturb a focal reproductive barrier; and selectively prevent onward transmission from the resulting hybrids in additional branches. This supplies the counterfactuals unavailable in a historical extinction sequence.

The scientific target is **causal amplification across distinct species boundaries**. It is not simply the presence of hybrids, a connected hybridisation network, retained alleles from a lost species, or the geographical spread of incompatibility collapse within one species pair.

The most relevant existing results make the project sharper:

- A three-species genetic bridge has already been proposed empirically, and a broader subsequent study substantially challenged its importance in that system. [1] [2]
- Particular intrinsic incompatibilities can erode, and that erosion can spread spatially within a two-species system. This need not itself establish whole-species fusion. [3]
- Environmental change affecting one member of a species flock can already cause an ecological collapse cascade. [10]

The new experiment must distinguish its mechanism from all three.

**Recommended project shape:** a theory-led first paper, followed by a fossil observability extension only if the biological result and available observations justify it. The initial biological scope is species complexes within reproductively connected parts of a clade. The project should not be sold as an explanation for the disappearance of distantly related families and orders during the Big Five.

**Why it suits the available resources:** the demanding work consists of many independent evolutionary histories, intervention branches, genetic architectures and observation replicates. This is well matched to CPU ensembles on kunanyi. Existing forward genetic simulation software supplies much of the low-level machinery; coding agents can integrate it with ecological dynamics, ancestry accounting, experiment orchestration and adversarial validation. The A100 is optional.

**The first investment should be finite:** reproduce a relevant two-species benchmark, build a three-species causal experiment, and determine whether the result survives a defensible species criterion. A continent-scale simulator is unnecessary at this stage.

## 2. Why this is a macroevolution question

### 2.1 The possible missing state variable

Many questions about diversification can be formulated in terms of the production and loss of independently evolving lineages. A lineage's vulnerability could depend on more than its own population size, environmental tolerance or geographic range. It could also depend on **which partially compatible lineages surround it, and how their genomes and mating systems change**.

This yields a concrete macroevolutionary hypothesis: the risk of losing reproductive independence is a property of an evolving multispecies system, with potentially nonlinear responses to a disturbance. A model in which each species experiences an independent extinction hazard could then miss an important source of correlated species loss.

The important unit is not every possible pairwise boundary. If four species become one breeding population, richness falls by three, not by the six pairwise distinctions that disappear. Counting boundaries naively would manufacture apparent amplification.

### 2.2 Three consequences that need separate accounting

A decline in species richness can accompany very different changes:

| Axis | Question | Example of what it does not establish |
| --- | --- | --- |
| Evolutionary independence | How many persistently differentiated breeding populations remain? | The existence of fertile hybrids does not itself show that an independent population has disappeared. |
| Demographic survival | How many organisms, recruits and occupied populations remain? | Stable total abundance does not imply that all formerly independent species persist. |
| Ancestral genetic retention | How much pre-disturbance genomic material remains, where, and at what abundance? | A surviving fragment of ancestry does not mean that the source species survives. |

These axes need not move together. They should not be forced into three mutually exclusive categories. In particular, after extensive admixture, “demographic extinction of the ancestral species” depends on an identity convention. The loss of individuals bearing a pure founder label is not a label-free measure of death.

Historical whitefish genomics already shows that appreciable genomic material from a lost species can persist within surviving species. Retention itself is therefore established background, not this project's novelty. [13]

The macroevolutionary contribution would be to establish **when the independent-lineage axis behaves collectively**, and to quantify its relationship to the other two axes under known causes.

### 2.3 Deep-time relevance and its limits

The mechanism could matter during repeated episodes of secondary contact, habitat compression or altered reproductive timing in taxonomically shallow radiations. Over geological time, such episodes could affect which bursts of speciation leave durable diversity.

Three conditional implications are worth testing:

1. **Clustered vulnerability.** Species with many ecologically overlapping, partially compatible neighbours could experience correlated losses even after accounting for their individual demographic exposure.
2. **Species-level selectivity.** Loss could concentrate within young or porous species complexes, leaving a different species-to-genus pattern than mortality distributed across reproductively disconnected clades.
3. **Decoupled recovery measures.** Census or morphological breadth might recover while the number of independently evolving lineages remains reduced.

These are predictions of the proposed mechanism, not descriptions of demonstrated ancient events. Young clade age is also an imperfect proxy for reproductive compatibility. It should not substitute for modelling barriers.

The primary fossil application should be a **Cenozoic coral species-complex problem**, where morphology and modern reproductive biology offer some leverage. A Pleistocene coral study provides an observation benchmark, while an older, sufficiently resolved turnover sequence remains an empirical acquisition gate. [15] This is a macroevolution project with deep-time implications and an explicit route to palaeobiological testing; it does not require claiming that a particular mass extinction was caused by fusion.

### 2.4 Why the opportunity is timely

The opportunity is integration and experimental coverage. Suitable simulation engines and relevant biological ideas already exist. SLiM now supports sophisticated forward eco-evolutionary simulations, including multiple chromosomes; its use here should be grounded in a pinned, tested version rather than a new population-genetic engine. [19]

Coding agents can make it practical for a small scientific team to maintain the experiment across genetics, ecology, species delimitation, ancestry analysis, fossil sampling and HPC execution. Their benefit is the ability to build and check these interfaces, explore competing mechanisms, and keep the resulting work reproducible.

More computational capacity is useful only after the scientific contrast is secured. Large ensembles cannot repair a circular species definition or identify ancient hybridisation from observations that contain no such information.

## 3. Relationship to EPRP

The portfolio was reviewed as context, including the applied and blue-sky registers, status, evidence guidance and capability inventory. Repository references below are pinned to commit **3d432f0aabef19c9d8e07928aa93e14fe83e06a8**, observed on 20 October 2026. This document is an external proposal for consideration; it does not change the portfolio's decisions or ownership.

| Existing entry | Proximity | What this proposal would have to add |
| --- | --- | --- |
| **Q-029: isolation, reconnection and durable diversity** | Closest overlap. The entry is parked because broad timing mechanisms are occupied. It already identifies Freitas et al. [11]. | A specific biological contrast: does a focal change cause additional boundary failures through hybrid descendants? Shared forcing is held constant in the causal comparison. Generic reconnection timing is insufficient novelty. |
| **Q-004: pseudoextinction-corrected background rates** | Both concern the interpretation of disappearance. | Biological many-to-one loss of reproductive independence differs from anagenetic renaming. The proposed simulation does not assume that Q-004's correction applies to reticulate histories. |
| **Q-022: evolutionary history lost with extinction** | Ancestral retention complicates correspondence between taxon loss and genealogical loss. | Explicit genomic ancestry accounting, used to interpret the cascade. This does not claim to replace a tree-based PD analysis with an empirically identified ancient network. |
| **Q-043: survivor composition and subsequent evolution** | Retained variation could affect later diversification. The broad question is parked. | Reradiation is a secondary outcome. Making it the central claim would collide with existing fusion–fission research. [12] [14] |
| **Q-020: spatial synchrony and extinction insurance** | Geography and shared forcing can affect contact. | The new causal mechanism is onward genetic transmission, not the synchrony of refugial habitat loss. |
| **B-005: climate/geography versus diversity dependence** | Both could use individual-based evolutionary simulations. | The focal estimand is collective boundary failure. A larger generic diversity simulator is not the contribution. |

**Recommendation for the register:** assess this as a mechanism-specific candidate adjacent to Q-029, while preserving Q-029's current parked status. It should earn a separate pilot only if its precise causal target survives the literature and model gates.

Context links:

- [Applied question register at the reviewed commit](https://github.com/BWBrook/eprp/blob/3d432f0aabef19c9d8e07928aa93e14fe83e06a8/ideas/register.md)
- [Blue-sky register at the reviewed commit](https://github.com/BWBrook/eprp/blob/3d432f0aabef19c9d8e07928aa93e14fe83e06a8/ideas/register-blue-sky.md)
- [Capability inventory at the reviewed commit](https://github.com/BWBrook/eprp/blob/3d432f0aabef19c9d8e07928aa93e14fe83e06a8/resources/capability-inventory.md)
- [Evidence guidance at the reviewed commit](https://github.com/BWBrook/eprp/blob/3d432f0aabef19c9d8e07928aa93e14fe83e06a8/docs/evidence.md)

## 4. What is already known, and the residual novelty

### 4.1 The closest work

| Primary work | What it already establishes or models | What remains to be tested here |
| --- | --- | --- |
| **McDonald et al. 2008** [1] | Three-way ancestry in suckers, interpreted as a hybrid bridge and a possible threat to several species' genetic integrity. | General conditions for persistent, causally attributable additional loss of species independence. The idea of a third-species bridge is already occupied. |
| **Bangs et al. 2020** [2] | A broader sucker study finds rare three-way hybrids and limited onward introgression, judging wholesale multispecies collapse improbable in that system. | Explain propagation and containment within the same theory. The model should recover arrested hybridisation, not treat every bridge as a cascade. |
| **Xiong & Mallet 2022** [3] | Intrinsic incompatibilities can erode; local collapse can initiate spatial waves in a two-species system. Genetic architecture changes the outcome. | Propagation across **different** species boundaries, such as A–B followed by loss involving C. Spatial expansion of one A–B failure is not the new result. |
| **Gilman & Behm 2011; Zhang et al. 2019** [4] [5] | Models of reproductive isolation breakdown, speciation collapse, and possible persistence or recovery under disturbance. | The additional multispecies transmission mechanism and its contribution beyond a calibrated pairwise response. |
| **Cannon & Lerdau 2015** [6] | Multispecies mating models can yield demographic benefits of hybridisation. Successful offspring inherit the mother's species identity. | Let reproductive units change independently of inherited taxon labels, so demographic rescue and maintenance of species independence can diverge. |
| **Boecklen 2017; Cannon et al. 2024** [7] [8] | Hybridisation-network structure and geographic networks of potential introgression are nontrivial and measurable. | Evolving compatibility and causal dynamic response, rather than network connectivity alone. Sympatry is not proof of effective introgression. |
| **Ostevik et al. 2021** [9] | Barrier erosion in a species pair can have indirect consequences for compatibility among populations. “Cascading reproductive isolation” already has related uses. | A succession of losses of independently evolving species, explicitly distinguished from within-species barrier changes and reinforcement. |
| **ten Brink 2025** [10] | Environmental change affecting one species can trigger a species-flock collapse through shared resources and life-history feedbacks. | Demonstrate an onward-transmission-dependent effect, while allowing ecological cascades as a competing explanation. |
| **Freitas et al. 2024** [11] | An individual-based macroevolution model includes intermittent barriers and species disappearances, explicitly pooling hybridisation/fusion with extinction in its accounting. | Disaggregate biological causes and identify causal amplification. Merely adding a fusion event to a macroevolution simulator is insufficient. |
| **Kagawa & Seehausen 2020; Frei et al. 2022; Meier et al. 2023** [12] [13] [14] | Simulation and genomic evidence already connect admixture, retained variation and repeated diversification or speciation reversal. | Collective boundary failure is the primary target. Retention and reradiation support interpretation; they cannot carry the novelty claim. |

### 4.2 A precise, provisional novelty claim

> Existing work establishes hybrid bridges, pairwise speciation collapse, spatial spread of incompatibility loss, and ecological collapse cascades. This project asks whether perturbing one reproductive boundary causes additional, persistent losses of species independence through onward hybrid transmission, across an initially stable multispecies complex, and determines which genetic and ecological conditions permit or arrest that amplification.

A bounded search did not locate this exact causal experiment. That is **evidence for a plausible research gap, not proof of priority**. Before substantial implementation, the agents should inspect the closest models and their code, and check forward citations of [1], [3], [6], [9] and [10]. The project should stop or change its question if those sources already answer the same experiment.

Novelty should be judged by the answerable biological question and the comparison it resolves. More species, a larger cluster, a richer interface or a new acronym would not establish it.

### 4.3 The most valuable negative result

A strong negative result would identify a broad class of biologically defensible barriers under which bridges occur but fail to remove additional independently evolving populations. It could show, for example, that sustained propagation requires a restrictive combination of weak ecological separation, compatible recombinant genotypes and prolonged reproductive contact.

That would be more useful than a single demonstration engineered to fuse three species. It would establish when the intuitive idea of a hybridisation cascade is misleading, and provide limits on its use in interpreting species-level extinction pulses.

A failure to obtain cascades because the model never generates viable hybrids, or because the classifier permanently preserves founder labels, would not be an informative negative result.

## 5. Definitions and falsifiable hypotheses

### 5.1 Operational terms

| Term | Meaning in this proposal |
| --- | --- |
| **Reproductive unit** | A persistently differentiated, self-maintaining breeding population, assessed by heritable variation and successful gene exchange. This is an operational approximation to evolutionary independence, not a universal species definition. |
| **Hybridisation** | Reproduction between individuals assigned to different pre-existing reproductive units, with offspring production recorded independently of viability or later fertility. |
| **Introgression** | Genetic material crosses a boundary and contributes through subsequent successful reproduction. An F1 alone does not establish it. |
| **Fusion** | Persistent loss of a distinction between previously independent breeding populations, with a pooled descendant population and material contributions from the sources under an explicit accounting rule. |
| **Secondary loss** | Additional reduction in reproductive-unit count involving at least one nonfocal pre-pulse unit. |
| **Cascade** | A sequence of secondary losses for which the focal intervention increases loss and onward hybrid transmission is causally implicated. Simultaneous collapse without resolved ordering is reported separately. |
| **Arrest** | Hybridisation occurs, but further persistent losses do not follow over the prespecified observation horizon. |
| **Persistence** | Continued loss over a finite, declared interval after the pulse and, in restoration experiments, after environmental restoration. It does not mean mathematical irreversibility. |

### 5.2 Hypotheses

**H1 — Cross-boundary amplification.** A focal barrier perturbation causes more persistent reproductive-unit loss than the directly targeted pair alone can account for, and some of that excess depends on onward hybrid transmission.

**H2 — Architectural containment.** The same encounter history produces substantially different propagation under alternative genetic architectures. Strong ecological differentiation, effective assortative mating or incompatible recombinant pathways can prevent onward boundary loss despite F1 production.

**H3 — Non-monotonic connectivity.** Increasing contact or the number of potential partners need not monotonically increase cascade risk. More contact could facilitate transfer, but might also preserve parental populations, strengthen selection against hybrids, or change mate limitation. The direction is an outcome.

**H4 — A collective effect beyond isolated pair forecasts.** Multispecies outcomes can differ from a model calibrated only on isolated pair responses, after accounting for abundance and shared forcing. This is a stronger claim than H1 and may fail even if causal cascades occur.

**H5 — Conditional fossil distinguishability.** Joint morphology, abundance and geographic information distinguishes some simulated mechanisms better than occurrence counts alone, but realistic time averaging and plasticity may erase the distinction between fusion and demographic loss.

H1–H4 are the core biological programme. H5 is an observation question and cannot rescue an uninformative biological model.

### 5.3 Predictions that could discriminate explanations

| Predicted observation in the simulator | Hybrid-transmission mechanism | Ecological cascade or common forcing | Classification artefact |
| --- | --- | --- | --- |
| Onward transmission ablation reduces nonfocal boundary loss | Expected in a causal transmission regime | May have little effect, unless reproduction changes mediate ecology | Often depends erratically on labels or thresholds |
| Nonfocal loss follows established hybrid contributions | Consistent, but temporal ordering alone is insufficient | Could coincide without being caused by transmission | Apparent onset may be immediate when a graph edge appears |
| Distinct breeding modes disappear while substantial census persists | Supports loss of independence without equivalent demographic collapse | Can occur through ecological homogenisation; needs the ablation test | Requires verification using continuous distributions |
| Alternative plausible barrier architecture arrests the process | Mechanistically informative | Could change ecology too; inspect mediators | If only one arbitrary threshold yields a cascade, suspect artefact |
| Results persist across species estimators and restoration horizons | Strengthens the interpretation | Also possible for ecological losses | Weakens the artefact explanation |
| Pairwise benchmark predicts the entire response | Causal propagation may still occur | Could explain the result | Does not by itself diagnose either mechanism |

### 5.4 What would count as a consequential result?

Predeclare a hierarchy:

1. **Existence:** a robust three-species example with a causal secondary loss.
2. **Generality:** the effect occurs in independently evolved founder states under at least two defensible barrier architectures, or a clear mechanistic explanation predicts why it is restricted to one class.
3. **Magnitude:** in a prespecified regime, the focal intervention produces an average loss exceeding the one-unit maximum of an isolated pair fusion, with uncertainty that excludes that direct-only value.
4. **Macroevolutionary relevance:** the effect occupies a non-negligible, independently justified biological parameter region, rather than an arbitrary fraction of a simulation grid.
5. **Palaeobiological application:** actual observations constrain that region or discriminate mechanisms after the observation model.

These are successive evidential claims. Success at level 1 does not establish level 4 or 5.


## 6. The simulation model

### 6.1 Scope: start with motifs, then earn larger systems

The discovery model should contain **three species and a few habitat patches**. It is the smallest system that can distinguish a focal A–B response from loss involving a third independently evolving population.

Confirm the causal result in three- and four-species motifs. Expand to four–eight species for the first ensemble only after species identification and the intervention work. Eight–32 species and more complex geography constitute a separately gated scaling study. Large species counts should not be a condition for success.

Use a variable-population, diploid, individual-based model. Each individual carries:

$$
X_j(t)=\{g_j,\ z_j,\ u_j,\ a_j,\ p_j,\ \mathcal A_j\},
$$

where $g_j$ is its recombining genotype, $z_j$ its inherited ecological phenotype, $u_j$ its inherited mating or spawning phenotype, $a_j$ age or stage, $p_j$ habitat patch, and $\mathcal A_j$ ancestry information. Environmental effects on phenotype are recorded separately.

Species names do not enter ordinary inheritance, viability or classification rules. Pre-pulse identifiers may be used to define the experimental intervention and trace ancestry; they must not guarantee continued species identity.

### 6.2 Environment and life cycle

Keep four environmental controls distinct:

$$
E(t)=\{K_p(t),\ \theta_p(t),\ M_{pq}(t),\ b_{AB}(t)\}.
$$

They represent habitat capacity, ecological conditions, dispersal/contact, and the focal barrier intervention. Coupling all four into one compression parameter would obscure what caused a cascade.

A minimal life cycle is:

1. Update the environment and survival of existing individuals.
2. Determine reproductive eligibility and potential reproductive effort.
3. Sample encounters and mating success.
4. Produce recombined diploid offspring.
5. Apply stage-specific intrinsic viability, ecological selection and density-dependent recruitment.
6. Disperse or settle recruits.
7. Record demography, successful parentage, phenotype distributions and genetic state.

The exact order is part of the model definition. In particular, pre-dispersal versus post-dispersal selection can affect contact and must be varied in a controlled sensitivity experiment.

For a first ecological model, use a continuous competition kernel:

$$
C_j(t)=\sum_{k\in p_j}
\exp\left[-\frac{\|z_j-z_k\|^2}{2\sigma_C^2}\right].
$$

An illustrative recruitment probability is

$$
r_j(t)=
V_{\mathrm{intr}}(g_j)\,
\exp\left[-\frac{\|z_j-\theta_{p_j}(t)\|^2}{2\sigma_E^2}\right]\,
\left[1+\frac{C_j(t)}{K_{p_j}(t)}\right]^{-1}.
$$

Here $V_{\mathrm{intr}}$ lies between zero and one. Capacities and competition are expressed in model-individual units. This equation is a proposed starting model, not a fitted coral demographic relationship. It permits variable abundance; recruitment is not a lottery that forces community size to remain constant.

An alternative explicit-resource formulation should be added only if the Gaussian competition model yields a scientifically relevant result. Resource substitution is more useful than adding many decorative parameters.

For mating, a minimal encounter-and-assortment kernel is

$$
w_{jk}(t)=D_{p_jp_k}(t)\,
\exp\left[-\frac{(u_j-u_k)^2}{2\sigma_U^2}\right]\,
c_{\mathrm{gam}}(g_j,g_k,t).
$$

The encounter weights $D$, inherited mating phenotype, assortment width $\sigma_U$, and gametic compatibility $c_{\mathrm{gam}}$ have separate roles. The kernel is used within an explicit reproductive-effort model that allows unsuccessful mating. It must not guarantee reproduction simply because one candidate mate exists.

Hybrid status itself receives no universal fitness bonus or penalty. Fitness follows from genotype, ecological phenotype, life stage and environment.

### 6.3 Genetic architectures

Use two genuinely different routes to reproductive separation.

**Architecture A: inherited assortment coupled to ecological differentiation.** Ecological and mating traits are quantitative, with variable linkage, pleiotropy and recombination. Changes in assortment or recombinant phenotypes can alter gene flow. Intrinsic incompatibilities may be weak or absent in the simplest version.

**Architecture B: multilocus intrinsic barriers with ecological and mating separation.** Explicit genotype-to-viability or fertility maps represent interacting genetic components. Include both redundant and nonredundant pathway structures rather than a single genetic-distance cutoff. A published two-species incompatibility model supplies a benchmark. [3]

Within each architecture, vary the linkage between compatibility, mating and ecological loci. Allow both containment and compatible recombinant pathways. A mechanism that operates only because ecological and mating traits are forced to be exactly the same variable is too fragile to generalise.

A practical first range is 8–64 selected loci across 2–8 linkage groups, with a small number of independently specified barrier modules. This is a modelling range, not an estimate of any fossil species' architecture. Neutral ancestry can be recorded with tree sequences rather than explicitly mutating every base.

The main ensemble should include populations whose differentiation developed under simulated isolation and selection. Hand-designed genotypes remain useful for analytical checks and minimal counterexamples, but results from them must be labelled separately.

### 6.4 Generating founder systems

Generate founder histories before choosing intervention outcomes:

1. Begin with shared ancestry and specified genetic architecture.
2. Allow divergence under several predeclared geographic and ecological histories.
3. Reconnect populations under the baseline environment.
4. Observe whether distinct breeding populations remain self-maintaining over a baseline window.
5. Identify eligible founder systems and candidate focal pairs using only pre-pulse information.
6. Freeze the resulting founder library before confirmatory interventions.

Eligibility defines the population to which the results apply: **complexes stable under the stated baseline protocol**. It is not a random sample of all radiations. Report the fraction of attempted founder histories that fail eligibility, and their reasons, separately for each architecture.

Do not require sham runs to survive after the pulse. That would select outcomes after treatment assignment and inflate the apparent importance of a focal intervention. Sham losses are part of the counterfactual distribution.

Focal pairs should be randomly selected within prespecified strata of initial resistance and contact. Analyses targeting particularly weak barriers can be useful, but must state that restricted target population.

### 6.5 Reproductive units without a percolation artefact

The critical measurement problem is to recognise loss of evolutionary independence without defining it into existence.

**Prohibited primary definition:** connected components of a graph with an edge whenever two individuals or populations can mate. A rare bridge could then unite all species by definition while distinct breeding populations persist. Microscopic macroevolution models make the consequences of species definitions especially consequential. [22]

Develop two independent estimators:

| Estimator | Proposed evidence | Main vulnerability |
| --- | --- | --- |
| **Breeding-population estimator** | Persistent heritable modes in mating/ecological phenotype, realised successful parentage, and the maintenance or loss of distinct breeding distributions through time | Weak modes can disappear from an undersampled rare population; geographic isolation can create spurious partitions. |
| **Genetic differentiation estimator** | Persistent differentiated gene pools across neutral and barrier-associated variation, using spatially balanced samples and temporal continuity | Genome-wide similarity can coexist with ecological or reproductive separation; clustering can mistake isolation by distance for species. |

A concrete initial pipeline is to fit candidate mixtures to inherited phenotypes and genetic summaries, compare their predictive fit in held-out samples, then evaluate their temporal persistence and successful exchange. Founder labels are excluded from fitting. A common-encounter mating assay can diagnose whether an apparent boundary is purely geographic, but it should not automatically disqualify an ecologically maintained species.

The pre-analysis calibration panel must include:

- A single continuous population with isolation by distance.
- Stable species that exchange a low level of genes.
- Ecologically distinct populations with substantial neutral introgression.
- An unambiguous merged population.
- A rare but still differentiated species.
- A disappearing population whose ancestry has previously introgressed elsewhere.

Require the estimators to distinguish these cases at known sampling depths. Analyse complete simulated populations where feasible, then deliberately rarefy them; biological extinction must not be inferred from a small measurement sample.

The initial persistence window can be 1,000 generations in the discrete-generation motif, with 250- and 5,000-generation sensitivity windows. These are operational horizons. In an overlapping-generation model, express them additionally in turnover times.

Predeclare alternative thresholds for within-mode separation, effective exchange and minimum detectable abundance after calibration, using separate calibration simulations. **No universal genetic-distance or $F_{ST}$ threshold is assumed.** Report continuous differentiation and exchange alongside every richness curve. If a result depends on one threshold or the two estimators disagree, report an unresolved event or interval, not a forced species count.

### 6.6 Event ledger and ancestry

Maintain a prospective ledger of reproductive units and their changes through time. A conservative fusion event requires:

- Independent breeding modes before the transition.
- Persistent collapse of their differentiated reproductive distributions.
- A pooled descendant population with continuing reproductive contributions from both sources.
- Persistence through the declared follow-up.
- Agreement of the primary estimators, or an explicit uncertainty classification.

The disappearance of A–B separation in several patches is one species-level event if it is the same global distinction. A later loss between the resulting AB population and previously independent C is an additional event. Local boundary loss and range-wide loss must be tabulated separately.

Material contribution should be evaluated continuously and across a threshold range, for example 1%, 5%, 10% and 20% of the pooled population's genomic ancestry. Also examine source-descended genome copies relative to the source's pre-pulse abundance. A fixed percentage alone can misrepresent a formerly rare source.

For source $i$, record its abundance-weighted genomic fraction:

$$
q_i(t)=\frac{1}{2N(t)L}
\sum_{h=1}^{2N(t)}
\int_0^L
\mathbf 1\{\text{the ancestry at }x\text{ passes through source }i
\text{ at the reference time}\}\,dx.
$$

The quantity $N(t)q_i(t)$ is a number of diploid genome equivalents, not a count of surviving source-species individuals. Its ratio to $N_i(0)$ can exceed one after expansion. For multichromosome simulations, sum over chromosome lengths.

Supplement it with genomic breadth, source-private variant retention after standardised sampling, and retention at ecological and compatibility loci. A trace allele is not preservation of a species or of its complete evolutionary history.

Tree-sequence ancestry requires deliberately retaining the pre-pulse reference generation and saving intervention metadata. Default simplification can remove historical individuals and nodes, and user-defined state requires separate handling. [20]

The ledger should distinguish conservative fusion, demographic disappearance, hybrid speciation, fission, transient introgression and unresolved transitions. Do not force an ancestry-exporting demographic collapse into a fusion category. Where classifications overlap, retain bounds on the number of fusion-attributable losses.

### 6.7 Spatial and temporal boundaries

A loss is “global” only across the entire simulated range. Loss in a sampled region is a regional disappearance. Include a sensitivity treatment with external parental refugia or immigration, because a closed domain can exaggerate permanent homogenisation.

Run short processes in generations. Map them to calendar time only for a stated life history and distribution of generation times. Do not compress millions of generations by adjusting population size, mutation and selection without demonstrating that drift, recombination, reproductive variance and barrier dynamics remain comparable.

The deep-time extension should use longer environmental histories around validated local processes. It need not simulate every neutral nucleotide throughout the Phanerozoic.

## 7. Causal experiments and estimands

### 7.1 The primary experiment

For each independently generated founder state $w$, assign intervention policies at the same pre-pulse checkpoint. All arms share background environmental forcing.

| Policy | Focal barrier pulse | Onward transmission from pulse-associated hybrids | Purpose |
| --- | --- | --- | --- |
| **S: sham** | Absent | Natural background | Counterfactual response to shared environmental forcing |
| **F: full pulse** | Present | Allowed | Total consequence of the focal intervention |
| **U: pulse with transmission block, unreplaced opportunities** | Present | A prespecified rule blocks eligible onward reproduction | Mechanistic intervention including its reproductive cost |
| **R: pulse with transmission block, replacement scheme** | Present | Same blocked route, with specified replacement offspring | Sensitivity to the reproductive cost of blocking |
| **SU: sham with unreplaced transmission block** | Absent | The same blocking rule applies to background A–B hybrid paths | Baseline effect of blocking without the pulse |
| **SR: sham with replacement transmission block** | Absent | The same replacement policy applies without the pulse | Baseline effect of replacement and blocking |
| **E: ecological rival** | A separately calibrated focal demographic or resource perturbation | No pulse-specific onward route | Test whether ordinary ecological feedback explains comparable loss |

The policy population includes **all** eligible founder blocks, including those in which the focal pulse never produces a hybrid, never causes fusion, or never reaches an onward mating opportunity.

Within each pulse condition, the blocking rule activates at the first eligible event; histories are identical to the corresponding unblocked policy until activation. For efficiency, the implementation can clone a checkpoint at activation. This must not redefine the analysis population as only the treatment-generated states that reach activation. SU and SR are essential because a post-reference A–B hybrid path can arise under sham as well as under the pulse.

If an additional experiment is conditioned on an activation state, label it a conditional mechanistic assay. It cannot by itself estimate the founder-level treatment effect.

### 7.2 How to perturb only the focal boundary

Use a surgical initial intervention to identify causation. For example, temporarily change the encounter or cue-recognition multiplier for the chosen pre-pulse A–B pair while leaving all other encounter kernels unchanged. Such a rule uses experimental labels; it is not proposed as a literal environmental law.

Then test whether the identified process is reached under less surgical environmental changes: a patch reconnection, altered breeding-time overlap, or compression of ecological conditions. These changes can affect several species directly. Their responses must be decomposed against the causal motif experiment rather than simply called cascades.

This ordering separates two questions:

1. Can the proposed transmission process operate?
2. Can a biologically plausible disturbance enter that process with appreciable probability?

A third-species decline caused directly by the environmental pulse is not evidence for the first question.

### 7.3 Specify what transmission blocking does

A candidate rule prevents a mating that would transfer genomic material through an A–B hybridisation path formed after the common reference time into an eligible nonfocal recipient. The same reference time and rule apply in pulse and sham arms. Use actual transmitted ancestry, not merely “has any hybrid ancestor in its pedigree,” which eventually becomes uninformative.

Freeze recipient eligibility before the experiment, separately from both species estimators. A concrete first rule identifies a recipient parent whose genome derives at least 50% from one reference-time nonfocal source C, D or later sources. The other parent supplies recorded material through the post-reference A–B route. Evaluate both parental directions, and predeclare 10% and 90% recipient-ancestry sensitivity thresholds. Reference-time labels identify the population containing a genome at that time; older admixture remains in its genotype. Background introgression after the reference time changes the measured source fractions.

Also freeze the rule defining A–B seed matings: a first surgical version requires one parent with at least 90% reference-time A ancestry and the other with at least 90% B ancestry. Vary this threshold explicitly. Subsequent transmitted material retains its route tag even when descendants no longer meet the seed-parent criterion. Neither seed nor recipient eligibility uses the evolving outcome-cluster labels.

Route-derived material remains traceable after an initial secondary merger, so its descendants can encounter a further eligible source. A highly mixed recipient lacking a dominant source may cease to meet a particular threshold; record this and compare the alternative rules. These are ancestry-based experimental policies, not definitions of species. Changing the outcome estimator must leave the simulated trajectories unchanged.

Predeclare sensitivity to blocking all such material versus transmission involving the recorded ecological or barrier regions. These are controlled, artificial interventions. Their purpose is to test dependence on a pathway; neither represents a unique natural removal of hybridisation.

In U, blocked opportunities are not replaced. In R, replacement offspring are generated from a prespecified nonfocal parental pool with matched reproductive effort or birth count. Record exactly whether matching occurs before viability or after recruitment. Both cannot generally be held fixed simultaneously.

Record births, failed matings, parentage, recipient recruitment, genotype distributions and density feedbacks in every arm. Agreement between U and R strengthens a qualitative interpretation. Disagreement is evidence that the intervention's demographic consequences matter.

Changing inheritance changes later ecology. Those later changes can be mediators of the mechanism. Do not claim to keep all subsequent abundance, competition and fitness identical.

An artificial ecological-replay experiment may be useful for a narrower decomposition. It is supplementary and must not replace the natural total-effect comparison. **Do not report a fraction of the total effect “mediated by genes” from these contrasts without additional identification assumptions.**

### 7.4 Primary and secondary estimands

Let $S_w^a(T)$ be the number of persistent reproductive units at endpoint $T$, according to a specified estimator, under policy $a$.

The founder-level intention-to-treat richness effect is

$$
\Delta_S(T)=
\mathbb E_w\!\left[S_w^S(T)-S_w^F(T)\right].
$$

The expectation is over the stated distribution of eligible founders and stochastic realisations. A successful focal A–B fusion alone can reduce richness by one. Consequently, $\Delta_S>1$ is a conservative test of **richness amplification beyond that direct merger**.

It is not sufficient evidence of a fusion cascade: demographic extinctions, suppressed originations or classification changes can also produce it. Require the event ledger to show that additional losses involve persistent merger of nonfocal breeding modes, and report alternative classifications.

For each blocking policy $b\in\{U,R\}$, estimate the within-pulse contrast

$$
\Gamma_b(T)=
\mathbb E_w\!\left[S_w^b(T)-S_w^F(T)\right].
$$

Let $S^{S_b}$ denote the corresponding sham-with-block outcome, SU or SR. The pulse-specific interaction is

$$
I_b(T)=
\mathbb E_w\!\left[
\{S_w^b(T)-S_w^F(T)\}
-
\{S_w^{S_b}(T)-S_w^S(T)\}
\right].
$$

This subtracts the effect of blocking background transmission without the pulse. A positive $\Gamma_b$ alone is insufficient: the proposed pulse-transmission interpretation also requires attenuation of the pulse effect in $I_b$, supported by the event ledger and demographic diagnostics. Estimate the analogous interaction for conservatively classified secondary fusion losses. These are controlled policy interactions, not natural indirect effects or a unique fraction mediated.

The main output set should include:

- Probability of focal hybridisation, sustained introgression and focal fusion, separately.
- Number of conservative secondary fusion losses and its uncertainty bounds.
- Total richness effect $\Delta_S$.
- Transmission-policy contrasts $\Gamma_U$ and $\Gamma_R$, and pulse-specific interactions $I_U$ and $I_R$.
- Demographic losses and new unit formation in all arms.
- Time from the focal perturbation to onward transmission and nonfocal loss.
- Persistence after pulse termination and environmental restoration.
- Source ancestry abundance, breadth and private-variant retention.

A failure to exceed one in $\Delta_S$ does not rule out smaller causal secondary effects. Report them without upgrading them to a large amplification claim.

### 7.5 Temporal evidence

A sequence should be counted as an ordered cascade only if the event history resolves successive losses. A–B failure followed by failure of the AB–C distinction is eligible; geographic spread of the same A–B failure is not another loss.

If hybrid transmission begins before A–B fully merges, and C subsequently loses independence, report a **hybridisation-induced secondary loss**. It is informative, but it does not prove that a completed initial fusion caused the next one.

Treat simultaneous or temporally unresolved multi-unit collapse as its own class. Long persistence windows should not create a false ordering merely because one event is retrospectively confirmed earlier.

### 7.6 The pairwise benchmark

Calibrate isolated pair experiments across the same baseline resistance, abundance, environmental forcing and contact conditions. Use their estimated transition rates to construct a pairwise-only forecast for recipient losses.

A credible benchmark conditions on recipient exposure, initial resistance, abundance and shared forcing. It is not an arbitrary sum of independent Bernoulli events. Pairs sharing a species are not statistically independent, and isolation changes competition; use controlled resource or competitor replay only with those limitations stated.

Ask whether updating the benchmark with measured abundance and contact explains the multispecies result, or whether changes generated by hybrid ancestry add predictive information.

This is a predictive comparison, distinct from the intervention. If the pairwise model predicts outcomes well, a causal propagation result may still stand, but the stronger claim of collective instability beyond pairwise opportunity should be withdrawn.

### 7.7 Analytical limits and limiting cases

Three simple limits are mandatory:

1. With no effective contact, no hybrid-mediated secondary event should occur.
2. With complete relevant incompatibility, a bridge cannot transmit viable genetic material through that barrier.
3. With only two original units and no other lineage processes, direct fusion removes at most one unit.

A conditional broader bound is useful. Suppose there are $C_{\mathrm{occ}}$ initially occupied, mutually transmission-isolated genotype classes whose descendants persist, with every reproductive unit lying wholly within one class. In the absence of demographic extinction or new unit formation, fusion can reduce $S_0$ units by at most $S_0-C_{\mathrm{occ}}$. Unoccupied accessible classes must not be counted.

The partition must be invariant under the allowed mutation and recombination processes. **Connected components of the initial observed hybridisation graph do not establish that bound**, because hybrids may create previously absent compatibility routes. Nor does failing to observe a cross in a finite simulation prove that it is impossible.

A branching-process or response-matrix approximation might summarise early propagation. Any threshold based on it must be validated against the individual-based model; shared recipients, state dependence and depletion prevent assuming a universal cascade theorem.

## 8. Simulation campaign and analysis

### 8.1 Factor hierarchy

Avoid a full factorial over every parameter. Use mechanism-based blocks.

| Block | Primary variation | Purpose |
| --- | --- | --- |
| Barrier biology | Assortment, ecological separation, intrinsic architecture, linkage | Propagation versus containment |
| Population state | Abundance ratios, reproductive variance, founder history | Distinguish susceptibility from simple rarity |
| Encounter process | Contact duration, patch overlap, dispersal, focal pulse strength | Estimate whether a bridge has the opportunity to act |
| Community context | Three/four species first; later richness and partner arrangement | Separate causal transmission from number of recipients |
| Observation | Sampling, plasticity, time averaging, dating and taxonomy | Assess what an investigator could infer |

Use broad model ranges for discovery, then justify narrower biological regions from empirical evidence. A uniform or log-uniform sweep is a design distribution, not a probability distribution of real species complexes.

### 8.2 Initial scale and precision

A proposed small-model envelope is:

- 3–4 reproductive units; 2–8 patches.
- Approximately 200–2,000 model individuals per starting unit, including deliberately unequal abundances.
- A baseline observation window of 1,000 generations.
- Pulse durations of 20–500 generations.
- Follow-up through at least 5,000 generations for selected confirmation cases.
- Longer or shorter horizons only through prespecified sensitivity comparisons.

These choices must be revised if the benchmark shows that a relevant barrier process operates on a different timescale. Census sizes are computational model sizes, not validated replacements for natural effective population sizes.

For a probability near 0.5, 100 independent observations yield an approximate 95% sampling half-width of 0.10; roughly 400 yield about 0.05. These are planning calculations, not a promised biological sample size. Paired effects require their own variance estimates, and repeated seeds within a founder do not supply independent founder histories.

### 8.3 Scaling without manufacturing an effect

Larger communities change recipient opportunity, niche packing and abundance. Conduct both fixed-total-abundance and fixed-per-species-abundance comparisons, and independently vary niche separation and contact exposure.

Report:

- Raw additional losses.
- Additional losses per eligible nonfocal recipient.
- The fraction of original units involved, without pair-count inflation.
- The residual against the opportunity- and abundance-adjusted pairwise forecast.
- Founder acceptance rates and the ecological structures needed for stable coexistence.

A result that grows with species number solely because there are more vulnerable recipients is a useful exposure relationship, but it is not evidence of a new collective instability.

### 8.4 Discovery, confirmation and uncertainty

Separate exploratory design points from confirmation. Choose representative propagation, containment and demographic-collapse regimes after screening, then freeze the comparisons before generating new founders and seeds.

Use paired effect estimates with uncertainty clustered over independent founder histories. Report architecture-specific results before pooling. When a cell has no observed cascade, provide an upper bound on its frequency rather than declaring the probability zero.

Distinguish four uncertainties:

1. Stochastic variation within a model.
2. Variation among evolved founder histories.
3. Parameter uncertainty within a biological interpretation.
4. Structural uncertainty across model architectures.

Thousands of simulations reduce the first; they do not automatically resolve the other three.

Keep right-censored trajectories separate from confirmed persistence. A run stopped at a resource limit is not an arrested cascade. Record numerical failures and exceptional states without silently excluding them.

### 8.5 A parsimonious macroevolutionary extension

Only after a robust motif result, embed the validated local process in repeated isolation/contact histories. Ask whether the process changes the distribution of durable richness, clustering of losses or within-clade selectivity compared with pairwise response forecasts.

The coarse model should retain a reticulate event history and use transition surfaces learned from the detailed model. Validate it on held-out individual-based trajectories before applying long forcing histories.

This extension earns its place by asking how an established mechanism alters macroevolutionary outcomes. It must not become a new generic timing study already covered by Q-029.


## 9. Fossil observation and empirical feasibility

### 9.1 The empirical strategy

Use three layers of evidence for three different purposes:

| Layer | Candidate resource | What it can constrain | Present access/feasibility assessment |
| --- | --- | --- | --- |
| Modern reproductive biology | Coral crossing and spawning studies [16] [17]; positive and arrested fish examples [1] [2] | Plausible barrier combinations, distinction between crossability and sustained transmission | Published evidence inspected; a parameter-ready harmonised dataset has not been assembled. |
| Fossil morphology and sampling | Budd & Pandolfi's Pleistocene Bahamas study [15] | Realistic colony sampling, morphological overlap and geographic heterogeneity | Paper and appendices inspected. A raw specimen-by-coordinate matrix was not verified. |
| Broader Cenozoic context | NMITA coral catalogue [18]; PBDB occurrences and collections [21] | Taxonomic, geographic, temporal and sampling context | Resource documentation inspected. Neither is presumed to encode reproductive networks or a resolved cascade sequence. |

A useful modern constraint is that coral reproductive separation can involve several interacting mechanisms, including spawning timing, gamete compatibility, and gamete dispersal and dilution. [16] The proposal should not reduce all of these to a single genetic distance. Modern regional differences in morphology and genetic differentiation also caution against treating morphological overlap as a universal proxy for introgression. [17]

### 9.2 What the fossil benchmark actually supplies

Budd & Pandolfi [15] examine last-interglacial Bahamian reef terraces, approximately 125 ka, using 106 measured colonies and geographically uneven samples. The appendices contain specimen information, transect line-intercept cover data and measurement definitions. Their hybridisation interpretation explicitly depends on a relationship between morphological overlap and lineage fusion.

This is a calibration case for the observation process. It is not a before–during–after extinction sequence, and it does not establish an ancient cascade. Raw morphometric coordinates may require an archive acquisition or remeasurement; neither is assumed available here.

An older coral turnover application should be selected only after auditing independent chronology, comparable measurements, regional coverage and the relevant taxonomic complex. A species catalogue or trait matrix is not a substitute for a specimen time series.

### 9.3 Synthetic fossil generator

For sampled individual or colony $j$, generate morphology as

$$
y_j = H z_j + P(E_j,a_j) + \epsilon_j,
$$

where $H$ maps inherited traits to observable characters, $P$ describes plasticity and ontogeny, and $\epsilon$ includes measurement error and unmodelled variation.

Then apply:

1. Habitat-dependent preservation and sampling.
2. Geographic pooling or transport.
3. Time averaging, reworking and incomplete strata.
4. Correlated dating uncertainty within horizons.
5. Unequal abundance and specimen recovery.
6. Morphological identification under explicit splitting/lumping rules.
7. Alternative historical and current taxonomic treatments.

The model-generated reproductive units are hidden from the fossil analyst. The observation pipeline must not use founder ancestry labels to classify fossils or select informative specimens.

No fixed mapping from the simulation's mating trait to skeletal morphology should be assumed. Vary their association, including a weakly informative mapping. Otherwise, the synthetic fossil record would be supplied with the answer.

### 9.4 Adversarial alternatives

Construct nonhybrid histories that approximate the same observable richness and abundance changes:

- Competitive replacement or demographic collapse with earlier low-level introgression.
- Convergent selection producing similar morphologies.
- Environmentally induced plasticity.
- Time averaging of successive, distinct populations.
- Regional immigration and mixing.
- Taxonomic revision without a biological event.

Match their major observable margins to the cascade examples. A classifier that distinguishes deliberately different abundance curves has not identified hybridisation.

Train and evaluate any statistical discriminator across independent biological histories, not random rows or observation replicates from the same simulation. Hold out entire parameter regions and at least one generative architecture. Evaluate calibration and false-positive rates as well as discrimination.

An interpretable baseline using richness, morphological multimodality, abundance turnover and geographic structure should precede a flexible machine-learning model. The latter is justified only if it adds stable information under model misspecification.

### 9.5 The empirical gate

Before making a claim about a particular ancient event, require:

- A target complex containing enough distinguishable pre-event units to test additional losses; three is the logical minimum.
- Comparable observations before, through and after the candidate change.
- Age uncertainty and time averaging evaluated against the predicted process duration.
- Regional observations sufficient to address immigration and survival outside the sampled locality.
- An independently supported forcing history.
- A morphological observation model that performs acceptably under realistic nonhybrid alternatives.
- Traceable measurements and taxonomic decisions, with usable access terms.

These are study requirements, not claims that the available datasets already satisfy them.

If only occurrence counts and broad morphospecies bins are available, restrict inference to compatible histories and sensitivity bounds. Do not estimate a genome-level cascade rate by fitting an overparameterised model to those counts.

A valuable observation result could identify combinations of sampling resolution and trait information under which fusion and demographic extinction remain indistinguishable. Its relevance would come from explaining a concrete limit on deep-time inference, alongside the independent biological result.

### 9.6 What large palaeodatabases can contribute

PBDB and NMITA can support the search for suitable complexes, establish collection coverage, expose taxonomic inconsistencies and supply sampling templates. Their role is substantial but targeted.

The project should preserve downloaded snapshots, query specifications, taxonomic opinions and checksums. It should not assume that rerunning a query reconstructs the same historical database state.

A global fit across all marine genera would be premature. The mechanism operates through reproductive compatibility, which such a fit would largely leave latent. The route to broader significance is to establish the process, derive defensible limits, and then assess the subset of fossil diversity for which its consequences are testable.

## 10. Implementation and HPC plan

### 10.1 Reuse a simulation engine

Use **SLiM with a non-Wright–Fisher life cycle** for the production eco-genetic simulator, subject to a small benchmark establishing that its representation suits the chosen reproduction rules. Use Python for experiment management, ancestry analysis and fossil observation. SLiM and tree-sequence tooling provide an appropriate starting foundation. [19] [20]

Pin the engine version, compiler, Python environment and dependency versions after the benchmark. Do not assume that code for an older SLiM release runs unchanged.

Use the Xiong–Mallet archive as a reproduction target, not an uninspected dependency. Its code and data are deposited at [Dryad, 10.5061/dryad.mgqnk992f](https://doi.org/10.5061/dryad.mgqnk992f). [3] Verify access, licence and the specific model variant before reuse.

An independently implemented small reference model should check elementary inheritance and intervention behaviour. It need not reproduce the entire production framework.

### 10.2 Module contract

| Module | Scientific responsibility | Essential output |
| --- | --- | --- |
| Founder generator | Produce and screen pre-pulse histories without looking at treatment outcomes | Founder checkpoint, eligibility record, acceptance/failure reasons |
| Eco-genetic engine | Reproduction, recombination, survival, selection and spatial contact | Trajectories and resource diagnostics |
| Intervention layer | Execute the prespecified pulse, sham, transmission and ecological policies | Activation log and intervention audit |
| Boundary estimator | Estimate persistent reproductive units without founder-label inheritance | Continuous diagnostics, counts and disagreements |
| Event and ancestry ledger | Separate source contributions, losses, fissions and ambiguous events | Time-stamped event table and ancestry summaries |
| Observation generator | Produce fossil-like data under known causes | Synthetic collections, morphology and chronology |
| Analysis pipeline | Paired effects, opportunity adjustment, uncertainty and validation | Tables and publication figures |

The module boundary should follow scientific responsibility. A change to a species estimator should not change the simulated mating process, and a fossil taxonomic rule should not change biological truth in the engine.

### 10.3 Minimal run manifest

Each run should record at least:

- Scientific model version and source commit.
- Parameter-set identifier and full configuration hash.
- Founder history identifier, checkpoint hash and eligibility definition.
- Intervention policy and activation rule.
- Master seed and independently tracked stochastic streams where supported.
- Shared forcing-file hash.
- Simulation time units and calendar-time mapping, if any.
- Species-estimator and ancestry-threshold versions.
- Observation scenario and its seed.
- Actual CPU time, peak RAM, output size and termination reason.

Assign randomness reproducibly. Common randomness can reduce paired variance while histories coincide, but divergent reproduction changes the number and meaning of random draws. Do not assume that using the same integer seed makes all later stochastic events matched.

Verify that restarting from a saved state reproduces the intended continuation, including user-defined state and intervention bookkeeping. A tree sequence alone must not be assumed to save everything required.

### 10.4 CPU execution

The reviewed EPRP inventory lists kunanyi capacity of **up to 48 nodes × 28 CPUs through PBS**. That is an inventory statement, not a measured current allocation or throughput guarantee. The user separately reports a Nectar VM with one A100, 64 CPUs and 128 GB RAM; GPU memory was not specified.

The principal parallel unit is a founder/parameter/replicate block, with intervention branches sharing the founder checkpoint. Start with single-core simulation processes; use additional threads only if benchmarking shows a benefit.

Use bounded PBS job arrays and pack independent processes into allocated nodes subject to measured memory requirements. Set numerical-library thread counts explicitly to avoid oversubscription. A process should write to a unique run directory, with compact results assembled after completion.

Prefer independent ensembles over a tightly coupled distributed simulation. No MPI requirement is expected for the core project. This is a proposed execution design; no cluster access or workload was undertaken in preparing this document.

### 10.5 Staged budgets

The following are **planning envelopes**, not runtime predictions:

| Stage | Illustrative experiment count | Proposed resource discipline |
| --- | --- | --- |
| Correctness and performance | Tens to a few hundred small runs, including restart and limiting cases | Measure runtime, RAM, ancestry growth and analysis costs before estimating a campaign. |
| Motif screening | 48 design cells × 8 founder blocks × 7 policies = 2,688 policy trajectories; architectures included as strata | A provisional ceiling of 2,000 CPU-hours before scientific review. Reduce scope if actual costs exceed the envelope. |
| Confirmation | Selected regimes with new founders; initial allocation of roughly 100 founders per regime, increased according to measured precision | A separately reviewed envelope, initially no more than 20,000 CPU-hours. Preserve negative and boundary regimes. |
| Community scaling | Only after the causal and measurement gates | Expand recipient structure, founder histories and model architectures before genome size. |
| Fossil observations | Many cheap observations per selected biological history | Avoid treating these as independent evolutionary replicates. |

Runtime arithmetic should be transparent:

$$
H_{\mathrm{CPU}}=
H_{\mathrm{founders}}+
\sum_{r=1}^{R}h_r+
H_{\mathrm{analysis}}.
$$

For illustration only, **20,000 trajectories at a measured 0.5 CPU-hour each would consume 10,000 CPU-hours**, excluding founder generation and analysis. On 224 actually allocated CPUs, ideal compute-only wall time would be about 45 hours, before queueing, imbalance and overhead. Neither the 0.5-hour runtime nor the 224-CPU allocation has been measured or secured.

Pre-pulse evolution can dominate cost. Reuse founder checkpoints across legitimate paired experiments, while accounting for their shared history in analysis. Never present correlated reuse as new evolutionary replication.

### 10.6 Memory and output

Benchmark the population size, number of remembered reference genomes, chromosome count, simplification interval, checkpoint frequency and boundary-estimation cost together.

Retain compact trajectories and event summaries from every run. Retain full ancestry outputs for confirmation, diagnostics and a representative subset of screening trajectories. Preserve the pre-pulse reference generation needed for source accounting.

For small motifs, record complete populations at the diagnostic intervals. For larger systems, use a documented combination of population-wide summaries and stratified genetic samples, with rare-population checks. A failed species estimator must not become an apparent extinction.

Set a provisional working-output budget, such as 100 GB for the first pilot, and revise it from measured file sizes. Write compressed, partitioned result tables and avoid millions of tiny files on shared storage. Checkpoint costs and failed jobs belong in the resource report.

### 10.7 Role of the A100

The A100 may help with a validated emulator, a large synthetic-observation likelihood or repeated tensor calculations. It is not required for the core experiment, and ordinary SLiM trajectories should not be assumed to gain GPU acceleration.

An emulator is useful only after there is a trustworthy simulation corpus. Validate it on withheld architectures and near transition boundaries. It should accelerate exploration, not become the source of an unverified biological threshold.

The 64-CPU Nectar host may also be useful for development or smaller ensembles, subject to its actual available resources. There is no need to design the science around a single GPU.

### 10.8 Validation that earns confidence

Prioritise scientifically meaningful checks:

1. Mendelian transmission, recombination and ancestry accounting in small known pedigrees.
2. No-contact and complete-incompatibility limits.
3. A published two-species benchmark.
4. Checkpoint continuation and equivalence of policies before activation.
5. Species-estimator calibration on the deliberately difficult cases in Section 6.5.
6. A positive hybrid-transmission example and a negative ecological-only example.
7. Conservation/accounting checks for births, deaths, migration and genome contributions.
8. Reproduction of the main qualitative conclusion under a second architecture and an independent minimal implementation.

Agent agreement is not independent biological validation. Tests written from the same incorrect model assumption can agree perfectly. The lead scientist must review the biological interpretation of the invariants and benchmark comparisons.

## 11. Work packages, decision gates and stopping rules

### 11.1 A bounded first phase

Indicative effort is expressed in working weeks, not guaranteed elapsed time. Literature/code access, founder stability and classifier development can change it.

| Work package | Indicative effort | Reviewable deliverable | Decision |
| --- | --- | --- | --- |
| **WP0: novelty and model audit** | 1 week | Exact comparison with [1]–[12], closest code inspected, missing access recorded | Stop if the proposed causal experiment is already answered. |
| **WP1: benchmark and measurement** | 1–2 weeks | Two-species benchmark; ancestry checks; species-estimator calibration panel | Stop if the engine or estimator cannot represent porous but persistent species. |
| **WP2: three-/four-species causal pilot** | 2–3 weeks | Paired policy results, event ledger, demographic rivals and cost report | Continue for a robust secondary-loss effect or an informative mechanistic obstruction. |
| **WP3: confirmation and limits** | 2–4 weeks | New founders, second architecture, uncertainty, opportunity adjustment | Establish the strongest warranted claim; do not require collective instability if only propagation is supported. |
| **WP4: scaling and fossil feasibility** | 2–4 weeks, conditional | Larger-context sensitivity and a documented data/observation gate | Undertake an empirical ancient-event application only if observations earn it. |

A theory manuscript could emerge from WP0–WP3. WP4 should not be allowed to postpone a complete, interpretable result indefinitely.

### 11.2 The first decision package

Before a major HPC campaign, produce a compact dossier containing:

- A one-page novelty claim and closest counterexample.
- A fully specified minimal model.
- One positive and one arrested trajectory, if both occur.
- Paired effect distributions, including unsuccessful focal interventions.
- A conservative event ledger with ancestry and demographic diagnostics.
- Sensitivity to species identification and persistence windows.
- Actual runtime, RAM and storage measurements.
- A recommendation to proceed, narrow or stop.

For an initial positive go decision, require a secondary effect in newly generated founder states and a biologically interpretable reason it occurs. A practical magnitude screen is an additional loss in at least 10% of founder trials in a declared regime, with uncertainty reported; this is a project-prioritisation threshold, not a natural constant or a claim about real-world prevalence.

For a negative go decision, require more than failure to find a cascade. There should be a reproducible obstruction or restrictive necessary condition that survives alternative implementations and explains successful hybrid production without propagated loss.

### 11.3 Explicit stopping or narrowing rules

| Finding | Response |
| --- | --- |
| Prior work already performs the same multi-boundary causal experiment | Stop the novelty claim; identify a genuinely unanswered residual before continuing. |
| Cascades occur only under connected-component or founder-label species definitions | Reject the result as a measurement artefact. |
| Richness declines, but nonfocal units disappear demographically without demonstrated merger | Reclassify the mechanism; do not claim a fusion cascade. |
| Pulse-specific transmission-policy interactions vanish | Prefer background transmission, shared forcing or ecological explanations, subject to checking that the block actually intervened on the intended route. |
| Blocking schemes disagree strongly because of births or replacement genotypes | Report the intervention dependence; redesign the mechanistic assay before making a genetic causal claim. |
| Apparent loss reverses rapidly after the pulse | Report transient homogenisation, not persistent loss. |
| Effects require contrived genotypes or fail in independently evolved founders | Restrict the claim to a proof of possibility, or stop if that contribution is trivial. |
| Pairwise opportunity forecasts explain the result | Retain any justified causal propagation result; withdraw the stronger collective-instability interpretation. |
| Large communities require artificial coexistence assumptions that determine the answer | Keep the result at motif scale. |
| Fossil observations cannot distinguish relevant mechanisms | Retain the theory and report the observation limit; do not force an ancient-event attribution. |
| Runtime or storage overwhelms the pilot budget | Simplify the state representation or narrow the experiment before scaling. |

### 11.4 Suggested division of labour for coding agents

The principal investigator should own the question, admissible biology, effect interpretation and decisions about scope. A useful parallel structure, after adoption, is:

- **Model agent:** implements the life cycle and genetic architectures against the written contract.
- **Measurement agent:** independently develops boundary and ancestry diagnostics using fixed calibration cases.
- **Experiment agent:** implements policies, manifests, HPC packaging and paired analysis.
- **Critical-review role:** searches for occupied novelty, circular definitions, counterexamples and misleading causal interpretations.

These are roles, not required simultaneous staffing. Work should follow the repository's current agent and compute instructions. Scientific contracts should be reviewed before an agent optimises or expands its module.

A future implementation could live in a dedicated experimental directory with separate model, analysis, observation, configuration and benchmark components. No repository path or register number is reserved by this proposal.

## 12. Expected scientific products

### 12.1 The primary paper

A suitable initial paper would ask:

> **When does hybridisation transmit the loss of reproductive independence across a species complex?**

Its contribution should be a causal result and a map of its limits, with a clear distinction between propagation and stronger collective amplification.

Proposed main figures:

1. **One decisive matched-world example:** sham, full pulse and transmission policies; breeding-mode distributions, census and ancestry shown together.
2. **Propagation versus containment:** effect surfaces across ecological separation and barrier architecture, with uncertainty and founder acceptance.
3. **Why a bridge succeeds or fails:** reproductive contributions and compatibility changes through the event sequence.
4. **Community scaling:** raw losses and recipient-adjusted effects under both abundance controls.
5. **What a fossil analyst would see:** the same known biological histories after sampling, including matched nonhybrid alternatives.

The fifth figure is optional in the first paper if the observation analysis is not mature. It should not replace a missing biological result.

### 12.2 Publishable outcomes

| Outcome | Scientific contribution |
| --- | --- |
| Robust causal propagation | A mechanism linking local barrier change to additional loss of independent lineages |
| Amplification beyond exposure and pairwise forecasts | Evidence that the collective genetic/ecological state adds predictive information |
| Strong architectural containment | An explanation for the stability of species despite opportunities for hybridisation |
| Restricted propagation | A defensible boundary on which radiations and disturbances could be affected |
| Fossil non-identifiability | A demonstrated limit on interpreting apparent species losses, tied to a known process |

A reusable framework and well-documented simulation corpus are supporting products. They are not substitutes for one of these scientific findings.

### 12.3 Why I would prioritise this candidate

The project connects a genuine macroevolutionary quantity—durable independent lineages—to a mechanism with direct empirical motivation and serious contrary evidence. It offers a decisive simulation intervention, can begin at a tractable scale, and expands naturally through independent CPU ensembles.

Its main risk is conceptual, not lack of compute: a model can too easily call ordinary introgression, demographic loss or a graph merger a cascade. The design above makes that risk testable early.

## 13. Risks and questions for independent review

The strongest objection is that the project may still be a narrow extension of established hybridisation theory. The response must come from the exact experiment and the biological information it supplies, not claims about framework sophistication.

The second objection is the distance between mechanism and fossils. That distance is real. A robust theory of species-boundary propagation can be worthwhile in macroevolution without a successful reconstruction of one ancient event. If the project is judged to require direct attribution of a deep-time extinction from the outset, this candidate should be ranked lower until the data gate is met.

The third objection is that species boundaries are not a single measurable scalar. The response is to expose that uncertainty through alternative estimators, continuous diagnostics and conservative event accounting. An apparent effect that depends on hiding this ambiguity should not survive review.

### Questions for Claude and Codex

1. Does any existing syngameon or incompatibility model already perturb one boundary and measure persistent failures involving additional independent species?
2. Is the surgical intervention biologically interpretable, and can realistic forcing plausibly activate the identified process?
3. Do the transmission policies answer the stated question, or mainly manipulate fecundity and replacement genotypes?
4. Can each claimed secondary fusion be distinguished from demographic disappearance with prior ancestry export?
5. Does the species estimator recognise stable porous species and rare populations without embedding the desired answer?
6. Is the larger-system effect explained by more recipients, lower abundance or tighter niche packing?
7. Are inferred biological parameter regions defensible, or merely convenient simulation ranges?
8. Does the fossil observation model allow weak genotype–morphology association and convincing nonhybrid alternatives?
9. What result would make this project uninteresting, even if its software worked perfectly?
10. Which smallest additional experiment would change the go/no-go decision?

The decision should turn on those questions before expensive expansion.

## 14. Evidence and search audit

### 14.1 Search scope

This proposal was researched on 20 October 2026 using the private EPRP portfolio as context and public primary literature and documentation for scientific claims.

The search was purposive and iterative, rather than a formal systematic review. It followed the candidate from speciation reversal and retained variation to hybrid bridges, syngameons, incompatibility collapse, ecological cascades and fossil coral interpretation.

Representative query families included:

- “speciation collapse” and “species fusion” simulation models.
- “hybrid bridge” three species and introgression.
- “syngameon” simulation, topology and stability.
- “collapse of genetic incompatibilities” and spatial propagation.
- “cascading reproductive isolation”.
- “species flock” environmental collapse.
- “admixture-derived adaptive radiation potential”.
- “Montastraea annularis” fossil hybridisation and reproductive isolation.
- SLiM, tree-sequence ancestry and official documentation.

Exact-title and DOI checks followed discovery. Relevant newer work, including the 2025 ecological-cascade paper and 2026 SLiM publication, was included. The search did not establish exhaustive coverage of unpublished work or every citation chain.

### 14.2 Access depth and remaining checks

| Sources | Access used for this proposal | Remaining work before empirical or code use |
| --- | --- | --- |
| [1] | Primary author/agency-hosted paper | No reanalysis of molecular data |
| [2] [3] [6] [7] [8] [10] | Primary full text, including relevant methods/discussion or data statements | Inspect and reproduce code where applicable; no published result was rerun |
| [4] [5] | Primary abstracts and indexed article material | Full methods/code audit required for the implementation-stage novelty gate |
| [9] | Primary abstract and indexed article material | Inspect complete methods before claiming exact model or experimental differences |
| [11] | Abstract, indexed main text and targeted full-text inspection in the research review | No simulator execution; priority remains checking its event definitions and relation to the new estimand |
| [12] | Primary article material and code-archive record | Reproduction not attempted; recovery is excluded from the central novelty |
| [13] | Primary abstract and institutional/publication records | No whole-genome reanalysis |
| [14] | Primary article PDF and abstract | No genomic reanalysis |
| [15] | Publisher abstract and author-uploaded full paper/appendices | Raw coordinate matrix and a suitable turnover sequence remain unverified |
| [16] [17] | Primary abstracts | Numerical calibration requires full methods, data and contemporary taxonomic reconciliation |
| [18] [21] | Official resource page/user documentation | Targeted data acquisition, licences, completeness and taxonomic audit |
| [19] [20] | Current primary software paper and official documentation | Pin and benchmark actual software versions |
| [22] | Published conceptual/methodological discussion | Used for species-definition context, not as evidence that a cascade exists |
| EPRP | Registers, status, guidance and capability inventory at the reviewed snapshot | Subsequent repository changes may alter portfolio position |

Links below identify sources, not a claim that all linked data are downloaded, runnable or openly licensed. No new empirical result is inferred from inaccessible supplementary material.

### 14.3 Claims deliberately left unresolved

- How often natural environmental change reaches the required genetic states.
- Whether propagation is common, rare or effectively prevented.
- Whether any older coral turnover contains a usable time-resolved signal.
- The fraction of species-level deep-time losses that fusion could explain.
- Actual kunanyi or Nectar runtime, memory limits, allocations and queue behaviour.
- Priority relative to unpublished or unlocated multispecies models.

These are explicit research questions or feasibility uncertainties. They should not be filled by agent consensus.


## 15. References

Publication years below refer to the journal issue or article year, rather than later website digitisation dates. All online resources were checked during preparation on 20 October 2026.

1. **McDonald, D. B., Parchman, T. L., Bower, M. R., Hubert, W. A. & Rahel, F. J. (2008).** An introduced and a native vertebrate hybridize to form a genetic bridge to a second native species. *Proceedings of the National Academy of Sciences*. [DOI: 10.1073/pnas.0712002105][1]. [Primary paper copy](https://files.cfc.umt.edu/cesu/BLM/UWY/McDonald_sucker%20Genetic_frpt.pdf).

2. **Bangs, M. R., Douglas, M. R., Brunner, P. C. & Douglas, M. E. (2020).** Reticulate evolution as a management challenge: Patterns of admixture with phylogenetic distance in endemic fishes of western North America. *Evolutionary Applications*, 13, 1400–1419. [DOI: 10.1111/eva.13042][2].

3. **Xiong, T. & Mallet, J. (2022).** On the impermanence of species: The collapse of genetic incompatibilities in hybridizing populations. *Evolution*, 76, 2498–2512. [DOI: 10.1111/evo.14626][3]. [Code and data: 10.5061/dryad.mgqnk992f](https://doi.org/10.5061/dryad.mgqnk992f).

4. **Gilman, R. T. & Behm, J. E. (2011).** Hybridization, species collapse, and species reemergence after disturbance to premating mechanisms of reproductive isolation. *Evolution*, 65, 2592–2605. [DOI: 10.1111/j.1558-5646.2011.01320.x][4].

5. **Zhang, X. et al. (2019).** Biodiversity loss through speciation collapse: Mechanisms, warning signals, and possible rescue. *Evolution*. [DOI: 10.1111/evo.13736][5].

6. **Cannon, C. H. & Lerdau, M. (2015).** Variable mating behaviors and the maintenance of tropical biodiversity. *Frontiers in Genetics*, 6, 183. [DOI: 10.3389/fgene.2015.00183][6].

7. **Boecklen, W. J. (2017).** Topology of syngameons. *Ecology and Evolution*, 7, 10486–10491. [DOI: 10.1002/ece3.3507][7].

8. **Cannon, C. H. et al. (2024).** Constructing sympatry networks to assess potential introgression pathways within the major oak sections in the contiguous US states. *Plants, People, Planet*, 6, 1437–1452. [DOI: 10.1002/ppp3.10546][8].

9. **Ostevik, K. L. et al. (2021).** Morning glory species co-occurrence is associated with asymmetrically decreased and cascading reproductive isolation. *Evolution Letters*, 5, 75–86. [DOI: 10.1002/evl3.205][9].

10. **ten Brink, H. (2025).** Environmental change can result in irreversible biodiversity loss in recently formed species flocks. *Global Change Biology*. [DOI: 10.1111/gcb.70239][10].

11. **Freitas, O., Campos, P. R. A. & Araujo, S. B. L. (2024).** Patch biogeography under intermittent barriers: Macroevolutionary consequences of microevolutionary processes. *Journal of Evolutionary Biology*, 37, 1488–1498. [DOI: 10.1093/jeb/voae035][11].

12. **Kagawa, K. & Seehausen, O. (2020).** The propagation of admixture-derived adaptive radiation potential. *Proceedings of the Royal Society B*, 287, 20200941. [DOI: 10.1098/rspb.2020.0941][12]. [Code and data: 10.5061/dryad.nzs7h44pv](https://doi.org/10.5061/dryad.nzs7h44pv).

13. **Frei, D., De-Kayne, R., Selz, O. M., Seehausen, O. & Feulner, P. G. D. (2022).** Genomic variation from an extinct species is retained in the extant radiation following speciation reversal. *Nature Ecology & Evolution*, 6, 461–468. [DOI: 10.1038/s41559-022-01665-7][13].

14. **Meier, J. I. et al. (2023).** Cycles of fusion and fission enabled rapid parallel adaptive radiations in African cichlids. *Science*, 381, eade2833. [DOI: 10.1126/science.ade2833][14].

15. **Budd, A. F. & Pandolfi, J. M. (2004).** Overlapping species boundaries and hybridization within the Montastraea “annularis” reef coral complex in the Pleistocene of the Bahama Islands. *Paleobiology*, 30, 396–425. [DOI: 10.1666/0094-8373(2004)030<0396:OSBAHW>2.0.CO;2][15]. [Author-uploaded paper and appendices](https://www.researchgate.net/publication/43449260_Overlapping_species_boundaries_and_hybridization_within_the_Montastraea_annularis_reef_coral_complex_in_the_Pleistocene_of_the_Bahama_Islands).

16. **Levitan, D. R. et al. (2004).** Mechanisms of reproductive isolation among sympatric broadcast-spawning corals of the Montastraea annularis species complex. *Evolution*, 58, 308–323. [DOI: 10.1111/j.0014-3820.2004.tb01647.x][16].

17. **Fukami, H. et al. (2004).** Geographic differences in species boundaries among members of the Montastraea annularis complex based on molecular and morphological markers. *Evolution*, 58, 324–337. [DOI: 10.1111/j.0014-3820.2004.tb01648.x][17].

18. **Neogene Marine Biota of Tropical America (NMITA).** Coral identification tool and associated database pages. [Official resource][18]. A taxonomic/character resource; not a verified specimen-level cascade dataset.

19. **Haller, B. C., Ralph, P. L. & Messer, P. W. (2026; online 2025).** SLiM 5: Eco-evolutionary simulations across multiple chromosomes and full genomes. *Molecular Biology and Evolution*, 43, msaf313. [DOI: 10.1093/molbev/msaf313][19]. [Official SLiM documentation and downloads](https://messerlab.org/slim/).

20. **Tskit Developers.** PySLiM manual: Overview, including recorded ancestry, simplification and historical individuals. [Official documentation][20]. Version to be pinned during implementation.

21. **Uhen, M. D. et al. (2023).** Paleobiology Database user guide. *PaleoBios*. [Primary user-guide PDF][21]. Used for database scope and acquisition context.

22. **Couvert, É. et al. (2024).** Opening the species box: What parsimonious microscopic models of speciation have to say about macroevolution. *Journal of Evolutionary Biology*, 37, 1433–1457. [DOI: 10.1093/jeb/voae134][22]. Conceptual/methodological context for the choice of species representation.

[1]: https://doi.org/10.1073/pnas.0712002105
[2]: https://doi.org/10.1111/eva.13042
[3]: https://doi.org/10.1111/evo.14626
[4]: https://doi.org/10.1111/j.1558-5646.2011.01320.x
[5]: https://doi.org/10.1111/evo.13736
[6]: https://doi.org/10.3389/fgene.2015.00183
[7]: https://doi.org/10.1002/ece3.3507
[8]: https://doi.org/10.1002/ppp3.10546
[9]: https://doi.org/10.1002/evl3.205
[10]: https://doi.org/10.1111/gcb.70239
[11]: https://doi.org/10.1093/jeb/voae035
[12]: https://doi.org/10.1098/rspb.2020.0941
[13]: https://doi.org/10.1038/s41559-022-01665-7
[14]: https://doi.org/10.1126/science.ade2833
[15]: https://doi.org/10.1666/0094-8373(2004)030%3C0396:OSBAHW%3E2.0.CO;2
[16]: https://doi.org/10.1111/j.0014-3820.2004.tb01647.x
[17]: https://doi.org/10.1111/j.0014-3820.2004.tb01648.x
[18]: https://nmita.rsmas.miami.edu/database/corals/identool/taxonkey.htm
[19]: https://doi.org/10.1093/molbev/msaf313
[20]: https://tskit.dev/pyslim/docs/latest/overview.html
[21]: https://escholarship.org/content/qt6tm05630/qt6tm05630.pdf
[22]: https://doi.org/10.1093/jeb/voae134
