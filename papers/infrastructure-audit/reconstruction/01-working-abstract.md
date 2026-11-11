# Step 1: working abstract (key questions)

Reconstruction pass, 12 November 2026. Not for submission: the reference point for every later step.
Main message (agreed in chat, 11 November): *agent-assisted replay of palaeobiology's shared data and
software produced twelve documented findings, each with receipts, that change what researchers should
record, test or trust.* Wording stays within `manuscript/estimands.md`.

## Why are we doing this?

Debates over palaeobiological inference have centred on sampling bias in the rock record. The shared
layers between rocks and results — databases, deposits, plate models, packages — are used constantly
but rarely replayed.

## What are the aims?

**Core:** show what systematic replay of that shared layer finds, and what each finding changes for
inference. **Sub-aims:** classify the kinds of finding; measure consequences where possible; record the
auditors' own errors.

## What hypotheses underpin the aims?

1. Problems concentrate at hand-offs between producers and users (deposits, version changes, unit and
   type conversions, reference frames), where assumptions are not shared, rather than in core algorithms.
2. Many are invisible from published text and documentation; they appear only when outputs are replayed
   against known truth or their own source.
3. First-pass findings overstate; a second actor checking by a separate route will narrow some of them.

## What did we do?

Mirrored databases and deposits, benchmarked packages against simulations with known answers, and
recomputed published numbers; chose twelve cases by consequence; replayed each from pinned inputs with
second-actor checks.

## What did we find?

The twelve findings span version changes, internal inconsistencies, implementation defects, interval
semantics, model disagreement and published numbers that fail replay. The second-actor check narrowed or
withdrew six original statements (supplement S3).

## What do the results mean?

Fidelity of the shared layer is a distinct source of uncertainty, alongside sampling bias. It is
checkable cheaply in time and data, and it is checkable only by execution, not by reading.

## What is it good for, and how does it generalise?

Concrete actions for users, maintainers, journals and depositors. The approach applies to any field built
on community databases and shared packages (ecology, biodiversity informatics), and to agent-assisted
verification generally.

## Notes for the next steps

- **The hypotheses are new.** The current draft has none. As a case series, the paper cannot test them
  formally, but the twelve cases bear on each. The Results could be organised around them rather than by
  case class: hypothesis 1 (where problems sit), hypothesis 2 (how they were found), hypothesis 3 (what
  rechecking changed).
- **Hypothesis 1 is the most interesting and the least supported.** Most of the twelve cases arguably sit at
  hand-offs (the clear exceptions are admtools and PyRate, which are core algorithms), but we selected them, so the count is not evidence. It needs stating as a pattern in this
  series, not a property of the infrastructure.
- **"Cheaply" in "What do the results mean?"** is unmeasured. It is fine as a working note, but the
  estimands forbid it in the products unless we cite cost evidence, such as replay wall-times from the
  receipts.
- **The long-standing question** (how much does the infrastructure, as opposed to the rock record, shape
  inference?) needs anchoring in the sampling-bias literature (e.g. Raup 1972; Alroy et al. 2008) and in
  reproducibility work. Our current 14 references do not do this.
