---
id: austarch
name: AustArch, radiocarbon and other ages from Australian archaeological sites
kind: compilation
status: "frozen (merged file of 28 November 2013; superseded by SahulArch)"
last_update: 2013-11-28
scope:
  taxa: [not taxonomic; archaeological age determinations]
  time: "radiocarbon to about 55 ka; luminescence and other methods older"
  space: "mainland Australia and Tasmania; 75 of 89 IBRA bioregions"
  record_unit: "one age determination"
size:
  as_of: "ADS deposit, file Austarch_1-3_and_IDASQ_28Nov13-1.csv"
  ages: 5522
  radiocarbon: 5044
  other_methods: 478
  sites: 1784
access:
  tier: registered
  licence: "ADS Terms of Use and Access (custom): non-commercial research and teaching, acknowledge depositors and ADS; sharing of data or derivatives limited"
  routes:
    - {type: ads, url: "https://doi.org/10.5284/1027216 (ADS collection 1661)", state: "CSV download without login; use implies acceptance of ADS terms; landing page blocked to scripts", checked: 2026-10-22}
    - {type: p3k14c, url: "doi:10.5281/zenodo.16394072", state: "Holocene subset only (3,624 dates in release 2025.07, to 10,000 BP)", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "single frozen file; older regional files (AustArch 1-3) no longer online"
mirror:
  path: deep-server:/data/paleodata/austarch/ads
  policy: "private local copy for EPRP research, authorised by Barry W. Brook on 2026-10-22; not for redistribution"
  state: "snapshot 2026-10-22T0422Z_url (data and citation CSVs)"
lineage:
  upstream:
    - "IDASQ (Queensland, Ulm and Reid 2000)"
    - "AustArch 1 (arid zone, 2008), 2 (Top End, 2012), 3 (south and Tasmania, 2013)"
  downstream:
    - "SahulArch (search guide; ages re-extracted)"
    - "p3k14c (Holocene subset)"
    - "rc-dates project (an author-supplied copy that differs from the ADS file)"
eprp_questions: []
citation:
  - "Williams, A. N., Ulm, S., Smith, M. & Reid, J. (2014). AustArch: a database of 14C and non-14C ages from archaeological sites in Australia. Internet Archaeology 36. doi:10.11141/ia.36.6"
  - "Williams, A. N. & Ulm, S. (2014). AustArch [dataset]. Archaeology Data Service. doi:10.5284/1027216"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); documentation read by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# AustArch

## Summary

AustArch merged the regional compilations of archaeological ages for Australia
into one table of 5,522 determinations (5,044 radiocarbon, 478 by other
methods) from 1,784 sites, frozen on 28 November 2013 and deposited with the
Archaeology Data Service in 2014. It underpinned a decade of continental
"dates as data" work, including population curves (Williams 2013) and Last
Glacial Maximum refugia. [SahulArch](../sahularch/README.md) supersedes it,
having re-extracted ages from the original sources over a wider area. Keep
AustArch for reproducing earlier analyses, not for new ones.

## Contents

Counts are our own ([profile](profile/austarch_profile.tsv)).

- **Methods.** Radiocarbon 5,044; OSL 220 (44 single-aliquot regenerative);
  TL 161; oxidisable carbon ratio (OCR) 35; U-series 28; ESR 26;
  cation-ratio 7; amino-acid racemisation 1.
- **Compilers' classification** for time series and calibration: terrestrial
  3,472, marine 1,110, unusable 462 (spelled "Unusuable"), blank for the 478
  non-radiocarbon ages.
- **Sites.** Open 3,107 and closed 2,382 ages. Direct association with
  occupation: yes 2,395, unknown 2,703, no 310.
- **Date issues.** 190 ages flagged erroneous and 185 not associated with
  human activity.
- **Ages.** Radiocarbon ages are uncalibrated BP. 45 values carry an
  inequality or qualifier (e.g. ">55000", "<1000", "c. 450"), and 76 begin
  with "Modern".
- **Against the data paper.** The file's 5,044 radiocarbon and 478 other ages
  match the paper. The paper's 1,748 radiocarbon sites compare with 1,743 in
  the file. Its "853 ages at 50–10 ka" compares with 929 radiocarbon ages of
  10,000–50,000 BP in the file (1,143 across methods). Its "52 of 89
  bioregions with fewer than 50 ages" compares with 45 of the 75 bioregions
  present (independent review).

## Provenance and lineage

Compiled from IDASQ (Queensland, 2000) and AustArch 1–3 (arid zone 2008, Top
End 2012, south and Tasmania 2013) by Alan N. Williams and Sean Ulm, with Mike
Smith and Jill Reid on the data paper (Williams et al. 2014). The three
compilers' interpretive fields (calibration class, open or closed, occupation)
are "our interpretations ... not necessarily those of the original
researchers" (data paper). Barry W. Brook is not an author. He used AustArch's
regional precursors in Johnson & Brook (2011).

