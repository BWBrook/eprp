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

## Amendment A1 (25 October 2026, after smoke runs, before the C2 and C3 runs and before M1 and M2 were scored)

**cGENIE toolchain.** The first image could not run either version:
`genie.job` calls Python 2 scripts (`translate_config.py`) as `python`, and
the `nccompare` tool built with every run needs the legacy netCDF C++
headers (`netcdf.hh`). v0.9.35 also fails to compile under gfortran ≥ 10
(rank mismatch in `outm_netcdf.F`; later makefiles add
`-fallow-argument-mismatch`). Both images now carry Python 2.7.18 and
`libnetcdf-cxx-legacy-dev` ([Dockerfile](env/Dockerfile.cgenie)), built on
Ubuntu 22.04 (gfortran 11.4, `eprp-sw/bench-cgenie:t5`) and 20.04
(gfortran 9.4, netCDF 4.7.3, `eprp-sw/bench-cgenie20:t5`). Three runs, each
with C1 first ([run_t5_cgenie.sh](run_t5_cgenie.sh)):

- `gf9-v0935`: v0.9.35 with gfortran 9, for C2;
- `gf11-v0978`: v0.9.78 with gfortran 11, for C3, as a new user would
  build it today;
- `gf9-v0978`: v0.9.78 with gfortran 9, added to separate the code
  version from the compiler; reported against C3's criteria.

The driver now keeps `testbiogem.out` before `make cleanall` removes it;
the first C1 attempt lost it.

**Metabolic index.** The first run of the checks stopped at a variable
name (`doMI.R` writes `temperature`, not `temp`); the corrected script then
gave the declared results below, except where these rules apply:

1. Two evaluated cells have slightly negative O₂ (−0.04 µmol/kg, a
   numerical artefact of the model) and so negative pO₂, for which
   `doMI.R` gives zero viability. M1 sets p = 0 there; M3 counts them as
   outside its tolerance and excludes them from its median and maximum.
2. **M2 is not met as declared.** `doMI.R` stores habitat viability as
   float32, so the recomputed percentages differ from the stored ones by
   up to 3.7 × 10⁻⁶, the float32 resolution near 100; the 10⁻⁹ tolerance
   was wrong for the storage. Post hoc, the exact check is against the
   stored 0/1 matrix `ecotype_viability` (10,000 ecotypes × cells):
   reported as the number of mismatches.
3. The output labels pO₂ as "matm" while its values (0 to 0.25) are in
   atm; the checks read the values as atm, as `doMI.R` uses them.

## Amendment A2 (25 October 2026): C1 evidence

C1's first, clean run (all three builds `**TEST OK**`, seen in the session
log at 12:03 AEDT) was overwritten on `deep-server` before it was copied:
the driver reruns C1 at the start of every run, and in a tree already built
for the 540 Ma experiment that rerun failed ("cannot stat 'fort.2'",
"ERROR PROCESSING"). C1 was therefore rerun in fresh copies of each tree
([run_t5_c1.sh](run_t5_c1.sh)), again `**TEST OK**` in all three; those
outputs are the committed C1 results, and the failed reruns are kept as
`results/t5/c1_*_rerun_dirty_tree.txt`.

## Amendment A3 (25 October 2026, before running any of it): gen3sis

Next in [SCOPE_T5.md](SCOPE_T5.md)'s order. gen3sis 1.6.0 from the
CRAN snapshot of 2026-10-22, with its source tarball for the shipped
tests (`eprp-sw/bench-r5g:t5`, [Dockerfile](env/Dockerfile.r5g)). Hagen et
al. (2021, *PLOS Biology*, 10.1371/journal.pbio.3001340) deposit their
configs, landscapes and per-simulation summaries (Zenodo 5006413, CC BY
4.0); their own simulation output records gen3sis 0.9.9 (pre-CRAN) on
R 3.6.1, so a bit-identical rerun is not expected.

1. **G1, shipped tests (T1).** `testthat` on the package's `tests/` with
   `NOT_CRAN=true`, which includes the CaseStudy1 reference outputs. Pass:
   no failures.
