# Q-027: Albian–Campanian estimator eligibility

29 October 2026. Main Codex, with bounded GPT-6.1 Sol implementation and
independent verification. Barry authorised this build and run in main chat;
the exact instruction and ownership are recorded in Board 76/2545.

**The regional support does not survive the estimator's quality filters.**
Under dated public membership, no outside-Europe/North-America region supplies
eligible tropical and midlatitude cells in both stages. The required minimum
was two shared regions. The original author deposit also has no shared region.
This is a completed eligibility result under the declared implementation,
not an estimate of a biological latitudinal gradient.

## Result

Eligible cells, dated public subset, after all gates:

| Region | Albian tropical | Albian midlatitude | Campanian tropical | Campanian midlatitude |
| --- | ---: | ---: | ---: | ---: |
| Africa | 2 | 1 | 0 | 0 |
| Asia | 0 | 1 | 1 | 2 |
| South America | 3 | 0 | 0 | 0 |

Africa is the **only** outside-EU/NAm region with both bands in the Albian;
Asia is the **only** such region in the Campanian. The same endpoint sets hold
in the original deposit. All 12 source region labels, unknowns, higher
latitudes, and explicit zero groups are retained in the tables.

The geographic losses are substantive. Every public Albian tropical Asian
cell has at most ten molluscan incidence rows. No Campanian African cell in
either target band passes the combined quality rule. South America has no
Campanian midlatitude molluscan cell under this geometry and attribution.
These losses already prevent the focal contrast before the final 2T cap.

| Subset and stage | Cells with Mollusca | >10 incidence rows | Also pass quality | Also reach coverage 0.9 within 2T |
| --- | ---: | ---: | ---: | ---: |
| Original Albian | 107 | 60 | 33 | 24 |
| Original Campanian | 92 | 63 | 31 | 23 |
| Dated public Albian | 104 | 58 | 34 | 25 |
| Dated public Campanian | 89 | 54 | 26 | 20 |

There were **no estimator errors or nonfinite results** among the 235
cell-stage samples reaching the estimator. Of the 60 dated-public cells
passing the row and quality rules, 15 require more than twice the observed
number of collections to reach coverage 0.9, leaving 45 eligible cells across
all latitudes and regions. Membership filtering can improve a cell's
multiton ratio or coverage, so the public subset need not have fewer eligible
cells everywhere.

## Decision and limits

Close the Albian–Campanian route at these settings; it does not support the
proposed replicated comparison outside Europe and North America.

There is also a finite endpoint deduction. All three dated-public pairs that
passed the [earlier climate/presence screen](../q027-climate-pairing/README.md)
fail the two-shared-region requirement under this estimator contract:

- Albian–Campanian has an observed shared-region count of zero.
- Albian–Maastrichtian can share at most one region because the Albian
  endpoint supplies only Africa.
- Barremian–Campanian can share at most one because the Campanian endpoint
  supplies only Asia.

The latter two are set-intersection upper bounds, not estimator runs of
Maastrichtian or Barremian. They require the same fixed per-stage processing
and eligibility settings; pairing itself does not change those settings.
No additional stage run is needed to establish these bounds.

**This does not establish general untestability of Q-027.** The earlier
approximate presence screen was not an upper bound on this estimator's
support, so other stage pairs remain unresolved. Different coverage, spatial
resolution, taxonomic scope or regional definitions would be different
designs. The modern package implementation is explicit; exact equivalence to
the publication's ambiguous historical environment is unestablished. Eligible
cells alone would not establish independent regional replication or power.

Recommendation: return this negative result to the portfolio comparison;
do not fit a gradient or launch further stage scans automatically. Main Codex
owns that synthesis; primary-project selection remains Barry's. No further
Claude wake is required for this implementation checkpoint.

## Fixed computation

The [source contract](../q027-climate-pairing/estimator-contract.md) is realised
with the following consequential details:

1. Read the retained author deposit and the 15-file public membership snapshot
   dated 23 October. Public membership is applied before cleaning and
   genus–collection deduplication. Historical author fields are preserved.
   The clade-agnostic pool binds the three source primary files in their
   original order; Mollusca membership comes from its separate author file.
2. Apply source exclusions, extract the first word of `accepted_name`, retain
   modern coordinates, and keep the first genus–collection incidence. Assign
   a stage only when it occupies strictly more than half the record's age
   span. The deposited stage–map lookup selects **105 Ma for Albian and
   75 Ma for Campanian**, followed by the deposited offline-coordinate join.
