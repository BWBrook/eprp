---
id: krapp2021
name: Krapp et al. (2021) statistics-based reconstruction of global terrestrial climate for the last 800,000 years
kind: deposit
status: frozen
last_update: "2023-11-26 (OSF project last modified)"
scope:
  taxa: ["not taxonomic: climate, bioclimate, vegetation and land/ice/ocean masks"]
  time: "800 ka to present at 1 kyr steps (800 time slices)"
  space: "global, 0.5 degrees on the CRU TS 4.04 grid, including Antarctica"
  record_unit: "grid cell at a time slice (monthly or annual fields)"
size:
  as_of: "OSF project 8n43x, retrieved 2026-10-22"
  files: 122
  bytes: 11812845398
  time_slices: 800
access:
  tier: open
  licence: "CC-BY-4.0 (OSF project licence)"
  routes:
    - {type: osf, url: "doi:10.17605/OSF.IO/8N43X (https://osf.io/8n43x)", state: "122 files, per-file downloads with md5", checked: 2026-10-22}
  api: "OSF API for file listings"
versioning:
  replay: partial
  notes: "no versioned releases; files corrected in place after reported issues (known_issues.md). Our snapshot's md5 sums are in osf-files.tsv"
mirror:
  path: deep-server:/data/paleodata/krapp2021
  policy: "the whole OSF project"
  state: "osf/raw/2026-10-22T0703Z_url (122 files, 11.8 GB); every file's size and md5 equal OSF's"
lineage:
  upstream:
    - "72 HadCM3 snapshots (as in Beyer et al. 2020), CO2 from EPICA, orbital parameters, ice and sea level from ICE-6G (0-122 ka), Ganopolski and Calov (2011, 123-799 ka) and Spratt and Lisiecki (2016); CRU TS 4.04 for bias correction; BIOME4"
  downstream:
    - "about 76 citing works (source scan)"
eprp_questions: []
citation:
  - "Krapp, M., Beyer, R. M., Edmundson, S. L., Valdes, P. J. & Manica, A. (2021). A statistics-based reconstruction of high-resolution global terrestrial climate for the last 800,000 years. Scientific Data 8: 228. doi:10.1038/s41597-021-01009-3"
  - "data: doi:10.17605/OSF.IO/8N43X"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Krapp et al. (2021): terrestrial climate for the last 800,000 years

## Summary

A global, 0.5° reconstruction of monthly and annual temperature,
precipitation and cloud cover, 17 bioclimatic variables, BIOME4 vegetation
and a land/ice/ocean mask at every 1,000 years for the last 800,000 years. It
extends [Beyer et al. (2020)](../beyer2020/README.md) beyond the last glacial
cycle with a statistical emulator of the same HadCM3 simulations. Reach for
it when a Sahul model needs climate through several glacial cycles, for
example to place human arrival or megafaunal history in a longer context. The
authors recommend Beyer et al. (2020) within the last 120,000 years; the
Holocene land masks of both are too far seaward.

## Contents

Counts are our own ([profile](profile/krapp_profile.tsv)).

- *Files.* 122 files, 11.8 GB: annual, monthly, minimum and maximum
  temperature; annual and monthly precipitation and total cloud cover;
  `bio01` and `bio04`–`bio19`; BIOME4 output (annual and monthly); the
  land/ice/ocean mask (`icesheets_000-800_cru.nc`); the regression
  coefficients (41 files); a proxy comparison spreadsheet; example scripts;
  the code, its inputs and BIOME4; `known_issues.md`.
- *Grid.* 720 × 360 cells, 0.5°, 800 time slices (−799,000 to 0 years).
- *Mask.* 0 ocean, 1 land, 2 ice. Land within our Sahul boxes (Australia
  45–10.6°S, New Guinea, Torres Strait), in million km²:

| Time | Land | Time | Land |
| --- | ---: | --- | ---: |
| 0 ka | 8.63 | 12 ka | 10.53 |
| 2 ka | 8.78 | 21 ka | 11.19 |
| 3 ka | 8.91 | 60 ka | 10.88 |
| 6 ka | 9.16 | 120 ka | 9.13 |
| 8 ka | 9.36 | 400 ka | 8.49 |
| 10 ka | 9.85 | 799 ka | 11.01 |

  New Guinea is joined to Australia in the mask at 6 ka and earlier slices
  tested (except the 400 ka interglacial), and separate at 0–3 ka.
