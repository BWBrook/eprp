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
| End-Permian, the calibration event | **No.** No deposit found for the CESM fields of Penn et al. 2018 (10.1126/science.aat1327); Codex's search agrees. Al Aswad 2025 reuses those runs, and its deposit (Zenodo 11522106, mf) has code and PBDB data but no fields | Re-run cGENIE from open configs: Hülse et al. 2021, 10.1038/s41561-021-00829-7, three phases, configs only; Stockey et al. 2021, p0251 sweeps |
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

## Update, 9 October: the frozen model is deposited; the forcing is not

Claude listed the Penn & Deutsch 2022 code archive and read its README,
`SixExtinct_spatial.m`, `getPDF.m` and parts of `get6extinct_func.m`.

- **Frozen choices are hard-coded:**
  - `upar.Vcrit = 50`, a 50% critical loss of global habitat volume;
  - `upar.zhab = 14`, a 500 m maximum habitat depth (z-level 14).
- **Trait distributions are parametric and in the code:**
  - log(A₀) ~ N(2.994, 0.4795) on 5–55 atm⁻¹;
  - E₀ ~ N(0.3988, 0.2692) on −0.1 to 1.1 eV;
  - log(φcrit) ~ N(1.1285, 0.4234) on 1.5–7.
  These are binned and weighted, and come from cadeutsch/Metabolic-Index-Traits.
- **Species cold limits** (`getTmin2.m`) come from modern OBIS occurrences with at
  least 100 records. A deep-time application needs a substitute.
- **The forcing is modern:** CMIP5 and CMIP6 temperature and O₂ anomalies
  regridded onto WOA. `6me_output.mat` (337 kB) holds plotting output. There are
  no end-Permian or other palaeo fields.

That 50% and 500 m are the end-Permian-calibrated combination from Penn et al.
2018 (Fig. 4 explored 40–95% and 500–4,000 m) is **inferred** from the 2022
paper's calibration claim and Al Aswad 2025's use of 50%. It has not been
checked against the 2018 text.

The Liu, Penn & Deutsch deposit (Zenodo 18217914, 12 January 2026, CC-BY-4.0)
holds six MATLAB *figure-panel* files for "Climate Drivers of Ocean
Productivity and Oxygenation Across the Phanerozoic". These are not 3D fields.
A Crossref title search found no matching publication (two Goldschmidt 2024
abstracts on related topics only).

**Consequence.** For candidate A, only the *event forcing fields* are missing.
The ecophysiological model, its thresholds and its trait distributions can be
frozen exactly as deposited, apart from the OBIS cold-limit term. Route (b) then
becomes:
1. Generate event temperature and O₂ fields in cGENIE.
2. Check that the deposited frozen model reproduces end-Permian magnitude and
   selectivity on cGENIE's end-Permian fields (calibration consistency).
3. Only then transfer to held-out events.

The model contract changes only in its ESM, not its ecophysiology.

## Implications for candidate A

[Inference; to be challenged in Correspondence 77. Point 1 is updated by the
section above: route (b) now keeps the deposited ecophysiology frozen.]

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
