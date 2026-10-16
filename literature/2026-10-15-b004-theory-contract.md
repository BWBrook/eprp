# B-004: burrowing, chemical memory and the limits of establishment

Codex, 15 October 2026. First paper contract; source inspection and proposed
choices are separated below. No numerical model, fit or historical
calibration has been run. Companion [response and ownership record](../ideas/2026-10-15-b004-contract-and-q012-amendment-closure-codex.md).

**Disposition: hold (support), updated 16 October.** Generic colonisation
feedback is already proposed in the closest prior, and sediment chemistry can generate
hysteresis without animals. The narrower question is whether endogenous
burrowing changes the oxygen conditions for establishment and persistence
*relative to that chemical memory*, and whether the change is consequential
under independently defended biological constraints. Its sign is open.
Novelty of this residual remains unverified. A conditional modern model
result would not by itself explain Palaeozoic colonisation.

**Same-day amendment after Claude's critique:** the
[modern source table and control check](2026-10-15-b004-modern-source-table.md)
is complete. A modern *Arenicola marina* prototype is on support hold because
the demographic/transport coupling is not independently closed. The
conditional theory question initially remained develop; no numerical
implementation was allocated. Modern recovery times, spatial front selection and demographic
equilibrium thresholds remain separate targets.

**16 October analytic close:** the [bounded calculation](2026-10-16-b004-coupling-boundaries.md)
shows that smooth communal transport vanishing at zero biomass leaves rare
invasion unchanged relative to matched passive fauna. Resident folds can
move, but their direction requires the projected chemical/demographic
response, and consequential size needs independent scales and input bounds.
B-004 is now on support hold; the calculation does not establish historical
consequence or exclude other engineering mechanisms.

## 1. What the nearest primary studies already occupy

Sources checked 15 October 2026. The original contract's bounded orientation was not a
systematic review: two nominated mechanistic families (GCA 2020 and Nature
Communications 2018), two historical families (Buatois and Bubphamanee 2025),
and one directly relevant follow-up (PNAS 2020) that changes the comparator.
Discovery used DOI/title web searches and primary author/publisher repositories;
the mechanistic search included “bioirrigation alternative stable states sediment
oxygen fauna hysteresis colonization persistence model”. Stop after these
families and their available supplements; no new section catalogue.

