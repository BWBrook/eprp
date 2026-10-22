---
id: shape-index
name: Palaeoarchive index for the SHAPE 6 ka and OZ-INTIMATE compilations (PANGAEA 879515)
kind: deposit
status: frozen
last_update: 2017-08-10
scope:
  taxa: [not taxonomic; palaeoclimate archives]
  time: "Holocene and last glacial records, mostly the last 35 kyr; 6 ka comparison"
  space: "Australia and surrounding seas, by OZ-INTIMATE region (TNW, TSW, TNE, TSE, StA, TeE, TeS, NSO, SSO)"
  record_unit: "one palaeoclimate record (core, speleothem, coral, lake or swamp sequence) described in free text"
size:
  as_of: "PANGAEA 879515 (single version)"
  records: 37
access:
  tier: open
  licence: "CC-BY-3.0 (PANGAEA)"
  routes:
    - {type: pangaea, url: "doi:10.1594/PANGAEA.879515 (Database_SUPPLEMENT2.xlsx)", state: "single version", checked: 2026-10-22}
    - {type: journal-supplement, url: "https://cp.copernicus.org/articles/13/1661/2017/ (supplement zip)", state: "same cell contents, different bytes", checked: 2026-10-22}
  api: none
versioning:
  replay: exact
  notes: "one deposited version"
mirror:
  path: deep-server:/data/paleodata/shape-index
  policy: "the deposited file"
  state: "2026-10-22 url snapshot (30.6 kB)"
lineage:
  upstream:
    - "OZ-INTIMATE regional synthesis (Reeves et al. 2013a, 2013b) and later records, compiled for the SHAPE project"
  downstream:
    - "Ackerley et al. 2017 (PMIP 6 ka evaluation)"
eprp_questions: []
citation:
  - "Ackerley, D., Reeves, J., Barr, C. et al. (2017). Climate of the Past 13: 1661-1684 (PMIP2 and PMIP3 mid-Holocene simulations evaluated against Australasian proxies). doi:10.5194/cp-13-1661-2017"
  - "data: Ackerley, D., Reeves, J. M. & Harvey, N. (2017), doi:10.1594/PANGAEA.879515"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# SHAPE / OZ-INTIMATE palaeoarchive index

## Summary

A one-sheet spreadsheet listing 37 Australasian palaeoclimate records that
underlie the OZ-INTIMATE synthesis (Reeves et al. 2013) and the SHAPE 6 ka
model evaluation (Ackerley et al. 2017), with each record's region, reference,
archive type, proxy, climate sensitivity, resolution and age span. It holds no
data values. Use it as a finding aid: to see which archives the regional
syntheses rested on, then fetch each record from NOAA, PANGAEA or the paper.

## Contents

Our counts ([profile](profile/shape_profile.tsv)):

- 37 records; regions (records can carry several codes): TNW 10, TSW 8, TSE 8,
  TeS 8, TeE 6, StA 4, NSO 3, TNE 3, SSO 1.
- Archive types (from free text, approximate): marine cores 13, corals 5,
  lakes 4, swamps or peat 3, speleothems 2, other or mixed 10.
- Completeness: coordinates or record identifiers in 35 rows, a 0–6 ka change
  statement in 22, start and end ages in 26 and 27, a link to data in 12, of
  which only 5 give a URL or DOI (the others give a person to contact).

## Provenance and lineage

Compiled at Federation University Australia (Ackerley, Reeves, Harvey) for
SHAPE (Southern Hemisphere Assessment of PalaeoEnvironments), the successor to
AUS-INTIMATE, and deposited with Ackerley et al. (2017). Region codes follow
Reeves et al. (2013a). Selection followed INTIMATE criteria (continuous,
centennial to millennial resolution, robust chronology), relaxed in
OZ-INTIMATE to admit discontinuous but well-dated records. The same table is
the paper's supplement.

## Structure

One sheet, 15 populated columns of free text: Region/Country, Reference,
Record Type, Record ID and Coord., Proxy, Proxy Measurement, Climate
Sensitivity, Change (0 ka to 6 ka), Comparison to Present?, Sample Resolution,
Dating Resolution, Start Year, End Year, Link to Data Storage, Notes.

## Access

`Database_SUPPLEMENT2.xlsx` from PANGAEA; mirrored at
`deep-server:/data/paleodata/shape-index/raw/` (index:
[snapshots.tsv](snapshots.tsv)).

## Strengths

- A compact, expert-selected list of the records behind the main
  Australasian palaeoclimate syntheses.

## Weaknesses and pitfalls

- **Metadata only**, in free text with mixed coordinate formats and no stable
  record identifiers; several rows describe multi-site or regional records.
- **Few data links.** Only 5 of 37 rows link to data; the rest must be traced
  through their references.
- **Personal contacts.** Some cells give individuals' email addresses as the
  data route; treat them as personal data, not as a catalogue route.
- Qualitative change and sensitivity columns mix sea-surface temperature,
  precipitation and vegetation signals.

## Overlap with other sources

Several listed records are in [SISAL](../sisal/README.md) (speleothems),
[Neotoma](../neotoma/README.md) (pollen) or NOAA and PANGAEA (marine cores
and corals). A record-by-record crosswalk has not been made.

## EPRP relevance

A finding aid for Late Quaternary Australian palaeoclimate archives, for
choosing validation records for climate forcings such as
[Beyer et al. 2020](../beyer2020/README.md).

## Citation and terms

CC BY 3.0. Cite the PANGAEA DOI and Ackerley et al. (2017); cite each
underlying record's own publication when used.

## Verification log

- 2026-10-22, checked: file mirrored; 37 records and column completeness
  counted; region codes; data-link cells.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): authorship,
  dates and licence; identity with the journal supplement; selection criteria
  and the SHAPE project history.
