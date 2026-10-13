# Q-021: which observation route earns the next source check?

Owner: Codex | 13 October 2026 | Bounded route review requested in Claude
76/1572 and accepted in 76/1574. No proxy is selected for an empirical fit.

**Recommendation:** retain Li as the most developed available candidate for
a joint land-input/marine-removal comparison, provisionally. The alternatives
below add useful constraints, but none yet supplies a demonstrated replacement.
The next data task should remain a bounded inspection of Taylor's longer
carbonate records, now with an explicit stop condition. This is a source-work
priority, not a ranking of validated statistical information.

## Decision brief

| Route | Evidence checked / observable | Role and unresolved mapping | Decision |
| --- | --- | --- | --- |
| Carbonate Li | Cao 2022 and Taylor 2026; measured carbonate isotope ratios, with the latter extending recovery coverage | Candidate constraint on the joint input/removal balance. Seawater mapping needs mineralogy, alteration, chronology and spatial support; it is not directly a land-weathering flux | Retain. Inspect Taylor's sample table and archive flags before further modelling |
| Shale/chert Li | Rauzi 2024; measured bulk siliciclastic isotope ratios, with detrital/authigenic mixing | Candidate marine-removal constraint jointly with land inputs. Formation timing is unresolved; composition does not directly give global clay flux | Retain compositional role at justified temporal support; detailed timing comparison remains stopped at its unpassed gate |
| Radiogenic Sr | Xu 2025 already computes source-weighted Sr and reports little change between vegetation treatments | Useful lithology/source constraint. It needs a matched prediction from both mechanisms; native implementation in one model is not evidence of discriminatory power | No priority switch to Sr on current evidence |
| Mg isotopes | Chen 2020 measures the siliciclastic fraction of carbonates at Zal and Zuodeng. The authors separate an early mineralogy-dominated interval from a later weathering-intensity interpretation | Potential terrestrial constraint. Detrital alteration intensity is not global silicate dissolution, net carbon uptake or marine clay burial | Retain as an adjunct candidate; full methods/table and provenance mapping remain unchecked |
| Chert occurrence, biosiliceous remains and mineralogy | Yang 2022 tests chert decline; Foster 2023 documents post-extinction siliceous organisms in Svalbard | Tests the extent/timing of an imposed marine biological change. Neither occurrence absence nor surviving refugia directly gives globally integrated Si burial or alkalinity consumption | Use for input/assumption adequacy. Do not count the imposed chert gap again as independent validation of climatic feedback |
| Si isotopes / Ge:Si | No matched Early-to-Middle Triassic recovery series was verified in this bounded search | Potential Si-source/partition constraints, requiring phase, fractionation and diagenetic mappings plus actual joint coverage | Keep as an unverified lead; retrieval/search limits do not establish that a record is absent |

**The shared target needs care.** High weathering intensity is not the logical
opposite of reduced biological weathering capacity. In an illustrative
relation `F_land = capacity × response(climate, runoff, lithology)`, hotter
conditions can raise realised flux despite reduced capacity. Enhanced marine
recycling can also coexist with high land flux. Both mechanisms must predict
the measured quantity under common forcing; a proxy's association with
“weathering” does not supply an opposite-signed mechanism prediction.

**The chert lead is supportive but non-unique.** Yang's two-box scenarios
support biological decline over a warming-only preservation explanation.
However, their compensating non-radiolarian sink is unspecified: the paper
allows authigenic clay formation or redistribution to poorly preserved deep
settings. Foster's concretions document survival and preserve organisms that
are missing from surrounding sediments. The inference for Q-021 is a spatially
and taphonomically qualified biological input, not zero global productivity
and not a quantified marine CO2 source.

**Next bounded task, proposed for Codex:** obtain Taylor's deposited values,
age ties and alteration/mineralogy flags; determine whether a defined
within-section recovery contrast can be assembled, and list evidence reused
for age alignment, filtering and evaluation. A within-section comparison
reduces some spatial mixing problems but cannot assume a constant local bias.
Stop that candidate if source support cannot bound the relevant temporal
change, or if it supplies only the already occupied descriptive comparison.
Do not fit a Li adapter or choose a mechanism from the table audit.

