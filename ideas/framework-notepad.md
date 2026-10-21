# Framework notepad: pre-project planning as a reusable harness

Owner: Claude (Codex welcome to add a section or reply on the board) |
Started 19 October 2026 | A running notepad, not a specification.

Barry, Claude chat, 19 October 2026 (exact):

> "I often found too much emphasis was placed on answering questions with AI
> apace, before actually taking the time and effort to ask if they were good
> questions (testable, separable, interesting, etc.), or whether they could be
> answered (available data, stats, simulation constraints). [...] we can
> probably use this as a template (later) for other domains, such as
> contemporary extinction risk, population viability analysis, conservation
> genetics, whatever. It's about developing the pre-project planning before the
> detailed science comes."

He asks for two things to be kept in view:
- how this work could be encoded as a framework or harness for other topics;
- how a chosen question would be seeded as a project for a dedicated
  Claude–Codex pair, perhaps orchestrated by the EPRP pair.

The target before any selection is a **ranked list of 25–50 questions**.

## 1. The pipeline as practised (EPRP, 7–19 October)

Each stage ends in a written artefact and a disposition. The examples are
real.

| Stage | Question it answers | Artefact | Example |
| --- | --- | --- | --- |
| Seed | Is this a question, and why would anyone care? | Register entry: question, motivation, owner | 50 applied + 18 blue-sky entries |
| Prior-work check | Has it been done, at this target? | Dated note with access depth (meta/abs/sect/full); "not found" means not found in a bounded search | `literature/2026-10-14-q012-prior-check.md` |
| Contract | What exactly is estimated, from what, against which rivals? | Target, observation unit, comparison, permitted interpretation, unresolved assumptions, next decision | Register conventions; Q-016 entry |
| Support audit | Do usable data exist in the needed form? | Source inventory, crosswalk, raw-file hashes | Q-021 Li records; Q-050 archive; B-003 inventory |
| Identification design | Can the rivals be separated, even with perfect data? | Analytic or simulation argument; what a positive result may claim | Q-012: unmeasured clade-tied exposure is equivalent to inheritance |
| Finite contract | Can it be answered at the available scale? | Generator, estimator, decision rules, power and coverage plan | `literature/2026-10-16-q012-finite-contract.md` |
| Technical pilot | Can the estimator be fitted reliably at all? | Frozen screens, fail-closed qualification, receipts, ceilings | Q-012 kunanyi pilot (R00, P11, diagnostic replay) |
| Disposition | Develop, hold, park or merge? | Reason plus reopening trigger | 14 Oct checkpoint: 10 develop / 29 hold / 8 park / 3 merges |
| Ranking (pending) | Which questions most deserve a team? | Ranked list, 25–50 entries | Not yet built |

**The stages are a revisable dependency structure, not a waterfall or a
document quota** (Codex, 76/2097). An early identification counterexample
can save a large support audit, so run the cheapest stage that could change
the disposition first.

Two distinctions earned their place early:
- **Scientific importance is not next-work priority** (Codex, 11 October).
  Rank them separately.
- **Tier separates consequence from tractability**, prior occupancy and
  cost.

## 2. Roles and protocol

- **Two agents as collegial antagonists.** Each owns entries. One single
  review per product, with findings posted as replies. Disagreements stay
  visible. Model agreement is not independent validation.
- **Human as facilitator and equal contributor.** Approval is needed only at
  one-way doors: public release, third-party contact, spending beyond a
  ceiling, project selection.
- **A board, not chat, for cross-agent work.** It gives allocation,
  acceptance, evidence and a named next responder. Barry's decisions are
  quoted exactly, with date and source.
- **Resources:** explicit ceilings, stop rules and accounting at each
  return. Wake on events (PBS mail), never by polling.

## 3. Failure modes the process caught (candidates for any domain)

- **Inference stronger than the evidence.** Identical saved records were
  read as identical unsaved trajectories, and the saved divergent row was
  read as the failing proposal. Remedy: state what was observed separately
  from what is inferred.
- **In-sample results presented as prediction.** Remedy: held-out or
  landmark-frozen designs (Q-012, Q-016, Q-038).
- **Changing a rule after seeing data.** Remedy: freeze screens before the
  run; fail closed; no passing-prefix selection; no automatic retries.
- **Fixing before diagnosing.** A remedy chosen from the symptom (a solver
  tolerance) was later shown not to touch the cause. Remedy: instrument and
  capture the failure first, then choose the remedy.
- **Conflating the target, its approximation and the computation.**
  - Keep three objects separate:
    - the scientific target;
    - the implemented approximation (here the Q-node normaliser);
    - the sampled numerical trajectory.
  - In Q-012, a quadrature failure sat at a *preceding* trajectory state,
    while the saved-state and failing-state checks both passed (Codex,
    76/2096–2097).
  - Remedy: check each object on its own terms, at the states where the
    computation actually went.
  - Instrumentation earned its place by resolving a decision. A seeded
    project should not inherit the whole Stan diagnostic machinery by
    default.
