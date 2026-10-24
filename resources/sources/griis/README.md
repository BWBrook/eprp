---
id: griis
name: Global Register of Introduced and Invasive Species (GRIIS), checklists on GBIF and the 2022 Country Compendium
kind: database
status: active
last_update: "checklists modified on GBIF to 2026-10-07; Country Compendium V1.0 2022-03-12"
scope:
  taxa: ["all kingdoms; plants 69% of checklist taxon rows, animals 29%"]
  time: "present-day status; an event date on 27% of distribution rows, meaning not defined"
  space: "global: 307 country, territory, island and sub-national checklists, plus 75 protected-area lists"
  record_unit: "an introduced or invasive taxon in a checklist's area, with occurrence, establishment and invasiveness"
size:
  as_of: "checklist snapshot 2026-10-24T1038Z; Compendium V1.0"
  checklists: 383
  griis_taxon_rows: 140390
  griis_distribution_rows: 147530
  compendium_rows: 101104
access:
  tier: open
  licence: "CC BY 4.0 for 379 checklists, CC0 for 3 (US), 1 unspecified (GISD); Compendium CC BY 4.0"
  routes:
    - {type: gbif, url: "https://api.gbif.org/v1/organization/cdef28b1-db4e-4c58-aa71-3c5238c2d0b5/publishedDataset", state: "the ISSG publisher's 383 checklist datasets, each with a Darwin Core Archive on an IPT (cloud.gbif.org/griis for 378); all mirrored as one dated snapshot", checked: 2026-10-24}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.6348164", state: "GRIIS Country Compendium V1.0 (196 countries), one version; mirrored", checked: 2026-10-24}
    - {type: web, url: "https://griis.org", state: "project site and search (not used)", checked: 2026-10-24}
  api: "GBIF registry and occurrence APIs; IPT archive.do?r=<resource>&v=<version> serves past versions of each checklist"
versioning:
  replay: partial
  notes: "each IPT keeps every published version of its checklist (archive.do?...&v=), but GBIF's DOI is per dataset, not per version; our snapshots are dated, with the dataset index beside each"
mirror:
  path: deep-server:/data/paleodata/griis
  policy: "the Compendium; a dated snapshot of every checklist archive, repeated as checklists change"
  state: "compendium: 1 file (24 MB); checklists: 383 archives (12 MB) in snapshot 2026-10-24T1038Z; both verify"
lineage:
  upstream:
    - "country and island inventories verified by national experts, compiled by the IUCN SSC Invasive Species Specialist Group (Pagad et al.)"
  downstream:
    - "the Country Compendium (Pagad et al. 2022); SInAS 3.x (Gómez-Suárez et al. 2025), which harmonises the Compendium with GloNAF and the First Records Database"
eprp_questions: [Q-047, Q-028]
citation:
  - "Pagad, S. et al. (2018) Introducing the Global Register of Introduced and Invasive Species. Scientific Data 5: 170202, doi:10.1038/sdata.2017.202"
  - "Pagad, S. et al. (2022) Country Compendium of the Global Register of Introduced and Invasive Species. Scientific Data 9: 391, doi:10.1038/s41597-022-01514-z; data doi:10.5281/zenodo.6348164"
  - "Each checklist: its GBIF dataset DOI (datasets-<snapshot>.tsv), e.g. Australia doi:10.15468/3pz20c"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# GRIIS: Global Register of Introduced and Invasive Species

## Summary

GRIIS lists, for each country, territory or island, the taxa recorded there
as introduced, and flags those with evidence of impact as invasive. The live
form is 383 checklists on GBIF, published by the IUCN SSC Invasive Species
Specialist Group. 307 are GRIIS checklists, 75 are protected-area lists and
one is the Global Invasive Species Database. A frozen form is the 2022
Country Compendium (101,104 records, 196 countries). For Q-047 it is the
modern alien *stock* across all kingdoms by country, the broadest of the
three sources here. For Q-028 its invasive flag is one definition of a modern
winner. Reach for the checklists for current status, and the Compendium for a
citable, harmonised snapshot. Neither gives origins, and the dates some
checklists carry are undefined.

## Contents

Checklist snapshot of 2026-10-24 ([profile](profile/griis_profile.tsv)):

| | Count |
| --- | ---: |
| datasets (GRIIS; protected area; GISD) | 383 (307; 75; 1) |
| GRIIS taxon rows | 140,390 |
| GRIIS distribution rows | 147,530 |
| distribution rows with an event date | 39,815 (27%), in 104 checklists |
| taxon rows by kingdom | Plantae 96,402; Animalia 41,147; Fungi 1,327; Chromista 1,231; others under 300 |
| species-profile `isInvasive` | invasive 19,168; null or blank 121,095; false 891; other forms 185 |

Last modified on GBIF: 180 checklists in 2020, 7 in 2021, 89 in 2022, 4 in
2023, 2 in 2024, 5 in 2025 and 96 in 2026. The register is a patchwork of
vintages.

The Compendium V1.0 has 101,104 rows, 196 countries and 23,685 species, with
16,221 rows flagged invasive.

## Provenance and lineage

ISSG compiles each checklist from national inventories, literature and
databases. Country experts verify it, and ISSG publishes it as a Darwin Core
checklist on an IPT (cloud.gbif.org/griis for 378 datasets; the US checklists
on ipt.gbif.us, Belgium's unified checklist on INBO's IPT), which GBIF then
indexes. Pagad et al. (2022) froze 196 country checklists into the
Compendium. SInAS harmonises the Compendium with GloNAF and the First
Records Database; its copy of the Compendium CSV differs in size from the
Zenodo file (20,731,436 against 23,964,428 bytes; scoping, not examined).

