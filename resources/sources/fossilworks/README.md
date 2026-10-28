---
id: fossilworks
name: Fossilworks, terrestrial fossil assemblages with specimen counts
kind: database
status: active
last_update: "live; all 20 visible fossil interval exports privately mirrored and audited 2026-10-28"
scope:
  taxa: ["terrestrial fossil animals, presently focused on Cenozoic and Cretaceous vertebrates"]
  time: "Cretaceous to Holocene in the public fossil download form; coverage concentrated in the Cenozoic, especially Pleistocene and Holocene"
  space: "global terrestrial sites; geographic and taxonomic coverage are uneven and not yet profiled"
  record_unit: "a taxon identification with a specimen count in a fossil sample; samples are linked to publications"
size:
  as_of: "John Alroy's September 2026 public description; not independently counted"
  samples: "more than 5,000 site inventories, provider-reported"
access:
  tier: open
  licence: "CC0 for data, according to the current FAQ; website and software are separately copyrighted"
  routes:
    - {type: web, url: "https://fossilworks.org/?page=works_home", state: "fossil home, search and sample browser", checked: 2026-10-28}
    - {type: documentation, url: "https://fossilworks.org/?page=works_FAQ", state: "current FAQ: provenance, count requirement, terms and relationship to PBDB and the Ecological Register", checked: 2026-10-28}
    - {type: download, url: "https://fossilworks.org/?a=downloadForm", state: "all 20 visible fossil intervals downloaded separately, each retaining five original sheets; stable files retain source count and reference omissions", checked: 2026-10-28}
  api: "no documented public API identified; the website provides a download form"
versioning:
  replay: none
  notes: "live database; no fixed release or version archive established. Save dated exports and the exact request to make an analysis reproducible"
mirror:
  path: "deep-server:/data/paleodata/fossilworks/raw/2026-10-28-intervals-v2"
  policy: "private dated source exports; retain each interval separately, with exact requests, UTC times and hashes; do not assemble before resolving source structure"
  state: "all 20 visible selections, 100 selected original sheets, stable repeated hashes and a verified read-only manifest; 15 interval bundles retain source count/reference inconsistencies"
lineage:
  upstream:
    - "published fossil lists, entered and checked under John Alroy's supervision; current FAQ says PBDB was not consulted when building this database"
  downstream:
    - "Fossilworks and the Ecological Register use the same underlying database and software, according to the current FAQ"
    - "Brook et al. 2025, Carter and Alroy 2025, and Todorov and Alroy 2025 are cited on the Fossilworks FAQ"
eprp_questions: []
citation:
  - "Fossilworks, https://fossilworks.org, accessed with the query and retrieval date; the FAQ encourages credit to John Alroy and Fossilworks"
  - "Brook, B. W. et al. (2025). Late Pleistocene faunal community patterns disrupted by Holocene human impacts. Biology Letters 21: 20250151. doi:10.1098/rsbl.2025.0151"
entry:
  created: 2026-10-28
  updated: 2026-10-28
  by: Codex (OpenAI), with a Codex research subagent
  reviewed: "independent Codex agents checked documentation and verified all 100 selected sheets against manifest hashes and repeat-GET copies; reviewer independently reproduced Holocene matrix differences and Middle Pleistocene count discrepancies, 2026-10-28; no live export replay by reviewer"
---

# Fossilworks: count-based fossil assemblages

## Summary

