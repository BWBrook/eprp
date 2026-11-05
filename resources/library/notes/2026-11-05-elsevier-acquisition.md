# Elsevier acquisition and restricted source checks

Codex, 5 November 2026, Australia/Hobart. Acquisition is in execution;
scientific re-reading remains partial.

Barry authorised proceeding on Claude's suggested library tranche, including
Elsevier acquisition, agenda classification and source checks, with downloads
in tmux on the campus server so the laptop can disconnect. Board 76/2895
records accepted ownership. References Codex owns this tranche; the programme's
other scientific allocations are unchanged.

## Corpus and custody

A fresh offline catalogue from the canonical open/Wiley store contains 28,850
works. Of 1,580 works with Elsevier DOI prefixes `10.1016/` or `10.1006/`, 247
have open copies and 1,333 lack them. Seventeen are excluded non-article types,
leaving 1,316 eligible existing works. Poon & Crampton (2026), explicitly
requested by Barry but missing from the catalogue, adds one: **1,317 selected**.
Its DOI `10.1016/j.cub.2026.02.026` and OpenAlex ID `W7137268908` were verified
against Crossref and OpenAlex. Its public metadata and a new seed were added
to the canonical store; no subscription text was transferred there.

The run prioritises the named sources, then cited/core, Barry-2003 and agenda
tiers, then neighbours and the remaining corpus. Existing open copies are
skipped. A new campus-only store holds the subscription acquisition:

```text
deep:/data/codex/paleodata/elsevier-library/
  catalogue.tsv
  priority-ids.txt
  tdm/elsevier/
    xml/                      original responses, read-only
    text/                     derived body text, read-only
    manifest.tsv              source and extraction hashes, structure, provenance
    attempts.tsv              outcomes without article text
    quarantine/               rejected payloads and finite access diagnostics
    provenance/               private forwarded approval, use case, input hashes
    derived/                  private question candidates and thematic summaries
    snippet-exports.json      persistent DOI-level output accounting
    smoke.log                 initial finite test
    run.log                   detached fetch progress
    completion.json           written when the fetch and mining commands exit
    held-coverage.tsv         metadata-only coverage receipt at exit
```

The canonical open/Wiley store remains on Nectar. Its manifest and search
indexes do not ingest these Elsevier copies. Everything restricted, including
correspondence, indexes, question wording and failed responses, stays beneath
the campus store's `tdm/elsevier/` subtree. The
[backup helper](../../tools/paleodata_backup.py) excludes any `tdm/elsevier`
subtree and the combined TDM index and sidecars. It also rejects a source root
inside those restricted areas before traversal. The reviewed helper was
deployed before acquisition; no recurring backup was found in checked schedules.
No existing backup generation was changed or deleted. Direct transfers must
honour the same custody rule.

## Retrieval and output controls

[elsevier.py](../elsevier.py) retrieves `FULL` XML using the existing private
key in an HTTP header. It refuses credential redirects and symlink ancestry,
checks the core metadata DOI, requires a substantial body or rawtext payload,
and records original/extracted hashes. A structured body establishes retrieval,
not content completeness. Rawtext is explicitly marked as unsegmented.
Metadata-only HTTP 200 responses do not qualify.

Requests have at least three seconds of spacing, persisted across restarts.
Authentication, rate-limit, exhausted-quota, server and transport failures stop
the run. `Retry-After` is retained. Successful copies are checksum-verified and
skipped on resumption; failed items require deliberate `--retry-failed`.
Repeated malformed responses also stop the run. Exceptions are sanitised so
server text cannot leak through logs.

Barry's 5 November instruction accepts the reported approved use case:
extracted facts/numbers, metadata and bounded DOI-attributed snippets may reach
agents. The private approval receipt records the exact forwarded approval
excerpt and the user-authorised use-case account, with hashes. **The original
MIME approval and complete submitted application were not recovered from the
connected mailbox**; the archived records are labelled accordingly.

