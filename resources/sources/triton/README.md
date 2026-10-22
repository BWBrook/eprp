---
id: triton
name: Triton, a species-level database of Cenozoic planktonic foraminiferal occurrences
kind: compilation
status: active
last_update: 2025-01-23
scope:
  taxa: [planktonic foraminifera]
  time: Cenozoic; ages 0-66.0 Ma (GTS2020)
  space: "global ocean: deep-sea drilling holes, piston and gravity cores, core-tops; some land sections"
  record_unit: one species (harmonised name) reported in one sample by one study, with abundance in the study's units
size:
  as_of: "v4 (2025-01-23), triton_update_2023.RData"
  presence_rows: 541846
  presence_rows_in_range: 532066
  rows_with_zero_abundance: 1265059
  samples: 51135
  holes: 5003
  species: 395
access:
  tier: open
  licence: CC0
  routes:
    - {type: figshare-collection, url: "https://doi.org/10.6084/m9.figshare.c.5242154", state: "v4, 11 items, 20 item versions", checked: 2026-10-22}
    - {type: r-package, url: "chronosphere::fetch(src = 'triton')", state: "serves v1 and v3 only; series 'main' at v3 is the sample-level no_dup table; pre-v4 units", checked: 2026-10-22}
    - {type: web-query, url: "https://www.mikrotax.org/system/ranges-tritonbiogeog.php", state: "experimental map query on a pre-v3 copy; no API", checked: 2026-10-22}
    - {type: github, url: "https://github.com/IFenton/TritonDB", state: "v1 code only, last push 2021-07-20, no licence", checked: 2026-10-22}
  api: "none beyond the Figshare API"
versioning:
  replay: exact
  notes: "four published data versions (2021, 2022, 2023, 2025); file names repeat across versions with different contents"
mirror:
  path: deep-server:/data/paleodata/triton
  policy: "all 20 item versions (1.6 GB): each data version is a distinct product, and the small code, documentation and working-file versions record each version's pipeline"
  state: "complete 2026-10-22"
lineage:
  upstream:
    - "PANGAEA: 213,800 presence rows"
    - "DSDP/ODP/IODP reports: 138,136"
    - "Neptune/NSB export of March 2019: 108,339"
    - "ForCenS core-tops: 64,033"
    - "Fenton et al. 2016: 14,387"
    - "Lloyd et al. 2012 land sections: 3,151"
  downstream:
    - "BioDeepTime: 822 time series"
    - "pforams@mikrotax: relational copy"
    - "Fenton et al. 2023 and Woodhouse et al. 2023, Nature"
eprp_questions: [Q-005, Q-007, Q-012, Q-020, Q-027]
citation:
  - "Fenton, I. S., Woodhouse, A., Aze, T., Lazarus, D., Renaudie, J., Dunhill, A. M., Young, J. R. & Saupe, E. E. (2021). Triton, a new species-level database of Cenozoic planktonic foraminiferal occurrences. Scientific Data 8: 160. doi:10.1038/s41597-021-00942-7"
  - "the Figshare item version used, e.g. doi:10.6084/m9.figshare.13517414.v4"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); paper, documentation and ecosystem reads by Claude Sonnet subagents
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# Triton

## Summary

Triton is the largest species-level compilation of Cenozoic planktonic
foraminifera: about 540,000 presence records of 395 species in 51,000 samples
from 5,000 holes and cores. Taxonomy is harmonised, ages are kept or re-derived
on GTS2020, and every record has a palaeolatitude (from two different plate
models; Pitfall 4). It merges six sources:
PANGAEA, ocean-drilling reports, Neptune (NSB), the ForCenS core-top census,
Fenton et al. (2016) and land sections from Lloyd et al. (2012). Reach for it
for foraminiferal diversity, biogeography, thermal-niche and turnover studies
at species level across the Cenozoic. It is CC0 and versioned on Figshare.
Choose the file variant deliberately: the main 2023 file is not deduplicated,
and the deduplicated file is a different, sample-level product (Pitfall 1).

