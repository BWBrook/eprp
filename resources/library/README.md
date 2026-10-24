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
  library.py              harvest | resolve | expand | fetch | withdraw | index
  seeds/<tier>.tsv        seed lists, one file per tier; rows give openalex_id, doi or pmid
  topics.md               the canon's topic tree (ids such as extinction/selectivity)
  notes/                  method records for curated tiers (how the canon and author-year seeds were built)
  review/                 candidates held back from the seeds: unsettled citations, canon reserve and unverified
  works.tsv               generated: one row per resolved work, with tiers, questions and full-text status
  INDEX.md                generated: counts by tier, full-text status, type, decade and venue
  by-question.md          generated: cited works grouped by question (Q-, B-) and catalogue entry (src:)
  unresolved.tsv          generated: seed rows that did not resolve to an OpenAlex work
  eprp-library-README.md  installed as /data/paleodata/library/README.md
```

The store is on `deep-server`, beside the data-source mirror:

```text
/data/paleodata/library/
  openalex/<W>.json       full OpenAlex record: metadata, abstract index, references, locations
  pdf/<W>.pdf             open-access full text, read-only
  text/<W>.txt            pdftotext output of pdf/<W>.pdf (derived; rebuildable)
  quarantine/             PDFs whose first pages did not contain the work's title
  quarantine/withdrawn/   copies removed by `withdraw`, with the reason in manifest.tsv
  tdm/<publisher>/pdf/    publisher text-and-data-mining copies (local search and mining only; see below)
  tdm/<publisher>/text/   their extracted text
  manifest.tsv            append-only: one row per stored or withdrawn copy, with its path; the latest row per work counts
  attempts.tsv            append-only: every download attempt and Semantic Scholar lookup, with its outcome
  aliases.tsv             seed key (doi:…, pmid:… or merged W id) to OpenAlex id
  unresolved-keys.tsv     seed keys OpenAlex lacks: Crossref-only, invalid or deleted
  _tools/                 the deployed library.py and seeds/
  _provenance/            read-only working files, scripts and API caches of the curated tiers
```

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
| `neighbours` | `seeds/neighbours.tsv` | works outside the tiers above that at least 5 of their works reference (`library.py expand`), with that count and the questions of the citing works |
| `field` | (planned) | complete runs of core journals and topic sweeps; citing works of the seeds; metadata only by default |

A work belongs to every tier that names it. `fetch` tries works in tier order:
the cited tiers first, then the canon, then neighbours by reference count.
Questions come from the citing context. In the registers, that is the
enclosing `### Q-NNN` or `### B-NNN` section. Elsewhere, it is a `q012`/`b003`
token in the path or a `resources/sources/<id>/` directory. `works.tsv` and
`by-question.md` carry the cited tiers' questions only. A neighbour's inherited
questions stay in `seeds/neighbours.tsv`, as leads rather than citations.
Canon works carry a topic id from the topic tree.

The `review/` lists hold candidates that are not yet seeds:

- author–year citations graded `ambiguous` or `unresolved`;
- the canon scout's 340 verified but unselected works;
- its 13 works that OpenAlex and Crossref could not confirm.

To promote a work, add it to a seed file with its reason.

Rerun `harvest` and `resolve` whenever the registers, notes or catalogue
cite new works. Rerun `expand` after any seed tier changes. At 5 references
the neighbours ring holds about 2,100 works; at 3, about 5,500; at 8, about 800.

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
  - Semantic Scholar's open-access link.

  Copies are private to EPRP and are not redistributed.
- **One exception, already held.** 34 copies predate this rule. They came
  from public university repositories (White Rose, UCL, HAL, Caltech,
  Southampton, NOAA and others) at locations OpenAlex does not flag open. They
  are kept because those repositories serve them to anyone. The fetcher no
  longer takes unflagged locations; CORE reaches such repository copies
  instead. One copy that came from cambridge.org through an unflagged
  location was withdrawn on 23 October 2026.
