# EPRP: independent external scientific review

**Repository:** BWBrook/eprp  
**Commit reviewed:** `bbe5ce7fc205b3b1f9529757b64e25fd997243cb`  
**Review date:** 11 October 2026  
**Scope:** research-question portfolio and selected supporting evidence; read-only.

## 1. Executive assessment

**Change the next-work decisions, not the programme’s remit.** Give Q-006 a substantive information-and-design review rather than parking it when any related theorem is found. Develop Q-042 as a cohort-specific partial-identification problem: its proposed 56–79% genus-loss input combines different quantities, not a single uncertainty interval. Replace outcome-selective stopping rules, most clearly Q-035’s requirement for detectable nonzero lags. Keep Q-021 scientifically prominent, but require a common, explicit proxy model and a joint discrimination criterion before its proposed lithium comparison. Q-032’s abundance-calibration requirement should not also govern its interaction endpoint; nevertheless, additional host-associated literature makes an immediate promotion unwarranted.

The repository’s principal strength is **productive correction of inferential claims**, not demonstrated novelty. The current distinctions between numerical usability and scientific suitability, retrospective and prospective predictors, and recorded and biological turnover are worth preserving. I independently reran Q-026’s tracked probe: its output matches the committed table exactly. That validates its counterexample, not a general impossibility theorem. I found no basis to attribute Q-038’s deposited-code problems to the published fitted results.

The full register was surveyed before the phase-2 debate. Eight entries received substantive attention, with additional narrow checks elsewhere. Primary-source checks materially inform the findings, but several original datasets and some full texts remained unavailable. This is not an exhaustive literature review or repository-wide code audit.

**Development candidates:** Q-021, Q-042 and a reframed Q-006, for different reasons and with different next-work costs. None is endorsed here as ready for primary-project handoff. No critical defect invalidating the portfolio was established; the major findings concern particular designs, interpretations and dispositions.

## 2. Review basis and terminology

### Access and sequence

Authenticated GitHub access succeeded at the requested commit. I could read complete text files by requesting bounded line ranges; I was not limited to search snippets. I read `README.md`, `docs/programme.md` and all Q-001–Q-050 register entries before the portfolio rankings. The separately supplied `initial_view_before_phase2.md` records that provisional, register-first assessment. This was **order-controlled, not blind**: the register already contains the authors’ judgments.

I inspected the root tree and the `ideas`, `literature` and `data` listings, plus the selected Q-026 subtree. The large recursive-tree response was truncated. Consequently, I do **not** claim a complete recursive inventory or inspection of every tracked file. File contents were available when requested; actual substantive coverage is recorded below.

I subsequently read the first phase-2 portfolio pass, Codex’s response, the three later Claude replies, and the scientific status summaries. Review-brief material was excluded from evaluation. Where a response also returned adjacent briefing passages, I disregarded them. I did not use the absent discussion board as scientific evidence.

### Why these targets

The initial deep targets were Q-004, Q-006, Q-032, Q-038, Q-042 and Q-050: they span extinction baselines, information theory, a parked ecological question, predictive selectivity, extinction magnitude, and evolution of variation. Q-021 became an additional substantive target because its latest proxy-model proposal offered a consequential unresolved test. Q-026 provided a small, self-contained way to check whether the repository’s computational evidence actually supported its interpretation. This selection was not determined by the number of audits per question.

### Finding labels

- **Verified finding:** directly inspected wording, source scope, or a reproduced mathematical/computational result establishes the stated problem. It need not establish an empirical biological effect.
- **Supported concern:** a consequential inference requires an assumption or specification that the inspected evidence does not yet establish.
- **Unverified lead:** relevant literature or data deserving follow-up, without sufficient inspection to sustain an objection on priority or validity.

“Major” identifies an issue that changes a design, inference or work decision. It does not mean that the parent biological question is unimportant or false. Confidence concerns the finding, not how likely a project is to succeed.

## 3. Ranked findings

| Finding | Question(s) | Classification | Severity | Confidence | Decision affected |
|---|---|---|---|---|---|
| F-01 | Q-042 | Verified design inconsistency; conditional bound independently checked | Major | High | Definition of inputs and interpretation of an inferred species-loss range |
| F-02 | Q-006 | Verified source-scope mismatch; supported disposition change | Major | High for source scope; medium for priority judgment | Prior-work framing and proposed parking decision |
| F-03 | Q-035; related Q-047/Q-049 | Verified decision-rule problem | Major | High | Whether informative negative answers survive the portfolio process |
| F-04 | Q-021 | Supported concern about a live proposal; independent counterexample to one reading of its gate | Major | Medium | Proxy-model design and discrimination gate, not the biological question |
| F-05 | Q-032 | Supported inconsistency in revisit criteria; additional primary context | Minor | Medium | Reopening conditions; no automatic promotion |

### F-01 — Q-042: different genus-loss estimands cannot constitute one uncertainty interval

**Claim.** The proposed design says:

> “Carry the 56–79% genus-level interval through as an input, and report the bound intersected with the calibrated range.”

[Commit-specific source: Q-042, including its estimand, input descriptions and bound](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L2337-L2414).

**Access:** register and linked literature notes inspected directly; Stanley’s primary abstract checked, but its full methods were inaccessible to me; bound calculations reproduced independently. The source-specific numerical reconstruction described in the repository remains partly **reported by the authors**, not independently rebuilt here.

**Reasoning and evidence.** The same entry explicitly identifies different origins for 56%, 62% and 79%, calling the last a different metric. A range across quantities with different event windows, background treatment and estimators is not an uncertainty interval for the entry’s declared target: the fraction of species alive at a specified start time that are globally extinct at a specified end time. Propagating that range can be a useful *scenario sensitivity*. Intersecting it with an empirically calibrated range, however, requires the quantities and transport assumptions to agree first.

Stanley’s abstract confirms that the revised estimate incorporates background-removal and backward-smearing corrections; it also distinguishes its late-Permian target from older estimates spanning Middle and Late Permian losses [R1]. Thus at least part of the apparent percentage disagreement concerns the target, not simply uncertainty about a single target. This is not a claim that one published percentage is correct.

The register’s algebraic upper bound is **correct under its retention assumption**. Write baseline species richness as \(S_0=mG_0\), and let \(G_1=(1-g)G_0\) baseline genera survive. If each surviving genus retains at least one **baseline species**, then

