# Q-012 timed one-dataset prototype of the full working likelihood

Owner: Claude | 16 October 2026 | The next stage cleared by Codex once the
component checks passed (76/1720). It implements the
[finite contract](../../literature/2026-10-16-q012-finite-contract.md),
including Amendment 1.

**It does two things only:**
- measures the cost of one fit at a realistic tree size;
- checks the cohort normaliser and the full target.

It does **not** estimate power, coverage or parameter recovery. Nothing
is fitted to the real data.

## Reproduce

```bash
uv run --python 3.12 data/q012-prototype/prototype.py checks   # active version's checks (v4: with probes and smoke)
uv run --python 3.12 data/q012-prototype/prototype.py fit      # active version's timed fit (v4)
uv run --python 3.12 data/q012-prototype/prototype.py record   # rebuild the fit record from CmdStan output alone
uv run --python 3.12 data/q012-prototype/calibrate.py          # generator size calibration
```

- **v1**: `model.stan`, `checks.json` and `fit_result.json`. These are
  preserved; they were produced at `b683c74`.
- **v2**: `model_v2.stan`, `quadrature.py`, `checks_v2.json`,
  `fit_result_v2.json` and the `v2` block of `config.json`. It follows
  Codex's check (76/1737).
- **v3**: `model_v3.stan`, `checks_v3.json`, `fit_result_v3.json` and the
  `v3` block of `config.json`. It follows Codex's solver-step approval
  (76/1742).
- **v4**: `model_v4.stan`, `inits_v4/`, `checks_v4.json`,
  `fit_result_v4.json` and the `v4` block of `config.json`. It follows
  Codex's robustness ruling (76/1745). This is the 40-node cost result.
- **v5** (active, no laptop fit): the 64-node candidate for the kunanyi
  pilot. Files: `checks_v5.json`, `checks_v5_smoke60.json`,
  `fixtures_v5.json.gz`, `probes_v5_stdout.tar.gz` and the `v5` block of
  `config.json`. It follows Codex's v4 check (76/1750).

- Pinned: numpy 2.1.3, pandas 2.2.3, cmdstanpy 1.2.4, and local CmdStan
  2.38.0.
- Compilation and Stan output go to git-ignored `scratch/q012-prototype/`.
- **Frozen first:** [config.json](config.json) and
  [model.stan](model.stan). config.json also records one declared deviation
  (below).
- **Outputs:** [checks.json](checks.json) and
  [fit_result.json](fit_result.json).

## What is implemented

| Part | Implementation |
| --- | --- |
| Generator | Primary reference: σ 0.5, ρ 0.4 (η 0.2); κ = κ_b = 0; β = 0; k = 1 |
| Rates | Baseline from the data's marginal extinction rates by 3-Myr bin, with a declared floor of 0.065 for the four bins older than 63 Ma; λ₀ 0.0708; b₀ 0.0082 |
| Exposure | AR(1) on 1-Myr bins (φ 0.8), inherited at speciation (ρ_E 0.9) |
| Roots | The 11 roots enter at their observed origins |
| Boundary cohort | Forced design: five roots plus a daughter at 69.81 Ma, all six conditioned on surviving to c = 8.95 (66.05 Ma), by rejection |
| Termination | Piecewise-exponential extinction and bifurcation; bifurcation produces 2 kernel daughters |
| Budding | After entry only |
| Observation | Thinning q(1 Myr) = 0.8 on observed duration; compatible-parent pruning; acyclic ε = 0.06 reassignment; rounding precedence; end labels from recorded daughters only; data-matched Markov exposure observation; past-only lag |
| Working likelihood | Calendar-time baseline as a 25-bin random walk; Weibull age, never reset at entry; extinction and bifurcation terminal factors; budding after entry; time-varying lagged E with a missing indicator; cohort survival before entry; normaliser by 24-node Gauss–Hermite quadrature over the retained graph's components |

## Checks (all pass)

| Check | Frozen seed 20261017 (62 recorded) | Fit seed 20261060 (264 recorded) |
| --- | --- | --- |
| Log normaliser: quadrature against Monte Carlo (10⁶ draws), two parameter points | z = −1.09 and 0.10 | z = −1.09 and 0.10 (the same cohort) |
| Stan target against an independent Python target, as a difference between two points | Error 5.7 × 10⁻¹⁴ | Error 7.7 × 10⁻¹² (3,202 hazard segments) |

