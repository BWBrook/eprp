# Q-021: Shangsi sample support and a conditional design check

Owner: Codex | Retrieved and checked 11 October 2026

**Result:** six analysed carbonates span about 7.97 Myr, with **one Induan
measurement and five Permian measurements**. Shangsi alone does not supply
a sequence through Early Triassic recovery. Retain it as a possible baseline
and early post-boundary constraint, not the proposed recovery-timing record.
This is a source-support result, not evidence against either biological
mechanism or lithium as a proxy.

## Source and preserved values

Source: Cao et al. 2022,
[10.1038/s41561-022-01009-x](https://doi.org/10.1038/s41561-022-01009-x),
official [Supplementary Table S1 workbook](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41561-022-01009-x/MediaObjects/41561_2022_1009_MOESM2_ESM.xlsx).
SHA256: `6a53745faff1535d4504636fb4caa6ad18977dd1e86527e88d30b3f760e090c4`.
The [supplementary PDF](https://media.springernature.com/original/springer-static/esm/art%3A10.1038%2Fs41561-022-01009-x/MediaObjects/41561_2022_1009_MOESM1_ESM.pdf)
has SHA256 `64d0811128412813f25286b80584e3d2cb4d1e36b34232c158b926e78824bd5c`.
Public asset links came from article HTML; the earlier browser failure did
not establish unavailable data. No raw publication files are committed.

[shangsi_samples.tsv](shangsi_samples.tsv) preserves original numeric strings,
both age columns, source stages, visible replicate values and the reported
SD formula. The table below rounds ages for display only.

| Workbook row | Sample | Study age (Ma) | Source stage | Carbonate δ7Li (‰) | Reported 2SD (‰) |
| --- | --- | ---: | --- | ---: | ---: |
| 69 | SS005605-5 | 259.3818 | Capitanian | 7 | 1.1 |
| 70 | SS006300-5 | 259.1850 | Capitanian | 12.2 | 1.1 |
| 71 | SS006900-5 | 259.0254 | Wuchiapingian | 12.5 | 1.1 |
| 76 | SS018585-2 | 253.3466 | Changhsingian | −2.1 | 1.9578 |
| 78 | SS022169-3* | 252.3157 | Changhsingian | 0.2 | 1.1 |
| 80 | SS030104-2 | 251.4093 | Induan | −0.25 | 1.1 |

The source labels depth, not height; its calculated-age header spells the
timescale “GST 2020”. We retain source values rather than silently harmonise
them. Decimal precision is not dating precision. Neither this table nor
the inspected SI supplies a joint sample-age uncertainty model.

Three source flags matter before empirical scoring:

- **Row 76:** the visible replicate values −2.98, −1.7 and −3.9 average
  −2.86, not the stored final −2.1. The formula `2*STDEV(L76:P76)` includes
  that final-value cell. The extractor preserves both; it does not declare
  which value is correct or reinterpret the reported SD as a sampling SE.
- **Row 78:** the source asterisk flags radiogenic Sr. Its stored Mn/Sr is
  3.6174; the main-text screening threshold is below 3 whereas the SI uses
  below 4. No sample is silently excluded by this extraction.
- **Archive conversion:** the main text says to subtract 5.5‰ from carbonate
  while naming the offset seawater minus carbonate. An explicitly signed
  observation equation is needed. We retain measured carbonate values and
  perform no seawater correction.

These are provenance/interpretation flags, not a reanalysis of the paper's
conclusions. The source stage for row 70 also differs from the corresponding
main-text description; it remains unchanged here.

## What a cheap design calculation can establish

Claude proposed a six-sample power calculation before obtaining native model
trajectories. A conditional design check is useful now. An empirical power
claim still needs the rival contrast, constrained transformations, age model
and error covariance; six independent errors cannot be inferred from six rows.

For an explicit counterexample, consider a perturbation to the **same**
baseline, with a first-order response

```text
u(t; A, t0, tau) = 0                              for t <= t0
                = A [1 - exp(-(t-t0)/tau)]        for t > t0.
```

On the reported point-age grid, an illustrative origin at 252 Ma leaves
only the last observation after onset. Holding tau at 1 Myr, amplitude 1‰
with onset 0 and amplitude 1.544918‰ with onset delayed 0.25 Myr produce
**identical perturbations at all six observation times**. Both predict
0.446061‰ at the last sample. Their predictions at 3 Myr differ.

More generally, for any later onset before the sole post-onset sample,
choose amplitude to match that one response. The amplitude and onset
sensitivities have only one nonzero row and cannot be identified separately
in this family, even with exact ages and a known baseline. This is a
constructive limitation of this design/model pair; fixed, independently
constrained rival histories could still differ at the single observed time.
No measured Li values were fitted or used to set these amplitudes.

The [check output](design_check.json) records all inputs and predictions.
Tau = 1 Myr is illustrative. Cao cites a roughly 1 Myr **modern** residence
time; it does not measure the Triassic inventory/flux ratio or isotope
relaxation time. In a simple linear response, high-frequency forcing is
attenuated, not completely erased. Amplitude, chronology, archive uncertainty
and the rival waveform jointly determine whether magnitude or timing is
more informative. No universal ranking follows from residence time alone.

**Next useful evidence:** a record with multiple observations within the
recovery interval, an age/dependency crosswalk and a constrained rival contrast.
Check the already identified Shanggang/siliciclastic records before building
an adapter. Shangsi may contribute jointly, but is not a six-point recovery
series. No source models or Li fits were run.

## Rebuild and verification

Download the linked workbook to an ignored cache, then run:

```bash
python3 -I data/q021-shangsi-support/build.py --source /path/to/41561_2022_1009_MOESM2_ESM.xlsx
```

Python standard library only. The script rejects a mismatched SHA256,
extracts the named six rows with source strings intact, and checks the
conditional counterexample and row-76 formula. `--output-dir` allows an
isolated reproduction. It makes no network requests or source edits.

Main-text Methods, SI screening text and Table S1 cells were inspected.
Source chronology inputs, complete proxy calibration and native flux
trajectories remain unverified. A GPT-6.1 Sol subagent retrieved the sources;
Codex integrated the extraction and checked the inference. No author contact.
