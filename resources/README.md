# Resource orientation

[catalogue.tsv](catalogue.tsv) is a small register of sources worth examining.
It is deliberately incomplete and is not an endorsement, quality ranking or
inventory of data ready for analysis. The seed selection favours accessible
infrastructure; later orientation must challenge that selection.

Each row separates a proposed EPRP use from directly checked evidence and an
open audit question. `checked_on` dates that particular check, not the source's
entire content. Preserve the `resource_id` when updating a record. Additional
resources should answer an active question rather than merely enlarge the list.

## Seed sources, checked 7 October 2026

- **PBDB:** its [versioned data-service documentation](https://paleobiodb.org/data1.2/)
  returned HTTP 200 from WSL. The browser retrieval failed with 403, so that
  failure does not show the service is unavailable. The
  [primary API paper](https://doi.org/10.1017/PAB.2015.39) is a reading lead;
  it has not been read in full for this programme.
- **Neotoma:** the [API specification](https://api.neotomadb.org/swagger.json)
  was retrieved and parsed, reporting `2.0-oas3`; official
  [data documentation](https://www.neotomadb.org/data) describes observations,
  dates and age inferences. Review the
  [data-use policy](https://www.neotomadb.org/data/data-use-and-embargo-policy)
  and relevant constituent-database requirements before selecting an extract.
  The API specification's MIT label does not establish a data licence.
- **Macrostrat:** its [API root](https://macrostrat.org/api) returned JSON
  documenting geological routes and CC-BY 4.0. See the
  [official documentation](https://dev.macrostrat.org/docs). Dataset-level
  coverage, source attribution and proposed fossil/geology joins remain unaudited.
- **palaeoverse:** the [package documentation](https://palaeoverse.palaeoverse.org/)
  describes preparation and exploration helpers for palaeobiological data.
  The package was not installed or tested. Its documentation links
  [Jones et al. (2023)](https://doi.org/10.1111/2041-210X.14099), a reading lead.

No fossil observations were downloaded in this foundation pass. Documentation
and service metadata establish a route to investigate, not scientific fitness.

## Gaps to address when relevant

The initial register has no dedicated taxonomic authority, geochronological
standard, trait/body-size resource, climate/environment reconstruction, modern
biodiversity comparator, or full sampling/preservation-methods map. Regional
and clade-specific resources, museum data and less digitised evidence may be
essential. Select additions against the questions being developed and record
overlap between aggregators; do not assume a global database is representative.
