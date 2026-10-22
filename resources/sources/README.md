# Data source catalogue

A catalogue of palaeobiological and related data sources that EPRP questions
may draw on. It covers living databases, compilations and deposited datasets.
Each entry says what a source contains, where its records came from, how to get
them programmatically, what they are good and bad for, and what we have
verified ourselves. Openly licensed sources are also mirrored on `deep-server`,
so the exact inputs are on hand when the science starts.

Entries follow [the evidence conventions](../../docs/evidence.md). This catalogue
adds structure; it does not relax those conventions. A catalogue entry is not a
fitness-for-purpose verdict. Suitability is always relative to a question.

## Layout

```text
resources/sources/
  README.md                 this file: conventions, template, lessons
  INDEX.md, index.tsv       generated index of all entries (build_index.py)
  BACKLOG.md                ranked sources to catalogue next
  CONTACTS.md               outreach queue: issues for outside parties, held for one tranche
  build_index.py            rebuilds the index: uv run resources/sources/build_index.py
  paleodata-README.md       the README installed at /data/paleodata/
  <id>/README.md            the entry: YAML front matter + guide
  <id>/<provider>-versions.tsv  full version index, where the source is versioned
  <id>/<id>_profile.py      our profiling code for that source
  <id>/profile/             profiling outputs quoted by the entry
  <id>/*.sql, *.py, *.R     tested extraction recipes and checks
resources/tools/            source-independent tools (data_mirror.py: Zenodo, Figshare,
                            GitHub, Dryad, WFS and plain URLs)
```

The mirror on `deep-server` uses the same `<id>`:

```text
/data/paleodata/
  README.md
  _tools/                   read-only copies of the committed tools used there,
                            named <id>_<script> for source-specific ones
  <id>/versions.tsv         index written by the mirror tool
  <id>/raw/<version_dir>/   unchanged source files + MANIFEST.json; read-only;
                            data_mirror.py names these per provider
  <id>/derived/<version_dir>/  conversions rebuilt by committed code; deletable
  <id>/mirror.log
```

`raw/` is immutable once written. Each `MANIFEST.json` records the source
identifier and DOI, version, licence, retrieval time, every file's size, the
provider's checksum, our sha256, and the sha256 of the tool that fetched it.
Verify with `python3 resources/tools/data_mirror.py verify <dest>`.
Anything under `derived/` must be rebuildable from `raw/` by committed code,
and its entry says which script writes it (for NSB, `nsb_profile.py` unzips
the SQLite and `age_check.py` writes recomputed ages). Deploy a tool to
`_tools/` only from a committed version, and check its sha256 matches.

Dryad serves its indexes openly but its file downloads only to an API
account. `data_mirror.py dryad` reads `DRYAD_CLIENT_ID` and
`DRYAD_CLIENT_SECRET` from the environment or from
`~/.config/dryad/credentials` (`KEY=value` lines, mode 600) on the host that
runs it. Credentials never enter the repository.

## Entry kinds

- **database**: a maintained, queryable service whose content changes (PBDB,
  Neotoma, NSB). Gets the full treatment: live access route, versioning and
  replay, schema, profiling, lineage and overlap.
- **compilation**: a curated assembly of other sources, usually versioned and
  deposited (Triton, BioDeepTime). Lineage and overlap with its inputs matter most.
- **deposit**: a fixed archive accompanying a paper (Dryad, Zenodo, Figshare,
  PANGAEA). Gets a lighter entry; its paper and whether it runs as deposited
  matter most.

## Access tiers and mirror policy

| Tier | Meaning | Mirror |
| --- | --- | --- |
| `open` | Licence allows copying and redistribution (CC0, CC-BY, ODbL) | Yes |
| `open-nc` | Copying allowed with non-commercial or share-alike terms | Yes, terms recorded |
| `registered` | Free access under terms that limit use or redistribution, accepted by account, click-through or download | No, unless the terms allow local copies (Barry decides) |
| `restricted` | Request, approval, embargo or paywall | No |
| `unclear` | No licence stated | No; treat as all rights reserved |

Software or API-documentation licences are not data licences. Record the data
terms that apply to the records themselves, including constituent-dataset
terms where a database aggregates contributors.

