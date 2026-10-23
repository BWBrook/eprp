---
id: classic-compendia
name: Classic range compendia — Benton's The Fossil Record 2 (families) and Sepkoski's compendium of fossil marine animal genera
kind: compilation
status: frozen
last_update: "FR2 files 1998 (re-posted 2019-08); Sepkoski 2002 (online port undated; R package head 2026-07-21)"
scope:
  taxa: ["FR2: all life, families and family-surrogates (animals, plants, algae, fungi, bacteria)", "Sepkoski: marine animal genera (26 phyla)"]
  time: "FR2: Hadean to Holocene in 86 divisions (dated from the Vendian, about 610 Ma); Sepkoski: Vendian to Recent"
  space: "global"
  record_unit: "FR2: one family's first and last appearance, coded division by division; Sepkoski: one genus's first and last period and stage"
size:
  as_of: "2026-10-23"
  fr2_family_rows: 7109
  fr2_rows_with_a_range: 7001
  sepkoski_genus_rows: 36372
  raw_files: 451
  mirrored_bytes: 64966051
access:
  tier: unclear
  licence: "none stated for FR2 (Bristol) or Peters' port (use with citation of Sepkoski 2002); the R package is GPL (>= 3); BHL's scan is in copyright, digitised with the Paleontological Research Institution's permission"
  routes:
    - {type: web, url: "https://palaeoresources.blogs.bristol.ac.uk/fr2-downloads/", state: "45 chapter workbooks, FR2.zip and summaries, posted 2019-08-04 to 2019-08-10", checked: 2026-10-23}
    - {type: web-archive, url: "https://web.archive.org/web/*/palaeo.gly.bris.ac.uk/frwhole/*", state: "original Bristol host dead; 1,015 captures 1997-12-24 to 2006-12-05; list in wayback_captures.tsv", checked: 2026-10-23}
    - {type: web, url: "https://strata.geology.wisc.edu/jack/", state: "Peters' online port of Sepkoski (2002): one page per phylum and class", checked: 2026-10-23}
    - {type: r-package, url: "https://github.com/palaeoverse/sepkoski", state: "CRAN 0.0.1 (2022-11-23); GitHub head 2026-07-21 (61 commits, sepkoski-package-versions.tsv)", checked: 2026-10-23}
    - {type: scan, url: "https://archive.org/details/bulletinsofameri363pale", state: "BHL scan of Bulletins of American Paleontology 363 (PDF and OCR text)", checked: 2026-10-23}
  api: none
versioning:
  replay: exact
  notes: "both compendia are frozen. FR2's chapter files are unchanged from the 1998 originals except two angiosperm rows; every Wayback capture is kept. Sepkoski's port matches the R package's 2022 scrape row for row"
mirror:
  path: deep-server:/data/paleodata/classic-compendia
  policy: "every independent copy found, mirrored at Barry's instruction although no licence is stated (see Access)"
  state: "six routes, 451 files (65.0 MB), each with a manifest; all verify. Derived tables in fr2/derived/ and sepkoski/derived/"
lineage:
  upstream:
    - "FR2: Benton (ed.) 1993, The Fossil Record 2 (Chapman & Hall), successor to Harland et al. 1967, The Fossil Record; spreadsheets compiled by Mary Benton"
    - "Sepkoski: Sepkoski 2002, A compendium of fossil marine animal genera (Bulletins of American Paleontology 363); its family-level predecessors, Sepkoski 1982 and 1992 (Milwaukee Public Museum Contributions in Biology and Geology 51 and 83), are not online"
  downstream:
    - "Benton 1995 (Science 268:52-58) and Holman's tallies (Bristol); Benton 1996 tetrapod family analyses"
    - "the Sepkoski curve and evolutionary faunas; Raup and Sepkoski's periodicity; much of PBDB's genus classification (36,832 opinions and 27,556 taxon records cite Sepkoski 2002)"
