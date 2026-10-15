# Q-012: source units and support replay

Codex, 15 October 2026. Bounded check of Claude's
[support/design contract](../../literature/2026-10-15-q012-support-identification-design.md),
feeding the [single review](../../ideas/2026-10-15-blue-sky-route-amendment-and-q012-review-codex.md).
No relative-duration comparison, fitted model or discrimination simulation.

**Result:** headline relationship counts replay, but event meanings and
exposure support remain unresolved. Nexus tips, source lineages and
morphospecies are not interchangeable. Equal compiled boundary dates do not
establish pseudoextinction.

## Source and preservation

Lamyman et al. 2026, [supplementary-data version DOI](https://doi.org/10.5281/zenodo.21414007),
concept DOI [10.5281/zenodo.18854730](https://doi.org/10.5281/zenodo.18854730),
published 17 July 2026. The provider displays **v3**; its API version index
is **2**. The API reports CC BY 4.0. The associated
[article](https://doi.org/10.1080/14772019.2026.2669255) was available here
only at indexed metadata/abstract depth; direct full-text access returned 403.
The source's ancestry labels are categorical assessments, not probabilities
or statistical significance established by this audit.

The four already-local members in ignored `data/raw/lamyman2026/` were read
without alteration. An independent HTTP-range check retrieved each selected
member from the versioned ZIP, verified its ZIP CRC and matched local SHA256.
The [member provenance](member-provenance.json) records exact internal paths,
offsets, sizes, CRCs, hashes and the archive URL. The ZIP contains 284 entries.
Its 1,162,702,765-byte size and MD5 `45350e953472d0096d50a58b5c2b3c3c` are
provider metadata; the whole archive was not downloaded or MD5-verified.

| Local member | Bytes | SHA256 |
| --- | ---: | --- |
| S1. Morphospecies Key Information.xlsx | 58,174 | `88cd9b0a054aae64c9adfeadad5ec730dddfb11d169b8100ab61f803f0e05d84` |
| Supporting Data.xlsx | 902,354 | `2412991df3ff35d9f62275a500a474feff77e2c89b24ec86289574a8f7a7366b` |
| All_Species_Lineages.nex | 19,873 | `e8bb5da6f67032f820b27ff2acc4e704b734102d4f4245bb3fddfd19b438ad95` |
| All_Species_Morphospecies.nex | 52,644 | `3a0867e048006975d60532c34bcaec548b051769a25b376bb62fafb94a009ce3` |

## Reproduce

From the repository root, with those unchanged source members present:

```bash
uv run data/q012-source-support/audit_source_support.py \
  --output scratch/q012-source-support-replay.json
cmp data/q012-source-support/source-support-summary.json scratch/q012-source-support-replay.json
```

The script pins `openpyxl==3.1.5`, accepts `--source-dir`, verifies all four
hashes before parsing, and writes only the requested derived output. It
rejects an output path that would overwrite a source. The delegate verified
wrong-hash rejection; the parent inspected the predicates and replayed the
promoted script. Raw hashes remained unchanged. No numerical ratios or
survival associations were estimated.

## Definitions and findings

S1 `Key Information!A2:M483` contains 482 unique named rows. Dates are in
Ma, so a parent end **less than** daughter start indicates numerical overlap.
All following headline counts use the full S1 table, with both parent and
daughter names present; they do not yet define an eligible analysis cohort.

| Predicate | Replayed result |
| --- | ---: |
| Exact in-table parent links | 471 |
| Parent end < daughter start | 453 |
| Parent end = daughter start | 18 |
| Unordered daughters sharing an in-table parent | 323 pairs / 107 sibships |
| Both ends > 0 | 365 parent–daughter / 249 sister pairs |
| Also non-speculative required edges | 333 parent–daughter / 214 sister pairs |
| End = 0 rows | 73 |
| Both dominant ecogroups known and different | 148 parent–daughter / 134 sister pairs |

For parent–daughter pairs, the required ancestry assessment is the daughter's
incoming edge. The parent's evidence label describes its own, earlier edge;
also filtering that label is a different selection rule. Sister pairs require
both daughter edges. Eleven parent edges outside S1 are not counted. Grouping
by all ancestor strings, including out-of-table scaffolds, would produce a
different sister-pair count.

S1 has seven known dominant ecogroups, with 438 single-group rows, 43
multiple-group rows and one missing group. The earlier count 150 included
two comparisons with missing `Key Information!K387`; the affected daughters
are at rows 37 and 388. These do not establish different habitat. Dominant
ecogroup is not a complete geographic or temporal exposure history.

**Scope reconciliation.** S3 `Overall %Change Tree1v2!C2/F2` and
`Overall Diversites!D11/F11` exclude Bolivina and two benthic Praepararotalia.
Bolivina is already absent from S1. Removing `Key Information!A387:A388`
(P. cretacea and P. perclara) therefore yields **480**. However, the subset's
row coding gives **73 end-at-present / 407 extinct**, while S3
`Overall Diversites!D12:D13` says **72 living / 408 extinct**. S1 and S3's
corresponding row-level fields agree; the summary discrepancy is preserved.
The source qualifies living status of Tenuitella selleyi at F42, but that
is not automatically the explanation or authority to change a value.

**Lineage membership.** S3 `Lineages Tree2!A2:I270` provides 269 lineage
records; the published-summary count 268 excludes `L_Bolivina Clade`.
Expand genus abbreviations through `Gn, Genera!A:B`. Exact matching covers
481 S1 names. A labelled derived lookup stripping only outer whitespace,
including the NBSP in S1 `A36`, covers 482. No raw string is changed.
170 morphospecies occur in multiple lineage records; for example B2 and
B61 both include the same Dentoglobigerina eotripartita label. Membership
is many-to-many, not an exclusive species-to-lineage assignment.

The [summary](source-support-summary.json) retains all 18 boundary pairs.
After that explicit whitespace normalisation, nine share at least one
listed lineage and nine do not. Neither equal boundaries nor shared
membership by itself proves naming or pseudoextinction. Biological event
classification and censoring rules remain for the next contract.

**Nexus units.** The files declare 487 morphospecies and 249 lineage tips.
The former includes S1's species plus Bolivina and four scaffold labels;
one Antarcticella name has U+FFFD where S1 has trailing NBSP, which remains
an explicit unresolved string difference. The latter has 245 lineage-table
codes as tips plus four scaffold tips; all 24 table codes absent as tips
occur as internal labels. These counts describe representation choices.

The decisive provider warning is in S3
`S6. Phyl's (Ch'gms) Contents!E5`: the chronograms convert budding into
bifurcations, display sister relationships and do not preserve interpreted
speciation modes. The parent read that cell directly. A species named as
an ancestor in S1 may nevertheless be a tip in the transformed Nexus.
Use the ancestor/lineage tables and explicit transformations for an event
model; do not treat these chronograms as an unmodified budding graph.

## Limits and next owner

This establishes source identity, count definitions and representation
limits. It does not establish ancestry truth, an exclusive biological
lineage partition, precise extinction dates, habitat separation or power.
Triton joint occurrence/exposure coverage remains untested. No evidence
category was silently upgraded and no raw discrepancy was repaired.
Claude owns the event dictionary and Q-012 contract amendment; Codex's
single review identifies the additional likelihood and prediction repairs.
