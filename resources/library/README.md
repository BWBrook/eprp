# Literature library

A growing, indexed collection of the scientific literature in quantitative and
theoretical palaeobiology, from its roots to current work. EPRP holds
metadata for every work it knows of, and full text where an open copy exists,
so the agents can search and read the literature locally. The library serves
the question registers, the [data-source catalogue](../sources/README.md) and
the package inventory. What it turns up may also reshape existing questions or
suggest new ones.

The library follows [the evidence conventions](../../docs/evidence.md). Holding
a work is not a judgment of its quality or of its relevance to a question.

## Layout

```text
resources/library/
  README.md               this file: conventions, tiers, access policy, lessons
  library.py              harvest | resolve | expand | frontier | journal | match | fetch | import-staged | ocr | verify-embedded | reject-incomplete | withdraw | index | textindex | search
  elsevier.py             restricted XML fetch | approval-gated, DOI-attributed query
  mine_elsevier.py         private agenda-question candidates and keyword themes
  seeds/<tier>.tsv        seed lists, one file per tier; rows give openalex_id, doi or pmid
  topics.md               the canon's topic tree (ids such as extinction/selectivity)
  notes/                  method records for curated tiers (canon, author-year seeds, Barry's 2003 materials with their build scripts) and source notes (the community's Big Questions, 2025; published question lists and agendas)
  review/                 candidates held back from the seeds: unsettled citations, canon reserve and unverified
  works.tsv               generated: one row per resolved work, with tiers, questions and full-text status
  INDEX.md                generated: counts by tier, full-text status, type, decade and venue
  by-question.md          generated: cited works grouped by question (Q-, B-) and catalogue entry (src:)
  duplicates.tsv          generated: OpenAlex records merged as duplicates of one work
  unresolved.tsv          generated: seed rows that did not resolve to an OpenAlex work
  eprp-library-README.md  installed as /data/paleodata/library/README.md
```

The canonical open/Wiley store moved to
`nectar:/data/codex/paleodata/library` on 30 October 2026. The retained
`deep:/data/paleodata/library` copy is historical. Use an explicit `--store`
with `library.py`; its old default has not followed the migration. The layout
below is relative to the chosen store:

```text
STORE/
  openalex/<W>.json       full OpenAlex record: metadata, abstract index, references, locations
  pdf/<W>.pdf             open-access full text, read-only
  text/<W>.txt            pdftotext output of pdf/<W>.pdf (derived; rebuildable)
  ocr/<W>.txt             searchable machine OCR of a scan, kept separately from the original extraction
  ocr/<W>.json            source and OCR hashes, engine, page coverage and other provenance
  quarantine/             PDFs whose first pages did not contain the work's title
  quarantine/rejected/    files verified to be incomplete or not the work; retained with their history
  quarantine/withdrawn/   copies removed by `withdraw`, with the reason in manifest.tsv
  tdm/<publisher>/pdf/    publisher text-and-data-mining copies (local search and mining only; see below)
  tdm/<publisher>/text/   their extracted text
  manifest.tsv            append-only: one row per stored or withdrawn copy, with its path; the latest row per work counts
  attempts.tsv            append-only: every download attempt and Semantic Scholar lookup, with its outcome
  aliases.tsv             seed key (doi:…, pmid:… or merged W id) to OpenAlex id
  unresolved-keys.tsv     seed keys OpenAlex lacks: Crossref-only, invalid or deleted
  _tools/                 the deployed library.py and seeds/
  _provenance/            read-only working files, scripts and API caches of the curated tiers
  search.sqlite           full-text search index of titles, abstracts and open texts (`textindex`; rebuildable)
  tdm/search-tdm.sqlite   contentless search index of TDM texts (no readable text; rebuildable)
  frontier-counts-*.tsv   every post-SINCE citer of the core, with its count of core references (`frontier`)
```

