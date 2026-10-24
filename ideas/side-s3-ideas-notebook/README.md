# S3 (side project): the fates of the claims in Barry's 2003 notebook

**Status.** Side project, low priority. This is not part of the main project
portfolio and not a register entry.

Barry (Claude chat, 24 October 2026, exact words): "I like S3 as a general
idea. Rather than it being part of the main body of possible projects, it's
more like a side hobby we can work on as the other lines continue to get
developed. I do find such meta-science interesting, and even if it only ever
remains private, it's grist for our ongoing intellectual mill."

**Source.** [Barry's 2003 list](../../literature/2003-brook-papers-of-interest.md),
293 entries.

**Background.**
- **Origin:** [Claude's 2003-list note](../2026-10-24-barry-2003-list-claude.md),
  seed S3.
- **Codex's narrowing, accepted (76/2360):**
  - this is an annotated intellectual history of one selected notebook, not a
    survival analysis of a field's ideas;
  - a reply and the claim it attacks are not independent controls;
  - "forgotten" is not "refuted";
  - Barry is not given routine adjudication.

## Rubric, version 0

The rubric was fixed on 24 October 2026, before any fate was coded. Changes
to it are versioned here with a reason, and codes made under an earlier
version are kept.

1. **The unit is a claim, not a paper.**
   - Each research article contributes one *central claim*, stated in a single
     sentence from its abstract or main conclusion.
   - Comments, replies and responses are linked to the claim they address and
     coded by *role*: support, challenge or reply. They are not separate
     claims unless they make a new one.
   - News pieces are coded as *coverage* of a claim.
   - Book reviews are excluded.
2. **Fates, as of the coding date.** Each needs at least one cited source
   published in 2015 or later, or the earliest source that settled the
   matter.

   | Fate | Definition |
   | --- | --- |
   | **Upheld** | The claim stands in current reviews, with independent support since 2003. |
   | **Refined** | The core stands, but scope, magnitude, timing or mechanism has materially changed. |
   | **Contested** | Active disagreement continues, with no consensus in recent reviews. |
   | **Overturned** | Current reviews reject it, and the refuting work is named. |
   | **Dormant** | Little engagement since about 2010, neither tested nor refuted. |
   | **Dissolved** | The question was reframed so that the claim no longer has a truth value as stated. |
3. **Confidence.** Each code is marked high, medium or low, with one sentence
   of reasoning.
4. **Coders.** Claude and Codex code independently, without seeing each
   other's codes. Each writes to its own file: `codes-claude.tsv` and
   `codes-codex.tsv`. Agreement (Cohen's κ) is reported, and disagreements are
   discussed and logged, not forced to consensus.
5. **Barry.** He may annotate any entry with what he saw in it in 2003, if he
   wishes. Nothing waits on him.
6. **Inference limits, to restate in any write-up:**
   - selection into the notebook is Barry's;
   - three journals dominate;
   - fates depend on how claims are defined.

## First batch: the extinction-statistics debates

There are 15 entries. Kerr's news pieces on these debates (entries 90, 119,
135 and 151) are linked to them as coverage.

| Entry | Paper | Debate |
| --- | --- | --- |
| 1 | Flessa & Jablonski 1985 | Declining background extinction as an effect of taxonomic structure |
| 3 | Stigler 1985 | Mass-extinction times and correlations |
| 85 | Raup, Sepkoski & Stigler 1983 | Mass extinctions in the fossil record (exchange) |
| 89 | Kitchell & Pena 1984 | Periodicity: deterministic against stochastic |
| 92 | Hoffman 1985 | Periodicity (comment) |
| 95 | Raup & Sepkoski 1986 | Periodic extinction of families and genera |
| 103 | Muller 1986 | Comet showers, periodicity and iridium |
| 108 | Raup & Sepkoski 1988 | Testing for periodicity |
| 109 | Stigler & Wagner 1988 | Testing for periodicity (response) |
| 146 | Rampino & Haggerty 1995 | Mass extinctions and periodicity |
| 147 | Benton 1995 | Periodicity (reply) |
| 49 | Solé, Manrubia, Benton & Bak 1997 | Self-similarity of extinction statistics |
| 59 | Kirchner & Weil 1998 | No fractals in extinction statistics |
| 67 | Kirchner & Weil 2000 | Delayed recovery from extinctions |
| 75 | Kirchner 2002 | Evolutionary speed limits |

Q-041 (periodicity under timescale uncertainty) and Q-011 (the size
distribution of extinction events) are the register's current forms of these
debates. A batch-1 code cannot be used as evidence for or against them; this
is intellectual history only.

**State (24 October).** The rubric is fixed. Draft claim sentences for batch 1
are in [`claims-batch1.tsv`](claims-batch1.tsv). As Codex asked (76/2364), the
claims are shared and agreed before either coder judges a fate, so that both
code the same unit.

How the sentences were drafted:
- A scout drafted them from each paper's own abstract or first page, blind
  to later work.
- All 15 DOIs were checked against Crossref.
- **Seven claims are inferred** from titles and reference lists, because no
  open abstract exists: entries 3, 85, 92, 103, 146 and 147, plus 109 in part.
  They need the full text before fate coding. Barry's library side session,
  or institutional access for private use, could supply it.

Codex may amend any sentence. No fates have been coded.
