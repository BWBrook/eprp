# Q-027 joint-support screen: where can the latitudinal gradient be estimated outside Europe and North America?

Owner: Claude | Built 11 October 2026; corrected the same day after [Codex's audit](../q027-support-audit/README.md) | Status: **a conservative presence screen, not an analysis of the gradient and not a power design**

Q-027 asks whether the latitudinal diversity gradient follows global climate
state. Its sharpest form is a dispute:
- Boag et al. 2021 find a tropical dip in warm intervals.
- Benson et al. 2025 argue that intense sampling in Europe and North America
  may have produced that apparent mid-latitude peak.

Before any power simulation or fit, this screen counts the stages that have
enough occupied cells in each palaeolatitude band *outside* Europe and North
America to estimate a gradient there at all.

## Rebuild

```bash
uv run data/q027-joint-support/build.py
```

The script pins pandas and numpy inline.
- **First run.** It fetches four members of the Benson et al. archive by HTTP
  range requests, without downloading the whole 1.55 GB zip; this took about
  8 minutes. The zipfile module checks each member's CRC32.
- **Later runs.** Members are cached in `data/raw/benson2025/` (git-ignored),
  and a run takes about 10 s.
- **Outputs (tracked):** [per_stage.tsv](per_stage.tsv) and
  [summary.tsv](summary.tsv).

## Source and contract

| Item | Value |
| --- | --- |
| Deposit | Zenodo record 15269137 (concept 10.5281/zenodo.15269136), "Data and code from publication: Marine animal diversity across latitudinal and temperature gradients during the Phanerozoic". CC BY 4.0. Single zip, 1,549,270,962 bytes, md5 6ca0d2b9995ce649ab138d3d6d23a34c (Zenodo's value; the full zip was not downloaded) |
| Companion Dryad deposit | 10.5061/dryad.6djh9w1bx (CC0, 79.5 MB). Anonymous file downloads return HTTP 401, so not used |
| Occurrence member | `input/marine_inverts/PBDB_CSV_data_downloads/2022-05-23-14-15-24/Animalia^Chordata_data.csv`: PBDB download of 23 May 2022, all animals except chordates, full field set. 712,947 rows. sha256 c5da9359fced2285e0d50f20626a1ab562738d80ff12cece2bb0af530746670d |
| Other members | `marine_regions.csv` (Close's region definitions), `country-codes_csv.csv`, `pbdb_time_int.csv` (PBDB intervals at download). sha256 values are printed by the script |
| PBDB query (from the archive's code) | `envtype=marine`, `pres=regular`, `idreso=lump_gensub`, `idqual=genus_certain`, `taxon_status=valid`, `pgm=scotese` palaeocoordinates |

What the archive does **not** contain: processed outputs. Benson et al.'s
pipeline reconstructs palaeocoordinates at bin midpoints and uses equal-area
dggridR cells with regional and coverage subsampling. Running it needs their
R environment (renv, R 4.1–4.2) and the climate-model fields (240 MB). This
screen does not run that pipeline.

## Method (deliberately light)

1. **Keep:**
   - genus-level or finer accepted names;
   - lithified or unrecorded lithification, excluding "unlithified", which is
     Benson et al.'s default;
   - occurrences with PBDB palaeocoordinates (Scotese model at the
     collection's age);
   - occurrences whose age range lies within one ICS stage (PBDB scale 1,
     level 5).

   382,266 occurrences in 95 stages remain.
2. **Cells.** Approximately equal-area cells: 5° latitude bands, with
   longitude width scaled by cos(latitude), about 555 km across. Benson et al.
   use dggridR cells of 100–2,000 km.
3. **Region.** "Europe + North America" uses Close's region table, joined on
   country names to ISO codes. Russia is in Asia, following that table; PBDB's
   `UK` is included.
   - Country codes are read as literal strings, so Namibia's `NA` is kept as
     a code.
   - The 822 retained records with an empty code are **unknown**: neither
     inside nor outside.
   - An occurrence counts as outside only when its country is known and not
     in Europe or North America.
   - The source study excludes whole cells by the modal region of their
     collections. This screen excludes occurrence rows instead, so 60
     stage × cell combinations hold both inside and outside occurrences
     (`cells_mixed`).
4. **Bands.** Absolute palaeolatitude bands of 0–20°, 20–40°, 40–60° and
   60–90°.
5. **Criterion.** A stage passes at threshold k if, outside Europe and North
   America, it has at least k occupied cells in the 0–20° band, at least k in
   20–40°, and at least k at 40° or more. Thresholds 3, 10 and 20 are
   screening levels. They are not power calculations, and cell counts are
   presence only, not coverage-standardised richness.

## Result

| Cells per band outside Europe + North America | Stages passing (of 95) | Palaeozoic | Mesozoic | Cenozoic |
| --- | --- | --- | --- | --- |
| ≥ 3 | 74 | 28/43 | 28/30 | 18/22 |
| ≥ 10 | 26 | 12/43 | 10/30 | 4/22 |
| ≥ 20 | 4 | 3/43 | 1/30 | 0/22 |

- **Corrections since first build.**
  - Era boundaries now come from the archived PBDB table, which puts the
    Induan (base 252.17 Ma) in the Mesozoic.
  - Unknown countries are no longer counted as outside. This cost one stage
    at k ≥ 10: the Ypresian, which goes from 30/10/12 to 28/9/12 cells.
- In the median stage, 42% of occupied cells contain any occurrence from
  Europe or North America. The cells overlap, so this is not a partition of
  coverage.
- **Warm intervals.** Several of the warmest intervals fail at 10 cells,
  because the mid-latitude band outside Europe and North America is thin:

  | Stage | Cells outside Europe + North America, 0–20° / 20–40° |
  | --- | --- |
  | Turonian | 15 / 8 |
  | Coniacian | 10 / 7 |
  | Santonian | 6 / 6 |
  | Lutetian | 22 / 6 |
  | Ypresian | 28 / 9 |
  | Toarcian | 7 / 12 |
  | Thanetian | 14 / 5 |

  Warm or transitional stages that pass at 10 are the Changhsingian and
  Induan, Aptian, Albian, Cenomanian and Burdigalian.
- **High latitudes.** The 60–90° band outside Europe and North America has 5
  or fewer cells in most Cenozoic stages.

**Inference (revised after Codex's audit).**

The first version said the test was possible "in only a handful of warm
stages". **That is withdrawn.** The count of 26 (27 before the fixes) is the
output of one conservative screen. It is neither a ceiling nor a count of
usable observations. Two of the screen's choices move it in opposite
directions (Codex's sensitivities, other choices held fixed):

- **Age rule raises it.** Full containment is stricter than the source's
  rule, which assigns an occurrence to the stage holding more than 50% of its
  age range. Under that rule:
  - 46 stages pass at k10;
  - the Turonian goes to 31/18/18 cells and the Lutetian to 31/13/14.

  The rule admits records with up to half their range in a neighbouring stage.
  That dilutes contrasts between adjacent stages with different climates, so
  it trades temporal precision for support. The estimator contract should
  record how much of each stage's support comes from such records.
- **Sample depth lowers it.** Requiring at least 2, 5 or 10 outside
  collections per cell leaves 14, 4 or 1 stages passing at k10. Occupancy
  says nothing about whether a cell can yield a coverage-standardised
  richness.

The combined effect of the two is unknown. Pooling hemispheres also matters:
at k10, only 3 stages pass using the north alone and 4 using the south alone.

**Next gate.** A support contract specific to the estimator comes before any
power simulation. It should use the source's:
- age rule and midpoint palaeocoordinates;
- dggridR cells;
- modal-region cell exclusion;
- coverage-quorum eligibility;
- region identity, so that latitude can be separated from region.

This screen cannot fix a power design.

## Limits

- PBDB palaeocoordinates come from the download (Scotese model at collection
  age), not Benson et al.'s midpoint reconstructions.
- Modern country is used as the "Europe + North America" proxy, as in the
  source study.
- Cells are 5° approximately equal-area cells, not dggridR; counts are
  occupancy, not richness.
- The 2022 download is fixed; current PBDB holdings differ. That is a
  publication-vintage choice, recorded here.
- Chordates, tetrapods and other separately downloaded groups in the archive
  are not included.
- Thresholds are arbitrary screening levels; what counts as enough cells
  depends on the estimator and is for the power gate to decide.

PBDB data are CC BY 4.0, and the Zenodo deposit is CC BY 4.0 (Benson, Close
et al. 2025). Only derived counts are tracked here.