eprp_questions: [Q-023, Q-039, Q-040, Q-041, Q-042, Q-044, Q-045]
citation:
  - "Benton, M. J. (ed.) 1993. The Fossil Record 2. Chapman & Hall, London, 845 pp."
  - "Benton, M. J. 1995. Diversification and extinction in the history of life. Science 268, 52-58. doi:10.1126/science.7701342"
  - "Sepkoski, J. J., Jr. 2002. A compendium of fossil marine animal genera. Bulletins of American Paleontology 363, 1-560"
  - "Peters, S. E. Sepkoski's Online Genus Database, University of Wisconsin-Madison (acknowledge as the site asks)"
  - "Jones, L. A. sepkoski: Sepkoski's Fossil Marine Animal Genera Compendium (R package). doi:10.32614/CRAN.package.sepkoski"
entry:
  created: 2026-10-23
  updated: 2026-10-23
  by: Claude (Opus 5.5, side session)
  reviewed: pending
---

# Classic range compendia: The Fossil Record 2 and Sepkoski's genera

## Summary

Before occurrence databases, the history of diversity was read from range
compendia: lists of taxa with their first and last appearances. Two of them
anchor most classic results. *The Fossil Record 2* (FR2; Benton, ed., 1993)
gives the range of every family of every kind of organism. Mary Benton
compiled it into spreadsheets, Bristol posted them in the 1990s, and Benton
(1995) drew his diversification and extinction curves from them. Sepkoski's
*Compendium of fossil marine animal genera* (2002) gives about 36,000 marine
genera; it underlies the Sepkoski curve, the three evolutionary faunas, and
Raup and Sepkoski's periodicity.

Both are frozen. We mirrored every independent copy we found and checked
the copies against each other:

- **FR2.** Bristol's 2019 re-posting, and the original 1997–2006 Bristol
  files recovered from the Wayback Machine.
- **Sepkoski.** Peters' online port (Wisconsin), the palaeoverse R package
  (GitHub head and CRAN release), and BHL's scan of the printed volume.

The copies are mostly faithful. Some convenient forms are not:

- **FR2 chapter workbooks: faithful.** 7,107 of their 7,109 rows match the
  1998 originals.
- **`All-Life.xlsx`, the one-file version: wrong.** It shifts 220 rows by a
  column.
- **`Diversitydata95.xlsx`, the 2019 file behind Benton's 1995 curves:
  scrambled.** Use the 1998 table from the Wayback capture instead.
- **Peters' port of Sepkoski: corrupted letters.** 28 genus names have one
  corrupted letter (bit 7 set). It is otherwise complete, and identical to
  the R package's 2022 scrape.
- **The R package's main table: incomplete.** It drops the 558 genera that
  lack a class page.

## Contents

### The Fossil Record 2 (Bristol)

- **Chapter workbooks.** 45 workbooks, one per phylum or class. They hold
  7,109 rows:

  | Kingdom | Rows |
  | --- | ---: |
  | Animalia | 6,541 |
  | Plantae | 389 |
  | Algae | 139 |
  | Fungi | 26 |
  | Monera | 14 |

  - Each row is a family or a family-surrogate: plesions, undivided orders,
    unassigned species and genera.
  - There are 7,059 distinct names; 6,840 end in -idae or -aceae.
  - 51 names are questioned (they contain "?").
  - 15 names repeat on 65 rows, among them "Unnamed", "Uncertain" and
    "Incertae sedis".
- **Columns.** Columns 1–5 are name, kingdom, phylum, other (class, or the
  plant part for angiosperms) and habitat. The habitat code is M marine on
  3,894 rows, T terrestrial 2,534, F freshwater 288 and MF 168, plus
  combinations. Columns 6–91 are the 86 FR2 divisions, Hadean to Holocene.
  Column 92 holds NFR (no fossil record) for 106 angiosperm families.
- **Range codes.** F1 marks the first appearance, 1 presence, and L1 the last
  appearance; a range to the Recent has no L code. ?F, ? and ?L mark
  uncertain parts. F2 and L2 mark the confident end of a range stated to
  lower resolution, and FL a range confined to one division (or, repeated,
  to one of several).
