# Barry's provocation: John Alroy's corpus and the PBDB literature as a blue-sky seam

Claude | 23 October 2026 | Prompted by Barry in Claude chat (exact words):
"I think this fits mostly with the blue-sky work, and might help expand the
range of questions posed in this section. That is the work of my close
colleague John Alroy … See what you think!"

**Status: proposals for Codex's antagonistic review.** Nothing is registered
yet. 

## Sources read

- **John Alroy's Google Scholar profile** (Professor, Macquarie University;
  12,472 citations, h-index 50; about 170 items, read on 23 October 2026).
- **The Paleobiology Database's Scholar profile** (110,826 citations; its
  top 100 papers read).
- **Targeted prior-art searches** on each candidate below (sources at the
  end).

**A correction to the premise.** The PBDB was not built from Benton's *The
Fossil Record*.
- It grew out of the NCEAS-funded Phanerozoic Marine Paleofaunal Database
  initiative (August 1998 to August 2000), founded by John Alroy and Charles
  Marshall.
- The working group included Sepkoski, Jablonski, Raup and Foote. It was
  motivated by the limits of range-based compendia such as Sepkoski's, and
  so built **occurrences in collections**, the design that made sampling
  standardisation possible.
- The database was at NCEAS from 2000 to 2010, with NSF funding from 2000
  to 2015. It is now at the University of Wisconsin–Madison, under CC BY.

## What the corpus says about our registers

Much of John's territory is **already in our registers**. That is
independent support for the programme's choices, not redundancy to remove:

| Alroy thread (Scholar items) | Our entry |
| --- | --- |
| Equilibrial dynamics, diversity limits (1996, 1998, 2008 PNAS, 2010 Science, 2016 PLoS Biol, 2018 Ecol Lett, 2019 NEE) | Q-044, B-005, B-014 |
| Sepkoski's faunas: coherence and a shifting balance (2004 EER, 2010 Science) | Q-039 |
| Phanerozoic marine diversity and its estimators (2001 PNAS, 2008 Science, 2010, 2018 MEE, 2020) | Q-040, Q-045 |
| Escalation trends are statistically independent (2006 Science) | B-003 |
| Community energy use (2022–2025) | Q-046, B-011 |
| Mammalian dispersal at the PETM (2002 Science); stochastic migration (1996) | Q-047 |
| Rate estimators: three-timer, gap-filler, Bayesian extinction (2008, 2014, 2015, 2016) | Q-004, Q-012 and Q-038 support |
| Abundance distributions, evenness (2015 Sci Adv, 2025 Ecol Lett) | B-015 |

The PBDB list's headline papers map onto our registers in the same way:
- Song et al. 2021 → Q-003;
- Penn et al. 2018 → Q-001;
- Payne & Finnegan 2007, Harnik et al. 2012 → Q-016 and Q-020;
- Zaffos et al. 2017 → Q-029;
- Kiessling et al. 2010 → B-010;
- Silvestro et al. 2015 → B-014;
- Condamine et al. 2020 → B-006;
- Mayhew et al. 2012 → Q-019 and B-018;
- Jablonski et al. 2013 → Q-027;
- Smith et al. 2018 → Q-031 and Q-037.

## Four new candidates (blue-sky), and two amendments

### C1. Is taxonomic practice a hidden macroevolutionary variable?

**Question.** How fast do fossil names die (synonymy, *nomen dubium*,
reassignment)? Does the rate differ predictably by clade, era, body size,
preservation and author community? And how much of the apparent signal in
origination and extinction, diversity and body-size trends does it carry?

- **Alroy anchor:** "How many named species are valid?" (2002 PNAS, 222
  citations) estimated the invalid share of North American mammal names
  from their revision histories. "Taxonomic inflation and body mass
  distributions" (2003) showed the error is not neutral with respect to
  traits.
- **What is new:** the PBDB now stores **dated taxonomic opinions** across
  all clades. A name's revision history is therefore data. A survival model
  for names, with the risk of being invalidated as a function of age, clade,
  rank, decade described and occurrence count, can be fitted across the
  whole database.
- **The payoff:** an expected-validity weight for every name, propagated
  into rates and curves. It would also give a **prediction**: which current
  names are likely to be synonymised, a forecast testable against future
  PBDB revisions.
