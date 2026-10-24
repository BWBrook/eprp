---
id: griis
name: Global Register of Introduced and Invasive Species (GRIIS), checklists on GBIF and the 2022 Country Compendium
kind: database
status: active
last_update: "checklists modified on GBIF to 2026-10-10; Country Compendium V1.0 2022-03-12"
scope:
  taxa: ["all kingdoms; plants 69% of checklist taxon rows, animals 29%"]
  time: "present-day status; timing in some lists only (list-specific event dates, introduction dates in the US occurrence files)"
  space: "global: 303 country, territory, island and sub-national checklists (85 of them nested in others), plus 79 protected-area lists"
  record_unit: "an introduced or invasive taxon in a checklist's area, with occurrence, establishment and invasiveness"
size:
  as_of: "checklist snapshot 2026-10-24T1038Z; Compendium V1.0"
  checklists: 383
  griis_taxon_rows: 140218
  griis_distribution_rows: 147358
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
    - "country and island inventories verified by national experts, compiled by the IUCN SSC Invasive Species Specialist Group (Pagad et al.); Belgium's list is INBO's unified checklist"
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
  reviewed: "2026-10-24, independent Claude Sonnet subagent; findings applied"
---

# GRIIS: Global Register of Introduced and Invasive Species

## Summary

GRIIS lists, for each country, territory or island, the taxa recorded there
as introduced, and flags those with evidence of impact as invasive. The live
form is 383 checklists on GBIF, published by the IUCN SSC Invasive Species
Specialist Group. 303 are GRIIS checklists (85 of them units nested in
another list, such as US states or Marshall Islands atolls), 79 are
protected-area lists and one is the Global Invasive Species Database. A
frozen form is the 2022 Country Compendium (101,104 records, 196 countries).
For Q-047 it is the modern alien *stock* across all kingdoms by country, the
broadest of the three sources here. For Q-028 its invasive flag marks
assessed invaders. Timing exists only in some lists, and each list defines
it differently:
- the US lists give introduction dates in their occurrence files;
- Belgium gives a range from first introduction to last observation;
- many lists give only the date an entry was added.

Reach for the checklists for current status and for those lists' extras, and
for the Compendium when you need a citable snapshot.

## Contents

Checklist snapshot of 2026-10-24 ([profile](profile/griis_profile.tsv)):

| | Count |
| --- | ---: |
| datasets (GRIIS; protected area; GISD) | 383 (303; 79; 1) |
| GRIIS taxon rows; distribution rows | 140,218; 147,358 |
| the same, lists not nested in another (218 lists) | 110,153; 117,293 |
| distribution rows with an event date | 39,686 (27% of all; 54% within the 100 lists that give dates) |
| of them, in lists whose dates are 80%+ from 2015 on (entry stamps) | 24,041 rows in 58 lists |
| in lists whose dates are spread over time | 15,478 rows in 42 lists |
| US occurrence rows with an introduction date in `eventRemarks` | 6,968 |
| distribution rows with a pathway | 20,954 (37 lists) |
| distribution rows with `degreeOfEstablishment` | 27,454 (7 lists) |
| Belgium description rows typed native range | 5,586 |
| taxon rows by kingdom | Plantae 96,282; Animalia 41,095; Fungi 1,327; Chromista 1,231; others under 300 |
| species-profile `isInvasive` | invasive 19,121; null or blank 120,970; false 891; other forms 185 |

Last modified on GBIF: 180 checklists in 2020, 7 in 2021, 89 in 2022, 4 in
2023, 2 in 2024, 5 in 2025 and 96 in 2026. The 2026 modifications may be
re-registrations rather than revisions: their cited version is blank and
their EML stamps date from 2017 to 2020 (review; inferred).

The Compendium V1.0 has 101,104 rows, 196 countries and 23,685 species, with
16,221 rows flagged INVASIVE and the rest NULL.

## Provenance and lineage

ISSG compiles each checklist from national inventories, literature and
databases, and country experts verify it. It is published as a Darwin Core
checklist on an IPT: cloud.gbif.org/griis for 378 datasets, the three US
lists on ipt.gbif.us, and Belgium's unified checklist on INBO's IPT. GBIF then
indexes it. Pagad et al. (2022) froze 196 country checklists into the
Compendium. SInAS harmonises the Compendium with GloNAF and the First
Records Database; its copy of the Compendium CSV differs in size from the
Zenodo file (20,731,436 against 23,964,428 bytes; scoping, not examined).

## Structure

Every archive holds `taxon.txt` (scientificName, acceptedNameUsage,
classification, taxonRank, taxonomicStatus), `distribution.txt` (locationID,
countryCode, occurrenceStatus, establishmentMeans, eventDate, and in some
lists pathway and degreeOfEstablishment), `speciesprofile.txt` (isInvasive,
habitat), `eml.xml` and `meta.xml`, joined by `id`. Three archives (the US
lists) add `occurrence.txt`, `reference.txt` and `vernacularname.txt`;
Belgium adds `description.txt` (pathways, native ranges, invasion stage).
The GISD archive has no distribution file. Vocabularies are not standardised
across checklists:
- `establishmentMeans`: alien 72,320; introduced 56,725; the long form
  "introduced (alien, exotic, non-native, nonindigenous)" 13,813;
  cryptogenic|uncertain 3,132; assisted colonisation 873; native|introduced
  327; and misspellings ("cryptogenic|uncerain").
