---
id: gcd
name: Global Paleofire Database (GPD), formerly the Global Charcoal Database (GCD)
kind: database
status: "active online (paleofire.org); last packaged release 2020-10-26; moving into Neotoma"
last_update: "online database live; CRAN GCD 4.0.7 dated 2020-10-26"
scope:
  taxa: [not taxonomic; sedimentary charcoal records]
  time: "Late Quaternary; Sahul sites mostly Holocene (median oldest age 9.3 ka), 38 reach 20 ka"
  space: "global; 185 Sahul sites in the CRAN release (Australia 152, New Guinea 24, Torres Strait 9)"
  record_unit: "site (one core) with charcoal samples: depth, estimated age, quantity, unit, method, type"
size:
  as_of: "CRAN GCD 4.0.7"
  sites: 935
  samples: 174980
  sahul_sites: 185
  sahul_samples: 15332
access:
  tier: open-nc
  licence: "data: CC BY-NC-ND per the paleofire.org terms of use (site footer: All Rights Reserved); CRAN package code: GPL (>= 2)"
  routes:
    - {type: web-ui, url: "https://paleofire.org (site listing at /site/, exports per the user manual)", state: "online GPD, 1,249 sites and 1,271 cores listed; exports not tested", checked: 2026-10-22}
    - {type: r-package, url: "https://cran.r-project.org/package=GCD (4.0.7); archive of 3.0.0-4.0.6", state: "frozen since 2020", checked: 2026-10-22}
    - {type: noaa, url: "https://www.ncdc.noaa.gov/paleo/study/20042 (GCD version 3, Access database)", state: "archived 2016", checked: 2026-10-22}
  api: none
versioning:
  replay: partial
  notes: "14 CRAN releases (3.0.0 to 4.0.7, 2013-2020) indexed in cran-versions.tsv and fetchable from the CRAN archive; the online database is unversioned"
mirror:
  path: deep-server:/data/paleodata/gcd
  policy: "latest CRAN release; online exports not taken (untested route)"
  state: "cran 2026-10-22T0634Z_url (GCD_4.0.7.tar.gz); derived/paleofiresites_4.0.7.tsv"
lineage:
  upstream:
    - "GCD1 (Power et al. 2008), GCD2 (Daniau et al. 2012), GCD3 (Marlon et al. 2016), GCD4 (Blarquez, CRAN, from 2018 mirroring the online SQL database); Global Palaeofire Working Group (PAGES, to 2019), now the International Paleofire Network"
  downstream:
    - "RPD (178 of its 182 Sahul entities); SahulCHAR (about a third of its records derive from or also exist in the GPD); Mooney et al. 2011; Mariani et al. 2024"
eprp_questions: []
citation:
  - "Power, M. J. et al. (2008). Changes in fire regimes since the Last Glacial Maximum. Climate Dynamics 30: 887-907. doi:10.1007/s00382-007-0334-x"
  - "Marlon, J. R. et al. (2016). Reconstructions of biomass burning from sediment-charcoal records to improve data-model comparisons. Biogeosciences 13: 3225-3244. doi:10.5194/bg-13-3225-2016"
  - "Blarquez, O. GCD: Global Charcoal Database, R package 4.0.7 (2020)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Global Paleofire Database (formerly the Global Charcoal Database)

## Summary

The GCD, now called the Global Paleofire Database, is the long-standing
community archive of sedimentary charcoal records, maintained by the
International Paleofire Network at paleofire.org. Its last packaged release
(CRAN `GCD` 4.0.7, 2020) holds 935 sites and 174,980 samples, 185 sites of them
in Sahul. It is the source for most Sahul charcoal in the
[RPD](../rpd/README.md) and much of [SahulCHAR](../sahulchar/README.md). Its
data terms are non-commercial and no-derivatives, and the package is frozen,
so for Sahul fire history SahulCHAR and RPD are usually the better entry
points; use the GCD for lineage and for records the others altered.

## Contents

Counts are our own from the CRAN release ([profile](profile/gcd_profile.tsv);
site table exported to `derived/paleofiresites_4.0.7.tsv`).

| | Global | Sahul |
| --- | ---: | ---: |
| Sites | 935 | 185 |
| Samples | 174,980 | 15,332 |

- Sahul sites by region: Australia 152, New Guinea 24, Torres Strait 9. By
  GCD version of entry: GCD2 104, GCD1 43, GCD3 25, GCD4 13. The `country`
  field disagrees with coordinates for some (14 blank).
