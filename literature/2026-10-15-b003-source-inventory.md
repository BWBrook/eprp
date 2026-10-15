# B-003: published-source and support inventory

Owner: Claude | 15 October 2026 | The next gate of the
[B-003 contract](2026-10-15-b003-escalation-evidence-contract.md). It was
run under the definitions frozen in section 8 (`29367db`).

Status: **inventory complete, and B-003 holds on support.** No new
measurement, fit or author contact.

**How it was compiled:**
- A Sonnet subagent compiled the rows. Claude checked them against the
  frozen schema and the earlier abstract reads.
- All 12 DOIs resolve in Crossref and match.
- Retrieved files are hashed (listed at the end).
- **Access was poor.** Full text was obtained only for Dietl 2003 (as
  publisher HTML, read through a summarising fetch; Tables 1, 9 and 10
  agreed across two passes) and Syverson et al. 2018 (CC BY PDF). The rest
  were read at abstract depth or were inaccessible: Cambridge and Taylor &
  Francis PDFs returned paywall pages, and BioOne, ScienceDirect and the
  Oxford PDF returned 403 or challenges, which were not circumvented.

## Rows

Screen: at least 4 joint horizons, at least 10 specimens per horizon per
side, lineage-level identification, and recoverable data. The screen is for
workflow only.

| Source (access) | Predator side | Prey side | Support | Screen |
| --- | --- | --- | --- | --- |
| Kelley 1989, 10.1080/08912968909386497 (abstract) | None in this paper (drilling mode) | Thickness (in the drilling row); internal volume (not in the row) | Five genera; "both gradual intraspecific and interspecific" change, so species turn over within genera. Horizons, n and variances inaccessible | Fail: cannot be scored |
| Kelley 1992, 10.1017/s0022336000020801 (abstract) | *Euspira heros*, *Neverita duplicata*: globosity, relative aperture, relative thickness, height. **Candidate capability**; no mapping stated in the abstract | Kelley 1989's series | Species-level. Horizons, n, variances and reuse of material inaccessible | Fail: cannot be scored |
| Dietl, Kelley & Handley 2014, 10.1017/s2475262200012156 (NAPC poster abstract, p. 100) | None. Drilling frequency (an outcome) | Thickness | Reanalyses "Kelley's original dataset" with paleoTS: "mixed support for Kelley's original interpretations", "especially for taxa represented by multiple species" | Fail |
| Dietl, Alexander & Bien 2000, Paleobiology 26:215 (abstract) | None. Repair frequency (an outcome) | Thickness, commissural shelf, ornament (in the crushing row) | Two oyster lineages; over 1,600 valves; horizons inaccessible | Fail |
| **Dietl 2003**, 10.1046/j.1095-8312.2003.00255.x (full text, HTML) | *Sinistrofulgur*: **maximum** shell length per horizon (Table 10). Candidate capability. The mapping is qualitative ("probability of successful predation depends on the predator:prey size ratio"), with no function or uncertainty | *Mercenaria* mean valve length (Table 9), in the chipping row | 4 joint horizons (Tamiami, Caloosahatchee, Bermont, Fort Thompson; no numeric ages). See the table below. No SD, SE or specimen values. One locality per horizon (three for the Caloosahatchee). No statement of species continuity. At most 2 lag-one pairs | Partial pass: horizon and sample counts pass; lineage identification is unverified (see below) |
| Kelley, Hansen, Graham & Huntoon 2001, 10.1016/s0031-0182(00)00207-8 (bibliographic only) | "Efficiency" appears in the title only; the measure is unverified | Not stated | Inaccessible | Fail: cannot be scored |
| Kelley & Hansen 2006, 10.1016/j.palaeo.2005.11.012 (abstract) | Drilling frequency and prey effectiveness (outcomes) | Outcomes only | 28 assemblages; reuses "previously derived" patterns | Fail: outcomes on both sides |
| Signor & Brett 1984, 10.1017/s0094837300008174 (abstract) | None. The durophage radiation is narrative | Genus-level frequencies of resistant features (in the crushing row) | Genus composition, not lineages | Fail |
| Syverson et al. 2018, 10.1017/pab.2017.38 (full text) | None measured. Spine regeneration is an outcome | Spinosity by genus over 21 intervals (Table 2); regeneration over 3 cladid horizons | Data on Dryad 10.5061/dryad.s7576 (CC0; not downloaded). No joint horizons | Fail: no predator series |