Elsevier subscription material has a separate, campus-only store at
`deep:/data/codex/paleodata/elsevier-library`. Its `catalogue.tsv` is a dated
metadata snapshot; all XML, extracted text, retrieval manifests, excerpt
accounting, question candidates and private approval records live beneath
`tdm/elsevier/`. This store does not change the canonical open/Wiley manifest.
Do not copy it to Nectar. The [5 November acquisition record](notes/2026-11-05-elsevier-acquisition.md)
gives the run, resumption and evidence boundaries.

`W` is the OpenAlex work id, the library's primary key. It covers works without
DOIs, including many books and pre-1990 papers. A seed resolves to the work
OpenAlex holds for it, after OpenAlex's own merges. A dataset version DOI
resolves to the deposit's concept record, and a preprint to its published
version. An old *Paleobiology* SICI resolves to its Cambridge reissue, and
occasionally a Dryad DOI resolves to the article it supports.

## Tiers: how the library grows

The library grows outward in rings, from the works EPRP already uses to the
whole field. Each ring has explicit membership rules, so its contents can be
rebuilt.

| Tier | Seed file | Membership |
| --- | --- | --- |
| `cited-ids` | `seeds/cited-ids.tsv` | every DOI (as written, including SICI forms), PMC, PubMed and arXiv id in a tracked text file (`library.py harvest`) |
| `cited-authoryear` | `seeds/cited-authoryear.tsv` | author–year citations in the registers and notes, resolved and graded `exact` or `probable` ([method](notes/authoryear-method.md)) |
| `canon` | `seeds/canon.tsv` | curated foundational and landmark works, from the 1830s to 2026, under the [topic tree](topics.md) ([method](notes/canon-method.md)) |
| `neighbours` | `seeds/neighbours.tsv` | works that at least 5 core works reference (`library.py expand`), with that count and the questions of the referencing works |
| `frontier` | `seeds/frontier.tsv` | works published since 2020 that cite at least 5 core works (`library.py frontier`), with that count and the questions of the works they cite |
| `agendas` | `seeds/agendas.tsv` | published question lists and research agendas: priority-question exercises, horizon scans, grand challenges, *Paleobiology*'s 50th-anniversary issue, and palaeontology reviews with question boxes ([note](notes/question-agendas.md)) |
| `barry-2003-list` | `seeds/barry-2003-list.tsv` | the 293 papers on Barry's 2003 list of the most promising papers for further research, with their group and item numbers ([note](notes/barry-2003.md)) |
| `barry-2003-endnote` | `seeds/barry-2003-endnote.tsv` | the 491 distinct works in his 2003–04 EndNote libraries and "Papers Held" bibliography, decoded and resolved ([note](notes/barry-2003.md)) |
| `field-<journal>` | `seeds/field-<journal>.tsv` | a core journal's complete run as OpenAlex lists it (`library.py journal ISSN --name NAME`); see below |

The journal runs so far (metadata, abstracts and reference lists; open full
text fetched for *Paleobiology* only):

| Tier | Journal (ISSN) | Works | Years | Added |
| --- | --- | ---: | --- | --- |
| `field-paleobiology` | *Paleobiology* (0094-8373) | 2,584 | 1975–2026 | 24 Oct 2026 |
| `field-journal-of-paleontology` | *Journal of Paleontology* (0022-3360) | 10,274 | 1927–2026 | 25 Oct 2026 |
| `field-lethaia` | *Lethaia* (0024-1164) | 2,875 | 1968–2026 | 25 Oct 2026 |
| `field-palaios` | *PALAIOS* (0883-1351) | 2,500 | 1986–2026 | 25 Oct 2026 |
| `field-palaeontology` | *Palaeontology* (0031-0239) | 2,045 | 1999–2026 (84 earlier) | 25 Oct 2026 |
| `field-papers-in-palaeontology` | *Papers in Palaeontology* (2056-2802) | 682 | 2014–2026 | 25 Oct 2026 |

