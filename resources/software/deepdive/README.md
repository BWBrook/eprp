---
id: deepdive
name: DeepDive and DeepDiveR
kind: python-package
domain: diversity-rates
languages: [Python, R]
home: https://github.com/DeepDive-project/deepdive
repo: https://github.com/DeepDive-project/deepdive
paper: [10.1038/s41467-024-48434-7, 10.1111/2041-210x.70070]
licence: "LGPL-2.1 (repository LICENSE files); DeepDive's setup.py declares AGPL-3.0: conflicting"
release: {version: "DeepDive v.1.0.28 (commit 58a6865, 2026-02-01); DeepDiveR 0.1.0 (GitHub b1592de)", date: 2026-02-01, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-08-23, checked: 2026-10-23}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: "../bench/env/Dockerfile.py4 (DeepDive); ../bench/env/Dockerfile.r4 (DeepDiveR)", image: "eprp-sw/bench-py4:t4 (sha256:8d46a3a1…); eprp-sw/bench-r4:t4 (sha256:d0c1c51a…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-017, Q-032, Q-018, Q-045, B-009, Q-013]
entry: {created: 2026-10-24, updated: 2026-10-25, by: Claude (Opus 5.5), reviewed: "Claude Sonnet subagents: design 24 Oct 2026 (A4 applied), results 25 Oct 2026 (findings applied)"}
---

# DeepDive and DeepDiveR

## Summary

DeepDive estimates richness through time by simulation-based inference: it
simulates clades and their fossil records across regions, trains a
recurrent neural network to map summaries of a fossil record to the true
richness per time bin, and applies the trained network to empirical data.
DeepDiveR is its R front end: it turns an occurrence table into DeepDive's
input file and writes the `.ini` configuration that drives simulation,
training and prediction. It is designed for total richness, including
unsampled species and regions, in records with regional structure that a
simulator can be tuned to. On the tranche-4 known-truth records, without
a present-diversity anchor, it held a trend through a fall in collections
(+0.10, just inside ±0.10) and tracked a mass extinction, but it
overestimated richness in every bin of the effort and mass-extinction
scenarios (by 24–76% on average), and under an evenness change it
overestimated the older bins and underestimated the recent ones, a
spurious decline of −0.58. Tuning it to each record did not fix either.
Use it beside per-bin estimators, not alone, and only with the
configuration fixes below.

## Method

Each training simulation draws a birth–death history (rate shifts, mass
extinctions, mass radiations, diversity dependence, with prior
probabilities set in the config), spreads species over regions with
dispersal, and samples localities and occurrences per region and bin with
heterogeneous, time-varying rates. Features per bin are global counts
(sampled species, occurrences, localities, singletons, endemics,
range-through richness, bin duration) and per-region counts of species,
occurrences and localities. Two bidirectional LSTM layers (64, 32 units)
and two dense layers (64, 32) predict log(1 + richness) in every bin,
trained by mean squared error with early stopping (patience 10, 20%
validation). Autotune sets most simulation priors from the empirical
input: localities per region and their trend, occurrence totals, the
fraction of singletons, gaps, carrying capacity and, when asked, starting
richness. Present-day richness, if known, can condition the simulations
and enter as a feature.

## Install

- DeepDive: `pip install git+https://github.com/DeepDive-project/deepdive@v.1.0.28`
  (not on PyPI; the PyPI name `deepdive` is an unrelated package). The
  benchmark image ([Dockerfile](../bench/env/Dockerfile.py4)) pins
  TensorFlow 2.15.1 (Keras 2), numpy < 2 and pandas < 2.3 and installs
  DeepDive without its dependencies, because the three dependency
  specifications at v.1.0.28 disagree: `setup.py` asks for TensorFlow
  ≥ 2.8 unpinned, so pip installs the latest; `requirements.txt` pins
  TensorFlow ~2.8, which needs Python ≤ 3.10 against the README's
  3.10–3.12; and `main` has since moved to TensorFlow ≥ 2.18 with Keras 3.