- **Range counts.** 7,001 rows have a range and 2,630 reach the Holocene. By
  Benton's (1995) definitions:
  - **Maximum range:** every coded cell.
  - **Minimum range:** from F1 or F2 to L1 or L2 (or to the Holocene), or a
    single FL. Ranges stated only to an interval longer than a division have
    none.

  6,458 rows have a minimum range. Per-family and per-division tables are in
  `fr2/derived/`.
- **Summaries.**
  - `Diversitydata95.xlsx`: Benton (1995)'s stage table, 78 stages from the
    Vendian.
  - `All-data.xlsx`: Eric Holman's tallies of phyla, classes, orders and
    families over 79 intervals.
  - The five pages of Benton's (1996) tetrapod families, with geography,
    size, diet and habitat. These are HTML tables of 857 rows in all, kept in
    `wp_pages.json`; Benton counts 840 non-singleton families.
  - `Birds.xlsx`: Fountaine et al.'s (2005) 124 Mesozoic bird species.
- **Bundled files.**
  - `All-Life.xlsx`: one-file version of the chapters (not to be used; see
    pitfalls).
  - `FR2.zip`: the 45 chapters, plus `Basal.xlsx`, which combines chapters
    1–3 and is not on the downloads page.

### The Fossil Record 2 (Wayback Machine, 1997–2006)

The original host, `palaeo.gly.bris.ac.uk/frwhole`, now times out. The Wayback
Machine holds 1,015 captures of 65 URLs; we mirrored the 204 distinct
payloads. They cover four kinds of file:

- **Chapter files (1998–2005).** Every chapter, 45 in all, as BinHex-encoded
  Mac files. Decoded, they are tab-delimited Excel text exports (type
  TEXT/XCEL, Mac Roman). Five of the 2000 captures are BinHex wrapped inside
  BinHex. [binhex4.py](binhex4.py) decodes them and checks every CRC, without
  dependencies.
- **Spreadsheets and archives.** Four 2004 `.xls` files (Monera, Fungi,
  Algae, basal), and two StuffIt archives of the chapters, which we did not
  unpack.
- **Stage table (1998).** `FR2.data95` is the 1998 stage table behind Benton
  (1995), with all 42 value columns. Four captures, from February 1998 to
  December 2000, hold identical values. From June 2001 three values are
  rounded (for example, 0.091075 to 0.09108); nothing else changed.
- **Holman's tallies (1998).** `FR2.families`, `.orders`, `.classes` and
  `.phyla`, with the introduction and chapter pages.

### Sepkoski's compendium

- **Peters' port.** Shanan Peters' port of the compendium at Wisconsin is
  complete:
  - **Pages.** The start page, plus one page per phylum (26) and per class
    (96).
  - **Rows.** The phylum pages list 36,372 genus rows, the class pages 35,813.
    Every page's row count agrees with its heading and the start page.
  - **Fields.** Each row gives order, genus, and the first and last period
    and stage.
  - **Simplifications.** As the site states, the port omits Sepkoski's "+"
    designations and references, and ignores question marks on first and
    last appearances.
  - **Class.** We recover class by matching class-page rows to phylum-page
    rows on all six fields. 559 genera have no class page (200 of them in
    Problematica, 142 in Mollusca), and Myriapoda spans two phyla.
- **Derived table and counts.** The derived table
  (`sepkoski/derived/.../sepkoski_genera.csv`) has 36,197 distinct names:
  - 144 names repeat on 319 rows.
  - 1,534 genera have order "uncertain" or "incertae sedis".
  - 5,232 genera are extant (last period R).
  - 15,824 are confined to one interval.
  - The stage codes number 262, with 661 first and 546 last stages given as
    "?".
- **R package (palaeoverse `sepkoski`, Lewis A. Jones).** It holds:
  - the 2022 scrape of the same pages (`inst/extdata`);
  - `sepkoski_raw`: the scrape joined into genus rows;
  - `sepkoski`: genus ranges mapped to GTS stages with ages, and Sepkoski's
    evolutionary fauna for each genus (Paleozoic 14,190, Modern 11,316,
    Cambrian 3,324, none 6,996);
  - the interval table: 302 rows.

  We mirror the GitHub head (2026-07-21) and the CRAN release 0.0.1.
