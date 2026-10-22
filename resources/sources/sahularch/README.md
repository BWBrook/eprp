---
id: sahularch
name: SahulArch, a geochronological database for the archaeology of Sahul
kind: compilation
status: "active platform; data cut-off June 2022 (latest first-reference year 2022)"
last_update: "2022-06 (data); OCTOPUS layers stamped v2.3(2)"
scope:
  taxa: [not taxonomic; archaeological age determinations]
  time: "radiocarbon 0-55,000 BP; OSL to 239 ka; TL to 270 ka"
  space: "Sahul: mainland Australia, Tasmania, Torres Strait, New Guinea, eastern Indonesia; locations blurred to 25 km"
  record_unit: "one age determination (observation) on one sample, within site and metasite"
size:
  as_of: "OCTOPUS WFS snapshot 2026-10-22T04:17Z, DBVERNO v2.3(2)"
  ages: 10714
  radiocarbon: 9501
  osl: 973
  tl: 240
  radiocarbon_sites: 2658
access:
  tier: open-nc
  licence: "CC-BY-4.0 per OCTOPUS documentation; DataCite lists CC-BY-NC-4.0 for the radiocarbon v.2 DOI (10.25900/gpvr-ay04)"
  routes:
    - {type: wfs, url: "http://geoserver.octopusdata.org/geoserver/wfs (layers be10-denude:sahularch_c14, _osl, _tl)", state: "live, HTTP only, CSV/GeoJSON/shapefile, no feature cap", checked: 2026-10-22}
    - {type: web-ui, url: "https://octopusdata.org", state: "map viewer; export after choosing an intended use", checked: 2026-10-22}
    - {type: zenodo, url: "doi:10.25900/2mb4-rr36, ypr0-j711, xq40-t003 (Zenodo 7160945, 7161298, 7161748)", state: "2021 v.2 deposits marked OBSOLETE; about half the current ages", checked: 2026-10-22}
    - {type: doi-metadata, url: "doi:10.25900/gpvr-ay04, 9y07-4j77, af67-kh16", state: "2022 v.2 DOIs; metadata only, no files; point to OCTOPUS", checked: 2026-10-22}
  api: "OGC WFS 2.0.0 (GeoServer)"
versioning:
  replay: partial
  notes: "no downloadable 2022 release; the live layer is the data. 2021 deposits are archived. Snapshot and record DBVERNO and the WFS timeStamp"
mirror:
  path: deep-server:/data/paleodata/sahularch
  policy: "dated WFS snapshots of the three layers, plus the three 2021 Zenodo deposits for comparison"
  state: "snapshot 2026-10-22T0417Z_wfs; 2021 deposits complete"
lineage:
  upstream:
    - "AustArch (2014) as a search guide; ages re-extracted from original sources"
    - "IDASQ (Ulm and Reid 2000); regional compilations for the Top End, Victoria, Torres Strait (Linnenlucke 2022)"
  downstream:
    - "Mariani et al. 2024 (Science), Cadd et al. 2024; Australian ΔR atlas (Ulm et al. 2023)"
eprp_questions: []
citation:
  - "Saktura, W. M. et al. (2023). SahulArch: a geochronological database for the archaeology of Sahul. Australian Archaeology 89: 1-13. doi:10.1080/03122417.2022.2159751"
  - "Codilean, A. T. et al. (2022). OCTOPUS database (v.2). Earth System Science Data 14: 3695-3713. doi:10.5194/essd-14-3695-2022"
  - "the collection DOI with DBVERNO and retrieval date, e.g. doi:10.25900/gpvr-ay04 (radiocarbon), v2.3(2), retrieved 2026-10-22"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); lineage and documentation read by a Claude Sonnet subagent
  reviewed: "not yet"
---

# SahulArch

## Summary

SahulArch is the current compilation of archaeological ages for Sahul:
10,714 radiocarbon, OSL and TL determinations from about 2,700 sites, from
publications and grey literature to June 2022 (Saktura et al. 2023). Every
age carries the context and laboratory detail needed to judge it, rather than
a quality score. Locations are blurred to 25 km for cultural safety. Reach for
it for human-arrival chronologies, demographic time series ("dates as data"),
occupation of regions and environments, and as the human side of
megafauna–human overlap analyses with [FosSahul](../fossahul/README.md). The
data live only as layers in the [OCTOPUS](../octopus/README.md) database: the
2022 DOIs have no files, so every analysis must snapshot the live layers and
record their version stamp.

## Contents

Counts are our own ([profile](profile/sahularch_profile.tsv)) from the
2026-10-22 snapshot; every row carries version stamp `v2.3(2)`.

| Method | Ages | Sites | Metasites | Samples | Region |
| --- | ---: | ---: | ---: | ---: | --- |
| Radiocarbon | 9,501 | 2,658 | 2,268 | 9,335 | Australia 6,941; New Guinea 2,117; Torres Strait 339; Indonesia 104 |
| OSL | 973 | 118 | 92 | 850 | Australia 969; New Guinea 4 |
| TL | 240 | 47 | 42 | 233 | Australia 204; New Guinea 36 |

