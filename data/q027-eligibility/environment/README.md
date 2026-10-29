# Q-027 isolated eligibility environment

Built and checked on `deep`, 29 October 2026. Parent authorised the modern
declared estimator environment and accepted the source-inspected legacy
geometry renderer adaptation. This is not an exact historical publication
replay. No occurrence data entered these environment checks.

Image `eprp-q027-eligibility:20261029` has immutable ID
`sha256:b7d5a9f9b91b153a29e38b7c117dcf5d3298adb4618a409d7d779280b16adef8`.
Its unchanged base is `eprp-sw/bench-r4:t4`,
`sha256:d0c1c51a6c65e5811654e60a54ab84aa25b65218064a8366c42f009f821db39b`.
The isolated additions are dggridR 3.0.0 and sp 2.2-4. The base supplies
R 4.6.1, iNEXT 3.0.2, sf 1.1-3, Rcpp 1.1.2, dplyr 1.2.1, rlang 1.3.0,
and their dependencies. Full installed versions and compiler/spatial-library
records are in `installed-packages.tsv`, `session-info.txt`,
`spatial-libraries.txt` and `toolchain.txt`. The image ID pins all inherited
system and package dependencies; no host R or global configuration was changed.

## Sources and build

Primary source archives retrieved from official CRAN on 29 October 2026:

- [dggridR 3.0.0](https://cran.r-project.org/src/contrib/Archive/dggridR/dggridR_3.0.0.tar.gz), SHA256 `4aa6e58b31209a4578626661bc7583bfad2f1a96fd8ce804d0d6701f10a325a4`.
- [sp 2.2-4](https://cran.r-project.org/src/contrib/sp_2.2-4.tar.gz), SHA256 `73f03473e61e89f3c0c1a96ac6e17e81a075637963d1d6b156dc9c969b2dbc93`.
- [dggridR 2.0.3](https://cran.r-project.org/src/contrib/Archive/dggridR/dggridR_2.0.3.tar.gz), SHA256 `7027991e8dda2e7ba3529db1ccc2ab95c4ad1a9ab5f47ca6cbb7165668eebcbd`; reference only, not installed.

The archives remain under
`deep:/data/codex/artifacts/eprp/q027-eligibility-20261029/environment/source/`.
`legacy-dg-process-polydata.R` is the verbatim `dg_process_polydata` function
from dggridR 2.0.3 `R/dggridR.R` lines 575–609; its MIT licence is retained in
`dggridR-2.0.3-LICENCE.txt`. The package authors include Richard Barnes,
Kevin Sahr, Gerald Evenden, Angus Johnson and Frank Warmerdam.

Run `bash replay.sh` in the remote environment directory. The script verifies
the base image ID before and after building, checks both installed-source
hashes, disables build networking, and caps the build at two CPUs and 7 GiB.
The first attempt used R's current default C++20 and failed on old constructor
syntax in `DgBoundedRF.h`. The successful second attempt uses a temporary
package-specific `R_MAKEVARS_USER` file selecting the package's declared
C++11 standard. The source archive is unchanged. Complete attempt logs remain
on `deep`; `build-evidence.txt` records their hashes and excerpts.
Rebuilding from pinned inputs reproduces the declared environment and
controls; build timestamps can change the resulting image ID.

## Geometry contract

`dgconstruct(spacing=1000, metric=TRUE, resround="down")` chooses ISEA3H
resolution 4: actual spacing 783.739159045648 km, area
629710.644103813 square km. Mapping remains
`dgGEO_to_SEQNUM(grid, longitude, latitude)$seqnum`.

dggridR 3.0.0 changed `dgcellstogrid(dggs,cells,savegrid=NA)` to return `sf`
polygons and removed `frame`/`wrapcells`. Source `legacy_geometry.R`, then call
`q027_cell_geometry(grid,cells)` to obtain `cell_id`, `cell_paleolat`,
`cell_paleolng`. The helper sends the native 3.0.0 `SeqNumGrid` rings through
the source-inspected 2.0.3 rendering operations: `sp::Polygon` closure and
orientation, `ggplot2::fortify`, and negative-longitude +360 for any ring
spanning more than 180 degrees. It retains the closing vertex when taking
arithmetic means. No polygon splitting or geodesic centroid is used.
`q027_cell_frame` exposes the intermediate legacy frame for checks.

Controls verify that native `sf` extraction matches raw rings in ordering and
closure, and that the helper exactly matches the verbatim old renderer for
regular, pentagonal, dateline and polar cells. The grid has 12 pentagons.
These checks establish the declared adaptation's behaviour; they do not
establish equivalence between the 2.0.3 and 3.0.0 native grid engines.
`fortify(SpatialPolygons)` emits a deprecation warning in the pinned ggplot2
but works. Geometry outputs are retained as synthetic TSVs.

## iNEXT contract

The tested modern point call is
`iNEXT::estimateD(list(site=c(T,Y1,...)), q=0, datatype="incidence_freq", base="coverage", level=.9, nboot=0, conf=.95)`.
Its columns are `Assemblage,t,Method,Order.q,SC,qD,qD.LCL,qD.UCL`.
Use `qD`; retain `t`, `T`, and explicit eligibility status. Reject the point
when `t==0` or `t>2*T`, with separate handling for nonfinite values/errors.
`nboot=0` disables bootstrap: the returned limit columns equal `qD` and are
not uncertainty estimates. The old source's `conf=NULL` fails in this version
with `arguments imply differing number of rows: 1, 0`.

Five finite controls cover rarefaction, extrapolation within 2T, insufficient
coverage at 2T, all singletons, and no singletons. Point `t`, `SC`, `qD` are
exactly unchanged against `nboot=20,conf=.95` and `nboot=0,conf=0`.
The insufficient-coverage fixture has `t=49.172124286216`, `2T=40`, and
coverage at 2T of 0.878942817035; it is rejected. The all-singleton fixture
is also rejected by 2T, without adding a preliminary singleton guard.
The exact zero/2T/over-2T boundary predicate passes. All control results are
in `synthetic-estimates.tsv`; `controls.log` reports the complete pass.

Parent Codex owns the occurrence-data run and scientific interpretation.
