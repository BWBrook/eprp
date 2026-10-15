# Ammonoid growth data: content and transition-support audit

Codex, 14 October 2026; source pilot added 15 October. B-002 (original D2).
The supplied workbook is verified and inspected. It supports descriptive growth comparisons, but does
not itself encode phylogenetic transitions or establish independent complete
juvenile-to-adult histories. The
[developmental-route contract](../../literature/2026-10-14-ammonoid-developmental-route-contract.md)
states the biological comparison and remaining launch gates.

The [small source/specimen pilot](source-pilot-20261015.md) is complete.
It recovers original specimen candidates and preserves unresolved numerical
links; no eligible independent evolutionary comparison is established. Hold
empirical promotion on this pilot. A broader crosswalk is not the next task.

## Source, delivery and preservation

Walton & Korn (2018), [Dryad 10.5061/dryad.c17p8](https://doi.org/10.5061/dryad.c17p8),
for their [2017 article](https://doi.org/10.1111/pala.12308).
The [source manifest](source-manifest.json) retains the API metadata and initial
401/403 download outcomes. Barry subsequently supplied the original file via
Claude (Correspondence 76/1639). Codex independently verified:

| Field | Verified value |
| --- | --- |
| Dataset / version IDs | 7205 / 7242; version number 1 |
| Publication / metadata modification | 2018-05-16 / 2020-06-24 |
| File ID and name | 34579; `Ontogenetic_Conch_Parameter_Data.xlsx` |
| Bytes | 215,182, matching the provider metadata |
| MD5 | `0302022d2f622b73754cf0e66c54f2ac`, matching the provider digest |
| SHA-256 | `fbe2012f1d420ef7b292141ae0ed0ea8d046c4c15303663565dc72e0727ebe40` |
| Dataset licence | CC0-1.0, as reported by the dataset API |

The unchanged source is locally under ignored
`data/raw/ammonoid-growth-walton-korn-2018/`. API responses and the original
retrieval log are there too. No raw workbook is committed. The manifest's exact
official URLs, filename, version and hashes identify the required input for
another agent; local file availability does not imply scripted Dryad downloads
now work. No source values or source metadata were corrected. Hashes before
and after content inspection agree.

## Reproduce

From the repository root:

```bash
uv run data/ammonoid-growth-support/audit_workbook.py
```

The script pins openpyxl 3.1.5 through inline uv metadata and requires Python
3.12 or later. It refuses an input with a different SHA-256. The recorded run
used Python 3.14.4. It reads formula and cached-value views separately, checks
the original XLSX XML, and writes only audit outputs:

- [Summary JSON](workbook-audit-summary.json): schema, counts, locators,
  missingness, source groupings, ambiguities and unchanged hashes.
- [Series audit TSV](workbook-series-audit.tsv): one record per original row,
  coverage counts, source text and source-row locators. It is not a cleaned
  measurement table or a specimen crosswalk.

The parent independently checked key counts and exception cells using ZIP/XML,
in addition to inspecting the script and outputs. No model was fitted and no
ratios were recomputed from unprovided raw dimensions.

## Observed schema and counts

There are five visible worksheets, no formulas, Excel errors, comments,
hyperlinks, defined names or external links. Missing measurement positions
contain the literal string `NA`, which is preserved.

| Sheet | Layout | Numeric measurement cells | Literal `NA` |
| --- | --- | ---: | ---: |
| Species | 179 records; A:H hold taxon, family, superfamily, stage, period, two ontogeny codes and source | — | — |
| dm | 179 records; A:F metadata; G:AE measurements | 2,925 | 1,550 |
| CWI | Same; parameter label `ww/dm` | 2,826 | 1,649 |
| UWI | Same; parameter label `uw/dm` | 2,643 | 1,832 |
| WER | Same; parameter label `WER` | 2,695 | 1,780 |

The 25 measurement headers run from `Whorl 12` to `Whorl 0` in half-whorl
steps. They are recorded indices, not independently verified chronological
ages, maturity or embryo/hatching labels. Diameter units are not explicitly
labelled in the workbook. The taxonomic list has **177 distinct exact labels**,
42 family labels and 23 superfamily labels; these are source classifications,
not externally validated taxonomy.

All four measurement sheets reproduce the Species taxon-label sequence
exactly. There are **2,643 aligned row/whorl positions with all four variables**,
10–23 per source row. This is numerical joint coverage, not 2,643 independent
organisms or evolutionary events. No metric is present without a corresponding
numeric diameter, but diameter often exists where a ratio is `NA`; do not
silently assume equal coverage for all four variables.

## Preserved ambiguities and exceptions

- **Repeated taxon labels:** `Macrocephalites macrocephalus` at rows 177–178
  and `Macrocephalites verus` at 179–180. Their measurement profiles differ.
  Retain all four rows; the workbook does not supply specimen IDs that would
  establish independent specimens or justify deduplication.
- **Superfamily conflicts:** `Species!C111:C113` says `Goniatitaceae` for
  three Sudeticeras records; C111:C113 on every measurement sheet says
  `Pericyclaceae`. These are 12 conflicting measurement-sheet cells. Preserve
  both source classifications and adjudicate before phylogenetic grouping.
- **Geological-label inconsistency:** `Species!D32:E32` assigns Acutimitoceras
  hilarum to `Famennian` / `Carboniferous`, while other Famennian records use
  `Devonian`. The same source assignments occur in the measurement metadata.
  No age or period was silently changed.
- **A zero is present:** `UWI!P138` is 0 for Schartymites methorius. It is
  retained, not automatically declared erroneous, replaced or log-transformed.
  There are no negative numeric measurements or other screening-bound flags.

131 source rows say `MfN material`; other rows provide collection descriptions
or abbreviated literature citations. Those strings do not provide a verified
specimen catalogue, full bibliography or independent-source crosswalk. Ontogeny
codes in Species F:G are preserved without inventing a legend.

## Evolutionary support and the next finite gate

The observed sheets contain no explicit specimen IDs, maturity labels,
phylogeny, ancestor/sister relations or transition records. **Zero explicit
evolutionary transitions are encoded in this workbook.** The number of
historical transitions, or transitions recoverable from its cited literature,
remains unknown. Shared family/genus, adjacent stages and similar shapes are
not ancestry evidence.

This resolves the access and numerical-schema gate. It does not resolve:

1. Which source rows represent independent specimens or composite trajectories.
2. Whether any record covers the relevant juvenile stages and independently
   established maturity. The lowest/highest diameter is not enough.
3. Which source cross-sections provide thickness, body-chamber/chamber geometry,
   scale and other physical inputs absent from the parameter sheets.
4. Which independently reconstructed evolutionary relations join eligible
   growth histories, including chronology uncertainty and alternative trees.
5. Whether source reuse would make proposed held-out lineages non-independent.

The **small specimen/primary-source and relationship crosswalk** is now
[recorded](source-pilot-20261015.md), with the conflicts above retained for adjudication.
Do not manufacture a 177-species transition dataset from this workbook. The
current B-002 disposition remains development of a conditional physical
comparison; empirical transition validation and numerical launch remain gated.
