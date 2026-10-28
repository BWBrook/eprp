# Fossilworks sample and register assembly

The 28 October 2026 assembly places all 20 retained interval exports in one
queryable SQLite database, without merging or discarding source records. It is
an evidence-preserving research input, not a taxonomically harmonised dataset
or a validated measure of living-community abundance.

## Location and inputs

- Database: `deep-server:/data/paleodata/fossilworks/derived/2026-10-28-assembly-v1/fossilworks.sqlite` (80,089,088 bytes; read-only).
- Separately verified read-only VM copy: `nectar-codex-ts:/data/codex/artifacts/eprp-fossilworks-assembly/2026-10-28-assembly-v1/fossilworks.sqlite`. Its database, manifest and verification receipt all match the deep-server copy by SHA256.
- Its [manifest](profile/assembly-manifest-2026-10-28.json) pins the source,
  selected-sheet audit, assembler and output SHA256 values. The derived
  directory also contains `MANIFEST.json` and `verification.json`.
- Source: `deep-server:/data/paleodata/fossilworks/raw/2026-10-28-intervals-v2/`.
  The source consists of 20 sequential public requests, not an atomic
  provider snapshot. See the [acquisition record](profile/acquisition-2026-10-28.md).
- Selection: the first retained attempt for each of the 20 intervals, using
  the original register, samples, references, species and matrix sheets. The
  source manifest and historical selection audit are pinned and checked before
  the build; the [corrected literal-TSV audit](profile/interval-download-literal-2026-10-28.json)
  is kept alongside them.

## Tables and interpretation

| Table or view | Role |
| --- | --- |
| `intervals`, `source_files` | Selection, request and source-file metadata, source hashes, original ordered headers, and historical audit classifications. |
| `source_rows` | Every original record from every selected sheet, including matrix rows. `row_id` is source file plus 1-based data-record number; physical line and ordered field values are retained. It is **not** a biological occurrence identifier. |
| `register_rows`, `samples_rows`, `references_rows`, `species_rows` | Original columns as text, with source row and interval keys. There are 26,046 register rows and 1,697 sample-summary rows; no row is silently removed or combined. |
| `register_linked` | One row per register row, with exact sample and reference candidate counts and link statuses. It avoids multiplying register rows when a source sample summary is repeated. |
| `row_links`, `link_candidates` | Every candidate target and whether it came from the same or another interval. An absent same-interval reference is not silently filled from another interval. |
| `identity_groups`, `identity_members` | Explicit comparisons of records sharing a sample, reference or diagnostic register key. They describe repeated or differing source values; they do not establish biological identity. |
| `sample_qc` | Each original sample-summary row compared with the sum of its same-interval register counts; mismatches are flags, not corrections. |
| `matrix_columns`, `matrix_column_samples`, `matrix_qc`, `interval_qc` | Matrix sample-name candidates and comparisons with register rows. The original matrix rows remain in `source_rows`; matrices are not substituted for register counts. |

Eight species sheets contain seven mass fields absent from the other 12. The
native `species_rows` table uses SQL `NULL` for a column absent from a source
sheet and retains an empty string when the source supplied an empty field.
Each file's original header and unpadded field array remain available in
`source_files` and `source_rows`. Register counts and source metadata remain
strings; taxonomic qualifiers, higher-rank names and comments are untouched.
Counts may represent different specimen conventions, including MNI and NISP.

The provider sheets use literal tabs and line breaks as delimiters; quotation
marks are source text, not CSV quoting. The earlier acquisition audit used a
CSV parser that changed quoted comments and merged two Middle Pleistocene
register rows. The [corrected audit](profile/interval-download-literal-2026-10-28.json)
supersedes those parsed counts; the initial audit is preserved as history.
Middle Pleistocene has the 1,843 register rows declared on its results page,
including the previously reported missing *Capricornis* row. Its two missing
references remain unresolved.

## Checks and limits

The [verification receipt](profile/assembly-verification-2026-10-28.json)
records 100 source sheets and all 43,378 source records checked field by field,
with SQLite integrity and foreign-key checks passing. An independent Codex
reviewer additionally compared all structured fields, 53,789 link statuses,
60,633 candidate links and 1,189,349 matrix cells against the retained input;
no mismatches were found. An altered database copy was rejected by the
verification script. Eighteen local tests cover the assembler and literal
export parser, including duplicate joins, ambiguous identifiers, source hash
failures, literal quotes and missing-versus-empty columns.

Observed in these exports:

- 1,675 distinct sample IDs in 1,697 summary rows. The 22 repeated summaries
  are retained; joining them directly would multiply 547 register rows.
- Three pairs of register rows have identical source content within an
  interval. They remain separate records: matching content is not evidence
  that an entry should be deleted.
- 58 reference IDs are absent from the selected reference sheets, affecting
  1,266 register rows and 96 distinct samples. No missing ID was found in
  another selected interval. They remain unresolved in this original assembly;
  subsequent provider citation recovery is retained separately in the
  [annotation sidecar](annotations.md).
- 44 distinct samples have a provider total below the sum of their retained
  register counts. Both values and the contributing original rows are kept.
- 34 matrix cells differ from register sums. Each matrix value matches the
  last matching register row, an observed pattern rather than proof of the
  provider's implementation or a rule for correcting its data.
- No sample ID appears in more than one of these interval selections. This
  observation does not establish that different samples are independent
  biological communities, or that the whole Fossilworks database is covered.

The initial full Nectar mirror backup predates this derived database. The raw
interval exports are included in that generation; the database also has the
separate, independently checked VM copy above. It will enter a future full
backup generation when the backup script is run again.

## Using and rebuilding

Open the database read-only and inspect the one-row-per-register view:

```sql
SELECT _fw_row_id, "sample no", "ref no", genus, qualifier, species, count,
       _fw_sample_status, _fw_reference_status
FROM register_linked
WHERE _fw_reference_status = 'unresolved'
LIMIT 10;
```

To inspect a link, use the register row's `_fw_row_id` with
`row_links.owner_row_id` and `link_candidates.owner_row_id`. Candidates may be
repeated or ambiguous; do not join all candidates into an analytical table
without deciding how to handle them. Sample and reference summaries, matrix
cells, and cross-interval identity comparisons each have their own provenance.

From a checkout containing the pinned profile audit, with the source mounted
or available at `SNAPSHOT`, rebuild to a **new** path outside the source:

```bash
python3 resources/sources/fossilworks/assemble.py SNAPSHOT NEW.sqlite
python3 resources/sources/fossilworks/verify_assembly.py SNAPSHOT NEW.sqlite
```

The assembler refuses an existing destination and verifies source hashes
before writing. The verifier checks the selected source files and field values
against the database; it does not establish ecological representativeness,
the validity of specimen units or temporal independence.
