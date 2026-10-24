# Tranche 2 validation: declared tests

Declared by Claude (Opus 5.5) on 24 October 2026, before any of these tests
was run. Results go in `results/t2/`; this file is not edited after the runs
except to append dated amendments. Environment: `eprp-sw/bench-r2:t2`
([Dockerfile](env/Dockerfile.r2)): the tranche-1 R image plus StratPal
0.7.1, admtools 0.7.0, paleoAM 1.0.1, EDE 0.2.0, tbea 1.8.0 (CRAN snapshot
2026-10-22), Rextinct 1.1.0 (GitHub `FredSaltre/CRIWM` at `508d3c9`) and
Alroy's `agnostic.R` (sha256 `1eb9268f…c8db42`).

A probe before declaration found that admtools' `strat_to_time` returns
wrong times for heights between a hiatus and the next tie point
(`get_time.adm` interpolates with `ties = list("ordered", min)`, which drops
the tie point at the end of the hiatus). S1 tests this in full; the
extinction benchmark avoids that function.

## Stratigraphic tools

**S1. admtools round trip.** Age–depth model with tie points
t = (0, 4, 6, 12, 15, 21, 24, 30) Myr, h = (0, 8, 8, 14, 14, 26, 32, 38) m:
hiatuses from 4 to 6 and from 12 to 15 Myr. 10,000 times uniform on (0, 30).
Pass: for every time with a non-missing height,
|strat_to_time(time_to_strat(t)) − t| < 1e−9. Also reported: the same
round trip on a dense model (tie points every 0.01 Myr, same hiatuses),
where the error should be bounded by the spacing.

**S2. admtools hiatus accounting.** On the S1 model and times: the fraction
of times for which `time_to_strat(..., destructive = TRUE)` returns `NA`
lies within 3 binomial standard errors of the hiatus duration over the total
duration (5/30); `get_completeness` equals 25/30 and `get_hiat_duration`
5 to 1e−9.

**S3. admtools constant accumulation.** Tie points t = (0, 30),
h = (0, 60): `time_to_strat` returns 2t to 1e−9 for 1,000 times.

**S4. StratPal Poisson point process.** 20,000 draws of
`p3(rate = 2, from = 0, to = 10)`: mean count within 3 standard errors of 20;
variance ratio within 1 ± 3·sqrt(2/n); pooled times uniform (KS p > 0.001).

**S5. StratPal thinning.** `thin` of 200,000 uniform points on (0, 10):
constant retention 0.3, pooled retained fraction within 3 binomial standard
errors; retention x/10, retained points distributed with density x/50
(KS p > 0.001).

**P1. paleoAM mixing.** Gulf of Alaska KDEs and occurrence models fitted
as in the package examples (`abundanceFloorRatio = 0.5`,
`nBreaksGradientHist = 20`, `modeledSiteAbundance = 10000`). Thirty gradient
values evenly spaced over the observed range. For 200 replicates: (a) the
pooled species proportions of `getTimestepAbundances(..., specimensPerTimestep
= 10000)` over the thirty values; (b) the proportions in
`simMixedAssemblageSample(..., specimensPerTimestep = 10000, nSpecimens =
2000)`. For every species whose mean pooled proportion exceeds 0.01, the
mean of (b) minus the mean of (a) lies within 3.5 replicate standard errors
(a time-averaged sample is an unbiased mixture). Pass if all such species
do.

## Extinction-date benchmark

Truth: paleobuddy, λ 0.3, μ 0.2, 50 starting species, 30 Myr, fossils by
`sample.clade` at ψ 1.0 per lineage-Myr. Cases: the first 2,000 species
that went extinct before the present with at least three fossils, across
seeded clades. For each, the true extinction age TE and the fossil ages.
Estimators work in forward time (t = 30 − age); EDE receives sighting counts
in units of 0.01 Myr, with the present as `test_year`.

Methods and what is scored:
- `tbea::stratCI`, Strauss–Sadler (1989), one endpoint (`one.par`, the
  younger end), 95%: the bound covers TE.
- `tbea::stratCI`, Marshall (1994), `quantile = 0.95`, `confidence = 0.95`:
  the upper bracket covers TE; cases it cannot compute are counted.
- EDE `strauss1989`, `robson1964` (one-sided), `ole` (two-sided):
  their intervals cover TE.
- EDE `solow1993`, `mcinerny2006`, `burgman1995` at α 0.05: their
  `estimate` (the date by which extinction is inferred) is at or after TE.
- Rextinct `griwm`, calendar dates (`radiocarbon = 0`), with `biased = TRUE`
  (α 0.05) and `biased = FALSE`, `resample = 1000`: the 2.5–97.5% interval
  covers TE.
- `agnostic` (Alroy 2014), 1-Myr bins from the bin of first occurrence to the
  present, presence per bin, `total = 1`, prior 0.5: the first bin at which
  the cumulative posterior reaches 0.95 is at or after the bin of TE; the
  posterior's calibration (by decile) is reported.
For every method the median error of its point estimate (where it gives
one), scaled by the observed range, is reported, with results split by
number of fossils (3–5, 6–10, more than 10).

**E4. Ideal sampling (arm A).** Exact fossil times (`griwm` given
errors of 0.001 Myr). **Pass criteria:** the coverage of the Strauss–Sadler
bound from `tbea` and from EDE each lies within the 99% binomial interval of
0.95 for the number of cases; and the two implementations' bounds agree
within 0.02 Myr (two EDE time units) in at least 99% of cases. Under
homogeneous Poisson sampling the fossils of a species, given their number,
are uniform over its life, which makes the Strauss–Sadler bound exact. All
other methods are reported without pass criteria.

**E5. Hiatuses (arm B).** The arm-A fossils, removing those that fall in
hiatuses of a fixed model with six 2-Myr hiatuses (12 of 30 Myr, at
3–5, 7–9, 12–14, 17–19, 22–24 and 26–28 Ma). Times of surviving fossils are
kept exactly (the model is known). Cases with fewer than three surviving
fossils are dropped and counted. All methods are reported, split by whether
TE falls in a hiatus, within 1 Myr after one, or elsewhere. No pass
criteria.

**E6. Dating error (arm C).** The arm-A fossils with independent Gaussian
errors (σ 0.25 Myr) added to their ages; `griwm` is given σ, the other
methods the perturbed ages. All methods are reported. No pass criteria.
