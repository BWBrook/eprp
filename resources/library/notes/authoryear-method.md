# Author-year citations without a DOI: extraction and resolution notes

Compiled 23 October 2026 by a Claude Sonnet 5.5 subagent, delegated by the Claude Opus 5.5 library session (Claude Code), over the repository's tracked Markdown at commit `4071bdd`. The exact and probable rows are `seeds/cited-authoryear.tsv`; the ambiguous and unresolved rows are `review/authoryear-unsettled.tsv`. The scout's working files, scripts and Crossref cache are archived read-only at `deep-server:/data/paleodata/library/_provenance/authoryear-20261023/`. Paths below are relative to that directory.
Output: `resolved.tsv` (434 rows). Companions: `new_to_harvest.tsv` (rows whose DOI the repo never writes), `other_ids.txt` (PMC/PubMed/arXiv ids in the repo), `review.txt` (per-citation candidate lists used in the manual pass), `overrides.py` (all 130 manual decisions with reasons).

## 1. Scope and extraction rules

- **Files scanned: 203** of the 259 tracked `.md` files: `ideas/` 89, `literature/` 62, `docs/` 16, and the 36 `data/**/README.md`.
  Not scanned (per brief): `papers/` (10), `resources/` (35), `logs/` (1), root `AGENTS/CLAUDE/README/STATUS`, and six non-README `data/` notes. A dry run over them found: `resources/` about 165 further author-year citations (data-source catalogue: mostly datasets such as "Austarch 2014"), root 2, data notes 3, `papers/` and `logs/` none. If dataset citations are wanted, `resources/` is the next tranche.
- **Blocks.** Each file is split into blocks: list item (with continuation lines), paragraph, table row, heading. Fenced code is skipped; inline code spans are blanked (they hold search queries such as `` `Rodland Bottjer 2001` ``); URLs are blanked before matching.
- **Citation forms matched** (regex in `extract.py`): `Smits 2015`, `Roy et al. 2009`, `Tamre & Parsons 2024`, `Lamyman, Fordham & Pearson 2026`, `Raup and Sepkoski (1982)`, possessives (`Alroy's 2002`, `Kim, Sheets & Mitchell's 2009`), name particles (`Van de Leemput`, `de Vos`, `ten Brink`), accents and hyphens, year suffixes (`2019a`), link-text years (`Peters's [2005 primary paper](url)`), continuations (`Close et al. 2017, 2019 and 2020`, `Alroy 2008/2014/2015`), and journal-year lists (`Fenton et al. 2023 Nature; 2016 Phil Trans B`).
  Formal reference lists (`Gutarra, S. et al. (2024)`, `[3] Minsky, C., Wordsworth, R., ... (2026)`, `22. **Couvert, É. et al. (2024).**`): 96 occurrences, almost all in the GPT-6 Pro consultation documents.
- **DOI skip rule.** DOIs are found in each block (including `10.xxxx/...(2000)26[74:...]2.0.co;2` legacy forms and link-reference definitions `[7]: https://doi.org/...`). Each DOI is paired 1:1 with the nearest citation in the same block, preferring the citation that precedes it (a DOI before a citation costs +8 characters of distance); table rows and formal references have no distance limit, other blocks 400 characters. Paired citations are skipped. A bullet such as "Smits 2015, Tamre & Parsons 2024 and Roy et al. 2009 (doi)" therefore keeps the two unpaired citations. Skipped citations are not lost: their DOI is used as a hint (section 3).
- **Hand supplement (36 items).** `ideas/2026-10-23-alroy-provocation-claude.md` cites about 25 Alroy papers only as `(2008 PNAS, 2010 Science ...)`, quoted titles, or "John's 2018"; plus Pradel 1996, Pledger 2003 (possessive/title forms) and Raup 1967 (bare year after a semicolon). They are in `supplement.py`. Alroy items carry a journal tag so that same-year papers (2008 PNAS vs Science; 2001 PNAS vs Science) stay separate rows.
- **Deduplication key:** normalised first-author surname (accents stripped, particles dropped) + year + suffix; mentions with named co-authors cluster by subset compatibility; bare mentions attach to the best-matching cluster. Supplement items with a journal tag are separate clusters.
- **Question ids.** Spec rule (enclosing `### Q-/B-` section in the two registers; `q012`/`b003` tokens in file or directory names) plus three extensions: the nearest enclosing heading that names a Q-/B- id in any file, ids named in the same table row (any file), and ids named in the same bullet/paragraph in non-register files. 338 of 434 rows have ids (58 distinct ids); the rest cite from notes with no id (mostly `docs/review/**`).

## 2. Counts at each stage

