---
id: gen3sis
name: gen3sis
kind: r-package
domain: simulation
languages: [R, C++]
home: https://cran.r-project.org/package=gen3sis
repo: https://github.com/project-Gen3sis/R-package
paper: [10.1371/journal.pbio.3001340]
licence: GPL-3.0
release: {version: "1.6.0", date: 2025-09-01, checked: 2026-10-24}
maintenance: {state: slow, last_commit: unknown, last_push: 2025-09-01, checked: 2026-10-24}
tier: T2
validated_uses: ["one-step Weibull dispersal with one occupied cell", "speciation timing for a two-cell isolated case"]
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r5g, image: "eprp-sw/bench-r5g:t5, sha256:8fd9be36d6e178014b0d1f01ea2b27ba8af90377f604a93bb9047baae68b1310", host: deep-server}
blockers: []
related_sources: []
eprp_questions: [B-005, Q-027, Q-044, Q-029]
entry: {created: 2026-10-28, updated: 2026-10-28, by: Codex, reviewed: "G3 retained-output audit by Codex; full tranche review pending"}
---

# gen3sis

gen3sis is a mechanistic spatial eco-evolutionary simulator. It follows
populations through changing landscapes with configurable dispersal,
speciation, ecological and evolutionary rules. It is a candidate simulator
for comparing spatial diversity mechanisms; its results depend on both the
rules and the landscape supplied. The narrow checks below do not establish
that a particular palaeobiological inference is valid.

## Method and installation

The [pinned bench image](../bench/env/Dockerfile.r5g) installs gen3sis
1.6.0. Its model inputs specify landscape and distance matrices through time
and R functions governing ecological and evolutionary processes. Hagen et
al.'s deposit uses an older landscape format and gen3sis 0.9.9; the bench
converts the landscape data to the current raster representation before
running the 1.6.0 package. See [A3–A5](../bench/VALIDATION_T5.md).

## Validation and characterisation

- **G1, shipped tests: not met as declared.** Two CaseStudy1 file-hash
  expectations failed because reference and generated files have different
  line endings; their lines and the summary agree. Nine of 18 tests were
  skipped by their authors. This is a documented comparison, not a pass of
  the declared test suite.
- **G2a and G2b: pass.** In the specified synthetic cases, 4,000 one-step
  dispersal replicates agree with the Weibull survival probability within
  the declared tolerance; the isolated two-cell speciation case reaches
  two species at the expected sixth step. Receipts are in
  [`t5_gen3sis_checks.json`](../bench/results/t5/t5_gen3sis_checks.json).
- **G3: ten deposited configurations completed and audited.** The nine
  retained outputs and substitute config 22 have internally consistent
  living-species and occupancy recounts. Eight of ten final living-species
  counts match the deposit; configs 2 and 10 differ by +9 and +4. The
  original selected config 9 remains missing from the deposit and its failed
  attempt is preserved. Config 22 was selected prospectively under A5 and
  finished normally at 17:28 AEDT on 28 October after 3.483 hours. It has
  **3,003 living species**, matching the deposit, and 1,560 occupied cells
  of 1,562 habitable cells. This compares different versions and landscape
  representations, not an isolated version-effect test.

The [independent recount](../bench/results/t5/g3_retained_audit_20261028.tsv)
has the nine pairs, occupancy counts and source-object hashes; its
[script](../bench/validate/t5_g3_audit.R) reads the retained output on
`deep-server`. The corresponding deposited `fraction_colonized` and
`perc_extinction` definitions are not independently established. Equal
numbers alone do not establish that their meanings coincide.

The deposit's `numerical_values/METADATA.txt` describes the S1 simulation
summary's `occupancy` as the proportion of inhabited terrestrial sites, but
does not equate that quantity to the S3 CSV's `fraction_colonized` or define
`perc_extinction`. A targeted search of the deposited Scripts and global
case-study note found no definition of those two CSV fields. Their meanings
remain open despite the matching occupancy values.

For config 22, [input hashes](../bench/results/t5/g3_config22_input_sha256_20261028.txt)
were saved before the run; the compiled-landscape
[file manifest](../bench/results/t5/g3_config22_landscape_sha256_20261028.txt)
was captured during it. The run mounts those inputs read-only, though a
post-start manifest cannot by itself prove their state at launch.

The [single-run recount](../bench/validate/t5_g3_single_audit.R) and
[completion watcher](../bench/watch_t5_g3_22.sh) checked config 22's final
state, source hashes and unchanged landscape manifest. The
[final audit](../bench/results/t5/g3_config22_audit_20261029.tsv),
[run receipt](../bench/results/t5/g3_m1_22_20261029.csv),
[completion status](../bench/results/t5/g3_config22_status_20261029.txt) and
[audit status](../bench/results/t5/g3_config22_audit_status_20261029.txt)
were collected on 29 October. Species, landscape and summary hashes are
in the audit. The extinct fraction is 28/3,031 = 0.009238; the deposit's
`perc_extinction` is 0.01, whose exact definition remains unconfirmed.
Remote evidence remains at
`deep:/data/codex/artifacts/eprp/g3-config22-20261028/`.

## Pitfalls and relevance

- Saved final species lists can contain extinct species with empty abundance
  vectors. Count species with positive abundance when the target is living
  diversity; do not simply take the list length.
- Outputs from different gen3sis versions and converted landscapes may
  differ even under the same seed. Match the version, input representation,
  model functions and target statistic before interpreting differences.
- G2 tests are deliberately small. They do not qualify arbitrary landscapes,
  alternative dispersal functions, or the full evolutionary model.
- For B-005, gen3sis is a possible shared implementation, not evidence that
  geography-only and diversity-dependent hypotheses are empirically
  distinguishable.

## Source and verification

Hagen et al. (2021), *PLOS Biology*, DOI: 10.1371/journal.pbio.3001340;
the simulation input and output deposit is Zenodo 5006413 (CC BY 4.0).
On 28 October Codex recounted all nine retained final states and independently
checked the source fields used in the comparison. Config 22 was independently
recounted on completion and collected on 29 October. The G3 completion audit
is closed; interpretation of the deposit's occupancy and extinction fields
remains qualified as above.