- **Requests are polite and honest.** The tool identifies itself, waits 3 s
  between downloads or Semantic Scholar lookups on the same host, follows
  http and https links only, and records every attempt. It does not evade bot
  protection or use shadow libraries. It does not download systematically
  from publisher sites through campus IP authentication; that breaches
  subscription terms and risks a university-wide block.
- **Keys.** Barry registered them on 24 October 2026. They live on
  `deep-server` in `~/.config/{openalex,core,elsevier}/api_key` and
  `~/.config/wiley/tdm_token`, mode 600, and are never printed or logged.
  - The OpenAlex key raises the daily budget to 10,000 credits.
  - The CORE key enables the CORE route.
- **Publisher text-and-data-mining (TDM) copies** are a separate class.
  - The publisher terms limit TDM to non-commercial academic research. They
    also require deleting downloaded copies when the project ends, and
    Elsevier's restrict third-party processing, which covers sending text to an
    AI service.
  - TDM copies are therefore kept apart, under `tdm/<publisher>/`, with
    manifest status `tdm_ok` and a note, and are used for local search and
    mining only. Agents read them only once UTAS Library confirms that its
    licences allow processing by AI services that do not train on the content.
  - A TDM route is tried only after every open route fails, and only for that
    publisher's DOIs.
  - **Wiley** (since 24 October 2026): `api.wiley.com` with the TDM token,
    from deep-server on the campus network, at most one request per 10 s
    (Wiley allows 60 per 10 minutes). It covers DOI prefixes 10.1111, 10.1002,
    10.1029 (AGU), 10.1046, 10.1034 and 10.1890 (ESA), including back files
    such as *Evolution* 1949.
  - **Elsevier**: the key works for Scopus abstracts and ScienceDirect search,
    but Article Retrieval refuses every request, open-access articles included
    (HTTP 403, "Requestor configuration settings insufficient"). New Elsevier
    keys carry no content access until Elsevier API Support verifies the
    institution's entitlement, so there is no Elsevier route yet.
- **Rate limits.** An HTTP 429 from a lookup service or TDM API pauses that
  host for the rest of the run, with no failure recorded; the next run
  continues where it stopped.
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
  - A scan without a text layer is kept with status `no_text`. Its title is
    unchecked, and it awaits OCR.

## Running it

`library.py` needs Python 3.9+ (standard library only) and poppler's
`pdftotext` and `pdfinfo`.

```bash
python3 resources/library/library.py harvest .
rsync -a resources/library/library.py resources/library/seeds deep-server:/data/paleodata/library/_tools/
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py resolve'
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py expand --out /tmp/expand' && scp deep-server:/tmp/expand/neighbours.tsv resources/library/seeds/
ssh deep-server 'cd /data/paleodata/library && setsid nohup python3 _tools/library.py fetch --workers 8 > fetch.log 2>&1 < /dev/null &'
ssh deep-server 'cd /data/paleodata/library && python3 _tools/library.py index --out /tmp/library-index'
scp 'deep-server:/tmp/library-index/*' resources/library/
```

- `resolve` fetches only keys it has not seen. It skips keys already found to
  be datasets, invalid or deleted; `--recheck` retries them.
- `fetch` skips works already held and URLs that failed permanently. Errors,
  timeouts, truncated downloads and HTTP 408, 429 and 5xx are retried on the
  next run. `--retry-failed` retries everything.
- `withdraw W… --reason TEXT` removes held copies, for example at the end of
  a TDM project, and records why.
- `resolve`, `fetch` and `withdraw` take a lock on the store, so two writers
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
- **The 48 held copies whose final host is a publisher** (cambridge.org,
  nature.com, Annual Reviews, Springer, *Science*) all came from locations
  OpenAlex marks open. Re-requesting them from an off-campus host would
  confirm that; it has not been done.

Maintained by EPRP agents for Barry W. Brook. Started 23 October 2026 (Claude
side session, worktree `library`).
