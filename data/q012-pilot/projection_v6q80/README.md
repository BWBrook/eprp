# Q-012 v6q80 runtime projection (local; not cluster evidence)

Claude, 19–20 October 2026. A pre-dispatch check added in 76/2099. Its
purpose is to keep a six-hour timeout from consuming the tranche's
remaining allocation. **Local runs: GCC 13 build of the same source and
patch.** The sampler path differs from kunanyi's, so this gives adaptation
outcomes and cost only. Nothing here is a fit result.

The scripts are provenance copies. They ran in place: `run.sh` from
`scratch/q012-pilot/q80_projection/` and `warm_run.sh` from its `warm/`
subdirectory, both with the binary in `scratch/q012-pilot/trace_build/`.
`setup.py` and `project.py` ran from the repository root. The raw chain CSVs
stay in scratch; their hashes are in `warm_chain_files.sha256`.

## Fixed-metric sweep (19 October)

- **Scripts:** `setup.py`, `run.sh`. **Output:** `fixed_metric_sweep.json`.
- **Setup:** P11 at Q = 80 and Q = 64, using v6p2's adapted inverse metrics
  for chains 1 and 3. Steps were 1.0, 0.8, 0.65 and 0.5 × v6p2's adapted
  steps, starting from saved draw 3,000.
- **Stopped early:** the runs were halted after 19–127 draws each.
- **Result:** at the v6p2 steps, mean acceptance (0.991, 0.995) reproduces
  v6p2's sampling means. Reaching mean acceptance near 0.999 *at a fixed
  metric* needs about 0.5–0.65 × the step, which gives depth-8 trees of
  about 250 leapfrogs.

## Four-chain warmup projection (20 October)

- **Scripts:** `warm_run.sh`, `project.py`. **Output:** `projection.json`.
- **Setup:** the real settings: Q = 80, adapt_delta 0.999, seed 77017,
  chain IDs 1–4 with their original starts, 2,000 warmup, then 200 draws.
- **Projection method:** local times are converted to kunanyi using:
  - v6p2's measured kunanyi Q = 64 cost per leapfrog (sampling phase):
    0.00538 s;
  - a Q = 80 / Q = 64 cost ratio of 1.5–1.6.
  - The machine carried other jobs during warmup, so local times are
    inflated and the projection is conservative.

| Chain | Adapted step | Sampling accept | Mean leapfrogs (depth) | Projected kunanyi hours (ratio 1.5 / 1.6) |
| --- | --- | --- | --- | --- |
| 1 | 0.0527 | 0.986 | 65 (6) | 1.71 / 1.82 |
| 2 | 0.0358 | 0.995 | 127 (7) | 2.84 / 3.02 |
| 3 | 0.0358 | 0.988 | 126 (7) | 2.87 / 3.06 |
| 4 | 0.0341 | 0.995 | 127 (7) | 2.44 / 2.60 |

- **The six-hour runner cap is not at risk** on this evidence.
- **The step-size mechanism is in doubt.** In this one local replicate,
  adapt_delta 0.999 gave adapted steps of 0.034–0.053 and sampling
  acceptance of 0.986–0.995. That is the same range as v6p2 at 0.995:
  steps 0.029–0.047, acceptance 0.988–0.996.
  - Dual averaging's final step did not shrink as the fixed-metric sweep
    implied.
  - Adapted steps vary between runs, so one replicate per chain cannot
    settle this. It does make "0.999 gives smaller steps" an untested
    assumption rather than a given.
