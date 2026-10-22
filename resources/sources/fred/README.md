---
id: fred
name: FRED, the Fossil Record Electronic Database (New Zealand Fossil Record File)
kind: database
status: active
last_update: "continual (web app v5.0.5, 2026-07-21)"
scope:
  taxa: "all fossil groups: a controlled list of 51 groups; foraminifera, molluscs, miospores and dinoflagellates dominate"
  time: "Cambrian to Recent, mostly Late Cretaceous–Cenozoic; ages as New Zealand stages (NZGT2015)"
  space: "New Zealand and its EEZ; also the Chathams, subantarctic islands, Ross Sea region of Antarctica, New Caledonia and some Pacific islands"
  record_unit: "a registered fossil locality (FR number, e.g. M25/f1) with its collections, palaeontological analyses (faunal lists) and age assessments"
size:
  as_of: "2026-10-22 (public locality layer); June 2020 (Clowes et al. 2020)"
  localities: 105492
  palaeontological_analyses: "over 100,000"
  taxonomic_identifications: "over 1,000,000"
access:
  tier: registered
  licence: "no data licence; research-only conditions of use. Public map service header says CC-BY 3.0 NZ (scope unclear)"
  routes:
    - {type: website, url: "https://fred.org.nz", state: "online; FR numbers, coordinates and locality text public, all else after free, manually approved registration", checked: 2026-10-22}
    - {type: wfs-wms, url: "https://data.gns.cri.nz/webmaps/gns/wfs (layer gns:pg_fred_site_view)", state: "public locality skeleton, 105,492 points; redistribution rights unresolved", checked: 2026-10-22}
    - {type: tsv-download, url: "FRED query results, registered users", state: "tab-separated; downloads are logged; not tested", checked: 2026-10-22}
    - {type: datacite, url: "https://doi.org/10.21420/JQQB-NK89", state: "DOI for the dataset as a whole; resolves to the GNS metadata record", checked: 2026-10-22}
  api: "none for full records (ODBC is GNS-campus only); WFS for the public locality layer"
versioning:
  replay: none
  notes: "live database, continually updated (about 60 localities and 45 analyses a month in 2020); no snapshots or versions"
mirror:
  path: none
  policy: "not mirrored: research-only conditions, restricted classification in the custodian's metadata, registration required"
  state: "catalogue entry and access recipe only"
lineage:
  upstream:
    - "NZ Fossil Record File paper register (from 1946; first FR number 1947)"
    - "NZ Geological Survey and GNS Science collections"
    - "university and museum collections"
  downstream:
    - "PBDB: 2,426 NZ collections naming 2,023 FR numbers, from literature, not a FRED import"
    - "NZ Geological Timescale; QMAP geological mapping; NZ molluscan macroevolution studies (from downloads)"
eprp_questions: [Q-034]
citation:
  - "GNS Science & Geoscience Society of New Zealand (2003). New Zealand Fossil Record File [Data set]. GNS Science. doi:10.21420/JQQB-NK89"
  - "Acknowledgement required: 'We acknowledge use of information contained in the New Zealand Fossil Record File.'"
  - "Clowes, C. D. et al. (2020). New Zealand Journal of Geology and Geophysics 64: 62-71. doi:10.1080/00288306.2020.1799827 (description)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# FRED: the New Zealand Fossil Record File

## Summary

FRED is the electronic form of the New Zealand Fossil Record File, the
national register of fossil localities kept since 1946 by the NZ Geological
Survey (now GNS Science, part of Earth Sciences New Zealand) and the
Geoscience Society of New Zealand. It holds 105,492 registered localities,
over 100,000 palaeontological analyses and over a million taxonomic
identifications, overwhelmingly from mainland New Zealand, for which its
custodians call it an essentially complete compilation. It underpins New
Zealand biostratigraphy, the national geological timescale and a run of
molluscan macroevolution studies. Access is free but needs approved
registration. Use is limited to research, and data cannot be redistributed,
so this catalogue holds an access recipe, not a copy. It is the catalogue's
test case for a registered-access source.

