# Tranche 5 scope: Earth-system, spatial and physiological simulators

A planning note, not a declaration. A Claude Sonnet subagent wrote it on
24 October 2026 while tranche 4 ran; Claude (Opus 5.5) checked three of
its claims (INDITEK-2.0's publication, goSPL's post-release fixes, the
shared metabolic-index code). Labels: `checked` with the source (GitHub
API, Zenodo, Crossref, Docker Hub, or computed from a deposited file);
`unverified` where inferred. Nothing has been built. Tests are proposals;
the tranche's `VALIDATION_T5.md` will declare the final set before
running.

## Recommended order

Build cGENIE first and start its long runs in the background, then:
metabolic index (cheapest; R and one deposited output), gen3sis (minutes;
deposited published inputs and outputs), INDITEK-2.0, goSPL, and pySCION
last (no deposited outputs; its only reference is MATLAB).

## cGENIE.muffin

- `derpycode/cgenie.muffin` v0.9.78, commit `852b9d4`, 2026-10-16, MIT
  (`checked`, GitHub, Zenodo 23420890). No official container; the
  Stanford Apptainer recipe (`aprow620/cgenie-on-sherlock`, Zenodo
  20435138) builds on Ubuntu 22.04 with gfortran, netCDF-C 4.9.2 and
  netCDF-Fortran 4.6.1 from source, and ends with `make testbiogem` on
  branch `master.python3` (`checked`).
- Branch hazard: `master.python3` is 227 commits behind `master`, and
  `master`'s `genie.job` calls Python-2 code (`checked`); whether
  `make testbiogem` runs on `master` with Python 3 only is `unverified`.
- The repository ships four reference outputs in `genie-knowngood/` for
  `make testbiogem` (`checked`). Pohl et al. 2023 (Zenodo 7545805, v0.9.35)
  deposit code and 168 configurations for 28 palaeogeographies (0–540 Ma),
  but no outputs; one output, the 540 Ma cold baseline
  (`fields_biogem_3d.nc`, 151 MB, 11 snapshots to 9,999.5 yr), sits in the
  Pohl metabolic-index repository (`checked`). Volume means from it: 3.79 °C
  and 159.6 µmol/kg O₂ at 999.5 yr; 3.03 °C and 134.7 µmol/kg at 7,999.5 yr.
- Compute: 300–400 model years per CPU-hour (manual), so 8,000 yr is about
  20–27 CPU-h per run (`unverified`).
- Proposed: **C1** `make testbiogem` against the knowngood file (T1);
  **C2** rerun the 540 Ma experiment at v0.9.35 for 1,000 and 8,000 yr and
  match the deposited volume means (|ΔT| ≤ 0.05 °C, |ΔO₂| ≤ 1 µmol/kg) and
  fields (r ≥ 0.99); **C3** the same at v0.9.78 (version drift).
- New palaeogeographies need MATLAB `muffingen`; existing ones do not.

## Metabolic index

- Pohl (`alexpohl/cGENIE_based_metabolic_index`, GPL-3.0) and Stockey
  (`richardstockey/cGENIE-metabolic_index.extinction`, no licence) share a
  byte-identical `Hofmann_functions.R` (same git blob `a7d11b2`, `checked`),
  the same trait sampling (seed 1993) and the same Φ line, so comparing them
  is an identity check, not a cross-check. Penn & Deutsch
  (`jlpenn/Metabolic-Index-Extinction`) is MATLAB, needs external seawater
  and O₂-solubility routines not in the repository, and computes pO₂ per
  volume rather than per mass (about 2.5% apart) (`checked`).
- Φ = A₀ · pO₂ · exp((E₀/k_B)(1/T − 1/T_ref)), T_ref 15 °C. With lognormal
  traits the viable fraction has a closed form; at 15 °C and 0.21 atm it is
  0.7059, at 25 °C and 0.10 atm 0.1050 (computed, Monte Carlo agrees to
  0.0006).
- [Detail withheld pending disclosure to the data custodian.]

## gen3sis and goSPL

