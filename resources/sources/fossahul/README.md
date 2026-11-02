---
id: fossahul
name: FosSahul, quality-rated fossil ages for Sahul's Late Quaternary vertebrates
kind: compilation
status: "frozen since the March 2021 update (GitHub last commit 2021-11-16)"
last_update: 2021-03
scope:
  taxa: ["non-human vertebrates (mammals, birds, reptiles, amphibians)"]
  time: "Late Quaternary, mostly the last 130 kyr (ages to about 900 ka)"
  space: "Sahul: mainland Australia, Tasmania and other islands, New Guinea"
  record_unit: "one taxon (genus and species) at one site, with one age determination and its quality rating"
size:
  as_of: "FosSahul_updated_March2021.csv (Figshare v3)"
  records: 11872
  distinct_lab_codes_normalised: 1755
  genus_species_strings: 515
  site_names: 600
access:
  tier: open
  licence: "CC0 (Figshare, byte-identical to the GitHub CSV); CC BY 4.0 (FosSahul 1 on TERN); GitHub has no licence file"
  routes:
    - {type: figshare, url: "https://doi.org/10.6084/m9.figshare.8796944 (v1-v3)", state: "v3 (2021-04-12) holds the 2019 and March 2021 CSVs and rating code", checked: 2026-10-22}
    - {type: tern, url: "https://doi.org/10.4227/05/56F077B3054E9 (FosSahul 1)", state: "2016 workbook, 9,302 records, CC BY 4.0", checked: 2026-10-22}
    - {type: github, url: "https://github.com/GlobalEcologyFlinders/FosSahul", state: "same 2021 CSV, byte-identical; last commit 2021-11-16", checked: 2026-10-22}
    - {type: octopus-wfs, url: "be10-denude:fossahul_webmercator_nrand_25000", state: "partner copy, 11,858 records, restructured, blurred to 25 km", checked: 2026-10-22}
  api: "none (files); the OCTOPUS copy via WFS"
versioning:
  replay: exact
  notes: "FosSahul 1 (2016), FosSahul 2.0 (2019), March 2021 update; Figshare versions v1-v3"
mirror:
  path: deep-server:/data/paleodata/fossahul
  policy: "Figshare latest (v3), GitHub latest commit, FosSahul 1 (TERN), and the OCTOPUS copy (snapshot) for comparison"
  state: "complete 2026-10-22"
lineage:
  upstream:
    - "FosSahul 1 (Rodríguez-Rey et al. 2016)"
    - "quality criteria of Rodríguez-Rey et al. (2015)"
    - "published dated fossil records, 1955-2018"
  downstream:
    - "OCTOPUS partner collection"
    - "Sahul megafauna extinction-chronology studies"
eprp_questions: []
citation:
  - "Peters, K. J., Saltré, F., Friedrich, T., Jacobs, Z., Wood, R., McDowell, M., Ulm, S. & Bradshaw, C. J. A. (2019). FosSahul 2.0, an updated database for the Late Quaternary fossil records of Sahul. Scientific Data 6: 272. doi:10.1038/s41597-019-0267-3"
  - "Rodríguez-Rey, M. et al. (2016). A comprehensive database of quality-rated fossil ages for Sahul's Quaternary vertebrates. Scientific Data 3: 160053. doi:10.1038/sdata.2016.53"
  - "the Figshare version used, e.g. doi:10.6084/m9.figshare.8796944.v3"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); papers and deposit read by a Claude Sonnet subagent
  reviewed: "independent adversarial review by a Claude Sonnet subagent, 2026-10-22; findings applied"
---

# FosSahul

## Summary