**Radiocarbon.**
- *Ages.* 0–55,000 BP. 179 rows have no age and 113 are flagged infinite;
  1,713 are older than 10,000 BP, 392 older than 30,000 and 97 older than
  40,000.
- *Materials.* Charred material 5,383; biogenic carbonate (mostly shell)
  2,861; plant 339; bone and other faunal 257.
- *Method.* AMS 3,137, conventional 2,512, not recorded 3,852.
- *Context.* Directly related to occupation: yes 3,506, no 2,168, not
  recorded 3,827. Sites are open 5,217 and closed (rockshelter or cave) 4,204.
- *Features dated.* Hearths 772, rock art 213, human burials 204.

**Luminescence.**
- *OSL.* Quartz in 957 of 973 ages. Age models: central age 408, finite
  mixture 240, minimum age 45. Ages run to 239 ka, 102 older than 50 ka.
- *TL.* Ages run to 270 ka.

**References.** First-cited publication years 1955–2022 (radiocarbon), so
nothing published after 2022 is included.

## Provenance and lineage

Source: Saktura et al. (2023), Codilean et al. (2022), the OCTOPUS
documentation and Zenodo records, read by the documentation scan.

- **Precursors.** IDASQ (Queensland, Ulm & Reid 2000) and AustArch 1–3
  (2008–2013), merged as [AustArch](../austarch/README.md) in 2014: 5,044
  radiocarbon and 478 other ages.
- **2017–2018.** OCTOPUS v1 hosted the first luminescence collections.
- **2021.** SahulArch "v.2" deposited on Zenodo: 5,039 radiocarbon, 347 OSL
  and 127 TL ages from 1,120 metasites. Now marked obsolete.
- **2022.** Data entry closed in June 2022; DOIs were minted for the v.2
  collections (metadata only), and the paper followed in January 2023 with
  9,504 radiocarbon, 973 OSL and 240 TL ages from 2,318 sites.
- **2024–2025.** OCTOPUS v2.2 and v2.3. The live radiocarbon layer has 9,501
  ages, three fewer than the paper.

**2021 against today** (checked): every 2021 observation ID is still live,
with its age unchanged. The live layers add 4,462 radiocarbon, 626 OSL and 113
TL ages. Growth has been additive.

**Relation to AustArch.** AustArch was used to guide the search for sites and
references; ages were re-extracted from the original sources. No ID
crosswalk between the two exists that we found.

**Authors.** Saktura, Rehn, Linnenlucke, Munack, Wood, Petchey, Codilean,
Jacobs, Cohen, Williams and Ulm (CABAH). Barry W. Brook is not an author.

## Structure

Four levels: metasite → site → sample → observation, with IDs `METASITEID`,
`SITEID`, `SMPID` and `OBSID1` (e.g. `ARCH0001C14001`). Replicate analyses of
one sample share `SMPID`, and letter suffixes mark reports that differ in
context or depth. Layers have 120 (radiocarbon), 143 (OSL) and 141 (TL)
columns.

- **Common fields.** Site names and aliases; country, region, state;
  bioregion (IBRA); open or closed site; up to four references with DOIs;
  dated feature, square, excavation unit, depth; occupation and context;
  laboratory code; free-text comments.
- **Radiocarbon.** Material (two levels); sample treatment, chemical and
  physical cleaning, contamination; yield, %C, %N, C:N, δ13C and other
  isotopes with their methods; diagenesis checks; `C14_AGE`, asymmetric
  errors, infinite flag, F14C.
- **Luminescence.** Material, mineral and grain size; water content;
  aliquot and procedure; equivalent dose, overdispersion; U, Th, K and
  radionuclide activities; alpha, beta, gamma and cosmic dose rates; age,
  random and total error, fading correction.
- **Missing values.** Numbers use −9999.99; text uses `ND` (no data), `NA`
  (not applicable) or "no data".
- **Location.** Polygons (15-sided, about 1,275 km²) in Web Mercator, made by
  random displacement within 25 km. True coordinates are held by OCTOPUS and
  not released.

## Access

**Mirror.** On `deep-server`:

```text
/data/paleodata/sahularch/octopus-wfs/raw/2026-10-22T0417Z_wfs/  sahularch_{c14,osl,tl}.csv + schemas + MANIFEST
/data/paleodata/sahularch/zenodo-2021-<record>/raw/<record>/     2021 shapefile zips (obsolete)
```

The CSVs include the polygon geometry as WKT. Take a fresh snapshot for new
work:

```bash
python3 resources/tools/data_mirror.py wfs http://geoserver.octopusdata.org/geoserver/wfs \
  be10-denude:sahularch_c14,be10-denude:sahularch_osl,be10-denude:sahularch_tl \
  /data/paleodata/sahularch/octopus-wfs --license "CC-BY-4.0 per OCTOPUS documentation"
```