## Contents

Counts are our own ([profile](profile/)), from v4 (2025-01-23),
`triton_update_2023.RData`, data frame `triton.pres`. "In range" means
`trim == "inc"` (see Structure).

| Measure | All presences | In range |
| --- | ---: | ---: |
| Presence rows | 541,846 | 532,066 |
| Samples | 51,135 | 50,968 |
| Holes and cores | 5,003 | 4,996 |
| Species (harmonised) | 395 | 392 |
| Original-name strings | 3,608 | 3,492 |
| Distinct original names, after splitting merged synonyms | 2,770 | |

`orig.species` joins merged synonyms with ", " (1,259 such strings), so name
strings overcount names. Sample and hole identifiers belong to one source:
3,435 of 47,415 samples with a depth share position and depth with another
source's sample, so samples and holes double-count some physical ones.

The companion data frame `triton` adds 1,265,059 zero-abundance rows, 1,806,905
rows in all. Zeros are not uniformly true absences (Pitfall 6).

**By source** (in-range presences):

| Source | Rows | Samples | Holes |
| --- | ---: | ---: | ---: |
| PANGAEA | 211,515 | 19,779 | 406 |
| DSDP/ODP/IODP reports | 134,470 | 14,202 | 544 |
| Neptune (NSB) | 105,527 | 11,022 | 240 |
| ForCenS core-tops | 64,033 | 4,205 | 3,664 |
| Fenton et al. 2016 | 13,639 | 1,494 | 60 |
| Lloyd et al. 2012 (land) | 2,882 | 266 | 82 |

**Time** (in range, GTS2020): Pleistocene–Holocene 280,065; Pliocene 73,096;
Miocene 98,369; Oligocene 22,533; Eocene 44,641; Paleocene 13,362. Ages run
from 0 to 65.997 Ma, with 682 rows marginally negative (to −0.00006 Ma).
64,644 in-range rows have age 0, almost all ForCenS core-tops (64,033). Every
row has an age and a palaeolatitude: rows without either were dropped during
the build.

**Space** (in range, present latitude): 0–30° 296,988; 30–60° 213,465; above
60° 21,613 (4.1%). Northern hemisphere 353,949, southern 178,117.

**How ages were obtained** (`age.calc`, in range): original author ages
315,763 (59%); Triton age-depth models 105,739; interpolation between zone
boundaries 48,051; biozone midpoints 39,984; magnetostratigraphy 22,529.

**Abundance units** (in range): binned categories 238,737 (45%); relative
abundance 182,186; presence/absence 60,570; counts 46,534; number per gram
4,039.

**Study purpose** (`reason`, all presences): community analysis 212,428;
biostratigraphy 161,718; unspecified 139,225; selected species 22,989; extreme
event 5,486. The authors advise taking alpha diversity only from studies that
recorded whole communities, about 40% of the data.

## Versions and file variants

The Figshare collection holds 11 items; the data item (`Triton`, 13517414)
has four versions, each a different product. All are mirrored.

| Version | Date | File(s) | Presence rows | In range | What it is |
| --- | --- | --- | ---: | ---: | --- |
| v1 | 2021-06-21 | `triton.RData` | 512,941 | 503,955 | the published dataset, deduplicated at record level |
| v2 | 2022-12-01 | `Triton dataset.zip`: `triton.RData` (= v1), `triton_full.RData`, `triton_No_rounding.RData` | 512,941 / 541,846 / 512,941 | 503,955 / 530,068 / 503,952 | v1 plus a non-deduplicated table and an unrounded-age table |
| v3 | 2023-07-20 | `triton_update_2023.RData`, `triton_no_dup.RData` | 541,846 / 514,243 | 532,066 / – | 2023 update (finer age rounding, `orig.age`), and a sample-level merged table |
| v4 | 2025-01-23 | `Triton.zip` with the same two file names | 541,846 / 514,243 | 532,066 / – | v3 with abundance units corrected |

