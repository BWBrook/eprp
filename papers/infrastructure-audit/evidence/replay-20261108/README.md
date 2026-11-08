# Twelve selected cases: fixed-input replay

8 November 2026. Main Codex integrated three bounded GPT-6.1 Sol delegates'
checks and its own membership, probability and output reviews. The
[manuscript ledger](../../manuscript/claims.csv) is the drafting source.
The older 189-row candidate catalogue records discovery, not current clearance
for every clause. The [selection note](../../case-selection.md) is retained
as the initial selection record.

All twelve cases have checked, bounded propositions. This does **not** promote
their initial headlines wholesale. In particular, missing public membership,
biased interval location, disagreement between archived scores, intended
model choices and numerical implementation defects require different claims.

| Case | Checked proposition and drafting boundary | Ledger IDs | Receipt |
| --- | --- | --- | --- |
| 1 | 71,103 of 368,760 deposited molluscan occurrences are absent from the dated public snapshot. Rebuilding the support table reproduces the 14-to-12 change among 21 stages. Absence alone does not establish withholding or present-day access. | C191, C192 | [Main checks](main/README.md) |
| 2 | Whole-snapshot interval comparisons reproduce 460/317/17 changed base-age modes in the three main brackets under the original **later-snapshot** sample threshold; requiring the threshold in both snapshots gives 460/316/17. This does not re-establish historical-query semantics or compare against ICS charts. | C076 | [Data replay](data/README.md) |
| 3 | Triton's specified key has 28,832 excess rows; the conservative source-priority recipe removes 16,260. Fresh paired builds establish changes to exposure and classifications. The old 1,454/423 counts and 11–13% sample inflation are not reproduced under this pinned recipe. | C043, C045 | [Paired builds and independent reconstruction](data/README.md) |
| 4 | 4,111 stored-versus-recomputed age discrepancies exceed 0.01 Myr under the stated first-tie rule, in 56 holes. Eight depend on the exact-tie convention. The sample count is 61,862, correcting a header-inclusive count. | C040 | [Data replay](data/README.md), [parent count](main/nsb_count_review.json) |
| 5 | admtools 0.7.0 mis-converts times in affected interpolation segments of the tested hiatus model. Later segments can be correct. Dense random-sample maximum 0.466 Myr and targeted 2.7-Myr probes are different results. | C096 | [Direct package and analytic checks](software/README.md) |
| 6 | fossilbrush 1.0.6's numeric-as-text comparison fails a deterministic threshold grid. This proves a tested mechanism, not its prevalence in real analyses. | C102 | [Direct package checks](software/README.md) |
| 7 | Raw posterior logs reproduce PyRate q coverage of 81/100 and 33/50 and upward median bias under the specified design. The width comparison does not support “too narrow”. Classical near-nominal coverage and retained generator moment controls discriminate; overall E4 still fails. Hiatus results belong to the executed, shifted design. | C107, C194, C196, C105, C111 | [Calibration replay](calibration/README.md) |
| 8 | GRIWM's interval varies with input dating uncertainty; a zero-uncertainty control collapses to a point. The tested implementation overwrites caller RNG state. This is a semantic finding plus a computational side effect, not general invalidity of the estimator. | C110, C098 | [Separate formula and RNG controls](software/README.md) |
| 9 | Raw local reconstructions reproduce all 7,200 retained rows; model-dependent latitude spread and sampled near-rigid differences between two reconstruction routes persist. No frame is thereby identified as correct, and spread is not calibrated error. | C125, C123 | [Raw models and independent geometry](software/README.md) |
| 10 | Monarrez's XLSX disagrees with 2,967 intact binary histories; 3,595 can be recovered exactly with known-width padding. Scientific notation is not a damage count. Fossil Record 2 has 220 shifted rows, of which 112 shift ranges, two shift habitat and range, and 106 move an NFR flag. | C035, C048 | [Direct OOXML and binary comparison](data/README.md) |
| 11 | The stated binomial contract gives about 0.315864, rather than 3.4 × 10⁻¹⁶. Exact complement recurrence, direct exact sum, integer polynomial convolution and R agree to floating precision. This does not refute the separate spectral analysis. | C190 | [Source and arithmetic](main/README.md), [separate reviewer](software/case11_reviewer.json) |
| 12 | Three archived **rejected proposals** reproduce forward predictions but not saved scores under deposited observations and scorer. Independent ZIP-array scoring agrees with the rerun. Cause and published-figure provenance remain unresolved; chain diagnostics were not rechecked. | C195, C193 | [Fresh forward and separate scoring checks](calibration/README.md) |

## What counts as independent here

The source findings were developed in other sessions. The delegates wrote
separate aggregation, interpolation, geometry or scoring implementations;
main reviewed their code and receipts and separately counted NSB samples,
recalculated Triton displayed-output differences, checked original input/output
hashes, and rederived the published probability. The probability has another
delegate's integer-polynomial check. The software runner was executed end to
end in a fresh directory with content-pinned images and verified staging.

These are separate actors and computational routes. Some use the same model
family as the original audit. They are not independent biological datasets,
proof of a cross-model advantage, or a controlled comparison with human
auditing. The ledger's `basis` identifies **fresh raw-data calculation**,
**fresh pinned implementation**, **retained posterior/output reaggregation**
or **mathematical/control check**. A supported row applies only to its stated
proposition and limits. Failed gates and unreproduced old summaries are kept.

## Reproduce and review

Commands and immutable input hashes are in the three linked subdirectories
and [main checks](main/README.md). Source archives, large raw fits and access
details are not copied here. The small paired Triton tables and differences
retain the joined comparison needed to audit the consequence for EPRP itself.
Raw sources were read-only; existing builders and catalogues were unchanged.

From the repository root, check the ledger and this handoff with:

```sh
python3 papers/infrastructure-audit/tools/claims.py check \
  papers/infrastructure-audit/manuscript/claims.csv \
  papers/infrastructure-audit/evidence/replay-20261108/README.md
```

The committed evidence revision in every row pins the checked receipt bytes;
individual receipts additionally hash original inputs and tested scripts.
An article build is not this tranche's acceptance test: article text and
references remain a drafting task, and the scaffold's previously reported
temporary-directory issue is not repaired here.

Claude's next step is to write the estimands and allowable wording from these
bounded rows, then draft the article and supplement, agent guide and brief.
Barry retains provider contact and final paper-release review. No further
campaign over the remaining candidate catalogue is needed for this handoff.
