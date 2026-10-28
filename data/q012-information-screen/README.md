# Q-012 information screen

**The complete-data oracle passes; the frozen recorded-data detector fails
the power target in both ensembles.** Oracle power lower bounds exceed 0.8,
but this cheap detector achieves only 0.126 and 0.1785 evaluated power. Its
four endpoint-null false-support rates meet the declared limits. This is a
negative result for this fixed detector, not an information limit for all
recorded-data methods. These results do not justify a sampler restart.

The simple comparison is eta=0.05 versus 0.20, with fixed unselected marginal
frailty SD sigma=0.5 and all other nuisances known. The exact likelihood-ratio
ordering uses every generated inheritance edge, including the forced cohort
daughter. [PROTOCOL.md](PROTOCOL.md) gives the factorization, survival-selection
constant, cap interpretation and simultaneous Monte Carlo construction.
[protocol.json](protocol.json) freezes the ensembles and independent seed
ranges. The [independent GPT-6.1 Sol static review](review.md) found no blocking
defect; it is an implementation/mathematical review, not empirical validation.

## Complete-data results

The [full summary](results-oracle-v1/summary.json) and
[all 12,000 replicate rows](results-oracle-v1/rows.jsonl) retain independent
2000-history null calibration, 2000-history null evaluation and 2000-history
alternative evaluation panels for each ensemble.

| Generator ensemble | Optimal power at exact size 0.05: simultaneous interval | Alternative rejection at nominal threshold | Independent null rejection |
| --- | --- | --- | --- |
| Marginal reference, lambda0=0.0708 | 0.823–0.931 | 1754/2000 = 0.877 | 94/2000 = 0.047 |
| Historical size calibration, lambda0=0.096 | 0.989–0.999 | 1990/2000 = 0.995 | 82/2000 = 0.041 |

The simultaneous intervals include uncertainty in the null population
quantile and alternative power, with at least 95% joint coverage across both
ensembles. The nominal-threshold rejection fractions are separate empirical
quantities, not point estimates of power at a known exact 0.05 population
threshold. Exact descriptive 95% intervals for evaluated null size are
0.038–0.057 and 0.033–0.051 respectively.

The histories differ materially from the real record:

| Ensemble | Median recorded N, null / alternative | Pooled present-day censor share, null / alternative |
| --- | --- | --- |
| Marginal reference | 87 / 99 | 34.0% / 36.5% |
| Historical size calibration | 274.5 / 294 | 43.3% / 45.2% |
| Compiled record, descriptive comparison only | 268 | 19.4% |

No caps occurred in any of the 12,000 histories. Caps were retained by design
and tested separately. Random tree sizes and censoring are part of each
ensemble; no history was selected to match the real tree. The oracle takes
262.05 seconds on deep-server, single process, from frozen source commit
`445dd84`. Results include SHA256 hashes of the executed source, generator
and configuration. The [20-history WSL timing](timing/summary.json) took
0.30 seconds and has no inferential role.

## Recorded-data follow-through

The [prospective design](recorded-design.md) was written before viewing the
oracle evaluation and accepted after the oracle passed. Its fixed eight
features combine mortality-risk proxies for recorded relatives with size,
censoring and marginal summaries. One regularized linear discriminant per
ensemble uses independent development histories. Separate endpoint-null
calibration at eta=0 and 0.05 precedes fresh evaluation at both nulls and
eta=0.20. Hidden frailties, true links and simulation cap indicators are
excluded from its inputs. [recorded-protocol.json](recorded-protocol.json)
specifies all 24,000 histories and the error budget.

Production development is complete: 4000 independent histories took 112.12
seconds on deep-server. The
[development summary](results-recorded-development-v1/summary.json),
[development rows](results-recorded-development-v1/rows.jsonl) and
[frozen coefficients](results-recorded-development-v1/coefficients.json)
are retained. Source was frozen at commit `ed8381e`; coefficients were
committed in `ee22c63` before evaluation, with SHA256
`3ac0cea54874ddadd1b3107c4a816fe5cac72d1d1967eb0352e7873b0d7e4d5b`.
The independent 20,000-history calibration/evaluation stage is complete with
that explicit coefficient hash and unchanged source. The
[evaluation summary](results-recorded-v1/summary.json) and
[all calibration/evaluation rows](results-recorded-v1/rows.jsonl) are retained.

