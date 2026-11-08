# What each case establishes: the allowed claims

The interpretation specification for the infrastructure-audit case series. Every product (article,
supplement, brief, agent guide) states each result only in these terms. Change this file before changing
the prose. Drafted by Claude on 8 November 2026 from the 22-row ledger Codex replayed (Board 146/3005),
then revised after Codex's semantic review (`docs/audits/2026-11-08-wording-review.md`, W01–W17).

A sentence passes only if its subject is the object of the calculation. A caveat does not rescue a
sentence whose noun has changed, for example from "absent from a dated public snapshot" to "withheld".
Quoting a forbidden phrasing as a trap or a withdrawn statement is allowed; adopting its interpretation
is not.

## Cross-cutting rules (all cases)

- **Estimand of the paper:** a series of checked propositions about named versions of named data products
  and software, found during one research programme from an initial 189-row candidate catalogue and later
  programme findings. It is not a sample of the infrastructure.
- **Allowed:** "in the version we tested", "under the stated convention", "in this synthetic design", "a
  case of", "we found and replayed".
- **Not allowed:**
  - any prevalence or rate claim ("widespread", "common", "most packages", "the infrastructure is
    unreliable", "fails silently", "rarely checked", "used far more often than checked");
  - any causal or economic claim about the method ("caught because two models reviewed each other", "AI
    auditing outperforms human auditing", "agents make auditing cheap", "nobody is paid to do it");
  - calling an intended design or version choice an error;
  - claiming a downstream published conclusion is changed. No published analysis was replayed; measured
    changes are to support counts, inputs or EPRP's own analyses;
  - asserting that providers did not already know a finding. Their knowledge is unresolved.
- **Independence is check-specific.** Each case combined replay by another actor with the computational or
  mathematical checks in its receipt: separate aggregation, interpolation, geometry or scoring code. Not
  every proposition was rederived by a fully separate route. The INDITEK forward run reused the original
  harness, and only its scoring was separately implemented. Some reviewers used the same model family and
  shared inputs. Not allowed: "every proposition was independently rederived"; "verified by a second AI"
  as if that established correctness beyond the route checked.
- **Reproducibility:** each result records its replay command, required inputs and their hashes. Some
  inputs are locally retained (container image IDs, posterior logs, source archives). Not allowed: "anyone
  can rerun every case from the public repository" (a cold public rebuild was not validated).
- **Correspondence:** reviewed snapshots of the board are public, with withheld messages left as
  placeholders. Not allowed: "the full correspondence record is published".
- **Disclosure:** third-party cases are reported as found, with no claim that providers or authors have
  been told, until Barry has sent the queued contacts. Restricted PBDB material appears as counts only;
  no identifiers and no access mechanism.

## Case 1. Deposited records absent from a dated public snapshot (C191, C192)

- **Estimand:** set difference between the occurrence identifiers in one retained published deposit
  (Benson et al. 2025, Mollusca member) and a public PBDB snapshot of 23 October 2026; and the change in one
  cheap regional-support threshold when only snapshot members are kept.
- **Class label:** snapshot membership and provenance finding.
- **Allowed:** "71,103 of 368,760 deposited molluscan occurrences are not in the dated public snapshot";
  "rebuilding from that snapshot would omit these identifiers"; "keeping only snapshot members reduced the
  stages passing our presence screen from 14 to 12 of 21".
- **Not allowed:** "withheld", "restricted", "embargoed", "deleted" or "leaked" as a description of these
  records; "cannot be rebuilt from today's database"; "the deposit cannot be reproduced"; "Benson et al.'s
  results change"; anything about how records come to be absent or how they can be retrieved.

## Case 2. Interval base ages change between archived snapshots (C076)

- **Estimand:** changes in the modal base age of intervals between consecutive archived PBDB query
  products across three snapshot brackets, for intervals with at least 50 single-interval occurrences in
  the later snapshot.
- **Allowed:** "460, 317 and 17 intervals changed modal base age across the three main brackets; requiring
  the threshold in both snapshots gives 316 for the middle bracket"; "a query repeated on different dates
  can return different ages for the same interval".
- **Not allowed:** "every record's age changed"; "PBDB keeps no versions"; "PBDB ages are wrong"; any
  comparison with the ICS chart; "silently".

## Case 3. Excess rows in a database update and their effect on one analysis (C043, C045)

- **Estimand:** rows sharing a specified key in the 2023 Triton update; the subset removed by a conservative
  recipe that deletes lower-priority-source rows only from cross-source groups with recorded depth,
  retaining all rows from the highest-priority source; and the change that removal makes to EPRP's own
  Q-012 exposure means and pair classes.
- **Allowed:** "28,832 excess rows under our key, of which the conservative recipe removes 16,260";
  "removing them changed 1,388 of 2,267 comparable (unrounded) exposure means, 411 by at least one degree".
- **Not allowed:** "duplicates" without "under the specified key"; "keeps one row per key"; the
  unreproduced 1,454/423 figures, or the 11–13% inflation, anywhere except the audit trail and traps; any
  claim about effects on published Triton-based studies.

## Case 4. Stored sample ages disagree with recomputation (C040)

- **Estimand:** among the 56,387 of 61,862 NSB samples with both a stored and a recomputed numeric age,
  differences above 0.01 Myr between the stored age and linear interpolation from current tie points, with
  the first age taken at exact depth ties.
- **Allowed:** "4,111 of 56,387 comparable samples, in 56 holes, differ by more than 0.01 Myr; eight of
  these depend on the exact-tie convention".
- **Not allowed:** "4,111 of 61,862" as a rate; "the stored ages are wrong" or "the recomputed ages are
  right"; treating the exact-tie sensitivity as a test of other interpolation models.

## Case 5. Age–depth conversion above hiatuses (C096)

- **Estimand:** admtools 0.7.0 time-from-height conversion against exact linear-segment truth, in two
  controls on one synthetic two-hiatus model: a sparse tie-point version and a dense one, plus a targeted
  near-hiatus probe of the dense version.
- **Allowed:** "in the sparse model, 3,972 of 8,282 query points were mis-converted, with maximum error
  about 3.0 Myr; the dense model mis-converted six of the same queries, with maximum error 0.466 Myr; a
  targeted dense-model probe gave about 2.7 Myr"; "errors fall in affected interpolation segments".
- **Not allowed:** joining one control's count with another's maximum; "wrong above every hiatus"; any
  statement about StratPal or published studies.

## Case 6. Numbers compared as text (C102)

- **Estimand:** fossilbrush 1.0.6 range-flagging decisions on a deterministic grid of differences and
  thresholds, against numeric truth.
- **Allowed:** "at a threshold of 5 it missed differences of 10, 20, 49.9, 100 and 499, while flagging
  others, including 50 and 99, as character order predicts".
- **Not allowed:** a range such as "10 to 499 were missed"; a prevalence of misflagged records in real data;
  "fossilbrush cleaning is unreliable".

## Case 7. Calibration of preservation-rate and range-end estimators, with retained controls (C107, C194, C196, C105, C111)

- **Estimand:** coverage and median bias of retained posterior or analytic intervals, in two different
  declared simulation designs: PyRate preservation-rate intervals under a constant-rate, homogeneous-Poisson
  design; and classical range-end bounds for retained species in two simulated clades.
- **Allowed:** "PyRate's 95% preservation-rate intervals covered the truth in 81 of 100 and 33 of 50
  replicates and were shifted high; the retained width comparisons do not support the earlier 'too narrow'
  diagnosis, and do not establish calibrated widths or the cause of the shift"; "under homogeneous sampling
  in two simulated clades, classical bounds were near nominal (Strauss–Sadler 1,895 and 1,899 of 2,000 in two
  implementations; Robson–Whitlock 1,909 of 2,000), although the declared overall agreement gate failed (91%
  against 99%)"; "the G1 and G2 generator moment controls matched analytic expectations"; "the executed
  hiatus windows were shifted one Myr from the declaration".
- **Not allowed:** "too narrow"; "not too narrow" or "widths are correct"; "the checks tell good from bad";
  ranking PyRate against the classical bounds (different targets and designs); citing the positive controls
  without the failed gate; "the generators are validated".

## Case 8. What an interval measures, and a random-seed side effect (C110, C098)

- **Estimand:** GRIWM in Rextinct 1.1.0 on fixed synthetic dates: the dependence of its interval on input
  dating uncertainty, and the caller's random-number state after a call.
- **Allowed:** "the interval measures sensitivity of the estimate to uncertain dates, conditional on the
  records; it does not quantify uncertainty from the fossil-sampling process; with zero dating error it
  collapses to a point"; "the call overwrites the caller's random-number state" (an implementation
  finding).
- **Not allowed:** "wrong answer" or "invalid" for the interval; "users misread it"; "results using GRIWM are
  biased".

## Case 9. Plate-model spread and two reconstruction routes (C125, C123)

- **Estimand:** palaeolatitude range across three named plate models (MERDITH2021, PALEOMAP,
  MATTHEWS2016_pmag_ref) for a starting pool of 300 public points at six ages, each age's median taken over
  the points reconstructable in all three models (194 points in all six ages); and geometric differences
  between two routes for reconstructing TorsvikCocks2017.
- **Allowed:** "median spread is age dependent and not monotonic, from 2.9 degrees at 10 Ma to 13.6 at
  400 Ma, the largest"; "model choice can change latitude-band assignments"; "two routes to the same named
  model differ by an approximately rigid, age-specific rotation, consistent with different reference
  frames".
- **Not allowed:** "rising with age"; "error"; "the correct frame is"; "points move between bands" as a
  tallied result; a general palaeolatitude uncertainty.

## Case 10. Published spreadsheets that differ from their source (C035, C048)

- **Estimand:** cell-by-cell comparison of a published spreadsheet with the intact deposit it was made
  from (Monarrez et al. 2023 capture histories) or with chapter workbooks (Fossil Record 2).
- **Allowed:** "2,967 of 6,562 capture histories in the spreadsheet differ from the intact binary deposit;
  3,595 can be restored exactly by padding to the known width"; "220 rows of the one-file Fossil Record 2
  table are shifted one column left: 112 shift ranges only, two shift habitat and range, and 106 move a
  not-found-in-record flag".
- **Not allowed:** "5,291 histories are corrupted"; "the published results are affected"; a stated cause
  of the spreadsheet damage.

## Case 11. A printed probability (C190)

- **Estimand:** the upper tail of a binomial with n = 47, k = 28, p = 0.55, as stated in the prose of
  Rampino & Caldeira (2025).
- **Allowed:** "the stated test gives about 0.316, not the printed 3.4 × 10⁻¹⁶".
- **Not allowed:** "the periodicity result is refuted"; "the paper is wrong"; anything about the spectral
  analysis.

## Case 12. Archived scores that do not replay (C195, C193)

- **Estimand:** in INDITEK-2.0's deposited synthetic-observation proof example (Herrero-Gascón et al.
  2026), forward predictions and saved residual sums of squares for three archived rejected proposals,
  rerun with the original pinned harness and rescored by a separately implemented scorer.
- **Allowed:** "the prediction vectors reproduce within about 5 × 10⁻¹⁴, but the saved scores differ from
  rescoring by about 42.4, 17.5 and 11.9"; "the cause and any connection to published figures are
  unresolved".
- **Not allowed:** "replay exactly"; attributing the archive to Cermeño et al. (2022); "INDITEK cannot be
  reproduced"; "the calibration is wrong"; "an independent forward-model implementation"; calling the
  proposals accepted or posterior draws.
