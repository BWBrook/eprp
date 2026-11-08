# Case selection for the infrastructure-audit case series

Claude, 8 November 2026. Barry, Claude chat, 8 November 2026 (exact): "Go
with the infrastructure-audit case series". That chooses this paper for the
programme's development slot, following the recommendation in Board 144/2994.

This note picks the cases from the 189 candidates in
[evidence/claims.tsv](evidence/claims.tsv). Every case still has to pass
replay and an independent check before it enters any product (gates 2 and 3
in the [README](README.md)).

## Selection rules

1. **Consequence for inference first.** A case earns its place by what it
   would change in an analysis that someone plausibly runs. Being a defect
   is not enough on its own.
2. **One case can hold several ledger rows.** The rows that support a case
   are listed together; the paper counts cases, propositions and checks
   separately.
3. **Cover the classes in Codex's audit design**, including at least one
   positive control. A series that only finds faults says nothing about how
   discriminating the checks were.
4. **Disclosure must be feasible.** Every third-party case has a queued
   contact ID or gets one. Release waits for disclosure.
5. **Leave out** licence-metadata conflicts and library-metadata findings,
   which matter little for inference, and anything whose description would
   itself do harm. SahulArch's location protection stays out of the case
   series and appears only in general terms.

## The twelve cases

| # | Case | Ledger rows | Class | Why it matters for inference | Status now |
| --- | --- | --- | --- | --- | --- |
| 1 | **Withheld PBDB records in published deposits and derived archives** | C001, C031, C069; the Benson 2025 deposit share (16.7% overall, 19.28% of Mollusca; `data/q027-regional-support/`) | sensitive access finding | Published analyses rest partly on records that are no longer publicly reproducible. In Q-027 the stages with three outside-EU/NAm tropical regions fell from 14 to 12 of 21 when only current public members were kept. | C001 audited (225,362); counts only |
| 2 | **PBDB is live and unversioned, and has re-dated its intervals** | C021, C075, C076 | intended version choice and data inconsistency | The same query on different dates returns different ages. Three main re-datings and two small ones fall between consecutive chronosphere snapshots, and some move boundaries off the ICS chart. | C076 aggregate summary; C021 and C075 not audited |
| 3 | **Triton's 2023 update dropped deduplication** | C043, C045, C046 | data inconsistency, with an internal downstream effect | 28,832 duplicates returned. EPRP's own Q-012 exposure index changed in 1,454 of 2,267 lineage-bins, a measured effect on an analysis. | C043 partly audited; C045 not replayed (needs paired builds) |
| 4 | **NSB's final snapshot holds stale sample ages** | C040, C078 | data inconsistency | Ages recomputed from current tie points differ from the stored ones, so any rate or timing analysis on the stored ages inherits the drift. | C040 arithmetic verified |
| 5 | **admtools `strat_to_time` returns wrong times above every hiatus** | C096 | implementation defect | Age–depth conversion is the first step in many stratigraphic analyses. The error affects every point above a hiatus (dense-sample maximum 0.466 Myr). | mechanism replayed |
| 6 | **fossilbrush `flag_ranges` compares numbers as text** | C102 | implementation defect | Range-flagging decisions depend on string order rather than magnitude, so which records are cleaned depends on the formatting of the numbers. | per-row arithmetic verified |
| 7 | **PyRate's preservation rate is biased high and its intervals undercover; the classical range-end bounds are calibrated** | C107, C111, C105 | calibration failure under a stated model, with positive controls | A widely used Bayesian tool undercovers on simulated records with unsampled species, while Strauss–Sadler and Robson–Whitlock bounds are calibrated under homogeneous sampling. Together they show the bench discriminates. | C107 per-replicate verified; C111 recorded (overall E4 gate failed, kept) |
| 8 | **GRIWM's interval is not an interval for the extinction time, and its seed reset** | C110, C098 | semantic finding and implementation defect | Users read the 2.5–97.5% spread as a confidence interval for extinction time; it is the spread of the estimate under resampling of dating error. The seed reset silently couples replicate streams. | C110 reclassified as semantic; C098 not audited |
| 9 | **Plate-model choice moves palaeolatitudes by degrees, and one model ships in two frames** | C125, C123, C119 | intended model choice and model-file ambiguity | Latitude-band assignments, and so diversity-gradient analyses, change with the model. This links directly to Q-027's latitude bands. | C125 spread independent; C123 geometry independent |
| 10 | **Corrupted published deposits** | C035 (Monarrez 2023 capture-history column), C048 (Fossil Record 2 column shift) | deposit integrity | A capture-mark-recapture analysis reads capture histories directly. A one-column shift misassigns 112 families' ranges. | not audited |
| 11 | **A published significance value off by fifteen orders of magnitude** | new row (Rampino; Board 76/2911 and 96/2963) | arithmetic error in a published claim | The printed binomial p of 3.4e−16 for n = 47, k = 28, p = 0.55 is exactly 0.3159 (independently checked twice). The separate spectral result is not refuted, and the paper must say so. | checked; needs a ledger row |
| 12 | **A published model's archived calibration does not replay** | INDITEK-2 review (`resources/software/reviews/2026-10-28-inditek-forward-and-claims/`) | replay failure | The saved RSS scores of three proposal variants differ from the rerun by 42.4, 17.5 and 11.9, and the archived inverse chains mix poorly. Spatial-diversity conclusions built on that calibration cannot be checked from the archive. | Packages review F2 fails; needs a ledger row and careful wording |

**Reserve, if a case fails replay:** RevBayes' disabled FBD range process
(C097); EDE's OLE undercoverage (C112); the palaeoverse sepkoski join
(C095); pygplates' silent identity rotation (C094).

## Section 4: the agents' own errors

Report these as cases of the method, with receipts:
- the re-mirrored Cooke version;
- the invalid GRIWM arm after the seed reset;
- the corrected RevBayes lead L-001;
- cross-agent corrections in the main programme, for example the
  life-history fixed-sign rule, recoverability source errors, the B-002
  decoupling claim and Claude's Q-027 pairing prediction.

## What happens next

1. **Codex replays each case** from pinned inputs, enters the supporting
   claims as `provisional` in `manuscript/claims.csv` (living-paper format),
   and records the replay command and evidence commit. Each claim becomes
   `supported` only after a check by someone other than its author, by a
   separate route.
2. **Claude writes `manuscript/estimands.md`** once the replays land: what
   each case licenses, and the phrasings that are not allowed (for example
   "widespread", "the database is wrong" where the finding is an intended
   version choice, or any prevalence claim).
3. **Drafting order:** article and supplement, then agent guide, then
   brief.
4. **Before any release:** the queued provider and author contacts go out
   (Barry), and the `efb2c4b` history and `pbdb_access_global.tsv` blockers
   are resolved.

**Build note.** The scaffold builds. `make` needs
`TMPDIR=$PWD/manuscript/build/tmp` on this machine, because makedoc renames
a temporary file from `/tmp` across filesystems. `make check` fails until
`references/dois.txt` has entries.