OpenAlex lacks *Palaeontology* before 2000. The Palaeontological Association
hosts that archive itself, so it needs its own route. Of the *Journal of
Paleontology* run, 4,445 works (mostly before the 1990s) have no DOI.

A work belongs to every tier that names it. The **core** is the cited tiers
plus the canon. The two rings grow from the core alone:

- **neighbours:** older works the core leans on;
- **frontier:** newer works that build on it.

Other tiers, such as journal runs and Barry's 2003 materials, add works
without reshaping the rings. `fetch` tries works in tier order:

1. the cited tiers and Barry's 2003 tiers;
2. the canon;
3. neighbours and frontier, by reference count;
4. field tiers.

Field tiers are fetched only when named (`fetch --tier field-paleobiology`).
`frontier-counts-<since>.tsv` in the store keeps every citer's count of core
references. It is written after each batch, as `.partial` until complete.
`frontier --reuse --min-refs K` re-thresholds it without new queries.

**Duplicate records.** OpenAlex sometimes holds one work under several ids:
a book and its book-review stub, two scans of one edition, or a preprint and
its published version under one title. `index` and `fetch` merge records that
meet three conditions:

- both are text works, so never a paper and its own data or code deposit;
- their full titles and first-author surnames agree, ignoring suffixes such
  as "Jr.";
- they share a publication year. A book-review or paratext stub instead joins
  the same-titled record nearest its year, within two years.

Different editions, and same-titled works from different years such as
Jablonski 1994 and 1995, stay separate. The canonical record is one with a
held copy, then a non-stub, then one with a DOI, then the most cited. `fetch`
tries one record per work. `works.tsv` lists the
merged ids in its `merged` column, and `duplicates.tsv` lists each merge.
Questions come from the citing context. In the registers, that is the
enclosing `### Q-NNN` or `### B-NNN` section. Elsewhere, it is a `q012`/`b003`
token in the path or a `resources/sources/<id>/` directory. `works.tsv` and
`by-question.md` carry the cited tiers' questions only. Questions inherited by
neighbours and frontier works stay in their seed files, as leads rather than
citations.
Canon works carry a topic id from the topic tree.

The `review/` lists hold candidates that are not yet seeds:

- author–year citations graded `ambiguous` or `unresolved`;
- the canon scout's 340 verified but unselected works;
- its 13 works that OpenAlex and Crossref could not confirm.

To promote a work, add it to a seed file with its reason.

Rerun `harvest` and `resolve` whenever the registers, notes or catalogue
cite new works. Rerun `expand` and `frontier` after the cited tiers or the
canon change.

When the neighbours ring was last built (24 October 2026, from all non-ring
tiers then present: the cited tiers and the canon), it held about 2,100 works
at 5 references, about 5,500 at 3 and about 800 at 8. "Neighbours" means
works the core references, so a few are recent.

## Access policy

- **Full text comes only from open copies.** The fetcher tries four kinds of
  source:
  - locations OpenAlex marks open access, from Unpaywall's checks made off
    any campus network (publisher, repository or preprint server);
  - the PubMed Central open-access subset, through its public AWS bucket;
  - PDF links on those locations' landing pages (`citation_pdf_url`, or a file
    link on the same host);
  - the original repository links CORE records for a DOI (used once a CORE
    key is installed; paced at 10 requests a minute);
  - Semantic Scholar's open-access link;
  - for works published 96 or more years ago (1930 or earlier in 2026), which
    are public domain in the US: unrestricted Internet Archive scans.
    - Scans are matched on title words, first author and year within one,
      never past that cutoff.
    - The title check reads their first 15 pages, because scans carry front
      matter.
    - Excluded: lending copies (`access-restricted-item`, or an LCP DRM
      identifier); items with an ISBN, a date or a title year after the
      cutoff, which are modern reprints.
    - The Biodiversity Heritage Library's own site refuses scripts, but its
      scans are mirrored on the Internet Archive.
    - The test is US law. Under Australian law some of these works, such as
      Fisher 1930 (Fisher died in 1962), are still in copyright. They are
      held as private research copies under Barry's decision of 23 October
      2026 for the whole programme ([data catalogue](../sources/README.md)):
      "Licence overrides confirmed, universally for the EPRP. Mirroring
      locally is always okay for us: we're not hosting anything here for
      public use".

  Copies are private to EPRP and are not redistributed.