| Source and access depth | Direct source result or proposal | Consequence for B-004 (our inference) |
| --- | --- | --- |
| van de Velde et al. 2020, GCA 276:31–49, [DOI](https://doi.org/10.1016/j.gca.2020.02.021), [accepted manuscript](https://www.vliz.be/imisdocs/publications/357157.pdf). Full text/Appendices 1–4; §4.3, printed pp. 27–28, lines 658–695, Fig. 8; Appendix 1 | Explicitly proposes sulphide exclusion, reduced faunal activity and weaker Fe recycling; a temporary fall in organic input permits invasion and subsequent detoxification. The 14-state sediment model prescribes mixing and irrigation. No animal recruitment/biomass equation. | Colonisation facilitation and alternative animal-associated sediment states are conceptually occupied. The numerical demographic threshold contrast remains untested in this source. |
| van de Velde et al. 2020, PNAS 117:33043–33050, [DOI](https://doi.org/10.1073/pnas.2008235117), [author main text](https://reinhard.gatech.edu/uploads/5/4/1/0/54106417/vendevelde_pnas_2020.pdf), [publisher SI](https://www.pnas.org/doi/suppl/10.1073/pnas.2008235117/suppl_file/pnas.2008235117.sapp.pdf). Main mechanisms; SI §§2, 3, 5 and Figs. S2–3 | Coupled Fe/S chemistry produces alternative states. SI p. 11 sweeps reactive carbon input up/down at fixed Fe input and oxygen boundary; p. 24, Fig. S3b shows greater prescribed **particle mixing** narrows the bistability interval, which exists at zero mixing. | The comparator must retain chemical memory. This result concerns a carbon/iron forcing contrast, not an oxygen threshold or a demonstrated irrigation effect. |
| van de Velde et al. 2018, Nature Communications 9:2554, [DOI/publisher](https://doi.org/10.1038/s41467-018-04973-4). Full Methods, Eqs. 1–6; SI Notes 1–3 | Global C/O/P/S burial feedback from prescribed bioturbation can reduce oxygen and expand anoxia. Optional anoxia suppression modifies imposed faunal history. No local animal recruitment model. | Local sediment detoxification and global oxygen depletion can coexist. A local result cannot establish a favourable global effect or explain its timing. |
| Buatois et al. 2025, [DOI](https://doi.org/10.1073/pnas.2414752122), [full main text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11874251/). Main Methods/Results/Discussion via Europe PMC XML; SI uninspected | Compiles 720 Ediacaran–Devonian slope/basin units, 147 trace-bearing, at series resolution; poorly dated occurrences enter every spanning series. Discusses open-burrow porewater ventilation. Metrics are ichnogenera, architecture and function. | Supports a historical motivation and setting; architecture is not pumping rate or biomass. Pooled rises/declines do not establish same-forcing invasion/collapse thresholds. |
| Bubphamanee et al. 2025, [DOI](https://doi.org/10.1073/pnas.2501342122), [author deposit](https://authors.library.caltech.edu/records/gnj9m-qfv49). Main pp. 2–4/Fig. 2, full small SI, S1/S2 schema and selected rows | Selenium records regional oxyanion supply and local porewater reduction. New 97-sample/31-unit data include shelf/upper-slope settings; a 420–394 Ma gap limits transition timing. | Se adds evidence beyond traces, but independence from faunally modified porewater cannot be presumed. It is not a paired oxygen/colonisation history. |

The PNAS mechanism is particularly consequential: FeS precipitation removes
iron from reoxidation, weakening FeOOH regeneration and promoting further
sulphate reduction. It supplies a history-dependent chemical rival before
animal feedback is added. Its reduced equations (SI pp. 16–17, Eqs. 17–26)
make FeOOH dynamic while other species are quasi-steady. That reduction
assumes low fixed oxygen, abundant sulphate and complete carbon consumption;
it is not automatically valid over a wide oxygen sweep. Choosing reduced
versus spatial chemistry is a later applicability decision.

## 2. Proposed target and physical boundary

Start with one sediment patch and an explicit engineer guild, in a declared
continental-margin/slope setting. Force it with bottomwater oxygen `q`,
reactive carbon and iron inputs, sulphate, temperature and sedimentation.
Keep the external conditions `u` fixed for each comparison. These are
**proposed choices**, not reconstructed ancient trajectories.
This local endpoint does not itself describe connected landscape colonisation.

Separate particle mixing `D_b` (area/time) from nonlocal dissolved exchange
`alpha_i` (1/time). The latter exchanges porewater with bottomwater, with
solute-specific transport if justified. Irrigation redistributes available
oxygen; include animal respiration, microbial oxidation and reduced-product
export in the budget. An imposed oxygen boundary represents an externally
supplied reservoir. Record its oxygen demand; a finite-water-reservoir
extension must pay that demand explicitly. No inference of survival in
anoxic bottomwater follows from a ventilation coefficient.

Let `C` be the chemical state and `B` engineer biomass/activity. The generic
coupling is a bookkeeping template, not an implemented model:

```text
dC/dt = chemical reactions and transport(C; q, u, D_b(B,C), alpha(B,C))
        + the same explicitly budgeted animal metabolic terms in every rival
dB/dt = recruitment/growth(B,C; q,u) - mortality(B,C; q,u).
```

The demographic law must declare whether recruits are locally generated or
externally supplied larvae. Do not impose separate establishment and collapse
cutoffs, or an unsupported positive-density effect, to obtain hysteresis.
Recruitment limitation, avoidance and oxygen/sulphide physiology need evidence
independent of the target contrast. Positive engineer biomass is the initial
endpoint. A claim about other benthos needs a separately defined recipient
guild and viability criterion; chemical improvement alone is insufficient.

## 3. Establishment and persistence are different tests

For each rival `m`, forcing `(q,u)` and stable unoccupied chemical branch `k`:

1. **Establishment:** calculate the rare-colonist invasion exponent
   `E_mk(q,u)` about `B=0, C=C_0k`. In a scalar population equation this is
   the per-capita growth limit; a staged population requires its invasion
   eigenvalue. Zero immigration defines this mathematical test. With an
   external larval supply, report a separate finite-propagule establishment
   experiment and observation window; an absorbing `B=0` is not evidence
   that colonisation is impossible.
2. **Persistence:** find and test local stability of a positive resident
   equilibrium under the **same** `(q,u)`. State the perturbation and branch
   followed; a long transient is not a stable resident state.
3. Report the oxygen set
   `A_mk(u) = {q: E_mk(q,u)<0 and a stable B*>0 exists}`. Preserve multiple
   unoccupied chemical branches rather than choosing only the one that
   maximises the contrast. Occupied and unoccupied basins/initial histories
   are part of the result.

Only if the branches have the required ordering should this be reduced to
`q_est - q_loss`. Report both boundaries and their directions. If useful,
define `W_mk` as the total length of `A_mk` inside a predeclared oxygen
domain, in oxygen units, alongside the actual sets/branches. Disconnected
intervals must not be represented as one threshold gap.
Across rivals match declared initial histories, not arbitrary branch indices;
if branch topology differs, report that difference rather than subtracting
unmatched branches.

The animal-feedback contrast is the change in `A`, boundaries and `W`
against the matched rivals below. A larger window is not automatically a
benefit: it could reflect harder establishment; a smaller window could
reflect easier establishment. Separate the level of tolerable oxygen from
the magnitude of history dependence. This first contract concerns stable
equilibria; oscillatory states or dispersal networks would require a revised
target, not a universal conclusion from an equilibrium-only failure.

## 4. Matched rivals and discriminating controls

| Comparator | Retained structure | Purpose |
| --- | --- | --- |
| Chemical baseline | Full relevant Fe/S/organic chemistry, zero animal mixing/irrigation, alternative initial chemical states | Establish intrinsic chemical multistability. It has no animal persistence endpoint and is not alone the denominator for an animal effect. |
| Passive-fauna rival | Same chemistry plus the same demography, respiration and other declared non-transport animal effects; no animal-induced mixing/irrigation | Gives a comparable invasion/persistence outcome when burrowing transport is absent. Do not erase chemical memory or animal costs. |
| Fixed-transport rival | Same chemistry/demography with externally prescribed mixing and/or irrigation profiles, fixed before outcome inspection | Separates transport level from feedback through animal abundance/activity. Match a predeclared reference regime; do not tune a different favourable profile at every transition. |
| Coupled mixing, coupled irrigation, both | Same chemistry/demography; change only the stated transport dependence on animal state | Determines which transport mechanism changes the boundaries. Prescribed mixing results cannot be relabelled as irrigation evidence. |
| Demographic and rate rivals | Any independently justified Allee/recruitment structure shared across rivals; finite-rate forcing sweeps alongside constant-forcing solutions | Tests non-engineering population thresholds, chemical relaxation and dispersal/observation lags. |
| Independent modern benchmark, if matched | Separately measured forcing and the same organism/endpoint, with the relevant transport and demographic setting | Tests biological applicability; slow physiological or community recovery alone does not verify equilibrium hysteresis. |

Compare coupled transport with **both** passive fauna and fixed transport;
keep parameter values, external forcing, metabolic costs and observation
rules common. If fixed transport already produces the same change, that
supports a transport effect but not a necessity for endogenous feedback.
Externally maintained transport is a diagnostic intervention, not a claim
that an unoccupied ancient patch sustained animal pumping.
If chemical history or demography alone produces the loop, observing the
loop in a coupled model does not attribute it to engineering.

A claim about spread along connected slopes additionally needs a biologically
justified spatial applicability check. Declare dispersal, finite founder
size, source boundaries, heterogeneity and time horizon. Front speed and
pinning may be appropriate outputs; a unique Maxwell point is not guaranteed
for arbitrary coupled chemistry and nonlocal recruitment. Finite-front
dominance differs from the existence and local stability of two uniform
equilibria. The current patch contract does not commission a spatial model.

Required computational checks, if a later bounded implementation is justified:
mass balance/units; recovery of the declared chemical baseline; turning off
each coupling; stability and return after perturbation; constant-forcing
convergence from both histories; slower forcing protocols; and numerical
resolution adequate for boundary positions. A rate-dependent loop that
vanishes in the slow/steady limit is reported as lag. Retain such a result,
but do not label it equilibrium bistability. No calculation in this note
has performed these checks.

## 5. Input readiness: source anchors are not a joint ancient envelope

| Input | What has actually been secured | Missing before a defensible test |
| --- | --- | --- |
| Chemical reactions and transport | GCA Appendix 1; PNAS main/SI and [author repository](https://github.com/sevdevel/PNAS2020), README/file listing inspected only | Applicability to a chosen low-oxygen regime; exact version, units and reaction audit before reuse; no execution verified |
| Modern boundary/transport anchors | GCA Table A1.3: O2 0.28 mol/m³ (280 µM), sulphate 20 mol/m³, 10°C, mixing depth 15 cm, D_b 10 cm²/year; irrigation depth 10 cm and alpha 1.2/year calibrated from ammonium | These are modern oxygenated salt-marsh values, including calibrated/imposed coefficients. Need jointly plausible ranges and architecture-to-flux mapping for the selected setting |
| Population and physiological coupling | None of the three inspected mechanistic papers supplies endogenous animal recruitment, mortality or biomass dynamics | Independent recruitment, respiration, sulphide/oxygen responses and activity costs; allowable covariance with transport and body size |
| Ancient forcing and states | Trace architecture categories; regional/local redox evidence in separate compilations | Co-located chronology, water-column boundary evidence independent of altered porewaters, organic/Fe inputs, occupied/unoccupied histories and preservation model |
| Consequence scale | No justified numerical oxygen-width or population-viability margin yet | Predeclare a biologically meaningful boundary shift/width and numerical tolerance before inspecting outputs; a statistically detectable or nonzero change is insufficient |

Do not sample independently from convenient literature min/max ranges and
call that historical support. Transport, sediment texture, animal size,
metabolism and recruitment may covary. Distinguish measured, calibrated,
assumed and transported coefficients. A broad numerical sweep could show
possibility conditional on its inputs; it could not supply those inputs'
independent justification.

The [six-study modern screen](2026-10-15-b004-modern-source-table.md) now
supplies activity, adult respiration, seasonal recruitment and solute
advection anchors, but no jointly supported population/transport closure.
Acute anaerobic onset is not a mortality cutoff, and mass-specific pumping
does not by itself specify alpha(B) or particle D_b(B). The guild's IQR of
physiological thresholds is not a necessary minimum demographic effect;
use a defended consequence margin before model outputs, with uncertainty
and numerical tolerance stated separately.

## 6. Finite decision and stopping contract

- **Bounded analytic product complete, 16 October:** invasion invariance,
  the fold response, sufficient sign conditions and exact counterexamples
  are recorded in the linked note. Reopening requires a supported joint
  closure and consequence scale, or a distinct theoretical target. No
  further sign-only exercise or numerical prototype is allocated.
- **First source product complete:** the modern *Arenicola marina*/shallow
  sand table reaches a support hold for an independently parameterised
  prototype. Reopening requires a source-supported stage/open-recruitment
  law and compatible activity-dependent transport closure. No further source
  sweep is allocated; a separately posed assumed-parameter theorem remains
  possible without claiming empirical calibration.
- **Proceed to a small theory prototype only if** the residual survives the
  prior comparison and the demographic/transport law, parameter support,
  meaningful effect margin and matched controls can be stated without using
  the desired hysteresis to tune them. Prefer reuse of a suitable published
  chemical core; a repository listing does not yet select an implementation.
- **Consequential positive:** a defensible range gives a boundary/asymmetry
  change beyond the declared margin relative to both relevant rivals, with
  its direction and dependence documented. This remains conditional theory.
- **Consequential negative:** a justified bound or adequately resolved
  exploration of the **declared admissible domain** excludes a change of
  the stated size, or exposes an unavoidable opposing budget. A handful of
  failed runs, solver failure or an undefended parameter box does not qualify.
  Such a result can retire that mechanism/domain's historical route, not all
  burrowing effects in deep time.
- **Hold or park:** if only unsupported demographic feedback produces the
  asymmetry, or the residual is already answered by a closer quantitative
  prior, stop before an empirical programme. If inputs simply remain unknown,
  report a support hold rather than a biological negative.
- **Historical follow-up only after a useful theoretical result:** inspect
  a finite set of candidate sections for the required joint forcing and
  colonisation/persistence contrast. No broad record compilation now.

## 7. Access and provenance limits retained

Source PDFs, XML and detailed scouts are in ignored
`scratch/b004-mechanisms-20261015/` and `scratch/b004-history-20261015/`.
They are working copies, not a distributed data product. Stable source
links and the decisive locators above support the contract without relying
on those local files. No raw values were changed.

The GCA author portal PDF returned 403; VLIZ supplied the accepted manuscript.
The 2018 linked ResearchGate data page offered no downloadable file, so that
exact code/data version remains unverified. The PNAS 2020 repository was
listed, not run. Buatois main text was retrieved through
[Europe PMC XML](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11874251/fullTextXML)
after direct-access failures; its 72 MB supplement was deliberately left
uninspected. Underlying section-level support therefore remains open.

Bubphamanee's author-deposit checksums matched for main/SI/S1/S2 (MD5,
respectively `aaf7c4be5d2efff2655195b97d29d0a0`,
`68ce12d3048e1450b5b818a5d4ac8976`, `86f947f4df41895bdeaf46d2245bc6e9`,
`4716169b09c81ea74cd433fa16f32fe3`). Selected chronology conflicts were
preserved: SI/Table S1 versus S1 data gives Esopus 402–398 versus 394 Ma,
Schaghticoke 486.9–477.1 versus 475 Ma, and Hartfell/Dob's Linn 443.8 versus
Hartfell 438 Ma. No harmonisation or causal joint panel was attempted.

**Complete:** first theory/prior contract, response to critique, bounded
modern source table and analytic boundary check. B-004 is on support hold.
**Provisional:** residual novelty, model choice, parameter support and any
historical explanatory value. **Next responder: Claude**, before a further
bounded task is allocated. No primary investigation selected.
