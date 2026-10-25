# Tranche 5 validation: declared tests (cGENIE.muffin and the metabolic index)

Declared by Claude (Opus 5.5) on 25 October 2026, before any of these tests
was run; Barry, 25 October 2026: "Yes, start tranche 5 on deep-server in
parallel: cGENIE first, then the metabolic index, as the scope recommends."
Planning in [SCOPE_T5.md](SCOPE_T5.md). Results go in `results/t5/`; this
file is not edited after the runs except to append dated amendments.

## Environment and inputs

- Toolchain image `eprp-sw/bench-cgenie:t5` ([Dockerfile](env/Dockerfile.cgenie);
  sha256:c340f2af…): Ubuntu 22.04, gfortran 11.4.0, netCDF-C 4.8.1,
  netCDF-Fortran 4.5.4, xsltproc 1.1.34, Python 3.10 with netCDF4. Code
  trees are mounted at `$HOME/cgenie.muffin`, one copy per concurrent run.
- cGENIE.muffin **v0.9.35**: the Zenodo archive cited by Pohl et al. (2023)
  (record 7545805, `derpycode/cgenie.muffin-v0.9.35.zip`, sha256
  b94659cf…, tree `derpycode-cgenie.muffin-f9b7eb6`).
- cGENIE.muffin **v0.9.78**: GitHub tag, commit `3d6846c` (2026-10-16).
- The deposited output: `fields_biogem_3d.nc` (sha256 cafe8ea9…) of
  experiment `AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN`
  (540 Ma, cold baseline), from `alexpohl/cGENIE_based_metabolic_index`
  commit `8e643af` (2022-10-19), 11 time slices at 9.5, 999.5, …,
  9,999.5 yr. The deposit's readme runs this experiment for 8,000 yr; the
  deposited output runs to 10,000 yr.
- Metabolic index: `doMI.R` and `sources/Hofmann_functions.R` at that
  commit. The Stockey repository's `Hofmann functions.R` is the same git
  blob (`a7d11b2`), so it is not tested separately.

## cGENIE.muffin

The experiment for C2 and C3, from the deposit's readme:
`./runmuffin.sh muffin.AP.540ebP2_.eb_go_gs_ac_bg.PO4.SPIN
PUBS/submitted/Pohl_et_al.SciAdv.2023
AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN 10000`, from
rest (no restart), so that every deposited slice has a counterpart.
Comparison ([validate/t5_cgenie_compare.py](validate/t5_cgenie_compare.py)),
at each slice from 999.5 yr on: the volume-weighted ocean means of
`ocn_temp` (°C) and `ocn_O2` (µmol/kg), weights from `grid_area` × layer
thickness over wet cells; and the Pearson correlation of each field with
the deposit over wet cells. The 9.5-yr slice and bitwise identity are
reported, not graded.

**C1. Regression (T1).** `make testbiogem` in `genie-main` for each
version. Pass: `testbiogem.out` reports `**TEST OK**` against the shipped
`genie-knowngood` output.

**C2. Reproduce the deposited trajectory at v0.9.35.** Pass, at every slice
from 999.5 yr: |ΔT_vol| ≤ 0.05 °C, |ΔO₂_vol| ≤ 1 µmol/kg, and r ≥ 0.99
for both fields. The tolerance reflects that the deposit predates v0.9.35
by three months and was built with another compiler, so bitwise identity
is not expected; the deposit itself moves by 0.004 °C and 0.10 µmol/kg
between its last two slices.

**C3. Version drift, v0.9.78.** The same experiment and criteria.

## Metabolic index

Run `doMI.R` on the deposited output at 7,999.5 yr with the readme's
standard options (`--vertical_dimension upperocean --mask shelves
--exclude_poles TRUE --output_netcdf TRUE --set_seed 1993`) and
`--neco 10000` ecotypes. Φ = A₀ · pO₂ · exp((E₀/k_B)(1/T − 1/T_ref)), with
ln A₀ ~ N(3.01, 0.49), E₀ ~ N(0.41, 0.29) eV, ln Φ_crit ~ N(1.10, 0.42),
T_ref = 15 °C; an ecotype is viable in a cell if Φ ≥ Φ_crit.

**M1. Closed form.** Viability is then a normal probability:
p = Φ_N((3.01 + ln pO₂ + 0.41x − 1.10) / √(0.49² + 0.42² + 0.29²x²)),
x = (1/T − 1/T_ref)/k_B. For every evaluated cell, compare `doMI.R`'s
habitat viability (as a fraction) with p from the cell's own pO₂ and T.
Pass: every cell within 4 SE, SE = √(max(p(1 − p), 1/n)/n), n = 10,000.
The same ecotypes serve every cell, so cell errors are correlated; the
criterion is per cell.

**M2. Internal consistency.** Recompute habitat viability for every cell
from the output file's own A₀, E₀, Φ_crit, temperature and pO₂. Pass:
equal to 1e−9 (in percent).

**M3. pO₂ against an independent implementation.** Recompute pO₂ for the
same cells with TEOS-10 (`gsw`: pressure from depth, potential temperature,
Garcia & Gordon 1992 O₂ solubility), Weiss & Price (1980) vapour pressure,
x_O₂ = 0.20946 and the hydrostatic correction exp(ν p / RT) with
ν = 32.0 cm³ mol⁻¹ ([validate/t5_mi_checks.py](validate/t5_mi_checks.py)).
Pass: |Δ ln pO₂| ≤ 0.02 in at least 99% of cells. This checks the
transcription of the pO₂ calculation, not the physiology. Reading the code
before declaring showed that `p_corr_pp` sets ν with
`mean(31.9, 31.9, 32.2, 32.3, 32, 31.7)`, which R evaluates as 31.9 (the
second argument is `trim`); its effect is reported separately.

Penn & Deutsch's MATLAB implementation is not run (no MATLAB or Octave on
any host).
