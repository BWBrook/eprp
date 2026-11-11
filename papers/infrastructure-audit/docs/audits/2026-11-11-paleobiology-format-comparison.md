# Paleobiology format comparison for the infrastructure-audit paper

Date: 2026-11-11. Compared: `papers/infrastructure-audit/manuscript/text/main.md` (3,864 words incl. tables; 9-page PDF; supplement 831 words) against four recent Paleobiology research articles and one review. Estimands constraints respected: no suggested change adds prevalence, causal or downstream-effect claims.

## 1. Bottom line (ranked)

1. **AI systems are listed as authors, which the journal forbids.** Instructions: AI tools cannot be authors; use of AI for text generation, data analysis or figures must be declared with tool name, version, dates of use, how to access it and a full description, placed in the acknowledgments (text), the methods (analysis) and figure captions (images). Our byline lists "Claude (Anthropic) and OpenAI Codex" as an author entry. Move them to a methods-level AI-use statement and acknowledgments; Barry becomes sole author (or add human co-authors who meet authorship norms).
2. **Required statements and front matter are missing or non-conforming.** No Competing Interests statement (required in the main file), no Acknowledgments or Funding, no Non-technical Summary (present in all four research articles read), and an abstract of about 298 words with a bullet list (the four comparators sit at 249-250 words in a single paragraph). Spelling is British ("palaeobiology"); the journal requires American English.
3. **Structure reads as a report, not a Paleobiology article.** Numbered headings; a stranded "Methods in brief" after Conclusions that only points to the supplement; Recommendations placed as a numbered section before the Discussion; the agents' errors as a stand-alone section; Introduction that ends without aims or questions. Comparators run Introduction, Methods, Results, Discussion (Conclusions), then statements, with unnumbered headings.
4. **No figures.** Comparators carry 2-11 figures (a 12-case quantitative series with a real curve in case 9 invites at least 3-4). Display-item balance is the biggest readership gap.
5. **Data and code availability is a bare GitHub URL.** Journal wants data and code in a stable public repository (Zenodo/Dryad, journal pays) cited in the Data Availability Statement. All four comparators cite a DOI. We need a tagged release with a Zenodo DOI, and a plain statement of which inputs are not redistributed.

Premise check: the type fit needs deciding. Paleobiology's types are Research Article, Rapid Communication, On the Record, Review, Methodological Advances, Invited, Comment/Reply (there is no "Matters of the Record"). Methodological Advances is described as usually submitted as a Research Article with an in-depth case study; we propose no method. **On the Record** (about 2,500-3,500 words, at most 2 figures/tables, 5-7 printed pages) matches a short case series, but would force cutting to roughly four to five cases. A Research Article of at most 8,500 words (15 figures/tables) fits the current twelve. Scope is also a risk: the journal wants broad biological or paleobiological process and pattern, and an infrastructure audit is nearer to data-quality and sampling bias (the comparators' theme). The journal accepts pre-submission inquiries (title page and abstract); that is outward-facing, so Barry's decision.

## 2. Comparison table

Approximate counts. Body words include captions and figure text, so they overstate prose by about 10-20%. BQ copy is the accepted manuscript (review layout, 113 pp), so its length is not comparable.