- **v1 against the paper.** The deposited file has 512,941 presences and
  1,716,250 rows in all; the paper reports 512,922 and 1,716,087. It flags
  8,986 presences out of range; the paper reports 10,990.
- **v4 against v3.** The version-history document says units changed from
  "Count" to "Number per gram" for holes SA03-1, AMC99-1, ST04-1 and
  188.1165.1165B. Our checks find exactly 1,520 presence rows relabelled
  (3,371 with zeros). The independent review compared the tables cell by cell:
  the only other differences are a date stamp, floating-point noise below
  3e-6, and whitespace in 12 `orig.species` cells. The v2 variants were not
  regenerated and keep the old labels.
- **v1 to the 2023 update.** On the 512,941 shared rows (independent review):
  3,663 Fenton et al. (2016) rows (66% of that source) change age, by up to
  1.18 Myr. v1's code skipped time-scale conversion for rows with no
  publication year, and the 2023 code converts them. `pal.lat` changes in 1,863
  rows (38 by more than 1°), `trim` in 44. Species and abundances are
  unchanged.
- **Readme lag.** The readme (v2) describes only the v2 files; v3 and v4 are
  documented only in the version-history `.docx` files.

## Provenance and lineage

Built by I. S. Fenton and colleagues (Fenton et al. 2021; Oxford, Bristol,
Leeds, MfN Berlin, NHM London). The deposited R pipeline (`Triton code` v3)
runs: age models (`Triton_1AgeModels.R`), source loaders (`Triton_2Neptune_plus.R`,
`Triton_3Pangaea.R`, `Triton_4MoveDB.R`, `Triton_5IODPextra.R`), combination
(`Triton_6CombinedData.R`) and the sample-level merge
(`Triton_8_RemovingDuplicates.R`). Source details, from the deposited code and
documents:

- **Neptune.** One export of all Cenozoic foraminifera on GTS2012, with
  questionable, invalid and reworked records excluded. The deposited
  spreadsheet's sheet is named "190314 Neptune forams Cenozoic" (14 March
  2019) and has 121,647 rows; the paper's Table 1 counts 112,598.
- **PANGAEA.** A search for "plank* AND foraminifera" gave 8,203 hits. They
  were filtered by keyword (multinet, sediment trap and box core excluded),
  for species-named columns, for non-isotope data and for age or zone
  columns, then accepted or rejected by hand.
- **Drilling reports.** Legacy DSDP/ODP/IODP cores missing from the first
  compilation, mined from DESClogik and PANGAEA. Cores were kept where two or
  more consecutive tie points existed. Blank count cells became zeros.
- **ForCenS.** The 4,205 quality-flagged core-top counts of Siccha & Kucera
  (2017).
- **Lloyd et al. (2012).** Land sections only; the marine records came from
  Neptune and were dropped.

Not deposited: the raw PANGAEA downloads, the MoveDB database and the
drilling-report spreadsheets. A full rebuild from raw inputs is therefore not
possible; the deposited `Triton working` intermediates are needed. The code is
interactive (it uses `svDialogs` prompts and saved choice objects) and was
written for R 3.6.1.

**Neptune input, measured record by record.** Triton's Neptune rows carry the
NSB `sample_id` in `sampleID` (`<leg>-<sitehole>_<sample_id>`). Linking v4 to
four NSB snapshots ([link_nsb.py](link_nsb.py),
[result](profile/link_nsb_v4.txt)):

- all 108,339 Neptune rows (11,105 samples) link to NSB foraminifera samples,
  with no hole or depth mismatch;
- Triton's pre-conversion age (`orig.age`) equals NSB's stored age on every
  row in the 2018-10-27 and 2019-08-30 snapshots, and 207 rows differ against
  2020-12-15. That is consistent with the March 2019 sheet name. All Neptune
  rows have `age.calc == "Orig"`;
- Triton's `pal.lat` equals NSB's `paleo_latitude` on all 106,095 rows where
  NSB has one (2018-10-27): Neptune rows carry NSB's Seton et al. (2012)
  palaeocoordinates, not Triton's Matthews et al. (2016) ones;
