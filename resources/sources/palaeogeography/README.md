---
id: palaeogeography
name: Palaeogeography — 26 plate models (the GPlates Plate Model Manager index), the PALEOMAP PaleoDEMs, and Wright et al. 2013 (PBDB's default model)
kind: compilation
status: active
last_update: "model index snapshot 2026-10-24 (newest model record, Alfonso et al. 2024, published 2026-07-20); PaleoDEMs 2018-08-01"
scope:
  taxa: ["not taxonomic: plate rotations, plate and coastline polygons, palaeotopography"]
  time: "Proterozoic to present (the index gives each model a range of 0-140 to 0-1,800 Ma; rotation files hold poles to 3,000 Ma in five models); PaleoDEMs 0-540 Ma in 109 slices"
  space: "global"
  record_unit: "a total reconstruction pole (plate, time, rotation); a static plate polygon; a palaeotopography grid at one time slice"
size:
  as_of: "2026-10-24"
  plate_models: 26
  paleodem_time_slices: 109
  raw_files: 142
  mirrored_bytes: 604291602
access:
  tier: open
  licence: "CC BY 4.0 for 20 models (their Zenodo records) and the PaleoDEMs; not stated in the index for 6 models (Torsvik and Cocks 2017, Matthews et al. 2016 palaeomagnetic frame, Domeier 2014, Müller 2008, Golonka, Rodinia); Wright et al. 2013 CC BY 3.0 (gplates-models-licences.tsv)"
  routes:
    - {type: index, url: "https://repo.gplates.org/webdav/pmm/config/models.json", state: "GPlates Plate Model Manager index: 26 models (plus aliases), each with rotation and layer zips; snapshot 2026-10-24 mirrored with every file it lists", checked: 2026-10-24}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.5348491", state: "PALEOMAP PaleoDEMs: 2 versions indexed; the newest (5460860, adding the 6-minute grids) mirrored; the notes cite the first (5348492)", checked: 2026-10-24}
    - {type: web, url: "https://doi.org/10.5194/bg-10-1529-2013", state: "Wright et al. 2013 supplement (rotation file, coastlines, continental regions, 2012 PBDB collection downloads)", checked: 2026-10-24}
    - {type: api, url: "https://gws.gplates.org", state: "GPlates Web Service: reconstructs points with these models on request; not used here", checked: 2026-10-24}
  api: "GPlates Plate Model Manager index; Zenodo; pygplates 1.0.0 (PyPI) for offline reconstruction"
versioning:
  replay: exact
  notes: "the index is unversioned and its file URLs carry no version: each snapshot is dated, and the index as fetched is kept in the snapshot and committed here (gplates-models-index-2026-10-24.json); its Version field names each model's Zenodo record or a date. The PaleoDEMs are DOI-versioned. Age grids and spreading-rate grids (thousands of files per model) are not mirrored"
mirror:
  path: deep-server:/data/paleodata/palaeogeography
  policy: "every model in the GPlates index, all layers; the PaleoDEMs; PBDB's default model"
  state: "three routes, 142 files (604 MB), each with a manifest; all verify"
lineage:
  upstream:
    - "EarthByte and collaborators' plate models (Seton et al. 2012; Matthews et al. 2016; Müller et al. 2016, 2019, 2022; Merdith et al. 2021; Cao et al. 2024 and others), PALEOMAP (Scotese and Wright 2018), Torsvik and Cocks 2017, Golonka, Domeier 2014, assembled by the GPlates team for gplately's Plate Model Manager"
  downstream:
    - "PBDB's palaeocoordinates (gplates = Wright et al. 2013, scotese = PALEOMAP, seton = Seton et al. 2012); NSB's (Seton et al. 2012); Triton's (Matthews et al. 2016 mantle frame for non-Neptune rows, NSB's Seton coordinates for Neptune rows)"
eprp_questions: [Q-012, Q-027, Q-030, Q-035, Q-040, Q-049, B-005, Q-020]
citation:
  - "Each model's own paper and Zenodo record (gplates-models-licences.tsv; the index's URL and Version fields), for example Seton et al. 2012 (Earth-Sci. Rev., doi:10.1016/j.earscirev.2012.03.002), Matthews et al. 2016 (Glob. Planet. Change, doi:10.1016/j.gloplacha.2016.10.002), Merdith et al. 2021 (Earth-Sci. Rev., doi:10.1016/j.earscirev.2020.103477), Müller et al. 2019 (Tectonics, doi:10.1029/2018TC005462), Müller et al. 2022 (Solid Earth, doi:10.5194/se-13-1127-2022), Young et al. 2019 (Geosci. Front., doi:10.1016/j.gsf.2018.05.011), Torsvik and Cocks 2017 (Earth History and Palaeogeography, Cambridge University Press, doi:10.1017/9781316225523; online 2016)"
  - "Scotese, C. R. & Wright, N. (2018) PALEOMAP Paleodigital Elevation Models (PaleoDEMS) for the Phanerozoic. Zenodo, doi:10.5281/zenodo.5460860; Scotese, C. R. (2021) Annu. Rev. Earth Planet. Sci. 49: 669-718, doi:10.1146/annurev-earth-081320-064052"
  - "Wright, N., Zahirovic, S., Müller, R. D. & Seton, M. (2013) Towards community-driven paleogeographic reconstructions. Biogeosciences 10: 1529-1541, doi:10.5194/bg-10-1529-2013"
  - "Müller, R. D. et al. (2018) GPlates: building a virtual Earth through deep time. Geochem. Geophys. Geosyst., doi:10.1029/2018GC007584 (GPlates and pygplates)"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "not yet"
---

# Palaeogeography: plate models and palaeotopography

## Summary

Palaeolatitude enters Q-012's exposure test, Q-027's latitudinal cells,
Q-035 and Q-049, and Q-040 asks for uncertainty to be propagated across
plate models. The sources the project uses compute palaeocoordinates with
different models. NSB uses Seton et al. (2012), Triton uses Matthews et al.
(2016) except for its Neptune rows, which carry NSB's Seton coordinates, and
PBDB offers three models. This entry mirrors the models themselves: every
model in the GPlates Plate Model Manager index (26 models, all layers), the
PALEOMAP PaleoDEMs, and the supplement of Wright et al. (2013), PBDB's
default. A profiler reconstructs points offline with pygplates and tests the
mirror against the coordinates NSB, Triton and PBDB publish.

**Findings.**

- **The mirror reproduces the sources.** NSB's 582,770 Seton coordinates
  are reproduced with the same plate on every row (median distance 0.00°,
  99.9% within 0.5°). Triton's non-Neptune rows match Matthews et al. 2016
  in its *mantle* reference frame (95.7% within 0.5° of palaeolatitude;
  57.9% in the palaeomagnetic frame). PBDB's three models are reproduced by
  Wright et al. 2013, PALEOMAP and Seton et al. 2012 at whole-Ma ages, with
  plate IDs agreeing on 99.9-100% of collections and median palaeolatitude
  differences of 0.00-0.02°; 5-10% of collections differ by more than 1°.
- **Mixing models moves palaeolatitudes by degrees (Q-012).** NSB's holes,
  re-reconstructed under Matthews et al. 2016 (mantle frame), move a median
  2.2° in palaeolatitude (95th percentile 4.8°); 1.0° for 0-23 Ma, 3.0° for
  23-66 Ma and 2.3° for 66-145 Ma. Triton's Neptune rows would move a median
  0.9° (95th percentile 3.8°, at most 5.5°) if computed like its other rows.
  Q-012's exposure support pools both models (its README says so). The
  profiler's reconstruction code can put all of them on one model.

## Contents

| Route | Content | Files | Size |
| --- | --- | ---: | ---: |
| `gplates-models` | the GPlates Plate Model Manager index (`models.json`) and, for each of its 26 models, the rotation zip and layer zips (static polygons, coastlines, continental polygons, topologies, COBs and others, as the index lists them) | 135 | 141.8 MB |
| `paleomap-paleodem` | Scotese and Wright 2018: PaleoDEMs for 109 time slices (0-540 Ma) at 1° and 6′ (netCDF) and as lon-lat-elevation CSV, the PALEOMAP PaleoAtlases (PDF), the PaleoAtlas for GPlates (with PALEOMAP's rotation file), and the documentation | 6 | 414.7 MB |
| `wright2013-supplement` | Wright et al. 2013: the Phanerozoic EarthByte rotation file, coastlines and continental regions (GPlates), and PBDB collection downloads of the time (carbonate marine, siliciclastic marine, terrestrial and general, with references) and sample shapefiles | 1 | 47.8 MB |

The model inventory ([profile](profile/palaeogeography_profile.tsv)) gives
each model's rotation files, poles, moving plates, oldest pole and static
polygons; [gplates-models-licences.tsv](gplates-models-licences.tsv) gives
each model's Zenodo record and licence. Five models have poles to 3,000 Ma
(Alfonso et al. 2024, Clennett et al. 2020 on Müller 2019, Müller et al.
2019, Zahirovic et al. 2016 and 2022), far beyond the ranges the index gives
them (170-410 Ma), so those poles are presumably placeholders (inference);
Cao et al. 2024 and Müller et al. 2025 have poles to 2,100 Ma and an index
range of 1,800 Ma.

## Provenance and lineage

The GPlates team maintains the index for gplately's Plate Model Manager; it
points at copies of each model's files on its own server, with each model's
DOI or source page. The files were fetched from those copies, not from the
models' Zenodo records, so they are the files gplately and the GPlates Web
Service use. The PaleoDEMs come from Zenodo. Wright et al.'s files are their
*Biogeosciences* supplement.

## Structure

Rotation files (`.rot`, `.grot`) give finite poles by moving plate, time and
fixed plate. Polygons are GPML or shapefiles. PaleoDEMs are netCDF grids and
CSV tables of longitude, latitude and elevation. The profiler,
[palaeogeography_profile.py](palaeogeography_profile.py), assigns each
present-day point the plate of the static polygon it falls in (at 0 Ma) and
rotates it to the requested age relative to the model's anchor plate 0; a
point whose polygon begins after that age (young ocean floor) has no
palaeoposition.

## Access

- **Mirror.** `deep-server:/data/paleodata/palaeogeography/<route>/raw/<version>/`
  with manifests; [snapshots.tsv](snapshots.tsv) lists them. Model files are
  named `<model>__<layer>.zip`.
- **Refresh.** [palaeogeography_snapshot.sh](palaeogeography_snapshot.sh)
  `[models] [paleodem] [wright2013]`; [pmm_specs.py](pmm_specs.py) turns the
  index into the file list. Each `models` run is a new dated snapshot.
- **Reconstruct.** `uv run palaeogeography_profile.py MODELS_RAW WRIGHT_RAW
  PALEODEM_RAW NSB_SQLITE TRITON_TSV_GZ PBDB_GLOBAL_RAW OUT_TSV`, on
  deep-server (pygplates 1.0.0 from PyPI; Python 3.10-3.13). Its `Model`
  class reconstructs any point under any mirrored model.

## Strengths

- Every model the project's sources use, and twenty others, side by side
  with their licences, for Q-040's model uncertainty.
- Tested: the mirror reproduces NSB's and PBDB's coordinates, and identifies
  the frame Triton used.

## Weaknesses and pitfalls

- **PBDB's default "gplates" model is Wright et al. (2013)**, not the GPlates
  Web Service's default (Zahirovic et al. 2022) and not Matthews et al.
  (2016), whose plate IDs agree on only 61.7% of PBDB collections and whose
  palaeolatitudes differ by a median 4.1°.
- **The reference frame matters as much as the model.** Triton's
  palaeolatitudes match Matthews et al. 2016's mantle frame (95.7% within
  0.5°) but only 57.9% of them match its palaeomagnetic frame that closely
  (95th percentile difference 8.4°). Against NSB's Seton coordinates, the
  mantle frame differs by a median 2.2° and the palaeomagnetic by 3.2°.
- **PBDB reconstructs at whole-Ma ages.** Rounding the collection's mid age
  brings the median difference to 0.00-0.02°; unrounded, it is 0.05-0.10°.
  The 5-10% of collections beyond 1° are not explained here.
- **Some positions differ by tens of degrees while palaeolatitudes agree**:
  24 of Triton's non-Neptune rows and 189 Neptune rows (under Matthews) are
  over 10° apart in position, none over 5.5° in palaeolatitude. Palaeolongitude
  is the thing to check before using it.
- **Not every point is reconstructable.** Points on ocean floor younger than
  the age, or outside a model's polygons, have no palaeoposition (32,646 of
  NSB's rows under Matthews et al. 2016; 107 of Triton's Neptune rows).