| Attribute | 1. Chupongstimun (10090) | 2. Andréoletti et al. (10094) | 3. Crestohl & Bush (10106) | 4. MacFadden et al. (10084) | 5. Smith et al. Big Questions (10042) | Ours |
|---|---|---|---|---|---|---|
| Type label | Article | Rapid Communication | Article | Methodological Advances | Review | none (internal draft) |
| Length | 11 pp; ~7.7k body words | 9 pp; ~5.6k | 12 pp; ~6.6k | 17 pp; ~10k | ~24 pp published (113 pp review copy) | 9 pp; ~3.9k + 0.8k supp |
| Abstract | 250 words, one paragraph, qualitative | 249, one paragraph, quantitative (37% unexplained; "nearly a third") | 250, one paragraph, some numbers (7000+ occurrences; <9-14 mm) | 249, one paragraph, quantitative (93.4%, ~99%) | ~300, one paragraph | ~298 incl. 11-bullet list; numbers in bullets |
| Non-technical Summary | yes (~140) | yes (~330) | yes (~270) | yes (~310) | not seen in manuscript copy | none |
| Section order | Intro (with Background) / Methods / Results / Discussion and Conclusions | Intro / Materials and Methods / Results / Discussion / Conclusion | Intro / Materials and Methods / Results / Discussion / Conclusions | Intro / Materials and Methods / Results / Discussion / Conclusions and Significance / Future Research | Intro / Methods / 11 theme sections / Concluding remarks | 1 Intro / 2 Finding-choosing-checking / 3 Cases / 4 Agent errors / 5 Recommendations / 6 Discussion / 7 Conclusions / Methods in brief / Roles / Data and code |
| Methods | main text, before Results, subsectioned (data, simulation, correction) | main text, before Results | main text, before Results, subsectioned | main text, long (model, imaging, stats) | main text, before results | Section 2 (~600 words) before cases, plus detail in supplement S1-S2; stub "Methods in brief" at end |
| Figures / tables | 5 / 0 | 2 / 0 | 10 / 0 | 11 / 2 | 3 / 13 | 0 / 2 |
| Figure roles | simulation line plots, histogram, empirical trajectories | comparison and time-series plots, effect-size summary | trend plot, map, specimen photos, heat-map-style taphocube, histograms | specimen photos, performance box plots, loss curves, confusion matrices, saliency maps | flowchart of the question pathway, assignment network, concept figure; tables list questions | none; Table 1 case list, Table 2 assumptions |
| Introduction ending | explicit statement of the three biases and the approach for each | explicit aims, in order, with the validation step | numbered aims (1)(2), plus test-of-approach question | stated purpose, predictions in Methods/Results | rationale for the project | "aim is not a rate or a ranking"; no questions |
| Voice, tense | first person singular, past/present mix | "we", past | "we", past | "we", past | "we", past | "we", past; matches |
| Discussion | subheadings in 2 of 4; limits and future work embedded; combined with conclusions in paper 1 | subheadings (e.g. sampling along lifetimes, multiple drivers) | subheadings plus "Implications for Diversity Analysis" | subheadings, overfitting, future research | thematic synthesis | 6.1-6.3 with an assumptions table; Recommendations separate |
| Conclusions | merged / short / short / extended / "Concluding remarks" | yes | yes | yes, with significance | yes | yes (short) |
| Data/code statement | DOI (Zenodo) for data, code, supplement | GitHub code plus OSF DOI for supplement and archived code | Dryad DOI plus two Zenodo DOIs | Zenodo images, GitHub code (licence stated), Dryad supplement | Zenodo DOI for supplement | GitHub URL; inputs partly retained locally, not redistributed |
| Statements | Acknowledgments, Competing Interests, Data | Acknowledgments with funding, Author Contribution, Competing, Data | Acknowledgments, Competing, Data | Acknowledgments with funding, Competing, Data | Acknowledgments with funding, Competing, Data | Roles of AI and humans; no acknowledgments, funding, competing interests |
| AI-use statement | none seen (not on topic) | none seen | none seen | none seen despite ML subject (software described in Methods) | none seen | partial: names and some versions; no dates, access, tool descriptions |
| References | ~37, author-year, "Literature Cited" | ~58 | ~67 | ~37 | several hundred | ~14, Chicago author-date, full given names, DOIs |
| Supplement | Zenodo (data, code, supplement) | OSF (supplement, code archive) | Dryad plus Zenodo (data, R script, tables) | Dryad (and GitHub) | Zenodo (raw and preliminary questions) | 4-page supplement (S1 selection, S2 replay, S3 withdrawn statements, S4 reproduction) |

## 3. Incongruities and suggested changes

**A. AI as author and AI-use disclosure.** We list the agents in the byline and describe their roles in a final section. Journal: AI cannot be authors; disclose with name, version, dates, access and description, split across methods, acknowledgments and captions. Matters because it is a policy violation that could cause desk return, and Barry wants full disclosure. Change: sole human byline; a "Use of AI systems" paragraph in Methods (analysis and audit roles; versions, date range, how accessed) and an Acknowledgments sentence for drafting and review; keep the roles list (condense) and the correspondence-snapshot pointer. Version strings need verifying against the logs; the draft names "Opus 5.5" and "GPT-6.1 Sol" but gives no date range and leaves Sonnet subagents unversioned.

**B. Abstract and Non-technical Summary.** 298 words and bullets versus about 250, single paragraph. Cut to 250, fold the bullets into two sentences with two or three headline numbers, and write a 150-300-word Non-technical Summary from the two-page brief (already a repo product). Keep abstract wording within estimands.md allowed forms.

**C. Spelling and style.** British forms throughout (palaeobiology, palaeolatitude, palaeontology). Switch to American English, including title and the section 3 wording. Drop numbered headings and the "With receipts:" title; use a descriptive title with a colon subtitle like the comparators. Remove the "Internal research draft" note before submission.

**D. Missing required statements.** Add Acknowledgments, Funding (state none or the grant), Competing Interests (required in the main file, "none" if none), Author Contributions (optional in the sample but common). ORCID for the corresponding author at submission.