- 93.3% carry an original name string that NSB records in the same sample,
  96.5% once merged synonyms are split;
- against NSB's final 2023 snapshot, 3,422 rows differ by more than 1 Myr from
  NSB's stored ages, and 5,101 from ages recomputed from NSB's current models
  (NSB Pitfall 5). Triton does not carry NSB's later age-model revisions;
- Triton's Neptune rows cover 11,104 of NSB's 14,503 dated foraminifera
  samples (77%). This is a lower bound: the same samples can also enter Triton
  through PANGAEA or drilling-report copies.

**Downstream.** BioDeepTime (822 Triton time series), a relational copy on
pforams@mikrotax, and about 50 citing papers (OpenAlex 53, Crossref 47, on
2026-10-22). Uses include Cenozoic diversity and turnover (Fenton et al. 2023,
*Nature*, doi:10.1038/s41586-023-05712-6; Woodhouse et al. 2023, *Nature*,
doi:10.1038/s41586-023-05694-5), ecogroup and community-equitability biogeography
(Swain et al. 2024, *Nature*, doi:10.1038/s41586-024-07337-9; Woodhouse et al.
2023, *Biogeosciences*, doi:10.5194/bg-20-121-2023), Pliocene–Pleistocene
turnover networks (Larina et al. 2025, *Nat. Commun.*,
doi:10.1038/s41467-025-60362-8), thermal niches against climate models (Mathes
et al. 2024, *GEB*, doi:10.1111/geb.13905), extinction risk and occupancy as an
independent check on NSB (Smith, Kocsis & Kiessling 2025, *Biogeosciences*,
doi:10.5194/bg-22-3503-2025), fossil-record completeness (Lamyman et al. 2026,
*J. Syst. Palaeontol.*, doi:10.1080/14772019.2026.2669255) and sampling
heterogeneity (Andréoletti et al. 2026, *Paleobiology*,
doi:10.1017/pab.2026.10094). These studies sit on different versions (v1, v2,
v3, v4), so their numbers are not interchangeable.

## Structure

Each RData file holds a pair of data frames: `<name>` with zero abundances and
`<name>.pres` with presences (`abundance > 0`). The main tables have 72
columns. `rowID` is unique; `sampleID` and `holeID` are scoped to one source.
The `no_dup` tables (`triton.no.dup`, `triton.no.dup.pres`) have 25 columns,
keyed by a merged sample id `triton.SID`. They keep the merged original sample
ids in `sep.sampleID` (with `no.samples`, `sep.abun`, `sep.abun.units`), but
have no `trim`, `db.source` or `source` column.

Key columns of `triton.pres` (definitions from the paper and code):

- **Taxon.** `species` is the harmonised name; `orig.species` holds the
  published name(s), with merged synonyms joined by ", ". Harmonisation uses a
  5,894-row synonym table with 437 accepted species.
- **Abundance.** `abundance` is in the units given by `abun.units`. Binned
  categories become ranks from 0, presence/absence becomes 0/1, and
  inconsistent records get a 0.01 placeholder. `num.ind` is the summed
  abundance of retained species in the sample (not `total.IDd`).
  `rel.abun = abundance / num.ind × 100`, and is computed even for binned
  ranks.
- **Age.** `age` is in Ma on GTS2020. `age.calc` records how it was obtained:
  `Orig`, `Model`, `Interp`, `Zone` or `Magneto`. `age.err` is 0 on every
  `Model`, `Interp` and `Magneto` row, NA on every `Orig` row, and the zone
  width (`rng.age`) on `Zone` rows, whose age is the zone midpoint. Rows with
  `age.err` above 5 were removed. `round.age` is the age rounded to whole Ma.
  `orig.age` (v3 onwards) is the age before conversion.
- **Place.** `latitude` and `longitude` are present-day positions. Neptune
  rows carry NSB's palaeocoordinates: Seton et al. (2012), at the sample's own
  age. All other rows use Matthews et al. (2016) via GPlates, computed on
  whole-Ma ages, with present positions where `round.age` is 0 (age below
  0.5 Ma). `round.lat` and `round.pal.lat` are rounded to 5°.