- gen3sis: CRAN 1.6.0, 2025-09-01, GPL-3 (`checked`); ships a CaseStudy1
  reference-output regression test. Hagen et al. 2021's supplement (Zenodo
  5006413, CC BY 4.0) deposits seeded configurations, landscapes and
  numerical outputs (`checked`); the Lorcery 2025 goSPL-to-gen3sis
  repository has scripts only, no outputs and no licence (`checked`).
- Proposed: **G1** the shipped regression; **G2** closed forms
  (one-step colonisation probability under Weibull dispersal; deterministic
  speciation time under the divergence threshold); **G3** rerun 10 deposited
  Hagen configurations at 1.6.0 and the archived 1.3 and compare summaries
  (exact on 1.3; 1.5.11 and 1.6.0 changed extinction accounting).
- goSPL: release v2026.7.14 (2026-07-10), GPL-3.0; Docker Hub
  `geodels/gospl-hpc` v2026.7.14 (amd64); default branch `dev` at `a998c3d`
  (2026-10-23) (`checked`). **15 of the 21 fixes in `docs/dev/FIXED_BUGS.md`
  postdate the release** (checked by Claude), including wrong stream-power
  slopes and advection volume loss, so the PyPI and Docker artefacts lack
  them. The repository shows AI-assisted development (`AGENTS.md`,
  `.claude/`).
- Proposed: **P1** the shipped tests and benchmarks on the release and a
  pinned `dev` commit; **P2** the analytic hillslope profile (peak 625 m
  within 5%); **P3** the stream-power slope–area relation (m/n within 5%);
  **P4** partition invariance (np 1 against 2).

## INDITEK-2.0

- Published: Herrero-Gascón, García-Comas, Bodin, Benton (2026),
  *Methods in Ecology and Evolution*, doi:10.1111/2041-210x.70422, 22
  October 2026 (`checked`, Crossref). GitHub has no licence; the Zenodo
  deposit 22079167 (code and data) is CC BY 4.0 (`checked`).
  `requirements.txt` pins numpy 2.4.6, pandas 3.0.3, scipy 1.17.1, which
  need Python ≥ 3.11; the README says 3.9 (`checked`). The MCMC and the
  synthetic-data generator are unseeded.
- The deposited proof chains (6 × 5,002 iterations) have pooled intervals
  that include the five nominal parameters in the deposited generator script
  (computed). **28 October correction:** this is not calibrated coverage,
  and the exact generating values are not established; saved-chain
  diagnostics show poor mixing. The earlier conclusion here that
  `D_proof.npz` was not the noise-free source of `observed_D.npz` was too
  strong: their correlation and slope cannot establish provenance. A
  subsequent nominal-parameter forward rerun does not reproduce that
  reference map; its precise role and the actual observation generation remain
  unresolved. See the [forward review](../reviews/2026-10-28-inditek-forward-and-claims/README.md).
- Proposed: **N1** forward-model reproduction of stored chain states
  (1e−9 relative on one stack); **N2** coverage and R-hat on the deposited
  chains; **N3** calibration on 10 seeded synthetic datasets (about
  330 CPU-h).

## pySCION

- `amer7632/pySCION` v1.0.0 (2025-01-16), Apache-2.0 on GitHub, CC BY 4.0 on
  Zenodo; unpinned; the README omits `cmcrameri` (`checked`). It ports
  MATLAB SCION v1.1.6 with different forcing files. Neither pySCION nor
  SCION deposits model output (`checked`).
- Proposed: **S1** its own tuning target (each reservoir within 5% of
  modern; calibration, not independent truth); **S2** solver convergence
  (tolerances tightened tenfold, ≤ 0.5% change); **S3** a port check
  against SCION v1.1.6 under Octave, if Octave is admitted (not on any host).

## Corrections to the landscape and leads

Applied on 24 October 2026: INDITEK-2.0 is published and its Zenodo
deposit is licensed (L-012); the two R metabolic-index codes are not
independent (L-013); pySCION's licences conflict and it ports v1.1.6
(L-014); the Hagen 2021 deposit, not Lorcery 2025, is gen3sis's
reproducible published case (L-015); goSPL's release predates most of its
logged fixes. Candidate author items (not yet verified enough to queue):
INDITEK's unseeded RNG, Python pins and GitHub licence; pySCION's
dependency list; the Stockey repository's licence; Penn & Deutsch's
missing external functions.
