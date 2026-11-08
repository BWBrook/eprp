# Semantic review of the four infrastructure-audit products

Reviewed source: `851d968271b6e0293d4b6d206ba7a71013706a25`.
Reviewer: main Codex, with two bounded `gpt-6.1-sol` delegates assigned
disjoint article/estimands and brief/supplement/guide scopes. All source
locations below refer to that commit. Paths are relative to
`papers/infrastructure-audit/`, except paths beginning `resources/`,
`docs/correspondence/` or `.gitleaks.toml`, which are repository-relative.

**Recommendation: revise before accepting the wording.** The numerical
checks pass, but the prose changes the meaning of several checked results.
The strongest corrections concern mixed admtools controls, attribution of
INDITEK's archive, PyRate interval widths, the brief's cross-target comparison,
and claims about present database access. The estimands need corrections
before they can govern revision.

This turn is a review. It changes no manuscript text, estimands, claims,
references, scanner configuration, figures or PDFs. It proposes concrete
replacements for Claude. The underlying bounded observations remain useful;
this review does not reclassify every clause of an initial headline as checked.

## Coverage and verification

Every result sentence and table cell was read in context, including the
article's abstract, selection/checking account, twelve-case table and all
case narratives, agent-error section, recommendations, assumptions table,
conclusions, roles and data/code statement. The supplement's selection,
replay, withdrawal table and commands; the guide's claims, vocabulary,
provenance, traps and conduct; and all five brief findings were reviewed.
All twelve estimand sections and the cross-cutting rules were checked against
the ledger limits and relevant receipts, rather than assumed correct.

| Case | Governing claims | Disposition of wording at the reviewed commit |
| --- | --- | --- |
| 1 | C191, C192 | Counts/screen supported; present-access and reconstruction claims exceed the check (W05). |
| 2 | C076 | Counts supported under the later-snapshot threshold; make that selection rule explicit (W11). |
| 3 | C043, C045 | Changed-mean and class counts supported; the deletion recipe is misdescribed (W06). |
| 4 | C040 | Discrepancies supported; comparison eligibility and exact-tie scope need stating (W10). |
| 5 | C096 | Count and maximum are joined across different controls (W01). |
| 6 | C102 | Narrative examples supported; table falsely turns examples into a continuous interval (W09). |
| 7 | C107, C194, C196, C105, C111 | Counts supported; width diagnosis, comparison and conditioning need correction (W03, W04). |
| 8 | C110, C098 | Conditional-interval and RNG observations supported; the brief calls semantics a wrong answer (W04). |
| 9 | C125, C123 | Spread/route observations supported; cohort and trend wording need correction (W11). |
| 10 | C035, C048 | Damage/padding and shifted-row counts supported; retain the FR2 category distinction (W15). |
| 11 | C190 | The bounded binomial calculation and separation from spectral evidence are supported. |
| 12 | C195, C193 | Vector/score observations supported; wrong citation/example and excessive exactness/independence (W02, W07). |

Executed checks:

- `make -C papers/infrastructure-audit/manuscript check` passed, including
  all-four-product numeric checks: 22 claims cited, zero errors/warnings,
  lint and reference audits.
- The pin is `3d1934ca42fd4368c6e9faf0c84992f9df279464`; it matches the
  clean local makedoc checkout. No build-tool source change was made here.
- `pdfinfo` confirms the committed brief/article/supplement have two/nine/four
  A4 pages. `pdftotext -layout` confirms the questioned statements also
  appear in the committed PDFs. A new build was unnecessary for unchanged
  manuscript sources.
- All 45 quoted forbidden phrases were searched across the products; matches
  were reviewed as context, including negations and quoted audit-trail traps.
  Literal phrase matching is navigation, not a semantic acceptance test.
- The NSB comparable-age count was independently summed from the source
  receipt: 52,276 agreements plus 4,111 disagreements equals 56,387.
- The bibliography contains twelve DOI-input lines and twelve generated
  records, rather than the thirteen reported in the handoff. The missing
  INDITEK-2 paper is substantive (W02), rather than a citation-style issue.
- A temporary deterministic, non-live token fixture confirms that the new
  global bibliography path exemption also suppresses a provider-specific
  `github-pat` finding (W17). No real credential was used or retained here.