- **Range flag.** `trim` is `exc` when the sample age lies more than 5 Myr
  (ages above 23 Ma) or 2 Myr (younger) beyond the species' global speciation
  or extinction age (`Speciation`, `Extinction`), otherwise `inc`.
- **Provenance.** `db.source`, `dbID`, `source`, `year`, `reason`,
  `processing`, `preservation`, `sample.type`.

Code vocabularies (distinct values in the v4 presence table,
[checks.tsv](profile/checks.tsv)): `trim` 2; `Macro/micro` 2; `segment` 4;
`age.calc` 5; `abun.units` 5; `reason` 6; `age.model` 23; `processing` 31;
`sample.type` 34 (free text mixing PANGAEA device terms with labels such as
"ODP"); `AM.type` 79; `preservation` 1,043 (unstandardised free text).
`reason` has six codes; the paper lists four.

## Access

**Mirror.** On `deep-server`:

```text
/data/paleodata/triton/raw/<item>_v<N>_<id>/        every item version + MANIFEST.json
/data/paleodata/triton/derived/Triton_v4_13517414/  triton_update_2023.RData, triton_no_dup.RData,
    triton_update_2023_pres.tsv.gz, triton_no_dup_pres.tsv.gz  (for non-R use)
    triton_update_2023_pres_dedup_cross_source.tsv.gz         (Pitfall 1 recipe)
/data/paleodata/triton/derived/Triton_v2_13517414/  the three v2 tables, unzipped
```

The version index is in [figshare-versions.tsv](figshare-versions.tsv).
`python3 resources/tools/data_mirror.py figshare 5242154 <dest> --latest`
fetches the newest version of each item.

**Loading.**

```r
e <- new.env()
load("/data/paleodata/triton/derived/Triton_v4_13517414/triton_update_2023.RData", envir = e)
tp <- subset(e$triton.pres, trim == "inc")
```

```python
import pandas as pd
tp = pd.read_csv("/data/paleodata/triton/derived/Triton_v4_13517414/triton_update_2023_pres.tsv.gz",
                 sep="\t", low_memory=False)
tp = tp[tp["trim"] == "inc"]
```

The TSV files are unchanged exports of the presence tables
([triton_export.R](triton_export.R)); their row counts match the profile.

**Removing cross-source duplicates.** [triton_dedup.R](triton_dedup.R) drops
only rows that duplicate another source's record by v1's key and have a
recorded depth, keeping the highest-priority source in each group (v1's order:
ForCenS, IODP, Neptune, PANGAEA, Lloyd, Fenton; a different order can be
passed). On v4 it removes 16,260 rows (PANGAEA 13,858, Fenton 2,282, Neptune
120) and leaves 525,586 ([log](profile/dedup_v4.txt)). It does not recompute
`num.ind` or `rel.abun`; afterwards 794 of 45,465 non-presence/absence samples
have relative abundances summing below 100.

**Other routes.** The R package `chronosphere` (`fetch(src = "triton")`)
serves v1 and v3 but not v4. At v3 its series `main` is the sample-level
`triton_no_dup` table, not the published one, and the four holes corrected in
v4 still carry "Count". Mikrotax offers an experimental map query
(ranges-tritonbiogeog.php) on an unedited copy of a pre-v3 version, with no
API. Triton is not in PANGAEA, GBIF or PBDB.

[triton_checks.R](triton_checks.R) reruns the data checks quoted here
([checks.tsv](profile/checks.tsv)).

## Strengths

- **Scale and harmonisation.** Four times Neptune's foraminiferal records,
  one taxonomy and one time scale, with original names, abundances and ages
  kept beside the harmonised ones.
- **Abundances where they exist.** Counts, relative abundances and binned
  categories, with zero-abundance rows that make counted assemblages explicit.
- **Open and well documented.** CC0 data, a data paper, the R pipeline, the
  intermediate working files, the synonym table and the time-scale tables are
  all deposited.