## Contents

**What a record is.** A locality carries a Fossil Record Number (FRN): map
sheet, `/f`, serial, e.g. `A44/f0001`. Older NZMS1 numbers (`N164/f500`) are
kept as aliases; re-collections add a letter suffix. A locality is an outcrop
spot sample, a vertical section (one FRN, samples by height) or a drillhole
(one FRN, samples by depth, top-of-hole coordinates only). Under it sit
collections, palaeontological analyses (one person's identifications of one
group on one date, never deleted when revised), taxonomic lists and age
assessments (FRED User Manual v1.0, 2018, §5).

**Counts.**

| Item | Count | Date, source |
| --- | ---: | --- |
| Localities in the public layer | 105,492 | 2026-10-22, WFS hit count (checked) |
| of which outcrop / drillhole / vertical section | 101,772 / 3,594 / 126 | 2026-10-22, documentation scan |
| Palaeontological analyses | over 100,000 | Clowes et al. 2020 |
| Taxonomic identifications | over 1,000,000 | Clowes et al. 2020 |
| Growth | ~60 localities and ~45 analyses a month | Clowes et al. 2020 |
| Samples by era | Cenozoic ~68,000; Mesozoic ~12,000; Palaeozoic ~1,000 | Clowes et al. 2020, Fig. 3 |
| Samples by group (top five) | foraminifera ~42,000; molluscs ~22,000; miospores ~11,500; algae ~8,400; brachiopods ~5,300 | Clowes et al. 2020, Fig. 3 |

Published totals range from "over 100,000" to "around 110,000"; the live
layer count is the one to quote, with its date. The FAQ's older split (over
50,000 localities with full data, about 30,000 with coordinates only) dates
from before a full-entry programme begun in 2005; the current split is not
published.

**Geography** (public layer, by bounding box, 2026-10-22): mainland New
Zealand 100,397; Pacific islands north of 30°S 2,474; Chathams region about
1,070; Antarctica 945; subantarctic 405.

**Fields** (manual, Appendix 12.1). Locality: coordinates in any of many NZ
grids, converted to WGS84, with an accuracy field defaulting to 10 m. Most
legacy positions were read from 1:63,360 or 1:50,000 maps to the nearest
100 m. Collection: collectors, date, whether fossils were in place.
Stratigraphy: unit name (linked to StratLex where possible), known and
inferred stage limits, dip and strike (poorly populated). Lithology: grain
size, colour and other descriptors, with an inferred environment (marine or
non-marine plus text). Palaeontology: identifier, date, institution and
number, determined stage limits, and a taxonomic list by group with names as
originally identified. Ages come in four kinds (known, inferred, determined,
adopted); a consensus age is computed automatically (since 2017–2020).

## Provenance and lineage

- **1946–1975.** The NZ Geological Survey adopted the Fossil Record Form in
  1946; the first FR number was allocated in 1947, on NZMS1 imperial map
  sheets (Clowes et al. 2020).
- **1970s.** Electronic transcription began in 1970. Numbers were migrated to
  NZMS260 sheets, and the NZMS1 master files closed in 1975.
- **2000–2005.** Grid coordinates for about 30,000 remaining localities were
  entered in 2000. FRED was on the web with online registration by 2005, when
  about 65% of some 86,000 paper records were in electronic form.
- **Now.** An Oracle database hosted by GNS Science (web app v5.0.5), funded
  as a Nationally Significant Collection and Database. It is jointly governed
  by GNS and the Geoscience Society under a memorandum of understanding, with
  regional curators. The dataset DOI was registered in 2020; its "2003" year
  is DataCite metadata, not a launch date.

The companion **National Paleontological Collection** (doi:10.21420/0X8Y-H306)
holds the physical specimens. Its public Type Catalogue links type and
figured specimens to FR numbers: the one openly browsable cross-link into
FRED.

## Structure

