# What turns up when AI agents check the foundations of fossil science?

Barry W. Brook (University of Tasmania), with Claude (Anthropic) and OpenAI Codex. Draft of 2026-11-08; a plain-language summary of a living research repository, <https://github.com/BWBrook/eprp>.

## The puzzle

Studies of the fossil record rarely start from the rocks. They start from shared databases of fossil
finds, published data files, geological time scales, maps of where the continents used to be, and
software that turns all of this into rates of extinction and diversity. Each layer is built by someone
else and changes over time. If a layer has a problem, a study built on it can carry the problem without
anyone noticing.

<div id="figures"></div>

## Why it is hard

Each layer has its own format, versions and assumptions. Checking one properly means copying it, finding
a case where the right answer is known, and comparing. Doing that across many layers is slow and
detailed work.

## What we did

- Two AI systems, working with one scientist, spent a month preparing a research programme on the fossil
  record. Along the way they copied databases, tested software against cases with known answers, and
  recomputed published numbers. That produced 189 candidate findings at first, and more later.
- We chose twelve that matter most for what a researcher would conclude.
- For each, a different agent redid the check from fixed copies of the inputs, alongside the extra checks
  recorded for that case. Every result is recorded with the command that reran it and the inputs it needs.

## What we found

1. **Some deposited records are absent from a dated public snapshot of the database.** About one in five
   of the [368,760]{.C191} mollusc records in one recent study's data file were not in the public
   database as it stood on 23 October 2026. We do not know why, and we report only counts.
2. **Fossil ages can shift between downloads.** Between two archived downloads, the most common recorded
   starting age of [460]{.C076} time intervals changed. In another database, stored ages disagreed with the database's
   own reference points, under our interpolation rule, for [4,111]{.C040} of [56,387]{.C040} samples that
   could be compared. Recording the
   date and version of every download matters.
3. **Software checks found errors and clarified what outputs mean.** One package converted rock thickness to
   time wrongly in some layers above gaps in the record: in one test, [3,972]{.C096} of [8,282]{.C096}
   points were wrong, by up to about [3.0]{.C096} million years. Another compared numbers as if they were
   words, so at a threshold of 5 it treated a difference of 100 as too small to flag. A third reports a
   range that measures how its answer changes with uncertain fossil dates, not the uncertainty from how
   patchily fossils are found.
4. **Some published numbers do not survive recomputation.** One paper printed a probability of about one
   in three thousand trillion; the test it describes gives about one in three ([0.316]{.C190}). Two
   published spreadsheets differ from the files they were made from, in [2,967]{.C035} and [220]{.C048}
   rows. We did not rerun those studies, so we cannot say whether their conclusions change.
5. **The checks found successes as well as failures.** Under even sampling in two simulated groups of
   species, a long-established method for bounding when a species disappeared covered the true answer in
   [1,909]{.C194} of [2,000]{.C194} cases, although a separate agreement check failed. In a different test,
   of how often fossils are preserved, one widely used tool's ranges covered the truth in only
   [33]{.C107} of [50]{.C107} simulated datasets.

## What it means

None of these problems needed new fossils or new theory to find. They needed each layer to be rechecked
against a known answer or against its own source. This is a set of examples from one programme, not a
survey: it does not tell us how common such problems are, it does not test whether any published
conclusion changes, and it does not show that AI checking is better than careful human checking.

## How this work was done

Claude (Anthropic) made most of the original findings, chose the twelve cases and drafted this summary.
OpenAI Codex made some findings, redid every check, built the record of results and reviewed the wording.
Barry Brook guided the programme and decides what is released and when the people responsible for each
data source are contacted. Every number here traces to a recorded command in the public repository.

## Sources
