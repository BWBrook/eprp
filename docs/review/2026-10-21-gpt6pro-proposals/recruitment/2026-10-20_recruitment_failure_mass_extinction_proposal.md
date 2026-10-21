# Can recruitment failure drive a mass extinction without its expected selectivity?

## A simulation test of life-cycle buffering during the K–Pg marine crisis

**Prepared for:** Barry W. Brook  
**Date:** 20 October 2026  
**Status:** External research proposal for critical consideration; no register identifier assigned  
**Recommended decision:** Develop an analytical and demographic pilot, with a parallel fossil-data audit; expand to a large ensemble only after the decision gates below pass.  
**Repository context:** BWBrook/eprp, main snapshot ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f. The repository was used as read-only context. [R1], [R2], [R3]  
**Research character:** Mechanistic extinction theory with a data-gated K–Pg application. Existing observations, published experiments and simulations; no new field campaign required.  
**What this document contains:** A research question, bounded novelty assessment, explicit estimands, a model hierarchy, data and observation requirements, a CPU-centred execution plan, falsification criteria and an implementation handoff. It reports no new ecological simulation results.

---

## 1. The proposal in one page

**Ask whether failure of larval recruitment can materially cause marine species extinction while leaving little extinction selectivity against species with feeding larvae.**

The question concerns a gap between a physiological mechanism and its expected macroevolutionary signature. If a crisis removes food required by larvae, we might expect species with feeding larvae to suffer greater extinction than species whose offspring are provisioned by their mothers. Yet species extinction is the eventual outcome of an entire life cycle: adults survive or starve, mothers fund eggs, juveniles mature, surviving patches exchange recruits, and populations either recover or lose their final viable individuals. The vulnerable stage and the trait associated with lost taxa need not have a simple relationship.

This is worth testing because the absence of an expected selectivity pattern can be used to argue against a proposed extinction mechanism. A rigorous test should establish when that inference is justified. The proposed study would produce a **map of the conditions under which selectivity is an informative diagnostic**, and of conditions under which it is misleading.

The empirical starting point is a regional K–Pg gastropod comparison with almost identical developmental-mode survival rates. Its authors already evaluated adult buffering, so that intuition is not new. [1]

The proposed advance is to put the argument through a stricter, quantitative test. In the same simulated assemblage, require all three of the following:

1. **Substantial global species loss**, excluding scenarios in which almost everything survives or dies.
2. **A small difference in extinction probability between developmental modes**, first measured with perfect knowledge of simulated species.
3. **A substantial reduction in extinction when larval food alone is restored**, while the rest of the crisis continues.

The third condition is essential. Equal losses between larval types can arise for several reasons. The controlled rescue tests whether restoring larval food can materially prevent extinction despite weak selectivity. Additional factorial contrasts distinguish that result from cases where either larval or postlarval stress can independently cause extinction.

Build the smallest model capable of answering this: an energy-constrained, stochastic age/stage population simulator, extended to a finite metapopulation where necessary. Simulate coherent life-history strategies, including feeding planktonic larvae, nonfeeding planktonic larvae and direct development. Preserve correlations among fecundity, egg investment, maturation, adult survival and dispersal. The K–Pg application would then add uncertain food and temperature histories and an explicit transformation from species survival to sampled genus survival.

The main computational opportunity is **large, paired ensembles across physiological uncertainty, alternative starvation rules, realistic abundance scales, food histories and observation processes**. It does not depend on simulating every organism or on building a new Earth-system model. Kunanyi is well matched to independent replicate families; the A100 is optional for carefully validated emulation.

A strong positive result would show that a consequential larval mechanism can evade its expected signature across an independently supported region of parameter space. A strong negative result would show that the coexistence requires unrealistic populations, survival schedules or trait combinations. Either result would improve how extinction selectivity is interpreted. Merely reproducing an insignificant fossil comparison would not.

## 2. Why this could matter beyond one historical puzzle

The intellectual target is the **transfer from stage-specific injury to taxon-level extinction**.

Physiological stress acts on organisms at particular ages, in particular habitats, at particular moments. Fossil selectivity is commonly measured among named species, genera or clades over much longer intervals. Between these scales lie demographic buffering, correlated mortality, reproductive compensation and taxonomic aggregation. A taxon can possess a highly exposed larval stage yet survive through other parts of its life cycle. Conversely, avoiding larval feeding may carry a reproductive cost when mothers themselves face famine.

The study therefore addresses a general inference problem: **how much can a trait–extinction association tell us about the mechanism that caused the losses?** The larval case offers a clear, biologically interpretable intervention, which makes it a better first test than an unrestricted simulator of every extinction process.

Three potential contributions would justify a substantial paper:

- **A mechanistic feasibility result:** identify or exclude combinations that give severe extinction, weak developmental selectivity and a material larval contribution simultaneously.
- **A diagnostic result:** quantify how often observed weak selectivity would wrongly suggest that larval food limitation was unimportant, and distinguish biological concealment from taxonomic or sampling concealment.
- **An empirical constraint:** establish which K–Pg food-collapse histories and life-history distributions remain compatible with a carefully reconstructed fossil cohort, without pretending to recover uniquely identifiable ancient life tables.

There is also a useful asymmetry in the design. If weak selectivity only appears after fossil sampling, the result concerns observation and statistical power. If it appears among perfectly observed species while the rescue effect remains large, the result concerns biology. Those are different findings and would be reported separately.

The general result stands on its own as extinction theory. Historical application is a demanding test of relevance, rather than a requirement to force a particular explanation of the K–Pg event.

## 3. Relationship to the current eprp programme

The proposal was chosen after reading the main and blue-sky registers at the pinned snapshot. Those registers already occupy many attractive simulation directions. In particular, geographic insurance, access to refugia and the effects of dispersal geometry would be poor choices for a supposedly independent new topic. [R1], [R2]

| Existing question | Shared ingredient | Boundary of this proposal |
| --- | --- | --- |
| Q-014: extinction debt after a deep-time perturbation | Delayed population loss | The target here is the diagnostic relationship between larval injury and developmental-mode selectivity, rather than a general chronology of extinction debt. |
| Q-020: when geographic range stops providing insurance | Spatial survival and recolonisation | Space is included only to make global extinction and rescue credible. The principal contrast is a stage-specific food intervention. |
| Q-023: origination failures versus extinction spikes | Failure of biological replacement | Recruitment means new individuals entering a population; origination means new species. The crisis model holds the species cohort fixed. |
| Q-030: changing biosphere sensitivity | Physiological susceptibility and clade composition | This tests an explicit within-life-cycle causal contrast, rather than a secular trend in biosphere susceptibility. |
| Q-038: predictability of which genera die | Trait selectivity and imperfect observation | Prediction is an output here; the distinguishing target is whether a controlled larval rescue reveals causation concealed by weak selectivity. |
| Q-042: how many species died | Species-to-genus aggregation | The mapping is needed for honest comparison with the fossil table. Estimating total species loss from generic diversity is not the main question. |
| B-002: juvenile viability blocking adult ammonoid innovations | Different constraints at different stages | This concerns demographic survival during famine, rather than developmental feasibility of an adult morphological innovation. |
| B-008 and B-012: refugia and dispersal strategy | Spatial population structure | Neither consistent refuge locations nor reversal of dispersal’s evolutionary value is the intended discovery. |

These distinctions should be revisited by the repository agents before assigning an identifier. The proposal is a candidate to evaluate alongside that programme, not an instruction to reopen or renumber existing entries.

## 4. The empirical hook is real, but its precision is limited

The original gastropod count table is:

| Developmental category | Extinct genera | Surviving genera | Genera assessed | Extinction fraction |
| --- | ---: | ---: | ---: | ---: |
| Planktotrophic: feeding larvae | 17 | 11 | 28 | 60.7% |
| Nonplanktotrophic | 14 | 9 | 23 | 60.9% |
| Total | 31 | 20 | 51 | 60.8% |

These are genera in a regional study cohort, not a global species-extinction estimate. Developmental assignments used larval-shell evidence. [1]

Recalculation from the published counts gives an extinction-risk difference, feeding minus nonfeeding, of **−0.16 percentage points**. A Wilson/Newcombe independent-binomial 95% interval is approximately **−25.1 to +25.3 percentage points**; Appendix A provides the arithmetic and method reference. [28] This descriptive interval ignores phylogenetic dependence, taxonomic uncertainty and fossil observation. It demonstrates why similar point estimates should not be treated as established biological equivalence.

The immediate empirical object is consequently the **observed count table and its uncertainty**, rather than a precisely known zero effect. A stronger claim requires recovering the taxa and their coding.

There are reasons to take that audit seriously. Gastropod protoconch preservation and developmental interpretation are uneven, and later reviews do not constitute independent replications of the original comparison. [3] A global echinoid analysis also reported no significantly greater loss among clades with feeding larvae, while placing more explanatory weight on adult ecology; that is an important conceptual precedent, not evidence that every marine group behaved identically. [2] Developmental strategies also changed before the boundary: a spatangoid phylogenetic study identified several independent Late Cretaceous transitions toward nonplanktotrophy. [17]

