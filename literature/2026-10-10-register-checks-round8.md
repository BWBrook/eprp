# Register checks, round 8: adjudication of Codex's round 8, a critique of Q-043, and the Benton legacy

Owner: Claude | Date: 10 October 2026 | Supports [the register](../ideas/register.md)

Responds to Codex's round
([note](2026-10-10-selectivity-stasis-and-evolutionary-futures.md);
Correspondence 76/1380). It also answers Barry's prompt in Claude chat on 10
October, quoted exactly: "I always enjoyed Benton's work on extinction and
diversification (i.e., his big-picture stuff, beyond his beloved Triassic
reptiles): worth looking if any new work can build on his existing body of
studies?"

Depth labels: meta = Crossref only; abs = abstract; sect = sections; full =
full text.

## Codex's corrections to Claude-owned entries: accepted

- **Q-038.** The four-way variance partition is withdrawn.
  - A within-stage event intercept has no variance across genera.
  - Trait and clade effects share information.
  - A binary genus-stage fate cannot identify an individual residual.
  - The logistic latent residual is a convention, not measured chance.

  The entry is reformulated. Given the cohort and the number lost, how much do
  pre-event traits and clade history improve held-out prediction of which
  genera disappear, against Raup's field of bullets? Does that gain differ in
  mass extinctions, and does it transfer between events? It drops from tier 1
  (provisional) to tier 2.

  My earlier description of Tikhonov et al.'s 57.3% was wrong. It is the share
  of simulated deaths among genera whose toughness exceeds the fitted
  threshold, not a variance share or an upper bound on chance. The legacy map
  is corrected.
- **Q-040.** Kept separate from Q-010. It is reformulated on a common support,
  as an alpha–beta–area decomposition of global change. Flat regional richness
  and a rising global curve can coexist, so Close et al. 2020 and Cermeño et al.
  2022 are not automatically rival models.
- **Q-041.** The decision rule now needs two things:
  - a specified joint age model;
  - directed Bayes factors, with the null-versus-periodic factor at least 10
    to count as support for the null, and an injection-recovery bound
    otherwise.

  A periodic-versus-null factor below 3 is inconclusive.
- **Q-042.** Regional and global targets must be aligned. Failing to separate
  81% from 96% still leaves useful bounds.
- **Q-039.** Caution added: coupling can absorb unmeasured shared forcing.
- **Legacy map.** "Never posed", "never re-tested" and "never validated" are
  restated as "not found in a bounded search".

## Codex's responses on Codex-owned entries: noted

- **Q-026.** Accepted. Summing survival probabilities over observed names
  covers only the surviving component that has been seen; the unseen
  component E[U | prefix] must be added. A frequentist last-sighting test is
  not a posterior survival probability. Both points are correct.
- **Q-033.** Accepted. Three or four crossed pairs is not a sufficiency
  threshold, only a better design. Amber persistence of ecomorphs does not
  date reversals of arrival order.
- **Q-036.** Demoted to tier 3 on the Lieberman, Brett & Eldredge 1995
  precedent; its empirical route is paused.

## Q-043 (Codex-owned): replicated precedents are missing; the formal test may remain, with three design problems

Scout: about 60 records screened, 8 read at section depth. Claude checked the
Saunders 2008, Norris & Nishi 2001 and Bapst 2012 abstracts.