- `isInvasive`: null, blank, invasive, false, yes, true, "invasive?", and
  free text. Null means not assessed: only 891 rows say false.
- `occurrenceStatus`: present 146,068; blank 981; uncertain 222; eradicated
  45; absent 18; and others.
- `eventDate`: years, ISO dates, ranges such as 1900/1950, decades, "From
  1900", "pre-1900", "NA" and "unknown". Its meaning is set per list in the
  EML. The US lists: "'eventDate' reflects the date the record was first
  added to the GRIIS-L48" (likewise for Alaska and Hawaii); "if earliest
  occurrence for the species is known or suspected, it is provided in the
  eventRemarks field". Belgium: "the year of first introduction and last
  assessment/observation … given as a year range in the event date". France
  (all "2020"), Germany and Spain ("2019") and five Pacific lists ("2022")
  carry one compilation year (review).
- `taxonomicStatus`: ACCEPTED, SYNONYM, DOUBTFUL, "Accepted GBIF", "Accepted
  ITIS" and similar.

## Access

- **Mirror.** `deep-server:/data/paleodata/griis/compendium/raw/V1_0_6348164/`
  and `griis/checklists/raw/<snapshot>_url/`: one zip per checklist, named
  by a slug of the title and the first eight characters of the GBIF key,
  with `datasets-<snapshot>.tsv` beside it. The protected-area files' slugs
  are cut before the area's name; the index gives the full titles.
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
- In some lists, more than status. The US lists give introduction dates (6,968
  occurrence rows). 37 lists give pathways and 7 an establishment degree.
  Belgium gives native ranges.

## Weaknesses and pitfalls

- **Vintages differ.** On GBIF, 180 checklists were last modified in 2020 and
  96 in 2026, but some 2026 dates may be re-registrations (inferred). A
  cross-country comparison mixes states of knowledge.
- **Nested units double count.** 85 checklists cover units inside another
  list (US states, atolls with their national list). Totals over all lists
  count those taxa twice; use the 218 lists that are not nested (110,153 taxon
  rows) for country totals.
- **Uncontrolled vocabularies.** Normalise `establishmentMeans`, `isInvasive`
  and `occurrenceStatus` before any count (Structure).
- **Event dates mean different things.** Most dated rows (24,041 of 39,686)
  sit in lists whose dates cluster after 2015, which marks entry or
  compilation rather than arrival. Read each list's EML, and use the US
  `eventRemarks` or Belgium's ranges for introduction dates.
- **Mostly status, not flow.** No source region or route, except
  Belgium's native ranges and the 37 lists with pathways.
- **Mixed units.** Countries, territories, islands, US states, parks. Some
  places appear twice (scoping: Galápagos, Rapa Nui, Socotra), and
  territories carry their sovereign's country code (the Faroes as DK;
  review).
- **The Compendium is frozen** at 2022 and differs from SInAS's copy.

## Overlap with other sources

- **GloNAF and the First Records Database.** In the 138 countries all three
  cover, GRIIS holds 59,805 plant species-country pairs, 24,802 of them also
  in GloNAF and 24,445 in First Records. 23,739 are in GRIIS alone (exact
  names, 218 country-level lists; see
  [alien-first-records](../alien-first-records/README.md)).
- **SInAS 3.2** ([register-deposits](../register-deposits/README.md)) holds
  the Compendium within its harmonised inputs.

## EPRP relevance

- **Q-047.** The all-kingdom modern stock by country: the broadest outcome
  side for the gate's crosswalk. Timing is patchy and list-specific: the US
  introduction dates, Belgium's first-introduction years and a minority of
  spread-out event dates. There are no source pools beyond Belgium.
- **Q-028 (iii).** `isInvasive` marks assessed invaders, but null means not
  assessed. Only 891 checklist rows and no Compendium rows say not invasive,
  so it gives positives without a contrast set. Winner and non-winner labels
  need another source or a defined comparison.
- Cannot support: flows, routes or arrival dates in general.

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
    including the event-date classes, pathways and extra files;
  - *checked*: the US and Belgian EML definitions of `eventDate` (quoted);
  - *source claim*: per-checklist IPT versions, the duplicated places and the
    SInAS copy's size (scoping subagent);
  - *inferred*: that 2026 GBIF modifications may be re-registrations
    (review).
  - Independent review (Claude Sonnet subagent), findings applied:
    - the event-date meanings and their split into entry stamps and spread
      dates;
    - the US introduction dates, pathways, establishment and native ranges;
    - four protected-area lists that had been counted as GRIIS;
    - nested units;
    - `last_update`;
    - the `isInvasive` contrast for Q-028.
