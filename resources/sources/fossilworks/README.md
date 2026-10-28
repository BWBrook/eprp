---
id: fossilworks
name: Fossilworks, terrestrial fossil assemblages with specimen counts
kind: database
status: active
last_update: "live; site documentation and a bounded export checked 2026-10-28"
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
    - {type: download, url: "https://fossilworks.org/?a=downloadForm", state: "public form offers taxon, geographic and time filters; requires at least one fossil time interval; broad export returned 504 and subsequent files were inconsistent", checked: 2026-10-28}
  api: "no documented public API identified; the website provides a download form"
versioning:
  replay: none
  notes: "live database; no fixed release or version archive established. Save dated exports and the exact request to make an analysis reproducible"
mirror:
  path: none
  policy: "a dated public export is desirable; establish its scope and reproducibility before treating it as a database snapshot"
  state: "not mirrored: broad export timed out and subsequent generated files were inconsistent"
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
  reviewed: "independent Codex subagent checked current FAQ, home page and form, 2026-10-28; export outcomes not independently replayed by reviewer"
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
according to the results page. Complete schemas, keys, units, coverage and
their relationship to the underlying database remain to be checked. The live site
also includes contemporary inventories and body-size data; a fossil-only
export must be explicitly delimited and must not be described as the entire
shared backend.

## Access and provenance

The [download form](https://fossilworks.org/?a=downloadForm) filters by life
form, genus, country, bounding coordinates and time interval. It requires at
least one time interval for fossil data. A bounded public export was checked on
28 October 2026; see the verification log below. Export links use generic
filenames without a request or version identifier; a subsequent test request
changed their contents. A broad request returned HTTP 504; afterwards, two
small requests yielded mutually inconsistent register and sample files, so
their retrieval is not yet a reliable snapshot procedure. Whether separate
users can overwrite one another's exports has not been established. The
database is live: no fixed version history or reproducible historical query
has been established.

The FAQ states that data are CC0, while Alroy retains copyright in the site
and its software. It encourages acknowledgement of both the database and its
creator. Its invitation to notify him of publications is not an EPRP
authorisation to contact him; communication remains Barry's decision.

## Strengths and limitations

- Specimen counts are integral to the database's entry criteria, providing a
  route beyond treating each occurrence as one interchangeable observation.
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
  observations. No comprehensive database download or profiling has been completed.
- **Source claim:** Alroy's September 2026 public post reports over 5,000 site
  inventories and specimen counts. The current FAQ reports counts for every
  identification and independent entry from published sources.
- **Checked:** the FAQ links Brook et al. (2025); the paper's title, DOI and
  presence–absence framing are confirmed from the published article's
  [open full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC12343122/).