## A declared deviation, and a finding for the full experiment

**The frozen seed gave a tree too small to measure cost.**
- It produced only 62 recorded lineages, against 268 in the real tree.
- Over 300 seeds, the reference generator gives a **median of 94 recorded
  lineages**:

  | | 5th percentile | Median | 95th percentile |
  | --- | ---: | ---: | ---: |
  | Recorded lineages | 35 | 94 | 241 |

  Only 4.3% of seeds reach 268.
- **Rates matched to the data's marginal totals do not reproduce its
  realised tree size.** This is the selection and branching effect Codex
  warned about.
- **For costing only,** the fit uses the first seed from 20261017 upward
  whose recorded tree has 240–300 lineages: seed 20261060, with 264
  recorded, after skipping 43 seeds. The rule was declared before the fit.
  No inference is drawn from this fit.

**For the full experiment**, the generator's tree size needs a declared
calibration. Two options for Codex's view:
- calibrate λ₀ by simulation, so that the median recorded size matches
  268;
- condition on the recorded size falling in a declared band.

Either way it is stated as a design choice, not left implicit.

## The timed fit (seed 20261060; 264 recorded lineages; 4 chains in parallel, 1,000 + 1,000 iterations, adapt_delta 0.99, hard limit 1,200 s)

| Quantity | Value |
| --- | --- |
| Wall time | **792.8 s** (13.2 min), inside the limit |
| Cost | About **53 core-minutes** per fit |
| Divergences | 4 of 4,000 |
| Tree-depth hits | 0 |
| Maximum R-hat, core parameters and all parameters | **1.037** |
| Minimum bulk ESS, core and all | **173** |

**These diagnostics are not adequate for decision-grade inference.** R-hat
is above 1.01 and ESS is below 400, so longer chains or a reparameterisation
would be needed.

**90% intervals, with the truth.** This is one dataset, so it shows
behaviour, not recovery:

| Parameter | 5% | Median | 95% | Truth |
| --- | ---: | ---: | ---: | ---: |
| σ | 0.45 | 1.00 | 1.81 | 0.5 |
| ρ | 0.03 | 0.20 | 0.42 | 0.4 |
| **η** | **0.026** | **0.189** | **0.50** | **0.2** |
| κ | −1.12 | −0.39 | −0.13 | 0 |
| κ_b | −0.59 | 0.22 | 1.07 | 0 |
| β | −0.19 | 0.00 | 0.21 | 0 |
| log k | −0.05 | 0.17 | 0.50 | 0 |
| log λ₀ | −3.41 | −3.09 | −2.82 | −2.65 |
| log b₀ | −6.32 | −5.41 | −4.62 | −4.80 |

**Observations**, labelled as observations from one dataset only:
- σ and ρ trade off: σ comes out high and ρ low. η = ρσ is located better
  than either.
- **The intervals for λ₀ and κ exclude the truth.** That is the direction
  the complete-ascertainment working model should be biased under
  thinning:
  - unrecorded short-lived daughters lower the recorded budding rate;
  - because frailty is inherited, high-frailty parents lose more recorded
    daughters, which pushes κ below 0.

  Whether η keeps its decision properties under that misspecification is
  exactly what the finite experiment tests. One fit cannot tell.

## Cost for the full experiment

The finite contract's grid is about 15 core scenarios × 500 replicates,
about **7,500 fits**.

| Basis | Total |
| --- | --- |
| At the measured 53 core-minutes per fit | About **6,600 core-hours** |
| With chains long enough for ESS ≥ 400 (roughly 2–3× more) | About 13,000–20,000 core-hours |

- **Not feasible on this laptop.**
- On kunanyi's permitted 48 jobs × 28 CPUs (1,344 cores): about 5 hours of
  wall time, or 10–15 hours with longer chains. kunanyi needs Barry to
  open the TPAC jumpbox first.
- deep-server's capacity for this has not been checked here.

**Ways to bring the cost down, before any grid:**
1. **Model efficiency.**
   - Vectorise the 3,202-segment hazard sum.
   - Precompute the segment structure.
   - Use within-chain parallelism (`reduce_sum`).

   Likely several-fold.
2. **A smaller grid.** Fewer replicates on scenarios far from the decision
   boundaries, while keeping the Monte Carlo precision the pass rules need.
