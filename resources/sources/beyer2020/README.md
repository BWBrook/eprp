---
id: beyer2020
name: Beyer, Krapp and Manica (2020) high-resolution terrestrial climate, bioclimate and vegetation for the last 120,000 years
kind: deposit
status: frozen
last_update: "2021-06-24 (Figshare v4 adds monthly NPP)"
scope:
  taxa: ["not taxonomic: climate, bioclimate and potential vegetation fields"]
  time: "120 ka to present: 2 kyr steps to 22 ka, then 1 kyr steps (72 time slices)"
  space: "global land, 0.5 degrees, 59.75S to 89.75N (no Antarctica); exposed shelves included"
  record_unit: "grid cell at a time slice (monthly or annual fields)"
size:
  as_of: "Figshare 12293345 v4"
  time_slices: 72
  grid: "720 x 300 cells"
  bytes: 1436359299
access:
  tier: open
  licence: "CC-BY-4.0 (Figshare)"
  routes:
    - {type: figshare, url: "doi:10.6084/m9.figshare.12293345 (v1-v4)", state: "v4 latest", checked: 2026-10-22}
    - {type: osf, url: "https://osf.io/p86rt (MATLAB code, BIOME4 monthly NPP)", state: "code only, no DOI", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "four Figshare versions; v1-v3 share the same files; v4 adds the monthly NPP file. Index in figshare-versions.tsv"
mirror:
  path: deep-server:/data/paleodata/beyer2020
  policy: "latest version"
  state: "v4 mirrored, md5 verified against Figshare"
lineage:
  upstream:
    - "HadCM3 snapshot simulations (72), HadAM3H high-resolution runs (last 21 ka), CRU observations, Spratt and Lisiecki (2016) sea level on ETOPO1, ICE-6G ice sheets, BIOME4"
  downstream:
    - "Krapp et al. 2021 800 ka extension (krapp2021 entry); about 110 citing works, including Australian studies"
eprp_questions: []
citation:
  - "Beyer, R. M., Krapp, M. & Manica, A. (2020). High-resolution terrestrial climate, bioclimate and vegetation for the last 120,000 years. Scientific Data 7: 236. doi:10.1038/s41597-020-0552-1 (addendum: Scientific Data 8: 262, 2021, doi:10.1038/s41597-021-01051-1)"
  - "data: doi:10.6084/m9.figshare.12293345"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Beyer et al. (2020): climate and vegetation for the last 120,000 years

## Summary

A global, 0.5° reconstruction of monthly climate, 17 bioclimatic variables and
BIOME4 vegetation (biome, net primary production, leaf area index) for 72
time slices over the last 120,000 years, made by downscaling and
bias-correcting HadCM3 snapshot simulations. It is the standard continuous
climate forcing for Late Quaternary species-distribution, demographic and
human-dispersal models, and it covers exposed continental shelves, so Sahul is
drawn as one landmass at low sea level. Reach for it to drive Sahul
simulations through the last glacial cycle; respect its assumptions (equilibrium
snapshots, a single global sea-level curve, extrapolated shelf climate).

## Contents

Counts are our own ([profile](profile/beyer_profile.tsv)).

- *Files.* `LateQuaternary_Environment.nc` (1.33 GB: monthly temperature,
  precipitation, cloudiness, relative humidity, wind speed; annual minimum
  and maximum temperature, biome, NPP, LAI, BIO1 and BIO4–BIO19),
  `LateQuaternary_MonthlyNPP.nc` (103 MB: monthly NPP with its own annual
  biome, NPP and LAI), and short R, Python and MATLAB readers.
- *Grid.* 720 × 300 cells, 0.5°, latitudes 59.75°S to 89.75°N; time in years
  before present, −120,000 to 0.
- *Sahul.* Land area within our Sahul boxes (Australia, New Guinea, Torres
  Strait), from the data's own land mask:

| Time | Land area (million km²) | Gain on present |
| --- | ---: | ---: |
| 0 ka | 8.73 | – |
| 6 ka | 9.13 | 0.40 |
| 12 ka | 10.42 | 1.68 |
| 21 ka | 11.09 | 2.36 |
| 30 ka | 11.00 | 2.27 |
| 40 ka | 10.83 | 2.10 |
| 50 ka | 10.64 | 1.91 |
| 60 ka | 10.79 | 2.06 |
| 80 ka | 10.03 | 1.30 |
| 100 ka | 9.57 | 0.84 |
| 120 ka | 9.09 | 0.36 |

  Over land in the 110–155°E, 45°S–0 window, mean annual temperature (BIO1)
  is 21.9 °C at present and 19.2 °C at 21 ka; mean annual precipitation
  (BIO12) 822 and 712 mm.

## Provenance and lineage

Beyer, Krapp and Manica (Cambridge) took 72 HadCM3 snapshots (30-year means),
downscaled them with a "dynamic delta" method borrowing fine-scale patterns
from HadAM3H runs of the last 21 ka, then bias-corrected them against CRU
observations (1901–1930 for temperature, precipitation and cloud; 1961–1990
for humidity and wind). The land mask is Spratt and Lisiecki's (2016) global
mean sea level applied to modern ETOPO1 topography; ice comes from ICE-6G;
vegetation is BIOME4. Krapp et al. (2021) extended the approach to 800 ka at
1 kyr resolution ([krapp2021](../krapp2021/README.md)), and recommend this
dataset for the last glacial cycle.

## Structure

NetCDF-4 with dimensions `longitude`, `latitude`, `time` (72) and `month`
(12); four-dimensional monthly fields and three-dimensional annual fields;
non-land cells are NaN. Biome is categorical (BIOME4 codes, 0 water and 28
land ice).

## Access

- **Figshare.** Version 4 of article 12293345; downloads redirect to
  short-lived signed URLs, so resume by re-resolving the link.
- **Mirror.** `deep-server:/data/paleodata/beyer2020/raw/` (v4, md5 verified).
  Version index: [figshare-versions.tsv](figshare-versions.tsv). Read with
  `netCDF4` or `xarray` ([beyer_profile.py](beyer_profile.py) runs under `uv`).

## Strengths

- Continuous, global, monthly fields through the whole last glacial cycle at
  a resolution usable for regional models.
- Shelves included, so Sahul's connected landmass is represented.
- Simple, documented files, with matching vegetation fields.

## Weaknesses and pitfalls

- **Sea level is global and eustatic.** One global mean sea-level curve on
  modern topography: no glacio-isostatic or regional adjustment, no
  sedimentation or tectonics. Shorelines on the Sahul and Sunda shelves are
  approximate.
- **Shelf climate is extrapolated.** The bias correction over exposed shelf is
  extended from modern coasts by inverse-distance weighting.
- **Equilibrium snapshots.** Each slice is a 30-year mean of an equilibrium
  run; no sub-millennial variability or transient behaviour.
- **Metadata errors.** The longitude variable is labelled `degrees_north` and
  latitude `degrees_east`; the paper's labels for BIO4, BIO5 and BIO6 differ
  from the file's (the file follows the standard definitions). The `Source`
  attribute points to an older, empty Figshare article.
- **The two files disagree on vegetation.** The annual biome and NPP in the
  monthly-NPP file differ from the main file: in the Sahul window 195 cells
  change biome at present and 577 at 21 ka, and NPP correlates at only 0.96
  and 0.73. Use one file consistently.
- **Potential vegetation only**, with no land use.
- **No Australian validation site** is singled out in the evaluation.

## Overlap with other sources

- **Krapp et al. (2021)** extends the same model chain to 800 ka with a
  statistical emulator; prefer this dataset within 120 ka.
- **Sea-level and shelf area.** The land gain in our Sahul boxes at 21 ka
  (2.36 million km²) is consistent with Williams et al. (2018), who report
  Australia (without New Guinea) losing 2.12 million km² of land between the
  Last Glacial Maximum and 8 ka, but it is more than twice the "Sahul" shelf
  gain in Pico et al. (2020, 1.08 million km²), whose region is evidently
  narrower ([sahul-sealevel](../sahul-sealevel/README.md)).

## EPRP relevance

The default climate and vegetation forcing for Late Quaternary Sahul
simulation: megafauna and human demography, dispersal and range models, and
fire-climate analysis.

## Citation and terms

CC BY 4.0. Cite Beyer et al. (2020), the addendum if the monthly NPP is used,
and the Figshare DOI.

## Verification log

- 2026-10-22, checked: v4 mirrored with Figshare md5 verification; version
  index of four versions.
- 2026-10-22, checked: dimensions, variables, units (including the swapped
  coordinate labels) and time axis; Sahul land areas, BIO1 and BIO12 means;
  differences between the two files.
- 2026-10-22, checked: Pico et al. (2020) shelf-area values from its deposit.
- 2026-10-22, source claim (paper, via source scan, Claude Sonnet subagent):
  method, observational baselines, land mask and ice sources; Williams et al.
  (2018) land-area figures; citation count.
