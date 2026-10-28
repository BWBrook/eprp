# Fossilworks interval acquisition, 28 October 2026

**Parser correction, 28 October:** the acquisition audit below interpreted
literal double quotes as CSV quoting. The provider files are literal tab- and
line-delimited text; an independent recheck found every selected sheet
rectangular under that interpretation. The old parser merged two Middle
Pleistocene register rows and changed quoted text elsewhere. Correcting it
gives 26,046 register rows across the selections, not 26,045; the Middle
Pleistocene register has all 1,843 declared rows, including the
*Capricornis* count previously described below as absent. There are 34 matrix
cells differing from register sums, not 35. The Middle Pleistocene reference
sheet still lacks two references. The historical audit and its numbers are
retained below as the original record, not as current findings. See the
[corrected interval audit](interval-download-literal-2026-10-28.json) and
[corrected interval table](interval-download-literal-2026-10-28.tsv).

All 20 fossil interval selections visible in the public download form were
retrieved sequentially. Each retained its original register, species, samples,
references and matrix sheets: **100 selected source sheets**, with no empty
selection or omitted visible interval. All five files in every selected bundle
match their second GET byte for byte. No data have been assembled,
deduplicated, harmonised or corrected.

## Location and integrity

- Read-only source: `deep-server:/data/paleodata/fossilworks/raw/2026-10-28-intervals-v2/`.
- Audit: `deep-server:/data/paleodata/fossilworks/derived/2026-10-28-intervals-v2-audit/`.
- The frozen manifest records 432 source, verification and metadata files.
  Every SHA256 was checked with zero failures. Its own SHA256 is
  `07463922820e97aa5bc44f2394236085fdb54d6e1f403f5a1cd086dad8a2d1e6`.
- Each interval has a numbered directory and each attempt retains its POST
  parameters/body, results page, original TSVs, verification copies, per-request
  UTC start/end times, HTTP headers, byte counts and SHA256 values. The exact
  acquisition-script versions are retained inside the snapshot.
- The live form and FAQ are retained. Data terms are CC0 according to the FAQ.
  This is a dated observation of public exports, not a provider release.
- `acquisition/aborted-2026-10-28-intervals-v1/` is explicitly incomplete
  diagnostic evidence outside `raw/`; it is not a second accepted snapshot.

The [interval receipt](interval-download-2026-10-28.tsv) lists every selection,
selected attempt, row count, distinct sample-ID count, duplicate summary-row
count and matrix/reference check. The [full audit](interval-download-2026-10-28.json)
pins the manifest and all 100 selected original-sheet hashes. The sum of the
register row counts across the interval exports is 26,045; that sum does not
establish unique occurrences or independent observations. Selections can
overlap, and no cross-interval identity or duplication audit has been done.
The interval labels retain the provider's spelling and granularity, including
`Pleistocene - Holocene`, subdivisions of epochs, and the Maastrichtian and
Campanian stages.

## What the checks establish

All 20 bundles have the correct selected interval labels, matching register
and sample ID sets, structurally rectangular sheets, and stable second-copy
hashes. Five also match the result-page row counts and reference identifiers:
Holocene, Pleistocene–Holocene, Late Pleistocene, Early Oligocene and Middle
Palaeocene. The remaining 15 contain reference identifiers used by register
and sample rows but absent from the reference sheet. Exact identifiers and
expected/observed counts remain in the full audit.

Middle Pleistocene additionally declares 1,843 register rows and 63 references
on its results page, while the files have 1,842 and 61. Referenced IDs `4446`
and `4509` are absent from the reference sheet. Its matrix contains a count of
4 for *Capricornis sumatraensis* at Tam Hang South (2007), with no matching
register count. Repeated requests preserved the same discrepancies. These
are unresolved source inconsistencies; nothing was inserted or repaired.

The matrix contains named species only. Its sample-name columns can occur in
a different order from rows in the sample sheet. Some sample sheets repeat
identical summaries for the same sample ID; matrices contain one column for
that identifier. Those repeated summaries are retained and counted separately
from distinct sample IDs.

Across interval exports, 35 matrix cells differ from sums of register rows
with the same species/sample name. In 34 cases the matrix equals the last
matching register row. This is an observed correspondence, not verification
of provider implementation. For example, Holocene *Canis lupus* at McNichol
Creek (midden) has register counts 9 (commented “domestic dog”) and 1; the
matrix contains 1. Holocene alone has 19 such differences. The remaining
case is the Middle Pleistocene discrepancy above. All differing cells are
retained in the [per-interval comparisons](interval-matrix-comparisons-2026-10-28/).
No matrix has been substituted for the register or repaired.

## Mutable exports and assessment corrections

All queries selected exactly one visible interval, omitting taxonomic and
geographic filters. The acquisition client used no cookies or authentication.
No POST queries overlapped. Generic paths such as `/eco/downloads/register.txt`
changed after subsequent selections. A [second-client probe](public-path-probe-2026-10-28.json)
from WSL, also without cookies, retrieved the same Campanian register generated
by the deep-server client. These are publicly shared mutable paths; uncontrolled
concurrent writers remain a limitation. No concurrent-write experiment was run.
This interval procedure avoided the broad-export HTTP 504 observed earlier.

The first diagnostic run exposed a local validation variable-order error and
was stopped. A subsequent validator initially required matrix column names
to match the multiset of sample-sheet rows, incorrectly rejecting repeated
summaries for the same sample ID. Its original assessments remain untouched.
Later assessments explicitly distinguish those source duplicates from mixed
exports. Completed bundles were reused on resume. Repeated stable reference
omissions were then classified separately from unstable downloads, allowing
the remaining intervals to proceed once each.

**The authoritative final classifications and selected attempts are the full
audit and interval receipt linked above.** For early intervals, original
`assessment.json` files can contain superseded rejection labels; the separate
post-acquisition reassessments and final audit record the correction. They do
not change source files. A successful acquisition is distinct from complete
source referential integrity and scientific readiness.

An independent Codex reviewer verified all 100 selected sheets against the
manifest and second-GET copies, independently reproduced the 19 Holocene
matrix differences, and rechecked the Middle Pleistocene 1,843/63 declared
versus 1,842/61 downloaded counts. This review checked retained evidence; it
did not repeat the provider POST requests.

## Reproduction and next work

Run [acquire_intervals.py](../acquire_intervals.py) against a **new** destination
to acquire another dated observation. Use `--resume` only for an unfinished
acquisition; the script refuses to modify a finalized manifest. Then run
[audit_snapshot.py](../audit_snapshot.py) with the source directory and a new
audit-output directory. The audit checks all manifest hashes and reads the
retained source sheets without altering them. An audit directory is derived
evidence and can be rebuilt.

The next task is to decide how to represent the original row identities,
repeated sample summaries, taxon qualifications, missing references and matrix
discrepancies before assembling anything. Provider contact has not occurred.
