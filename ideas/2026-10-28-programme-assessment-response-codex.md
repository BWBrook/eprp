# Response to the programme assessments and implementation handover

Codex, 28 October 2026. Reviewed the [separate Codex assessment](2026-10-25-programme-direction-assessment-codex.md)
and [Fable assessment](2026-10-25-programme-direction-assessment-claude.md),
Correspondence 76 through 2432, and supporting records at `8403eef`.
Two GPT-6.1 Sol reviewers checked the Q-012 argument and candidate readiness.
No fits, restricted-data inspection or empirical analyses were run.

**Recommendation:** rebalance the next allocation towards a consequential
biological comparison. Complete the integrated ranking and put a cheap Q-012
information check ahead of more sampler engineering. Keep the infrastructure
paper finite. These are recommendations, not selection of a primary
investigation or instructions to restart parked campaigns.

**Implementation responsibility is decided.** Barry's instruction in this chat
on 28 October is: “I will need you to take over the bulk of the action-oriented
tasks on EPRP moving forward.” He retains cross-model correspondence and asks
that most Claude time go to discussion and ideation. I accept the execution
lead: Codex handles most sourcing, preparation, coding, runs, verification,
drafting and integration; Claude supplies selected discussion, criticism and
scientific adjudication. Codex continues to exercise scientific judgment.
Existing active files still require coordinated handover.

## Diagnosis: broadly right, with consequential corrections

The opportunity-cost criticism is justified. Q-038's [terminal record](2026-10-23-q038-terminal-review-codex.md)
contains 13 unsuccessful full-fit attempts and 660.9114 allocated core-hours,
excluding preparation. They produced no qualified biological answer. Q-012's
numerical repairs have not demonstrated the operating characteristics its
scientific decision requires. Rejection and qualification are valuable, but
do not by themselves show that better biological investigations are emerging.
My reviews contributed to this imbalance; changing the executor alone will
not cure it.

I agree especially with distinguishing an occupied broad idea from an
unimportant question. Familiar mechanisms can motivate consequential new tests.
Failure of a database-only route need not defeat targeted synthesis of
published observations. Two well-supported events can answer a narrower
comparison even when they cannot establish a universal relationship. Revise
the claim and replication scope rather than automatically parking the question.

“Nothing finished” is too strong: catalogues, known-truth benchmarks,
mathematical results and reusable tools are substantive outputs. The missing
outputs are the intended integrated ranking and a developed biological
comparison ready for downstream handoff. Commits and correction counts do
not measure wasted effort or model performance. Fable read the Codex
assessment first; their agreement is not independent empirical validation.

## Q-012: screen information, but correct the premise

Fable's three intervals are not three comparable real-scale experiments:

| Record | Actual design | What it establishes |
| --- | --- | --- |
| v4, interval 0.029–0.492 | Seed 20261060; 264 recorded lineages; numerical problems | Development evidence, not a qualified power replicate |
| R00 v6, interval 0.024–0.499 | Replay of the **same seed and tree**; passes the numerical screen | One successful real-scale posterior, with broad uncertainty |
| Amended P11, interval 0.005–0.594 | Seed 20261211; **19 recorded, 20 latent lineages** | A much smaller case |

The [prototype record](../data/q012-prototype/README.md),
[R00/P11 manifest](../data/q012-pilot/payload/manifest.json) and
[v6 ruling](2026-10-17-q012-v6-result-and-panel-ruling-codex.md) establish
these identities. Broad uncertainty warrants concern; it does not demonstrate
that the real design cannot separate the working values. The completed
[component check](../data/q012-component-check/README.md) also uses smaller
trees and a different effect.

The [finite contract](../literature/2026-10-16-q012-finite-contract.md) already
defines false support, positive power, informative negatives and Monte Carlo
tolerances. The missing item is a completed test at the relevant design.
The [Fisher code](../data/q012-pilot/fisher_tree.py) uses **Fisher's identity
to calculate a score**, not expected Fisher information; it is not an existing
achievable-precision calculation.

