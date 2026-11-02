---
id: stratdat
name: STRATDAT, Geoscience Australia's borehole biostratigraphy (WFS layer resfacs:Biostratigraphy)
kind: database
status: active
last_update: "record dated 2022; live WFS snapshot 2026-10-22"
scope:
  taxa:
    - "microfossil biozones: dinocysts, spore-pollen, planktonic and benthic foraminifera, nannoplankton"
    - "sequences, time slices and chronostratigraphic picks (stage, series, system)"
  time: "Proterozoic to Quaternary; most picks with ages have Cretaceous or Paleogene base ages"
  space: "Australian sedimentary basins, mostly the offshore North West Shelf (Northern Carnarvon, Bonaparte, Browse) and the Gippsland and Otway basins; 1,636 boreholes"
  record_unit: "pick: one zone datum (zone top, zone base, exact start or end, or presence only) or stratigraphic interval at one measured sample depth in one borehole, with the zone's age range, pick type and confidence grade"
size:
  as_of: "WFS snapshot 2026-10-22T0856Z"
  picks: 50128
  boreholes: 1636
  picks_with_real_zone_ages: 44234
  zone_names: 1373
access:
  tier: open
  licence: "CC-BY-4.0 (WFS capabilities; eCat 146442)"
  routes:
    - {type: wfs, url: "https://services.ga.gov.au/gis/resfacs/ows", state: "live; layer resfacs:Biostratigraphy; CSV output, 80 fields, no feature cap", checked: 2026-10-22}
    - {type: catalogue, url: "https://doi.org/10.26186/146442", state: "eCat 146442; metadata record dated 2022", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 (GeoServer)"
versioning:
  replay: none
  notes: "live layer with no releases; snapshot and record the date"
mirror:
  path: deep-server:/data/paleodata/stratdat
  policy: "dated WFS snapshots"
  state: "2026-10-22T0856Z_wfs (40 MB CSV and schema; rows equal numberMatched)"
lineage:
  upstream:
    - "petroleum company well reports (the original Esso data set, 8,152 picks, is the largest single source)"
    - "AGSO and GA basin modules and well folios (Spencer, Kennard and colleagues, 1993-2002)"
    - "palynological reviews by Morgan, and Partridge's 1996 reinterpretations of STRATDAT datums"
  downstream:
    - "GA Basin Biozonation and Stratigraphy charts of 1996-99 (ga-biozonation entry); basin geohistory studies"
eprp_questions: []
citation:
  - "Geoscience Australia, STRATDAT biostratigraphy, doi:10.26186/146442, WFS resfacs:Biostratigraphy, retrieved 2026-10-22, CC BY 4.0"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent; review fixes by a Claude Sonnet 5.5 subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# STRATDAT: Geoscience Australia borehole biostratigraphy

## Summary

STRATDAT is Geoscience Australia's database of biostratigraphic picks in
petroleum and stratigraphic boreholes. A record is a datum at one sample depth:
the biozone (dinocyst, spore-pollen, foraminiferal, nannofossil and others),
whether the depth marks the zone's top, its base or only its presence, the
zone's age range in Ma, a confidence grade, the stratigraphic unit and the
source report. The open WFS layer holds 50,128 picks from 1,636 boreholes,
mostly on the North West Shelf and in the southern-margin basins. As far as we
know it is the only open, tabular source of Australian biozone assignments
(recall). Reach for it to date sedimentary sections in Australian basins, to
study Mesozoic and Cenozoic microfossil zones at basin scale, or to tie
boreholes into time. Two cautions govern its use. Only 13.8% of picks name a
stratigraphic unit that can be matched to [ASUD](../asud/README.md), and the
`_MIDPOINT` unit and sequence fields are evaluated at half the sample depth, so
only the `_TOP` fields describe the sample. It records zones, not taxon
occurrences.

## Contents

Counts are our own ([profile](profile/stratdat_profile.tsv),
[midpoint check](profile/stratdat_midpoint_check.tsv)).

- 50,128 picks, 1,636 boreholes (petroleum 49,841 picks, stratigraphic 284,
  groundwater 3); 45,528 offshore and 4,600 onshore. By state: Western
  Australia 27,651, Ashmore and Cartier Islands 8,869, Victoria 7,332,
  Northern Territory 2,480, South Australia 1,556, Tasmania 1,238, Queensland
  997, New South Wales 5.
- Basins, from the first token of `BOREHOLE_PROVINCE` (picks, boreholes):
  Northern Carnarvon 18,192 and 448; Bonaparte 11,602 and 308; Gippsland
  5,913 and 244; Browse 5,530 and 106; Otway 1,952 and 63; Eromanga 1,500 and
  190 (1,392 picks and 179 boreholes also carry a Cooper Basin token); Bass
  995 and 30; Perth 894 and 48; Roebuck 775 and 10; Eucla 765 and 16;
  Canning 710 and 63. A few provinces list a sub-basin first (Torquay
  Sub-basin, 101 picks). The second token gives the sub-basin or structural
  element: Dampier Sub-basin 5,633 picks and 137 boreholes, Vulcan 5,499 and
  159, Caswell 4,248 and 70, Barrow 3,936 and 121, Rankin Platform 2,514 and
  50, Exmouth Plateau 2,352 and 41, Petrel 2,121 and 62, Gippsland Central
  Deep 1,932 and 72; Gippsland picks with no sub-basin 2,554 and 102.
- Classes: dinocyst 11,916 (+2,894 subzone), planktonic foraminifera 7,828,
  spore-pollen 5,221 (+4,507 subzone), nannoplankton 3,962 (+524 subzone), time
  slice 2,936, sequence 2,738 (+271 sequence boundary), stage/age 826, benthic
  foraminifera 672, series/epoch 657, system/period 370; 3,309 unclassed.
- Zone names: 1,373 distinct. 5,722 picks (11.4%) have no zone name, and
  these are exactly the picks with no age. Another 172 carry the placeholder
  zone `unknown` at 0-0 Ma, leaving 44,234 picks (88.2%) with real zone ages.
- Zone span (base minus top age, real ages with base not younger than top):
  median 3.0 Myr; deciles 0.6, 1.2, 1.6, 2.4, 3.0, 3.9, 5.2, 8.2, 11.9 Myr;
  314 picks have zero span and 1,633 (3.7%) span more than 20 Myr. 103 picks
  have a base age younger than the top.
- Base age, in GTS2012 system edges (23.03, 66.0, 145.0, 252.17 and 541 Ma; a
  base on an edge counts as the younger system): Neogene and Quaternary 3,555,
  Paleogene 7,780, Cretaceous 20,668, Jurassic-Triassic 9,159, Palaeozoic
  2,972, Precambrian 100. The layer's own system rows put the Paleogene base at
  66.04, the Cretaceous base at 145.7 and the Triassic base at 251.9 Ma (see
  Time scale below). With those edges 534 picks with a base of 66.04 move from
  the Cretaceous to the Paleogene and 731 picks with bases of 145.01 to 145.7
  move from the Jurassic-Triassic to the Cretaceous: Paleogene 8,314,
  Cretaceous 20,865, Jurassic-Triassic 8,428.
- Pick types: `HIGH_LOW` H 20,966, L 19,964, M 9,071, T 56, B 65 (6 blank; the
  codes are defined under Structure); 49,045 preferred and 1,082 alternate
  picks. Confidence grades 1 to 9 (1 excellent), mostly 2 and 3 (13,934 and
  20,150).
- Boreholes by rig-release decade: 1910s 1, 1930s 3, 1940s 1, 1950s 16, 1960s
  177, 1970s 264, 1980s 552, 1990s 419, 2000s 191, 2010s 9, undated 3; 1,433
  of 1,636 (87.6%) were released before 2000.

## Provenance and lineage

Picks were compiled by AGSO and Geoscience Australia from company well
completion reports and basin studies: the original Esso data set (8,152
picks) and the AGSO basin modules and well folios of the 1990s (Dampier,
Barrow-Exmouth, Vulcan, Browse, Petrel, Beagle-Bedout) lead the sources, with
palynological reviews by Morgan and reinterpretations by Partridge. The rig
release date is the drilling date, not the date of interpretation: source
references run to 2002 (Browse Basin composite well logs, Petrel geohistory
modelling). The layer is the pick database behind the 1996-99
[GA biozonation charts](../ga-biozonation/README.md), which name STRATDAT; the
2013-17 chart series does not (source claim: the independent review of that
entry).

## Structure

One flat layer of 80 fields, documented in the WFS schema
(`Biostratigraphy_schema.xml`, mirrored beside the data). Quotations below are
from it.

- **Borehole:** `ENO`, name, type, purpose, collar coordinates (GDA94),
  rig-release date, onshore or offshore, state, permit, operator, depth
  reference, and `BOREHOLE_PROVINCE` (a comma-separated list of GA basins,
  then sub-basins). `BOREHOLE_PID` is complete in all picks.
- **Sample:** `SAMPLE_DEPTH_M`, "the measured depth of the sample (m) relative
  to KB/RT". Every pick has one depth and no top or base depth. The depth
  reference is rotary table (28,516 picks), kelly bushing (19,218), drill
  floor (1,381), rig floor (516), ground surface (358), seafloor guide base (37)
  or unknown (102), with `DEPTH_REF_POINT_ELEV_M` its elevation (metres, except
  15 picks in two boreholes recorded in feet). Depths are measured depths along
  the hole, not true vertical depths or depths below sea level. `SAMPLENO` is
  empty in all picks and `SAMPLE_PID` is the bare prefix
  `http://pid.geoscience.gov.au/sample/AU` with no number in all 50,128, so the
  layer carries no usable sample identifier.
- **Pick:** `ZONE_NAME` with `ZONE_ABBREVIATION` and `CLASS`, `TOP_AGE_MA` and
  `BASE_AGE_MA` ("age in millions of years at top/base interval (International
  Geological Time Scale 2012)"), `HIGH_LOW`, `PICK_DESC`, `PREFERRED_ALTERNATE`,
  `CONFIDENCE_CODE`, `SOURCE_REF` (filled for 50,079 picks),
  `BIOSTRATIGRAPHY_REMARK` and `ACTIVE`.
- **Stratigraphic context:** `STRAT_UNIT_TOP`, `_MIDPOINT` and `_BASE` (the GA
  preferred group, subgroup, formation and member, comma-separated; several
  units are separated by semicolons, as in 137 midpoint values), `STRATNO_MIDPOINT`
  (ASUD numbers), `STRATIGRAPHIC_AGE_MIDPOINT`, `DINOCYST_MIDPOINT`,
  `SPORE_POLLEN_MIDPOINT` (empty), `SEQUENCE_TOP`, `_MIDPOINT` and `_BASE`,
  `STATE_STRAT_UNIT_TOP`, `_MIDPOINT` and `_BASE` (state-advised names,
  semicolon-separated), and the distances to the unit and the sequence above
  and below. The schema defines each as the unit "at the top depth / midpoint of
  the depth / base depth of the sample"; the midpoint and base fields do not do
  that (see Weaknesses).

Code vocabularies, with counts:

- `HIGH_LOW` (documented): H "top of zone" 20,966; L "base of zone" 19,964; M
  "presence of zone but no indication of position" 9,071; T "exact start of
  zone" 56; B "exact end of zone" 65; blank 6. H and L together are 81.7% of
  picks, so most picks mark a zone boundary, not "this depth lies in the zone".
- `PREFERRED_ALTERNATE`: P 49,045, A 1,082, blank 1. The schema calls the
  alternate depth a second option for a low-confidence datum.
- `CONFIDENCE_CODE` (documented): a sample type plus a grade, "1 = excellent, 9 =
  bad". Types: side-wall core 27,519, ditch cuttings (`Ditch Cut`) 10,358,
  horizon 8,957, core 1,097, miscellaneous 699, core or side-wall core 244, with
  a few others (`Junk` 13, `Coal` 5); 1,209 have no type. Grades: 3 20,150, 2
  13,934, 4 6,316, 1 5,364, 5 2,324, 9 232, 6 128, 7 61, 8 5; 1,614 have no grade
  (48,932 picks carry a code).
- `PICK_DESC` (the schema says only "type of data used to select the zone";
  the values are not defined): PALAEO 26,823; SNGL DEPTH 9,441; SEQ BD/INT
  3,115; TIMESLICE 2,999; MIN AGE 2,255; MAX AGE 1,646; UNCON FLT 1,522;
  FORMATION 1,377; WELL 417; LOG PICK 325; LOG PALAEO 104; ALL DATA 92;
  CONDENSED 3; KEY HORIZ 2; blank 6.
- `ACTIVE` is A and `OVERALL_ACCESS` is O in all picks.

## Access

- **WFS.** `data_mirror.py wfs https://services.ga.gov.au/gis/resfacs/ows
  resfacs:Biostratigraphy stratdat --license ...` returns the whole layer as
  one CSV (40 MB) with the schema and checks the row count.
- **Mirror.** `deep-server:/data/paleodata/stratdat/raw/2026-10-22T0856Z_wfs/`
  (`Biostratigraphy.csv`, `Biostratigraphy_schema.xml`). Index:
  [snapshots.tsv](snapshots.tsv).
- **Profiling.** `python3 stratdat_profile.py Biostratigraphy.csv
  StratigraphicUnit.csv profile/stratdat_profile.tsv` (the ASUD file from
  `deep-server:/data/paleodata/asud/raw/2026-10-22T0604Z_wfs/`) and `python3
  stratdat_midpoint_check.py Biostratigraphy.csv
  profile/stratdat_midpoint_check.tsv`. Standard library only.

## Strengths

- To our knowledge the only open, tabular record of Australian biozone
  assignments (recall), with a zone age range, pick type, confidence grade and
  source reference for each pick, at national scale.
- Every pick has a borehole with a persistent identifier, collar coordinates
  and a measured depth.
- Covers the offshore basins that outcrop data cannot: 45,528 of 50,128 picks
  are offshore.
- `STRAT_UNIT_TOP` is consistent with ASUD: for 77.0% of the picks that can be
  checked the zone's age range overlaps the unit's, against 10-32% for
  randomly reassigned units (below).

## Weaknesses and pitfalls

- **The `_MIDPOINT` fields describe half the sample depth, not the sample.** Each
  pick has one depth. `STRAT_UNIT_TOP` is the unit there, and
  `STRAT_UNIT_MIDPOINT` differs from it for 5,096 of the 5,383 picks that carry
  both. Rebuilding each borehole's unit sequence from `STRAT_UNIT_TOP` and
  `DISTANCE_TO_STRAT_UNIT_ABOVE_M`, the midpoint unit equals the unit at 0.50
  times the sample depth for 3,213 of the 3,214 picks that can be tested. At
  other fractions the match falls: 4.9% at 1.00, 9.7% at 0.90, 26.8% at 0.70,
  68.7% at 0.55, 85.7% at 0.52, 90.7% at 0.48 and 76.4% at 0.45; a looser
  reconstruction gives 96.6% at 0.50 and 6.3% at 1.00. The result holds in
  every depth band (99.8-100%) and for the 1,453 picks testable at every
  fraction (100% at 0.50, 12.5% at 1.00). No constant depth offset can do this:
  the best match for offsets up to 1,000 m is 32.9%. So the fields give the
  unit at the midpoint of 0 and the sample depth, as if the top of a depth
  interval were missing and read as zero (inferred; the schema documents one
  depth and defines the midpoint as "the midpoint of the depth of the sample").
  At Yampi 1 seven units first appear in the midpoint field at 2.00 to 2.05
  times the depth of their tops, and the Aptian dinocyst zone
  *Diconodinium davidii* 2biii (113.14-122.25 Ma) at 1,863 m sits in the
  Jamieson Formation by `STRAT_UNIT_TOP` (ASUD 125-95 Ma) but in the Hibernia
  Formation by the midpoint field (ASUD 50-42 Ma). The midpoint unit is
  shallower, so normally younger. Checked against ASUD ages on the 4,758 picks
  that have both units, real zone ages and matched ASUD ages, 77.4% overlap
  through the top unit and 11.6% through the midpoint unit.
- **The same applies to the other midpoint and base fields.** `STRAT_UNIT_BASE`
  equals `STRAT_UNIT_MIDPOINT` in 5,464 of 5,579 picks and is a member of its
  semicolon list in 5,557. `SEQUENCE_MIDPOINT` equals the sequence at 0.50 times
  the depth for 2,204 of 2,207 testable picks (9.6% at 1.00), and
  `SEQUENCE_BASE` equals it in 3,067 of 3,070. `DISTANCE_TO_STRAT_UNIT_BELOW_M`
  is measured from half the depth: half the depth plus the distance lands on a
  known unit top (within 0.06 m) for 3,818 of 5,579 picks, the full depth plus
  the distance for 9. `STRATNO_MIDPOINT`, `STRATIGRAPHIC_AGE_MIDPOINT` and
  `DINOCYST_MIDPOINT` are defined at the same midpoint and we expect the same
  offset (inferred; not tested separately). `STATE_STRAT_UNIT_MIDPOINT` differs
  from `STATE_STRAT_UNIT_TOP` in 8,332 of 9,690 picks, `SEQUENCE_MIDPOINT` from
  `SEQUENCE_TOP` in 2,355 of 2,600, and `STATE_STRAT_UNIT_BASE` equals
  `STATE_STRAT_UNIT_TOP` in all 11,751, so it adds nothing. Use the `_TOP`
  fields; `STRAT_UNIT_TOP` is the one we tested against ASUD ages.
- **Few picks link to ASUD, and none by identifier.** `STRAT_UNIT_TOP` is filled
  for 6,911 picks (13.8%) in 369 boreholes (22.6%). Matching its most specific
  name to a name that is unique in ASUD (17 ASUD names are shared) resolves all
  of them. `STATE_STRAT_UNIT_TOP` is filled for 11,751 picks (23.4%, 547
  boreholes), 8,874 of them where `STRAT_UNIT_TOP` is empty; for 52.4% of these a
  state string equals a unique ASUD name, which we have not age-checked. The only
  ASUD numbers are in `STRATNO_MIDPOINT` (5,579 picks, 11.1%), the half-depth
  field.
  Their order is not "group to formation": for picks with several numbers and one
  unit list the most specific unit's number is first in 2,592, last in 1,263 and
  in the middle in 14.
- **Zone ages agree with unit ages well above chance, but the check is weak.**
  631 of the 6,911 picks with a top unit have no zone age. Of the other 6,280
  (366 boreholes), 4,836 (77.0%) overlap the ASUD age of their unit, 698 miss
  by up to 5 Myr, 489 by 5-20 Myr and 257 by more than 20 Myr (a strict
  last-name match gives 4,830 of 6,274, also 77.0%). Reassigning units at random
  gives 10.5% over all picks, 15.8% within the same state, 19.0% within the same
  basin and 32.2% within the same borehole (30.1% where the borehole has two or
  more distinct units; observed 76.9%; means of 20 shuffles, seed in the code).
  By borehole, the median overlap rate is 0.86, 39.9% of boreholes have every
  pick overlapping and 7.9% have under half, but 46.7% have five or fewer
  checked picks. By class, dinocyst zones overlap in 1,141 of 1,485 picks,
  spore-pollen 786 of 961, planktonic foraminifera 398 of 556 and benthic
  foraminifera 61 of 108. ASUD ranges can be wide, and ASUD ages are rounded and
  carry known errors (CONTACTS.md (queue held back), C9), so overlap is a
  necessary check, not proof. ASUD snapshot used: 2026-10-22T0604Z.
- **Time scale: documented as GTS2012, not uniformly applied.** The schema says
  the ages are on GTS2012 (source claim) and the catalogue record says zones "can
  be calibrated to GTS 2004, 2012, 2020" (source scan). The layer's own
  chronostratigraphic rows carry values close to GTS2012 in the Cenozoic
  (23.03, 33.89, 55.96, 66.04 Ma; recall), but the Cretaceous base is 145.7 in
  the system, series and Berriasian rows and 145.01 in the 113 Neocomian picks,
  and the Triassic base is 251.9 (checked, table `chronostrat_ages`). GTS2012
  itself has 145.0 and 252.17 and, for the Aptian and Barremian bases, 125.0 and
  129.4 (recall), where the layer has 126.3 and 130.77. The scale is not
  uniform inside the layer, so check it before any comparison finer than about
  1 Myr (inferred from the differences above).
- **A pick is a datum, not an occurrence in the sample.** H and L picks mark where
  a zone starts or ends (81.7% of picks), M only that the zone is present (9,071),
  and T and B give exact start and end. A user who treats a pick as "this depth
  is in zone X" has to handle H and L explicitly. Confidence runs 1 (excellent)
  to 9 (bad), with 426 picks at grades 6 to 9.
- **Zones, not occurrences.** The taxon lists behind a pick are not in the layer.
- **Coverage gaps in age.** 5,722 picks (11.4%) have no zone name and no age;
  172 more have the placeholder `unknown` at 0-0 Ma and are not ages.
- **Data errors.** 103 picks have a base age younger than the top; 3 have a
  depth of zero or less. 65 picks in 15 boreholes are deeper than 5,000 m, up to
  14,900 m at Petrel 1A (Poeppels Corner 1 14,033 m, Tern 1 9,150 m, Fishburn 1
  8,200 m), though the schema states metres. These are probably feet recorded as
  metres (inferred): 14,900 ft is 4,542 m, and no borehole is known to reach
  14.9 km (recall; the world's deepest is about 12.3 km). None of them has the
  feet elevation unit; the 15 picks that do are in COOK 1 (12) and Palm Valley 1
  (3).
- **Old data.** 87.6% of boreholes were released before 2000 and only 9 in the
  2010s. The release date is not the interpretation date.

## Overlap with other sources

- **ASUD.** Unit names link to ASUD for 13.8% of picks; see above. The
  [ASUD entry](../asud/README.md) records the register's own age errors.
- **NSB and Triton.** Both hold species occurrences from ocean-drilling cores;
  STRATDAT holds zone picks from petroleum boreholes on the continental
  margin. Complementary in place and kind.
- **GA biozonation charts.** The 1996-99 charts summarise the zone schemes these
  picks use, with their calibrations.

## EPRP relevance

Dated sections across Australia's continental margins for Mesozoic and
Cenozoic questions: marine plankton turnover and basin histories around
Australia, and age control for any analysis tied to offshore stratigraphy.
It cannot support unit-level dating through the midpoint fields, and zone ages
need their calibration checked before they are compared across schemes.

## Citation and terms

CC BY 4.0. Cite Geoscience Australia, the DOI and the retrieval date, and the
source references of the picks used.

## Verification log

- 2026-10-22, checked ([stratdat_profile.py](stratdat_profile.py), output in
  [profile/stratdat_profile.tsv](profile/stratdat_profile.tsv)): the row count
  of 50,128 (equal to numberMatched in `MANIFEST.json`); counts by state,
  class, basin (first and second token), pick type, confidence grade and
  depth reference; rig-release decades; ages, placeholders, span deciles and
  base-age bins under both edge sets; the ages of the layer's chronostratigraphic
  rows; depth anomalies; identifier completeness; ASUD link coverage;
  `STRATNO_MIDPOINT` order; the top-unit age check against ASUD snapshot
  2026-10-22T0604Z with its strict variant, per-borehole spread and
  reassignment null; the like-for-like top and midpoint comparison; the Yampi 1
  example at 1,863 m.
- 2026-10-22, checked ([stratdat_midpoint_check.py](stratdat_midpoint_check.py),
  output in [profile/stratdat_midpoint_check.tsv](profile/stratdat_midpoint_check.tsv)):
  the half-depth test of `STRAT_UNIT_MIDPOINT` and `SEQUENCE_MIDPOINT` against
  the rebuilt top sequences (fractions, offsets, depth bands, fixed set); base
  and state field equalities; `DISTANCE_TO_STRAT_UNIT_BELOW_M`; the Yampi 1
  unit tops.
- 2026-10-22, source claim: the field definitions, GTS2012 ages, `HIGH_LOW` and
  confidence codes and the depth reference from the mirrored schema
  (`Biostratigraphy_schema.xml`); the eCat record, DOI, licence and the
  calibration statement (source scan, Claude Sonnet subagent); the 1996-99
  chart lineage (independent review of the ga-biozonation entry).
- Inferred: that the midpoint fields use the midpoint of 0 and the sample depth,
  and that the other midpoint fields share it; that the deepest samples are
  feet; the need to check the time scale for comparisons finer than about 1 Myr.
- Recall: GTS2012 boundary ages (145.0, 252.17, 125.0, 129.4 Ma, and the
  Cenozoic values close to the layer's); the depth of
  the world's deepest borehole; that STRATDAT is the only open, tabular source of
  Australian biozone assignments.
- 2026-10-22, independent adversarial review (Claude Sonnet subagent); the
  findings on the schema, the half-depth mechanism, the `STRATNO_MIDPOINT` order
  bug, basin levels, age statistics, ASUD coverage, the null and the minor
  points are applied above.
