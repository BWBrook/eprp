# Capitanian to end-Permian: support inventory for the hidden-state test

Claude, 24 October 2026. This is the bounded inventory agreed in 76/2364, on
Codex's amended terms: descriptive, built from metadata and published tables,
with no fitting. It asks whether this event pair could support the narrowed
hidden-state test set out in the
[contract](../../ideas/2026-10-24-hidden-state-contract-and-contrary-worlds-claude.md),
as repaired in the
[repair note](../../ideas/2026-10-24-collapse-conditions-and-contract-repair-claude.md).

**How it was done:**
- A Sonnet scout searched read-only.
- I re-ran the decisive table tallies myself (`dr1_tally.py`, with its output
  in `dr1_tally.txt`).
- No PBDB API call was made, consistent with the 23 October data hold.
- Downloads stay in session scratch. The DR1 PDF is CC BY-NC and is not
  committed; it is recorded by DOI and md5.

## Answer

**This pair can supply a global genus-level cohort with fate variation and
linked Capitanian presence. It cannot supply exposure to a regional footprint,
a classification of immigrants, or comparable forcing from any deposited
table.**

**The first practical limitation is exposure.**
- **The Capitanian footprint is contested.** It is severe or an artefact of
  truncation depending on region and latitude.
- **No marine Changhsingian exists in West Texas.**
- **The Wuchiapingian separates the two events,** so onset state for the
  second shock comes from a different stage than the history.

## What exists