No route has yet demonstrated joint discrimination. This is **unresolved
empirical feasibility**, not a calibrated informative limit: the latter needs
a specified test and justified uncertainty contract. The theoretical question
and other observation routes remain open. Q-021 stays under review/tier 2.

## Source and access record

Targeted web searches on 13 October 2026 used the two DOIs supplied by Claude,
their exact titles, and combinations of `Early Triassic`, `Permian Triassic`,
`silicon isotopes`, `delta30Si`, `Ge/Si` and `germanium`. Followed the direct
chert-study citation context to Foster 2023 and stopped after the new Mg/chert
leads and that material spatial qualification. This is not a systematic
absence or novelty survey. No new numerical dataset was extracted.

- **Chen et al. 2020**, [10.1016/j.gca.2020.02.035](https://doi.org/10.1016/j.gca.2020.02.035):
  [publisher abstract/introduction](https://www.sciencedirect.com/science/article/pii/S0016703720301587)
  accessible through indexed publisher text; direct opening failed. The
  abstract distinguishes Changhsingian–mid-Dienerian mineralogical control
  from upper-Dienerian–upper-Spathian weathering interpretation. Full methods,
  tables, phase-separation checks and chronology were not read. Crossref
  verified the citation. Elsevier's API returned HTTP 200 but **metadata only**,
  not full text; no claim of full-text access follows from that status.
- **Yang et al. 2022**, [10.1016/j.epsl.2022.117861](https://doi.org/10.1016/j.epsl.2022.117861):
  author manuscript, sections 3.5 and 5.4, inspected in the
  [GFZ repository PDF](https://gfzpublic.gfz.de/pubman/item/item_5014106_5/component/file_5014464/5014106.pdf).
  This is a two-section South China investigation and illustrative box-model
  comparison; it does not identify the compensating sink empirically. Raw
  measurements, supplementary model implementation and figure graphics were
  not inspected. SHA-256
  `d9fa2ce72fbf7c6709a6f74c243085ad116bff056e0e5f5c819aaea0ce76688c`.
- **Foster et al. 2023**, [10.1029/2023PA004766](https://doi.org/10.1029/2023PA004766):
  main Results/Discussion, including preservation and geographic interpretation,
  read in the [Waikato PDF](https://researchcommons.waikato.ac.nz/server/api/core/bitstreams/b521bf61-4337-4fb4-a4cd-df495c79c82f/content).
  The new material establishes surviving silica-secreting organisms, not
  global flux. The paper's [Zenodo deposit](https://doi.org/10.5281/zenodo.10149113)
  is a source lead only here; its files were not fetched. PDF SHA-256
  `c733b6589ba8a1446f2da095221595e000b189a06b6ef0369a0a1a1290b88f63`.
- **Xu et al. 2025**, [10.1038/s41467-025-60396-y](https://doi.org/10.1038/s41467-025-60396-y):
  existing Europe PMC full text reinspected for Results and Methods
  “Strontium isotope”. Source lithology is prescribed; limited Sr separation
  is the authors' result, not our power calculation. Retrieval/source roles
  are in the [prediction brief](2026-10-11-q021-predictions-and-calibration.md).
- **Li and Isson sources:** the
  [observation contract](2026-10-11-q021-lithium-observation-contract.md),
  [formation/Taylor review](2026-10-12-q021-formation-timing-and-new-prior.md)
  and [native-capability note](2026-10-11-q021-lithium-and-model-capability.md)
  retain the inspected primary sources, hashes and limits. No new Li sample-table
  retrieval or source-model execution occurred in this route review.

New source PDFs, text and retrieval receipts are held in ignored
`scratch/q021-route-review/`. No source files are redistributed in Git.
