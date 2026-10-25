---
id: cgenie-muffin
name: cGENIE.muffin
kind: model
domain: earth-system
languages: [Fortran, C++, Python 2, shell]
home: https://github.com/derpycode/cgenie.muffin
repo: https://github.com/derpycode/cgenie.muffin
paper: [10.1126/sciadv.adg7679]
licence: MIT
release: {version: "v0.9.78 (tag commit 3d6846c); v0.9.35 (Zenodo 7545805) also tested", date: 2026-10-16, checked: 2026-10-25}
maintenance: {state: active, last_commit: 2026-10-16, checked: 2026-10-25}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.cgenie, image: "eprp-sw/bench-cgenie:t5 (Ubuntu 22.04, gfortran 11; sha256:caa05fb8…) and eprp-sw/bench-cgenie20:t5 (Ubuntu 20.04, gfortran 9; sha256:75846569…)", host: deep-server}
blockers: ["new palaeogeographies need the MATLAB muffingen generator"]
related_sources: []
eprp_questions: [Q-001, Q-021, Q-049, B-005]
entry: {created: 2026-10-25, updated: 2026-10-25, by: Claude (Opus 5.5), reviewed: not yet}
---

# cGENIE.muffin

## Summary

cGENIE.muffin is an Earth system model of intermediate complexity: a
36 × 36 frictional-geostrophic ocean (GOLDSTEIN; 17 levels here) with an
energy–moisture-balance atmosphere and sea ice, coupled to ocean
biogeochemistry (BIOGEM), atmospheric chemistry, sediments and
weathering. Its speed (hundreds of model years per CPU-hour) makes
thousand-year spin-ups and parameter ensembles on deep-time
palaeogeographies practical. Pohl et al. (2023) ran it on 28 Phanerozoic
slices to drive the metabolic-index analysis
([cgenie-metabolic-index-pohl](../cgenie-metabolic-index-pohl/README.md)).

## Install

Toolchain-only images ([Dockerfile](../bench/env/Dockerfile.cgenie)); the
code tree is copied per run and mounted at `$HOME/cgenie.muffin`, where
the scripts expect it, with output in `$HOME/cgenie_output`. What it
needs, found by failing (tranche 5, amendment A1):

- **Python 2.** `genie.job` runs `translate_config.py` and `config2xml.py`,
  which use Python 2 `print` statements, as `python`; this holds at v0.9.78
  as at v0.9.35, so a Python-3-only system fails at the first run.
- **The legacy netCDF C++ interface** (`netcdf.hh`; Ubuntu
  `libnetcdf-cxx-legacy-dev`) for the `nccompare` tool that every build
  compiles.
- **netCDF under `/usr/local`** (`NETCDF_DIR` in `user.mak`); Debian and
  Ubuntu install it under `/usr`, so link it or edit `user.mak`.
- **v0.9.35 needs gfortran < 10.** Newer gfortran stops on a rank mismatch
  in `outm_netcdf.F`; later makefiles add `-fallow-argument-mismatch`.
  Ubuntu 20.04 (gfortran 9.4) builds it.
- One run per code tree at a time: `runmuffin.sh` cleans and rebuilds when
  the base configuration changes. Rerunning `make testbiogem` in a tree
  built for another configuration failed ("cannot stat 'fort.2'", "ERROR
  PROCESSING"); run it in a fresh tree.
- A build takes about six minutes.

## Validation

[bench/VALIDATION_T5.md](../bench/VALIDATION_T5.md), declared before
running; three builds: v0.9.35 with gfortran 9, v0.9.78 with gfortran 11,
and v0.9.78 with gfortran 9.

| Test | Result |
| --- | --- |
| C1: `make testbiogem` against the shipped `genie-knowngood` output | **pass** in all three builds (`**TEST OK**`; `bench/results/t5/c1_*`) |
| C2: rerun Pohl et al.'s 540 Ma cold baseline (`AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN`) for 10,000 yr at v0.9.35 and match the deposited output (volume means within 0.05 °C and 1 µmol/kg O₂, r ≥ 0.99, at every slice from 999.5 yr) | running (to about 21:30 AEDT 26 Oct). At 999.5 yr: **pass**, ΔT_vol < 10⁻⁴ °C, ΔO₂_vol −0.001 µmol/kg, r = 1.0000; not bitwise identical (largest cell differences 0.13 °C and 5.6 µmol/kg, in the southernmost rows) |
| C3: the same at v0.9.78 | running. At 999.5 yr: **pass**, ΔT_vol < 10⁻⁴ °C, ΔO₂_vol −0.045 µmol/kg. gfortran 9 and 11 give bitwise-identical v0.9.78 fields, so the drift is the code version, not the compiler |

The deposit's readme runs this experiment for 8,000 yr; its deposited
output runs to 10,000 yr and includes a 9.5-yr slice that our 10,000-yr
runs do not write, so it was probably made with different run settings.

## Weaknesses and pitfalls

- The build requirements above are not documented together in the
  repository; the Python 2 dependency is the one most likely to stop a new
  user today.
- New palaeogeographies need the MATLAB `muffingen` generator; the shipped
  ones do not.

## EPRP relevance

The ocean-state engine for Q-001, Q-021 and Q-049 and for B-005's
spatial models; deep-server runs it at about 300–400 model years per
CPU-hour per run, and kunanyi would take ensembles.

## Citation and licence

Pohl, A. et al. (2023). Why the Early Paleozoic was intrinsically prone to
marine extinction. *Science Advances* 9, eadg7679.
doi:10.1126/sciadv.adg7679 (checked on Crossref). Code: MIT. Cite the
release used (Zenodo DOIs per tag, e.g. 10.5281/zenodo.7545805 for
v0.9.35).

## Verification log

- 2026-10-25 `checked`: tag v0.9.78 cloned (commit `3d6846c`); v0.9.35
  from Zenodo 7545805 (sha256 b94659cf…); `runmuffin.sh`, `genie.job`,
  `makefile.arc` and `user.mak` read; C1 on `deep-server`.
