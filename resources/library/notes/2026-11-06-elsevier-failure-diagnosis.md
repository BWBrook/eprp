# Elsevier failure diagnosis and cached chapter recovery

Codex, 6 November 2026, Australia/Hobart. This follows the
[5 November acquisition](2026-11-05-elsevier-acquisition.md). Barry authorised
diagnosis and legitimate recovery of the remaining failures. Restricted XML,
error responses and derivatives remain on the campus server; this note contains
metadata, aggregate outcomes and implementation evidence only. The diagnosis
and finite recovery checks are complete: **17 of the 187 initial failures were
recovered**, comprising 16 XML chapters and one complete PDF.

## Initial inventory

The completed selection contained 1,317 works: 1,130 held copies and **187
failures**, comprising 166 HTTP 400 responses, 20 responses labelled
`metadata_only`, and one HTTP 404. These are retrieval outcomes, not uniform
evidence of subscription denial.

The failed catalogue records comprise 85 articles, 75 book chapters, 23 reference
entries, three books and one book review. Eighty name *Elsevier eBooks*, 56
*Palaeogeography, Palaeoclimatology, Palaeoecology* and 11 *Earth-Science Reviews*.
Their publication decades are 1970s: three; 1990s: 23; 2000s: 47; 2010s: 20;
2020s: 94. DOI patterns comprise 90 ISBN chapter identifiers, 57 journal-style
identifiers, 35 legacy serial identifiers, three Academic Press `10.1006`
identifiers and two book concept identifiers.

Define the core explicitly as the union of `canon`, `cited-ids`,
`cited-authoryear`, `barry-2003-list` and `barry-2003-endnote`. In the frozen
catalogue it contains 153 Elsevier works: 25 already held openly, 113 acquired
through TDM, 13 failed, and two excluded or unattempted. Adding `agendas` gives
236 Elsevier works: 46 openly held, 173 acquired through TDM, the same 13 failed,
and four excluded or unattempted. The selected missing-copy tranche therefore
contains 126 core works, or 186 including agendas. A denominator of 321 was not
reproduced from these membership rules and is not used for coverage claims.

## Verified extraction defect and recovery

Inspection of all 20 rejected HTTP 200 XML responses found **16 legitimate
book-chapter payloads** with `originalText/doc/nonserial-item/chapter/sections`.
The original selector accepted `body` or `rawtext`, and missed this hierarchy.
The targeted correction accepts direct `sections` children only when exactly
one `chapter` exists beneath `originalText`. It retains the core-metadata DOI
identity check, text minimum, DTD/entity refusal and existing body/rawtext paths.
Head matter, metadata and bibliographies are excluded. The extraction mode is
`chapter_sections`; completeness remains explicitly unverified.

The versioned diagnostic helper recovered all 16 directly from their cached
quarantine XML. Each original hash matched its earlier attempt receipt; the
original bytes were retained unchanged and read-only. New restricted text and
manifest rows were written under the existing store lock. Earlier attempts and
the snippet-export ledger were preserved. The ledger SHA256 before and after
recovery was
`36056914d21aeaaa58b97c9442a59e0946058dbbecaf1c662c1076ed835f2763`.
This raised held coverage to **1,146 of 1,317**, leaving 171 unresolved works.

The other four cached cases have no accepted scientific-body container. Three
are older `10.1006` articles containing converted-article head matter, with a
bibliography in one. The remaining catalogue book chapter is represented as
`fb-non-chapter` bibliography/back matter. Their large XML sizes do not establish
that the scientific body is present; none was promoted at the XML-only stage.
The later PDF check recovered one of these older articles, as detailed below.

## Access diagnostics

