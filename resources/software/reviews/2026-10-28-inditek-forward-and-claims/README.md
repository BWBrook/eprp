# INDITEK-2.0: forward model, saved chains and the recovery claim

28 October 2026, Codex. **Assessment:** selected forward predictions in the
public software deposit reproduce very closely, but their saved fit scores
do not. The deposited chains show substantial mixing and convergence
problems. If these are the chains behind the paper's proof-of-concept and
sensitivity results, their reported posterior uncertainty and sensitivity
summaries need re-evaluation. We cannot yet establish that exact connection,
or determine the direction or size of any change in the published results.

The version-of-record [abstract](https://doi.org/10.1111/2041-210x.70422)
reports synthetic parameter recovery with relatively low uncertainty and
mechanism-disabled sensitivity analyses. We could retrieve the abstract,
but not the independently accessible full article; the library's restricted
text-mining copy was not read. We therefore do not claim to have audited the
published figures, the exact data used to create them, or all their stated
interpretations. The work below concerns the checksum-verified
[Zenodo 22079167 code and outputs](https://zenodo.org/records/22079167),
not a confirmed reconstruction of that article's analysis.

## Forward-model checks

The declared [F1 controls](../../bench/validate/t5_inditek_forward_controls.py)
independently calculate food limitation, temperature limitation and carrying
capacity at five synthetic points and three times. The `proof`, `food`,
`temp` and `expo` cases match the archive's rate implementation to at most
7 × 10⁻¹⁸ in the evaluated values; the applicable carrying capacities agree
exactly. Adding 10 °C uniformly within each time slice leaves the computed
rate unchanged in these cases. The implementation normalises temperature
relative to that time slice's 99th percentile, so spatially uniform shifts
cancel in that temperature factor. This is a property of the tested model,
not a test of whether that environmental assumption is biologically right.
The [receipt](../../bench/results/t5/inditek_forward_controls_20261028.json)
records source hash, cases and errors.

In [F2](../../bench/validate/t5_inditek_forward_replay.py), three
preselected proof-chain **proposals**, including rejected proposals, were
re-evaluated from the deposited inputs. Each saved vector of 2,978 diversity
predictions agrees with the rerun to within 5 × 10⁻¹⁴. The saved and rerun
RSS values differ by 42.360, 17.468 and 11.937 respectively, so **F2 fails
its declared combined prediction-and-score criterion**. An independent
calculation from the rerun predictions and deposited observation map exactly
matches the rerun's RSS in all three cases (**F3 passes**); the finite-cell
masks agree. The [receipt](../../bench/results/t5/inditek_forward_replay_20261028.json)
includes parameters, acceptance flags, scores, versions and input hashes.
The most direct unresolved alternatives are different observations or a
different scoring implementation in the chain-generating analysis; these
checks cannot choose between them. The retained `D` values are proposals,
not necessarily samples from the accepted chain.

An exploratory [reference-map check](../../bench/results/t5/inditek_reference_check_20261028.json)
reran the forward code at `[161, 19, 0.035, 0.002, 2]`, the active reference
parameters in the deposited synthetic-data script. Its mask agrees with
`D_proof.npz`, but the grid differs by as much as 7.84. The deposited
notebook uses `D_proof.npz` as a sensitivity-figure reference; we have not
established that it generated the deposited observation map. The reference
and observations also differ substantially, including away from the
lower-clipping boundary. This is a provenance discrepancy to resolve, not a
demonstration of how the paper's synthetic data were generated.

Each of the five saved `residuals` arrays consists entirely of zeros, even
though 560–600 of 600 sampled proposal RSS values per variant are finite
and positive. Thus these arrays do not permit reconstruction of the saved
scores. See the [independent archive audit](../../bench/results/t5/inditek_saved_residuals_20261028.json).
We do not know whether those arrays were used in the analysis or why they
were saved this way.

## Saved-chain diagnostics

The deposited notebook's histogram uses all six chains from index 2,000;
the diagnostic applies that same slice, or 3,003 saved states per chain,
to every active parameter in all five archived variants. It reports
rank-normalised split R-hat and bulk and tail ESS with ArviZ 0.22.0 in a
separate locked environment. These are diagnostics of the recorded traces,
not evidence that their transition kernel targets the correct posterior.

| Variant | Rank-split R-hat range | Bulk ESS range | Example of concern |
| --- | ---: | ---: | --- |
| proof | 1.018–1.623 | 10–186 | Q10: R-hat 1.623, bulk ESS 10 |
| open | 1.214–2.349 | 7–21 | minimum speciation: R-hat 2.349 |
| expo | 1.093–1.880 | 9–71 | one chain accepts no post-2,000 proposals |
| food | 1.066–3.237 | 7–66 | Q10: R-hat 3.237, bulk ESS 7 |
| temp | 1.675–2.035 | 8–13 | two chains remain in a different parameter region |

The nominal 18,018 retained states per parameter do not imply that many
independent draws. Stored proposal scales continue to change after index
2,000, which also means that the post-burn-in transition procedure remains
adaptive. A diagnostic calculation cannot establish that such adaptation is
valid or that any posterior interval is calibrated. The complete per-chain
means, acceptance rates, proposal-scale counts, R-hat, both ESS measures,
input hashes and code are in the [receipt](../../bench/results/t5/inditek_chain_diagnostics_20261028.json)
and [script](../../bench/validate/t5_inditek_chain_diagnostics.py).

The same notebook uses different subsets for the **mean lines in its trace
plots**: four of six chains for `temp` and five for `expo`, although all six
traces are plotted. For `temp`, Kmax averages 115.07 in the selected four
chains but 93.44 across all six; maximum speciation averages 0.0215 and
0.0476 respectively. The histogram routine instead pools all six chains.
These figures are outputs of the deposited notebook, not demonstrably the
version-of-record figures. Excluding visibly different chains may change a
summary but does not establish convergence of the remaining chains.

The notebook's combined density plot, labelled Figure 4 in the notebook,
uses those same `temp` and `expo` subsets and, separately, all `open` chains
from index 3,000. Even on these selected slices, `temp` maximum speciation
has R-hat 1.262 and bulk ESS 11.7; `expo` Q10 has 1.327 and 12.4; and
`open` minimum speciation has 2.367 and 7.4. This exploratory
[figure-pipeline diagnostic](../../bench/results/t5/inditek_figure_diagnostics_20261028.json)
was identified in the independent review after the main diagnostics. It
does not establish that this plot is the article's Figure 4.

## Relation to the sampler finding and the paper

The separate [sampler review](../2026-10-28-inditek-sampler/README.md)
established a wrong first-transition prior calculation in the deposited
sampler. The saved chains cannot have followed that sampler under its stated
settings, whereas an earlier candidate rule and settings satisfy a necessary
acceptance check. That candidate also has a demonstrated prior-calculation
defect and fails a simple known-target diagnostic with its adaptation. In a
further controlled comparison that fixes proposal scales and initialisation,
retaining just that historical proposed-prior expression still produces
severely displaced or stalled chains; the corrected expression samples the
simple target in the tested runs. See the sampler review for the modified
code and receipts. This identifies a mechanism capable of producing poor
sampling, but does not establish that it caused the archived traces: the
exact generating source and random draws remain unknown.

The paper's recovery claim is a proof of concept using synthetic observations,
not independent verification of evolutionary history. Even if those
observations and figures are eventually mapped to the archived chains, a
nominal interval containing the chosen truth is not a calibration study:
the sampled intervals first need adequate convergence and a correct target,
and repeated known-truth data sets would be needed to assess coverage.
The historical candidate's Q10 prior is centred at 2 with standard
deviation 0.08, and the deposited generator script lists 2 as its nominal
Q10. If those were the actual prior and generating value for a reported
analysis, recovery of that parameter alone would also be consistent with
strong prior information. Their use in the version of record is not yet
established.

The next decisive step is to identify the exact code, priors, observed map,
seeds and chains underlying each article figure, then re-fit the same data
with a verified sampler and adequate independent-chain diagnostics. A
simulation-based calibration or repeated recovery study can then assess
coverage. Author contact is in Barry's outreach queue; none has been sent.

## Independent check

An independent Codex subagent (GPT-6.1 Sol, 28 October) re-scored the three
saved proposal vectors directly against the deposited observations,
checked the proposal and next-state array alignment, manually reproduced
proof Q10 rank-split R-hat, verified all-zero residual arrays and inspected
the notebook's figure-specific slices. It found no numerical error in F2,
F3 or the main A8 diagnostics. Its strongest qualification is retained:
the proof means are close to the nominal reference and the five nominal
values fall inside the recorded marginal intervals, so these results do not
demonstrate failure to recover the chosen point values. The issue is whether
the intervals and sensitivity summaries are reliable posterior results.
This is an independent computational audit of the same archive, not an
independent dataset or empirical validation.