- **Reach beyond drilling.** Piston and gravity cores and 4,205 ForCenS
  core-tops add modern and high-resolution Quaternary coverage.

## Weaknesses and pitfalls

1. **The 2023 update is not deduplicated, and neither available fix is
   simple.** v1 removed records sharing species, abundance, depth and position
   to 0.001°, keeping one per group by source priority (ForCenS, IODP,
   Neptune, PANGAEA, Lloyd, Fenton). The 2023 pipeline (code v2) no longer
   does, so `triton_update_2023.RData` has 28,832 duplicate rows by v1's exact
   key (5.3%), in 22,342 groups ([checks.tsv](profile/checks.tsv)). Its row and
   sample counts equal v2's non-deduplicated table.
   - *Cross-source copies:* 16,256 groups (16,267 excess rows) span two sources,
     12,608 of them Neptune and PANGAEA. These are true duplicates.
   - *Within one source:* 6,086 groups (12,565 rows). Most are not duplicates:
     8,450 of the duplicate rows have no depth, so v1's key collides distinct
     samples at one position. In 1,249 of those 1,991 groups the ages differ by
     more than 0.5 Myr. Applying v1's key wholesale would delete 62% of Fenton
     et al. (2016) and 47% of Lloyd et al. (2012) records.
   - *The remedy:* drop cross-source copies only, with a recorded depth
     ([triton_dedup.R](triton_dedup.R), Access). Choose the source priority
     deliberately: v1's keeps the Neptune copy, with its 2019 NSB age and Seton
     palaeocoordinates. Records with the same species, depth and position but
     a different abundance or unit survive (about 4,750 more, per the
     independent review).
   - *`triton_no_dup.RData` is a different product.* It merges records into
     samples by position, depth and whole-Ma age, and drops samples with more
     than half their species out of range (out-of-range rows in kept samples
     remain: 8,618 would be `exc`). It merges abundances by unit: maximum for
     presence/absence and binned, mean for relative abundance and number per
     gram, sum for counts (the version history says mean). Use it for
     sample-level work, not occurrence counts.
2. **File names do not identify versions.** v3 and v4 ship files with the
   same names and different contents. Cite the Figshare version DOI, and check
   the sha256 in the mirror's manifest.
3. **Neptune records are frozen at 2019.** Ages and palaeocoordinates are
   NSB's as they stood in 2018–19 (Provenance). 3,422 rows differ from NSB's
   final stored ages by more than 1 Myr, and 5,101 from its recomputed ages.
   For Neptune-derived samples, decide which chronology to trust.
4. **Two plate models.** The 108,339 Neptune rows (20% of presences) carry
   Seton et al. (2012) palaeocoordinates at the sample's exact age; the rest
   are Matthews et al. (2016) on whole-Ma ages. The paper says all are
   Matthews. Palaeolatitude bands therefore pool two models; recompute
   palaeocoordinates for Neptune rows if that matters.
5. **Age uncertainty is mostly unrecorded.** 59% of in-range ages are the
   original authors' (no error given). `age.err` is 0 on every `Model`,
   `Interp` and `Magneto` row (83% of re-derived ages): a placeholder, not a
   measured zero. Zone-midpoint ages can rest on zones up to 5 Myr wide.
6. **Zeros are not uniformly absences.** Zero-abundance rows come from
   explicit absence codes, binned codes outside the expected sequence, blank
   drilling-report cells, and Neptune entries originally coded "extremely
   rare or questionable".
7. **Mixed abundance units.** 45% binned, 11% presence/absence. `rel.abun`
   is computed for binned ranks, and the "Relative abundance" or "Count" label
   was assigned by rule, so a count dataset can be mislabelled.
8. **Purpose-driven recording.** 30% of presence rows come from
   biostratigraphic studies that often list marker species only, so absence
   from such a sample is weak evidence.
9. **Range flag is coarse.** `trim` uses global speciation and extinction
   ages (often from subtropical zonations) and the sample age alone; the
   authors expect it to be less precise at high latitudes.