- **One exception, already held.** 34 copies predate this rule. They came
  from public university repositories (White Rose, UCL, HAL, Caltech,
  Southampton, NOAA and others) at locations OpenAlex does not flag open. They
  are kept because those repositories serve them to anyone. The fetcher no
  longer takes unflagged locations; CORE reaches such repository copies
  instead. One copy that came from cambridge.org through an unflagged
  location was withdrawn on 23 October 2026.
- **Author-hosted copies, 28 October.** Barry asked Codex to import the
  individually identified Bristol and Yale author-site copies in the
  [staging record](notes/2026-10-28-codex-author-site-recovery.md). They are
  private research copies with the source and unverified licence/version
  recorded; public availability is not a redistribution licence. Future
  author-site candidates require individual source and identity checks.
- **Requests are polite and honest.** The tool identifies itself, waits 3 s
  between downloads or Semantic Scholar lookups on the same host, follows
  http and https links only, and records every attempt. It does not evade bot
  protection or use shadow libraries. It does not download systematically
  from publisher sites through campus IP authentication; that breaches
  subscription terms and risks a university-wide block.
- **Keys.** Barry registered them on 24 October 2026. They live on
  `deep-server` in `~/.config/{openalex,core,elsevier}/api_key` and
  `~/.config/wiley/tdm_token`, mode 600, and are never printed or logged.
  - A key file must hold a single printable token; anything else is
    ignored.
  - Credential headers follow a redirect only to an https URL on the same
    site (for example `api.wiley.com` to `alm.wiley.com`).
  - The OpenAlex key raises the daily budget to 10,000 credits.
  - The CORE key enables the CORE route.
- **Publisher text-and-data-mining (TDM) copies** are a separate class.
  - The publisher terms limit TDM to non-commercial academic research and
    require deleting downloaded copies when the project ends. Corpus access
    and permission to send material to an AI service are separate.
  - TDM copies are therefore kept apart, under `tdm/<publisher>/`, with
    manifest status `tdm_ok` and a note, and are used for local search and
    mining only. Until UTAS Library confirms that its licences allow
    processing by AI services that do not train on the content, Wiley text
    stays out of agent sessions, including grep output. Counts and aggregate
    statistics from scripts are fine. The bounded Elsevier output exception
    below follows Barry's 5 November instruction; it does not apply to Wiley.
  - Everything obtained under a TDM licence stays under `tdm/`, including
    rejected downloads (`tdm/<publisher>/quarantine/`) and withdrawn copies
    (`tdm/<publisher>/withdrawn/`). Deleting `tdm/` therefore discharges the
    end-of-project duty.
  - A TDM route is tried only for that publisher's DOIs, and only after every
    open route has been tried in that run with no transient failure. A lookup
    service paused for rate limits (Semantic Scholar often is) does not block
    TDM, because an open copy found later replaces the TDM copy.
  - If an open copy turns up later (with `--retry-failed`), it replaces the
    TDM copy, which is deleted.
  - **Wiley** (since 24 October 2026): `api.wiley.com` with the TDM token,
    from deep-server on the campus network, at most one request per 11 s
    (Wiley allows 60 per 10 minutes). It covers DOI prefixes 10.1111, 10.1002,
    10.1029 (AGU), 10.1046, 10.1034 and 10.1890 (ESA), including back files
    such as *Evolution* 1949.
  - **Elsevier**: Article Retrieval access was enabled by API Support and
    [verified on 4 November 2026](notes/2026-11-04-elsevier-entitlement-probe.md).
    One non-open-access article returned full-text XML with HTTP 200 both
    through the laptop's GlobalProtect connection and directly on campus.
    This establishes access for that article and those requests; other
    subscription entitlements remain article-specific. `elsevier.py` now
    retrieves XML through that API on `deep`, with at least three seconds
    between calls, durable quota pauses, hashes and resumable manifests.
    Open copies are retained in preference to new subscription copies.
    Barry authorised the user-reported approved use case on 5 November:
    agents may receive extracted facts/numbers, metadata and short snippets
    with a DOI. `elsevier.py query` requires a private approval receipt and
    enforces a conservative cumulative limit of 200 excerpt characters per
    DOI across calls, source credit, DOI link and the required rights notice.
    Bulk text, unrestricted passages and question wording stay in the
    restricted store. The forwarded approval/use-case excerpts are archived
    there; the original MIME approval has not been independently recovered.
    This is a publisher-specific output exception, not permission to send
    the corpus to an AI service.