- *Sahul window means over land (110–155°E, 45°S–0).* Annual temperature
  295.3 K (22.1 °C) at present and 291.8 K (18.6 °C) at 21 ka; precipitation
  843 and 764 mm a year.

## Provenance and lineage

Krapp, Beyer, Edmundson, Valdes and Manica regressed,
cell by cell, the 72 HadCM3 snapshots of the last 120,000 years on CO2, three
orbital terms and a surface-type mask, then drove the regression with 800,000
years of forcing (EPICA CO2; ice from ICE-6G to 122 ka and from Ganopolski and
Calov's model beyond; sea level from Spratt and Lisiecki 2016), bias-corrected
and downscaled to the CRU grid. Vegetation is BIOME4. The mask's own metadata
names these sources.

## Structure

NetCDF-4 (CF-1.6), one variable per file with dimensions `time`, `lat`,
`lon`; time in years since 0000-01-01, negative for the past. Temperature is
in kelvin and precipitation in mm a year, but the variables carry no `units`
attribute. Monthly fields are one file per month.

## Access

- **OSF.** Per-file downloads (`https://osf.io/download/<id>/`), listed with
  sizes and md5 in [osf-files.tsv](osf-files.tsv).
- **Mirror.** `deep-server:/data/paleodata/krapp2021/osf/raw/2026-10-22T0703Z_url/`
  with OSF paths flattened (`data/temperature/x.nc` is
  `data__temperature__x.nc`). Index: [snapshots.tsv](snapshots.tsv). Read with
  `netCDF4` ([krapp_profile.py](krapp_profile.py) runs under `uv` and checks
  every md5).

## Strengths

- 800,000 years at 1 kyr resolution, globally, with consistent bioclimatic and
  vegetation fields.
- Built on the same simulations as Beyer et al. (2020), so the two can be
  joined at 120 ka.
- Regression coefficients and code published, so the emulator can be rerun
  with other forcings.

## Weaknesses and pitfalls

- **Statistical emulation.** Climate beyond 120 ka is extrapolated from a
  regression fitted to the last glacial cycle; non-analogue states are not
  simulated.
- **Holocene coastlines too far seaward.** As in Beyer et al. (2020), the mask
  adds 0.53 million km² of Sahul land at 6 ka and keeps New Guinea joined to
  Australia then; do not use the Holocene masks for coastline questions.
- **Known issues** (`known_issues.md`). Annual precipitation holds a
  placeholder of 15000 over ice sheets and masked lakes (treat as missing;
  none fall in the Sahul window at the times we checked). BIO15 was computed
  as a standard deviation instead of a coefficient of variation; the note says
  it has been corrected, so files fetched before May 2022 differ.
- **No units attributes**, and units differ from Beyer et al. (kelvin and mm a
  year here; °C and mm a month there).
- **Equilibrium climate at 1 kyr steps**: no sub-millennial variability.

## Overlap with other sources

- **Beyer et al. (2020).** Same simulations; at 21 ka Krapp's mask gives 2.56
  million km² of extra Sahul land against Beyer's 2.36 million (different
  masks and grids). Prefer Beyer within 120 ka.
- **Sea level.** The mask's sea level is the Spratt and Lisiecki (2016) stack
  ([sahul-sealevel](../sahul-sealevel/README.md)).

## EPRP relevance

Long-run climate and vegetation forcing for Sahul simulations that span
several glacial cycles, and context for deep Quaternary records such as the
Naracoorte caves.

## Citation and terms

CC BY 4.0. Cite Krapp et al. (2021) and the OSF DOI.

## Verification log

- 2026-10-22, checked ([krapp_profile.py](krapp_profile.py)): all 122 files'
  sizes and md5 sums equal OSF's; mask values and Sahul land areas;
  connectivity; temperature and precipitation means; no 15000 placeholders in
  the Sahul window at 0, 21 and 120 ka; `known_issues.md` read.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): method,
  forcing sources, the authors' recommendation of Beyer et al. within 120 ka,
  citation count.
