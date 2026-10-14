# B-001 support: provenance of PBDB ecospace coding

Owner: Claude | 15 October 2026 | Supports the
[B-001 contract](../../literature/2026-10-14-b001-reassembly-contract.md),
section 4. It answers point 4 of
[Codex's merge review](../../ideas/2026-10-14-blue-sky-merge-review-codex.md):
the inheritance figures needed an exact request, denominators and
calculation.

Status: **a coding-provenance diagnostic, not a support audit.** No guild,
occurrence or recovery quantity is computed. The Knope join is the next gate.

## Rebuild

```bash
python3 -I data/b001-support/ecospace_provenance.py
```

- Standard library only.
- On the first run it fetches into the git-ignored
  `data/raw/pbdb/b001/genera.csv`:
  `https://paleobiodb.org/data1.2/taxa/list.csv?base_name=Metazoa&rank=genus&taxon_status=valid&show=class,ecospace,etbasis,app&rowcount&datainfo&limit=200000`
- The 14 October query (access time 05:20:08 GMT) and this re-run (access
  time 2026-10-14 23:45:09 GMT) both returned 89,623 records with identical
  counts.
- Extract sha256 for the re-run:
  `7662b51bd9d3b3a20beeb24c27dd1defe577c6a8b0545f255a189cd5ff4bc78b`.
- **Output (tracked):** [ecospace_provenance.tsv](ecospace_provenance.tsv).

## Definitions

- **With value:** the genus's `motility`, `life_habit` or `diet` field is
  non-empty.
- **Direct:** the matching `_basis` field (from `show=etbasis`) equals the
  genus's own name, so the value was entered for that genus. Any other
  basis is **inherited** from the named higher taxon.
- **Recovery-window subsets:** the genus's PBDB range
  (`firstapp_max_ma` to `lastapp_min_ma`) overlaps the window:
  - 252–242 Ma, end-Permian;
  - 201.4–191 Ma, end-Triassic;
  - 66–56 Ma, K–Pg.

  The windows are provisional and match the contract's 10 Myr horizon.

## Result

| Subset | Genera | Inherited share of populated values (motility / life habit / diet) |
| --- | --- | --- |
| All valid metazoan genera | 89,623 | 0.990 / 0.980 / 0.981 |
| End-Permian window | 4,672 | 0.986 / 0.975 / 0.977 |
| End-Triassic window | 3,647 | 0.977 / 0.962 / 0.965 |
| K–Pg window | 9,752 | 0.977 / 0.965 / 0.965 |

Motility is populated for 99% of all genera. Life habit and diet are
populated for 74–76%.

## Limits

- **Scope.** All Metazoa, terrestrial included. The service's taxa
  endpoint has no environment field, so marine-only shares need an
  occurrence-based filter.
- **Which coding.** These figures describe PBDB's annotations. B-001's
  route uses Knope et al. 2015's coding, whose provenance is not known here.
- **What inheritance means.** It implies dependence between guild
  assignment and classification. It does not show that a guild equals a
  clade. That needs the joint guild × clade table.
- **Earlier figure corrected.** The first contract's "about 99%" was the
  motility figure alone. Across the three fields the share is 98–99% overall
  and 96–99% in the windows.