The current Fossilworks is John Alroy's public database of terrestrial fossil
assemblages. It focuses on Cenozoic and Cretaceous vertebrates and is especially
rich in Pleistocene and Holocene sites. Each entered taxon identification in a
fossil list has a specimen count, according to the [FAQ](https://fossilworks.org/?page=works_FAQ).
Counts make it a useful lead for questions about local abundance distributions,
community composition and sampling-standardised diversity. They are not
automatically counts of living individuals or unbiased ecological abundances.

This is **not merely the historical Fossilworks interface to PBDB**. The current
FAQ says the new fossil data were entered afresh from publications without
consulting PBDB. Sites may occur in both, so independent entry does not make
the fossil assemblages independent observations. Fossilworks and the
Ecological Register share the same database, according to the FAQ.

## Contents and structure

Alroy described more than 5,000 site inventories with specimen counts in a
[September 2026 public post](https://bsky.app/profile/johnalroy.bsky.social).
This is a provider claim, not an independently verified current count. The
site's [home page](https://fossilworks.org/?page=works_home) describes broad
terrestrial coverage, with the above age and taxonomic concentrations. The
download form offers fossil time intervals from Holocene through Campanian and
Maastrichtian; presence in the form is not a measured coverage count.

The public form returns separate taxon-count (`register.txt`), species, sample
and reference tables, and a species-by-sample matrix. The register has
sample and reference identifiers, fossil age fields, coordinates, taxon,
count and comments; the sample table adds collection, preservation,
archaeology and sampling information and summary diversity estimates.
The matrix includes only identifications with proper Linnaean species names,
according to the results page. The retained matrix columns use sample names,
and their order can differ from the sample table. Several sample tables repeat
identical summary rows for one sample identifier; the matrix contains one
column for that identifier. Complete schemas, keys, units, coverage and
their relationship to the underlying database remain to be checked. The live site
also includes contemporary inventories and body-size data; a fossil-only
export must be explicitly delimited and must not be described as the entire
shared backend.

## Access and provenance

The [download form](https://fossilworks.org/?a=downloadForm) filters by life
form, genus, country, bounding coordinates and time interval. It requires at
least one time interval for fossil data. On 28 October 2026 we retrieved all
20 visible fossil selections sequentially, with no taxonomic or geographic
filter. Each retains the five original sheets, request parameters, result
page, per-request UTC times and response headers, SHA256 checksums, and a
second copy of every sheet to test stability. The original source snapshot is
read-only; no datasets have been assembled or deduplicated. The
[acquisition receipt](profile/acquisition-2026-10-28.md) and
[corrected interval table](profile/interval-download-literal-2026-10-28.tsv)
describe the files.

Export links use generic filenames without a request or version identifier;
submitting another interval changes their contents. Stable repeated hashes,
matching selected interval labels and cross-table identifiers provide checks
against mixed downloads. They cannot exclude uncontrolled concurrent writers.
A broad request previously returned HTTP 504 and subsequent small requests
produced mixed files; the sequential interval procedure avoided that failure.
The database is live: the dated files are retained observations of public
exports, with no fixed provider release or historical-query replay established.
The [sample and register assembly](assembly.md) provides a queryable,
provenance-preserving SQLite representation, with unresolved source issues
retained rather than corrected.

The FAQ states that data are CC0, while Alroy retains copyright in the site
and its software. It encourages acknowledgement of both the database and its
creator. Its invitation to notify him of publications is not an EPRP
authorisation to contact him; communication remains Barry's decision.

## Strengths and limitations

- Specimen counts are integral to the database's entry criteria, providing a
  route beyond treating each occurrence as one interchangeable observation.
- All 20 interval bundles were downloaded with stable five-sheet hashes. Five
  satisfy result-page counts and sample/reference identifier checks; 15 retain
  references used by register/sample records but absent from the reference
  sheet. These are retained source inconsistencies, rather than repaired values
  or evidence of failed file transmission. A previous claim that the Middle
  Pleistocene register lacked a row was a parser error, corrected below.
- The provider matrix is not a safe substitute for summing the register.
  Across retained interval exports, some cells differ from summed repeated
  taxon/sample rows and match the last such row instead. This is an observed
  pattern, not a verified account of provider code. The previously reported
  Middle Pleistocene matrix count is present in its register; the earlier
  audit incorrectly merged two rows. The historical per-interval
  [cell comparisons](profile/interval-matrix-comparisons-2026-10-28/) preserve
  the discrepancies. No source counts have been changed.
- The count unit, reporting protocol, collection and preservation processes,
  identification history, duplicate samples and age uncertainty must be
  examined for the question at hand. A list of specimens is not necessarily a
  census of individual animals or a complete record of a community.
- Sample totals and richness in a taxon-filtered export reflect the selected
  taxa, not the complete sample. A genus-filtered test returned totals of 4
  and 28 for two samples; without the genus filter, the same samples had 101
  and 320 specimens. Richness changed from 1 and 1 to 6 and 12. A sample's
  total can include taxonomically indeterminate identifications; additional
  unallocated counts can appear only in comments. Preserve these fields and
  check source-specific conventions before analysis.
- Coverage depends on published lists with counts and on curation priorities.
  Missing samples and missing taxa are not evidence of absence. Quantitative
  geographic, temporal and taxonomic coverage has not yet been profiled.
- The present data are distinct from the earlier PBDB-facing Fossilworks
  portal, although the same sites and publications may overlap. Do not combine
  them as independent replicates without linking their provenance.

## Relevance and example

Fossilworks offers potential for developing questions about community
reorganisation, abundance and biomass around Quaternary extinction, as well as
older Cenozoic and Late Cretaceous assemblages. These are ideation leads, not
claims that any particular question or comparison is already feasible.

The FAQ cites Brook et al. (2025), *Late Pleistocene faunal community patterns
disrupted by Holocene human impacts*, doi:10.1098/rsbl.2025.0151. That paper
used presence–absence to compare patterns among fossil mammal assemblages;
the availability of specimen counts does not imply that every published use
analysed abundance.

## Verification log

- **Correction, 28 October 2026:** provider TSV fields contain literal double
  quotes, not CSV quoting. Parsing them as quoted CSV merged two Middle
  Pleistocene rows and changed quoted comments in other rows. The corrected
  literal-TSV audit gives 26,046 register rows across selections, 34
  matrix-versus-register-sum differences, and no missing Middle Pleistocene
  register/matrix row. That interval has 1,843 register rows, matching its
  results page; its reference sheet still contains 61 of 63 stated references.
  The [corrected audit](profile/interval-download-literal-2026-10-28.json)
  supersedes the original CSV-derived counts; the earlier audit remains linked
  as a historical record. Neither count is a count of independent observations.
- **Acquisition complete, 28 October 2026:** all 20 visible fossil interval
  inputs, including the mixed `Pleistocene - Holocene` selection and the
  Maastrichtian/Campanian stages, were submitted separately. All returned
  nonempty five-sheet exports; no visible selection was omitted. The
  [original audit](profile/interval-download-2026-10-28.json) verifies all 432
  file hashes and records the selected 100 original sheets. Its parsed counts
  are superseded by the corrected audit above. Source acquisition is complete;
  scientific readiness and a rational assembly remain subsequent work.
- **Checked, 28 October 2026:** read the current Fossilworks FAQ, home page and
  download form over HTTPS; recorded the stated CC0 terms, entry and lineage
  policies, and visible filter controls. An independent research subagent's
  public form POST selected
  Australia, genus *Diprotodon*, Late Pleistocene and the rectangle 37.5–37° S,
  144.5–145° E: two count rows and two samples. Removing the genus filter
  returned 18 count rows for the same two samples and changed the sample
  summaries as described above.
- **Checked, 28 October 2026:** a request selecting all 20 visible fossil
  intervals returned HTTP 504. Subsequent attempts to reproduce the bounded
  comparison returned inconsistent register and sample files. One unfiltered
  register contained 26,045 rows while the sample table contained two samples;
  a later retrieval contained an 18-row register with a 1,701-row sample
  table. The cause, including whether a timed-out server process or another
  request overwrote the generic paths, is not established. The
  [comparison script](check_filtered_export.py) rejects tables with different
  sample-ID sets; its current run failed that check. An
  [aggregate receipt](profile/export-check-2026-10-28.json) records the
  observations. This earlier failure is superseded for acquisition by the
  interval downloads above; it remains evidence about the mutable export path.
- **Source claim:** Alroy's September 2026 public post reports over 5,000 site
  inventories and specimen counts. The current FAQ reports counts for every
  identification and independent entry from published sources.
- **Checked:** the FAQ links Brook et al. (2025); the paper's title, DOI and
  presence–absence framing are confirmed from the published article's
  [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12343122/).