The original fits, simulations and package campaigns were not repeated.
The review uses the already pinned evidence and mathematical distinctions.

## Triage

`Required` means the proposed result wording should be corrected before
semantic acceptance. `Clarify` marks a scope/provenance repair. All remain
open for **Claude**, unless a row identifies another owner. The replacements
below are proposals, not edits already applied.

| ID | Severity | Finding | How checked | Disposition | Owner |
| --- | --- | --- | --- | --- | --- |
| W01 | MAJOR | admtools count and maximum come from different controls | Case05 JSON and R construction | Required: separate sparse, dense and targeted results | Claude |
| W02 | MAJOR | Wrong paper/example attributed to INDITEK score failure | Source entry, archive hashes, primary publisher metadata | Required: cite the 2026 proof-example source and qualify vector agreement | Claude |
| W03 | MAJOR | Unsupported width diagnosis becomes its categorical opposite | C107 limit and raw-log width receipt | Required across article, supplement, guide and estimands | Claude |
| W04 | MAJOR | Brief compares different targets and groups semantics with wrong answers | C194/C107/C110 designs and failed E4 gate | Required: separate targets and finding classes | Claude |
| W05 | MAJOR | Dated membership absence becomes present-day access failure | C191 limit and fixed-snapshot set difference | Required: restore dated-snapshot object; revise case label | Claude |
| W06 | MAJOR | Triton recipe described as keeping one row per key | Literal source-priority deletion predicate | Required: describe retained highest-priority-source rows and eligibility | Claude |
| W07 | MAJOR | Every proposition is said to have a separate rederivation | C195 reuses original harness; independent ZIP route concerns scoring | Required: describe check-specific independence | Claude; Codex clarifies its earlier handoff |
| W08 | MINOR | Universal public cold replay is promised without its prerequisites | Content-pinned local image IDs and retained input requirements | Clarify availability and conditions; no new archive campaign required for this review | Claude |
| W09 | MAJOR | fossilbrush missed examples become a false numeric interval | Grid includes flagged differences 50 and 99 | Required: list the missed examples | Claude |
| W10 | MINOR | NSB numeric eligibility and tie sensitivity are incomplete | Full source class counts and interpolation implementation | Clarify inventory versus comparable ages, tolerance and exact-tie scope | Claude |
| W11 | MINOR | Spatial cohort/trend and PBDB selection rules are underspecified | Cohort census, six median spreads and asymmetric threshold comparison | Clarify denominators, nonmonotonicity and modal-age statistic | Claude |
| W12 | MINOR | Selection is described as entirely from the initial 189 rows | Selection note identifies later new cases | Clarify initial catalogue plus later findings | Claude |
| W13 | MAJOR | Assumptions introduce unverified consequences and provider novelty | No downstream published fit or comprehensive novelty search | Required: distinguish measured changes, proposed consequences and unknown provider knowledge | Claude |
| W14 | MINOR | Full correspondence and unmeasured cost claims | Published placeholders; no cost-comparison design | Clarify snapshot coverage and remove unmeasured economic/prevalence claims | Claude |
| W15 | MINOR | Smaller version, category and role precision | Case receipts and recorded actor metadata | Clarify without inventing missing provenance | Claude |
| W16 | MINOR | Agent commands lack a clear working directory | Actual paper-root versus repository-root layout | Clarify executable entry point and interpretation-aware invariant | Claude |
| W17 | MINOR | Scanner exception suppresses all rules for a bibliography path | Same synthetic provider-token fixture detected outside and ignored inside the path | Narrow exemption in a separate bounded fix; retain provider-token detection | Claude/Codex implementation owner to be agreed |

### W01 — preserve the admtools control identity

Locations: `manuscript/estimands.md:76`, `text/main.md:108`, `:159`;
`text/brief.md:38` also gives an unqualified maximum.

The sparse-model count is 3,972 wrong among 8,282 deposited random queries,
with maximum error **2.995776523137465 Myr**. The dense tie-point model has
**six** wrong queries, maximum **0.4659138824790183 Myr**. Its targeted
near-hiatus probe reaches about **2.7 Myr**. Joining the sparse count to the
dense maximum is false even though every quoted number occurs in C096.
Evidence: `evidence/replay-20261108/software/case05_admtools.json` and
`software/replay_packages.R` in that bundle.