Four entities: location → collection → palaeontological analysis → list of
fossils. Each analysis is one identifier's list for one group on one date;
re-identifications are appended. There is no taxonomic synonymy: names stay
as identified, checked only against a spelling thesaurus. Ages are New
Zealand stages calibrated to the current NZ Geological Timescale (NZGT2015);
numeric ages are searchable but not entered.

## Access

**Without registration** (checked 2026-10-22):

- FR number search, locality numbers and coordinates, and the interactive map.
  Map pop-ups also show the locality description, and a detail page shows
  original and converted coordinates.
- The map's GNS GeoServer layer `gns:pg_fred_site_view` is open on WMS and
  WFS 2.0.0. It returns FR number, locality type, locality text and a WGS84
  point for all 105,492 localities, as CSV, GeoJSON or Shapefile, with no
  feature cap. It holds no stratigraphy, ages or taxa.

```bash
curl -s 'https://data.gns.cri.nz/webmaps/gns/wfs?service=WFS&version=2.0.0&request=GetFeature&typeNames=gns:pg_fred_site_view&resultType=hits'
```

We fetched only counts and the schema. See Terms before using the layer.

**With registration.** Apply at
`https://data.gns.cri.nz/register/user_reg.jsp?DBase=FRED`. Approval is
manual and takes a few days. The form asks for name, organisation, contact
details, a reason, read or add access, and acceptance of the conditions.
Registration lapses after two years of inactivity. Registered users see full
locality, stratigraphic and lithological data and released palaeontology and
adopted ages; embargoed lists stay hidden. Query results download as
tab-separated files (locality, adoption and palaeontology record sets); the
manual states that downloads are logged. Records also export as PDF. The
query interface cannot search within results or for co-occurring taxa, so
analyses download per taxon and join locally.

**Recipe for an EPRP analysis.** Barry registers (or authorises an agent
account in his name). Run the query; save the TSV with its download date
under the analysing project, not `/data/paleodata`. Record query terms, date
and row counts. Cite originators as the conditions require. Do not share the
download.

## Strengths

- **Completeness for mainland New Zealand.** Over a century of national
  survey collecting in one register, with a stable identifier (the FR number)
  that journals require and other databases cite.
- **Expert identifications.** Molluscan determinations come largely from a
  few specialists (76% from Beu, Marwick and Fleming, per Womack 2022), which
  makes regional species-level analysis feasible.
- **Rich context.** Stratigraphy, lithology, collection circumstances and
  multiple age assessments per sample, with a consensus age.
- **Drillholes and sections.** Petroleum-well and measured-section
  biostratigraphy alongside outcrop samples.
- **Proven research use.** Rock-volume, sequence-stratigraphic, body-size,
  aragonite and Pull-of-the-Recent biases were all quantified on FRED data.

## Weaknesses and pitfalls

1. **Not reproducible as a snapshot.** It is a live database with no
   versions. Record the download date and keep the file; the same query
   later can return different data.
2. **No taxonomic synonymy.** Names are as identified, often outdated.
   Users must harmonise (Crampton et al. 2006 synonymised mollusc names
   against a revised list).
3. **Ages are coarse and often unadopted.** Ages are NZ stages; adopted ages
   exist for few records. In Crampton et al.'s mollusc data, 39% of
   stage-level lists were not dated to a single stage.
4. **Position precision.** Legacy positions are good to about 100 m at
   best, and the FAQ admits some are wrong; converted coordinates are printed
   to spurious precision.
5. **Uneven data entry.** Dip and strike, stratigraphic names, authors and
   collector names are poorly or inconsistently populated. The custodian's
   metadata states that checking is limited and errors are not sought
   systematically.
6. **Embargoes.** Palaeontological lists may be embargoed for five years,
   renewable; the number embargoed is not published.
7. **Off-mainland coverage is thin.** Clowes et al. (2020) judge Antarctica,
   the wider Zealandia and the southwest Pacific insufficiently complete for
   mainland-style studies.
8. **Locality counts are not occurrence counts.** Analyses and
   identifications are the occurrence-like units; one locality can carry many
   of each.

## Overlap with other sources

