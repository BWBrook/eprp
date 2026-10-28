# Count-convention evidence, 28 October 2026

The additive overlay profiles all 26,046 retained register rows and all 1,697
sample-summary source rows (1,675 interval/sample keys). No original count,
comment, reference, taxonomy or sample field changes. The source database is
opened read-only, hash-checked before and after profiling, and must match
`ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610`.

## What is established

The current [Fossilworks FAQ](https://fossilworks.org/?page=works_FAQ) requires
specimen counts but does not supply a count-harmonisation rule. That is a
provider-level description, separate from each row's operational unit.
Unmentioned units remain **unknown**. Neither minimum counts nor incidental
MNI/NISP mentions identify the unit by themselves.

The bounded manual ledger contains **66 reviewed rows**: 26 checked against
primary publications, 40 interpreted from provider comments only. It assigns
58 row units and explicitly leaves eight reviewed cases unresolved. Thus
25,988 units remain unknown; this is an annotation-coverage result, not an
estimate of unknown protocols in the underlying literature. The 26 primary
checks cover two deliberately selected samples, not a representative audit.

| Sample | Directly checked evidence | Interpretation |
| --- | --- | --- |
| Ein Gev I, 4400, ref 3985 | Davis 1974, DOI [10.3406/paleo.1974.4873](https://doi.org/10.3406/paleo.1974.4873), pp.453,458–461 and Table I | All 17 rows checked. The eight large-mammal rows use Table I's bone totals, with MNI separately printed. Smaller taxa include bones, mandible fragments, mollusc specimens and minimum individuals. Full sample has mixed units. |
| Deardorff Hill, 4903, ref 4556 | McGee & Turnbull 2010, [institutional author PDF](https://www.sjsu.edu/people/elizabeth.mcgee/publications/McGee%20and%20Turnbull%202010.pdf), pp.1–3 and Table 1 | All nine rows checked. Dominant-taxon count 806 equals the postcranial column sum; eight associates' counts match enumerated catalogue identifiers. Those protocols are not equivalent animal counts. |

Two conflicts are retained explicitly. Ein Gev's hare row
`03-late-pleistocene/attempt-1/register.txt#5933` stores **7**, whereas the
printed paragraph on p.458 gives minimum **11** animals. Deardorff's row
`15-early-eocene/attempt-1/register.txt#934` stores the supported **806**, but
its comment says MNI **14**; the source gives jaw-based MNI **10** and
humerus-based MNI **12**. Neither discrepancy authorises a silent correction.
The latter reference also retains export year 2009 despite the PDF's 2010
publication date. These checks used original full-text counting passages and
visually inspected tables/page images; they are not abstract-only conclusions.

The eight Ein Gev Table I rows define a useful, precisely delimited shared
counting-protocol subset. Their exact row IDs and separate published MNI are
in the ledger. This does not establish equal recovery, ecological
representativeness, or cross-site comparability. Taxonomic updates in either
sample have not been independently adjudicated.

## Separation of evidence and interpretation

`count-conventions-reviewed-2026-10-28.json` records expected sample/reference,
taxon, count and full comment for each reviewed row. Any changed evidence
fails the build. Each review has an identifier, interpretation, evidence
level, issues and, where checked, source values. Source records give URLs,
DOIs where identified, page/table scope, retrieval hashes and access limits.
The Deardorff DOI was not identified in this bounded check. Publisher access
to Evans et al. 2015 failed; Miller 1976's PDF route returned HTML. Neither is
treated as a full-text source check.

The required source evidence is retained read-only at
`deep-server:/data/paleodata/fossilworks/evidence/2026-10-28-count-conventions-v2`.
A separately verified private copy is at
`nectar-codex-ts:/data/codex/artifacts/eprp-fossilworks-annotations/count-evidence-2026-10-28`.
The nine-payload bundle contains the FAQ, original McGee PDF, Davis counting
pages 453/458/459/460/461, and the two images used for visual checks. Its
`MANIFEST.json` has SHA256
`56b6e0eb9e4275365193df62fae51468104a2df84844e83e735d79ba37f60739`;
a repository copy is `count-conventions-source-evidence-manifest-2026-10-28.json`.
It records exact UTC request windows, original/final URLs, status, content
headers, hashes, byte sizes, and access/reuse constraints. Parent Codex
independently checked all nine remote payload hashes. The retained PDF and
two visual images match the originally inspected payloads byte-for-byte;
counting statements were checked in retained HTML. Public availability does
not establish redistribution permission; these sources remain in the private
mirror and are not included in the repository.

The script also records literal text spans for nine retrieval flags.
**817 rows** trigger at least one; eight mention MNI and five NISP. These are
search aids with no validated precision/recall claim. They cannot assign a
unit. A comment giving MNI 2 alongside stored count 257 is one explicit
negative control. Other controls include taxonomic references to juvenile
individuals, associated teeth explicitly excluded from a count, and minimum
numbers of maxillae plus mandibles. These cases prevent converting arbitrary
material mentions into NISP or minimum counts into MNI. Independent review
also withdrew C031's initial mixed-individual-and-element label: its reference
to skeletal material representing at least 49 animals does not establish
whether individuals or skeletal specimens contribute to the stored 211. That
row remains reviewed with an unknown unit and explicit arithmetic ambiguity.

Provider metadata are retained independently: taphonomic context is nonempty
in 1,207 sample-source rows, preservation in 86, archaeology in 576 and
sampling methods in 1,363. They do not supply quantitative bias corrections
or infer missing protocols. Ein Gev's source specifies dry sieving, a detail
the provider's `screenwash` category does not preserve. Deardorff's blank
taphonomic field does not negate the original bonebed description. Repeated
sample summaries stay separate and do not multiply register rows.

Counts are positive finite integers in all retained register rows. This
syntactic check does not validate their units. Life forms include 511 leaf
rows and nine herb rows, besides vertebrates and invertebrates; the overlay
does not infer plant or animal individuals from those categories.

## Files and replay

- `count-conventions-2026-10-28/register-count-evidence.tsv`: one row per
  original register row, with raw count/comment/taxon, separate provider
  default, reviewed unit, review identifier and exact retrieval spans.
- `count-conventions-2026-10-28/sample-count-evidence.tsv`: one row per
  original sample-summary row, with observed reviewed units, unknown coverage,
  issue row IDs, raw taphonomic metadata and bounded source-review scope.
- `count-conventions-2026-10-28/summary.json`: counts, limits, input/code/review
  hashes and output hashes. Hashes attest reproducibility, not scientific truth.

These derivative TSVs use standard CSV quoting with tab delimiters. Read them
with `csv.DictReader(..., delimiter="\t")`; their quoting convention is
different from the provider's literal-tab source format.

```sh
python3 -m unittest discover -s resources/sources/fossilworks -p test_count_conventions.py -v
python3 resources/sources/fossilworks/count_conventions.py ASSEMBLY.sqlite NEW_DIRECTORY
```

Eight tests cover incidental mentions, minimum-versus-individual ambiguity,
exact spans, changed/missing/duplicate review guards, non-propagation,
literal-quote preservation, duplicate-summary cardinality, immutable input,
connection closure when evidence guards fail, and refusal to overwrite output
or accept a different assembly hash. SQLite reads use `contextlib.closing`,
including failed-query paths; the tests also pass with ResourceWarnings
promoted to errors.

The next scientific step is question-specific sampling of source protocols,
including material selection, association/deduplication, mesh size, taxonomic
resolution and temporal aggregation. The present overlay supports that work;
it does not establish a globally harmonised abundance dataset.
