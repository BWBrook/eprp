# Q-027 regional-gate audit

GPT-6.1 Sol Codex bounded delegate, integrated by main Codex, 29 October 2026.
Read-only inspection of existing code,
documentation, static region definitions and aggregate results. No occurrence
identifiers or occurrence rows inspected; no held data executed, fetched,
rematerialised or reclassified. No correspondence posted by the delegate.
Main Codex owns the
allocation recommendation and source-owner coordination.

## Decision

The requested molluscan Cretaceous–Paleogene stage × latitude-band × region
count is **not recoverable from the existing support aggregates**. Neither a
regional replication pass nor a failure has been established. A new count
requires a source-owner-qualified input or a newly certified aggregate export;
rerunning the cached support scripts is outside this audit's permitted scope.
The proposed three-tropical-region rule is a useful screen for concentration,
but does not by itself identify a latitude-shape or temperature effect.

## Existing evidence and its limits

- `data/q027-joint-support/build.py:28–38,109–149` selects the
  `Animalia^Chordata_data.csv` member and columns without phylum/class. It keeps
  genus-level/finer records, but cannot implement a molluscan restriction from
  its selected fields. Its region function returns only the EU/NAm code set
  (`85–100`), and its output retains only binary inside/outside cell counts.
  `per_stage.tsv:1` confirms no region identity, taxon or public-membership axis.
- `data/q027-support-audit/5deg-min2collections-support.tsv:1` contains stage
  and band/hemisphere counts, not region identities or taxon-specific support.
  `probe.py:65–90` counts all non-EU/NAm rows using `~eu_na`, including unknown
  countries. It does not apply the later corrected builder's known-country
  outside rule (`build.py:126–127`). Its two-collection filter is applied by
  stage × cell before band counting, not by region × cell. It is not a
  corrected or molluscan estimator-support table.
- Existing scratch `cell-diagnostics.tsv:1` has stage, cell, collection and
  genus totals, latitude and binary region flags; it also lacks taxon identity,
  distinct outside regions and public membership. It cannot supply the count.
- The original screen uses fully contained age ranges, collection-age Scotese
  coordinates, approximate 555 km cells and occurrence-row exclusion
  (`data/q027-joint-support/README.md:46–80,142–165`). Benson's intended
  estimator uses a different age allocation, midpoint coordinates, dggridR,
  modal-region cell exclusion and richness eligibility
  (`data/q027-support-audit/README.md:24,29–51`). Two collections per cell is
  not an incidence-frequency coverage/quorum check.

## Public-membership evidence

These are source-owner aggregate reports, not new access probes:

| Scope | Distinct rows/occurrences | Outside 23 October public snapshot |
| --- | ---: | ---: |
| Entire 33-file Benson deposit | 779,050 | 130,386 (16.7%) |
| Exact cached Q-027 Animalia excluding Chordata member | 712,947 | 116,387 (16.3%) |
| Deposited Mollusca member, all ages/geographies | 368,760 | 71,103 (19.28%) |

[Detail withheld pending disclosure to the data custodian.]

The 23 October hold record applies to its named affected direct extracts;
it does not establish a blanket prohibition on published deposits
(`ideas/2026-10-23-response-closure-and-data-holds-codex.md:8–12,110–114,124–133`).
Barry subsequently authorised keeping published deposits flagged, and the
data/raw audit interprets that to cover main-checkout copies and says they remain in use
(`resources/sources/data-raw-audit/README.md:177–192`;
`resources/sources/register-deposits/README.md:373–381`). This is not a
certificate that their old derived support counts are public-only. For this
proposed analysis main Codex retains the public-membership support requirement;
this is an analytical provenance choice, not a new retention/access ban.
The current Q-027 proposal stops the proposed reuse route if ancestry remains unresolved
(`ideas/2026-10-28-integrated-ranking-codex.md:277–295`). Main Codex should
resolve the narrow permitted export contract with the database owner, without
silently changing either source status or programme priority.

