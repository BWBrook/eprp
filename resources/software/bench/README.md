# Tranche 1: a known-truth bench for rates

Validation of two fossil-record generators and three rate estimators against
known truth, run on `deep-server` on 23 October 2026. The tests were declared
in [VALIDATION.md](VALIDATION.md) and committed (`2be84d6`) before any ran;
amendment A1 records the changes made before the full run, and A2 the
test added and the disclosures made after an independent review (Claude
Sonnet subagent, 24 October 2026), whose findings are applied here. Each
tool's entry
interprets its results: [FossilSim](../fossilsim/README.md),
[paleobuddy](../paleobuddy/README.md), [divDyn](../divdyn/README.md),
[PyRate](../pyrate/README.md), [RevBayes](../revbayes/README.md).

## Results

| Test | Tool | Result | Key numbers |
| --- | --- | --- | --- |
| G1 birth–death moments | paleobuddy `bd.sim` | **pass** | mean extant 4.523 vs 4.482 (z = 0.66); survival 0.3934 vs 0.3916 (z = 0.51); 20,000 replicates |
| G1 | TreeSim `sim.bd.age` | **pass** | 4.606 (z = 1.95); 0.3953 (z = 1.06) |
| G2 Poisson fossil sampling | paleobuddy `sample.clade` | **pass** | z = −0.29; dispersion 0.994 (tolerance ±0.030) |
| G2 | FossilSim `sim.fossils.poisson` | **pass** | z = −0.48; dispersion 0.990 (±0.048); 7,895 trees |
| G3 piecewise speciation | paleobuddy | **pass** | 2.115 vs 2.117 (z = −0.08) |
| G3b shift order (A2) | paleobuddy | **pass** | species alive 7.5 Myr after the origin: 4.569 vs 4.482 (z = 0.55); 0.472 if the order were reversed; 2,000 runs |
| G4 cross-generator | paleobuddy vs TreeSim + FossilSim | **pass** | KS p = 0.25 (extant), 0.55 (species), 0.44 (duration), 0.56 (fossils); about 7,900 surviving clades each; low power (TreeSim 1.0–1.4% higher on all four) |
| G5 taxonomy | FossilSim `sim.taxonomy` | **pass** | originations 95,458 vs 95,677 expected, terminations 73,431 vs 73,650 (z = −1.27 each); 2,000 trees |
| E1 binned rates, complete sampling | divDyn 0.8.3 | **pass** | extinction 0.1998 against μΔ = 0.20, origination 0.2501 against λΔ = 0.25 (every rate column reduces to these two values here); 200 replicates × 18 bins |
| E1, Poisson sampling ψ = 0.5 | divDyn | reported | relative bias: corrected three-timer +1.2% / −0.3%; gap-filler +1.5% / +1.0%; boundary-crosser +7.9% / +0.2%; raw three-timer +482% / +385% (uncorrected by design); second-for-third −36% / −36% (unexplained) |
| E2 coverage, ψ = 1.0 | PyRate `6a27efb` | **fail (q)** | 95% intervals cover λ 95/100, μ 95/100, **q 81/100** (declared ≥ 90); median bias λ −11%, μ −12%, q +9%; all ESS ≥ 100 |
| E2, ψ = 0.25 | PyRate | reported | coverage λ 44/50, μ 40/50, q 33/50; median bias λ +6%, μ −3%, q +46% |
| E3(a) deposited coverage | skyfbdr study runs | reported | coverage over 1,000 prior draws: λ **0.932** / 0.945 / 0.954, μ 0.945 / 0.938 / 0.948, ψ 0.941 / **0.903** / 0.944 (oldest to youngest stage; pooled 0.939; 936/1,000 is the 2.5% binomial bound) |
| E3(b) rerun | RevBayes v1.4.1 | **blocked** | the range process is disabled in every release since April 2024 (A1) |

## What the bench found