- **BHL scan.** The printed volume as a 42.8 MB text PDF and its OCR text,
  from the Internet Archive.

## Provenance and lineage

- **FR2.** Benton (ed.) 1993 updated Harland et al.'s (1967) *The Fossil
  Record*. Mary Benton compiled the family ranges in Excel, and Bristol
  posted them as BinHex files from late 1997 (first capture 1997-12-24). The
  site moved to a University of Bristol WordPress blog in August 2019, when
  the chapters were re-posted as `.xlsx` (media dated 2019-08-04). Benton
  (1995) and Holman's tallies derive from the spreadsheets. A biography
  describes the compilation as a forerunner of PBDB (source claim, Cambridge
  core-reader biography).
- **Sepkoski.** Sepkoski compiled genus ranges until his death in 1999, and
  the 2002 volume was published after it (recall: edited by D. Jablonski and
  M. Foote, with a CD-ROM). Peters ported it to the web (date not stated).
  Jones scraped Peters' pages for the R package in 2022.
- **Family predecessors.** Sepkoski's family compendia of 1982 and 1992 were
  distributed on paper and, by one library record seen in a search, on
  diskette (not verified). We found no digital copy: the
  NASA technical report record of the 1992 edition (NTRS 20040120307) has no
  file, and the Internet Archive has neither edition. Stanley (2016), cited in
  Q-042, used them.
- **PBDB.** PBDB took much of its genus classification from Sepkoski
  (checked in our PBDB snapshot):
  - Reference 6930 (Sepkoski 2002) is cited by 36,832 opinions and 27,556
    taxon records.
  - Reference 26158 (Benton 1993) is cited by 99 opinions.

  PBDB and Sepkoski are therefore not independent at the level of names and
  classification.

## Structure

```
classic-compendia/
  fr2/bristol/raw/2026-10-23T0505Z_url/       52 files: 45 chapters, All-Life, FR2.zip, 3 summaries, WordPress page and media JSON
  fr2/wayback/raw/2026-10-23T0507Z_url/       204 files named <capture timestamp>__<original name>
  fr2/derived/2026-10-23T0505Z_url/           fr2_families.csv, fr2_divisions.csv, fr2_stage_counts.csv, fr2_vs_pbdb.csv
  sepkoski/peters/raw/2026-10-23T0520Z_url/   125 HTML pages (index, start, explain, phylum_<id>, class_<id>)
  sepkoski/r-package-github/raw/2026-07-21_3d0c62507e/   63 files at the GitHub head
  sepkoski/r-package-cran/raw/2026-10-23T0536Z_url/      sepkoski_0.0.1.tar.gz
  sepkoski/bhl-scan/raw/2026-10-23T0536Z_url/            PDF, OCR text, Internet Archive metadata
  sepkoski/derived/2026-10-23T0520Z_url/      sepkoski_genera.csv, sepkoski_vs_pbdb.csv
```

`fr2_divisions.csv` dates the FR2 divisions from the Vendian on, using the
Harland et al. (1990) durations and midpoints in the 1998 table. The stages
match the workbook columns one for one; the 1998 table abbreviates four
names (`SERPUKHOV.`, `PLIENSBACH.`, `KIMMERIDG.`, `MAASTRICHT.`).

## Access

- **Terms.** No licence is stated for the Bristol files. Peters' site says
  "You are welcome to use these data with proper citation of Sepkoski's
  work. It would also be appropriate to acknowledge this online database and
  its creator/maintainer." The R package is GPL (>= 3); its authors' right
  to license Sepkoski's data is not discussed. The BHL scan is "In copyright.
  Digitized with the permission of the Paleontological Research
  Institution."
- **Why mirrored.** By the catalogue's tier rules an `unclear` source is not
  mirrored. Barry approved this mirror in chat on 23 October 2026: "Approved
  to mirror both on `deep-server` irrespective of lack of stated licence.
  We're not making this public, although we might publish a public registry
  at some point, but that would point everything back to original
  locations."
