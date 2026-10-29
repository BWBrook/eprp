# Q-027: bounded molluscan regional support diagnostic

29 October 2026. Databases Codex accepted Board 76/2506–2509 at 2512.
This is the requested aggregate-only presence diagnostic, completed within the
one-hour preparation bound. Main Codex owns the scientific contrast and allocation.

## Result

The table is available; region–latitude overlap can be counted under the stated
screen. Public membership affects support nonuniformly. No climate windows were
selected, richness estimator run, or empirical gradient fitted.

| Selected Cretaceous/Paleogene support | Original deposit | Dated public members |
| --- | ---: | ---: |
| Occurrence rows | 69,931 | 60,103 |
| Distinct collections | 11,208 | 9,180 |
| Stage × cell units | 1,194 | 1,068 |
| Stage × cell units with ≥2 collections within that subset | 811 | 726 |
| Sum of region × band × cell units with ≥2 collections within that group/subset | 816 | 727 |
| Stages with ≥3 outside-EU/NAm regions supplying eligible tropical cells | 14 of 21 | 12 of 21 |

Region–band counts are not additive independent replicates. A cell can span
regions or bands, and two one-collection regions can together qualify a stage
cell while neither region qualifies alone. All thresholds here are cheap
presence diagnostics. The 12-region map, including EU and NAm separately, is
retained, with unknown country separate. Island groups and RoW are sampling
partitions, not evidence of independent palaeobiogeographic histories.

Under the dated-member subset, only Albian has three outside regions each
supplying at least one qualifying cell in **all three bands** (AF, AS, SA).
Campanian (AF, AS) and Maastrichtian (AS, SA) each have two such regions.
This does not choose warm/cool windows, establish a connected time-by-region
contrast, or determine statistical power. For example, Cenomanian and Rupelian
lose some within-region band support after filtering. The full tables retain
all candidate stages before any window selection.

## Files and definitions

- `support.tsv`: all 21 stages × 3 bands × 13 region labels × 2 subsets,
  including explicit zero rows (1,638 rows). Occurrences and distinct
  collections describe that stage/band/region/subset. `cells` counts distinct
  approximate grid cells within that group.
- `cells_ge2_within_region_band` recomputes the ≥2 distinct collection rule
  within each stage × band × region × subset. `cells_ge2_within_stage` instead
  counts those group cells passing ≥2 collections anywhere in that stage and
  subset, to expose the difference from the earlier screen's global cell rule.
- `region-band-overlap.tsv`: for each stage/region/subset, lists bands having
  at least one `cells_ge2_within_region_band` cell, with tropical/midlatitude
  and all-three-band flags (546 rows). It does not count independent regions.
- `summary.json`: aggregate inclusion totals, exact input and archive-member
  hashes, builder hash, output hashes, stage bounds and the complete region map.
  The local `.gitattributes` preserves the TSV writer's CRLF bytes so a Git
  checkout retains the recorded hashes.
- `build.py`: standard-library offline builder, with no API route. It refuses
  an existing destination. No occurrence, collection or reference identifiers
  are exported. Internal identifiers support membership and distinct counts.

**Source.** The retained flagged published Benson deposit is
`deep:/data/paleodata/register-deposits/benson2025-marine-latitudinal-diversity/raw/v4_361737/marine-lbg-ms-dryad-repo.zip`,
SHA256 `7536adf67816407559698b59efc6a25f686ac48bd6b49a95590de94a320e0fe1`.
Its 23 May 2022 `Mollusca_data.csv` defines taxon membership: 368,760 distinct
occurrence IDs. This member lacks country/coordinate/genus fields, so all IDs
are internally joined to its same-download `Animalia^Chordata_data.csv`.
All join, with no duplicated IDs or non-Mollusca phylum values among matches.
That geographic member's SHA256 is
`c5da9359fced2285e0d50f20626a1ab562738d80ff12cece2bb0af530746670d`,
identical to the previously cached Q-027 source. ZIP member reads verify CRC;
both selected members have their own SHA256 in the summary.

