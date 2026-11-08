# What turns up when AI agents check the foundations of fossil science?

Barry W. Brook (University of Tasmania), with Claude (Anthropic) and OpenAI Codex. Draft of 2026-11-08; a plain-language summary of a living research repository, <https://github.com/BWBrook/eprp>.

## The puzzle

Studies of the fossil record rarely start from the rocks. They start from shared databases of fossil
finds, published data files, geological time scales, maps of where the continents used to be, and
software that turns all of this into rates of extinction and diversity. Each layer is built by someone
else and changes over time. If a layer has a problem, every study built on it can carry the problem
without anyone noticing.

<div id="figures"></div>

## Why it is hard

Checking these layers is slow, unglamorous work that nobody is paid to do. The people best placed to
spot a problem are usually the busiest. So the layers are used far more often than they are checked.

## What we did

- Two AI systems, working with one scientist, spent a month preparing a research programme on the
  fossil record. Along the way they copied databases, tested software against cases with known answers,
  and recomputed published numbers. That produced 189 possible problems.
- We chose twelve that matter most for what a researcher would conclude.
- For each, one agent redid the check from fixed copies of the inputs, and a different agent rederived
  the result by a different method. Every result has a command that anyone can rerun.

## What we found

1. **Some published data cannot be rebuilt from today's public database.** About one in five of the
   [368,760]{.C191} mollusc records in one recent study's data file are missing from the public database
   as it stood in October 2026. We do not know why, and we report only counts.
2. **Fossil ages can shift between downloads.** The same database query on different dates returned
   different ages for [460]{.C076} time intervals in one gap between downloads. In another case, a
   database's stored ages disagreed with its own reference points for [4,111]{.C040} samples. Recording
   the date of every download matters.
3. **Some widely used software gives wrong answers in specific situations.** One package converted rock
   thickness to time wrongly in some layers above gaps in the record, by up to [0.466]{.C096} million
   years. Another compared numbers as if they were words, so a difference of 100 counted as smaller than
   5. A third reports a range that reflects only uncertainty in the dates it is given, not uncertainty
   about when a species died out.
4. **Some published numbers do not survive recomputation.** One paper printed a probability of about
   one in three thousand trillion; the test it describes gives about one in three ([0.316]{.C190}). Two
   published spreadsheets differ from the files they were made from, in [2,967]{.C035} and [220]{.C048}
   rows. We did not rerun those studies, so we cannot say whether their conclusions change.
5. **The checks can tell good from bad.** Long-established methods for estimating when a species
   disappeared did what they claim in our tests, covering the true answer in [1,909]{.C194} of
   [2,000]{.C194} cases for one method. Another tool's ranges missed the truth more often than they
   should ([33]{.C107} of [50]{.C107} hits where about 48 were expected).

## What it means

None of these problems needed new fossils or new theory to find. They needed someone to recheck each
layer against a known answer or against its own source. AI agents make that kind of checking cheap. This
is a set of examples, not a survey: it does not tell us how common such problems are, and it does not
show that AI checking is better than careful human checking.

## How this work was done

Claude (Anthropic) made most of the original findings, chose the twelve cases and drafted this summary.
OpenAI Codex redid every check and built the record of results. Barry Brook guided the programme and
decides what is released and when the people responsible for each data source are contacted. Every
number here traces to a rerunnable command in the public repository.

## Sources