- **Rebuild.** Copies of the tools are on deep-server, under
  `/data/paleodata/_tools/` and `_tools/classic-compendia/`.

  ```sh
  # list the Wayback captures (a CDX query), then mirror (routes: bristol wayback peters github cran bhl)
  python3 wayback_captures.py wayback_captures.tsv
  classic_compendia_snapshot.sh wayback_captures.tsv [ROUTE ...]
  # profiles (uv on deep-server, in a login shell); $P = /data/paleodata/classic-compendia
  uv run fr2_profile.py $P/fr2/bristol/raw/2026-10-23T0505Z_url $P/fr2/wayback/raw/2026-10-23T0507Z_url \
      $P/fr2/derived/2026-10-23T0505Z_url profile/fr2_profile.tsv
  uv run sepkoski_profile.py $P/sepkoski/peters/raw/2026-10-23T0520Z_url $P/sepkoski/r-package-github/raw/2026-07-21_3d0c62507e \
      $P/sepkoski/r-package-cran/raw/2026-10-23T0536Z_url $P/sepkoski/bhl-scan/raw/2026-10-23T0536Z_url \
      $P/sepkoski/derived/2026-10-23T0520Z_url profile/sepkoski_profile.tsv
  uv run compendia_vs_pbdb.py $P/fr2/derived/2026-10-23T0505Z_url $P/sepkoski/derived/2026-10-23T0520Z_url \
      $P/sepkoski/r-package-github/raw/2026-07-21_3d0c62507e/data/sepkoski.rda \
      /data/paleodata/pbdb/global/raw/2026-10-23T0329Z_url profile/compendia_vs_pbdb.tsv
  ```

  The PBDB comparison reads the 1.78 million public occurrences and takes
  about 2 min. The snapshot pauses 1–2 s between requests, because Bristol,
  the Wayback Machine and Wisconsin are small or rate-limited services.

## Strengths

- **Complete, citable, frozen.** Each is a complete expert compilation in a
  fixed state, the basis of a large body of published work. FR2 is the only
  whole-of-life, family-level range list; nothing in PBDB replaces it.
- **Exact replay.** We hold FR2's original 1998 files as well as the 2019
  re-posting, and can show where they agree.
- **Primary source for Sepkoski.** The printed text is in the mirror (OCR finds
  36,106 of 36,153 plain genus names), so the port's simplifications ("+",
  "?", references) can be recovered from the volume when needed.

## Weaknesses and pitfalls

- **Do not use `All-Life.xlsx`.** It follows the chapters row for row, but
  220 rows are shifted one column left:
  - **Ranges one division too old:** 112 families, among them Helicoplacidae
    and Erniettidae.
  - **Range shifted and habitat in the wrong column:** 2 more, whose habitat
    lands in column 4.
  - **NFR in the Holocene column:** 106 angiosperm families. A parser would
    read them as Holocene presences.

  The 1998 originals agree with the chapter workbooks for all 220. The
  shifted rows are blocks in chapters 6, 25, 26, 28, 29, 43, 44 and 45.
- **Do not use `Diversitydata95.xlsx`.** Its header promises 42 columns in
  seven labelled blocks, but it holds 38 values per stage:
  - **Missing blocks.** The log-diversity and origination blocks are
    missing.
  - **Scrambled columns.** The first 20 columns hold the 1998 family and
    extinction columns in a scrambled order: xlsx column 1 is 1998 column
    19, column 2 is column 1. Eight columns match no 1998 column at most
    stages.
  - **Swapped pairs.** In the percent-extinction and rate blocks the min/max
    pairs are swapped.

  The 1998 table (`fr2/wayback/.../19980212044602__FR2.data95.html`) is the
  record of Benton (1995). Its own labels are inconsistent: the column
  labelled "min" exceeds "max" for all organisms at 42 of 78 stages, and for
  marine at 19 (never for continental).
- **Benton's counts can't be rebuilt exactly.** Recounted from the chapters
  by the stated rules (marine: habitat containing M; continental: F, T or V):
  - **Continental:** the recount falls inside Benton's 1998 min–max pair at
    all 78 stages.
  - **All organisms and marine:** the recounted minimum runs 10% and 6% above
    the smaller 1998 value (medians).

  Benton evidently excluded rows that the pages do not describe (inferred).
  Holman's tallies also count orders, which the chapter files lack, so he
  worked from fuller data: a recount under his stated rules misses his
  family counts by 86 a stage on average. His tallies are identical in the
  1998 HTML and the 2019 workbook (79 of 79 intervals).