**Which versions to mirror.** Index every version the provider offers, and
commit the index with the entry. Mirror the latest version, plus any older
version that an entry's profile or an EPRP analysis depends on. Fetch other
versions on demand (`data_mirror.py ... --only <version_dir>`) when a past
analysis has to be reconstructed. Forward-looking work uses the latest
version, after the entry's pitfalls are dealt with (for NSB, its stale stored
ages). Persistent, DOI-versioned repositories such as Zenodo and Figshare
already preserve the rest; a full local history earns its place only for a
source that lacks such an archive. A live database with no releases (PBDB,
ASUD, the OCTOPUS layers) is the extreme case: each dated snapshot is a
version that cannot be fetched again, so keep them all.

## Entry template

Front matter carries the fields an index needs; the body carries the guidance.
Keep values factual and dated. Use `unknown` rather than guessing.

```yaml
---
id: short-lowercase-id                  # also the mirror directory name
name: Full name (ACRONYM)
kind: database | compilation | deposit
status: active | frozen | retired       # frozen = no updates since last_update
last_update: YYYY-MM-DD                 # newest content we can see (YYYY-MM if that is all that is known)
scope:
  taxa: [...]
  time: text, with numeric bounds in Ma
  space: text
  record_unit: what one row represents
size:                                   # our counts, not the provider's claims
  as_of: version or date
  ...
access:
  tier: open | open-nc | registered | restricted | unclear
  licence: SPDX id or text
  routes:                               # every way to get the records
    - {type: ..., url: ..., state: ..., checked: YYYY-MM-DD}
  api: text or none
versioning:
  replay: exact | partial | none        # can a past state be recovered?
  notes: text
mirror:
  path: deep-server:/data/paleodata/<id>
  policy: text
  state: text
lineage:
  upstream: [...]
  downstream: [...]
eprp_questions: [Q-..., B-...]
citation: [...]
entry:
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  by: participant (model)
  reviewed: "who and when, or not yet"
---
```

Quote any YAML value or list item that contains a comma or colon; the front
matter must parse (`yaml.safe_load`) to the intended structure.

Body sections, in order:

1. **Summary**: what it is and when to reach for it, in one paragraph.
2. **Contents**: what is in it, with our own counts and coverage tables.
3. **Provenance and lineage**: who built it, from what, and who copied it.
4. **Structure**: tables or files, keys and relations, and every code
   vocabulary with counts; flag codes the documentation does not define.
5. **Access**: every route, the mirror location, and for databases a tested
   extraction query that reproduces the provider's default output.
6. **Strengths**.
7. **Weaknesses and pitfalls**: what will bite an analyst, with evidence.
8. **Overlap with other sources**: measured where possible, otherwise flagged.
9. **EPRP relevance**: questions it serves, and what it cannot support.
10. **Citation and terms**.
11. **Verification log**: dated checks, each labelled `checked` (we ran or read
    it), `source claim` (the provider or a paper says so), `inferred` (our
    reasoning from checked facts) or `recall` (known but not checked here).

## Adding a source

1. Establish identity and access: licence, routes, registration, versioning.
2. Index every available version before mirroring anything.
3. Mirror if the tier allows; verify checksums; make `raw/` read-only.
4. Profile from the mirror: counts, coverage, schema, codes, filters, drift.
   Reconcile counts with those the provider or paper reports, and rebuild any
   provider export (filtered files, default downloads) from the raw tables.
5. Read the primary description paper and documentation in full; scan for
   lineage, overlap, uses and published critiques.
6. Write the entry; quote our numbers, cite theirs. Every number labelled
   `checked` must come from committed code with a committed output. Rebuild
   the index.
7. Have the entry reviewed independently before treating it as settled.
8. Add any issue that needs a provider or custodian to act (errors, stale
   documentation, licence conflicts, access problems) to
   [CONTACTS.md](CONTACTS.md). Never contact them directly; Barry handles the
   queue as one tranche.

## Lessons so far

Lessons from each source added, kept short. They should change the template or
the workflow when they generalise.

**NSB (pilot, 22 October 2026; [entry](nsb/README.md)).**

- *Index every version, and profile a series, not a pair.* The year-end
  series separated three causes of age drift (time-scale change, model
  revision, batch recomputation) that a two-snapshot comparison blurred, and
  exposed stale stored ages in the final snapshot (4,111 samples in 56 holes).
  Profile the snapshot a paper's counts match, too.
