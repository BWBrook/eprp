# Independent Q-012 information-screen audit

28 October 2026, independent GPT-6.1 Sol Codex subagent; static scientific/code review only. No
generator runs, result inspection, scientific-code edits, Board writes or
commits. Reviewed the frozen protocol and `screen.py` against the original
`q012-prototype/prototype.py` generation and observation paths.

## Finding

No blocking mathematical or implementation defect found in the declared
fixed-nuisance, accepted-cohort, capped computational experiment.

The ratio of daughter-transition densities is the only nonconstant
rho-dependent factor in the joint density of accepted generated histories.
Independent root priors have fixed sigma. Exposure generation, termination,
budding and queue/cap rules have the same conditional laws given latent
frailties under both hypotheses. This remains true where those processes
depend on frailty; their conditional factors cancel rather than being
assumed independent of frailty. The forced daughter contributes a real
transition density and is included by the implementation.

Rejecting entire initial cohort proposals until all six survive conditions
the accepted joint history on one event. Integrating out rejected proposals
and their count leaves one selection normalizer Z_rho, constant across
accepted histories. It does not require estimating Z_rho for LR ordering.
Sigma=.5 is the unselected marginal SD, not an asserted variance of the
survival-selected cohort. The implementation uses the correct rho-specific
conditional variances .25*(1-rho^2).

The lineage cap prevents adding a complete pending daughter batch. Existing
lineage frailties and terminations are nevertheless already generated. Some
offspring histories remain ungenerated. The output is therefore a stopped
computational history. Its cap indicator and partial true-bud-count pattern
carry information, but their conditional factors are common across rho.
Marginalizing any unreturned bud times likewise adds only common conditional
factors. All generated edges, including edges whose parents' offspring have
not yet been expanded, enter the score. No selection on size or cap removes
a further normalizer from the current ensemble.

The original observation map is a common rho-independent Markov kernel on
this complete history when observation randomness is fresh and independent.
Consequently the complete-history NP optimum bounds every recorded-input
test for the same ensemble. Fixed seed offsets are reproducibility devices;
seeds, rejected proposals and internal RNG state are not inferential inputs.
This argument does not extend to a size-selected or uncapped ensemble by
relabeling the output.

## Calibration and uncertainty

For B~Binomial(n,.95), lower rank l=ppf(.0025) and upper rank
u=ppf(.9975)+1 bracket the population .95 quantile on l<=B<=u-1.
`threshold_bracket` reports the corresponding exact coverage with the correct
CDF difference. Strict greater-than rejection at the nominal rank
ceil(.95*(n+1)) has unconditional size at most .05. Score continuity is
supported by a nonconstant Gaussian quadratic score on every finite tree;
the forced daughter guarantees a nonempty transition set, and a terminal
daughter has a nonzero squared-frailty coefficient.

The code evaluates the alternative rejection count at the higher threshold
for the lower power bound and at the lower threshold for the upper power
bound. Its beta-quantile endpoints are one-sided Clopper-Pearson bounds at
the declared .01 tails, including k=0 and k=n. Conditional on calibration,
the evaluation observations are independent Bernoulli draws at either
threshold. Using the same alternative panel for both counts needs no extra
independence assumption: the union bound suffices. Two ensembles consume
2*(.005+.01+.01)=.05 error probability. The independent null-evaluation
interval is correctly described as descriptive rather than part of the
optimal-power guarantee.

One nonblocking implementation limit: although the rank helper permits
infinite endpoints, `allow_nan=False` cannot serialize them into summary JSON.
The frozen n=2000 and alpha/error settings yield finite endpoint ranks, so
this cannot affect the declared run. It would matter if the protocol were
later changed to very small calibration panels.

## Interpretation and handoff

An upper confidence bound below .8 can exclude target recorded-input power
only for the named simple comparison and computational ensemble. A lower
bound above .8 supports trying a fresh recorded-input test. Neither outcome
validates the empirical generator, composite-null performance, interval
coverage, biological inheritance or sampler readiness. Parent Codex owns
runtime checks, execution, source freeze and final result interpretation.

## Reviewed identities

SHA256:

- screen.py: bb775b1161c543674e8c0e1d409065b0df8add8226be9a7628ef3e3202e671da
- PROTOCOL.md: 6156eca31593ed1229119690550b9f454e192ba2670d8dc68ff97193cb49188e
- protocol.json: d32a476a5cd98091781950486f15a507e012d837ecd5e454bf62eb19e8d433d5
- prototype.py: afb001d47d9761ae092003ac2f2a45aa423aaac0223bcb461126444813016067
- prototype/config.json: 619242a767012849b6f2758c3809e1f7bfced47d2aadd19937ecc51b58e20d4a
