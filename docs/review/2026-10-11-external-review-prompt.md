# External adversarial review: final prompt

Final version, 11 October 2026.
- **Base:** Codex's candidate
  ([2026-10-11-external-review-prompt-codex.md](2026-10-11-external-review-prompt-codex.md)).
- **Added by Claude:** why the review exists; prior work as the
  highest-value target; a glossary of the register's conventions; Barry's
  instruction to ignore drafts of the prompt.
- **Replaces** Claude's first draft, which remains in Git history.
- **Review snapshot:** commit `bbe5ce7fc205b3b1f9529757b64e25fd997243cb`.
  This file was committed after that snapshot, so the reviewer will not see
  it.

Barry sends everything below the line.

---

Review the private GitHub repository [BWBrook/eprp](https://github.com/BWBrook/eprp)
at commit **`bbe5ce7fc205b3b1f9529757b64e25fd997243cb`**. Act as an
independent, constructive scientific critic.

The main product is a register of research questions in quantitative
palaeobiology. We want your independent assessment of:
- their scientific value;
- their prior-work context;
- whether their target quantities can be identified;
- what evidence could feasibly answer them.

Challenge strong-looking arguments as carefully as weak-looking ones. A useful
review may defend a question the authors dismissed, as well as expose a flaw
they missed.

## Why this review exists

Two AI agents developed the repository over five days: Claude (Anthropic) and
Codex (OpenAI). They worked under the direction of Barry W. Brook (University
of Tasmania), who works on extinction, palaeoecology and global change.

The agents acted as collegial antagonists, checking and challenging each
other. But they read many of the same sources and argued with each other for
days. Models that co-read in this way share blind spots, anchor on early
framings, and can converge on a well-argued error. **Your independent
knowledge and reasoning are the point of this review.**

Their agreement, disagreement, model identities and volume of discussion do
not validate any scientific claim. Evaluate arguments and evidence, not which
participant advanced them.

## Access and review boundary

**Access.**
- Use your authenticated access to the **private GitHub repository**. You do
  not have Barry's local checkout, the ignored downloads and scratch files,
  or the agents' private discussion board.
- Local absolute paths in documents are provenance, not files available to
  you. Do not assume a public URL will expose a private repository.
- Review the commit above throughout, and use commit-specific GitHub links in
  findings.
- State whether you could inspect complete files and the tree. If you can
  see only excerpts, say which conclusions that prevents. If authentication
  or your tools cannot expose the repository, report that; do not substitute
  an inferred review.

**Read-only.**
- Return your report to Barry.
- Do not change files, open issues, contact source authors, or start a
  primary analysis.
- Source checks, algebraic counterexamples and small calculations are
  welcome if your tools support them. Record precisely what you ran. A
  command printed in a README is not evidence that it was executed.

**Ignore the material about briefing you.** Earlier drafts of this prompt,
and the agents' discussion of how to brief you, are in the snapshot. They are
not material for review, and reading them would only send you back over this
prompt. Ignore:
- everything under `docs/review/`;
- `ideas/2026-10-11-phase2-review-preparation-codex.md`;
- passages in `STATUS.md` and the phase-2 replies
  (`ideas/2026-10-11-phase2-claude-reply-2.md` and `-reply-3.md`) that
  discuss the external review or its prompt.

The rest of those files is in scope.

## Remit

EPRP (Extinction and Paleontology Research Programme) develops a continuously
revised portfolio of consequential, well-posed questions for downstream
research teams. It supplies literature orientation, data preparation,
criticism and small feasibility probes. It does not select one winning
project or produce primary research results.

- **Deep time has priority.**
- Extinction, and the reciprocal relevance of past and present biodiversity
  change, are major interests. Neither is required of every question.
- Questions in theory and simulation are as legitimate as empirical ones.
- Do not optimise the portfolio around convenient datasets, Barry's previous
  specialisms, or immediate modern applications.

The first tranche holds 50 questions, Q-001 to Q-050, and expansion is paused
for review. Statuses, tiers and phase-2 rankings are provisional. A
high-value question may have difficult next steps; a cheap, useful audit may
support a question of modest importance. Keep those judgments separate.

**Conventions you will meet.**
- Each register entry has a status (sketch / under review / promising /
  ready for handoff / parked / rejected), a tier from 1 to 3, and an owner
  agent.
- Evidence-depth labels record what was actually read: "abstract checked",
  "full text", "title checked", "sect: …" and similar.
- "Not found" means not found in a bounded search. It is not a claim of
  novelty.
- The phase-2 scores are S (scientific importance), O (openness), D (data
  readiness) and G (gate cost). Importance and next-work priority are meant
  to be ranked separately.
- References such as `76/1518` point to the unavailable discussion board.

## Form an independent view before reading the debate

1. **Survey first.**
   - Read `README.md`, the remit in `docs/programme.md`, and
     `ideas/register.md`.
   - Note your own most consequential opportunities, concerns and missing
     ideas before reading the agents' ranking documents.
   - Use the whole register to choose targets, including neglected and
     parked entries. The number of audit files attached to an entry should
     not dictate its importance.
2. **Choose a manageable set for depth**, and explain your choice.
   - Follow each selected entry's evidence links into `literature/` and
     `data/`.
   - Check the nearest primary literature. Check whether the proposed
     evidence can distinguish the actual rivals.
   - Prefer a few decisive checks to superficial claims of coverage.
3. **Then test your view against the agents' strongest arguments.**
   - Read `STATUS.md` and the phase-2 discussions in `ideas/`: the first
     portfolio pass, Codex's response, and the later replies.
   - State where your view changed, where it did not, and why.

This order reduces anchoring. It does not make the review blind, because the
register already contains the agents' judgments.

`AGENTS.md` and `CLAUDE.md` describe the agents' workflow. Reading them does
not commission you to perform its operational tasks.

## Evidence you can inspect

The snapshot contains scientific notes, scripts, source manifests and
selected derived TSV tables. It does **not** contain `data/raw/`,
`data/derived/`, `scratch/`, or the full set of local outputs.

- Some probes are self-contained, with tracked code and small outputs, for
  example `data/q026-boundary-observation/`.
- Some source archives can be fetched independently from documented public
  URLs, for example `data/q050-covariance-support/`. Check that the URLs work
  in your environment before relying on them.
- The Q-038 and Q-044 probes use Dryad files Barry supplied locally; those
  files are not on GitHub. The Q-027 source is a large external archive, with
  code for fetching selected members.
  - Their tracked tables and scripts allow logical and internal-consistency
    checks, not an automatic rerun from raw data.
  - Several READMEs record checksums and rebuild commands.
- Dated audits may refer to an older builder or source snapshot. Respect the
  stated version: current code and historical output need not match.
- Identify any consequential claim that cannot be assessed without the
  missing board discussion. Durable evidence is meant to stand on its own in
  the repository.

Label each finding by its access:
- source, code or table inspected directly;
- calculation reproduced independently;
- result reported by the authors;
- evidence unavailable.

Missing inputs limit verification; they do not prove a claim false. A
checksum or a reproducible script does not establish scientific suitability.
Do not ask for an export of the whole local cache or the board before
reviewing what you can see. Instead, name the smallest additional item that
would settle a consequential uncertainty.

## Questions for your review

- **Prior work: the highest-value thing you can supply.**
  - Look for published work that already answers a question, occupies its
    claimed residual, makes its design obsolete, or contradicts a premise.
  - Both recent work (especially 2022–2026) and older foundational work
    matter, as do adjacent fields the agents may not have read:
    geochemistry, phylogenetics, macroecology, theory and others.
  - Compare estimands and assumptions, not just titles.
  - What would a credible positive or negative answer change? Which
    questions deserve more development even though their data are
    difficult?
- **Inference.**
  - Are the biological quantity, the observational unit, the time window,
    the comparison and the alternatives defined?
  - Can the proposed evidence distinguish the alternatives?
  - Challenge:
    - circular calibration;
    - effects of the observation process;
    - conditioning on later outcomes;
    - quantities that are saturated or fixed by construction;
    - algebraic identities presented as mechanisms;
    - unjustified claims of impossibility or identifiability.
- **Evidence and feasibility.**
  - Do the cited sources support the actual claims? Look for misattributed
    findings and DOIs pointing to the wrong work.
  - Does nominal access to data supply the joint temporal, geographic,
    taxonomic and environmental support the question needs?
  - Are shared data and shared chronology mistaken for independent
    replication?
  - Are the numerical decision rules calibrated? Can they yield an
    informative result against the question?
- **Portfolio.**
  - Which entries are consequential, incremental, redundant, or parked too
    early?
  - Distinguish three kinds of failure: an implementation, an empirical
    route, and a biological question that is not important.
  - Challenge the S/O/D/G rubric itself as well as how it was applied. Give
    your own judgment without forcing every question into one score.
- **Process and reuse.**
  - Which practices improve scientific decisions, and which consume effort
    without doing so?
  - Could a new team use the evidence in this snapshot?
  - Treat dated, superseded arguments as history. Flag contradictions that
    still affect the current register or its decisions.

## Standards for findings

For each consequential finding, give:
- the precise claim, as a short quotation, with its Q-ID and a
  commit-specific link to the file or section;
- your reasoning and the evidence that supports it;
- its consequence;
- the smallest useful remedy or discriminating check;
- the strongest reasonable defence of the claim;
- what would change your own judgment.

Separate verified findings, supported concerns and unverified leads.

For literature:
- Give a verified DOI or a stable source URL.
- Say whether you read the relevant primary sections, only an abstract or
  metadata, or are recalling the work.
- **Never invent an identifier.** A precise lead from memory, described well
  enough to find, is useful. Keep it distinct from an established objection
  on priority or novelty. A confident fabrication does real harm.
- Log access failures as access failures.

Rate severity (critical / major / minor) and confidence (high / medium / low)
separately. For a critical or major issue, explain what it invalidates or
changes: the implementation, the interpretation, the empirical route, the
ranking, or the question itself. A design flaw does not automatically
invalidate the parent question. Include well-supported strengths and
justified disagreements you keep. There is no quota of faults or
recommendations.

## Report

1. **Executive assessment.** At most 300 words, leading with the decisions
   your evidence would change.
2. **Ranked findings.** A compact table or numbered list with the fields
   above, numbered F-01, F-02, … so the agents can respond item by item. Do
   not force long arguments into unreadably wide tables.
3. **Coverage and dispositions.**
   - Mark each entry as substantively reviewed, skimmed, or unassessed.
   - Give keep / revise / merge / park / reject only where you have grounds;
     "unassessed" is a valid answer.
   - A compact ledger grouped by ID is enough. Do not invent 50 verdicts to
     fill a template.
4. **Development priorities.** Up to three candidates for further
   development, possibly none. For each:
   - distinguish scientific importance from next-work priority;
   - name the cheapest decisive test, the usable evidence, and the main way
     it could fail.

   Recommend readiness for a project only if the evidence you inspected
   supports it. Selection is Barry's decision.
5. **Gaps and process.** Only where warranted:
   - up to five consequential missing questions;
   - up to five concrete changes to the workflow.

   Proposed gaps do not add entries to the paused register.
6. **Verification limits.** The commit you reviewed, any limits on access or
   tools, the computations you actually ran, and the most consequential
   claims you could not verify.

Spend effort where it can change a scientific decision. We value a small
number of findings that hold up, including unexpected defences of neglected
questions, over a comprehensive-looking set of weak verdicts.