The proposal should therefore avoid the phrase “the universal larval-selectivity paradox.” Its empirical claim is narrower: **a historically influential weak-selectivity result motivates a quantitative examination of what such a result can diagnose**.

## 5. What is already known, and what remains worth doing

The following is a bounded novelty audit of primary literature and available code or data descriptions. It is not a guarantee that no relevant unpublished or inaccessible model exists.

| Closest precedent | What it already establishes or models | Residual addressed here |
| --- | --- | --- |
| Valentine & Jablonski (1986) [1] | Developmental-mode comparison; rejection of adult waiting-out under severe mortality/prolonged recovery; related size/lifespan arguments. | Quantitative testing of that demographic rejection and its auxiliary predictions, with finite populations and controlled rescue worlds. |
| Smith & Jeffery (1998) [2] | K–Pg echinoid selectivity interpreted in relation to adult as well as larval ecology. | A causal decomposition that distinguishes a consequential larval pathway from an adult-only explanation. |
| Robertson et al. (2013) [5] | An impact-winter synthesis linking food supply, survival and recovery across aquatic environments. | A falsifiable demographic compatibility analysis, with the mechanism separated from the fossil observation process. |
| Gibbs et al. (2020) [7] | Plankton recovery through size/trophic strategies; public code includes low-biomass extinction and Allee terms. | Finite benthic species with linked adult reproduction, larval development and taxonomic survival. |
| Ying et al. (2026) [6] | A global ocean/biogeochemical simulation of K–Pg plankton functional-type extinction involving darkness and size. | Explicit benthic life cycles and the mapping from stage-specific damage to species and genus loss. |
| Sarà (2026) [8] | Individual energy-budget responses to feeding interruption, reserve state, duration and life stage; public code describes alternative starvation hazards. | Population and taxon extinction, coherent larval-mode strategies, controlled food rescue and fossil selectivity. |
| Bradshaw et al. (2021) [16] | Stochastic age-structured simulations testing demographic explanations of a palaeoextinction chronology. | A marine food-collapse contrast with stage-specific interventions and genus-level observation. |
| McQuaid & Chambers (2025a,b) [9], [10] | Paired developmental strategies with different demography and reproductive investment. | These constrain the model; the simulation cannot treat reproductive traits as freely interchangeable. |
| Holland & Patzkowsky (2015) [20] | Simulation of stratigraphic processes that distort fossil last occurrences. | The biological inference must remain valid before, and be tested after, a declared observation model. |

**The defensible novelty claim is:** a quantitative test of the joint compatibility of severe finite-population extinction, weak developmental-mode selectivity and a substantial controlled larval-food-rescue effect, followed through the species-to-genus observation process.

This excludes four tempting but occupied claims: that adults can buffer a recruitment failure; that reserve state matters during starvation; that disturbance duration can differ from cumulative deficit; and that a sophisticated K–Pg ecosystem simulation is newly possible. Their prior demonstration strengthens the foundation but narrows the contribution.

Before full implementation, conduct one final focused literature check for an existing model that already combines the proposed estimands. If such a study exists, compare its intervention, abundance scale, empirical support and taxonomic mapping directly. A change of programming language or a larger parameter sweep would not establish novelty.

## 6. Define the test before writing the simulator

### 6.1 The biological unit and the outcome

Begin with a fixed cohort of gastropod-like species present immediately before the disturbance. The primary theoretical domain includes the full simulated geographic range of every species.

For species i, let Y_i(H) equal one if **no viable individuals remain in any explicitly modelled stage or patch by horizon H**, and zero otherwise. Viable eggs, broods, larvae, settled juveniles and adults all count. There is no new speciation in the principal crisis experiment and no unmodelled external immigration.

Loss of all reproductive adults while viable offspring remain is not extinction. Neither is a surviving but reproductively failing adult population. Record these as demographic states that can precede extinction.

Use identical follow-up horizons in matched worlds. Proposed primary horizons are 100 and 1,000 years after onset, for the initial forcing family whose deficit and recovery window ends within the first 100 years. These are design choices, not claims about fossil resolution. Report both endpoints and extinction-time distributions. Longer forcing scenarios require a separately declared horizon and analysis rather than being mixed silently into the primary comparison.

### 6.2 Five matched worlds

The core experiment has four food-exposure worlds plus a no-event baseline:

| World | Larval food | Postlarval food | Other event conditions |
| --- | --- | --- | --- |
| Y11 | Event trajectory | Event trajectory | Event trajectory |
| Y01 | Larval deficit rescued | Event trajectory | Event trajectory |
| Y10 | Event trajectory | Postlarval deficit rescued | Event trajectory |
| Y00 | Both deficits rescued | Both deficits rescued | Event trajectory |
| Ybase | No-event trajectory | No-event trajectory | No-event trajectory |

The first index is larval food stress; the second is postlarval food stress. “Postlarval” includes settled juveniles and adults. Maternal provisioning is generated by adult energetics, so it responds to the postlarval intervention. The food-restored Y00 world can still experience event-related cooling or other declared hazards; it is therefore distinct from Ybase.

All worlds begin with the same populations, trait draws and geography. Use appropriately indexed common random streams to reduce Monte Carlo noise, without forcing divergent populations to share an impossible future. The table describes prescribed food trajectories. In the shared-resource extension, the same factorial interventions hold external forcing and non-target supply rules fixed while allowing endogenous resources to respond.

### 6.3 What the rescue does

Use a specified **attainable-ration intervention**, rather than leaving “food restoration” ambiguous. Store the paired no-event food trajectory first. During the declared deficit-and-recovery window, evaluate normal attainable assimilation from that reference food at each recipient’s current size, stage and event temperature. Add only the missing edible ration needed to reach that rate when event food provides less. Keep normal ingestion limits, food quality requirements, development and background mortality. The intervention supplies neither perfect survival nor unlimited food.

This is an intentionally artificial intervention used to ask a causal question inside the model. Book the added food and its energy/nutrients as an external subsidy. Its delivery is restricted to the specified stage. In the shared-resource extension, later excretion, death, settlement and competition by rescued organisms can legitimately affect other consumers and resources; these downstream effects follow the declared ecological model. They must be distinguished from an accidental direct subsidy to adults.

The intervention holds **external exposures and physiological rules** fixed outside the rescued food pathway. It does not hold adult abundance fixed. Rescued larvae must be allowed to settle, grow, compete and reproduce; preventing those downstream effects would destroy the mechanism being measured.

In the first, prescribed-food model, isolate the physiological pathway without shared-resource feedback. In a later shared-resource model, report the additional ecological consequences of the subsidy separately. Increased recruitment can increase subsequent competition, so rescue effects need not be positive in every replicate. Never enforce monotonicity.

As an implementation check, apply the same deficit-restoration operator in a no-event world. It should add no food and change no outcome.

### 6.4 Primary estimands

Evaluate the following quantities within a fixed initial assemblage/trait draw, forcing scenario, model form and horizon. Expectation averages demographic and declared environmental stochastic replicates, with the initial species cohort as denominator. Repeat this entire test across biological draws; do not pool different forcing regimes or opposing assemblage responses to make the joint screen pass.

For the main theoretical experiment, fix design weights at 50% PT, 25% nonfeeding planktonic and 25% direct-developing species. These are balanced experimental weights, not inferred ancient frequencies. Repeat with other declared compositions and report the whole-cohort rescue effect as well as the PT-conditioned contrast.

**Total and event-excess extinction:**

$$
M = \frac{1}{n}\sum_i \mathbb{E}[Y_{i,11}],
\qquad
M_{\mathrm{base}} = \frac{1}{n}\sum_i \mathbb{E}[Y_{i,\mathrm{base}}],
\qquad
M_{\mathrm{excess}} = \frac{1}{n}\sum_i \mathbb{E}[Y_{i,11}-Y_{i,\mathrm{base}}].
$$

**Developmental-mode selectivity:**

$$
S = \mathbb{E}[Y_{11}\mid \mathrm{PT}]
  - \mathbb{E}[Y_{11}\mid \mathrm{NPT}].
$$

PT denotes feeding planktonic larvae. NPT denotes the declared mixture of nonfeeding planktonic and direct-developing strategies. Also report the two separate PT comparisons; a pooled NPT category must not hide different responses.

Report event-induced selectivity as well:

$$
S_{\mathrm{excess}} =
\mathbb{E}[Y_{11}-Y_{\mathrm{base}}\mid\mathrm{PT}]
-
\mathbb{E}[Y_{11}-Y_{\mathrm{base}}\mid\mathrm{NPT}].
$$

Raw selectivity can be near zero because the event removes a pre-existing advantage. That differs from equal event effects on initially equivalent strategies.

**Controlled larval-food rescue effect:**

$$
R_L=\mathbb{E}[Y_{11}-Y_{01}\mid\mathrm{PT}].
$$

