# External review (GPT-6 Pro): Claude's response

Owner: Claude | Date: 11 October 2026 | Review of snapshot `bbe5ce7`.

**Provenance.**
- The bundle is filed verbatim in [docs/review/2026-10-11-gpt6pro-review/](../docs/review/2026-10-11-gpt6pro-review/README.md);
  start with [review.md](../docs/review/2026-10-11-gpt6pro-review/review.md).
- Barry delivered it as `EPRP_external_review_bbe5ce7.zip` (sha256
  `4ae979fc12fefca75027390929f2f3032d32c09c614c5d177b61707f8aa613a9`).
- Its `MANIFEST.sha256` verifies.
- The bundle's `checks.py` and `probe.py` were **not executed** here: they are
  external code, kept as a record.
- I checked by hand the two calculations I rely on:
  - the Q-042 range: 62/500 = 12.4% and 1 − 38/500 = 92.4%;
  - the Q-021 error: Φ(−2/0.354) ≈ 7.7×10⁻⁹.
- The reviewer's new sources were checked against metadata: Donovan et al.
  2020 and 2023, Stadler et al. 2018, and the abstract of Dieselhorst &
  Stadler 2026 (arXiv).

**Overall.** The review is favourable but sharp where it matters. Its five
findings change designs and decision rules, not the remit. It examined eight
entries in depth, reproduced the Q-026 probe exactly, and found no gap large
enough to justify a 51st question. Four findings concern Claude's entries;
F-04 concerns Claude's Q-021 proposal in an entry Codex owns.

## Dispositions

| Finding | Entry and owner | Disposition | What changed |
| --- | --- | --- | --- |
| F-01: the 56–79% genus-loss inputs are different targets, not one interval; the bound needs retention of *baseline-cohort* species | Q-042, Claude | **Accept** | Design step 3 now starts with a cohort and window crosswalk. Inputs are carried as labelled scenarios. No regional calibration is intersected with a global bound without an argument for transport. The bound now states baseline-cohort retention, and the reviewer's 12.4–92.4% fixture is added |
| F-02: Beaulieu & O'Meara concern rate heterogeneity, not fossils in general; the parking rule could end two residuals on finding one; "methodological" is not an importance category | Q-006, Claude | **Accept**; tier 3 → 2 (provisional) | Summary corrected. The residual is reframed as an information table (observations × sampling model × rate class × target). The decision rule closes only a matched residual, and "the added information would not change an inference" counts as an answer. Stadler et al. 2018 and the Dieselhorst & Stadler preprint are added |
| F-03: stopping rules required the hoped-for effect | Q-035, Q-047, Q-049, Claude | **Accept** | All three now have outcome-neutral rules: an informative positive, an informative negative or equivalence, and inadequate discrimination, against a consequential effect size fixed in advance. Feasibility screens are kept as screens |
| F-04: "each model already outputs the fluxes a Li box model needs" overstates; "overlap at the prior's width" is not a valid discrimination test | Q-021, Codex (Claude's proposal) | **Accept in full** | Silicate-weathering and silica fluxes are not Li fluxes. Conversion needs composition, uptake, fractionation, and an archive model for shale or chert. Overlap of marginal bands is the wrong criterion: the joint predictive separation, with nuisance parameters free, is the test. Fixing a conversion can also *manufacture* separation. The reviewer's units-and-observation contract supersedes my reply-3 gate. The entry is Codex's to revise |
| F-05: the interaction endpoint needs its own trigger for reopening; the *Agathis* host-continuity work occupies part of that route | Q-032, Claude | **Accept**; stays parked | A third reopening trigger is added (host-resolved event/control contrast, no abundance calibration needed), together with the Donovan et al. 2020 and 2023 priors |

I do not dispute any finding. One note on F-02: the tier change is my
judgment, not deference. The scope mismatch is verified; the importance
argument (an information-design result could change many sampling and
inference decisions) is persuasive but untested. Codex may challenge it.

## Leads in the reviewer's first view, not raised as findings

The reviewer's [register-first notes](../docs/review/2026-10-11-gpt6pro-review/initial_view_before_phase2.md)
contain leads worth recording without treating them as verified:
- **Q-017 (Claude).** Detection theory may be undervalued for the same reason
  as Q-006. I will check this when Q-017's equivalence note is done.
- **Q-049 (Claude).** R is unstable where the isotherm displacement is near
  zero, and a ratio does not remove dependence on scale. Add this to Q-049's
  design when it is next worked on.
- **Q-030 (Claude).** Temperature is a mediator of carbon input, not an
  interchangeable measure of forcing.
- **Q-046 (Codex).** Lacking an absolute density need not rule out partial
  identification.

## Process recommendations

| Recommendation | Claude's view |
| --- | --- |
| 1. Outcome-neutral gates | **Adopted** for Claude's active entries (above). Codex should check its own |
| 2. A nearest-prior matrix by target and assumption, for promising questions | **Agree.** Do it for the three development candidates before any further broad scan |
| 3. One current scientific contract per active question | **Agree; the most useful process change.** The reviewer is right that the main cost of reuse is reconstructing which claim is current. Proposal for Codex: each active entry starts with a short "Current contract" block (target, unit, comparison, permitted interpretation, open assumptions, next decision), with dated debate linked as history. Pilot it on Q-042, Q-006 and Q-021 |
| 4. Small hash-pinned fixtures and a record of shared dependencies | **Agree.** Q-026 is the model; reused data and chronology should be recorded so they are not counted as replication |
| 5. Retire "3 is modest or methodological" | **Agree.** The tier definition is shared text in the register header, so I propose rather than edit. Suggested wording: "3 is narrower in consequence, or currently a supporting or diagnostic question". Importance stays separate from tractability and cost |

## Development candidates

The reviewer names Q-021, Q-042 and a reframed Q-006, none ready for
handoff. Its cheapest decisive tests:
- **Q-042:** a cohort and window crosswalk for the end-Permian, then
  conditional sharp bounds;
- **Q-006:** an information table, with one target functional and one
  observation setting;
- **Q-021:** the units-and-observation contract for one record and one pair
  of rival flux histories.

All three are small and need no raw-data cache. I propose that Claude takes
Q-042, as owner, as the next bounded task; that Codex takes Q-021's contract;
and that Q-006 follows. Barry's direction on what is next takes precedence.
