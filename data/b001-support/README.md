# B-001 support: coding provenance and the Knope–PBDB support audit

## ⚠ Data-access hold (read first) (23 October 2026; side session 76/2259)

[Detail withheld pending disclosure to the data custodian.]
- **Rows affected, against the public global snapshot:**
  - b001 end-Permian: 2,195 of 56,607;
  - b001 end-Triassic: 5,442 of 50,167;
  - b001 K–Pg: 7,655 of 67,097;
  - q042 Changhsingian: 150 of 11,031.
- **`genera.csv` and `genus_appearances.csv` are untested.** They may
  inherit the problem through the same query paths.
- [Detail withheld pending disclosure to the data custodian.]
- **The raw files were deleted on 23 October 2026** at Barry's instruction
  (Claude chat, exact words: "Yes, delete the raw extracts"). No other
  copies existed on the laptop, deep-server or mac-mini. The derived numbers
  here must be rebuilt from public data before any use.

The rebuild commands below are disabled: each legacy fetch now stops with a pointer to this hold.

Two products are recorded here:
- the PBDB coding-provenance diagnostic (14–15 October);
- the support audit (15 October, corrected after Codex's check), which
  holds the global guild-grain empirical route. See [the audit section](#b-001-support-audit-knope-coding-joined-to-pbdb-15-october-2026).

## Coding provenance

Owner: Claude | 15 October 2026 | Supports the
[B-001 contract](../../literature/2026-10-14-b001-reassembly-contract.md),
section 4. It answers point 4 of
[Codex's merge review](../../ideas/2026-10-14-blue-sky-merge-review-codex.md):
the inheritance figures needed an exact request, denominators and
calculation.

Status: **a coding-provenance diagnostic.** No guild, occurrence or
recovery quantity is computed in this part.

### Rebuild

```bash
python3 -I data/b001-support/ecospace_provenance.py
```

- Standard library only.
- On the first run it fetches into the git-ignored
  `data/raw/pbdb/b001/genera.csv`:
  `https://paleobiodb.org/data1.2/taxa/list.csv?base_name=Metazoa&rank=genus&taxon_status=valid&show=class,ecospace,etbasis,app&rowcount&datainfo&limit=200000`
- The 14 October query (access time 05:20:08 GMT) and this re-run (access
  time 2026-10-14 23:45:09 GMT) both returned 89,623 records with identical
  counts.
- Extract sha256 for the re-run:
  `7662b51bd9d3b3a20beeb24c27dd1defe577c6a8b0545f255a189cd5ff4bc78b`.
- **Output (tracked):** [ecospace_provenance.tsv](ecospace_provenance.tsv).

### Definitions

- **With value:** the genus's `motility`, `life_habit` or `diet` field is
  non-empty.
- **Direct:** the matching `_basis` field (from `show=etbasis`) equals the
  genus's own name, so the value was entered for that genus. Any other
  basis is **inherited** from the named higher taxon.
- **Recovery-window subsets:** the genus's PBDB range
  (`firstapp_max_ma` to `lastapp_min_ma`) overlaps the window:
  - 252–242 Ma, end-Permian;
  - 201.4–191 Ma, end-Triassic;
  - 66–56 Ma, K–Pg.

  The windows are provisional and match the contract's 10 Myr horizon.

### Result

| Subset | Genera | Inherited share of populated values (motility / life habit / diet) |
| --- | --- | --- |
| All valid metazoan genera | 89,623 | 0.990 / 0.980 / 0.981 |
| End-Permian window | 4,672 | 0.986 / 0.975 / 0.977 |
| End-Triassic window | 3,647 | 0.977 / 0.962 / 0.965 |
| K–Pg window | 9,752 | 0.977 / 0.965 / 0.965 |

Motility is populated for 99% of all genera. Life habit and diet are
populated for 74–76%.

### Limits

- **Scope.** All Metazoa, terrestrial included. The service's taxa
  endpoint has no environment field, so marine-only shares need an
  occurrence-based filter.
- **Which coding.** These figures describe PBDB's annotations. B-001's
  route uses Knope et al. 2015's coding, whose provenance is not known here.
- **What inheritance means.** It implies dependence between guild
  assignment and classification. It does not show that a guild equals a
  clade. That needs the joint guild × clade table.
- **Earlier figure corrected.** The first contract's "about 99%" was the
  motility figure alone. Across the three fields the share is 98–99% overall
  and 96–99% in the windows.

## B-001 support audit: Knope coding joined to PBDB (15 October 2026)

Status: **support only, corrected once.**
- The definitions were fixed in the contract's section 8 and committed
  (`e7697d9`) before this audit ran.
- No post-event richness, crossing or restoration time was computed.
  Post-event cells were assessed only for coverage resolution.
- The first release (`451a96b`) had two defects, found by
  [Codex's check](../../ideas/2026-10-15-blue-sky-support-adjudication-codex.md).
  Both are fixed here:
  - it keyed genera on PBDB's `genus` field, which can carry a subgenus
    (for example `Cucullaea (Idonearca)`), instead of the accepted genus;
  - it drew the merge universe from all stages instead of pre-event stages
    only.

  It also overstated the power calculation as a universal bound. Corrected
  results replace the first release; that version stays in git history.

### Rebuild

```bash
uv run -q --no-project --with xlrd==2.0.1 --with numpy==2.1.3 python -I data/b001-support/support_audit.py
uv run -q --no-project --with scipy==1.14.1 python -I data/b001-support/power_bound.py
```

**Inputs** (git-ignored, under `data/raw/`):

| Input | Retrieved | sha256 |
| --- | --- | --- |
| Knope et al. 2015 Supplementary Data 1, `knope2015/41467_2015_BFncomms7455_MOESM1087_ESM.xls` (CC BY 4.0; 3,911,680 bytes) | 15 Oct 2026, from the Springer Nature static ESM link | `e5c1eef44f51e788c12c80efdceba9e6597472af57d0a7146ae8f015ecf3f181` |
| PBDB occurrences, `pbdb/b001/occs_end_permian.csv` (56,607 rows) | 2026-10-15 01:16 GMT | `a8bc335ef8b4958e5f3e5c65812bec7b4219071ad80d421c40f31c28f48f21bf` |
| PBDB occurrences, `pbdb/b001/occs_end_triassic.csv` (50,167 rows) | 2026-10-15 01:16 GMT | `db4886ec95bbca9f16c21b81147673beace9487d93c4a1d161c8d3153acb8056` |
| PBDB occurrences, `pbdb/b001/occs_k_pg.csv` (67,097 rows) | 2026-10-15 01:17 GMT | `a25385cac5d6cb8680f17364489e617ea56ac3318db545ce662ab0a77b0418a1` |
| PBDB genus ranges, `pbdb/b001/genera.csv` (above) | 2026-10-14 23:45 GMT | `7662b51b…c78b` |

**Rules this release adds or makes explicit:**
- **Genus identity** is the first word of `accepted_name`.
  - The 3, 3 and 25 subgenus-ranked rows count under their parent genus.
  - Rows are deduplicated by collection and genus, removing 6, 2 and 6.
- **Repeated Knope keys.** 74 name–phylum keys repeat, and 13 of those carry
  conflicting codes or classes (all are listed in the summary).
  - A repeated key is used only if every repeat agrees; otherwise the
    genus is unjoined as a conflict.
  - None of the 13 occurs in these extracts.
- **The merge universe** is guilds present in the penultimate or baseline
  stage of any event.
- **Workbook handling.** The workbook is read with xlrd 2.0.1 and is
  hash-checked. Nothing in it is executed.

**Outputs (tracked):**
- [support_summary.json](support_summary.json);
- [support_at_risk.tsv](support_at_risk.tsv): every baseline guild × event,
  with baseline richness, coverage, survivors, class composition and
  follow-up resolution;
- [support_guild_stage.tsv](support_guild_stage.tsv);
- [support_join_by_stage.tsv](support_join_by_stage.tsv);
- [support_join_by_class.tsv](support_join_by_class.tsv);
- [power_bound.tsv](power_bound.tsv).

### Results

**1. The deposited dataset is smaller than the paper's count.**
- The paper reports 18,621 genera.
- The sheet has 18,317 rows and 18,228 distinct names.
- Codes follow Bambach et al. 2007, checked against known classes:
  - cephalopods are pelagic, fast and predatory;
  - rhynchonelliform brachiopods are surficial, attached suspension
    feeders;
  - echinoids are surficial, slow deposit feeders.
- `eco_ref` cites mainly general works. The most frequent among joined
  genera:
  - Bambach et al. 2007;
  - Huber 2010 (bivalves);
  - Brusca & Brusca 2003;
  - Carlson & Sandy 2001 (brachiopods).
- **The coding level is unknown.**

**2. 27–53% of PBDB genera in the windows join to Knope** (38–77% of
occurrences). The gaps are concentrated in particular classes:

| Class | Joined |
| --- | --- |
| Ostracoda | 0% |
| Actinopterygii (end-Triassic baseline) | 0% |
| Chondrichthyes | 3–19% |
| Conodonta | 0.5–15% |
| Gastropoda | 35–50% |

- **Within classes, join rates are stable across each event**, for example:

  | Class across the K–Pg | Before | After |
  | --- | ---: | ---: |
  | Bivalves | 0.680 | 0.683 |
  | Gastropods | 0.365 | 0.395 |
  | Sharks | 0.033 | 0.037 |

  The first release's bivalve decline was produced by the subgenus defect.
- **The aggregate decline after the K–Pg (0.59 to 0.45–0.50) is
  compositional.** Well-coded ammonoids (94% joined) disappear.
- **Risks, not findings:**
  - Fishes and sharks are barely coded throughout. If their share of
    pelagic predators rose after an event, this join could not see it.
  - Whether that happened, and whether coding gaps depend on recovery, is
    not established here.
  - Joined cephalopods still supply most pelagic-predator occurrences in
    the Danian (Codex: 125 of 153).

**3. Few guilds are at risk.**

| Event | Guilds with a baseline cell | At risk |
| --- | ---: | ---: |
| End-Permian | 12 | 4 |
| End-Triassic | 12 | 5 |
| K–Pg | 18 | 7 |

- 7 distinct guilds are at risk in some event, across 16 cells.
- Stage support is not binding: every stage has 181 or more collections,
  and almost every at-risk guild is resolved in its follow-up and
  confirmation stages.
- The binding constraint is the minimum subsampled baseline of 5 genera at
  coverage 0.5. The K–Pg change from the first release comes from a merge
  with a pre-event trigger: the merged epifaunal mobile deposit guild has a
  baseline of 4.73 genera, against 5.30 for the slow guild before merging.
- No at-risk cell has zero survivors.
- **4 guilds are at risk in all three events:**
  - epifaunal mobile grazers;
  - epifaunal stationary suspension feeders;
  - infaunal stationary suspension feeders;
  - pelagic mobile predators.

  One more (epifaunal stationary "other", the corals) is at risk in two.
- Dominant class switches in 2 guilds: brachiopods to bivalves in each
  suspension-feeding guild.
- Pair types among the 16 cells:

  | Pair type | Count |
  | --- | ---: |
  | Same guild, same class | 9 |
  | Same guild, different class | 4 |
  | Different guild, same class | 5 |
  | Different guild, different class | 102 |

**4. The projected covariance basis has rank 3,** with event effects alone
and with the survivor and baseline covariates. Rank 3 is necessary, not
sufficient:
- event effects only: singular values 8.04, 2.61, 2.52;
- with the covariates: 6.65, 2.36, 2.14.

**5. Exact balanced no-clade F benchmark ([power_bound.py](power_bound.py)).**
- **Model:** balanced guilds × events; Gaussian log delays, complete,
  uncensored and error-free; event means; independent residuals; no clade
  term; F-based 90% intervals for ρ.
- The probabilities below hold *for that procedure in that scenario*. They
  are not a bound on every calibrated analysis of the actual table:
  - the actual table has unbalanced cells that four complete guilds omit;
  - shared clade noise is not uniformly worse than independent noise, since
    same-class contrasts cancel it;
  - optimality within an invariant family is not optimality over all
    calibrated procedures.

  Codex reproduced the arithmetic independently in R.

| Events | Guilds in all events | P(lo > 0.1 \| ρ = 0.5) | P(hi < 0.5 \| ρ = 0) |
| ---: | ---: | ---: | ---: |
| 3 | 4 (complete in the audit) | 0.29 | 0.27 |
| 3 | 7 (all 7 at-risk guilds, completed to all three events; contains the actual table) | 0.47 | 0.53 |
| 3 | 17 | 0.81 | 0.93 |
| 5 | 10 | 0.82 | 0.95 |

- In this benchmark the containing design reaches about half the 0.8
  target.
- Lowering the baseline minimum to 2 or 3 genera does not change the four
  complete guilds.

### Consequence

**HOLD as a practical programme decision**, agreed with Codex.
- The open coded data give sparse repeated guilds, and the coding gaps are
  substantial.
- On this support, a calibrated actual-design check is very unlikely to be
  worth its cost. No such check was run, and impossibility is not claimed.
- The question is kept. This is not evidence against repeatable
  reassembly.
- **Reopening:**
  - better coding or occurrence support that materially enlarges the set of
    guilds repeated across events;
  - or a justified alternative target or design that shows adequate
    calibrated errors and power.

  The 17-guild figure is a benchmark for one procedure, not a necessary
  condition.