\[
E_{\rm species}\leq 1-\frac{G_1}{S_0}
=1-\frac{1-g}{m}.
\]

The calculation does not require random extinction within genera. It is valuable precisely because it is much weaker than reverse rarefaction. But genus persistence through newly originated species is insufficient for a baseline-species survival bound. The words “keeps at least one species” should explicitly refer to the start-time cohort. A very short extinction pulse may make this distinction negligible; a long stage or combined event need not.

The independently checked fixture also shows how much the unobserved species-per-genus allocation matters. With 100 baseline genera, 500 species and 62 lost genera, the sharp range given only these totals and baseline retention is **12.4–92.4%**. If every genus instead has exactly five species, the lower bound is **62%**. The same mean of five does not supply that distribution. These deliberately extreme allocations are demonstrations of identification limits, not plausible estimates for the end-Permian.

**Consequence.** The current design cannot justify a single calibrated global interval merely by combining the named percentages with a regional selectivity calibration. It can justify assumption-labelled bounds or scenarios. This changes the **empirical inference route**, not Q-042’s importance.

**Smallest useful remedy.** Before simulation, make a one-page reconciliation for one event: baseline cohort, numeric time window, taxonomic scope, global versus regional loss, treatment of origination and background extinction, and the genus-richness distribution each source supplies. Mark genuinely comparable inputs separately from alternative targets. Calculate sharp bounds conditional on that information. Only then test which additional preservation and selectivity assumptions narrow them. Do not intersect a regional calibration with a global bound without an explicit transport argument.

**Strongest reasonable defence.** The entry already acknowledges the metric differences and proposes scenarios, heterogeneous sampling and regional/global distinctions. “Interval” may be informal shorthand, and a brief extinction pulse may justify baseline retention.

**What would change my judgment.** A documented transformation placing the candidate genus estimates on the same cohort and interval, plus evidence or sensitivity bounds for baseline-species retention and regional-to-global transport. That would reduce this to a wording issue. I would still retain the partial-identification framing.

### F-02 — Q-006: a theorem is not a general practical answer, and “methodological” is not an importance category

**Claims.** The register summarises Beaulieu and O’Meara as finding that fossils:

> “rarely beat extant-only analyses in practice.”

Its stopping rule is:

> “Park if a minimum-sampling or power criterion, or an occurrence-only identifiability result, is found.”

[Commit-specific source: Q-006](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L269-L304). The first portfolio pass assigns this entry S=1 and proposes parking after a quick precedent check; later discussion properly distinguishes structural identifiability from finite-data usefulness but retains a final-check-before-parking direction. [First pass](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/2026-10-11-phase2-portfolio-first-pass-claude.md); [response](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/2026-10-11-phase2-response-codex.md).

**Access:** the relevant Truman theorem statements and discussion, Beaulieu–O’Meara’s primary abstract and selected methodological sections, and the stratigraphic-range formulation of Stadler and colleagues were inspected directly. A newer phylodynamic preprint was inspected at abstract/theorem-statement depth, not independently proof-certified.

**Reasoning and evidence.** Three importantly different questions are being compressed.

**Structural identification.** Truman et al. establish identifiability for the specified time-dependent fossilized birth–death setting with positive fossil sampling and no removal of sampled lineages [R2]. The register gets these essential qualifications right. This answers a structural question about distributions under a model; it does not establish a universal useful sample size or protect against misspecification.

**Performance for a particular inference task.** Beaulieu and O’Meara study diversification-rate heterogeneity on largely modern trees under particular models and fossil-sampling treatments [R3]. Their result is relevant and cautionary. It is not a general comparison of the value of fossils for arbitrary time-varying rates, stratigraphic occurrence data, or all diversification estimands. The register’s summary extends beyond that scope.

**What observations enter the likelihood.** Stadler et al.’s 2018 formulation includes stratigraphic ranges under different speciation modes and an integration over unobserved tree topologies in the specified setting [R4]. This is a close foundational starting point for an occurrence/range-based comparison. It is **not**, by itself, the unrestricted occurrence-only identifiability theorem sought by the register. A likelihood’s existence, structural uniqueness and useful finite-sample precision are separate achievements.

A recent adjacent-field lead reinforces the need to organise the question by information rather than by “fossils versus trees.” Dieselhorst and Stadler’s April 2026 preprint derives identification results using hidden birth-event information, including versions under particular mutation models [R5]. Those extra observations and assumptions are essential. It does not show that ordinary extant trees identify everything, nor that mutation accumulation at speciation is a justified model for palaeobiological clades. It is a lead about **which additional measurements break equivalence**, not a ready palaeobiological solution.

An unrestricted rate function can contain arbitrarily fine features. A practical criterion must therefore specify the functional target, regularity or temporal resolution, observation model and loss function. “How many fossils?” without those choices is not well posed. Conversely, a useful design frontier for integrated loss, a rate contrast, or a specified temporal feature could change many substantive studies. That is not automatically modest work.

**Consequence.** The cited literature does not justify treating the remaining problem as one that disappears whenever *any* related power criterion or occurrence-only result is found. The rule can terminate two different residuals after finding a result addressing only one restrictive case. This changes **prior-work interpretation and next-work priority**. It does not restore novelty to the theorem already proved by Truman et al.

**Smallest useful remedy.** Replace the binary fossil/tree framing with an information table: observed topology or none; occurrence times or ranges; taxonomy/speciation convention; sampling model; rate-function class; and estimand. Place the nearest theorems and estimators in those cells. Choose one consequential target and ask how much information particular fossil observations add under realistic misspecification. A bounded analytic or simulation design comparison is appropriate only after that target is fixed.

**Strongest reasonable defence.** The authors already recognise the structural/practical distinction, and a portfolio can reasonably decline a methodological project even when it is sound. A new power calculation for a familiar model may indeed be incremental.

**What would change my judgment.** A closely matching existing result covering the same observations, rate class, target and practical operating conditions—or a convincing demonstration that the residual information would not change a scientific inference or sampling decision. I would then support parking the corresponding residual, not automatically the whole entry.

### F-03 — Q-035 and related entries: stopping rules should not require the hoped-for effect

**Claim.** Q-035 says:

> “Park if Δ cannot be distinguished from zero in at least two of three LIP events with paired high-precision records.”

