# Outline (scaffold)

Working title: *With receipts: what agentic AI audits found in the data and
software infrastructure of quantitative palaeobiology.*

Each section lists the claims it needs, by ledger ID once the ledger exists,
and what would undercut it.

## 1. Introduction

- **The infrastructure layer.** Quantitative palaeobiology depends on
  shared databases (PBDB, Macrostrat, GBDB), published deposits, time scales,
  plate models and packages.
- **The problem.** Problems in these layers can reach published inference
  without being noticed. The paper reports *cases*, not a prevalence rate
  (thesis revised after Codex's audit design). The community asks for exactly this auditing in Big Questions
  AFR1–AFR3 and FI1.
- **The gap.** Audits are rare because they are tedious, broad and thankless.
  Agentic AI changes that cost.
- **The aim.** Report what systematic agentic audits found, how each finding
  can be replayed, and what the method's own failures were.

## 2. How the audits were run

- **The setting.** EPRP is a research programme run by two AI agents (Claude
  and Codex) with a human facilitator. Three Claude side sessions handled
  databases, packages and simulations, and references, each in its own
  worktree.
- **Practices:**
  - read-only mirrors with hashes;
  - validation tests declared before running, with dated amendments (the
    `VALIDATION_T*.md` files);
  - independent second-model reviews before merging;
  - known-truth simulation benches;
  - replay scripts;
  - [Detail withheld pending disclosure to the data custodian.]
- **Scale and cost:** wall time, compute and the number of tools and
  datasets audited.

*Undercut if:* the practices were applied unevenly. The process receipts in
the ledger must show which checks each claim actually had.

## 3. What the audits found

Each case is presented as the claim, the receipt with its evidence status,
and the consequence for inference. Each is also classified (Codex's audit
design) as one of:
- an implementation defect;
- a data inconsistency;
- a calibration failure under a stated model;
- a violated assumption or semantic finding;
- an intended version or model choice;
- a sensitive access finding;
- an internal downstream effect.

The subsections below are a first grouping.

| Subsection | Findings |
| --- | --- |
| **3.1 Data access and provenance** | Published PBDB-derived deposits carry them, at measured fractions. Every sampled chronosphere vintage holds them. Macrostrat's PBDB counts include them. [Detail withheld pending disclosure to the data custodian.] |
| **3.2 Time scales** | PBDB's three interval re-datings, each bracketed between two consecutive downloads, including moves off the ICS chart. Version drift in packaged time-scale tables. |
| **3.3 Software correctness** | admtools `strat_to_time`; fossilbrush `flag_ranges`; GRIWM's intervals and its seed reset; RevBayes's disabled FBD range process |
| **3.4 Software calibration** | PyRate's preservation-rate bias, traced to inferred durations; hiatus effects on range-end bounds; calibrated cases (tbea, EDE, Robson–Whitlock) as positive controls |
| **3.5 Deposit integrity** | A corrupted capture-history column in a published spreadsheet |
| **3.6 Spatial models** | Palaeolatitude spread across plate models; two absolute frames under one model name; a wrong polygon layer in a mirrored model |
| **3.7 Coverage claims** | Macrostrat's "global" coverage is largely North American, with few independent dates. LegacyPollen ages and ensembles. |

*Undercut if:* a finding fails replay, a provider shows it is intended
behaviour, or a defect was already fixed or documented before our audit.
Every one needs a prior-disclosure check.

## 4. What the agents got wrong, and how it was caught

- Errors corrected by the declared amendments and reruns, such as the rerun
  after GRIWM reset the random seed.
- Corrections from independent review.
- [Detail withheld pending disclosure to the data custodian.]
- Cross-agent corrections in the main programme, where the counterexamples
  in the correspondence record show the same mechanism.

This section makes the receipts honest. It is evidence that verification
needs a second checker, not that the agents are infallible.

## 5. Recommendations

- **Providers:** expose access status in query results, version time scales
  explicitly, and keep changelogs.
- **Software authors:** known-truth benches; seed hygiene; numeric types.
- **Journals and deposits:** machine-readable deposits; no spreadsheet
  storage of identifiers or histories; time-scale and plate-model metadata.
- **Users:** pin versions, run more than one plate model, replay before
  reuse.
- **Programmes using agents:** declare tests before running, use second-model
  review, keep hashes and publish the correspondence.

## 6. Discussion

- **Cost and benefit**, compared with how these audits are usually done.
- **Limits:** coverage is a sample, not a census, and the findings are a
  snapshot that providers may since have fixed.
- **Generality beyond palaeontology.**
- **Roles of the AI systems and of the human facilitator.**

## Data and code availability

Replay scripts, hashes and ledger, from the EPRP repository, which is
private now. Release is Barry's decision. Restricted-record materials are
excluded by design.
