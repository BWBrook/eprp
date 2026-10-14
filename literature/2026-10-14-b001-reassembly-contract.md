# B-001: target contract for a repeatable reassembly order after crises

Owner: Claude | 14 October 2026 | The first bounded product for
[B-001](../ideas/register-blue-sky.md#b-001-do-ecosystems-reassemble-in-a-repeatable-order-after-crises).
It applies Codex's corrections from cross-critique.

Status: **a design contract.** No data were analysed and no model was fitted.

Sources:
- A Sonnet subagent read Song et al. 2018, Dunhill et al. 2024 and Nicholls
  et al. 2026 in full; Cribb et al. 2023 and Dunhill et al. 2018 in their
  Methods; Chen & Benton 2012 by abstract only (paywalled); the rest by
  abstract.
- Claude checked the decisive points against the extraction.
- All DOIs were checked against Crossref.

## 1. The two "conflicting" accounts measure different things

| Work | What it measures | Scale and resolution | What "order" means there |
| --- | --- | --- | --- |
| Chen & Benton 2012, 10.1038/ngeo1475 (abstract) | Rebuilding of **trophic structure**, asserted narratively: "rebuilt stepwise from low to high trophic levels"; a stable ecosystem "did not re-emerge until ... 8–9 Myr after the crisis". It allows ammonoids and others to diversify within 1–3 Myr | Global review; south China figure | A narrative sequence of tiers |
| Song, Wignall & Dunhill 2018, 10.1126/sciadv.aat5091 (full) | **Subsampled genus richness and proportion** for three motility classes: non-motile (which lumps planktonic protists with sessile benthos), motile, and nekton. "Top-down" is inferred by *assuming* nekton are top predators | Global; 17 bins, mean 3.1 Myr; 4,321 genera | Group curves and the nekton proportion, not first reappearance |
| Dunhill et al. 2024, 10.1038/s41467-024-53000-2 (full) | Inferred feasible **food webs** (13 metrics) and guild richness | One basin (Cleveland, Toarcian), 4 intervals | Metrics recover at different times: the early community was "tall, thin and top-heavy" |
| Nicholls et al. 2026, 10.1038/s44185-025-00117-2 (full; a perspective) | Reconciles the accounts as different metrics: "rapid recovery of multiple trophic levels albeit in the form of top-heavy, unstable Early Triassic ecosystems" | Global against local | — |

**Inference.** Chen & Benton and Song et al. are not a clean test between
bottom-up and top-down assembly rules. They differ in:
- endpoint: trophic completeness against richness and proportion by
  motility class;
- the meaning of "recovery";
- classification: motility is not trophic level.

So B-001's residual is **not** "resolve the end-Permian conflict". It is:
for a *defined* endpoint, is there a shared order of re-establishment
across events, beyond survivor pools, sampling, clade contingency and
shared environmental tolerances?

Other single-event or descriptive work: Foster & Twitchett 2014; Dunhill et
al. 2018 (10.1111/pala.12332, end-Triassic, recovery timing by mode of
life); Cribb et al. 2023; Edie et al. 2018; Alvarez et al. 2019 and Lowery &
Fraass 2019 (K–Pg plankton function and complexity). No cross-event test of
order was found in this bounded search.

## 2. The target

- **Primary endpoint: guild re-establishment time.**
  - A guild's re-establishment time is the first post-event bin in which
    its subsampled genus richness regains a fixed fraction (set in advance;
    proposed 50%) of its baseline in the last pre-event bin.
  - The order within an event is the ranking of these times across guilds.
  - This is endpoint 2 (richness), not first reappearance (endpoint 1). A
    single occurrence is too exposed to Lazarus effects and sampling.
- **Secondary endpoints, reported separately and never pooled:**
  - relative dominance (endpoint 3);
  - local trophic completeness (endpoint 4), only where Lagerstätten or
    basin-scale data exist, as in Dunhill et al. 2024.
  - Recovery of process (endpoint 5; for example reef building) is out of
    scope except as context.
- **Guild:** Bambach-style tiering × motility × feeding.
- **Events:** at least three of the Big Five, provisionally end-Permian,
  end-Triassic and K–Pg first (the best-sampled recoveries). Bins are
  stages or substages.

## 3. Conditioning (Codex's corrections)

The order must be interpreted *given*:
- the **surviving functional pool**. A guild with no survivors must
  re-evolve or immigrate, so its "evolutionary availability" differs;
- **pre-event occupancy**. Dominant guilds have more survivors and
  re-establish faster mechanically;
- **continuing stress** after the event (for example the Early Triassic
  hothouse);
- **event severity.**

## 4. Explicit rival assembly processes

| Rival | What generates the order | What it predicts |
| --- | --- | --- |
| R0. Sampling and survivor-pool null | Survivor counts, per-genus origination neutral among guilds, and detection specific to each guild | The baseline order, simulated per event |
| R1. Clade contingency | Clades dominating each guild recover at their own rates | Order tracks clade identity. No shared functional order once clade composition is accounted for |
| R2. Bottom-up assembly rule | Primary-consumer guilds (suspension and deposit feeders, grazers) re-establish before predators | A shared order beyond R0 and R1 |
| R3. Top-down or opportunistic | Mobile or nektonic predator guilds re-establish early (as in Song et al.; Dunhill et al. 2024's "top-heavy") | A shared order in the opposite direction |
| R4. Shared environmental tolerance | Order follows environmental recovery (oxygen, temperature) through guild tolerances | A repeated order that disappears once the trajectory of environmental recovery is conditioned on |

**Key discriminators:**
- **R1 against R2 and R3 (functional rule against clade contingency).**
  Are guilds refilled by *different clades* in different events? Refilling
  of the same guild by different clades, at the same rank, supports a
  functional rule. Refilling by the same clades at the same rank is
  compatible with R1.
- **R2 and R3 against R4.** Does the order persist after conditioning on
  the timing of environmental recovery?

## 5. Observation model

- **Trait coding mostly mirrors the classification.**
  - In PBDB's ecospace fields, about 99% of genus values are *inherited
    from higher taxa*; only about 1–1.5% are entered directly for genera
    (queried 14 October).
  - So a guild largely equals a clade. Any test must state that R1 cannot
    be excluded by coding alone; the cross-event refilling test in section
    4 is required.
- **Detection by guild:**
  - nekton and soft-bodied predators preserve poorly;
  - the mineralogy of aragonite and calcite matters;
  - post-event facies change (microbialites);
  - Lagerstätten inflate local completeness.
- **Resolution:** substages of about 1–3 Myr against a recovery pace of
  about 1–10 Myr, plus time-averaging.
- **Range-through against occurrence data:** first reappearance needs
  occurrences; range-through inflates presence.

## 6. Data support

| Resource | Contents | Terms | Coverage |
| --- | --- | --- | --- |
| Knope et al. 2015 Supplementary Dataset 1 (10.1038/ncomms7455) | 18,621 genera, Bambach-coded tiering, motility and feeding; stage first and last appearances | CC BY 4.0; 3.8 MB (not yet downloaded) | Whole Phanerozoic, but range-through only |
| PBDB occurrences | Occurrences for subsampling | CC0, API | All events |
| Foster & Twitchett, PANGAEA 824825 | Permian–Triassic occurrences and ranges, 12 substages | CC BY 3.0 | Permian–Triassic check |
| Dunhill et al. 2018 Dryad (10.5061/dryad.bg30k); Cribb et al. 2023 Zenodo (10.5281/zenodo.8398420) | End-Triassic modes of life | Open | End-Triassic check |
| Dunhill et al. 2024 Zenodo (10.5281/zenodo.11400588) | Toarcian guild tables and PFIM scripts | CC BY 4.0 | Endpoint 4, one basin |

**No open occurrence-level ecospace matrix spans three or more
recoveries.** The route is PBDB occurrences joined to Knope's coding by
genus.

## 7. Test, informative either way

- **Statistic.** Concordance of guild re-establishment ranks across events
  (Kendall's W), conditioned as in section 3.
  - It is compared with the R0 null simulated per event, using that
    event's survivor pool and detection.
  - It is also compared with R4, by conditioning on the environmental
    trajectory.
- **A consequential repeatability threshold, fixed now:** W ≥ 0.5 and
  above the 95th percentile of the null.
- **Outcomes:**
  - **(a) Assembly rule supported:** W above the threshold, beyond R0 and
    R4, with refilling by different clades. The direction (R2 against R3)
    is then reported.
  - **(b) Informative negative:** the interval for W lies below a
    negligible level (proposed 0.2) beyond the null. That indicates
    contingent reassembly at this grain.
  - **(c) Inadequate discrimination:** the interval spans both levels.
    Park the empirical route at this grain and keep the question.
- **Stop rules:**
  - joint support fails (below);
  - or the R0 null alone reproduces any observed concordance.

## 8. Next gate: a support audit, before any analysis

1. Download Knope's Dataset S1 and audit how well it joins to PBDB genera
   occurring in the recovery windows of the three first events.
2. Count the guild × event × bin cells that reach a minimum subsampled
   occurrence count, set in advance.
3. Record how many guilds have zero survivors per event, and how many are
   refilled by clades different from those that filled them before the
   event.
4. **Stop** if fewer than about 6 guilds have adequate support in each of
   3 events. Concordance across fewer guilds is uninformative.

**Overlap.** Q-007 and Q-009 are linked. B-010 (reef export) and B-011
(energetic autonomy) may share trait resources but are different tests.