- **Generic classifiers** (keyword matching on error text). Remedy: an exact
  grammar for expected messages; everything else fails closed.
- **Domain ceilings** (palaeobiology-specific; each domain needs its own
  list):
  - cross-event designs top out at roughly 6–30 events;
  - temporal resolution limits lags and precursors;
  - "non-random" is not "event-specific".
  - See the lessons section in `ideas/register.md`.

## 4. What transfers, and what does not

**Likely domain-general:**
- the stage sequence and artefacts;
- the disposition vocabulary with reopening triggers;
- the contract fields;
- the antagonistic two-agent protocol and the board;
- fail-closed qualification and prospectively frozen rules;
- resource ceilings and stop rules.

**Domain-specific, built per domain:**
- the source catalogue;
- the domain ceilings and lessons list;
- the canonical rival hypotheses;
- typical identification traps. For PVA, for example: parameter
  non-identifiability, and environmental against demographic stochasticity
  in short series. For conservation genetics: N_e estimators' assumptions.

**Open:** how much of the first round in a new domain must be spent learning
its ceilings before the register is any good. EPRP's lessons list came
mostly from its first round of prior checks (9–10 October).

## 5. Seeding a chosen question as a project (sketch)

When a high-ranked question is selected, a dedicated Claude–Codex pair
would get a new repository seeded from the EPRP record:
- `AGENTS.md`: remit, authority, the one-way doors, the resource ceiling
  and stop rules, inherited from the EPRP decision;
- `STATUS.md`: ownership table and the first allocation;
- `contract.md`: the register entry's contract, the prior check, the support
  audit and the identification design, copied with provenance and frozen
  hashes;
- `evidence.md` conventions, the board project and the wake protocol;
- milestones that return to the EPRP pair for review: design freeze, pilot
  result, first estimate, release candidate. Barry reviews at least the
  final version.
- **The unsuccessful record too** (Codex, 76/2097): the exact claimed
  estimand, the strongest unresolved objection, and every failed gate
  alongside the successful artefacts.

**To decide later:**
- how much autonomy the project pair has between milestones;
- whether EPRP reviews by board or by reading the project repository;
- how negative results flow back into the register.

## 6. Notes to revisit

- **Ranking method.** Codex (76/2097) proposes three views, kept side by
  side rather than summed:
  1. **Scientific consequence:** which competing account would change, at
     what breadth, and whether a positive *or* negative result would
     matter.
  2. **Project readiness:** target-specific prior occupancy, separability,
     actual joint data support, demonstrated computational feasibility.
     Missing evidence counts as unknown, not as a middling score.
  3. **Next-work priority:** how much a bounded check could change the
     disposition or rank, relative to its cost.
  - Do not penalise "risk of a null" as such. Distinguish an informative
    negative from a low-power or non-identifiable outcome.
  - **Procedure:** a common *evidence card* per entry, then ordered bands,
    then explicit pairwise comparisons near the allocation boundary. Keep
    ties, and show whether plausible weightings reorder the leaders.
  - The card covers: target, consequence, strongest rival, closest prior,
    decisive test, support and feasibility, failure or reopening condition,
    and uncertainty.
  - I agree, and would add only that the card should name the *cheapest
    disposition-changing check*, which links view 3 to the evidence.
- **Measuring the framework.** Counting kills alone is not enough: a
  harness can look efficient by admitting only trivial questions (Codex).
  Track:
  - which evidence changed each decision;
  - whether the decision was later reversed;
  - the attention and compute needed to settle the main rival.
- As models improve, which gates become cheap enough to run for every
  entry, for example identification simulations?
- **External idea injection (21 October).** Barry commissioned three
  GPT-6 Pro simulation briefs
  ([assessment](2026-10-21-gpt6pro-proposals-assessment-claude.md)). The
  intake protocol that worked:
  - file the package verbatim, with hashes;
  - assess each brief against the same gates as internal entries;
  - map its adjacency to the register;
  - name the cheapest disposition-changing check;
  - hand it to the other agent before any register change.
  Two lessons:
  - **A briefer that reads the repository returns in-distribution ideas.**
    They are easy to assess but less independent. Commission at least one
    brief blind to the repository.
  - **Asked to exploit large-scale simulation, all three briefs concluded
    that evidence, not compute, binds.** A small analytic or motif model
    decides the first question, and historical application is data-gated.
    In deep time, simulation earns its scale mainly in:
    - information and observation studies;
    - causal counterfactuals for theory;
    - simulation-based inference over sample-level data.
    This belongs in any domain template's resource section.
