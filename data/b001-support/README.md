# B-001 support: coding provenance and the Knope–PBDB support audit

Two products are recorded here:
- the PBDB coding-provenance diagnostic (14–15 October);
- the support audit (15 October), which parks the global guild-grain
  empirical route. See [the audit section](#b-001-support-audit-knope-coding-joined-to-pbdb-15-october-2026).

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

Status: **support only.** The definitions were fixed in the contract's
section 8 and committed (`e7697d9`) before this audit ran. No post-event
richness, crossing or restoration time was computed. Post-event cells were
assessed only for coverage resolution.

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

**Workbook handling.** The workbook is read with xlrd 2.0.1 and is
hash-checked. Nothing in it is executed.

**Reproducibility.** A second run reproduced all five audit outputs byte
for byte.

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
- The sheet has 18,317 rows and 18,228 distinct names, with 89 repeated
  names.
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
- **The coding level is unknown.** Codes are probably applied largely at
  higher-taxon level, as in PBDB.

**2. Only 25–48% of PBDB genera in the windows join to Knope** (32–67% of
occurrences). The gaps are concentrated in particular classes:

| Class | Joined |
| --- | --- |
| Ostracoda | 0% |
| Chondrichthyes | 3–4% |
| Conodonta | 15% |
| Gastropoda | 33–44% |

- The K–Pg occurrence join falls from 0.545 in the Maastrichtian to
  0.39–0.44 after the event.
- Bivalves fall from 0.61 to 0.53 across the K–Pg.
- The K–Pg pelagic predators are 93% cephalopods at baseline. After the
  event that role passes to fishes and sharks, which are barely coded. This
  is outcome-related missingness of exactly the kind the contract warned
  about.

**3. Few guilds are at risk.**

| Event | Guilds with a baseline cell | At risk |
| --- | ---: | ---: |
| End-Permian | 12 | 4 |
| End-Triassic | 12 | 5 |
| K–Pg | 17 | 8 |

- Stage support is not binding: every stage has 181 or more collections.
  Almost every at-risk guild is resolved in all follow-up stages and in its
  confirmation stage.
- The binding constraint is the minimum subsampled baseline of 5 genera at
  coverage 0.5.
- No at-risk cell has zero survivors.
- 4 guilds are at risk in all three events:
  - epifaunal mobile grazers;
  - epifaunal stationary suspension feeders;
  - infaunal stationary suspension feeders;
  - pelagic mobile predators.

  One more (epifaunal stationary "other", the corals) is at risk in two.
- Dominant class switches in 2 guilds: brachiopods to bivalves in each
  suspension-feeding guild.
- Pair types among the 17 at-risk cells:

  | Pair type | Count |
  | --- | ---: |
  | Same guild, same class | 9 |
  | Same guild, different class | 4 |
  | Different guild, same class | 5 |
  | Different guild, different class | 118 |

**4. The covariance basis has rank 3,** with event effects alone and with
the survivor and baseline covariates. Rank 3 is necessary, not sufficient:
- event effects only: singular values 8.22, 2.65, 2.55;
- with the covariates: 7.03, 2.40, 2.14.

**5. Best-case discrimination bound ([power_bound.py](power_bound.py)).**
- **Assumptions:** balanced guilds × events; complete, uncensored and
  error-free log delays; event effects only; no clade term; exact F-based
  90% intervals. The F test is the standard optimal invariant test for
  these variance-component hypotheses in a balanced design. A calibrated
  procedure on the real censored, unbalanced and confounded data should do
  no better.

| Events | Guilds in all events | P(lo > 0.1 \| ρ = 0.5) | P(hi < 0.5 \| ρ = 0) |
| ---: | ---: | ---: | ---: |
| 3 | 4 (observed) | 0.29 | 0.27 |
| 3 | 6 (planning target) | 0.41 | 0.45 |
| 3 | 7 (every guild with any resolved baseline in all three events) | 0.47 | 0.53 |
| 3 | 17 | 0.81 | 0.93 |
| 5 | 10 | 0.82 | 0.95 |

- **Even perfect data on these guilds cannot meet the section 7 power
  criteria** (both at least 0.8).
- At three events the best case needs about 17 guilds at risk in every
  event; at five events, about 10. The "about 6" planning target was far
  too low.
- **The conclusion does not depend on the baseline minimum.**
  - A minimum of 2 or 3 genera still gives 4 guilds.
  - Dropping it entirely gives 7. Each of the three additions has a
    baseline of 1 to 1.5 subsampled genera in at least one event.

### Consequence (contract section 7)

**Inadequate discrimination is predicted before any restoration time is
computed.**
- The global guild-grain empirical route is **parked**, as the contract
  prescribed. The question is kept.
- This is not a finding about recovery order. It is a finding that the open
  coded data cannot discriminate rule strength from absence at this grain.
- **Reopening needs one of these:**
  - about 17 or more supported guilds in three events (or about 10 in five),
    which needs better coding coverage than this join gives;
  - a reformulated estimand needing less replication across guilds, such as
    one signed contrast replicated across many events. That needs its own
    contract, and it faces clade confounding: pelagic predators are
    cephalopods before the K–Pg and fishes after.
