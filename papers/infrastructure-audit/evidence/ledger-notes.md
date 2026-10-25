# Claims ledger: first pass (25 October 2026)

`claims.tsv` holds 189 claims in nine columns:
- `claim_id`;
- `category`;
- `finding`;
- `evidence`, as path:line;
- `replay`;
- `checks_recorded`;
- `sensitivity`;
- `owner_session`;
- `related`.

**How it was compiled.** A Claude Sonnet subagent compiled it read-only from
the side sessions' catalogues (`resources/sources/`, `resources/software/`
and `resources/library/`). It then checked every cited path and line range by
script, and checked that each cited number appears in the cited lines.
Claude, main session, spot-checked C001 and C096 against their sources, and
checked the structure (189 rows, no malformed rows) and the absence of email
addresses.

**What first-pass status means.** The ledger records what the catalogues
*say*. No number has yet been replayed against data. That is gate 2 in the
[README](../README.md).

## Counts

| Category | Claims |
| --- | ---: |
| provenance-deposit | 54 |
| process-receipt | 29 |
| coverage | 24 |
| timescale | 20 |
| data-access | 19 |
| spatial-model | 14 |
| software-correctness | 13 |
| library-metadata | 9 |
| software-calibration | 7 |

| Owner session | Claims |
| --- | ---: |
| Databases | 143 |
| Packages | 30 |
| References | 14 |
| Databases and Packages | 2 |

**The scout's ten most consequential:**
1. [Detail withheld pending disclosure to the data custodian.]
3. **C076 and C077:** PBDB re-datings.
4. **C043 and C045:** Triton's deduplication was dropped. Q-012's exposure
   index changes in 1,454 of 2,267 lineage-bins.
5. **C040:** stale NSB ages.
6. **C096:** admtools `strat_to_time`.
7. **C107:** PyRate's q bias.
8. **C110 and C111:** GRIWM intervals and hiatus effects on bounds.
9. **C119, C123 and C125:** plate models.
10. **C102:** fossilbrush `flag_ranges`.

## Inconsistencies across catalogue files

These go to the owning side sessions. The main session does not edit their
files.

1. [Detail withheld pending disclosure to the data custodian.]
2. **BioTIME local loss.** A "24% pooled" figure in `sources/README.md:594-597`
   does not appear in the entry, which gives 36% pooled and 32% by site.
3. **PBDB** `modified` before `created`: 17.1% (C10 d) against 11%, or
   204,301 (`pbdb/README.md:352-353`).
4. **Neotoma default-chronology counts:** C11 a against
   `neotoma/README.md:113, :149-152`.
5. **Stale review text.** `software/README.md:54-56` says "All five were
   reviewed", but the table lists 15.
6. **Barry's 2003 EndNote tier:** 491 (`library/README.md:71`) against 493
   (the notes and INDEX).
7. **Missed-deposit count:** 20 listed (`sources/README.md:502-507`) against
   19 (`register-deposits/README.md`).
8. **PBDB re-datings** are "three main steps and two small ones", not
   "three". The paper must say so.
9. **The Australian PBDB subset:** BACKLOG against the pbdb entry. BACKLOG
   says the entries supersede it.
10. [Detail withheld pending disclosure to the data custodian.]
11. **palaeoverse "GTS2020"** is said to be chart v2020/03, but it equals
    v2020/01 at 59 of 60 stages (`bench/README.md:264`).
12. **Unresolved:** C150, "22% of paired collections shared nothing", could
    not be traced to an entry.

## Items that need care before any release

- [Detail withheld pending disclosure to the data custodian.]
  - **Now:** the repository is private, so nothing is exposed.
  - **Before any public release** of the repository or a derived archive,
    either publish from a fresh repository or rewrite history. That is
    Barry's decision, and a history rewrite on a shared branch is a one-way
    door.
- **Reviewer independence.** Every catalogue review recorded was by a Claude
  Sonnet subagent, apart from GitHub Copilot's review of the pull requests.
  - Two entries (krapp2021, fred) were never reviewed.
  - Three were not re-reviewed after fixes.

  The paper must say this plainly. Codex's audit would be the first
  non-Claude reviewer of the claims.
- [Detail withheld pending disclosure to the data custodian.]
- **Third-party defects** carry their queued contact IDs in the `sensitivity`
  column: C1–C35 for data and S1–S11 for software. Nothing has been sent.
  Disclosure precedes release.
- **The agents' own errors** are under `process-receipt`, for example the
  re-mirrored Cooke version, the invalid GRIWM arm after the seed reset, and
  the corrected RevBayes lead L-001. These are material for section 4.

## Codex's first independent audit (25 October; `085b5b8`)

[priority-review-2026-10-25/](priority-review-2026-10-25/README.md) covers 16
priority rows and records its verdicts in the ledger's `audit_status` and
`audit_note` columns. The other 173 rows are not yet audited. Its
reaggregation replays byte-identically. It summarises saved outputs; it does
not rerun the original extraction or fitting.

**Corrections now in the ledger:**
- [Detail withheld pending disclosure to the data custodian.]
- C096's dense-sample maximum is 0.466 Myr, and "above every hiatus" is
  qualified.
- C110 is reclassified as an interval-semantics finding, not a bug.
- C111: the overall E4 gate **failed**.
- C031, C069, C119 and C125 now state their denominators and how far their
  units are independent.
- C045's notification statement is stale, and C045 is not replayed.

## Release blockers and owner actions (updated)

- [Detail withheld pending disclosure to the data custodian.]
  - **The Databases owner** should review it, then quarantine it or replace
    it with a counts-only receipt, within Barry's hold and before any public
    artefact is assembled.
  - Nothing has been deleted, and nothing will be without Barry's decision.
- **The Packages owner** should document the deviation in VALIDATION_T2's E5
  declaration: the hiatuses were executed 1 Myr earlier than declared. Keep
  both records, and decide whether the declared design needs a companion
  run.
- **The Q-012 and Q-007 owners** should save paired builds, from the original
  inputs and with conservative deduplication, plus a row-joined diff. That
  moves C045 from an observation to replayable evidence.
- **The Databases and Packages owners** should supply pinned replay paths
  for the priority claims, as listed in the priority review: NSB and Triton
  snapshot manifests, an offline counts-only path for PBDB access, and the
  admtools, fossilbrush, PyRate and Rextinct images.
