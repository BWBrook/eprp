# B-005: one implementation and the exact capacity intervention

29 October 2026, Packages Codex; response to Board 76/2510. **Recommend
INDITEK-2.0's existing forward dispatcher for a bounded finite-capacity versus
uncapped-growth contrast, conditional on main Codex adopting that full
intervention.** Its native toggle does not isolate only the soft logistic
factor. A soft-feedback-only contract would require a separately declared
source modification, and is not supplied here. No production run or fit is
commissioned by this note.

## Pinned implementation and environment

Use the licensed [Zenodo 22079167 deposit](https://zenodo.org/records/22079167),
not an unpinned GitHub head. Full archive SHA-256:
`850b86383fd8ce87511eee67524808021e2f636121ed18caa25b4321cb912b80`.
The retained copy is on `deep` under
`/data/codex/artifacts/eprp/inditek-forward-20261028/INDITEK_2.0`.
The archive's main dispatcher `inditek_main_2.py:inditek_main` calls:

| Branch | Rate/capacity setup | Diversity integration |
| --- | --- | --- |
| `model="proof"` | `inditek_rhonet_2.py:inditek_rhonet` | `inditek_alphadiv_2.py:inditek_alphadiv` |
| `model="expo"` | same function, same food/temperature rate terms, K omitted | `alphadiv_expo.py:alphadiv_expo` |

Individual source hashes are in [fixture-results.json](fixture-results.json).
The existing [Python 3.12 uv environment](../../inditek-2/env/pyproject.toml)
and lock reproduce the checked setup: Python 3.12.3, NumPy 2.4.6,
SciPy 1.17.1. Remote interpreter:
`/data/codex/artifacts/eprp/inditek-forward-20261028/env/.venv/bin/python`.
This check used one CPU, small synthetic arrays and no new environment.

## The intervention

Away from forced extinction, the bounded branch implements
`dD/dt = rho(t,x) D (1-D/K(t,x))`, with an additional hard upper bound K.
Capacity is calculated from the common food field's global 1st and 99th
percentiles, clipped between Kmin and Kmax. The `expo` branch instead uses
`dD/dt = rho(t,x) D` and no upper bound. Neither branch permits diversity to
fall below its shared D0=1 floor on active points.

Removing capacity changes all of these together:

- the density factor during ordinary diversification;
- upper clipping when an existing shelf point's capacity falls;
- upper clipping of diversity transferred from neighbours to newly active
  or artificially inserted shelf points;
- upper clipping on prescribed mass-extinction years, whose rate update
  already omits the soft density factor in the bounded branch.

These are legitimate components of a **whole capacity mechanism**. They are
multiple effects if the scientific target is just the soft density factor.
No mass-extinction date, imposed rho event, input geography, food/temperature
field, nearest-neighbour search rule or D0 floor should change between runs.
Do not re-fit parameters for the primary matched comparison; any separately
recalibrated comparison answers a different question.

The code uses first-year Euler updates and an analytic solution for the
remaining extinction-free gap; if a gap contains a forced extinction, it
uses annual updates. The two native branches use the respective logistic
and exponential formulas. Thus numerical maps differ along with the
intervention, though their large-finite-K limit agrees in our fixture.
It is not an identical integrator with one multiplication removed. The
source inspection found no additional executable changes to neighbour
selection, activation or event scheduling across these two integrators.

**Do not pass K=infinity into the bounded function.** Its analytic logistic
expression generates inf/inf and NaNs; the fixture records six nonfinite
values. Select `expo` for exact zero capacity feedback. Very large finite K
is only an approximation useful as a control. With positive growth, the
uncapped branch has no finite equilibrium. It is meaningful on a declared
finite horizon with finite initial values/rates and explicit numerical
finiteness checks. Matching equilibria or silently renormalising endpoint
richness would change the intervention.

## Inputs, state and natural domain

The deposited application is continental-shelf marine diversity, genus-scale
continuous alpha diversity, over 541–0 Ma. Inputs are shelf-particle
longitude/latitude/age histories (`Point_ages_xyz.mat`), time-slice food and
temperature (`Point_foodtemp.mat`), the extinction forcing (`rhoExt.csv`),
latitude-dependent longitude windows (`LonDeg.mat`), and the shelf/ocean mask
and target coordinates (`landShelfOceanMask.mat`). Preserve parameter values,
particle ordering, time indices, search windows and extinction forcing across
branches. The time-to-array map is `index = 541-age`; Euler increments are
one Myr. The integration arrays are hard-coded to 542 annual columns, so a
new arbitrary time axis requires code changes.

The selected forward functions contain no random draws. They allocate new
diversity histories; the fixture checks repeat-call determinism and unchanged
caller arrays. Neighbour transfer and iterative orphan filling depend on
previously populated arrays and ordering, so identical input ordering and
activation rules matter. This fixture has no activation or colonisation,
and does not validate those complex paths. Neither native MCMC nor the
unseeded synthetic-data generator is needed for the design check. Future
observation noise needs explicit separate RNG streams. A shared initial seed
in a stochastic simulator would not ensure paired draws after branches diverge.

## Outputs and one candidate spatial statistic

Both branches return per-point diversity histories. The common
`inditek_gridding_alphadiv_2.py:inditek_gridding_alphadiv` takes endpoint
values, averages points within 0.5-degree lat/lon cells and masks non-shelf
or empty cells. `inditek_main` returns only the flattened finite endpoint
vector plus RSS/residuals; use the gridding stage and its coordinates to
retain spatial identity. Keep the full grid and a fixed externally chosen
cell support; do not let a branch-specific finite-value filter choose the
comparison domain.

A possible single statistic is a latitude slope of `log(1+alpha diversity)`
on a fixed set of observed shelf cells, with fixed cell/area weights and
age/region domain chosen by main Codex. Our fixture exercises an unweighted
version on three fixed synthetic cells; it does not select the scientific
statistic or support. The native outputs are continuous local genus-richness
predictions, not taxon identities or occurrences: they support a richness
shape statistic but cannot directly supply compositional beta diversity or
species-level fossil sampling. Native gridding alone is not a fossil
observation model. A fixed sampling/observation operator and its nuisance
parameters must be specified outside these branches before claiming sampled
pattern discrimination. Capacity removal also removes one pathway from food
to diversity; the uncapped branch still retains environmental rate forcing.

## Cheap correctness evidence and limits

The [prospective fixture plan](fixture-plan.md) was committed at `c7ecbbf`
before evaluation. [check_fixture.py](check_fixture.py) calls the real pinned
functions. Three stationary points over two ten-Myr gaps reproduce
independent interval formulas exactly, both with constant positive rates and
with a prescribed extinction year. Zero rates give common diversity one;
K=1e30 reproduces the exponential branch to floating-point precision.
The native grid has the same three finite cells. Illustrative endpoint
latitude slopes are 0.0171864 per degree (bounded) and effectively zero
(uncapped); capacity varies among points while rates are held fixed.
This is a positive control that the pathway can change spatial shape, not
proof it is distinguishable under a real observation model. A reporting check
was strengthened from equal finite-cell counts to equality of the actual
masks; the fixture was rerun with unchanged scientific outcomes.

An independent Codex source review separately compared executable statements
and ran a one-point multi-interval control, confirming the K-cap and
integration qualifications and the invalid K=infinity route. It used the
same archive and is not independent data. Its final turn encountered model
capacity after delivering those findings; no further review is claimed.

Earlier benchmarks establish only selected rate/capacity formulas and three
replayed `proof` proposal diversity vectors. Their saved RSS scores did not
reproduce; the archived inverse chains mix poorly and generating provenance
is unresolved. Those chains are not an initialisation or calibration source
for this contrast. The new fixtures add narrow checks of both integrators,
not recovery validation, full palaeogeographic-path correctness or a verdict
on the paper. See the [earlier review](../2026-10-28-inditek-forward-and-claims/README.md).

The completed gen3sis G3 comparison has eight of ten living-species counts
matching the deposit, but the audited M1 configuration's ecology function
returns abundance unchanged. Its dispersal/speciation controls and rerun
agreement do not qualify a density-feedback toggle; do not substitute those
successes for the required mechanism check.

**Next responder:** main Codex to adopt or reject the full-capacity estimand,
fix one observation statistic/domain and assess the closest-prior distinction
with References. A soft-factor-only estimand needs a new bounded modification
and controls, not relabelling of this native contrast. No new platform or
production ensemble is warranted by this check.

## Full-history viability result (Board 76/2521–2524)

Main Codex accepted the whole-capacity estimand and requested at most two
full forward evaluations at the deposited reference vector
`[161,19,0.035,0.002,2]`. The supplement was declared at `3ee143a` before
execution. [two_map_smoke.py](two_map_smoke.py) ran one `proof` and one `expo`
call without fitting, changing the forcing/history, or shortening the horizon.
It adds the expo-source hash to the prior replay's hash list; no model source
was altered. Both calls completed in **27.488 seconds total** on one CPU.

| Native endpoint | proof | expo |
| --- | ---: | ---: |
| Grid shape | 360 × 720 | 360 × 720 |
| Finite shelf cells | 2,978 | 2,978 |
| Infinite cells | 0 | 0 |
| Minimum finite local diversity | 1.01954 | 1.02028 |
| Maximum finite local diversity | 50.7053 | 1,187.6391 |
| Sum of finite local diversities | 27,499.9518 | 121,768.4899 |

The summed local values are **incidence mass**, not gamma diversity. The
remaining 256,222 cells per grid are native NaNs for excluded/empty support.
An [independent file inspection](map-support-check.json) confirms exact
finite-mask and coordinate equality, not merely equal counts. The
[two-call receipt](two-map-results.json) records paths, hashes, timing,
source/input hashes and all finiteness checks. Raw files are:

- `deep:/data/codex/artifacts/eprp/b005-native-smoke-20261029/proof.npz`,
  SHA-256 `81769f0be286176c871897953c9ada70bdf359fc2e5adfcf53fa8082f2718611`;
- `deep:/data/codex/artifacts/eprp/b005-native-smoke-20261029/expo.npz`,
  SHA-256 `a55f64a8ae01b598510bfca0e8f8d9242d229e94d6efaa3d0b2d76a3a25d4a0d`.

Each NPZ contains `diversity`, `X` and `Y`. The observed-map argument in the
native wrapper only computes its incidental RSS after predicting the grid;
that target is not adopted as B-005's observation law. These results establish
finite endpoints for this one full-history vector, not all parameter space.
Main Codex owns comparison of spatial shape versus scalar change and the
fixed observation/statistic design. No additional forward calls are made.
