# Q-038 predictor contract and four prior checks: Codex review

20 October 2026. Owner: Codex. Response to Claude's Q-038 contract
(`9bfba9d`) and Q-017, Q-015 and Q-023/Q-031 notes (`1296757`, `5a90388`,
`8c41db4`); reviewed from checkout `756bd2f`. Barry explicitly requested
this backlog review alongside the two [Q-012 rulings](2026-10-20-q012-reference-and-adaptation-rulings-codex.md).
Q-016 is independent. Two bounded GPT-6.1 Sol reviews supplied independent
source/code checks; parent Codex checked the arguments and integrated this
record. This is a review, not an empirical fit or fresh comprehensive
novelty search. Claude's source notes and raw inputs are preserved.

## Disposition

| Item | Accepted | Required before the proposed next analysis |
| --- | --- | --- |
| Q-038 | Six support tables reproduce exactly; genus-ID primary unit, separate within-stage entrants, recency and missing-range distinctions are useful | Amend biological versus observed outcome, prospective cohort, fold masking, taxonomy mapping and size provenance. Contract not yet accepted for a fit |
| Q-015 | One bounded measurement/support audit is worthwhile | Replace thermal-limit language; specify habitat/proxy rivals and a survival landmark that prevents outcome leakage |
| Q-017 | Develop the analytic correspondence and identification note | Align finite-window likelihoods; reject two conditionally independent incomplete lists as sufficient calibration evidence |
| Q-023 | Develop a matched Frasnian/end-Triassic design | Define excess-depletion accounting, common units and baseline/boundary sensitivity before rate extraction |
| Q-031 | Develop a stratified lineage/local-temperature support table | Separate ectotherm TSR from mammal comparisons; distinguish independent events from series and rows |

These are next-work recommendations, not five newly commissioned projects.
The bounded searches leave novelty provisional. No primary investigation,
register status or tier is promoted by this review.

## Q-038: material contract amendments

### 1. The detection-null gate rejects valid prediction of observations

The [draft](../data/q038-predictor-contract/README.md) scores observed last
appearances, yet requires no predictive gain when biological losses are
uniform and only detection varies. Those requirements conflict.

Our exact two-genus counterexample starts with two known living genera,
each having biological loss probability 0.2. Conditional on survival,
post-boundary detection probabilities are 0.2 and 0.8. Observed terminal-loss
probabilities are therefore 0.84 and 0.36. Given exactly one observed loss,
the low-detection genus is the victim with probability 0.9032258. A correct
prediction of this observation gains **0.3752104 expected log-score nats**
over uniform loss, despite zero biological selectivity. This finite-occasion
example does not refute identification in every longer capture experiment.

Declare two distinct assessments: prediction of fossil observations and
recovery/prediction of latent biological victims. Synthetic validation can
score true simulated deaths and check biological selectivity under a
detection-only null, while allowing observed-history predictive gain. Include
a biological positive control and explicit uncertainty/recovery tolerances.
For empirical data, neither inferred deaths nor the true loss count D are
known labels: specify how their uncertainty, including cohort membership,
enters the likelihood and assessment. Calling the model CJS/Pradel, or using
the same covariates in hazard and detection, does not establish identification.
Failure of an incoherent zero-gain check cannot justify parking the question.

If independent biological Bernoulli loss odds are exp(eta_i), a coherent
conditional set model is

    P(S | D, eta) = exp(sum_{i in S} eta_i) /
                    sum_{A: |A|=D} exp(sum_{i in A} eta_i).

Uniform eta gives probability 1/choose(N,D). This follows directly by
conditioning the product Bernoulli likelihood on D. It is the Fisher
conditional model; Wallenius corresponds to a different sequential sampling
story. Choose the biological story before comparing scores. An observation
layer generally prevents substituting observed disappearance odds for
biological loss odds.

### 2. The incoming cohort is retrospective

`fad < k & lad >= k` uses the focal or later record to establish membership.
Histories `1,0,0` and `1,0,1` have the same prefix before stage 2, but different
range-through membership at stage 2. Scaling over that future-selected cohort
also leaks information. In the actual incoming cohorts, **29/65** Late
Devonian Bivalvia, **18/63** end-Triassic Rhynchonellata and **50/269** K–Pg
Bivalvia have no focal-stage occurrence and qualify through a later record.

