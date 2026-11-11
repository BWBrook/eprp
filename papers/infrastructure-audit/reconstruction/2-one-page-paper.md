# Step 2: the one-page paper

Draft of 12 November 2026, built from step 1 (`1a`–`1d`). About 600 words. American spelling; numbers
follow `manuscript/claims.csv`.

---

## AI agents as auditors of paleobiology's shared infrastructure: twelve verified cases

**Why.** Large-scale paleobiology rests on shared infrastructure: occurrence databases such as the
Paleobiology Database (PBDB), published data deposits, time scales, plate-tectonic models and analysis
packages. The field has long studied how the rock record distorts inference; the layer between rocks and
results has had far less scrutiny. Checking it means re-running each part against known answers or its own
sources: broad, detailed work suited to AI agents.

**Aims.** We asked what systematic checking by AI agents finds in this layer and what each finding means
for researchers. We expected that (1) problems cluster at hand-offs between producers and users of data
and code, (2) many become visible only when work is re-run, and (3) a second, independent check narrows
first-pass findings.

**Methods.** In October–November 2026, a research program run by two AI agents (Anthropic's Claude and
OpenAI's Codex) with a human facilitator mirrored databases and deposits, benchmarked packages against
simulations with known answers, and recomputed published numbers. From 189 initial candidate findings and
later additions, we chose twelve by consequence for inference. A second agent re-ran each from fixed
inputs, rederived key numbers by separate calculation where possible, and logged each verified result
with its evidence and command.

**Results.** *Data.* Of 368,760 molluscan occurrences in a published deposit, 71,103 were absent from the
public PBDB snapshot of 23 October 2026; dropping them cut stages passing a regional screen from 14 to 12
of 21. Between archived PBDB snapshots, 460, 317 and 17 intervals changed modal base age. Removing 16,260
excess rows from the Triton foraminiferal database changed 1,388 of 2,267 mean exposures in one of our
analyses, 411 by at least one degree. In the Neptune Sandbox Berlin database, 4,111 of 56,387 stored sample
ages differed by more than 0.01 Myr from ages recomputed from its own tie points.

*Software and models.* The admtools package mis-converted 3,972 of 8,282 heights to times in a two-hiatus
model, by up to 3.0 Myr. The fossilbrush package compared numbers as text, so differences of 10, 100 and
499 passed unflagged at a threshold of 5. PyRate's 95% preservation-rate intervals covered the truth in 81 of 100
and 33 of 50 simulated datasets; classical range-end bounds reached 1,895–1,909 of 2,000 in their own test.
The GRIWM extinction-time interval measures dating sensitivity alone. Three plate models disagreed on
paleolatitude by a median of 2.9° at 10 Ma and 13.6° at 400 Ma.

*Published work.* A deposited spreadsheet altered 2,967 of 6,562 capture histories; the Fossil Record 2
compilation shifted 220 rows; a printed probability of 3.4 × 10⁻¹⁶ is 0.32 by its stated test; archived
INDITEK-2 model scores differed from rescoring.

*Expectations.* Most cases sat at hand-offs (deposits, version changes, type conversions, reference
frames). All twelve surfaced through re-running. The second agent's checks narrowed six original claims.

**Meaning.** The fidelity of shared infrastructure is a source of uncertainty in its own right, alongside
sampling bias, and it can be checked directly; AI agents made that checking feasible across a whole
program. Users should record query dates and versions, run several plate models and re-run published
numbers before building on them; maintainers should version and document changes; journals should require
machine-readable deposits with scoring code; agent programs should pair every finding with a second
agent's check and publish the receipts.

**Limitations.** Cases were chosen for consequence, so the series shows kinds of problem, not their
frequency. No published analysis was re-run, no comparison with human auditors was made, some checks share
inputs or model family with the original finding, and providers have yet to be contacted.

**Conclusion.** AI agents can systematically check the databases and software behind fossil-record
research, and what they find is specific, verifiable and actionable.
