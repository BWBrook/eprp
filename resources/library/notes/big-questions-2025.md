# The community's Big Questions in paleontology (Smith, Dowding et al. 2025)

Smith, J. A., E. M. Dowding, and 98 co-authors. 2025. Identifying the Big
Questions in paleontology: a community-driven project. *Paleobiology*
51(3):408–431. <https://doi.org/10.1017/pab.2025.10042> (OpenAlex
W4414545731). Licence CC BY 4.0. Supplement CC BY 4.0:
<https://doi.org/10.5281/zenodo.14278551>.

The library found this paper while building its frontier tier, the works
since 2020 that cite at least five EPRP core works. It cites 70 core works,
more than any other frontier work. It is the field's own question list,
assembled from nearly 200 contributors, so it is both a benchmark for the
novelty and positioning of EPRP's registers and raw material for ideation.

## How the list was made

- Three open solicitations to the global community produced 528 questions.
- Twelve working groups, of 16–17 participants each, condensed the questions
  assigned to their theme into 117 preliminary questions.
- Every participant commented on all of them. The groups then produced 89
  final questions in 11 themes. The twelfth group, "Ecosystems,
  Environments, and their Records", was dissolved into the others because
  of overlap.
- The final lists are unranked and unordered within each theme.

Groups judged questions against seven criteria from Sutherland et al. (2009).
A Big Question:

1. addresses an important gap in knowledge;
2. is more than just a general topic area (e.g., "climate change");
3. is answerable through a realistic research design;
4. has a spatial and temporal scale that can be addressed by a research
   team;