- **"Angiosperms 2" is missing.** Bristol describes two angiosperm files:
  one from macroplant records, one adding palynomorph ages from Muller.
  Chapter 45 is the first (column 4 holds the plant part). We found no
  second file in the 2019 posting or among the individually captured 1997–2006
  files. The two StuffIt archives, not unpacked, might hold it.
- **Coding errors in the chapter files** (all present in 1998 too):
  - **Codes outside the key:** 3 (`)`, and `1L1` twice).
  - **Stray "1" in column 92:** 10 rows, in pairs four rows apart in chapters
    10, 16, 21 and 38.
  - **Gaps inside a range:** 7 families.
  - **More than one F1/F2:** 11; **more than one L1/L2:** 3.
  - **Neither a range nor NFR:** 2 angiosperms (Heliconiaceae, Paeoniaceae).

  The full list is in the profile.
- **Changes since 1999.** Two angiosperm rows changed between the October
  1999 capture and 2019 (Orchidaceae and Vitaceae). Nothing else changed.
- **Sepkoski genus names with a corrupted letter.** 28 names in Peters' port
  have one letter with bit 7 set:

  | Captured | With bit 7 cleared |
  | --- | --- |
  | `Còyptoporocyathus` | *Cryptoporocyathus* |
  | `Såkwia` | *Sekwia* |
  | `Holocùsôió` | *Holocystis* |

  - **Clearing the bit recovers the names.** 23 of the 28 cleared names are
    accepted PBDB genera; none are as captured. The other five
    (*Hexaheliocoenia*, *Hydnophorarea*, *Isastraea*, *Jyxiella*,
    *Kangilacyathus*) are not PBDB genus names, perhaps through spelling.
  - **The R package keeps the corrupted spellings.**
  - **The OCR finds only some.** It finds 13 of the 28 cleared names, and 1
    as captured.
- **Sepkoski's 'Maes'.** The port spells Maastrichtian "Maes" in 1,765
  stage codes; the R package replaces it with "Maas".
- **The package's `sepkoski_raw` and `sepkoski` lack 559 genera.** They join
  class pages to phylum pages with an inner join, which:
  - drops 558 genera without a class page (and one more);
  - adds 13 duplicate rows where identical rows repeat.

  Its time-scale update to GTS 2023, listed in NEWS, changes no age: the
  GitHub head's ages equal CRAN 0.0.1's for all 35,826 rows. Use the
  capture-derived table for counts.
- **Port simplifications.** Peters' port drops Sepkoski's "+" designations,
  his question marks on first and last appearances, and his references
  (source claim, site); the scan holds them.
- **Family compendia unavailable.** Sepkoski's family compendia (1982, 1992)
  are not online.

## Overlap with other sources

**PBDB public snapshot, 23 October 2026** (checked;
[profile](profile/compendia_vs_pbdb.tsv)).

- **Names.**
  - **Sepkoski.** Of 36,372 captured genus rows:
    - 31,984 are accepted PBDB genus names.
    - 1,721 are subjective synonyms, 129 replaced names and 73 objective
      synonyms.
    - 23 are nomina nuda, vana, dubia or oblita.
    - 2,442 are not PBDB names.
  - **FR2.** Of 7,109 family rows:
    - 5,603 are accepted PBDB family names.
    - 228 are synonyms or invalid subgroups.
    - 1,278 are not PBDB names (among them surrogates such as "Unnamed").