- **Prior:** clade-specific sensitivity tests exist (a 2025 ostracod study
  that randomly synonymised species; Wagner and colleagues on taxonomic
  standardisation and genus-assignment error, 2006–07, PMC1702387; a 2022 bryozoan comparison of revised and unrevised PBDB data). I
  found no cross-clade synonymy-dynamics model.
- **Cheapest disposition-changing check:** pull the PBDB opinions table for
  two well-curated clades and one poorly curated clade. Measure the
  invalidation hazard against name age.
  - If the hazard is flat and small, the question collapses into a
    correction factor and goes to park.
  - If it is large and structured by clade or trait, develop.
- **Prior missed in the first pass:**
  - Benton 2008 (*Paleobiology* 34: 516–533) estimated about 40% error at
    genus level and 50% at species level across the history of dinosaur
    naming.
  - There is an Alroy–Benton methods exchange on the "flux ratio" estimate
    of eventual valid names (Alroy 2002; Alroy 2011 *Paleobiology*).
  - So this is occupied clade by clade. The novelty has to be the
    cross-clade model, its propagation into rates and curves, and the
    forecast.
- **Cheapest check, run 23 October** (`data/c1-name-survival-check/`;
  public PBDB API, genus names, recorded opinions):

  | Clade | Genus names | Invalid now | Median years to invalidation (invalid names) | Still valid after 50 y | After 100 y | Invalid share by description era (pre-1900 / 1900–49 / 1950–89 / 1990+) |
  | --- | ---: | ---: | ---: | ---: | ---: | --- |
  | Bivalvia | 3,823 | 10.9% | 74 | 0.96 | 0.90 | 14 / 12 / 9 / 5% |
  | Brachiopoda | 3,551 | 10.9% | 25 | 0.90 | 0.85 | 13 / 13 / 12 / 6% |
  | Trilobita | 4,021 | 15.1% | 37 | 0.89 | 0.81 | 21 / 18 / 15 / 8% |
  | Mammalia | 8,900 | 20.0% | 48 | 0.88 | 0.78 | 34 / 25 / 14 / 4% |
  | non-avian Dinosauria | 2,313 | 19.8% | 19 | 0.76 | 0.63 | 45 / 37 / 33 / 9% |

  **What this means:**
  - **The hazard is not flat or small.** A century after description,
    between 10% (bivalves) and 37% (non-avian dinosaurs) of genus names
    are invalid. The timescale also differs by clade: a median of 19 years
    to invalidation in dinosaurs against 74 in bivalves.
  - **Recently described names have had less time to fail,** and recent
    description is concentrated in some clades and intervals. So a
    time-varying "taxonomic maturity" bias in diversity and rates is
    plausible. **That is the question, not yet a result.**
  - **The PBDB's recorded opinions under-record revisions.** Non-avian
    dinosaur genera are 20% invalid here against Benton's 40%. Any model
    would need a correction for recording lag.
  - **An artefact excluded:** for a synonym, the API's `n_occs` is the
    senior taxon's count, so occurrence-based breakdowns are not used.
  - **Disposition implication:** the stated collapse criterion (flat and
    small) is not met. My recommendation is develop, subject to Codex.
- **Provisional:** I = M–H, T = H (data in hand), V = M–H (it touches every
  PBDB-based estimate).

### C2. What makes Cope's rule: drift within lineages or sorting among them, and why does the answer differ between clades?

**Question.** In North American mammals, size increase arose **within
lineages** (Alroy 1998 Science, 637 citations). Across 17,208 marine animal
genera, Heim et al. (2015 Science) attribute it to **differential
diversification among classes**. Is the mechanism set by metabolism,
ecology, taxonomic level or sampling grain?

- **What is new:**
  - body-size compilations now exist for marine genera, mammals and
    dinosaurs;
  - occurrence-based ranges come from the PBDB;
  - a Price-equation or multilevel decomposition separates the
    within-lineage, sorting and extinction-selectivity components on the
    same footing for every clade.
- **Distinct from** Q-031 (shrinking under warming) and B-015 (stability of
  macroecological distributions), though it shares Q-031's machinery.
- **Cheapest check:** a prior check for any cross-clade decomposition after
  Heim et al. 2015. If one exists, the question narrows to its unexplained
  residual. Then decompose two clades at matched taxonomic level (genera
  of mammals and of marine bivalves).
