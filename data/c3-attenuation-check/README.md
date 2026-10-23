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
