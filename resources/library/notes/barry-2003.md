# Barry's 2003–04 papers of interest and EndNote libraries

Barry W. Brook compiled these materials in 2003–04, when the name EPRP was
already in use, as a record of the papers he found most promising for further
research in quantitative palaeontology. He shared them on 24 October 2026
with the main EPRP agents. They transcribed and interpreted the list:

- [the transcription](../../../literature/2003-brook-papers-of-interest.md);
- [Claude's reading](../../../ideas/2026-10-24-barry-2003-list-claude.md);
- [Codex's response](../../../ideas/2026-10-24-2003-interests-and-new-seeds-codex.md).

He shared them again with this side session on 25 October 2026: "I'd like
these properly catalogued herein, and ideally, to see how many of the pdfs of
these that we can pull in to our private collection on deep-server."

This note records the library's part:

- each entry resolved to a verified work;
- the EndNote libraries decoded, which the main agents had left unconverted;
- both added as seed tiers;
- the full texts fetched.

## The files

All are archived unchanged at
`deep-server:/data/paleodata/library/_provenance/barry-2003/original/`.
The decoded tables are in `…/decoded/`.

| File | Date | Contents | sha256 (first 16) |
| --- | --- | --- | --- |
| `eprp_old_papers_of_interest.docx` | (re-saved 2026) | the list: 293 papers in four groups (*Nature* 78, *Science* 137, *TREE* 66, other 12) | `95c7040d83faca78` |
| `EPRP - Papers Held.txt` | 7 Jan 2003 | RTF bibliography of 68 papers held, with abstracts | `9c93f350e0429b18` |
| `EPRP - Nature.enl` | 10 Jan 2003 | EndNote library, 36 records (31 distinct) | `ad276cc22b5451f5` |
| `EPRP - Papers and Books Held.enl` | 13 May 2004 | EndNote library, 236 records (217 distinct) | `89198780a8439f64` |
| `EPRP - To obtain [Mixed].enl` | 13 May 2004 | EndNote library, 116 records (113 distinct) | `84ef50cc857832b6` |
| `EPRP - Science.enl` | 24 May 2004 | EndNote library, 65 records (61 distinct) | `8fa84bd2cd9bad7b` |
| `EPRP - Body mass.enl` | 24 May 2004 | EndNote library, 90 records (90 distinct) | `3e715f73c81bbdb3` |
| `Benton - Quality of fossil record of vertebrates.mht` | 14 Jan 2003 | saved web page: the text of Benton (1998), *The quality of the fossil record of vertebrates* | `d753cad603363b6a` |

Full checksums are in [barry-2003/files.sha256](barry-2003/files.sha256).
They agree with those Codex recorded for the docx and the saved page.

## How the materials were read

- **The list and the RTF bibliography** were converted with pandoc (`pandoc -t
  plain --wrap=none eprp_old_papers_of_interest.docx -o list.txt`; `pandoc -f
  rtf -t plain --wrap=none "EPRP - Papers Held.txt" -o papers_held.txt`) and
  split into one citation per paragraph. The list keeps its group and item
  number, such as `Nature 32`, which match the transcription. The RTF's
  abstract paragraphs are skipped.
- **The EndNote libraries** are in the EndNote 5–8 binary format, which is
  undocumented. `barry-2003/enl_decode.py` reads them directly. Every field
  is stored as a tag (2 bytes), the field's length including its header
  (2), the string's length (2) and the string, in Mac Roman encoding, with
  padding. An edited field can carry spare allocated space.
  - Tags seen: 2 author, 3 year, 4 title, 5 pages, 6 journal or secondary
    title, 7 volume, 8 issue, 10 secondary author, 11 place, 12 publisher,
    15 keywords, 17 date, 18 abstract, 19 edition, 20 URL, 23 notes,
    24 ISBN or ISSN, 29 alternate journal, 30 accession number (Web of
    Science), 31 call number.
  - Every year field in this layout falls inside a decoded record. The 16-bit
    number at bytes 6–7 of the header is not a record count.
  - Some records appear more than once, as byte-identical copies (hence the
    distinct counts above). The build deduplicates them.
  - The files also hold about 65 stale copies of records in an older field
    layout, and five headless fragments. Our independent review checked
    them: every one duplicates a decoded record. The single exception, Beerling
    1998 in "To obtain", was decoded in "Papers and Books Held". It was
    probably moved between libraries.
  - `enl_decode.py FILE...` writes `FILE.records.json` beside each input.
- `barry-2003/build_citations.py` combines the three sources into one table
  of 904 citations: 293 from the list, 68 from the RTF, 543 from the EndNote
  libraries. It runs in a folder holding `list.txt`, `papers_held.txt` and
  `src/*.records.json`, all archived under `…/decoded/`.

## How they were resolved

`library.py match` (general; use it for any reference list) takes Crossref's
top five candidates for each citation, published within a year of the cited
one. Each candidate is scored on three agreements:

- **first author:** surnames folded to ASCII, with particles handled, so
  "Conway Morris" matches "Simon Conway Morris";
- **title:** a similarity of at least 0.85, or containment covering at least
  60% of the cited title, with a book's subtitle included;
- **volume and first page.**

The best-scoring candidate wins, and it is graded:

- **exact:** the author agrees with the title or with the volume and page;
  or the title, volume and page agree where no author is known.
- **probable:** the title, volume and page agree but the author does not;
  or the title agrees and no author is known; or the author and title agree
  but the cited volume and page conflict.

Three kinds of candidate are rejected:

- a title match whose first author differs, which is usually a review of
  the cited book;
- *Choice* reviews (DOI prefix 10.5860);
- errata, replies and comments, unless the citation is of that kind or the
  author, volume and page all agree.

Citations with no Crossref match get an OpenAlex title search graded the
same way, and rows that hit errors are retried once.

An independent review (a Claude Sonnet 5.5 subagent) checked all 856 exact
DOI matches of the first run against Crossref metadata and found five wrong,
an error rate of 0.6%:

- Chown & Gaston's 2000 *TREE* reply, three rows, had been resolved to the
  adjoining Storch letter;
- Steadman 1995, two rows, had been resolved to its erratum.

The fixes are a scoring tie-break, erratum and reply handling, name folding,
numeric volumes and book subtitles. A full re-run with the final rules
corrected those five. Against the first run, it changed nothing else except
three cases (`barry-2003/rematch-changes.txt` lists every changed row):

- an equivalent re-registered *Ecography* DOI;
- Gittleman et al.'s 2001 reply;
- Palmer's review.

The last two were then checked by hand.

Five resolutions were checked by hand (`barry-2003/manual.tsv`, seven rows,
with reasons):

- Hallam's 1994 *Nature* review of Glen's *The Mass-Extinction Debates* is
  `10.1038/372296a0`, "Theories in collision" (two rows).
- Palmer's 1997 review of Benton's *Vertebrate Palaeontology* is in
  *Nature*'s "At a glance" column, `10.1038/41263`, whose authors are Handy
  and Palmer (two rows).
- Gittleman, Gompper & Jones's 2001 *Science* reply has no DOI.
  `10.1126/science.292.5515.217b` is MacPhee & Flemming's letter it answers.
  OpenAlex holds the reply as W2742052218.
- Balmford 1996 in *TREE* is `10.1016/0169-5347(96)10026-4`.
- Raup's *Extinction: Bad Genes or Bad Luck?* is held in OpenAlex only as a
  *Choice* review stub, W1599898647, as in the canon.

| Grade | Citations |
| --- | ---: |
| exact | 892 |
| probable | 4 |
| unresolved | 8 |

The four probable rows are:

- Steadman 1995 (two rows). The cited records are the *Science* erratum
  notice (268, 625), and they resolve to the paper itself (267, 1123).
- Raup & Jablonski (eds), *Patterns and Processes in the History of Life*
  (1986), a book with no listed author.
- The Raup stub above.

The eight unresolved are books and chapters that neither Crossref nor
OpenAlex holds. They are in
[review/barry-2003-unresolved.tsv](../review/barry-2003-unresolved.tsv):

- Damuth & MacFadden (eds), *Body Size in Mammalian Paleobiology* (1990);
- Harper (ed.), *Numerical Palaeobiology* (1999), and three of its chapters
  (Carlson, Benton, Johnson & McCormick);
- Martin's "Prehistoric overkill: the global model" (1984);
- O'Connell's "An emu hunt" (2000);
- an Erwin-edited special issue on biotic recovery.

Benton's 1998 chapter, the saved web page, has no DOI or OpenAlex record
either. Its text survives in the archived page.

## The tiers

- **`barry-2003-list`**: all 293 list items, one row each, with its group
  and item number. They are 289 distinct works, because three multi-book
  reviews are listed once per book: Hallam's 1991 *Nature* review (two
  books), Ward's 1997 *Nature* review (three) and Russell's 1996 *Science*
  review (two).
- **`barry-2003-endnote`**: 493 distinct works from the five libraries and
  the RTF bibliography. Each row lists every library and item holding it.

The list is a subset of the libraries: all 289 of its works are held there.
Both tiers rank with the cited tiers for fetching. They carry no register
questions, because the list predates the registers; the main agents' notes
map its themes onto the questions.

Of the 289 list works, 75 (26%) were already in the library:

| Tier | List works |
| --- | ---: |
| canon | 27 |
| neighbours | 39 |
| cited by the repository | 22 |
| *Paleobiology* run | 5 |

Of the 493 library works, 138 (28%) were. Most of Barry's 2003 reading sits
outside what EPRP has cited so far.

## Full text

Three fetch passes on 25 October 2026 tried every route: open-access
locations, CORE, Semantic Scholar, Internet Archive public-domain scans and
Wiley text and data mining (TDM).

| Tier | Works | Open copy | Wiley TDM copy (mining only) | Covered |
| --- | ---: | ---: | ---: | ---: |
| `barry-2003-list` | 289 | 3 | 1 | 1.4% |
| `barry-2003-endnote` | 493 | 13 | 15 | 5.7% |

The gap is structural. Almost all of the list is *Science* (134 works without
a copy), *Nature* (74) and *TREE* (66), from 1985 to 2002. The libraries add
*PNAS* (48) and the Royal Society's *Proceedings B* and *Philosophical
Transactions B* (49). Little of this is open access. The library has no route
to AAAS, Springer Nature, the Royal Society or *PNAS*, and Elsevier's (for
*TREE*) awaits UTAS Library.

Four routes would close most of it:

- PDFs Barry kept from the time;
- Elsevier entitlement, already requested;
- UTAS text-and-data-mining arrangements with Springer Nature, AAAS, the
  Royal Society and *PNAS*;
- per-article requests through the library.

Current status per work is in [works.tsv](../works.tsv) (tiers
`barry-2003-*`, column `fulltext`).