A retrospective conditional comparison is legitimate if labelled as such.
For a forecast, freeze a candidate/risk-set rule from the observed prefix and
integrate uncertain current survival/membership. Scaling must use training
data or a genuinely available pre-event cohort, with zero-variance and
all-missing rules. Excluding within-k entrants does not solve future selection.
That entrant stratum can remain descriptive; it cannot acquire pre-k size
or clade predictors simply because those values appear in a later archive.

### 3. Define forbidden information for every held-out fold

Forward chaining tests historical forecasting. Leave-one-event-out training
that includes later events/background tests retrospective transport. Both
may be useful, but answer different questions. Repeated genera and persistent
frailties can disclose the held-out fate through later detection/survival
histories even after its focal row is removed.

Specify fold-specific masking of histories, traits, standardisation and
latent-state smoothing. A forward forecast fits/filters only the prefix.
State the distinct known-genus/clade and new-clade targets, unseen-level
handling, and any permitted later information used solely to adjudicate
test outcomes. Do not select informative events after seeing score gains.
There are five events, not ten independent events supplied by two classes.

### 4. Genus merging requires an explicit attribute rule

Accept PBDB `genus_no` as the primary unit. The independent audit finds
multiple deposited size values for **140 Bivalvia and 9 Rhynchonellata IDs**,
and multiple nonempty order/family labels for **108/12 Bivalvia IDs**.
These include nomenclatural differences; they are unresolved mappings, not
108 demonstrated biological contradictions. Taking the first nonmissing size
is not a scientific aggregation rule. Preserve source taxon/subgenus identity,
export ambiguities, and freeze a taxonomy/aggregation policy.

At K–Pg, the authors' incoming Bivalvia units give N/D = **313/87** versus
**269/78** after merging: 44 units and 9 losses differ. Small effects on
predictions are not established. The audit also finds 1,212 repeated
occurrence-number rows across the two classes; distinct collection/reference
calculations tolerate many such joins, whereas raw row counts do not.

### 5. Keep primary size exclusion; tighten the rescue condition

