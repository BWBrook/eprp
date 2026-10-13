# Q-021: Taylor carbonate sample and archive audit

Owner: Codex | 13 October 2026 | Accepted in Correspondence 76/1581 after
Barry's explicit request for the Taylor audit.

**Decision: stop Taylor alone as the next empirical mechanism-discrimination
route.** Its records support descriptive within-section carbonate Li changes,
already analysed in the paper. They do not yet bound the contribution of
changing carbonate formation, alteration or local-water composition to those
changes. Retain the data and close prior; do not build the Li adapter from
this package. This is unresolved feasibility, not demonstrated impossibility
or a calibrated upper limit on either biological mechanism. Q-021 remains
under review/tier 2; other observation routes remain open.

This completes the [route review's](../../literature/2026-10-13-q021-route-review.md)
sample/age/alteration/evidence-role task and updates the
[observation contract](../../literature/2026-10-11-q021-lithium-observation-contract.md).
No hypothesis test, source-model fit, adapter or primary investigation was run.

## Sources and reproducible extraction

Taylor et al. (2026), *American Journal of Science* 326, article 5,
[10.2475/001c.156171](https://doi.org/10.2475/001c.156171), published 23 March.
Main scientific text pp. 1–18, relevant figures, all Table S1 cells, and
supplement text/tables were inspected. An independent Codex subagent checked
chronology, alteration and evidence roles; this does not replace Claude's review.

The data DOI [10.26207/xah3-3r67](https://doi.org/10.26207/xah3-3r67) resolves
via DataCite to a [ScholarSphere record](https://scholarsphere.psu.edu/resources/a97f2d40-a265-4db6-ac30-a4cd13d1d031).
Its landing page was obtained with `?download=1`; it lists version 2, updated
8 April 2026, accessible-copy DOCXs and CC BY 4.0. Direct repository file
requests either reset or returned HTML, **not DOCX data**. The successful
files audited here are the publisher attachments below; identity with the
repository's accessible copies has not been established.

| Pinned input | Bytes | SHA-256 |
| --- | ---: | --- |
| [Publisher Table S1](https://ajsonline.org/article/156171-heterogeneous-carbonate-lithium-isotope-records-across-the-end-permian-mass-extinction-indicate-a-highly-perturbed-lithium-cycle-in-the-early-triassic/attachment/333328.docx) | 39,830 | `5a34ca9c21319466353d0904c0155a1d178838f9bbf2b4e150702cc746629fc6` |
| [Publisher supplement](https://ajsonline.org/article/156171-heterogeneous-carbonate-lithium-isotope-records-across-the-end-permian-mass-extinction-indicate-a-highly-perturbed-lithium-cycle-in-the-early-triassic/attachment/333327.docx) | 718,271 | `b910d9f7d8dcd7570283cd9605d3957bc069feb876e8c21b32e98e4b32c22249` |
| [KIT main PDF](https://publikationen.bibliothek.kit.edu/1000191820/178006672) | 2,569,104 | `4f06e29c8ccfbd0f55b84213785646714a2c4169fd13337ea03f30d6946adc5a` |

Attachments were retrieved 13 October 2026 at 01:22 UTC. The working URLs
include the full article path: the previously attempted bare
`https://ajsonline.org/attachment/...` addresses are not equivalent. This
resolves the earlier supplement-access limit. Searches used the data DOI,
exact article title and ScholarSphere metadata, then followed the publisher's
actual attachment links. This was a bounded source retrieval, not a novelty survey.

Raw DOCXs, landing page, metadata, receipts and rendered checks are retained
in ignored `scratch/q021-taylor-audit/`; the main PDF remains in
`scratch/q021-formation-timing/`. No raw source document is redistributed in Git.
The factual extract is an internal resource with source attribution; the
repository's CC BY licence is recorded without claiming byte identity between
its files and the publisher attachments.

```bash
python3 -I data/q021-taylor-support/build.py \
  --table scratch/q021-taylor-audit/table-s1.docx
```

The standard-library build verifies the source checksum and table schema.
[table_s1.tsv](table_s1.tsv) preserves all **83 measurement rows**, including
the 19 attributed to Cao. No row is excluded or silently repaired.
[support_summary.json](support_summary.json) records coverage, missingness,
duplicate identities, source-stage summaries and descriptive contrasts.

Dictionary: the 15 source fields retain the literal cell text; units are in
the column names and the original header/caption is retained in the summary.
`NA` remains the literal source missing marker; `0.00` is not changed into a
missing value. `docx_table`/`docx_row` are one-based XML table/row locations,
including caption and header rows. `labelled_duplicate` identifies the literal
`-dup` suffix; `base_id_from_suffix` removes only that suffix. These two derived
fields expose dependence without editing measurements. `source_doi` points
to Taylor, and `reference` distinguishes its measurements from reused Cao data.
The printed isotope heading uses delta; its XML text yields `d7Licarb`.

Verification: an independent `python-docx` reader matched all 1,245 source
fields; all three rendered table pages were visually checked. A fresh build
reproduced both outputs byte for byte, and an unpinned input was rejected.
All 19 reused Cao IDs, stages, ages and isotope values matched the existing
extracts at the published precision. Source hashes, local links and unchanged
register statuses/tiers were checked. These are extraction and consistency
checks, not validation of the paper's statistical pipeline or Q-021 mechanisms.

## What temporal contrast is actually supported?

| Source section | Rows / base IDs | Source-stage row counts | Nominal measured age range |
| --- | ---: | --- | --- |
| Taskent | 35 / 34 | Changhsingian 8; Induan 10; Olenekian 9; Anisian 4; Ladinian 1; Carnian 3 | 252.93–235.18 Ma |
| Takachiho | 29 / 26 | Changhsingian 1; Induan 9; Olenekian 9; Anisian 10 | 252.99–240.53 Ma |
| Shanggang, reused Cao | 16 / 16 | Changhsingian 4; Induan 7; Olenekian 5 | 252.43–248.77 Ma |
| Shangsi, reused Cao | 3 / 3 | Changhsingian 2; Induan 1 | 253.35–251.41 Ma |

**Defined descriptive contrast:** within each Taylor section, mean measured
carbonate δ7Li for source-labelled Anisian samples minus the mean for
source-labelled Induan plus Olenekian samples. The raw-row differences are
**+7.96‰ at Taskent** (4 versus 19 rows) and **+7.93‰ at Takachiho** (10 versus
18). Averaging only each explicitly labelled duplicate pair and then weighting
base samples equally gives +7.96‰ and +7.94‰. This sensitivity preserves the
direction; it does not decide the correct replicate or error model. No standard
error, p-value or power is inferred from these row counts.

The broader Taskent Anisian–Carnian contrast is +8.76‰ with all rows and
+9.05‰ with equal base-sample weights. It combines a different duration from
Takachiho. Even the narrower common stage label is not a matched window:
Taskent's Anisian-labelled values are 242.00–240.59 Ma; Takachiho's are
247.75–240.53 Ma. Retain those source labels and ages together, without
quietly choosing a replacement time scale.

Taskent's last Olenekian measurement (`TK-464.5`, 247.08 Ma) and first Anisian
measurement (`TK-627`, 242.00 Ma) are **5.08 Myr apart**. This is a gap between
retained Li samples, not a geological hiatus or a measured recovery duration.
Takachiho's corresponding point-age gap is 0.89 Myr (`TCD-2.7`, 248.64 Ma, to
`TCD-3.75`, 247.75 Ma), but its Spathian is mostly missing, with an inferred
unconformity and an arbitrary covered interval in Fig. 4. Its TCB and TCD
heights are distinct section coordinates; the table supplies no composite
height transformation. Sorting all Takachiho rows on raw height would be wrong.

The broad rise is an occupied descriptive result (Taylor §§3, 5). It does
not yet measure onset, lag, global seawater recovery or either flux contribution.

## Chronology, archive mapping and source conflicts

**Shared chronology (main §2.1, pp. 3–5).** Taskent is correlated to dated
Guandao using fossils, lithology and carbon isotopes, updating Lau 2016/2017.
Takachiho is correlated to Taskent with carbon isotopes/lithology and conodont
constraints. Ages interpolate at constant sedimentation between ties. Table S1
supplies point ages but no tie-point table, joint uncertainty, sample age bounds
or Li-incorporation ages; the inspected supplement adds none. Site clocks and
samples within a tied interval cannot be treated as independent. Existing
upstream chronology sources could add detail, but that would not by itself
resolve the archive-mapping limitation below.

**What was measured (main §2.2, pp. 5–6).** Selected carbonate chips were drilled
to avoid veins/heterogeneity, prewashed, and subjected to three pooled weak-acid
leaches. Al/Ca >0.8 mmol/mol was excluded before isotope processing, then a
minimum Li amount was required. All new Taylor rows are below the Al/Ca cutoff
(maxima 0.73 and 0.25). The table contains elemental ratios and Taskent carbonate
content, but no sample-linked original/current mineral phase, pass/fail
alteration field or excluded-sample inventory. Selection does not certify
constant fractionation or primary formation time.

**Strongest rival (main §§4.2–4.3, pp. 9–13; §5, p. 15).** Taskent's 18 paired
Ca/Li samples support archive assessment, but their positive association
(ρ=0.57, p=0.02) is compatible with diagenesis as well as primary stratigraphic
change. The authors explicitly allow a shift toward fluid-buffered diagenesis
to contribute to the later Li increase. Takachiho lacks Ca-isotope constraints;
its Lower Triassic dolomite is coarsely recrystallized and its Li-fluid mapping
is uncertain. Taylor also allows pH/growth-rate effects of up to approximately
11‰ and a partial contribution from their recovery. That magnitude is relevant
to the roughly 8‰ contrasts above, but is **not** a sample-calibrated nuisance
bound or proof that all observed change is alteration. Common pH changes could
affect both sites, so matching directions do not remove this rival.

**Supplementary controls have narrower roles.** Fig. S5's stricter Takachiho
Al/Ca screen addresses contamination. Table S5's pooled additive regression
uses section, stage and four log elemental ratios; residual stage effects do
not calibrate phase, pH, growth, changing fluids or formation time. Only 12/35
Taskent rows and 27/29 Takachiho rows have all four positive, nonmissing ratios
needed by that specification. The supplement does not identify fitted rows,
duplicate handling or missing-value policy; we did not infer or rerun them.

Keep these discrepancies visible before any quantitative reuse:

- Methods' 34/26 samples match base IDs, while Results' 35/29 totals match
  measurement rows. However, Takachiho's source stage counts are 9 Induan and
  9 Olenekian, versus 8/10 in Results; their raw-row means also differ slightly.
  The table alone therefore does not reconstruct the published grouping.
- **33/35 Taskent `err.` values are below 0.36‰**, although the caption defines
  error as the greater of repeat-analysis and bracketing-standard 2SD and
  Table S2 gives 0.36‰ for Yale. Keep the literal errors; do not silently inflate
  them or treat them as total archive uncertainty. Takachiho's minimum is 0.89‰,
  whereas its stated bracketing reproducibility is 0.58‰.
- The four labelled duplicate-pair differences are 1.96, 8.68, 4.40 and 6.76‰.
  They do not recover the main text's reported 2.2‰ average difference for four
  powder duplicates. The exact relationship between those statements and rows
  is unresolved; no replacement repeat-error model is inferred.
- Main p. 10 calls Takachiho's Mn/Sr–Li association significant, but Table S4
  gives ρ=−0.29, p=0.15. Treat that as a source conflict. Earlier screening
  counts and prose age/stage endpoints also differ from Table S1; the extract
  retains the table rather than repairing it from prose.
- `TCD-9.9` has height 9.7 m and `TCD-12.6` has height 12.7 m. IDs need not be
  coordinates; preserve both. Taskent `TK-426` has Li concentration `0.00`
  at the table's precision; it is not proof of zero lithium.

## Evidence roles and reuse

| Evidence | Already used for | Downstream implication |
| --- | --- | --- |
| δ13C, lithology, conodonts and Guandao ties | Age alignment; δ13C also supports Takachiho preservation | Alignment and preservation arguments share evidence; carry common chronology uncertainty |
| Taskent δ18O near the Spathian–Anisian contact | Avoiding potentially meteoric-altered samples | Transition coverage is selection-dependent; omitted identities and their contribution to the measured-sample gap are unresolved |
| Al/Ca, Li yield, elemental ratios and paired Ca isotopes | Selection and archive interpretation; the Li regression uses the same rows | These checks are not independent held-out evidence for the resulting interpretation |
| 19 Cao rows | Previous carbonate measurements and model interpretation | All 19 IDs exactly match existing EPRP Cao extracts, with Li values and ages consistent at printed precision; do not count them twice |
| Rauzi siliciclastic rows and Fig. 7 envelopes | Prior mechanism interpretation and inferred seawater constraints | Reused observations and their smoothed envelopes are not new replication |
| Chert gap/return and temperature | Mechanism context; source scenarios may already use them as forcing/calibration | Retain scenario-specific evidence roles before evaluation |
| Rauzi-derived riverine Li and cGENIE dye | Illustrating transport to Takachiho | No Li isotope/removal fit; the supplement excludes Turkey/South China transport from its remit |

The supplement also qualifies the siliciclastic-to-seawater inequality: its
argument assumes diffusion-dominated marine diagenesis. It admits an advective
Rayleigh countercase while arguing against that setting for these records.
This is an assumption to carry, not evidence of such alteration at Waiheke,
and it supplies no authigenesis-time bound.

For a within-section contrast, writing measured carbonate Li schematically as
`local-water Li − fractionation + alteration` shows the limitation: subtraction
eliminates a constant offset, but leaves the temporal changes in fractionation,
alteration and local-to-global water composition. The inspected evidence does
not bound those terms tightly enough for a declared rival prediction contrast.
Resolving the printed error discrepancy would not remove that limitation.

**Next responder: Claude.** Adjudicate the stop decision and the conditions for
reopening: an independently supported temporal archive/local-water mapping,
a non-occupied prediction contrast and explicit joint evidence roles. A coarse
contrast robust to justified bounds could suffice; direct mineral dates are
not mandatory. Do not allocate another Taylor-only chronology cleanup as if
it would automatically supply mechanism discrimination.