- **A plain install of v.1.0.28 cannot train a model today.** pip
  resolves TensorFlow 2.21.0, Keras 3.15.1, numpy 2.4.6 and pandas 3.1.0
  (24 October 2026; [Dockerfile](../bench/env/Dockerfile.py4plain)). The
  simulations run, then `build_rnn` stops: Keras 3 rejects the layer sizes,
  which DeepDive passes as numpy integers ("Received an invalid value for
  `units`, expected a positive integer. Received: units=64"). With
  TensorFlow 2.15.1 the same config trains and predicts.
- DeepDiveR: `remotes::install_github("DeepDive-project/DeepDiveR")`, here
  at commit `b1592de` (DESCRIPTION version 0.1.0; the GitHub release is
  tagged v.1.0) in the tranche-4 R image
  ([Dockerfile](../bench/env/Dockerfile.r4)), with ConfigParser, R6 and
  dplyr from CRAN.
- Compute: the default 10,000 training simulations (plus 112 test
  simulations) took 5.0–6.0 h of wall-clock per model on 16 cores of
  `deep-server` at `nice 10`, with the host at a load of 48–55 of 64
  cores; that is about 28–34 s per simulation per core. Early stopping
  came after 30–57 epochs; training and prediction take minutes.

## Validation

Tranche 4 ([bench/VALIDATION_T4.md](../bench/VALIDATION_T4.md); A1, A3 and
A4 cover DeepDive): records from an independent generator (paleobuddy
birth–death, eight areas with contiguous ranges, lognormal abundances,
Poisson collections), 20 replicates per scenario, with known richness per
bin. DeepDive had no pass criterion; everything here is characterisation.
Configuration: DeepDiveR `create_config` defaults with autotune, except
`extant_sp = "0 inf"` and `s_species = NA` (A1; the second was chosen
after a smoke run showed the default prior could not reach the
generator's starting richness, which we knew), with no present-diversity
anchor; one model per scenario autotuned to replicate 1 (the shared arm),
and, as DeepDive intends, a model autotuned to and trained on each of
replicates 2–4 (the per-dataset arm, A4). Bias is the error in the log
ratio of the late half (bins 11–20) to the early half; 0 is perfect.

| Scenario | Shared model, 20 replicates: trend bias | Mean log ratio to global richness; to DeepDive's own label | Median abs. log error, global | Replicates 1–4: shared; per-dataset; Chao2 |
| --- | --- | --- | --- | --- |
| S: collections fall 70% | +0.10 (SE 0.014) | +0.57; +0.73 | 0.57 | trend +0.10; +0.11; −0.15. Level +0.55; +0.65; −0.29 |
| E: evenness falls (σ 0.5 → 2) | **−0.58** (SE 0.016) | +0.13; +0.30 | 0.30 | trend −0.58; −0.47; −0.33. Level +0.17; +0.32; −0.31 |
| M: 60% extinction at 50 Ma (true drop −0.78) | drop error +0.04 (SE 0.025) | +0.21; +0.39 | 0.22 | drop error +0.07; +0.17; +0.06. Level +0.25; +0.32; −0.19 |

All headline numbers were recomputed independently by the reviewer, who
also confirmed that our pipeline reproduces DeepDive's own predictions
(to 5 × 10⁻⁸) and that the features it reads equal our occurrence files
exactly, so the results are DeepDive's behaviour, not an artefact of the
harness.

- **By period.** The mean log ratio to global richness was +0.51, +0.56
  and +0.63 in bins 1–4, 5–16 and 17–20 of S (no bin below the truth);
  +0.20, +0.22 and +0.21 in M (7% of bins below); and +0.43, +0.14 and
  −0.19 in E, where 19 of 20 replicates underestimate the last four bins.
- **Error on its own simulations is not a guide.** On its 112 test
  simulations DeepDive's mean squared error in log(1 + richness) was
  0.14–0.21 (shared) and 0.15–0.24 (per-dataset) with almost no bias
  (−0.04 to +0.08 for richness 300–1,000); on our records, against its own
  label, it was 0.55, 0.20 and 0.17 (S, E, M), almost all bias (S +0.73,
  SD 0.14; M +0.39, SD 0.13).
- **Prior window.** Autotune confines every training simulation to within
  a factor 1.2 of the tuning record's occurrence total, and only 17, 11 and
  2 of 20 replicates (S, E, M) fall inside; 16 of S's 17 inside also exceed
  `maximum_localities_per_bin`. Stratifying by the window left the trend
  unchanged (S +0.10 inside, +0.11 outside; E −0.575 in both; M drop +0.07
  inside, from two replicates, +0.04 outside), but not the level or rank
  agreement in E (mean log ratio +0.07 inside, +0.21 outside; Spearman
  median 0.71 and 0.05). The strata have little power.
- **Per-dataset tuning (n = 3 refits per scenario, one training run each,
  so tuning effects and run-to-run noise cannot be separated).** All three
  E refits reduced the spurious decline (by 0.09–0.21) and all raised the
  level error; the M refits were no better on the drop (+0.17 against
  +0.07 for the shared model on the same replicates; difference +0.13,
  SE 0.06); the S refits held the effort trend (+0.11 against +0.10) and
  raised the level error (+0.65 against +0.55). In no scenario did tuning
  to the record fix the level bias.
- **Cause (consistent with the evidence, not tested).** Our records are
  much more completely sampled than most of DeepDive's autotuned prior: in
  its training simulations the median ratio of sampled to true richness
  was 0.30–0.37, and 7–14% of bins exceeded 0.7, against 0.71–0.89 in
  ours; training simulations matched to replicate 1's sampled richness and
  occurrences have true richness 1.6–1.8 times ours (reviewer's
  exploratory check). Under the evenness change, its error tracks sampled
  richness almost one for one (slope 0.98 of error on log sampled/true
  richness, R² 0.70), and the scenario lies outside its simulator, whose
  per-species sampling rates are fixed through time, so E is a
  misspecification test.
- Spearman correlation with true richness across bins (median 0.47, 0.63,
  0.87) is uninformative in S and E, where the truth is flat in
  expectation; it was similar for every estimator.

## Strengths

- Held the trend through a fall in the number of collections (+0.10, just
  inside the ±0.10 used for the coverage methods, though 7 SE from zero;
  Chao2 −0.15, raw richness −0.37) and tracked the mass-extinction drop
  (+0.04, as Chao2 and squares did).
- Targets total richness, including unsampled regions, by design, and uses
  regional structure that the per-bin estimators ignore.
- The whole pipeline (simulate, train, predict) runs from one `.ini`
  file, and DeepDiveR writes both the input and the config.

## Weaknesses and pitfalls

- **Level bias.** Without a present-diversity anchor it overestimated
  every bin of S and nearly every bin of M (mean log ratio +0.57 and
  +0.21 to global richness), and more against its own label definition,
  so this is not a matter of what counts as "alive in a bin". Its absolute
  error (0.22–0.57) was comparable to raw richness's (0.29–0.50) and larger
  than Chao2's (0.17–0.31) or the geometric Weibull's on occurrence
  frequencies (0.06–0.10). Supplying present diversity, which DeepDive is
  designed to use and our generator records, was not tested.
- **It read an evenness change as a decline**: −0.58 with richness flat,
  between Chao2 (−0.31) and SQS (−0.70), overestimating early and
  underestimating late. Per-dataset tuning, its intended use, reduced this
  to −0.47 on four replicates and raised the level error, as it did in S
  and M.
- **The default prior cannot start a window on a diverse clade.**
  DeepDiveR's `s_species = 1` with `root_r` at 80–100% of the span starts
  every training clade from one species. In 80 training simulations of the
  default prior (reviewer's rerun) the oldest bin never held more than 5
  species and 78% held none, and the third-oldest at most 110, against
  about 490 in our records. Set `s_species = NA` so autotune draws the
  starting richness. The default arm was not itself scored against truth.
- **Without present diversity, the DeepDiveR config crashes DeepDive
  1.0.28**: `extant_sp` stays `NA` and is parsed as a number; `0 inf` (the
  simulator's own default) works.
- **A plain install fails at training** under Keras 3 (above); pin
  TensorFlow 2.15.
- DeepDiveR's README asks for an `Area` column; `prep_dd_input` requires
  `Region`.
- Under DeepDiveR's defaults the output is a point prediction (one model,
  no dropout, one age replicate), so there is no interval to check.
- Each record DeepDive is meant to be tuned to costs one 5–6 h fit on 16
  cores (about 90 core-hours of allocation); the intended use across 20
  replicates of three scenarios would take about 5,000 core-hours, a
  kunanyi-scale job.
- Queued for the authors as CONTACTS (queue held back) S12.

## Alternatives and overlap

Per-bin estimators on the same records: Chao2 and squares (divDyn, iNEXT),
SQS and coverage-standardised richness (divDyn, iNEXT), and Alroy's
geometric Weibull ([alroy-richness](../alroy-richness/README.md)), which
had a fraction of DeepDive's absolute error and a smaller evenness bias
on these records. PyRate estimates diversity trajectories from
occurrence-level ranges in continuous time ([pyrate](../pyrate/README.md)).

## EPRP relevance

The only tool here that targets total richness with regional structure,
which Q-040 and Q-042 need, but on these records, unanchored, it
overestimated it and misread an evenness change. It should not be the sole estimator in any
EPRP analysis; beside the geometric Weibull and Chao2 it adds a
model-based check that fails differently (lead N-002). The register already
cites DeepDive's published net-decline estimate for Q-042 (landscape row).

## Citation and licence

Cooper, R. B., Flannery-Sutherland, J. T. and Silvestro, D. (2024).
DeepDive: estimating global biodiversity patterns through time using deep
learning. *Nature Communications* 15, 4199. doi:10.1038/s41467-024-48434-7.
Cooper, R. B., Allen, B. J. and Silvestro, D. (2025). DeepDiveR—A software
for deep learning estimation of palaeodiversity from fossil occurrences.
*Methods in Ecology and Evolution* 16, 1923–1934.
doi:10.1111/2041-210x.70070. Both checked on Crossref, 24 October 2026.
Repository LICENSE files: LGPL-2.1 (both); DeepDive's `setup.py`
classifier says AGPL-3.0.

## Verification log

- 2026-10-23 `checked`: repositories, tag v.1.0.28 and licence files by
  `landscape.py`.
- 2026-10-25 `checked`: tranche-4 shared and per-dataset runs on
  `deep-server` (`bench/results/t4/`).
- 2026-10-24 `checked`: `config_runner.py`, `deepdiver_utilities.py`
  (`config_autotune`, `create_sim_obj_from_config`, `predict_from_config`),
  `utilities.py` (`parse_dd_input`, `predict`) at v.1.0.28, and DeepDiveR's
  `prep_dd_input`, `create_config` and `edit_config` at `b1592de`, read in
  the images.