**Proposed first check:** a generator-only, complete-data likelihood-ratio
oracle comparing η=0.05 with 0.20 at fixed nuisance settings. Changing dependence
at fixed marginal frailty variance changes Gaussian parent–daughter kernels
in the primary generator. The complete latent tree permits a likelihood-ratio
ordering without collapsed integration or sampling. Keep every true edge,
including the forced cohort daughter; preserve selection, censoring and caps.
Check that construction before trusting a result.

Freeze the ensemble and independent calibration/evaluation seeds. “268 lineages”
alone is not a design: the selected tree and size-calibrated generator have
much more censoring than the real record. For a declared simple comparison,
an upper bound on the optimal oracle's power below 0.8 at size 0.05 would
rule out the required recorded-data power **for that generator and ensemble**.
Include uncertainty in both threshold calibration and power. Failure of an
imperfect approximation to the oracle is not an impossibility result.

Oracle success is only an optimistic bound; it would justify trying a cheap
frozen statistic on recorded inputs, not immediately resuming sampler
engineering. A passing, independently calibrated recorded-data test establishes
that information survives observation in that simulator. Failure of one such
test does not establish that all estimators fail. Retain the contract's
false-support and informative-negative checks at η=0, where equal-tail
coverage is structurally unavailable under its positive continuous prior.

The target remains residual phylogenetic dependence. Neither oracle success
nor a more elaborate model identifies biological inheritance against
unmeasured clade-tied exposure.

## Q-038: a simpler estimator can answer a smaller question

Fable is right that a complex model should not be the only entry point.
A penalised classifier could test **future recorded histories**, after an
eligibility check. It needs a landmark-available risk set, prefix-only
predictors, training-only transformations and temporal/event holdouts that
prevent leakage through shared features. A next-record indicator is observed;
it is not a known biological death label. Declare whether the score conditions
on the recorded loss count or predicts it, and use the corresponding baseline.

The [existing contract](../data/q038-predictor-contract/contract.md) already
separates observed-history prediction from latent biological-victim recovery.
The simpler test would answer the former or a stated amendment. Detection
alone can generate predictive gain for recorded outcomes: that is informative
about the record, but cannot establish the predictability of biological
extinction. Future-derived size or range is not repaired by describing its bias.

Resolve input eligibility under the [public-data hold](2026-10-23-response-closure-and-data-holds-codex.md)
and the retained deposits' provenance flags before any empirical classifier.
The asserted “one day” delivery time is unverified. I would not reopen Q-038
ahead of the portfolio comparison merely because a classifier is easy to fit.

## Compare candidates before choosing the development slot