- **Both generators reproduce analytic birth–death and Poisson-sampling
  truth.** paleobuddy and TreeSim/FossilSim are independent codebases; both
  hit the analytic moments, and KS tests did not distinguish their
  distributions, though with little power: TreeSim's clades ran 1.0–1.4%
  larger on all four summaries (z = 1.95 against the analytic mean), within
  tolerance. paleobuddy applies rate shifts in the stated order (G3b).
  Either can serve as truth for later tranches. FossilSim's taxonomy layer
  gives the expected morphospecies counts (one combined check; A2).
- **PyRate's preservation rate is biased high, and the bias tracks the
  durations it infers for sampled species.** The q intervals are about
  the right width (mean posterior sd 0.084q against a spread of posterior
  medians of 0.078q at ψ = 1.0) but shifted by about one posterior sd
  (+1.03; +1.41 at ψ = 0.25), and every miss has the truth below the
  interval (19 of 19; 17 of 17). Post hoc diagnostics on the same
  histories (not declared tests):
  - `validate/pyrate_durations.py` compares PyRate's posterior species
    times with the truth. Inferred durations are 8% short at ψ = 1.0 and
    31% short at ψ = 0.25; singletons are inferred at 66% and 50% of their
    true durations.
  - The same script maximises PyRate's own zero-truncated preservation
    likelihood with durations fixed. At the true durations it gives q
    1.006 (ψ = 1.0) and 0.246 (ψ = 0.25), within 2% of the truth. At
    PyRate's inferred durations it gives 1.096 and 0.358, against PyRate's
    posterior medians of 1.090 and 0.364.
  - `validate/pyrate_attribution.R` computes rates from true species
    times: conditioning on clade size moves λ and μ by under 4%; dropping
    unsampled species moves them by −20% (ψ = 1.0) and −36% (ψ = 0.25).

  So the preservation likelihood is sound and the q bias comes from the
  shortened durations. Why they are short is our reading, not tested: the
  likelihood divides by the probability of being sampled, (1 − e^{−qD}),
  while the birth–death prior on each species' times carries no matching
  factor, so short durations are favoured. The same shortening raises λ and
  μ, partly offsetting the missing short-lived species. At ψ = 1.0 their
  medians are still 11–12% low (about 0.8 posterior sd, all five misses on
  one side), but the intervals are wide enough that no undercoverage is
  detectable (95/100 is compatible with roughly 89–98%). At ψ = 0.25 the λ
  and μ intervals are narrower than the spread of the medians.
