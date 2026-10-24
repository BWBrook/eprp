# Data products found by the software scans

The four software scans of 23 October 2026 met data products that belong in
the [data source catalogue](../sources/README.md), not here. They are listed
for that catalogue's owner; nothing below has been fetched or profiled. Facts
are the scans' (`verified` = a scan read the page; otherwise unchecked). The
right-hand column compares with the data catalogue's entries and backlog as
of 23 October.

| Product | What the scans found | Data catalogue |
| --- | --- | --- |
| PBDB data archives | Archives fix content, format and vocabulary at creation; a DOI can be requested and then the archive is immutable (`archives_doc.html`, verified). Who approves DOIs is not stated. `chronosphere`'s registry lists 1,171 dated PBDB occurrence snapshots with Zenodo DOIs, 2019-11-22 to 2026-10-18 (checked; [Detail withheld pending disclosure to the data custodian.] | `pbdb` entry exists; archives and `chronosphere` snapshots bear on its replay section and on Q-045 ([LEADS](LEADS.md) L-005) |
| NSB Zenodo backups | Record 10062080: PostgreSQL, SQLite and denormalised CSV, versions 2020-12-15 and 2023-06-05, CC BY 4.0 (verified) | `nsb` entry exists |
| NOW (New and Old Worlds) | Cenozoic mammal localities; citation 10.5281/zenodo.4268068; CC BY 4.0; no API; outage notice from 2026-10-21 (verified) | Not catalogued |
| Geobiodiversity Database | Section-based Cambrian–Triassic data, CONOP export; ESSD 10.5194/essd-12-3443-2020 (verified); access status uncertain | Not catalogued |
| BioDeepTime | Assemblage time series, Zenodo 8154672; licence not stated; `chronosphere` can fetch it | Named in the capability inventory; not catalogued |
| `sepkoski` (CRAN data package) | Sepkoski 2002 genera as an R data package, 0.0.1, GPL (≥ 3) (verified) | `classic-compendia` covers Sepkoski 2002 and Peters' port |
| FosSahul 2.0 | Quality-rated ages and rating scripts (verified) | `fossahul` entry exists |
| ICS chart (SKOS/RDF) and WaverideR `GTS_info` | Official chart as Turtle, CC BY 4.0, no error fields; `GTS_info` holds GTS2020 ages with errors (verified) | `timescale` entry in progress on the side branch |
| DeepTimeKB | Knowledge graph, MIT, dormant since 2022 (verified) | Not catalogued |
| PhanGrids (Jones & Domeier 2024) | Palaeocoordinate grids for five plate models, Zenodo 10.5281/zenodo.10069221, consumed by `palaeorotate` (verified) | Backlog rank 4 (palaeogeography and plate models) |
| PANALESIS atlas | Phanerozoic palaeogeography, seafloor age, crust, climate; Zenodo 10.5281/zenodo.19134591; dataset licence not stated (verified) | Backlog rank 4 |
| PaleoDEMs (PALEOMAP; EarthByte amplitude-corrected) | 109 corrected NetCDFs at 5-Myr slices (verified) | Backlog rank 4 |
| Phanerozoic climate-model fields | HadCM3L stage runs, PhanDA priors, GMST arrays (Zenodo 8237751; not opened) | `climate-forcing` entry in progress on the side branch |
| Fossil Calibration Database | Domain now serves unrelated spam (fetched 2026-10-23); content recoverable only through archives, untested | Not catalogued |
| MorphoBank | Morphological matrices; HTTP 403 to scripted fetches | Not catalogued |
| GBIF fossil specimens | 10,257,862 records with `basisOfRecord=FOSSIL_SPECIMEN` on 2026-10-23 (verified) | `gbif-ala-fossils` covers the Australian slice |
| Mesozoic food webs (`tylercl/Mesozoic-Food-Webs`) | Species-level metanetworks and R code, CC BY 4.0 (verified) | Not catalogued |
| Toarcian palaeo-web code and data | Zenodo 11400588, CC BY 4.0, for Dunhill et al. 2024 (verified) | Not catalogued |

## From tranche 3 (24 October 2026)

- [Detail withheld pending disclosure to the data custodian.]
- **The Plate Model Manager's `torsvikcocks2017` does not reproduce the
  GPlates Web Service's TorsvikCocks2017** (2–22° of palaeolatitude by age),
  while the Web Service and the Jones & Domeier grids agree. MERDITH2021,
  PALEOMAP and MATTHEWS2016_pmag_ref from the `palaeogeography` mirror agree
  with the Web Service to 0.0001° ([palaeoverse](palaeoverse/README.md)).