The source describes maximum biovolume from figured specimens. A type
species' stratigraphic range does not date the actual specimen or aggregation
supplying that maximum, especially after genus merging. Recover specimen and
reference provenance before accepting a prospective size predictor; the sign
of leakage bias is not predetermined. The archive was already selected for
body-size data and stage-resolved occurrences. Dropping size as a predictor
does not remove that ascertainment: scope claims to this archive unless
representativeness is separately established. See Monarrez et al., Methods
pp. 3–4, [primary PDF](https://par.nsf.gov/servlets/purl/10514226), and the
[deposit](https://doi.org/10.5061/dryad.931zcrjqw).

Other concrete repairs: reverse the Ma subtraction for the age proxy (first
record base minus evaluation age), specify evaluation time and interval
uncertainty, distinguish located occurrence rows from distinct coordinate
pairs, and retain recency in elapsed time as well as stages. The 3,424
history matches validate name-aggregated occupancy; seven matched names span
multiple genus IDs, so they do not validate the merged taxonomy. The 56–58%
missing-predictor share concerns **observed** background losses, not identified
biological hazard. References/collections need a sampling-opportunity and
clustering interpretation before serving as independent detection replicates.
The text says four informative class-event cases but lists five; explain any
exclusion of end-Triassic Rhynchonellata (33 incoming losses).

**Next deliverable, Claude:** one amended target/observation/fold contract
with deterministic prefix-invariance and detection-null examples, an explicit
transition/exposure likelihood, and an attribute-ambiguity export. Preserve
the present support tables as the reviewed snapshot. These repairs decide
whether a small synthetic recovery probe is earned; they do not commission
an empirical fit or a general capture–recapture engine.

## Q-015: a shell temperature is not a physiological limit

Accept a support audit of **occupied calcification-temperature response beyond
a specified habitat/observation null**. Shells condition on occurrence,
growth, survival, preservation and sampling. Residual temperature change can
reflect depth/season use, abundance weighting, chemistry or calibration
without changed physiological tolerance. The proposed “realised thermal-limit
lability” therefore overstates the estimand even after withdrawing adaptation.

Jonkers & Kučera report approximately **40% attenuation**, not 0.4°C recorded
per degree: the simple corresponding recorded fraction is about 0.6. Their
modern six-species result supplies a sensitivity model, not a fixed Eocene
tracking law. [Journal abstract and summary](https://cp.copernicus.org/articles/13/573/2017/).
Kearns' individual-isotope study makes changed depth occupancy a live rival
requiring explicit treatment. [Primary article](https://www.frontiersin.org/journals/ecology-and-evolution/articles/10.3389/fevo.2021.679722/full).

Full-event lability used to predict event survival leaks outcome information:
early victims cannot supply complete response trajectories. Define a response
window ending before a survival landmark and report its restricted at-risk
cohort, including which early losses it excludes. Whole-event victim prediction
instead needs pre-event predictors or an explicit joint observation/survival
design. Do not discard terminal records and then generalise to all victims.

For one event, map species-resolved shell distributions, independently
constrained ambient fields, depth/season/proxy uncertainty and subsequent
fates. Test whether plausible unchanged-physiology models span the response.
If they do, hold the thermal-limit interpretation; if informative responses
exist only for survivors, hold the survival comparison. Two sites and a
handful of series are a source-access screen, not a demonstrated power gate.
A null prediction gain supports static niches only when the competing
measurement and survival contrast were informative. The prior study claims
remain at Claude's stated access depths, not newly certified here.

## Q-017: a valid identity, an unresolved equivalence, and a failed calibration rule

For exponential lifetime with rate mu and Poisson finds at rate lambda,
the whole-lifetime probability of no finds is mu/(mu+lambda). An initially
undetected living species with detection rate d has the analogous eventual
extinction-before-detection probability mu/(mu+d). Accept that identity.

For a finite modern window T, however,

    P(extinct and undetected by T) = mu/(mu+d) * [1-exp(-(mu+d)*T)],
    P(alive and undetected at T)   = exp(-(mu+d)*T).

The fraction of all extinctions that were never detected has yet another
conditioning denominator. Match the entry cohort, windows, censoring,
discovery versus subsequent sightings, and observed-data likelihoods before
claiming equivalence of zero-truncated fossil-range and historical-record
estimators. Time variation changes the simple formula; it does not rule out
every correspondence. The flagship estimator texts are necessary for their
equivalence claim, not merely optional checks for discussion citations.

**Reject the proposed replacement of calibration evidence by two conditionally
independent incomplete lists alone.** Our counterexample has equal classes
with detection probabilities (0.8,0.8) and (0.2,0.2), independent within each
class. At 500 species per class, expected cells (both, A only, B only,
neither) are (340,160,160,340). A homogeneous independent-list model instead
matches the three observed means with N = 735.294, detection 0.68 and only
75.294 unseen. Under independent Poisson class abundances with mean 500,
Poisson thinning makes the **entire three-cell observed law identical** to
that of a homogeneous Poisson population of mean 735.294; unseen means still
differ. Thus this is more than a discrepancy between two point estimators.
Measured strata, informative replication, external completeness constraints
or defensible partial bounds must address the missing information.

Duncan et al. already use historical species as marked and fossil occurrences
as recaptures, model detection/extinction heterogeneity, and compare predictions
with New Zealand. The primary PDF is accessible (pp. 6436, 6438–6440): this
upgrades the note's secondary-source lead. It occupies the generic bridge,
without proving SEUX/Foote–Raup equivalence. Prehistorically extinct species
cannot enter a later historical list, so an unchanged closed-fauna assumption
also needs repair. [Duncan et al. 2013](https://www.pnas.org/content/pnas/110/16/6436.full.pdf).

**Next deliverable:** the finite-window analytic/likelihood note first, with
this heterogeneity counterexample; then assess one dual-record system for
information resolving it. With only two unreplicated lists, retain a methods
or sensitivity contribution and hold empirical calibration claims. This is
an internal ordering of Q-017's work, not a reversal of the programme's
deep-time priority.

## Q-023: fix the counterfactual before partitioning diversity loss

The attribution residual is worthwhile. Bambach's result for Frasnian and
end-Triassic neighbourhoods concerns depressed origination and excess
extinction; its descriptive accounting does not identify a causal mechanism.
[Primary paper](https://biology.kenyon.edu/courses/biol241/extinction%20and%20marine%20diversity%20banbach%202004.pdf).
Our recommended continuous per-capita accounting, if that is the selected
scale, defines excess log depletion relative to baseline p0,q0 as

    integral [(q-q0) + (p0-p)] dt.

This differs from actual diversity decline. Require common rate denominators,
time exposure, bins and sampling treatment. Contributions may be negative or
offset each other; fractions can exceed 100%. Do not force a positive pie or
interpret the origination deficit as directly observed missing taxa.

Design the two-event reproduction/contrast before extraction, matching the
original substage versus proposed stage definitions and the neighbouring
observations needed for rate estimators. Predefine reasonable background
windows, boundary placements and origination-detection lags. A larger
standardised extinction peak alone does not overturn origination dominance;
compare both excess terms on the same scale. If equally defensible baselines
or boundaries reverse dominance, report that dependence and hold a general
event attribution. Full-text Alroy 2008 detail remains unverified in this
review; absence of an all-event standardised analysis is not established.

## Q-031: preserve the decomposition, repair the benchmark and replication

Forster et al. concern developmental responses of ectotherms; their terrestrial
approximately −0.5%/°C comparator is conditional on approximately 100 mg dry
mass. Comparing PETM/ETM2 equids with that value does not establish a tenfold
departure from a matched experimental expectation. Keep an ectotherm TSR arm
and a distinct mammal/Bergmann/ecological-evolutionary arm. Even within
ectotherms, harmonise size, ontogeny, habitat, exposure and mass conversion.
Within-lineage change alone does not identify plasticity.
[Forster et al. 2012](https://pmc.ncbi.nlm.nih.gov/articles/PMC3511100/).

A count-only replay of the existing `S1.RData` and inspection of `S1.R`
lines 519–567 confirms 5,655 rows, 4,976 with finite lnRR and known warming,
including 4,544 zero-warming rows and 432 positive-warming rows. There are
**four** nonzero values (4,5,6,10°C), shared across **six** events:

| Event | Retained crisis rows | Assigned warming, °C |
| --- | ---: | ---: |
| Permian–Triassic | 114 | 10 |
| Triassic–Jurassic | 16 | 6 |
| Toarcian | 194 | 5 |
| OAE1a | 4 | 4 |
| OAE2 | 90 | 4 |
| PETM | 14 | 5 |

The crisis-only row-level slope/SE/p is not an independent event-level test.
Rows share temperature assignments, studies, clades and intervals. No slope
was refitted here. “Eight events,” “eight event × taxon series,” and “eight
series” in the register and note are different requirements; none is a
universal support threshold.

The next finite table should record event IDs, lineage continuity, site/study,
local temperature estimate and uncertainty, size scale, habitat and
thermoregulation. Assess independent contrasts and covariate overlap before
counting rows. Hold a cross-event magnitude/duration regression if confounded
with clade or method, or driven by one event; a smaller within-event
decomposition may remain worthwhile. Define weights and the turnover-share
denominator, allowing offsetting size components. Published PNAS SI remains
unread, so the prior-occupancy check remains open; absent citations are weak
evidence about an unread analysis.

## Evidence and handoff

The [review archive](../data/review-20261020-codex.tar.gz) retains the two
independent memos, Q-038 replay script/log/six outputs and byte-comparison,
independent raw-data audit and three source hashes, Q-031 count script/output,
Q-017 exact counterexample, input hashes, environment and an internal manifest.
It contains no new raw-source copies. Replay used base R 4.6.1 and Python
standard libraries; no empirical fit or remote workload ran in this review.
The review scripts read preserved local inputs; the package README gives
paths and rerun instructions.

Archive: 24,986 bytes, 21 members; SHA256
`3262e9e001eac353d11a030f22e39475d3fb22bdebfa461746f7a18e186d82b4`.
All 20 internal member hashes passed; the manifest excludes itself.

Source access on 20 October: Q-038 primary Methods/deposit inspected locally;
Jonkers–Kučera abstract/summary; Kearns relevant primary HTML sections;
Duncan full primary PDF with relevant methods/validation passages; Bambach
abstract and accounting context; Forster primary abstract and relevant text.
The parent verified the decisive Jonkers and Duncan passages and Forster
comparator. This targeted verification is not a rerun of Claude's citation
censuses. Access failures for Chisholm/Alroy and published Nätscher SI remain
limits. Equations and counterexamples labelled ours are analytical inference,
not attributed source claims.

**Next responder: Claude.** Implement the already-issued Q-012 rulings under
its existing ownership, independently of Q-016; then respond to these material
contract/estimand amendments and integrate accepted corrections into owned
notes. Q-038 contract repair is the next bounded backlog product. Sequence
the four narrower analytic/support tasks within the existing two-task limit;
do not open four audits at once. Codex's separate Q-018 → Q-024 → Q-010 queue
is retained and was not started during this review. No Barry-only decision
or external contact is needed to resolve these corrections.
