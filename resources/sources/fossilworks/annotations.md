# Fossilworks reference and count annotations

The 28 October 2026 annotations add evidence to the [sample and register
assembly](assembly.md) without editing the original interval exports or the
assembled database. The base assembly's unresolved-reference status continues
to describe the original reference sheets. Its SHA256 is
`ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610`.

## Missing references

All 58 reference IDs missing from the selected export sheets have a later
provider citation, covering 1,266 register rows and 96 distinct sample IDs.
For 57, the Fossilworks reference page returned the exact reference ID and
links to the affected samples. The remaining ID, 4414, returned no match on
that route; the provider's sample 4697 page supplies the explicit sample ID
and full citation with `[ER 4414]`. The failed search and supporting sample
page are both retained. See the [recovery record](profile/reference-recovery-2026-10-28.md)
for methods, evidence and offline replay.

Recovery verifies the provider's linkage, not the accuracy of every citation.
In one checked case, reference 4030, the provider's 2015 and `Hirs` differ
from the [journal record](https://hrcak.srce.hr/en/314667), which gives 2024
and Hir. Reference 3996's 2015 online and 2016 print dates are compatible
publication conventions. These checks are separate annotations; provider text
and original missing flags remain unchanged.

## Counts

The [count-convention record](profile/count-conventions-methods-2026-10-28.md)
contains the full method, reviewed cases and evidence. All 26,046 register rows
are included; 66 were reviewed, including 26 checked directly against two
original publications and 40 interpreted from provider comments. Evidence
supports a guarded unit annotation for 58 rows. The other 25,988 remain unknown:
this describes the current extent of review, not a measured rate of missing
protocols in the literature. Literal text flags are retrieval aids, not unit
classifications. The sample overlay retains all 1,697 original sample rows,
including repeated summaries.

[Ein Gev I](https://www.persee.fr/doc/paleo_0153-9345_1974_num_2_2_4873)
illustrates different protocols within a single sample: the eight large mammal
counts correspond to bone totals, with minimum individual numbers stated
separately, while smaller taxa use other units. The provider's hare count is 7;
the publication describes a minimum of 11 animals. At
[Deardorff Hill](https://www.sjsu.edu/people/elizabeth.mcgee/publications/McGee%20and%20Turnbull%202010.pdf),
the count 806 matches the table's sum of postcranial elements, but the provider
comment's MNI of 14 differs from the publication's jaw-based 10 and humerus-based
12. Original counts and comments are preserved; neither example establishes a
conversion to living abundance or comparability across sites.

## Using the sidecar

The sidecar SQLite is stored separately from the base assembly:

- `deep-server:/data/paleodata/fossilworks/derived/2026-10-28-annotations-v1/fossilworks-annotations.sqlite`
- `nectar-codex-ts:/data/codex/artifacts/eprp-fossilworks-annotations/2026-10-28-annotations-v1/fossilworks-annotations.sqlite`

The sidecar is 12,165,120 bytes, SHA256
`ebac4771b4b0f400c7cb91b9c4e8499ba781731374148f3f77aac672737f66b6`.
The [build receipt](profile/annotation-build-receipt-2026-10-28.json),
[deep-server verification](profile/annotation-verification-2026-10-28.json),
and [VM verification](profile/annotation-vm-verification-2026-10-28.json)
record the input hashes, integrity checks and join results. The 100 selected
original sheets were rehashed against the source manifest; an independent
review checked the sidecar joins and raw fields. Input hashes are also pinned
in [annotation-input-hashes](profile/annotation-input-hashes-2026-10-28.json).
It contains the exact input documents, keyed reference and count tables, and a
`suggested_queries` table with a complete read-only join. A register join uses
`register_linked._fw_row_id = register_count_evidence.row_id`; a reference
join uses `register_linked."ref no" = reference_recovery.ref_no`. A sample join
uses source row ID, not sample number, so repeated summaries are preserved
without multiplying register rows. Reference and bibliographic evidence are
separate from the provider data, and source values must not be overwritten.

To reproduce from a local read-only copy of the pinned assembly, use a new
output path:

```sh
python3 resources/sources/fossilworks/build_annotations.py \
  ASSEMBLY.sqlite resources/sources/fossilworks/profile NEW-ANNOTATIONS.sqlite \
  --expected-hashes resources/sources/fossilworks/profile/annotation-input-hashes-2026-10-28.json
```

The citation-page responses and retrieval receipts are retained in this private
repository. The nine-payload source-publication evidence bundle is retained
privately on deep-server and verified separately on the Nectar VM; its
[manifest](profile/count-conventions-source-evidence-manifest-2026-10-28.json)
records the source URLs, retrievals and hashes. Public access to the papers does
not itself establish permission to redistribute their full text.

For analyses, select samples and taxa for the question, inspect the relevant
publications and collection protocols, and explicitly evaluate taxonomic,
temporal and sampling comparability. The present annotations are a starting
point for that work, not a global harmonisation of abundance.
