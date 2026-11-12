# Step 1d: display items

12 November 2026; revised the same day after Codex's critique (160/3260, section 4). The plan serves the
main message (`1c-main-message.md`) and the three organizing questions in `1a-working-abstract.md`.

**Budget: three figures and two tables in the main text; everything else in the supplement.** Twelve
cases already ask a lot of a reader, and one figure per case would bury the message. The *Paleobiology*
comparators carry 2–11 items, and Research Articles allow up to 15; five sits comfortably at about
6,000–7,000 words.

**Coding rule.** Every case is assigned one primary kind: **data transformation, implementation, model
choice or output meaning**. The rule is written down before the figure is drawn and applied in Table 1.
Mixed cases carry a secondary kind.

## Main text

**Figure 1: the checked dependencies and the audit workflow (two panels).**
- **A.** A map of the selected cases along the path from rocks to a published result: collection,
  database or deposit, time scale and age model, plate model, analysis package, published number. Each
  case sits where it was found and is coloured by its kind. This is a map of twelve selected cases.
  *Ready:* editorial, from the ledger and estimands.
- **B.** The workflow as a sequence of steps, each in its own unit: candidate findings (189 initial,
  plus later additions with no fixed total) → twelve chosen cases → replay from pinned inputs → second
  check → 22 supported propositions. The six cases whose initial accounts replay corrected are marked.
  *Ready:* catalogue, selection record, ledger and supplement S3.

**Figure 2: findings in data transformations (four panels).**
- **A.** Case 1: deposited molluscan records present in (297,657) and absent from (71,103) the dated
  snapshot. *Ready:* `R/main/case01.json`.
- **B.** Case 2: intervals with a changed modal base age in each bracketed snapshot pair, labeled with the
  ≥50 later-snapshot threshold. These are counts, without denominators. *Ready:*
  `R/data/results/pbdb.json`.
- **C.** Case 3: change in each mean absolute paleolatitude when the excess Triton rows are removed.
  *Preparation:* recompute full-precision per-bin means. The three-decimal tables give 1,385 changes, not
  1,388; plot the four newly missing bins separately.
- **D.** Case 4: stored minus interpolated NSB sample ages for the 56,387 comparable samples, with
  ±0.01 Myr marked. *Preparation:* extract signed per-sample differences from the SQLite source under the
  recorded interpolation rule; the receipt keeps absolute-difference classes only.

**Figure 3: findings in implementations, model choices and output meaning (four panels).**
- **A.** Case 5: admtools time error against height in the sparse synthetic model, with the hiatus
  boundaries (heights 8 and 14, zero thickness) marked as lines. *Preparation:* rerun the pinned
  conversion for the full curve; the receipt holds ten probes and grid summaries.
- **B.** Case 6: fossilbrush flag decisions across the test grid, against numeric truth and text order,
  with the threshold and test direction labeled. *Ready:* `R/software/case06_fossilbrush.json`.
- **C.** Case 7: observed coverage against the 95% nominal line, in two separate groups:
  - PyRate preservation-rate intervals (two arms);
  - extinction-time range-end bounds.

  Any interval shown is labeled as descriptive. *Ready:* `R/calibration/pyrate_raw.json` and
  `classical_reaggregate.json`.
- **D.** Case 9: median paleolatitude spread among the three plate models by age. Use either the fixed
  194-point cohort or all reconstructable points with the n for each age; both are retained. *Ready:*
  `R/software/case09_plate_models.json`.

`R` is `evidence/replay-20261108/`.

**Table 1: the twelve cases.** Columns:
- the layer and kind (primary, plus any secondary);
- how the finding was discovered, recorded from the dated discovery notes and allowing mixed routes;
- how it was checked in replay;
- the checked result;
- what review changed;
- the claim IDs.

*Preparation:* editorial extraction of discovery routes from the correspondence and catalogue records.

**Table 2: recommended actions.** Rows are audiences: users, database and package maintainers, journals
and depositors, programs using AI agents. Each row gives the actions and the cases behind them. It
replaces the prose Recommendations section.

## Supplement

- **Cases 8, 10, 11 and 12 in detail,** with supplementary tables for case 10's row-level breakdown,
  case 11's arithmetic and case 12's forward replay and score comparison.
- **Case 9's reference-frame comparison** (two routes to TorsvikCocks2017).
- **Case 7's positive controls,** with the failed agreement gate and the shifted hiatus arm.
- **The Limitations material in full,** the audit trail of corrections and the replay commands.

## Preparation tasks before drawing

Three extractions are needed, all from held material with no new external data:
1. full-precision Triton per-bin means (Figure 2C);
2. signed NSB per-sample differences (Figure 2D);
3. a rerun of the admtools curve (Figure 3A).

Table 1 also needs its discovery routes extracted. Every plotted value then comes from a committed table,
with the figure script and its hash in the repository and the claim ID in the caption. Captions state any
role an AI system played in producing the figure, including writing the plotting code.
