---
id: glonaf
name: Global Naturalized Alien Flora (GloNAF) 2.0, snapshot 2.02
kind: database
status: active
last_update: "2025-02-24 (database snapshot); Zenodo version of 2025-09-12"
scope:
  taxa: ["vascular plants (WCVP v12 names), naturalized or invasive outside their native range"]
  time: "present-day status; no dates of introduction"
  space: "global: 1,343 regions (427 islands; 219 equivalent to an ISO country), many overlapping"
  record_unit: "a taxon in a regional list of naturalized or invasive plants, with status"
size:
  as_of: "Zenodo 17105725 (2.02 snapshot)"
  taxon_region_rows: 349271
  accepted_taxa: 16504
  regions: 1343
  lists: 2774
access:
  tier: open
  licence: "CC BY 4.0 (Zenodo)"
  routes:
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.13235356", state: "concept: three versions (2024-08-05 XLSX, 2025-02-25 XLSX, 2025-09-12 CSV); the newest mirrored", checked: 2026-10-24}
    - {type: web, url: "https://glonaf.org", state: "project site: version 2.0, citation request, contact the core team before use (quoted below)", checked: 2026-10-24}
    - {type: web, url: "https://idata.idiv.de/DDM/Data/ShowData/257", state: "GloNAF 1.2 (van Kleunen et al. 2019) on iDiv's portal; its download link returned HTTP 500 to the scoping check, not retried", checked: 2026-10-24}
  api: "none; Zenodo REST for the snapshots"
versioning:
  replay: partial
  notes: "each Zenodo version is a snapshot; the three versions of concept 13235356 are indexed (zenodo-versions.tsv), and the newest is mirrored. GloNAF 1.2 (2019) is on another host"
mirror:
  path: deep-server:/data/paleodata/glonaf
  policy: "the newest Zenodo version; earlier ones on demand"
  state: "17105725: 15 files (162 MB) with manifest; verifies"
lineage:
  upstream:
    - "about 336 published floras, checklists and databases (glonaf_reference), harmonised to the World Checklist of Vascular Plants by the GloNAF team (van Kleunen, Pyšek, Essl, Kreft, Weigelt, Winter and others)"
  downstream:
    - "SInAS 3.x (Gómez-Suárez et al. 2025), which harmonises an earlier GloNAF with GRIIS and the First Records Database; 3.2 mirrored in register-deposits"
eprp_questions: [Q-047]
citation:
  - "Davis, A. J. S. et al. (2025) The Updated Global Naturalized Alien Flora (GloNAF 2.0) Database. Ecology 106(11): e70245, doi:10.1002/ecy.70245"
  - "GloNAF core team (2025) Global Naturalized Alien Flora (GloNAF) version 2.02. Zenodo, doi:10.5281/zenodo.17105725"
  - "van Kleunen, M. et al. (2019) The Global Naturalized Alien Flora (GloNAF) database. Ecology 100: e02542, doi:10.1002/ecy.2542"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# GloNAF: Global Naturalized Alien Flora

## Summary

GloNAF records which vascular plants are naturalized, or invasive, in each of
1,343 regions worldwide: 349,271 taxon-by-list rows, 16,504 accepted species
and infraspecific taxa (WCVP names). For Q-047 it is the modern *stock* of
alien plants by recipient region: what has established where. It carries no
dates and no source regions. It is the plant side of any crosswalk with GRIIS
and the First Records Database, and the only one of the three that grades each
list's completeness. Reach for it when the question is where alien plants
have naturalized, not when or from where they came.

## Contents

| Table | Rows | Content |
| --- | ---: | --- |
| `glonaf_flora2.csv` | 349,271 | taxon × list × region, status Naturalized (300,106) or Invasive (49,165) |
| `glonaf_taxon_wcvp.csv` | 95,635 | original names and their WCVP accepted names (16,504 accepted names occur in the records) |
| `glonaf_list.csv` | 2,774 | one list per reference and region: taxon group, completeness, invasives-only flag |
| `glonaf_region.csv` | 1,343 | regions: code, TDWG equivalents, ISO equivalence, island flag, parent |
| `glonaf_reference.csv` | about 370 | the published sources |
| `glonaf_TxR.csv` | 15,892 × 987 | accepted taxon × non-overlapping region matrix |
| shapefiles | 2 zips | all regions, and the non-overlapping set used by TxR |

