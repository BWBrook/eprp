# Step 1a: working abstract (key questions)

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

## What questions organize the paper? (revised 12 November after Codex's critique)

1. **Where did the selected findings arise?** In data transformations, implementations, model choices or
   output meanings, coded by a stated rule.
2. **What checks established them?** Re-execution against known answers, recomputation from source, code
   inspection and arithmetic, recorded case by case, including mixed routes.
3. **What changed during review?** The corrections to initial accounts made during replay, and to the
   paper's wording during review.

*Why questions, not hypotheses.* The three expectations in the first draft were written after the
findings, and the cases were chosen for consequence, not sampled. They could not test where problems
concentrate or isolate the benefit of a second reviewer (Codex critique R1, 160/3260). Barry's template
asks for a priori hypotheses. For a selected case series, organizing questions are the honest
equivalent. A prospective test would need an eligible audit population, fixed classification and matched
review routes: a separate study.

## What did we do?

Mirrored databases and deposits, benchmarked packages against simulations with known answers, and
recomputed published numbers; chose twelve cases by consequence; replayed each from pinned inputs with
second-actor checks.

## What did we find?

The twelve findings span version changes, internal inconsistencies, implementation defects, interval
semantics, model disagreement and published numbers that fail replay. The second-actor check narrowed or
withdrew six original statements (supplement S3).

## What do the results mean?

Checking the shared layer means checking four things: data transformations, implementations, model
choices and the meaning of outputs. Each can change what a researcher should conclude, and each can be
checked directly against known answers or its own source. Agents carried out those checks across a whole
research program.

## What is it good for, and how does it generalise?

Concrete actions for users, maintainers, journals and depositors. The approach applies to any field built
on community databases and shared packages (ecology, biodiversity informatics), and to agent-assisted
verification generally.

## Notes for the next steps

- *(Superseded by the questions above.)* **The hypotheses are new.** The current draft has none. As a case series, the paper cannot test them
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
