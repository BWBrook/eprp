# What turns up when AI agents check the foundations of fossil science?

Barry W. Brook (University of Tasmania), prepared with Claude (Anthropic) and Codex (OpenAI). Draft of
12 November 2026; a plain-language summary of a living research repository,
<https://github.com/BWBrook/eprp>.

## The puzzle

Studies of the fossil record rarely start from the rocks. They start from shared databases of fossil
finds, data files published with papers, geological time scales, maps of where the continents used to
be, and software that turns all of this into rates of extinction and diversity. Each of these resources
is built by someone else and changes over time. A problem in one of them can travel quietly into every
study that uses it.

<div id="figures"></div>

*Where along the chain from fossil to published result the checks found problems; colors mark the kind of check.*

## Why it is hard

Each resource has its own format, versions and assumptions. Checking one properly means copying it,
finding a case where the right answer is known, and comparing. Doing that across a whole field's
toolkit is slow, detailed work. In this program, AI agents did it and recorded every step.

## What we did

- Two AI systems, working with one scientist, spent a month building a research program on the fossil
  record. Along the way they copied databases, tested software against cases with known answers, and
  recomputed published numbers. That produced 189 candidate findings at first, and more later.
- We chose the twelve that matter most for what a researcher would conclude.
- A second agent reran each check from fixed, checksummed copies of the inputs. Every result is recorded
  with the command that reproduces it.

## What we found

1. **A database can lack records that a published study deposited.** About one in five of the
   [368,760]{.C191} mollusk records in one recent study's data file were absent from the public
   Paleobiology Database as it stood on 23 October 2026.
2. **Ages can shift between downloads, or disagree with their own sources.** Between two archived
   downloads of that database, the most common starting age of [460]{.C076} time intervals changed. In a
   microfossil database, [4,111]{.C040} of [56,387]{.C040} stored sample ages differed from the ages
   implied by the database's own reference points. Recording the date and version of every download
   keeps such changes visible.
3. **Software can contain errors, and its outputs can mean something narrower than expected.** One
   package converted rock thickness to time wrongly next to gaps in the record: in one test,
   [3,972]{.C096} of [8,282]{.C096} points were off, by up to about [3.0]{.C096} million years. Another
   compared numbers as if they were words, so at a threshold of 5 it let a difference of [100]{.C102} pass
   unflagged. A third reports a range that measures how its answer depends on uncertain fossil dates.
4. **Published numbers can fail recomputation.** One paper printed a probability of about one in three
   thousand trillion; the test it describes gives about one in three ([0.316]{.C190}). Two published
   spreadsheets differ from the files they were made from, in [2,967]{.C035} and [220]{.C048} rows.
5. **Tests against known answers show where methods hold and where they slip.** In simulated fossil
   records, a long-established method for bounding when a species disappeared covered the true answer in
   [1,909]{.C194} of [2,000]{.C194} cases. A widely used tool's ranges for how often fossils are preserved
   covered the truth in [33]{.C107} of [50]{.C107} simulated datasets, against the 95% it promises. Three
   maps of past continents placed the same fossil sites a median of [13.6]{.C125} degrees of latitude apart
   400 million years ago.

## What it means

AI agents can check the foundations of fossil science systematically, and what they find is specific
enough to act on. Researchers can record download dates and versions, compare more than one map of past
continents, and recompute a published number before building on it. Database and software maintainers
can version their changes and test against known answers. Journals can ask for data in formats that
machines read exactly. The agents' own mistakes were caught the same way: a second check corrected the
first account of six of the twelve cases.

## Limits

These are twelve examples chosen for their consequences, so they say nothing about how common such
problems are. We did not rerun the studies that used these resources, so whether any published
conclusion changes is open, and so are the causes of the database differences. The people responsible
for each resource had not yet been contacted when this was written. Nothing here compares AI checking
with careful human checking.

## How this work was done

OpenAI's Codex reran every check, built the record of results and reviewed the wording. Anthropic's
Claude compiled the candidate findings, chose the twelve cases and drafted this summary. Barry Brook
guided the program and decides what is released and when the people responsible for each resource are
contacted. Every number here traces to a recorded command in the public repository.

## Sources
