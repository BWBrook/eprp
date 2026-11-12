# AI agents check the foundations of fossil science

Barry W. Brook (University of Tasmania), prepared with Claude (Anthropic) and Codex (OpenAI). Draft of
12 November 2026; a plain-language summary of a living research repository,
<https://github.com/BWBrook/eprp>.

<div id="figures"></div>

## The puzzle

Large-scale fossil research depends on shared resources: databases of fossil finds, data files
published with papers, geological time scales, maps of past continents, and software that turns it all
into rates of extinction and diversity. Each is built by someone else and changes over time, so a
problem in one can travel into the studies that use it. Checking them means copying each resource,
finding cases where the right answer is known, and comparing.

## What we did

Two AI systems, working with one scientist, spent a month building a research program on the fossil
record. Along the way they copied databases, tested software against known answers and recomputed
published numbers, logging 189 initial candidate findings and later additions. We selected twelve
varied cases for their consequences for analysis and re-checked each from fixed, checksummed inputs. Every result is recorded
with the command that reproduces it.

## What we found

1. **Databases can lack records that a study deposited.** About one in five of the [368,760]{.C191}
   mollusk records in one recent study's data file were absent from the public Paleobiology Database as
   it stood on 23 October 2026.
2. **Ages can shift, or disagree with their own sources.** Between two archived downloads of that
   database, the most common starting age of [460]{.C076} time intervals changed. In a microfossil
   database, [4,111]{.C040} of [56,387]{.C040} comparable stored ages differed by more than 10,000 years
   from those implied by its own reference points.
3. **Software can convert or compare numbers wrongly.** One package gave the wrong age to
   [3,972]{.C096} of [8,282]{.C096} test points, by up to [3.0]{.C096} million years. Another compared
   numbers as words, so a difference of [100]{.C102} passed a threshold of 5 unflagged.
4. **Published numbers can fail recomputation.** A printed probability of about one in three thousand
   trillion is about one in three ([0.316]{.C190}) under the test the paper describes. Two published
   spreadsheets differ from their source files in [2,967]{.C035} and [220]{.C048} rows.
5. **Uncertainty ranges and model choices need checking.** In two simulated groups of species with
   constant fossil sampling, a bound on when a species disappeared contained the true end in
   [1,909]{.C194} of [2,000]{.C194} cases. In a separate design, a tool's ranges labeled 95% contained
   the true preservation rate in [33]{.C107} of [50]{.C107} datasets. Three maps of past continents placed each tested
   site at latitudes a median of [13.6]{.C125} degrees apart, 400 million years ago.

## What it means

AI agents can check the foundations of fossil science systematically, and what they find is specific
enough to act on: record download dates and versions, compare more than one map of past continents,
recompute a number before building on it, version database changes, and test software against known
answers. The agents' own mistakes were caught the same way: re-checking corrected the first account of
six of the twelve cases.

## Limits

These twelve examples were chosen for their consequences, so they say nothing about how common such
problems are. We did not rerun the studies that used these resources, so whether any published
conclusion changes is open, as are the causes of the database differences. The people responsible for
each resource had not yet been contacted, and nothing here compares AI checking with careful human
checking. The range-end benchmark also failed one predeclared agreement check.

## How this work was done

OpenAI's Codex re-checked every finding, built the record of results and reviewed the wording.
Anthropic's Claude compiled the candidate findings, chose the twelve cases, drafted this summary and
designed the graphical abstract. Barry Brook guided the program and decides on release and on contact
with the people responsible for each resource.

## Read more

The full article, its supplement and a guide for AI agents are in the repository under
`papers/infrastructure-audit/`. Each number above carries a claim identifier in the article's claims
ledger, with the evidence and the command that reproduce it.