- **divDyn's binned rates are exact under complete sampling.** Under
  incomplete sampling its corrected three-timer and gap-filler rates are
  within 2% of truth. The raw three-timer is biased as theory predicts. The
  second-for-third rates are 36% low. divDyn substitutes the median of the
  three subsequent-sampling counts, which its source comment attributes to
  Alroy (2015); the cause is open (one untested candidate: continuous
  turnover within bins violates the method's assumptions). Under complete
  sampling every rate column reduces to the same two numbers, so E1's pass
  is one check of extinction and one of origination.
- **The skyline FBD-range study's own runs are close to calibrated, but
  two rates fall short.** Pooled over the nine rates, coverage is 93.9%.
  Below the 2.5% binomial bound (936/1,000) are the oldest-stage
  speciation rate (0.932) and, clearly, the middle-stage sampling rate
  (0.903). MCMC is not the cause: median effective sample sizes are about
  3,900 of 4,000 retained samples, and ψ2 coverage is 0.903 to 0.907 at
  burn-ins of 0 to 50%. The misses sit in the tails of the truth: by
  quintile of the true value, coverage is 0.89, 1.0, 1.0, 1.0, 0.63 for
  ψ2 and 0.72, 0.98, 1.0, 1.0, 0.97 for λ1. The study redraws every
  parameter when the number of sampled species falls outside 5–50, which
  preserves calibration. Two loops in its code condition at fixed
  parameters and do not: `bd.sim(..., nFinal = c(5, Inf))` (at least five
  species in total) and resampling fossils until one species is sampled.
  The first fits the λ1 pattern, since low early speciation is what it
  rejects; that is our reading, not tested. The reversed stage order gives
  lower coverage in every end stage (by 0.012 to 0.081), supporting the
  index mapping.
- **The released RevBayes cannot run the FBD range process at all** (see
  [the RevBayes entry](../revbayes/README.md)).

## Rerun

On `deep-server`, with this directory copied to `/data/paleosoft/bench`
(the host has no GitHub credentials; copy with `rsync`):

```bash
tmux new-session -d -s eprp-t1-build 'bash /data/paleosoft/bench/env/build.sh'
```

```bash
tmux new-session -d -s eprp-t1 'bash /data/paleosoft/bench/run.sh'
```

The review follow-up (G3b, timings, diagnostics, extended E3(a) and divDyn
standard errors) is `followup.sh`; the extended E3(a) was run on its own
with `validate/skyfbdr_coverage.py`.

The study inputs for E3(a) come from a sparse clone of
`brpetrucci/skyfbdr_simstudy` at `950b9bc`
(`results/skyfbdr-commit.txt`). PyRate run directories (MCMC logs) stay on
`deep-server` under `results/e2/runs/`; their inputs, truths and summaries
are committed here. Wall time on 23 October: generators 62 min and divDyn
1 min on 12 cores; PyRate 3 h 50 min as 12 parallel jobs.

# Tranche 2: the stratigraphic filter and extinction dates

Run on `deep-server` on 24 October 2026 (`run_t2.sh`, tmux, 12 cores, about
7 minutes). Tests declared in [VALIDATION_T2.md](VALIDATION_T2.md) before
running (`74892e4`); amendment A1 records the changes made after a 24-case
smoke run, and A2 the rerun and post-hoc additions after an independent
review (Claude Sonnet subagent), whose findings are applied here. Results in
`results/t2/`; follow-up checks in `results/t2/t2_checks.json`.

## Results: stratigraphic tools

| Test | Tool | Result | Key numbers |
| --- | --- | --- | --- |
| S1 round trip height ↔ time | admtools 0.7.0 | **fail** | 3,972 of 8,282 deposited times return wrong, by up to 2.0 and 3.0 Myr (the two hiatus durations): every time in the two segments directly above the hiatuses. Dense model (tie points every 0.01 Myr): 6 of 8,282 wrong, but by up to 2.7 Myr just above a hiatus, so the declared expectation of an error bounded by the spacing also fails |
| S2 hiatus accounting | admtools | **pass** | 17.18% of times in hiatus vs 16.67% (z = 1.38); completeness 25/30 and hiatus durations exact |
| S3 constant accumulation | admtools | **pass** | exact |
| S4 Poisson point process | StratPal 0.7.1 `p3` | **pass** | mean 19.96 vs 20 (z = −1.40); variance ratio 1.001; KS p = 0.35 |
| S5 thinning | StratPal `thin` | **pass** | retained 0.2995 vs 0.3 (z = −0.49); linear retention KS p = 0.21 |
| P1 time-averaged mixture | paleoAM 1.0.1 | **pass** (self-consistency only) | 17 species above 1%; max \|z\| = 2.57 (declared < 3.5); but `simMixedAssemblageSample` calls `getTimestepAbundances` and subsamples, so this checks only the subsampling (A2) |

`strat_to_time` fails because `get_time.adm` interpolates with
`stats::approx(..., ties = list("ordered", min))`: the two tie points at a
hiatus height collapse to the hiatus start, so heights above the surface are
interpolated from the wrong time. `hiat_mode = "end"` errs below hiatuses
instead, a segment between two hiatuses is wrong in both modes, and
`"destroy"` returned `NA` for every height on the S1 model
(`t2_checks.R`). `time_to_strat` is correct. The code dates from 2023.
StratPal's `last_occ` ends with `strat_to_time`.

## Results: extinction dates

2,000 extinct species with at least three fossils (two seeded paleobuddy
clades; λ 0.3, μ 0.2, ψ 1.0). Arm B keeps 1,272 species with at least three
fossils outside the hiatuses. Arm C is the A2 rerun with independent
dating errors (the first arm C was invalid: `griwm` resets the random
stream). Coverage of the true extinction time:

| Method (scored as declared) | A: ideal | B: hiatuses | C: dating error |
| --- | --- | --- | --- |
| Strauss–Sadler, `tbea` (95% one-sided) | **0.948** | 0.884 | 0.953 |
| Strauss–Sadler, EDE | **0.950** | 0.886 | 0.955 |
| Robson & Whitlock, EDE (95% one-sided) | 0.955 | 0.921 | 0.959 |
| OLE, EDE (95% two-sided) | 0.610 | 0.496 | 0.552 |
| Solow 1993, EDE (estimate as bound; scored cases) | 0.933 | 0.831 | 0.939 |
| McInerny 2006, EDE (same) | 0.866 | 0.701 | 0.878 |
| Burgman 1995, EDE (same) | 0.752 | 0.523 | 0.811 |
| GRIWM interval, biased / unbiased | 0.009 / 0.003 | 0.002 / 0.005 | 0.689 / 0.682 |
| `agnostic` 95% bin (never reaching 0.95 counted as covered) | 0.990 | 0.997 | 0.991 |
| Marshall 1994, `tbea` | no upper bound for any case | same | same |

Post hoc (A2):

| Score | A | B | C |
| --- | --- | --- | --- |
| Solow / McInerny / Burgman, a missing estimate read as "not inferred extinct" | 0.950 / 0.885 / 0.851 | 0.886 / 0.767 / 0.694 | 0.955 / 0.896 / 0.889 |
| GRIWM biased median read as a 95% bound | 0.672 | 0.528 | 0.743 |
| `agnostic`, cases whose posterior reaches 0.95 (number) | 0.970 (639) | 0.986 (218) | 0.973 (657) |

E4's coverage criteria pass: both Strauss–Sadler implementations lie in the
99% binomial band [0.937, 0.962]. Its agreement criterion fails: 91.0% of
bounds agree within 0.02 Myr against the declared 99%. Two causes, both
characterised:
- EDE works in 0.01-Myr units (A1);
- EDE's `strauss1989` uses distinct sighting times (`unique()` in its
  source), so when two fossils share a unit it uses n − 1.