Proposed article/estimand wording:

> In the sparse model, 3,972 of 8,282 deposited query points were
> mis-converted, with maximum error about 2.996 Myr. A dense tie-point model
> mis-converted six of the same queries, with maximum error 0.466 Myr; a
> targeted dense-model probe gave about 2.7 Myr.

For a shorter brief, identify the dense random-query test when using 0.466.
If 2.996 is quoted in a product, first add the already evidenced sparse
maximum to C096's values and bind it normally; no new experiment is needed.

### W02 — identify the INDITEK source and synthetic proof example

Location: `text/main.md:227`; also qualify `estimands.md:139`.
The current citation is Cermeño et al. (2022), DOI
`10.1038/s41586-022-04932-6`. The audited archive is INDITEK-2.0's deposited
**proof example using synthetic observations**, associated with Herrero-Gascón
et al. (2026), DOI **10.1111/2041-210x.70422**, and Zenodo record **22079167**.
The [publisher's article record](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210x.70422)
confirms the title, author and 2026 version of record. The synthetic-example
identity and archive member are established by
`resources/software/inditek-2/README.md` and the replay receipts, rather than
by an assumed link to any published figure.

Proposed wording:

> In INDITEK-2.0's deposited synthetic-observation proof example, three
> archived rejected proposals reproduce their prediction vectors within
> 5 × 10⁻¹⁴, but their saved scores differ from rescoring under the deposited
> observations and scorer. The cause and connection to published figures
> remain unresolved.

Replace “replay exactly” at `main.md:229`: the observed maximum vector
difference is nonzero. Add the correct DOI through the bibliography workflow;
retain the 2022 paper only if it has a separate, explicitly relevant use.
This correction prevents attaching the score finding to the wrong article.

### W03 — unsupported narrowness is not proof of calibrated width

Locations: `text/main.md:184`, `text/supplement.md:61`,
`text/for-agents.md:80`, and the permitted wording in estimands case 7.

“The intervals are not too narrow” is stronger than the replay. Every miss
placing truth below the lower endpoint establishes directional misses;
it does not exclude a simultaneous width problem. The width/median-spread
comparison is descriptive and does not identify the cause of the shift or
prove width calibration separately from location. This limit is explicit in
`evidence/replay-20261108/calibration/README.md:36`.

Proposed replacement in all products:

> The intervals are shifted high. The retained width comparisons do not
> support the earlier “too narrow” diagnosis; they do not independently
> establish calibrated widths or the cause of the shift.

The supplement should say “undercoverage with upward-shifted intervals”,
rather than “undercoverage from location bias”. Add the categorical opposite
to the estimand's prohibited interpretations.

### W04 — retain positive controls without ranking unlike estimands

Locations: `text/brief.md:47`, `text/main.md:180`, and estimands case 7.
The brief juxtaposes Robson–Whitlock extinction upper bounds for retained
species in two simulated clades with PyRate preservation-rate intervals
across a different simulation design. “Can tell good from bad” can read as
a ranking of competing methods for the same question. The brief also omits
the failed E4 implementation-agreement gate. The article needs the two-clade
qualification beside its positive control and the tested constant-rate/HPP
conditions for PyRate. Generator success should name the retained **G1/G2
moment controls**, rather than imply that all generator behaviour was checked.

Proposed brief replacement:

> The checks retained successful controls as well as failures. Under
> homogeneous sampling in two simulated clades, one 95% extinction bound
> covered 1,909 of 2,000 species, although a separate agreement gate failed.
> A different design tested preservation rates: PyRate's 95% intervals
> covered 33 of 50 datasets.

Also separate GRIWM from the brief's “software gives wrong answers” heading
at `brief.md:38`. Its conditional dating-error spread is a semantic finding,
not a demonstrated wrong estimate. Suggested sentence: “Another check
clarified that a reported interval measures sensitivity to uncertain fossil
dates, conditional on those records.” The RNG overwrite remains a separate
implementation finding. This addresses Claude's explicit question about
brief finding 5: **yes, the current comparison can mislead**.

### W05 — keep the dated snapshot as the object

Locations: `text/main.md:104`, `:124`, `text/brief.md:31`.
“Today's public database cannot obtain the same input” and “published data
cannot be rebuilt” exceed C191. The check is a membership difference on
**23 October 2026**, not a live-query test or a proof that the deposited data
cannot be recovered. The article's “sensitive access finding” label should
not imply that these absent records were restricted.

Proposed brief heading: **Some deposited records are absent from a dated
public snapshot.** Proposed article sentence: “Rebuilding from that dated
public snapshot would omit these deposited occurrence identifiers.”
Use a membership/provenance label for case 1. The 71,103/368,760 and
14-to-12-of-21 observations themselves are supported.

### W06 — the conservative Triton recipe does not keep one row per key

Location: `text/main.md:139`. The source predicate in
`resources/sources/triton/triton_dedup.R` removes only rows with recorded
depth in cross-source groups whose source priority is below the best in the
group. It retains **all rows belonging to the highest-priority source**;
within-source groups and missing-depth groups are untouched. For a group
containing two best-source rows and one lower-priority row, it keeps two,
not one. This is a material distinction for anyone implementing the recipe.

Replacement: “A conservative recipe removes lower-priority-source rows only
from cross-source groups with recorded depth, retaining rows from the
highest-priority source.” Keep the removal count and clarify that the
1,388 count concerns unrounded comparable means at the stated tolerance.

### W07–W08 — distinguish the checks from universal validation and access

Locations: `text/main.md:77`, `:249`, `:300`;
`text/brief.md:26`; `text/supplement.md:31`.

C195's new forward execution reused the original harness. The separate
model-free ZIP scorer supplies an independent **score calculation**; it does
not independently implement the forward model. The receipt explicitly says
so. “Every supporting proposition was rederived by a separate route” is
therefore too broad. This qualification applies to **Codex's earlier blanket
handoff wording too**, not only Claude's draft. The bounded direct replay
observation remains valid; an independent forward-model implementation has
not been supplied.

Suggested methods wording:

> Each case combined replay by another actor with the computational or
> mathematical checks specified in its receipt. These included separate
> aggregation, interpolation, geometry and scoring code. The INDITEK forward
> run reused the original pinned harness; its scoring check was separately
> implemented. Some reviewers used the same model family and shared inputs.

Replace “caught because” with an observational account of what was identified
during those reviews; a controlled causal benefit was not measured.

“Anyone can rerun” also needs conditions. The software wrapper requires two
locally retained image content IDs; calibration reaggregation requires
retained posterior logs and source archives. Hashes and commands identify
requirements but do not demonstrate a public cold replay of every case.
Replacement: “Each result records its replay command, required inputs and
their hashes.” An exact public rebuild may be a release task, but it was not
validated in this review.

### W09–W12 — retain selection and denominator definitions

- **fossilbrush, `main.md:109`:** “10 to 499 were not flagged” is false as
  a range: 50 and 99 are flagged in the test. List the missed values
  **10, 20, 49.9, 100 and 499**. The case narrative already does this correctly.
- **NSB, `main.md:149`, `brief.md:36`, `for-agents.md:39`:** the snapshot has
  61,862 rows, but only **56,387** have both numeric ages. State this before
  the 4,111 comparison count; the total is still a valid inventory count.
  Other classes are 4,712 undated by both routes, 294 dated only in storage
  and 469 dated only by recomputation. Keep the >0.01-Myr threshold and
  first-age-at-exact-tie convention. Eight discrepancies disappear under
  the other exact-tie choice; this is not a full alternative treatment of
  all between-tie interpolation segments. Add any newly quoted derived
  count to C040 before binding it in products.
- **Plate models, `main.md:202`, `estimands.md:113`:** 300 is the starting
  pool. Counts reconstructable in all three models vary by age:
  **269/260/255/247/217/194**; the complete cohort is 194. Medians
  **2.885/5.654/4.317/5.495/4.730/13.554** are nonmonotonic. Replace
  “rising with age” by “age dependent, with the largest median at 400 Ma”.
  Name the three models and qualify medians by age-specific reconstructable
  cohort. Use “can change band assignments” unless a band-transition tally
  is supplied.
- **PBDB, `main.md:131`, `estimands.md:43`:** specify ≥50 single-interval
  occurrences in the **later** snapshot; requiring it in both changes 317
  to 316. The statistic is a modal base age, not necessarily every record's age.
- **Selection, `main.md:54`, `:69`, `supplement.md:7`, `brief.md:24`:** the
  initial 189-row catalogue was supplemented by later findings, including
  Rampino and INDITEK. Write “the initial catalogue and subsequent programme
  findings”, rather than imply all twelve were drawn from the frozen pool.
  “189 possible problems” also mislabels positive controls and intended
  behaviours; use “candidate findings”.

### W13–W15 — keep conclusions and provenance observational

At `main.md:282`, a different version restricts scope; it does not falsify
the observation made on the pinned version. The table's claim that “the
consequence for inference is real” must distinguish measured support/input
changes from effects on a published conclusion, which were not replayed.
“Third-party findings are not already known” at `main.md:285` is not an
established conclusion: provider knowledge remains unresolved. Replace that
row with an open question rather than an assumption that creates novelty.

At `main.md:249`, **reviewed correspondence snapshots**, not the full
record, are public. At review time the policy cleared eight messages and
withheld 469 as placeholders. General assertions about agents making work
“cheap”, nobody being paid to audit, or how often users check resources
(`main.md:9`, `:42`, `:47`, `:51`, `:298`; `brief.md:17`, `:55`) have no
cost, employment or prevalence study behind them. Remove them or identify
an independently supported source; the observed workflow is sufficient.

Smaller precision points for the same pass:

- Describe GRIWM as not quantifying uncertainty from the fossil-sampling
  process, rather than declaring its conditional interval generally invalid.
- FR2 has 112 range-only shifts, **two additional habitat-and-range shifts**,
  and 106 NFR shifts. Do not imply only 112 rows can affect ranges when
  explaining all 220.
- The proposed AI-role division broadly matches the catalogues. The replay
  provenance records that the exact parent Codex model identifier was not
  available; either supply contemporary evidence for the label at
  `main.md:310` or retain “Codex” and the known `gpt-6.1-sol` delegates.
  Original INDITEK and later Rampino work include Codex discovery, so retain
  “most original findings” when attributing discovery to Claude.

### W16–W17 — functional review of commands and scanner changes

The guide's commands at `for-agents.md:92` need an explicit
`cd papers/infrastructure-audit` from the repository root. Its front-matter
governing paths also start at repository root, despite the stated default
path convention. Make the two roots explicit. “No text uses a not-allowed
phrase” at line 98 should instead prohibit **adopting the interpretation**;
quoted mistakes in the supplement and guide are intentional.

The makedoc pin is valid and `make check` passes. The root `.gitleaks.toml`
is broader than the reported generic-key false-positive fix: its **global
path allowlist** ignores every secret rule for every matching
`references/refs.yaml`. In a temporary control, the same deterministic
synthetic GitHub-token value was detected as `github-pat` in `control.yaml`
and suppressed in `references/refs.yaml`. This demonstrates rule suppression
beyond citation keys; it is not evidence of a credential in the bibliography.
Narrow the exemption to the relevant citation-key content and rule, and
retain provider-token detection in bibliography files. Verify with the same
control after revision. No scanner configuration was changed in this turn.

## Revision order and next owner

1. **Claude:** correct the estimands, especially cases 5, 7, 9 and 12 and
   check-specific independence, then revise the four products together.
2. **Claude:** use the receipt-backed values when updating C096/C040 if the
   newly stated maxima or eligible counts appear in products; maintain
   numerical bindings and the audit-trail/trap corrections.
3. **Claude/Codex implementation owner:** narrow the scanner exception as a
   separate bounded fix; this review has not done so.
4. Rerun checks and rebuild after the edits, preserving the brief's two-page
   limit. Codex can then verify the corrected passages; there is no need to
   rerun the underlying analysis campaign for these wording repairs.

Figures, journal style, author/provider contacts and paper release were not
commissioned by this review. Barry retains external contact and release
decisions. No contact or release action was taken.

Next: Claude — revise the estimands and four products using this triage.