| Stage | Count |
|---|---|
| Naive regex survey, distinct strings (incl. months etc.) | 1,019 |
| Citation occurrences after filters | 2,222 |
| ... skipped (DOI in same bullet/row/sentence) | 1,406 |
| ... kept | 816 (+36 hand-supplement items) |
| Unique (surname, year) keys overall | 746 |
| ... only ever DOI-adjacent (skipped) | 341 |
| ... with at least one DOI-free mention | 405 |
| Clusters after variants, distinct same-year works, supplement | 435 |
| Dropped as false positive | 1 (`Smith & Alroy 2014`, parse artefact of "Chisholm, Solow & Smith and Alroy 2014") |
| **Rows in `resolved.tsv`** | **434** |
| Citing files represented | 97 (849 file:line locations, all checked to contain the surname within -4/+2 lines) |

Final grades: **exact 368, probable 44, ambiguous 11, unresolved 11.** 420 rows carry a DOI; 417 of those also an OpenAlex id (3 DOIs are legacy bracket forms OpenAlex stores differently: Alroy 2000, Foote 1999, Foote 2000); 3 rows have an OpenAlex id and no DOI (works without DOIs: Alroy 2004 EER, Raup 1966, Raup 1967).
**345 of the 420 resolved DOIs are already written elsewhere in the repo** (note flag `doi_in_repo`); only **75 rows add a DOI the harvest does not have** (`new_to_harvest.tsv`).

## 3. Resolution method (what was actually done)

Budget changes mid-task (OpenAlex shares about 1,000 credits/day per IP, a key needs an email) set the design. No email, key, `mailto=` or contact header was sent anywhere; the User-Agent is `eprp-library-seed/0.1 (research-library harvest)`.

1. **Candidate discovery: Crossref** (public pool, 0.27 s spacing). Three queries per citation (author + topic words; bibliographic string; exact-year author + palaeo-domain words), then a fourth author-only pass (100 rows) for the 186 weakest. Topic words come from the citing context and the deepest heading.
2. **Local scoring** (`score.py`): first-author surname +5 (+4.5 for the Alroy-corpus items, where he is often a co-author); named co-authors +1.5 each / -1.5 if absent; year exact +3, +-1 +0.5, else -3; palaeo/ecology domain terms in title or journal +0.5..+3, none -3; idf-weighted overlap with the citing context up to +6; journal tag match +2.5 / mismatch -1; preprint -1; erratum/comment/peer-review/dataset penalties; "et al." with two or fewer authors -1..-2. Same-title and near-same-title (Jaccard >= 0.6, same first author) records are collapsed; the published version is preferred and the preprint noted.
3. **Repo DOI hints.** For each citation also written with a DOI elsewhere, the paired DOI(s) became candidates (+4), scored with OpenAlex metadata. This settled most bare citations and corrected several automatic picks (e.g. Aronson et al. 2009, Pradel 1996).
4. **Manual review of all 435 clusters** (`review.txt`): 130 overrides in `overrides.py`, each with its reason. Auto-to-final grade moves: 295 exact kept, 39 probable->exact, 31 ambiguous->exact, 22 ambiguous->probable, 6 ambiguous->unresolved, 4 probable->unresolved, 4 exact->probable, 3 unresolved->exact (OpenAlex), others unchanged. Decisions rest on the API records shown plus the citing context; none uses recall of the literature. One identity was confirmed independently: Newcombe 1998 via the PubMed id in the citing line (NCBI esummary).
5. **OpenAlex.** 385+2 hint DOIs and 163+1 final DOIs by `filter=doi:a|b|...` (50 per request, 1 credit). Ten author+year filter queries (`raw_author_name.search`) for citations Crossref missed; **these cost 10 credits each, not 1**, so I stopped there (about 177 credits were left at last check; shared with another agent). They found Alroy 2004 (EER, no DOI), Bailer-Jones 2011 (MNRAS), Seton et al. 2012, Dieselhorst & Stadler 2026 (arXiv), Raup 1966/1967 (no DOI); nothing for Mayhew 2008, Guedes 2025, Brusca & Brusca 2003. Semantic Scholar returned HTTP 429 immediately and was not used.

Grade meaning used: **exact** = author, year and topic agree and the match was checked against title words, journal tag, a quoted title/URL slug, a repo DOI hint or a PubMed id; **probable** = one strong candidate with a stated doubt; **ambiguous** = two or more live candidates (top pick is still in `doi`/`openalex_id`, alternatives in `note`, at most three); **unresolved** = no accepted record (columns blank; reason in `note`).

## 4. False-positive patterns excluded

