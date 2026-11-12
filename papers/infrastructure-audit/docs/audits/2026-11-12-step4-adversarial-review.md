# Step 4: adversarial manuscript review

12 November 2026. Review of `8ad22d8`, accepted at Board 160/3306 in reply
to 3303. Main Codex checked Methods, provenance and the port; two bounded
GPT-6.1 Sol reviewers checked disjoint Results/Table 1/caption and
framing/Discussion/limitations scopes. Manuscript sources, reconstruction,
ledger, references, metadata and build settings were read-only.

**Recommendation: approve with one targeted wording change.** The hard edit
preserves the case-specific estimands. The six statements of the main message
are defensible, and no material caveat creep was found. Keep the structure and
the lean text; no further general rewrite is warranted.

## Finding and disposition

| ID | Severity | Evidence and consequence | Minimal correction | Owner |
|---|---|---|---|---|
| S4-01 | MINOR; repair before closing the text review | `manuscript/text/main.md:254–255` says the two TorsvikCocks2017 routes differ by an age-specific rotation, “consistent with the two reference frames its authors distinguish.” The hard edit joins two statements that the revised 3c kept separate: a geometric result consistent with different frames, and the authors' documented frame options. C123 does not identify the archived service's frame setting. `manuscript/text/supplement.md:71–74` correctly preserves that uncertainty. | Say **“consistent with a reference-frame difference (Supplement S2).”** Keep the documented frame pair as context in S2. This identifies the supported relation without adding a caveat to Results. | Claude |

Evidence: `evidence/replay-20261108/software/README.md:14` distinguishes the
fresh local reconstructions from retained web-service responses and limits
the geometry to an approximately rigid route discrepancy. The revised
`reconstruction/3c-full-draft.md:258–260` likewise separates the geometric
observation from the documented frame pair. No geometry needs rerunning.

## Answers to the three review questions

**Did the hard edit or definitions change an estimand?** Apart from S4-01's
frame attribution, no material change was found. The glosses for pinned
inputs, modal base age, mean absolute paleolatitude, capture histories,
GRIWM, PyRate and range-end bounds preserve the calculated objects. The
following prior repairs remain closed:

- NSB's total is sample records, and its disagreement denominator is the
  56,387 comparable ages.
- fossilbrush lists discrete missed values and includes threshold equality.
- Sparse/dense admtools counts and maxima remain paired with their own
  controls; the targeted probe remains separate.
- The capture-history comparison retains its intact binary comparator.
- INDITEK retains rejected proposals, successful vector replay, rescoring
  under deposited observations and a separately written scorer. It assigns
  no cause to the saved-score disagreement.
- PyRate and range-end controls retain different targets and designs. GRIWM's
  interval meaning and random-state effect remain distinct findings.
- Caption populations retain full-precision paired Triton differences and
  the age-specific plate-model cohort. C125's model sensitivity remains
  distinct from C123's route geometry.

**Do the repetitions overreach?** No. The summary describes source/known-answer
checks; the Abstract states demonstrated auditing capability; the Introduction
describes program-scale breadth; Results reports the selected cases across
four families; Discussion states their practical consequences; Conclusions
states the demonstrated capability and three distinct future tests. None
claims defect prevalence, exhaustive infrastructure coverage, superiority to
human auditors, economic advantage or general scientific reliability.
“Systematic checks” describes the organized checks, not a population-sampling
design. The matched human comparison and downstream replay remain future work.

**Have caveats crept outside Limitations?** No material instance was found.
Named versions, dated snapshots, exact-tie conventions, two simulated clades,
conditional interval targets and reconstructable cohorts identify methods or
estimands. The eight-sample exact-tie sensitivity is a result. Calling a
proposed transfer a proposal preserves its status. Count-only handling,
third-party licenses and AI-role disclosure belong where reported. Keep
these statements in place. The general limits on selection, downstream
scope, independence, calibration, causes, public rebuilding and disclosure
are already consolidated at `main.md:316–333`.

## Actor wording: reviewed, not a false-provenance finding

One reviewer initially flagged “checked by a second agent” in the Abstract
(`main.md:21`) and the Introduction's corresponding question (`:60`). Main
challenged that interpretation against the retained role records: cases
11/12 received later bounded software/calibration reviewer checks, including
integer-polynomial convolution and separate scoring. The reviewer agreed
that no case lacking a second actor had been identified and withdrew the
material finding. A second session/subagent need not mean a different provider.

Methods (`main.md:113–119`) and S2 now describe the relevant routes adequately.
Optional precision edits are **“checked again”** in the Abstract and **“what
changed during replay and review”** in the Introduction. These are not required
corrections to demonstrated provenance, and they add no limitation. The
existing independence limits must remain check-specific.

## Verification and remaining scope

Executed `make -C papers/infrastructure-audit/manuscript check`: 22 supported
claims, 22 cited, zero errors/warnings; source-glyph checks passed across six
files; manuscript lint/reference audits passed for main, supplement and brief.
The article cites 32 keys from a 33-entry bibliography; the unused Raup entry
remains passage-pending. Pandoc citeproc with the selected CSL also completed
without warnings. These checks establish numeric/citation consistency, not
the semantic correctness of every sentence or the alignment of the old brief.

The makedoc pin matches the installed checkout; its only commit beyond the
old pin is the adjacent-target DOCX write fix. Human-only author metadata is
now implemented. PDF metadata confirms twelve A4 pages; no full PDF build or
visual layout review was rerun. Figure meanings were reviewed, not generated
plots. No source analyses or scientific replays were rerun.

The already reported follow-ups remain separate: prepare the three figure
inputs and draw the figures; realign the brief and agent guide; obtain Barry's
final human declarations; address the book-page suffix. This review does not
open another general prose pass or authorize release.

Next: Claude — narrow the reference-frame wording, then continue the outstanding figure and product work.
