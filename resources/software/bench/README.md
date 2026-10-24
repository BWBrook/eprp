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
smoke run and before the full run. Results in `results/t2/`.

## Results: stratigraphic tools

| Test | Tool | Result | Key numbers |
| --- | --- | --- | --- |
| S1 round trip height ↔ time | admtools 0.7.0 | **fail** | 3,972 of 8,282 deposited times return wrong, by up to 2.0 and 3.0 Myr (the two hiatus durations): every time in the segment directly above each hiatus. Dense model (tie points every 0.01 Myr): max error still 0.47 Myr |
| S2 hiatus accounting | admtools | **pass** | 17.18% of times in hiatus vs 16.67% (z = 1.38); completeness 25/30 and hiatus durations exact |
| S3 constant accumulation | admtools | **pass** | exact |
| S4 Poisson point process | StratPal 0.7.1 `p3` | **pass** | mean 19.96 vs 20 (z = −1.40); variance ratio 1.001; KS p = 0.35 |
| S5 thinning | StratPal `thin` | **pass** | retained 0.2995 vs 0.3 (z = −0.49); linear retention KS p = 0.21 |
| P1 time-averaged mixture | paleoAM 1.0.1 | **pass** | 17 species above 1%; max \|z\| = 2.57 (declared < 3.5); 200 replicates |

`strat_to_time` fails because `get_time.adm` interpolates with
`stats::approx(..., ties = list("ordered", min))`: the two tie points at a
hiatus height collapse to the hiatus start, and every height above the
surface, up to the next tie point, is interpolated from the wrong time.
`time_to_strat` is correct. The code dates from 2023.

## Results: extinction dates

2,000 extinct species with at least three fossils (two seeded paleobuddy
clades; λ 0.3, μ 0.2, ψ 1.0). Coverage of the true extinction time:

| Method (scored as declared) | A: ideal | B: hiatuses | C: dating error |
| --- | --- | --- | --- |
| Strauss–Sadler, `tbea` (95% one-sided) | **0.948** | 0.884 | 0.938 |
| Strauss–Sadler, EDE | **0.950** | 0.886 | 0.939 |
| Robson & Whitlock, EDE (95% one-sided) | 0.955 | 0.921 | 0.946 |
| OLE, EDE (95% two-sided) | 0.610 | 0.496 | 0.591 |
| Solow 1993, EDE (estimate as bound; scored cases) | 0.933 | 0.831 | 0.918 |
| McInerny 2006, EDE (same) | 0.866 | 0.701 | 0.849 |
| Burgman 1995, EDE (same) | 0.752 | 0.523 | 0.754 |
| GRIWM interval, biased / unbiased | 0.008 / 0.003 | 0.002 / 0.006 | 0.706 / 0.682 |
| GRIWM biased median as a bound (post hoc) | 0.672 | 0.528 | 0.706 |
| `agnostic` 95% bin | 0.990 | 0.997 | 0.990 |
| Marshall 1994, `tbea` | not computable for any case | same | same |

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
  degrade only slightly with 0.25-Myr dating error.
- **Hiatuses near the extinction break them.** In arm B, Strauss–Sadler
  coverage is 0.943 when the extinction falls away from a hiatus, but 0.829
  when it falls inside one and 0.838 within 1 Myr after one. 728 of the 2,000
  species dropped below three fossils.
- **OLE's 95% interval covers far below nominal:** 0.42 with 3–5 fossils,
  0.81 with 6–10, 0.89 above 10.
- **Solow's test is calibrated once its missing estimates are read
  correctly.** Its 506 missing estimates come from species whose last
  fossil is close to the present (median 2.2 Myr, against 9.5 Myr for the
  scored ones): the test never rejects persistence before the present.
  Counting those as "not inferred extinct" (post hoc), coverage is 0.950.
  McInerny reaches 0.886 and Burgman 0.850 under the same reading.
- **GRIWM's 2.5–97.5% interval is the spread of its estimate under dating
  error, not an interval for the extinction time.** With negligible dating
  error it covers the truth 0.3–0.8% of the time; with 0.25-Myr error,
  about 0.7. As a point estimator the unbiased GRIWM is the most accurate
  method here: median error −0.049 and median absolute error 0.117 of the
  observed range, against 0.149 for Strauss–Sadler's estimate. Its biased
  form (α 0.05) used as a 95% bound covers 0.67.
- **`agnostic` (prior 0.5) is conservative:** its 95% bin covers 0.99. Its
  posterior is miscalibrated in both directions for these all-extinct
  species: posteriors of 0.1–0.2 correspond to 63% extinct; 0.8–0.9 to
  94%. Every case here is extinct, against the method's default prior of
  0.5, so this is a characterisation, not a test of the method.
- **Marshall (1994) in `tbea` returned no bound for any case.** With
  quantile 0.95 and confidence 0.95, its upper bracket exists only when
  0.95^N < 0.025 for N gaps, which needs at least 72 gaps (73 fossils);
  the largest record here has 30.
