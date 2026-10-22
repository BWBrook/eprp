---
id: stratdat
name: STRATDAT, Geoscience Australia's borehole biostratigraphy (WFS layer resfacs:Biostratigraphy)
kind: database
status: active
last_update: "record dated 2022; live WFS snapshot 2026-10-22"
scope:
  taxa: ["microfossil biozones: dinocysts, spore-pollen, planktonic and benthic foraminifera, nannoplankton; also sequences and chronostratigraphic picks"]
  time: "Proterozoic to Neogene; most picks Cretaceous to Paleogene"
  space: "Australian sedimentary basins, mostly the offshore North West Shelf, Bonaparte, Browse, Gippsland and Otway basins; 1,636 boreholes"
  record_unit: "pick: one biozone or stratigraphic interval assigned to one sample depth in one borehole, with zone age range and confidence"
size:
  as_of: "WFS snapshot 2026-10-22T0856Z"
  picks: 50128
  boreholes: 1636
  zone_names: 1374
access:
  tier: open
  licence: "CC-BY-4.0 (WFS capabilities; eCat 146442)"
  routes:
    - {type: wfs, url: "https://services.ga.gov.au/gis/resfacs/ows (layer resfacs:Biostratigraphy)", state: "live; CSV output, 80 fields, no feature cap", checked: 2026-10-22}
    - {type: catalogue, url: "doi:10.26186/146442 (eCat 146442)", state: "metadata record dated 2022", checked: 2026-10-22}
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
    - "petroleum company well reports (the original Esso data set is the largest single source), AGSO and GA basin modules and well folios (Spencer, Kennard and colleagues, 1993-2002), palynological reviews (Morgan, Partridge)"
  downstream:
    - "GA Basin Biozonation and Stratigraphy charts (ga-biozonation entry); basin geohistory studies"
eprp_questions: []
citation:
  - "Geoscience Australia, STRATDAT biostratigraphy, doi:10.26186/146442, WFS resfacs:Biostratigraphy, retrieved 2026-10-22, CC BY 4.0"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# STRATDAT: Geoscience Australia borehole biostratigraphy

## Summary

STRATDAT is Geoscience Australia's database of biostratigraphic picks in
petroleum and stratigraphic boreholes: for each sample depth, the biozone
assigned (dinocyst, spore-pollen, foraminiferal, nannofossil and others), the
zone's age range in Ma, the pick type and confidence, the stratigraphic unit,
and the source report. The open WFS layer holds 50,128 picks from 1,636
boreholes, mostly on the North West Shelf and in the southern-margin basins.
It is the only open, tabular source of Australian biozone assignments, and
links each pick to the national stratigraphic register
([ASUD](../asud/README.md)). Reach for it to date sedimentary sections in
Australian basins, to study Mesozoic and Cenozoic microfossil zones at basin
scale, or to tie boreholes into time. It records zones, not taxon
occurrences.

## Contents

Counts are our own ([profile](profile/stratdat_profile.tsv)).

- 50,128 picks, 1,636 boreholes (petroleum 49,841 picks, stratigraphic 284,
  groundwater 3); 45,528 offshore and 4,600 onshore. By state: Western
  Australia 27,651, Ashmore and Cartier Islands 8,869, Victoria 7,332,
  Northern Territory 2,480, South Australia 1,556, Tasmania 1,238, Queensland
  997, New South Wales 5.
- Largest basins by picks: Northern Carnarvon (Dampier, Barrow, Exmouth,
  Rankin, Beagle sub-basins), Bonaparte (Vulcan, Petrel), Browse (Caswell),
  Gippsland and Otway. By boreholes: Cooper–Eromanga 143, Vulcan 136,
  Dampier 127, Barrow 106, Gippsland 102.
- Classes: dinocyst 11,916 (+2,894 subzone), planktonic foraminifera 7,828,
  spore-pollen 5,221 (+4,507 subzone), nannoplankton 3,962, time slice 2,936,
  sequence 2,738, stage/age 826, benthic foraminifera 672, series/epoch 657,
  system/period 370; 3,309 unclassed. 1,374 distinct zone names.
- Ages: 44,406 picks give a zone top and base age in Ma; the median zone spans
  3.0 Myr. By base age: Cretaceous 19,963, Jurassic–Triassic 9,781, Paleogene
  7,775, Neogene 3,727, Palaeozoic 2,961, Precambrian 199.
- Pick types: high, low and mid picks (H 20,966, L 19,964, M 9,071); 49,045
  preferred and 1,082 alternate; confidence codes combine sample type and a
  grade from 1 to 5 (side-wall core, ditch cuttings, horizon).