On identical discretised input the two agree exactly in 97.35% of cases. In
the other 53 the inferred sample size is n − 1 (52 cases) or n − 2 (1).
**E4 therefore fails as declared**, on a convention, not a formula error.

## What tranche 2 found

- **Strauss–Sadler and Robson–Whitlock are calibrated under homogeneous
  sampling**, at every fossil count tested (3–5, 6–10, more than 10), and
  with 0.25-Myr dating errors (0.953 and 0.959).
- **Hiatuses near the extinction degrade them.** In arm B, Strauss–Sadler
  coverage is 0.943 when the extinction falls away from a hiatus, 0.829 when
  it falls inside one and 0.838 within 1 Myr after one. Losing fossils to
  the hiatuses already lowers coverage for the same species: in arm A they
  score 0.955, 0.921 and 0.939. The paired effect of the hiatuses is
  therefore about −9 and −10 points in the two hiatus classes (fossil counts
  fall from 7.6 to 5.0 on average). This is one design, with 40% of the
  time in hiatuses.
- **EDE's OLE interval covers far below nominal:** 0.42 with 3–5 fossils,
  0.81 with 6–10, 0.89 above 10. Its misses are symmetric: the truth falls
  below the interval in 23.9% of the 1,988 scored cases and above it in
  24.5%, and the lower limit lies above the last fossil in 96%. This is EDE's
  implementation of the Roberts–Solow interval with k = all sightings; we
  have no second implementation to compare.
- **Solow's test is calibrated once its missing estimates are read
  correctly (post hoc).** Its 506 missing estimates in arm A come from
  species whose last fossil is close to the present (median 2.2 Myr, against
  9.5 Myr for the scored ones): the test never rejects persistence before the
  present. Counting those as "not inferred extinct", coverage is 0.950.
  McInerny reaches 0.885 and Burgman 0.851.
- **GRIWM's 2.5–97.5% interval is the spread of its estimate under dating
  error, not an interval for the extinction time.** With negligible dating
  error it covers the truth under 1% of the time; with 0.25-Myr errors,
  0.69. Its unbiased median has the lowest median scaled absolute error of
  the methods run (0.117 of the observed range in arm A), but a
  median-unbiased Strauss–Sadler point, last + R(2^{1/(n−1)} − 1), is
  essentially as good (0.123) and better on root-mean-square error
  (0.862 against 0.914 Myr), and is closer to the truth in 55% of paired
  cases against GRIWM's 48% (both compared with EDE's Strauss–Sadler
  estimate). 62% of GRIWM's unbiased estimates fall before the truth.
