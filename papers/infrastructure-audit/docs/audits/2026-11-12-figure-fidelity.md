# Figure-fidelity review

12 November 2026. Review of `7157814`, accepted at Board 160/3318 in reply
to 3314. Main Codex checked Figure 1, the rendered manuscript pages and
integration; two bounded GPT-6.1 Sol reviewers independently covered Figures
2 and 3 against the checked tables, replay receipts and estimands. Production
code, figures, captions, manuscripts and data were read-only.

**Recommendation: approve after two small presentation repairs.** The plotted
values and stated populations match the evidence. Figures 1–3 regenerate
byte-for-byte as PNGs in a scratch directory. The repairs concern the age-axis
geometry and the rendered threshold notation, rather than numerical claims.

## Findings and dispositions

| ID | Severity | Evidence | Repair and verification | Owner |
|---|---|---|---|---|
| F-01 | MINOR; repair before the final figure pass | `manuscript/figures.py:280–289` uses `range(len(ages))` for connected points labeled “Age (Ma).” Figure 3D gives 10–50 Ma the same horizontal distance as 100–200 Ma, changing the temporal spacing and apparent slopes. The medians and cohorts are correct. | Use numeric ages as x coordinates and change the x limits to the age domain. Retain the cohort labels. If categorical cohorts were intended instead, remove the connecting line and label them as discrete cohorts; numeric age is recommended. Regenerate Figure 3 and check its manuscript page. | Claude |
| F-02 | MINOR; rendered caption defect | `manuscript/text/main.md:391–393` puts only the plus/minus command inside dollar delimiters, directly followed by the numeric threshold. The actual PDF, page 10, visibly prints `$±$1°` and `$±$0.01 Myr`. A Pandoc AST check finds no `pm` Math nodes in the production source: the closing dollar is followed directly by a digit. | Put the complete quantity inside math, using the exact replacements below. Scratch parsing produces both intended Math nodes. Rebuild and inspect page 10 for plain ± thresholds without dollar signs. | Claude |

Exact caption replacements:

```text
$\pm$1°        -> $\pm 1^\circ$
$\pm$0.01 Myr  -> $\pm 0.01$ Myr
```

These repairs require no change to the data, estimands or claims ledger.

## Panel decisions

**Figure 1 passes.** The twelve case numbers, primary families, dependency
positions and four-family legend agree with Table 1. Case 8's additional
computation finding is stated in the caption. The workflow preserves 189
initial candidates plus later additions, twelve selected cases, 22 supported
propositions and the six corrected initial accounts (1, 3, 4, 5, 7, 10).

**Figure 2 passes numerically and in population, with F-02 affecting its caption.**

- **A/B:** Snapshot membership counts, archived pair dates and interval counts
  match the receipts. The caption identifies the later-snapshot threshold.
- **C:** The caption and y-axis explicitly identify the conditional population
  of 1,388 changed means out of 2,267 comparable bins. Excluding the 879
  unchanged paired bins is therefore transparent. All changed values enter
  the quarter-degree histogram; none falls outside its edges. The four newly
  missing bins are excluded from that paired population and retained in their
  separate table. The signed deltas and ±1° lines match the inputs.
- **D:** All 56,387 comparable samples enter the signed histogram. Its symmetric
  logarithmic edges cover the complete range, with no clipping. The central
  ±`1e-6` Myr bin contains 52,029 samples; it is a near-zero bin, rather than
  a count of exact zeros. The caption makes no exact-zero claim. Counts are
  plotted per bin, rather than as a density; the symlog x scale and log count
  scale are labeled. The 4,111 threshold exceedances and 56-hole count match
  the source values. No rebinning is required for fidelity.

**Figure 3 passes numerically and in grouping, with F-01 affecting its age axis.**

- **A:** Correct signed sparse-model errors, units and original 8,282 sampled
  heights; deposition segments are separate and hiatus lines are at 8 and 14.
- **B:** Correct older-than-reference grid, numeric threshold equality, five
  discrete misses and contrasting decisions at 50 and 99. The caption defines
  filled markers and shaded mismatches. Categorical spacing is appropriate
  for these explicitly discrete test values.
- **C:** The preservation-rate and range-end targets are separated by names,
  a divider and the caption. The five counts, nominal 95% line and tbea/EDE
  implementation labels agree with the receipts. No uncertainty bars or
  unsupported ranking are introduced.
- **D:** The six nonmonotonic medians and age-specific cohorts
  (269/260/255/247/217/194) match the receipt and caption.

## Verification and limits

Main imported `manuscript/figures.py`, redirected its `OUT` directory to
ignored scratch space and executed all three figure functions. All assertions
passed under matplotlib 3.10.9 and NumPy 2.5.4. Each regenerated PNG has the
same SHA-256 as its committed counterpart; the compact
[reproduction receipt](2026-11-12-figure-reproduction.json) retains the hashes.
Thus the inspected figures correspond to the current script and inputs.

The figure pages (13–15) and caption page (10) of the actual fifteen-page
manuscript PDF were rendered and inspected. Labels and marks are legible,
with no material clipping or overlap. The threshold delimiters in F-02 are
visible despite clean source-glyph checks. Scratch caption replacements
parse as `\pm 1^\circ` and `\pm 0.01` Math nodes; the production build was not
modified or rerun. Palette appearance was inspected, but the reported formal
color-vision-deficiency validation was not independently rerun.

`make -C papers/infrastructure-audit/manuscript check` passes: 22 supported
and cited claims, six clean source-glyph checks, and successful main,
supplement and brief lint/reference audits. No scientific source analyses
were rerun. The plotting assertions compare current expected constants with
input values; they do not read `claims.csv` dynamically. Current fidelity is
verified here, rather than a guarantee against every future text/figure drift.

The simplified Figure 1A remains a reasonable brief figure, with its own
two-page edit and render check. That known product task remains open. After
the two repairs and that figure, hand the complete draft package to Barry
for the final read; no new article rewrite is recommended.

Next: Claude — repair the age axis and caption math, finish the brief figure, then hand the draft to Barry.
