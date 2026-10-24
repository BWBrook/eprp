---
id: chronosphere
name: chronosphere
kind: r-package
domain: data-access
languages: [R]
home: https://chronosphere.info/
repo: https://github.com/chronosphere-info/r_client
paper: []
licence: "CC BY 4.0 (CRAN DESCRIPTION); GPL-3.0 (GitHub repository): conflicting"
release: {version: 0.6.1, date: 2023-08-17, checked: 2026-10-24}
maintenance: {state: active, last_commit: 2026-09-18, checked: 2026-10-24}
tier: T1
validated_uses: []
environment: {route: docker, lockfile: ../bench/env/Dockerfile.r3, image: "eprp-sw/bench-r3:t3 (sha256:44432c89…)", host: deep-server}
blockers: ["[Detail withheld pending disclosure to the data custodian.]"]
related_sources: [pbdb, triton]
eprp_questions: [Q-045, Q-040]
entry: {created: 2026-10-24, updated: 2026-10-24, by: Claude (Opus 5.5), reviewed: "not yet"}
---

# chronosphere

## Summary

chronosphere is an R client for a registry of versioned Earth-system and
palaeobiological datasets on Zenodo: `fetch(src, ser, ver)` downloads a
named version. Its public registry lists 1,171 dated PBDB occurrence
snapshots from 22 November 2019 to 18 October 2026, each with a Zenodo DOI
under CC BY 4.0 ([pbdb_versions.tsv](pbdb_versions.tsv)), which is the
closest thing to a PBDB history that exists (lead L-005).

## Validation

[Detail withheld pending disclosure to the data custodian.]

## Weaknesses and pitfalls

- [Detail withheld pending disclosure to the data custodian.]
- Licence metadata conflict: CRAN says CC BY 4.0, the repository GPL-3.0.
- Series change columns (for example `geological_group` in `occs4`,
  `stratgroup` in `occs2`); check names before joining.
- Queued for the maintainer as [CONTACTS](../CONTACTS.md) S7.

## EPRP relevance

Q-045 (robustness of estimates to future data) can still use the series
as a record of how the PBDB grew, restricted to records public today, with
that caveat stated. Main-agent analyses must not take these files as public
PBDB data (the 23 October PBDB data hold).

## Citation and licence

chronosphere software DOI 10.5281/zenodo.3525481 (from scan A; not
checked here). Each snapshot cites its own Zenodo DOI (`pbdb_versions.tsv`).

## Verification log

- 2026-10-23 `checked`: registry listing (`pbdb_versions.py`).
- [Detail withheld pending disclosure to the data custodian.]
