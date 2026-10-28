---
id: cgenie-metabolic-index-pohl
name: cGENIE-based metabolic index (Pohl; Stockey)
kind: workflow
domain: earth-system
languages: [R]
home: https://github.com/alexpohl/cGENIE_based_metabolic_index
repo: https://github.com/alexpohl/cGENIE_based_metabolic_index
paper: [10.1126/sciadv.adg7679, 10.1073/pnas.2101900118, 10.1126/science.aat1327]
licence: "GPL-3.0 (Pohl repository); the Stockey repository has no licence"
release: {version: "v0.0 (Zenodo 10.5281/zenodo.7224943); tested at commit 8e643af", date: 2022-10-19, checked: 2026-10-25}
maintenance: {state: dormant, last_commit: 2022-10-19, checked: 2026-10-25}
tier: T2
validated_uses: ["habitat viability equals its closed form under the Penn et al. trait distributions (M1)", "pO2 from cGENIE output agrees with a TEOS-10 recomputation to 0.0006 in log (M3)", "per-ecotype viability recomputes exactly from the stored traits (M2, post hoc)"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r5, image: "eprp-sw/bench-r5:t5 (sha256:e8c844e9…); checks in eprp-sw/bench-py5:t5 (sha256:589bb0c3…)", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [Q-001, Q-049, Q-021]
entry: {created: 2026-10-25, updated: 2026-10-28, by: Claude (Opus 5.5), reviewed: "Codex, 28 October 2026, retained-output review"}
---

# cGENIE-based metabolic index (Pohl; Stockey)

## Summary

R code that turns a cGENIE ocean state into ecophysiological habitat: it
samples a population of marine ectotherm "ecophysiotypes" from the trait
distributions of Penn et al. (2018), computes each one's metabolic index Φ
in every ocean cell from temperature and oxygen partial pressure, and
reports which cells each can live in and the fraction of ecotypes viable
per cell. Pohl et al. (2023) and Stockey et al. (2021) use it to link
Phanerozoic ocean states to extinction vulnerability. Reach for `doMI.R`
when a question needs aerobic habitat from a cGENIE run; it takes a single
command line and writes netCDF.

## Method

Φ = A₀ · pO₂ · exp((E₀/k_B)(1/T − 1/T_ref)), T_ref = 15 °C, with
ln A₀ ~ N(3.01, 0.49), E₀ ~ N(0.41, 0.29) eV and ln Φ_crit ~ N(1.10, 0.42)
sampled once per run (seed 1993 by default); an ecotype is viable in a cell
where Φ ≥ Φ_crit. pO₂ comes from Hofmann et al.'s (2011) functions: the
Garcia & Gordon (1992) O₂ solubility at potential temperature, water vapour
after Weiss & Price (1980), x_O₂ = 0.20946, and a hydrostatic correction
exp(ν p / RT). Options select the upper ocean or all levels, shelves, a
mask, and whether to drop polar rows.

**Pohl and Stockey are one implementation.** The two repositories'
`Hofmann_functions.R` are the same git blob (`a7d11b2`), and the trait
sampling and Φ line are identical; Pohl's README says the science is
unchanged from Stockey's. Comparing them checks nothing independently.
Penn & Deutsch's own implementation is MATLAB, with external seawater and
solubility routines that are not in their repository.

## Install

R from the tranche-4 image plus optparse, AquaEnv, ncdf4, reshape2 and
RNetCDF and the system netCDF library
([Dockerfile](../bench/env/Dockerfile.r5)); clone the repository and run
`Rscript doMI.R` from its top directory, which reads `input/` and writes
`output/`.

## Validation

[bench/VALIDATION_T5.md](../bench/VALIDATION_T5.md), declared before
running; amendment A1 records three handling rules. Run on the deposited
540 Ma cold-baseline cGENIE output (the repository's own test input, which
is a real model run, not synthetic) at 7,999.5 yr, upper ocean, shelves,
poles excluded, 10,000 ecotypes, seed 1993: 524 evaluated cells
(`bench/results/t5/t5_mi.json`).

| Test | Result |
| --- | --- |
| M1: habitat viability against its closed form, p = Φ_N((3.01 + ln pO₂ + 0.41x − 1.10)/√(0.49² + 0.42² + 0.29²x²)), x = (1/T − 1/T_ref)/k_B; every cell within 4 binomial SE | **pass**: max \|z\| 1.81, mean 0.67, largest difference 0.0085 |
| M2: viability recomputed from the stored A₀, E₀, Φ_crit, T and pO₂, to 10⁻⁹ percent | **not met as declared**: the file stores viability as float32 (largest difference 3.7 × 10⁻⁶ percent, float32 resolution). Post hoc, the stored per-ecotype presence matrix matches the recomputation in all 5,240,000 ecotype–cell entries |
| M3: pO₂ against an independent TEOS-10 (`gsw`) recomputation, \|Δ ln pO₂\| ≤ 0.02 in ≥ 99% of cells | **pass**: 522 of 524 cells, median 0.00036, maximum 0.00058; the other two have negative O₂ (below) |

## Strengths

- For the tested field and options, viability matches the analytic
  distribution within the declared sampling tolerance, and positive pO₂
  matches the seawater-library calculation within 0.1%.
- One command line from cGENIE output to netCDF maps of viability, with a
  seed for reproducibility.
- Fast: 90 s for 10,000 ecotypes on the upper-ocean shelves.

## Weaknesses and pitfalls

- **The pO₂ variable in the output is labelled "matm" but holds atm**
  (values 0 to 0.25); `doMI.R` itself uses it correctly as atm.
- **Within an evaluated cell**, `ecotype_viability` stores 1 for viable
  and leaves non-viable entries missing: 3.0 million of 5.2 million entries
  here. Unevaluated cells also contain missing values. Define the evaluation
  domain from `habitat_viability` and the input masks first; treat missing
  as nonviable only inside that domain.
- **Two cells had slightly negative O₂** (−0.04 µmol/kg, a numerical
  artefact of the model) and so negative pO₂, which the code silently
  treats as uninhabitable; filter or report such cells.
- `p_corr_pp` sets the partial molar volume of O₂ with
  `mean(31.9, 31.9, 32.2, 32.3, 32, 31.7)`, which R evaluates as 31.9 (the
  second argument is `trim`), not the intended average 32.0; the same
  pattern sets the other gases. The effect on pO₂ here is under 10⁻⁴ in
  log, negligible.
- Viability is stored as float32.
- The Stockey repository has no licence; use Pohl's (GPL-3.0).
- Only the upper-ocean, shelves configuration of the README was tested.

## Alternatives and overlap

Penn & Deutsch's MATLAB code (`jlpenn/Metabolic-Index-Extinction`) is the
independent implementation, not run here (no MATLAB or Octave). The
cGENIE runs themselves are benchmarked in tranche 5
([cgenie-muffin](../cgenie-muffin/README.md)).

## EPRP relevance

The aerobic-habitat step for Q-001 and Q-049 style questions and for
pairing physiology with cGENIE palaeogeographies (lead L-013). The tests
support the stated calculations for one field and set of options; other
configurations, masks, boundaries and scientific assumptions need their own
checks. See the [independent review](../reviews/2026-10-28-tranche5-codex/README.md).

## Citation and licence

Pohl, A. et al. (2023). Why the Early Paleozoic was intrinsically prone to
marine extinction. *Science Advances* 9, eadg7679.
doi:10.1126/sciadv.adg7679. Stockey, R. G. et al. (2021). Decreasing
Phanerozoic extinction intensity as a consequence of Earth surface
oxygenation and metazoan ecophysiology. *PNAS* 118, e2101900118.
doi:10.1073/pnas.2101900118. Penn, J. L. et al. (2018).
Temperature-dependent hypoxia explains biogeography and severity of
end-Permian marine mass extinction. *Science* 362, eaat1327.
doi:10.1126/science.aat1327. All checked on Crossref, 25 October 2026.
Code: GPL-3.0 (Pohl).

## Verification log

- 2026-10-25 `checked`: `doMI.R` and `sources/Hofmann_functions.R` read at
  commit `8e643af`; the Stockey file compared by git blob hash.
- 2026-10-25 `checked`: M1–M3 on `deep-server` (`bench/results/t5/`).
