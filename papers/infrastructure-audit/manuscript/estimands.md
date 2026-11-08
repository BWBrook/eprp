# What each case establishes: the allowed claims

The interpretation specification for the infrastructure-audit case series. Every product (article,
supplement, brief, agent guide) states each result only in these terms. Change this file before changing
the prose. Drafted by Claude on 8 November 2026 from the 22-row ledger that Codex replayed (Board
146/3005); Codex's semantic review is requested before the drafts are treated as settled.

A sentence passes only if its subject is the object of the calculation. A caveat does not rescue a
sentence whose noun has changed, for example from "absent from a dated public snapshot" to "withheld".

## Cross-cutting rules (all cases)

- **Estimand of the paper:** a series of checked propositions about named versions of named data products
  and software, each found during one research programme. It is not a sample of the infrastructure.
- **Allowed:** "in the version we tested", "under the stated convention", "in this synthetic design", "a
  case of", "we found and replayed".
- **Not allowed:** any prevalence or rate claim ("widespread", "common", "most packages", "the
  infrastructure is unreliable", "fails silently"); any causal claim about the method ("because two
  models reviewed each other", "AI auditing outperforms human auditing", "catches more errors"); calling
  an intended design or version choice an error; claiming a downstream published conclusion is wrong
  unless that conclusion was itself replayed (none was).
- **Independence:** "independently checked" means a different actor and a different computational route.
  Same-family models are not independent evidence of a cross-model benefit. Do not write "verified by a
  second AI" as if it established correctness beyond the route checked.
- **Disclosure:** third-party cases are reported as found, with no claim that providers or authors have
  been told, until Barry has sent the queued contacts. Restricted PBDB material appears as counts only;
  no identifiers and no access mechanism.

## Case 1. Deposited records absent from a dated public snapshot (C191, C192)

- **Estimand:** set difference between the occurrence identifiers in one retained published deposit
  (Benson et al. 2025, Mollusca member) and a public PBDB snapshot of 23 October 2026; and the change in one
  cheap regional-support threshold when only snapshot members are kept.
- **Allowed:** "71,103 of 368,760 deposited molluscan occurrences (19.3%) are not in the dated public
  snapshot"; "keeping only snapshot members reduced the stages passing our presence screen from 14 to 12
  of 21".
- **Not allowed:** "withheld", "restricted", "embargoed", "deleted" or "leaked" as a description of these
  records; "the deposit cannot be reproduced"; "Benson et al.'s results change"; anything about how
  records come to be absent or how they can be retrieved.

## Case 2. Interval base ages change between archived snapshots (C076)

- **Estimand:** changes in the modal base age of intervals between consecutive archived PBDB query
  products, across three snapshot brackets, for intervals with at least 50 single-interval occurrences.
- **Allowed:** "460, 317 and 17 intervals changed modal base age across the three main brackets (317 becomes
  316 if the threshold must hold in both snapshots)"; "a query repeated on different dates can return
  different ages for the same interval".
