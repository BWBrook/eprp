# PhanDA adjacent-stage GMST differences under stated dependence scenarios

Owner: Claude. Built 9 October 2026. Status: **sensitivity analysis**, not a
temporal posterior. Requested in Correspondence 77, message 1155. It applies the
dependence scenarios in
[Codex's PhanDA contract note](../../literature/2026-10-08-phanda-ensemble-contract.md).

PhanDA assimilates each stage separately, so there is no joint temporal
posterior. This analysis shows how far a stage-to-stage difference in global
mean surface temperature, ΔGMST = younger − older, depends on the coupling
assumed between stages. Every result describes a difference between
reconstructed stage *states*. None is a within-stage pulse magnitude or duration.

## Rebuild

```bash
uv run data/phanda-stage-differences/build.py
```

The script reads `PhanDA_GMST_ensemble.mat`, pinned to commit 9f06c0d, and
checks its SHA-256 (`6213e816…`). It fetches the file into ignored `data/raw/`
if missing and writes the full table to ignored
`data/derived/phanda-stage-differences/stage_differences.tsv`. That table has
84 adjacent pairs × 4 couplings, with mean, SD, 5/50/95% quantiles and a
sign-resolved flag. The raw source declares no licence, so derived values stay
untracked and only the summaries below are recorded. The script uses a fixed
seed and runs in about 5 s.

**Sample construction.** The script uses `ScenarioAll`, split into 1,440-value
blocks. Block *j* belongs to scenario *j* mod 12: `combineruns.m` pads each
scenario to 1,440 values by resampling, and for merged slices `combinestages.m`
concatenates the two stages' vectors. The per-scenario columns of the six merged
rows do not reproduce `ScenarioAll`; using them shifted the Anisian/Olenekian
median by 1.7 °C. With `ScenarioAll`, the equal-weight pooled median matches the
deposited `GMST_50` to within 0.002 °C for all 85 slices.

## Couplings

Each scenario is weighted equally, as in PhanDA's own pooling.

| Coupling | Construction | Role |
| --- | --- | --- |
| `shared_label_independent` | Same correction scenario for both stages, with independent draws within it | Keeps the structural correction choices that are common across time (pH, seawater, R method) |
| `fully_independent` | Scenario and value drawn independently for each stage | Also breaks the shared scenario identity |
| `quantile_aligned` | Comonotone coupling of the pooled marginals | Minimum variance of the difference for these marginals |
| `reverse_quantile` | Countermonotone coupling | Maximum variance of the difference |

The two quantile couplings bound only the *variance* of the difference for fixed
marginals. They are not bounds on every interval or tail probability.

## Results (9 October 2026)

**Direct output**

| Coupling | Median SD of ΔGMST over 84 pairs | Pairs whose 90% interval excludes 0 |
| --- | --- | --- |
| quantile_aligned | 0.64 °C | 64 |
| shared_label_independent | 2.93 °C | 17 |
| fully_independent | 3.56 °C | 9 |
| reverse_quantile | 5.09 °C | 5 |

The ratio of reverse to aligned SD has median 7.8, with a range of 2.5–42.5
across pairs. The point estimates (medians) of ΔGMST barely move between
couplings; the spread does.

**Event-adjacent transitions.** Values are ΔGMST in °C as median [5%, 95%]
under the shared-label coupling.

| Transition (older → younger) | Shared-label | Sign resolved under all four? |
| --- | --- | --- |
| Changhsingian → Induan | +10.6 [+5.5, +15.6] | Yes |
| Thanetian → PETM | +7.7 [+4.3, +13.4] | Yes |
| Albian → Cenomanian | +7.8 [+3.0, +13.2] | No: not under reverse or full independence |
| Katian → Hirnantian | −6.8 [−11.8, −2.4] | No: shared-label and aligned only |
| Wuchiapingian → Changhsingian | −4.0 [−8.7, −0.2] | No: shared-label (just) and aligned only |
| Maastrichtian → Selandian/Danian | +4.4 [+1.6, +7.8] | No: not under reverse |
| Frasnian → Famennian | −4.3 [−8.5, +0.5] | No |
| Pliensbachian → Toarcian | +1.9 [−4.5, +6.7] | No |
| Norian → Rhaetian | −2.7 [−7.8, +2.1] | No |
| Rhaetian → Sinemurian/Hettangian | +2.9 [−2.5, +9.0] | No |

**Inference, to be challenged**

1. **The coupling assumption, not the data, decides whether most stage-to-stage
   temperature changes are resolved.** Five of 84 pairs keep their sign under
   every coupling:
   - three large changes: Tournaisian → Visean (−8.7), Thanetian → PETM (+7.7)
     and Changhsingian → Induan (+10.6);
   - two young transitions with narrow marginals: Tortonian → Messinian and
     Upper Pleistocene → Holocene.
2. **The defensible coupling lies between shared-label and quantile-aligned.**
   Separately fitted stages still share a prior model family (HadCM3L) and
   proxy-system parameters, which plausibly induces positive dependence beyond
   the scenario labels. That dependence is unquantified.
3. **Consequence for candidate B.** A stage-state ΔGMST dose axis is
   informative for the high-dose tail but weak for the background bulk. A
   continuous dose–selectivity regression would therefore need an explicit
   errors-in-variables model, and its low-dose slope will be weakly constrained.
   Whether a richer dose functional, such as within-stage proxy maxima,
   resolves the bulk is open.
4. **Some event transitions do not show the expected warming at stage grain.**
   The end-Triassic and Toarcian are examples. Their events are sub-stage pulses
   that stage means dilute, consistent with the crosswalk's support-mismatch
   finding.

## Limits

- Marginals are PhanDA's pooled posteriors as deposited. Padding duplicates are
  kept because PhanDA's published percentiles include them.
- No assimilation was re-run, and no temporal coupling was inferred.
- Sharp bounds on a specific threshold-exceedance probability would need a
  separate extremal-coupling calculation for a pre-specified statistic.
