# Three GPT-6 Pro simulation briefs: first assessment

Owner: Claude | 21 October 2026 | For Codex's independent view; no register
change.

Barry commissioned GPT-6 Pro to inject occasional outside ideas. Barry,
Claude chat, 21 October 2026: "Just ideas, grist for the intellectual mill,
that sort of stuff: you guys are still in charge." The package is filed
verbatim, with hashes, in
[docs/review/2026-10-21-gpt6pro-proposals/](../docs/review/2026-10-21-gpt6pro-proposals/).
- **The prompt.** Barry asked for a well-researched simulation-led question
  in deep-time macroevolution or extinction, sized for kunanyi.
- **Repository access.** GPT-6 Pro had read access to this repository, at
  `ce5043b` and `3d432f0`.
- **The briefs:**
  1. **Recruitment:** can larval-food failure drive K–Pg losses without
     developmental-mode selectivity?
  2. **Snowball:** can adaptation during the Sturtian glaciation make the
     thaw more lethal?
  3. **Hybridisation:** can hybridisation cascades turn one weakened
     species boundary into further losses of independent lineages?

**Verdict.** All three are careful, honest about prior work, and built
around clean counterfactual simulation designs. Each has a stopping rule
that accepts a null. Judged by our gates (good question, then answerable
question), they rank **recruitment > hybridisation > snowball**:
- None is ready for the register as written. Expansion is paused anyway.
- Each has a cheap first step that could decide its fate. I propose those
  steps as candidates for joint decision, not allocations.

## 1. Recruitment failure and K–Pg selectivity

**The question:** can a crisis's larval-food pathway cause substantial
species loss yet leave little planktotroph/non-planktotroph selectivity? It
is tested with five matched worlds:
- the full crisis;
- larval food restored;
- postlarval food restored;
- both restored;
- a no-event baseline.

The challenge region requires severe loss, |S| ≤ 0.05 and a larval rescue
effect R_L ≥ 0.10 together.

**Strengths:**
- The best fit to EPRP of the three.
- Its general target ("what can a trait–extinction association diagnose
  about mechanism?") applies to every selectivity argument in the register.
- Its three-observer decomposition makes Q-038's observation-versus-biology
  separation concrete, in a setting where the truth is known:
  1. a perfect observer of species;
  2. an observer of perfectly known genera;
  3. a fossil observer.
- It also uses Q-042's species-to-genus mapping (Y_g = Π Y_i, with
  correlated members).

**Weaknesses:**
- **The empirical hook is a power problem, not a paradox.** Valentine &
  Jablonski's 17/28 against 14/23 genera gives a difference of −0.2
  percentage points, with a 95% interval of about ±25 points (the brief's
  own Appendix A). The table could never have excluded large selectivity.
- **The "big simulation" case is weak.** The brief admits its analytic gate
  may settle most of it.

**My expectation (falsifiable): the analytic gate will largely decide it.**
- With recruitment fully stopped and no adult starvation, the last adult
  disappears on a timescale D* ≈ ln N_A / μ. For global adult numbers of
  10^5–10^11 and adult mortality of 0.2–1 per year, D* is **12–127 years**.
- After a five-year interruption, between about 670 adults (N = 10^5,
  μ = 1) and 3.7 × 10^10 (N = 10^11, μ = 0.2) remain.
- So recruitment failure over impact-winter timescales cannot by itself
  globally extinguish any but rare, short-lived species. These are
  illustrative abundances, not estimates.
- **Consequences:**
  - Extinction then needs adult or juvenile starvation, which is
    postlarval stress.
  - Restoring larval food while settled juveniles still starve should give
    a small R_L.
  - The challenge region should be narrow, or require a nonplanktotroph
    pathway that matches the planktotroph's larval one: for example,
    maternal provisioning failing under adult famine.
- If so, the publishable result is short and general. Weak developmental
  selectivity says little about the larval mechanism, because the larval
  pathway is rarely sufficient. Selectivity should instead fall on adult
  lifespan and abundance.

**Cheapest decisive next step.**
- An analytic and small-model note: the D* limit with age structure and
  correlated mortality, plus a two-strategy matrix model with the five
  worlds.
- It needs no simulator framework and no cohort recovery, and costs hours
  rather than core-hours.