| Source | What it gives | What it lacks |
| --- | --- | --- |
| **Clapham & Payne 2011, Table DR1** ([Figshare 10.1130/2011310](https://doi.org/10.1130/2011310); md5 `357d6a3b…`) | Genus × stage, Kungurian to Changhsingian: 4,508 rows, 1,874 genera, with abundance, a range-bin count, species richness, four physiological traits and an extinction flag. No PBDB identifiers. | No regions or localities. Fate is coded range-through (last record anywhere, with Triassic records defining survival), and genera alive but unsampled at onset are absent. |
| **Clapham, Shen & Bottjer 2009**, online data 10.1666/08033.s1 | 53,731 occurrences from 9,790 collections, in 30°×30° palaeo-bins | The supplement was not accessible (bot wall, not circumvented), so its contents are unknown |
| **GBDB snapshot** (Zenodo 4245604, CC BY 4.0) | Occurrence-level data with section coordinates. 387 genus names in the Capitanian window and 933 in the Changhsingian, 171 in both; 5 sections hold both. | Almost all of it is from China (plus 221 Iranian Capitanian rows). Names are not standardised and ages are stage-level. |
| **Fan et al. 2020** (Zenodo 4977790, CC0) | Species ranges per section, with high-resolution composite time | China only, no coordinates, genus names truncated, and no stage labels |
| **Clapham 2015** census (Dryad and GitHub, CC0) | Brachiopod occurrence frequencies for Tethys, Iran, South China and Pakistan | Adjacent stages only. It carries PBDB *collection* numbers, unchecked against the snapshot. |
| **Monarrez et al. 2023 ESM** | Genus × stage, per-stage range, five benthic classes | **The `ch` capture-history column in the xlsx is stored as numbers.** An 86-digit history cannot survive that (row 1 reads "1.11E+47"), so the intact histories exist only in the Dryad `.Rdata`. Q-038 is unaffected: it read only the cleaned CSV for deposit constants, and fitted simulated data. [Detail withheld pending disclosure to the data custodian.] |
| **Al Aswad et al. 2025; Kocsis 2018; others** | PBDB extracts with palaeocoordinates | Al Aswad has no Capitanian. [Detail withheld pending disclosure to the data custodian.] |
| **PBDB public snapshot** (catalogue, 2026-10-23) | Occurrence-level data with collection palaeocoordinates; Permian is 146k of 1.78M | Not queried. This is the route by which exposure and immigrants could be built, under the hold's public-record rule. |

## Fate variation, read from Table DR1 (counts, re-tallied)

- **The Changhsingian cohort:** 657 genera, 548 flagged extinct and 109 not.
  The abstract says 701 genera were sampled in the bin; the gap of 44 is
  unexplained.
- **The Capitanian cohort:** 725 genera, 315 flagged extinct and 410 not.
- **Genera with rows in both stages:** 310, of which 243 died in the
  Changhsingian and 67 survived. 250 also have a Wuchiapingian row.

A descriptive cross-tab, with no inference drawn from it:

| Changhsingian cohort | n | Extinct (%) |
| --- | ---: | ---: |
| Has a Capitanian row | 310 | 78.4 |
| No Capitanian row | 347 | 87.9 |
| … with a Wuchiapingian row | 146 | 84.9 |
| … no Capitanian or Wuchiapingian row | 201 | 90.0 |
| Capitanian and Changhsingian rows, none in the Wuchiapingian | 60 | 88.3 |

**This table is not a test.** A ten-point gap of this kind is what the
following would produce, *with no history effect at all*:
- **Fate coding:** range-through fates favour well-sampled genera, which are
  more likely both to appear in more stages and to be recorded in the
  Triassic;
- **Genus age;**
- **Range size.**

The contract's Price identity adds selection on stable susceptibility,
predicting the same sign wherever the two shocks select on the same axes.
Clapham & Payne find poorly buffered physiology selected against in both.

**Corrected (Codex, 76/2375):** the gap does *not* measure the size of the
confounds. It is a difference those candidates could produce, and their
contributions are unestimated. It is uninterpretable without a
detection-aware design. The 60 genera seen in the Capitanian and
Changhsingian but not the Wuchiapingian have survival like the newcomers'.
That is consistent with sampling driving the pattern, but it is a small
group.

## Exposure, immigrants and forcing

**Exposure.**
- Clapham et al. 2009 find Capitanian extinctions clustered in western
  Laurentia, and call that "more likely an artifact" of the loss of the
  record.
- Shen et al. 2020 call the North American event "possibly an artefact of a
  stratigraphic truncation effect". They describe South China as mainly
  species turnover at a lowstand, and allow that the event "may have been
  profound" at high latitude.
- Bond et al. 2015 report an 87% loss of brachiopod species in Spitsbergen,
  with disputed age control.

Any footprint therefore has to be built from regional occurrence data, and
would itself be contested. **A footprint defined by observed taxonomic losses
is a biological *response*, not exposure.** Exposure needs an independent
environmental measure (Codex, 76/2375).

**Immigrants against new origins.** No deposit supports this distinction. It
needs:
- global occurrence-level data with palaeocoordinates for all three stages;
- consistent taxonomy;
- a detection model;
- a rule for Lazarus genera (60 of the linked genera skip the Wuchiapingian).

**Comparable forcing.** No source has proxies for both events in the same
sections. Conodont δ18O exists for the Guadalupian of South China and West
Texas (Shen 2020). Bond 2015 gives redox proxies for the Capitanian of
Spitsbergen only.

**What could carry a legacy across about 8 Myr.**
- **Composition continuity.** In South China, mixed Guadalupian–Lopingian
  faunas point to it (Shen 2020).
- **Brachiopod rank correlations across the boundary** are weak or negative
  (Clapham 2015). Clapham's own Mantel tests show they are confounded with
  sampling geography.
- **Stable susceptibility** is suggested by physiological selectivity
  recurring across the pair (Clapham & Payne 2011). This is the contract's
  first rival.

## Assessment against the repaired contract

| Contract element | Support from this pair |
| --- | --- |
| Cohort and unit | Genus, global. Available in DR1, but fates are range-through and unsampled genera are missing. |
| Fate variation | Ample: 548 extinct and 109 surviving in the Changhsingian. |
| Linking history to fate | By genus name in DR1 (310 genera). No taxon identifiers, and synonymy is untested. |
| Exposure to the shock-1 footprint | **Not available from deposits.** Buildable only from regional occurrence data, and the footprint is contested. |
| Classifying cohorts (place × cohort) | Not available from deposits. Needs the occurrence-level route. |
| Comparable forcing | Weakest: no sections with proxies for both events. |
| Observation model | Required before any comparison. The cross-tab above is uninterpretable without one; candidate confounds are not yet estimated. |

**Implication.** Building the test on this pair would mean assembling it from
the public PBDB snapshot under the hold, with a detection model and a
defended footprint. That is feasibility work beyond this inventory. Whether
hidden state has earned it is a question for the interest discussion.

## Flags for other sessions

- **For the Databases side session.** `resources/sources/pbdb/README.md` says
  Clapham "alone entered 11,484 (25%)". The scout reports that this figure
  refers to the Australian-region extract, not global PBDB. Not edited here.
- **For the Databases side session.** The Monarrez et al. 2023 ESM xlsx
  `ch` column is corrupted, as described above.
- **Outreach candidate for Barry's queued tranche.** Clapham's own Permian
  database, or the 2009 supplement, which a bot wall blocks.
- **Personal data in downloaded files** (enterer names, an author email) stays
  in session scratch and is not reproduced here.

## Sources

| Source | Access |
| --- | --- |
| Clapham & Payne 2011, Geology 39:1059, [10.1130/G32230.1](https://doi.org/10.1130/G32230.1), and DR 2011310 | Paper full text (author copy); DR table fully parsed and re-tallied |
| Clapham, Shen & Bottjer 2009, Paleobiology 35:32, [10.1666/08033.1](https://doi.org/10.1666/08033.1) | Full text (author copy); supplement inaccessible |
| Clapham 2015, Paleobiology 41:266, [10.1017/pab.2014.15](https://doi.org/10.1017/pab.2014.15) | Full text; census table header and counts |
| Shen et al. 2020, Earth-Science Reviews 211:103412, [10.1016/j.earscirev.2020.103412](https://doi.org/10.1016/j.earscirev.2020.103412) | Full text (Subcommission on Permian Stratigraphy copy) |
| Bond et al. 2015, GSA Bulletin (Capitanian of the Boreal Realm) | Read by the scout; locator in its report |
| Fan et al. 2020, Science, deposit Zenodo 4977790 | Deposit structure only; paper closed |
| Xu et al. 2020, ESSD, [10.5194/essd-12-3443-2020](https://doi.org/10.5194/essd-12-3443-2020), and GBDB Zenodo 4245604 | Paper full; workbook structure and counts |
| Monarrez et al. 2023 ESM (Zenodo 8341743) | Header and structure |
| Catalogue entries `register-deposits`, `pbdb`, `classic-compendia` | Repository profiles read |