An R_L of 0.10 means that restoring ordinary larval food reduces mean extinction probability by ten percentage points among the initial PT cohort under the specified continuing event. It is an intervention effect, not a uniquely attributable fraction of all deaths or extinctions.

Put this effect on the same denominator as M:

$$
\Delta_L=\frac{1}{n}\sum_i\mathbb{E}[Y_{i,11}-Y_{i,01}].
$$

With prescribed food and no effect of larval rescue on NPT species, Delta_L equals the PT frequency times R_L. Shared-resource effects can break that identity, so report both quantities. A large effect in a very rare developmental category need not represent a large effect on assemblage extinction.

Report the postlarval contrast and interaction on the same PT cohort:

$$
R_P=\mathbb{E}[Y_{11}-Y_{10}\mid\mathrm{PT}],
$$

$$
I_{LP}=\mathbb{E}[Y_{11}-Y_{10}-Y_{01}+Y_{00}\mid\mathrm{PT}].
$$

A large interaction means stage effects cannot be added to assign unique shares of responsibility. Also report

$$
R_{L\mid P=0}=\mathbb{E}[Y_{10}-Y_{00}\mid\mathrm{PT}],
\qquad
R_{\mathrm{food}}=\mathbb{E}[Y_{11}-Y_{00}\mid\mathrm{PT}],
$$

and corresponding whole-cohort quantities. The first measures larval rescue with postlarval food already restored; the second measures joint food rescue under continuing nonfood event conditions.

A zero single-stage rescue is not proof of an unimportant mechanism. For example, Y11 = Y01 = Y10 = 1 and Y00 = 0 describes redundant lethal food pathways: neither rescue alone prevents extinction, but the joint rescue does. The principal positive test uses R_L as a clear preventive effect under continuing postlarval stress; it is not an exhaustive definition of larval causal importance.

### 6.5 A deliberately demanding challenge region

For the pilot, use the following operational screen:

$$
\mathcal{C} =
\left\{
M_{\mathrm{excess}}\geq0.30,\;
M\leq0.85,\;
M_{\mathrm{base}}\leq0.05,\;
|S|\leq0.05,\;
R_L\geq0.10,\;
\Delta_L\geq0.05
\right\}.
$$

These cut-offs are **proposed design thresholds**. They are not estimates of K–Pg global species loss, an agreed definition of mass extinction, or a claim that the fossil data establish five-percentage-point equivalence.

Publish the continuous joint response surface and sensitivity to sensible alternative margins. Uncertain Monte Carlo classifications near the boundary remain uncertain; they should not be rounded into success. Show between-assemblage distributions, opposite selectivity signs, and the frequency of nearly complete survival or loss. Passing only by averaging all-survive and all-die outcomes is a bimodal catastrophe regime, not evidence for the intended partial-extinction result.

Finding a single member of this region is insufficient. The result must occupy a reproducible, non-negligible region under several independently defensible joint trait distributions, with an interpretable mechanism. Its weight under an ensemble is conditional on that ensemble’s assumptions. It is not the probability that larval famine caused the historical extinction.

## 7. An analytical gate that could save most of the compute

Before building a large simulator, ask whether a recruitment interruption can plausibly eliminate a geographically widespread species at all.

Consider N_A original adults, with independent probability s_A(D) of surviving a food interruption of duration D. The probability that none of those adults remains at the end is

$$
P_0(D)=[1-s_A(D)]^{N_A}
\approx \exp[-N_A s_A(D)]
$$

when s_A is small. If adult mortality has a constant hazard mu, so that s_A(D)=exp(−mu D), the transition toward order-one surviving adults occurs roughly when

$$
D \sim \frac{\log N_A}{\mu}.
$$

This is an analytical limiting case, not a complete extinction formula. It ignores survivors’ reproductive prospects, sex structure, recruitment during the event, age dependence and correlated mortality. Its importance is the scale constraint: a short loss of recruitment combined with even a small surviving fraction of a very large adult population usually leaves many adults.

For illustration only, with one million original adults and survival probability 10^-3, the expected number remaining is 1,000 and the independent no-survivor probability is approximately exp(−1,000). With survival probability 10^-6, the expected number is one and the approximation is exp(−1), about 0.37. These are constructed arithmetic examples, not palaeontological abundance estimates.

The age-structured version uses a product over cohorts or individuals with different survival probabilities. Correlated exposure must be represented explicitly rather than folded into an artificially small “effective population.” A lethal environmental threshold shared across a habitat can behave very differently from independent individual mortality.

This gate identifies what the full model must resolve:

- Does a plausible event leave almost no viable breeders, or does it merely interrupt replenishment?
- Can surviving adults reproduce before their remaining lifespan ends?
- Do provisioning, juvenile development and food recovery create a genuine gap between surviving adults and replacement breeders?
- Are mate limitation or fertilisation thresholds supported well enough to matter?
- Can surviving patches recolonise the rest of the range?
- Does the event impose correlated mortality across enough of that range?

**Stop or simplify if the answer is already controlled by this limit.** A clean analytical result about why recruitment failure cannot generate the relevant global losses would be valuable. It would not justify a much larger model merely to make the project look computationally ambitious.

## 8. The simulation hierarchy

### 8.1 Level 0: demographic reference models

Implement a transparent age/stage matrix or cohort model with prescribed survival and recruitment. Include a no-recruitment experiment, an age-specific adult-survival experiment and a known branching-process limit.

Its purpose is to establish the large-population constraint, distinguish finite-time extinction from decline, and identify dimensionless quantities worth exploring: deficit duration relative to reserve endurance, time to maturity, remaining breeder lifespan and the replacement interval.

This is also the independent reference implementation against which the faster kernel will be checked. It should remain small enough to read and reason about.

### 8.2 Level 1: energy-constrained life cycles with prescribed food

Represent eggs or broods, feeding or nonfeeding larvae, settled juveniles and adults. Track age or developmental progress, structural size and reserve state sufficiently well to preserve delayed development and starvation heterogeneity.

A generic bookkeeping identity for stage s is

$$
\frac{dE_s}{dt}
=
A_s(F,T,\mathbf{z})
-
C_{\mathrm{maintenance},s}
-
C_{\mathrm{growth},s}
-
C_{\mathrm{maturation},s}
-
C_{\mathrm{reproduction},s},
$$

where E is reserve energy, A is assimilation, F is the relevant food field, T is temperature and z contains traits. This is a conservation requirement, not a replacement for a specified DEB formulation. Allocation rules and maintenance priority must be explicit and validated against an existing implementation. AmP provides a structured foundation for such parameterisation, while distinguishing observations, fitted parameters and model-implied traits. [13], [14]

Use two levels of physiology where support allows: a parsimonious reserve-and-vital-rate model, and a documented DEB variant. Agreement between them matters more than adding unverified physiological detail.

Critical biological requirements are:

- **Provisioning costs.** Larger, nonfeeding offspring consume maternal reproductive investment. Their protection is not free.
- **Developmental delay.** Food shortage can slow growth and affect post-metamorphic performance, rather than simply killing every feeding larva immediately. Experimental gastropod work provides a relevant precedent. [12]
- **Post-settlement vulnerability.** Both feeding and nonfeeding strategies can fail when juveniles begin feeding.
- **Age and reserve distributions.** A species is not represented by one average adult. Conversely, unbounded longevity or reserve tails must not create effectively immortal survivors.
- **Reproductive timing.** Seasonality, spawning opportunities and maturation delays determine whether survivors can replace themselves.
- **Temperature.** Cooling can alter maintenance, ingestion, development and direct mortality. It must not be encoded as automatically beneficial because one metabolic term slows.
- **Compensation.** Density dependence may make a large reduction in larval production produce only a small reduction in successful recruits. The degree of compensation must be explicit.
- **Finite reproduction.** Egg production, survival and settlement generate actual individuals or correctly scaled counts, not fractional organisms that persist forever.

Keep a species’ strategy coherent. The intervention changes food availability; it does not instantly turn a planktotroph into a lecithotroph while preserving all its fecundity, provisioning and dispersal advantages.

### 8.3 Level 2: finite metapopulations

Add space only after the nonspatial models reveal a boundary that spatial population dynamics could change.

Start with synthetic shelf networks, declared habitat area and depth classes, rather than an expensive full-ocean reconstruction. Give each species an occupied range, local densities and a dispersal kernel or transport matrix. Nonfeeding planktonic larvae can disperse; direct development is a separate strategy. Both recolonisation and retention matter.

Track demographic variation separately from correlated environmental variation. Vary connectivity, spatial correlation of food collapse, range extent and refuge size independently only where biologically meaningful; otherwise preserve their joint constraints.

Convert density and habitat area into explicit population counts. If many individuals are represented by cohorts or weighted particles, elimination of one computational representative must not be equated with species extinction. A hybrid method may use efficient high-abundance transitions and exact integer dynamics near extinction, but the switching rule requires convergence and scaling checks.

The spatial domain must include potential source populations. A regional model with a closed boundary can measure regional loss; it cannot establish global extinction merely by labelling its last patch “the world.”

