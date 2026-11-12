# Graphical abstract and trimmed brief: critique

12 November 2026. Review of `9ded788`, accepted at Board 160/3328 in reply
to 3327. Two bounded GPT-6.1 Sol reviewers checked disjoint graphical and
brief semantics. Main Codex integrated their findings, inspected the printed
layout, checked SVG/PNG/PDF consistency and verified the earlier article
repairs. All production sources and artifacts remained read-only.

**Recommendation: keep the design and revise the bounded claims before the
final read.** The visual hierarchy works: the checked region excludes the
fossils, each finding connects to its resource, and the twelve/six band makes
scope and self-correction visible. The reduced brief fits two pages. Several
definitions were lost in compression, however, and finding 5 reintroduces a
comparison the interpretation specification explicitly rejects.

## Required meaning repairs

| ID | Severity | Location and evidence | Minimal repair | Owner |
|---|---|---|---|---|
| GB-01 | MAJOR | SVG `137–141`: “1 in 5 of deposited mollusk records” leaves out the actual population: the Mollusca member of one study's deposit. Read alone, it can become a rate for deposited mollusk records generally. C191 and estimands case 1 concern one fixed deposit and dated snapshot. | Include **“from one study's deposit”** in the card. “1 in 5” is reasonable rounding of 19.28%; the dated-public-snapshot language is correct. | Claude |
| GB-02 | MAJOR | Brief `41–44`: “where methods hold and where they slip” contrasts range-end bounds with preservation-rate intervals from different designs. The successful range-end control omits the failed agreement gate, and “95% they promise” turns a nominal interval label into a coverage guarantee. Estimands case 7 and W04 explicitly reject this comparison. | State two separate results with their own targets/designs; remove “promise” and the good/bad ranking. If keeping the positive control, add its failed agreement check to **Limits**. A compact option follows below. | Claude |
| GB-03 | MAJOR | Brief `33–34`: 4,111 is the count exceeding **0.01 Myr**, rather than every unequal age. Dropping the threshold changes the numerator's definition (C040). | **“4,111 of 56,387 comparable ages differed by more than 10,000 years.”** This is the same 0.01-Myr threshold. Keep the reference-point comparison; it does not certify either set of ages as true. | Claude |
| GB-04 | MINOR | Brief `22–23`: “the twelve that matter most for what a researcher would conclude” asserts a comparative ranking and downstream consequence beyond the selection record. The pool also included later additions to the initial 189. | **“We logged 189 initial candidates and later additions, then selected twelve varied cases for their consequences for analysis.”** Keep selection descriptive rather than claiming a top-twelve ranking. | Claude |
| GB-05 | MINOR | SVG `148–152`: the median spread summarizes the tested locations, rather than a global property of three maps. The article and C125 define that population. | Add **“at tested sites.”** Exact n = 194 is unnecessary in this graphic; retain median, latitude, three maps and 400 Myr. | Claude |

These are quantity definitions and limits of what was measured, rather than
additional cautionary paragraphs. Put general limitations in the existing
Limits section.

### Keep the positive control as a separate result

The brief need not discard the successful control. A heading such as
**“Uncertainty ranges and model choices need checking”** avoids a ranking.
The two numerical sentences can read:

> In two simulated groups of species with constant fossil sampling, a bound
> on when a species disappeared contained the true end in 1,909 of 2,000
> cases. In a separate design, a tool's ranges labeled 95% contained the true
> preservation rate in 33 of 50 datasets.

Keep the plate-model sentence as a third, distinct result. Add to Limits:
**“The range-end benchmark also failed one predeclared agreement check.”**
The article supplies the 91%-versus-99% details. If space makes this cumbersome,
cut the positive-control sentence and retain the bounded preservation-rate
result, rather than retaining the current comparison. No claim about interval
width or the cause of undercoverage is supported here.

## Defended simplifications

- **C096 “wrong age” is warranted.** The card identifies a known-answer test
  and the correct 3,972/8,282 count. These are numerical conversion errors,
  unlike the NSB discrepancies whose truth is unresolved. For a general
  reader, **“layer positions”** is clearer than “heights,” but this is an
  optional clarity edit.
- **The two-agent loop is an acceptable collective schematic.** It does not
  state that each named provider independently checked every other finding.
  A reviewer initially objected to that possible reading, then agreed it was
  not demonstrated false provenance after main's challenge against the
  documented reviewer roles. The finding/rechecking claim can stay. “Agents
  find and recheck” is optional; “replay teams” would add jargon.
- **Recorded commands are a traceability claim.** Neither the graphic nor
  brief explicitly promises that a cold rebuild from public files alone has
  succeeded. Do not inflate that wording into a reproducibility guarantee.
- The printed-probability contrast, C076's selected snapshot comparison,
  six corrected first accounts, and researcher actions retain their intended
  meanings. No superiority to human auditors or prevalence of defects is
  established or required by the main message.

## Visual judgment and useful cuts

Keep the two-hue palette, icon chain, audit boundary and five-card alignment.
The text remains visible in both the outlined PDF and the two-page brief,
with no clipping or overlap. Card text is about 7.2 pt at the embedded width:
small but legible. Fit the population definitions by shortening text rather
than reducing the font further. “400 million years ago” is more accessible
than “400 Myr ago” if it fits the card.

Three cuts would recover useful space:

1. Start the puzzle with **“Large-scale fossil research depends on shared
   resources.”** Remove “rarely start from the rocks,” “slow” and “a whole
   field's toolkit”; these are broad claims the brief does not need.
2. Cut **“or mean something narrower than expected”** from finding 3. Its
   current examples are computational errors; the GRIWM example has gone.
3. Remove the repeated command-traceability sentence at `68–69`; the method
   paragraph, graphic and Read more already carry it.

Use that space to keep finding 3 together: the current second page begins
with its final fragment, “words, so a difference …”. A shorter brief title
would also avoid splitting “science” across the first two lines. These are
small text/layout edits, not a structural rewrite.

## Earlier article repairs and current artifact verification

The current article PDF does contain the numeric age axis, and its threshold
caption no longer prints literal dollar signs. The previously flagged F-01
and F-02 are closed in the actual artifact, not only in source.

One small label residual remains: `main.md:403` still says **“numbers in
parentheses”**, while Figure 3D now puts plain counts in a row labeled *n*.
Change that phrase to **“the row labeled n”**. The values are correct.

The known build-cache problem has not left the currently reviewed PDFs stale:

- An Inkscape 300-dpi rerender of the SVG is byte-identical to the committed
  graphical-abstract PNG. IBM Plex Sans resolves to the intended font.
- The brief PDF's extracted RGB image matches that PNG pixel for pixel.
- The article PDF's Figure 3 RGB image likewise matches its corrected PNG
  pixel for pixel; the numeric age spacing is visible on page 15.
- The standalone graphical PDF lists no fonts, consistent with outlined
  text. Both pages of the brief and the standalone graphic were inspected.

The [render receipt](2026-11-12-graphical-brief-render-check.json) records
hashes and comparisons. `make -C papers/infrastructure-audit/manuscript check`
passes: 22 supported/cited claims, six clean source-glyph checks and all
profile lint/reference audits. Those checks do not establish the semantics
of the missing NSB threshold or the calibration comparison; the SVG wording
was checked manually. No scientific analyses or production builds were rerun.
The makedoc figure-dependency fix remains a separate software task.

Next: Claude — revise the bounded claims and small label/layout residuals, then hand the package to Barry.
