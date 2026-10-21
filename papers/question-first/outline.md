# Outline (WIP)

Each section lists its **claims**, the **evidence** already in the record,
**gaps** to fill, and **threats** that could undercut the claim. Pointers are
to repository paths and Correspondence messages (thread 76 unless stated).

Working title: *Question first: adversarial vetting of research questions by
AI agents before project work.* Alternative: *Most of the work is choosing
the question.*

## 1. Introduction

- **Claims:**
  - AI systems now make execution cheap: code, literature synthesis,
    analysis, drafting.
  - The cheap path is to start answering at once.
  - The expensive failures are upstream: questions that are already
    answered, cannot be answered with existing data, cannot separate their
    rival explanations, or cannot reach the needed precision.
- **Evidence:** framing quotes from Barry (19 and 21 October, in the
  framework notepad and the folder README).
- **Gaps:** prior literature, none of it yet verified. Each entry needs a
  bounded, cited check:
  - on problem formulation and Type III error;
  - on preregistration and pre-mortems;
  - on research-on-research;
  - on AI-scientist and co-scientist systems, and how they evaluate novelty
    and feasibility.
- **Threats:** the claim may be familiar ("plan before you act"). The
  contribution must be the *measured* record and the specific failure
  catalogue, not the slogan.

## 2. Setting and participants

- **Claims:** the programme in brief.
  - Deep-time palaeobiology.
  - One human: Barry Brook, facilitator and equal contributor.
  - Two AI agents, Claude and Codex, as collegial antagonists.
  - An append-only board, a git repository, and a cluster allocation.
  - The period is 7 October 2026 onwards.
- **Evidence:** `AGENTS.md`, `STATUS.md`, `docs/programme.md`,
  `resources/capability-inventory.md`, and the board history.
- **Gaps:**
  - the exact model versions per period (board model fields);
  - Barry's time per week, which is not yet recorded.
- **Threats:** a single programme. One domain, one human and one pair of
  agent families.

## 3. The method

- **Claims:**
  - **A stage structure with artefacts:** seed, prior check, contract,
    support audit, identification design, finite contract, technical pilot,
    disposition, ranking.
  - **The order is a dependency structure, not a waterfall.** Run first the
    cheapest check that could change the disposition.
  - **Gates:**
    - is it a good question? (testable, separable, interesting);
    - can it be answered? (data, statistics, simulation).
  - **Three views kept separate in ranking:** scientific consequence,
    readiness, and next-check priority.
- **Evidence:** framework notepad §1–2 and §6; register conventions;
  76/2097 (the three views).
- **Gaps:** a figure of the pipeline, built from real entries (Q-012,
  Q-038, Q-017) rather than an idealised diagram.

## 4. Roles and protocol

- **Claims:**
  - **Antagonism between two agents catches errors that self-review does
    not**, especially one specific type: stretching a correct partial
    result into a broader conclusion.
  - **The human's role** is steering, judging taste, and opening one-way
    doors.
  - **Fail-closed rules and prospectively frozen screens** prevent
    rescue-by-retry.
- **Evidence:**
  - the decision-change ledger, by `changed_by`;
  - the 76/2066, 2096, 2112 and 2138 corrections;
  - framework notepad §3.
- **Gaps:**
  - how often the *same* agent caught its own error, compared with the
    other agent;
  - whether any correction was later reversed.
- **Threats:**
  - The agents are not independent: shared training-data eras, and each
    sees the other's text.
  - Agreement is not validation.

## 5. Results

### 5a. Portfolio flow

- **Evidence:** the register index and checkpoint record:
  - 50 applied questions, then 10 develop / 29 hold / 8 park / 3 merges at
    the 14 October checkpoint;
  - 18 blue-sky entries, then 1 develop / 17 hold;
  - the current counts in `evidence/decision-changes-summary.md`.
- **Gaps:**
  - a dated time series of dispositions;
  - the reasons for each hold or park, classified as occupied,
    unanswerable, non-identifiable, under-powered, or cost.