FosSahul compiles published ages of Late Quaternary non-human vertebrate
fossils from Sahul, each rated for reliability by a fixed set of criteria. The
current release (March 2021, CC0) holds 11,872 records of about 355 species
in 217 genera from about 600 deposits, mostly mammals and centred on
megafauna. Its core contribution is the quality rating: A* and A ages (1,626
records) are the ones extinction-chronology studies use. Reach for it for
megafauna extinction timing, species' last and first appearances in Sahul, and
pairing with [SahulArch](../sahularch/README.md) to compare faunal and human
chronologies. A record is a taxon at a site tied to one age, not an
independent date: one dated layer often supports many taxa.

Barry W. Brook is an author of FosSahul 1 (2016) and of the rating criteria
(2015), not of FosSahul 2.0 or its addendum.

## Contents

Counts are our own ([profile](profile/fossahul_profile_2021.tsv)) from the
March 2021 CSV unless stated.

| Measure | Value |
| --- | ---: |
| Records (rows with data) | 11,872 (+1 stray all-`na` row, excluded throughout) |
| Distinct lab codes (`AgeID`, trimmed, case-folded) | 1,755; 268 rows carry a placeholder (`?`, `Not given`, `na`) |
| Distinct determinations (lab code, age, precision, age type, site, technique; placeholders lumped) | 2,577 (2,508 on lab code × age × site) |
| Genus and species strings / genera | 515 / 219 (217 excluding "indet") |
| Deposit names | 600 |
| Megafauna records (flag "Yes") | 3,196 |
| Quality A* / A / B / C | 228 / 1,398 / 4,182 / 6,064 |
| Publication years | 1955–2018 |

- **Taxa.** Mammals 9,441, birds 1,733, reptiles 593, amphibians 97.
  Extinct 2,497 (2,480 plus 17 spelled "Exinct"), extant 6,060, unknown
  3,035, both 280. Humans are excluded.
- **Dating.**
  - Radiocarbon 7,571: conventional 4,754, AMS 2,611, ABOX 142,
    δ13C-adjusted 53, ABA 11.
  - U-series 1,912, OSL 1,344 (plus TT-OSL 1), TL 2, amino-acid racemisation
    710, ESR 319, stratigraphic correlation 10, not stated 3.
  - Association: indirect 9,941 (the dated material is not the fossil itself),
    direct 1,787.
- **Ages.**
  - Ages are in ka: under 12 ka 3,960; 12–30 ka 3,127; 30–50 ka 1,637; 50–130 ka 1,732; 130–500 ka 1,286;
    500 ka or more 130 (maximum 897 ka, Cuddie Springs ESR).
  - Age type: exact 9,345, minimum (`>`) 1,266, maximum (`<`) 1,157, `<=` 7,
    not stated 97.
- **Regions.** Mainland Australia 8,315, Australian islands 1,792, New Guinea
  1,757. All A*/A records are on the mainland, Tasmania or Kangaroo Island,
  concentrated in South Australia (868) and Western Australia (505).

## Provenance and lineage

- **FosSahul 1** (Rodríguez-Rey et al. 2016): literature to October 2013,
  9,302 records, rated by hand on the criteria of Rodríguez-Rey et al. (2015).
  Deposited on TERN/ÆKOS (CC BY 4.0) as a workbook with precise coordinates
  and a point-radius location uncertainty, "to reduce the chance of
  encouraging undesirable behaviour at palaeontological/archaeological
  sites". Authors: Rodríguez-Rey, Herrando-Pérez, Brook, Saltré, Alroy,
  Beeton, Bird, Cooper, Gillespie, Jacobs, Johnson, Miller, Prideaux, Roberts,
  Turney, Bradshaw.
- **FosSahul 2.0** (Peters et al. 2019): literature to 2018, 11,871 CSV
  rows, and an R algorithm that reproduces the rating automatically. Released
  on Figshare and GitHub (CC0 on Figshare). Coordinates rounded to 0.1°.
  Authors: Peters, Saltré, Friedrich, Jacobs, Wood, McDowell, Ulm, Bradshaw.