The query command requires that private receipt and its matching source hash.
It allows a conservative cumulative **200 excerpt characters per DOI**, across
invocations and queries, with source credit, DOI link and the required rights
notice. This is stricter than treating each query as a fresh allowance. It
does not permit corpus upload or reconstruction through repeated excerpts.
Wiley remains count-only. Question wording stays out of this public repository.
See Elsevier's [TDM licence](https://www.elsevier.com/about/policies-and-standards/text-and-data-mining/license)
and [API specification](https://dev.elsevier.com/documentation/ArticleRetrievalAPI.wadl).

## Live test and detached execution

The initial nine-request test retrieved eight structured XML bodies, totalling
2,963,298 original bytes. These include all three agendas, Rampino & Caldeira,
Poon & Crampton, Boag et al., Chen et al. and Yang et al. Body sizes ranged from
1,414 to 9,853 words; neither these counts nor retrieval certify completeness.

Kelley et al. (2001), `10.1016/s0031-0182(00)00207-8`, remains unavailable:
`FULL` returned HTTP 400, while a finite `ENTITLED` diagnostic returned HTTP
401 stating that the resource was not entitled. Default-view retrieval gave
metadata only. DOI case/encoding and a Crossref-provided PII route did not
establish full-text access. No further retries of this item follow in this run.
This is an access limit, not absence of evidence.

The main job started at **14:31 AEDT** in tmux session
`eprp-elsevier-20261105`. It resumes the held set and skips the recorded failure.
It runs entirely on `deep`; laptop disconnection does not terminate it.
The final command reruns private agenda mining and writes completion/coverage
receipts, including whether the fetch stopped early. Inspect with:

At **14:35 AEDT**, the restricted manifest held 62 works (19,520,380 XML bytes),
with seven HTTP 400 outcomes across 69 recorded attempts. Ten held works used
rawtext rather than structured-body extraction. This is an interim checkpoint,
not a completed-corpus count. The canonical Nectar store had no Elsevier TDM
subtree or Elsevier TDM manifest rows at that check.

```bash
ssh deep 'tmux attach -t eprp-elsevier-20261105'
ssh deep 'tail -n 12 /data/codex/paleodata/elsevier-library/tdm/elsevier/run.log'
```

After checking any stop reason, resume the same corpus with the deployed
`elsevier.py fetch`, explicit `--catalogue`, `--store`, `--ids` and
`--interval 3`. Do not use `--retry-failed` merely to resume successful work.

## Agenda and claim-check results

[mine_elsevier.py](../mine_elsevier.py) retains question-mark candidates and
deterministic keyword themes in the restricted store. Initial counts are 15
for *Cell*, 29 for López-García & Moreira, and six for Abdelhady et al. These
are **unreviewed candidates**, including possible rhetorical questions and
fragmented sentences, with possible missed headings. They are not published
question totals. Labels include unclassified candidates; no canonical agenda
inventory or register ranking changes follow.

The following separates access from the actual depth of rechecking:

| Source / DOI | Current check and limit |
|---|---|
| Rampino & Caldeira 2025, `10.1016/j.earscirev.2025.105100` | A bounded body excerpt confirms the authors report a 31 Myr spectral maximum for stage-boundary ages over the last 253 Myr. Their reported significance is not independently validated; age uncertainty, spectral procedure and biological interpretation remain unchecked. |
| Poon & Crampton 2026, `10.1016/j.cub.2026.02.026` | A bounded body excerpt supports the reported bidirectional signal-suppression statement. Methods, data and alternative interpretations have not been independently reanalysed. |
| Boag et al. 2021, `10.1016/j.cub.2021.04.021` | Structured text acquired. The bounded excerpt confirms metabolic-theory context, but does not establish the full shape result or absence of spatial-bias control. Those earlier claims retain their previous evidence level. |
| Chen et al. 2020, `10.1016/j.gca.2020.02.035` | Structured methods text acquired, beyond the earlier metadata-only API response. The limited excerpt identifies mineralogical analyses; phase controls and weathering/chronology interpretation remain queued. |
| Yang et al. 2022, `10.1016/j.epsl.2022.117861` | Structured version acquired. The earlier open-manuscript check already covered selected sections; this run does not independently recheck tables, figures or the model. |
| Kelley et al. 2001, `10.1016/s0031-0182(00)00207-8` | Entitlement not established. Predator-efficiency measure remains unverified. |
| van de Velde et al. 2020, `10.1016/j.gca.2020.02.021` | Already held openly. Independent recheck supports prescribed transport without an animal demographic state: Appendix 1, printed pp. 35–37, Eqs. 1, 4–6; p. 40, all 14 state variables; scenarios pp. 43–45. The rival evidence is explicit conceptual colonisation feedback in §4.3, pp. 27–28/Fig. 8. Thus the mechanism is conceptually occupied despite missing demographic coupling. |
| Schachat et al., `10.1016/j.revpalbo.2021.104564` | Already held openly as the 25 October 2021 bioRxiv preprint. §4, pp. 15–17 proposes the ordinary-change counterfactual; Conclusions pp. 21–22 leaves it unresolved. §6, p. 20 nevertheless performs a coverage-based rarefaction reanalysis of before/after damage diversity. “No extinction analysis” would be false. Identity with the final 2022 article remains unchecked. |

The latter two checks used only the permitted open texts. Their text SHA256s
are respectively `e612bc114cf362313c27fc849b5acdd81ce2ad03c925cb665d5a808d1cb0f985`
and `9db731093057ad846ea12ad1a7b005c2167c71dde90beaa15a43dd7d08ae3e5c`.
No restricted article wording is reproduced here. Historical register entries
remain unchanged; this dated source record supplies the qualifications.

## Verification and next owner

Forty library tests pass, including 22 new Elsevier tests, plus 12 backup
tests. Tests cover metadata-only responses, DOI mismatch, body/hash retention,
resumption, pacing, rate-limit stops, malicious XML, symlink custody, bounded
exports and backup transfer exclusions. Independent review exposed the backup
root and DOI-accounting defects; both were fixed before launch. A deployed
custody smoke and the live retrieval test passed. The miner's keyword labels
have only a small synthetic smoke check, not semantic validation.

References Codex next inspects the detached completion receipt, separates
entitlement/format failures from successful retrieval, curates agenda candidates
and completes the pending source checks within the approved output limits.
Other publishers' and Wiley's permissions remain separate and outstanding.
