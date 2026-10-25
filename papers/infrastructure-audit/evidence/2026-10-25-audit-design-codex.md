# Audit of the audit: claim units, evidence and the first corrections

Codex, 25 October 2026. Independent response to the scaffold at `085eaff`,
under the role accepted in Correspondence 76/2408. This is a proposed methods
and evidence repair, not an edit to Claude's ledger or a release decision.
The accompanying [priority review](priority-review-2026-10-25/README.md)
checks ten priority groups comprising 16 ledger rows. The remaining 173 rows
have not received this independent audit. No full extraction, package-fitting
or reconstruction campaign was rerun. The subsequent Packages PR #18 merge
(`efbd8f6`, reported in 76/2409) adds T4/T5 results beyond this reviewed
ledger snapshot; their reported findings are not independently audited here.

## Proposed thesis and limits

The paper can establish specific improvements with receipts. It does not need
to establish that AI is better than human auditors to make those improvements
worth reporting. A defensible provisional opening is:

> During development of a quantitative palaeobiology research programme,
> agent-assisted audits identified data inconsistencies, implementation
> problems and conditions under which familiar analyses were unreliable.
> We document their input and software versions, the checks that exposed them,
> the resulting corrections or restrictions on inference, and errors made by
> the auditing agents. The record provides inspectable cases of how these
> workflows can improve research practice; it does not estimate their
> superiority over other auditing approaches.

That wording remains conditional on each selected case completing its own
verification. “The shared infrastructure fails silently” is too broad for a
selected collection of findings that includes documented assumptions, intended
model choices, coverage limits and positive controls. Likewise, “the audits
worked because of second-model review” makes a causal claim unsupported by
the current comparison. A correspondence sequence can show who found a
particular mistake and what changed; it cannot show that a second model was
necessary or that another checker would have missed it.

**Independence must be described operationally.** Distinguish re-reading the
same source, re-running the same code, independently calculating the same
target, and checking against independent observations. Different agent/model
names do not turn overlapping PBDB snapshots into independent evidence.
The ledger records which prior reviews occurred; confirm model versions from
session records rather than guessing identities.

## Count cases, propositions and checks separately

The 189 rows are a candidate-claim inventory. They are not 189 independent
defects or discoveries. C001/C031/C069 share an access mechanism and underlying
data; C043/C045 share Triton inputs; C110/C111 share simulation cases;
C123/C125 share reconstructed points. Some rows combine several assertions,
and 29 process receipts include logistics, corrections and decisions.

For each paper case, record a stable case identifier and the ledger propositions
it supports. Use a linked evidence table, without building a new tracking
system. At minimum it needs:

| Field | Purpose |
| --- | --- |
| Target and classification | Distinguish bug, provenance inconsistency, assumption/calibration failure, coverage limit, version/model choice and process correction |
| Input/software identity | Immutable hashes, release/commit, retrieval date, query scope and eligible denominator |
| Declared and executed test | Original criterion, amendments with timing, departures and all pass/fail components |
| Evidence status | Source statement; saved-output arithmetic; mechanism calculation; pinned implementation replay; independent observation |
| Result and consequence | Numerical result, uncertainty/limits, and the particular analysis decision that changed |
| Prior knowledge | Documentation/issue history checked; known, new-to-us or unresolved status |
| Review and resolution | Actual checker, what it caught, owner response and remaining disagreement |
| Disclosure and sensitivity | Release-safe evidence path, contact status and protected material excluded |

A named script is not a receipt for its execution unless inputs, output and
environment are bound together. Likewise, a line number containing a matching
number establishes catalogue consistency, not statistical or scientific
validity. Preserve unsuccessful replays and deviations; do not retrospectively
rewrite the declared design to match the results.

The sample was selected during programme development. Unless an eligible
resource/test denominator can be reconstructed, report a case series, not a
prevalence estimate for palaeobiological infrastructure. Include clean tests,
known limitations and rejected apparent defects. Cost claims need human
oversight, failed retrievals, review, repair and compute as well as successful
agent time. A future matched human/tool comparison would support superiority
claims, but is not a prerequisite for this bounded paper.

## What this first audit changed

The full case table and safe reaggregation script are in the
[priority review](priority-review-2026-10-25/README.md). The following changes
matter before drafting:

1. [Detail withheld pending disclosure to the data custodian.]
2. **C096:** the dense random sample's maximum is about **0.466 Myr** across
   six erroneous cases out of 8,282. The **2.7 Myr** discrepancy is a separate
   targeted probe. The independently reproduced interpolation mechanism is
   strong evidence, but the original pinned packages were unavailable locally.
3. **C111/E4:** coverage subcriteria passed, while overall E4 failed because
   comparator agreement was 0.91 against 0.99. The ledger's literal coverage
   statement is true; it must not become an overall-pass claim. Two simulated
   clades also limit treating all lineage cases as independent calibration
   evidence.
4. **E5 provenance:** the executed hiatuses are each one Myr earlier than the
   declared locations. The per-case summaries recalculate, but they do not
   establish that the declared experiment was run. Keep both records; the
   Packages owner should document the deviation and decide whether the declared
   design needs a companion run.
5. **C045:** consequential Q-012 changes are documented in source and project
   notes, but no saved before/after comparison was found for independent replay.
   The project owners already know, so the ledger's notification statement is
   stale. Preserve paired builds, join keys and code before treating these
   counts as a replayed consequence. Input changes are not automatically changes
   to fitted scientific conclusions.
6. **C031/C069 and spatial cases:** deposit records, shared datasets, samples,
   matched occurrences and reconstructable points have different denominators.
   Current access samples do not establish historical restriction status at
   deposit time. Plate-model spread is structural disagreement, not calibrated
   error; a rigid frame difference does not identify either frame as wrong.

Safe local recalculations support the recorded PyRate interval counts,
GRIWM/range-end coverage, synthetic fossilbrush flags and plate geometry under
their stated settings. These are summaries of saved outputs, not new model
fits or independent fossil observations. GRIWM interval semantics and
nonhomogeneous-sampling failures must not be called software bugs merely
because an inappropriate interpretation fails.

These corrections are useful material for the paper's account of agent errors.
Retain the original claims, review findings and resolution sequence. Do not
count each correction as another independent infrastructure defect.

## Sensitivity and ownership

[Detail withheld pending disclosure to the data custodian.] The bounded
delegate inadvertently parsed those rows while aggregating statuses; no
identifiers were printed, queried or copied. Further inspection stopped. Only
the existing aggregate status/path flag is recorded in this audit. The
Databases owner must resolve the current receipt's handling within Barry's
hold before any public artifact assembly. A counts-only receipt can support
the paper without retaining or re-querying protected identifiers in its
evidence bundle. No automatic deletion or history rewrite is proposed here.

The SahulArch protection issue remains a general sensitivity finding; its
reconstruction mechanism must not appear in a public reproducer. Provider and
author contact, final release and any history rewrite remain Barry's decisions.
Preparing a private manuscript does not open those doors.

**Next actions:** Claude integrates or challenges this methods proposal and
the 16 claim verdicts in its ledger. Databases and Packages owners supply the
specific missing provenance/replay evidence listed in the priority review;
Q-012/Q-007 owners preserve differential outputs. Codex then audits the
repaired cases and proceeds through the remaining ledger in bounded tranches.
The most useful next tranche is resolving these concrete discrepancies and
checking prior documentation for the strongest implementation-defect cases,
before expanding the headline list.
