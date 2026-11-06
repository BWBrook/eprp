# Boag and Schachat: two bounded register checks

Owner: Codex. Checked 6 November 2026, Australia/Hobart.
Scope: Q-027 and Q-032 source wording only; no register edit, reanalysis or
change of scientific priority. Access was to independently sourced open
material. No restricted Elsevier XML, text or excerpt budget was used.

## Boag, Gearty and Stockey 2021 — qualify Q-027

DOI: [10.1016/j.cub.2021.04.021](https://doi.org/10.1016/j.cub.2021.04.021).
The [register](../ideas/register.md#q-027-is-the-latitudinal-diversity-gradient-a-climate-state-variable)
reports a non-monotonic temperature relationship combining metabolic kinetics
with the Metabolic Index, and says spatial sampling bias was not modelled.

**Confirm the reported relationship.** Main text pp. 2906, 2908–2910,
Figures 3–4, and STAR Methods e3 describe the thermal hump and combined
kinetic/aerobic-habitat model. This confirms what the authors report, not
independent validation of their mechanism.

**Qualify the sampling statement.** Strong counterevidence occurs on p. 2908
and STAR Methods e2: geographic occurrence maps, coverage against latitude
and temperature, SQS, alternative binning/diversity estimators and quorum
sensitivities. STAR Methods e3 repeats regression fitting at sampling cutoffs
of 30, 50 and 200 occurrences. Thus sampling bias was explicitly investigated.

**Narrower remaining limitation — inference.** The specified regression
candidates use temperature; the inspected methods do not specify region
effects, regional reweighting or a separate spatial observation model. Their
coverage diagnostics do not by themselves establish that uneven regional
representation is harmless. Describe this narrower unresolved control rather
than imply no sampling treatment. No code or separate supplementary-file
audit was performed.

### Open provenance

- Source: coauthor [William Gearty's publications page](https://williamgearty.com/publications/),
  which directly links the [paper PDF](https://williamgearty.com/assets/pdf/Boag%2C%20Gearty%2C%20and%20Stockey%202021%20Current%20Biology.pdf).
- Retrieved independently on 6 November. The 12-page file carries final
  journal pagination 2906–2913 and STAR Methods e1–e3, dated 12 July 2021.
  It is an author-hosted journal PDF, not the restricted API acquisition.
  Public availability does not imply a new redistribution licence.
- PDF SHA256: `9292cc74182758aef7e703498053e31c44d4f1f7c25eba6e826fdd34c5a606d2`.
- `pdftotext -layout` output SHA256:
  `616764d5e95d4282c257205c3fe9f582d79d06aeb4527e3936559093253a4d38`.
- Access depth: main results and relevant STAR Methods; e2 also rendered
  and visually checked. No numerical replay or reading of unheld supplement.

## Schachat et al. — confirm for the preprint; final version unresolved

Final DOI: [10.1016/j.revpalbo.2021.104564](https://doi.org/10.1016/j.revpalbo.2021.104564).
The [Q-032 residual](../ideas/register.md#q-032-have-insects-had-ecological-crises-that-family-counts-miss)
concerns change exceeding expected change without an event.

**Confirm, version limited.** In the 25 October 2021 preprint, §4,
pp. 15–17, numbered lines 384–432, develops that ordinary-change null and
leaves its estimation to future datasets. Conclusions §7, pp. 21–22,
lines 528–537, retain it as unresolved. The register's narrow counterfactual
claim is supported for this version.

**Counterevidence to any broader absence claim.** §6, p. 20, lines 488–501,
uses coverage-based rarefaction to reassess 17 end-Cretaceous/Paleogene beds
and supports lower subsequent damage diversity while emphasising within-period
variation. The paper therefore includes an empirical before/after comparison.
That comparison is not an estimated distribution of ordinary temporal change
in the absence of the event. Neither finding licenses saying no extinction
analysis was performed.

**Unresolved:** equivalence to the final 2022 journal article. Cite the checked
preprint explicitly; do not silently promote its claims to a final-version
audit. Q-032's parked status is unchanged.

**Parent follow-through, later on 6 November:** the published XML was then
retrieved and targeted passages compared with this public preprint. The
[integrated check](2026-11-06-register-claims-after-elsevier.md) closes the
narrow version check for the proposed counterfactual while retaining the
limits on whole-article equivalence and analytical validation. The independent
preprint-only check above should not be read as a claim that the final text
remains unavailable.

### Open provenance

- Version: [bioRxiv preprint, 25 October 2021](https://www.biorxiv.org/content/biorxiv/early/2021/10/25/2021.07.16.452692.full.pdf),
  DOI `10.1101/2021.07.16.452692`. The PDF header identifies a preprint and
  CC BY 4.0. It contains 52 pages, including supplementary material.
- Read-only source: canonical open library, work `W3214080352`; existing
  manifest retrieval time `2026-10-23T10:02:14Z`. Version attribution
  here follows the inspected PDF header. The manifest's `acceptedVersion`
  label likewise does not establish identity with the published article.
- PDF SHA256: `7c4b5e748e4e72767365dda36241c65169d73b3857ffcaa96b4a67b011429a96`.
- Existing extracted text SHA256:
  `9db731093057ad846ea12ad1a7b005c2167c71dde90beaa15a43dd7d08ae3e5c`.
- Access depth: specified sections, numbered lines and version header;
  p. 20 rendered and visually checked. No reanalysis or final-version diff.

## Retrieval boundary and next action

Searches used the two exact DOIs, the exact titles and primary author or
institutional locations. Boag was recovered directly from a coauthor;
Stanford also lists an openly hosted copy, which was not substituted for the
hashed source. Exact Schachat searches at Stanford, Smithsonian and bioRxiv
did not establish an open final version. The public ScienceDirect landing
page returned HTTP 403; the bioRxiv web-tool request also failed, but the
already-held openly licensed PDF was readable. Those access failures are not
evidence of absent analyses.

Ignored local check material is under `scratch/boag-schachat-20261106/`:
`boag-author.pdf`, `boag-author.txt`, `schachat-preprint.pdf`,
`schachat-preprint.txt` and two page renders. Reproduce the text extraction
with `pdftotext -layout boag-author.pdf boag-author.txt` and compare the
hashes above. No full text or images are included in this repository note.

References Codex next integrates the qualifications and, if useful, registers
the independently recovered Boag copy through the staged import route.
The canonical library was not changed. A final-version Schachat check remains
open only if a legitimate readable copy becomes available; no further
restricted-text query is needed to support the conclusions above.
