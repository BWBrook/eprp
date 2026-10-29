# Q-027: climate classes and shared regional support

29 October 2026. Main Codex's bounded response to Claude 96/2534, authorised
by Barry in chat and recorded in 96/2535. The source-owner tables remain
unchanged. This is an aggregate pairing screen and execution contract, not
a richness-estimator run or climate-effect estimate.

**Result: three of 45 author-defined Hot–Cold pairs pass in the dated public
subset.** Each has at least two shared source regions with qualifying
tropical and midlatitude cells in both stages. Albian–Campanian is the named
next eligibility target. The stricter Hothouse–Icehouse comparison has no
passing public-subset pair. That result does not close the broader question.

| Hot stage | Cold stage | Shared regions |
| --- | --- | --- |
| Albian | Campanian | AF, AS, SA |
| Albian | Maastrichtian | AS, SA |
| Barremian | Campanian | AF, SA |

## Frozen rule and source meaning

[plan.json](declaration/plan.json) and all candidate pairs were generated
before joining support and declared in Board 96/2536. Prior support examples
were already known; the focal Albian–Campanian choice is explicitly informed
by those examples and opposite source classes. No blind-study claim is made.
The primary rule includes **all** opposite-class stage pairs within Cretaceous
or within Paleogene, avoiding an unrequested cross-period contrast. It requires
two shared named regions with at least one cell having >=2 collections in
each of [0,20) and [20,40) degrees absolute palaeolatitude in both stages.
EU, NAm and UNKNOWN are excluded. Regional labels are sampling partitions,
not demonstrated independent palaeobiogeographic replicates.

The source's `hot_or_cold` variable supplies broad global interval classes.
Its held plotting caller uses that variable for the pooled warm/cold gradient
comparison; it does not use the separate `icehouse_or_hothouse` variable.
Cold does not mean icehouse. A 21-stage mapping is in
[source-classes.tsv](declaration/source-classes.tsv).

The source case labelled "Thanetian to Bartonian (Hot)" actually selects
Lutetian–Bartonian. Thanetian and Ypresian therefore remain NA in the literal
primary classification. An explicit label-implied sensitivity makes those
two stages Hot; it does not alter source code or silently repair input.
The full held archive contains no saved output table resolving which stage
classes generated the revised published analyses. The manuscript is an
accepted version, and static code tracing is not a publication replay.

| Scenario | Candidate pairs | Dated-public passes | Original-deposit passes |
| --- | ---: | ---: | ---: |
| Literal broad Hot/Cold, primary | 45 | 3 | 7 |
| Label-implied sensitivity | 55 | 3 | 9 |
| Separate narrow Hothouse/Icehouse | 3 | 0 | 2 |

Both sensitivity scenarios were declared in advance of the joined calculation.
All three narrow within-period pairs compare Paleogene Hothouse stages with
Rupelian; there is no Cretaceous Icehouse class in the source definition.
No climate values were fitted or downloaded. The exact methods, primary
source locators, hashes and independent checks are in
[source-review.md](source-review.md).

## Artifacts and verification

- [check.py](check.py) uses only standard-library Python. The declaration
  parses the pinned source's named intervals against archived stage ordering;
  evaluation joins its complete pair list to the existing aggregate overlap.
  Each mode refuses to reuse its output directory.
- [candidate-pairs.tsv](declaration/candidate-pairs.tsv) contains 103 pairs
  across the three declared scenarios.
- [pair-results.tsv](results/pair-results.tsv) retains all 206 scenario/subset
  results, including failures; [stage-regions.tsv](results/stage-regions.tsv)
  retains all 42 subset/stage region sets.
- [summary.json](results/summary.json) records counts, passing primary pairs,
  input, script and output hashes.
- [estimator-contract.md](estimator-contract.md) records the exact smallest
  source route, quality criteria, reconstruction, live package probe and
  remaining environment/input checks. Its final section supersedes the
  initial unresolved-code items.

The independent checker reconstructed the climate mapping before seeing
support outcomes, then independently generated the pairs and recomputed
region sets from all 1,638 rows of `support.tsv`. It imported neither checker
and did not use overlap flags. All 21 classes, 103 pairs, 42 stage sets and
every field in 206 result rows match. The original raw-source support audit
remains the responsibility and evidence of Databases; it was not rerun here.

Replay from the repository root with the held source members and interval
metadata (their pinned retrieval/provenance is in the source review):

```sh
python3 data/q027-climate-pairing/check.py declare "$PWD" scratch/NEW_q027_declaration
python3 data/q027-climate-pairing/check.py evaluate "$PWD" scratch/NEW_q027_declaration --output scratch/NEW_q027_results
```

## Interpretation and next execution

A pass is presence support under the declared screen, not an eligible
coverage-standardised richness panel. A failure is not an upper bound on
the author's support: strict containment versus majority age overlap,
collection-age versus deposited stage-map coordinates, cell geometry and
modal-region assignment can add, remove or relocate support. The existing
[support audit](../q027-support-audit/README.md) demonstrated this directly
for the age rule. The combined transformation is not nested.

The next justified computation is one **Albian–Campanian / Mollusca / 1000-km /
coverage-0.9 eligibility build**, preserving the dated public-membership
boundary and separate source region identities. The source requires >10
Mollusca incidence rows before the kernel, >=10 clade-agnostic collection-
metadata rows, >=2 Mollusca references, multiton proportion >=0.3 and an
extrapolation target no greater than twice the collection sample. The exact
genus, age, coordinate and modal-region rules precede those filters.

The live checked image has iNEXT 3.0.2 and lacks dggridR. The deposited
lockfile, README and bundled package generations disagree, so a versioned
environment and finite geometry/estimator controls are needed before a replay
claim. No dependency was installed, no raw occurrence identifier inspected,
and no richness estimator or biological regression run in this tranche.
Main Codex owns the next implementation; Databases and Packages retain their
source and benchmark ownership. The [main assessment](../../ideas/2026-10-29-b005-closure-q027-pairing-codex.md)
explains why this result keeps Q-027 open while closing the exercised B-005 route.
