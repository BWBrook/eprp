# C1 check: how fast are fossil genus names invalidated?

Claude, 23 October 2026. This is the cheapest check that could change the
disposition of candidate C1 in
[the Alroy provocation note](../../ideas/2026-10-23-alroy-provocation-claude.md).
It is not a registered question.

- **Data:** the public PBDB API (CC BY), queried on 23 October 2026, with no
  account or contact parameters. For each clade, the script pulls genus
  names (`taxa/list`, `variant=all`) and every recorded opinion on them
  (`taxa/opinions`). Run with
  `uv run --python 3.12 data/c1-name-survival-check/check.py`.
- **Event:** the name is invalid now (subjective or objective synonym,
  replaced, nomen dubium, nudum, vanum or oblitum, or invalid subgroup). It
  is dated by the first invalidating opinion. Rank changes do not count.
- **Censoring:** valid names are censored at 2026. Survival is estimated by
  Kaplan–Meier.
- **Not used:** the API's `n_occs` reports the senior taxon's count for a
  synonym.
- **Outputs:** [summary.json](summary.json) and
  [name_survival.tsv](name_survival.tsv), one row per genus name.

**Limitations:**
- PBDB opinions under-record revisions. Benton 2008 put dinosaur genus
  error at about 40%, against 20% here.
- Genus rank only.
- The first invalidating opinion may predate a later revalidation and
  re-invalidation.
