---
id: ga-biozonation
name: Geoscience Australia Basin Biozonation and Stratigraphy charts, and palynology zonations
kind: deposit
status: frozen
last_update: "2017"
scope:
  taxa: ["biozone schemes: dinocysts, spore-pollen, foraminifera, nannofossils, conodonts and others"]
  time: "Proterozoic to Neogene"
  space: "Australian sedimentary basins and margins (34 numbered charts)"
  record_unit: "one chart: a basin's biozonation, lithostratigraphy and sequences against a time scale"
size:
  as_of: "url snapshot 2026-10-22T0856Z"
  files: 39
  bytes: 120369345
  chart_pdfs: 36
access:
  tier: open
  licence: "Conflict across layers: eCat metadata says CC BY 4.0 for every record (source claim); the PDFs print CC BY 4.0 on 4 charts, CC BY 3.0 Australia on 1, an all-rights-reserved notice on chart 9 and on Record 2006/23 with its 4 charts, and only a Commonwealth copyright line or no statement on the rest. Mirrored on the metadata licence; no redistribution right beyond what each file prints (CONTACTS.md)."
  routes:
    - {type: catalogue, url: "https://pid.geoscience.gov.au/dataset/ga/76687", state: "eCat 76687, the chart series: 24 PDFs (13 printed 1997-99, 11 printed 2013-17)", checked: 2026-10-22}
    - {type: catalogue, url: "https://pid.geoscience.gov.au/dataset/ga/23332", state: "eCat's '1994 charts', 12 PDFs printed 1996-2001: eCat 23332, 23334, 23346, 23350, 23352, 23354, 23356, 24220, 24222, 24225, 31035", checked: 2026-10-22}
    - {type: catalogue, url: "https://pid.geoscience.gov.au/dataset/ga/64962", state: "eCat 64962, Record 2006/23 and Data.zip; eCat 61127 (NWS dinocyst zonation, 2004) is a separate record", checked: 2026-10-22}
    - {type: file, url: "https://d28rz98at9flks.cloudfront.net/76687/Chart_03_Arafura_Money_Shoal_Basins.pdf", state: "PDFs sit at d28rz98at9flks.cloudfront.net/<eCat>/<file>; all 39 files fetched 2026-10-22", checked: 2026-10-22}
    - {type: catalogue, url: "https://pid.geoscience.gov.au/dataset/ga/68802", state: "eCat 68802, TimeScale Creator 7.0 with the GA datapack; not mirrored, the bundled software is all rights reserved", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "superseded chart versions remain as separate eCat records (2008 versions, annual compilations) and series record 76687 was revised in 2018 (both source claims); the series record holds charts printed 1997-99 beside their 2013-17 revisions"
mirror:
  path: deep-server:/data/paleodata/ga-biozonation
  policy: "every PDF in the chart series (eCat 76687) and in the eCat records labelled 1994, because the older charts are the only versions for some basins (Bowen, 28a/b) and no chart names the one it replaces; plus the NWS dinocyst zonation (61127) and Record 2006/23 with Data.zip. Not mirrored: TimeScale Creator (68802), 2008 versions and annual compilations."
  state: "2026-10-22T0856Z_url (39 files)"
lineage:
  upstream:
    - "AGSO and GA biostratigraphers' zone schemes for each basin"
    - "STRATDAT, the AGSO and GA well-pick database that 24 of the charts printed 1996-2001 say their zonations come from (see ../stratdat/README.md)"
    - "Geologic Time Scale tables and Australian zone schemes compiled in the TimeScale Creator software (2013-17 charts, as they state)"
    - "Partridge's recalibration of the zones to GTS2004 (Record 2006/23)"
  downstream:
    - "basin studies and petroleum exploration"
    - "the TimeScale Creator Australian datapack"
eprp_questions: []
citation:
  - "Geoscience Australia (AGSO for charts printed before 2005), Basin Biozonation and Stratigraphy charts, with the chart number, the printed year and the eCat record; check each PDF's printed terms first"
  - "Monteil, E. (coordinator) (2006). Australian Mesozoic and Cenozoic Palynology Zonations, updated to the 2004 Geologic Time Scale. Geoscience Australia Record 2006/23 (eCat 64962)"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent; review fixes by Claude Sonnet 5.5 (subagent)
  reviewed: "2026-10-22, independent review by a Claude Sonnet 5.5 subagent; its findings G1-G3 applied the same day, not yet re-reviewed"
---

# Geoscience Australia biozonation charts and palynology zonations

## Summary

Geoscience Australia's Basin Biozonation and Stratigraphy charts set out, for
each Australian sedimentary basin, the biozones (dinocyst, spore-pollen,
foraminiferal, nannofossil and others), lithostratigraphic units and
sequences against a time scale. The mirror holds 36 chart PDFs in two
generations: 25 printed 1996-2001 by the Australian Geological Survey
Organisation (AGSO), 24 of which say their zonations come from
[STRATDAT](../stratdat/README.md), and 11 printed 2013-17 by Geoscience
Australia on GTS2012 or GTS2016, ten of which say they revise earlier charts. It also holds a 2004
dinocyst zonation and the 2006 palynology Record. The charts are large PDFs,
not data. The time scale depends on the chart's date, and 11 charts name none.
Terms differ file by file: see Weaknesses before copying anything. Reach for
the charts to read a basin's zone scheme and correlations; tabular zone ages
are in STRATDAT (ages per pick) and in the TimeScale Creator datapack, which
is not mirrored and whose redistribution status is unclear.

## Contents

Every count, year and statement below comes from
[ga_charts_profile.py](ga_charts_profile.py), run on deep-server against the
mirror; outputs are [profile/ga_charts_profile.tsv](profile/ga_charts_profile.tsv)
(one row per file, and per PDF inside `Data.zip`) and
[profile/ga_charts_summary.tsv](profile/ga_charts_summary.tsv). "Printed" means in
the PDF's text layer.

| Set | eCat | PDFs | Printed years | Time scale named on the chart | Terms printed |
| --- | --- | --- | --- | --- | --- |
| Series record, older charts | 76687 | 13: charts 3, 4, 5, 8A, 8B, 14, 16, 17, 19, 20, 21, 22, 26 | 1997 (2), 1998 (8), 1999 (3) | "AGSO timescale" on 3, 4, 5, 8A, 8B, 14, 16; Gradstein et al. 1995 on 20, 21; none on 17, 19, 22, 26 | Commonwealth copyright line only on 11; none on 5, 21 |
| Series record, newer charts | 76687 | 11: charts 6, 31-36, 38-41 | 2013 (4), 2014 (2), 2015 (3), 2017 (2) | GTS2012 on 31, 33, 35, 36, 41; GTS2012 and the Concise Geologic Timescale (Ogg et al. 2008) on 34, 38, 39, 40; GTS2016 on 6, 32 | CC BY 4.0 on 34, 39, 40, 41; CC BY 3.0 Australia on 38; copyright line only on 6, 31, 32, 33, 35, 36 |
| Charts eCat labels "1994" | 23332, 23334, 23346, 23350, 23352, 23354, 23356, 24220, 24222, 24225, 31035 | 12: charts 1, 2, 7, 9-13, 15, 18, 28a, 28b | 1996 (1), 1997 (1), 1998 (9), 2001 (1) | "AGSO timescale" on 1, 2, 7, 10, 12; none on 9, 11, 13, 15, 18, 28a, 28b | all rights reserved on 9; copyright line only on 10 charts; none on chart 10 (Bowen) |
| NWS dinocyst zonation | 61127 | 1 (2 pages) | 2004 | first column "Australian Timescale, Young & Laurie 1996" | copyright line only |
| Palynology zonations | 64962 | Record 2006/23 (8 pages); Data.zip holds four charts (PDF, EPS, JPEG each), preface, title page, splash screen | 2006 | GTS2004 (Gradstein et al. 2004) | all rights reserved on the Record, the four charts and the title page |

The "1994" is eCat's label (it is in the file names): the PDFs print 1996-2001.
The mirrored set is 39 files, 120,369,345 bytes, all matching the manifest's
sizes and sha256; the largest is the 2014 Bonaparte Basin chart (44 MB). 34
distinct chart numbers are present (8A/B and 28a/b count once); numbers 23-25,
27, 29, 30 and 37 are absent. Charts 35 and 41 print no chart number (taken
from their file names).

**The AGSO scale.** Twelve of the 25 older charts name "the AGSO timescale"
(no year), in the note "Magnetic polarity timescale after J.G. Ogg (1995),
rescaled to AGSO timescale"; 19 of the 25 say "the ages used are the
preferred AGSO ages" for each zone's global range, with the local Australian
range possibly different. Charts 20 and 21 name Gradstein et al. 1995 for stage
terminology (chart 20 also for some boundary dates). Charts 17, 19, 22 and 26
name no scale, and 28a and 28b name neither a scale nor "preferred AGSO ages".
The year of the AGSO scale is inferred, not printed on any older chart: six
newer charts (6, 31, 32, 33, 35, 36) call the
scale their predecessors used "AGSO 1996", and the other four revising charts
(34, 38, 39, 40) name "GTS 2004 and GTS 2008". Chart 20's "AGSO 1996" is a
source citation for the Petrel chart, not a time-scale statement (read from the
text). Record 61127's reference list cites Young and Laurie (eds) 1996, *An
Australian Phanerozoic Timescale*, the scale in its first column; we infer it
is the AGSO scale.

**What the newer charts revise.** Ten of the 11 newer charts (all but 41) print
"This chart represents a revision of previous charts including Australian
biozonation schemes calibrated to earlier geological timescales". None names
the charts it revises. Pairing by basin name in the titles (inferred):

| Newer chart | Older chart or charts, by basin |
| --- | --- |
| 31 Canning (2013) | 2 Canning (1998) |
| 32 Browse (2017) | 7 Browse (2001) |
| 33 Bonaparte (2014) | 15 Northern Bonaparte (1998); probably 1 Petrel Sub-basin (1996), part of the Bonaparte Basin (recall) |
| 34 Otway and Sorell (2015) | 9 Otway (1998), 13 Sorell (1998) |
| 35 Bight (2014) | 22 Southern Margin Basins (1999), which names the Bight Basin |
| 36 Northern Carnarvon (2013) | 11 North Carnarvon (1998) |
| 38 Offshore Northern Perth (2013), 39 Onshore Perth (2015) | 12 Perth (1998) |
| 40 Gippsland (2015) | 18 Gippsland (1998) |
| 6 Amadeus (2017), 41 Georgina (2013) | none in the mirror; 41 prints no revision statement |

The other 15 older charts have no newer chart of the same basin in the mirror:
3, 4, 5, 8A, 8B, 10 (Bowen), 14, 16, 17, 19, 20, 21, 26, 28a and 28b. Whether
GA's catalogue links them to newer records was not read.

**Status and revision notes.** Chart 5 prints "Preliminary version"; charts 19,
22 and 26 print "DRAFT". Bowen (10) says "the numerical time scale is under
revision because of the current SHRIMP program"; charts 4 and 28a say the
Permian and Triassic zone-to-stage correlations "are currently being revised".

**Printed identifiers.** Chart 7 prints "AGSO Catalogue No. 36593" but sits in
eCat 23346; charts 34, 39, 40 and 41 print "Geocat 83216"; charts 6 and 32
print 76687; the Record and its title page and preface print 64962. Source
claim (source scan): the superseded 2008 versions (eCat 65648, 65649, 65665)
and the annual compilations (68801, 70371, 73734, 75819, 83216) duplicate the
series and are not mirrored.

## Provenance and lineage

Compiled by AGSO and Geoscience Australia biostratigraphers. 24 of the 25
older charts print "The zonations presented here are from the STRATDAT Oracle
database", developed under the Australian Petroleum Systems Project and
maintained by the AGSO Phanerozoic Timescales Calibration and Development
Project team; the 25th (chart 7, Browse) cites STRATDAT only in notes on datums
and taxonomy. Record 61127 compares its new boundaries with "those currently
used in the STRATDAT database". None of the 11 newer charts or of the Record's
PDFs names STRATDAT. All 11 newer charts name the TimeScale Creator software,
in which they say their Australian zonations were compiled. The palynology
zonations were recalibrated to GTS2004 in 2006 (Monteil, coordinator;
Partridge's calibrations). Source claim (source scan): GA's biostratigraphy
page names GTS2012 as its standard and refers to an internal Timescales
Database that is not public. The newest printed year is 2017 (charts 6 and
32).

## Structure

Each of the 36 chart PDFs is one very large page with a text layer (36 of 36
have one page; 61127 has two pages, the Record eight): columns for time scale,
zones by fossil group, lithostratigraphy, sequences and events. On the
Petrel chart (rendered) the (c) symbol is a graphic; the 22 older charts with a
copyright line show only "Commonwealth of Australia 1998" or similar in the
text layer. Charts 5, 10 and 21 hold no copyright statement in the text layer
and no raster images. Source claim (source scan): the palynology zonation
charts' text layer is scrambled and needs coordinate parsing.

## Access

- **eCat.** Files at `https://d28rz98at9flks.cloudfront.net/<eCat>/<file>`;
  record pages at `https://pid.geoscience.gov.au/dataset/ga/<eCat>`, which
  redirects to the eCat page (hand check; it does not show that a record
  exists). Record metadata through the eCat CSW service (source scan).
- **Mirror.** `deep-server:/data/paleodata/ga-biozonation/raw/2026-10-22T0856Z_url/`,
  files prefixed with their eCat number. Index: [snapshots.tsv](snapshots.tsv).
- **Profile.** `python3 -I ga_charts_profile.py <raw version dir>
  profile/ga_charts_profile.tsv profile/ga_charts_summary.tsv`; needs
  `pdftotext` and `pdfimages` (poppler). Run on deep-server 2026-10-22.
- **TimeScale Creator datapack (not mirrored).** eCat 68802 ships TimeScale
  Creator 7.0 with an unencrypted tab-delimited datapack, "Geoscience
  Australia Biostratigraphy and Regional Lithostratigraphy" (GTS2016; about
  290 biostratigraphic columns and 12,000 zone and datum entries, per the
  scan). The eCat record says CC BY 4.0, but the software's licence reserves
  all rights to the Geologic TimeScale Foundation and its public Australian
  datapack is encrypted, so we hold no copy until GA confirms the datapack may
  be redistributed.

## Strengths

- Basin-by-basin zone schemes with lithostratigraphy and sequences on one
  page, compiled by the national survey's biostratigraphers.
- The 11 newer charts name GTS2012 or GTS2016 as their time scale and the
  TimeScale Creator software; 24 older charts name STRATDAT as their source.

## Weaknesses and pitfalls

- **Licence conflict across layers.** eCat's ISO metadata gives CC BY 4.0 for
  every record (source claim; not re-fetched in this pass). The PDFs print
  otherwise (checked): CC BY 4.0 on charts 34, 39, 40 and 41; CC BY 3.0
  Australia on chart 38; an all-rights-reserved notice ("no part may be
  reproduced by any process without written permission") on the 1998 Otway
  chart (9, eCat 23350), on Record 2006/23 and on each of its four charts and
  its title page in `Data.zip` (7 PDFs; the EPS and JPEG copies were not read);
  only a Commonwealth copyright line on 27 charts and on 61127; no copyright
  statement in the text layer of charts 5, 10 and 21. The CC statements
  exclude the Coat of Arms and material "otherwise noted". The mirror stays,
  on the metadata licence and Barry's authorisation to mirror openly licensed
  GA products (as relayed to this session, not quoted), but no document gives
  a redistribution right beyond what it prints. Do not pass copies to others,
  or cite them as CC BY 4.0, until GA answers (queued in CONTACTS.md). It is
  the same cross-layer conflict as FRED.
- **Mixed and partly unnamed time scales.** Charts of different years use
  different scales and 11 chart PDFs name none (9, 11, 13, 15, 17, 18, 19, 22,
  26, 28a, 28b); see Contents. Check each chart's scale before combining
  ages, and read an older chart's ages as AGSO ages (inferred AGSO 1996).
- **Many older charts are superseded; some are provisional.** Of the 12
  charts eCat labels "1994", nine have a newer chart of the same basin (2, 7,
  9, 11, 12, 13, 15, 18, and probably 1); 10, 28a and 28b do not. Of the 13
  older charts in the series record, only 22 probably does, in part. The newer
  charts say they revise earlier schemes but name no chart. Chart 5 is a
  preliminary version, 19, 22 and 26 are drafts, and Bowen (10) says its time
  scale is under revision.
- **The "1994" label.** eCat's "1994 charts" are 1996-2001 charts; do not cite
  them as 1994.
- **Printed identifiers and years.** Printed catalogue numbers do not always
  match the eCat record holding the file; chart 41 prints (c) 2013 while its
  file name says 2015; charts 35 and 41 print no chart number.
- **Not data.** Ages and zone boundaries must be read off PDFs. Tabular zone
  ages are in STRATDAT and in the TimeScale Creator datapack (restricted).
- **No updates after 2017** (newest printed year, checked); no chart can be on
  GTS2020, which came later (inferred).
- **Gaps in the numbering** (charts 23-25, 27, 29, 30, 37 not found).

## Overlap with other sources

STRATDAT is the database the older charts say they plot from and holds the
well picks these zones are assigned in; the ASUD register holds the unit names
and ages; PBDB's Australian ages use its own GTS2020-era scales, so a zone age
read from a pre-2012 chart will differ from PBDB's.

## EPRP relevance

Reference for interpreting STRATDAT picks and for dating Australian basin
successions in deep-time case studies. It cannot supply machine-readable zone
ages without digitising, and the older charts' scale is not tied to a named
year on the page.

## Citation and terms

Terms are per file, not per catalogue (see Weaknesses). Cite Geoscience
Australia (AGSO for charts printed before 2005), the chart number, its printed
year and the eCat record. Quote a chart's own printed licence, not CC BY 4.0
by default. The all-rights-reserved files (chart 9, Record 2006/23 and its
`Data.zip` PDFs) call for GA's written permission under their own notice.

## Verification log

- 2026-10-22, checked (`ga_charts_profile.py`, outputs in `profile/`, run on
  deep-server against mirror `2026-10-22T0856Z_url`): 39 files, 120,369,345
  bytes, every size and sha256 matching MANIFEST.json; 38 PDFs plus 7 PDFs
  inside `Data.zip`; 36 chart PDFs (24 in eCat 76687, 12 in other records); 25
  printed 1996-2001 and 11 printed 2013-17; printed years, chart numbers (34
  distinct; 23-25, 27, 29, 30, 37 absent), licence statements by file, time
  scales named, revision statements (10 charts), STRATDAT named (25 older
  charts, 24 of them saying their zonations come from it, and 61127),
  TimeScale Creator named (11 newer charts), draft and revision notes, printed
  catalogue numbers; raster images per PDF (none in charts 5, 10, 21).
- 2026-10-22, checked by reading, not coded: the Petrel chart's (c) symbol is
  drawn as a graphic (page rendered); chart 20's "AGSO 1996" is a source
  citation (text read).
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): eCat ISO
  metadata licence CC BY 4.0 for each record (two attempts to re-read eCat
  metadata through its API failed, so it was not re-fetched); superseded 2008
  versions and annual compilations; the 2018 revision of the series record;
  GA's standard time scale and internal database; the TimeScale Creator
  datapack's content and licence conflict; scrambled text layers in the
  palynology charts.
- 2026-10-22, inferred: the older charts' scale is the "AGSO 1996" of the
  newer charts' revision statements; the older-to-newer pairing by basin name;
  no chart can use GTS2020.
- 2026-10-22, recall: the Petrel Sub-basin lies in the Bonaparte Basin.
- 2026-10-22, independent review (Claude Sonnet 5.5 subagent) found three
  problems, applied here: the licence conflict (G1), the "1994" label and
  supersession (G2), and no committed code behind the checked claims (G3).
  Differences from its text, found by the profile: chart 38 prints CC BY 3.0
  Australia, not 4.0, and is dated 2013; charts 15 and 18 do print 1998; charts
  5, 10 and 21 print no copyright statement at all; chart 20's "AGSO 1996" is a
  citation, not a time scale; chart 41 is the only newer chart without a
  revision statement.