There **was** a [44-entry first ranking](2026-10-11-phase2-portfolio-first-pass-claude.md),
which Codex challenged. What is overdue is the integrated 25–50-question
ranking incorporating later evidence and the blue-sky portfolio. Use the
already agreed [three views](framework-notepad.md#6-notes-to-revisit):
scientific consequence, readiness, and value of the cheapest next check.
Keep unknowns and ties; compare candidates near the allocation boundary.
Do not make ranking an exhaustive new source-review campaign.

| Candidate | Consequence | Cheapest useful next check |
| --- | --- | --- |
| **Q-027**, climate state and the diversity gradient | Named biological contrast with substantial support investigation | Define one estimator's eligible spatial/time windows on admissible inputs; presence counts do not establish richness eligibility or power |
| **Q-016**, range change and future loss | Clear predictive target, with useful negative outcomes | Count jointly available landmark predictors and later outcomes in one microfossil system; establish added value beyond published forecasting priors |
| **B-005**, geography/climate versus diversity dependence | Strong matched mechanistic comparison | Identify one observed spatial statistic/domain, closest prior, and a mechanism toggle that holds nuisance assumptions fixed |
| **Q-009**, organisation and later response | Timely comparative leads from the [new recovery synthesis](../literature/2026-10-28-extinction-recovery-disagreements-codex.md) | Resolve counts/ages and independent later outcomes; References Codex already owns this source work |
| **Q-040**, diversity-estimator application | Strongest instrument-to-biological-interpretation connection | Find one common-support empirical contrast; estimator disagreement does not identify the true historical curve |
| **Q-042**, species loss | Consequential headline and explicit conditional bounds | Establish the start cohort and species–genus mapping; the richness benchmark does not solve this inversion |

The relevant entries are in the [applied register](register.md) and
[blue-sky register](register-blue-sky.md); the
[matched-toggle critique](2026-10-14-blue-sky-cross-critique-codex.md)
and [T4 record](../resources/software/bench/README.md) supply additional
boundaries. Q-027 has the strongest combination of a live dispute and
investigated support among this shortlist; Q-016 offers a particularly clear
narrower predictive result; B-005 has the strongest controlled mechanistic
comparison. None is established as the winner. Include B-002 and the rest
of the portfolio in the integrated ranking. The new Q-009 lead earns its
bounded source check, not priority through recency alone.

I favour **one protected development slot**, chosen from that comparison,
with a claim-sized result, a compute ceiling and an exit condition. An
informative negative counts. Neither a three-week budget nor a particular
candidate is adopted here. EPRP remains a broad question-development programme;
this would demonstrate depth without selecting a permanent flagship.

## Bound the audit; simplify the coordination

Finish a selected infrastructure case series, not all 189 ledger rows.
Begin selection with the evenness/richness benchmark, stratigraphic
interpolation defect, capture-history corruption and plate-frame differences.
Consider Triton once the paired downstream comparison is saved, and the
access-control case under its separate sensitivity/disclosure conditions.
These are candidate anchors, not release-cleared claims or a mandatory number.
Eight to twelve cases is a suggestion, not a scientific finishing criterion.

Each retained case needs attributable inputs/version, a reproduced result,
checks against intended behaviour and prior documentation, and a demonstrated
change to an analysis or research-use decision. Preserve clean controls and
our own errors. The richness bench does not replicate Alroy's published
method on its intended input; no benchmark winner automatically wins on fossils.
The [T5 review](../resources/software/reviews/2026-10-28-tranche5-codex/README.md)
also shows why a global replay pass need not qualify local ecological use.
The case-series thesis is already accepted in 76/2414. Keep the question-first
material as a record, without a new exhaustive ledger sweep or claims of
workflow superiority.

Fable's materiality rule needs interpretation: act now on errors affecting
a result, interpretation, next action, reproducibility, data integrity or
release; batch cosmetic and redundant explanation changes. A rule limited
to numbers and dispositions would be too narrow: withdrawing the historical
adult-mortality inference mattered even though retirement was unchanged.
Preserve historical records while making STATUS a short current handoff.
Use concise chat reports at work checkpoints; a weekly reporting obligation
or automation is not needed to solve the board backlog.

Do not replace the rejected seven-criteria gate with an empirical-only gate
on theory. Prefer nominations tied to live disagreements, unexpected results
or well-supported phenomena. Allow a bounded theoretical comparison when
its result would change understanding, even before a fossil discriminator
is available. Purposeful data assembly remains eligible.

## Consequence and next owner

The immediate recommendation is **Codex-led integrated ranking plus the
small Q-012 information screen**, instead of defaulting straight to another
sampler-engineering tranche. Then bring competing development options to
Barry with evidence and a finite result criterion. Existing Codex References
and Packages sessions continue their owned streams; main Codex coordinates
rather than duplicating them. Claude's next useful contribution is a compact
challenge to these scientific and allocation judgments.

Claude's 76/2414 accepted “guidance, not gates,” the first-pair wording repairs,
the builders merger and the audit thesis. Those disputes are closed.
Its [CN3 brief](2026-10-25-innovation-windows-prior-claude.md) gives no reason
to prioritise a standalone model now. Keep the residual question in reserve,
with a correction to its proposed binary: inherited components can be lost
or costly, while externally acquired components can persist. Transmission
mode is not itself a measure of persistence or a guarantee of free waiting.
No new prior search or empirical support claim is made by that observation.

This turn completes assessment and records the implementation handover.
No new scientific priority, registered disposition, compute campaign,
provider contact or release is enacted by this note.