- **Addendum and March 2021 update** (Peters et al. 2021, *Sci. Data* 8:
  133). Contamination reports were dropped from the rating, otoliths regrouped
  with shell and coral, pretreatment records corrected, and six ages added
  (IDs 11924–11929). Figshare v3 and GitHub carry
  `FosSahul_updated_March2021.csv`, which also restores FosSahul 1's precise
  coordinates and uncertainty radii.
- **OCTOPUS partner copy** (Codilean et al. 2022): 11,858 records in OCTOPUS's
  schema, blurred to 25 km. The 25 km blurring belongs to OCTOPUS, not to
  FosSahul.

**2019 against March 2021** ([comparison](profile/fossahul_compare.txt),
checked):
- *Records.* The 2019 file has 11,866 populated rows plus 5 empty rows; Peters
  et al.'s "11,871 records" counts the empty rows. The 2021 file adds 6 records
  (IDs 11924–11929) and removes none.
- *Ratings.* 232 changed, all upward from C: 172 to B and 60 to A*. Ages,
  precisions and techniques are unchanged.
- *Coordinates.* Rounding the 2021 coordinates to 0.1° (half away from zero)
  reproduces the 2019 values for all 11,829 records with numeric coordinates.
  The 2021 values equal FosSahul 1's rounded to four decimals (9,222 of
  9,270), except 27 Tea Tree Cave records whose FosSahul 1 position was wrong
  and was corrected in 2019. Uncertainty radii exist for 9,268 of the 9,302
  FosSahul 1 records but only 57 of the 2,570 records added since.
- *Codes and other fields* (independent review): `na` became `?` in Status
  (3,035 rows) and Megafauna (1,175); 7 age types changed from `=` to `<=`;
  contamination and extraction fields changed in 251 rows; the family typo
  "Scindidae" appeared (188 rows); `Uncertainty` was added.

## Structure

One CSV of 62 columns (2021; the 2019 file has 61, raw header names and a
byte-order mark), one row per taxon–site–age record:
- **Identity and taxonomy.** `ID`, `Latitude`, `Longitude`, `Uncertainty`
  (metres, 2021 only), genus to class, `Status`, `Megafauna..40kg.`.
- **The age.** `AgeID` (lab code), material dated, `Age` (ka), `AgeType`
  (`=`, `>`, `<`), `Precision` with `PrecisionType` (1σ or 2σ),
  `DatingTechnique`, `Calibration`.
- **Rating inputs.** Method-specific fields for radiocarbon pretreatment and
  collagen chemistry, AAR, U-series, ESR and luminescence, and `Association`
  (direct or indirect) with its sub-category.
- **Context and source.** Region, deposit, chamber, stratigraphy, abundance
  comments, citation fields.
- **Ratings.** `preQuality` (m*, m, B, C), `Reason`, `Quality` (A*, A, B, C)
  and `QualityReason`.

Missing values are `na` (not available) or `null` (does not apply). Companion
files: calibrated radiocarbon ages (7,580 rows, unchanged since 2019) and time
bins for the biodiversity index.

**The rating** (Peters et al. 2019; code in
`FosSahul_Rating_updated_March2021.R`). Step 1 rates the material and
procedure for each technique: for example, collagen radiocarbon needs
ultrafiltration or an equivalent pretreatment and a C:N ratio between 2 and 4
for the top grade. Ages graded B or C at step 1 keep that grade. Step 2 uses
association: direct ages of the target species become A* or A; indirect ages
become A, B or C by stratigraphic association. Only direct ages can be A*.

## Access

**Mirror.** On `deep-server`:

```text
/data/paleodata/fossahul/figshare/raw/FosSahul-2.0-database-and-R-code_v3_8796944/   2019 and 2021 CSVs, R code, metadata
/data/paleodata/fossahul/github/raw/2021-11-16_0fae5218ea/                           same 2021 CSV, byte-identical
/data/paleodata/fossahul/tern-fs1/raw/2026-10-22T0431Z_url/                          FosSahul 1 workbook (2016)
/data/paleodata/fossahul/octopus-wfs/raw/<stamp>_wfs/                                OCTOPUS copy (blurred)
```