- Boreholes by rig-release decade: 1960s 177, 1970s 264, 1980s 552, 1990s
  419, 2000s 191, 2010s 9.

## Provenance and lineage

Picks were compiled by AGSO and Geoscience Australia from company well
completion reports and basin studies: the original Esso data set (8,152
picks) and the AGSO basin modules and well folios of the 1990s (Dampier,
Barrow–Exmouth, Vulcan, Browse, Petrel, Beagle–Bedout) lead the sources, with
palynological reviews by Morgan and reinterpretations by Partridge. It is the
pick database behind the [GA biozonation charts](../ga-biozonation/README.md).

## Structure

One flat layer of 80 fields: borehole (ENO, name, type, purpose, coordinates,
rig-release date, operator, permit, depth reference), sample (depth, sample
type), stratigraphic context (`STRAT_UNIT_TOP`, `_MIDPOINT`, `_BASE`; ASUD
unit numbers in `STRATNO_MIDPOINT`, sometimes several, from group to
formation; sequence and state-unit fields), the pick (`ZONE_NAME` with its
authority, `ZONE_ABBREVIATION`, `CLASS`, `HIGH_LOW`, `PICK_DESC`,
`PREFERRED_ALTERNATE`, `CONFIDENCE_CODE`, `TOP_AGE_MA`, `BASE_AGE_MA`,
`SOURCE_REF`, `BIOSTRATIGRAPHY_REMARK`) and persistent identifiers for the
borehole and sample.

## Access

- **WFS.** `data_mirror.py wfs https://services.ga.gov.au/gis/resfacs/ows
  resfacs:Biostratigraphy stratdat --license ...` returns the whole layer as
  one CSV (40 MB) and checks the row count.
- **Mirror.** `deep-server:/data/paleodata/stratdat/raw/2026-10-22T0856Z_wfs/`.
  Index: [snapshots.tsv](snapshots.tsv).

## Strengths

- The only open, tabular record of Australian biozone assignments, with ages,
  confidence and sources, at national scale.
- Ties picks to boreholes with persistent identifiers and to ASUD units.
- Covers the offshore basins that outcrop data cannot.

## Weaknesses and pitfalls

- **The `_MIDPOINT` unit fields do not describe the sample.** For 5,096 of
  the 5,383 picks that carry both, `STRAT_UNIT_MIDPOINT` differs from
  `STRAT_UNIT_TOP` for the same point sample, and the midpoint unit is often
  much younger: at Yampi 1, 1,863 m, an Aptian dinocyst zone sits in the
  Jamieson Formation by the top-unit field but in the Eocene Hibernia
  Formation by the midpoint field. Use `STRAT_UNIT_TOP`; the ASUD numbers in
  `STRATNO_MIDPOINT` inherit the problem.
- **Zone ages agree with unit ages only moderately.** Through the top-unit
  field, 4,834 of 6,361 picks with ages (76%) overlap the ASUD age of their
  unit; 701 miss by up to 5 Myr and 336 by more than 20 Myr. The unit fields
  are filled for only about an eighth of picks.
- **Time scale not recorded.** No pick states which time scale its ages use;
  the catalogue record says zones "can be calibrated to GTS 2004, 2012, 2020"
  (source scan). Treat ages as nominal to a few hundred thousand years.
- **Zones, not occurrences.** A pick is an interpretation of a sample's zone;
  the taxon lists behind it are not in the layer.
- **Data errors.** 103 picks have a base age younger than the top; the deepest
  sample is recorded at 14,900 m, beyond any Australian borehole.
- **Old data.** Most boreholes were released before 2000; few picks are later
  than the 2000s.

## Overlap with other sources

- **ASUD.** Unit names and numbers link to ASUD; see the age check above.
- **NSB and Triton.** Both hold species occurrences from ocean-drilling cores;
  STRATDAT holds zone picks from petroleum boreholes on the continental
  margin. Complementary in place and kind.
- **GA biozonation charts.** The charts summarise the zone schemes these picks
  use, with their calibrations.

## EPRP relevance

Dated sections across Australia's continental margins for Mesozoic and
Cenozoic questions: marine plankton turnover and basin histories around
Australia, and age control for any analysis tied to offshore stratigraphy.

## Citation and terms

CC BY 4.0. Cite Geoscience Australia, the DOI and the retrieval date, and the
source references of the picks used.

## Verification log

- 2026-10-22, checked ([stratdat_profile.py](stratdat_profile.py)): WFS
  snapshot of 50,128 features equal to numberMatched; counts above; top- and
  midpoint-unit disagreement; zone ages against ASUD unit ages through both
  unit fields; the Yampi 1 example read directly.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): eCat record,
  DOI and licence; the calibration statement.