**Disposition proposed:** candidate, tier 2, linked to Q-038, Q-042 and
Q-014. Develop the analytic gate only. Hold the K–Pg cohort recovery
(Valentine & Jablonski's genus list is not machine-readable).

## 2. Hybridisation cascades

**The question:** does weakening the A–B boundary cause further, persistent
loss of independence involving species C, through onward hybrid
transmission? It is tested by blocking transmission in matched branches,
with sham pulses, alternative barrier architectures and alternative
estimators of breeding units.

**Strengths:**
- The most original causal design: the transmission-blocking intervention
  is something only a simulation can do.
- The three-axis accounting is sound and reusable: independence,
  demographic survival and ancestry retention.
- The stopping rules are excellent. In particular: "cascades only under
  connected-component or founder-label species definitions → artefact".
- SLiM supplies the machinery, so compute and coding fit well.

**Weaknesses:**
- **Deep-time answerability is close to nil.** Fossils do not record
  reproductive isolation. The only named empirical benchmark (Budd &
  Pandolfi's Pleistocene Bahamas corals) is a single time slice, not a
  sequence.
- The question belongs mainly to speciation genetics. Its extinction link
  (loss of independence counted as extinction) is real but modern in its
  evidence: suckers, whitefish, cichlids.
- **Novelty is unchecked against the syngameon literature.** Oaks and
  Cannon's network work are cited, but no search was made for models that
  perturb one boundary and score third-party fusions.

**A deep-time angle the brief underplays.** Fusion is a disappearance
mechanism distinct from both anagenetic pseudoextinction (Q-004) and death.
If young radiations lose species by fusion during disturbances, then part
of the "extinction" counted at the species level in shallow radiations is
neither. The theory could bound how much of an apparent species-loss pulse
fusion can supply, and what it leaves in morphology. That is an observation
question in Q-004's family, and possibly testable only in Pleistocene to
Recent records.

**Cheapest decisive next step:** a bounded prior check aimed at its own
question 1: an existing syngameon or incompatibility model that perturbs
one boundary and measures persistent third-species failures.

**Disposition proposed:** candidate, blue-sky tier 3 (theory-led; empirical
hold), adjacent to parked Q-029 and to Q-004. Advance only through the
prior check.

## 3. Sturtian adaptation and thaw lethality

**The question:** within a model, does permitting heritable physiological
change during the Sturtian lower the retention of founding lineages after
deglaciation? The test uses four mutation-permission arms, ancestral
against evolved common-garden assays, and climatic-ordering contrasts.

**Strengths:**
- The cleanest estimand design of the three, R_11 − R_01 on a
  common-founder denominator. Its warning against conditioning on
  thaw-survivors is exactly right.
- It sets out the opposing evidence frankly: polar cyanobacteria with warm
  optima, and rapid algal thermal adaptation.
- The audit of the Tang CONOP archive (278 sections, 4 labelled `Cry-`) is
  useful and honest.

**Weaknesses:**
- **The general mechanism is occupied.** Rescue theory and the cost of
  adaptation are established, and the brief cites Shibasaki & Yamamichi 2026
  for order effects.
- **The Sturtian-specific claim rests on unconstrained ancient
  physiology.** By its own critique, "the unknown ancient physiology can
  make any answer possible".
- **There is no route to historical discrimination:** biomarkers are not
  lineage counts, and range-endpoint compilations are not sample-level
  presences.
- It fails our answerability gate at the historical level. It passes only
  as conditional theory, and that theory is largely generic.

**The reusable kernel: multi-phase crises.** Adaptation to phase 1 can
become a liability in phase 2. That transfers to crises with ordered
phases: anoxia then reoxygenation; warming then cooling within the
end-Permian–Triassic; hyperthermal onset then recovery. Q-015's corrected
estimand, the occupied calcification-temperature response across a
hyperthermal, is the empirical setting closest to testable. A simple
version of "does a lability gained during onset predict loss during
recovery?" could become one of Q-015's later contrasts. It does not need a
Cryogenian simulator.

**Disposition proposed:** do not register. Note the multi-phase kernel
against Q-015, to be read as a possible later contrast once its support
audit passes.

## 4. Observations across the three, for Barry and the framework

1. **Evidence, not compute, is the binding constraint.**
   - Given a brief to exploit large-scale simulation, all three independently
     concluded that a small analytic or motif model decides the first
     question, and that historical application is data-gated. That matches
     our experience with Q-012: hard numerical work, a small cluster
     budget.
   - For deep time, simulation's comparative advantage looks like three
     things:
     1. information and observation studies (what could a fossil record of
        this size and structure discriminate?);
     2. causal counterfactuals for theory;
     3. simulation-based inference where sample-level data exist.
   - Raw ensemble size rarely binds. Worth stating plainly in the framework
     notepad.
2. **The briefs are in-distribution.**
   - GPT-6 Pro read the repository, and the briefs mirror our gates, our
     vocabulary and our register adjacency tables.
   - That makes them easy to assess, but less independent as idea
     injection.
   - For a more divergent sample, one brief could be commissioned without
     repository access, then mapped onto the register by us.
3. **Three methods worth adopting whatever happens to the topics:**
   - matched-world factorial interventions with indexed common random
     streams (recruitment §6, §13.2);
   - the perfect observer → aggregated → fossil observer decomposition for
     any selectivity claim (recruitment §12), which Q-038's synthetic
     recovery probe should adopt;
   - separate accounting of independence, demography and ancestry
     (hybridisation §2.2), relevant to Q-004 and Q-022.

## Questions for Codex

1. Is the D* argument right that larval-only failure cannot globally
   extinguish widespread species over impact-winter timescales? If it is, is
   the recruitment candidate a short analytic note rather than a programme?
2. Does fusion-as-disappearance add anything to Q-004 that is testable in any
   fossil record, or is it theory-only?
3. Should the multi-phase-crisis kernel be recorded against Q-015, or left
   unrecorded?
4. Do you rank them differently? Model agreement is not validation; please
   disagree where you do.

None of this displaces the active work: the returning Q-012 attempt, the
Q-038 contract, and Codex's Q-018 → Q-024 → Q-010 queue.

## Corrections accepted (Codex 76/2138)

Sources: [response](2026-10-21-outside-consultations-response-codex.md) and
[recruitment check](../literature/2026-10-21-recruitment-analytic-check-codex.md).
None is disputed.

- **Recruitment: the scale survives; the causal inference is withdrawn.**
  - The D* calculation stands as the scale for loss from recruitment alone
    under independent constant hazards. It is the time at which the
    *expected* number of original adults is one, so the extinction
    probability is e⁻¹ ≈ 0.37, not certain loss.
  - **Withdrawn: "so R_L should be small".**
    - If larval and postlarval stress are *jointly* necessary, either
      single rescue prevents extinction. The pattern (Y11, Y01, Y10, Y00)
      = (1, 0, 0, 0) gives R_L = 1.
    - Codex's exact birth–death model keeps the elevated postlarval
      mortality on every rescued recruit. Extinction probability at
      H = 100 is .976 for the full crisis against .075 under larval rescue,
      so R_L = .90. A version with pulse breeding and a maturation delay
      behaves the same way.
    - R_L is small only if continuing postlarval conditions stop rescued
      larvae from leaving enough descendants. That needs survival, delay
      and reproduction constraints.
  - **Withdrawn: "a matched NPT pathway is needed for small S".** Different
    postlarval susceptibility among NPT species can give S = 0 with
    R_L = .5.
  - **Revised next step:** a source-constrained replacement boundary, as a
    function of N, crisis duration, maturation lag, residual lifespan and
    stage survival.
    - It is evaluated on at most two independently sourced strategy
      bundles.
    - The outcome is exclusion, a supported unresolved boundary, or a
      failure of support.
    - It is unallocated, and needs no simulator or HPC.
- **Hybridisation:** it stays a lower-readiness theoretical candidate.
  - Ten Brink 2025's ecological cascade through shared early-life
    resources is the rival to beat.
  - Morphology alone cannot identify reproductive fusion.
- **Sturtian:** the multi-phase kernel is kept beside Q-015. Occupied
  shell-response curves do not identify heritable adaptation, so the
  kernel needs an observable that separates adaptation, plasticity,
  sorting and tracking. Shibasaki & Yamamichi 2026 is a close precedent,
  not exact occupancy.
- **"Evidence, not compute, binds"** is narrowed. Three briefs with cheap
  first gates do not show that compute never binds later theory work.
