---
id: sahul-sealevel
name: Sahul sea-level and palaeogeography pack (Pico et al. 2020; Spratt and Lisiecki 2016; Borreggine et al. 2026)
kind: deposit
status: frozen
last_update: "2024-01-29 (Borreggine deposit; paper 2026)"
scope:
  taxa: [not taxonomic; sea level, shelf exposure and palaeotopography]
  time: "global sea level 0-798 ka; Sahul and Sunda shelf exposure 0.1-122 ka; palaeotopography at 45-65 ka"
  space: "global (stack); Sahul and Sunda shelves (Pico); Sunda and northern Sahul to 18.15S (Borreggine)"
  record_unit: "time step (sea level, shelf area) or grid cell at a time slice (palaeotopography)"
size:
  as_of: "Zenodo 3959365, NOAA study 19982, Zenodo 8299571"
  pico_rows: 95
  spratt_rows: 799
access:
  tier: open
  licence: "CC-BY-4.0 (Pico and Borreggine deposits on Zenodo); Spratt and Lisiecki via NOAA WDS-Paleo (paper CC BY 3.0)"
  routes:
    - {type: zenodo, url: "doi:10.5281/zenodo.3959365 (Pico et al. 2020)", state: "single version", checked: 2026-10-22}
    - {type: noaa, url: "doi:10.25921/rd66-5820 (Spratt and Lisiecki 2016, NOAA study 19982)", state: "single file", checked: 2026-10-22}
    - {type: zenodo, url: "doi:10.5281/zenodo.8299571 (Borreggine et al.)", state: "single version, 7.5 GB", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "fixed deposits"
mirror:
  path: deep-server:/data/paleodata/sahul-sealevel
  policy: "the deposits whole"
  state: "pico2020-zenodo and spratt2016 mirrored; borreggine-zenodo downloading (7.5 GB)"
lineage:
  upstream:
    - "Pico: ICE-PC2 (Pico et al. 2017) and Waelbroeck et al. (2002) sea-level histories on modern topography"
    - "Spratt and Lisiecki: principal components of seven marine sea-level reconstructions"
    - "Borreggine: ICE-PC2 regional sea level with GIA, GMRT topography, MITgcm and CESM runs"
  downstream:
    - "Spratt and Lisiecki 2016 sets the land masks of Beyer et al. 2020 and Krapp et al. 2021"
eprp_questions: []
citation:
  - "Pico, T. et al. (2020). Paleoceanography and Paleoclimatology 35(8): e2020PA003998. doi:10.1029/2020PA003998"
  - "Spratt, R. M. & Lisiecki, L. E. (2016). A Late Pleistocene sea level stack. Climate of the Past 12: 1079-1092. doi:10.5194/cp-12-1079-2016"
  - "Borreggine, M. et al. (2026). Quaternary Science Reviews 381: 109950. doi:10.1016/j.quascirev.2026.109950; data doi:10.5281/zenodo.8299571"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Sahul sea level and palaeogeography pack

## Summary

Three open deposits that set how much of the Sahul shelf was land, and when:
the Spratt and Lisiecki (2016) global sea-level stack (the curve behind the
[Beyer 2020](../beyer2020/README.md) and [Krapp 2021](../krapp2021/README.md)
land masks), Pico et al.'s (2020) shelf-exposure series for Sahul and Sunda
under two ice histories, and Borreggine et al.'s palaeotopography and regional
sea level for 45–65 ka. Reach for them to set coastlines, land area and
connectivity in Late Quaternary Sahul models, and to test how sensitive a
result is to the sea-level history. None includes regional sea level for the
whole continent; for that, combine the global stack with modern bathymetry
(GEBCO or AusBathyTopo, listed in the backlog) and accept the eustatic
approximation.

## Contents

Counts are our own ([profile](profile/sealevel_profile.tsv)).

- **Spratt and Lisiecki (2016).** 799 rows, 0–798 ka at 1 kyr, two stacks
  (short and long principal component) with 1σ and 95% bounds. Short-stack
  sea level: −76.6 m at 14 ka, −113.0 m at 18 ka, −120.0 m at 21 ka, −130.0 m
  at 24 ka (the minimum), −105.8 m at 30 ka, −85.9 m at 40 ka, −68.3 m at
  50 ka, −84.7 m at 60 ka, +2.7 m at 120 ka; 1σ is 4–12 m.
- **Pico et al. (2020).** 95 rows, 0.1–122 ka: the increase in exposed
  continental shelf relative to today, for "Sahul" and Sunda, under ICE-PC2 and
  Waelbroeck et al. (2002). Sahul peaks at 1.10 million km² at 26 ka
  (Waelbroeck; 1.09 million under ICE-PC2), Sunda at 1.96 million.
- **Borreggine et al. (2026).** Six files (7.5 GB): `paleotopo.zip` (CSV
  grids at 45, 50, 55, 60 and 65 ka, about 0.07°, 84.9–155.07°E,
  18.15°S–18.15°N), MITgcm inputs and outputs, a migration-model package with
  ICE-PC2 regional sea level back to 126 ka (a glacio-isostatic product), and
  CESM output (6.8 GB). Details from the source scan; our mirror is still
  downloading.

## Provenance and lineage

Spratt and Lisiecki stacked seven independent sea-level reconstructions from
marine records into a principal-component stack; it is the sea-level input of
the Beyer and Krapp climate fields. Pico et al. computed shelf exposure from
two global ice histories on modern topography, to study the shelves' effect on
Indo-Pacific hydroclimate. Borreggine et al. built palaeotopography from
GMRT topography and ICE-PC2 regional sea level for ocean and climate modelling
of Sunda and northern Sahul during MIS 3 and 4.

## Structure

The stack is a NOAA template text file (comment lines with `#`, then a
tab-separated table). Pico's file is one small CSV. Borreggine's grids are CSV
matrices with separate latitude and longitude grids; the regional sea level is
a MATLAB file.

## Access

- **Mirror.** `deep-server:/data/paleodata/sahul-sealevel/`:
  `spratt2016/raw/2026-10-22T0643Z_url/`, `pico2020-zenodo/raw/3959365/`
  (md5 verified against Zenodo) and `borreggine-zenodo/` (in progress). Pico's
  series is also at NOAA (study 30794).

## Strengths

- The standard global stack with uncertainties, to 798 ka.
- Two ice histories side by side in Pico et al., showing how much the
  shelf-area series depends on the sea-level model (little at the glacial
  maximum, more in MIS 3: at 50 ka, 0.76 against 0.56 million km²).
- A glacio-isostatic regional sea-level product in the Borreggine deposit.

## Weaknesses and pitfalls

- **The stack is not zeroed at the present.** Short-stack sea level is +8.5 m
  (1σ 5.2) at 0 ka and 0 at 5 ka; subtract the offset you intend, and record
  it, before building a land mask.
- **Pico's "Sahul" is a narrower region than the continent's shelf.** At
  21 ka it gains 1.08 million km², while Beyer's land mask gains 2.36 million
  km² within our Sahul boxes, and Williams et al. (2018) report Australia
  alone losing 2.12 million km² of land between the Last Glacial Maximum and
  8 ka. The file does not define the region; do not use it as continental
  land area.
- **Eustatic only, except Borreggine.** The stack and Pico's areas apply a
  global curve to modern topography: no regional isostasy, sedimentation or
  tectonics.
- **Borreggine's domain stops at 18.15°S**, so it covers Sunda and northern
  Sahul, not the continent, and only five time slices.
- **Deposit dates mislead.** The Borreggine deposit is dated 2023 on Zenodo;
  its paper appeared in 2026.

## Overlap with other sources

The Spratt and Lisiecki stack is embedded in the Beyer (2020) and Krapp
(2021) land masks. Pico's ICE-PC2 history and Borreggine's regional sea level
come from the same ice model. Modern topography for palaeoshoreline work
(GEBCO_2026, AusBathyTopo 2026) is listed in the [backlog](../BACKLOG.md).

## EPRP relevance

Land area, coastline position and connectivity (Sahul–New Guinea, Bass
Strait, the Arafura plain) through the last glacial cycle, for megafauna,
human-dispersal and climate simulations, and for sensitivity tests on the
sea-level history.

## Citation and terms

CC BY 4.0 (Zenodo deposits); NOAA asks for the original publication, the
landing page and dataset DOIs, and the access date. Cite the three papers.

## Verification log

- 2026-10-22, checked: Pico and Spratt files mirrored (Pico md5 verified);
  rows, ranges, peaks and the values above from
  [sealevel_profile.py](sealevel_profile.py).
- 2026-10-22, checked: the comparison with Beyer's land mask
  ([beyer_profile.py](../beyer2020/beyer_profile.py)).
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): Borreggine
  file list, grid extent and contents; Williams et al. (2018) land areas;
  NOAA mirrors; paper details.