**Dietl 2003, per horizon:**

| | Tamiami | Caloosahatchee | Bermont | Fort Thompson |
| --- | ---: | ---: | ---: | ---: |
| *Mercenaria*, n | 192 | 151 | 133 | 135 |
| *Mercenaria*, mean length (mm) | 84.9 | 91.3 | 97.7 | 103.1 |
| *Sinistrofulgur*, n | 16 | 19 | 36 | 35 |
| *Sinistrofulgur*, maximum length (mm) | 268 | 278 | 312 | 276 |

## Data for relating local results to global composition (Level B, availability only)

- **Kosnik et al. 2011 supplement** (85 pp):
  - bin definitions;
  - per-bin genus occurrence counts;
  - **one row of static scores per genus**.

  There are no per-bin trait values. This confirms the main text: Level B
  cannot use it for change within genera.
- **Finnegan et al. 2011:** Appendix 1, a 160 KB .xls on Cambridge Core,
  under publisher terms. No repository was found. It was not opened.
- **Heim et al. 2015:** in the Stanford Digital Repository
  (purl.stanford.edu/rf761bx8302), as one file of 17,208 genera.
  - Body volume and length are **static per genus**.
  - Naticids (28 genera), muricids (59), decapods (211) and fishes are
    present; *Sinistrofulgur* and *Busycon* are absent.
  - It cannot supply time-resolved predator size.

## Assessment

**One system passes the horizon and sample-count part of the screen, and it is weak:**
- The predator measure is a **sample maximum** from 16–36 shells per
  horizon. A maximum rises with sample size, and the predator samples
  roughly doubled between the two older horizons and the two younger ones.
  Dietl himself notes the maximum is "potentially affected by sampling
  bias".
- The functional mapping is qualitative, with no uncertainty.
- No variances are given.
- There is one locality per horizon, except the Caloosahatchee, which has three.
- Lineage continuity is not stated, so the lineage-identification part of
  the screen is not established.
- No numeric ages are given.
- There are at most two lag-one pairs.
- It falls short of the contract's candidate-capability requirement, and it
  could not be informative alone.

**The Chesapeake naticid–bivalve pair is the most relevant system, but
cannot be scored.**
- On the abstracts, both series are trait series from one section, in the
  drilling row.
- Horizons, n, variances and tables are behind paywalls not reached here.
- The 2014 reappraisal reports "mixed support" for the original prey
  interpretation.

**Everything else fails:**
- no candidate predator series;
- outcomes only;
- or genus composition rather than lineages.

**Level B stays held:**
- Kosnik's and Heim's data are static per genus.
- Finnegan's is a publisher appendix that was not opened.

## Disposition (the contract's stopping rule, pre-agreed in 76/1668)

**Practical hold on support.**
- The question is kept.
- This is not evidence against escalation. It is a finding about the
  accessible, published evidence for the narrowed target.
- **Reopening terms:**
  - full texts of Kelley 1989 and 1992, through library access, which
    would make the Chesapeake pair scorable;
  - **and** at least one further matched system with a candidate predator
    series, mapped to function with uncertainty, and with recoverable
    variances;
  - **or** time-resolved lineage traits for Level B.
- Then a labelled benchmark on the actual supported design decides.
- **Unfollowed lead, outside the nominated list:** Western Washington
  University's repository has free full texts of Kelley & Hansen 1993, 1995
  and 1996 (Palaios). These may hold the assemblage data behind Kelley &
  Hansen 2006. They are outcome series, so they do not by themselves repair
  the predator side.

## Retrieved files

All are in session scratch and are not committed.

| File | sha256 |
| --- | --- |
| Syverson et al. 2018 PDF | `99b136e64fb4f3d507a147e3321451cc02662c24ecf68307e82d506cd41c3ce0` |
| Kosnik et al. 2011 supplement PDF | `277b9e5a46945f6c78af719130685738305e38e3ade895927038685f841ff2ab` |
| Dietl, Kelley & Handley 2014 first-page image | `8afd3d7437705df6031b3c8ba302ed82eeb231f88120a058041d615a1b83783a` |
| Heim et al. 2015 data file | `5b911416208d2500e63f3f40b81b6f3396127608fe8ac5619522aba3d3ed0f62` |

Dietl 2003 was read as HTML, so it has no file hash.
