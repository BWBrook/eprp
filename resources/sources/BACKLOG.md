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

## Next: driven by the EPRP question registers (23 October 2026)

A survey of the applied register (50 questions) and the blue-sky register (18)
against this catalogue (Claude Sonnet subagent, 23 October; its scores are its
own construct) found little overlap: the catalogue serves 12 of 68 questions,
through Triton, NSB, FRED and the PBDB Australian extract, and no question
names any of the Australian-tranche sources (their uses are inferred: Q-024,
Q-034, Q-047, Q-022). The registers' inputs are mostly global and deep-time.
Ranked by the questions served (develop status weighted above hold) and by
readiness:

| # | Source | Serves | Access | Notes |
| ---: | --- | --- | --- | --- |
| 1 | ~~PBDB, global~~ **done 23 Oct** ([pbdb](pbdb/README.md)) | 43 questions (8 develop) | public global snapshot, reconciled by partition | [Detail withheld pending disclosure to the data custodian.] |
| 2 | ~~Dryad deposits the registers name~~ **done 23 Oct** ([register-deposits](register-deposits/README.md)) | 16 questions incl. Q-038 and B-002 | `data_mirror.py dryad` | 15 deposits, 545 MB |
| 3 | **Fossil-inclusive dated trees** | Q-012 (active), Q-022, Q-004, Q-043 | Lamyman 2026, Zenodo 18854730 (1.16 GB, CC BY 4.0); Aze 2011; Cantalapiedra 2019 (Figshare) | Only 0.9 MB of Lamyman is held locally |
| 4 | **Palaeogeography and plate models** | 15 questions; the Triton/NSB plate-model inconsistency blocking Q-012 exposure; B-005, Q-020, Q-040, Q-049 | PaleoDEM (Zenodo 5348492); GPlates rotation models (Seton 2012, Matthews 2016, Merdith 2021; recall) | PBDB already returns three palaeocoordinate models |
| 5 | **Climate reconstructions and forcing** | Q-030 (develop), Q-027, Q-049, Q-007, Q-011, Q-003 | PhanDA, PhanSST (GitHub, no licence declared; papers CC BY), HadCM3L priors (Zenodo 8237751), Song 2021 (Zenodo 5027293), CENOGRID and LR04; LIP, CO2 and δ13C event tables (Green 2022, Rothman 2017) | 62 MB held locally; licence question for the repositories |
| 6 | **Time scale** | Q-041, Q-035, Q-005 | GTS2020 and ICS boundary ages with uncertainties | TimeScale Creator datapack blocked (C9 f) |
| 7 | **Macrostrat, global** | B-005, B-007, B-008 and inferred others | open API, CC BY 4.0 | Reclassify: the Australian negative does not decide a global need |
| 8 | **Island-extinction compilations** | Q-034, Q-017, Q-004 | Rozzi 2023 (Figshare, GitHub); Cooke 2023 (Zenodo 10014585) | Joins the Sahul and FRED work |
| 9 | **Modern-bridge time series and invasions** | Q-025 (develop), Q-028, Q-047 | BioTIME, GRIIS, SInAS 3.1.1, Seebens first records, GloNAF | Hosting to confirm |
| 10 | **LegacyPollen and LegacyAge 1.0** | Q-024 | ESSD data papers (PANGAEA; recall) | Neotoma covers the Sahul slice only |

Also: document the main agents' local holdings (`data/raw/`, 2.9 GB on the
laptop) as catalogue entries or archived extracts, so nothing is fetched
twice; their Triton v4 files match this mirror's manifest.

## Ranked: Australia and Sahul (22 October; catalogued)

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
- **TimeScale Creator GA datapack** (eCat 68802): licence conflict, C9(f).

## Elsewhere

- **PBDB (global)**: after the Australian pilot.
- **Deposits already cited in EPRP**: 78 Dryad, Zenodo, Figshare and PANGAEA
  DOIs (28, 39, 5, 6).