2. **G2a, dispersal closed form.** gen3sis draws one dispersal value per
   (occupied, free) cell pair and colonises a free cell if any draw reaches
   its distance. With one occupied cell and Weibull(shape k, scale λ)
   draws, a free cell at distance d is colonised in one step with
   probability exp(−(d/λ)^k). Call the internal `disperse` on a synthetic
   species and distance matrix (one occupied cell, free cells at
   d = 100, 300, …, 1,500 km; k = 3, λ = 700, the shape and scale of
   Hagen's first M1 config), 4,000 replicates. Pass: every cell's
   colonisation fraction within 4 binomial SE of the formula.
3. **G2b, speciation timing.** Two occupied cells farther apart than any
   dispersal draw, so isolated from the first step, divergence factor 1,
   threshold T = 5: run the internal `loop_speciation` step by step. Pass:
   one species through step T, exactly two after step T + 1.
4. **G3, Hagen's deposited M1 simulations (characterisation).** Rerun the
   first ten M1 configs (by number) that finished and use a deposited
   landscape (`straume_4d` or `scotese_4d`) at gen3sis 1.6.0 with their
   own seeds, and compare species alive at the end, the final fraction of
   habitable cells occupied, and the deposited `perc_extinction` with our
   reading of it (extinct ÷ total species ever). Reported, no criterion:
   NEWS for 1.5.11 and 1.6.0 lists changes to extinction accounting and
   indexing since the version that produced the deposit.

## Amendment A4 (25 October 2026, after G1 and G2 ran, before G3 ran)

1. The CRAN tarball of gen3sis 1.6.0 has no `tests/`; G1 used the
   repository's tests at the release commit (`cf76a62`, DESCRIPTION 1.6.0,
   2025-09-01). Its first run errored in our setup (the simulation test
   opens a plot device and the tests sat in a read-only directory); it was
   rerun from a writable copy. **G1 is not met as declared**: of 18 tests,
   9 are skipped by the authors' own `skip()` calls, and the CaseStudy1
   test fails two of its three expectations, the md5 checks of `phy.nex`
   and `phy.txt`. The stored reference files have Windows (CRLF) line
   endings and the files written on Linux have LF; line by line they are
   identical, and the summary reference matches (`all.equal`).
2. G2a and G2b ran as declared (`results/t5/t5_gen3sis_checks.json`).
3. G3: the deposit's `landscapes.rds` (2020, gen3sis 0.9.9) is a list of
   data frames (x, y, one column per time step), which gen3sis 1.6.0's
   `create_input_landscape` rejects; each column is converted to a raster
   with `raster::rasterFromXYZ`, values unchanged, and the landscapes are
   compiled with the deposit's own settings (`compile_gen3sis_landscape.R`:
   water cost function, 8 directions, full distance matrices, 391 steps).
   The first selection of configs let an `NA` row through (an unfinished
   config compared with `==`); the corrected list is configs 1, 2, 8, 9,
   10, 12, 13, 15, 16 and 18.

## Amendment A5 (28 October 2026, before the additional G3 run)

G3's original selection included config 9, but its M1 configuration file is
absent from `config.zip`; the attempt failed without producing a simulation.
Keep that failure and the nine completed results. For the tenth **deposited**
configuration, select the next finished M1 row with one of the two declared
landscapes and an actual M1 config file: **config 22**, scotese_4d, seed
66770, with deposited final alive count 3,003. This is a post-hoc selection
repair before running config 22, not a claim that the original selection ran.
The existing G3 outputs remain characterisation, with no pass criterion.

Do not reconstruct config 9 for this tranche: the deposited R1 and R2 M1
templates both differ structurally from the actual M1 config files, and the
summary's seed, shape, scale and divergence threshold do not establish all
the original code. A reconstruction would not be the deposited experiment.
Use the retained compiled landscape and pinned gen3sis 1.6.0 image, with an
isolated output directory and a 12-hour wall-clock ceiling. Report a timeout
or non-OK result explicitly; do not change the selected configuration after
seeing its result. Preserve seed, config file and input hashes with the
receipt. Audit the retained nine and the additional result separately; the
deposit's occupancy and extinction column meanings remain unconfirmed.