**Dated membership.** All 15 `occurrences__p*.csv` files under
`deep:/data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url/` provide the
public membership set of 1,782,649 distinct occurrence IDs. Of the complete
Mollusca member, 297,657 belong to that snapshot and 71,103 do not,
reproducing the previous source-owner aggregate. [Detail withheld pending
disclosure to the data custodian.] The `dated_public_member` label means
membership on that date; it makes no live access or field-level update claim.
The original deposit remains retained and flagged. This task does not reopen
held direct extracts or access receipts.

**Conventions.** Preserve genus/subgenus/species accepted rank with nonempty
genus, exclude explicitly `unlithified` records, require finite valid original
collection-age paleolatitude/longitude and numeric ages. Of the joined source,
312,271 pass these filters; 69,931 are fully contained within the selected
21 stages. Stages are the source `pbdb_time_int.csv` scale-1 level-5 descendants
of Cretaceous and Paleogene (12 and 9 stages), preserving their dated bounds.
There are no multiply contained selected records. Absolute collection-age
palaeolatitude defines bands [0,20), [20,40), [40,90]. The original approximate
555-km grid uses 5-degree latitude strips and a cosine-adjusted longitude
partition, retaining the original collection coordinates. This is not dggridR
or reconstruction at each stage midpoint.

Country lookup uses the deposited static `marine_regions.csv` and
`country_codes.csv` retained in `data/raw/benson2025/`. Literal `NA` is Namibia,
not missing; UK/GB, AA/AQ and FA/FK are handled explicitly. Six static country
name aliases are explicit in the builder. Missing/unmapped country becomes
`UNKNOWN`; no nonempty selected country code is unmapped. Region assignment is
per occurrence row: no whole-cell modal-region exclusion is performed. Cell
and band boundary effects are retained rather than presented as distinct
independent geographical observations.

## Replay and verification

The production scratch area is
`deep:/data/codex/scratch/eprp-q027-regional-20261029/`.
It contains the script, three hash-recorded static files, the initial output
and `output-v2/` with the final aggregate summary. Both runs produced identical
support and region-band tables; v2 adds summary totals. Inputs are read-only;
all input SHA256 values are recorded and size/mtime signatures are checked
before versus after processing. Neither the source nor the snapshot is edited.
Run with those inputs and a **new** destination:

```sh
ssh deep 'python3 /data/codex/scratch/eprp-q027-regional-20261029/build.py \
 /data/paleodata/register-deposits/benson2025-marine-latitudinal-diversity/raw/v4_361737/marine-lbg-ms-dryad-repo.zip \
 /data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url \
 /data/codex/scratch/eprp-q027-regional-20261029/static \
 /data/codex/scratch/eprp-q027-regional-20261029/NEW_OUTPUT'
```

The parent checked source totals against the earlier permitted aggregate,
output cardinality and hashes, and the change in regional support. A separate
Codex auditor independently recomputed all 1,638 support rows and 546 overlap
rows from original files without importing the builder: every row matched.
It also confirmed all summary totals, the historical geographic-member hash,
and that no selected collection spans multiple support groups. There are eight
original and five dated-member mixed-region stage-cells; there are no blank
collection IDs, ambiguous stage assignments, unmapped nonempty countries, or
exact pole/dateline coordinates among selected rows. Both subset tables pass
count/set inequalities and every public-subset metric is no greater than its
original counterpart. Cenomanian and Rupelian are the two stages losing the
three-outside-tropical-region presence threshold. The independent aggregate
receipt is retained in `verification.json`.
These are source-retention and aggregate-computation checks, not validation of
a richness estimate or biological mechanism.

## Next decision and remaining qualifications

Main Codex can now inspect the complete stage × band × region support before
choosing any comparison. Estimator-specific feasibility is **unmeasured**:
Benson's majority-overlap age allocation, stage-midpoint palaeocoordinates,
dggridR geometry, modal-region cell exclusion, collection-incidence coverage,
quorum/extrapolation rules, and taxonomic treatment still differ. Two
collections per cell supplies neither a richness eligibility certificate nor
an effective sample size. Reference, formation and temporal dependence also
remain. Climate classification and the mapping between latitude-gradient shape
and local temperature require independent evidence. No additional source
campaign, estimator rebuild or scientific rejection follows from this screen.
