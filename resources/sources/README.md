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
  paleodata-README.md       the README installed at /data/paleodata/
  <id>/README.md            the entry: YAML front matter + guide
  <id>/<provider>-versions.tsv  full version index, where the source is versioned
  <id>/<id>_profile.py      our profiling code for that source
  <id>/profile/             profiling outputs quoted by the entry
  <id>/*.sql, *.py, *.R     tested extraction recipes and checks
resources/tools/            source-independent tools (data_mirror.py: Zenodo, Figshare)
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
| `registered` | Free account needed; terms limit use or redistribution | No, unless the terms allow local copies (Barry decides) |
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
source that lacks such an archive.

## Entry template

Front matter carries the fields an index needs; the body carries the guidance.
Keep values factual and dated. Use `unknown` rather than guessing.

```yaml
---
id: short-lowercase-id                  # also the mirror directory name
name: Full name (ACRONYM)
kind: database | compilation | deposit
status: active | frozen | retired       # frozen = no updates since last_update
last_update: YYYY-MM-DD                 # newest content we can see
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
6. Write the entry; quote our numbers, cite theirs.
7. Have the entry reviewed independently before treating it as settled.

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
- *Profile many versions; mirror few.* The year-end series was worth
  profiling, but keeping all 372 snapshots locally was not: Zenodo preserves
  them, and forward-looking work uses the latest (Barry, 22 October). The mirror
  keeps the 13 snapshots the profile depends on. Zenodo serves about
  0.2–0.3 MB/s per connection; Figshare about 3 MB/s.