[Commit-specific source: Q-035](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L1860-L1907).

Related active wording includes Q-047’s parking condition when the cross-validated skill interval includes zero, and Q-049’s requirement for a negative tracking-ratio effect in hyperthermals. [Q-047](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L2681-L2769); [Q-049](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L2820-L2873).

**Access:** the decision rules and later debate inspected directly. This is a logical assessment of those rules, **not** an independent reanalysis of terrestrial–marine onset ages or forecast skill. Those empirical estimates remain unverified here.

**Reasoning.** Q-035’s revised scientific question concerns the magnitude and variation of a land–sea lag. A sufficiently precise result near zero answers that question. A wide interval containing zero may instead be uninformative. The quoted rule treats both as a reason to park, using the observed sign/significance rather than the information supplied.

For example, an interval tightly contained within a prespecified biologically negligible lag would oppose a substantial lead–lag mechanism. An interval spanning both large terrestrial leads and large marine leads would not. “Includes zero” cannot distinguish them. Nor does failure to reject zero establish a useful negative answer.

The same logic applies to prediction. A precise upper bound on the added value of deep-time information for modern interchange forecasting could be a consequential negative result for Q-047. A wide interval containing both zero and substantial improvement is a design limitation. For Q-049, the predicted negative coefficient belongs among the hypotheses to test, not among conditions for accepting a competent analysis.

This is especially clear because Q-041 already makes the correct distinction: inconclusive support is not evidence for the null, and a useful bound requires a calibrated procedure. The programme therefore contains its own better precedent. [Q-041 decision rule](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L2313-L2335).

**Consequence.** Used literally, these criteria favour positive-looking questions and can suppress decisive negative science. They can also mislabel low precision as a negative result. This affects **portfolio disposition and design**, not the truth of the underlying hypotheses.

**Smallest useful remedy.** Give each gate three outcomes: informative positive evidence, informative negative/equivalence evidence, and inadequate discrimination. Define a smallest scientifically important lag, effect or predictive improvement before examining the relevant result. Use interval width, calibrated power and attainable bounds to decide feasibility. A project can close because it has answered the question negatively; record that as an answer, not as failure to ask an important question.

**Strongest reasonable defence.** “Park” could mean that EPRP need not commission more work after a negative pilot, and the phrases could be informal descriptions of poor resolution rather than significance filters. The later response explicitly says Q-049’s negative coefficient is a hypothesis, not an acceptance condition.

**What would change my judgment.** Current register wording that carries those distinctions through to operational decisions, including what a precise null would teach. The concern is smaller if the existing rules have never governed an actual selection; it still matters before downstream handoff.

### F-04 — Q-021: keep the lithium idea, but do not let a convenient observation model manufacture—or erase—discrimination

**Claims.** The latest scientific reply proposes that:

> “Each model already outputs the fluxes a seawater Li box model needs”

and says to stop:

> “if the predicted Li distributions overlap at the prior’s width.”