Elsevier's [Article Retrieval API](https://dev.elsevier.com/documentation/ArticleRetrievalAPI.wadl)
documents XML responses and both `FULL` and `ENTITLED` views. Its
[TDM overview](https://www.elsevier.com/about/open-science/research-data/text-and-data-mining)
explicitly includes book chapters. Thus a catalogue type or ISBN-shaped DOI
alone does not establish an unsupported endpoint. Its
[access guidance](https://dev.elsevier.com/tecdoc_article_access.html) distinguishes
API configuration and document entitlements; an HTTP 400 alone does not settle
which applies to an individual document.

A finite stratified sample of 12 resources tested both documented views: journal
articles from different periods, a book, legacy and ISBN book chapters, a
reference entry, a book review, two core `10.1006` cases and the original HTTP
404. Kelley et al. (2001) is excluded because its unchanged `FULL` 400,
`ENTITLED` 401 and metadata-only default response were already diagnosed on
5 November. The sample ran detached, with at least three seconds between
requests. Payloads are private; logs contain only work identifiers, view, HTTP
status and controlled error categories. Resource-specific denial is kept
distinct from invalid credentials, quota exhaustion and transport failure.

Nine sampled resources returned `FULL` HTTP 400 with a controlled `view_invalid`
error category. Eight then returned a directly confirmed, resource-specific
`ENTITLED` HTTP 401 denial. The ninth, a whole-book concept DOI, returned HTTP
500 and remains unresolved. Two older `10.1006` articles returned `ENTITLED`
HTTP 200 with affirmative document-entitlement responses, despite their
scientific-body-free `FULL` XML. The original HTTP 404 remained 404 under both
views. These outcomes justify a single, separately recorded `ENTITLED` check
for each remaining HTTP 400 resource; they do not justify assigning untested
works to the sample's denial category.
An API resource denial describes this caller's request; it does not identify
whether the university lacks a browser subscription, whether format rights
differ, or whether additional API entitlement configuration would be required.

The per-work pass encountered two further whole-book HTTP 500 responses. These
three resources comprise all three catalogue whole books among the failures:
two concept identifiers and one legacy serial identifier. Their server errors
are directly observed; an unsupported document-unit explanation remains an
inference. None was retried. Every remaining HTTP 400 resource received its own
`ENTITLED` check; no sample result was substituted for an individual result.

The third older `10.1006` article and the bibliography/back-matter record were
also checked individually: both returned affirmative `ENTITLED` HTTP 200
responses. All four XML body-absence/back-matter cases therefore have direct
positive entitlement evidence.

Within Barry's diagnosis scope, Codex ran two finite `text/plain` format checks
for the directly entitled `10.1006` articles. The 1997 *Journal of Theoretical Biology* record
returned HTTP 200, but its 851 normalised tokens essentially reproduce the
851 tokens from the cached limited XML (token-sequence similarity 0.998825;
one token absent from the XML). This provides no convincing additional
scientific body. The 2001 *Journal of Archaeological Science* request returned
HTTP 504 with a 120-second retry delay, which subsequent API work honoured.
Neither was promoted to held status; format/body availability remains distinct
from the positive entitlement evidence.

For the original HTTP 404, a finite Crossref metadata request returned HTTP 200
for `10.1016/s0967-0653(97)84825-9`, a 2000 journal article under publisher
`Unmaintained records`. It is a registered DOI whose Elsevier API resource
was not found; the API failure does not establish an invalid DOI.

## PDF recovery and completeness checks

Within the same scope, three finite requests used the documented DOI endpoint
with `Accept: application/pdf`, no view parameter and no credential redirects.
All returned HTTP 200, but HTTP success and a matching first-page title were
insufficient to establish complete copies.

| DOI | Returned / expected PDF pages | Result |
|---|---:|---|
| `10.1006/jtbi.1997.0508` | 18 / 18 | Recovered: title match 1.0; DOI matches cached core metadata; 13,527 extracted words and 1,780 novel tokens beyond the limited XML. |
| `10.1006/jasc.2000.0556` | 1 / 11 | Incomplete first-page preview; not held as full text. |
| `10.1006/bijl.1998.0255` | 1 / 46 | Incomplete first-page preview; not held as full text. |

Expected counts come from each original XML's `web-pdf-page-count`; the first
two also agree with printed page ranges 235–252 and 115–125. All three PDFs
contained embedded text, so OCR was unnecessary. The recovered 18-page PDF has
SHA256 `b6af1ccb1463327076cf8a036efe3624b8db7566ae79be4fd035c4d252907d18`;
its text SHA256 is
`cef56a2aefcc892a679b195da04f42ed0f2c14c5c3298aac6536e4d37569afb9`.
Identity and page coverage are verified; scientific content was not reviewed.
No failed request or incomplete preview was retried.

PDFs and their derivatives have a separate restricted `pdf-format.json`
inventory and remain outside the XML manifest. The same approval-gated query
command accepts only the verified complete PDF, checking PDF/text/source-XML
paths and hashes, source DOI, expected page count and actual PDF pages. It
shares the existing cumulative DOI export ledger; previews and altered page
counts are rejected. A live lookup check verified the recovered PDF and rejected
both previews without exporting text or spending any additional excerpt budget.

The parent then independently checked every stored XML/text pair: 1,147
records, 2,294 files and 655,402,178 bytes passed their recorded hashes.
The full-PDF lookup passed identity/page/hash checks and rejected both
previews. All nine DOI excerpt budgets remained within 200 characters.
The aggregate [integrity receipt](2026-11-06-elsevier-validation.json)
contains no article text. The full library suite passes 67 tests.

## Final disposition of the original 187 failures

| Category | Works | Evidence |
|---|---:|---|
| Recovered XML chapters | 16 | Cached original hashes, scoped extraction and appended manifest rows. |
| Recovered complete PDF | 1 | API PDF, matching identity, complete expected page count and substantial new text. |
| API resource not entitled | 163 | 162 new per-work `ENTITLED` HTTP 401 responses plus the preserved Kelley diagnostic. |
| Entitled articles with incomplete PDF previews | 2 | Body-free XML, positive entitlement, then 1/11 and 1/46 PDF pages. |
| Bibliography/back matter | 1 | Direct `fb-non-chapter` structure and positive entitlement; not a missing research body. |
| Registered DOI, API resource not found | 1 | Direct `FULL`/`ENTITLED` HTTP 404 and Crossref registration. |
| Whole-book diagnostic error, cause unresolved | 3 | Direct per-work `ENTITLED` HTTP 500 responses. |

These categories total 187. The original selection now holds **1,147 of 1,317
works**: 1,130 initial XML successes, 16 chapter recoveries and one complete PDF;
170 remain outside the held set, including the back-matter record retained in
the frozen denominator. The 13 initial core failures now comprise one recovered
PDF, ten direct API denials, one incomplete preview and one unresolved whole-book
error. All counts use the frozen acquisition catalogue; later independently
obtained open copies do not change this cohort's denominators.

## Additional final-version copy

For a separate source-version comparison, Codex retrieved the
published Schachat et al. version, `10.1016/j.revpalbo.2021.104564`, for comparison
with the already open preprint. It contains 642,826 XML bytes and 7,711 extracted
body words. XML SHA256 is
`fb4cebc4ca576e56721bf9370bd35b2d54f9e2c640d49f63b81996a461db4809`;
text SHA256 is
`a11c0c451a9790f2835a38d4674cce8c4e0fed9104f4ba2f97050d21c60499b2`.
The canonical preprint was preserved, and the excerpt ledger was unchanged.
This additional copy is outside the original 1,317-work missing-copy batch and
does not enter its recovery denominator. Acquisition alone does not establish
agreement between versions; that source check is recorded separately.
The XML manifest therefore holds 1,147 works including this additional copy;
the union of XML and the verified complete PDF contains **1,148 distinct works**.

## Evidence and verification

[diagnose_elsevier.py](../diagnose_elsevier.py) writes private sidecars below
`tdm/elsevier/diagnostics/20261106/`: `classification.json`, `recovery.json`,
`sample-ids.txt`, `probes.jsonl`, private payloads and completion receipts.
`diagnosis.json` gives the final per-work grades; `pdf-format.json` records
PDF identity and completeness separately. There are 182 diagnostic response
records, covering 170 distinct resources' entitlement checks plus 12 paired
`FULL` responses. The historical Kelley response and 16 cached recoveries
complete the initial 187-work evidence set.
The initial 187-work classification was written before recovery and remains
the denominator for the diagnosis. Deployed helpers occupy a new versioned
directory; the earlier acquisition tools were not overwritten.
Classification preserves its initial snapshot on rerun; recovery receipts retain
their cumulative work set rather than replacing it with an empty resumed run.
Final per-work grades are emitted separately by `summarize`.

On the restricted host, the metadata-only diagnosis can be reproduced without
new API requests:

```bash
python3 diagnose_elsevier.py summarize \
  --catalogue "$ELSEVIER_STORE/catalogue.tsv" --store "$ELSEVIER_STORE"
```

Thirty-nine focused synthetic tests pass: 28 for acquisition/extraction/query
and 11 for classification, recovery and diagnostic controls. New regressions
cover chapter/head/reference boundaries, ambiguous multiple chapters, wrong
DOIs, cache corruption, original-byte preservation, unchanged attempts and
export budgets, sanitized error output, resource-specific denial and invalid
credential stops. PDF regressions cover complete-copy query access, shared
200-character accounting, DOI and source-hash mismatches, altered expected page
counts and rejection of first-page previews. Live recovery verified the 16
cached source checksums and the recovered PDF's identity/page coverage.

Next owner: main References Codex integrates programme status and the source-check
handoff; the remaining API denials, previews and server errors are access/format
limits rather than grounds for repeated unchanged requests. No Wiley
requests, third-party messages, corpus transfers or scientific ranking changes
are part of this diagnosis.