- **`agnostic` (prior 0.5) is conservative, partly by construction of the
  score:** 67% of arm-A cases never reach a posterior of 0.95 and count as
  covered; among the 639 that do, coverage is 0.970 (0.995 under the
  declared wording, which allows the extinction's own bin). Its posterior
  is below the observed fraction extinct in every decile (0.16 → 0.63;
  0.86 → 0.945): underconfident, as expected for all-extinct species under a
  prior of 0.5. The decile pairs are dependent; this is a characterisation.
- **Marshall (1994) in `tbea` gave no upper bound for any case.** Its upper
  bracket needs at least 110 gaps (111 fossils) at quantile 0.95 and
  confidence 0.95 (`t2_checks.R`); the largest record here has 30.
- **Two tools reset or break the caller's state.** `griwm` calls
  `set.seed()` inside its loop, which invalidated our first arm C; and
  `agnostic.R` fails under R ≥ 4.3 when `total` is supplied.

# Tranche 3: data preparation and palaeogeography

Run on `deep-server` on 24 October 2026 (`run_t3.sh`, tmux, about 40
minutes, most of it downloading snapshots and pacing PBDB requests). Tests
declared in [VALIDATION_T3.md](VALIDATION_T3.md) before running (`ec37fab`);
A1 records the changes made after smoke runs and before the full run, and A2
the post hoc checks after an independent review (Claude Sonnet subagent),
whose findings are applied here. Read-only inputs from the data catalogue's
mirror: the public PBDB snapshot, the plate models and the ICS chart tables.
Results in `results/t3/`; post hoc checks in `t3_checks.json` and
`t3_checks_r.json`.

## Results

| Test | Tool | Result | Key numbers |
| --- | --- | --- | --- |
| V1 `bin_time` mid, majority | palaeoverse 1.5.0 | **pass** | mid: 20,000 of 20,000 agree with independently computed bins; majority: 19,983 of 19,983 (17 exact two-bin ties excluded) |
| V2 `bin_time` random | palaeoverse | **pass** | equal draws among overlapped bins, χ² p = 0.40 (10,273 occurrences, 200 replicates) |
| V3 `bin_time` point | palaeoverse | **pass** | draws in proportion to overlap, χ² p = 0.51 |
| V4 `tax_range_time` | palaeoverse | **fail** (rounding) | FAD and LAD within 0.0005 of the truth; the function rounds to three decimals |
| V5 `GTS2020` table | palaeoverse | reported | equals chart v2020/01 at 59 of the 60 stages that table covers (Priabonian 37.71 against 37.8); differs by more than 0.001 Myr from chart v2024/12 at 61 of 97 stages with printed values (including 0.01 rounding cases; largest Barremian 129.4 against 125.77, Fortunian 541 against 538.8) |
| V6 `palaeorotate` vs pyGPlates | palaeoverse | **pass** for MERDITH2021, PALEOMAP, MATTHEWS2016_pmag_ref; **fail** for TorsvikCocks2017 | point method within 0.00007° of pyGPlates for every point–age of the three models; grid method median 0.37–0.38° (grid snapping), 98% of returned values within 1°, but no value for 40–56 point–ages the Web Service reconstructs (2.6–3.6%); TorsvikCocks2017: a rigid frame offset (below) |
| F1 `check_taxonomy` | fossilbrush 1.0.6 | **fail** (misspellings) | conflicts 30 of 30 and formatting 10 of 10; misspellings 26 of 30, the four misses all beyond the default Jaro–Winkler threshold (0.104–0.179 against 0.1); one false synonym pair among clean names |
| F2 `flag_ranges` | fossilbrush | **fail** (bugs) | 24 of 100 injected outliers flagged, no false flags; a numeric reading of its returned differences catches 100 of 100 |
| [Detail withheld pending disclosure to the data custodian.] | chronosphere 0.6.1 | reported | [Detail withheld pending disclosure to the data custodian.] |

## What tranche 3 found

- **palaeoverse's binning is correct for continuous ages away from bin
  boundaries**, including the length-weighted "point" draw and the
  length-blind "random" draw. At boundaries (`t3_checks.R`): `mid` returns
  `NA` when the midpoint falls exactly on one; a zero-width occurrence on a
  boundary makes `majority` and `random` stop with an error; an exact
  two-bin tie goes to the older bin under `majority`.
- **palaeorotate's Web Service route and pyGPlates agree to 0.0001° for
  three models**, as they should on the same model files (a consistency
  check, not independent rotation code). The grid route's error is the
  present-day distance from a point to its cell centre (median 0.38°), which
  rotation preserves, except near plate boundaries (up to 56°), and the grid
  returns nothing for 2.6–3.6% of point–ages.
- **TorsvikCocks2017 differs between routes only by its absolute frame.** A
  single rigid rotation per age maps the pyGPlates positions onto the Web
  Service's with residual at most 0.00007°: rotation angles 3.1°, 9.6°,
  2.5°, 22.0°, 7.0° and 28.0° at 10, 50, 100, 200, 300 and 400 Ma, with the
  pole at 0°N 169°W from 200 to 400 Ma. Relative plate motions are
  identical. Separately, the mirror's TorsvikCocks2017 "StaticPolygons" layer
  is the terrane file (byte-identical to its Coastlines layer), so 49 of the
  300 points get no plate. The Web Service and the Jones & Domeier grids
  share one frame; which frame the Plate Model Manager's rotation file
  (`Torsvik_Cocks_HybridRotationFile.rot`) is in, and why they differ, is
  unresolved.
- **Plate-model choice moves palaeolatitudes by degrees.** Across
  MERDITH2021, PALEOMAP and MATTHEWS2016_pmag_ref the same collections
  spread by a median 2.9° at 10 Ma, 4.3–5.7° from 50 to 300 Ma and 13.6° at
  400 Ma (90th percentiles 5.0–19.5°); holding the 194 points
  reconstructable at every age fixed changes little (`t3_checks.json`). The
  four-model figures in `v6_summary.json` include TorsvikCocks2017's frame
  offset and should not be used.
- **fossilbrush's `flag_ranges` has two bugs.**
  - It compares its differences with `flag.diff` as text, because they
    start as copies of a character vector. At `flag.diff = 5`, a difference
    is flagged only if its leading digit is 5–9 (5–9.99, 50–99.99,
    500+); 10–49.99 and 100–499.99 are never flagged. The text-comparison
    prediction matches all 100 injected flags. The 24% is a property of the
    injected 10–30 Myr shifts, chosen after the smoke run had shown the bug,
    not an estimate for real data.
  - It measures occurrences beyond the LAD from the reference FAD. The
    returned LAD difference equals the true excess plus the taxon's range.
- **fossilbrush's spell check is threshold-limited, not broken.** All four
  missed misspellings exceed the default Jaro–Winkler distance of 0.1, and
  the check compares only names in the same family with the same first
  letter; `jw` is tunable. Ten of the eleven extra pairs it reported pair our
  injected format errors with their source names, which is a correct catch.
- [Detail withheld pending disclosure to the data custodian.]

# Tranche 4: richness estimators on spatially structured records

Run on `deep-server` on 24–25 October 2026 (`run_t4.sh`, `run_t4b.sh`,
`run_t4c.sh`, tmux). The R estimators take under a minute per scenario,
the geometric Weibull fits about an hour in all, and DeepDive's training
DD_HOURS. Tests declared in [VALIDATION_T4.md](VALIDATION_T4.md) before
running (`64d7818`), after a generator-only pilot disclosed there. The
amendments: A1, smoke-test fixes; A2, post hoc K2 variants when SQS
missed its quorum; A3, DeepDive scored against its own label definition;
A4, DeepDive's prior-window strata and a per-dataset arm; A5, after an
independent review, a collection-size scenario, an evenness dose–response
and Alroy's geometric Weibull (his CEGS model; that it is the 2026 paper's
geometric Weibull is our inference); A6, after a second review, a null
control, quorum 0.8 and an abundance-family robustness arm. Each was
declared before it ran. Results in
`results/t4/`.