- **Not allowed:** "PBDB keeps no versions" (C076's limit: not established here); "PBDB ages are wrong"; any
  comparison with the ICS chart; "silently" unless a changelog check is cited (none was run).

## Case 3. Excess rows in a database update and their effect on one analysis (C043, C045)

- **Estimand:** rows sharing a specified key in the 2023 Triton update; the subset removed by a conservative
  source-priority recipe; and the change that removal makes to EPRP's own Q-012 exposure means and pair
  classes.
- **Allowed:** "28,832 excess rows under our key, of which a conservative recipe removes 16,260";
  "removing them changed 1,388 of 2,267 comparable exposure means, 411 by at least one degree, and changed
  eight, eight, two and one pair classifications".
- **Not allowed:** "duplicates" without "under the specified key"; "28,832 duplicated observations";
  the unreproduced 1,454/423 figures, or the 11–13% inflation, anywhere except the audit trail; any claim
  about effects on published Triton-based studies.

## Case 4. Stored sample ages disagree with recomputation (C040)

- **Estimand:** stored NSB sample ages against ages recomputed from the current tie points by linear
  interpolation with the first age taken at exact depth ties, over 61,862 samples.
- **Allowed:** "4,111 samples in 56 holes differ by more than 0.01 Myr; eight of these depend on the
  exact-tie convention".
- **Not allowed:** "the stored ages are wrong" or "the recomputed ages are right" (neither is certified);
  "stale" without saying stale relative to what.

## Case 5. Age–depth conversion above hiatuses (C096)

- **Estimand:** admtools 0.7.0 time-from-height conversion against exact linear-segment truth on a
  synthetic two-hiatus model.
- **Allowed:** "returned wrong times in affected interpolation segments of the tested model"; "3,972 of
  8,282 random query points were wrong, by up to 0.466 Myr; a targeted probe gave about 2.7 Myr".
- **Not allowed:** "wrong above every hiatus"; "every point above a hiatus"; any statement about StratPal
  or published studies.

## Case 6. Numbers compared as text (C102)

- **Estimand:** fossilbrush 1.0.6 range-flagging decisions on a deterministic grid of differences and
  thresholds, against numeric truth.
- **Allowed:** "compared differences with its threshold in character order: at a threshold of 5 it missed
  differences of 10, 20, 49.9, 100 and 499" (only examples present in the grid).
- **Not allowed:** a prevalence of misflagged records in real data; "fossilbrush cleaning is unreliable".

## Case 7. Calibration of extinction and preservation estimators, with positive controls (C107, C194, C196, C105, C111)

- **Estimand:** frequentist coverage and median bias of retained posterior or analytic intervals in the
  declared simulation designs.
- **Allowed:** "PyRate's 95% intervals for the preservation rate covered the truth in 81 of 100 and 33 of 50
  replicates, and posterior medians sat high"; "classical range-end bounds were near nominal in the ideal
  arm (Strauss–Sadler 1,895 and 1,899 of 2,000 in two implementations; Robson–Whitlock 1,909 of 2,000)"; "simulation generators matched analytic moments"; "the declared overall
  E4 agreement gate failed (91% against 99%)"; "the executed hiatus windows were shifted one Myr from the
  declaration".
- **Not allowed:** "PyRate's intervals are too narrow" (C107's limit); "PyRate is biased" without the
  design; "classical methods are calibrated" without "in the ideal arm of two simulated clades"; omitting
  the failed E4 gate when citing the positive controls.

## Case 8. What an interval estimates, and a random-seed side effect (C110, C098)

- **Estimand:** GRIWM in Rextinct 1.1.0 on fixed synthetic dates: the dependence of its interval on input
  dating uncertainty, and the caller's random-number state after a call.
- **Allowed:** "the interval is the spread of the estimate under resampling of dating error; with zero
  dating error it collapses to a point"; "the call overwrites the caller's random-number state".
- **Not allowed:** "users misread it" or "commonly mistaken" (not tested); "GRIWM is invalid"; "results
  using GRIWM are biased".

## Case 9. Plate-model spread and two reconstruction routes (C125, C123)

- **Estimand:** palaeolatitude range across three named plate models for 300 public points at six ages;
  and geometric differences between two routes for reconstructing one model.
- **Allowed:** "the three models disagree by a median of a few degrees, rising with age (cite the C125
  values with ages)"; "two routes to the same named model differ by an approximately rigid, age-specific
  rotation, consistent with different reference frames".
- **Not allowed:** "error"; "the correct frame is"; "uncertainty in palaeolatitude is X degrees" as a
  general statement.

## Case 10. Published spreadsheets that differ from their source (C035, C048)

- **Estimand:** cell-by-cell comparison of a published spreadsheet with the intact deposit it was made
  from (Monarrez et al. 2023 capture histories) or with chapter workbooks (Fossil Record 2).
- **Allowed:** "2,967 of 6,562 capture histories in the spreadsheet differ from the intact binary deposit;
  3,595 can be restored exactly by padding to the known width"; "220 rows of the one-file Fossil Record 2
  table are shifted one column left".
- **Not allowed:** "5,291 histories are corrupted" (that is the scientific-notation count); "the published
  results are affected" (no fit was rerun).

## Case 11. A printed probability (C190)

- **Estimand:** the upper tail of a binomial with n = 47, k = 28, p = 0.55, as stated in the prose of
  Rampino & Caldeira (2025).
- **Allowed:** "the stated test gives about 0.316, not the printed 3.4 × 10⁻¹⁶".
- **Not allowed:** "the periodicity result is refuted"; "the paper is wrong"; anything about the spectral
  analysis.

## Case 12. Archived scores that do not replay (C195, C193)

- **Estimand:** forward predictions and saved residual sums of squares for three archived rejected
  proposals of the INDITEK-2 calibration, rerun from the pinned archive.
- **Allowed:** "the archived predictions replay, but three saved scores differ from the rescored values by
  about 42.4, 17.5 and 11.9"; "the cause is unresolved".
- **Not allowed:** "INDITEK cannot be reproduced"; "the calibration is wrong"; "Cermeño et al.'s
  conclusions are affected"; calling the three proposals accepted draws or posterior samples.
