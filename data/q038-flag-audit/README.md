# Q-038: independent audit of the deposited survival-model design

Owner: Codex | 11 October 2026 | Design construction verified; no CMR fit

This checks the flag claim in [Claude's data contract](../q038-monarrez-contract/README.md).
Barry lifted the earlier deferral in Correspondence 76/1515. The audit does
not select Q-038 as a primary investigation.

## Result and scope

**The one-occasion displacement is confirmed for the deposited inputs and
model specification under historical RMark 3.0.0.** Constructing the actual
design with `process.data`, `make.design.data` and `make.mark.model` assigns
`mass.ext39` to Phi for 39→40 (Induan→Olenekian), while 38→39
(Changhsingian→Induan) uses `mass.ext38 = 0`.

| Deposited flag | Phi transition carrying it | Transition into the flagged stage |
| --- | --- | --- |
| 8 | Rhuddanian→Aeronian | Hirnantian→Rhuddanian, 7→8 |
| 22 | Famennian→Tournaisian | Frasnian→Famennian, 21→22 |
| 39 | Induan→Olenekian | Changhsingian→Induan, 38→39 |
| 46 | Hettangian→Sinemurian | Rhaetian→Hettangian, 45→46 |
| 69 | Danian→Selandian | Maastrichtian→Danian, 68→69 |

The [complete mapping](phi-mapping.tsv) uses stage names and ages in the
deposited occurrence CSV. Frasnian→Famennian is the authors' chosen Late
Devonian boundary; this does not settle treatment of other extinction
pulses or the Hangenberg event.

This confirms code behaviour, **not the provenance of the paper's fitted
coefficients or a change to its scientific conclusions**. The authors'
installed RMark version is unknown. RMark 3.0.0 was published in August 2022;
the official archive lists no intervening release before the 2023 study.
The full Bivalvia histories and the authors' duplicate-named
`design.parameters` list were retained. Default model checks passed. No
MARK executable, optimisation or model averaging was run.

## Further corrections to data readiness

- **Five-class reconstruction is incomplete.** The cleaned occurrence CSV
  contains 253,747 rows but no Strophomenata or Trilobita. Bivalvia (88,856),
  Gastropoda (53,673) and Rhynchonellata (57,297) match the paper's counts.
  The paper's total of 242,871 additionally includes 33,935 Strophomenata and
  9,110 Trilobita. Other classes account for the remaining deposited rows.
  This is more than a discrepancy with the README's total of 284,309.
- **Published coefficient provenance remains unresolved.** Sorted classes
  in the capture histories are Bivalvia, Gastropoda, Rhynchonellata,
  Strophomenata and Trilobita. Deposited scripts 05c/05d/05e select indices
  4/5/6 respectively; the last is missing. The 05 scripts save `class6`
  filenames while 06 loads `class5`. No repair or inference about which
  scripts produced published results follows from these observations.
- **Subgenus elevation was intentional.** The paper explicitly treats
  subgenera as genera. The 811 subgenus-style rows, 769 with a represented
  base name, require a taxonomic-unit/observation-overlap audit. Name nesting
  alone does not establish duplicate observations or justify automatic collapse.
- **Same-stage range is not a complete prospective predictor contract.**
  All absent capture cells have zero range, but so do 812 of 29,486 present
  cells. The transformation is `log10(distance + 1)`, then within-class/stage
  standardisation and replacement of resulting missing values by zero.
  Zero has several meanings. Lagging a column does not resolve taxonomic
  ascertainment, missing ranges, standardisation or the timing of body-size
  measurements. Those must be audited for any prospective prediction target.
- **Observed last occurrences are not known biological deaths.** Their
  concentration before the flags supports a descriptive check, not validation
  of a CMR estimate. Gamma uses matching `rec.mass` suffixes; biological
  recovery attribution under reverse-time seniority remains unadjudicated.

## Reproduce

From the repository root, with Python 3.12 and base R:

```bash
python3 data/q038-flag-audit/fetch_sources.py
Rscript --vanilla data/q038-flag-audit/probe.R
cmp data/q038-flag-audit/phi-mapping.tsv scratch/q038-independent-audit/phi-mapping.tsv
```

The fetcher verifies the historical CRAN archive SHA256 and the deposited
author-script MD5 values in [the manifest](author-source-manifest.json).
Downloaded sources and generated outputs stay under ignored
`scratch/q038-independent-audit/`; `Q038_AUDIT_DIR` overrides that directory.
The probe loads unmodified package source without installing it. Its only
shim redirects package resource lookup to the extracted `inst/` directory.
The Dryad inputs must already be in `data/raw/monarrez2023/`, with checksums
as recorded in Claude's contract. The independent run and parent rerun used
R 4.6.1 and reproduced the tracked mapping exactly.

## Primary evidence

- [Official RMark archive](https://cran.r-project.org/src/contrib/Archive/RMark/),
  `RMark_3.0.0.tar.gz`, SHA256
  `08a20f4246dcfe6a8bfe8acd673346b79dc1b9b42a4354d865364f577329305b`.
  `inst/parameters.txt:39–41` gives Pradsen defaults;
  `R/process.data.R:147–148` gives `begin.time=1`, `reverse=FALSE`;
  `R/compute.design.data.R:236–242` assigns beginning-time labels;
  `R/make.mark.model.R:1762–1763` matches covariate suffixes.
- [Deposited author code, record 7816408](https://zenodo.org/records/7816408):
  script 04:20–33 sets ordering and flags; 04:80–85 standardises ranges;
  05a:22–23, 34–41, 64–65 specifies processing and the model;
  05c/05d/05e:19 selects classes; 05a:70 and 06:5 expose filename differences.
- [Monarrez et al. paper](https://doi.org/10.1098/rsos.230795), Methods pp. 3–4,
  read through the [NSF-deposited PDF](https://par.nsf.gov/servlets/purl/10514226):
  taxonomic convention, range construction and occurrence counts.

Claude's next response should correct the contract's readiness claims and
separate deposited-design behaviour from published-result provenance. No
author contact or full refit is authorised by this audit itself.
