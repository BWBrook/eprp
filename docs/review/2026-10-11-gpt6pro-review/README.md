# EPRP external review bundle

Pinned repository commit: `bbe5ce7fc205b3b1f9529757b64e25fd997243cb`.

Start with **review.md**. It is the complete, self-contained report, including executive assessment, five ranked findings, all-50 coverage ledger, development priorities, sources and verification limits.

Companions:

- `coverage.tsv`: machine-readable coverage and qualified dispositions.
- `initial_view_before_phase2.md`: provisional register-first assessment, recorded before the ranking debate; not the final verdict.
- `checks.py` and `checks_results.json`: four independently executed deterministic fixtures, using hypothetical inputs and the Python standard library.
- `reproduction/q026/probe.py` and `summary.tsv`: source copied from the pinned commit and the independently reproduced output. These are the repository authors’ probe, not a new reviewer implementation.
- `q026_rerun_receipt.json`: execution and source/output Git blob hashes.
- `verification_receipt.json`: final bundle checks.
- `MANIFEST.sha256`: artifact integrity checksums, excluding this manifest itself.

Run the independent fixtures with `python checks.py`. Run the included repository probe with `python reproduction/q026/probe.py`; this overwrites only the included local output table. Neither command accesses GitHub or requires fossil inputs. The reviewer actually executed both during the review.

Only the Q-026 probe was reproduced from the repository. Other raw-data and model executions are explicitly limited in the report. No repository writes, primary analysis or author contact occurred.
