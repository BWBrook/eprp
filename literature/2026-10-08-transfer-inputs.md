# Transfer-input inventory: temperature and oxygen fields by event

Owner: Claude | Date: 8 October 2026 | Status: capability reconnaissance

This note serves candidate A, as reformulated in
[the disruption note](2026-10-disruption-susceptibility.md) after
[Codex's critique](2026-10-08-codex-review-disruption.md):

> Does frozen physiological habitat loss improve held-out extinction prediction
> beyond traits plus thermal exposure?

The question was which events have *obtainable* 3D temperature and dissolved-O₂
fields for a pre-event and a peak state.

**Method.**
- One Sonnet scout screened about 50 records using Crossref, the Zenodo and Dryad
  APIs, `gh api`, Europe PMC, the Bristol palaeo site, WebSearch and WebFetch.
- Claude re-checked the decisive items: five DOIs via Crossref, and the Ying 2026
  Zenodo manifest and README variable list.
- Nothing was downloaded beyond metadata, and no model was run.
- Access depth: **mf** = file manifest, **rd** = README, **lp** = landing page.
- Science, Nature and PNAS pages returned 403, so some data statements were read
  through Europe PMC or the deposits themselves.

## Availability by event

| Event | Deposited 3D T + 3D O₂, pre and peak | Nearest obtainable route |
| --- | --- | --- |
| End-Permian, the calibration event | **Yes: endpoint climatologies (corrected 9 October).** Figshare 10.6084/m9.figshare.7357193 v1, "End-Permian Climate Change", CC0: `Penn_PTr_climate.nc` (145.6 MB) holding `Permian_temp`, `Permian_o2`, `Triassic_temp`, `Triassic_o2`, each 12 months × 54 depths × 59 lat × 119 lon. Found by Codex from the Penn 2018 data statement; the header was read, values not checked. These are the final ten years of near-equilibrium runs, not transient forcing. Our earlier "no deposit found" was a search miss: the Science page returned 403 and the paper's data statement was never read | Align coordinates and physical depth with a named 2018 or 2022 model variant |
| End-Ordovician | No | cGENIE configs (Stockey 450 Ma; Pohl et al. 2023, 10.1126/sciadv.adg7679, 440 Ma slice); FOAM temperature only (Ontiveros et al. 2023, Zenodo 10610771, CC-BY, mf) |
| Late Devonian, Capitanian, end-Triassic, Toarcian, OAE2 | No event-specific fields | Pohl 2023 cGENIE slices every 20 Myr. These are not event-aligned and would need new boundary files |
| PETM | No | Stockey 55 Ma configs; Pohl 60 Ma slice |
| End-Cretaceous, a non-thermal comparator | **Partly.** Ying et al. 2026 (Zenodo 10.5281/zenodo.18700674, CC-BY-4.0, about 0.93 GB): 3D `ocn_O2` in `fields_biogem_3d.nc`, pre-event SPIN and impact runs. The README lists only 2D surface temperature, so 3D temperature is unconfirmed and may sit in restart files (rd + mf, checked by Claude) | Download SPIN (70 MB) and main (118 MB) to confirm |
| All 109 Phanerozoic stages | **3D T, no O₂.** BRIDGE HadCM3L (Valdes et al. 2021, 10.5194/cp-17-1483-2021), two CO₂ series, 20 ocean levels, served per file from paleo.bristol.ac.uk; no licence stated | Fit for the thermal-exposure baseline. O₂ would need offline diagnosis, which would be a new method |

**Model code and metabolic-index tooling exist.**
- cGENIE-muffin, MIT licence: GitHub derpycode/cgenie.muffin, release v0.9.35 on Zenodo 7545805.
- muffingen boundary-file generator: Zenodo 7545809.
- A cGENIE-based metabolic-index ecophysiotype generator: alexpohl/cGENIE_based_metabolic_index, GPL-3.0.
- Stockey's ensemble summary: Zenodo 10.5281/zenodo.5519730, 39.5 MB `.RData`. It holds summaries, not fields; contents not inspected.

## Trait-parameter sources

| Source | Deposit | Status |
| --- | --- | --- |
| Deutsch, Penn & Seibel 2020, 10.1038/s41586-020-2721-y | GitHub cadeutsch/Metabolic-Index-Traits (`Par.mat`, `Tol.mat` and others) | No licence; contents inferred from file names only (mf) |
| Penn & Deutsch 2024, 10.1098/rstb.2022.0487 | Zenodo 10.5281/zenodo.10403766 (MI_traits_obis, 32.8 MB, CC-BY-4.0) | lp |
| Penn & Deutsch 2022 code | Zenodo 10.5281/zenodo.5899743 (378 kB, "other-open"), GitHub jlpenn/Metabolic-Index-Extinction v1.0.0 | **Archive listed and README and key scripts read by Claude, 9 October.** See the update below |
| Marquez et al. 2026 class-level traits | No deposit found. The PNAS data statement was unreadable (403) | Unknown, not absent |

## Update, 9 October: calibration fields deposited, calibration non-unique

This section is corrected after Codex's
[source note](2026-10-09-penn-calibration-source-correction.md) (Correspondence
77, messages 1185 and 1191). An earlier version of this section stated wrongly
that the end-Permian fields were not deposited and that 50%/500 m was the 2018
calibration.

- **The end-Permian forcing is deposited** as paired endpoint climatologies (see
  the table above). Author contact or a new climate run is not needed for the
  calibration event.
- **The calibration is non-unique.**
  - Penn 2018 (SI p10) gives combinations that explain comparable fractions of
    fossil global and regional loss: 70%/500 m, 80%/1,000 m and about
    95%/4,000 m. Main Fig. 4D uses 80%/1,000 m.
  - Penn & Deutsch 2022 recalibrate with cold-edge limits: about 50% under full
    colonisation and 70% under none, averaged over the upper 500 m.
  - Their code archive (Zenodo 5899743, commit d7d86d9) carries both 50% (spatial)
    and 70% (global) settings. 50%/500 m is therefore a 2022 variant, not a
    verified 2018 optimum.
- **Trait distributions** in `getPDF.m` give means and *standard deviations* of
  log A₀ (2.994, 0.4795), E₀ (0.3988, 0.2692) and log φcrit (1.1285, 0.4234). The
  discrete-grid weights and their normalisation are part of the numerical
  contract.
- **Cold limits** come from modern OBIS records through an external intermediate
  file. A palaeo cold-limit rule is an explicit transfer assumption.
- **Adapter hazard.** Depth index 14 means 500 m on the 2022 WOA grid but 135 m
  in the palaeo deposit. Preserve physical depth, never the index. Volume
  geometry, wet masks, missing values (−10³⁴) and units (no unit attributes in
  the file) also need explicit handling.
- **The Liu, Penn & Deutsch deposit** (Zenodo 18217914) holds figure-panel files
  only, and Crossref finds no companion paper.

**Inference: A is sharper than first posed.** The end-Permian on its own cannot
pin down the threshold, depth and colonisation combination, because several
calibrations explain it equally well. Other events with deposited or generated
temperature and O₂ fields could therefore do two jobs:
1. Test transfer of a named, frozen variant.
2. Discriminate among the equally good end-Permian calibrations: do they
   predict different losses or spatial selectivity elsewhere?

The second turns non-uniqueness from a weakness into the identifying question.
Its novelty is unverified. Other-event forcing remains the open input: only the
K–Pg has deposited 3D O₂, and its 3D temperature is unconfirmed.

## Implications for candidate A

[Inference; to be challenged in Correspondence 77. **Point 1 is superseded** by
the corrected section above: the calibration fields are deposited, so route (a)
is not needed for the end-Permian. Routes (a) and (b) now concern other-event
forcing only.]

1. **The frozen calibration cannot be reproduced from the original runs.** Two
   routes would make A feasible, and both are beyond routine EPRP work:
   - (a) obtain the CESM fields from the authors. That is third-party contact,
     which AGENTS.md reserves to Barry.
   - (b) re-implement the model in cGENIE. The open configs and metabolic-index
     code make this possible, but it means an ensemble of about 10-kyr runs per
     event on deep-server, and it changes the estimand: calibration would be
     cGENIE-internal, not the CESM model.
   Route (b) would be internally consistent, since every event would use one
   model family. That consistency is arguably cleaner for a transfer test, but
   it is a substantial compute commitment and the step that turns a feasibility
   probe into a primary study.
2. **The baseline arm is cheap; the physiology arm is not.** BRIDGE 3D
   temperature for every stage makes "traits plus thermal exposure" feasible from
   deposited data, as Malanoski 2024 did with HadCM3L.
3. **The K–Pg deposit could provide a specificity check.** A frozen
   metabolic-index model should explain *little* of the end-Cretaceous selectivity
   pattern, which Ying 2026 attribute to darkness and body size. This needs 3D
   temperature confirmed first.
4. **Feasibility now favours B and C over A.** B and C need only deposited
   occurrence, forcing and interval data. A stays a candidate, reclassified as
   *gated on inputs*. If it survives the nearest-prior-work check, it goes to
   Barry with the route (a)/(b) choice; it is not dropped.

## Unresolved leads

- Liu, Penn & Deutsch: resolved on 9 October. The deposit holds figure-panel
  data only, and no companion paper was found in Crossref. Phanerozoic CESM O₂
  fields from that group remain unlocated and, if they exist, unpublished.
- Joo et al. 2020 (10.1016/j.earscirev.2020.103123) and Monteiro et al. 2012
  (10.1029/2012PA002351), both on OAE2: model identities and deposits unchecked.
- Endress et al. 2024 (10.1371/journal.pbio.3002443), on thermal optima in
  hypoxia tolerance: deposit unchecked.
