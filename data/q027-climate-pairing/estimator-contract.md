> Execution contract assembled by the bounded source delegate. The final
> remote-code completion section resolves the initial open code questions.
> No estimator has been executed; main Codex owns environment selection and
> the one-pair implementation.

# Q-027: smallest Benson estimator route for one stage pair

Read-only reconnaissance, Codex, 29 October 2026. Parent owns the stage pair,
climate-source gate and scientific go/no-go. No pair was selected, occurrence
identifiers or held extracts inspected, estimator run, remote session opened,
or new source downloaded. This note is the only write by this delegate.

## Finding

The smallest faithful computational kernel already exists: **the zero-quota
branch** of `scratch/q027-independent-audit/source/subscripts/rscript-run-grid-cell-subsampling-analysis-100km-dggridR-cells.R`,
lines 83–175. It computes the ordinary per-cell richness, without experimental
100-km cell rarefaction. Use only Mollusca, ungrouped, excluding-unlithified,
one 1000-km grid and the two parent-approved stages; no full master-script,
climate/GCM loading, paleoDEM, PaleoReefs or plotting run is needed for this
support test. Grid construction is fixed by `dgconstruct`, rather than fitted
to all the added paleoDEM/reef points, so other point sets need not be loaded
to identify the occupied fossil cells.

**Exact source-faithful support cannot yet be certified from the selected local
source alone.** The full mirrored Zenodo archive needs a bounded code-only
inspection for its quality helper, reconstruction-age assignment and original
package lock. The master sources missing scripts, and the revised plotting
helper is called but not defined in the selected local files. Do this finite
inspection before claiming an exact Benson replay or writing a full pipeline.

The existing cheap support screen is **not an upper bound** on this estimator's
support: assignment, coordinates, cell geometry, cell-region attribution and
eligibility all change. Failure of its regional intersection can motivate a
check, but cannot prove estimator impossibility.

## Author estimator and input grain

- Settings file lines 78–92: estimator labelled `sqs`; coverage quora
  `0.4, 0.7, 0.9`, default **0.9**; spacings 100/500/1000/2000 km. This is
  **iNEXT incidence-frequency coverage-standardised genus richness**, not
  `divDyn::subsample(type="sqs")` or the older `runSQS.R` function.
- Kernel lines 114–133 counts collections and genera, then tabulates
  `operational_taxon_name`; lines 160–174 build `list(site=c(T, Y_1,...))`,
  where T is distinct collections and each genus frequency counts its occupied
  collections after upstream genus×collection deduplication. Lines 164–168
  call `run_SQS_iNEXT_simple_no_empty_tibbles`.
- `functions/run_SQS_iNEXT_simple.R:65–78` calls
  `estimateD(datatype="incidence_freq",base="coverage",level=q,conf=NULL)`;
  richness becomes NA if returned `t==0` or `t>2*T`. Retain t/T and explicit
  failure reasons; a numeric extrapolated value alone is insufficient.
- The actually called `no_empty_tibbles` function has **no** preliminary
  all-singleton/three-genus rejection. Those guards belong to other helpers
  in the same file (lines 4–21 and 50–60); do not silently substitute them.
- No subsampling trials or bootstrap intervals are needed for the quota-zero
  point-estimate eligibility gate. Preserve the author's point calculation;
  changing uncertainty options would need a separate equivalence check.

Minimum private working grain is one cleaned genus×collection incidence with
internal occurrence membership linkage, collection identifier, original modern
lat/lng, min/max age, country/region, lithification and collection-method fields.
Faithful cleaning also needs `accepted_name`, `geoplate`, preservation mode,
geographic/stratigraphic scale and the deposited terrestrial/freshwater exclusion
terms. Preserve reference/formation IDs internally if later dependence checks
are wanted; do not export identifiers. The final public/committed product can
be aggregate stage×region×band eligibility with warnings/failure totals.

## Reconstruction contract that cannot be replaced by the presence table

1. **Membership and names.** Reuse the existing builder's offline dated-public
   ID membership join and author Mollusca membership, not a new PBDB query.
   Regional-support README records the retained Dryad archive and exact
   15-file public-snapshot paths/hashes; the same-download geographic member
   is hash-identical to the cached source. The public snapshot supplies only
   membership; retain the author's historical fields. Apply membership before
   any deduplication, modal regions or collection-quality counts, including
   clade-agnostic counts. Author `load-occurrence-data.R:287–317` constructs
   genus from the first word of accepted_name, does not elevate subgenera,
   requires modern coordinates, and removes duplicate genus×collection rows.
   The current screen instead trusts `genus` plus accepted-rank filtering.
   Their equality has not been verified.
