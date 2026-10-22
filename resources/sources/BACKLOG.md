# Catalogue backlog

Sources to catalogue next, ranked. Barry's interest (22 October 2026):
Quaternary and deep-time analytical and simulation work with Australian case
studies. The Australian scan of 22 October 2026 (Claude Sonnet subagent;
evidence labelled verified or not in its report) produced the list below.
Ranking = relevance × openness ÷ effort. Update this file as entries are
written.

## Done or in progress

NSB, Triton, FRED (documented, not mirrored), FosSahul, SahulArch, AustArch,
OCTOPUS; then the Australian tranche of 22 October: PBDB (Australia and New
Guinea extract), ASUD, Neotoma/IPPD, RPD, GCD, SahulCHAR, SISAL, Beyer 2020,
the SHAPE index, the Sahul sea-level pack and Krapp 2021; then ranks 9–15:
STRATDAT, GA biozonation charts, fossil checklists, Australian fossil-biota
deposits, GBIF and ALA fossil records, AusTraits, the ALA vertebrate species
counts, and the names and status lists. See [INDEX.md](INDEX.md). Ranks 1–15
below are now catalogued; their entries supersede the scan figures quoted in
the table.

## Ranked: Australia and Sahul

| # | Source | Holds | Access and licence | Why |
| ---: | --- | --- | --- | --- |
| 1 | Neotoma, Australasian holdings (IPPD) | 234 Australian sites, 451 datasets (148 pollen, 150 geochronological, 15 charcoal); PNG 22 sites | open API; data licence not yet confirmed (check before mirroring) | Quaternary vegetation and fire context for megafauna and human-arrival work |
| 2 | Beyer et al. 2020 climate and vegetation, 120 ka (doi:10.6084/m9.figshare.12293345) | 0.5° monthly climate, bioclim, NPP, biome; 72 snapshots | Figshare, CC BY 4.0, 1.3 GB | Continuous Sahul forcing for the whole late-Quaternary window |
| 3 | Global Charcoal Database, Australian subset | 148 Australian sites, 13,415 charcoal rows, 790 dates | CRAN package (GPL); paleofire.org data terms to check | Fire history against human arrival |
| 4 | SISALv3 speleothems, Australian caves | 16 caves, 65 entities, 13,838 samples | Oxford ORA, CC BY 4.0 | Hydroclimate records with precise U-series ages |
| 5 | SHAPE / OZ-INTIMATE palaeoarchive index (doi:10.1594/PANGAEA.879515) | 37 records indexed | PANGAEA, CC BY 3.0, 30 kB | Finding aid for Australian palaeoclimate archives |
| 6 | ASUD, Australian Stratigraphic Units Database (GA WFS) | 18,357 units | open WFS, CC BY 4.0 | Resolves formation names for deep-time occurrence data |
| 7 | PBDB, Australian subset | 8,849 collections, 51,242 occurrences (Ediacaran to Quaternary); PNG 155 collections | open API, CC0 | The core open Australian deep-time dataset, and a medium-scale PBDB pilot |
| 8 | Sahul sea-level and palaeogeography pack | shelf area under two ice histories; time-evolving landscapes; 65–45 ka palaeotopography (Zenodo 3959365, 10889086, 8299571) | Zenodo, CC BY 4.0 | Land area and connectivity through time for Sahul models |
| 9 | Australasian fossil species checklists (auFNSL) and Alcheringa checklists | 9 PDF checklists (mammals and birds updated 2026); Mesozoic tetrapods; fossil mammals | PDFs; licences mostly unstated; birds CC BY-NC-ND; old .org domain now redirects to an unrelated site | The only expert-curated Australian fossil species lists; extract, mirror only CC BY items |
| 10 | Ediacaran, Cambrian and Devonian Lagerstätten data (Dryad) | Nilpena bed maps; Dickinsonia; Emu Bay Shale; Gogo | Dryad, CC0 | Fills what PBDB lacks for flagship Australian biotas |
| 11 | ALA and GBIF fossil specimen records | 17,531 (ALA) and 66,252 (GBIF) Australian fossil specimens, mostly foreign museums and NSB | open search APIs; bulk download needs an account | Low novelty; document as partly negative (state museum palaeo collections show zero records) |
| 12 | AusTraits plant traits (doi:10.5281/zenodo.15718081) | Australian flora traits, v7.0.0 | Zenodo, CC BY 4.0 | Vegetation and fire parameterisation |
| 13 | ALA occurrences, vertebrate subset | 185.7 M records in total | open API, mixed licences incl. non-commercial | Modern range comparators |
| 14 | Names and status: APC (NSL export), EPBC lists, AVONET, COMBINE | APC 113,869 rows; EPBC state lists; bird and mammal traits | open; CC BY 3.0 / CC BY 4.0; COMBINE licence unverified | One harmonised taxon table for extinction-risk comparisons |
| 15 | GA basin biozonation and palynology charts | about 22 basin charts; palynology zonations on GTS2004 | eCat PDFs, mostly CC BY 4.0 | Biozone ages for basin sections |

