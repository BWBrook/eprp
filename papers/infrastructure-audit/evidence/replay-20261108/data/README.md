# Fixed-input data replay: cases 2, 3, 4 and 10

Codex, 8 November 2026. New evidence files only; source resources and existing
products were read-only. Source checkout at start:
`bc7e1d81b2f36954ca517639cf4f789ad362d658`. The integrating
[manuscript ledger](../../../manuscript/claims.csv) records reviewed status
only for its narrowed propositions. This is raw-input regeneration,
with the specifically identified derived-table checks below, rather than a
recalculation of the old catalogue's numerical claims.

The computations ran on the authorised Linux data host, with archived inputs,
base R and Python standard libraries. No live PBDB request was made. Raw PBDB
tables, SQLite databases, workbooks, capture histories, occurrence identifiers
and the temporary Triton projection stayed on that host. The tracked receipts
contain counts, hashes and EPRP's own aggregate support tables. No database or
source-resource file was modified.

## Decisive results

| Case | Fixed-input replay | Scope and consequence |
|---|---|---|
| 2 / C076 | Whole chronosphere ZIP tables reproduce **460, 317 and 17** changed modal interval bases at the three major steps. The original rule requires at least 50 single-interval occurrences in the **later** table. Requiring 50 in **both** gives **460, 316 and 17**. | Archived query products change their temporal meaning. This alone establishes neither a database defect nor the broader assertion that PBDB maintains no versions. C021's historical creation-date query and C075's ICS chart comparison were not replayed. |
| 3 / C043 | Triton v1 has zero excess rows under its exact key; v4 has **28,832**, partitioned into **16,267** cross-source and **12,565** within-source excess rows. There are 16,256 cross-source groups and 6,086 within-source groups. | Key collisions do not by themselves prove repeated physical observations. The conservative, recorded-depth, source-priority recipe removes **16,260** rows, leaving **525,586**. Python and original R deletion memberships agree exactly. |
| 3 / C045 | Fresh before/after builds reproduce committed undeduplicated Q012 tables byte-for-byte. Independently computed **unrounded observed means change in 1,388/2,267 comparable lineage-bins** at absolute tolerance `1e-9` degrees; **411** change by at least 1 degree. | A measurable change to EPRP's support covariate; no fitted biological outcome or published third-party result is replayed. Complete paired builds and joined differences are saved. |
| 4 / C040 | In the final NSB snapshot, **4,111/61,862** samples disagree by more than 0.01 Myr under the specified first-tie interpolation, across 56 holes. 52,276 agree; 2,475 differ by 0.01–0.5, 683 by 0.5–1 and 953 by more than 1 Myr. | Eight disagreements disappear when the last age replaces the first at exact duplicate-depth ties: **4,103** remain under that sensitivity. These are stored-versus-model inconsistencies, not proof that every stored age is stale or every recomputed age true. |
| 10 / C035 | All **6,562** spreadsheet histories are numeric; 5,291 use scientific notation. Against intact 86-character R-binary histories, **2,967** have altered integer values. Of these, **1,469** contain nonbinary digits after padding and **1,498** remain binary but wrong. | Leading zeros alone are recoverable with known width: **3,595** rows recover exactly by padding. Numeric alteration, not notation alone, is the decisive corruption. No CMR fit was rerun. |
| 10 / C048 | Direct OOXML comparison finds **220/7,109** FR2 rows shifted left: **112** range rows, **2** habitat-plus-range rows and **106** NFR flags moved into the Holocene column. | Range assignment changes mechanically. Treating NFR as a Holocene presence requires a parser that counts any nonempty cell; a valid-code parser need not make that error. This replay compares current chapter workbooks and All-Life, not the earliest Wayback copies. |

## Triton paired builds and independent checks

[paired_builds.json](results/paired_builds.json) defines the row keys, output
hashes, every changed column and the complete displayed-value comparison.
[triton_independent.json](results/triton_independent.json) records a separate
Python implementation of numeric-tuple duplicate keys, deletion, species and
lineage membership, bin means and the past-only older-bin lag. Neither the
original checker nor its grouping code was imported. R deserialised RData;
the projection used 17 significant digits so binary64 numeric values round-trip.

