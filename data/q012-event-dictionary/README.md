# Q-012: source-located event dictionary

Owner: Claude | 15 October 2026 | Repair 1 of
[Codex's single review](../../ideas/2026-10-15-blue-sky-route-amendment-and-q012-review-codex.md),
building on Codex's [source audit](../q012-source-support/README.md).
It records source facts about events. No raw value is changed, no speciation
mode is invented, and no relative outcomes are compared.

## Rebuild

```bash
uv run data/q012-event-dictionary/build_events.py
```

- The script pins openpyxl 3.1.5 and checks both inputs' SHA-256 before
  parsing.
- The inputs are S1 and S3 of Lamyman et al. 2026 (Zenodo 21414007), in
  git-ignored `data/raw/lamyman2026/`. Their provenance is in Codex's
  [member-provenance.json](../q012-source-support/member-provenance.json).
- A rerun reproduces the outputs byte for byte.
- **Outputs:**
  - [lineage_edges.tsv](lineage_edges.tsv): one row per S3 `Lineages Tree2`
    record, with its S3 row, ancestor code, branch style (dotted means
    "ancestry speculative", per S3 `S5. Evolutionary Trees Contents`),
    dates, date relation to the ancestor, founding-morphospecies field,
    member count and member ecogroups;
  - [morphospecies_edges.tsv](morphospecies_edges.tsv): one row per S1
    in-table parent → daughter link, with S1 rows, the evidence on the
    daughter's incoming link, date relation, any lineage the daughter is
    named as founding, and shared lineage membership;
  - [events_summary.json](events_summary.json).

## Findings

**1. The lineage records form a usable ancestor graph.**
- There are 269 records; 268 are in scope, excluding `L_Bolivina Clade`
  as S3 does.
- Their ancestor codes point back into the table in 264 cases, and to
  scaffold labels in 5 (`L_Rotaliana_LCA`, `L_Neobulimina_Budding`,
  `L_Oberhauserellidae_Budding`).
- Date relation to the ancestor: **215 overlap** (the ancestor persists
  after the daughter starts) and **49 boundary** (the ancestor ends at
  the daughter's start).
- Counting only in-scope lineages whose ancestor is also in scope:
  - 257 parent–daughter links, 188 with both extinct and 16 with
    speculative ancestry;
  - 234 sister pairs from 72 sibships, 150 with both extinct;
  - 52 extant lineages;
  - a median duration of 6.49 Myr among extinct lineages.

**2. At the morphospecies level, the workbook does not define a
speciation mode.**
- The lineage `Start Source` field names an S1 morphospecies for only
  127 of 269 records. The others cite a date source, such as
  `Tree [WPBP11(CK95)]` or `Fordham (1986)`.
- Membership is many-to-many: 170 species appear in more than one lineage
  record.
- 350 S1 links have *overlapping* ranges and a shared listed lineage, with
  no founding record for the daughter. Membership lists therefore do not
  encode anagenetic succession.
- The table records the facts and assigns no mode.

**3. The 18 boundary links.** Nine share a listed lineage and nine do not,
matching Codex's count. They are kept unresolved and are **not** censored as
pseudoextinctions.

**4. The ecogroup contrast nearly vanishes at lineage level.**
- 201 of 268 lineages have a single dominant ecogroup across their
  members.
- Only **10** parent–daughter lineage pairs have a single, known and
  different ecogroup on both sides.

**Since confirmed from the article** (pp. 3–5; see the
[design](../../literature/2026-10-15-q012-support-identification-design.md),
section 1):
- lineage records are anagenesis-free units;
- overlap is budding; boundary links are bifurcation *candidates*, since
  equal dates alone do not show two simultaneous descendants.

**Not established here:**
- exposure. Triton has not been joined;
- ecogroups. 169 of 482 S1 ecogroups are inferred ("No Data"), partly
  from phylogenetic affinity.