- **Rate limits and refusals.** An HTTP 429 from a lookup service or TDM API,
  or a 401 or 403 from a lookup service (a key problem), pauses that host for
  the rest of the run, with no failure recorded; the next run continues where
  it stopped. An unexpected error on one work is logged and the run carries
  on.
- **No email address or other personal identifier** is sent to any service.
  An OpenAlex key is read from `OPENALEX_API_KEY` or
  `~/.config/openalex/api_key`, if one exists.
- **Every PDF is checked.**
  - The download must be complete, start with `%PDF-`, and open in `pdfinfo`
    and `pdftotext`.
  - At least 60% of the title's content words (three or more letters, minus
    common short words) must appear in its first three pages. A title with
    fewer than two content words must appear whole.
  - A PDF that fails the title check goes to `quarantine/`.
  - A scan without a usable text layer is kept with status `no_text`. Older
    scans may have an unchecked title; `import-staged` checks first-page OCR.
    Neither status means the full text has been OCRed. See the manifest note.
  - `ocr_ok` means an open scan has machine OCR passing an identity and basic
    page-coverage check. It is not a verified transcription: inspect the PDF
    for exact wording, figures, tables and claims.

## Running it

`library.py` needs Python 3.9+ (standard library only) and poppler's
`pdftotext` and `pdfinfo`. `import-staged` for scans and `ocr` additionally
need `pdftoppm` and Tesseract with English language data.

```bash
python3 resources/library/library.py harvest .
rsync -a resources/library/library.py resources/library/seeds deep-server:/data/paleodata/library/_tools/
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py resolve'
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py expand --out /tmp/expand' && scp deep-server:/tmp/expand/neighbours.tsv resources/library/seeds/
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py frontier --out /tmp/frontier' && scp deep-server:/tmp/frontier/frontier.tsv resources/library/seeds/
ssh deep-server 'cd /data/paleodata/library && setsid nohup python3 _tools/library.py fetch --workers 8 > fetch.log 2>&1 < /dev/null &'
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py textindex'
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py index --out /tmp/library-index'
scp 'deep-server:/tmp/library-index/*' resources/library/
```

- `resolve` fetches only keys it has not seen. It skips keys already found to
  be datasets, invalid or deleted; `--recheck` retries them.
- `fetch` skips works already held and URLs that failed permanently. Errors,
  timeouts, truncated downloads and HTTP 408, 429 and 5xx are retried on the
  next run. `--retry-failed` retries everything.