**E. Section order and orphan sections.** Delete "Methods in brief" (the stub adds nothing). Move section 4 content into Results (after the cases, as "Corrections during replay") with the limitation sentence in Discussion. Fold section 5 Recommendations into Discussion as one "Implications" subsection, prose rather than bullets (comparator 3 does this). Keep Conclusions short. Convert Table 2 to a "Limitations" paragraph; the journal's 15-item allowance is not the issue, but no comparator uses an assumptions matrix.

**F. Introduction does not state aims.** Comparators end with explicit aims or questions. Add two or three, in estimands-safe form: what kinds of problem did systematic replay expose in one programme; what does each change in an analysis someone plausibly runs; what did replay withdraw. Do not frame as a rate.

**G. No figures.** Candidates: (1) layered schematic, database to age to palaeolatitude to rate, with the twelve cases located on it (conceptual, opens Section 3); (2) pipeline flowchart, 189 candidates to 12 cases, replay by different actor, withdrawals (replaces much of Section 2 prose and is parallel to the BQ flowchart); (3) quantitative panel from cases 2, 5 and 9: interval-age changes by snapshot bracket, age-conversion error against depth, palaeolatitude spread against age 10-400 Ma (a real curve, 2.9 to 13.6 degrees); (4) case 7 coverage plot with retained controls. Total at most 4 figures plus Table 1; Table 2 removed. Every figure needs alt text (WCAG 2.1 AA), and the replay commands should appear in captions or data availability.

**H. Methods depth.** Comparators give 1,500-3,000 words of Methods with subheadings. Ours is about 600 words and defers to the supplement. Expand Section 2 into Methods with subheadings (Candidate sources, Case selection rules, Replay and independence, Claims ledger, Use of AI systems) and keep S1-S4 as supplement. The "independence is check-specific" caveat belongs here.

**I. Data and code availability.** Requires data, code and software in a stable public repository, accessible at review, with FAIR practice. Do: tag a release with a Zenodo DOI (journal covers Zenodo costs), cite it, state licences, and state exactly which inputs are retained locally and not redistributed. Do not claim a public rebuild (not validated; estimands "Not allowed").

**J. References.** 14 entries against 37-67; style is author-year Chicago with full given names, while the journal uses initials and volume:pages without DOI links in the list. Check the CSL repository for a Paleobiology style (not verified here) and switch. The reference count is thin for a paper about palaeobiological infrastructure: cite the cases' primary literature and the sampling-bias papers the comparators cite (PBDB, Triton, time scale and plate-model sources), verified through DOI metadata.

**K. Scope and type.** See premise check above. If scope is doubtful, the pre-submission inquiry costs one title and abstract but is Barry's call.

**L. Supplement.** The journal's supplementary material must be non-essential to understanding the article and is not typeset. Our supplement carries S2 (per-case replay) and S3 (withdrawn statements), which the text relies on; S3 is partly duplicated in Section 4. Keep S1-S2 and S4 in the supplement, host on Zenodo, and ensure the main text stands alone.

## 4. Sources

Fetch date for author instructions: 2026-11-11.

- Instructions for contributors (article types, scope): https://www.cambridge.org/core/journals/paleobiology/information/instructions-contributors
- Preparing your materials (types and limits, figures, data, AI, competing interests): https://www.cambridge.org/core/journals/paleobiology/information/author-instructions/preparing-your-materials
- Submitting your materials: https://www.cambridge.org/core/journals/paleobiology/information/author-instructions/submitting-your-materials (logistics only)
- Research transparency page: no substantive text. The abstract limit, Non-technical Summary rule, reference style and funding-statement rule were not on any fetched page (they sit in the linked style guide and file-requirements documents); the 250-word abstract limit and the Non-technical Summary are inferred from the four research articles.

Articles read from the library (nectar `/data/codex/paleodata/library/pdf/`, copied read-only to the session scratchpad, text via `pdftotext`):

| DOI | Library file | Copy |
|---|---|---|
| 10.1017/pab.2025.10090 | W7127050957.pdf | published version, CC BY |
| 10.1017/pab.2026.10094 | W7140890541.pdf | published version, CC BY |
| 10.1017/pab.2026.10106 | W7171633830.pdf | published version, CC BY |
| 10.1017/pab.2025.10084 | W7126258625.pdf | published version, CC BY-NC-ND |
| 10.1017/pab.2025.10042 | W4414545731.pdf | accepted manuscript (review layout, 113 pp), CC BY, via institutional repository |

No substitutions made. Caveats: reference and word counts are regex-based estimates (references plus or minus 5); paper 5's published page count is taken from our own reference entry (51(3): 408-31); Non-technical Summary presence in paper 5 not established from the manuscript copy.
