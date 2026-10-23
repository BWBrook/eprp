# C3 check: does aggregation flatten a known latitudinal gradient?

Claude, 23 October 2026. The first half of candidate C3's cheapest check
([Alroy provocation note](../../ideas/2026-10-23-alroy-provocation-claude.md)).
It is not a registered question.

**Composite side, done.**
- **Data:** OBIS Bivalvia (AphiaID 105) in a coastal strip along eastern
  Australia, from 0.5° west to 1.5° east of the coastline, at 11–37° S.
  Public OBIS API v3, queried on 23 October 2026, with no account or contact
  parameters. `obis_fetch.py` returned 66,356 records, of which 59,488 are
  at species level. The raw JSON is not committed; rerun the script to get
  it.
- **Method:** Hurlbert-rarefied species richness in 1° bands
  (`obis_gradient.py`); full output in
  [obis_gradient_output.txt](obis_gradient_output.txt).

**Result:** the slope of log rarefied richness per degree southward.

| Records | Rarefied to n = 100 | Rarefied to n = 300 |
| --- | --- | --- |
| All (59,488) | −0.003 | −0.011 (−10% over 10°) |
| Specimen-based (35,489) | −0.003 | −0.007 (−7% over 10°) |
| Observation-based (17,186) | **+0.012** | **+0.006** (reversed) |

- **The composite gradient is almost flat,** and observation records
  reverse it. This is the same direction as Kerr, Currie, Kosnik & Alroy
  (2025), whose OBIS composite had 36,226 specimens, matching our 35,489
  specimen-based records.

**Field side, pending.**
- The standardised field collection (5,552 individuals) is on Dryad
  (CC0, doi:10.5061/dryad.p5hqbzm03).
- Automated download is refused (the API requires a token; the web route
  returns 403). It needs a browser download with Barry's approval.
- The attenuation factor is the composite slope divided by the field slope
  on the same bands and the same standardisation. It can be computed once
  the file is here.

## Field half and the attenuation factor (23 October, after Barry set up the Dryad API account)

**Data.**
- The Kerr et al. deposit (CC0) was mirrored on deep-server with the side
  session's `data_mirror.py`, copied read-only from its branch, using
  Barry's Dryad API account. Checksums were verified.
- **Field data:** 15 beaches between 16.7° S and 37.2° S, with species valve
  counts per quadrat.
- **Matching OBIS data:** a window of ±1° around each beach.
- Script: [attenuation.py](attenuation.py); output in
  [attenuation.json](attenuation.json).

**Change in rarefied richness per 10° southward.**

| Data | Change per 10° | r |
| --- | --- | --- |
| Field, rarefied to 26 valves (all 15 sites; Shelly Central has only 26 valves) | ×0.82 | −0.52 |
| **Field, rarefied to 200 valves (14 sites, Shelly Central excluded)** | **×0.71** | −0.69 |
| Field, rarefied to 100 valves (14 sites) | ×0.76 | −0.61 |
| Field, raw species counts | ×0.66 | — |
| OBIS, all records (rarefied to 150) | ×0.88 | −0.64 |
| OBIS, specimen records | ×0.86 | −0.89 |
| OBIS, observation records | ×1.16 (reversed) | +0.66 |

**Reading.**
- **The composite keeps about 40–45% of the field gradient's slope** when
  the field side is rarefied to a fair depth of 200 valves. It keeps 66–76%
  at the 26-valve depth that the smallest site forces, because rarefying
  that shallowly compresses the field slope itself.
- **Observation-based records reverse the gradient.**
- So aggregation attenuates this gradient by roughly 1.5–2.5×. That is
  material. It is a partial flattening, not an erasure: the specimen
  composite still correlates strongly with latitude (r = −0.89).
- **For deep time:** PBDB-type data are specimen- and literature-based,
  closer to the specimen composite than to observation records. An
  attenuation of about 0.4–0.75 could weaken an apparent deep-time
  gradient. It cannot by itself turn a strong gradient into none.
- **Limits:** one system and one clade. The two sides count different
  units (valves against records) and are standardised at different
  depths. The windows are ±1°. A deep-time transfer would need several
  modern calibrations, and a simulation of the PBDB filter.

## Correction (Codex 76/2250; [review](../../ideas/2026-10-23-alroy-review-codex.md))

- **The slope ratio is not a portable correction.** Field valves and OBIS
  records are different sampling units; equal rarefaction depth does not
  align them, their habitats or their latitudinal support.
- **The "specimen" category above includes generic `Occurrence` and
  `MaterialCitation` records.**
- **Death assemblages are a filtered comparator, not field truth.**
- Read the table as descriptive only. The next step is a paired
  observation-operator test on the same eligible units. C3 holds as support
  for Q-027.
