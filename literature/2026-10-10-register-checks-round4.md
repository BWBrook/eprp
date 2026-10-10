# Register checks, round 4: Q-030 and Q-031, and the Q-022 power-calibration design

Owner: Claude | Date: 10 October 2026 | Supports [the register](../ideas/register.md)

**Method.**
- Bounded Sonnet scouts checked prior work, stopping after two empty rounds.
- Claude checked the decisive abstracts directly in Crossref.
- Depth labels: meta = Crossref only; abs = abstract; sect = sections; full =
  full text; full\* = full text read through a summarising fetch tool.
- The Q-022 power-calibration design is in the
  [pre-mortem README](../data/q022-premortem/README.md#next-gate-power-calibration-design-not-run).
  It has not been run. It was revised after Codex 76/1340: it now calibrates
  false positives against ordinary-time clustered loss, tests incremental event
  effects, and reports induced clustering and PD-loss distributions rather than
  a single strength parameter.

## Q-031 Shrinking under warming: under review, tier 3 (headline occupied)

Scout: about 55 records screened, 12 read at section or full depth.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Nätscher, De Baets & Kiessling 2026 PNAS | 10.1073/pnas.2505564123 | abs (Claude); full preprint, code and data (scout) | About 9,000 marine-ectotherm size changes from six hyperthermals and other events. Dwarfing is general and larger in hyperthermals. Greater warming gives greater dwarfing, with slope −0.018 lnRR/°C and R² 0.018 (preprint). ΔT is one constant per event. No within/among partition; no temperature–size-rule comparison found. Data: Zenodo 10.5281/zenodo.15096088 |
| Foster, Prinoth, Kustatscher & Hautmann 2026 Biogeosciences | 10.5194/bg-23-1181-2026 | abs (Claude); sect (scout) | Permian–Triassic Dolomites bivalves: genus-level shrinking came from the origination of smaller species; the three surviving species did not shrink. "Unpredictable" response |
| Rankin et al. 2015 Proc B | 10.1098/rspb.2015.1097 | abs (Claude) | PETM mammals, extended Price equation: within-lineage change and immigration shrank mean size, while species selection favoured larger species |
| Rego et al. 2012 Paleobiology | 10.1666/11040.1 | abs | Permian–Triassic foraminifera: within-lineage shrinking dominates |
| Schaal et al. 2015 Paleobiology | 10.1017/pab.2015.36 | abs | Eight Permian–Triassic clades: both selective extinction and within-lineage change |
| Rita et al. 2019 R Soc Open Sci | 10.1098/rsos.190494 | abs (scout) | Toarcian belemnites: rostrum volume −40%, mainly within species |
| Nätscher et al. 2023 Palaeontology | 10.1111/pala.12667 | abs (scout) | Permian–Triassic ostracods: turnover towards larger species; no within-species dwarfing |
| Piazza, Ullmann & Aberhan 2020 Sci Rep | 10.1038/s41598-020-61393-5 | sect (scout) | Toarcian bivalves: compositional size–temperature link; no consistent within-species reduction |
| D'Ambrosia et al. 2017 Sci Adv; Secord et al. 2012 Science | 10.1126/sciadv.1601430; 10.1126/science.1213859 | full; abs (scout) | Equid dwarfing: ETM2 −14% at about 3 °C, PETM about −30%, then a rebound during recovery |
| Hunt & Roy 2006 PNAS | 10.1073/pnas.0510550103 | abs (scout) | Cenozoic cooling increased size overall and within lineages |
| Forster et al. 2012 PNAS; Deutsch et al. 2022 PNAS; Verberk et al. 2021 Biol Rev | 10.1073/pnas.1210460109; 10.1073/pnas.2201345119; 10.1111/brv.12653 | abs | The experimental rule, a size-dependent oxygen-limitation model, and the argument that the rule is itself evolved |

**Disposition.**
- The general warming–dwarfing relation for marine ectotherms is established
  (Nätscher 2026).
- What remains is mechanistic:
  - a within- versus among-lineage partition across events, regressed on local
    ΔT, and compared with the size-class expectation from the
    temperature–size rule;
  - the terrestrial and mammal arm.
- Event-level partitions already disagree within single events (Permian–Triassic
  foraminifera versus bivalves and ostracods). Turnover-driven shrinking may
  therefore be common.
- Tier 2 → 3.
- Not accessed, and decisive: the PNAS full text and supplement (403), which
  may already contain the partition or the comparison with the rule.
- Scout's own arithmetic, *not verified and not published*: the marine slope
  converts to about −5% mass/°C under isometry, close to Forster's aquatic
  value. It is too loose to cite: ΔT is one constant per event and R² is 0.018.

## Q-030 Declining sensitivity to perturbation: under review, tier 2 (stated and disputed, not quantified)

Scout: about 85 records triaged, 16 read at section or full depth. Claude
checked the Clapham & Renne, Green, Pohl and Wang & Bush abstracts and the
Henehan & Witts metadata directly.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Clapham & Renne 2019 Annu Rev Earth Planet Sci | 10.1146/annurev-earth-053018-060136 | abs (Claude); full (scout) | About 12 flood-basalt/hyperthermal events, discussed qualitatively. Outcomes explained by release rate "modulated by longer trends in ocean carbon cycle buffering and the composition of marine ecosystems". Only Cenomanian OAE2 among post-Jurassic hyperthermals caused even moderate extinction. **Nearest prior** |
| Payne, Bachan, Heim, Hull & Knope 2020 Interface Focus | 10.1098/rsfs.2019.0106 | abs; sect\* (scout) | Lists falling sensitivity and stronger stabilising feedbacks among the candidate causes of declining extinction; qualitative |
| Green, Renne & Keller 2022 PNAS | 10.1073/pnas.2120441119 | abs (Claude); full (scout) | LIP–extinction correlation is unlikely by chance and stronger at higher eruptive rates. Pooled across all ages; no era term |
| Henehan & Witts 2023 PNAS (letter), with Green's reply | 10.1073/pnas.2303700120; 10.1073/pnas.2304194120 | meta (Claude); full (scout) | "Continental flood basalts do not drive later Phanerozoic extinctions". The reply tests timing only |
| Wang & Bush 2008 Paleobiology | 10.1666/07060.1 | abs (Claude) | Class-level susceptibility "has generally declined through the Phanerozoic"; rates adjusted for it. No independent forcing |
| Pohl et al. 2023 Sci Adv | 10.1126/sciadv.adg7679 | abs (Claude) | Model: early Palaeozoic susceptibility 10× higher from climate and continental configuration; holds at present-day pO₂ |
| Stockey et al. 2021 PNAS | 10.1073/pnas.2101900118 | full (scout) | Model: response to 5 °C warming depends on pO₂ |
| Li et al. 2021 Geochem Persp Lett | 10.7185/geochemlet.2137 | full (scout) | 41 events: extinction against a δ13C turbulence index (R² 0.835 for 31); Cambrian–Silurian outliers |
| Bachan et al. 2017 Am J Sci | 10.2475/06.2017.01 | sect (scout) | Carbon-isotope excursion amplitude declines through the Phanerozoic |
| Song et al. 2021 Nat Commun | 10.1038/s41467-021-25019-2 | full (scout) | ΔT–extinction across 45 bins of about 10 Myr; no secular term |
| Gilinsky 1994; Foote 2000 Paleobiology | 10.1017/s0094837300012926; 10.1666/0094-8373(2000)026<0578:oaecot>2.0.co;2 | abs; full (scout) | Declining rates partly from loss of high-turnover taxa; no partition computed |
| Bond & Wignall 2014 GSA SP 505 | 10.1130/2014.2505(02) | abs (scout) | LIP volume does not track extinction; gas-release rate matters |
| Sudakow et al. 2026 Nat Commun | 10.1038/s41467-026-75655-9 | full (scout) | Vulnerability index from diversity and turnover. Proposes, as future work, comparable stressors applied to different background states |

**Disposition.**
- The forcing-versus-response framing is stated in words and live: Clapham &
  Renne versus Green, with Henehan & Witts's reply.
- The composition side is partly quantified, without forcing (Wang & Bush).
- The geography side is modelled (Pohl).
- Not found: per-unit-forcing sensitivity with a time term, and a
  between/within-clade partition of its change.
- The binding gate is the number of post-Jurassic events with forcing estimated
  independently of extinction (Green's reply notes that high-eruptive-rate LIPs
  are rare in this interval).
- Tier stays 2. It is a live dispute about identification (lesson 4), which
  argues for keeping it, but it is limited by event count (lesson 1).
- Not read: Ridgwell & Zeebe-era carbonate-buffering model papers, which may
  already contain the forcing-side pulse experiment.
