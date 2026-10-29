# B-005 design evidence

29 October 2026. Main Codex's finite profile/observer checks support the
[scientific contract](../../ideas/2026-10-29-b005-design-contract-codex.md).
This directory contains no fossil measurements or model parameter ensemble.

- `design.json`: declared domain, weighting, statistic, observer and budget.
  SHA-256 and script hash were posted in Board 76/2527 before map comparison.
- `map_check.py`, `map-check.json`: hash-checked comparison of the two native
  maps. H²=0.1126043931; the power upper bound at N=100 is 1.0 and inconclusive.
  Four is only a necessary lower bound on N for the declared target.
- `observer_check.py`, `observer-check.json`: 16 enumerated synthetic controls,
  including scalar invariance, positive redistribution, missing-cell selection,
  N=0 and disjoint supports; four invalid profiles are rejected. This small
  enumeration is not a large-N numerical method.
- [Independent design and numerical audit](design-audit.md): counterexamples,
  rational fixture enumeration, separate raw-map reaggregation using exact
  spherical areas, reviewed hashes and final scientific-claims review.

The common domain is the 2,978 present-day native shelf cells with finite
predictions in both source maps. Required mask and coordinate equality are
checked before calculation. Spherical area is proportional to cosine of the
fixed half-degree latitude-bin centre. The native gridding source indexes
those bins using `lat_edges`; coordinate labels are checked for equality but
do not define these weights. Native cell means retain their original spatial
support: area weighting does not convert local richness to a new grain.

The observer adds independent cell-incidence draws with replacement and fixes
their detected total. This is neither unique-genus counting nor a fitted fossil
sampling model. Uniform effort retains all native supported mass in this
comparison. Weighted and unweighted local-richness sums are not gamma richness.

Raw maps remain on `deep` in
`/data/codex/artifacts/eprp/b005-native-smoke-20261029/`. The
[Packages receipt](../../resources/software/reviews/2026-10-29-b005-design/two-map-results.json)
pins the model/input/output hashes and environment. Main Codex's scripts and
design were copied to `/data/codex/scratch/eprp-b005-profile-20261029/` for the
small map calculation with that existing Python 3.12.3 / NumPy 2.4.6 environment.
No new environment or simulator run was required.

Replay the synthetic controls locally with standard-library Python:

```sh
python3 data/b005-design/observer_check.py
```

From the repository root, the map calculation can be repeated after copying
`design.json` and `map_check.py` to the stated remote scratch directory:

```sh
ssh deep '/data/codex/artifacts/eprp/inditek-forward-20261028/env/.venv/bin/python /data/codex/scratch/eprp-b005-profile-20261029/map_check.py /data/codex/scratch/eprp-b005-profile-20261029/design.json /data/codex/artifacts/eprp/b005-native-smoke-20261029'
```

Independent small-fixture verification used rational ordered-sequence
enumeration, rather than importing the count-vector implementation. Across
13,842 sequences it reproduced power to 8.33e-17 and bounds to 1.12e-16.
Independent raw-map calculation also reproduced both weighted means, H²,
affinity and the power/sample-budget bounds to floating-point precision.
These checks validate the stated mathematical/numerical controls, not a fossil
observation law or historical biological claim.
