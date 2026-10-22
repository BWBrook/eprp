---
id: ga-biozonation
name: Geoscience Australia Basin Biozonation and Stratigraphy charts, and palynology zonations
kind: deposit
status: frozen
last_update: "2017 (newest charts); series record revised 2018"
scope:
  taxa: ["biozone schemes: dinocysts, spore-pollen, foraminifera, nannofossils, conodonts and others"]
  time: "Proterozoic to Neogene"
  space: "Australian sedimentary basins and margins (34 numbered charts)"
  record_unit: "one chart: a basin's biozonation, lithostratigraphy and sequences against a time scale"
size:
  as_of: "url snapshot 2026-10-22T0856Z"
  files: 39
  bytes: 120369345
access:
  tier: open
  licence: "CC-BY-4.0 (eCat ISO metadata of every record)"
  routes:
    - {type: catalogue, url: "eCat 76687 (chart series), 23332-24225 and 31035 (1994 charts), 64962 (Record 2006/23), 61127", state: "PDFs on d28rz98at9flks.cloudfront.net", checked: 2026-10-22}
    - {type: catalogue, url: "eCat 68802 (TimeScale Creator 7.0 with the GA datapack)", state: "not mirrored: the bundled software is all rights reserved", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "superseded chart versions remain as separate eCat records (2008 versions, annual compilations)"
mirror:
  path: deep-server:/data/paleodata/ga-biozonation
  policy: "current chart series, the 1994 charts not superseded in it, and the palynology zonations"
  state: "2026-10-22T0856Z_url (39 files)"
lineage:
  upstream:
    - "AGSO and GA biostratigraphers' zone schemes and well picks (see stratdat)"
  downstream:
    - "basin studies and petroleum exploration; the TimeScale Creator Australian datapack"
eprp_questions: []
citation:
  - "Geoscience Australia, Basin Biozonation and Stratigraphy Chart Series (eCat 76687), CC BY 4.0, with the chart number and year"
  - "Monteil, E. (coordinator) (2006). Australian Mesozoic and Cenozoic Palynology Zonations, updated to the 2004 Geologic Time Scale. Geoscience Australia Record 2006/23 (eCat 64962)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Geoscience Australia biozonation charts and palynology zonations

## Summary

Geoscience Australia's Basin Biozonation and Stratigraphy charts set out, for
each Australian sedimentary basin, the biozones (dinocyst, spore-pollen,
foraminiferal, nannofossil and others), lithostratigraphic units and
sequences against a time scale. They are the standard reference for dating
Australian basin successions, and the scheme behind the picks in
[STRATDAT](../stratdat/README.md). The charts are large PDFs, not data; the
time scale changes with the chart's date (AGSO 1996, GTS2004, GTS2012,
GTS2016). Reach for them to read a basin's zone scheme and correlations;
for tabular zone ages, the only machine-readable source is the TimeScale
Creator datapack, whose redistribution status is unclear.

## Contents

From the mirrored files and the source scan (time scales read from chart
text by the scan):

| Set | eCat | Charts | Dates | Time scale |
| --- | --- | --- | --- | --- |
| Chart series | 76687 | 24 PDFs, charts 3–6, 8A/B, 14, 16, 17, 19–22, 26, 31–36, 38–41 | 1997–2017 | 1997–99 charts: AGSO 1996 time scale; 2013–15 charts: GTS2012; Amadeus (6) and Browse (32), 2017: GTS2016 |
| 1994 charts | 23332, 23334, 23346, 23350, 23352, 23354, 23356, 24220, 24222, 24225, 31035 | charts 1, 2, 7, 9–13, 15, 18, 28a/b | 1994 versions | pre-GTS2004 |
| Palynology zonations | 64962 | GA Record 2006/23 and `Data.zip` (four charts as PDF, EPS and JPEG) | 2006 | GTS2004 |
| North West Shelf dinocyst zonation | 61127 | one PDF | 2004 | pre-GTS2004 |

The mirrored set is 39 files, 120 MB; the largest is the 2014 Bonaparte Basin
chart (44 MB). Superseded 2008 versions (eCat 65648, 65649, 65665) and the
annual compilations (68801, 70371, 73734, 75819, 83216) duplicate these and
are not mirrored. Chart numbers 23–25, 27, 29, 30 and 37 were not found.

## Provenance and lineage

Compiled by AGSO and Geoscience Australia biostratigraphers from the zone
schemes of the basins and the well picks in STRATDAT; the palynology
zonations were recalibrated to GTS2004 in 2006 (Monteil, coordinator, with
Partridge's calibrations). GA's biostratigraphy page names GTS2012 as its
standard and refers to an internal Timescales Database that is not public.
No chart is newer than 2017.

## Structure

Each chart is one very large PDF page with a text layer: columns for time
scale, zones by fossil group, lithostratigraphy, sequences and events. The
palynology zonation charts' text layer is scrambled and needs coordinate
parsing.

## Access

- **eCat.** Files at `https://d28rz98at9flks.cloudfront.net/<eCat>/<file>`;
  record metadata through the eCat CSW service.
- **Mirror.** `deep-server:/data/paleodata/ga-biozonation/raw/2026-10-22T0856Z_url/`,
  files prefixed with their eCat number. Index: [snapshots.tsv](snapshots.tsv).
- **TimeScale Creator datapack (not mirrored).** eCat 68802 ships TimeScale
  Creator 7.0 with an unencrypted tab-delimited datapack, "Geoscience
  Australia Biostratigraphy and Regional Lithostratigraphy" (GTS2016; about
  290 biostratigraphic columns and 12,000 zone and datum entries, per the
  scan). The eCat record says CC BY 4.0, but the software's licence reserves
  all rights to the Geologic TimeScale Foundation and its public Australian
  datapack is encrypted, so we hold no copy until GA confirms the datapack may
  be redistributed.

## Strengths

- Authoritative, basin-by-basin zone schemes with lithostratigraphy and
  sequences on one page, openly licensed.
- Charts dated 2013 or later are calibrated to GTS2012 or GTS2016.

## Weaknesses and pitfalls

- **Mixed time scales.** Charts of different years use different scales; check
  each chart's scale before combining ages.
- **Not data.** Ages and zone boundaries must be read off PDFs; only the
  restricted TimeScale Creator datapack is tabular.
- **No updates since 2017**, and no chart on GTS2020.
- **Gaps in the numbering** (charts 23–25, 27, 29, 30, 37 not found).

## Overlap with other sources

STRATDAT holds the well picks these zones are assigned in; the ASUD register
holds the unit names and ages; PBDB's Australian ages use its own GTS2020-era
scales, so a zone age read from a pre-2012 chart will differ from PBDB's.

## EPRP relevance

Reference for interpreting STRATDAT picks and for dating Australian basin
successions in deep-time case studies.

## Citation and terms

CC BY 4.0. Cite Geoscience Australia, the chart number and year, and the eCat
record.

## Verification log

- 2026-10-22, checked: 39 files mirrored (sizes in the manifest); eCat
  records and file URLs read from the catalogue metadata.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): time scale of
  each chart (read from chart text), the palynology zonation content, the
  TimeScale Creator datapack's content and licence conflict, GA's standard
  time scale and internal database, missing chart numbers.
