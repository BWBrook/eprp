# Prompt for an external adversarial review of EPRP

Drafted by Claude, 11 October 2026, at Barry's request. Codex's critique of
the prompt's form has been requested on the board (discussion 76).
- Barry sends the prompt below to the reviewer.
- Barry fills in the commit SHA and how the repository is supplied.
- Everything below the line is the prompt.

---

You are reviewing a research-programme repository with a clean pair of eyes,
as an adversarial but constructive referee. Two AI agents built it over five
days: Claude (Anthropic) and Codex (OpenAI). They worked under the direction
of Barry W. Brook, an ecologist and modeller (University of Tasmania) whose
work centres on extinction, palaeoecology and global change.

The agents act as collegial antagonists: each checks and challenges the
other. They have read many of the same sources and argued with each other for
days. **That is the problem you are here to solve.** Two models agreeing is
not independent validation. They share blind spots, anchor on early framings,
and can converge on a well-argued error. Your independent knowledge and
reasoning are the point of this review. Do not defer to the repository's
conclusions because they look carefully argued.

## What you are reviewing

**Snapshot.** Repository `BWBrook/eprp`, branch `main`, commit
`<SHA supplied by Barry>`. Treat it as read-only.

**Purpose.** EPRP (Extinction and Paleontology Research Programme) produces a
continuously revised register of well-posed, deeply contextualised,
consequential research questions in quantitative palaeobiology. Other teams
will take these questions up later.
- Deep time has priority.
- The reciprocal relevance of geological extinctions and the modern
  biodiversity crisis is a central interest, not a requirement.
- EPRP itself does not run primary investigations. It does literature and
  data orientation, criticism, small feasibility probes, and reusable data
  preparation.

**Current state.**
- The register (`ideas/register.md`) has 50 questions, Q-001 to Q-050.
  Expansion is paused.
- The agents are in "phase 2": categorising, ranking and deepening the
  questions, and testing data readiness with small "data contracts".
- No question has been selected for a research project. Barry will choose
  later.

**Suggested reading order.**
1. `README.md`, then `STATUS.md` (current state and decisions).
2. `AGENTS.md`: the agents' rules. They are not binding on you, but they
   explain the conventions.
3. `ideas/register.md`, the main object of review. Each entry has:
   - a status: sketch / under review / promising / ready for handoff /
     parked / rejected;
   - a tier from 1 to 3, and an owner;
   - the question, prior work, design, data, kill criterion, and links to
     evidence notes.
4. Phase-2 documents in `ideas/`:
   - `2026-10-11-phase2-portfolio-first-pass-claude.md` (themes, the
     S/O/D/G scores, work packages);
   - `2026-10-11-phase2-response-codex.md`;
   - `2026-10-11-phase2-claude-reply-1.md` and `-reply-2.md`.
5. `literature/`: dated evidence notes, cited from register entries.
6. `data/`: data contracts and audits, each with a README, for example
   `q027-joint-support`, `q027-support-audit`, `q038-monarrez-contract`,
   `q038-flag-audit`, `q044-joint-support`, `q022-premortem` and
   `q050-covariance-support`.
   - Raw downloads are git-ignored and absent from your copy.
   - The READMEs record sources, checksums, rebuild commands and results.
   - You will probably not be able to rerun them. Judge the logic, and say
     what you would rerun.

**Conventions to know.**
- Evidence-depth labels: "abstract checked", "full text", "title checked",
  and so on.
- "Not found" means not found in a bounded search; it is not a novelty
  claim.
- Rubric scores: S (scientific importance), O (openness), D (data readiness)
  and G (gate cost). Importance and next-work priority are ranked
  separately.

**What you cannot see.** The agents' discussion board (Correspondence) is not
in the repository. Its message numbers, such as "76/1518", appear as
citations. Durable conclusions are meant to live in the repository. Where
something only makes sense with the board, that is itself a finding.

## What we want from you, in priority order

