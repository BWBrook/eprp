# Independent review: tranche 5 retained outputs

28 October 2026, Codex. Scope: the committed 25 October cGENIE and
metabolic-index declarations, scripts and entries; the retained output on
`deep-server`; and the remote gen3sis G3 status. No new model run was made.
The package session was asked for a handover in Correspondence 76/2429; no
response had arrived when this note was written. Its active ownership remains
unchanged pending a response.

**Recommendation: retain the declared C2/C3 passes for the ten graded
snapshots, with an explicit spatial-use qualification; retain M1 and M3 as
passes and M2 as failed as declared.** The completed comparison is stronger
than the first-snapshot summary in the current catalogue, but neither the
global comparison nor the metabolic-index checks validates every downstream
spatial use.

## Findings

### MAJOR for spatial inference: global agreement masks local differences

Three retained runs completed on 26 October; their logs end in normal
shutdown. Independently recomputing the prespecified comparisons from the
netCDF fields gives passes at all ten graded times from 999.5 through
9,999.5 years, for all three runs. Across those slices, the worst absolute
volume-mean temperature and oxygen differences are 0.00145 °C and
0.326 µmol/kg; the smallest field correlations are 0.99985 and 0.99946.
Wet-cell masks match at every comparison. These are passes on the declared
criteria, not bitwise equality with the deposited experiment.

At 9,999.5 years, the v0.9.35 run's largest cellwise oxygen difference is
73.22 µmol/kg; 154 of 13,868 wet cells differ by more than 10 µmol/kg.
The run and deposit fall on opposite sides of 20 µmol/kg in 34 cells.
The 10, 20 and 60 µmol/kg cutoffs in the accompanying results are **post hoc
diagnostics**, not predeclared ecological thresholds or estimates of an
extinction effect. They show why global means and correlations cannot alone
qualify local hypoxia or habitat maps. The largest temperature difference is
2.70 °C. For spatial biology, compare the specific cells, depth range,
thresholds and derived habitat quantities that matter to the proposed
analysis. No ecological impact was calculated here.

The two v0.9.78 netCDF files have identical SHA-256 hashes despite being
compiled with different gfortran versions; this establishes byte identity
of these output files only. It does not establish general compiler invariance
or that every configuration will reproduce a published experiment.

### MAJOR for data interpretation: missing ecotype values have two meanings

The entry says to read missing `ecotype_viability` as nonviability. This is
valid **only within an evaluated cell**. In the retained output all 5,240,000
ecotype-by-evaluated-cell values agree with independently recomputed
presence/absence when missing is interpreted as zero. But all values in the
3,364 unevaluated grid cells are also missing. Globally replacing missing
with zero silently turns land, excluded poles, and other unevaluated cells
into nonviable habitat. Use the `habitat_viability` and input masks to define
the evaluation domain first; retain missing outside that domain.

The 524-cell M1 maximum |z| is 1.81246, and M2's maximum discrepancy is
3.6621e-6 percentage points, reproducing its **declared failure**. The
post-hoc ecotype matrix result is not a retroactive M2 pass. Temperatures in
the output match the corresponding source fields exactly on these evaluated
cells. Rerunning the author's M3 script reproduces its reported 522/524 and
0.0005764 maximum absolute log difference for positive oxygen; this is an
implementation replay, not an independent reimplementation of M3. Two
negative-oxygen cells are counted outside its tolerance. The script emits
overflow/invalid warnings when seawater functions receive masked grid fill
values; evaluated-cell results reproduce, but future implementations should
mask before calculation and explicitly check finiteness.

The catalogue's statement that remaining uncertainty is in the model state
and trait distributions rather than code is too broad: the tests cover one
configuration, one field, the scored formulas and their stated domains.
They do not validate all masks, coordinate mappings, parameter choices,
boundary cases or other code paths. Its claim that Pohl and Stockey share
the named source is a code-provenance observation, not an independent test.

### MINOR: completeness flag disagrees with the declared grading rule

The retained comparison JSONs were saved after only 999.5 years. The
comparison script's `complete` requires all eleven deposited times, including
9.5 years, whereas the declaration explicitly excludes that time from
grading. The three completed runs have the ten required times but no
9.5-year output, so rerunning that script would still report `complete:
false` even when every declared graded comparison is present. Define
completion from the required graded-time set, and report ungraded coverage
separately. This does not change the recorded numerical results.

### Current gen3sis state

The committed G1/G2 receipts are present; G1 did not meet its declared
criterion, while G2a and G2b passed the stated tests. G3's committed CSV is
empty. A retained server CSV contains nine of the ten planned rows. The
rerun log reports config 9 failed and its log says the config file was not
found. The nine rows are descriptive evidence and have not been independently
audited here; neither their presence nor normal completion of the driver
establishes completion of all ten. Preserve the outputs and ask the owner
about the missing config before repair.

## Reproducibility and limits

`check.py` reads the existing outputs through a read-only container mount;
it independently recomputes the ten graded C2/C3 metrics, mask comparisons,
post-hoc local oxygen diagnostics, M1, M2, and source-temperature alignment.
Full per-time results and SHA-256 hashes of the inputs are in
[`results.json`](results.json). The pinned local image was
`eprp-sw/bench-py5:t5`, image ID
`sha256:589bb0c3d3f3f1ff56cc55aad8ed396b5f6f9aa25bb672f3ecc617670d3326db`.
From the repository root on a machine with access to the retained server
files, reproduce without modifying that work area:

```sh
ssh deep-server 'docker run --rm -i --network none -v /data/paleosoft/bench/t5:/data:ro eprp-sw/bench-py5:t5 python - /data' \
  < resources/software/reviews/2026-10-28-tranche5-codex/check.py
```

The saved cGENIE and metabolic outputs, not the original models, were
replayed. C1's original build or `doMI.R` itself was not rerun. M3 was
replayed using the author's script and is not independently verified here.
The normal end-of-run logs and nine-row G3 receipt were read, not copied
into or changed in the owner's working directory. No source author was
contacted. No catalogue entries or programme priorities have been changed.