- `import-staged MANIFEST DIRECTORY` imports individually reviewed local PDFs
  with their source URLs and hashes. It locks the store, verifies the batch
  and DOI identities before writing, checks titles using embedded text or
  first-page OCR, never replaces an existing open or withdrawn record, and
  records uncertain licences and versions as such. A verified open copy may
  supersede a TDM record in the catalogue while leaving that TDM copy intact
  under `tdm/` with its historical manifest entry. It can also replace a
  specifically rejected incomplete file, which remains in quarantine. A scan gets `no_text`; OCR checks
  its identity but is not a full-text transcription. Rerunning an intact
  imported batch is idempotent. An interrupted partial write requires inspection,
  not automatic overwriting.
- `ocr W…` processes explicitly selected open `no_text` scans, at most 40
  pages per work unless `--max-pages` is set. It verifies the original PDF
  hash, checks the first-page title and minimum text coverage, preserves the
  PDF and its original text extraction, and records page-level counts and
  checksums in `ocr/`. It does not process publisher TDM copies. An intact
  completed run is idempotent; unregistered output from an interrupted run
  requires inspection before retrying. `--language por`, for example, selects
  an installed Tesseract language; when `TESSDATA_PREFIX` identifies a model
  directory its model hashes are recorded in the receipt.
- `verify-embedded W…` rechecks an open `no_text` copy whose stored extraction
  has usable embedded text despite its first pages. It verifies the PDF hash,
  page count, title within the first 15 pages, and agreement between a fresh
  extraction and the stored text, then records `ok` without changing either
  file. `--title-pages` selects a different title-check window.
- `withdraw W… --reason TEXT` removes held copies, for example at the end of
  a TDM project, and records why.
- `reject-incomplete W… --reason TEXT` moves an open `no_text` copy known to
  be an incomplete document or unrelated figure into `quarantine/rejected/`.
  It preserves the file and manifest history; a separately checked complete
  copy can then be imported. Automatic `fetch` skips rejected works, including
  on retry, so it cannot silently reacquire the same incomplete file. A regular
  withdrawal cannot be replaced through `import-staged`.
- `search QUERY` searches the whole library: every work's title and abstract
  (reconstructed from OpenAlex), and the extracted text of every held copy.
  It is SQLite FTS5 with BM25 ranking (titles weighted 5), Porter stemming
  and accent folding. Queries take words (all required), `"phrases"`, `OR`,
  `NOT`, `NEAR(a b, 10)` and `prefix*`; a query FTS5 cannot parse is retried
  as all its words. `--tier` and `--part` narrow it, and `--tsv` gives
  machine-readable output.
  - Results show matching passages from abstracts and open full texts. A match
    in a TDM text is reported without a passage, so no licensed text reaches
    an agent session.
  - From any machine:
    `ssh deep-server 'python3 /data/paleodata/library/_tools/library.py search "age-dependent extinction"'`.
  - `textindex` rebuilds the indexes in about a minute. Run it after
    `resolve`, `fetch`, `import-staged`, `ocr`, `verify-embedded`, `reject-incomplete` or `withdraw` changes works or texts.
    - `search.sqlite` holds titles, abstracts and open texts.
    - `tdm/search-tdm.sqlite` holds TDM texts in a contentless index. It
      stores no readable text and gives no passages, and it sits under `tdm/`
      with the copies it derives from, so deleting `tdm/` removes all of it.
- `match IN.tsv OUT.tsv` resolves a reference list to DOIs or OpenAlex ids:
  - Input columns: `raw` (the citation), `first_author`, `year`, and where
    known `title`, `volume` and `pages`.
  - Crossref candidates come first, then an OpenAlex title search.
  - Each match is graded `exact` or `probable`. The rules are in
    [the 2003 note](notes/barry-2003.md), where 892 of 904 citations
    resolved exactly.
  - Add the resolved rows to a seed file to make a tier.
- `resolve`, `fetch`, `import-staged`, `ocr`, `verify-embedded`, `reject-incomplete` and `withdraw` take a lock on the store, so two writers
  cannot run at once.
- Run anything longer than a few minutes on `deep-server`, never on the
  laptop.

## Lessons so far

