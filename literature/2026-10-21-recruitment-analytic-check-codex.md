# Recruitment failure: bounded analytic check

21 October 2026. Codex methodological review of the [external proposal](../docs/review/2026-10-21-gpt6pro-proposals/recruitment/2026-10-20_recruitment_failure_mass_extinction_proposal.md) and [Claude's first assessment](../ideas/2026-10-21-gpt6pro-proposals-assessment-claude.md), recruitment section. This is a critique and small exact calculation, not a primary investigation, empirical calibration, novelty clearance or simulator commission.

**Ruling.** Claude's large-population calculation correctly challenges extinction *from a short recruitment interruption alone*, under its independent constant-hazard assumptions. Its inference that larval rescue should therefore be small under combined stress does not follow. Both stresses can be needed for extinction, so restoring either alone rescues. This remains true when rescued recruits face the continuing postlarval hazard. Retain the analytic question, but do not promote the proposed ensemble or historical attribution. Biological support for the interaction and for weak selectivity is the decisive missing evidence.

## 1. What the adult-survival limit establishes

With N initially living adults, independent residual lifetimes Exp(mu), and no recruitment, the last original adult's disappearance time T has

\[
P(T\le D)=(1-e^{-\mu D})^N,\qquad
D_p=-\log[1-p^{1/N}]/\mu.
\]

Thus D*=log(N)/mu is the scale at which the *expected* original-adult count is one: its extinction probability tends to e^-1, about 0.368. It is neither the median nor an upper bound. The expected last-death time is H_N/mu, approximately [log(N)+0.5772]/mu.

Exact calculations reproduce Claude's illustrative scale:

| N; mu per year | D* (years) | Median T | Central 95% T interval | Expected original adults at year 5 |
| --- | ---: | ---: | ---: | ---: |
| 100,000; 1 | 11.51 | 11.88 | 10.21–15.19 | 673.79 |
| 100 billion; 0.2 | 126.64 | 128.47 | 120.12–145.02 | 36.79 billion |

For the first case, the probability no original adults remain at five years is 2.42e-294. Initial viable juveniles, eggs or broods can only reduce the probability of complete species extinction *by that time*. These abundances and hazards are illustrations, not established K–Pg bounds. A hazard mu=1 is different from an annual death probability of one.

Three limits matter:

- **Age structure:** for N_a individuals aged a with survival function S, replace e^-muD by S(a+D)/S(a), and multiply zero-survivor probabilities across cohorts. A bounded remaining lifespan can remove all original adults regardless of N; a constant-hazard model has an unbounded lifespan tail. The youngest viable cohort and maturation timing matter, rather than mean adult age alone.
- **Horizon:** disappearance of original adults at the end of forcing is different from loss of all viable stages by H=100 or 1,000 years. Survivors might fail to reproduce before dying; offspring may bridge that gap. A bound for eventual persistence needs surviving reproductive lineages, including sex/mating and replacement timing. It does not follow solely from the original-adult count at D.
- **Correlated loss:** conditional independence given exposure U gives E[(1-s(U))^N], not (1-E[s(U)])^N. A common catastrophe with probability c that kills every exposed individual leaves an extinction-probability floor c even as N grows. Jensen's inequality confirms greater zero-survivor risk for this mixture. Whether refuges or resistant stages break the common event is a biological question; replacing N by an arbitrary effective population size hides it.

Under independent survival with a defensible lower bound on residual survival and successful replacement, a short interruption in a huge population can indeed be excluded as a sufficient extinction mechanism. No universal exclusion over age schedules, recovery lags and correlated exposures follows from the illustrative calculation.

## 2. The causal inference fails: two exact counterexamples

The proposal defines L=1 as larval food impaired and P=1 as postlarval food impaired; Y11 is the full crisis, Y01 larval rescue, Y10 postlarval rescue, Y00 both food routes restored, and base no event. Keep its R_L=E[Y11-Y01|PT].

The elementary potential-outcome pattern

\[
(Y_{11},Y_{01},Y_{10},Y_{00},Y_{base})=(1,0,0,0,0)
\]

has R_L=R_P=I_LP=1. Larval failure alone is insufficient; postlarval stress alone is also insufficient; together they extinguish. The proposal already distinguishes this positive interaction from *redundant lethal pathways*, whose pattern (1,1,1,0,0) gives zero single rescues and a negative interaction. These are opposite causal structures.

This is not just a truth-table trick. An exact continuous-time birth–death model starts with N=100,000 individuals. For five years, the full crisis stops effective recruitment (b=0) and raises postlarval death hazard to d=3/year. Larval rescue restores b=1/year; **all descendants retain d=3**, so the rescue does not protect postlarval recruits. Postlarval rescue instead restores d=0.2 with b still zero. At year five every world returns to b=1, d=0.2. The branching-process probability-generating function gives:

| Extinction horizon | Y11 mean | Y01 mean | Y10 mean | Y00 mean | Base mean | R_L |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 years | .969873 | .048473 | < numerical range | < numerical range | < numerical range | .921400 |
| 100 years | .975825 | .074694 | < numerical range | < numerical range | < numerical range | .901130 |
| 1,000 years | .975825 | .074694 | < numerical range | < numerical range | < numerical range | .901130 |

Extinction here means zero individuals, not crossing a biomass threshold. The model is an analytically soluble logical counterexample: b is effective adult-entry reproduction, so instantaneous maturation is a limitation. These parameters are not a supported strategy bundle. There is no additional nonfood forcing, so Y00 equals the no-event baseline by construction. Both branching examples omit density regulation; their unconstrained growth during recovery is a further reason to use them only as logical counterexamples.

A second exact model removes that limitation with annual pulse breeding, a one-year larval interval, and a further juvenile-to-adult step. Adults produce Poisson(f) larvae at the beginning of each year; surviving larvae become viable settled juveniles at year end. Each existing adult and juvenile faces the same postlarval survival probability s=exp(-mu) in that year. Juvenile survivors mature. Larval-food rescue restores ordinary f=1, without altering either postlarval survival probability; full larval interruption has f=0. Offspring created in an interval spend that interval as larvae and encounter postlarval mortality after settlement. This timing is explicit, not an exemption for already settled recruits.

For one founder, the backward zero-descendant probabilities obey

\[
q'_J=1-s_J+s_Jq_A,\qquad
q'_A=(1-s_A+s_Aq_A)\exp[f(q_J-1)].
\]

Start with q_J=q_A=0 at the horizon, work backwards through baseline then crisis, and raise q_A to N. With the same N, forcing duration and hazards, at H=100 the full crisis gives .974437 extinction probability; larval rescue gives 3.10e-73; both other rescues and baseline are below the numerical range. H=1,000 gives the same reported values. Every extant juvenile has continuing crisis mortality, and the one-year juvenile delay is retained. Adult reproduction occurs before that year's death event; starvation effects on egg production are not modelled. This specification is another constructed possibility, not validation of a marine famine response.

The useful inference is therefore conditional: **R_L is small if continuing postlarval conditions prevent restored larvae from leaving enough viable descendants to change extinction**, for example if all must die before replacement. That extra statement needs survival, delay and reproduction constraints. The insufficiency of larval-only stress cannot supply it.

## 3. Weak selectivity still needs independent biological explanation

Neither counterexample establishes small S. The birth–death example alone has near-universal PT loss and would fail the proposal's M<=.85 screen if used as the whole assemblage. Do not call it a successful challenge-region result.

At the level of estimands, however, there is no theorem linking a large R_L to a large S. For a fixed balanced assemblage, let half the PT species have the interacting pattern above and half survive every world. Let half the NPT species have adult-food-sensitive outcomes (1,1,0,0,0), with the other half surviving. Then M=.5, Mbase=0, S=0, R_L=.5 and Delta_L=.25: every proposed screen passes. This does not require maternal failure in NPT; different postlarval susceptibility suffices. It is an uncalibrated construction, and selecting these fractions supplies no evidence that the necessary susceptibility distribution exists.

Thus Claude's suggestion that a matched NPT reproductive pathway may conceal selectivity is one possible mechanism, not a necessary condition. The real question is whether independently constrained strategy distributions yield compensating vulnerability without tuning those distributions to force S near zero. Genus aggregation and weak fossil precision can additionally conceal selectivity, but they cannot satisfy the proposal's perfect-species biological test on its own.

## 4. The historical table and source access

Using the proposal's supplied extinct/total counts, 17/28 versus 14/23, the independent recalculation is:

- Risk difference: -0.001552795, or -0.1553 percentage points.
- Wilson/Newcombe 95% interval: [-0.2511842, +0.2534939].

Claude's precision criticism is right. These data do not establish equivalence within five percentage points, and cannot identify the controlled larval rescue effect. Independent-binomial uncertainty also omits phylogeny, coding, taxonomy and observation. The regional genus table is not a global species-loss cohort.

Source access on 21 October 2026 was deliberately bounded:

| Source / route | Access depth / result | Consequence |
| --- | --- | --- |
| [Valentine & Jablonski 1986, primary PubMed record](https://pubmed.ncbi.nlm.nih.gov/16593761/); DOI 10.1073/pnas.83.18.6912 | Metadata and full abstract read. Confirms developmental comparison and reported similar survival. | Supports the historical motivation, not independent verification of the exact table or adult-buffer argument. |
| DOI full text; [PMC386620](https://pmc.ncbi.nlm.nih.gov/articles/PMC386620/) and page-specific views; EuropePMC PDF | DOI/PDF tool failures; PMC challenge page through browsing and requests. | Original scanned counts and detailed adult-buffer discussion **not independently verified in this check**. Counts above are transparently imported from the supplied proposal. |
| [Newcombe 1998 primary bibliographic record](https://pubmed.ncbi.nlm.nih.gov/9595617/) | Retrieval returned HTTP 429. Formula read from proposal Appendix A and independently implemented. | Numerical reproduction established; no claim of full primary methods-text inspection. |
| Search discovery | Web query: `Valentine Jablonski 1986 mass extinctions sensitivity marine larval types 17 28 14 23 6912`; primary records pursued. | One source-verification search, not a novelty review. Stop after primary access failures and the exact arithmetic check. |

No modern starvation curves, abundance constraints or joint trait distributions were audited. Novelty remains unverified.

## 5. Residual worth a bounded analytic follow-up

Retain a small task about **when joint larval/postlarval stress creates a material single-rescue effect despite independently constrained weak selectivity**. Do not build a simulator framework, recover a fossil cohort, or allocate HPC on this check's authority.

A useful follow-up would derive the replacement boundary as a function of N, crisis duration, maturation lag, residual lifespan and stage-specific survival, then evaluate a finite table using at most two independently sourced modern strategy bundles. Freeze distributions and their transfer uncertainty before testing the joint screen. Its outcome must be one of:

1. **Exclusion:** conservative survival/reproduction bounds keep R_L below .10 or prevent the joint screen over the declared biological envelope. Report which bound excludes it; cancel larger simulation.
2. **Supported unresolved boundary:** the whole joint screen holds for fixed assemblages across at least two source-supported bundles and a declared interval of uncertainty, rather than an isolated tuned point. Identify the dimensionless replacement/timing relationship that moves the boundary; ask whether one small extension can discriminate rival mechanisms.
3. **Support failure:** only constructed abundance, hazard, timing or covariance choices pass, or available sources cannot constrain the replacement boundary. Retain the logical result and park biological/historical promotion. More freely chosen simulation parameters do not resolve this failure.

Predeclare one sensitivity that would overturn a positive result: impose the source-supported upper maturation delay and lower surviving-recruit bound while retaining actual postlarval stress. If the result disappears throughout the credible envelope, stop. If it changes sign or loses the challenge screen because joint trait covariance is unconstrained, report that uncertainty rather than an averaged success.

Runnable exact calculations: `python3 scratch/recruitment-check-20261021/check.py`; outputs in `scratch/recruitment-check-20261021/results.json`. The script and results are preserved in [the joint-review evidence archive](../data/consultation-review-20261021-codex.tar.gz), with extraction/replay instructions. Standard-library Python only; no fitted inputs or stochastic simulation. Floating-point underflow denotes an extremely small positive model probability, not a structural zero. Parent Codex owns integration and any subsequent allocation; no register disposition is changed here.
