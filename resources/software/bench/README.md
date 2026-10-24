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