- **PBDB.** Of PBDB's 4,017 New Zealand collections (20,825 occurrences),
  2,426 name an FR number in the collection name (strict pattern
  `<sheet>/f<number>`), covering 2,023 distinct FR numbers (about 2% of FRED
  localities) and 10,498 occurrences, half of PBDB's New Zealand total. They
  come from 175 literature references, chiefly systematic monographs (one
  1992 Triassic–Jurassic brachiopod monograph supplies over 1,000). These are
  literature citations of FRED localities, not an import. Measured by us
  ([method](#verification-log)).
- **GBIF.** No FRED dataset among the publisher's 61 datasets; New Zealand
  fossil specimens in GBIF are mostly Neptune microfossils.
- **Deposited datasets.** None derived from FRED found in Zenodo, Dryad,
  PANGAEA or Figshare. The major mollusc compilations (Crampton et al. 2003,
  2006; Foote et al. 2007; Womack et al. 2020–21) analysed FRED downloads
  without depositing them.

## EPRP relevance

- **Q-034** (pre-human island extinction rates) lists New Zealand among
  candidate systems and needs island fossil compilations. FRED registers New
  Zealand fossil localities, but vertebrates are sparse in it; specialist
  vertebrate compilations will matter more.
- More broadly, FRED is the route to New Zealand Cenozoic marine
  macroevolution (molluscs, foraminifera, palynology) at regional scale, a
  well-trodden test bed for sampling-bias methods.

## Citation and terms

Conditions of use (fred.org.nz/conditions.jsp), accepted at registration:

1. Bona fide research only; the custodians will act to prevent use for
   commercial exploitation of fossil localities.
2. No warranty: data "represent opinions of individual contributors and may
   be incomplete, incorrect, or obsolete".
3. Users who retrieve data "are also expected to contribute appropriate
   data".
4. Locality, stratigraphic and sedimentological data are open to registered
   users; full palaeontological data may be embargoed by the originator.
5. Acknowledge the FRF in publications, reports and presentations: "We
   acknowledge use of information contained in the New Zealand Fossil Record
   File", and cite the dataset DOI.
6. Cite originators (author and date) of palaeontological data used. Where
   data from one or a few palaeontologists form a substantive part of a
   project, invite them to participate in interpretation and publication.

Nothing permits redistribution or a public copy. The custodian's metadata
classes the dataset as restricted ("Research IP", "Commercial data"). The
public map service's header says "These map data are released free under
the Creative Commons Attribution 3.0 New Zealand (CC-BY 3.0) Licence" but
does not name FRED. Whether the locality skeleton may be archived or shared
is unresolved; settling it means asking the custodian (frf@earthsciences.nz).
That question is parked in [CONTACTS.md](../CONTACTS.md) as C8.

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | Conditions of use, FAQ, quick start, what's new, user manual v1.0 (2018) | source claim (read in full) |
| 2026-10-22 | Clowes et al. 2020 description paper | source claim (read in full by the documentation scan) |
| 2026-10-22 | GNS metadata record: restricted, Research IP, scope incl. Antarctica and New Caledonia | checked |
| 2026-10-22 | Public WFS layer: 105,492 localities; CC-BY 3.0 NZ service header | checked (hit count and capabilities only) |
| 2026-10-22 | Locality types and regional counts from the WFS | checked (documentation scan; counts only) |
| 2026-10-22 | PBDB: 2,426 of 4,017 NZ collections name 2,023 FR numbers; 10,498 occurrences; 175 references | checked (PBDB API, regex `[A-Z]\d{2,3}/f\d+` on collection names) |
| 2026-10-22 | No FRED dataset in GBIF; none deposited in Zenodo, Dryad, PANGAEA, Figshare | checked (searches; absence is search coverage only) |
| 2026-10-22 | Registered-user downloads and their content | source claim (manual); not tested, no account |
| 2026-10-22 | Uses and bias studies (Crampton, Foote, Cooper, Collins, Prebble, Womack) | source claim (abstracts, papers and Clowes et al. 2020) |
