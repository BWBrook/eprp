# Supplement: case selection, replay and audit trail

<div id="authors"></div>

## S1. Case selection

The initial candidate catalogue is `papers/infrastructure-audit/evidence/claims.tsv`: 189 candidate
findings, including positive controls and intended behaviors, compiled read-only on 25 October 2026 from
the program's database, package and reference catalogues. Later program findings were added to the
pool, including cases 11 and 12. The twelve cases were
chosen on 8 November 2026 (`case-selection.md`) by five rules:

1. consequence for inference before defect status;
2. one case may hold several ledger rows;
3. coverage of the finding classes, including positive controls;
4. disclosure must be feasible;
5. findings of little consequence, and anything whose description could cause harm, are left out.

Four reserves were named in case a case failed replay: RevBayes's disabled fossilized birth–death range
process, the optimal linear estimation interval's undercoverage in one package, a join error in a scraped
diversity table, and a silent identity rotation in a reconstruction library. None was needed.

## S2. Replay and independent check, by case

Each case was replayed on 8 November 2026 from pinned inputs. The replay records are in
`papers/infrastructure-audit/evidence/replay-20261108/`, in four parts:

- `main/`: cases 1 and 11, and the parent checks;
- `data/`: cases 2, 3, 4 and 10;
- `software/`: cases 5, 6, 8 and 9;
- `calibration/`: cases 7 and 12.

Each record states:

- the required inputs and their hashes;
- the replay command;
- the checks made by a different actor, which are specific to each case:
  - a fresh raw-data calculation;
  - a fresh pinned implementation;
  - reaggregation of retained outputs;
  - a mathematical or control check.

The `basis` column of the claims ledger names the route for each proposition, and the `limit` column
states what it does not show.

**What counts as independent.** Independence is check-specific. The replays were made by Codex's replay team (the main Codex session and bounded
GPT-6.1 Sol delegates), combined with separate aggregation, interpolation, geometry or scoring code where
the receipt records it. Not every proposition was rederived by a fully separate route: the INDITEK forward
run reused the original pinned harness, and only its scoring was separately implemented. Some reviewers
used the same model family and shared inputs. The checks are not independent biological datasets, and
they are not evidence that using two model families helps.

**Availability.** Some required inputs are retained locally rather than published: two content-pinned
container images, retained posterior logs and source archives. A cold rebuild from public inputs alone was
not validated.

**Software environment.** R 4.6.1 with admtools 0.7.0, fossilbrush 1.0.6 and Rextinct 1.1.0;
pyGPlates 1.0.0; content-pinned container images for the software runner. Full versions are recorded in
each replay record.

**Case notes.** Details that the main text cites to this section:

- **Case 3 (Triton).** The row key and the source-priority recipe are defined in
  `evidence/replay-20261108/data/results/paired_builds.json`. Python and the original R deletion
  memberships agree exactly.
- **Case 7 (calibration controls).** In the retained [20,000]{.C105}-row tables, the G1 birth–death mean and
  survival and the G2 Poisson-sampling moments agree with their analytic expectations; the paleobuddy and
  FossilSim dispersions are [0.9942762]{.C105} and [0.9903592]{.C105}[]{.C105}. The
  declared overall agreement gate (E4) failed, and the executed hiatus windows were shifted one Myr from
  the declaration; in that arm [728]{.C111} cases were excluded, leaving [1,272]{.C111}.
- **Case 9 (plate models).** The TorsvikCocks2017 model's authors document a hybrid mantle frame (anchor
  plate 0) and a paleomagnetic frame (anchor plate 1); the replay's rotation routine uses anchor 0. The
  observed route difference is consistent with a frame difference; the archived service's parameters
  were not established.
- **Case 11 (printed probability).** Four routes: the original direct exact-rational upper-tail sum and R
  (Codex reference session, 6 November), a complement recurrence and R (main Codex, 8 November), and
  integer-polynomial convolution (a bounded Codex reviewer).
- **Case 12 (INDITEK).** The forward replay reused the original pinned harness at the three proposal
  states; the model-free scorer was written separately.

## S3. Statements withdrawn or narrowed during replay

| Case | Original statement | Found by | Replaced by | Record |
|---|---|---|---|---|
| 3 | 1,454 changed means, 423 by at least one degree; two per-bin class flips; 11–13% sample inflation | Codex replay, 8 Nov 2026 | [1,388]{.C045} changed means, [411]{.C045} by at least one degree; class flips as in C045 | `evidence/replay-20261108/data/README.md` |
| 4 | Sample count including a header row | Codex parent count | [61,862]{.C040} samples | `evidence/replay-20261108/main/nsb_count_review.json` |
| 5 | "Wrong times above every hiatus" | Codex replay | Errors in affected interpolation segments only | C096 limit |
| 7 | PyRate intervals "too narrow" | Codex replay | Undercoverage with upward-shifted intervals; width comparisons do not support "too narrow" and do not establish calibrated widths | C107 limit |
| 10 | 5,291 damaged histories | Codex replay | [2,967]{.C035} altered histories; 5,291 is the count of cells in scientific notation | C035 limit |
| 1 | Records described as "withheld" | Codex replay | Absent from a dated public snapshot; cause not established | C191 limit |
| 5 | First draft joined the sparse-model count with the dense-model maximum | Codex wording review, 8 Nov 2026 | Each control reported separately | `docs/audits/2026-11-08-wording-review.md` W01 |
| 12 | First draft attributed the INDITEK archive to Cermeño et al. (2022) and said predictions "replay exactly" | Codex wording review | Herrero-Gascón et al. (2026) synthetic proof example; vectors within about $5 \times 10^{-14}$ | W02 |
| 7 | First draft said the PyRate intervals "are not too narrow" | Codex wording review | Width calibration not established either way | W03 |
| all | First draft said every proposition was rederived by a separate route, and that anyone can rerun every case | Codex wording review | Check-specific independence; locally retained inputs named | W07, W08 |

## S4. Reproduction

From the repository root:

```sh
python3 papers/infrastructure-audit/tools/claims.py check \
  papers/infrastructure-audit/manuscript/claims.csv \
  papers/infrastructure-audit/manuscript/text/{main,supplement,brief,for-agents}.md
```

Each ledger row carries its own `reproduce` command and the commit at which its evidence was verified.
Third-party archives are not redistributed; each replay record names the source and its hash, so a
reader can obtain and verify the same input. Records absent from public database snapshots are reported
as counts only and are not reproduced here.

## References