- **OpenAlex without a key** allows each IP address about 1,000 credits a
  day ($0.10). A `search=` costs 10 credits. A `filter=doi:A|B|…` or
  `filter=openalex:W1|W2|…` list returns up to 50 works for 1 credit. Find
  candidates with Crossref or Semantic Scholar, then verify them in OpenAlex
  in batches.
- **Older *Paleobiology*, *Geology* and *PALAIOS* DOIs are SICIs**, such as
  `10.1666/0094-8373(2004)030<0396:OSBAHW>2.0.CO;2`. The registered forms
  differ in bracket style (`<…>` or `[…]`) and zero padding, and text alters
  both. The harvester keeps each DOI as written. `resolve` then tries the
  other spellings on a miss.
- **Batch DOI filters silently drop alias DOIs and DataCite deposits**, such
  as JSTOR's `10.2307/…` and Zenodo versions. A single `works/doi:` lookup
  follows them.
- **Publishers refuse scripted PDF downloads** (HTTP 403) even for
  open-access papers: Wiley (including AGU and *Evolution*), PNAS, Elsevier,
  OUP, Taylor & Francis. Europe PMC's PDF renderer and NCBI PMC do the same.
  PNAS and many others are free in PMC but not in its open-access subset.
- **Many repository records OpenAlex lists are metadata only**, with no file
  attached, so a failure there is not a missed copy.
- **The Internet Archive's scholarly endpoints** (fatcat, scholar.archive.org)
  were unavailable on 23 October 2026.
- **OpenAlex holds many classics only as reissues** (Simpson's *Tempo and
  Mode* as a 1984 or 2005 record) or as book-review stubs (Gould 1989, Raup
  1991). The same book can also appear as several W ids (21 such groups among
  3,334 records on 23 October 2026), and some referenced ids are deleted
  records (HTTP 404). The canon records OpenAlex's values and gives the
  original citation in its `why` column. Deduplicating across W ids is still
  to do.
- **NCBI's id converter** maps PMC ids to DOIs without a key. OpenAlex's
  `pmcid` filter returned nothing for valid PMC ids, but its `pmid` filter
  works.
- **CORE's cached PDFs cannot be fetched by script.** `core.ac.uk/download/…`
  and even the authenticated `api.core.ac.uk/v3/outputs/<id>/download` answer
  with a Cloudflare browser challenge (24 October 2026). Some of CORE's
  `sourceFulltextUrls` are reference-list text, not links. The route keeps
  only the repositories' own http(s) links.
- **The Internet Archive holds most pre-1931 classics** as unrestricted
  scans. The route recovered 9 of the 12 such works the library lacked (11
  of 14 OpenAlex records). They include Lyell's *Principles*, Darwin's
  *Origin*, Thompson's *On Growth and Form*, Fisher's *Genetical Theory* and
  Moseley's 1838 *Phil. Trans.* paper, from JSTOR's free Early Journal
  Content.
- **Not every unrestricted Internet Archive item is a public-domain scan.**
  Some items carry no access restriction yet are LCP-protected lending copies
  of modern reprints, such as Cambridge's 2014 Canto edition of *On Growth
  and Form*, dated 1917 in its metadata. The route excludes LCP items,
  ISBN-bearing items and titles carrying a later year. One *On Growth and
  Form* copy taken from a lending item before this check was withdrawn.
- **The Internet Archive reports search errors inside an HTTP 200.** The
  route treats them as transient errors, not as "no copy".
  - Catalogue titles need cleaning before search: drop leading numbering
    such as "XVII." and statements of responsibility such as "/ by John
    Phillips".
- **The 48 held copies whose final host is a publisher** (cambridge.org,
  nature.com, Annual Reviews, Springer, *Science*) all came from locations
  OpenAlex marks open. Re-requesting them from an off-campus host would
  confirm that; it has not been done.

Maintained by EPRP agents for Barry W. Brook. Started 23 October 2026 (Claude
side session, worktree `library`).
