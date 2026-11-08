# Supplement: case selection, replay and audit trail

<div id="authors"></div>

## S1. Case selection

The candidate pool is `papers/infrastructure-audit/evidence/claims.tsv`: 189 findings compiled read-only
on 25 October 2026 from the programme's database, package and reference catalogues. The twelve cases were
chosen on 8 November 2026 (`case-selection.md`) by five rules:

1. consequence for inference before defect status;
2. one case may hold several ledger rows;
3. coverage of the finding classes, including positive controls;
4. disclosure must be feasible;
5. findings of little consequence, and anything whose description could cause harm, are left out.

Four reserves were named in case a case failed replay: RevBayes's disabled fossilised birth–death range
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

- the input hashes;
- the command;
- the separate route by which a different actor rederived the result:
  - a fresh raw-data calculation;
  - a fresh pinned implementation;
  - reaggregation of retained outputs;
  - a mathematical or control check.

The `basis` column of the claims ledger names the route for each proposition, and the `limit` column
states what it does not show.

**What counts as independent.** The original findings were made in one set of sessions. The replays and
their checks were made by other actors using separate aggregation, interpolation, geometry or scoring
code. Some of those actors use the same model family as the original auditors. The checks are therefore
independent computational routes, not independent biological datasets, and they are not evidence that
using two model families helps.

**Software environment.** R 4.6.1 with admtools 0.7.0, fossilbrush 1.0.6 and Rextinct 1.1.0;
pyGPlates 1.0.0; content-pinned container images for the software runner. Full versions are recorded in
each replay record.

## S3. Statements withdrawn or narrowed during replay

| Case | Original statement | Found by | Replaced by | Record |
|---|---|---|---|---|
| 3 | 1,454 changed means, 423 by at least one degree; two per-bin class flips; 11–13% sample inflation | Codex replay, 8 Nov 2026 | [1,388]{.C045} changed means, [411]{.C045} by at least one degree; class flips as in C045 | `evidence/replay-20261108/data/README.md` |
| 4 | Sample count including a header row | Codex parent count | [61,862]{.C040} samples | `evidence/replay-20261108/main/nsb_count_review.json` |
| 5 | "Wrong times above every hiatus" | Codex replay | Errors in affected interpolation segments only | C096 limit |
| 7 | PyRate intervals "too narrow" | Codex replay | Undercoverage from location bias; widths not too narrow | C107 limit |
| 10 | 5,291 damaged histories | Codex replay | [2,967]{.C035} altered histories; 5,291 is the count of cells in scientific notation | C035 limit |
| 1 | Records described as "withheld" | Codex replay | Absent from a dated public snapshot; cause not established | C191 limit |

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