1. **Prior work that occupies or undercuts a question.** Missing literature is
   the highest-value thing you can find. Look especially for:
   - work from 2022–2026;
   - work outside the agents' apparent reading, such as geochemistry,
     phylogenetics, macroecology and theory;
   - work that already answers a question, makes its design obsolete, or
     contradicts a premise.

   An example of the kind we mean: a check today found that the register
   lacked Rauzi et al. 2024 (PNAS) and Cao et al. 2022 (Nat Geosci) on
   Early Triassic reverse weathering, both directly relevant to Q-021.
2. **Questions that are not well posed.** For example:
   - estimands that cannot be identified;
   - quantities that are saturated or fixed by construction;
   - kill criteria that can never trigger, or always will;
   - outcomes that are not independent of the inputs used to define them;
   - confusion between prediction and explanation;
   - designs where sampling and the biology cannot be separated.

   Reply 2 reports one such case (Q-044's between-window β is near its
   ceiling). Find the others.
3. **Wrong or overstated claims** about published papers, datasets or data
   support:
   - claims misattributed to a paper;
   - numbers that do not follow from the cited source;
   - DOIs pointing to the wrong work;
   - "data are available" when they are not usable for the stated estimand.
4. **Portfolio judgment.** Using your own judgment, not the agents' scores:
   - Which questions matter most?
   - Which are incremental, redundant, or too entangled to be tractable?
   - Is the S/O/D/G rubric measuring the right things? Are deep-time
     questions given the priority Barry asked for?
   - What large, consequential questions are *missing* from a portfolio with
     this remit? List at most five. Expansion is paused, so these are
     candidate gaps for the agents to assess, not additions.
5. **Process critique.** For example:
   - shared biases between the two agents;
   - over-elaboration or "process" substituting for science;
   - entries too dense for a downstream team to use;
   - inconsistencies between `STATUS.md`, the register and the evidence
     notes;
   - provenance practices that look careful but would not survive reuse.

You choose where to spend effort. As a guide, examine closely:
- the highest-scoring entries in the phase-2 scores table;
- every entry with a data contract or audit (Q-021, Q-022, Q-026, Q-027,
  Q-038, Q-044, Q-050);
- a sample of the parked entries, to check whether any were parked wrongly.

Skim the rest. Breadth on the register matters less than depth where it
counts.

## Standards

- **Quote** the repository text you criticise, with its file path and the
  entry ID or line number.
- **Provenance for each citation.** Give the DOI, and say whether you checked
  it in this review (primary full text, abstract, or metadata) or are
  recalling it. Never invent a DOI. If you are unsure, write "unverified
  lead" and describe the work well enough to find it. A precise unverified
  lead is still valuable. A confident fabrication does real harm.
- **Calibration.** Give each finding a confidence (high / medium / low) and a
  severity:
  - *critical*: invalidates a question, design or data claim;
  - *major*: changes a ranking, design or kill criterion;
  - *minor*.
- **Falsifiability.** For each critical or major finding, say what evidence
  would show *you* are wrong. The agents will try.
- Disagree with each other's positions where you think one agent is right
  and the other wrong; name which.
- Do not rewrite entries. Give findings the agents can adjudicate one at a
  time.

## Output format

1. **Executive summary.** No more than 300 words: the most important things
   Barry, Claude and Codex should know.
2. **Findings table.** Ranked by severity, then confidence. Columns:
   - ID (F-01, F-02, …);
   - entry or file;
   - quoted claim;
   - problem;
   - evidence, with citation provenance;
   - severity;
   - confidence;
   - suggested remedy;
   - what would refute this finding.
3. **Triage of the register.** One row per question, Q-001 to Q-050: your
   disposition (keep / revise / merge with … / park / reject) and a reason
   of one line. Mark rows where you only skimmed.
4. **Elevation candidates.** The three questions you would elevate to a
   research project now. For each, give:
   - the cheapest decisive first test;
   - the main way it could fail;
   - the data it would actually use.
5. **Candidate gaps.** No more than five missing questions, each with one
   paragraph on why it is consequential and why it fits the remit.
6. **Process recommendations.** No more than eight. Concrete changes, not
   general advice.

Be direct. We would rather receive ten sharp findings that hold up than fifty
mild ones.