There are **3,184** total lineage-bin rows. Observed means are nonmissing in
2,271 before and 2,267 after; the **2,267 paired nonmissing rows** are the
denominator for the 1,388 raw changes. Four additional means become missing.
The source R builder saves means to three decimals: **1,385** comparable
displayed values change, plus those four missingness changes (1,389 changed
cells altogether). Both raw and displayed routes find **411** paired changes
of at least 1 degree. The maximum absolute paired change is 26.89925 degrees
before display rounding.

Lagged model inputs are nonmissing in 2,124 before and 2,122 after. Of the
**2,122 comparable** values, **1,320 raw** and **1,319 displayed** values
change; **394** change by at least 1 degree, and two become missing.
Standardisation also changes when the underlying observed mean and SD change;
2,121 comparable standardised values change, plus two new missing values.
These are separate quantities, not alternative denominators for observed E.

All independently derived occurrence counts and missingness flags agree
exactly with both R builds. Full-precision Python means and lagged means agree
with the saved R values to **0.000500001 degrees**, half the three-decimal
display unit plus a small floating-point tolerance. At decimal half ties,
Python's rounded display differs from R in 14/13 observed/lagged cells before
and 19/18 after; these are reported, not silently made identical. The
independent change criterion `>1e-9` is applied to unrounded Python means.
The one-degree criterion uses `>=1-1e-9` to handle binary arithmetic at the
boundary.

A separate [raw R census](raw_mean_check.R), using a copy of the original
builder body with display rounding removed, reproduces all raw change counts,
one-degree counts, missingness changes and maxima in
[raw_mean_check.tsv](results/raw_mean_check.tsv). Thus the full-precision
1,388/411 result is checked by two numerical implementations as well as the
parent's exact-decimal review of displayed values.

A separate R census in [raw_mean_check.tsv](results/raw_mean_check.tsv)
confirms **1,388/2,267**, **411**, and every raw lagged-value count above.
[raw_mean_check.R](raw_mean_check.R) executes the original builder only
through exposure-matrix construction, with display rounding removed in the
copy, then compares its unrounded R values directly. Thus the new raw-change
count is independently obtained in R and Python, not inferred from their
agreement within the saved table's rounding unit. The original source file
is unchanged.

The recipe's source priority is **ForCenS, IODP, Neptune, Pangaea,
Lloydetal2012, Fentonetal2016**. It removes 13,858 Pangaea, 2,282 Fenton and
120 Neptune rows. [dedup_membership.tsv](results/dedup_membership.tsv)
compares every removal index with the original R recipe: both asymmetric
differences are zero. Same-source collisions and missing-depth groups are
left alone. This is a sensitivity recipe, not a definitive adjudication of
physical duplicate records.

Among 491 pair rows, **8 `E_class`, 8 `E_systematic_class`, 2
`used_systematic_class` and 1 `used_perbin_class`** values flip. Python
separately joins the saved bin values and recomputes all four classifications
using the original five-degree and three-bin rules: **zero mismatches in
both arms**. Jaccard class and covered-lineage flags are unchanged, although
58 numerical Jaccard values and four coverage values change.

Q007's five event summaries retain identical qualifying `gate_sites`. Its
pre-deduplication sample totals exceed the conservative totals by 8.35% for
K–Pg, 0.75% for PETM, 0% for ETM2, 3.23% for ETM3 and 4.28% for EOT. Two
individual `biota_ok` flags and one `ages_ok` flag change. The current pinned
recipe **does not reproduce** the historical 1,454/423 Q012 counts, two
`used_perbin` flips, or Q007's 11–13% inflation. Original paired receipts
were absent; the reason for those differences remains unestablished. Existing
source READMEs have not been rewritten to conceal the disagreement.

The source-version check also reproduces **1,520** v3-to-v4 presence-unit
changes, all Count to Number per gram. Archived CombinedData source has an
active `duplicated()` call in v1 and none in v3. The code ZIPs and members
are hashed in [inputs_triton.json](results/inputs_triton.json). This does not
rebuild Triton's original upstream compilation, whose missing upstream files
are a separate limitation. The optional `triton_versions.tsv` age-change
counter uses a `1e-6` threshold and includes age-grid differences; it is not
a replay of the catalogue's 3,663 age-conversion claim.

