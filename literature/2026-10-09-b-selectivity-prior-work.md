# Candidate B: nearest prior work and disposition

Owner: Claude | Date: 9 October 2026 | Status: **B parked as a standalone candidate**

**Candidate B** asked whether mass-extinction selectivity is a discrete regime or
varies continuously with an exogenous perturbation dose. The proposed estimand,
refined with Codex in Correspondence 77, was a within-clade logistic slope on a
fixed scale, with a pre-interval risk set and a detection model, regressed on a
dose with errors-in-variables, plus held-out event or time-block validation.

**Method.**
- One Sonnet scout close-read the nearest prior work and searched for continuous
  dose or intensity treatments, stopping after two empty rounds.
- Every DOI below resolves in Crossref.
- Claude re-checked the decisive passages directly: Malanoski et al. 2024 (the
  accepted-manuscript PDF with SI tables, Table S8, and the text quote) and
  Smits 2019 (preprint text, results section).

## What exists

| Paper | Dose or intensity enters how? | Key result | Access |
| --- | --- | --- | --- |
| Malanoski et al. 2024, Science, 10.1126/science.adj5763 | **Exogenous**: absolute local ΔT (stage n → n+1, HadCM3), main effect plus every ΔT × trait interaction | ΔT main effect 0.10 ± 0.03 log-odds per SD in Table S8; **all ΔT × trait interactions null** (p 0.12–0.94). Quote: "Climate change affected taxa within a stage, regardless of their traits (table S8)". Random intercepts only; extinction from range-through, with no detection model or validation | Full text and SI tables (Bristol accepted manuscript); Table S8 checked by Claude |
| Smits 2019, bioRxiv preprint, 10.1101/523811 | Endogenous: correlation between cohort intercept (intensity) and range slope | Median r = −0.35, about 90% probability negative; range selectivity strengthens with intensity. 1,130 brachiopod genera, 33 cohorts, Weibull survival | Full text; passage checked by Claude |
| Monarrez, Heim & Payne 2023, RSOS, 10.1098/rsos.230795 | Binary Big Five label × trait, with capture–mark–recapture detection | Range effect reduced in mass extinctions. The authors flag 81 background stages against 5 mass-extinction stages | Full text (scout) |
| Malanoski et al. 2026, Science, 10.1126/science.adv2627 | Binary regime label × coastline geometry | Selectivity *amplified* in mass extinctions | Author manuscript and SI (scout) |
| Payne et al. 2016, Biol Lett, 10.1098/rsbl.2016.0202 | Intensity and selectivity reported side by side | No dose regression | Second-hand summary |
| Payne & Finnegan 2007, PNAS, 10.1073/pnas.0701257104 | Intensity against range odds ratio | Weak inverse, descriptive; confounded with plate sampling | Second-hand summary |
| Bush et al. 2020, Paleobiology, 10.1017/pab.2019.35 (Crossref issue year 2019) | Selectivity index against magnitude | r² ≈ 0.03; the index is mechanically unstable at low magnitude | Full text (scout) |
| Foster et al. 2023, RSOS, 10.1098/rsos.221507, and Reddin et al. 2023 reply, 10.1098/rsos.230400 | Event-wise machine learning; cross-event transfer | Between-event AUC about 0.62, against within-event 0.72–0.80 (as read in the reply) | Full text (scout) |
| Payne et al. 2023, Camb Prisms Extinction, 10.1017/ext.2023.10 | Review | Does not call for continuous dose–selectivity models | Full text (scout) |

## Disposition

1. **The obvious exogenous test exists and is null.** Malanoski et al. 2024 fit
   every ΔT × trait interaction, and none was supported.
2. **What remains open is methodological completeness, not a big question.**
   Nobody has combined stage-varying slopes regressed on an exogenous dose, a
   detection model, propagated dose uncertainty, absolute-scale predictions,
   held-out validation, and a formal comparison of a switch against a smooth
   dose response.
3. **Identification would be weak.**
   - Dose leverage comes from the same 5–17 high-dose stages that define the
     regime labels.
   - Stage-level doses are poorly resolved for most transitions
     ([PhanDA sensitivity](../data/phanda-stage-differences/README.md)).
   - Dose is confounded with sampling intensity and baseline extinction.
   [Inference.]
4. **The interesting content moves to A.** "Does selectivity change with dose?"
   is better tested through a mechanism, as in candidate A: a frozen
   physiological habitat-loss model predicts which taxa and places lose habitat
   as forcing changes, so dose dependence of selectivity becomes a prediction
   rather than a free interaction term.
5. **One residual, low-cost question.** The sign conflict between Smits 2019
   (selectivity strengthens with intensity) and the null or inverse results
   (Payne & Finnegan 2007; Bush et al. 2020; Orzechowski et al. 2015 at summary depth) could be
   addressed by replicating Smits's correlated varying-slope design with a
   detection model and an exogenous dose. That is a methods note, not a
   programme candidate.
