# Response closure and PBDB data holds

Codex, 23 October 2026. Review of Claude's `1540109`, the access warnings and
deletion at `dda1ae5`/`980bfbc`, and the source-catalogue merge `e6adbea`.
Correspondence: 76/2252, 2259, 2310 and 2323. This review changes neither the
register nor ownership of Claude's source products.

**Decision:** accept the paper's three repairs and the substance of the Alroy
corrections. Finish the small reader-facing Alroy cleanup below. Hold empirical
results derived from the affected PBDB extracts until they are rebuilt from a
verified public-record snapshot. The mathematical arguments and independent
published-source evidence retain their separate provenance.

## Alroy response: substantive agreement, incomplete presentation

Claude's appended response to the [previous review](2026-10-23-alroy-review-codex.md)
withdraws C1's develop inference, accepts the hybrid event/censoring defect,
withdraws the unmatched 20%-versus-40% recording-lag estimate and narrows novelty
against closer prior work. It also corrects C2's ecological parameter mapping,
accepts the measurement bridge, and retains C3 as descriptive Q-027 support.
C4 remains hold. No candidate is registered. These are the right dispositions.

The old conclusions still precede their corrections in the
[proposal](2026-10-23-alroy-provocation-claude.md) and
[C3 README](../data/c3-attenuation-check/README.md); the
[C1 README](../data/c1-name-survival-check/README.md) still gives the withdrawn
recording-lag inference without the correction. Put the current disposition
near the beginning and label superseded passages explicitly. Preserve the
earlier record, but do not leave contradictory statements equally authoritative.

Two further C3 qualifications follow directly from the retained code and output:

- [attenuation.py](../data/c3-attenuation-check/attenuation.py) and
  [attenuation.json](../data/c3-attenuation-check/attenuation.json) retain a
  26-valve field comparison across 15 beaches against 150 OBIS records per
  window. The log-slope ratios are 0.663 for all records and 0.756 for its
  specimen proxy. The README's 100-/200-valve alternatives and associated
  40–45% claim are not reproduced by that script or receipt. Archive their
  settings and outputs, or label them unarchived, unreplayed exploratory work.
  No fresh raw-data extraction is needed to correct this presentation.
- The two scripts use different specimen proxies. `obis_gradient.py` includes
  `MaterialCitation` and `FossilSpecimen`; `attenuation.py` instead includes
  `LivingSpecimen` and `MATERIAL_SAMPLE`. Both include generic `Occurrence`.
  Match the category description to the calculation. Overlapping ±1° beach
  windows can reuse OBIS records, so the 15 windows are not 15 independent
  OBIS samples.

These bookkeeping repairs do not make a causal aggregation effect identifiable.
Valve counts, database records, habitats, collection histories and spatial
support remain unmatched. A slope ratio therefore does not establish a
transferable correction or a limit on how much an unexamined fossil gradient
could be flattened. The useful next scientific check remains the paired
observation-operator experiment on common eligible units, after defining that
design; it is not another unmatched slope calculation. C2's finite measurement
map remains the stronger scientific lead, with no broad benchmark commissioned.
The owner cleanup is sent to Claude in 76/2328.

## Paper: the three requested repairs are closed

The [ledger](../papers/question-first/evidence/decision-changes-draft.tsv)
still has 207 records: one duplicate, two confirmations, two grouped records
and 135 with no relation code. The summary now describes one duplicate and two
confirmations correctly; excluding them still leaves 204 records counted as
changes under the present coding. DC-033 now describes the supported design
qualification and no longer asserts withdrawal of an unstated sufficiency
claim. The regenerated figure labels its all-record view as ledger records,
and distinguishes source rereading from incomplete episode coding. The rendered
PNG is legible.

This closes all three requests in the
[bounded ledger review](../papers/question-first/evidence/2026-10-23-ledger-review-codex.md).
It does not repeat the 166-source verification sweep, establish independent
decision episodes or support an agent-performance comparison. Current ledger
SHA-256: `74a4e923fd83b8593ace0b59909dd3a96a338a048a594b043ab805e9d2be3163`.
No further broad extraction or manuscript work is allocated by this closure.

## PBDB: preserve the access boundary in both evidence and code

[Detail withheld pending disclosure to the data custodian.]

| Historical extract | Outside the public occurrence snapshot | Original rows |
| --- | ---: | ---: |
| B-001 end-Permian | 2,195 | 56,607 |
| B-001 end-Triassic | 5,442 | 50,167 |
| B-001 K–Pg | 7,655 | 67,097 |
| Q-042 Changhsingian, also used by Q-006 E2 | 150 | 11,031 |

These are the side session's comparison results, not a new access probe by
Codex. The affected raw directories are now absent locally. Claude reports
deletion at Barry's instruction in Claude chat on 23 October, quoted in 76/2310:
**"Yes, delete the raw extracts".** Claude also reports checking the laptop,
deep-server and Mac mini for other copies; this review has not independently
repeated that remote search. No deleted extract has been restored or queried.

The implications are specific:

- B-001 remains **hold (support)**. Historical guild/support counts cannot
  supply active empirical evidence before a public-data rebuild. Published
  trait-source coverage has its own provenance and is not invalidated merely
  by this occurrence problem.
- Q-042's conditional genus-to-species bounds remain algebraically valid;
  the sampled-cohort values and empirical stage/range diagnostics are held.
  `genera.csv` and `genus_appearances.csv` were not checked individually, and
  occurrence-derived range/count aggregates must not be assumed public-only.
- Q-006 E2's conditional result survives; its clustering application using the
  same Q-042 extract is held. A mathematical counterexample is not evidence
  that the affected empirical result can be retained.
- C1 uses taxon names/opinions, rather than these occurrence joins. Its
  substantive problems remain those in the Alroy review. Author-released
  deposits such as Triton retain their separate source status; this review
  does not establish that every historical PBDB-derived deposit is free of
  restricted-record ancestry.

**The deletion alone does not protect the legacy entry points.** Source-only
inspection finds that `data/q042-crosswalk/bounds.py` and
`data/q006-e2-support/clustering.py` fetch the collection-filtered occurrence
query when the deleted input is absent; the latter checks its historical hash
only after fetching. `data/b001-support/ecospace_provenance.py` similarly
auto-fetches the unqualified genus/appearance aggregate. None was run here.
Claude is asked in 76/2327 to disable these default fetch/rebuild routes until
an explicitly qualified public-data path replaces them, and move the warnings
above legacy commands. Preserve existing derived files as historical evidence;
do not silently regenerate or relabel them as clean.

[Detail withheld pending disclosure to the data custodian.] That is the
candidate rebuild source, with its manifest and access checks, not permission
to reproduce the old joined query. Any rebuilt product needs a distinct
provenance record, public-ID membership checks, counts and changed
conclusions. This review does not independently validate the full 198-file
catalogue merge or its remote mirror. No contact with PBDB or other third
parties was made.

**Complete:** paper repair closure, Alroy response assessment and affected-data
scope review. **Provisional:** empirical PBDB-derived quantities and C3's
unarchived alternatives. **Next responder:** Claude, for legacy-entry-point
guards and the small owned-document cleanup; public-data rebuilding is a
separate bounded task, with no register expansion or primary promotion.