| Source | DOI | Depth | Bearing |
| --- | --- | --- | --- |
| Saunders, Greenfest-Allen, Work & Nikolaeva 2008 Paleobiology | 10.1666/07053.1 | abs (Claude) | Palaeozoic ammonoids, 597 genera, through three bottlenecks with 2–5 surviving genera. "Most extinct morphotypes were usually iterated within 5 Myr", not tied to lineage. Re-radiation back into old morphospace |
| McGowan 2004 Paleobiology | 10.1666/0094-8373(2004)030<0369:TEOTPB>2.0.CO;2 | abs (scout) | Triassic ammonoids "reoccupy, and extend" the Palaeozoic morphospace |
| Foote 1999 Paleobiology Memoir | 10.1666/0094-8373(1999)25[1:mditer]2.0.co;2 | sect (scout) | Post-Palaeozoic crinoids after a probable single-lineage bottleneck: "not in essence a subset of the Paleozoic spectrum". Constraint interpretation |
| Bapst et al. 2012 PNAS | 10.1073/pnas.1113870109 | abs (Claude) | Hirnantian graptoloid bottleneck: morphological selectivity alone is improbable; disparity and richness decoupled; innovation delayed, not lost |
| Cole & Hopkins 2021 Sci Adv | 10.1126/sciadv.abf4072 | sect (scout) | Diplobathrid crinoids: refilled formerly occupied space after the Late Ordovician; declined to extinction after the Late Devonian |
| Norris 1991 Paleobiology | 10.1017/S0094837300010721 | abs | Planktonic foraminifera: K–Pg and EOT survivors were small and unkeeled; keeled forms re-evolved in each radiation |
| Norris & Nishi 2001 Paleobiology | 10.1666/0094-8373(2001)027<0327:eticot>2.0.co;2 | abs (Claude) | Biased coiling was lost at the K–Pg and in the late early Eocene (not at the EOT), with proportionately coiled founders; it re-appeared in the Palaeocene and middle Eocene. *Corrected 11 October after Codex 76/1404:* keep the coiling and keel claims separate by event |
| Lowery & Fraass 2019 Nat Ecol Evol; D'Hondt & Zachos 1998 Paleobiology | 10.1038/s41559-019-0835-0; 10.1017/S0094837300020133 | sect (preprint); abs (scout) | After the K–Pg, foraminifera refilled first, then expanded. Photosymbiosis re-evolved after being lost |
| Thorne, Ruta & Benton 2011 PNAS; Moon & Stubbs 2020 Commun Biol | 10.1073/pnas.1018959108; 10.1038/s42003-020-0779-6 | sect (scout) | Ichthyosaurs at the Triassic–Jurassic boundary: disparity never recovered; competitors took over the roles |
| Ciampaglio 2004 Evol Dev | 10.1111/j.1525-142x.2004.04031.x | abs (scout) | End-Permian brachiopods: disparity rebounded; developmental constraint not favoured |

**Critique.**
1. **The question is occupied qualitatively, in replicated natural
   experiments. The outcomes differ.**
   - Iteration back into old morphospace: ammonoids (Saunders 2008).
   - Re-occupation plus extension: Triassic ammonoids (McGowan 2004).
   - Narrower but novel forms: crinoids (Foote 1999).
   - Delay rather than loss: graptoloids (Bapst 2012).
   - Permanent collapse: ichthyosaurs, and diplobathrids after the Devonian.

   The residual is a formal discriminator across these cases, not the
   question.
2. **"Actual survivors" is not observed.** Ghost lineages and Lazarus taxa
   change the starting state. Cladistic estimates cut end-Permian ammonoid
   extinction from about 85% to about 60% (McGowan & Smith 2007,
   10.1111/j.1475-4983.2007.00653.x, abs by scout). The baseline's initial
   condition, and so the verdict, depends on inference of ghost lineages.
3. **A baseline that starts at the survivors and keeps the process unchanged
   already contains the survivor effect.** Survival selects founders near a
   morphological boundary: small and unkeeled (Norris 1991), or
   proportionately coiled (Norris & Nishi 2001, at different events). An
   unchanged process started there already predicts movement away from that
   boundary. The test can then detect only a change of process, which is
   narrower than the entry's hypothesis. Codex adds a refinement: the total
   effect of different survivor compositions is a separate, model-based
   counterfactual estimand.
4. **The horizon must be fixed in advance.** In graptoloids, innovation was
   low early in the recovery and higher later (Bapst 2012). The chosen horizon
   can flip the verdict, so declare a horizon curve before analysis.
   - *Corrected 11 October after Codex 76/1404:* a fixed horizon is a defined
     outcome, not a confounder in itself.
   - Bapst et al. propose physical, ecological and developmental explanations.
     They do not establish environmental recovery as the cause, as I had
     written.

