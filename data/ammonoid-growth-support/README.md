# Ammonoid growth data: access and transition-support gate

Codex, 14 October 2026. Supports D2 / proposed B-002. This is an access audit,
not a numerical inspection of the workbook. The
[developmental-route contract](../../literature/2026-10-14-ammonoid-developmental-route-contract.md)
states the scientific comparison and stopping conditions.

## Source and observed access

Walton & Korn (2018), [Dryad 10.5061/dryad.c17p8](https://doi.org/10.5061/dryad.c17p8),
for their [2017 article](https://doi.org/10.1111/pala.12308).
The [source manifest](source-manifest.json) preserves the relevant API fields
and this retrieval's outcomes. Dataset metadata and its one-file inventory
were successfully read from the official Dryad API on 14 October 2026.

| Field | Verified metadata value |
| --- | --- |
| Dataset / version IDs | 7205 / 7242; version number 1 |
| Publication / metadata modification | 2018-05-16 / 2020-06-24 |
| File ID and name | 34579; `Ontogenetic_Conch_Parameter_Data.xlsx` |
| Advertised bytes | 215,182 |
| Provider MD5 | `0302022d2f622b73754cf0e66c54f2ac` |
| Dataset licence | CC0-1.0, as reported by the dataset API |
| Official API download | HTTP 401 |
| Official browser file stream | HTTP 403 |

The article/deposit description advertises 177 species, taxonomic affiliations,
geological stages, source references, and conch-width, umbilical-width and
whorl-expansion series. These are **source descriptions**, not observed workbook
headers or independently verified counts. Neither the XLSX bytes nor its
checksum, sheets, formulas or numerical values were inspected. The HTTP error
responses were not saved as a workbook. Repeated unchanged retrieval attempts
were stopped.

Original API responses and retrieval log are locally under ignored
`data/raw/ammonoid-growth-walton-korn-2018/`. The tracked manifest makes the
resource identifiable without depending on those local copies. It contains the
exact metadata/download URLs and expected checksum. Another agent can retrieve
the file through ordinary Dryad access and compare bytes/MD5 before inspection.

## What can be counted now?

| Quantity | State | Reason |
| --- | --- | --- |
| Advertised study species | 177, source claim | Article abstract and repository description agree |
| Actual workbook species/specimens/series | Unverified | Content not retrieved |
| Complete juvenile-to-adult trajectories | Unverified | Stage coverage and specimen linkage not inspected |
| Repeated measurements and uncertainty | Unverified | Workbook/source-level replication unknown |
| Sister or ancestor–descendant transitions | Unverified | No transition table has been inspected; taxonomic affiliation alone would not establish one |
| Independent eligible transitions | Unverified | Requires phylogenetic, chronological, physical and source-reuse checks |

An unverified count is not zero. In particular, the 177-species study count is
not 177 independent evolutionary transitions or biological replicates.

## Finite content audit once the source is available

1. Preserve the source unchanged and verify size/MD5 against the manifest.
   Inventory sheets, headers, notes, formulas and stored values before parsing.
2. Separate species, individual specimens, whorl measurements and reconstructed
   or pooled trajectories. Retain original spellings, measurements and units;
   record uncertainty in added fields.
3. Count observed growth ranges, missing early whorls, terminal-size coverage,
   dimorphism assignments and repeated specimens. A large final measurement
   is not automatically a mature individual; diameter is not chronological age.
4. Crosswalk each series to its primary source and actual geometry. Identify
   which shell thickness, body-chamber, chamber/septal and scale information is
   measured, borrowed or unavailable. Dimensionless shape indices do not alone
   identify hydrostatic performance.
5. Audit any claimed phylogenetic transitions separately: evidence for the
   relation, temporal ordering/uncertainty, linked juvenile/adult measurements,
   maturity, independent source material and alternative relationships.
   Shared genus membership or neighbouring stages are not ancestry.
6. Report candidate, excluded and unresolved relationships with reasons. A held-out
   prediction must reserve entire source/lineage blocks where they share
   specimens or reconstructions. More rows from one specimen do not add
   independent transitions.

No workbook adapter, transformed table or empirical fit has been created. The
current result is **support gate unpassed because source content is inaccessible**.
It does not show that suitable growth data or phylogenetic evidence are absent.
