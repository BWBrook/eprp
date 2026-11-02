---
id: octopus
name: OCTOPUS, an open geochronology and environmental database for Sahul and beyond
kind: database
status: "active (site banner v.2.3, July 2025)"
last_update: 2025-07
scope:
  taxa: [not taxonomic; hosts age and proxy collections]
  time: "Quaternary (cosmogenic nuclides to Pleistocene; luminescence, radiocarbon, charcoal, pollen)"
  space: "Sahul for most collections; global for cosmogenic denudation rates"
  record_unit: "per collection: an age determination, a sample, a basin or a proxy observation"
size:
  as_of: "WFS hit counts, 2026-10-22"
  layers: 25
  sahularch_ages: 10714
  fossahul_records: 11858
  sahulchar_rows: 48234
  ippd_pollen_rows: 155952
access:
  tier: open
  licence: "CC-BY-4.0 for site content and collections per OCTOPUS documentation (exceptions noted per collection)"
  routes:
    - {type: wfs, url: "http://geoserver.octopusdata.org/geoserver/wfs (namespace be10-denude)", state: "open, HTTP only, CSV/GeoJSON/GML/shapefile/KML, paging, no practical cap", checked: 2026-10-22}
    - {type: wms, url: "http://geoserver.octopusdata.org/geoserver/wms", state: "open", checked: 2026-10-22}
    - {type: web-ui, url: "https://octopusdata.org", state: "map viewer and export", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 and WMS 1.3.0 (GeoServer)"
versioning:
  replay: none
  notes: "live database; each row carries DBVERNO; past versions archived on Zenodo and marked obsolete"
mirror:
  path: "deep-server:/data/paleodata/<collection>/octopus-wfs (sahularch, fossahul so far)"
  policy: "snapshot collections as they are catalogued, not the whole platform"
  state: "SahulArch and FosSahul layers snapshotted 2026-10-22"
lineage:
  upstream:
    - "CABAH and University of Wollongong compilations (SahulArch, SahulSed, SahulChar)"
    - "partner collections: FosSahul, ExpAge, IPPD pollen"
  downstream: []
eprp_questions: []
citation:
  - "Codilean, A. T. et al. (2022). OCTOPUS database (v.2). Earth System Science Data 14: 3695-3713. doi:10.5194/essd-14-3695-2022"
  - "Codilean, A. T. et al. (2018). OCTOPUS: an open cosmogenic isotope and luminescence database. Earth System Science Data 10: 2123-2139"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation read by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# OCTOPUS

## Summary

OCTOPUS, run from the University of Wollongong, is a PostGIS database and map
service for Quaternary geochronology, built to hold Sahul-wide compilations
under shared conventions (one schema per collection type), with blurred
locations for the culturally sensitive collections.
It is the only current route to [SahulArch](../sahularch/README.md), and it
also serves SahulSed (luminescence ages of aeolian, coastal, fluvial and lake
sediments), SahulChar (charcoal), the Indo-Pacific Pollen Database baseline,
global cosmogenic-nuclide denudation rates, and partner copies of
[FosSahul](../fossahul/README.md) and the ExpAge exposure-age compilation.
Every collection is reachable through one open WFS, which makes OCTOPUS a
high-value programmatic route for Sahul palaeoenvironmental work. This entry
describes the platform; profiles and extraction recipes live with each
collection's own entry.

## Contents

WFS hit counts on 2026-10-22 (documentation scan; SahulArch and FosSahul
confirmed by our snapshots):

| Collection | Layer(s) | Records |
| --- | --- | ---: |
| SahulArch | `sahularch_c14`, `_osl`, `_tl` | 9,501 / 973 / 240 |
| FosSahul (partner) | `fossahul_webmercator_nrand_25000` | 11,858 |
| SahulSed OSL | aeolian, coastal, fluvial, lacustrine | 772 / 1,008 / 1,212 / 474 |
| SahulSed TL | aeolian, coastal, fluvial, lacustrine | 361 / 362 / 564 / 41 |
| SahulChar | `sahulchar`, `sahulchar_units` | 48,234 rows / 535 units |
| IPPD pollen | `ippd_baseline_pollen`, `ippd_datasets` | 155,952 rows / 311 datasets |
| CRN denudation | Australian, international, large basins, in preparation | 297 / 5,376 / 261 / 157 basins |
| ExpAge (partner) | `expage` | 16,009 |

## Provenance and lineage

OCTOPUS v1 (Codilean et al. 2018) held cosmogenic-nuclide and luminescence
data. Version 2 (Codilean et al. 2022) added SahulArch, SahulSed and partner
collections, funded through the ARC Centre of Excellence for Australian
Biodiversity and Heritage (CABAH). The site banner reads v.2.3 (July 2025).
Each row carries a `DBVERNO` stamp, e.g. `v2.3(2)` for SahulArch and
`v2.3(1)` for FosSahul.

## Structure

One schema per collection type with shared conventions: hierarchical IDs
(metasite, site, sample, observation), up to four references per record,
missing values coded −9999.99, `ND` or `NA`, and a version stamp. Only the
SahulArch and FosSahul layers are blurred, served as 25 km random-displacement
polygons with true coordinates held back. SahulSed, SahulChar, IPPD, ExpAge and
the cosmogenic layers carry point coordinates (`X_WGS84`, `Y_WGS84`). Field descriptions and the database schema are
archived on Zenodo (records 7352827 and 7352807, marked obsolete).

## Access

```bash
python3 resources/tools/data_mirror.py wfs http://geoserver.octopusdata.org/geoserver/wfs \
  be10-denude:<layer>[,be10-denude:<layer>] /data/paleodata/<id>/octopus-wfs --license "CC-BY-4.0 per OCTOPUS documentation"
```

GetCapabilities lists 25 feature types. CQL filters work. The service is HTTP
only on its own subdomain; `https://octopusdata.org/geoserver/wfs` proxies
capabilities. The web UI enables export after an "intended use" is chosen;
cosmogenic "Download Collection" asks for name, email and intended use.

## Strengths

- **One open, programmatic door** to several Sahul compilations that are not
  downloadable elsewhere.
- **Consistent schema and missing-value coding** across collections.
- **Cultural safety intended** for the archaeological and fossil
  collections, which are blurred to 25 km (but see Pitfall 4).

## Weaknesses and pitfalls

1. **Live and unversioned for download.** Archived versions on Zenodo are
   marked obsolete; snapshot what you use and record `DBVERNO` and the
   server timestamp.
2. **Partner copies diverge from their sources.** The FosSahul layer has
   11,858 records against 11,872 in its March 2021 release: it carries the
   2021 ratings but lacks the 6 records added in 2021 and 8 older ones. It is
   restructured into OCTOPUS fields and blurred to 25 km.
3. **Fragile transport.** HTTP only for the WFS subdomain; DOIs for some
   collections are metadata-only or "TBA".

## Overlap with other sources

- **SahulArch** exists only here (see its entry).
- **FosSahul.** OCTOPUS holds a restructured, blurred copy of the March 2021
  release; use the Figshare release as the reference.
- **IPPD and SahulChar** overlap Neotoma's Australasian pollen and the
  Global Charcoal Database; both are in the Australian backlog.

## EPRP relevance

The access route for Sahul archaeological, sedimentary, charcoal and pollen
chronologies. Charcoal and pollen layers are candidates for the Quaternary
palaeoenvironment bundle in the [backlog](../BACKLOG.md).

## Citation and terms

Cite Codilean et al. (2022) and each collection's own reference and DOI.
CC BY 4.0 per the documentation; check each collection (SahulArch's
radiocarbon DOI says CC BY-NC 4.0 in DataCite).

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | WFS capabilities, 25 layers, hit counts | checked (documentation scan) |
| 2026-10-22 | SahulArch and FosSahul layer snapshots | checked |
| 2026-10-22 | Platform history, schema, licence statements | source claim (Codilean et al. 2022; OCTOPUS documentation) |
| 2026-10-22 | Which layers are blurred | checked (independent review) |