## Structure

One CSV of 27 columns (the last header is blank): `ADSID`, IBRA region,
longitude and latitude (unblurred, precision varies), site, site type,
laboratory code, age, error, δ13C and error, material (two levels), context,
depth, method, technique, the three interpretive fields, source, notes,
record source (c14 or nonc14), date issues, normalised age, additional
issues. A second CSV lists citations.

## Access

**Mirror.** `deep-server:/data/paleodata/austarch/ads/raw/2026-10-22T0422Z_url/`
holds both CSVs with a manifest. Barry authorised this private copy on 22
October 2026 ("I say yes for local mirror ... AustArch"), noting he had already
used a copy supplied by two of the data paper's authors for the rc-dates work.

**From ADS.** The files download without login from
`archaeologydataservice.ac.uk/catalogue/adsdata/arch-1661-1/dissemination/csv/`,
but the ADS terms apply to anyone who uses them. The landing page blocks
scripted access.

## Strengths

- **The reference compilation for 2014–2022 work.** Many published analyses
  rest on it, so it is needed to reproduce them.
- **Exact coordinates.** Unlike SahulArch, locations are not blurred, so
  site-scale questions are possible (with care for cultural sensitivity).
- **Explicit usability classes.** Marine, terrestrial and unusable flags, and
  date-issue notes, encode the compilers' screening.

## Weaknesses and pitfalls

1. **Copies in circulation differ.** The copy used in the rc-dates project
   (an author-supplied file of the same name) differs from the ADS deposit
   ([comparison](profile/compare_ads_vs_rcdates_copy.txt), checked; finer
   breakdown by the independent review):
   - *Rows.* It has 5,288 rows, 17 of them empty, so 5,271 ages; 251 ADS ages
     are absent (216 radiocarbon, 35 other).
   - *What is missing.* The copy is almost exactly the ADS rows with a
     numeric age and a numeric error: of the 251 absent ages, 149 have a
     non-numeric age (Modern 76, inequality 33, blank 9, `na` 6, "c." 5,
     infinite 2, others) and 75 a non-numeric error such as "+900/-800".
     The copy therefore lacks all "Modern" ages, 33 of 39 limiting ages and
     the asymmetric-error ages.
   - *What changed.* Of 5,271 shared ages, 239 differ: 104 only in number
     formatting, and 135 in substance. 104 depth ranges and one context value
     were turned into dates ("11-17" became "Nov-17"); six limiting ages and
     one approximate age lost their qualifier (">13930" became "13930"); and
     missing coordinates changed from "Not given" to "NA".
   - *Format.* LF line endings where ADS uses CRLF.

   Analyses built on that copy should be checked against the ADS file: the
   missing Modern, limiting and asymmetric-error ages, and the seven ages
   kept with their qualifier stripped.
2. **Superseded.** Frozen at November 2013; SahulArch adds a decade of ages
   and re-extracts the old ones.
3. **Thin Pleistocene coverage.** 929 radiocarbon ages fall in 10,000–50,000
   BP; more than half of sites have a single age (data paper), and 45 of the
   75 bioregions present have fewer than 50 ages.
4. **Restrictive terms.** The ADS agreement limits use to non-commercial
   research and teaching and restricts passing on data or derivatives. The
   catalogue classes it `registered`: no account, but downloading accepts
   the terms.

## Overlap with other sources

- **SahulArch** re-extracted AustArch's ages without an ID crosswalk, but 98%
  of AustArch radiocarbon ages with a usable laboratory code (4,846 of 4,944)
  appear in SahulArch by code (independent review). Do not pool them.
- **p3k14c** carries 3,624 AustArch dates in release 2025.07 (Holocene only),
  with AustArch's exact locations.

## EPRP relevance

None directly. Needed to reproduce earlier Australian dates-as-data studies,
and as the baseline for checking how SahulArch changed the record.

## Citation and terms

Cite Williams et al. (2014) and the ADS dataset DOI, and acknowledge ADS.
ADS terms: research, learning and teaching use; acknowledge depositors and
ADS; no sale; derivatives' redistribution restricted (Common Access
Agreement). Our copy is private to EPRP work.

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | ADS CSVs downloaded (sha256 in manifest); 5,522 rows = paper's 5,044 + 478 | checked |
| 2026-10-22 | Profile of methods, classes, issues, qualifiers | checked |
| 2026-10-22 | ADS file against the rc-dates copy | checked (breakdown by the independent review) |
| 2026-10-22 | Paper counts reconciled with the file; SahulArch lab-code link; p3k14c release count | checked (independent review) |
| 2026-10-22 | ADS terms, authorship, lineage, p3k14c subset | source claim (Wayback copies of ADS pages; data paper; documentation scan) |
| 2026-10-22 | Barry's authorisation of a private copy | checked (side-session chat, 22 Oct 2026) |