## Structure

Each checklist archive holds `taxon.txt` (scientificName, acceptedNameUsage,
classification, taxonRank, taxonomicStatus), `distribution.txt` (locationID,
countryCode, occurrenceStatus, establishmentMeans, eventDate),
`speciesprofile.txt` (isInvasive, habitat), `eml.xml` and `meta.xml`, joined
by `id`. Vocabularies are not standardised across checklists:
- `establishmentMeans`: alien 72,446; introduced 56,771; the long form
  "introduced (alien, exotic, non-native, nonindigenous)" 13,813;
  cryptogenic|uncertain 3,132; assisted colonisation 873; native|introduced
  327; and misspellings ("cryptogenic|uncerain").
- `isInvasive`: null, blank, invasive, false, yes, true, "invasive?", and
  free text.
- `occurrenceStatus`: present 146,238; blank 981; uncertain 222; eradicated
  45; absent 18; and others.
- `eventDate`: years (16,315), ISO dates (14,705), ranges such as 1900/1950
  (8,122), decades ("1990s"), "From 1900", "pre-1900", "NA" and "unknown".
  GRIIS does not say what the date marks. The full US lists carry one on
  every row.
- `taxonomicStatus`: ACCEPTED, SYNONYM, DOUBTFUL, "Accepted GBIF", "Accepted
  ITIS" and similar.

## Access

- **Mirror.** `deep-server:/data/paleodata/griis/compendium/raw/V1_0_6348164/`
  and `griis/checklists/raw/<snapshot>_url/` (one zip per checklist, named
  by a slug of the title and the first eight characters of the GBIF key),
  with `datasets-<snapshot>.tsv` beside it. The protected-area files'
  slugs are cut before the area's name; the index gives the full titles.
  [snapshots.tsv](snapshots.tsv);
  [datasets-2026-10-24T1038Z_url.tsv](datasets-2026-10-24T1038Z_url.tsv) is
  the committed index.
- **Refresh.** [griis_snapshot.sh](griis_snapshot.sh) `[compendium]
  [checklists]`; [griis_specs.py](griis_specs.py) lists the ISSG publisher's
  datasets through the GBIF API. Every checklist run is a new dated snapshot.
- **Past versions** of a checklist: `archive.do?r=<resource>&v=<version>` on
  its IPT (e.g. Australia v1.0, 24 December 2019, to v1.13, 18 June 2026;
  scoping).
- **Profile.** `python3 griis_profile.py CHECKLISTS_RAW DATASETS_TSV
  COMPENDIUM_CSV OUT_TSV`.

## Strengths

- Every kingdom and nearly every country, verified by national experts.
- Openly licensed, versioned per checklist on its IPT, and indexed by GBIF.
- An invasiveness flag, which GloNAF supplies only for plants and the First
  Records Database only sparsely.

## Weaknesses and pitfalls

- **Vintages differ by six years.** 180 checklists were last modified in
  2020, 96 in 2026. A cross-country comparison mixes states of knowledge.
- **Uncontrolled vocabularies.** Normalise `establishmentMeans`, `isInvasive`
  and `occurrenceStatus` before any count (Structure).
- **Undefined dates.** `eventDate` is filled on 27% of distribution rows in
  mixed formats. Its meaning (first record, observation, publication) is not
  stated. Do not treat it as a first-record year without checking each
  checklist's EML.
- **Status, not flow.** No source region, pathway or route.
- **Mixed units.** Countries, territories, islands, US states, parks; some
  places appear twice (scoping: Galápagos, Rapa Nui, Socotra).
- **The Compendium is frozen** at 2022 and differs from SInAS's copy.

## Overlap with other sources

- **GloNAF and the First Records Database.** In the 125 countries all three
  cover, GRIIS holds 62,834 plant species-country pairs, 22,856 of them also
  in GloNAF and 27,766 in First Records; 24,692 are in GRIIS alone (exact
  names; see [alien-first-records](../alien-first-records/README.md)).
- **SInAS 3.2** ([register-deposits](../register-deposits/README.md)) holds
  the Compendium within its harmonised inputs.

## EPRP relevance

- **Q-047.** The all-kingdom modern stock by country: the broadest outcome
  side for the gate's crosswalk, and the only one beyond plants with
  country-wide coverage. It supplies no timing (the event dates are
  undefined) and no source pools.
- **Q-028 (iii).** `isInvasive` as a pre-defined winner label, after
  normalisation.
- Cannot support: flows, routes, dates of arrival.

## Citation and terms

379 checklists are CC BY 4.0, 3 CC0 and 1 unspecified (GBIF dataset
metadata). The Compendium is CC BY 4.0. Cite Pagad et al. (2018), the
Compendium (Pagad et al. 2022) where used, and each checklist's GBIF DOI.

## Verification log

- 2026-10-24 (Claude, Opus 5.5):
  - *checked*: listed the ISSG publisher's 383 datasets through the GBIF API
    and mirrored every archive as one dated snapshot (all present; the url
    route records sha256, since IPTs publish no checksum);
  - *checked*: mirrored the Compendium (md5 verified);
  - *checked*: profiled both ([profile](profile/griis_profile.tsv)),
    including the event-date formats;
  - *source claim*: per-checklist IPT versions, the duplicated places and the
    SInAS copy's size (scoping subagent, 2026-10-24).
