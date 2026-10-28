# Q-012 information screen

**The complete-data oracle passes in both declared generator ensembles.** Its
95% simultaneous power bounds at population size 0.05 exceed 0.8. This rules
out an information-based stopping argument for the complete-data experiments;
it supports trying the frozen cheap recorded-data detector. It establishes
neither recorded-data power nor recovery by the existing sampler.

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

Production recorded-data development and evaluation are pending. A passing
detector would establish only that information survives this simulator's
observation map at known nuisances. Its failure would apply to this fixed
cheap statistic and would never establish an information limit. The
posterior/interval contract, informative-negative power, composite-null
performance, prediction, empirical biological interpretation and sampler
readiness remain unqualified by this screen.

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