[Commit-specific source: reply 3, Q-021 proposal](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/2026-10-11-phase2-claude-reply-3.md#L77-L113). This is a **live design proposal**, not an executed result or agreed scientific conclusion. The preceding [lithium/model-capability note](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/literature/2026-10-11-q021-lithium-and-model-capability.md) already identifies much of the necessary additional structure.

**Access:** both repository arguments inspected directly. Cao et al.’s primary model description and equations were read; attempts to render its table pages failed, so I do not claim visual validation of those tables. Rauzi’s complete numerical priors, the rival source-model executions and actual flux trajectories were not independently inspected or run.

**Reasoning and evidence.** Cross-prediction is a good objective: independently constrained consequences can be more useful than reproducing a shared temperature history. The dispute is whether the proposed mapping is already sufficiently specified.

A continental silicate-weathering flux is not automatically a dissolved lithium flux, and an authigenic silicon flux is not automatically lithium burial. Conversion depends on composition, retention, uptake and isotope fractionation. Predicting measured shale or chert additionally requires an archive model for detrital versus authigenic contributions. A common *equation form* is helpful, but common fixed priors are not automatically fair if the competing mechanisms themselves imply changes in the relevant fractions or mineralogy.

Cao et al.’s box-model equations explicitly require riverine and hydrothermal Li inputs, two sinks and fractionation terms; their discussion couples enhanced reverse weathering with changed fractionation [R6]. That establishes why a carbon/silica output alone is not the complete isotope prediction. It does not demonstrate that coupling the models is infeasible. The repository’s more cautious note is already substantially right about this.

There is also an important ambiguity in the stopping rule. If “overlap” means overlap of pointwise prior-predictive bands, it is not a valid discrimination test. I constructed a two-observation example:

\[
\mathbf y_A=(-1,1)+b\mathbf 1+\boldsymbol\epsilon,
\qquad
\mathbf y_B=(1,-1)+b\mathbf 1+\boldsymbol\epsilon,
\]

with \(b\sim N(0,10^2)\) shared by both observations and independent errors of standard deviation 0.25. The marginal 95% bands overlap almost completely. Nevertheless, the within-sequence contrast has mean \(+2\) or \(-2\), standard deviation 0.354, and equal-prior optimal classification error approximately \(7.71\times10^{-9}\). The common uncertainty cancels. This deliberately simple calculation proves only that **marginal overlap need not imply joint equivalence**; it says nothing quantitative about Triassic lithium.

The converse is equally important: sharply separated predictions obtained by fixing an unjustified Li-to-Si conversion would not identify the biological mechanism. An assumed mapping can supply the apparent information.

**Consequence.** Neither “unused proxy” nor “shared box model” yet establishes a decisive comparison. A pointwise-overlap stopping rule could discard a useful joint test. An overconstrained mapping could produce false confidence. This affects the **proposed empirical route**, not Q-021’s high importance.

**Smallest useful remedy.** Make one units-and-observation contract: each rival’s native outputs; conversion to elemental Li flux; isotope/fractionation assumptions; sediment measurement equation; chronology; and the data used to constrain each component. Preserve justified mechanism-specific dependencies. Then assess joint predictive separation through the actual observation model, allowing nuisance parameters to vary. This can initially be an algebraic and source-support check, not an integrated climate-model build.

**Strongest reasonable defence.** The proposal expressly says it is not run and may intend full joint predictive distributions, not marginal envelopes. Post-processing native flux histories with a shared module is perfectly legitimate. Much of the missing contract has already been requested by the preceding note.

**What would change my judgment.** Obtained, unit-checked trajectories; a source-backed lithium/archive mapping; and a defined joint decision criterion showing discrimination—or a useful lack of discrimination—across defensible nuisance ranges. If “overlap” already means an appropriately calibrated joint comparison, that part of the concern disappears.

### F-05 — Q-032: retain the abundance caution, but give the interaction question its own revisit condition

**Claims.** The current entry correctly states:

> “It remains an endpoint for ecological interactions.”

But its explicit reopening triggers are a paired abundance calibration or Early Triassic damage censuses. [Commit-specific source: Q-032](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L1687-L1734).

**Access:** the register and its round-5 evidence note inspected directly. Donovan et al. 2020 was read at relevant results, discussion and methods depth; the related 2023 treatment was checked at abstract/metadata depth. Several other cited damage studies were not independently read in full.

**Reasoning and additional context.** The authors have already corrected the mistaken claim that damage has failed an abundance calibration. I agree with that correction. The remaining inconsistency is narrower: demonstrating a host-standardised change in an interaction does not logically require conversion to insect abundance. An interaction endpoint can have ecological importance even if population density cannot be recovered.

However, my initial inclination to reopen this question weakened after checking additional primary context. Donovan et al. describe persistent damage associations on *Agathis*, including a likely K–Pg-crossing leaf-mine association, while distinguishing persistent guilds from proven identity of the insect lineages [R7]. Their later treatment extends the host-associated record [R8]. This is a concrete precedent for using host continuity to investigate interaction persistence; that general route is not an untouched alternative. It also counsels against turning a broad loss-of-specialised-associations pattern into an exceptionless statement.

These studies do not, on the evidence I inspected, establish a calibrated multi-event comparison of interaction disruption against background change. Conversely, demonstrating that such a comparison can be described does not establish its importance, novelty or support. The repository already identifies an event-versus-counterfactual residual. Its value depends on what it would distinguish beyond the existing case studies, not merely on finding an analysis that has not been run.

**Consequence.** I would **retain the current empirical hold**, while revising the revisit conditions and adding the host-associated prior. I would not require an abundance calibration to reopen a genuinely distinct interaction question, nor promote another demonstration of K–Pg damage change.

**Smallest useful remedy.** Add a third trigger: an existing host-resolved dataset and independently defined event/control comparison that can distinguish loss or persistence of interactions from host turnover, sampling and ordinary temporal change. First compare that precise contrast with the closest primary studies. No new register entry or broad data compilation is needed.

**Strongest reasonable defence.** The entry explicitly recognises interactions as an endpoint, records the residual, and parks because several reasons combine—not solely because abundance is uncalibrated. This may be a concise queue-management choice rather than a conceptual error.

**What would change my judgment.** A close published test occupying the specified conditional interaction contrast would favour retaining the hold without further work. A well-supported residual with a clear scientific consequence would justify reopening that route without awaiting abundance calibration.

## 4. Well-supported strengths and judgments I retain

These are affirmative assessments within the inspected scope, not extra faults to satisfy a quota.

### Q-026: the counterexample is real, and the current conclusion is appropriately limited

[Tracked probe](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/data/q026-boundary-observation/probe.py); [tracked table](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/data/q026-boundary-observation/summary.tsv); [current interpretation](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/STATUS.md#L193-L213).

The self-contained code was copied from the pinned file, verified against its Git blob hash and executed. Its output matches the committed table byte-for-byte. Twenty biological lineages persist while their names and fossil detections change. Observed range-through boundary counts and their increments change despite constant true standing richness. The same-prefix fixture also demonstrates that a retrospective boundary count can depend on later fossils.

This is strong evidence against bypassing the observation process by using naive richness-increment moments. It does **not** establish that all capture–recapture or joint observation models fail, and the current status text explicitly avoids that overreach. No biological rate was fitted. This distinction should remain prominent in any handoff.

For Q-026 itself, a prospective cohort and a measurable future recovery target still matter more than elaborating first-passage mathematics on an unsuitable observation series. A valid null forecast could nevertheless be scientifically informative.

### Q-038: conditional prediction is a useful target; deposited-code provenance must remain separate

[Design audit](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/data/q038-flag-audit/README.md); [probe inspected, not rerun](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/data/q038-flag-audit/probe.R).

The move away from a causal “bad luck fraction” toward predicting victim identity conditional on the incoming cohort and total losses is scientifically defensible. It asks whether measured attributes discriminate victims beyond event severity, rather than claiming to partition stochastic and deterministic causes.

The deposited-design flag audit is carefully limited. I inspected its assertions and mapping logic, but did not have the original local RData inputs and did not construct the RMark design myself. Thus its runtime mapping remains an **author-reported result supported by inspected code**, not an independent rerun here. The published coefficient provenance remains unresolved. The primary paper’s methods explicitly support deliberate subgenus elevation [R9]; name nesting alone is not a licence to collapse observations.

One useful implementation contract for the revised question is an exact fixed-loss-count distribution. Under an independent-Bernoulli working model before conditioning, with odds \(w_i\), the conditional probability of a victim set \(A\) of size \(D\) is

\[
P(A\mid |A|=D,X)=
\frac{\prod_{i\in A}w_i}{
\sum_{B:|B|=D}\prod_{j\in B}w_j}.
\]

A common multiplicative change in all odds cancels. The homogeneous null is uniform over the \(\binom ND\) possible sets. I verified the normalisation and cancellation by enumerating six sets for \(N=4,D=2\). This is **one admissible model, not a discovered implementation bug**; correlated extinction models can require a different joint distribution. Scores should match the declared conditional target, and cross-event comparisons should account for cohort size and severity. Conditional skill does not identify absolute risk or the proportion of extinction caused by unmeasured factors.

### Q-004: defend the rate identity, but preserve its biological and model contract

[Register](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/ideas/register.md#L192-L231); [prior-work note](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/literature/2026-10-10-register-checks-round7.md).

Silvestro et al.’s primary derivation supports the common increment in apparent origination and termination rates under its speciation-mode model [R10]. I found no algebraic basis for rejecting the correction. This is a useful question, provided the compared rates refer to compatible clades, intervals, sampling models and biological units.

The subtraction is not a universally applicable discount for any published background number. Differences between fossil and tree estimates can also expose incompatible models or data. Nor does a correction to lineage termination automatically quantify the separate effect of modern taxonomic splitting. The proposed matched-clade design is a reasonable starting safeguard, not proof that both components have been estimated. I recommend **keep, with an explicit matched-estimand contract**; I do not classify the conditional identity itself as a major defect.

### Q-050: protect the distinction between phenomenology and genetic mechanism

[Scientific note](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/literature/2026-10-11-evolvability-and-first-tranche-close.md); [numerical-support audit](https://github.com/BWBrook/eprp/blob/bbe5ce7fc205b3b1f9529757b64e25fd997243cb/data/q050-covariance-support/README.md).

The current note correctly recognises that alignment, climatic-regime comparisons and the broad constraint-versus-selection framing already have close precedents. My selected-section reading of Tsuboi et al. supports that treatment [R11]. The forward route must therefore distinguish explicit rival predictions, not merely fit another alignment relationship.

A useful elementary rival is population mixture. For fixed subpopulation means \(\mu_1,\mu_2\) and common within-population covariance \(\Sigma\), changing mixture weight \(w\) gives

\[
\bar z=(1-w)\mu_1+w\mu_2,
\qquad
P=\Sigma+w(1-w)(\mu_2-\mu_1)(\mu_2-\mu_1)^\mathsf T.
\]

The independent fixture changes the observed mean and covariance while neither constituent population evolves. It demonstrates one confound already acknowledged in the note, not a universal impossibility result. Likewise, unrestricted selection gradients prevent uniquely decomposing a response into genetic covariance and selection. Constrained phenomenological models can still be usefully compared.

I could not independently retrieve the Q-050 archive in this environment. The two numerical objects, shared grid, checksum and matrix checks therefore remain **author-reported audit results**, though the audit text itself was inspected. Its caution about missing original-sample/environment/age support is appropriate. No automatic causal promotion follows from an accessible covariance matrix, and lack of such promotion does not make evolvability an unimportant question.

### Additional limited endorsements

The later rejection of unconditional Q-034→Q-004 and Q-037→Q-038 mergers is justified by their different target quantities. Shared methods are not scientific redundancy. The decision against an integrated, one-size-fits-all PBDB/chronology engine is also sensible before accepted analyses establish common requirements.

I agree with Q-044’s corrected distinction between recorded near-saturation and biological turnover, and with Q-027’s withdrawal of a support-count “ceiling.” Those are **text-level endorsements**: I did not independently rerun their data screens. Q-046’s density problem is a valid limitation on the proposed total-flux route; I did not inspect enough of its nearest energetic literature to recommend reopening the parent question.

## 5. How the phase-2 debate changed this review

The register-first record is supplied separately so these changes are inspectable.

| Initial assessment | After the debate and source checks |
|---|---|
| Cheapness and modern transfer might dominate importance. | The later replies explicitly accept separate importance and next-work judgments, and remove modern transfer as a significance bonus. I do not report the superseded first rubric as the current policy. The register’s tier definition still mixes tractability, openness and importance, and “modest or methodological” remains an unhelpful category. |
| Q-006 could be undervalued. | Retained, strengthened by comparing the actual scopes of the primary sources. The later discussion acknowledges the distinction but does not fully repair the parking rule. |
| Q-032 might have been parked too quickly. | Narrowed. Its current text is more careful than its original wording, and the additional *Agathis* literature occupies part of the obvious rescue route. Revise the trigger; do not simply promote it. |
| Q-021 could support a major mechanistic programme. | Retained, with lower confidence in the immediate lithium shortcut. The latest unresolved exchange concerns an actual observation-model contract, not merely which published model is preferred. |
| Q-042 is more valuable as partial identification than as another point estimate. | Retained. The algebra checks out; the incompatible input definitions become the first decision to resolve. |
| Q-027/Q-044 might still overstate what support screens establish. | Much of this is already corrected. I do not reissue the withdrawn country/era/saturation claims as present errors. Their next empirical gates remain unverified. |
| Q-038 and Q-050 need strict inference boundaries. | Retained, but the current audit notes already make most of those boundaries explicit. They are strengths to preserve rather than newly discovered oversights. |

Agreement between agents was never counted as evidence. Their later reasoning mattered where it repaired a claim or supplied an inspectable source, not because two models endorsed it.

## 6. Coverage and dispositions

**Substantively reviewed** means more than the register: a relevant evidence note, primary-source comparison, code inspection or independent calculation was used to assess a material part of the question. It does not mean every cited source, implementation or empirical claim was verified. **Skimmed** means the full register entry was read but the supporting scientific dossier was not deeply audited. No entry is wholly unassessed at register level; many subordinate empirical and novelty claims remain unassessed.

Only eight entries are marked substantive. Narrow rule checks on Q-035/Q-047/Q-049 do not turn them into full scientific reviews. “No disposition” is deliberate, not a missing table cell.

| ID | Coverage | Disposition within this review |
|---|---|---|
| Q-001 — Physiological habitat-loss transfer | Skimmed | No disposition |
| Q-002 — Dose and extinction selectivity | Skimmed | No disposition |
| Q-003 — Threshold versus smooth response | Skimmed | No disposition |
| Q-004 — Pseudoextinction and background rates | Substantive | Keep; clarify contract |
| Q-005 — Deep-time precursors | Skimmed | No disposition |
| Q-006 — Diversification identifiability | Substantive | Revise; develop |
| Q-007 — Biotic legacy under an environmental path | Skimmed | No disposition |
| Q-008 — Geographic differentiation and recovery | Skimmed | No disposition |
| Q-009 — Predictive ecological memory | Skimmed | No disposition |
| Q-010 — Biological innovation and diversity capacity | Skimmed | No disposition |
| Q-011 — Extinction-event size distribution | Skimmed | No disposition |
| Q-012 — Heritable susceptibility versus ageing | Skimmed | No disposition |
| Q-013 — Modern extinction through the fossil filter | Skimmed | No disposition |
| Q-014 — Deep-time extinction debt | Skimmed | No disposition |
| Q-015 — Thermal-niche evolution | Skimmed | No disposition |
| Q-016 — Range-based extinction prediction | Skimmed | No disposition |
| Q-017 — Unseen extinction and detection frameworks | Skimmed | No disposition |
| Q-018 — Plant and terrestrial mass extinctions | Skimmed | No disposition |
| Q-019 — Climate versus biotic turnover drivers | Skimmed | No disposition |
| Q-020 — When range stops providing insurance | Skimmed | No disposition |
| Q-021 — Biological functions and Earth-system recovery | Substantive | Keep; revise gate |
| Q-022 — Evolutionary-history loss | Skimmed | No disposition |
| Q-023 — Origination failure versus extinction spikes | Skimmed | No disposition |
| Q-024 — Quaternary early warnings | Skimmed | No disposition |
| Q-025 — Local-to-global loss scaling | Skimmed | No disposition |
| Q-026 — Prospective reversible versus terminal decline | Substantive | Keep |
| Q-027 — Climate and the latitudinal diversity gradient | Skimmed | No disposition |
| Q-028 — Winners of past and present crises | Skimmed | No disposition |
| Q-029 — Ordering isolation and reconnection | Skimmed | No disposition |
| Q-030 — Changing biosphere sensitivity | Skimmed | No disposition |
| Q-031 — Warming and body-size change | Skimmed | No disposition |
| Q-032 — Insect ecological crises | Substantive | Park empirical route; revise trigger |
| Q-033 — Arrival order and radiation | Skimmed | No disposition |
| Q-034 — Pre-human island extinction baselines | Skimmed | Do not merge into Q-004 |
| Q-035 — Land–sea collapse lags | Skimmed | Revise rule only |
| Q-036 — Morphological stasis and geography | Skimmed | No disposition |
| Q-037 — Trophic selectivity | Skimmed | Do not merge into Q-038 |
| Q-038 — Conditional victim prediction | Substantive | Keep revised target |
| Q-039 — Coupling of evolutionary faunas | Skimmed | No disposition |
| Q-040 — Marine diversity and spatial support | Skimmed | No disposition |
| Q-041 — Extinction periodicity | Skimmed | Keep corrected rule only |
| Q-042 — Species magnitude of mass extinctions | Substantive | Keep; revise design |
| Q-043 — Survivor composition and future evolution | Skimmed | No disposition |
| Q-044 — Terrestrial diversity and regional richness | Skimmed | No disposition |
| Q-045 — Data-vintage robustness | Skimmed | No disposition |
| Q-046 — Total animal energy use | Skimmed | No disposition |
| Q-047 — Past interchange and modern prediction | Skimmed | Revise rule only |
| Q-048 — Predator release and prey persistence | Skimmed | No disposition |
| Q-049 — Pre-outcome isotherm tracking | Skimmed | Revise rule only |
| Q-050 — Changing capacity to evolve | Substantive | Keep; retain empirical hold |

`coverage.tsv` adds the exact scope limitation for every row.

## 7. Development priorities—not project selection

### Candidate A: Q-021 — biological functions and Earth-system recovery

**Scientific importance: high.** A credible result could distinguish whether particular ecological losses materially altered recovery dynamics, rather than merely accompanying external forcing. An informative negative result would restrict claims that biological feedbacks are needed to explain the persistence of a disrupted state. The scientific value is not contingent on modern applications.

**Next-work priority: high for a bounded contract; low for immediate model integration.** The existing comparative notes already reveal a potentially informative disagreement, but the native outputs do not yet establish the shared observable prediction.

**Cheapest decisive test.** Take one candidate record and one pair of rival flux histories. First establish that their units, chronology, transformations and calibration roles permit a common lithium/other-proxy observation model. Determine whether any joint contrast remains constrained after plausible conversion and archive uncertainty. Missing or unconstrained transformations can terminate that particular comparison before codebases are coupled.

**Usable evidence inspected:** the repository’s contrasting arguments and capability note, plus Cao’s model equations. Actual native trajectories and complete numerical priors were not verified here.

**Main failure mode:** mechanism predictions become interchangeable once weathering composition, uptake, fractionation and sediment mixing vary realistically—or seemingly strong separation comes only from fixing those nuisance quantities. The appropriate result can be a map of what extra observation is needed, not a preferred mechanism.

### Candidate B: Q-042 — species-level magnitude of mass extinction

**Scientific importance: high.** This affects what quantitative claims about the severity of major losses actually mean. The useful contribution may be demonstrating which comparisons are defensible and how much of a familiar percentage comes from extrapolation.

**Next-work priority: high for estimand reconciliation and bounds; conditional for a larger simulator.** An elaborate simulation with mismatched inputs would not solve the current problem.

**Cheapest decisive test.** Reconcile one event’s genus inputs to an explicit baseline species cohort and time interval. Establish what is known about genus sizes and species retained in surviving genera. Compute sharp assumption-labelled bounds, then ask which proposed regional observations could tighten them without silently assuming global representativeness.

**Usable evidence inspected:** the register’s explicit conflicting inputs, the cited Stanley abstract and the independently verified bound. The Wang/Fan raw species–genus crosswalk was not inspected; it remains a lead, not verified calibration data.

**Main failure mode:** bounds remain too broad, or their useful narrowing depends on species/genus composition and transport assumptions that cannot be constrained. A rigorous demonstration of that limit may still matter, but it would not justify a new preferred global percentage.

### Candidate C: Q-006 — what information makes diversification inference useful?

**Scientific importance: potentially high and cross-cutting.** The value lies in changing a substantive inference or evidence-acquisition decision, not in proving a theorem simply because it remains open in a general form.

**Next-work priority: high for a tightly scoped theory/literature comparison; not a universal “minimum fossil count” project.** This can proceed without the ignored raw cache.

**Cheapest decisive test.** Choose one biological functional—such as an integrated extinction contrast over a stated interval—and one observation setting. Compare the compatible range/FBD formulations and their identification assumptions. Ask whether a small change in fossil information breaks relevant equivalence or merely sharpens a misspecified estimate. Preserve separate labels for topology information, occurrence information and assumptions supplied by the model.

**Usable evidence inspected:** Truman’s specified structural results, Stadler’s range likelihood, Beaulieu–O’Meara’s more restricted performance question, and the newer adjacent-field information lead. These supply starting models and cautionary boundaries, not a new theorem proved here.

**Main failure mode:** the matched practical question is already answered, or the proposed extra information only helps under assumptions that dominate the inference. That would support closing the specified residual. It would not retrospectively establish that fossils have little general practical value.

**Readiness:** these are candidates for further programme development. I do not recommend immediate handoff as a primary research project for any of them on this inspection alone.

## 8. Gaps and process

### Missing questions

I do not recommend adding entries during this pause. I did not establish a sufficiently distinct, consequential omission after accounting for the register’s broad overlaps. The strongest missing *treatment* is an explicit information-design perspective within Q-006 and related entries, not a defensible fifty-first question. Q-010, Q-029, Q-043 and Q-046 should not be judged unimportant merely because their current empirical routes are difficult; I have not completed the prior-work checks needed to reopen them.

### Five concrete workflow changes

1. **Make gates outcome-neutral.** Every gate should distinguish an informative answer in either direction from insufficient discrimination. Keep minimum event/window counts as screens unless calibrated; keep numerical effect thresholds tied to scientific consequences.
2. **Compare prior work by target and assumptions.** For a promising question, replace another broad scan with a small nearest-prior matrix: what was observed, what was estimated, which rival was tested, what remained ambiguous, and what the proposed result would change. A published assertion, a test and a decisive answer are not the same thing. Neither “not found” nor a changed title establishes novelty.
3. **Maintain one current scientific contract per active question.** Record the target, observation unit, comparison, permitted interpretation, unresolved assumptions and next decision in one short location. Link dated debates as history. The latest accepted rule should not have to be reconstructed from several replies. Explicitly label live disagreements, as in the Q-021 proposal.
4. **Keep small evidence fixtures and dependency provenance.** Hash-pinned, self-contained examples like Q-026 are unusually reusable. Add a compact dependency record for shared data, chronology and calibration, so reused series are not counted as replication. Shared extraction utilities are useful; shared scientific assumptions should not become defaults by accident.
5. **Separate importance, evidence sufficiency and expected information from cost.** The later debate makes the right change, but the register’s tier definition still calls tier 3 “modest or methodological.” Retire that association. A difficult foundational question can merit protection; a cheap contract audit can be valuable work without elevating its parent question. Do not assign replacement numerical scores without a decision they improve.

The repository is already better than a list of attractive titles: its evidence-depth labels, retention of parked questions, correction history and explicit observation concerns can save a new team substantial false starts. Its main reuse cost is the amount of debate a team must reconstruct to know which claim is current. More commentary is not the remedy; a shorter current contract is.

## 9. Verification limits and reproducibility

### What was actually executed

**Q-026 source reproduction.** The pinned `probe.py` was copied into a local working directory and its Git blob hash verified as `0409b0a48ce8c02c8594c3972cf549438c34633e` (6,079 bytes). It was executed with Python 3.13.5 using the supplied defaults: 20 lineages, 12 bins, 1,000 replicates for each of six fossil/replacement-rate combinations, and the six documented seeds. All assertions passed. The generated `summary.tsv` has Git blob hash `e903f5070abe271405c5118f12acffff15030c65`, matching the committed table exactly. `q026_rerun_receipt.json` records the run; the bundle includes the inspected source and reproduced output.

**Independent review fixtures.** `python checks.py` was actually executed. Four deterministic checks passed: Q-042 conditional bounds and cohort-retention example; Q-021 marginal-versus-joint discrimination example; Q-038 exact conditional normalisation and intercept cancellation; and Q-050 mixture covariance. Inputs are hypothetical. The code and `checks_results.json` are supplied. These are algebraic checks, not new analyses of fossil observations.

**Not executed:** RMark/MARK fitting or design reconstruction; Q-027/Q-044 raw-data pipelines; Q-050 archive inspection; SCION/Isson/Rauzi/Cao model runs; extinction-rate estimation; primary ecological analyses. Commands printed in repository READMEs were not counted as runs.

### Consequential uncertainties and the smallest resolving items

| Uncertainty | What can be assessed now | Smallest additional item that would materially help |
|---|---|---|
| Q-042 common genus/species target | Internal metric mismatch and conditional mathematics | One source-by-source cohort/window/metric crosswalk, followed by one suitable species–genus table with sampling scope |
| Q-006 matching practical precedent | Scope of selected primary models and results | A precise target/observation/model specification; not an export of more data |
| Q-021 lithium discrimination | Model-mapping requirements and invalidity of marginal-overlap shorthand | One unit-checked pair of native trajectories, a source-backed Li/archive mapping, and the full nuisance/observation contract |
| Q-038 actual deposited runtime mapping | Code logic and repository-reported table; not independent execution | The named checksum-matched RData input for the existing probe; published-fit attribution separately needs the source-to-fit/session mapping |
| Q-050 original numerical series and environmental support | Audit text and theoretical limits | The versioned archive for numerical verification, plus a compact original-sample/absolute-age/environment crosswalk for scientific support |
| Q-027/Q-044 biological support and sampling effects | Current reconciled interpretations and reported screens | A small estimator-specific worked support table with eligibility and detection definitions; raw inputs only where needed to reproduce it |
| Claims attributed to unavailable board discussions | Durable scientific content in linked notes | The precise missing assumption or derivation written into its current contract, not the board export |

No finding here depends on an unseen board message. I cannot verify board-only authorisations, execution claims or reasoning. References to local absolute paths identify provenance, not files I possessed.

### Access failures

Some PMC/PNAS/publisher routes returned challenge pages or access errors; direct container network requests failed DNS resolution. In particular, I did not obtain Stanley’s full methods or independently verify Rauzi’s full numerical prior specification. Q-050’s documented public archive URLs were attempted but did not yield usable bytes in this environment. These are **access limitations, not evidence of absent data or false author claims**.

PDF text was used only where legible. I attempted page screenshots for the relevant source checks. A screenshot of the 2026 phylodynamic preprint’s first page succeeded; several other PDF screenshots, including Cao’s table pages, returned internal errors. Therefore those failed images/tables were not visually verified. No empirical figure measurement was inferred from an unseen image.

No primary author was contacted, no GitHub issue or pull request was created, and no repository file was changed. The supplied artifacts are local review deliverables only.

## 10. Primary-source verification record

The links below are verified identifiers or stable primary-source URLs. Access depth is the reviewer’s, not the deeper reading sometimes reported by the repository’s authors. This is a targeted record, not a systematic bibliography. The individual paper summaries are deliberately restricted to the claims used above.

**R1 — Stanley (2016).** *Estimates of the magnitudes of major marine mass extinctions in earth history.* DOI [10.1073/pnas.1613094113](https://doi.org/10.1073/pnas.1613094113); [PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/27698119/). **Read:** primary abstract. **Not read:** full methods/supplement; attempted routes failed. Supports differences in background treatment and event scope, not an independently verified reconstruction of the 81% calculation.

**R2 — Truman et al. (2025).** DOI [10.1093/sysbio/syae058](https://doi.org/10.1093/sysbio/syae058). **Read:** primary HTML, relevant theorem statements and discussion of finite-data limits. The specified fossil-sampling and removal assumptions matter. I did not independently certify the entire proof. A later supplement correction was located; it was not treated as a reversal of the theorem.

**R3 — Beaulieu & O’Meara (online 2022; issue 2023).** *Fossils Do Not Substantially Improve, and May Even Harm, Estimates of Diversification Rate Heterogeneity.* DOI [10.1093/sysbio/syac049](https://doi.org/10.1093/sysbio/syac049). **Read:** abstract, introduction and selected sections on sampling ancestors and model treatment. Used to delimit the practical claim’s scope, not to generalise its performance results to all fossil inference.

**R4 — Stadler et al. (2018).** *The fossilized birth–death model for the analysis of stratigraphic range data under different speciation modes.* DOI [10.1016/j.jtbi.2018.03.005](https://doi.org/10.1016/j.jtbi.2018.03.005); [author preprint](https://arxiv.org/abs/1706.10106). **Read:** published abstract; preprint introduction, relevant topology-integration/corollary discussion and discussion sections. Supplies a range-data likelihood under specified conditions, not a general occurrence-only identifiability proof.

**R5 — Dieselhorst & Stadler (2026).** *Information on hidden birth events restores identifiability in phylodynamic inference.* [arXiv:2604.17926v1](https://arxiv.org/abs/2604.17926v1). **Read:** preprint abstract and relevant theorem statements, including the extra-information/mutation assumptions; first-page screenshot checked. **Status used here:** inspected preprint version, not an asserted peer-reviewed or empirically validated palaeobiological method. Its general transfer to macroevolution is an unverified lead.

**R6 — Cao et al. (2022).** *Persistent late Permian to Early Triassic warmth linked to enhanced reverse weathering.* DOI [10.1038/s41561-022-01009-x](https://doi.org/10.1038/s41561-022-01009-x); [author-institution PDF](https://earthsciences.osu.edu/sites/default/files/2022-11/s41561-022-01009-x.pdf). **Read:** selected results/discussion on reverse weathering and fractionation, and Methods’ Li mass/isotope balances. Table screenshots failed; no model execution or supplement validation. Used for the required mapping terms, not to settle the competing seawater reconstructions.

**R7 — Donovan et al. (2020).** *Persistent biotic interactions of a Gondwanan conifer from Cretaceous Patagonia to modern Malesia.* DOI [10.1038/s42003-020-01428-9](https://doi.org/10.1038/s42003-020-01428-9). **Read:** relevant primary results, discussion and methods, including the distinction between guild/association persistence and secure insect-lineage continuity. No image-based identification was independently performed.

**R8 — Donovan et al. (2023).** *Insect herbivore and fungal communities on Agathis (Araucariaceae) from latest Cretaceous to Recent.* DOI [10.3897/phytokeys.226.99316](https://doi.org/10.3897/phytokeys.226.99316); [PubMed](https://pubmed.ncbi.nlm.nih.gov/37274755/). **Read:** abstract and metadata. Not used to claim that a formal multi-event counterfactual test is already done.

**R9 — Monarrez et al. (2023).** DOI [10.1098/rsos.230795](https://doi.org/10.1098/rsos.230795); [NSF-deposited paper](https://par.nsf.gov/servlets/purl/10514226). **Read:** relevant methods on taxonomic conventions and occurrence construction. Original local data and fitted-result provenance were not reconstructed. PDF screenshot attempt failed; no claim of figure-level replication.

**R10 — Silvestro et al. (2018).** DOI [10.1038/s41467-018-07622-y](https://doi.org/10.1038/s41467-018-07622-y). **Read:** primary results/equations on apparent versus lineage rates, compatible/incompatible model treatment, and relevant discussion. Supports the conditional rate identity, not universal attribution of fossil/tree discrepancies to pseudoextinction.

**R11 — Tsuboi et al. (2024).** *The paradox of predictability provides a bridge between micro- and macroevolution.* DOI [10.1093/jeb/voae103](https://doi.org/10.1093/jeb/voae103). **Read:** selected primary sections on constraint, selection shaping variation, and process-based variance models. Did not rerun the associated [versioned archive](https://doi.org/10.5281/zenodo.13294509).

**R12 — Brombacher et al. (2021), supporting context only.** *The Dynamics of Diachronous Extinction Associated With Climatic Deterioration Near the Neogene/Quaternary Boundary.* DOI [10.1029/2020PA004205](https://doi.org/10.1029/2020PA004205). **Read:** primary methods/results and relevant discussion returned through the publisher’s indexed text. Useful for population-specific trajectories and evidence crosswalks; not treated as a new AR(1) test or independent replication of reused material.

**R13 — Schachat et al. (2022), limited-access lead.** DOI [10.1016/j.revpalbo.2021.104564](https://doi.org/10.1016/j.revpalbo.2021.104564). **Checked:** metadata for the theoretical-ecospace treatment of fossil insect herbivory. Full text not obtained by this reviewer. The description of its proposed event/control test remains attributed to the inspected repository note, not independently established on priority.

**R14 — Rauzi et al. (2024), verification limit.** DOI [10.1073/pnas.2318860121](https://doi.org/10.1073/pnas.2318860121); [PubMed metadata verified](https://pubmed.ncbi.nlm.nih.gov/39074280/); [PMC record attempted](https://pmc.ncbi.nlm.nih.gov/articles/PMC11317597/). The repository’s source-specific account was inspected; my direct route encountered an access challenge. I do not rely on an independently verified numerical prior or model rerun from this paper.

---

**Bottom line:** retain the programme’s broad scientific ambition, but make the next decisions depend on matched target quantities, actual information and useful answers in either direction. The strongest contribution of this review is a small set of changes to those decisions—not a replacement ranking of fifty incompletely audited ideas.
