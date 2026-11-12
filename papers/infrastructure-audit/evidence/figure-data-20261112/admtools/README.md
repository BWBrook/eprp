# Sparse admtools curve for Figure 3A

`sparse_curve.tsv` contains all 8,282 deposited draws from C096's original
seed-901 sample, sorted by height. Of them, 3,972 have absolute time error
above `1e-9` Myr; the maximum is `2.9957765231374651` Myr. The error is
**estimated time minus true time**. The raw sample contains 10,000 draws;
the 1,718 draws in the two nondeposition intervals are excluded as in the
original replay.

Columns are `draw_index` (index in the original 10,000 draws), `height`,
`truth_time_myr`, `estimated_time_myr`, `error_myr`, and
`deposition_segment`. Heights use the synthetic model's height units.
`tie_points.tsv` preserves all eight time–height points, including repeated
heights 8 and 14. Plot segments separately to avoid drawing through the
hiatus jumps; mark those heights as vertical lines.

The extraction freshly calls `admtools::strat_to_time` in the content-pinned
R 4.6.1/admtools 0.7.0 image used on 8 November. It checks the input hash,
both recorded function hashes and the original receipt, then exports numbers
at 17 significant digits and verifies exact readback. The receipt identifies
the image, environment, inputs, script and output hashes.

From the repository root, on a host with that image:

```bash
task=papers/infrastructure-audit/evidence/figure-data-20261112/admtools
prior=papers/infrastructure-audit/evidence/replay-20261108/software
mkdir -p "$OUTPUT"
docker run --rm --network none --cpus 1 --memory 2g \
  --user "$(id -u):$(id -g)" \
  -v "$PWD/$task:/scripts:ro" -v "$PWD/$prior:/inputs:ro" \
  -v "$OUTPUT:/out" \
  sha256:44432c896c3622e92c68f11716d639745b0fa2b4d6c47124538461389f6daab6 \
  Rscript --vanilla /scripts/extract_admtools.R /out \
  /inputs/case05_admtools.json /inputs/package_environment.json
```

`OUTPUT` must be an absolute directory. The shared `../check_tables.py`
independently recomputes every true time using explicit deposition segments
and every returned time using linear interpolation through first-at-tie
knots. Both agree exactly with the saved table in this run.

This is the original sparse-model sampled curve. It is separate from the
dense model and targeted near-hiatus probes. No regular grid or additional
boundary points have been substituted for the original 8,282 draws.