2. **Cleaning.** Settings lines 62–75 and load-occurrence-data lines 176–284
   exclude basin/group-scale collections, soft parts and listed
   terrestrial/freshwater taxa. `specify-settings.R:63–78` excludes both
   explicitly unlithified and poorly-lithified+sieved records. The current
   screen only excludes explicitly unlithified records. It is not the exact
   source cleaning route.
3. **Time.** `define-time-ints.R:12–26` uses deposited PBDB scale-1 level-5
   stages and time midpoint. `assign-occurrences-using-bin-schemes.R:31–50`
   requires a unique stage with strictly >50% of each record's age span,
   rejects zero-duration and unresolved ranges, and joins deposited offline
   reconstructed coordinates by `plate_model_age,lat,lng`. Do not prefilter
   by full containment; records spanning the chosen stage boundary can enter.
   The selected local code does not define the mapping from midpoint to
   `plate_model_age`; inspect the mirrored loader rather than invent rounding.
4. **Coordinates/grid.** The author discards collection-age default
   palaeocoordinates (`load-occurrence-data.R:307–312`). Use deposited
   `offline_gplates_reconstructions.csv` (profile: 99,852 rows; columns
   plate_model_age,lat,lng,paleolng,paleolat). `compute-dggridr-cells.R:31–46`
   uses `dgconstruct(spacing=1000,metric=TRUE,resround='down')`, then
   `dgGEO_to_SEQNUM`. Lines 62–100 obtain wrapped polygons with `frame=TRUE`
   and define cell latitude/longitude as mean polygon-vertex coordinates.
   The cell latitude here is not the input occurrence latitude or a separately
   computed geodesic centroid.
5. **Cell/region.** `compute-clade-agnostic-env-vars.R:36–48,66–109` computes
   modal region from distinct collection-metadata rows across the most
   inclusive source taxon set; ties become NA. `n_total_colls` is implemented
   as number of those distinct metadata rows, not an explicit collection-ID
   count. Reproduce that literal operation or report a deliberate change.
   The source's outside-EU/NAm analysis excludes whole modal-region cells
   (`plotting-scripts/explore-eu-nam-peak-latitudinal-richness.R:48`), whereas
   the presence screen excludes occurrence rows. A modal-outside cell can
   contain EU/NAm rows. Preserve the complete static region map, unknowns
   and ties; do not collapse outside regions into RoW before overlap checks.
6. **Eligibility.** `compute-clade-agnostic-env-vars.R:31–32` sets
   min_occs_per_cell=10; `run-clade-specific-computations-in-rscript.R:63–79`
   requires **strictly >10 clade-specific occurrence rows per cell** before
   calculation. The older deposited plotting-preparation helper
   `load-shiny-data-for-plotting-figures.R:10–15` imposes clade-agnostic
   collection-metadata count >=10 and multiton_ratio >=0.3. Revised main
   plotting code instead calls `identify_regions_that_meet_quality_criteria`
   (line 15), then uses its flag downstream. That helper and the exact
   `multitonRatio` definition are absent from the selected local source.
   Treat >=10/0.3 as a traced deposited route, not yet a proven definition of
   the revised paper route.
7. **Requested Q-027 bands.** After assigning cells, use absolute *cell*
   latitude for tropical [0,20) and midlatitude [20,40); require eligible
   cells in both bands **within each same named region in each selected
   stage**, and report the common region intersection across stages. These
   20/40-degree boundaries are Q-027's contract: the author's stored low/mid/high
   labels use 30/60 degrees (`compute-dggridr-cells.R:115–117`). Document
   that adaptation. No hemispheric independence or power follows from it.

## Minimal executable tranche, conditional on parent go

First inspect existing remote archive **metadata and source code only**, then
write one bounded adapter on the authorised compute host: reuse public-set and
Mollusca joins, selected source cleaning/age/coordinate/grid operations, and
the quota-zero estimator kernel. Restrict stages after the majority-overlap
calculation; retain the clade-agnostic pool for cell metadata, while calculating
only Mollusca richness. Choose no climate/window thresholds during execution.

Export counts through successive gates, the same-region/two-band/two-stage
intersection, and per-group counts of insufficient occurrence rows, quality
failure, undefined region/tie, missing reconstruction, estimator errors and
extrapolation-cap failure. Keep raw richness and incidence diagnostics as
support diagnostics. No empirical gradient regression is needed to answer
whether this estimator yields the required connected support.

The atomic computation is small (one iNEXT call per retained stage-cell at
one quorum). No benchmark of this exact job exists. Preparation risk is source
reconstruction/environment fidelity, not a reason for a production ensemble.
Do a tiny synthetic-format smoke first, with explicit <=2T checks, and stop at
the finite support result. Runtime and RAM must be measured before promising
a bound; no remote readiness was verified in this reconnaissance.

## Existing replay and environment evidence