## Other qualifications

PBDB's full-table replay uses eight pinned archives. The one-interval step
has only the coarse January-to-March 2024 bracket here, and the ten-interval
step only April 2025-to-February 2026. Fine date brackets obtained previously
from partial HTTP heads were not regenerated. No prevalence statement, ICS
correctness statement or causal explanation follows from these counts.

NSB's 61,863-line old TSV contains a header: **61,862 samples** is the correct
denominator. Exact duplicate-depth sensitivity changes only evaluation at
those ties; between-tie segments retain the original convention (last tied
age at the lower endpoint, first tied age at the upper endpoint). This is
not a complete alternative model for duplicate-depth tie points. The seven
2019 disagreements all disappear under the exact-tie sensitivity; do not
present seven as proven stale ages. Four independently read SQLite snapshots
also reproduce **7,178/35,415** common dated samples changing by over 1 Myr
from 2014 to 2023; attribution to particular update mechanisms was not tested.

Monarrez's files have 6,562 rows but 6,554 unique genus keys. Eight extra
duplicate-name rows carry identical intact histories, so matching by genus
does not change the comparison; genus-key multiplicities match across files.
Only **6,288** original histories start with zero. Thus neither "every
history lost leading zeros" nor "5,291 histories are damaged" is licensed.
The comparison uses raw OOXML decimal strings with arbitrary-precision
`Decimal`, not Python float rounding, against the intact character histories.

## Reproduce

Run on an authorised host holding the fixed mirrors. Keep working projections
and raw-derived histories in the private work directory. No installed R
packages or Python dependencies are required. The input manifests pin actual
files by SHA256 and size; check those before treating another run as this one.

```sh
# Set these to the authorised checkout, immutable mirror and a NEW work directory.
repo=/path/to/eprp
mirror=/path/to/paleodata
work=/path/to/private-audit-work
scripts="$repo/papers/infrastructure-audit/evidence/replay-20261108/data"

sh "$scripts/run_triton.sh" "$repo" "$mirror" "$work"
Rscript --vanilla "$scripts/check_dedup_membership.R" \
  "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData" \
  "$work/drop_rows.txt" "$work/out/dedup_membership.tsv"
Rscript --vanilla "$scripts/raw_mean_check.R" "$work" \
  "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData"
Rscript --vanilla "$scripts/triton_versions.R" \
  "$mirror/triton/raw/Triton_v1_13517414/triton.RData" \
  "$mirror/triton/raw/Triton_v3_13517414/triton_update_2023.RData" \
  "$mirror/triton/derived/Triton_v4_13517414/triton_update_2023.RData" \
  "$work/out/triton_versions.tsv"
python3 "$scripts/replay.py" "$mirror" "$work/out" nsb fr2 pbdb
Rscript --vanilla "$scripts/monarrez_extract.R" \
  "$repo/data/raw/monarrez2023/encounter_history_bs_gr_5class_Big5.Rdata" \
  "$work/monarrez_histories.tsv"
EPRP_AUDIT_MONARREZ_RDATA="$repo/data/raw/monarrez2023/encounter_history_bs_gr_5class_Big5.Rdata" \
  python3 "$scripts/replay.py" "$mirror" "$work/out" monarrez
```

The actual run used the equivalent staged scripts in a new data-host work
directory. The only builder adaptations redirect input/output paths and inject
the original or retained presence table; the analytical builder bodies are
unchanged. Paired outputs are under [results/before](results/before/) and
[results/after](results/after/), joined changed rows in `results/*_diff.tsv`.
Original builder SHA256s are preserved in `inputs_triton.json`; the before-arm
Q012 lineage-bin and pair-table hashes equal the committed products.

Input receipts are `results/inputs_nsb_fr2_pbdb.json`,
`results/inputs_monarrez_nsb.json`, `results/inputs_monarrez.json` and
`results/inputs_triton.json`. Narrower manifests overlap intentionally.
The first full replay preceded the explicit exact-tie sensitivity addition;
the later NSB run supplies the final sensitivity receipts. No replay output
was silently changed to match a historical claim.

Next: main Codex integrates and independently reviews the bounded claims;
Claude then adjudicates scientific wording. No expansion or provider contact
is part of this tranche.