## Available region definitions

The existing non-occurrence `data/raw/benson2025/marine_regions.csv` maps modern
countries to 12 region codes: Africa (AF), Atlantic Ocean Islands (AOC), Asia
(AS), Antarctica (ATA), Australasia (AUS), Central America (CAm), Europe (EU),
Indian Ocean Islands (IOC), North America (NAm), Pacific Ocean Islands (POC),
Rest of World (RoW), South America (SA). Thus the full map has ten possible
outside categories. The source code also declares eight major regions and
four simplified regions
(`scratch/q027-independent-audit/source/subscripts/define-regions.R:21–48`).
These are different maps; do not choose one after observing the count. A
simplified outside map of AS/RoW cannot pass a three-region gate by definition.
The required codes UK/GB, AA/AQ, FA/FK, Namibia's literal NA, and unknown-country
handling are explicit source/audit issues (`define-regions.R:15–35`;
`data/q027-support-audit/README.md:18–24`). A known static map is available;
stage/band/region observations and their admissibility are not.

Modern-country regions are a declared sampling partition, not independent
palaeobiogeographic or reference-level replicates. The full map's islands and
RoW require particular care. Cells should receive the prespecified source
collection-modal region if reproducing Benson's exclusion, rather than counting
one mixed cell as several regional replicates
(`compute-clade-agnostic-env-vars.R:100–109`).

## Statistical critique

Three tropical regions in two warm and two cool windows is a concentration
gate, not an identifiability theorem. Three regions could each supply only
tropical cells while other regions supply all mid/high-latitude cells. Region
and latitude would then be inseparable under unrestricted region effects,
despite passing the tropical count. A random-intercept model would gain its
separation from an exchangeability assumption, not from these counts.

A minimally informative table must show region × band overlap within each
window, along with eligible-cell counts and region recurrence across warm/cool
windows. The candidate design matrix or region-band overlap graph should then
show whether within-region contrasts connect the three bands and the climate
comparison. Three regions also do not quantify the precision of a regional
variance component. Adjacent stages, reused collections/references, broad
ages and shared geological histories can reduce effective replication. Two
warm plus two cool windows must be declared independently of the fitted
gradient, and their temporal dependence retained.

Freeze the estimand before applying the gate. A midlatitude-minus-tropical
richness contrast conditional on global climate state is a latitude-shape
question. Richness as a function of local reconstructed SST is a different
question: palaeolatitude is not interchangeable with temperature, and thermal
bands need not coincide with latitude bands. Discriminating a shape is also
narrower than attributing it to thermal physiology. Region matching does not
remove environment, preservation or sampling-history confounding. The existing
screen has no SST or global-climate classification fields.

## Smallest useful next step

Main Codex should first freeze the incremental same-taxon/window contrast and
the intended region map. Ask the database owner for an existing certified
public-membership aggregate if one exists; otherwise agree a bounded export
contract rather than run the cached builder. The export should contain only
window × clade × band × region counts, with:

1. Original, admitted-public and unknown-country occurrence totals, without
   identifiers; dated source snapshot/hash and exact taxon mapping.
2. Original versus public-only cell/collection counts under the frozen age,
   coordinate, grid and modal-region rules; the effect of membership filtering
   on eligibility, not just occurrence percentages.
3. Coverage-eligible cell counts and an aggregate region-band overlap table;
   warmth classification and the independent evidence/rule assigning it.
4. A clear distinction between the cheap two-collection presence diagnostic
   and the intended richness estimator's eligibility.

If the export cannot be admitted and produced inside the proposed gate, return
that source/support limitation to the allocation decision. This is not a
scientific rejection of the gradient question or permission to launch an
alternative primary investigation.

Complete: artifact/code/source-boundary audit. Provisional: all regional support
and identifiability claims until the table and estimand are fixed. Next owner:
main Codex, coordinating the narrow source decision with database Codex.

29 October 2026, 13:45 AEDT (Australia/Hobart).