### 8.4 Level 3: limited resource feedback

Only add shared resources if they change the primary inference in targeted sensitivity experiments.

Use a small set of food pools that preserves the important pathways: edible suspended plankton, detrital/microbial resources and food available to benthic adults or juveniles. Supply, consumption, transfer and decay must balance. Diets can depend on size and quality; a scalar multiplier of net primary production is not an adequate universal food variable.

This level can test whether detrital buffering, changed food composition or competition after rescue alters the compatibility region. Published plankton models are useful precedents and possible forcing sources, but their functional-type biomasses cannot be substituted directly for benthic species life histories. [6], [7]

A complete food web, evolving genomes and a new ocean circulation model are outside the first paper. Their addition would require evidence that the simpler hierarchy misses a decisive mechanism.

### 8.5 Evolutionary scope

The principal experiment studies extinction of an existing species cohort. It does not generate diversification over millions of years, and a mass-extinction question does not require speculative speciation machinery to qualify as deep-time research.

A later extension could ask whether repeated crises change the distribution of developmental strategies, after allowing background origination and inherited life-history covariance. That becomes worthwhile only if the initial study identifies a robust selection mechanism and enough data exist to test its longer-term consequences.

## 9. Environmental histories, traits and data readiness

### 9.1 Separate the forcing from the food organisms can use

Start with generic, declared food histories: abrupt interruption and recovery; partial reduction; a short severe deficit versus a longer mild deficit; and delayed restoration of benthic food. Their purpose is to discover the demographic boundaries, not to reconstruct an impact by fitting arbitrary curves.

Represent at least four distinct quantities where relevant: light available for production, edible suspended food, benthic food stocks/fluxes, and temperature. A collapse in photosynthesis does not by definition remove every detrital or microbial food source. Conversely, restoration of total biomass does not guarantee restoration of the food sizes and qualities required by a particular consumer. The published impact-winter and plankton studies motivate these distinctions but do not directly supply benthic demographic exposure. [5], [6], [7]

The K–Pg application can use Senel et al.’s impact-winter scenarios and Ying et al.’s ocean simulations as linked forcing representations. Ying uses Senel-derived solar forcing, so they do not provide independent upstream environmental evidence. [24], [6] Their archives are leads to inspect, not pre-certified inputs. Before importing a variable, establish its units, spatial support, output cadence, spin-up reference, experiment identity and whether it represents the consumer’s actual resource.

A model’s internal timestep is not the archive’s output interval. If only coarse averages are available, use explicitly bracketed subinterval scenarios; interpolation cannot recover missing starvation episodes. Do not infer year-by-year recruitment failure from a stage-averaged palaeoproxy.

The primary intervention concerns food. Add cooling and other direct hazards as separately specified alternatives where evidence supports them. Avoid estimating unconstrained oxygen, pH, toxicity and adult mortality curves simultaneously from one small extinction table.

### 9.2 Build organisms from joint biological constraints

The main parameter distribution should preserve relationships among adult size, energy stores, maximum attainable age, fecundity, egg investment, larval development, maturation and dispersal.

The paired modern Siphonaria studies are especially useful because contrasting developmental strategies occur in closely related, co-occurring limpets, with demographic and reproductive-energy observations. They offer a way to construct coherent strategy bundles, although their rocky-shore ecology does not make them direct Cretaceous substitutes. [9], [10]

Use modern observations to constrain possible mechanisms and ranges, then carry uncertainty in transferring them to extinct taxa. Fossil shell size can constrain a morphological quantity; it does not measure an ancient starvation-survival curve. Distinguish these evidence levels in every parameter manifest:

| Evidence level | Example | Treatment |
| --- | --- | --- |
| Direct observation | Size, temperature, food treatment and survival measurements in a modern experiment | Retain sampling error, censoring and experimental conditions. |
| Fitted physiological parameter | An AmP estimate inferred jointly from growth and respiration data | Retain model dependence and parameter covariance. |
| Model-implied trait | Longevity or reproduction predicted by fitted parameters | Do not count it as independent validation of the same model. |
| Borrowed quantity | A parameter supplied from a related species or pseudo-data | Flag the transfer and test its influence. |
| Fossil inference | Developmental coding, body size, adult guild or range | Retain ambiguity, taxonomy and observation support. |
| Deliberate stress test | Extreme abundance, reserve tail or food-interruption duration | Keep outside the biological prior unless independently justified. |

A gastropod starvation synthesis provides a route to lineage/habitat heterogeneity; full curve and supplement extraction remains necessary. [11] The Laternula DEB study is useful for adult seasonal energetics, but explicitly does not model larval development. It cannot validate the proposed larval pathway. [15]

Fix the principal joint distributions before searching for the challenge region. Report alternative defensible covariance assumptions, and show whether apparent concealment depends on finely tuned compensation between dispersal, fecundity and endurance.

### 9.3 Source and access ledger

“Verified” below describes what was inspected while preparing this proposal. It does not imply that a package was executed or a dataset cleaned.

| Resource | Verified support | Immediate next task |
| --- | --- | --- |
| Original gastropod comparison [1] | All three scanned article pages inspected; aggregate table checked. | Recover the original genus list, assignments and survival evidence. |
| Subsequent Cretaceous mollusc work [4] | Relevant larval-mode/range and background-survivorship analysis identified; abstract and indexed methods inspected. | Obtain the full taxon-level material and determine whether it resolves the original cohort. |
| Echinoid comparison [2] | Publisher abstract and figure descriptions inspected. | Obtain full article/data before using it as an independent fitted test. |
| Paired Siphonaria [9], [10] | Demographic publisher abstract and companion energy-budget full text inspected. | Extract demographic tables and assess raw-data availability. |
| AmP [13], [14] | Primary project paper and current portal organisation inspected. | Pin relevant entries; read their empirical-input files, parameters and references separately. |
| Sarà model [8] | Primary abstract and public package description inspected; archive lists code, forcing and outputs. | Download, inspect and reproduce a bounded case. |
| Ying model [6] | Full main article/Methods and relevant public source files inspected. | Audit archive contents and cadence; separate supplementary PDF was not retrieved. |
| Senel forcing [24] | Primary paper record and linked archive identified. | Audit downloadable variables and temporal/spatial resolution. |
| Gastropod starvation [11], [12] | Primary abstracts inspected; quantitative extraction incomplete. | Recover experimental curves and uncertainty before parameter fitting. |
| Laternula physiology [15] | Full paper and relevant methods inspected. | Use for adult-module checks within its declared scope. |
| Lockwood abundance/ecology [18] | Full article inspected. | Assess available supplement and whether its bivalve information can constrain a relevant sensitivity check. |
| Bryozoan developmental data [19] | Primary study and Dryad record inspected. | Optional observation/power check with its different biology and time support. |

Useful stable entry points are:

