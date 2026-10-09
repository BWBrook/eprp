# Register checks, round 1: Q-011 to Q-015 and the Q-007 Cenozoic support audit

Owner: Claude | Date: 9 October 2026 | Supports [the register](../ideas/register.md)

**Method.**
- Six bounded Sonnet scouts ran in parallel: one nearest-prior-work check per
  sketch, and one data-capability audit.
- Each stopped after two consecutive search rounds with nothing new.
- All DOIs resolved in Crossref, which was checked by the scouts. Claude
  re-checked eleven key DOIs and the Strona & Bradshaw abstract.
- Where the scouts' years differ from Crossref's, Crossref's are used: Silvestro
  et al. 2019 (Ecol Lett); Saulsbury et al. 2023 (PNAS).
- Depth: abs = abstract; sect = named sections; full = full text; 2nd =
  secondary summary only.
- Novelty is never established by "not found".

**Overall result.** None of the five sketches posed as tier 1 stays at tier 1
after its first check. Each is partly occupied, or limited by the small number
of well-dated events (about 6–30) and by forcing metrics that share no common
scale. See the lessons section at the end.

## Q-011 What sets the size distribution of extinction events?
Verdict: **under review, tier 2**.

**Established.**
- Magnitudes form a continuous, right-skewed distribution with no break between
  background and mass extinction (Raup 1991; Wang 2003; Alroy 2008; Marshall
  2023; Crampton et al. 2026).
- Power-law or self-organised-criticality signatures do not discriminate
  between mechanisms. Newman's stress-threshold model gives an exponent of
  about 2 for almost any stress distribution (Newman 1997,
  10.1006/jtbi.1997.0508, full). A ~1/t decline in rate alone reproduces it
  (Newman & Eble 1999, 10.1017/s0094837300020303, abs). The 1/f spectra were an
  interpolation artefact (Kirchner & Weil 1998, 10.1038/26384, 2nd). Alroy 2008
  found no autocorrelation.
- Forcing and extinction are positively related, but only coarsely:
  - Song et al. 2021: ρ = 0.63 across 45 bins.
  - Kaiho 2022: a linear fit on six crises.
  - Green et al. 2022 (10.1073/pnas.2120441119, full): flood basalts coincide
    with stage boundaries above chance, and response is roughly linear in
    eruption rate.
  - Arens & West 2008 (10.1666/07034.1, abs): across 73 stages, extinction is
    uncorrelated with LIP or crater size alone.
  - Rothman 2019 (10.1073/pnas.1905164116, abs) attributes disruption size to
    the carbon cycle's intrinsic excitable dynamics, not to forcing strength.

**Not found:** a fitted forcing-to-extinction transfer function that tests
whether the observed tail needs amplification.

**Inference.** The shape of the tail alone cannot discriminate forcing-only
from amplification, because the Newman exponent does not depend on the forcing.
Identification needs paired forcing and response events.

**Open.**
- A dose–response *form* test on a catalogue chosen independently of
  extinction, including benign perturbations, with age and measurement error.
- Covariates for residual tail weight: O₂, background temperature, diversity.
- Whether the fitted map reproduces the observed extinction tail.

**Kill.** Only about 10–30 well-dated events; forcing metrics (ΔT, δ¹³C size,
LIP rate, crater size) with no common scale; stage averaging that hides pulses;
event-to-driver attribution that is itself circular.

**Link.** The reduced form overlaps Q-003, which supplies the detectability
diagnostic.

## Q-012 Is extinction risk age-dependent?
Verdict: **promising, tier 2, reframed**.

**Established.**
- Declining hazard with age is widely replicated in observed survivorship:
  - Silvestro et al. 2019 (10.1111/ele.13441, sect): >90% of 21 invertebrate
    clades.
  - Hagen et al. 2018 (10.1093/sysbio/syx082, sect): fossil analyses give
    declining hazard; phylogenetic analyses give the opposite sign.
  - Januario & Quental 2021 (10.1111/evo.14177, abs).
  - Kocáková et al. 2025 (10.1098/rspb.2025.2272, abs).
- Quintero et al. 2025 (10.1038/s41559-025-02873-7; abstract plus preprint
  sections): heritable rates drift so that extinction rises in absolute time
  across 27 clades.
- Tikhonov et al. 2026 (openRxiv 10.64898/2026.07.21.739780, full): fixed
  per-genus "toughness" plus event "luck" fits Sepkoski survival curves with no
  age effect.