The generator is independent of every estimator: paleobuddy birth–death
(400 starting species, λ = μ = 0.05), eight areas in a row with contiguous
species ranges, fixed lognormal abundances, and Poisson collections of 40
individuals per area and bin. Scenarios, 20 replicates each:
- **S**: the number of collections falls 70% at 50 Ma; evenness fixed.
- **C**: the number of collections is fixed; each shrinks from 40 to 12
  individuals at 50 Ma.
- **E**: effort fixed; evenness falls (σ of log abundance 0.5 → 2), with
  doses at 0.75, 1 and 1.5 sharing E's seeds.
- **M**: 60% of species die at 50 Ma, then recovery (true drop −0.78 in
  log richness, bins 11–12 against 9–10).

True richness is flat in expectation in S, C and E. "Bias" is the log
ratio of mean estimates in the late half (bins 11–20) to the early half,
minus the true log ratio: 0 is perfect, −0.69 a spurious halving.

## Results

| Estimator | S: fewer collections | C: smaller collections | E: late σ 0.75, 1, 1.5, 2 (early 0.5) | M: drop error | Error against global richness (median abs. log) |
| --- | --- | --- | --- | --- | --- |
| raw (sampled in bin) | −0.37 | −0.33 | −0.03, −0.08, −0.26, −0.49 | +0.10 | 0.24–0.50 |
| range-through (divDyn) | −0.27 | – | σ 2 only: −0.40 | +0.10 | – |
| Chao2 (divDyn; iNEXT agrees within 0.01) | −0.15 | −0.15 | −0.01, −0.04, −0.16, −0.31 | +0.04 | 0.14–0.31 |
| squares (divDyn) | −0.15 | −0.12 | −0.01, −0.04, −0.15, −0.31 | +0.04 | 0.18–0.36 |
| SQS q = 0.6 (divDyn) | K2 **not met** (2 bins below quorum; post hoc +0.03) | K5 **fail**, −0.12 | −0.07, −0.17, −0.41, −0.70 | +0.11 | relative only |
| iNEXT coverage 0.6 | K2 **pass**, +0.03 | K5 **fail**, −0.13 | −0.08, −0.19, −0.45, −0.76 | +0.11 | relative only |
| geometric Weibull (`cegsML`), occurrence frequencies | +0.03 | +0.09 | −0.01, −0.02, −0.06, −0.12 | −0.01 | 0.06–0.10 |
| geometric Weibull (`cegsML`), pooled individual counts | +0.06 | +0.11 | +0.03, +0.07, +0.21, +0.46 | −0.05 | 0.06–0.15 |
| DeepDive | DD_ROW |