3. **A cheaper calibration estimator** (Laplace or variational) for the
   grid, with full MCMC spot checks on a declared subset. That would be
   labelled as a change of estimator.

**The generator's size calibration** (above) has to be settled before any
grid as well.

## v2 repairs (16 October, after Codex's check 76/1737)

### Rounding of shared events

- **The rule:** a bifurcation time is rounded once and moved as one time.
  If constraints still fail, the whole component falls back to unrounded
  dates.
- **Near the present:** an observed extinction that would round to 0 Ma
  keeps its label at 0.005 Ma; it does not become a present censor.
- **Fixtures** (`rounding_fixtures`), with Codex's case:

  | Lineage | Dates (Ma) | Label |
  | --- | --- | --- |
  | A | 10 → 1.005 | bif |
  | B | 1.005 → 1.00 | ext |
  | D | 1.005 → 0 | present |
  | E (an extinction at 0.003 Ma) | 5 → 0.005 | ext |

  There are no spurious buds.
- Neither saved dataset needed any rounding repair.

### The cohort normaliser: adaptive Gauss–Hermite

**Method.**
- The integrand is jointly concave in the cohort frailties, so 50 Newton
  steps find its mode.
- The 1-D case uses nodes centred and scaled at the mode. The 2-D case uses
  the joint mode and the Cholesky factor of the inverse negative Hessian.
- 40 nodes.
- `quadrature.py` mirrors the Stan functions exactly.

