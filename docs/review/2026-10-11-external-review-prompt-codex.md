# Proposed external-review prompt: private GitHub access

Prepared by Codex, 11 October 2026, in response to Claude's request for a
critique of the [first draft](2026-10-11-external-review-prompt.md).
Barry clarified in Codex chat that the reviewer has access only to the private
GitHub repository, not this workstation's checkout. This is a concrete revised
candidate for Claude and Barry; it does not start or transmit a review.

Copy everything below the line. The review should identify its immutable
commit at the start; the accompanying handoff supplies the current pushed SHA.

---

Review the private GitHub repository [BWBrook/eprp](https://github.com/BWBrook/eprp)
as an independent, constructive scientific critic. The main product is a
register of research questions in quantitative palaeobiology. We want your
independent assessment of their scientific value, prior-work context,
identifiability and feasible evidence. Challenge strong-looking arguments as
carefully as weak-looking ones. A useful review may defend a question that the
authors have dismissed, as well as expose a flaw they missed.

## Access and review boundary

Use your authenticated access to the **private GitHub repository**. You do
not have access to Barry's local checkout, ignored downloads or scratch files,
or the agents' private discussion board. Local absolute paths in documents
are provenance, not files available to you. Do not assume a public GitHub URL
will expose a private repository.

Use the full commit SHA supplied with this prompt. If none is supplied,
resolve `main` once at the start and record its full SHA. Review that snapshot
throughout, and use commit-specific GitHub links in findings. State whether
you could inspect complete files and the tree. If authentication or your tool
cannot expose the repository, report that access blocker; do not substitute
an inferred repository review. If you can access only excerpts, state which
conclusions that prevents.

Review read-only. Return your report to Barry. Do not change files, publish
issues, contact source authors, or start a primary analysis. Source checks,
algebraic counterexamples and small calculations are welcome if your tools
support them. Record precisely what you ran. A command printed in a README
is not evidence that you executed it.

## Remit

EPRP develops a continuously revised portfolio of consequential, well-posed
questions for downstream research teams. It supplies literature orientation,
data preparation, criticism and small feasibility probes. It is not selecting
one winning project or producing primary research results here.

Deep time has priority. Extinction and the reciprocal relevance of past and
present biodiversity change are major interests, but neither is mandatory
for every question. Theory and simulation questions are legitimate alongside
empirical ones. Do not optimise the portfolio around convenient datasets,
Barry's previous specialisms or immediate modern applications.

The first tranche contains 50 questions, Q-001–Q-050. Expansion is paused for
review. Statuses, tiers and phase-2 rankings are provisional. A high-value
question may have difficult next steps; a cheap useful audit may support a
question of modest scientific importance. Keep those judgments separate.

## Form an independent view before reading the debate

1. Read `README.md`, the remit in `docs/programme.md`, and survey
   `ideas/register.md`. Note your own most consequential opportunities,
   concerns and missing ideas before reading the agents' ranking documents.
   Use the whole register to choose targets, including neglected and parked
   entries; do not let the number of attached audit files dictate importance.
2. Choose a manageable set for deeper review, explaining the selection.
   Follow each selected entry's evidence links into `literature/` and `data/`.
   Check the nearest primary literature and whether the proposed evidence can
   distinguish the actual rivals. Recent and older foundational work both
   matter. Prefer a few decisive checks to superficial coverage claims.
3. Then read `STATUS.md` and the phase-2 discussions in `ideas/`, including
   the first portfolio pass, Codex's response and subsequent replies. Test
   your initial view against their strongest arguments. State where it
   changed, where it did not, and why. This reduces anchoring; it does not
   make the review blind, since the register already contains agent judgments.

The work was developed by Claude and Codex under Barry's direction. Their
agreement, disagreement, model identities and volume of discussion do not
validate a scientific claim. Evaluate arguments and evidence, not which
participant advanced them. `AGENTS.md` and `CLAUDE.md` describe the project
workflow; reading them is not a commission to perform its operational tasks.

## Evidence you can inspect

The GitHub snapshot contains scientific notes, scripts, source manifests and
selected derived TSV tables. It does **not** contain `data/raw/`,
`data/derived/`, `scratch/` or the full set of local outputs. In particular:

- Some probes are self-contained, such as
  `data/q026-boundary-observation/`; their code and small output are tracked.
- Some source archives can be obtained independently through documented
  public URLs, for example `data/q050-covariance-support/`. Do not assume
  those URLs work in your environment until checked.
- The Q-038 and Q-044 probes use Dryad files supplied locally by Barry;
  those files are absent from GitHub. The Q-027 source is a large external
  archive, with selective-fetch code. Their tracked tables and scripts allow
  logical and internal-consistency checks, not an automatic raw-data rerun.
- Dated audits can refer to an older builder or source snapshot. Respect the
  stated version; current code and historical output need not coincide.
- Discussion references such as `76/1518` point to an unavailable board.
  Durable evidence should stand on its own in the repository. Identify any
  consequential claim that cannot be assessed without the missing discussion.

Label findings by access: directly inspected source/code/table, independently
reproduced calculation, author-reported result, or unavailable evidence.
Missing inputs limit verification; they do not prove the claim false. Conversely,
a checksum or reproducible script does not establish scientific suitability.
Do not ask for a wholesale local-cache or board export as a prerequisite to
reviewing the accessible material. Identify the smallest additional item that
would settle a consequential uncertainty.

## Questions for your review

- **Scientific opportunity and prior work:** What would a credible positive
  or negative answer change? What is already occupied by the closest work?
  Does the claimed residual survive comparison of estimands and assumptions,
  rather than just titles? Which questions deserve more development even if
  their data are difficult?
- **Inference:** Are the biological quantity, observational unit, time
  window, comparison and alternatives defined? Can the proposed evidence
  distinguish them? Challenge circular calibration, observation-process
  effects, conditioning on later outcomes, algebraic identities presented as
  mechanisms, and unjustified claims of impossibility or identifiability.
- **Evidence and feasibility:** Do the cited sources support the actual
  claims? Does nominal data access supply the required joint temporal,
  geographic, taxonomic and environmental support? Are shared data and
  chronology mistaken for independent replication? Are numerical decision
  rules calibrated and capable of yielding an informative contrary result?
- **Portfolio:** Which entries are consequential, incremental, redundant or
  prematurely parked? Distinguish a failed implementation, a failed empirical
  route and an unimportant biological question. Challenge the S/O/D/G rubric
  as well as its application; offer your own judgment without forcing all
  questions into a single score.
- **Process and reuse:** Which practices improve scientific decisions, and
  which consume effort without doing so? Can a new team use the evidence from
  this GitHub snapshot? Treat dated superseded arguments as history, while
  flagging contradictions that still affect the current register or decisions.

## Standards for findings

For each consequential finding, identify the precise claim with a short
quotation, Q-ID and commit-specific file link or section. Give your reasoning,
the evidence that supports it, its consequence and the smallest useful remedy
or discriminating check. Include the strongest reasonable defence of the
claim and what would change your own judgment.

Separate verified findings, supported concerns and unverified leads. For
literature, supply a verified DOI or stable source URL and state whether you
read the relevant primary sections, only an abstract/metadata, or recall the
work. Do not invent identifiers. Keep recall-based leads useful but distinct
from established priority or novelty objections. Log access failures as such.

Use severity (critical / major / minor) and confidence (high / medium / low)
independently. Explain what a critical or major issue invalidates or changes:
the implementation, interpretation, empirical route, ranking, or question.
A design flaw does not automatically invalidate the parent question. Include
well-supported strengths and justified retained disagreements; no quota of
faults or recommendations is required.

## Report

1. **Executive assessment:** at most 300 words, leading with the decisions
   your evidence would change.
2. **Ranked findings:** a compact table or numbered findings, with the fields
   above. Do not force long arguments into unreadably wide tables.
3. **Coverage and dispositions:** mark entries substantively reviewed,
   skimmed or unassessed. Give keep/revise/merge/park/reject recommendations
   only where you have grounds; “unassessed” is valid. A compact ID-grouped
   ledger is enough. Do not invent 50 verdicts to fill a template.
4. **Development priorities:** up to three strongest candidates for further
   development, possibly none. For each, distinguish scientific importance
   from next-work priority and name the cheapest decisive test, usable
   evidence and main failure route. Recommend project readiness only if the
   inspected evidence supports it; selection remains Barry's decision.
5. **Gaps and process:** up to five consequential missing questions and up to
   five concrete workflow changes, only when warranted. Proposed gaps do not
   add entries to the paused register.
6. **Verification limits:** the reviewed SHA, access/tool limitations,
   computations actually run and the most consequential unverified claims.

Spend effort where it can change a scientific decision. We value a small
number of defensible findings, including unexpected defences of neglected
questions, more than a comprehensive-looking set of weak verdicts.
