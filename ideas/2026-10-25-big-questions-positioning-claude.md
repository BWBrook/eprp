# The community's Big Questions as a benchmark for EPRP

Claude, 25 October 2026. Barry's prompt (Claude chat, 25 October 2026):
"Note also the 'Identifying the Big Questions in paleontology: a
community-driven project' (Paleobiology, 2025) that the References side agent
has uncovered. Definitely worth you and Codex taking a look at this!"

The source is Smith, Dowding et al. 2025, *Paleobiology* 51(3):408–431,
doi 10.1017/pab.2025.10042, CC BY 4.0. The References session catalogued it
in `resources/library/notes/big-questions-2025.md`, with the 89 final, 117
preliminary and 528 raw questions as TSV files, and a crosswalk to our
registers (76/2405). I read the note, the 89 final questions and targeted
raw questions; I have not read the paper's full text.

## 1. What it tells us about EPRP

**Our register sits inside the field's own priorities.** 61 of the 89 final
questions have a register neighbour, including every question in the four
core themes:
- Scaling (SEP);
- Biodiversity Dynamics (BST);
- Biodiversity Drivers (BD);
- Extinction Dynamics (ED).

Barry's 2003 list (76/2357) maps onto the same territory. Overlap at this
level confirms relevance; it does not establish novelty.

**Their selection criteria are a sharper gate than ours.** The 89 questions
were filtered against Sutherland et al. 2009's seven criteria. A Big Question:
- addresses a real gap;
- is not just a topic;
- is answerable with a realistic design;
- has a scale a team can address;
- has a factual answer;
- is not answerable with "it all depends";
- is not answerable with yes or no.

**Criterion 6 diagnoses our first contract pair.** Both retired contracts
ended in "it depends" answers:
- **Life history:** the route sets the sign, and duration modulates it.
- **Recoverability:** whether the mechanisms can be distinguished depends on
  what is observed.

Both were also answered by priors that a full-text check would have found
first. I propose adding the seven criteria, with criterion 6 stated
explicitly, to the nomination cards and the contract gate, beside the
prior-first rule proposed in 76/2402.

## 2. Raw questions close to our live candidates

The final questions are broad programme statements. The 528 raw questions
are sharper, and a close match there is a positioning flag: someone in the
field is asking it.

| Our candidate | Closest raw or final question | Reading |
| --- | --- | --- |
| Card 3, recovery on substitute builders | Raw: "What does it mean for ecosystems when after extinctions not every niche that was emptied gets filled again during recovery and diversification?"; final ED5 (functions maintained) and ED7 (recovery patterns) | The community poses the *vacancy* half. Card 3's prerequisite and substitute half is the sharpening. |
| Q-045 and the copied-sea vintages | Raw: tools that use geological maps and occurrence databases to "predict where and what fossils we might expect" | The forecasting framing has a community neighbour |
| Q-038 and Q-012 | Raw: "How predictable is extinction?"; final PTS2 (determinants of species longevity) | Positioning for both |
| L1 and B-001 | Raw: deep-sea records as "repeating 'natural experiments' in community assembly" | Natural-replicates branch |
| Q-011 | Final ED2: a unified definition of "mass extinction" | See section 3 |

Neither CN2 (cue reliability) nor the order null has a close raw neighbour.
For theory that could mean either open ground or a question the field does
not prioritise.

## 3. Two openings the benchmark exposes

**1. ED2 and Q-011: what makes a mass extinction a class, if anything does?**
- The quantitative core is largely settled as a continuum:
  - Alroy 2008: lognormal rates, with no sharp break;
  - Marshall 2023: the Big Five are not statistically distinct from
    background;
  - Crampton et al. 2026: graptoloid extinction magnitudes are continuous
    and unimodal.

  A *unified definition* would therefore be either a convention or
  *process-based*. One process-based candidate defines a mass extinction by
  its regime: events where extinction outruns the capacity of recovery
  processes, using the order null's absorbing-boundary logic and Q-011's
  question of forcing against biotic amplification.
- This is offered as a later candidate, not a replacement in the next pair.
  Q-011 is on hold behind Q-030's forcing audit, and a definition risks
  failing criterion 5 (a factual answer).

**2. AFR1–AFR3: an output EPRP has nearly built without trying.** The
Databases, Packages and References side sessions have documented, with
replayable evidence, how data access, processing and software shape
palaeobiological inference:
- [Detail withheld pending disclosure to the data custodian.]
- **Time scale:** PBDB has silently re-dated its intervals three times since
  2024.
- **Software defects:**
  - admtools `strat_to_time` above hiatuses;
  - fossilbrush `flag_ranges` comparing text;
  - GRIWM intervals that are not intervals for extinction time;
  - RevBayes's FBD range process disabled;
  - a high bias in PyRate's preservation rate.
- **Deposits:** a corrupted capture-history column in a published deposit.
- **Plate models:** palaeolatitude spreads of degrees across models, and two
  absolute frames under one name.

That is a direct, evidence-backed answer to:
- AFR1 (quantifying biases);
- AFR2 (identifying and correcting data-entry and processing biases);
- AFR3 (data loss in historical collections);
- FI1 (open, combinable data).

It is also an example of AI-assisted auditing of shared research
infrastructure, which is close to Barry's interest in how science is
changing.

**This is outside the hypothesis registers and touches outward-facing
matters.** Barry has queued contacts with the data and software providers: the sources
catalogue's CONTACTS, for example C10 for PBDB, and the software catalogue's
contacts for package authors. Whether and when to turn it into an output is his
decision. I raise it because the Big Questions list shows the field
explicitly asking for it.

## 4. Effect on the next pair (76/2402)

The proposal stands, with two additions:
- **Card 3 should cite the raw vacancy question and ED5/ED7 as its
  positioning.** Its first gate is the full-text prior check (the
  vacancy-refilling literature) and the PaleoReefs support check.
- **Nomination cards and contracts should state their nearest Big Question
  and pass the seven criteria before drafting.**

Codex has not yet replied to 76/2402. These notes inform its reply and do
not pre-empt it.
