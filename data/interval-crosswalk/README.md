# Interval crosswalk: PhanDA, Song et al. 2021 and PBDB

Owner: Claude. Built 8 October 2026. Status: **descriptive capability probe**. This is
not an analytical forcing–response table. It was agreed in Correspondence 77
(messages 1129 and the reply to it) and serves candidates A–C in
[the disruption note](../../literature/2026-10-disruption-susceptibility.md).

The probe keeps each source's native intervals and maps them to named ICS stages.
It then computes overlaps in one reference frame: PBDB stage ages, ICS chart v2024/12,
PBDB ref:87596. No temperature, extinction or occurrence values are combined.

## Rebuild

```bash
uv run data/interval-crosswalk/build.py
```

The script runs from the repository root. It downloads any missing raw file into
the git-ignored `data/raw/` and records its URL, size and SHA-256 in
[sources.tsv](sources.tsv). PhanDA is pinned to commit `9f06c0d`; Song et al. to
Zenodo record 5027293. The PBDB interval list is a live service response, so
compare checksums before reusing outputs. Dependencies are pinned inline:
numpy, pandas, and `mat-io`, which reads PhanDA's MATLAB table objects.

## Sources and terms

| Source | What is used | Terms |
| --- | --- | --- |
| PhanDA, Judd et al. 2024, [EJJudd/PhanDA](https://github.com/EJJudd/PhanDA) at 9f06c0d | Stage slices and ages from `PhanDA_GMSTandCO2_percentiles.csv`; ensemble member structure from `PhanDA_GMST_ensemble.mat` | No licence declared in the repository. Raw files stay untracked. Tracked outputs hold only interval names, boundary ages and ensemble member counts and correlations, no temperatures |
| Song et al. 2021, [Zenodo 5027293](https://doi.org/10.5281/zenodo.5027293) | Stage-to-bin assignments parsed from `R code for extinction rate.R` | CC-BY-4.0 |
| PBDB intervals, [data1.2 service](https://paleobiodb.org/data1.2/intervals/list.json?scale=1) | ICS stage names and ages; the Pridoli epoch stands in for its missing stage | CC BY 4.0 |

## Outputs

- [intervals.tsv](intervals.tsv): every native interval from the three sources.
  Columns: source, interval, component ICS stages, native ages (Ma), reference-frame
  ages (Ma) and flags.
- [phanda_song_overlaps.tsv](phanda_song_overlaps.tsv): each PhanDA slice paired
  with each overlapping Song bin. Columns: shared Myr, fraction of slice, fraction
  of bin, relation, and the extinction event that the slice contains.
- [phanda_ensemble_members.tsv](phanda_ensemble_members.tsv): ensemble members per
  stage for each of PhanDA's 13 scenario columns.
- [phanda_ensemble_adjacency.tsv](phanda_ensemble_adjacency.tsv): for each pair of
  adjacent stages and each scenario, whether member counts match, and the
  correlation of member *k* across the pair where they do.

## Findings (8 October 2026)

**Direct observations from the build**

1. **Interval structure.**
   - Of PhanDA's 85 slices: 22 map one-to-one to a Song bin, 56 sit inside a
     longer Song bin, 2 straddle bins, and 5 Quaternary slices have no Song bin.
     Song bins 1–6 (Cambrian) have no PhanDA slice.
   - The straddling slices are Visean, which Song splits at 338.8 Ma, and
     Anisian/Olenekian. Song pairs Induan+Olenekian and Anisian+Ladinian, so the
     Early Triassic has no one-to-one match at the supplied resolution. A common
     coarsening through Induan–Ladinian is possible, at a large loss of temporal
     information (qualification from Codex, message 1155).
2. **Event stages occupy a small share of Song's bins (support mismatch).**

   | Event stage | Share of Song bin | Song bin |
   | --- | --- | --- |
   | Hirnantian | 22% | Katian+Hirnantian |
   | Changhsingian | 28% | Wuchiapingian+Changhsingian |
   | Turonian | 40% | Turonian+Coniacian+Santonian |
   | Toarcian | 71% | Toarcian+Aalenian |
   | PETM slice | 4% | Ypresian |

   Frasnian, Famennian, Capitanian/Wordian, Rhaetian, Cenomanian and Maastrichtian
   map one-to-one. Pairing PhanDA's event-stage forcing with Song's bin-level
   extinction therefore mixes supports. For the end-Ordovician and end-Permian,
   the bin is 3.5–4.6 times longer than the event stage. These shares measure
   support mismatch only. They are not attenuation factors: a maximum, a mean, a
   count and a rate each aggregate differently, and rates and quantiles cannot
   be combined without the underlying counts or model.
3. **Timescale versions differ materially.**
   - 15 of 83 single-name PhanDA slices (GTS2020) have a boundary more than
     0.5 Myr from PBDB's ICS 2024/12 value; 22 differ by more than 0.1 Myr.
   - The largest differences are 3.41 Myr at the Givetian/Frasnian boundary and
     2.31 Myr at the Roadian/Wordian boundary. Frasnian duration moves from
     7.8 Myr to 10.2 Myr, which changes any per-Myr rate there by about 30%.
   - Song's proxy sheets label ages "2012", and its occurrence ages came from PBDB
     in January 2021. That makes a third timescale version.
4. **PhanDA ensemble members are not joint trajectories by construction.**
   - Members per stage vary within each scenario (65–2,880 in Scenario01).
     ScenarioAll has 17,280 or 34,560 members per stage.
   - Adjacent stages have equal member counts in only 24–67 of 84 pairs, depending
     on the scenario.
   - Where counts are equal, member *k* is correlated across stages: median
     r = 0.60–0.82 by scenario. Members are not sorted within a stage: in three Scenario01 stages checked,
     53–63% of consecutive steps are non-decreasing.
   - The percentile CSV's median matches the ensemble median (checked for the Aalenian).
5. **The Song et al. deposit cannot reproduce the bins as deposited.**
   - The script reads `pbdb-dm.csv` and a local `bindata2.txt` of bin ages, and
     neither is deposited.
   - It writes `extinction-result.csv` but reads back `extinction-result.csv.csv`.
   - "Stage 4" is listed twice in bin 4, and the Cambrian Wuliuan stage is in no bin.
   - The Visean split (lines 39–40) indexes with `which(...) && (...)` and computes
     the midpoint as `(earlyage+earlyage)/2`. Under R 4.6.1 this line stops with
     `'length = 2' in coercion to 'logical(1)'`, tested on a toy vector.

**Inference, unverified**

- *PhanDA ensemble.* The cross-stage correlation probably reflects members
  indexed by shared prior or scenario structure, not posterior trajectories.
  Differencing members by index is therefore unjustified until the assimilation
  design (Judd et al. 2024 Methods; PhanDA code) is read. Differencing marginal
  percentiles is also wrong. An interim ΔGMST bound would treat adjacent stages as
  independent draws and report how much of the interval that assumption drives.
- *Song et al. Visean code.* Before R 4.2 the documented behaviour of `&&` was to
  use only the first element of each side. The subscript would then be a single
  TRUE, FALSE or NA, set by the first data row. TRUE recycles to every row; FALSE
  or NA assigns nothing. What the published bins actually contained cannot be
  established from the deposit. This is a reproducibility observation, not
  evidence that the published rates are wrong.

## Limits

- Reference-frame overlaps use PBDB stage ages throughout. Two exceptions use
  native ages: the PhanDA PETM slice (GTS2020, 56.0–55.7 Ma) and Song's Visean
  split at 338.8 Ma, whose timescale frame is not stated.
- Song bin ages are reconstructed from stage composition, because the bin-age
  table is not deposited.
- Which 45 of the 56 Song bins entered the threshold analysis is not identified
  in the deposit.
- No occurrence-level data or proxy values were joined.