Lists by completeness (GloNAF's own judgement): very incomplete, under 50% of
naturalized taxa, 1,513; incomplete, 50–90%, 688; complete or nearly so, 563;
not stated, 10. 724 lists are restricted to invasive taxa. The richest
regional floras are the contiguous USA (3,827 accepted taxa), Australia
(3,266) and France with Corsica (2,509); the median region has 81. Poaceae,
Asteraceae and Fabaceae supply 36% of rows
([profile](profile/glonaf_profile.tsv)).

## Provenance and lineage

The GloNAF team compiles regional lists from about 336 published sources and
matches every name to the World Checklist of Vascular Plants (v12). Version
1.2 (van Kleunen et al. 2019) was released on iDiv's data portal. Version 2.0
(Davis et al. 2025) is on Zenodo, and the 2.02 snapshot of 12 September 2025
is "a snapshot of the GloNAF database last updated on February 24, 2025",
with structural changes only (glonaf.md, in the deposit). SInAS harmonises an
earlier GloNAF with GRIIS and the First Records Database.

## Structure

`glonaf_flora2` links to the taxon (`taxon_wcvp_id`), list, reference and
region tables by id. A region can carry several lists (several sources), so
count distinct taxa per region, not rows. Regions overlap (a country and its
states). For non-overlapping maps use `glonaf_TxR` and the `glonaf_2024_nol`
shapefile. Codes, as the data dictionaries define them:
- `status`: Naturalized, Invasive. Other statuses (casual, cultivated) exist
  in GloNAF but are not in this table (glonaf.md).
- `completeness_id`: 1 very incomplete, 2 incomplete, 3 complete or close to
  complete.
- `completeness_judge_id`: who judged completeness (0 the authors, explicitly;
  1 the authors, implicitly; 2 the GloNAF team).
- `taxon_group_id`: 1 Tracheophyta, 2 Spermatophyta, 3 Angiospermae, 4
  Gymnospermae, 5 Pteridophyta, 6 other, 7 not clear, 8 Embryophyta.
- `naturalized_explicit_id`: whether the source uses the word naturalized or
  established.
- `iso_equivalent`, `island`: 0/1 flags on regions.

## Access

- **Mirror.** `deep-server:/data/paleodata/glonaf/raw/17105725/` with its
  manifest; [snapshots.tsv](snapshots.tsv).
- **Refresh.** [glonaf_snapshot.sh](glonaf_snapshot.sh) fetches the newest
  Zenodo version; [zenodo-versions.tsv](zenodo-versions.tsv) indexes all.
- **Profile.** `python3 glonaf_profile.py GLONAF_DIR OUT_TSV`
  ([glonaf_profile.py](glonaf_profile.py)).

## Strengths

- One harmonised name backbone (WCVP) across 336 sources and 1,343 regions.
- List completeness is graded, so analyses can weight or filter by it.
- Islands and ISO-equivalent regions are flagged, which eases joins to
  country-level sources.

## Weaknesses and pitfalls

- **No time.** Status is present-day; no first-record or introduction dates.
  Pair with the First Records Database for timing.
- **No origin.** Native ranges and source regions are not in this table.
- **Four-fifths of lists are very incomplete or incomplete** by GloNAF's own
  judgement (2,201 of the 2,764 judged). Richness differences between regions are
  partly list quality.
- **Rows are not taxa.** A region with several lists repeats taxa; 327,807
  distinct taxon-region pairs underlie the 349,271 rows.
- **Plants only.** A three-source crosswalk with GRIIS and First Records is a
  plant crosswalk.
- **Its own README miscounts the list table** (2,274 rows; the file has
  2,774).

## Overlap with other sources

- **GRIIS and the First Records Database.** Exact-name matching of plant
  species by country, in the 125 countries all three cover: 36,058 GloNAF
  pairs, of which 22,856 are also in GRIIS, 17,064 in First Records and
  12,480 in all three ([crosswalk](../alien-first-records/profile/crosswalk_plants.tsv);
  exact names, so a lower bound). See
  [alien-first-records](../alien-first-records/README.md).
- **SInAS 3.2** ([register-deposits](../register-deposits/README.md)) holds
  an earlier GloNAF taxon-region-reference table (357,783 rows) within its
  harmonised inputs.

## EPRP relevance

- **Q-047.** The modern alien-plant stock by recipient region: one outcome
  side of the "crosswalk of outcomes and denominators within one taxon" that
  Codex set as the first gate (76/1420). It supplies naturalization, not
  flows, routes or timing.
- Cannot support: rates or dates of invasion, source regions, animals.

## Citation and terms

Zenodo licence CC BY 4.0. glonaf.org asks users to cite Davis et al. (2025)
and says (checked 2026-10-24): "If you plan to use the GloNAF dataset, we
encourage you to contact the GloNAF core team to check whether there have
been recent updates of the dataset" and "If GloNAF is a major part of the data
analyzed in your study, you should consider inviting the GloNAF core team as
collaborators." Queued as a courtesy contact ([CONTACTS.md](../CONTACTS.md)
C33).

## Verification log

- 2026-10-24 (Claude, Opus 5.5):
  - *checked*: indexed the three Zenodo versions and mirrored the newest (15
    files, 162 MB, md5 verified);
  - *checked*: profiled all tables ([profile](profile/glonaf_profile.tsv));
    16,504 accepted names in the records, against 16,429 taxa on glonaf.org
    (the site's count, not reconciled);
  - *checked*: glonaf.org's citation and contact requests (quoted above);
  - *source claim*: the snapshot date and structural changes (glonaf.md);
    the 336 sources (scoping, from glonaf.md and the data paper);
  - *checked*: plant crosswalk with GRIIS and First Records (see Overlap).