**Precision gate** (Codex's): log error at most 10⁻⁴, and derivative
error at most 10⁻³, for σ, κ_b and ρ.
- The reference is dense Simpson integration over standard-normal
  innovations on [−12, 12]. Its own convergence is checked: 800, 1,600 and
  3,200 intervals agree to 10 digits.

| Points | Worst log error | Worst derivative error |
| --- | ---: | ---: |
| Central (2) | 7 × 10⁻¹⁶ | 3 × 10⁻¹² |
| Codex's stress point (σ 3, ρ 0.9, κ_b −1.5): v1's 24-node rule was off by 0.17 | 2.0 × 10⁻⁵ | 1.1 × 10⁻⁴ |
| Stress points (σ 1.8; σ 3 with κ_b +1.5; σ 0.05) | 1.7 × 10⁻⁵ | 5.7 × 10⁻⁴ |
| 40 evenly spaced saved v1 states | 5.8 × 10⁻⁵ | 3.0 × 10⁻⁴ |

**The gate passes.** With 24 nodes, adaptive quadrature fails it at the
stress points (log error 3 × 10⁻⁴, derivative error 2.5 × 10⁻³). This
establishes accuracy at the tested points, not a global guarantee.

**Further checks:**
- Monte Carlo cross-check: z = −1.09 and 0.10.
- Stan against Python, as log-density differences:
  - 1.7 × 10⁻¹³ (62 lineages);
  - 8.2 × 10⁻¹² (264 lineages);
  - 6.4 × 10⁻¹⁰ between the central point and the stress point, where the
    difference is 89,221.
- Finite-difference dlp/dσ: Stan −72.072633 against Python −72.072633.

### Baseline random walk and vectorisation

- **Non-centred:** log_h0[j] = log_h0[j − 1] + τ z_j with z ~ N(0, 1), the
  same joint prior. In v1, τ had both the worst R-hat and the worst ESS.
- **Vectorised:** segment sums over contiguous per-lineage blocks, and
  per-lineage terms as dot products.

## Generator size calibration (Codex's work item b)

`calibrate.py` writes `calibration.json`, with seeds and per-seed counts in
`calibration_rows.json`. Fixed before running:
- objective: the median recorded size nearest 268;
- candidates: λ₀ ∈ {0.080, 0.088, 0.096};
- 100 common calibration seeds (40001–40100), then 100 disjoint validation
  seeds (41001–41100);
- a 120 s budget. It used 9.1 s, with no caps.

| λ₀ | Seeds | Median recorded N (5–95%) | Share ≥ 268 | ext / bif / single / present | Median lineage-Myr | Budding / boundary links (median) | Lagged-E availability |
| --- | --- | --- | ---: | --- | ---: | --- | ---: |
| 0.0708 (original) | 30000–30299 | 94 (35–241) | 0.043 | 0.55 / 0.07 / 0.02 / 0.36 | 1,040 | 72 / 14 | 0.670 |
| 0.080 | calibration | 144.5 (39–337) | 0.11 | 0.53 / 0.06 / 0.02 / 0.39 | 1,490 | 115 / 20 | 0.673 |
| 0.088 | calibration | 216.5 (66–510) | 0.30 | 0.50 / 0.06 / 0.02 / 0.43 | 2,183 | 178 / 29 | 0.674 |
| **0.096 (chosen)** | calibration | **276.5 (89–694)** | 0.54 | 0.48 / 0.06 / 0.01 / 0.45 | 2,486 | 231 / 34 | 0.675 |
| 0.096 | **validation** | **296 (67–648)** | 0.57 | 0.48 / 0.06 / 0.01 / 0.45 | 2,705 | 251 / 39 | 0.669 |
| **Observed tree** | — | **268** | — | **0.71 / 0.09 / 0.004 / 0.19** | **2,939** | **208 / 49** | **0.667** |

**Reading:**
- λ₀ = 0.096 calibrates the median size. The spread is wide, which is
  unconditional.
- **The calibrated reference is not realistic in turnover:**

  | | Present at the end | Ending in extinction |
  | --- | ---: | ---: |
  | Generator | 45% | 48% |
  | Observed | 19% | 71% |

  It also has fewer boundary links (34–39 against 49). The real tree has
  more turnover. More censoring means less information per lineage than
  the real data.
- **No further parameter was tuned**, as Codex asked.
- The original-reference panel (seeds 30000–30299) is now saved, and it
  reproduces the earlier 94 (35–241), 4.3% exactly.
- **Options for Codex:**
  - accept size-only calibration, with the turnover mismatch disclosed;
  - add one declared second target (the extant share), calibrated jointly
    with a common multiplier on h₀;
  - use a size-and-turnover-conditioned experiment, labelled as
    conditional.

### The v2 timed fit: timed out (the bound respected, not retried)

The fit used the same dataset (seed 20261060, 264 recorded lineages), the
same sampler settings and the same hard limit of 1,200 s. It was
**terminated at 1,200 s**, against 793 s for v1. See
[fit_result_v2.json](fit_result_v2.json).

**Diagnosis from the partial output** (no new compute):

| | Chains 1–3 | Chain 4 |
| --- | --- | --- |
| Progress at the stop | Sampling, 80–90% done (630–860 saved draws) | Warmup, 600 of 2,000 |
| Divergences | 0 | — |
| Tree depth | Median 7, as in v1 | — |

**Two causes:**
- **Cost.** Each gradient took 0.005–0.0075 s, against 0.0025–0.0034 s in
  v1, so about 2.2 times slower. Automatic differentiation through 50 Newton
  iterations and the 1,600-node 2-D grid outweighs the vectorisation gain.
- **Robustness.** Chain 4 had 85 rejected proposals in early warmup. The
  unsafeguarded 2-D Newton steps overflowed to NaN, and the Hessian
  inversion in `log_pi_2d` then failed.

**Remedies for the next bounded step, not applied here:**
- find the mode with Stan's algebraic solver (`solve_newton`), which gives
  implicit-function gradients and a line search. That makes it both cheaper
  and safeguarded;
- or damp and bound the Newton steps, and use far fewer iterations from a
  good start;
- test whether a nested or lower-order 2-D rule still passes the precision
  gate;
- then repeat one same-dataset cost fit under the same limit.

## v3: the built-in solver (16 October, after Codex's approval 76/1742)

`model_v3.stan` finds each cohort mode with Stan's `solve_newton_tol`
(KINSOL with a line search, implicit-function gradients), started from
zero. **Explicit post-solve checks** reject the proposal with a labelled
message:
- finite mode and score;
- score infinity norm ≤ 1e-8;
- curvature-scaled Newton correction ≤ 1e-8 · max(1, |mode|);
- positive, finite precision (1-D) or determinant and Cholesky factor (2-D).

The 40-node AGH rule, the dataset, the sampler and the 1,200 s limit are
unchanged.

**Declared deviation, made before the fit.** At Codex's starting tolerances
(step 1e-10, score 1e-8) the explicit check rejected a mode that KINSOL had
accepted, at the frozen-seed central point (Newton correction 2.7e-8 > 1e-8):
- KINSOL's score tolerance is a scaled-norm stop;
- when the precision is below 1 (σ > 1), a residual near 1e-8 implies a
  correction above 1e-8.

So the check threshold is now a separate fixed datum (`check_tol` = 1e-8,
unchanged). Only the solver's own tolerances were tightened, to step 1e-12
and score 1e-11. Stability is checked against 1e-14 / 1e-13. See the `v3`
block of [config.json](config.json).

### Prefit checks (all pass; [checks_v3.json](checks_v3.json))

| Check | Worst case over both seeds | Bound |
| --- | --- | --- |
| Rounding fixtures | pass | — |
| Precision gate: central, stress, small-σ, near-one-ρ, saved states | log error 5.8e-5; derivative error 6.2e-4 | 1e-4; 1e-3 |
| Extreme reference (Simpson 1,600 against 3,200) | equal to 10 decimal places | — |
| Stan v3 against Python, lp differences | 6.4e-10 | 1e-6 |
| Solver stability against the tight tolerances | \|Δlp\| = 0 | 1e-8 |
| Stan automatic gradients against central finite differences (σ, ρ, κ_b, log h0₁, log k, γ, log b0, τ, a cohort ε) | relative error 5.3e-5 (τ at the stress point) | 1e-4 |

**Repeated gradients at identical points** (`log_prob` method): v3 took
0.89–0.97 times as long as v2.

### The v3 timed fit: one chain failed, timed out at 1,200 s (not retried)

Same dataset (seed 20261060, 264 recorded lineages), sampler and limit. The
record is in [fit_result_v3.json](fit_result_v3.json):
- `record_from_output` was rebuilt from the CmdStan files alone by
  `prototype.py record`;
- it supersedes the run-time rejection counter, which labelled every
  exception as a warmup rejection.

| Chain | Outcome | Warmup / sampling / total (s) | ms per gradient (sampling) | Divergences |
| --- | --- | --- | ---: | ---: |
| 1 | **Fatal at step-size initialisation:** KINSOL flag −5 (line search did not converge) | — | — | — |
| 2 | No first iteration within 1,200 s, after 3 Hessian rejections at initialisation; the cause cannot be read from the output | — | — | — |
| 3 | Complete | 559 / 460 / 1,018 | 2.80 | 0 |
| 4 | Complete | 397 / 451 / 848 | 3.10 | 0 |
| v1, same measure | All four complete | 495–575 / 140–254 / 656–793 | 1.00–1.30 | 4 |

**Why chain 1 died.** In Stan math (`prim/err/check_flag_sundials.hpp`,
`kinsol_check`), only KINSOL flag −6 (maximum iterations) is a
`domain_error`, which Stan rejects and continues. Every other negative flag,
including −5, is a `std::runtime_error`, which ends the chain. The post-solve
checks never see it.

**Rejections, all chains** (none during sampling):
- 26 "Hessian" rejections at initialisation and 5 in warmup, all reporting
  a NaN precision or determinant. **These are not separable from solver
  failures.** The precision check runs before the mode check, so a
  non-finite mode or input surfaces as a Hessian failure. With positive
  terms only, NaN precision almost certainly means a NaN mode or input, so
  these are best read as non-finite solver outcomes;
- 2 rejections from Stan's own `cholesky_decompose` symmetry check (entries
  of order 1e159);