The GitHub CSV is byte-identical to the CC0 Figshare v3 file, which settles
the data licence. Barry, a FosSahul 1 author, authorised mirroring the GitHub
copy on 22 October 2026 ("the intention was public domain, as an update to
FosSahul ... even if the repo License doesn't specify that").

**Rating check.** [rating_check.R](rating_check.R) re-runs the authors' rating
script on their CSV: the 2021 CSV with `FosSahul_Rating_updated_March2021.R`
([result](profile/fossahul_rating_check_2021.txt)) and the 2019 CSV with
`FosSahul_Rating.R` ([result](profile/fossahul_rating_check_2019.txt)).
Crossing them (2019 CSV with the 2021 script) gives 230 disagreements, so name
the script with the result.

## Strengths

- **Transparent, reproducible ratings.** The March 2021 ratings reproduce
  exactly from the published algorithm on all 11,873 rows.
- **Method-aware criteria.** Each technique is judged on what matters for
  it: pretreatment, closed-system behaviour, dose rates, bleaching.
- **Coverage of Sahul's dated fossil record.** Sixty years of literature in
  one table, with the evidence behind every rating kept in columns.
- **Heavily used.** The standard input for Sahul megafauna extinction
  chronologies (Saltré et al. 2016, 2019; Bradshaw et al. 2021).

## Weaknesses and pitfalls

1. **Records are not dates.** About 2,577 determinations sit behind 11,872
   records, and about 330 behind the 1,626 A*/A records (key in Contents;
   2,441–2,786 across plausible keys). One lab code (ANU-1221) supports 170
   records. Deduplicate before date-level statistics.
2. **Use the March 2021 file.** The 2019 CSV disagrees with its own
   algorithm on 61 records (60 ESR ages stored C that the script rates A*),
   and its ratings do not match the published paper's totals. The 2021 file
   matches the script and the paper's 1,626 A*/A. The README and Figshare
   description still describe the 2019 file.
3. **The algorithm screens method, not age.** It applies no radiocarbon age
   limit: 27 radiocarbon ages of 45 ka or more are A*/A. It ignores minimum
   and maximum ages (70 A*/A records carry `>` or `<`). Filter `AgeType`
   yourself.
4. **Mixed uncertainty conventions.** A*/A errors are nearly half 2σ (796)
   and half 1σ (827). Most radiocarbon ages are uncalibrated, 261 are stored
   calibrated, and 66 unknown. The companion calibrated file treats all as
   uncalibrated and does not state its point estimate.
5. **Indirect ages dominate.** 84% of records date associated material, not
   the fossil. Their rating depends on a stratigraphic-association judgement.
6. **Opportunistic for small fauna.** Non-megafauna records were included
   only when published with megafauna dates (Peters et al. 2019): not a
   complete small-vertebrate record.
7. **Data cleaning needed.**
   - *Coordinates.* Three Outer Arumpo Lake records have longitude 14.877
     (should be about 142.9), and 37 records have non-numeric coordinates.
   - *Same name, different site.* "Cathedral Cave" is both Wellington Caves,
     NSW (224 rows, all C; redated by Fusco et al. 2023) and Naracoorte, SA
     (479 rows; 376 A and 3 A*, which carry 379 of the 568 A*/A ages older
     than 120 ka). Filter by region, not name.
   - *Spelling variants.* "Exinct" (17), "Austrlian Islands", and the family
     "Scindidae" (188 rows, new in 2021).
   - *Unknown codes.* Status "?" covers 3,035 rows.
   - *Megafauna flag.* The header says 40 kg, but the paper defines megafauna
     as over 44 kg. Emu (*Dromaius*) supplies 938 "Yes" rows, mostly an
     extant species.
8. **Reliable records are geographically narrow.** A*/A ages come from the
   south and west of the continent. The authors note that reliable records
   older than 120 ka come from three areas: Leeuwin–Naturaliste, Naracoorte
   and Cuddie Springs.
9. **Coordinate precision differs by release.** FosSahul 1 and the 2021 file
   give precise coordinates with an uncertainty radius; the 2019 file rounds to
   0.1°; OCTOPUS blurs to 25 km. The 2,513 records added since FosSahul 1
   mostly lack a radius, so their precision is unstated. Respect the authors'
   caution about site disturbance.

**What the literature says.** Price et al. (2018, *Nature*) criticised
megafauna extinction meta-analyses built on poorly understood dates.
Herrando-Pérez & Stafford (2025) note that reporting gaps push radiocarbon
dates into the lowest categories in curated datasets such as this one: 3,413
records carry "Missing info about pretreatment". Site-specific redating has
since refuted late survival at Cloggs Cave (David et al. 2021) and earlier
dates at Cathedral Cave (Fusco et al. 2023). FosSahul already rated both
sites' dates C.

## Overlap with other sources

- **SahulArch.** 372 normalised radiocarbon lab codes occur in both. 4,233
  FosSahul records (36%) carry one, overwhelmingly indirect charcoal and shell
  ages from archaeological contexts, and 50 deposit names match exactly
  (53 after normalisation). These are the sites where faunal and human
  chronologies meet. A shared code is not proof of the same determination:
  447 of the 4,233 records differ by more than 1% in age from the SahulArch
  row with that code.
- **PBDB.** 2,316 Quaternary tetrapod occurrences in the 22 October extract
  by interval midpoint (2,263 with a maximum age of 2.58 Ma or less), with
  interval ages, not dates; only 9 shared references. Complementary, not
  overlapping: only 78 of PBDB's 414 Quaternary tetrapod collections lie
  within 5 km of a FosSahul site (see the [PBDB entry](../pbdb/README.md)).
- **Neotoma** has no vertebrate datasets for Australia or New Guinea.
- **OCTOPUS** holds a blurred, restructured copy of 11,858 records with the
  March 2021 ratings but without its 6 additions and 8 older records (5 of
  them lacking coordinates).

## EPRP relevance

No register question uses it yet. It is the faunal-chronology input for Sahul
megafauna extinction work, Barry's long-standing field, and pairs with
SahulArch and the palaeoenvironment bundle in the [backlog](../BACKLOG.md).

## Citation and terms

Cite Peters et al. (2019) with the addendum, Rodríguez-Rey et al. (2016) for
FosSahul 1, and the Figshare version used. CC0 on Figshare; CC BY 4.0 on
TERN.

## Verification log

Labels as in the [catalogue conventions](../README.md).

| Date | Check | Label |
| --- | --- | --- |
| 2026-10-22 | Figshare v1–v3 indexed; v3 mirrored (md5 verified); GitHub HEAD mirrored (blob hashes); CSVs byte-identical | checked |
| 2026-10-22 | FosSahul 1 TERN files mirrored (md5 match the documentation scan's) | checked |
| 2026-10-22 | Profiles of the 2019 and 2021 CSVs; 2019-to-2021 comparison; OCTOPUS copy coverage | checked |
| 2026-10-22 | Rating script re-run: 2021 reproduces exactly; 2019 has 61 disagreements | checked |
| 2026-10-22 | (row withdrawn) | checked (documentation scan, from the same files) |
| 2026-10-22 | Lineage, authorship, rating scheme, coordinate treatments, uses and critiques | source claim (FS1, FS2, addendum, OCTOPUS paper) |
| 2026-10-22 | Barry's authorisation of the GitHub copy | checked (side-session chat, 22 Oct 2026) |
| 2026-10-22 | Entry reviewed adversarially (with SahulArch, AustArch, OCTOPUS): findings applied, incl. record and lab-code counts, coordinate lineage, name collisions | checked (Claude Sonnet subagent) |
