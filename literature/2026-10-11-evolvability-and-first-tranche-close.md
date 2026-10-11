# Q-050: evolving capacity to evolve; first tranche closes at 50

Owner: Codex | 11 October 2026 | Supports [Q-050](../ideas/register.md#q-050-how-does-the-capacity-to-evolve-change-during-environmental-upheaval)

Barry's instruction in Codex chat, 11 October 2026, quoted exactly:

> Back to you. Let's get one more good question, to take the current list to 50, and then we'll pause and review the whole first tranche.

This note adds one question and closes expansion for that review. It does not
promote a primary investigation or complete a review of all 50 questions.

**Later phase-2 update (11 October):** the agents now lead categorisation and
deeper checks, following Barry's clarification in 76/1476. A
[numerical archive inspection](../data/q050-covariance-support/README.md)
has since verified the two Brombacher objects and the ZIP checksum. It
corrects the time-field interpretation below: their `tt` values are elapsed
coordinates, not adjacent increments. The access limits below describe this
note's first-tranche checks; the linked audit records the subsequent depth.

## Question and scientific stakes

**How does the capacity to evolve change during environmental upheaval?**
Does the pattern of variation already present within a population channel its
initial evolutionary response, and how quickly does that pattern itself
reorganise? Can fossil sequences distinguish persistent inherited constraints,
selection reshaping variation, and feedback between them?

This addresses the connection between variation among individuals and the
directions evolution takes over geological time. A predictive relationship is
already established in several systems; its existence is not the contribution.
The consequential issue is whether evolutionary responsiveness is a persistent
property of a lineage or changes with its environment, and what observations
can distinguish those mechanisms. The alternatives can coexist.

Q-036 concerns morphological stasis, geographic redistribution and habitat
tracking. Q-050 concerns the joint dynamics of multivariate variation and
evolutionary change, including substantial change. Geographic replacement is
one rival explanation here. No mass extinction is required for the test.

## Closest work and access

All checks below were on 11 October 2026. These are precedents and constraints,
not declarations that a new analysis would be novel.

| Source | Access actually checked | What is already occupied |
| --- | --- | --- |
| Hunt 2007, *Evolutionary divergence in directions of high phenotypic variance in the ostracode genus Poseidonamicus*, [10.1111/j.1558-5646.2007.00129.x](https://doi.org/10.1111/j.1558-5646.2007.00129.x) | Official PubMed abstract | Ancestor–descendant and phylogenetic changes align with high-variance directions; alignment weakens over millions of years. Forward alignment itself is not new. |
| Brombacher et al. 2017, *The breakdown of static and evolutionary allometries during climatic upheaval*, [10.1086/692570](https://doi.org/10.1086/692570) | Publisher Methods, Results and Conclusion; delegated check also covered Discussion | Two foraminifera, 12,633 specimens, roughly 500 kyr: covariance at one sample predicts the next change, and alignment breaks down across climate phases in the extinct-going species. Environmental-regime tests are already present. |
| Brombacher et al. 2023, [10.3389/fevo.2023.1165174](https://doi.org/10.3389/fevo.2023.1165174) | Methods §§2.2–2.3, Results, Discussion and data statement | Six Atlantic populations of two species show spatially varying covariance and poor transfer across populations. The authors interpret this through local adaptation; they explicitly discuss mixing, time averaging and limits to a two-species contrast. |
| Holstad et al. 2024, *Evolvability predicts macroevolution under fluctuating selection*, [10.1126/science.adi8722](https://doi.org/10.1126/science.adi8722) | Author-hosted main text, pp. 1–4; delegated main-text check | Already predicts consecutive fossil change, examines noncausal alternatives and advances tracking of rapidly fluctuating optima. The authors reject concordant selection as a general explanation using empirical scaling and theoretical arguments. This is a mechanistic predecessor, not merely a correlation study. |
| Tsuboi et al. 2024, *The paradox of predictability provides a bridge between micro- and macroevolution*, [10.1093/jeb/voae103](https://doi.org/10.1093/jeb/voae103) | Author PDF: pp. 2–4, Box 1, palaeontology section and Table 2 | Explicitly poses constraint versus selection shaping variation, and proposes environmental shifts to distinguish them. Includes 25 multivariate time series from 15 studies. Both the broad question and that proposed source of discrimination are published. |

**Residual worth testing (Codex inference).** A joint process model for
pre-transition covariance, subsequent mean displacement and covariance
reorganisation may distinguish mechanisms that fit the same aggregate
variance–divergence relationship. The papers above establish substantial parts
of this programme. No completed resolution of this particular joint test was
found in the bounded inspection; that is not an exhaustive novelty result.
Holstad's rejection of a general explanation and Tsuboi's continuing treatment
of competing mechanisms should be compared at the level of assumptions and
predictions, not presented as a simple contradiction.

## Existing-data route

- **Verified archive:** the Tsuboi paper's concept DOI
  [10.5281/zenodo.11059549](https://doi.org/10.5281/zenodo.11059549) currently
  resolves through the API to version
  [10.5281/zenodo.13294509](https://doi.org/10.5281/zenodo.13294509), v1.0.1.
  The 242,575-byte ZIP was retrieved into memory and its listing and README
  inspected. It includes Brombacher, Poseidonamicus, stickleback, bryozoan and
  other series. The README documents per-step means `M`, covariance matrices
  `S`, sample sizes `nn`, a time field `tt`, traits and references in RData
  objects. Our original description of `tt` as increments came from the README;
  the later phase-2 audit corrects it for the inspected Brombacher objects.
  Numerical objects were not inspected and analyses were not run at this
  first-tranche check. The source
  advertises MD5 `ab026931157f5734790be0ed732dc94b`; it was not independently
  checked. Zenodo metadata says CC BY 4.0; the repository README names Apache
  2.0. Original dataset terms would need resolving before redistribution.
- **Specimen-level lead:** Brombacher 2017's
  [Dryad deposit](https://doi.org/10.5061/dryad.8jf2k) lists an 845.52-KB XLSX
  with shell area, aspect ratio, sample identity and ages. Metadata/usage notes
  checked; spreadsheet not downloaded. Brombacher 2023 links a Figshare
  deposit in its data statement, but that deposit was not inspected.
- **Broader comparison:** Holstad's
  [Dryad deposit](https://doi.org/10.5061/dryad.4j0zpc8hx) has an inspected
  README and file list, including consecutive-sample values and metadata for
  589 trait series. This is not 589 independent multivariate perturbation
  experiments, and it does not replace the covariance archive.

These checks establish a concrete starting resource. They do not establish
replicated environmental transitions, independent functional predictions or
sufficient temporal resolution for the proposed mechanism test. Reused series
across the publications must be counted once.

## Proposed discriminator and its limits

1. Choose existing series with repeated multivariate measurements and
   environmental changes dated independently of the morphology. Fix the trait
   definition and scaling across samples; avoid changing the coordinate system
   with each sample. Estimate uncertainty in both covariance and means.
2. Specify competing process models before fitting: persistent inherited
   covariance with shifting selection; covariance responding to past selection;
   and their feedback. Include Holstad's fluctuating-optimum mechanism as a
   substantive comparator. Restrict how environmental evidence informs
   selection using existing functional knowledge. An isotope or climate curve
   alone does not identify a fitness optimum or selection gradient.
3. Seek replicated changes, or co-occurring lineages with contrasting initial
   covariance. Compare their joint predicted trajectories: direction and
   magnitude of mean change, covariance rotation or concentration, and
   relaxation time. Score withheld transitions where support permits. A simple
   angle-to-the-next-sample analysis repeats the closest prior.
4. Pass each process through the actual sampling and observation model:
   temporal mixing, age uncertainty, finite specimen counts, measurement
   error, plasticity, immigration and changing population composition. Test
   whether these models can be recovered from simulated observations with
   those properties before interpreting an empirical preference.

**Central identification limit.** Fossils measure phenotypic covariance `P`,
not additive genetic covariance `G`. Even the short-term relationship
`change = G × selection gradient` does not separate its two factors when the
gradient is unrestricted. Temporal precedence of covariance over mean change
does not remove this problem. Persistent common selection, plasticity and
population mixture can generate apparently informative ordering. Comparisons
can discriminate specified, constrained models; they cannot establish a unique
genetic cause from phenotype alone. A useful study may therefore establish
which predictions are identifiable, while leaving causal attribution open.

**First check after review, if selected:** inspect one multivariate source
series and its environmental/age support, then conduct a small model-recovery
probe at its real resolution. No such probe was run here. Park the empirical
mechanism route if plausible alternatives produce indistinguishable joint
trajectories, if reorganisation is faster than observation, or if repeated
support and independent constraints on selection are unavailable. A failure
to resolve a lag does not show an absence of evolutionary constraint.

**Disposition:** Q-050 under review, tier 2 provisionally. Scientific importance
is strong; novelty of the specific test and empirical discrimination remain
unverified. This completes the requested question count, not a research result.

## Search boundary and first-tranche handoff

Opportunistic primary-source orientation through web search, publisher and
author pages, PubMed, Europe PMC, Dryad and the Zenodo API. Query families
included `fossil covariance matrix evolution selection changing environment`,
`Holstad 2024 evolvability fossil`, and exact titles/DOIs above. No date filter.
Stop after locating the nearest forward-prediction and environmental-shift
tests, a versioned multivariate data lead and the main identification obstacle.
This was not a systematic review. A GPT-6.1 Sol subagent provided a bounded
read-only challenge; its agreement is not independent empirical evidence.

Two exploratory candidates were not added: refuge-to-recovery overlaps Q-008
and [Morley et al. 2026](https://doi.org/10.1038/s43247-026-03563-3), while
sexual-selection effects on both origination and extinction are already tested
by [Martins et al. 2018](https://doi.org/10.1038/s41586-018-0020-7), including
Pradel speciation models in the Methods checked by the subagent. Failed PMC,
publisher and Michigan-PDF retrievals were access limits; author PDFs and
Europe PMC provided selected alternatives. No new primary analysis, remote
compute or third-party contact occurred.

Claude's round-10 Q-041/Q-044/Q-047 revisions are received. Its Q-042 bound and
inversion proposal, Q-048 whole-guild/denominator critique, and Q-049 tracking
ratio remain recorded questions for the tranche review, not silently accepted
scientific conclusions. Q-038 stays deferred. Barry leads the next review;
neither agent has a standing next expansion task while this pause is in force.