- *Recompute derived fields from their inputs.* NSB's sample ages are a cache
  of its age models; checking the cache against the models found the
  staleness. Any stored derived value (ages, palaeocoordinates, resolved
  names) deserves the same test.
- *Rebuild the provider's convenience exports from the raw tables.* NSB's
  "filtered" file silently keeps undated samples, and its full file carries
  recorded absences that look like presences. Neither is documented. Every
  database entry should ship an extraction recipe whose agreement with the
  provider's export is checked by committed code on each profile run, with
  any intended differences stated.
- *Check which file is the whole database.* NSB's SQLite copy omits 14 of
  the PostgreSQL dump's 35 tables, including one that links NSB to Triton
  record by record.
- *Enumerate every code column.* Five qualifier codes, one taxon status and
  both sample-status codes were undefined in the description paper.
- *Reconcile our counts with the provider's, with like-for-like definitions.*
  The 2019-08-30 snapshot reproduces the paper's counts exactly, validating
  the mirror and profiler at once. Comparing "sourced" coverage under two
  different definitions nearly produced a false improvement.
- *Measure overlap at site level first.* It is cheap and decisive (NSB
  foraminifera are 95% inside Triton's sites). Look for linking keys before
  attempting record-level matching by taxonomy.
- *Commission an independent review before calling an entry settled.* The
  adversarial pass on NSB found five major problems in a carefully built
  entry, and supplied the evidence for the stale-ages finding.
- *Live services die; deposits survive.* NSB's website went down with a
  museum cyberattack in October 2023 and never returned; its Chronos
  predecessor vanished earlier. The Zenodo snapshots, uploaded weeks after the
  attack, are now the only route. Prefer deposited versions as the citable
  input, and record each service's status with a date.
- *Aggregator copies go stale.* GBIF still serves a 2016 copy of NSB, a third
  smaller and without ages. Record such copies in the entry so nobody mistakes
  them for the source.
- *Run a lineage-and-literature scan alongside profiling.* It found the
  outage's cause, the current R access route, documented critiques and four
  downstream compilations; none of these was visible from the data.
**Triton (compilation, 22 October 2026; [entry](triton/README.md)).**

- *Test a compilation for duplicates with its own key, then test the key.*
  Triton's 2023 file silently dropped the deduplication its 2021 version
  applied: 28,832 duplicate rows by the authors' own key. But 44% of them
  collide distinct samples within one source (rows with no depth), so the
  authors' key would have deleted real records. Only the cross-source groups
  are true duplicates.
- *Check derived fields against their inputs, not their documentation.*
  Triton's paper says all palaeocoordinates are Matthews et al. (2016); the
  20% from Neptune are NSB's Seton et al. (2012) values, found by comparing
  them with NSB record by record.
- *Rerun downstream analyses when a data flaw is found.* Rerunning EPRP's
  Q-007 and Q-012 builds with and without duplicates turned "probably
  harmless" into measured effects (Q-007 gate unchanged; Q-012 exposure
  classes shift).
- *Know which table you loaded.* File names repeat across versions with
  different contents, the "deduplicated" file is a different (sample-level)
  product, and a third-party mirror (`chronosphere`) labels that product
  "main". Record the version DOI and sha256 of the exact file.
- *Look for carried identifiers before matching records.* Triton keeps NSB's
  `sample_id`, which made a record-level overlap with NSB a join rather than a
  taxonomic matching problem, and dated Triton's NSB copy to March 2019.
- *Downstream copies lag.* `chronosphere` stops at v3 and Mikrotax at a
  pre-v3 copy; both miss v4's unit corrections.
- *A data paper's counts may not match its deposit.* Reconcile them and
  report the difference rather than quoting the paper.

**FRED (registered access, 22 October 2026; [entry](fred/README.md)).**

- *A registered source still gets a full entry.* Contents, provenance, terms
  and a step-by-step access recipe are all documentable from public pages,
  the manual, the custodian's metadata and the description paper. What it
  cannot get is a profile; counts come from the provider, dated.
- *Look behind the map.* Public web maps often sit on open WFS/WMS layers
  that expose more than the stated public view (FRED's gives locality text
  for all 105,492 localities). Record such routes, but do not harvest until
  the terms are clear.
