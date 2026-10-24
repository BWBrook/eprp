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
tier: PENDING
validated_uses: []
environment: {route: docker, lockfile: "../bench/env/Dockerfile.py4 (DeepDive); ../bench/env/Dockerfile.r4 (DeepDiveR)", image: "eprp-sw/bench-py4:t4 (sha256:8d46a3a1…); eprp-sw/bench-r4:t4 (sha256:d0c1c51a…)", host: deep-server}
blockers: []
related_sources: [pbdb]
eprp_questions: [Q-040, Q-042, Q-017, Q-032, Q-018, Q-045, B-009, Q-013]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: not yet}
---

# DeepDive and DeepDiveR

## Summary

DeepDive estimates richness through time by simulation-based inference: it
simulates clades and their fossil records across regions, trains a
recurrent neural network to map summaries of a fossil record to the true
richness per time bin, and applies the trained network to empirical data.
DeepDiveR is its R front end: it turns an occurrence table into DeepDive's
input file and writes the `.ini` configuration that drives simulation,
training and prediction. Reach for it when the target is total richness,
including unsampled species and regions, and the record has regional
structure that a simulator can be tuned to.

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
- Compute: under the autotuned priors used here a simulation took about
  21–54 s per core, so the default 10,000 training simulations took
  TRAINING_HOURS per scenario on 16 cores of `deep-server`. Training and
  prediction are minutes.

## Validation

PENDING

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
- 2026-10-24 `checked`: `config_runner.py`, `deepdiver_utilities.py`
  (`config_autotune`, `create_sim_obj_from_config`, `predict_from_config`),
  `utilities.py` (`parse_dd_input`, `predict`) at v.1.0.28, and DeepDiveR's
  `prep_dd_input`, `create_config` and `edit_config` at `b1592de`, read in
  the images.
