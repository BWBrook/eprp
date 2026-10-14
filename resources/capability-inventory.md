# Capability inventory for blue-sky deep-time ideation

Drafted by Claude, 14 October 2026, as shared input to the blue-sky round
(see [ideas/register-blue-sky.md](../ideas/register-blue-sky.md)). Codex is
invited to amend it.

**Factual only. It proposes no questions.** Access labels:
- **held**: in the git-ignored `data/raw/`;
- **used**: inspected in an EPRP audit. That means inspected, not
  successfully executed. No model listed here has been run;
- **named**: cited in EPRP notes, not yet accessed;
- **recall**: known to exist, not checked in EPRP.

Licences and terms are recorded where an EPRP note checked them. The
round-1 resource table in
[literature/2026-10-disruption-susceptibility.md](../literature/2026-10-disruption-susceptibility.md)
has more detail.

## Occurrence, range and assemblage data

| Resource | What it gives | Access in EPRP |
| --- | --- | --- |
| Paleobiology Database (PBDB) | Global occurrences, collections, taxonomy, palaeocoordinates (several plate models) | **used** through the API (Q-027, Q-042, Q-006 extracts, pinned by sha256). The API serves current data only; filters do not restore historical versions (Q-045) |
| Benson et al. 2025 archive | PBDB download of 2022, LBG code, climate-model fields | **held** (selected members); Zenodo 15269137 |
| Close et al. 2019 deposit | Tetrapodomorpha PBDB downloads from 2017, local-richness code | **held**; Dryad 10.5061/dryad.3v0p84v |
| Monarrez et al. 2023 deposit | Genus capture histories over 86 stages, traits, PBDB extract | **held**; Dryad 10.5061/dryad.931zcrjqw |
| Triton | Species-level planktonic foraminifera occurrences, Cenozoic | **held**, **used** (Q-007 support screen) |
| Neptune (NSB) | Cenozoic marine microfossil occurrences (Renaudie 2020, 10.26879/1032) | **named** (Q-016) |
| Geobiodiversity Database | High-resolution section ranges (Fan et al. 2020, ~11,000 species, Cambrian–Triassic) | **named** (Q-042) |
| BioDeepTime | Local assemblage time series (10.1111/geb.13735; Zenodo 8154672) | **named** |
| NOW | Cenozoic mammal localities | **named** (Q-016); access terms not checked |
| Neotoma | Quaternary palaeoecological records | **named** (catalogue) |
| Macrostrat | Rock units and sediment-volume context | **named** (catalogue) |
| Crampton et al. 2026 graptoloids | High-resolution CONOP composite | **named**; Dryad 10.5061/dryad.vx0k6dk71 |

## Phylogenies and trait data

| Resource | What it gives | Access |
| --- | --- | --- |
| Cantalapiedra et al. 2019 | Dated mammal trees, 10 Nexus files | **held**, **used** (Q-022 pre-mortem) |
| Aze et al. 2011 | Macroperforate foraminifera phylogeny, lineage-level | **named** (Q-012) |
| Brombacher et al. 2017 | Specimen morphometrics, Site U1313 | **held** (workbook, MD5 verified); Tsuboi archive **used** (Q-050) |
| Tsuboi et al. 2024 archive | Two covariance series | **used** (Q-050) |
| Open Tree of Life | Synthesis tree | **named** |

## Climate, environment and chronology

| Resource | What it gives | Access |
| --- | --- | --- |
| PhanDA (Judd et al. 2024) | Phanerozoic GMST and CO2 ensemble; GTS2020 | **held**, **used** (stage-difference sensitivity) |
| PhanSST | Sea-surface temperature proxy compilation | **held** |
| Song et al. 2021 | Stage ΔT and extinction data | **held** |
| HadCM3L priors and BRIDGE stage simulations (Valdes et al. 2021) | Spatial climate fields | **named**; the Benson archive bundles 240 MB of fields (not fetched) |
| LR04; CENOGRID | Cenozoic benthic δ18O stacks | **used** (LR04, Q-050) / **named** |
| PANGAEA site exports | Same-site proxies (for example, U1313) | **used** (Q-050, five exports) |
| Li-isotope records (Cao 2022; Rauzi 2024; Taylor 2026) | Permian–Triassic Li series | **used** (Q-021 audits) |

## Palaeogeography

| Resource | Access |
| --- | --- |
| PBDB palaeocoordinates (several models) | **used** |
| PALEOMAP-derived geography (via Cermeño et al.) | **named** |
| GPlates and open plate models | **recall**; not checked in EPRP |

## Models and simulators

| Tool | Kind | Access |
| --- | --- | --- |
| cGENIE (Stockey 2021; Ying 2026 deposits) | Earth-system model of intermediate complexity | **named**; deposits not checked |
| SCION (Xu 2025 fork) | Long-term carbon–climate model | **used** (code inspected for Q-021) |
| INDITEK; SNCI | Diversity and recovery models | **used** (data listings inspected for Q-007/Q-010) |
| TREED | Vegetation and Earth-system model | **named** |
| gen3sis | Spatially explicit eco-evolutionary simulator | **named** (a capability lead) |
| DeepDive simulator and estimator | Simulated fossil records; richness estimation | **named** (LGPL-2.1, v1.0.28) |
| PyRate | Rates from occurrences | **named** (AGPL-3.0) |
| FossilSim; RevBayes; BEAST2 (sampled ancestors) | FBD simulation and inference | **named** |
| divDyn; iNEXT; dggridR; palaeoverse | Rates, coverage, grids, data preparation | **named**; Benson's pipeline uses iNEXT and dggridR |
| RMark/MARK | Capture–recapture | **used** (RMark 3.0.0 design, Q-038 audit) |

## Compute

| Host | Capacity | Status |
| --- | --- | --- |
| wsl-laptop | 8 cores, 16 logical CPUs (i9-9880H); WSL memory capped at 12 GB, about 11 GB visible | Small local probes only |
| deep-server | Large memory, many cores | Large-memory and long runs |
| kunanyi (TPAC) | Up to 48 nodes × 28 CPUs through PBS | **Barry must open the authorisation jumpbox before agents probe it** |
| alienware | 2 × RTX 2080 | Not ready for serious workloads until Barry confirms |

## Access lessons from phases 1–2

- Anonymous or scripted downloads failed (HTTP 401/403) for the Dryad
  deposits we tried: Close 2019, Benson 2025 (Dryad companion), Monarrez
  2023, Brombacher 2017, and the Slattery deposit for Q-036. Barry's manual
  downloads worked for the first four.
- Some publisher full texts and supplements are blocked. Europe PMC and
  author copies often work.
- PBDB cannot replay historical versions of its data.
- Deposits are often not runnable as deposited (Close 2019). Their outputs
  may not match the published fits (Monarrez 2023).
