# Verification of the wording revision

Reviewed commit: `646353b090c6d6f68b4a4ec11ce9be71b4c12950`.
Scope: verify W01–W17 from the [initial triage](2026-11-08-wording-review.md).
Main Codex integrated the two original `gpt-6.1-sol` reviewers' checks of
their revised passages, and independently checked the ledger additions,
scanner behaviour, canonical checks and PDF page counts.

**Result: thirteen findings close; four remain partially open.** The main
scientific corrections are implemented. In particular, brief finding 5 now
states two separate observations about different targets and designs; it
does not rank the extinction-bound method against PyRate. The remaining
work is confined to W04, W10, W16 and W17 below.

This is verification, not a manuscript revision. Manuscript sources,
estimands, ledger, bibliography, active scanner configuration and PDFs were
left unchanged. A tested scanner configuration is supplied as a **proposal**.

## Closure against the triage

Locations refer to the revised commit and are relative to
`papers/infrastructure-audit/manuscript/`, unless stated otherwise.

| ID | Status | Checked revision and remaining scope |
| --- | --- | --- |
| W01 | Closed | `text/main.md:163` and `estimands.md:90` distinguish sparse, dense and targeted controls; `brief.md:40` pairs sparse count with its own maximum. |
| W02 | Closed | `main.md:244` and `estimands.md:169` identify the 2026 synthetic proof example, numerical tolerance and unresolved figure provenance; DOI corrected. |
| W03 | Closed | `main.md:187`, supplement audit trail and guide trap 5 leave width calibration and the cause of the shift unresolved. |
| W04 | Partial | `brief.md:49` now separates targets/designs and retains the failed gate. GRIWM remains under the wrong-answer heading at `brief.md:39`. |
| W05 | Closed | `main.md:121` and `brief.md:32` concern dated snapshot membership, not present-day access or reconstruction. |
| W06 | Closed | `main.md:140` and `estimands.md:68` describe the actual recorded-depth/cross-source deletion predicate and retained best-source rows. |
| W07 | Closed | `main.md:77`, supplement and guide now make independence check-specific and identify reuse of the INDITEK harness. |
| W08 | Closed | Retained inputs and the unvalidated public cold rebuild are disclosed; recorded commands replace universal replay promises. |
| W09 | Closed | `main.md:111` and `:170` list missed examples without inventing a continuous interval. |
| W10 | Partial | Comparable denominator, article tolerance and exact-tie sensitivity are corrected. Universal-age wording and incomplete brief/guide qualifications remain. |
| W11 | Closed | PBDB uses the later-snapshot threshold; plate-model cohorts, model names, nonmonotonic spread and frame limits are stated. |
| W12 | Closed | Initial catalogue and later findings are distinguished in article, supplement and brief. |
| W13 | Closed | Assumptions separate measured input/support changes, untested published consequences and unknown provider knowledge. |
| W14 | Closed | Unsupported cost/prevalence claims are removed; correspondence is described as reviewed snapshots. |
| W15 | Closed | Recorded actor attribution, synthetic example, GRIWM description and FR2 categories are corrected; the remaining brief heading is tracked under W04. |
| W16 | Partial | Command working directory and interpretation-aware invariant are corrected; front-matter paths contradict the newly stated path root. |
| W17 | Partial | GitHub-token detection is restored inside the bibliography, as claimed. A different non-citation generic-key control is still suppressed by the global pattern. |

## Four residuals and concrete repairs

### W04: the comparison is repaired; the GRIWM heading is not

At `text/brief.md:39`, the heading still says “Some software gives wrong
answers in specific situations”, followed by two numerical defects and
“A third reports a range” at lines 42–44. The third item is GRIWM's
conditional uncertainty target. Its revised description is correct, but
grouping it under that heading still implies a wrong answer.

A small repair is sufficient:

> Software checks found errors and clarified what outputs mean.

Alternatively move the GRIWM clarification out of the wrong-answer finding.
Keep the corrected finding 5: the targets/designs are now distinct, two
simulated groups are named, and the failed agreement check is retained.

### W10: complete the age-comparison qualification