No exact Benson pipeline replay was found in the tracked repo or ignored
Q-027 scratch. `data/q027-support-audit/README.md` explicitly says its source
inspection did not execute the pipeline. `resources/software/LANDSCAPE.md:132`
is an inventory entry, not a checked execution. Deposited README line 31
reports R 4.2.1 and a bundled renv library/lock; those packages have not been
restored or inspected here.

There is a checked **iNEXT kernel** environment, not a Benson environment:
`resources/software/inext/README.md` and
`resources/software/bench/env/Dockerfile.r4` record iNEXT 3.0.2 in image
`eprp-sw/bench-r4:t4` on deep (dated README digest prefix d0c1c51a).
`bench/validate/t4_estimate.R:18–42` constructs incidence vectors, calls
estimateD and retains t, coverage and collection counts. Its tests are on
synthetic data at quorum 0.6/0.8, not this public-subset 0.9 source contract.
No dggridR install is shown in the r4/r3 Dockerfiles inspected.

**Output-schema hazard:** deposited helpers select the old richness column
`q = 0`; the checked 3.0.2 bench uses `qD` and matches Assemblage names. Directly
sourcing the old helper in that image is not a demonstrated working route.
Inspect original renv versions, or make a narrow version-specific adapter
verified against a synthetic incidence fixture. Do not silently treat missing
columns as an estimator failure/no-support result.

Exact questions for parent to resolve on existing mirror (no SSH here):

- In `/data/paleodata/register-deposits/close2025-marine-latitudinal-diversity-code/raw/15269137/`,
  what are the manifest hash and ZIP member paths for `renv.lock`,
  `subscripts/load-offline-paleocoord-reconstructions.R`, package-loading and
  plotting-preamble scripts, `identify_regions_that_meet_quality_criteria`,
  `multitonRatio` and `compute-clade-specific-env-vars.R`?
- What exact `plate_model_age` mapping and reconstruction data version/model
  does that loader apply? Does the deposited table cover the chosen stages?
- What package versions does the lock specify for iNEXT/dggridR, and is there
  an already working dggridR environment on deep? The existing checked bench
  is only a candidate base; availability and versions need a live check.

The source inventory is `resources/sources/register-deposits/snapshots.tsv`
(Dryad v4_361737 and Zenodo 15269137), with offline-reconstruction schema in
`profile/register_deposits_profile.tsv`; exact locally selected member SHA256s
are in `data/q027-support-audit/source-member-checksums.tsv`. No archive source
or data should be replaced or refreshed for this bounded check.
All 25 selected local source members were SHA256-checked against that manifest
during this reconnaissance; all matched.

Complete: local route reconnaissance. Provisional: exact revised quality rule,
age-reconstruction mapping and runnable environment. Next responder: parent
Codex for the climate/source pairing decision and bounded mirror inspection.

2026-10-29 15:11 AEDT, Australia/Hobart.

## Finite remote code completion, 15:14 AEDT

Parent authorised this source-read extension after passing the author broad
Hot/Cold and shared-region gate for Albian–Campanian (AF, AS, SA). That
decision belongs to parent. The findings below supersede the unresolved-code
items above; the earlier no-remote statement describes the initial pass only.
No occurrence or coordinate data rows, identifiers, or held extracts were
read; no estimator, installation, build or biological fit was run.

Read the existing mirrored ZIP through configured `ssh deep`. Bounded code,
lock metadata and four package DESCRIPTION files are retained under
`deep:/data/codex/scratch/eprp-q027-estimator-route-20261029/`, with
`extraction-manifest.json` recording member paths, byte counts and SHA256s.
ZIP reads checked member CRC. The mirror manifest SHA256 is
`dbe500eb70f5b4b2cadf6ca5f72ebbe144284062d1399468dee010a113c53997`;
it records archive SHA256
`45f89554de79a34b5f2de70c60fc71a3dbd126d1b7072c559be9b8ea6a815bdf`.
The full 1.55-GB archive was not rehashed by this delegate.

### Exact revised quality and multiton rule

`subscripts/load-packages.R` defines the helper called by revised main plots:

```r
clade_agnostic_n_total_colls >= 10 & n_refs >= 2 & multiton_ratio >= 0.3
```

This is the clade-agnostic-quality helper, not its neighbouring clade-specific
variant (which uses `n_colls>=10`). For the selected Mollusca kernel, `n_refs`
is the distinct nonmissing occurrence-reference count within that Mollusca
cell-stage sample (`rscript-run-grid-cell-subsampling-analysis...R:121`).
The upstream strict >10 Mollusca occurrence-row gate also applies. Therefore
an ordinary >=2-collection screen is very far from sufficient.