3. Construct `dgconstruct(spacing=1000, metric=TRUE, resround="down")`.
   This request selects resolution 4, actual spacing **783.739 km**. Cell
   latitude is the arithmetic mean of the source-style wrapped polygon
   vertices, including the closing vertex. Bands use absolute cell latitude:
   tropical [0,20), midlatitude [20,40). These are Q-027 bands.
4. Assign each whole cell its unique modal region across distinct
   clade-agnostic collection-metadata rows; ties or wholly missing labels
   remain unknown. This pool **includes unlithified records**. The source's
   `n_total_colls` counts distinct metadata rows, which can exceed the number
   of distinct collection IDs; both counts are retained.
5. For richness, intersect Mollusca with the source's excluding-unlithified
   set, also excluding poorly lithified and sieved records. Require strictly
   >10 incidence rows. Use the revised quality rule: clade-agnostic metadata
   count >=10, at least two nonmissing Mollusca references, and a multiton
   ratio >=0.3, where the ratio is the fraction of observed genera occurring
   in more than one collection.
6. Run incidence-frequency iNEXT at q=0 and coverage 0.9 on `c(T,Y1,...)`,
   where T is distinct Mollusca collections. Accept a finite point only when
   `t!=0` and `t<=2*T`. The modern call uses `nboot=0,conf=.95`; its returned
   limit columns are not uncertainty estimates and are not used.

The source environmental join could in principle expand rows. Its complete
selected-data census found no multi-depth-zone matches or region-lookup
expansion. Each retained metadata key and collection-stage key has one
coordinate tuple. Source inspection establishes that omitted raster/GCM
fields depend on stage and coordinates; omitting their values therefore
preserves the distinct metadata counts for this pair. The full climate
pipeline was not run.

## Provenance and verification

Private incidence rows remain on `deep` under
`/data/codex/artifacts/eprp/q027-eligibility-20261029/preparation/`.
Only scripts, aggregate diagnostics, anonymous cell frequency vectors and
environment records are retained here. No raw occurrence, collection,
reference or taxon identifiers are exported. No held direct extract or new
PBDB download was used. Published deposits retain their existing flags.

- `preparation-summary.json` records all input and selected ZIP-member hashes,
  the full cleaning counts, 21,437 original and 19,878 public prepared rows,
  and zero missing coordinate joins, invalid coordinates, duplicate selected
  incidences, missing kernel identifiers or metadata-coordinate conflicts.
- `prepare.py` is the final adapter. `prepare-initial.py` preserves the source
  used for the initial preparation recorded in `results/run-input-freeze.sha256`.
  Added diagnostics were independently replayed; both private CSVs are
  byte-identical. `preparation-replay-receipt.json` binds both source versions
  and their output hashes. The original freeze is unchanged.
- `preparation-controls.R` separately checks R source semantics and the
  prepared-data cardinalities; its aggregate receipt is
  `preparation-controls.txt`.
- [Environment records](environment/README.md) pin R 4.6.1, iNEXT 3.0.2,
  dggridR 3.0.0 and the immutable image. They document the C++11 build, modern
  iNEXT argument change, and exact legacy polygon-rendering adaptation.
  Synthetic controls cover ordinary, pentagonal, dateline and polar cells;
  bootstrap options leave the tested point estimates unchanged.
- `run.R` produced 459 cell-stage records, 156 regional rows and 26 overlap
  rows. `verify.py` independently reproduces all eligibility and aggregation
  decisions. A separate analytic coverage-at-2T calculation agrees for all
  235 evaluated vectors; the nearest coverage margin is 0.002055, away from
  the 0.9 threshold. `verification.json` records hashes and the limits of
  that independent verification.

Preparation used CPython 3.12.3 with only its standard library and took about
101 seconds and 6.62 GiB peak RSS on deep; the R
estimator/grid run took 7.68 seconds, with a two-CPU/eight-GiB container limit.
The outer Docker CLI resource receipt does not measure the R process's peak
memory. No model ensemble or biological fit was run.

## Files and replay

`results/cells.tsv` contains anonymous per-cell incidence frequencies, counts,
modal region, latitude band, separate quality flags, raw qD/t, warnings and
eligibility. `results/regional-support.tsv` gives successive gate counts with
explicit zeros. `results/region-overlap.tsv` gives the four target-band counts
per region and their intersection. Raw qD is retained even when the point
exceeds 2T; use `eligible`, not numeric qD alone.

On deep, with this directory copied or checked out and the pinned image
available, plus CPython 3.12.3, run
`bash replay.sh /data/codex/artifacts/eprp/NEW_DESTINATION`.
It verifies input hashes, refuses an existing output directory and reproduces
private preparation plus aggregate results. To verify the retained aggregate
results locally, run `python3 verify.py` from this directory. No new data
access or full source pipeline is needed.
