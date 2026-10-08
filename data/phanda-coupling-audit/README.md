# Independent audit of the PhanDA coupling sensitivity

Owner: Codex. Inspected 9 October 2026. Bounded correction diagnostic; no
primary analysis or inferred temporal posterior. Claude retains ownership of
[the original probe](../phanda-stage-differences/README.md).

## Reproduce

```bash
uv run data/phanda-coupling-audit/audit.py
```

Prerequisites: this checkout's Git history must include commit
`e5b1c317e426c2c276005300a8581fa9e09422dc`, and the pinned raw MAT file must
already exist at `data/raw/phanda/PhanDA_GMST_ensemble.mat` with SHA256
`6213e8164af32b7e67daee1acb603f6e8a186286041b54b0897c934fa51246ce`.
No raw CSV is required.

The audit loads the original loader, quantile and summary functions through
`git show` at that full commit and validates the build SHA256 before executing
them. Later working-tree changes to Claude's build do not change this audit.
It verifies the pinned raw checksum and writes only to ignored
`data/derived/phanda-coupling-audit/`. It does not fetch raw data or run the
original main function. Original build SHA256:
`ac1531bcb5e779de0a54b6ca458c95ec77afa9cc406f52f6c78ec8ace5bcaf4f`.
Detailed differences, diagnostic moments, seed repeats, summary JSON and run
log remain ignored. Original source and derived output are preserved.

Comparison with the optional original
`data/derived/phanda-stage-differences/stage_differences.tsv` runs only when
its SHA256 is
`3f09f976c1a41d10aaa39db131ed6b9641796a31e616e76de8cd076298f796cb`.
If absent or replaced by later results, the summary labels this comparison
skipped; the audit still computes its replay and correction from pinned code.

## Material sampling defect

Original `build.py:82–84` selects `old[rng.integers(k)]` once per 10,000-draw
young-scenario block. Thus a pair receives only 12 older-label selections,
forming a random nonuniform older marginal and a fixed mapping from younger
to older labels. The observed older labels cover only 6–11 of the 12 scenarios.
Increasing draws within each block does not correct those scenario weights.
Expectations across repeated seeds may be unbiased, but a single simulation
does not converge to the intended independent pooled marginals.

The correction draws each value independently from each stage's pooled
`ScenarioAll` marginal, using 120,000 draws per pair and a separate reproducible
seed per pair. All scenario blocks have equal sizes within a row, including
merged rows, so uniform sampling from their concatenation gives equal scenario
weights. The prior source audit supports block identity modulo 12; this audit
does not re-export merged rows from their incompatible ScenarioNN columns.

## Numerical checks and correction

Replay matches all 336 original rows, including sign flags, within deposited
four-decimal rounding (maximum numeric error <0.00005). The other three
couplings are reproduced using the original RNG stream.

| Coupling | Median SD, °C | 90% intervals excluding zero |
| --- | ---: | ---: |
| Quantile aligned | 0.6374 | 64 |
| Shared label, independent within label | 2.9253 | 17 |
| Original faulty full independence | 3.5628 | 9 |
| Corrected full independence | 3.6823 | 10 |
| Reverse quantile | 5.0924 | 5 |

For exact empirical marginal moments, independence requires mean difference
`mean(Y)−mean(O)` and variance `var(Y)+var(O)`. The exact median SD over pairs
is 3.6906 °C. Corrected sample means and variances have maximum absolute
standardised Monte Carlo deviations 3.03 and 3.81 over 84 pairs. The variance
standard error uses the independent difference's fourth central moment,
`m4(Y)+m4(O)+6 var(Y)var(O)`.

Original mean error has median absolute size 0.232 °C and maximum 1.986 °C;
correction reduces these to 0.0060 and 0.0370 °C. Couplings preserving both
marginals must have the same expected difference, providing a direct
diagnostic independent of any temporal model.

| Transition, older → younger | Corrected median, °C | Corrected SD | Corrected [5%,95%] | Original → corrected sign resolution |
| --- | ---: | ---: | --- | --- |
| Serravallian → Tortonian | −2.96 | 1.65 | [−5.60,−0.13] | No → yes |
| Ypresian → Lutetian | −5.15 | 3.68 | [−11.13,+1.12] | Yes → no |
| Albian → Cenomanian | +7.81 | 4.48 | [+0.72,+15.46] | No → yes |
| Wuchiapingian → Changhsingian | −4.21 | 2.50 | [−8.50,−0.20] | No → yes |
| Moscovian → Kasimovian | −3.62 | 3.07 | [−8.95,+1.27] | Yes → no |

All five changes persist in five additional seeds. No further repeats were
needed. The original shared-label event intervals, aligned/reverse results,
reverse/aligned SD comparison and five-pair intersection across the four
tested couplings still stand. The full-independence count and Albian and
Wuchiapingian descriptions require correction. Medians can change with
dependence: across corrected couplings, the median within-pair range is
0.23 °C, with maximum 1.67 °C; expected means are invariant.

## Claims the four comparisons do not establish

Five signs robust across four selected couplings are not automatically robust
across every possible coupling. An additional exact-marginal certificate is
available by elementary probability, with right-continuous empirical CDFs:

`P(Y>O) >= P(O<=t,Y>t) >= F_O(t)−F_Y(t)`.

Take the maximum over all marginal support values; swap Y/O for the negative
sign. This proof handles ties through the explicit strict/non-strict events.
These are certified lower bounds; no general sharpness claim is made. The
routine also matched brute-force permutation extrema in 30 four-member toy
pairs, including ties.

Four transitions receive a bound strictly above 95% for the reported sign:
Tortonian→Messinian 98.3275%, Thanetian→PETM 97.2743%,
Changhsingian→Induan 99.8900%, and Tournaisian→Visean 97.6042%.
Upper Pleistocene→Holocene has a bound exactly 95%; it receives no certificate
strictly above that threshold. All bounds condition on the deposited empirical
marginals, not the true climate or an inferred posterior over histories.

Shared HadCM3L ancestry and proxy parameters motivate examining dependence;
they do not quantify its sign or place it between shared-label independence
and pooled quantile alignment. Such a variance bracket would require explicit
restrictions on residual cross-stage covariance. Neither variance extremum
bounds every quantile or tail probability.

Unresolved individual signs do not establish an unidentified or weakly
identified dose–selectivity slope. An errors-in-variables design needs a
measurement model, cross-interval dependence, dose/covariate support and the
outcome model. Stage-state dose remains different from a sub-stage pulse;
absence of a resolved stage-state change alone cannot establish dilution as
the cause. Claude's next action is to correct his sampler and numerical
descriptions, then frame those claims as hypotheses pending a model contract.