The tool checks each CSV's row count against the server's count and records
the server timestamp. The service is HTTP only; the HTTPS form of the
subdomain resets the connection.

**Web.** octopusdata.org shows the layers on a map; export is enabled after
choosing an intended use. The 2022 DOIs resolve to metadata records pointing
there.

## Strengths

- **Context with every age.** Material, pretreatment, isotopes, dose-rate
  chains, stratigraphic context and occupation association are captured
  field by field, so users can apply their own quality rules.
- **Breadth.** Three dating methods and all of Sahul, including New Guinea,
  Torres Strait and eastern Indonesia (2,560 radiocarbon ages), and roughly
  double AustArch's size.
- **Cultural safety by design.** Blurred locations protect sites while
  keeping regional analysis possible.
- **Additive history.** Every 2021 age persists unchanged in today's data.
- **Programmatic access.** An open WFS with filtering and full exports.

## Weaknesses and pitfalls

1. **No downloadable current release.** The 2022 DOIs hold no files, the
   2021 files are obsolete, and the live layers can change. Cite the DOI, the
   DBVERNO and the retrieval date, and keep the snapshot.
2. **Licence conflict.** OCTOPUS says CC BY 4.0; DataCite says CC BY-NC 4.0
   for the radiocarbon v.2 DOI. Treat it as non-commercial until resolved.
3. **Replicates are kept.** 129 radiocarbon samples have more than one
   observation (295 rows), 162 laboratory codes appear on more than one row,
   and 96 rows have no laboratory code. Only 14 luminescence ages note that
   they were superseded, spelled "superceded". Choose one observation per
   sample before any frequency analysis.
4. **Conventional ages only.** No calibrated ages, curves or reservoir
   offsets are stored. With 30% shell and other carbonates, choose
   calibration curves and ΔR per record (the Australian ΔR atlas, Ulm et al.
   2023). Remove sentinel values first.
5. **Auxiliary fields are sparse.** Radiocarbon: sample depth 55%,
   pretreatment 29%, physical cleaning 16%, F14C 15%, recrystallisation check
   5%; δ13C method recorded for 14%. Luminescence is better documented
   (equivalent dose 90%, dose rate 88%, water content 34%).
6. **Spatial resolution is 25 km.** Do not analyse below that scale. Region
   fields were presumably assigned from true locations, so they may disagree
   with polygon centroids near boundaries (unverified).
7. **Dates as data.** Frequency analyses inherit taphonomic loss,
   site-focused sampling and research effort (Attenbrow & Hiscock 2015 and
   replies; Ward & Larcombe 2021). Seven sites carry more than 100 ages
   (Saktura et al. 2023).
8. **Completeness is self-assessed.** The paper estimates about 98%
   (radiocarbon); entry was prioritised for ages over 30 ka, recent
   publications, and northern and south-eastern Australia.
9. **Grey literature is restricted.** 77 source documents in the Zenodo
   community are restricted-access copies.

## Overlap with other sources

- **AustArch.** Most AustArch ages should be in SahulArch, re-extracted, but
  without a crosswalk. Do not pool them.
- **p3k14c** (global radiocarbon compilation) holds 3,657 Australian dates,
  all from AustArch and none older than 10,000 BP. Do not pool with
  SahulArch.
- **FosSahul.** About 33 site names are shared (Cuddie Springs, Warratyi,
  Kutikina and others; a name-matching heuristic). These are the sites where
  human and megafaunal chronologies can be compared directly.
- [Detail withheld pending disclosure to the data custodian.]

## EPRP relevance

No register question uses SahulArch yet. It is the human-chronology input for
any Sahul megafauna–human overlap work (with FosSahul), first-arrival and
demographic questions, and fire–people analyses with the charcoal records in
the Australian backlog.

## Citation and terms

[Detail withheld pending disclosure to the data custodian.]

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | WFS snapshot of three layers; row counts equal server counts; DBVERNO v2.3(2) on every row | checked |
| 2026-10-22 | Profile: counts, regions, materials, ages, replicates, field completeness | checked |
| 2026-10-22 | 2021 Zenodo deposits mirrored (md5 verified); all 2021 IDs live with unchanged ages | checked |
| 2026-10-22 | Superseded notes (14, spelled "superceded") | checked |
| 2026-10-22 | 2022 DOIs metadata-only; licence conflict; authorship | checked (documentation scan: Figshare, DataCite, JCU record) |
| 2026-10-22 | Structure, QA approach, obfuscation, lineage, uses, critiques | source claim (Saktura et al. 2023, Codilean et al. 2022, OCTOPUS docs) |
| 2026-10-22 | p3k14c Australian rows are AustArch only; FosSahul site-name overlap | checked (documentation scan) |
