# paleodata: local mirror of palaeobiological data sources

Read-only private research copies of data sources catalogued by EPRP
(Extinction and Paleontology Research Programme), under mixed terms: open
licences, non-commercial or no-derivatives licences, sources that state no
licence, and an in-copyright scan. The catalogue, with each
source's contents, provenance, access routes, strengths and pitfalls, is in
the private repository `BWBrook/eprp` under `resources/sources/`. This file is
a copy of `resources/sources/paleodata-README.md` there.

## Layout

```text
<id>/versions.tsv        every version the provider offers (index, not all mirrored)
<id>/raw/<version>/      unchanged source files + MANIFEST.json (read-only)
<id>/derived/<version>/  reproducible conversions; safe to delete and rebuild
<id>/mirror.log          fetch log
_tools/                  read-only copies of the tools that wrote raw/
```

## Rules

- Never modify, rename or delete anything under `raw/`. To correct a mirror,
  add a new version directory and record why in the catalogue entry.
- Verify inputs against `MANIFEST.json` (sha256) before an analysis, and cite
  the version directory and its DOI in that analysis.
- Write analysis outputs to the analysing project, not here. `derived/` holds
  only conversions that committed code can rebuild from `raw/`.
- Licences travel with the data: each `MANIFEST.json` records the terms as
  stated (or "none stated"). Being here does not grant reuse or redistribution:
  check the source's catalogue entry and manifest before either.
- Nothing here is hosted for public use. Barry W. Brook, 23 October 2026:
  "Licence overrides confirmed, universally for the EPRP. Mirroring locally is
  always okay for us: we're not hosting anything here for public use, except
  perhaps later for the frameworks, but not the actual source files."
- [Detail withheld pending disclosure to the data custodian.]

Maintained by EPRP agents (Claude, Codex) for Barry W. Brook. Created
22 October 2026.
