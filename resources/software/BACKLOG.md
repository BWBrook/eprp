# Validation backlog

Tools to take from T0 (catalogued in [LANDSCAPE.md](LANDSCAPE.md)) to T1–T3,
in tranches. Ranked by register demand (questions served, and whether the
main agents are working on them now), by what the tool makes checkable that
nothing else does, and by readiness (open licence, installable on our hosts).
Proposed by Claude (Opus 5.5), 23 October 2026; not yet started.

Every tranche needs truth to validate against, so the simulators come first:
they generate known histories for every estimator that follows. Where two
generators come from different codebases, each is first checked against
analytic expectations and then against the other.

## Tranche 1: a known-truth bench for origination, extinction and sampling rates

**Run 23–24 October 2026; results in [bench/README.md](bench/README.md).**
FossilSim and paleobuddy pass every generator test (T2; their cross-check
had little power); divDyn passes under complete sampling (T2); PyRate fails
E2 on q, with no undercoverage detected for λ and μ (T2 for that use);
RevBayes' range process is disabled in releases, so it stays at T1 with
E3(b) deferred. All reviewed independently on 24 October. Follow-ups: a
higher-power generator comparison; a pinned `fbdr` build for E3(b),
simulated without fixed-parameter conditioning (L-020); the cause of
divDyn's second-for-third bias. The plan as proposed:

| Tool | Role | Validation planned | Serves |
| --- | --- | --- | --- |
| FossilSim (R) | Generator: trees, taxonomy, fossil sampling | Constant-rate birth–death and Poisson sampling against analytic moments (expected richness, survival probability, fossil counts per unit branch length); pseudoextinction under `sim.taxonomy` | Q-004, Q-006, Q-045 |
| paleobuddy (R) | Generator: time-varying birth–death and fossil sampling | The same analytic checks, then distributional agreement with FossilSim on shared settings (independent codebases) | Q-004, Q-006, Q-012 |
| PyRate (Python) | Estimator: Bayesian rates and preservation from occurrences | Coverage of 95% intervals for λ, μ and q over replicate simulated records, constant and piecewise rates | Q-006, Q-012, Q-045 |
| divDyn (R) | Estimator: three-timer, gap-filler and other binned rates | Recovery of known per-capita rates from binned simulated records, with the documented biases reproduced in sign | Q-040, Q-042, N-002 |
| RevBayes (C++) | Estimator: FBD-range with piecewise rates (`timeline`) | Reproduce one scenario of the published skyfbdr coverage study; then test the stage-binned input form Q-006 needs | Q-006 ([L-001](LEADS.md)) |

Compute: replicate fits on `deep-server` (Docker images per tool), well under
a day on its free cores; nothing long on the laptop.

## Later tranches (order provisional)

2. **The stratigraphic filter and range ends.** StratPal, admtools, paleoAM;
   then an extinction-date benchmark across EDE, Rextinct (GRIWM, CRIWM),
   `tbea` and Alroy's `agnostic.R`, with tranche 1's generators and the
   stratigraphic filter as truth (L-008, L-011; Q-013, Q-017, Q-034, Q-041,
   B-007).
3. **Preparation and palaeogeography.** palaeoverse, fossilbrush,
   `chronosphere` (list its PBDB snapshots, L-005), and a cross-implementation
   check of palaeocoordinates between `palaeorotate` and pyGPlates or
   GPlately (L-010).
4. **Richness estimators.** DeepDive/DeepDiveR, squares, iNEXT and divDyn's
   SQS on the same simulated records with spatial sampling structure (L-006,
   N-002; Q-040, Q-042, Q-045).
5. **Earth-system and spatial simulators.** cGENIE.muffin, pySCION,
   INDITEK-2.0 (licence first), gen3sis with goSPL, and the metabolic-index
   implementations (L-012 to L-015; B-005, Q-001, Q-021, Q-049).
6. **Trait, disparity and comparative tools.** paleoTS and evoTS, mvMORPH,
   dispRity, Claddis, BioGeoBEARS (GitHub), BEAST2 2.7.8 with SA and BDMM.
7. **Food webs.** cheddar's cascade workflow (Dunhill et al. 2024 code), ATNr,
   NetworkExtinction (L-016; Q-011, Q-037, Q-048).
