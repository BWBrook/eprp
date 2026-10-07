# EPRP foundation — 7 October 2026

Author: Codex. Source of remit and permissions: Barry's launch message in the
Codex Desktop chat on this date. The following is a paraphrase, not a transcript.

## Mandate

Create an ongoing collaborative resource hub for quantitative palaeobiology,
existing literature/data, ideas, criticism, planning and reusable research
resources. Emphasise the reciprocal relevance of geological extinctions and
the modern biodiversity crisis while retaining broader scope. Primary research
will live in downstream projects. Work with Claude through Correspondence,
allocate tasks by mutual consent, preserve productive disagreement and reserve
Barry's scarce attention for consequential judgments. Bundled commits and
pushes are authorized. Closing chat replies require a Hobart timestamp.

## Observed starting state

- `/home/bwbrook/git/eprp` was empty and was not a Git repository.
- No active EPRP Correspondence section existed. Codex created `eprp` and
  opened discussion 76 with message 1101. No prior EPRP discussion was present.
- Correspondence reported API version 2 and configured participant `Codex`.
  Its current interface and recovery documents were read from the Mac mini.
- The public ORCID API returned Barry W. Brook's identity and research biography.
  The biography was last modified in 2018; its historical output counts were
  not adopted as current facts. Programme direction comes from the launch brief.

## Structural choices

One shared instruction file with a Claude entry point; one status/ownership
record; a programme roadmap and evidence conventions; a small source register;
places for literature, ideas and data; and this dated record. No application,
workflow engine, CI, package environment or bulk data mirror was introduced.

These are reversible Codex implementation choices. The charter preserves
Barry's remit; detailed source choices and the first orientation design remain
agent proposals. Claude was invited to independently challenge the framing and
offer literature/methods ownership, not assigned work without agreement.

A bounded independent Codex review recommended a clear project-promotion
boundary, explicit coverage gaps, concrete discriminating tests, minimal
provenance, routine agent autonomy and lean coordination. Incorporated those
points. This review is distinct from the still-pending Claude critique.

Barry subsequently specified GPT-6.1 Sol for future Codex subagents, with effort
appropriate to the task. The completed foundation critique had used the
GPT-5.6 Sol medium-scientist preset before this instruction. The shared agent
instructions now preserve his updated preference; future delegations must follow it.

## Source access observations

Checks from WSL on 7 October 2026 (around 03:22 UTC / 14:22 AEDT):

| Exact request | Observed response | Limit |
| --- | --- | --- |
| `https://paleobiodb.org/data1.2/` | HTTP 200, HTML, 23,472 bytes | Documentation root only; browser retrieval separately returned 403 |
| `https://api.neotomadb.org/swagger.json` | HTTP 200, parsed JSON, 100,667 bytes, `2.0-oas3`, 77 paths | Specification only; no scientific record extraction |
| `https://macrostrat.org/api` | HTTP 200, parsed JSON, 1,687 bytes, API version 2 | Root metadata only; data routes and joins untested |

These were live `urllib.request` GETs with a 15-second per-request timeout and
a 1.5 MB read ceiling, using `User-Agent: EPRP-orientation/0.1`. The requests
returned less than the ceiling. Source documents were inspected in memory;
no frozen data snapshot is implied. The palaeoverse package homepage was read
through web retrieval; software was not installed or executed. Source links,
verification limits and open audit questions are retained in the resource register.

The ORCID browser page needed JavaScript; its public API worked. An attempted
PaleoClim homepage retrieval was inaccessible to the browser tool; no claim
about that resource's present availability or suitability follows, and it was
not added to the seed register on that evidence.

## Closeout

Foundation checks passed: all 23 local Markdown links resolved, all four TSV
resource identifiers were unique and every required field was populated, and
Git ignored the intended credentials/data/scratch/environment paths. No software
test suite was appropriate for this documentation and catalogue tranche. A
focused content review checked scope, attribution, authority, verification
limits and the new subagent preference. The staged diff is checked before the
bundled commit; its hash and final receipt belong in the discussion handoff.

Git was initialized on `main`. No remote was supplied or configured, so there
is no push or presumed second checkout. This remains a local foundation until
a hosting/synchronization destination is established. No primary investigation,
scientific result or comprehensive review was produced by this setup pass.
