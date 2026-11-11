# Step 4: display items

12 November 2026. The plan serves the main message (`03-main-message.md`) and its four lines of evidence.

**Budget: three figures and two tables in the main text; everything else in the supplement.** Twelve
cases already ask a lot of a reader. One figure per case would bury the message, and a result the reader
must hunt across six or more items stops being a message. The *Paleobiology* comparators carry 2–11
items; five sits comfortably for a Research Article of about 6,000–7,000 words.

## Main text

**Figure 1 — Where the checks were made, and how (context schematic, two panels).**
- **A.** The path from rocks to a published result: collection, database or deposit, time scale and age
  model, plate model, analysis package, published number. Each of the twelve cases is pinned to the layer
  or hand-off where it sits. This orients a new reader and shows hypothesis 1 at a glance.
- **B.** The audit workflow: 189 initial candidates plus later findings, then twelve chosen cases, replay
  from pinned inputs, a second agent's check, and 22 supported claims, with six original claims narrowed
  on the way. This is the methods schematic and shows hypothesis 3.

**Figure 2 — Findings in the data layer (four panels, quantitative).**
- **A.** Case 1: deposited molluscan records present in, and absent from, the dated public snapshot.
- **B.** Case 2: intervals whose modal base age changed, in each snapshot bracket.
- **C.** Case 3: the change in each exposure mean when excess Triton rows are removed. A histogram makes
  the 411 shifts of at least one degree visible.
- **D.** Case 4: stored minus recomputed NSB sample ages, a histogram with the 0.01-Myr threshold marked.

**Figure 3 — Findings in models and software (four panels, quantitative).**
- **A.** Case 5: admtools error against stratigraphic height, with the hiatuses shaded.
- **B.** Case 6: fossilbrush flag decisions across the test grid, against numeric truth and character
  order.
- **C.** Case 7: interval coverage with 95% binomial intervals. Two clearly separate groups: PyRate
  preservation rates (two arms) and the classical range-end bounds.
- **D.** Case 9: median paleolatitude spread among the three plate models by age.

**Table 1 — The twelve cases (the backbone of the Results).** For each case:
- where it sits (layer or hand-off);
- what kind of finding it is;
- how it was found (by execution or by reading);
- the checked result;
- what the second agent's check changed;
- the claim IDs.

This table carries hypotheses 1–3 for all twelve cases in one place.

**Table 2 — What to do about it.** Rows are audiences: users, database and package maintainers, journals
and depositors, programs using AI agents. Each row lists the actions and the cases behind them. It
replaces the current prose Recommendations section.

## Supplement

- **Cases 8, 10, 11 and 12 in detail.** These are clear in one sentence each, and Table 1 carries them.
  Case 11's arithmetic, case 12's score comparison and case 10's row-level breakdown go in supplementary
  tables.
- **Case 9's reference-frame comparison** (two routes to TorsvikCocks2017).
- **The positive-control details for case 7**, including the failed agreement gate and the shifted
  hiatus arm.
- **The assumptions table**, the audit trail of narrowed statements, and the replay commands.
- **Per-case receipts**, by path.

## Practicalities

- Every plotted value comes from a committed receipt or replay table, with the figure script and its hash
  in the repository, and each panel cites its claim ID in the caption.
- Codex confirms that the per-item data for each panel are already retained. Most panels draw on existing
  receipts (case 5 probes, case 7 per-replicate coverage, case 9 reconstructed points, case 3 paired
  tables). Case 4's per-sample differences and case 1's counts may need extracting from the replay
  outputs.
- Captions name any AI system that generated a figure, as the journal requires.