## Serve together

- **PBDB Australian pilot**: PBDB Australia and PNG + ASUD names + fossil
  species checklists + ALA/GBIF fossil records (deduplicated against PBDB
  material citations and NSB).
- **Quaternary palaeoenvironment bundle**: Neotoma/IPPD + Global Charcoal
  Database + SISAL + SHAPE index + Beyer 2020 + sea-level pack, with OCTOPUS
  SahulChar and IPPD layers. Check Neotoma and charcoal-database overlap.
- **Modern comparators bundle**: APC + EPBC + AusTraits + AVONET (+ COMBINE)
  + ALA vertebrate subset.

## Document only (restricted, oversized or unavailable)

- **IUCN Red List**: token and registration; no redistribution.
- **CHELSA-TraCE21k**: 3.85 TB; licence statements conflict.
- **PaleoView**: tool, not archived data. **BRIDGE HadCM3 raw runs**:
  redundant with Beyer 2020.
- **Macrostrat**: no Australian columns (negative result; its name lexicon
  holds 12,279 names imported from ASUD in 2015).
- **GEBCO_2026** (doi:10.5285/4f68d5c7-45eb-f999-e063-7086abc036fa, 7 GB) and
  **AusBathyTopo 250 m 2026** (doi:10.26186/151280, CC BY 4.0, 2.4 GB, south
  of 8°S only): modern topography and bathymetry for palaeoshoreline work;
  DOI-versioned, fetch on demand.
- **Salles et al. 2024** (Zenodo 10889086): figure outputs of a landscape
  model, not a time series of palaeotopography.
- **Lambeck et al. 2014** and **Williams et al. 2018** sea-level curves: tables
  in supplements only (Williams CC BY-NC-ND).
- **Museums Victoria Collections API**: blocked to scripts (Cloudflare 403);
  retry from another host.
- **Queensland Museum palaeontology CSV**: dead link; queued for the museum
  as [CONTACTS.md](CONTACTS.md) C6.
- **Australian Faunal Directory**: per-taxon CSV exports, no licence of its
  own, and a 1,000-taxon export limit; full extract and licence queued as C17.
- **BirdLife Australia Working List**: no licence found.
- **ALA records and GBIF downloads**: both bulk routes need an email address
  or account. Record-level work should filter the GBIF open-data snapshot on
  AWS (288 GB, monthly, citable). ALA's fossil specimens are a subset of
  GBIF's ([gbif-ala-fossils](gbif-ala-fossils/README.md)).
- **Dryad-only deposits** (Craffey et al. 2024, Arman et al. 2025, Couzens et
  al. 2026): downloads need a Dryad API account; Barry to fetch
  ([au-fossil-deposits](au-fossil-deposits/README.md)).
- **TimeScale Creator GA datapack** (eCat 68802): licence conflict, C9(f).

## Elsewhere

- **PBDB (global)**: after the Australian pilot.
- **Deposits already cited in EPRP**: 78 Dryad, Zenodo, Figshare and PANGAEA
  DOIs (28, 39, 5, 6).