- Saulsbury et al. 2023 (10.1073/pnas.2307629121, sect): a neutral model with
  explicit sampling fits graptoloid ages. A comment by Johnson
  (10.1073/pnas.2412160122) argues curve-fitting cannot discriminate between
  models.

**Inference (scout).** Quintero's drift is a secular within-clade trend, not
hazard as a function of species age, so the two papers are not direct rivals.

**Open, reframed.** Is the decline intrinsic, or produced by selection on fixed
heterogeneity (frailty)? A decisive design:
- Triton species-level foraminifera combined with a lineage phylogeny with
  pseudoextinction removed (Aze et al. 2011, 10.1111/j.1469-185x.2011.00178.x).
- A Weibull hazard with preservation modelled in each bin.
- One simulation null that generates constant-hazard, frailty and neutral data,
  each passed through the same sampling.

**Kill.** Frailty mixtures may be unidentifiable from survivorship alone;
taxonomic artefacts in foraminifera (Pearson 1992); an active group already
working on this (Quental, Silvestro, Liow, Saulsbury).

## Q-013 Would the current extinction register as a mass extinction in the rock record?
Verdict: **promising, tier 2**.

**Correction to my sketch.** Strona & Bradshaw 2026 (openRxiv, full by scout;
abstract by Claude) concerns species that go extinct before being *described*.
Their "49%" is a share of a parameter grid, not a probability of rock-record
detection. There is no preservation filter, stage-grain model or genus
aggregation. It does not pre-empt Q-013.

**Nearest work.**
- Payne et al. 2016 (10.1126/science.aaf2416, full author copy): of 2,497
  marine vertebrate and mollusc genera, 24–40% would be lost under the
  pessimistic IUCN scenario. That reaches end-Cretaceous levels. Their genus
  rule (a genus counts as lost if any species is threatened) probably overstates
  committed genus loss [inference].
- Krone et al. 2024 (10.1017/pab.2023.34, abs): about 30% of tetrapod species
  have almost no chance of fossilising; amphibian losses would be
  underestimated by 66–98%.
- Plotnick et al. 2016 (abs) and Spalding & Hull 2021 (full).
- Shaw et al. 2021 (10.1130/g47907.1, abs): 38% of modern marine assemblage taxa
  have a PBDB record.
- Kowalewski et al. 2023 (10.1017/ext.2023.22, sect): preservation potential at
  order level for IUCN invertebrates.

**Open.**
- Marine invertebrates beyond molluscs, with clade-specific preservation.
- Correct aggregation to genus loss: all congeners must be lost.
- An explicit stage-grain observation model with Signor–Lipps smearing,
  compared against the full magnitude spectrum.
- An operational definition of "registers as a mass extinction", given that
  the Big Five are not statistically distinct (Marshall 2023).
- Committed versus realised scenarios, and full uncertainty propagation.

**Kill.** Marine invertebrates are barely assessed, so committed loss would be
mostly imputed. The IUCN API needs a token and its terms must be checked.

## Q-014 How long is the extinction debt after a deep-time perturbation?
Verdict: **sketch, tier 3 as posed**.

**Measured timings.**
- End-Permian: first Siberian lavas about 300 kyr before extinction onset; sill
  onset coincident (Burgess et al. 2017, 10.1038/s41467-017-00083-9, full);
  extinction interval 60 ± 48 kyr (Burgess et al. 2014).
- End-Triassic: CAMP synchronous with extinction (Blackburn et al. 2013; Davies
  et al. 2017).
- K–Pg: impact within 32 kyr of extinction (Renne et al. 2013).
- PETM: benthic loss at, or about 10 kyr after, CIE onset (Alegret et al. 2009).
- Panama closure: extinction lags environmental change by 1–2 Myr (O'Dea et al.
  2007, 10.1073/pnas.0610947104, abs).
- Kasbohm et al. 2021 (10.1002/9781119507444.ch2, abs): LIP onset leads
  extinction by several hundred kyr across 12 couplets, with no magnitude
  regression.

**Not found:** any cross-event regression of lag on perturbation size or rate.

**Inference.** "Lag" is ill-defined: it depends on which forcing onset is used
(first lava, sill, CIE). It is at or below resolution for most mass extinctions,
and Signor–Lipps bias pushes it negative. The resolvable debts are slow regional
perturbations such as the Panama closure.

**Reframe for tier 2.** "Extinction debt under slow, regional perturbations",
using Cenozoic cases with dense records, plus an explicit power analysis.

## Q-015 Could past lineages evolve thermal niches as fast as climate changed?
Verdict: **under review, tier 2**. Codex's objection is accepted.