- **Prior check, run 23 October.** The mechanism is already known to vary,
  studied clade by clade:
  - North American mammals: within-lineage increase of 9.1% (Alroy 1998),
    or turnover by larger close relatives (Raia et al. 2012, *Am Nat*);
  - Triassic therapsids and archosauromorphs: within-lineage increase
    "extremely rare", with passive diffusion dominant (Sookias, Butler &
    Benson 2012);
  - marine animals: differential diversification among classes (Heim et
    al. 2015);
  - Mesozoic birds: a methods dispute.

  Theory now predicts *where* each pattern should occur. Roy, Brännström &
  Dieckmann (2024, *Communications Biology*) predict Cope's rule under low
  extinction risk and weak interference competition, recurrent episodes
  when top predators face high extinction risk, and the inverse rule under
  strong interference competition. They name empirical cases only as
  future tests. I found no cross-clade synthesis.
- **Reframed question:** do the ecological determinants the theory names
  (clade extinction rate from PBDB occurrences; interference proxies)
  predict where Cope's rule appears, fails or inverts across fossil clades?
- **Cheapest next check:** tabulate published clade-level outcomes (about
  15–30 clades) with their mechanism class. Ask whether PBDB-estimated
  extinction rates separate the clades with the rule from those without.
- **Provisional:** I = H, T = M, V = M, with occupancy partial.

### C3. Calibrate the instrument on the present: how much does database aggregation flatten deep-time gradients?

**Question.** Composite occurrence databases attenuate macroecological
gradients that systematic field data recover. Kerr, Currie, Kosnik & Alroy
(2025 Ecography) show this for latitudinal richness in Australian marine
bivalves, with observation-based records obscuring the gradient. Can the
attenuation be **measured on modern systems**, where field truth exists,
and used to correct the deep-time latitudinal and environmental gradients
built from PBDB-type aggregates?

- **The payoff:** the deep-time debate over flattened gradients in
  greenhouse intervals (relevant to Q-027) may be partly an artefact of
  aggregation. An attenuation factor with an uncertainty would say how much.
- **Prior:** the 2025 modern comparison exists. I found no transfer of it to
  deep time.
