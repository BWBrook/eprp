# GPT-6 Pro consultation prompt, blind to the repository (drafted 21 October 2026)

Drafted by Claude at Barry's request (Claude chat, 21 October 2026): "could you give me a new prompt to use for an
additional session for GPT-6 Pro, that does not give it access to the repo and tries to deliver us additional
novelty". It tests whether a consultant without our notes returns less in-distribution ideas than the three
repository-informed briefs in [2026-10-21-gpt6pro-proposals/](2026-10-21-gpt6pro-proposals/). The focus is
deliberately an interval with no register or blue-sky entry. The text below is what Barry pastes.

---

## Independent research-question consultation: the Ediacaran–Cambrian world (about 580–485 Ma)

I am Barry Brook, an ecologist and modeller working on extinction, macroevolution and simulation. I work with AI
research agents that can build substantial analysis and simulation software. I also have a large CPU cluster
(48 nodes × 28 cores) and one A100 GPU. We are assembling a long list of candidate research questions before
choosing any to pursue.

I want you as an independent consultant. Your value is ideas we would not generate ourselves, so I am deliberately
giving you no access to our working notes. Please do not search for or consult any repository or document of mine.

### Focus

The interval runs from the first macroscopic multicellular communities, the Avalon assemblage at about 575 Ma, to
the end of the Cambrian at about 485 Ma. It includes:

- the Ediacaran biota (rangeomorphs, erniettomorphs, dickinsoniids and others) and its disappearance, including the
  White Sea–Nama turnover and the proposed late-Ediacaran ("Kotlin") and end-Ediacaran extinctions;
- the Cambrian radiation and small shelly faunas;
- early predation;
- ecosystem engineering, including the agronomic or substrate revolution;
- Cambrian extinctions and turnovers: Sinsk or Botomian, Drumian, the trilobite biomere boundaries and SPICE.

Questions may concern extinction, diversification or ecology, or how reliable our inferences about any of these
are.

### Part A: up to ten candidate questions

Give one card per question, each at most 350 words, covering:

1. **The question**, in one sentence precise enough that a specialist would accept it.
2. **Why it matters.** Which accepted account would change, and what would a negative result teach?
3. **Closest prior work.** Two to four primary sources, with DOIs, and why each does not already answer the
   question. Say how deeply you read each: full text, abstract only, or recalled.
4. **The decisive test.** Which observation, analysis, experiment or simulation would discriminate the main
   competing answers?
5. **Evidence.**
   - The named datasets, databases, collections or archives, and whether you verified that each is accessible.
   - The main identification problem: taphonomy, dating, sampling or taxonomy.
6. **The cheapest first step** that could kill or support the idea in days rather than months.
7. **Your honest probabilities** that the question is (a) novel and (b) answerable with existing data within two
   years.

Across the set:

- At least three questions should be ones you expect most specialists to find surprising, or wrong-headed at
  first, yet defensible.
- At least two should rely on datasets, methods or tools that appeared from 2023 onward.
- At least two should import a concept or method from outside palaeobiology where it does real work: for
  example from ecological theory, epidemiology, statistics, physics, evolutionary genomics or machine learning.
- At least two should concern the reliability of inference itself, such as taphonomic windows, dating or
  sampling, rather than the biology directly.
- Use simulation or heavy computation only where it is the decisive tool, and say why. Several questions should
  need neither.

If fewer than ten candidates meet the bar, give fewer and say why.

### Part B: deep dives on your two best candidates

About 2,500 words each, covering:

- the competing hypotheses and what each predicts;
- a concrete design, saying what is held fixed and what is varied;
- the data needed and their real availability;
- the main ways the study could fool itself;
- stopping rules that accept a null result.

### Part C: the consultant's view

About 800 words, answering:

- Where in this interval does the consensus rest on weaker evidence than its confidence suggests?
- Which long-running debates remain unresolved because they cannot be tested as posed, and what reformulation
  would make them testable?
- What is the most under-asked question about this period?

### Standards

- Prefer primary literature and give DOIs. Distinguish the sources you read from those you recall. Do not invent
  citations; if you are unsure, say so.
- Write "not found in my search" rather than "nothing exists".
- Use plain, precise language, with equations where they help.
- Deliver a single markdown file.
