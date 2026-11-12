# Step 1c: the main message (25 words or fewer)

12 November 2026, distilled from `1a-working-abstract.md` and `1b-abstract.md`.

> **AI agents can systematically check the databases and software behind fossil-record research; they found
> verifiable errors and pitfalls that researchers need to know about.** (24 words)

Revised the same day after Barry's comment that the first version was not clear to a new reader ("too much
wood for trees. Don't assume anything of your reader"). The first version was: "AI agents can
systematically replay the shared data and software beneath big paleobiology, exposing documented,
checkable findings that change what researchers should trust."

## Why this wording

- **Plain words for a reader new to the topic.** "Check" replaces "replay". "The databases and software
  behind fossil-record research" replaces "shared data and software beneath big paleobiology", and
  "verifiable errors and pitfalls" replaces "documented, checkable findings". The paper can introduce the
  technical terms later.
- **"Errors and pitfalls"** covers the whole series. Some cases are errors (package defects, a
  misprinted probability, corrupted spreadsheets). Others are intended choices that trip users up (interval
  re-dating, plate-model disagreement, what an interval measures).
- **"Verifiable"** carries the receipts: every finding has a command and pinned inputs.

The notes below on the first version still apply where relevant:

- **The agents are the subject.** Barry, 12 November: "the agent aspect here is notable, because we're
  highlighting a potentially valuable new approach to 'big paleo'." The 11 November version made replay the
  subject and the agents a modifier.
- **"Can"** is a capability shown by doing it, once, in one program. It is not a comparison with human
  auditing, which the estimands forbid.
- **"Big paleobiology"** names the audience: database-scale, computational work that depends on this
  layer.
- **"Findings", not "problems"**, because two of the twelve cases are intended design choices.
- **"Documented, checkable"** carries the receipts. Every finding has a replay command and pinned
  inputs.
- **"Change what researchers should trust"** is the consequence. Keep it plural and general. It must not
  become a claim that published conclusions changed; none was replayed.

## Lines of evidence that serve it

1. **What replay found:** the twelve cases.
2. **Where findings sit:** hypothesis 1, hand-offs between producers and users.
3. **How they were found:** hypothesis 2, by re-execution, not reading.
4. **What the second-agent check changed:** hypothesis 3, six original claims narrowed.

Each section of the rebuilt paper should advance this message. Anything that does not should be cut or
moved to the supplement.

## After Codex's critique (160/3260)

The main message stands. The explanatory frame widens from "fidelity" to four kinds of dependency that
agents checked: **data transformations, implementations, model choices and output meaning**. Legitimate
plate models can disagree while each is implemented faithfully, and a correctly computed interval can
answer a narrower question than a user expects. "Errors and pitfalls" covers both. The organizing
questions in 1a replace the post hoc hypotheses.
