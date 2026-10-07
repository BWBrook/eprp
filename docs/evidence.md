# Evidence, provenance and downstream reuse

Use plain files and stable source identifiers. Record enough to revisit a
consequential claim or recreate a dataset without building a ledger for every
casual thought.

## Sources and claims

For a source used in substantive reasoning, retain its citation or identifier,
DOI/URL, access date or version, access depth (metadata, abstract, relevant
sections, full text, code inspected or execution checked), and a short note on
what it supports and does not support. Preserve a page/section/table location
when a conclusion depends on an exact passage. Distinguish the source's claim
from our interpretation; link corrections and contrary evidence.

Search snippets are discovery aids. Reviews map a field, while primary work
must support consequential claims about results or novelty. A repository's
existence does not establish that its code runs or reproduces a published result.
Record unsuccessful retrievals; do not convert them into negative evidence.
Keep bibliographic duplicates and retracted/corrected versions distinguishable.

The seed catalogue uses separate fields for directly verified evidence, a
potential EPRP use, and the next unanswered question. Add a deeper resource note
only when one is needed. A source can be usable for one task and unsuitable for
another; avoid a universal “validated” badge.

## Literature orientation

Record the search service or corpus, date, query, filters, inclusion rationale
and stopping rule for each bounded sweep. Note inaccessible and contradictory
work as well as selected papers. Snowball from citations and check related
data/code where they matter. Label opportunistic orientation as such; do not
call it a systematic review without the corresponding design and coverage.

Novelty starts as **unverified**. Before recommending a project, state exactly
what the nearest prior studies already achieved and what remains unresolved.
“Not found in this search” is narrower than “has never been studied”.

## Data and APIs

Before relying on a new extract, record:

- Provider, dataset identifiers, version/release or retrieval time, exact query
  and filters, pagination/completeness checks, response format and schema.
- Provider citation and access/reuse terms, including dataset-specific limits.
  Software/API-documentation licensing is not necessarily data licensing.
- A preserved source snapshot and checksum, or an accessible immutable source
  when retaining a copy is inappropriate; storage location and access limits.
- Scripts and environment for parsing, exclusions, taxonomic/name mappings,
  age/coordinate transformations, unit conventions and derived outputs.

Retain original values. Put corrections and harmonised values in derived
fields with explicit rules. Keep unresolved identifications and provenance
gaps visible. Counts of rows are not counts of independent observations; check
duplicate publications, collection/dataset overlap and reused source records.

For palaeobiological use, establish the time scale and age convention; distinguish
age bounds from probability distributions and age estimates from observations.
Record age-model and calibration provenance where relevant. Do not silently
replace intervals with midpoints or treat “not recorded” as a true absence.
Distinguish modern coordinates from reconstructed palaeocoordinates and record
the reconstruction model/version. Check taxonomic rank, synonymy decisions,
environmental coverage, sampling/collection structure and preservation filters.

Public access and a successful API call do not establish that a proposed
biological quantity is identifiable. A feasibility audit should ask whether
the available joint coverage, resolution and uncertainty can discriminate the
actual alternatives, including relevant dependence and confounding.

## Reuse and handoff

Downstream projects should pin an EPRP commit and identify the exact resource
or dataset version they use. Each shared dataset needs a dictionary, provenance,
known limitations and a reproducible build/export route before being described
as ready for research. Distinguish source access, technical reproducibility,
scientific suitability and permission to redistribute.

Study-specific code and primary outputs live with their investigation. Return
general lessons and shared fixes to EPRP with a link; do not silently change a
snapshot already used in a downstream claim. A private Git push is not a data
release, and an API's openness does not authorize redistributing every item.