- **Wright et al.'s supplement has no static polygons.** Its continental
  regions were used to assign plates, which reproduces PBDB's plate IDs on
  99.9% of collections.
- **The index is not versioned, and six models state no licence.** A later
  snapshot may hold different files under the same names; the committed copy
  of the index records what this one held.
- **Age grids are not mirrored.** The index lists seafloor-age and
  spreading-rate grids by URL pattern (thousands of files per model).

## Overlap with other sources

- **PBDB** ([pbdb](../pbdb/README.md)): its collection snapshot carries
  three palaeocoordinate sets per collection; this entry holds the models
  behind them. Wright et al.'s supplement holds PBDB collection downloads
  of 2012.
- **NSB** ([nsb](../nsb/README.md)) and **Triton**
  ([triton](../triton/README.md)): the coordinates tested above.
- **Climate forcing** ([climate-forcing](../climate-forcing/README.md)):
  Scotese et al.'s 2021 temperature maps use the PALEOMAP frame.
- **Sahul sea level** ([sahul-sealevel](../sahul-sealevel/README.md)): the
  Australian palaeotopography and shelf series, at higher resolution for the
  last glacial cycle.

## EPRP relevance

Q-012's exposure test pools two plate models; this entry measures the
offset (a median 2.2° of palaeolatitude for NSB's holes) and provides the
means to remove it. Q-040 can draw its model ensemble from the 26 models
here. Q-027, Q-035 and Q-049 use palaeolatitude or palaeogeography directly.

## Citation and terms

Cite each model's paper and Zenodo record (front matter;
[gplates-models-licences.tsv](gplates-models-licences.tsv)), the PaleoDEMs
by their DOI, and Wright et al. (2013) for PBDB's default model. Six models
state no licence in the index; check their sources before reuse.

## Verification log

- 2026-10-24, checked: the index (26 models, 134 files) and every file it
  lists mirrored as one dated snapshot with
  [palaeogeography_snapshot.sh](palaeogeography_snapshot.sh); the PaleoDEMs
  verified against Zenodo's md5; Wright et al.'s supplement fetched;
  `data_mirror.py verify` passes on all three.
- 2026-10-24, checked: [palaeogeography_profile.py](palaeogeography_profile.py)
  ([output](profile/palaeogeography_profile.tsv)) on deep-server: the
  inventory, and the NSB, Triton and PBDB tests (PBDB: one collection in 6
  to 12 for each model).
- 2026-10-24, source claim: PBDB's three models and their references from
  PBDB's `colls/list` documentation; each model's licence from its Zenodo
  record (gplates-models-licences.tsv).