- **Cheapest check:**
  - Aggregate a modern, well-surveyed system (Australian bivalves, which
    John's group has already assembled) through a PBDB-like filter: lists,
    reference structure, lumping of localities.
  - Measure how much the gradient is attenuated.
  - Only if the attenuation is large does the deep-time correction become
    a question.
- **Composite half run on 23 October** (`data/c3-attenuation-check/`).
  - OBIS bivalves along eastern Australia at 11–37° S: 59,488
    species-level records.
  - Rarefied richness falls only about 7–10% over 10° southward, and
    observation-based records reverse the gradient. The specimen subset
    (35,489) matches the 2025 paper's OBIS composite (36,226).
  - The field half is pending: the CC0 Dryad file needs a browser download
    with Barry's approval. The attenuation factor follows from it.
- **Provisional:** I = H, T = M–H, V = H. The value is high because it bears
  on Q-027, Q-040 and every gradient result.

### C4. How synchronous are "global" appearance events, and what does diachrony reveal about dispersal through time?

**Question.** Biochronology and most event analyses assume first appearances
are near-synchronous. Is the diachrony of first appearances predictable
from palaeogeographic distance and barriers? Does it give a Phanerozoic
time series of **dispersal speed**, and does that speed change around
crises and interchanges?

- **Alroy anchors:**
  - "Diachrony of mammalian appearance events" (1998 Geology);
  - appearance event ordination (1994 Paleobiology);
  - conjunction biochronology (1992).
- **Prior:** regional case studies only. Planktonic foraminifera are
  strongly diachronous; the nannoplankton Probable Datum Method separates
  sampling offset from true diachrony; Miocene micromammals show rare
  synchrony; trilobite dispersal increased in the Early Ordovician. No
  global quantification found.
- **Links:**
  - B-007, whose null is clustering produced by stratigraphic architecture;
  - Q-047 (when biotas meet);
  - Signor–Lipps assumptions throughout the programme.
- **Cheapest check:** for one well-dated interval with dense records
  (Cenozoic planktonic foraminifera or Neogene mammals), estimate how far
  sampling offset alone, under a PDM-type correction, explains the spread
  of first appearances in space. If it explains almost all of it, park.
- **Provisional:** I = M–H, T = M, V = M.

### Amendments rather than new entries

- **Q-047 (when biotas meet): add John's multispecies overkill mechanism**
  (2001 Science, 809 citations).
  - A novel predator, sustained by abundant alternative prey, can drive
    large, slowly reproducing prey to extinction. That yields a testable
    **selectivity signature** after deep-time predator arrivals
    (interchanges, nekton and durophage radiations), distinct from
    competitive displacement.
  - Barry's own Quaternary expertise makes this the place to transfer the
    model, not a new Quaternary entry. The programme's deep-time focus
    stands.
- **Q-040 and Q-045 (diversity estimands; robustness): add John's estimator
  critiques.**
  - These are "How should we estimate diversity…" (2018 MEE), "On four
    measures of taxonomic richness" (2020 Paleobiology) and "Coverage-based
    rarefaction fails to quantify relative species richness". Its Dryad
    dataset is dated May 2026; it reports large over- and under-estimation
    and near-random values for singleton-matched pairs.
  - SQS-type coverage standardisation underlies most published PBDB
    curves, including John's own, so whether headline conclusions survive
    under the alternative estimators is a direct robustness test for Q-045.

## A tool, not a question

**A synthetic Phanerozoic benchmark.**
- **What it is:** a simulated biosphere with known truth (species,
  occurrences, collections, taxonomic error and aggregation), sampled
  through PBDB-like filters.
- **Who it would serve:** C1, C3 and the amendment to Q-040 and Q-045 above,
  plus B-005 and B-007.
- **Precedent:** John's 2018 discovery-curve method is the empirical
  analogue.
- It would be programme infrastructure, worth building only if two or more
  of these move to develop.

## Recommendation

- **Put C1 and C3 first for Codex's review.** Both have cheap checks that
  can change their disposition, data already in hand, and the clearest role
  for John. Both also improve the instruments that the rest of the
  programme relies on.
- **C2 is scientifically the most interesting,** but needs a proper prior
  check before any work.
- **C4 is a reasonable hold.**
- **The two amendments should go in regardless.**

## Sources

- [Paleobiology Database (Wikipedia)](https://en.wikipedia.org/wiki/Paleobiology_Database); [re3data record](https://www.re3data.org/repository/r3d100010760)
- [Heim et al. 2015, Cope's rule in the evolution of marine animals](https://works.swarthmore.edu/fac-math-stat/166)
- [Kerr, Currie, Kosnik & Alroy, regional databases versus field data (Dryad)](https://datadryad.org/dataset/doi:10.5061/dryad.p5hqbzm03); [preprint](https://authorea.com/users/763528/articles/740917-regional-databases-demonstrate-macroecological-patterns-less-clearly-than-systematically-collected-field-data)
- [Coverage-based rarefaction fails to quantify relative species richness (Dryad)](https://datadryad.org/dataset/doi:10.5061/dryad.pg4f4qs50)
- [Wagner and colleagues, effects of taxonomic standardisation (PMC1702387)](https://pmc.ncbi.nlm.nih.gov/articles/PMC1702387)
- [Cyprideidae taxonomic-inflation test, Palaeontologia Electronica 2025](https://palaeo-electronica.org/content/2025/5732-evolutionary-dynamics-of-cyprideidae)
- [Roy, Brännström & Dieckmann 2024, Ecological determinants of Cope's rule and its inverse](https://pmc.ncbi.nlm.nih.gov/articles/PMC10796397)
- [Raia et al. 2012](https://www.nowdatabase.org/static/now/pdf/Raia_etal_AmNat2012.pdf); [Alroy 1998](https://pdodds.w3.uvm.edu/files/papers/others/1998/alroy1998a.pdf)
- [Kerr et al. 2024 preprint, Field data reveal strong latitudinal gradients in Australian marine bivalves](https://essopenarchive.org/users/726878/articles/709076-field-data-reveal-strong-latitudinal-gradients-in-australian-marine-bivalves)
- [Benton 2008, How to find a dinosaur, and the role of synonymy in biodiversity studies](https://www.cambridge.org/core/journals/paleobiology/article/abs/how-to-find-a-dinosaur-and-the-role-of-synonymy-in-biodiversity-studies/BD633A34515CF0FC4E4ED9F540A43CD0)
- [PBDB occurrence and opinion API documentation](https://dev.paleobiodb.org/data1.2/occs_doc.html)
- [Probable Datum Method (Schueth et al. 2014)](https://www.clima.psu.edu/bib-items/Schueth2014-ps.html)
- [Models of historical biogeography and continental biochronology](https://ojs.uv.es/index.php/sjpalaeontology/article/view/17847)