- *Licence signals conflict across layers.* A service-wide CC-BY header and
  a restricted dataset classification can both apply. Resolving it is a
  question for the custodian, which is an outward-facing step for Barry.
- *Measure overlap through stable identifiers.* FR numbers in PBDB
  collection names gave a measured overlap (about 2% of localities, half of
  PBDB's New Zealand occurrences) without any FRED access.
- *Registration is Barry's call.* Accounts carry obligations (research-only
  use, contribution, inviting originators); an agent should not register
  on his behalf without his say.

**Sahul tranche (22 October 2026; [FosSahul](fossahul/README.md),
[SahulArch](sahularch/README.md), [AustArch](austarch/README.md),
[OCTOPUS](octopus/README.md)).**

- *A live service can be the only release.* SahulArch's DOIs hold no files;
  the data exist as WFS layers. Snapshot them, check row counts against the
  server, and record the version stamp and server time (`data_mirror.py
  wfs`).
- *Compare every copy in circulation.* The AustArch copy used in Barry's
  rc-dates work is close to "numeric age and error only" (it lacks the Modern,
  most limiting and the asymmetric-error ages), and shows spreadsheet damage:
  depth ranges turned into dates, and seven qualifiers stripped. FosSahul's
  GitHub, Figshare, TERN and OCTOPUS copies differ in coordinates, schema and
  record count.
- *Read flags in context before acting on them.* SahulArch's 14
  "supercedes" notes mark the preferred ages, not the rejected ones.
- [Detail withheld pending disclosure to the data custodian.]
- *Use applicable denominators for completeness.* Field coverage measured
  on all rows understates it for method-specific fields (F14C: 15% of all
  ages, 33% of AMS ages).
- *Re-run the provider's own algorithm.* FosSahul's rating script reproduces
  the 2021 ratings exactly but not the 2019 file's, which locates when the
  ratings were corrected.
- *Read README claims as hypotheses.* FosSahul's README says coordinates are
  rounded; the current file is not. The precision varies by release, and the
  catalogue records which is which.
- *Record authorship and authorisation.* Barry co-authored FosSahul 1; the
  entry says so, and records his authorisation of the GitHub copy and of the
  private AustArch copy, quoting him.
- *Scan before choosing.* The Australian scan found that obvious-looking
  routes add little for Australian palaeontology: Atlas of Living Australia
  fossil records are almost entirely foreign-museum or NSB specimens, and
  Macrostrat has no Australian columns. PBDB's Australian subset is the real
  deep-time workhorse ([BACKLOG.md](BACKLOG.md)).

**PBDB, ASUD and the Quaternary tranche (22 October 2026; [pbdb](pbdb/README.md),
[asud](asud/README.md), [neotoma](neotoma/README.md), [sahulchar](sahulchar/README.md)).**

- *A live, unversioned database's snapshots are its only versions.* Keep every
  dated PBDB extract; neither `created` filtering nor timestamps rebuild a past
  state, and interval ages are recomputed when time scales change.
- *Make live snapshots self-verifying.* Fetch a `limit=0&rowcount` count beside
  every table, and take a second extract minutes later: the two PBDB extracts
  were identical, which shows the output is deterministic.
- *Ask for everything once.* Entry history (`crmod`), all three plate models
  and specimens cost nothing extra at download time and decided several
  findings. Overlapping `show` blocks duplicate column names; check that the
  duplicates agree before trusting any reader.
- *Check documentation against the data.* PBDB's User Guide says its time
  scales are mostly GTS2012; the ages use GTS2020-era boundaries. Neotoma
  labels 200 ka ages "calibrated radiocarbon". Data win.
- *Match to an authority with state and age, and report a null.* Name
  matching alone produced homonyms across states. Reporting exact and
  core-name tiers separately, and the age agreement of random same-state units
  (12% against 95%), shows what the match is worth.
- *Use one regional classification across sources.* The same Sahul boxes in
  every profiler made the four charcoal sources comparable, and exposed that
  Pico et al.'s "Sahul" is a narrower region than Beyer's land mask.
- *Scope every percentage to its table and region.* The review caught
  collection-level timestamps applied to occurrences, early-Palaeozoic
  plate-model differences stated as general, and extract-wide blanks stated
  as Australian.
- *Describe distributions, not medians.* A 98% median overlap hid that 22% of
  paired collections shared nothing.