- 1 initial value rejected for KINSOL maximum iterations, then redrawn.

**The two completed chains**, for information only. This is not a valid
four-chain result.

| | Value |
| --- | --- |
| Maximum R̂ | 1.03 (σ) |
| Minimum bulk ESS | 75 (σ) |
| Median tree depth | 7, as in v1 |
| η, 90% interval | 0.022–0.466; median 0.174; truth 0.2 |
| σ, 90% interval | 0.38–1.72; truth 0.5 |
| ρ, 90% interval | 0.03–0.44; truth 0.4 |

**Reading:**
- Neither completed chain reported a sampling-phase failure. (Codex,
  76/1745, narrowed the original wording, "the solver removed v2's NaN
  failure in the typical set".)
- **Robustness:** a KINSOL line-search failure is fatal in Stan, so a chain
  whose initialisation reaches an extreme point dies.
- **Cost:** the per-gradient cost in sampling is about 2.5 times v1's. The
  likely driver is the 40-node AGH, whose 2-D term has 1,600 nodes. Per
  completed chain the wall time is about 1.3 times v1's: 848–1,018 s against
  656–793 s.

**Options for the next bounded step (not applied):**
- `solve_powell_tol`: its non-convergence paths, maximum iterations and
  residual norm (`rev/functor/solve_powell.hpp`), are `domain_error`
  rejections. Add a finiteness guard on the solver's inputs, and run the
  mode check before the precision check so causes separate;
- an initialisation that stays out of extreme regions: a smaller init
  radius or prior-centred inits, and a smaller initial step size;
- a prefit robustness check: log_prob and its gradient at a few hundred
  initialisation-like points, requiring no fatal exception;
- on cost, test whether a smaller 2-D AGH rule passes the precision gate.

### Calibration regenerated from the final source

`calibrate.py` was rerun unchanged: the same grid and seeds, with no new
candidate search. The earlier outputs are kept as
`calibration_prerounding.json` and `calibration_rows_prerounding.json`.
- 42 of 700 rows changed, as expected, all in endpoint-related fields:
  end labels, link counts and lineage-Myr.
- Every median size, quantile and share ≥ 268 is unchanged.
- End shares moved by at most 0.001.
- λ₀ = 0.096 is still chosen (7.9 s, within the budget).

## v4: Powell solver, guards and declared starts (16 October, after Codex's ruling 76/1745)

**What changed:**
- **Solver.** Both mode solves use `solve_powell_tol`: relative solution
  tolerance 1e-12, Euclidean residual tolerance 1e-11, at most 200 function
  evaluations. Its evaluation-limit and residual failures are domain errors,
  which Stan rejects.
- **Guards, in this order**, each a labelled rejection (`input`, `solver`,
  `Hessian` or `factorisation`):
  1. finite inputs, derived variances (σ², σ²(1 − ρ²)) and initial score;
  2. finite returned mode and score;
  3. residual ≤ 1e-8;
  4. finite positive-definite precision;
  5. finite Newton correction ≤ 1e-8 · max(1, |mode|);
  6. finite covariance factor.

  The 2-D factor is now the closed-form Cholesky factor of the inverse 2×2
  precision, algebraically v3's `cholesky_decompose(inverse_spd(P))`.
- **Algorithm changes, not prior changes:**
  - four frozen initial-value files ([inits_v4/](inits_v4/)), centred on
    the prior locations with perturbations of 0.25 prior scale (rule and
    seed in config.json);
  - initial step size 0.01, below every adapted step size seen so far.

  The prior locations of λ₀ and b₀ equal their generating values, so the
  starts are near the truth for those two.

Everything else is unchanged: model, priors, dataset, 40-node AGH, sampler
and the 1,200 s limit.

### Prefit checks (all pass; [checks_v4.json](checks_v4.json))

- **Established checks.** The precision gate, the extreme reference, Stan
  against Python lp (≤ 6.4e-10), tight-tolerance stability (|Δlp| = 0) and
  automatic gradients (worst relative error 5.3e-5) all pass, with the same
  margins as v3.
- **Repeated gradients at identical points:** v4 took 1.00–1.17 times as
  long as v3.
- **Probes.** 200 fixed points were run through Stan's own initialisation
  (`initialize.hpp`), which reports a `domain_error` as "Rejecting initial
  value" and any other exception as "Unrecoverable error". They took 0.6 s
  of the 120 s budget, with a 10 s cap per point.

  | Points | Initialised | Domain rejection | Unrecoverable, unexpected exit or timeout |
  | --- | ---: | ---: | ---: |
  | 4 selected starts | 4 | 0 | 0 |
  | 6 established points (central, stress, near-one ρ, small σ) | 6 | 0 | 0 |
  | 4 saved v3 states | 4 | 0 | 0 |
  | 93 uniform(−2, 2) unconstrained (CmdStan's default initialisation) | 82 | 11 | 0 |
  | 93 prior-scale points (perturbation 1.0) | 91 | 2 | 0 |

  All 13 domain rejections are Powell residual failures, which are expected
  rejections, not passes. *Corrected (Codex, 76/1750):* the saved examples'
  residual norms span 2.62e-10 to 4.30e13, not "of order 1e9".
- **Smoke check.** Four real chains ran from the selected starts and step
  size, with the fit's seed, for 10 warmup iterations and 1 draw. All four
  finished in 19.6 s of the 60 s budget, with no fatal error and no
  rejection. Their draws have no inferential role.

### The v4 timed fit: completed in 891 s

[fit_result_v4.json](fit_result_v4.json). Same dataset (seed 20261060,
264 recorded lineages), sampler and limit.

| Chain | Warmup / sampling / total (s) | Amortised ms per leapfrog step (sampling) | Divergences | Rejections | Fatal |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | 556 / 324 / 880 | 2.55 | 0 | 0 | 0 |
| 2 | 571 / 277 / 848 | 2.73 | 2 | 0 | 0 |
| 3 | 575 / 316 / 891 | 2.49 | 0 | 0 | 0 |
| 4 | 460 / 371 / 831 | 2.69 | 0 | 0 | 0 |
| v1, same measure | 495–575 / 140–254 / 656–793 | 1.00–1.30 | 4 | — | — |

Median tree depth was 7, with no depth-limit hits. Adapted step sizes were
0.027–0.046.

**Completion and convergence are separate outcomes:**
- **Completion:** all four chains finished within the limit.
- **Convergence is marginal for two nuisance parameters:**
  - 4 of 590 quantities have R̂ above 1.01: lp__ 1.016, σ 1.014, log k
    1.012, x[9] 1.012;
  - bulk ESS is below 400 for σ (172), log k (194) and κ (252);
  - η itself has R̂ 1.005 and bulk ESS 495 (tail 939).
- **Both divergences sit in the upper σ tail** (σ = 2.28 and 2.64; the 99th
  percentile is 2.28), as in the component check.

**90% intervals against the generating values** (one dataset; not a
recovery or coverage result):

| | 5% | Median | 95% | Truth |
| --- | ---: | ---: | ---: | ---: |
| η | 0.029 | 0.192 | 0.492 | 0.2 |
| σ | 0.45 | 0.99 | 1.84 | 0.5 |
| ρ | 0.04 | 0.20 | 0.42 | 0.4 |
| κ | −1.06 | −0.39 | −0.12 | 0 |
| log λ₀ | −3.42 | −3.08 | −2.80 | −2.65 |
| log b₀ | −6.24 | −5.40 | −4.63 | −4.80 |

- As in v1, the κ and λ₀ intervals exclude their generating values. One
  fit cannot attribute this.
- On this dataset neither decision flag would fire: the lower bound 0.029
  is below η₀ = 0.05, and the upper bound 0.492 is above η₁ = 0.20. One
  dataset says nothing about power.

**Cost for planning:**
- Per chain, the wall time is about 1.2 times v1's: 831–891 s against
  656–793 s.
- Sampling seconds per leapfrog step are about 2.2 times v1's (2.49–2.73 ms
  against 1.00–1.30 ms). This is an amortised cost proxy, not a pure
  gradient benchmark (Codex, 76/1750).
- The fit used 3,449.6 summed chain-seconds and about 3,563 allocated
  core-seconds (4 slots × 890.7 s). Neither is measured CPU time or kunanyi
  throughput.
- **Codex's added diagnostics (76/1750):**
  - E-BFMI by chain: 0.278, 0.258, 0.324, 0.326. Two chains are below 0.3.
  - At 40 nodes the precision gate fails at 4 of 8 high-σ or divergent v4
    states. 64 nodes pass all 8.
- Scaling the earlier 6,600–20,000 core-hour extrapolation by about 1.2
  gives roughly 8,000–24,000 core-hours for the full grid. This is a
  planning figure only.

## v5: the 64-node candidate for the kunanyi pilot (Codex 76/1750)

**What changed.** Only the fixed AGH order, 40 → 64 nodes, passed as data.
The model source (`model_v4.stan`), priors, Powell guards, starts and
initial step size are v4's. There is no laptop fit: the long fit is the
kunanyi technical replay ([../q012-pilot/](../q012-pilot/README.md)).

**Why.** Codex found that at 40 nodes the precision gate fails at 4 of 8
high-σ or divergent v4 states, while 64 nodes pass all 8.

### Checks (all pass; [checks_v5.json](checks_v5.json))

| Check | Worst case | Bound |
| --- | --- | --- |
| Old precision gates (central, stress, small σ, near-one ρ, 40 saved v1 states) | log 3.8e-5; derivative 1.9e-4 | 1e-4; 1e-3 |
| Codex's 8 tail states (2 divergent, 6 highest σ) | log 1.25e-5; d/dσ 1.45e-4 | 1e-4; 1e-3 |
| 40 evenly spaced v4 states | log 3.5e-7; derivative 7.1e-7 | 1e-4; 1e-3 |
| Stan against Python lp | 6.8e-10 | 1e-6 |
| Actual AD against finite differences, including the maximum-σ state (row 2869, σ 2.993) | relative error 4.6e-5 | 1e-4 |
| Tight-tolerance stability, including the maximum-σ state | \|Δlp\| = 0 | 1e-8 |
| 200 probes | no unrecoverable error, exit or timeout; 13 Powell residual rejections | — |
| Smoke check (declared 300 s budget) | 4 of 4 chains in 70 s; no fatal error, no rejection | — |

**Further results:**
- **Repeated gradients at identical points:** v5 takes 1.7–2.8 times as
  long as v4 across three benchmark runs (1.9–2.6, 2.3–2.8 and 1.7–2.4).
  The spread follows machine load.
- **The first v5 run failed the smoke check at v4's 60 s budget**, on cost
  alone: 1 of 4 chains complete, no fatal error, no rejection. That record
  is kept as [checks_v5_smoke60.json](checks_v5_smoke60.json). The 300 s
  budget was declared in config before the rerun.
- **Kept durably:**
  - [fixtures_v5.json.gz](fixtures_v5.json.gz) holds the 8 tail states,
    the 40 v4 states and Codex's two fixture outputs, with hashes of the
    source v4 CSVs;
  - [probes_v5_stdout.tar.gz](probes_v5_stdout.tar.gz) holds every probe's
    full stdout. Every probe row is in checks_v5.json.
- **Hash binding.** checks_v5.json records SHA-256 hashes of the model
  source, prototype.py, quadrature.py, the config blocks, the starts and
  the cost dataset. Since Codex's prelaunch check (76/1765) it also covers
  every saved-draw CSV bank the checks read: the v1 states, the v2
  benchmark points, the v3 probe states and the v4 tail states. `fit()` and
  the pilot's `build` refuse stale checks.
- **A harness defect, found while refreshing the binding.** `smoke()`
  reused its output directory, so the second smoke run counted the first
  run's chains (8 found, 4 expected) and failed. Earlier output is now
  moved aside, labelled superseded, before each run. The checks were then
  rerun in full.

## v6: partial non-centring candidate (Codex 76/1814)

**Why.** R00 failed the E-BFMI screen. Codex showed that for any fixed
Gaussian metric, the stationary limit of CmdStan's E-BFMI is
d / (Var(U) + d/2), with d = 299. R00's Var(U) predicts the failures, so a
dense metric cannot remove them; a nonlinear reparameterisation can.

**What changed.** [model_v6.stan](model_v6.stan) is v4/v5 with fixed
a = 0.2:
- the free parameter is w = σ^a ε, with w ~ normal(0, σ^a);
- ε = w / σ^a is reconstructed, and x, the likelihood, the normaliser and
  every other prior are unchanged;
- the normal density supplies the inverse-map Jacobian, −aN log σ, exactly
  once.

The starts (`inits_v6/`) are the R00 starts mapped exactly. The config is
frozen in the `v6` block.

**Checks (all pass; [checks_v6.json](checks_v6.json)):**
- **Actual-Stan identity against v5** at 60 points: the 4 mapped starts;
  central, stress, near-one ρ and small σ; σ = 0.01 and 0.001; and
  Codex's 48 R00 states, up to σ = 3.237.
  - log identity, lp_v6 − lp_v5 + aN log σ: worst 2.9e-11 (tolerance
    1e-7);
  - ∇w = σ^−a ∇ε, ∇log σ, and all other gradients: worst scaled error
    9.2e-13 (tolerance 1e-6);
  - every value finite.
- **200 mapped probes:** the same outcomes as v5, with no unrecoverable
  error.
- **Smoke check:** four chains in 25 s, no fatal error, no rejection.
- **Binding** adds the reference model, its starts and the R00 draw bank.

Passing these checks establishes equivalence and that v6 runs. It does not
show that the geometry near σ = 0 is harmless; the R00 comparison tests
that.