Standard errors of the biases are 0.007–0.046 (20 replicates). "Global"
richness counts every species alive at any time in a bin, including the
9–11% that live only in areas without collections; against the
identifiable target, richness in the sampled areas, the median absolute
log errors are 0.036–0.077 (geometric Weibull, occurrence frequencies),
0.06–0.15 (Chao2) and 0.10–0.18 (squares). K1 (divDyn squares against
Alroy's formula): identical, **pass**, a check that the formula is
transcribed, not of the estimator. K3: both Chao2 implementations equal
re-implementations of their own formulas (to 5 × 10⁻¹³ and 5 × 10⁻⁴)
and differ from each other by a median 0.2% (range −1.9% to +9.4%, the
extreme in a thin bin). K4 (Alroy's package on counts drawn from its own
model): **pass**, median log(R̂/R) −0.03 and −0.01; it has no
occurrence-frequency analogue. `cegsLD` matched `cegsML` where run (S, E,
M).

## What tranche 4 found

- **On this generator, the geometric Weibull fitted to occurrence
  frequencies had the lowest absolute error of the estimators run, but it
  does not pass on the declared terms.** Against sampled-area richness
  its median error was 0.036–0.077, against Chao2's 0.06–0.15, and it was
  closer than Chao2 in 49–80% of bins (49% at the smallest evenness dose).
  Its trend bias stayed inside ±0.10 except under the strongest evenness
  change (−0.118, SE 0.021), and it has its own, smaller dose–response
  (−0.01, −0.02, −0.06, −0.12; about a sixth of SQS's). Its 90–98%
  recovery of global richness comes partly from overshooting sampled-area
  richness by 3–10%. It failed to fit 4 of the 400 bins of scenario S
  (all with 14 or fewer collections), which were dropped from its means;
  keeping the truth to the same bins changes the bias by 0.001.
- **Its ranking held across abundance families; its size did not (A6, 20
  replicates per condition).** Under scenario S's effort fall with gamma
  (log-series-like), log-uniform or Pareto abundances, or variable
  collection sizes, at about 77 or 30 collections per bin early, it had a
  lower median error against sampled-area richness than Chao2 in all ten
  conditions, but by margins from a near tie (Pareto: 0.19 against 0.20)
  to large (log-uniform: 0.14 against 0.32), and under gamma abundances
  both were poor (0.40–0.43 against 0.58–0.66). Its trend bias stayed
  within −0.11 to +0.06 except for Pareto abundances at low effort
  (−0.47, worse than Chao2's −0.27). With about 9 collections per bin late
  it failed to fit 22–31% of bins (`results/t4/t4_rob.json`).
- **This is not a test of Alroy's (2026) method as published.** The input
  that worked, collections per species, is not the paper's; on pooled
  individual counts, the paper's kind of input, it overshot as evenness
  fell (+0.46 at σ 2). Which variant the paper used (`cegsML`, `cegsLD` or
  `cegsB`; we ran the first two) is not known.
- **The bias statistic is calibrated.** K6, with nothing changing (late σ
  left at 0.5): every estimator within 0.014 of zero, **pass**.
- **Coverage standardisation corrected fewer collections fully and smaller
  collections mostly.** Fewer collections of the same size: SQS and iNEXT
  +0.03, within ±0.10 (SQS's +0.034 is 2.4 SE above zero). The same number
  of collections, each a third the size: −0.12 and −0.13, outside ±0.10 by
  about 1.5 SE (K5 fail), though still removing about 64% of the raw
  artefact (raw −0.33). At q = 0.8 the collection-size bias fell to −0.07
  and −0.08, inside ±0.10, but 71 low-effort bins of scenario S could not
  reach the quorum and iNEXT extrapolated 59. Across the four abundance
  families and variable collection sizes, both kept the fewer-collections
  trend within about ±0.13, the property they are designed for, though SQS
  failed in up to 36% of bins at low effort.
- **Coverage standardisation responds to evenness by degrees, at the
  quorum tested.** At q = 0.6 (native coverage 0.85–0.97, so a strong
  rarefaction), as the late-half σ rose from the early 0.5 to 0.75, 1, 1.5
  and 2 with richness flat, SQS moved −0.07, −0.17, −0.41 and −0.70, and
  iNEXT slightly more, worse than raw richness at every dose. At q = 0.8
  the response was smaller but of the same kind (SQS −0.05, −0.13, −0.32,
  −0.58). Alroy (2026; [LEADS](../LEADS.md) L-006) reaches the same
  conclusion by other tests; this is consistent with it, not a
  replication.
- **Chao2 and squares are biased by every change, by 0.4–0.64 of raw
  richness's bias**, and underestimate global richness by 15–30%.
- **Thin bins fail differently.** In one replicate two bins had 4 and 7
  collections: divDyn's SQS returned NA with no warning or message; iNEXT
  extrapolated 4.5× beyond the sample and returned 281 species from 86
  observed, with a warning that a loop or `mclapply` easily loses; `cegsML`
  returned NA for both, silently, as it did for two other thin bins.
- **divDyn** stops on integer taxon IDs in SQS and reads them as
  abundances in `indices()`; its Chao2 uses (S − 1)/S where Chao's has
  (T − 1)/T: a median +0.14% and 99th percentile +2.4% here, but +25% in
  the bin with 4 collections.
- DD_FINDINGS
