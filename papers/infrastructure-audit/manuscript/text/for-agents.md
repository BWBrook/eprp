---
document: agent-facing paper
study: Infrastructure-audit case series (twelve checked cases from agent-assisted audits of paleobiology's data and software; target journal Paleobiology)
status: internal draft
human_paper: papers/infrastructure-audit/manuscript/text/main.md (+ supplement.md, brief.md)
claims_ledger: papers/infrastructure-audit/manuscript/claims.csv (single source for all renderings; checked by tools/claims.py)
interpretation: papers/infrastructure-audit/manuscript/estimands.md (what each case establishes; allowed and forbidden phrasings)
governing_docs: [papers/infrastructure-audit/README.md, papers/infrastructure-audit/case-selection.md, papers/infrastructure-audit/evidence/replay-20261108/README.md]
authority: Barry W. Brook decides provider and author contact, public release of the paper, submission and any correspondence outside the collaboration
updated: 2026-11-12
---

# Infrastructure-audit case series for agents: what was established, how to verify it, and how not to break it

This is the paper written for an agent arriving cold. The human paper argues; this one indexes. Paths in
the front matter are relative to the repository root. In the body, paths are relative to
`papers/infrastructure-audit/` (the paper root) unless they start with `data/`, `resources/` or
`docs/correspondence/`, which are relative to the repository root. When this file and a primary artefact disagree, the artefact wins
and this file is wrong: fix it in the same commit.

## 1. Read order and trust

1. This file, then `manuscript/estimands.md`, then `manuscript/claims.csv`. Quote a claim only with its
   limit.
2. `evidence/replay-20261108/README.md` and its four subdirectories for how each case was replayed.
3. `manuscript/text/main.md` for the argument; `supplement.md` for selection, replay, case notes and the
   audit trail. `reconstruction/` records how the article was rebuilt from first principles (working
   abstract to full draft, 12 November 2026), with Codex's critique of each step in `docs/audits/`.
4. `evidence/claims.tsv` is the 189-row candidate pool from 25 October. It records discovery, not
   clearance. Never cite a number from it without a matching supported row in `manuscript/claims.csv`.

`status` is *supported* (replayed by a different actor and checked by the routes recorded in its receipt;
independence is check-specific, see `basis`), *provisional*, *refuted* or *superseded*. All 22 rows were
supported on 8 November 2026.

## 2. The answer, as claims

Each case is coded by the family of check that established it (Methods; Table 1): **DP** data provenance
and transformation, **CI** computation and implementation, **MS** model sensitivity, **OI** output
interpretation and calibration. Cases 1–4 and 10 are DP; 5, 6, 11 and 12 are CI; 7 is OI; 8 is OI with CI;
9 is MS. The families are defined by what was compared, not by cause.

- **Case 1.** Deposited records absent from a dated public snapshot: C191, C192. [71,103]{.C191} of
  [368,760]{.C191}; regional screen [14]{.C192} to [12]{.C192} of [21]{.C192} stages.
- **Case 2.** Interval base ages change between archived snapshots: C076. [460]{.C076}/[317]{.C076}/[17]{.C076}.
- **Case 3.** Excess rows in Triton's update and their effect on Q-012: C043, C045. [1,388]{.C045} of
  [2,267]{.C045} means changed.
- **Case 4.** Stored NSB ages against recomputation: C040. [4,111]{.C040} of [56,387]{.C040} comparable
  samples (of [61,862]{.C040} in the snapshot) differ by more than 0.01 Myr, under linear interpolation from
  current tie points with the first age at exact depth ties. Eight disappear with the other exact-tie choice;
  that does not test other interpolation between ties.
- **Case 5.** admtools height-to-time conversion: C096.
- **Case 6.** fossilbrush text comparison: C102.
- **Case 7.** PyRate calibration with positive controls: C107, C194, C196, C105, C111.
- **Case 8.** GRIWM semantics and random-number state: C110, C098.
- **Case 9.** Plate-model spread and reconstruction routes: C125, C123.
- **Case 10.** Published spreadsheets: C035, C048.
- **Case 11.** A printed binomial probability: C190, [0.316]{.C190}.
- **Case 12.** INDITEK archived scores: C195, C193.

## 3. Vocabulary that the files use

| Term | Meaning |
|---|---|
| dated public member | an occurrence present in the public PBDB snapshot of 23 October 2026; absence is not evidence of withholding |
| excess rows under the key | rows beyond the first sharing a specified Triton key; not necessarily repeated observations |
| first-tie convention | taking the first age when two NSB tie points share a depth |
| E4 | the declared overall agreement gate in the range-end calibration benchmark; it failed |
| arm | a simulation design condition (e.g. ideal, hiatus; psi 1.0, psi 0.25) |
| rejected proposal | an INDITEK calibration state the sampler did not accept; not a posterior draw |
| route | a computational path to a result; independence is check-specific (see each row's `basis`) |
| replay team | main Codex with GPT-6.1 Sol subagents, 8 November 2026; Codex also first recorded cases 11 and 12 |
| DP, CI, MS, OI | the four families of check; see section 2 |

## 4. Provenance map

| Result | Inputs | Code and receipts | Claims |
|---|---|---|---|
| Cases 1, 11 | Benson deposit and PBDB snapshot (hashes in receipts, not redistributed); published paper | `evidence/replay-20261108/main/` | C191, C192, C190 |
| Cases 2, 3, 4, 10 | Archived PBDB query products; Triton RData; NSB SQLite; Monarrez and Fossil Record 2 deposits | `evidence/replay-20261108/data/` | C076, C043, C045, C040, C035, C048 |
| Cases 5, 6, 8, 9 | Content-pinned package images; raw plate-model archives | `evidence/replay-20261108/software/` | C096, C102, C110, C098, C125, C123 |
| Cases 7, 12 | Retained posterior logs and benchmark tables; INDITEK-2 archive | `evidence/replay-20261108/calibration/` | C107, C194, C196, C105, C111, C195, C193 |

Each ledger row's `reproduce` field is the exact command; its `commit` pins the verified evidence bytes.

## 5. Traps: superseded results and known misreadings

1. **"Withheld PBDB records."** The checked object is absence from a dated snapshot. Cause is not
   established (C191).
2. **"28,832 duplicates."** They are excess rows under a key (C043).
3. **"1,454 changed means, 423 by a degree or more."** Not reproduced; use C045's [1,388]{.C045} and
   [411]{.C045}.
4. **"admtools is wrong above every hiatus."** False; only affected segments (C096).
5. **"PyRate's intervals are too narrow" or "are not too narrow".** Neither is established. The
   intervals are shifted high; the width comparisons do not settle width calibration or the cause (C107).
6. **"5,291 damaged histories."** That is the scientific-notation cell count; altered histories number
   [2,967]{.C035} (C035).
7. **"The classical methods are calibrated."** Only in the ideal arm of two simulated clades, and the
   overall E4 gate failed (C194, C196).
8. **"Rampino and Caldeira's periodicity is refuted."** Only the printed binomial tail is checked (C190).
9. **"INDITEK cannot be reproduced."** Predictions replay; three saved scores do not (C195, C193).
10. **"admtools: 3,972 of 8,282 wrong, by up to 0.466 Myr."** That joins the sparse-model count with the
    dense-model maximum. Report each control separately (C096; review W01).
11. **"INDITEK-2 is Cermeño et al. (2022)" or "predictions replay exactly".** The archive is the
    synthetic-observation proof example of Herrero-Gascón et al. (2026); vectors agree within about
    5e-14 (C195; review W02).
12. **Comparing the Robson–Whitlock and PyRate coverages as a ranking.** Different targets and designs
    (C194, C107; review W04).
13. **"Every proposition was independently rederived" or "anyone can rerun every case".** Independence
    is check-specific, and some inputs are retained locally (review W07, W08).
14. **Any prevalence, cost or method-superiority statement.** The series is a set of cases, with no
    comparison (`estimands.md`, cross-cutting rules).
15. **"Each case was replayed by an agent other than its original finder."** False for cases 11 and 12,
    which Codex first recorded and Codex's replay team checked (`docs/audits/2026-11-12-full-draft-provenance.md`).
16. **"The TorsvikCocks2017 routes use the authors' two documented frames."** The geometry is consistent
    with a reference-frame difference; the archived service's frame setting is not identified (C123;
    review S4-01).
17. **The seven-class scheme of the 8 November draft** (implementation defect, data inconsistency,
    calibration failure, semantic finding, intended choice, membership, replay failure). Superseded by the
    four families of check in section 2.

## 6. Checks before and after any change

From the repository root:

```sh
cd papers/infrastructure-audit
uv run tools/refs.py build        # bibliography from references/dois.txt
make -C manuscript check          # claims, glyphs, makedoc lint and citation audit
TMPDIR=$PWD/manuscript/build/tmp make -C manuscript   # PDF and DOCX; TMPDIR avoids a cross-device rename
```

Invariants: every cited number matches its ledger value; all 22 supported rows are cited; no text adopts
an interpretation listed as not allowed in `estimands.md` (quoting one as a trap or withdrawn statement is
allowed); `docs/audits/` holds the triage of every review.

## 7. Open edges

- **Disclosure.** Provider and author contacts are queued (Barry's decision). Their replies may show a
  finding is known, intended or fixed; update the case and its limit if so.
- **Downstream consequence.** No published analysis was rerun. Rerunning one that uses an affected layer
  would measure consequence directly.
- **Comparison.** Nothing here compares agent-assisted with human auditing.
- **Figures.** Figures 1–3 are drawn by `manuscript/figures.py` (`uv run manuscript/figures.py` from the
  paper root) from the replay receipts and the checked tables in `evidence/figure-data-20261112/`; the
  script asserts every plotted count against its ledger value. The brief figure, `figB1_brief`, comes from the same script.
- **Sources.** Raup 1972 and the original Robson–Whitlock passages are unread; GTS2020 is cited only as
  the named reference work (`resources/library/notes/2026-11-12-infrastructure-audit-citations.md`).
- **Declarations.** Acknowledgments, funding and competing interests await Barry.

## 8. Conduct in this repository

- Works without a usable Crossref record go in `references/manual.yaml`; edited books carry their
  editors as one literal author string so the Paleobiology CSL renders them as books.
- When adding a DOI, review the generated citation key and add it exactly to the repository's
  `.gitleaks.toml` allowlist; no pattern-based exemption.
- Read `AGENTS.md` (or `CLAUDE.md`). Facts and citations come from sources read in the task; every DOI
  is checked against Crossref.
- To add or change a claim: edit `manuscript/claims.csv`, reverify the evidence, run
  `python3 tools/claims.py stamp manuscript/claims.csv ID`, then make every document pass the check.
- Change `manuscript/estimands.md` before changing how a result is described.
- Restricted PBDB material: counts only, no identifiers, no access mechanism.
- Do not edit generated artefacts by hand: `references/refs.yaml`, marked table blocks, `figures/`,
  `build/`.
