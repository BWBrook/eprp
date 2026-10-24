---
id: palaeogeography
name: Palaeogeography — 26 plate models (the GPlates Plate Model Manager index), the PALEOMAP PaleoDEMs, and Wright et al. 2013 (PBDB's default model)
kind: compilation
status: active
last_update: "model index snapshot 2026-10-24 (newest model record, Alfonso et al. 2024, published 2026-07-20); PaleoDEMs 2018-08-01"
scope:
  taxa: ["not taxonomic: plate rotations, plate and coastline polygons, palaeotopography"]
  time: "Proterozoic to present (the index gives each model an age range, most from 0 Ma to between 140 and 1,800 Ma; Domeier 2014 250-410 Ma, Rodinia 530-1,100 Ma; rotation files hold poles to 3,000 Ma in five models); PaleoDEMs 0-540 Ma in 109 slices"
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
  licence: "CC BY 4.0 for 20 models (their Zenodo records) and the PaleoDEMs; not stated in the index for 6 models (Torsvik and Cocks 2017, Matthews et al. 2016 palaeomagnetic frame, Domeier 2014, Müller 2008, Golonka, Rodinia); Wright et al. 2013 CC BY 3.0 (snapshots.tsv); per-model licences in gplates-models-licences.tsv"
  routes:
    - {type: index, url: "https://repo.gplates.org/webdav/pmm/config/models.json", state: "GPlates Plate Model Manager index: 26 models (plus aliases), each with rotation and layer zips; snapshot 2026-10-24 mirrored with every file it lists", checked: 2026-10-24}
    - {type: zenodo, url: "https://doi.org/10.5281/zenodo.5348491", state: "PALEOMAP PaleoDEMs: 2 versions indexed; the newest (5460860, adding the 6-minute grids) mirrored; the notes cite the first (5348492)", checked: 2026-10-24}
    - {type: web, url: "https://doi.org/10.5194/bg-10-1529-2013", state: "Wright et al. 2013 supplement (rotation file, coastlines, continental regions, 2012 PBDB collection downloads)", checked: 2026-10-24}
    - {type: api, url: "https://gws.gplates.org", state: "GPlates Web Service: reconstructs points with these models on request; not used here", checked: 2026-10-24}
  api: "GPlates Plate Model Manager index; Zenodo; pygplates 1.0.0 (PyPI) for offline reconstruction"
versioning:
  replay: exact
  notes: "the index is unversioned and its file URLs carry no version: each snapshot is dated, and the index as fetched is kept in the snapshot and committed here (gplates-models-index-2026-10-24.json); its Version field names each model's Zenodo record or a date. The PaleoDEMs are DOI-versioned. The seafloor-age and spreading-rate grids that 10 of the 26 models list (hundreds to thousands of files each) are not mirrored"
mirror:
  path: deep-server:/data/paleodata/palaeogeography
  policy: "every model in the GPlates index, all layers; the PaleoDEMs; PBDB's default model"
  state: "three routes, 142 files (604 MB), each with a manifest; all verify"
lineage:
  upstream:
    - "EarthByte and collaborators' plate models (Seton et al. 2012; Matthews et al. 2016; Müller et al. 2016, 2019, 2022; Merdith et al. 2021; Cao et al. 2024 and others), PALEOMAP (Scotese and Wright 2018), Torsvik and Cocks 2017, Golonka, Domeier 2014, assembled by the GPlates team for gplately's Plate Model Manager"
  downstream:
    - "PBDB's palaeocoordinates (gplates = Wright et al. 2013, scotese = PALEOMAP, seton = Seton et al. 2012; matched closely under 100 Ma, less so for older collections); NSB's (Seton et al. 2012); Triton's (Matthews et al. 2016 mantle frame for non-Neptune rows, NSB's Seton coordinates for Neptune rows)"
eprp_questions: [Q-012, Q-027, Q-030, Q-035, Q-040, Q-049, B-005, Q-020]
citation:
  - "Each model's own paper and Zenodo record (gplates-models-licences.tsv; the index's URL and Version fields), for example Seton et al. 2012 (Earth-Sci. Rev., doi:10.1016/j.earscirev.2012.03.002), Matthews et al. 2016 (Glob. Planet. Change, doi:10.1016/j.gloplacha.2016.10.002), Merdith et al. 2021 (Earth-Sci. Rev., doi:10.1016/j.earscirev.2020.103477), Müller et al. 2019 (Tectonics, doi:10.1029/2018TC005462), Müller et al. 2022 (Solid Earth, doi:10.5194/se-13-1127-2022), Young et al. 2019 (Geosci. Front., doi:10.1016/j.gsf.2018.05.011), Torsvik and Cocks 2017 (Earth History and Palaeogeography, Cambridge University Press, doi:10.1017/9781316225523; online 2016)"
  - "Scotese, C. R. & Wright, N. (2018) PALEOMAP Paleodigital Elevation Models (PaleoDEMS) for the Phanerozoic. Zenodo, doi:10.5281/zenodo.5460860; Scotese, C. R. (2021) An Atlas of Phanerozoic Paleogeographic Maps: The Seas Come In and the Seas Go Out. Annu. Rev. Earth Planet. Sci. 49: 679-728, doi:10.1146/annurev-earth-081320-064052 (PBDB cites pages 669-718)"
  - "Wright, N., Zahirovic, S., Müller, R. D. & Seton, M. (2013) Towards community-driven paleogeographic reconstructions. Biogeosciences 10: 1529-1541, doi:10.5194/bg-10-1529-2013"
  - "Müller, R. D. et al. (2018) GPlates: building a virtual Earth through deep time. Geochem. Geophys. Geosyst., doi:10.1029/2018GC007584 (GPlates and pygplates)"
entry:
  created: 2026-10-24
  updated: 2026-10-24
  by: Claude (Opus 5.5, side session)
  reviewed: "2026-10-24, independent Claude Sonnet subagent; findings applied"
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

- **The mirror reproduces NSB and Triton, and PBDB for younger collections.**
  NSB's Seton coordinates are reproduced with the same plate on every row
  the mirror can reconstruct (582,746 of 582,770; 99.9% within 0.5°, at
  most 1.64°). Triton's non-Neptune rows with ages above 0 (249,912 rows)
  match Matthews et al. 2016 in its *mantle* reference frame (90.8% within
  0.5° of palaeolatitude, against 31.9% in the palaeomagnetic frame). PBDB's
  three models are matched by Wright et al. 2013, PALEOMAP and Seton et al.
  2012, with plate IDs agreeing on 99.5-100% of collections at every age.
  Under 100 Ma, 98-99.7% of collections are within 1° of palaeolatitude.
  From 100 Ma the match weakens: within 1° for 75-92% (Wright), 86-97%
  (PALEOMAP) and 81-88% (Seton), by age band. The plates agree, so the
  rotations differ; PBDB probably uses later versions of these rotation
  files (inference, unresolved). PBDB cites Scotese 2021 for its scotese
  model; the PALEOMAP rotation file here is the 2016 one.
- **Q-012 pools two models; the offset is under a degree, typically.**
  Q-012's exposure support pools Triton's Neptune rows (NSB's Seton
  coordinates) with its other rows (Matthews et al. 2016). Recomputing the
  Neptune rows the way Triton computed the others (mantle frame, whole-Ma
  ages) moves them a median 0.65° of palaeolatitude (95th percentile 3.7°,
  at most 5.6°; 108,062 rows). On NSB's own grid of hole positions every
  0.5 Myr (2,526 positions, 0-145 Ma), the same switch moves palaeolatitudes
  a median 2.2° (95th percentile 4.8°; 3.0° for 23-66 Ma, 3.1° for 100-145
  Ma); that grid weights every hole and age equally, not by samples. The
  profiler's reconstruction code can put all of Q-012's rows on one model.

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
them (170-410 Ma); those poles are identity or frozen copies of the last
in-range pole, that is, placeholders;
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
rotates it to the requested age relative to the model's anchor plate 0. A
point has no palaeoposition if its polygon begins after that age (young
ocean floor), if the age lies beyond the model's range in the index, or if
its plate has no pole at that age (pygplates would otherwise return the
identity rotation and leave the point where it is today).

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
  class holds the reconstruction rule above; it is a script, not an
  importable module.

## Strengths

- Every model the project's sources use, and 23 others, side by side with
  their licences, for Q-040's model uncertainty.
- Tested: the mirror reproduces NSB's coordinates and PBDB's for collections
  under 100 Ma, and identifies the frame Triton used.

## Weaknesses and pitfalls

- **PBDB's default "gplates" model is Wright et al. (2013)**, not the GPlates
  Web Service's default (Zahirovic et al. 2022) and not Matthews et al.
  (2016), whose plate IDs agree on 60.3% of PBDB collections and whose
  palaeolatitudes differ by a median 3.2° (collections within Matthews'
  410 Ma range).
- **The reference frame matters as much as the model.** Triton's
  palaeolatitudes (ages above 0) match Matthews et al. 2016's mantle frame
  (90.8% within 0.5°) but only 31.9% match its palaeomagnetic frame that
  closely (95th percentile difference 8.8°). Against NSB's Seton
  coordinates, the mantle frame differs by a median 2.2° and the
  palaeomagnetic by 3.2°.
- **PBDB's ages: probably the mid age rounded to whole Ma** (inference;
  PBDB's documentation does not say). Rounding brings the median
  palaeolatitude difference to 0.00-0.02° (unrounded 0.05-0.10°), though it
  does not improve the share within 0.5°. Every collection in the snapshot
  uses the mid age, so the early and late bases were not tested.
- **PBDB's older collections do not match closely** (above): from 100 Ma,
  3-25% are beyond 1° of palaeolatitude, depending on model and age, and
  more in position. Use the mirrored
  rotations as PBDB's models only for younger collections, until the
  rotation versions PBDB uses are identified.
- **Some positions differ by tens of degrees while palaeolatitudes agree**:
  2,748 of Triton's non-Neptune rows (ages above 0) and 1,447 Neptune rows
  (under Matthews) are over 10° apart in position, none over 5.6° in
  palaeolatitude. The palaeolongitudes disagree; the cause is not
  identified. Check palaeolongitude before using it.
- **Not every point is reconstructable.** Points on ocean floor younger than
  the age, outside a model's polygons or range, or on a plate with no pole at
  that age have no palaeoposition: 24 of NSB's rows under Seton et al. 2012,
  32,646 under Matthews et al. 2016; 760 of Triton's non-Neptune rows and
  277 Neptune rows under Matthews. Without the pole check, pygplates
  returns the identity rotation and the point stays at its present
  position.
- **Wright et al.'s supplement has no static polygons.** Its continental
  regions were used to assign plates, which reproduces PBDB's plate IDs on
  99.9% of collections.
- **The index is not versioned, and six models state no licence.** A later
  snapshot may hold different files under the same names; the committed copy
  of the index records what this one held.
- **Age grids are not mirrored.** Ten models list seafloor-age and
  spreading-rate grids by URL pattern (hundreds to thousands of files each).

## Overlap with other sources

- **PBDB** ([pbdb](../pbdb/README.md)): its collection snapshot carries
  three palaeocoordinate sets per collection; this entry holds the models
  behind them. Wright et al.'s supplement holds PBDB collection downloads
  of 2012.
- **NSB** ([nsb](../nsb/README.md)) and **Triton**
  ([triton](../triton/README.md)): the coordinates tested above.
- **Sahul sea level** ([sahul-sealevel](../sahul-sealevel/README.md)):
  complementary, not overlapping. It holds Sunda-Sahul palaeotopography and
  shelf series for the last glacial cycle; the PaleoDEMs' youngest slices
  are 0 and 5 Ma.

## EPRP relevance

Q-012's exposure test pools two plate models; this entry measures the
offset (a median 0.65° of palaeolatitude for the pooled Neptune rows, at
most 5.6°) and provides the means to remove it. Q-040 can draw its model
ensemble from the 26 models here. Q-027, Q-035 and Q-049 use palaeolatitude
or palaeogeography directly; Q-030 treats palaeogeography as a changing
confounder; B-005 and Q-020 are linked by inference (the 23 October survey
of the registers).

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
  to 12 for each model). Inputs: NSB 2023-06-05 (nsb.sqlite), Triton v4
  (triton_update_2023_pres.tsv.gz), PBDB snapshot 2026-10-23T0329Z.
- 2026-10-24, reviewed by an independent Claude Sonnet subagent. Applied:
  the age dependence of the PBDB match (age bands added); an age guard and
  a pole check in the reconstruction (24 NSB rows and old PBDB collections
  had been rotated by the identity); the Q-012 offset taken from Triton's
  pooled rows, not NSB's grid; Triton's frame test restricted to ages above
  0 and weighted by rows; the Scotese 2021 citation; licence sources; the
  rounding claim marked as inference; the overlap and question links. Its
  report that some Triton palaeolongitudes equal the palaeolatitude did not
  reproduce on this file.
- 2026-10-24, source claim: PBDB's three models and their references from
  PBDB's `colls/list` documentation; each model's licence from its Zenodo
  record (gplates-models-licences.tsv).