Month + year (339 hits in the naive survey: "October 2026", "May 2025"); function words before a year ("The 2018", "Their 2025", "Its 1997"); ALL-CAPS abbreviations ("PNAS 2020", "GSA 2021", "GCA 2020", "TPP 2019", "GTS2020", "ICS 2024"); journal or section words ("Science, 2010", "Adv, 2025", "Electronica 2025"); dates (`2026-10-14`) and year ranges (`2022-2026`, `2023-2026`); `Q-`/`B-` ids and "76/1750"-style board message numbers; data-vintage years ("2017 extract", "the 2023 update"); repo, tool and model names (`MitchellManica2026`, `SCION_Xu2025`, `GTS2012`); programme labels (Claude, Codex, Fable, Phase, Round); inline code (search queries); "John's 2018" (first-name possessive for Alroy, folded into the supplement). Anonymous year-only references with no author cannot be resolved and are excluded: "PNAS 2020 Fe/S hysteresis", "GCA 2020", "the 2018 paper" (B-004 notes), "a 2025 ostracod study", "a 2022 bryozoan comparison", "Community energy use (2022-2025)" (Alroy row).

## 5. Data-quality problems and cautions

- **Shorthand covering several works** (one cluster, one row): `Buatois and Bubphamanee 2025` = two PNAS papers (both DOIs written in the same file; row ambiguous), `Lau 2016/2017`, `Foote 1994/2000/2005`, `Alroy 2008/2014/2015`, `Mayhew 2008/2012`, `Close et al. 2017, 2019 and 2020`. For ambiguous rows, adding every listed alternative is safe.
- **Same surname-year, different works in different files** merge into one cluster: Smits & Finnegan 2019 (two papers), Cribb 2023 and Zhang 2025 (resolved to the paper the DOI-free mentions mean; a second same-year paper is DOI-cited elsewhere), Raup 1991 (book vs kill-curve paper), Silvestro 2019, Alroy 2010/2014/2016.
- **Online-first vs issue year**: 24 resolved rows differ by one year from the citation (e.g. Burthe 2016/2015, Callaway & Sant'Anna 2021/2020, Truman 2025/2024); flagged in `note`.
- **Not DOI-bearing works**: Alroy 2004 (EER) and Raup 1966/1967 have OpenAlex ids only; Krug, Congreve & Patzkowsky 2015 is a conference abstract (related PLoS ONE paper named in note); Brusca & Brusca 2003 (textbook), Huber 2010 (monograph), Padfield 2018 (Dryad archive) are unresolved.
- **Preprints**: Kerr et al. 2024 (ESS Open Archive; published as Kerr et al. 2025, separate row), Tikhonov 2026, McElwain 2026, Strona & Bradshaw 2026, Beaulieu & O'Meara 2026, Liao 2025, Dieselhorst & Stadler 2026. Several use the new openRxiv prefix `10.64898`, which Crossref and OpenAlex already index.
- **Dataset DOIs** can win over papers when the repo cites the deposit (Bolton 2018 PANGAEA); the note says so. Alroy 2026 (title-only) points to the Oikos paper, not the Dryad dataset.
- **First-author column** holds the resolved record's first author, which is not Alroy for his co-authored Scholar items (Bowen 2002, Madin 2006, Benson 2016, Close 2018/2019).
- **Unresolved (11):** Alroy 1998 [equilibrial], Betancourt 2016 (Stan/arXiv), Brusca & Brusca 2003, Du 2025, Guedes et al. 2025, Huber 2010, Krug et al. 2015 (abstract), Lau 2017, Ma, Vermeij & Grosberg 2010, Mayhew et al. 2008, Padfield 2018. Du, Lau 2017, Ma and Huber have common surnames and no topical cue; they would need a keyed OpenAlex run or the source note's author.
- **Limits of the check**: Crossref candidate recall is imperfect for off-domain works (Bailer-Jones, Seton surfaced only through OpenAlex). Some "exact" rows rest on a unique author-year-domain match plus a repo DOI hint rather than a title confirmation; the weakest are bare names with no context (e.g. `Du 2025` was refused, `Rothman 2017` accepted on title fit).
- `doi_in_repo` compares against all DOIs found in the 259 tracked Markdown files with the same regex; legacy bracket/angle-bracket DOI spellings may be missed, giving a few false "new" DOIs.
- Non-DOI identifiers in the repo, not covered by either harvest: 26 PMC ids, 9 PubMed urls, 3 arXiv ids (`other_ids.txt`).

## 6. Pipeline (all in this directory)

`extract.py` (blocks, citations, DOI pairing) -> `cluster.py` (+ `supplement.py`) -> `fetch_crossref.py`, `fetch_crossref2.py` -> `grade.py` (scores in `score.py`, helpers in `common.py`; repo-DOI hints from `oa_hints.json` via `openalex_lookup.py`) -> `assign.py` (auto grades, `review.txt`) -> `overrides.py` (manual) -> `assemble.py collect|build` -> `resolved.tsv`. QC scripts: `qc1/2/3.py`, `check_final.py`, `check_authors.py`, `check_lines.py`, `final_stats.py`. `oa_fallback.py` is the 10-query OpenAlex author-year pass; `cache/` holds raw Crossref responses.