`functions/multitonRatio.R` computes `(S-s1)/S`, where S is the number of
observed genera and s1 the number occurring once in the incidence vector.
It is a fraction of genera with repeated collection incidence, not Good's u
and not a minimum number of repeated occurrences. Missing metadata/flags must
remain missing and be counted separately; the plotting downstream requires
`meets_quality_criteria==TRUE`.

### Exact reconstruction-age rule

`subscripts/load-scotese-paleodems.R:82–114` joins stages by name to
`input/PaleoDEMS netcdf/stages_scotese_lookup_table.csv`, then to the map table
`input/PaleoDEMS netcdf/PaleoAtlasTimeIntervalsv22b copy.csv` using its map
name. The latter's `Plate Model Age` becomes `plate_model_age`. Thus stage
coordinates use the **author's hand-coded stage-to-map lookup**, not stage
midpoint or any inferred rounding. Only equal-length bins choose the map
nearest their midpoint (lines 117–125).

The offline loader simply reads the already deposited reconstruction table;
if missing, it writes coordinate-age inputs and stops for manual
chronosphere/GPlates reconstruction. Rebuilding those coordinates is outside
the minimal route. The two lookup CSVs, reconstruction CSV and the
terrestrial/freshwater exclusions R file are confirmed present by ZIP member
names only. Their contents/coverage for this pair were not inspected under
the code-only boundary. Reading the two small stage/map tables is necessary
to get the pair's exact numerical reconstruction ages; no netCDF raster load
is needed. The loader does not name a GPlates model/version, so its provenance
should be described as the deposited reconstruction, without inventing the
underlying plate model.

### Original package metadata and live probe

The lockfile reports R 4.1.2, iNEXT 2.0.20 and dggridR 2.0.3. The bundled
R-4.1 DESCRIPTIONs confirm those package versions and R 4.1.2 builds. The
same deposit also contains R-4.3 DESCRIPTIONs for iNEXT **3.0.0** and dggridR
**3.0.0**, both built with R 4.3.1. The README says R 4.2.1. This is a real
provenance ambiguity: the lock/README/bundled libraries do not establish
which package generation executed the revised final analysis.

A harmless network-disabled, read-only-container package probe of the existing
image returned:

| Component | Live result |
| --- | --- |
| R | 4.6.1 |
| iNEXT | present, 3.0.2 |
| dggridR | **absent** |
| dplyr / tidyr / purrr | 1.2.1 / 1.3.2 / 1.2.2 |

Parent verified image identity:
`eprp-sw/bench-r4:t4`,
`sha256:d0c1c51a6c65e5811654e60a54ab84aa25b65218064a8366c42f009f821db39b`.
Probe output is retained as `package-probe.txt`. No bundled compiled libraries
were loaded into this modern R image.

### Implementability and minimum remaining blockers

The **one-pair eligibility computation is fully specified algorithmically**.
It is not runnable faithfully in the probed image yet because dggridR is
missing. A finite implementation can still avoid the whole analysis stack:
stage/map CSV joins, deposited offline-coordinate join, one dggridR geometry,
two cell-stage Mollusca incidence tables, revised quality gates and quorum-0.9
iNEXT values with the author's 2T cap. The necessary reference field is already
in the deposited source's input schema. The generic iNEXT 3.0.2 bench is a
working kernel base, not an exact historical environment.

Minimum execution work for parent is:

1. Read the two tiny static map lookups and check the deposited coordinate
   join's cardinality/completeness for the pair during authorised processing;
   preserve no-match counts rather than silently dropping them. Existing
   inputs are present; there is no demonstrated need for a download.
2. Supply dggridR in an isolated usable environment and state the chosen
   version. To claim exact **lock-defined** replay, use iNEXT 2.0.20/dggridR
   2.0.3 with a compatible R stack. To use the current kernel, explicitly
   label it an estimator-faithful modern replay, adapt only the old `q = 0`
   versus `qD` output schema and verify deterministic synthetic cases and
   selected cell geometry before interpreting support. Modern-version
   equivalence to the historical geometry/estimator is not established by
   this reconnaissance. Avoid restoring dozens of unrelated plotting/GCM
   packages merely to compute these quantities.
3. Make the Q-027 regional adaptation explicit: revised source labels whole
   cells by modal collection region; Q-027 uses [0,20)/[20,40) absolute cell
   latitude and preserves AF/AS/SA separately. Do not mix this with a
   region-row-split estimator or the source's RoW-collapsed plots.

No finite source-code unknown remains for the requested quality, multiton or
age-allocation rule. Remaining uncertainty is numerical input join coverage
and chosen package-generation fidelity. These can be resolved in the bounded
eligibility run; they do not justify a full pipeline reconstruction. Parent
Codex owns the environment choice and next execution tranche.

2026-10-29 15:14 AEDT, Australia/Hobart.