10. **Documentation and data disagree in places.**
    - *Rounding.* The readme says v1 ages were rounded to 5 kyr; the code
      rounds converted ages to two decimals, and the version history says the
      same. By method, v1 original ages sit on a 10-kyr grid (98%) and zone
      midpoints on 5 kyr (99%), while age-model ages (`Model`, `Interp`,
      `Magneto`, 44% of v1 ages) are essentially unrounded. Those are the ages
      the readme's rationale targets.
    - *Counts.* The paper's counts differ slightly from the deposited v1 (see
      Versions).
    - *Merge rules.* The version history describes means for merged counts;
      the code sums them (Pitfall 1).
    - *Conversion.* v1 skipped time-scale conversion for records with no
      publication year (Versions).
    - *File names.* The readme's `Triton_non_rounded.RData` is
      `triton_No_rounding.RData` in the zip.
11. **Identifiers are source-scoped.** No `sampleID` or `holeID` spans
    sources, so a physical sample reported via two sources counts twice in
    sample and hole totals, and in per-site sample counts.
12. **Cenozoic only.** No records older than 66 Ma, so no Cretaceous baseline
    for the K–Pg (relevant to Q-007).

**What the literature says** (source claims, from our ecosystem scan):

- *Sampling heterogeneity.* Andréoletti et al. (2026) model Triton's
  sampling: raw data show an excess of recent occurrences for extinct
  species; geography explains about a third of the variation, and age method
  and biostratigraphic purpose are significant predictors.
- *Taxonomy.* Smith et al. (2025) find Triton consistently less diverse than
  NSB's other plankton groups and suggest taxonomic lumping. Weitkamp et al.
  (2025, doi:10.5194/jm-44-1-2025) call Neogene planktonic foraminiferal
  taxonomy out of date. Triton's ranges and names rest on the Aze et al.
  (2011) framework, which Lamyman et al. (2026) supersede; they find 43 of 390
  macroperforate morphospecies with no Triton records.
- *Individual errors.* Pearson et al. (2023, doi:10.5194/jm-42-211-2023)
  identify the only Atlantic *Pulleniatina primalis* record older than 6 Ma
  (DSDP Site 141) as a database error.
- *Provenance.* A 2026 thesis comparing Triton, Neptune and eODP in PBDB
  (McCoy, University of Victoria; abstract only) notes that Triton and Neptune
  lack provenance for many occurrences, and that the databases diverge in the
  Oligocene and the last few million years.

## Overlap with other sources

- **NSB.** Every Triton Neptune row links to an NSB sample (above).
  Site-level, 181 of NSB's 203 foraminifera sites are in Triton. Do not pool
  Triton and NSB foraminifera; use one or the other, and if Triton, choose its
  chronology for Neptune samples deliberately.
- **PANGAEA.** The largest input (40% of presences). Most cross-source
  duplicates in the 2023 update pair a PANGAEA record with a Neptune record.
- **ForCenS** (Siccha & Kucera 2017): all 4,205 quality-flagged core-top
  samples are in Triton.
- **BioDeepTime** holds 822 Triton series and 609 NSB series, so the same
  foraminiferal data can enter it twice.
- **PBDB and eODP.** No Triton import into PBDB. PBDB's own planktonic
  foraminifera are modest (about 74,000 Globigerinoidea occurrences). The eODP
  project (Sessa et al. 2023, doi:10.1029/2022GC010655) loads shipboard
  drilling data into PBDB and Macrostrat from the same reports Triton mined,
  with different taxonomy: an alternative, not a duplicate.
- **Related compilations.** ForCenS-LGM (Jonkers et al. 2024, 2,365 Last
  Glacial Maximum assemblages, CC BY 4.0) and FORCIS (modern water-column
  census) postdate or complement Triton; neither is included in it.

## EPRP relevance

The independent review reran both EPRP builds that use Triton, unchanged and
then after deduplication. Both reproduce their committed outputs from the
mirror's v4 file.