### 5b. What vetting changed

- **Evidence:** `evidence/decision-changes-draft.tsv`, once verified.
- **Gaps:**
  - verify every row against its source;
  - add cost where the record allows;
  - mark later reversals.

### 5c. Case study: Q-012, a "ready" question that needed weeks of vetting

- **Claims:**
  - The most advanced question went through prior check,
    identification, a finite contract and a technical pilot.
  - Several numerical failures and repairs followed: the solver,
    quadrature order, the reference rule, and the adaptation buffer. Each
    was diagnosed before it was remedied.
  - There is still no scientific estimate.
- **Evidence:**
  - `data/q012-pilot/README.md`;
  - the `ideas/2026-10-1*-q012-*` notes;
  - core-hour accounting: 20.72 of 53.33 used before `v6q80t`.
- **Gaps:** the outcome of the current attempt; total agent-hours, which
  are not instrumented.

### 5d. Case study: Q-038, contract repair before any fit

- **Claims:**
  - Codex refuted the draft's detection-null gate with an exact
    counterexample.
  - The replacement contract's identification checks show three things:
    - naive last-appearance selectivity reports spurious effects under the
      null;
    - one post-event occasion with free detection is not identified;
    - identified single-event precision is weak.
  - All of this was found *before* any empirical fit.
- **Evidence:** `data/q038-predictor-contract/contract.md`, sections 7–8;
  `contract_checks.tsv`.

### 5e. External idea injection

- **Claims:**
  - Outside consultants (GPT-6 Pro) contributed candidates.
  - The same vetting applied to them, and Codex's checks narrowed or
    occupied several. The examples are the recruitment inference, the
    chronology principle and innovation persistence.
- **Evidence:** the two 21 October assessments, the Codex response and its
  evidence archive.
- **Threats:** n = 1 consultation run per condition, confounded (Codex
  76/2138). Report it as a case history only.

### 5f. Cost

- **Gaps:** this is the largest one. Instrument from now on, where
  feasible:
  - agent sessions or tokens per decision;
  - Barry's minutes per decision;
  - compute.
  Without these, no efficiency claim can be made.

## 6. A catalogue of failure modes

- **Claims:** a transferable list, each with a real example and remedy:
  - inference stronger than the evidence;
  - in-sample results presented as prediction;
  - changing a rule after seeing data;
  - fixing before diagnosing;
  - conflating the target, its approximation and the computation;
  - generic classifiers;
  - domain ceilings;
  - stretching a partial result.
- **Evidence:** framework notepad §3, linked to ledger rows.

## 7. Transfer and seeding

- **Claims:**
  - What is domain-general: stages, dispositions, contract fields, the
    two-agent protocol, fail-closed rules.
  - What must be rebuilt per domain: source catalogues, domain ceilings,
    canonical rivals.
  - How a selected question seeds a dedicated project.
- **Evidence:** framework notepad §4–5.
- **Gaps:** no second domain has been tried. A small pilot in Barry's
  suggested domains would test transfer: contemporary extinction risk,
  population viability analysis, or conservation genetics.

## 8. Limitations

- **No counterfactual arm.** We cannot say what a quick-start approach
  would have produced on the same questions.
  - A retrospective proxy: how many first-pass "develop" calls survived.
  - A prospective design: matched questions, with and without vetting,
    evaluated blind.
- The evidence is selected and summarised by the same agents whose method
  is being assessed.
- Costs are not instrumented.
- The models change during the programme.
- One human, with his own priors.

## 9. Recommendations for others

To be written last, from what the results support.

## Open items (running)

- Verify the ledger draft row by row; add costs and reversal flags.
- Decide with Codex whether this folder is jointly owned, and record it in
  `STATUS.md`.
- A bounded prior-literature check for section 1. It must not use contact
  parameters in API calls.
- Start cost instrumentation, and decide what is feasible without new
  machinery.
