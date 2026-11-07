# Pacific variability: bounded counting and precision diagnostics

8 November 2026. Barry forwarded Claude's Board 144/2970 assessment and next
action to main Codex. Main owns this directory. This specifies diagnostics
before window outcomes or simulations are computed; source schema, coverage,
and the following training-only abundance summaries have already been viewed.
This is not a frozen forecast evaluation or a fitted biological test.

## Observation and training domain

Use the unchanged original Fig. 1 workbook, SHA256
`5fc615afdf94fa7842375e9c34b98d1f87f41e29700ef97da11b149eb59c7caa`.
Restrict to Site 1209 (normalising the optional U prefix), source investigator
SA, and the previously specified half-Myr landmarks 56.5–65.5 Ma. These
nineteen candidates avoid investigator changes. Each older predictor window
is `(t,t+0.15]` Ma and each later outcome window `[t-0.15,t)` Ma; larger Ma
means earlier time. Keep original observations and no interpolation.

Taxon selection uses the 420 SA samples at 60.15–65.9 Ma only. Among the 60
original abundance fields, exclude `total_remaining_nannos` and
`calcisphere_fragments`; require explicit numeric observations in every
training row, a positive observation in >65% of those rows, and mean relative
abundance >=1%. Keep every qualifying taxon; do not force eight. Initial
training inspection shows six qualify. Zeros remain zeros; blanks are missing.
Do not change this set after seeing window or simulation results.

Require >=3 complete original rows in each window and all selected fields
numeric. Record any excluded row/window. An all-zero taxon mean makes summed
CV undefined; report that result instead of removing the taxon or setting its
CV to zero. The fixed-training-scale variance below remains defined there.

## Counting scenarios

The public accepted manuscript, Methods lines 314–318, states counts of
500–1,000 liths per sample. Primary scenarios are multinomial N=500 and1000.
Stress scenarios N=250 and2000 test counting depth; Dirichlet-multinomial
design effect D=2 at N=500/1000 tests within-sample overdispersion. These are
working models, not estimated denominators or certified observation bounds.
Generate 4,000 independent replicates per window/scenario, seed20261108.

Use joint selected-taxon probabilities plus a residual other category. Do not
close the selected taxa to one. Two frozen-composition diagnostic nulls use:
(a) the earlier window's mean composition, which is available before the
outcome; (b) the later window mean, an offline plug-in diagnostic that must
never enter a forecasting baseline. Each null holds that composition constant
across the later window's actual number of original observations. N and
overdispersion are fixed within a scenario. No within-window ecological
variation is simulated. Neither null accounts for preservation, age errors or
among-sample counting dependence.

For proportions P_j, summed CV is `sum_j sd(P_j)/mean(P_j)` using sample SD.
The population marginal counting CV `sqrt((1-p)/(Np))` is not the expected
finite-window summed CV. Estimate the latter by simulation. Retain the
frequency of undefined simulated CV; quantify finite draws only with that
qualification. Compare the *between-window* dispersion of null means and
within-null spread with observed dispersion, without calling their ratio an
identified biological counting-noise share. Plug-in p uses noisy observations.

Also evaluate `V=sum_j s_j^2/a_j^2`, where positive a_j are fixed training
mean proportions. Under independent unbiased observations with fixed
within-window p, its expected counting component is
`D/N * sum_j p_j(1-p_j)/a_j^2`.
For changing latent p_i, the ordinary sample-variance identity is additive in
within-window ecological variance and mean marginal observation variance.
This supplies a better behaved alternative for zeros, not known latent
ecological variability. Negative noise-corrected estimates must not be clipped.

## Dependence and precision

Report lag-1 correlation and finite AR(1) effective-n diagnostics for observed
older-window and later-window variability over complete consecutive landmark
pairs. These are response diagnostics, not estimated precision of a forecast
gain. Do not use negative estimated correlation to inflate n above its row
count; preserve the raw correlation and qualify the heuristic.

For squared-error score, define paired gain D=L_baseline-L_enriched. A
precision claim concerns the dependence and SD of D, which are unknown before
predictions. Report an explicit *conditional* known-variance Gaussian grid:
two-sided alpha=.05, targetpower=.8, AR(1) correlations0,.25,.5,.75,.9 at
half-Myr spacing, and SD(D)/baselineMSE c=.25,.5,1,2. Compute the exact
finite covariance of the sample mean, retaining gaps in landmark spacing.
Use `z(.975)+z(.8)` as the usual normal-approximation detection threshold.
Estimation uncertainty, fitted-model uncertainty, nonnormality and regime
changes are excluded, so these are design sensitivities, not a power guarantee.

Report all19 candidate windows, the11 older training landmarks>=60.5Ma,
and the7 possible same-investigator evaluation landmarks<=59.5Ma. The60.0Ma
landmark is reserved as a temporal separation; it is not evaluated as a test.
The illustrative consequential target is **10% baseline-MSE reduction**.
This is an analyst-declared pilot criterion, not a known biological threshold.
For each rho and sample set, solve the maximum c compatible with that target.
Do not infer failure for every method from an assumed grid value of c.

## Decision boundary and delivery

This tranche ends with observed aggregate diagnostics, conditional noise/null
comparisons, a precision sensitivity table, and the independent Walvis source
check. No forecast fit or post-result taxon/window changes are part of it.
If raw summed CV is undefined or dominated by plausible counting scenarios,
recommend the declared variance alternative or stop that endpoint. A positive
precision clearance requires justified paired-loss uncertainty; response ESS
alone cannot provide it. Preserve unresolved uncertainty and recommend the
smallest decision-relevant next action. Raw window vectors and simulations
stay ignored; only code, aggregate results and scientific interpretation enter
the public repository.
