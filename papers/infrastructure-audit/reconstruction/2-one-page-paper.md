# Step 2: the one-page paper

Draft of 12 November 2026, built from step 1 (`1a`–`1d`); revised the same day after Codex's critique
(160/3260). About 600 words. American spelling; numbers
follow `manuscript/claims.csv`.

---

## AI agents as auditors of paleobiology's shared infrastructure: twelve verified cases

**Why.** Large-scale paleobiology depends on shared infrastructure: occurrence databases such as the
Paleobiology Database (PBDB), published data deposits, time scales, plate-tectonic models and analysis
packages. Errors or misreadings in this layer pass into every inference built on it.

**Questions.** In twelve cases checked by AI agents, we ask: where did each finding arise (in a data
transformation, an implementation, a model choice or the meaning of an output); what checks established
it; and what changed when a second agent re-examined it?

**Methods.** In October–November 2026, a research program run by two AI agents (Anthropic's Claude and
OpenAI's Codex) with a human facilitator re-ran data transformations, software and published
calculations against known answers and their own sources. From 189 initial candidate findings and later
additions, we chose twelve cases by consequence for inference. A second agent replayed each from
pinned inputs, rederived key numbers by separate calculation where possible, and logged each verified
proposition with its evidence and command.

**Results.** *Data transformations.* Of 368,760 molluscan occurrences in a published deposit, 71,103 were
absent from the public PBDB snapshot of 23 October 2026, and our regional presence screen passed 12 of 21
stages with snapshot members against 14 with the full deposit. Across three bracketed PBDB snapshot pairs,
460, 317 and 17 intervals changed modal base age. Removing 16,260 excess rows from the Triton
foraminiferal database changed 1,388 of 2,267 mean absolute paleolatitudes in our analysis, 411 by at
least one degree. In the Neptune Sandbox Berlin database, 4,111 of 56,387 stored sample ages differed by
more than 0.01 Myr from ages interpolated from its own tie points.

*Implementations.* In a synthetic two-hiatus model, admtools converted 3,972 of 8,282 heights to times in
error, by up to 3.0 Myr. fossilbrush compared numbers as text, so differences of 10, 100 and 499 passed
unflagged at a threshold of 5. A deposited spreadsheet altered 2,967 of 6,562 capture histories relative
to its intact source file, and the one-file Fossil Record 2 table held 220 rows with left-shifted cell
tails. A printed probability of 3.4 × 10⁻¹⁶ is 0.32 under its stated binomial test. In INDITEK-2's
synthetic demonstration, three archived rejected proposals reproduced their predictions, while their saved
residual-sum-of-squares scores differed from rescoring by up to 42.4.

*Model choices and output meaning.* PyRate's 95% preservation-rate intervals covered the true value in 81
of 100 and 33 of 50 simulated datasets, while extinction-time range-end bounds covered it in 1,895–1,909 of
2,000 cases in their own test. GRIWM's dating-error resampling interval measures sensitivity to dating
error. Three plate models disagreed on paleolatitude by a median of 2.9° at 10 Ma and 13.6° at 400 Ma.

*Checks and review.* Re-execution, recomputation from source, code inspection and arithmetic, often
combined, established the findings. Replay corrected the initial accounts of six cases.

**Meaning.** Agents checked all four kinds of dependency across a whole research program, and each
finding points to an action: users recording query versions, comparing plate models and replaying
published numbers; maintainers versioning changes; journals requiring machine-readable deposits; and agent
programs pairing each finding with a second check.

**Limitations.** The cases were selected for consequence, so they describe kinds of finding, not their
frequency. We replayed published calculations and part of one deposited model, not whole downstream
studies. Independence varies by check, and some checks share inputs or model family. Calibration controls
rest on two simulated clades, and one declared gate failed. Some inputs are held locally, and a
cold public rebuild is untested. Providers and authors have yet to be contacted.

**Conclusion.** AI agents can systematically check the databases and software behind fossil-record
research, and what they find is specific, verifiable and actionable.