| Ensemble | Alternative power at frozen threshold | Simultaneous power interval | False support at eta=0.05 | False support at eta=0 |
| --- | --- | --- | --- | --- |
| Marginal reference | 252/2000 = 0.126 | 0.109–0.144 | 85/2000 = 0.0425 | 56/2000 = 0.028 |
| Historical size calibration | 357/2000 = 0.1785 | 0.159–0.199 | 92/2000 = 0.046 | 59/2000 = 0.0295 |

Thresholds are 0.7673605533 and 0.8859034703 respectively. Each is the maximum
of separately calibrated upper 0.95-quantile confidence thresholds at eta=0
and 0.05; eta=0.05 supplies the higher threshold in both ensembles. All four
independent null estimates are below 0.05 and their exact descriptive 95%
upper bounds are below 0.07. Both detector-only pass flags are false because
alternative power falls far below 0.8 and its lower bound falls below 0.75.

The power intervals and endpoint-null threshold guarantees jointly have at
least 95% coverage across both ensembles, including calibration uncertainty.
The recorded detector uses conservative calibrated thresholds, whereas the
oracle interval concerns optimal power at population size exactly 0.05.
Their power difference therefore does **not** quantify irreducible loss
through observation: the detector is suboptimal and the calibrated sizes
differ. Stronger recorded-data methods remain possible. No post-evaluation
tuning, retry, statistic selection or sampler work was performed.

Recorded calibration/evaluation took 534.25 seconds on deep-server; no caps
occurred in its 20,000 histories. All production stages together generated
36,000 histories in approximately 908.41 seconds of single-process runtime
(0.2523 allocated core-hours). Timing/control histories are separate.

The [recorded-detector review](recorded-review.md) documents its input
boundary, staged coefficient freeze, calibration and interpretation limits.
Separate [oracle reaggregation](results-oracle-v1/independent-reaggregation.json)
and [recorded reaggregation](results-recorded-v1/independent-reaggregation.json)
reproduce the raw-row summaries and confidence bounds. The latter independently
refits the development coefficients and reproduces all 20,000 saved scores
(maximum absolute difference 1.17e-15). Neither check reruns the full generator
or supplies empirical validation.
This screen leaves the posterior/interval contract, informative-negative
power, composite-null performance beyond the two checked endpoints,
prediction, unknown-nuisance recovery, empirical biological interpretation
and sampler readiness unqualified. Main Codex owns programme integration;
any further method should be justified as a new bounded investigation rather
than tuning this detector against its evaluation outcomes.

## Reproduction

From the repository root, use the pinned inline uv environments:

```bash
uv run --python 3.12 data/q012-information-screen/test_screen.py
uv run --python 3.12 data/q012-information-screen/test_recorded.py
uv run --python 3.12 data/q012-information-screen/screen.py run --output /absolute/new-oracle-output
uv run --python 3.12 data/q012-information-screen/recorded.py develop --output /absolute/new-development-output
```

Freeze and verify `coefficients.json` before starting recorded evaluation:

```bash
uv run --python 3.12 data/q012-information-screen/recorded.py evaluate \
  --output /absolute/new-recorded-output \
  --coefficients /absolute/new-development-output/coefficients.json \
  --expected-coefficients-sha256 VERIFIED_SHA256
```

Use new output directories: existing evidence is never overwritten. Route
production panels to deep-server; WSL is used only for small controls and
timing. Source and coefficient SHA checks enforce development/evaluation
separation. The twelve controls cover complete-data density/selection,
stationary variance, cap/cohort edges, exact quantile ranks, recorded-input
leakage, hazard integration, quadrature, sister products, development and
calibration separation, coefficient integrity and disjoint seed panels.