**Established.**
- Occupancy-defined niches are mostly static:
  - planktonic foraminifera over 700 kyr (Antell et al. 2021,
    10.1073/pnas.2017105118, full);
  - molluscs over 3 Myr (Saupe et al. 2014);
  - turritellines across the K–Pg.
- Ying et al. 2024 (10.1038/s41586-024-08029-0, full) find an optimum shift in
  symbiont-bearing foraminifera from the Last Glacial Maximum to the Holocene,
  labelled acclimatisation. That verdict is opposite to Antell's on the same
  class of data and depends on the niche definition.
- Saupe et al. 2019 (GEB, 10.1111/geb.12904, abs) shows that realised-niche
  patterns arise with no niche evolution. This makes it a required null, not a
  decisive rebuttal.
- Modern heat tolerance evolves slowly (Bennett et al. 2021,
  10.1038/s41467-021-21263-8; Araújo et al. 2013).

**Not found:** any fossil niche-evolution *rate* separated from tracking, or
any test of whether faster adapters survived.

**Possible overlap.** An Antell & Saupe GSA 2021 abstract (10.1130/abs/2021am-369023)
is titled "rate and mode of thermal niche evolution… Cenozoic planktonic
foraminifera". Its text was not retrieved. Check it first.

**Sharpest version.** Same-shell calcification temperature (Mg/Ca, δ¹⁸O;
Boscolo-Galazzo et al. 2025, 10.5194/bg-22-1095-2025) against ambient
temperature across hyperthermals, with a fixed-niche null run through the same
climate model and sampling.

## Q-007 support: Cenozoic deep-sea audit
Owner of this audit: Claude, agreed in 82/1220.

**Sources inspected.**

| Source | Licence | What was inspected |
| --- | --- | --- |
| Triton v4 (Figshare collection c.5242154) | CC0 | Metadata, README and inputs only. The final `Triton.zip` (307 MB) was not opened, being over the scout's cap |
| NSB snapshot (Zenodo 10063218) | CC-BY-4.0 | Data inspected: 783,987 occurrences; age-model tiepoints for 483 holes with quality flags |
| CENOGRID (PANGAEA 917503) | CC-BY-4.0 | Data inspected: benthic records only; one dominant site per event window (1262; 1262/1263; 1218/1263) |
| PhanSST v0.0.1 (GitHub) | — | Data inspected: site-level d18c, Mg/Ca, TEX86 and UK'37, with diagenesis flags |
| DeepMIP v0.1 | — | Workbook structure only |

**Coverage by event** (NSB; at least 5 samples on each side of the event):

| Event | Sites with species-level sampling | Sites with both biota and site-level temperature |
| --- | --- | --- |
| K–Pg | 2 foraminifera / 7 nannoplankton | 0 |
| PETM | 2 / 4 | 2, or 0 when diagenesis-flagged records are dropped |
| Eocene–Oligocene | 12 / 17 | 5, or 4 well preserved, clustered at 57–65°S |

Abundance is largely categorical or presence-only. Ages come mostly from
biostratigraphic interpolation, which risks circularity with range ends. Triton
has no pre-K–Pg baseline.

**Verdict.**
- The support is *not adequate* to discriminate instantaneous tracking,
  finite-rate response and additional memory across events.
- A within-event pilot is feasible at the Eocene–Oligocene transition only.
- My hyperthermal-loop proposal (82/1224) fails the gate as currently known:
  PETM has fewer than three usable sites. ETM2 and ETM3 were not checked.

**Cheapest next step.** Download the full Triton release (307 MB) on
deep-server. Rebuild the per-event site table with `age.calc` and `abun.units`,
joined to PhanSST and DeepMIP. Gate: at least 5 sites per event with age models
not based solely on biozones.

## Lessons for future ideation

[Inference from this round.]

1. **Cross-event questions hit a ceiling of roughly 6–30 events.** Few events
   are well dated, forcing metrics are not commensurable, and attribution is
   circular. Questions designed around many events are weak by default.
2. **Stronger designs exploit replication *within* events or continuous
   records.** That means spatial and taxonomic contrasts within one event, all
   stage transitions as a continuum, species-level microfossil series, and
   lineage-resolved phylogenies.
3. **Resolution sets what can be identified.** Lags, precursors and pulses
   shorter than about 50–100 kyr are mostly unresolvable before the Cenozoic.
4. **Live disputes are promising seeds** (Q-012, Q-015), provided the dispute
   turns on identification rather than data volume.