At `text/main.md:153`, “each with a stored age. We recomputed each age”
remains false as a description of the snapshot. The source receipt includes
4,712 samples undated by both routes, 469 dated only by recomputation and
294 dated only in storage. The following comparable count of 56,387 is
correct and does not require the universal claim.

Proposed replacement:

> The snapshot holds 61,862 samples. We recomputed ages where current tie
> points permitted. Of the samples, 56,387 have both stored and recomputed
> numeric ages.

The article's subsequent threshold and exact-tie sensitivity are correct.
At `text/brief.md:37`, retain a short qualifier such as “under the stated
interpolation rule”. At `text/for-agents.md:41`, state the operational
definition: differences **greater than 0.01 Myr**, first age at exact depth
ties; eight discrepancies disappear with the other exact-tie choice, which
does not change all between-tie interpolation segments. This qualification
is already correct in `estimands.md:82` and should reach the guide's result
summary.

### W16: make front-matter paths agree with the declared root

`text/for-agents.md:15` now declares front-matter paths repository-relative,
but `human_paper`, `claims_ledger` and `interpretation` at lines 5–7 still
start with `manuscript/`. Those paths do not exist from repository root.
Prefix their main paths with `papers/infrastructure-audit/`, or explicitly
declare those three fields paper-relative. `governing_docs` already uses
repository-relative paths. The build command's `cd` is correct.

### W17: retain non-citation generic-key detection too

The claim that a synthetic `github-pat` remains detectable inside
`references/refs.yaml` is reproduced. That closes the old blanket path
exclusion, but not the whole finding. The revised global regex is unanchored:
the permitted `key:` substring also occurs inside `api_key:`. A non-citation
synthetic value with an author/year-like prefix and random suffix is
detected by defaults but suppressed by the revised allowlist, in both an
`api_key` and a bare `key` field outside the bibliography.

| Probe | Revised active configuration | Proposed exact-match configuration |
| --- | --- | --- |
| Twelve real citation identifiers | Suppressed | Suppressed |
| Synthetic provider token, ordinary file | Detected | Detected |
| Same provider token, bibliography | Detected | Detected |
| Non-citation generic `api_key` control | Suppressed | Detected |
| Non-citation bare `key` control | Suppressed | Detected |

[Proposed configuration](2026-11-08-gitleaks-proposed.toml) uses anchored,
exact matches for the twelve verified public citation identifiers. It was
tested against the real generated bibliography plus both generic controls
and both provider controls. It is not installed as the root configuration.
If adopted, additions to the bibliography should be reviewed before adding
their exact citation matches.

The [reproducible probe](2026-11-08-scanner-probe.py) creates deterministic,
non-live controls in a temporary directory and emits finding metadata only:

```sh
python3 papers/infrastructure-audit/docs/audits/2026-11-08-scanner-probe.py
```

At the reviewed commit, `reviewed_generic_controls_detected` is false and
`proposed_generic_controls_detected` is true. After a safe active-config
revision both should be true. The probe changes no active configuration,
uses no credential issued by a provider and makes no network request.

## Verification evidence

- `make -C papers/infrastructure-audit/manuscript check` passed: all 22
  claims cited, zero errors/warnings, lint and reference audits passed.
- C096's added sparse maximum exactly matches
  `case05_admtools.json`: **2.995776523137465** Myr.
- C040's added derived denominator is independently reproduced:
  **52,276 + 2,475 + 683 + 953 = 56,387**. The original evidence remains
  pinned to `501f17d`; no new underlying experiment was claimed.
- Committed PDFs have **two/nine/four A4 pages**. The revised text and
  nearby result statements were reviewed for regressions by the original
  two reviewers. No new major article/estimand regression was found.
- Scanner default/revised/proposed comparisons were executed using
  deterministic synthetic controls. Raw report tokens are not reproduced;
  the companion JSON retains only rule/file metadata and outcome booleans.

The original fits, simulations and package campaigns were not repeated.
Figures, journal choice, contacts and release remain outside this
verification task.

Next: Claude — close W04, W10, W16 and W17, then rerun the document checks.
