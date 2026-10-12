# Q-021: Shanggang and siliciclastic recovery-record support

Owner: Codex | 12 October 2026 | Accepted next task: Correspondence 76/1543.

**Decision:** the records supply more temporal coverage than Shangsi, but no
common numerical recovery sequence is ready. Retain Festningen and Waiheke
as complementary candidates for an age/formation-time contract. Shanggang
can constrain the boundary and early aftermath; it does not reach the
Middle Triassic endpoint. Do not yet build the Li adapter or treat the
records as contemporaneous observations of one seawater trajectory.

This completes a sample, chronology and evidence-role crosswalk, not a
source-model reproduction, power analysis or empirical mechanism test.
It develops the [observation contract](../../literature/2026-10-11-q021-lithium-observation-contract.md).

## Retrieved evidence and reproducible outputs

The original Cao workbook, already obtained on 11 October, is unchanged.
Rauzi's supplementary archive was obtained on **12 October 2026** from the
[Europe PMC supplementary-files API](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11317597/supplementaryFiles).
The earlier local files named as its PDF/XLSX were failed HTML/JavaScript
responses, not data; they were not used. A fresh PNAS XLSX request returned
403 and the NCBI OA lookup returned 404. The Europe PMC ZIP succeeded.

| Input | SHA-256 |
| --- | --- |
| Cao `41561_2022_1009_MOESM2_ESM.xlsx` | `6a53745faff1535d4504636fb4caa6ad18977dd1e86527e88d30b3f760e090c4` |
| Europe PMC ZIP | `9c46e74788f1e5e722540d1f23f783e3719e52f3b7679d04c442a05fe79270f5` |
| Rauzi `pnas.2318860121.sd03.xlsx` (Dataset S3) | `3f92702b0f60a9a7b1b9ecebca8508cdd1fb8dc8fc1e816addb04b33a88edd38` |
| Rauzi `pnas.2318860121.sapp.pdf` | `d1519629691b58cb60bab6a7027cec5957dc91c681f780f4c660da728071e105` |

Raw sources and HTTP receipts remain in ignored
`scratch/q021-shangsi-support/` and `scratch/q021-recovery-crosswalk/`.
GitHub readers can retrieve the linked originals and compare the checksums;
the raw workbooks/PDF are not redistributed. The source article for Rauzi
states CC BY-NC-ND 4.0; Cao is under its publisher's terms. These factual
derived tables are an internal evidence resource, not a new public data release.

```bash
python3 -I data/q021-recovery-support/build.py \
  --cao scratch/q021-shangsi-support/41561_2022_1009_MOESM2_ESM.xlsx \
  --rauzi scratch/q021-recovery-crosswalk/pnas.2318860121.sd03.xlsx
```

The standard-library build accepts only the pinned workbooks. It preserves
stored cell strings, cached values, formulas, source rows, original units
and URLs. No samples are excluded, no ages assigned and no seawater values
calculated. Outputs:

- [Shanggang measurements](shanggang_samples.tsv): Table S1 rows with a
  reported final lithium value. Ages remain in the two source columns;
  `reported_2sd_permil` retains its source uncertainty convention.
- [Rauzi measurements](rauzi_samples.tsv): Dataset S3's 305 lithium rows,
  including section labels, depth, lithology, Li concentration and elemental
  indicators. The source labels uncertainty `STD error (‰)`; it has not been
  converted to 2SD or treated as full archive uncertainty.
- [Support summary](support_summary.json): counts, source age/depth ranges
  and literal screening discrepancies. No row-count-to-power inference.

Blank fields are missing source entries. Section names and lithology strings
retain their original spaces. `depth_as_stored` must be interpreted using
`depth_header_as_stored`; centimetres and metres are not silently combined.
`source_formulas` records the source Excel formula text, if any; cached values
are not recalculated. Source `Depth` is called height in the SI figures;
this export does not alter its sign or origin. All source lithium values and
sample IDs were independently cross-checked with openpyxl, including that no
numerical lithium rows were omitted. A temporary rebuild matched all outputs;
an altered-source checksum was rejected.

## Section and chronology crosswalk

Counts below are direct workbook observations. Chronological descriptions
come from Cao Methods/Extended Data Fig. 1 and Rauzi SI sample descriptions
(PDF pp. 2–3) and Figs S2–S4 (pp. 14–16), visually inspected. These are
section-level descriptions, **not newly assigned ages for each sample**.

| Record | Li rows | Temporal support and gaps | Proposed evidence role / limit |
| --- | ---: | --- | --- |
| Cao Shanggang carbonate | 16 | Four Changhsingian, seven Induan and five Olenekian values; stored ages 252.4325–248.7667 Ma. Conodont correlations underpin the age model; original ages were harmonised to GTS2020. All 16 exported conodont-zone cells are blank | Boundary/early-aftermath carbonate constraint. No Middle Triassic recovery endpoint; stored decimal precision does not establish chronological accuracy or covariance |
| Rauzi Ubara | 24 | Upper Changhsingian–Induan; carbon isotopes, biostratigraphy and sequence stratigraphy constrain the boundary | Boundary comparison, not a complete recovery trajectory |
| Rauzi Akkamori | 51 | Two intervals: extinction boundary and later Induan/early Olenekian. Faults and separated intervals appear in Fig. S2 | Early-aftermath support; do not interpolate through the section breaks |
| Rauzi Momotaro | 48 | Separate Smithian and Spathian portions, defined with carbon isotopes and biostratigraphy | Later Early Triassic support; no measured extinction onset or continuous bridge between portions |
| Rauzi Lusitaniadalen | 19 | Upper Changhsingian–lower Induan; carbon isotopes, bioturbation collapse and facies change constrain the event | Boundary support; the biological/facies tie is not independent dating evidence for its own timing |
| Rauzi Festningen | 51 | Upper Permian–Middle Triassic, through Anisian in Fig. S4. Carbon-isotope excursions, sequence stratigraphy and biostratigraphy; an igneous sill intersects the section | Broad shelf recovery candidate. No numerical sample ages or covariance in Dataset S3; local source changes and thermal history need explicit treatment |
| Rauzi Waiheke | 112 | Late Permian–Middle Triassic, through Anisian. Part of Induan/lower Olenekian unexposed because of faulting; another fault is marked within the Anisian. Carbon-isotope and conodont correlations | Broad deep-marine candidate complementary to Festningen, with a large gap. The high-Li observations already set a model-selection constraint in Rauzi |