- Sahul samples: sieved 8,558, pollen-slide 6,774; concentration 9,627,
  influx 3,507, charcoal-to-pollen ratio 1,706, other 492; units led by
  particles >125 µm (3,356).
- Median oldest estimated age per Sahul site 9.3 ka; 38 sites reach 20 ka and
  18 reach 50 ka.
- The package also carries lookup tables (methods, 169 units, site and
  basin types), publications (714) and dates (4,904).

## Provenance and lineage

Founded by the Global Palaeofire Working Group (PAGES), which ended in 2019;
the International Paleofire Network now runs it, hosted by MSHE (Besançon) with
the Université de Montréal. Versions: GCD1 (Power et al. 2008, Access
database at NOAA), GCD2 (Daniau et al. 2012, 679 sites), GCD3 (Marlon et al.
2016, 736 sites, NOAA study 20042), GCD4 on CRAN (from 4.0.0 it mirrors the
online SQL database). The online database lists 1,249 sites today. Since 2022
the network has planned to recast it as a Neotoma constituent database
(number 47); one pilot site, in Siberia, had been loaded by October 2026.

## Structure

`paleofiresites` (one row per site: coordinates, elevation, site type, basin
size, preferred units, GCD version, update date) and `paleofiredata` (one row
per sample: `ID_SITE`, `DEPTH`, `EST_AGE`, `QUANTITY`, `UNIT`, `METHOD`,
`TYPE`), with code tables for methods (`SIEV`, `POLS`, ...), types (`CONC`,
`INFL`, `C0P0`, ...) and 169 units. Ages are estimated ages from each
record's original chronology. Two vegetation rasters (`PNV_*`) need the
`raster` package.

## Access

- **CRAN.** `GCD_4.0.7.tar.gz` (1.4 MB); `.rda` tables load in base R.
  Archived releases from 3.0.0 (2013) are listed in
  [cran-versions.tsv](cran-versions.tsv).
- **Online.** paleofire.org lists sites openly; the user manual describes CSV
  exports by site, region or all sites. Not tested here.
- **Mirror.** `deep-server:/data/paleodata/gcd/cran/raw/2026-10-22T0634Z_url/`
  and `derived/paleofiresites_4.0.7.tsv`. Index: [snapshots.tsv](snapshots.tsv).

## Strengths

- The reference lineage for charcoal records: most later compilations trace
  to it.
- Simple tables, easy to load; versions archived on CRAN since 2013.

## Weaknesses and pitfalls

- **Restrictive and conflicting terms.** Data are CC BY-NC-ND under the
  paleofire.org terms, with an "All Rights Reserved" footer, while the RPD
  republishes GCD-derived records under CC BY 4.0. Keep use non-commercial
  and cite the GCD until the conflict is resolved.
- **Frozen package, moving database.** CRAN has not been updated since 2020;
  the online database has grown by about 300 sites and is being migrated to
  Neotoma.
- **Stale documentation.** The package help says 881 sites and 134,269
  samples; the data hold 935 and 174,980.
- **Original chronologies only.** Ages come from each record's own model,
  built at different times with different calibration curves.
- **Heterogeneous measures and units** (169 unit codes), as in all charcoal
  compilations.

## Overlap with other sources

From [charcoal_overlap.py](../sahulchar/charcoal_overlap.py): 162 of the 185
Sahul GCD sites lie within about 2 km of an RPD entity and 119 within 2 km of
a SahulCHAR record (146 within 5 km). Five places are GCD-only.

## EPRP relevance

Lineage and cross-checking for Sahul fire-history work; direct use is limited
by the terms.

## Citation and terms

CC BY-NC-ND for the data (paleofire.org terms of use), with the acknowledgement
"Data were obtained from the Global Charcoal Database
(https://www.paleofire.org), and the work of the data contributors and the
Global Palaeofire Working Group is gratefully acknowledged." Cite the version
papers and the package.

## Verification log

- 2026-10-22, checked: CRAN 4.0.7 mirrored; tables loaded in R 4.6.1; counts
  above; release table of 14 versions.
- 2026-10-22, checked: Sahul overlap with RPD, SahulCHAR and Neotoma by
  location.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): terms of use,
  network history and hosting, version papers, online site count, Neotoma
  migration status, stale help text.