5. has a factual answer that does not depend on value judgments;
6. tends not to be situationally dependent (i.e., answerable with "it all
   depends");
7. is not likely to be answerable with "yes" or "no".

## Files

| File | Rows | Contents |
| --- | --- | --- |
| [final-questions.tsv](big-questions-2025/final-questions.tsv) | 89 | `id`, `theme`, `question`, `eprp_nearest` (this note's crosswalk) |
| [preliminary-questions.tsv](big-questions-2025/preliminary-questions.tsv) | 117 | the working groups' first refinement, including the dissolved group's 16 (EER1–16); its IDs do not match the final IDs |
| [raw-questions.tsv](big-questions-2025/raw-questions.tsv) | 528 | every contributed question, unedited, with the one or two working groups it was assigned to |

The final questions come from the paper's Tables 3–13, in the accepted
manuscript held at `deep-server:/data/paleodata/library/pdf/W4414545731.pdf`
(text in `text/`; open repository copy). The version of record prints the
tables as images, so its wording could not be compared and may differ
slightly. The two supplement sheets were converted unchanged from
`SuppMat1_Smith.xlsx` (sha256 `b15149bbc94122f3…`), which is archived at
`deep-server:/data/paleodata/library/supp/`. Its spelling, such as
"Biodiveristy Drivers", is kept as published.

The raw questions are often sharper than the final ones, which were merged
into broad programme statements. For example: "How explosive was the
Cambrian diversification event?", "Is the origin of Xenarthra related to
tropical climates?" and, from the dissolved group, "Do ecosystems in
greenhouse worlds function differently than those in icehouse worlds?"

## Crosswalk to the EPRP registers

`eprp_nearest` lists the register entries (Q-001–Q-050, B-001–B-018)
closest in subject to each Big Question. This is topical proximity judged
by the library session, not equivalence and not a prior-work check.

- **61 of 89 have a register neighbour.** Every question in SEP, BST, BD
  and ED does; none in Fundamental Issues does, nor any in Looking Inward
  and Outward except LIO1, which is about publication bias.
- **The most-linked entries** are Q-019 (6 Big Questions), Q-004, Q-006,
  Q-028 (5 each), and Q-002, Q-009, Q-015, Q-030 (4 each).
- **Register entries no Big Question touches:** Q-032 (insect crises),
  Q-041 (extinction periodicity), Q-042 (species-level death tolls), B-008
  (refugia), B-012 (dispersal value and habitat geometry) and B-015
  (stability of macroecological distributions).
- **Big Questions with no register neighbour that fit EPRP's quantitative
  and theoretical remit:**
  - AFR2: data-entry bias in databases;
  - AFR7: geochemical diagnosis of preservation bias;
  - AIO1: drivers of the origins of life and of major clades;
  - AIO4: integrating tools to time the origin of adaptations;
  - PTS6: developmental data in phylogenetic inference;
  - PTS8: better phylogenetic methods;
  - PTS10: environmental and geological processes read from phylogenies;
  - CPP1: fossils as climate proxies.
- **Weakly linked but well suited to simulation:** SEP4, scale
  "transmutations" in ecological and evolutionary models, and ED2, a unified
  definition of mass extinction. Q-011's size distribution of extinction
  events bears directly on ED2.

## The 89 questions

Each question is followed, in brackets, by its nearest EPRP register
entries where there are any.

### The Adequacy of the Fossil Record

- **AFR1** How can we best quantify preservation and collecting biases? [Q-017, Q-045, B-007]
- **AFR2** How do we develop methods to identify, minimize, and correct data entry biases?
- **AFR3** How do we account for data loss in historical collections and publications? [Q-045]
- **AFR4** How do we standardize taxonomic, stratigraphic, and ecological reporting during data acquisition?
- **AFR5** How can we improve the collection of biomolecules from fossils, and what are the limits for biomolecule analysis?
- **AFR6** How can we correlate marine and terrestrial strata more precisely? [Q-035]
- **AFR7** In what ways can we use isotopic systems and geochemical methods to help identify preservation biases?
- **AFR8** Which opportunities and threats for fossil discovery will arise as a result of the changing climate?

### Scaling Ecological and Evolutionary Processes and Patterns

- **SEP1** Which evolutionary and ecological processes (local to global) can be best evaluated using the fossil record? [Q-006]
- **SEP2** In the fossil record, how do we interpret and measure ecological and evolutionary trends at different taxonomic, spatial, and temporal scales to infer directionality or causality? [Q-019, Q-030]
- **SEP3** How do we address the spatial, temporal, and taxonomic incompleteness of the fossil record to be able to interpret ecological and evolutionary processes and patterns at different scales? [Q-017, Q-040, Q-006]
- **SEP4** How can we identify and counteract spatial and temporal transmutations (a change in the relationship between variables caused by crossing data scales, leading to interpretive error) within ecological and evolutionary models? [Q-025]
- **SEP5** Given incompleteness of the fossil record and spatiotemporal averaging, how do we estimate rates of change in taxonomic composition, community structure, ecosystem function, niches, traits, life modes, turnover etc., using the fossil record? [Q-015, Q-024, B-013]
- **SEP6** What drives metacommunity composition and community assembly over time and space? [B-001, Q-033]
- **SEP7** How do external environmental drivers (e.g., plate tectonics, global temperature, sea level) influence the structure of biological systems at different spatiotemporal scales? [Q-019, Q-029, B-005]
- **SEP8** What are the signatures of emergent processes at macroevolutionary timescales (e.g., species sorting, species selection, clade competition)? [B-014, B-016, Q-039]
- **SEP9** How do biological systems impact the abiotic systems and the feedback between them at different scales? [Q-021, B-004]

### Phylogenetics, Taxonomy, and Systematics

- **PTS1** What causes the mechanism of speciation or character evolution to change over time? [Q-050]
- **PTS2** Which abiotic and biotic factors determine species longevity (stratigraphic duration)? [Q-012, Q-038, B-017]
- **PTS3** Which aspects of the macroevolutionary process are identifiable in the molecular or fossil records using phylogenetic methods, and under which circumstances? [Q-006]
- **PTS4** How can traditional taxonomy be used to inform the process of selecting the best operational taxonomic unit for a particular phylogenetic analysis (e.g. diversification, disparification, phylogeny)?
- **PTS5** How can taxonomic practice help to harmonize boundaries between taxa in fossil and extant groups? [Q-004]
- **PTS6** How can we collect and integrate developmental data observable in the fossil record (e.g., timing of organogenesis, gene expression) into phylogenetic approaches?
- **PTS7** How much phylogenetic information can be gained from combining different types of data (e.g. morphology, stratigraphy, biogeography, environmental)? [Q-006]
- **PTS8** How can we improve the performance of phylogenetic inference through the development of better methods?
- **PTS9** How do we improve the representation of uncertainty and bias from the fossil and geological records in phylogenetic inference? [Q-006, Q-022]
- **PTS10** What can we learn about environmental and geological processes using phylogenetic methods?

### Biodiversity Dynamics in Space and Time

- **BST1** What is the global diversity trend through time and how is diversity constrained, if at all? [Q-040, Q-010, Q-044]
- **BST2** How have large-scale spatial diversity patterns (e.g., latitudinal diversity gradient, distribution of diversity hotspots) changed across deep time? [Q-027, B-005]
- **BST3** What are important drivers of global trends in taxonomic diversity or ecological disparity, and has their relative importance changed through time? [Q-019, B-013]
- **BST4** What is the relationship between deep-time biodiversity (e.g., taxonomic richness, ecomorphological disparity) and ecosystem function (the combination of all biological interactions and physical processes occurring in an ecosystem)? [Q-046, Q-009]
- **BST5** What are the drivers of origination in space and time? [Q-023, B-018, B-009]
- **BST6** What is a common basis (e.g., taxonomic units, morphological traits) that can be used consistently to bridge modern and fossil biodiversity research? [Q-004, Q-028]
- **BST7** In what ways is the “Anthropocene” creating a unique signature in biodiversity over geologic time (both direct and indirect effects; e.g., changes in climate and in connectivity)? [Q-013]

### Biodiversity Drivers

- **BD1** How does the ecological niche of species influence their response to perturbation? [Q-001, Q-002, Q-015]
- **BD2** How does the prevailing climate state experienced by species and communities influence their response to perturbation? [Q-030, Q-027]
- **BD3** How do methodological choices influence the outcome of studies investigating the relative importance of abiotic and biotic drivers in driving biodiversity dynamics? [Q-019]
- **BD4** How do the rate and magnitude of environmental change impact diversification? [Q-050, Q-003, Q-002]
- **BD5** How did biologic evolution affect the evolution of other Earth systems (e.g., litho-, atmo-, and hydrosphere)? [Q-021, B-004, B-006]
- **BD6** How has the relative importance of biotic and abiotic drivers of biodiversity and extinction changed through time? [Q-019, Q-030]
- **BD7** What is the relative role of biotic and abiotic drivers in increasing ecosystem complexity? [Q-010, B-010, B-003]
- **BD8** To what extent do population-based characteristics determine resilience to extinction through geological time? [Q-020, Q-016]
- **BD9** How do changes in community structure observed at the population level relate to evolutionary changes in ecosystems through time? [Q-009, Q-007]

### Adaptations, Innovations, Origins

- **AIO1** What were the geological and biological drivers of the origin of life, and major groups of organisms such as eukaryotes, plants, animals, and fungi?
- **AIO2** How were major life transitions (e.g., origins of biomineralization, early Paleozoic diversifications, terrestrialization, evolution of planktonic lifestyle) in Earth’s history associated with major changes in the geological and/or biological environment? [B-009, B-006, B-011]
- **AIO3** How is our understanding of the origination of novelties and innovations affected by fossil preservation, the global quality of the fossil record, and stratigraphic completeness? [B-013]
- **AIO4** What are best practices for integrating different analytical tools and techniques to improve our interpretation of the ecological context and timing of the origin of adaptations and features?
- **AIO5** How have changes in ontogeny (i.e., life history traits such as larval/juvenile ecology, growth, and developmental patterns including heterochronies) influenced macroevolution or themselves been influenced by environmental change? [B-002, Q-028]
- **AIO6** Which common patterns of morphological or behavioral responses to environmental change on evolutionary timescales can be identified and how do these compare with modern systems on ecological timescales? [Q-031, Q-036]
- **AIO7** Which observable differences in the origin and fixation of features at different scales of biological hierarchy can be identified and what generated these patterns? [B-016]

### Extinction Dynamics

- **ED1** Which data types can be used to most effectively compare past extinctions to the current biodiversity crisis? [Q-013, Q-004, Q-034]
- **ED2** With our changing understanding of extinctions, how should the definition of “mass extinction” be updated to reflect a unified concept? [Q-011, Q-013, Q-018]
- **ED3** Which, if any, biotic traits associated with survival through a mass extinction (e.g. body size, trophic mode, species associations) are universal across taxa and/or time? [Q-028, Q-038, Q-002]
- **ED4** Which, if any, ecological impacts of extinction are generalizable across time? [Q-037, Q-022, Q-009]
- **ED5** To what extent are ecological functions maintained following the extinction of species? [Q-009, Q-021, Q-043]
- **ED6** To what extent are the phases of events (e.g., collapse, recovery) during extinctions consistent across different biotic crises? [Q-005, Q-014, Q-035]
- **ED7** Which, if any, patterns in the process and timing of recovery following extinction events are universal across clades? [B-001, Q-008, Q-026, Q-007]
- **ED8** At what threshold can climate or other abiotic change cause an extinction? [Q-003, Q-002, Q-001]
- **ED9** What is the role of cascading biological effects in extinction dynamics? [Q-037, Q-048, Q-025]

### Climate Change Past and Present

- **CPP1** How can fossils best be used to reconstruct climate change over different time scales?
- **CPP2** Which climate factors are the proximate drivers of extinction? [Q-001, Q-049]
- **CPP3** How can we best use the fossil record to predict climate change impacts on the modern biota? [Q-028, Q-015, Q-047]
- **CPP4** What is the "ecosystem sensitivity" of ecosystem structure in response to climate change? [Q-030]
- **CPP5** How have the spatial distributions of organisms shifted in response to climate change? [Q-049, Q-027]
- **CPP6** How have organisms’ tolerances changed in response to climate change? [Q-015]
- **CPP7** Which cascading effects of climate change can be identified from the fossil record? [Q-048, Q-037]
- **CPP8** What adaptation and management options for conservation biology can be derived from past biosphere responses to climate change?
- **CPP9** How has climate change affected the evolution of life? [Q-050, Q-019, B-018]

### Conservation Paleobiology

- **CPB1** What translational science strategies could be adopted to ensure that conservation paleobiology research remains relevant and aligned with the priorities of environmental resource managers and conservation practitioners?
- **CPB2** How do we integrate multiple types of paleontological data (e.g., molecular, environmental, ecological) with planning and decision support tools for guiding ecosystem management?
- **CPB3** How can our understanding of past episodes of environmental change be used to develop scenarios of biological responses to modern and future environmental stressors? [Q-028, Q-047]
- **CPB4** How can we use paleontological data to define meaningful ecological baselines that are relevant to conservation across spatial and temporal scales? [Q-004, Q-034]
- **CPB5** How can the fossil record inform our ability to diagnose and mitigate the effects of multiple interacting human and non-human drivers of environmental change on biodiversity and ecosystem functioning? [Q-048]
- **CPB6** How can we compare rates of biodiversity change (e.g., extinction, adaptation, geographic range shifts) across ecological, historical, and paleontological timescales? [Q-004, Q-025, Q-034]
- **CPB7** How can recent sedimentary records expand the temporal scope over which ecological resilience can be evaluated? [Q-024]
- **CPB8** In what ways can paleoenvironmental reconstructions improve the accuracy and scope of ecosystem services risk assessments?

### Fundamental Issues

- **FI1** How can we efficiently collect, store, and combine different paleontological data types in an openly accessible and inclusive way?
- **FI2** What are best practices for training paleontologists to have a broad set of skills (e.g., data analyses, research skills, soft skills) that is transferable to an increasingly wider range of job requirements inside and outside of academia?
- **FI3** How can we best motivate taxonomic and systematic work and facilitate cross-talk and collaboration with other paleontological disciplines?
- **FI4** How can paleontologists communicate findings and foster critical thinking skills so that the public can understand the utility of paleontological information and differentiate valid scientific ideas from other ideas?
- **FI5** What are the best practices for the protection and valorization of geosites and unique fossil heritage?

### Looking Inward and Outward

- **LIO1** How is our understanding of past ecological and evolutionary processes shaped by biases in publication by location, authorship, language use, and funding availability? [Q-045]
- **LIO2** Which processes drive turnover in diversity trends (e.g., gender identities, different geographic regions) of academic paleontologists over time, and how could increased diversity lead to increasingly diverse products and outcomes?
- **LIO3** Which socioeconomic and identity factors—and their intersections—underlie variability in publication rate, professional advancement, and grant awards among the global paleontology community, both historically and in the present day?
- **LIO4** To what extent are paleontological specimen collecting and repository practices built on a legacy of colonial economic structures and how can we avoid recapitulating these interactions today across individual and institutional collaborations?
- **LIO5** How should qualities of fossil origin (e.g., country, sovereignty, collection process, local collaborative involvement, political conflict) be considered when designing research and navigating potential trade-offs in ethics and scientific value?
- **LIO6** Which settings (e.g., economic, cultural, physical) govern the biogeography of where paleontological field work occurs and who (e.g., gender/ethnic identity) carries out—and benefits from—that work?
- **LIO7** Which institutional and mentorship attributes, such as accountability mechanisms, facilitate equitable collaboration among paleontologists, avoid bias, and promote the retention of students from backgrounds and identities currently underrepresented in paleontology?
- **LIO8** How do we integrate and sustain a commitment to diversity, equity, and inclusion initiatives into the foundations of hiring, promotion, and funding schemes in paleontology?