The 305 Rauzi rows reproduce the main-text regional totals: Japan 123,
Svalbard 70, New Zealand 112. They contain depths but **no numerical age
column**. There are two split Japanese records, not six continuous time
series. No new numerical cross-section alignment or sample-age covariance
has been recovered. Rauzi's 254–246 Ma model forcing range is not a supplied
age model for these observations.

### Source discrepancies retained

Cao Methods reports 15 Shanggang Li samples, but 16 Table S1 rows contain
final values. Row 62 (SG-10-0.1) stores Q-ICP-MS 0.2‰ and final 1.2‰ with
no other visible Li replicate. Seven exported rows have Mn/Sr at least 3,
the main-text selection threshold; two (42, 58) are also at least 4, the
SI threshold. Row 43 retains its radiogenic-Sr asterisk. The SI further
discusses high-Mg phases and distinct carbonate fractionation. These are
unresolved source/reporting flags, not grounds for choosing a preferred
value, dropping a row or declaring the paper's conclusion false. The
earlier [Shangsi check](../q021-shangsi-support/README.md) also records the
carbonate-offset sign ambiguity. Keep measured values separate from any
future seawater reconstruction.

## The observation time is not necessarily the depositional time

**Source claim:** Rauzi SI, “Locus of marine clay authigenesis” (PDF
pp. 4–5), explicitly interprets high pre-extinction sediment values as
possible post-extinction clay formation on older material. Upper Permian
samples can therefore be included in the plotted Early Triassic warm-period
group; the SI also reports sensitivity excluding them. This is an archive
interpretation, not directly measured formation ages.

**Consequence for Q-021 (inference):** an improved depositional chronology
alone would not establish timing of the Li-bearing authigenic component.
For a temporal comparison, each sample needs a constrained distribution of
formation times, as well as its detrital/authigenic Li mixture and section
effects. The existing instantaneous archive mapping must be extended where
formation is delayed or distributed through burial. Any such averaging must
respect Li amounts/isotope fractions, as in the shared contract; a sediment
mass-weighted average of delta values is not the required operation.

This strengthens the objection to a simple lead–lag test. It does not prove
that the record is uninformative. Broad state contrasts or one-sided
composition constraints may remain useful under weaker chronology assumptions.
The strongest rival explanation for a measured shift remains changing local
detrital delivery, fractionation or authigenesis timing without the proposed
change in global biological feedback.

## Evidence reuse and the next discriminating step

| Evidence | Published use verified | Contract for a future comparison |
| --- | --- | --- |
| Cao carbonate Li and assumed carbonate–water offset | Defines seawater targets in a steady-state box-model exploration | Evaluate measured carbonate under explicit offsets; do not count fitted reconstruction targets as held-out evidence |
| Rauzi temperature composite | Drives the lithium model and inferred weathering | Shared forcing or calibration, not an independent temperature prediction |
| Waiheke high Li | Supplies a minimum seawater constraint used to filter simulations | If retained for selection/calibration, do not count that same bound again as independent validation |
| Shale mean and multi-section range | Compared with filtered and unfiltered outputs | Declare their use before comparison; pooled values are neither independent samples of seawater nor a ready time series |
| Carbon-isotope, fossil and facies ties | Help correlate sections and delimit events | Propagate shared correlation errors; do not use the same alignment to claim independent synchrony |

The newly accessed SI preserves adverse and supporting evidence together.
Its unfiltered analysis retains the reverse-weathering interpretation of
the shale mean. Removing Waiheke, however, lets both model scenarios cover
the remaining observed range (SI “Unfiltered model results”, p. 12;
Figs S13–S16). Thus the reported full-range discrimination and the pooled-mean
comparison are different tests. Neither is a held-out test of Xu versus
Isson's biological mechanisms.

**Proposed next bounded gate:** for Festningen and Waiheke, trace the existing
chronology citations into a section-segment/biozone tie table and assess what
constrains authigenesis time. Ask whether these support a coarse
Early-to-Middle-Triassic state contrast with independently constrained mixing
and shared age uncertainty. If temporal formation support fails, retain only
the composition constraint and explicitly retire the timing test for these
records. A negative timing result does not park Q-021. This is a proposal for
Claude's response, not an accepted allocation or permission to fit a model.

## Access scope

Targeted retrieval, 12 October; no novelty search. Sources:
[Cao et al. 2022](https://doi.org/10.1038/s41561-022-01009-x), original Table S1,
Methods, Extended Data Fig. 1 caption and SI screening discussion;
[Rauzi et al. 2024](https://doi.org/10.1073/pnas.2318860121), main Results/Methods,
original Dataset S3 and the named SI sections/figures. Cao's publisher page
failed through the web reader; its previously retrieved official workbook
and institutional full-text PDF were usable. No author was contacted and
no native model or Li adapter was run.