- **Sarà data/code:** [Mendeley Data, 10.17632/r2h822zzxp.1](https://doi.org/10.17632/r2h822zzxp.1), with CC BY 4.0 declared by the archive.
- **Ying model:** [cgenie.muffin, rui_kpg branch](https://github.com/ruiying-ocean/cgenie.muffin/tree/rui_kpg); [experiment configurations](https://github.com/ruiying-ocean/cgenie.muffin/tree/rui_kpg/genie-userconfigs/PUBS/submitted/Ying_et_al.Nature.2025); [analysis repository](https://github.com/ruiying-ocean/kpg_selectivity); [output archive, 10.5281/zenodo.17742290](https://doi.org/10.5281/zenodo.17742290).
- **Gibbs model:** [MCM release 1.0](https://github.com/geebes/MCM/tree/1.0), archived at [10.5281/zenodo.3701302](https://doi.org/10.5281/zenodo.3701302).
- **Senel archive:** [OSF, 10.17605/OSF.IO/2CDQG](https://doi.org/10.17605/OSF.IO/2CDQG).
- **AmP:** [official portal](https://debtheory.fr/add_my_pet/) and [species list](https://debtheory.fr/add_my_pet/species_list.html).
- **Fossil occurrences:** [Paleobiology Database data service](https://paleobiodb.org/data1.2/). [27]
- **Optional bryozoan data:** [Dryad, 10.5061/dryad.1vhhmgr44](https://doi.org/10.5061/dryad.1vhhmgr44), with supporting material at [Zenodo, 10.5281/zenodo.14104270](https://doi.org/10.5281/zenodo.14104270).
- **Palaeodemographic precedent:** [MegafaunaSusceptibility code](https://github.com/cjabradshaw/MegafaunaSusceptibility). [16]

Record the actual licence and version for every imported component. Public availability and permission to redistribute an integrated derivative are separate questions; record that information during normal dependency selection, without making it an obstacle to the present proposal.

## 10. The fossil application: recover the cohort, then simulate its observation

### 10.1 A bounded empirical gate

The original short article does not supply a complete machine-readable list of all evaluated genera. Recovering identities and coding is therefore a specific first task, rather than an assumed property of an occurrence download.

Construct a versioned crosswalk with original name, accepted name, revision source, constituent species where recoverable, developmental assignment, evidence for that assignment, pre-boundary presence, survival evidence, and geographic support. Retain unresolved names and competing interpretations. If revisions change the apparent selectivity, determine whether taxonomy, trait coding, sampling or the cohort denominator changed.

Later work on larval ecology and geographic range is a lead for that reconciliation; background species survivorship is not automatically an updated boundary-extinction dataset. [4]

If the original cohort cannot be recovered reliably, retain its aggregate result as motivation and proceed with the theoretical paper. A new fossil cohort would need inclusion rules specified independently of the desired answer. Do not expand data collection indefinitely to rescue a preferred historical narrative.

### 10.2 Population → species → genus → recorded occurrence

The biological and observational mapping must remain explicit:

1. Local loss is the disappearance of a population from a patch.
2. Species extinction requires loss of all viable stages throughout its biological domain.
3. A genus from the initial cohort survives if at least one of its constituent species survives.
4. Recorded survival additionally requires detection and an appropriate taxonomic assignment in the observation window.

With fixed genus membership and no speciation during the crisis, latent genus extinction is

$$
Y_g = \prod_{i\in g}Y_i.
$$

The probability of this event is not generally the product of marginal species-extinction probabilities: related species can share traits, ranges and exposure.

Simulate several supported distributions of species per genus, correlated vulnerability and mixed developmental modes. If those cannot be constrained sufficiently, bracket the mapping and keep the historical conclusion correspondingly broad. Do not treat a species-level model result as a genus-level estimate.

Distinguish three domains: where the cohort was selected, where fossils were observed, and the geographic range over which biological extinction is defined. Check whether a published survivor was documented locally or elsewhere. A taxon absent from the Coastal Plain but present elsewhere has not become globally extinct.

### 10.3 Developmental coding and occurrence uncertainty

Record whether larval mode comes from a preserved protoconch, another species in the genus, or a broader phylogenetic inference. Ambiguous genera and mixtures remain uncertain rather than being assigned to the category that improves model agreement. Multiple shell criteria and uneven preservation make an evidence-based coding model preferable to automatic binary classification. [3]

PBDB can augment taxonomy, occurrence distributions and sampling support, but it does not automatically supply verified developmental assignments. Preserve the original identification, subsequent revision and accepted name where available. [27]

Occurrence counts, collections, species, genera and independently supported larval assignments are different sample sizes. Repeated records of one taxon are not independent evolutionary trials. Group observation effects by the relevant locality, formation and taxonomic source; treat clade dependence separately from sampling dependence.

Use a generative observation model for detection in declared pre- and post-boundary windows. Include, where consequential, missing collections, age uncertainty, facies shifts, reworking and delayed reappearance. Stratigraphic simulation already demonstrates why last occurrences need not coincide with biological extinction. [20] Spatial sampling and false extinction assignments also warrant explicit sensitivity checks. [21]

The biological model may resolve hours or days during a famine while the fossil comparison uses a boundary-crossing endpoint. Annual fossil resolution is not required. The study must, however, avoid comparing a 1,000-year biological outcome with a much longer fossil interval as if background turnover in the intervening time were absent.

### 10.4 What historical inference would be justified?

Begin with synthetic observations at the actual cohort size and uncertainty. Ask whether they distinguish models with substantial R_L from models with negligible R_L after taxonomic aggregation and sampling, retaining the other factorial contrasts to identify redundant pathways. Report the result even if the answer is that the existing cohort cannot discriminate them.

An insignificant PT–NPT comparison is not an equivalence result. Predefine any equivalence margin, propagate the relevant uncertainty, and assess whether the observed data can support that precision.

Keep two selectivity estimands: the total association among realistic strategy bundles and an explicitly standardised comparison over a declared common trait/range distribution. Geographic range can be part of a developmental strategy’s pathway to survival; automatically adjusting it away changes the question. A regression coefficient for larval mode is not itself the controlled food-rescue effect.

The optional cheilostome bryozoan dataset supplies coded developmental and occurrence evidence, but its broad Maastrichtian–Thanetian analysis and colony biology make it an observation/power check, not an interchangeable K–Pg gastropod replication. [19] The echinoid comparison is a possible later external test once its primary data and subgroup coding have been audited. Neither extension should delay the theoretical experiment.

## 11. Competing explanations and the patterns that distinguish them

The experiment should not search only for a favourable mechanism. Run the following predeclared model comparisons:

| Explanation | Expected diagnostic pattern | Decisive check |
| --- | --- | --- |
| Recruitment interruption is mostly buffered | Low event-excess global loss or a small rescue effect over the relevant window | Extend follow-up; test realistic adult abundance, remaining lifespan and recovery timing. |
| Larval and postlarval pathways interact | A material R_L with an interaction that changes across timing and reserve regimes | Restore each food pathway separately and both together. |
| Larval rescue alone cannot prevent most losses | Severe extinction but negligible R_L | Use postlarval, conditional and joint rescues to distinguish postlarval-dominated loss from redundant lethal pathways. |
| Strategy trade-offs conceal selectivity | Small S but meaningful effects revealed by changing supported trait covariance | Fixed-prior, targeted ablations of range, provisioning and longevity correlations. |
| Genus aggregation conceals species selectivity | S is appreciable among species but attenuated among genera | Change species richness and within-genus vulnerability dependence without changing biology. |
| Fossil information is insufficient | Latent selectivity is appreciable, but sampled tables often look inconclusive | Compare perfect observation, taxonomic aggregation alone and full observation error. |
| Food rescue cannot overcome other continuing hazards | Limited food rescue despite severe loss | Use hazard-only, food-only and combined-exposure worlds to distinguish dominance from redundant causes. |
| Almost universal loss erases differences | Small S occurs only near saturation | Enforce the nondegenerate severity criterion and show the full response surface. |

Additional response variables should reveal the mechanism: minimum viable breeder count, age distribution after the event, reserve quantiles, reproductive output, time until first successful post-event recruitment, occupied patches and the timing of final species loss. These are simulator diagnostics. They should not be advertised as recoverable fossil measurements unless corresponding evidence exists.

The most useful empirical prediction may be an interaction—developmental mode with independently inferred adult ecology or life-history scale—rather than a universal main effect of larval type. Select a small number of such predictions from the mechanism study, freeze them, and evaluate them on withheld fossil or modern evidence. Avoid screening many covariates on the historical table and then presenting the best one as a forecast.

## 12. Analysis strategy: robust boundaries before historical fitting

Use an initial space-filling design over a manageable number of scientifically meaningful factors. Sample biological parameters from joint distributions; use targeted changes to forcing, abundance and model structure. Do not construct a full factorial over dozens of independent, biologically incompatible traits.

After the first pilot, concentrate replication near boundaries in M, S and R_L, while retaining a predeclared independent validation sample. Adaptive sampling should improve precision rather than select only successful regimes. Separate Monte Carlo uncertainty from uncertainty about physiology, trait distributions, forcing and fossil observation.

For each ensemble, report:

- The joint response surface and the location of the challenge region.
- The continuous distribution of rescue effects, including negative values where they occur.
- Mechanistic explanations of boundary shifts, supported by targeted ablations.
- Sensitivity to trait covariance, rare survival tails, abundance scale and model form.
- The fraction of the declared ensemble meeting the screen, with uncertainty and its dependence on the chosen weighting.
- The diagnostic performance of a weak-selectivity observation for distinguishing a consequential from a negligible larval-food effect.

For diagnostic performance, distinguish an ideal observer of every species, an observer of perfectly known genera, and an observer of the fossil data. Prespecify the decision rule and report both false-negative and false-positive rates under the declared generating models. There is no universal error rate independent of the mixture of possible crises and life histories.

Keep historical inference modest initially: identify **compatible and excluded regions** rather than fit a unique ancient parameter vector. Many combinations of duration, reserves, food quality, spatial refuge and population size may produce the same genus table. More simulation does not remove that identifiability problem.

If simulation-based inference or a learned classifier becomes useful, test calibration on withheld simulations and test robustness by withholding an entire physiological model, forcing family or trait-covariance structure. A distinct forcing family must differ in relevant upstream assumptions: holding out the Ying ocean response after using its Senel-derived forcing does not establish independent forcing validation. Randomly splitting rows from one simulator is inadequate evidence that inference will work when the actual biological mechanism differs. Decisive emulator predictions must be confirmed by direct simulation.

## 13. Implementation and compute plan

### 13.1 Reproduce one existing physiological result first

Use the archived Sarà model for a bounded reproduction exercise: one control trajectory and one published disturbance contrast. Its described package provides Python modules, hourly forcing and factorial results. [8] Check reserve, survival, maturity and reproduction definitions and units; record discrepancies before extending any component.

This is a proposed implementation gate. No package was executed for this proposal. Reproduction would check software and equations within their published domain, not validate transfer from modern mussels to ancient gastropods.

Keep physiological and demographic interfaces explicit. A Python reference implementation plus a profiled numerical kernel is a sensible starting point. Choose one acceleration route after profiling—such as a compiled cohort kernel or JIT compilation—rather than maintaining several languages from the outset.

Existing platforms should be reused selectively. Gen3sis addresses broad spatial eco-evolutionary processes; its existence does not make it the appropriate crisis-time, stage-structured engine. [23] FossilSim may supply useful observation-model components if its assumptions match the declared sampling problem. [22] Using an established tool is valuable when it reduces validated work, not when it adds a dependency without resolving a scientific uncertainty.

### 13.2 Parallelise replicate families

The basic job unit is a **five-world family**: Y11, Y01, Y10, Y00 and Ybase for one initial assemblage, trait draw, forcing scenario and replicate. Extra diagnostic worlds add explicit cost.

Use deterministic identifiers and seeds derived from the configuration, model version and replicate. Separate random streams by process, species, patch and event/time index so an extra birth in one arm does not arbitrarily shift every later draw. Verify each arm’s marginal distribution independently of the coupling.

Run families independently across CPU workers. Batch short families into moderate-duration tasks, with no oversubscription from nested numerical-library threads. Precompute shared forcing transformations and read-only trait inputs once where practical.

TPAC documents PBS submission and the -J array-job option for kunanyi. [25] Its public hardware descriptions and the repository capability inventory are useful orientation; current queue limits, allocation and usable concurrency must be checked when an authorised implementation reaches the cluster. The inventory records up to 48 nodes × 28 CPUs, not a guarantee that all are simultaneously available. [R3], [26]

The user’s stated Nectar resource—one A100 with 64 CPU and 128 GB RAM—can support an optional emulator or sensitivity surrogate. The principal scientific calculation should remain viable on CPU. Validate any surrogate near extinction boundaries and under withheld structural models before using it to guide expensive work.

### 13.3 Budget measured CPU time, not imagined speedups

Let F be the number of complete replicate families and t_f their measured CPU-seconds per family, summed across all five worlds and any within-family threads. Then

$$
C_{\mathrm{core\ hours}} = \frac{F t_f}{3600}.
$$

| Illustrative family cost | Families | Core-hours | Ideal runtime with 500 continuously effective cores |
| --- | ---: | ---: | ---: |
| 60 CPU-seconds | 100,000 | 1,667 | 3.3 hours |
| 600 CPU-seconds | 100,000 | 16,667 | 33.3 hours |

These are arithmetic scenarios, not benchmarks or promised runtimes. The family cost already includes all five worlds. Queue delays, setup, imperfect utilisation, analysis and recovery from failures add time. If a benchmark reports per-world time instead, sum the five worlds before applying the equation.

A useful planning envelope is:

| Stage | Provisional compute ceiling | Purpose |
| --- | ---: | --- |
| Analytical/reference and physiology pilot | 100 core-hours | Establish correctness and measure family cost. |
| First mechanism ensemble | 5,000 core-hours | Locate interpretable regimes and decide whether space changes the result. |
| Targeted spatial/structural/observation campaign | 20,000–50,000 core-hours, conditional on the preceding result | Test robustness and diagnostic information content. |

These are project-planning caps to revise after measurement, not allocations to request or jobs authorised by this document. A much cheaper decisive result is a success. A slow implementation must earn its additional cost scientifically.

The largest memory requirements will depend on cohort resolution, numbers of species/patches and retained trajectories. Measure peak memory on a complete family before selecting job size. Large-memory nodes may help with shared ensembles and analysis, but high memory is not a reason to retain every state at every timestep.

### 13.4 Outputs and reproducibility

Store compact species and family summaries for every completed run, plus detailed state trajectories for a fixed diagnostic subset. Avoid millions of small files; write independent shards and merge them through a documented step. Do not let concurrent workers write unsafely to the same state file.

Every result must carry configuration hash, source version, input checksums, parameter/forcing versions, units, seed identity, horizon, intervention definitions and completion status. Preserve failed or invalid runs with explicit reasons. Quietly dropping failures can bias the inferred compatibility region.

Checkpoint at restartable boundaries, and verify that restart does not change outcomes under the declared reproducibility standard. Archive a small reproducible figure-generating example as well as the full experiment manifest.

Coding agents are particularly useful for implementing alternative kernels, data adapters, provenance checks, parallel execution and reproducible analysis. Their outputs still require independent biological specification and adversarial numerical review. Agreement between two implementations derived from the same mistaken requirement is not independent scientific validation.

## 14. Verification that matters to the inference

The following checks target ways the proposed conclusion could be wrong.

| Risk | Required verification |
| --- | --- |
| Extinction produced by numerical compression | Compare small explicit-individual simulations with the cohort/hybrid method; match extinction probabilities and variance, not just mean biomass. |
| Unrealistic global demographic noise | Reproduce the large-population analytical limit and vary density, habitat area and total abundance separately. |
| A built-in famine result | Check no-event persistence, energy conservation and ordinary replacement before applying a crisis. |
| Incorrect rescue | Verify food is capped by the declared baseline availability, subsidy is booked, and unaffected exposures retain their rules. |
| Accidental removal of the larval pathway | Confirm rescued larvae can mature and affect future adult abundance. |
| Artificial synchronised death or immortal tails | Compare supported age/reserve distributions and bounded tail alternatives; show which tail assumptions drive survival. |
| Time discretisation creates starvation | Halve the relevant timestep and refine developmental/reserve bins near the decision boundary. |
| Incorrect geographical extinction | Expand the biological domain and inspect source populations/refuges; record local and global outcomes separately. |
| Genus mapping manufactures a null | Test known synthetic genus memberships and dependence structures with perfect observation. |
| Inference recognises its own simulator only | Hold out an entire model structure or forcing family, not merely random replicates. |
| Selectivity is a low-power artefact | Compare perfect species observation, genus aggregation and realistic fossil sampling in separate stages. |
| Model fit substitutes for external support | Evaluate withheld physiological responses and predeclared fossil predictions. |

Numerical acceptance tolerances should be chosen in relation to the scientific margins. For example, numerical error that can move S by five percentage points is unacceptable when the challenge defines equivalence at that scale. Set tolerances and Monte Carlo precision targets before evaluating a preferred result.

Once the relevant risks and gates are resolved, stop expanding the verification suite. The purpose is trustworthy scientific discrimination, not indefinite software construction.

## 15. Falsifiers, stopping rules and fallback outcomes

| Finding | Decision and scientific interpretation |
| --- | --- |
| A prior study already measures essentially the same controlled contrast | Narrow the claim only if a material unsupported boundary remains; otherwise abandon this candidate. |
| The challenge region appears only with implausibly small populations, extreme reserves or unsupported Allee thresholds | Reject that explanation for the intended domain. Report the required assumptions explicitly. |
| Weak S occurs only when almost all taxa survive or die | The main question has not been answered. Do not present the degeneracy as concealment. |
| Severe loss and weak S occur, but R_L is negligible | The principal single-rescue challenge fails. Inspect conditional and joint rescues before inferring that larval stress was unimportant. |
| A large R_L and small S require fine tuning of trait covariance | Treat the result as a constructed possibility; it is insufficient support for a major historical claim. |
| The result is analytically determined across the supported range | Publish or retain the simpler theoretical result and cancel unnecessary HPC expansion. |
| The initial genus cohort cannot be recovered or its coding materially changes | Update the motivation and retain a theoretical paper; do not fit the old aggregate table as if it were a complete dataset. |
| Species-to-genus or regional-to-global mapping dominates uncertainty | Report bounds and drop precise historical attribution. |
| The fossil data cannot distinguish large from negligible larval-rescue effects | State that the diagnostic is unresolved at the available information level; retain the factorial interpretation. |
| Different supported physiological models give opposing results | Present structural uncertainty; seek a discriminating existing observation before adding more free parameters. |

A useful null result would delimit where the demographic-buffer explanation fails. A useful positive result would demonstrate robust biological concealment and specify the conditions that generate it. An underpowered fossil comparison remains underpowered regardless of the number of simulation runs.

## 16. A staged work programme and handoff for Claude/Codex

The timings below are planning estimates for a researcher supervising capable coding agents, not promises of autonomous completion.

| Work package | Main task | Reviewable output | Gate |
| --- | --- | --- | --- |
| WP0: question and evidence, roughly week 1 | Freeze estimands; final nearest-prior check; attempt cohort recovery; audit two or three modern calibration sources. | Short evidence ledger, inclusion rules, initial joint parameter manifest and unresolved-data list. | The question remains distinct; core physiological quantities can be bounded. |
| WP1: analytical and numerical pilot, roughly weeks 1–2 | Derive limits; reproduce one existing physiological case; implement five matched worlds in a reference model. | Reproducible pilot with analytical checks and measured cost. | Correct limits, no-event viability, valid interventions and interpretable population scaling. |
| WP2: mechanism experiment, roughly weeks 3–4 | Explore the supported parameter space; compare physiological models and trait covariance; identify why S and R_L agree or diverge. | First response surfaces, failure cases and an explicit decision on spatial extension. | A robust unresolved scientific boundary justifies additional simulation. |
| WP3: spatial and observation tests, roughly weeks 5–8 | Add finite metapopulations where needed; species-to-genus mapping; cohort-sized observation experiments. | Structural robustness results and a historical information-content assessment. | Biological conclusions survive numerical checks; historical claims match data support. |
| WP4: synthesis, roughly weeks 9–12 if prior gates pass | Evaluate frozen predictions, write the paper and archive reproducible results. | Manuscript, documented simulator, versioned data/forcing adapters and experiment manifests. | Claims match the actual result, including negative or indeterminate outcomes. |

Assign separate responsibilities to improve review:

- **Scientific specification agent:** maintains units, stages, estimands, permissible interventions and explicit assumptions.
- **Implementation agent:** builds the reference and optimised kernels from that specification, without changing biology to improve performance.
- **Data agent:** records source-level support, taxonomy, uncertainty and licences; never invents missing life-history values.
- **Adversarial reviewer:** looks specifically for coarse-population extinction, correlated-trait tuning, observation-induced nulls and novelty already occupied by prior work.

Barry’s role is to resolve biological assumptions and judge which empirical transfers are defensible. Coding agents can make a demanding implementation practical; they cannot infer trustworthy ancient physiology from absent evidence.

### First executable task for the repository agents

Before building a broad framework, produce one compact pilot report answering:

1. Can the no-recruitment reference reproduce the large-N adult-survival limit?
2. Can the five-world intervention be implemented without altering unrelated exposures or preventing rescued offspring from maturing?
3. Under at least two coherent, independently sourced strategy bundles, can any nondegenerate joint region be found?
4. If one is found, does it persist under abundance scaling and more than one supported trait-covariance assumption?
5. Which quantity currently limits inference: physiological support, spatial survival, taxonomic mapping or fossil precision?
6. Is the next valuable step more simulation, a focused data audit, or simplification?

The pilot should include unsuccessful parameter regions and the reason for each failure. Do not treat “found a visually attractive phase diagram” as a gate.

## 17. The intended paper and reusable products

**Working paper title:** *When extinction selectivity fails to reveal a larval food crisis.*

A six-figure structure would keep the scientific argument focused:

1. The causal experiment and the distinction between latent species loss and observed genus survival.
2. Analytical demographic limits and verification against the reference simulator.
3. The joint M–S–R_L response surface, showing where the challenge is met and where it fails.
4. The mechanism behind boundary shifts: reserve distributions, reproduction timing, provisioning and supported strategy covariance.
5. The effect of spatial populations and species-to-genus aggregation, separated from fossil sampling.
6. The K–Pg compatibility/information-content result, or an explicit demonstration that current fossil evidence cannot resolve the diagnostic.

The reusable contribution would be a tested stage-structured extinction simulator with bounded physiological modules, paired interventions and a clean observation interface. It could support other questions about extinctions acting on different life stages, but the initial code should be organised around the present test.

**Why this is a good first proposal for the available opportunity:** it has a precise biological question, a recognisable deep-time motivation, unusually relevant modern physiological material, a substantial falsification burden, and an ensemble calculation that can exploit many CPU workers. The central uncertainty is scientific and explicit: whether a robust, biologically defensible region of causal concealment exists. The proposed work is designed to find out.

---

## Appendix A. Reproducible arithmetic for the historical count table

The following standard-library Python reproduces the descriptive calculation in Section 4. It uses Wilson score intervals for each proportion and the Newcombe combination for their difference. [28] Inputs are extinct/total genera from the original table. [1]

This is an independent-binomial approximation for two proportions. It is not a likelihood for the full fossil process and does not account for clade dependence, misclassification or revised taxonomy.

~~~python
from math import sqrt

def wilson_interval(successes, trials, z=1.959963984540054):
    p = successes / trials
    denominator = 1.0 + z * z / trials
    centre = (p + z * z / (2.0 * trials)) / denominator
    half_width = (
        z
        * sqrt(p * (1.0 - p) / trials
               + z * z / (4.0 * trials * trials))
        / denominator
    )
    return centre - half_width, centre + half_width

extinct_pt, total_pt = 17, 28
extinct_npt, total_npt = 14, 23

p_pt = extinct_pt / total_pt
p_npt = extinct_npt / total_npt
lower_pt, upper_pt = wilson_interval(extinct_pt, total_pt)
lower_npt, upper_npt = wilson_interval(extinct_npt, total_npt)

difference = p_pt - p_npt
lower_difference = difference - sqrt(
    (p_pt - lower_pt) ** 2 + (upper_npt - p_npt) ** 2
)
upper_difference = difference + sqrt(
    (upper_pt - p_pt) ** 2 + (p_npt - lower_npt) ** 2
)

print(f"PT extinction fraction: {p_pt:.6f}")
print(f"NPT extinction fraction: {p_npt:.6f}")
print(f"Risk difference: {difference:.6f}")
print(f"95% interval: [{lower_difference:.6f}, "
      f"{upper_difference:.6f}]")
~~~

Expected output:

~~~text
PT extinction fraction: 0.607143
NPT extinction fraction: 0.608696
Risk difference: -0.001553
95% interval: [-0.251184, 0.253494]
~~~

The interval’s width is the relevant warning about information content. A more complete empirical analysis should use the recovered taxonomic data and an appropriate hierarchical observation model.

## Appendix B. Minimal data contracts for an implementation

These are proposed records, not existing files or a claim that all fields can be populated immediately.

| Record | Minimum fields |
| --- | --- |
| Biological strategy | species identifier; developmental mode and evidence; joint trait-draw identifier; physiology variant; stage definitions; adult and juvenile diet; provisioning; maturation and ageing rules; source/transfer uncertainty. |
| Population initial state | species; patch; habitat area; density/count conversion; stage/age/reserve distribution; viable count; reproductive configuration; initialisation and no-event checks. |
| Environmental scenario | scenario identifier; upstream forcing provenance; food pools and units; temperature; time grid; spatial grid; baseline trajectory; deficit/recovery window; transformation version. |
| Intervention | target stage; attainable-ration policy; reference-food identity; start/end rule; food-quality limits; subsidy accounting; downstream resource-feedback setting. |
| Fossil taxon crosswalk | original and accepted names; genus membership; developmental evidence/confidence; cohort inclusion; pre/post-boundary occurrence support; survival domain; revision sources. |
| Replicate family | all biological/scenario identifiers; five world identifiers; model version; seeds/substreams; horizon; numerical settings; runtime; memory; completion/failure reason. |
| Biological outcome | extinction by stage-inclusive zero count; local versus global status; time of loss; minimum breeders; recruitment recovery; M, Mbase, Mexcess, S, Sexcess and all rescue contrasts. |
| Observed outcome | latent species/genus mapping; sampling model/version; occurrence windows; observed developmental assignment; apparent survival; cohort sizes; uncertainty. |

Before exporting a result, a reader should be able to establish which species and worlds entered its denominator, what food was restored, how extinction was determined, and which assumptions make it interpretable.

## References and source notes

Numbers in the text refer to the sources below. Stable DOI or official-resource links are supplied so the document remains useful independently of this conversation. Access limitations are recorded in Section 9; a citation does not imply that raw data or every supplement were retrieved.

**1. Valentine, J. W. & Jablonski, D. (1986).** Mass extinctions: Sensitivity of marine larval types. *Proceedings of the National Academy of Sciences* 83, 6912–6914. [DOI](https://doi.org/10.1073/pnas.83.18.6912).

**2. Smith, A. B. & Jeffery, C. H. (1998).** Selectivity of extinction among sea urchins at the end of the Cretaceous period. *Nature* 392, 69–71. [DOI](https://doi.org/10.1038/32155).

**3. Nützel, A. (2014).** Larval ecology and morphology in fossil gastropods. *Palaeontology* 57, 479–503. [DOI](https://doi.org/10.1111/pala.12104). Used for interpretation and evidence limitations, not as an independent recount of the original extinction table.

**4. Jablonski, D. & Hunt, G. (2006).** Larval ecology, geographic range, and species survivorship in Cretaceous mollusks: organismic versus species-level explanations. *The American Naturalist* 168, 556–564. [DOI](https://doi.org/10.1086/507994).

**5. Robertson, D. S., Lewis, W. M., Sheehan, P. M. & Toon, O. B. (2013).** K–Pg extinction patterns in marine and freshwater environments: The impact winter model. *Journal of Geophysical Research: Biogeosciences* 118, 1006–1014. [DOI](https://doi.org/10.1002/jgrg.20086).

**6. Ying, R., Monteiro, F. M., Witts, J. D. & Schmidt, D. N. (2026).** Darkness and body size shaped end-Cretaceous marine extinction patterns. *Nature*. [DOI](https://doi.org/10.1038/s41586-026-10541-4). [Accessible primary manuscript](https://ueaeprints.uea.ac.uk/id/eprint/103214/1/s41586-026-10541-4.pdf).

**7. Gibbs, S. J. et al. (2020).** Algal plankton turn to hunting to survive and recover from end-Cretaceous impact darkness. *Science Advances* 6, eabc9123. [DOI](https://doi.org/10.1126/sciadv.abc9123).

**8. Sarà, G. (2026).** Disturbance duration governs mortality risk while cumulative energetic deficit shapes reproduction in Mediterranean mussels. *Marine Environmental Research* 222, 108411. [DOI](https://doi.org/10.1016/j.marenvres.2026.108411). Available online 15 September 2026. [Data/code](https://doi.org/10.17632/r2h822zzxp.1).

**9. McQuaid, C. D. & Chambers, R. J. (2025a).** Reproduction, recruitment, growth and mortality of co-occurring species of the intertidal limpet Siphonaria with contrasting reproductive modes. *African Journal of Marine Science* 47, 51–61. [DOI](https://doi.org/10.2989/1814232X.2025.2454626).

**10. McQuaid, C. D. & Chambers, R. J. (2025b).** Congruence in annual energy input into reproduction in siphonariid limpets with planktonic and direct development. *Journal of Molluscan Studies* 91, eyaf036. [DOI](https://doi.org/10.1093/mollus/eyaf036).

**11. Ullah, M. A. & Marshall, D. J. (2025).** Starvation and dormancy in marine gastropods: taxonomic and ecological patterns, and energetic implications. *Journal of Molluscan Studies* 91, eyaf016. [DOI](https://doi.org/10.1093/mollus/eyaf016).

**12. Pechenik, J. A., Hammer, K. & Weise, C. (1996).** The effect of starvation on acquisition of competence and post-metamorphic performance in the marine prosobranch gastropod Crepidula fornicata (L.). *Journal of Experimental Marine Biology and Ecology* 199, 137–152. [DOI](https://doi.org/10.1016/0022-0981(96)00010-X).

**13. Marques, G. M. et al. (2018).** The AmP project: Comparing species on the basis of dynamic energy budget parameters. *PLOS Computational Biology* 14, e1006100. [DOI](https://doi.org/10.1371/journal.pcbi.1006100).

**14. Add-my-Pet project.** Official portal, species entries and data organisation. [Portal](https://debtheory.fr/add_my_pet/). Inspected 20 October 2026. Entry versions must be pinned during implementation.

**15. Agüera, A., Ahn, I.-Y., Guillaumot, C. & Danis, B. (2017).** A Dynamic Energy Budget (DEB) model to describe Laternula elliptica (King, 1832) seasonal feeding and metabolism. *PLOS ONE* 12, e0183848. [DOI](https://doi.org/10.1371/journal.pone.0183848).

**16. Bradshaw, C. J. A., Johnson, C. N., Llewelyn, J., Weisbecker, V., Strona, G. & Saltré, F. (2021).** Relative demographic susceptibility does not explain the extinction chronology of Sahul’s megafauna. *eLife* 10, e63870. [DOI](https://doi.org/10.7554/eLife.63870). [Code](https://github.com/cjabradshaw/MegafaunaSusceptibility).

**17. Cunningham, J. A. & Jeffery Abt, C. H. (2009).** Coordinated shifts to non-planktotrophic development in spatangoid echinoids during the Late Cretaceous. *Biology Letters* 5, 647–650. [DOI](https://doi.org/10.1098/rsbl.2009.0302). Cited for developmental history; a purported subgroup extinction contrast requires further primary-text verification.

**18. Lockwood, R. (2003).** Abundance not linked to survival across the end-Cretaceous mass extinction: Patterns in North American bivalves. *Proceedings of the National Academy of Sciences* 100, 2478–2482. [DOI](https://doi.org/10.1073/pnas.0535132100). Relative fossil abundance is useful empirical information, not a direct count of global living individuals.

**19. Leventhal, S. & Samuels-Fair, M. (2025).** Larval brooding correlated with high early origination rates in cheilostome Bryozoa. *Paleobiology* 51, 261–267. [DOI](https://doi.org/10.1017/pab.2024.63). [Data](https://doi.org/10.5061/dryad.1vhhmgr44).

**20. Holland, S. M. & Patzkowsky, M. E. (2015).** The stratigraphy of mass extinction. *Palaeontology* 58, 903–924. [DOI](https://doi.org/10.1111/pala.12188). [Archived study material](https://doi.org/10.5061/dryad.1mg27).

**21. Darroch, S. A. F., Casey, M. M., Antell, G. S., Sweeney, A. & Saupe, E. E. (2020).** High Preservation Potential of Paleogeographic Range Size Distributions in Deep Time. *The American Naturalist* 196, 454–471. [DOI](https://doi.org/10.1086/710176).

**22. Barido-Sottani, J., Pett, W., O’Reilly, J. E. & Warnock, R. C. M. (2019).** FossilSim: An R package for simulating fossil occurrence data under mechanistic models of preservation and recovery. *Methods in Ecology and Evolution* 10, 835–840. [DOI](https://doi.org/10.1111/2041-210X.13170).

**23. Hagen, O. et al. (2021).** gen3sis: A general engine for eco-evolutionary simulations of the processes that shape Earth’s biodiversity. *PLOS Biology* 19, e3001340. [DOI](https://doi.org/10.1371/journal.pbio.3001340).

**24. Senel, C. B. et al. (2023).** Chicxulub impact winter sustained by fine silicate dust. *Nature Geoscience* 16, 1033–1040. [DOI](https://doi.org/10.1038/s41561-023-01290-4). [Linked archive](https://doi.org/10.17605/OSF.IO/2CDQG).

**25. TPAC.** HPC FAQ. [Official documentation](https://www.tpac.org.au/hpc-faq/). Inspected 20 October 2026; verify actual submission policy when implementing.

**26. TPAC.** HPC facilities and data-storage guidance. [Facilities](https://www.tpac.org.au/tpac-hpc-facilities-2/); [storage](https://www.tpac.org.au/faq/data-storage/). Public descriptions are orientation, not a guarantee of available capacity.

**27. Paleobiology Database.** Data Service documentation. [Official service](https://paleobiodb.org/data1.2/). For the published API description, see Peters, S. E. & McClennen, M. (2016), *The Paleobiology Database application programming interface*, [DOI](https://doi.org/10.1017/pab.2015.39). Freeze exports and taxonomy during an empirical analysis.

**28. Newcombe, R. G. (1998).** Interval estimation for the difference between independent proportions: comparison of eleven methods. *Statistics in Medicine* 17, 873–890. [Primary bibliographic record](https://pubmed.ncbi.nlm.nih.gov/9595617/).

### Repository sources

**R1.** BWBrook/eprp, [main question register at the inspected commit](https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/ideas/register.md).

**R2.** BWBrook/eprp, [blue-sky register at the inspected commit](https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/ideas/register-blue-sky.md).

**R3.** BWBrook/eprp, [capability inventory at the inspected commit](https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/resources/capability-inventory.md).

[1]: https://doi.org/10.1073/pnas.83.18.6912
[2]: https://doi.org/10.1038/32155
[3]: https://doi.org/10.1111/pala.12104
[4]: https://doi.org/10.1086/507994
[5]: https://doi.org/10.1002/jgrg.20086
[6]: https://doi.org/10.1038/s41586-026-10541-4
[7]: https://doi.org/10.1126/sciadv.abc9123
[8]: https://doi.org/10.1016/j.marenvres.2026.108411
[9]: https://doi.org/10.2989/1814232X.2025.2454626
[10]: https://doi.org/10.1093/mollus/eyaf036
[11]: https://doi.org/10.1093/mollus/eyaf016
[12]: https://doi.org/10.1016/0022-0981(96)00010-X
[13]: https://doi.org/10.1371/journal.pcbi.1006100
[14]: https://debtheory.fr/add_my_pet/
[15]: https://doi.org/10.1371/journal.pone.0183848
[16]: https://doi.org/10.7554/eLife.63870
[17]: https://doi.org/10.1098/rsbl.2009.0302
[18]: https://doi.org/10.1073/pnas.0535132100
[19]: https://doi.org/10.1017/pab.2024.63
[20]: https://doi.org/10.1111/pala.12188
[21]: https://doi.org/10.1086/710176
[22]: https://doi.org/10.1111/2041-210X.13170
[23]: https://doi.org/10.1371/journal.pbio.3001340
[24]: https://doi.org/10.1038/s41561-023-01290-4
[25]: https://www.tpac.org.au/hpc-faq/
[26]: https://www.tpac.org.au/tpac-hpc-facilities-2/
[27]: https://paleobiodb.org/data1.2/
[28]: https://pubmed.ncbi.nlm.nih.gov/9595617/
[R1]: https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/ideas/register.md
[R2]: https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/ideas/register-blue-sky.md
[R3]: https://github.com/BWBrook/eprp/blob/ce5043b85d55e05ec46ccdadbce0cd8ea3017e8f/resources/capability-inventory.md