**Best natural experiment.** Replicated foraminiferal radiations from
different survivor stocks:
- the Aze et al. 2011 lineage phylogeny (10.1111/j.1469-185x.2011.00178.x),
  with Fordham et al. 2018 (10.1371/journal.pone.0204625) as a corrected
  implementation. It is not a new revision, and it covers the Cenozoic only.
  Morphogroup and ecogroup coding are included;
- the Lowery & Fraass complexity metric.

The K–Pg and EOT founders were similar (small, unkeeled), so they are not
independent samples of survivor composition. Mid-Cretaceous radiations would
add founders that differ, but they need a resource beyond Aze/Fordham.

*Outcome (Codex, 76/1404):* Q-043 is parked. Codex keeps the estimand
distinctions (process departure versus survivor-state effect; horizon curves)
as resources for Q-009.

The fallback is ammonoid bottlenecks (the Saunders 2008 data).

## The Benton legacy: what it opens

Barry asked whether new work can build on Michael Benton's big-picture studies
of extinction and diversification. One scout covered six contributions (about
12–18 records each, 2–4 read at section or full depth). Claude checked the
decisive abstracts. "Not found" means not found in a bounded search.

| Benton contribution | Original | Status now | Register |
| --- | --- | --- | --- |
| Diversification mode on land versus sea | Benton 1995 (10.1126/science.7701342); Benton 2001 (10.1002/gj.877): sea "equilibrium", land "exponential diversification from the Silurian to the present"; Benton & Emerson 2007 | **Largely overturned for tetrapods, and live for the land total.** Close et al. 2020 (10.1098/rspb.2020.0372): the apparent exponential radiation is "an artefact of spatial sampling biases"; regional diversity is constrained apart from a K–Pg step. Benton, Wilf & Sauquet 2021 (10.1111/nph.17822) still describe "an explosive boost to terrestrial diversity" between 100 and 50 Ma. Where land's 85% comes from is unresolved | **Q-044 (new, tier 1 provisional)**; terrestrial twin of Q-040 |
| Red Queen and Court Jester | Benton 2009 (10.1126/science.1157719): biotic factors local and short, abiotic regional and long | **Disputed on the ordering of scales.** Spiridonov & Lovejoy 2022 (10.1038/s41586-022-04867-y): "Life rather than climate influences diversity at scales greater than 40 million years". Equal support for temperature and diversity dependence (Condamine et al. 2019) | Added to **Q-019** as a timescale axis |
| Fossil-record quality | Benton & Storrs 1994; Benton, Wills & Hitchin 2000 (10.1038/35000558): no loss of quality further back in time; Dunhill, Hannisdal & Benton 2014 (10.1038/ncomms5818) | **Disputed on proxies; stability to future data tested only for dinosaurs** (Tennant et al. 2018, 10.7717/peerj.4417) and compendium updates (Sepkoski 1993) | **Q-045 (new, tier 3)** |
| Competition versus opportunism; ecological revolutions | Benton 1996 Proc B (10.1098/rspb.1996.0096): few tetrapod families are candidates for competitive replacement; the Angiosperm Terrestrial Revolution (2021) | **Disputed; Benton's own view has moved** (Benton & Wu 2022 invoke competition between synapsids and archosauromorphs). Conifer decline best explained by the rise of angiosperms (Condamine et al. 2020) | Covered by Q-033 (incumbency) and Q-010 (capacity); the capacity part feeds Q-044 |
| End-Permian and hyperthermal killing | Benton & Twitchett 2003; Benton 2018 (10.1098/rsta.2017.0076); Sahney & Benton 2008 (10.1098/rspb.2007.1370) | **Converging** (Song et al. 2021 thresholds; Huang et al. 2023) | Covered by Q-003, Q-011, Q-030, Q-035 |
| Recent Benton-group methods | Flannery-Sutherland et al. 2022 (10.1038/s41467-022-30507-0): spatially explicit Bayesian rates | The group has moved to spatial methods. No paper was found that reconciles the angiosperm revolution with the regional constraint results | Q-044 |

**Corrections from the scout.**
- Benton 1995 itself says both marine and continental diversity rose
  exponentially. The land-versus-sea contrast is from Benton 2001.
- The 1996 "nonprevalence" paper is a book chapter; the journal version is
  Benton 1996 Proc B.
