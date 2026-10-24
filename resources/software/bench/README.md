# Tranche 1: a known-truth bench for rates

Validation of two fossil-record generators and three rate estimators against
known truth, run on `deep-server` on 23 October 2026. The tests were declared
in [VALIDATION.md](VALIDATION.md) and committed (`2be84d6`) before any ran;
amendment A1 records the changes made before the full run. Each tool's entry
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
| G4 cross-generator | paleobuddy vs TreeSim + FossilSim | **pass** | KS p = 0.25 (extant), 0.55 (species), 0.44 (duration), 0.56 (fossils); about 7,900 surviving clades each |
| G5 taxonomy | FossilSim `sim.taxonomy` | **pass** | originations 95,458 vs 95,677 expected, terminations 73,431 vs 73,650 (z = −1.27 each); 2,000 trees |
| E1 binned rates, complete sampling | divDyn 0.8.3 | **pass** | all ten rate columns within 0.2% of λΔ = 0.25 and μΔ = 0.20; 200 replicates × 18 bins |
| E1, Poisson sampling ψ = 0.5 | divDyn | reported | relative bias: corrected three-timer +1.2% / −0.3%; gap-filler +1.5% / +1.0%; boundary-crosser +7.9% / +0.2%; raw three-timer +482% / +385% (uncorrected by design); second-for-third −36% / −36% (unexplained) |
| E2 coverage, ψ = 1.0 | PyRate `6a27efb` | **fail (q)** | 95% intervals cover λ 95/100, μ 95/100, **q 81/100** (declared ≥ 90); median bias λ −11%, μ −12%, q +9%; all ESS ≥ 100 |
| E2, ψ = 0.25 | PyRate | reported | coverage λ 44/50, μ 40/50, q 33/50; median bias λ +6%, μ −3%, q +46% |
| E3(a) deposited coverage | skyfbdr study runs | reported | coverage over 1,000 prior draws: λ 0.932 / 0.945 / 0.954, μ 0.945 / 0.938 / 0.948, ψ 0.941 / **0.903** / 0.944 (oldest to youngest stage; 936/1,000 is the 2.5% binomial bound) |
| E3(b) rerun | RevBayes v1.4.1 | **blocked** | the range process is disabled in every release since April 2024 (A1) |

## What the bench found

- **Both generators reproduce analytic birth–death and Poisson-sampling
  truth, and agree with each other.** paleobuddy and TreeSim/FossilSim are
  independent codebases; both hit the analytic moments and their
  distributions are indistinguishable. Either can serve as truth for
  later tranches. FossilSim's taxonomy layer gives the expected
  pseudoextinction counts.
- **PyRate's preservation rate is biased high and its intervals too narrow,
  and the cause is the durations it infers for sampled species.** Two post
  hoc diagnostics (not declared tests; same seeds, so the histories are the
  E2 histories exactly):
  - `validate/pyrate_attribution.R` computes rates from true species times.
    Conditioning on clade size alone moves λ and μ by under 4%. Using only
    the sampled species gives λ −21%, μ −20%, q +6.5% at ψ = 1.0, and
    −37%, −36%, +43% at ψ = 0.25.
  - `validate/pyrate_durations.py` compares PyRate's posterior species
    times with the truth. Its inferred durations are 8% short at ψ = 1.0
    and 31% short at ψ = 0.25; singletons are inferred at 66% and 50% of
    their true durations.

  PyRate's preservation likelihood is zero-truncated (each species is
  conditioned on at least one fossil; `PyRate.py` line 3342), which would
  be exact if durations were known. The shortened durations push q up and
  the truncation pulls it down, and the posterior median lands on the naive
  estimate from true durations (1.089 against 1.065 at ψ = 1.0; 0.364
  against 0.356 at ψ = 0.25). Our reading, not yet tested: the birth–death
  prior on each species' times is not conditioned on the species being
  sampled, and sampled species are a duration-biased subset. The same
  shortening raises λ and μ, partly offsetting the missing short-lived
  species, so at ψ = 1.0 their intervals still cover at the nominal rate.
- **divDyn's binned rates are exact under complete sampling.** Under
  incomplete sampling its corrected three-timer and gap-filler rates are
  within 2% of truth. The raw three-timer is biased as theory predicts. The
  second-for-third rates are 36% low; divDyn always substitutes the median
  of the three subsequent-sampling counts, and its source comment questions
  whether that matches Alroy (2015). Do not use `ext2f3`/`ori2f3` until that
  is checked against the paper.
- **The skyline FBD-range study's own runs are close to calibrated, with
  one weak stage.** The middle-stage sampling rate is covered 90.3% of the
  time. The study rejected simulations by the number of sampled species,
  which breaks exact simulation-based calibration, so this need not be a
  fault of the likelihood. Comparing against the reversed stage order gives
  much worse coverage, confirming the index mapping.
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

The study inputs for E3(a) come from a sparse clone of
`brpetrucci/skyfbdr_simstudy` at `950b9bc`
(`results/skyfbdr-commit.txt`). PyRate run directories (MCMC logs) stay on
`deep-server` under `results/e2/runs/`; their inputs, truths and summaries
are committed here. Wall time on 23 October: generators 62 min and divDyn
1 min on 12 cores; PyRate 3 h 50 min as 12 parallel jobs.