- *Commit the checks behind every "checked".* Scratch scripts became
  `pbdb_checks.py`; a claim with no committed code behind it is not checked.
- *Strip personal data from committed outputs.* NetCDF attributes and
  spreadsheet cells carried individuals' email addresses.
- *Keep raw read-only.* A script bug pointed its output at a mirrored input;
  the permissions refused the write.
- *Run large pulls per host in parallel.* Zenodo served about 0.6 MB/s to
  deep-server; OSF and Figshare downloads ran alongside instead of in a queue.

**Ranks 9–15 (22 October 2026; [stratdat](stratdat/README.md),
[fossil-checklists](fossil-checklists/README.md),
[au-fossil-deposits](au-fossil-deposits/README.md),
[gbif-ala-fossils](gbif-ala-fossils/README.md), [austraits](austraits/README.md),
[ala-vertebrates](ala-vertebrates/README.md), [names-status](names-status/README.md)).**

- *A negative result is a finding; write it down.* No deposit holds occurrence
  or census data for any flagship Australian biota, and GBIF and ALA fossil
  records add little beyond foreign-museum specimens and NSB's copy. The
  entries say so, so the searches are not repeated.
- *Publishers block servers; repositories do not.* Publisher PDFs returned 403
  to deep-server, and one "PDF" was a bot-check page. `data_mirror.py url` now
  refuses HTML served for a non-HTML file name. Prefer a repository copy;
  otherwise fetch on the laptop and verify the copy.
- *Dryad downloads need a token; Zenodo copies usually exist.* The source scan
  found Zenodo copies carrying the Dryad DOI for 50 of 58 deposits.
  `data_mirror.py dryad` indexes without a token and downloads with one.
- *Check field names against an independent authority.* STRATDAT's
  `_MIDPOINT` unit fields do not describe the same unit as `_TOP` for 95% of
  picks; matching unit names to ASUD's ages showed which field to trust.
- *Tables in PDFs are data; check every extraction.* Count rows per table
  against the PDF, and test the extraction for empty and merged fields.
- *Aggregators page shallowly.* GBIF slows beyond an offset of about 10,000
  and ALA stops at 5,000. Partition queries (by dataset, then by latitude) and
  reconcile the harvest with the service's reported count.
- *Subspecies are not species; listed names are not current names.* EPBC's
  extinct list mixes species and subspecies of living species, and carries a
  current name beside the listed one (117 rows differ). Truncating listed
  names to binomials would mark living species extinct and miss renamed ones.
- *A record's year is not a living animal.* ALA's records of extinct species
  dated after 1950 mix genuine late records, subfossil specimens, synonymies
  and name collisions; screen them before using last-record dates.
- *Redact as you echo.* A profiler that echoes spreadsheet headers or README
  text copied an author's email address; profilers now redact addresses.
- *Read the provider's field documentation before interpreting fields.* The
  mirrored STRATDAT schema already stated the time scale, the meaning of the
  pick codes and the confidence scale that the first draft called
  undocumented; and testing the documented `_MIDPOINT` definition against the
  data showed the fields hold the unit at half the sample depth.
- *An absence needs spelling variants and the right window.* Four of five
  "absent" Mesozoic tetrapods were misspellings in the source, a variant
  spelling in PBDB, or an age-window artefact.
- *Count data rows, not spreadsheet rows.* Captions, headers and totals
  inflated several deposit counts.
- *Pick the denominator that answers the question.* "13% raw values" in
  AusTraits mixed categorical traits, where the mode is the normal label,
  with numeric ones (30% raw).
- *Quality screens can share an author with what they screen.* The
  thylacine and devil "screen" of FosSahul applies FosSahul's own rating.

**Outreach (Barry, 22 October 2026).**

- *Queue contacts; send them as one tranche.* Cataloguing keeps turning up
  issues only providers can fix. Collect them per recipient in
  [CONTACTS.md](CONTACTS.md), so that one message goes to each party and
  replies are tracked in one place.

**Both pilots.**

- *Profile many versions; mirror few.* The year-end series was worth
  profiling, but keeping all 372 snapshots locally was not: Zenodo preserves
  them, and forward-looking work uses the latest (Barry, 22 October). The mirror
  keeps the 13 snapshots the profile depends on. Zenodo serves about
  0.2–0.3 MB/s per connection; Figshare about 3 MB/s.