- **Q-007** (biotic legacy): the event-support gate uses
  `triton_update_2023.RData` (`trim == "inc"`). Its event-window sample counts
  are inflated by 11–13%, but the gate's qualifying sites are unchanged after
  deduplication. Only EOT site 1332 changes, on the biota criterion, and it
  fails the temperature test regardless.
- **Q-012** (heritable susceptibility vs ageing): the exposure build uses the
  same file. Its Jaccard and coverage measures are robust to duplicates. Its
  exposure index (a row-weighted mean |palaeolatitude|) is not. After removing
  duplicates with a recorded depth, the mean changes in 1,454 of 2,267
  lineage-bins (423 by 1° or more), and 8 exposure classes flip. Per-bin site
  counts are inflated because hole IDs are source-scoped. Its palaeolatitudes
  also pool two plate models (Pitfall 4). These are side-session findings,
  not yet passed to the Q-012 owners.
- **Q-005, Q-020, Q-027** name Triton as a candidate input.
- Good for: species-level diversity, ranges, biogeography and thermal-niche
  work across the Cenozoic; assemblage-level analyses where counts exist.
- Not good for: pre-Cenozoic questions; abundance comparisons across unit
  types without recoding; analyses needing per-sample age uncertainty.

## Citation and terms

CC0 on every Figshare item; the paper applies the CC0 waiver to the data.
Cite Fenton et al. (2021) and the Figshare version. The paper asks: "If a
significant fraction of your data subset derives from ForCenS or Neptune, we
ask those papers are also cited". That means Siccha & Kucera (2017) and
Renaudie et al. (2020), plus Lazarus (1994) and Spencer-Cervato (1999).

Licence signals are not fully consistent. The collection's DataCite record
says CC BY 4.0 while every item says CC0. One input, the ForCenS dataset on
PANGAEA (doi:10.1594/PANGAEA.873570), is CC BY-NC-SA 3.0, which sits
awkwardly with CC0 redistribution of its records. Terms of the other PANGAEA
inputs are not stated in Triton's documents. Inside EPRP, treat the data as
CC0 for analysis, and cite the inputs.

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | Figshare API: 11 items, 20 item versions, all CC0, 1.6 GB | checked |
| 2026-10-22 | All 20 item versions mirrored with size and md5 verification | checked |
| 2026-10-22 | Profiles of all eight data tables across v1–v4 ([profile/](profile/)) | checked |
| 2026-10-22 | v4 RData files differ from v3's despite identical names (md5) | checked |
| 2026-10-22 | Duplicates by v1's exact key, split by source and depth; unit relabelling; age grids by method; `age.err`; vocabularies; source-scoped samples ([checks.tsv](profile/checks.tsv)) | checked |
| 2026-10-22 | Cross-source dedup recipe on v4 ([dedup_v4.txt](profile/dedup_v4.txt)) | checked |
| 2026-10-22 | Record-level link of Neptune rows to four NSB snapshots: `orig.age` and `pal.lat` equal NSB's (2018–19) | checked |
| 2026-10-22 | v1-to-2023 drift (Fenton conversion), v3/v4 cell-by-cell, `no_dup` replication, Q-007 and Q-012 reruns with and without duplicates | checked (independent review) |
| 2026-10-22 | Entry reviewed adversarially: 5 major and 11 minor findings, all applied | checked (Claude Sonnet subagent) |
| 2026-10-22 | TSV exports equal the presence tables (row counts) | checked |
| 2026-10-22 | Pipeline, sources, filters, column definitions, `trim` rule, merge rules | source claim (paper, readme, version histories and R code read in full) |
| 2026-10-22 | Neptune export date 14 March 2019 | inferred (deposited sheet name and file date) |
| 2026-10-22 | Variant purposes (full, unrounded) | source claim (readme v2) |
| 2026-10-22 | chronosphere serves v1 and v3; `main` v3 = no_dup; pre-v4 units | checked (live fetch by the ecosystem scan) |
| 2026-10-22 | Uses, critiques, related compilations, licence records | source claim (papers, DataCite and registries read by the ecosystem scan) |