- **Ranges.** First and last appearances from public PBDB occurrences, with
  junior synonyms looked up under their senior name. PBDB occurrences are
  dated by interval bounds and the time scales differ, so "within 5 Myr"
  counts as agreement.
  - **Sepkoski** (package ages; 35,517 genera with unique names). 11,245
    have no public PBDB occurrences.

    | Sepkoski genera | Within 5 Myr | PBDB older | PBDB younger | Median, PBDB minus Sepkoski |
    | --- | ---: | ---: | ---: | ---: |
    | First appearance (24,272) | 10,565 | 8,216 | 5,491 | 0.0 Myr |
    | Last appearance (20,643 extinct) | 9,337 | 3,752 | 7,554 | −0.6 Myr |

  - **FR2** (maximum ranges, Harland 1990 ages; 6,712 non-angiosperm
    families with unique names from the Vendian). 1,611 have no public
    occurrences.

    | FR2 families | Within 5 Myr | PBDB older | PBDB younger | Median, PBDB minus FR2 |
    | --- | ---: | ---: | ---: | ---: |
    | First appearance (5,101) | 1,248 | 2,297 | 1,556 | +2.8 Myr |
    | Last appearance (3,185 extinct) | 870 | 995 | 1,320 | −1.6 Myr |

    Thirty years on, PBDB often extends a family's range further back than
    FR2, though coarse occurrence dating inflates "older" too (inferred).

  Per-genus and per-family tables are in the derived directories.
- **Other entries.** FosSahul, PBDB (AU+NG) and the Australian deposits
  reach these families and genera only through names; there is no
  record-level overlap.

## EPRP relevance

- **Q-039 (evolutionary faunas).** The package assigns each genus to
  Sepkoski's Cambrian, Paleozoic or Modern fauna; the capture adds the 559
  genera the package drops.
- **Q-040 (did marine diversity rise?).** Sepkoski's curve is the classic
  baseline against PBDB.
- **Q-041 (periodicity).** The register asks for "the Sepkoski compendium as
  a second series". Benton (1995), which found "no support" for
  periodicity, is reproducible from the 1998 table.
- **Q-042 (species loss).** Stanley (2016) worked from Sepkoski's genus and
  family compendia; the genus compendium is here, the family compendia are
  not.
- **Q-023 (origination failures).** Its prior work uses Sepkoski genera.
- **Q-044 (terrestrial diversity, inferred).** FR2 gives the only
  family-level continental series.
- **Q-045 (data vintage, inferred).** Three vintages can be set side by
  side: FR2 (frozen 1993/1998), Sepkoski (2002) and the 2026 PBDB snapshot,
  with the range shifts between them measured above.

## Citation and terms

- **FR2.** Cite Benton (ed.) 1993 and, for the stage table, Benton 1995
  (doi:10.1126/science.7701342). For Holman's tallies, acknowledge Eric
  Holman (UCLA), as Bristol does.
- **Sepkoski.** Cite Sepkoski 2002, acknowledge Peters' online database,
  and cite the R package when it is used
  (doi:10.32614/CRAN.package.sepkoski).
- **Terms.** No redistribution: see Access.

## Verification log

- 2026-10-23, checked: six routes mirrored with
  [classic_compendia_snapshot.sh](classic_compendia_snapshot.sh) (commits
  c98b594 and 32d42fe; the CRAN and BHL legs were rerun after an argument
  fix). All 451 files re-verify, and the BHL PDF and OCR text match the
  Internet Archive's MD5s. Indexes: [snapshots.tsv](snapshots.tsv),
  [wayback_captures.tsv](wayback_captures.tsv) and
  [sepkoski-package-versions.tsv](sepkoski-package-versions.tsv).
- 2026-10-23, checked: [fr2_profile.py](fr2_profile.py)
  ([output](profile/fr2_profile.tsv)),
  [sepkoski_profile.py](sepkoski_profile.py)
  ([output](profile/sepkoski_profile.tsv)) and
  [compendia_vs_pbdb.py](compendia_vs_pbdb.py)
  ([output](profile/compendia_vs_pbdb.tsv)), run on deep-server against the
  mirror. [binhex4.py](binhex4.py) matches Python 3.10's `binhex` on a 1998
  chapter file.
- 2026-10-23, source claim: Bristol's and Peters' descriptions of their data
  (pages mirrored); the dates of the WordPress pages and media; the NTRS
  record of the 1992 family compendium.
- 2026-10-23, recall: the editors and CD-ROM of the posthumous 2002 volume.
