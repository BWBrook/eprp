---
id: fossil-checklists
name: Australasian fossil species checklists (AAP National Fossil Species Lists; Alcheringa annotated checklists)
kind: compilation
status: active
last_update: "2026-06"
scope:
  taxa: ["mammals, birds, reptiles and amphibians, Mesozoic tetrapods, trilobites, echinoderms, archaeocyaths, microbialites, Triassic dinocysts"]
  time: "Cambrian to Holocene, by list"
  space: "Australia (mammal list also New Guinea; Jackson et al. also New Zealand and eastern Indonesia)"
  record_unit: "accepted species with authority and synonyms (AAP lists); taxon occurrence by rock unit with age and references (Poropat et al. 2023)"
size:
  as_of: "2026-10-22"
  mirrored_occurrence_rows: 299
  mirrored_appendix_tables: 12
  aap_lists_documented: 9
access:
  tier: open
  licence: "mirrored: Poropat et al. 2023, CC BY 4.0. Not mirrored: the AAP lists have no licence stated (unclear; treat as all rights reserved), Worthy and Nguyen 2020 is CC BY-NC-ND 4.0, Jackson et al. 2024 and Jell and Cook 2025 are closed access. The tier describes what we hold"
  routes:
    - {type: web, url: "https://www.australasianpalaeontologists.com/national-fossil-species-lists", state: "nine PDFs; the cited .org domain is dead", checked: 2026-10-22}
    - {type: journal, url: "https://doi.org/10.1080/03115518.2023.2228367", state: "Poropat et al. 2023, open access, CC BY 4.0; mirrored; corrected in 2025 (doi:10.1080/03115518.2025.2508434)", checked: 2026-10-22}
    - {type: journal, url: "https://doi.org/10.1080/03115518.2024.2434062", state: "Jackson et al. 2024; closed access; documented only", checked: 2026-10-22}
    - {type: journal, url: "https://doi.org/10.1080/03115518.2025.2457423", state: "Jell and Cook 2025; closed access; documented only", checked: 2026-10-22}
    - {type: journal, url: "https://doi.org/10.1080/03721426.2020.1756560", state: "Worthy and Nguyen 2020, CC BY-NC-ND; the publisher served a bot check to scripted requests; not mirrored", checked: 2026-10-22}
  api: none
versioning:
  replay: partial
  notes: "AAP lists are replaced in place (dated inside each PDF); journal checklists are fixed, with published corrections"
mirror:
  path: deep-server:/data/paleodata/fossil-checklists
  policy: "openly licensed checklists only; AAP lists documented until a licence is stated"
  state: "poropat2023 (PDF in raw/; the appendix tables extracted to derived/2026-10-22T0900Z_url/)"
lineage:
  upstream:
    - "Australasian Palaeontologists (AAP) National Fossil Species Lists: one committee of specialists per list"
    - "Alcheringa annotated checklists (Poropat et al. 2023, which calls itself the inaugural article; Jackson et al. 2024; Jell and Cook 2025)"
    - "Worthy and Nguyen (2020), Transactions of the Royal Society of South Australia, the fossil bird checklist behind the AAP bird list (source claim)"
  downstream:
    - "candidate comparators for PBDB's Australian taxonomy"
eprp_questions: []
citation:
  - "Poropat, S. F., Bell, P. R., Hart, L. J., Salisbury, S. W. & Kear, B. P. (2023). An annotated checklist of Australian Mesozoic tetrapods. Alcheringa 47: 129-205. doi:10.1080/03115518.2023.2228367 (correction: doi:10.1080/03115518.2025.2508434)"
  - "Jackson et al. (2024). An annotated checklist of Australasian fossil mammals. Alcheringa 48: 548-746. doi:10.1080/03115518.2024.2434062 (authors, title, pages and DOI are from the source scan, not checked: closed access)"
  - "each AAP list by its compilers and date, as given in its How to cite line"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent; review fixes by a Claude Sonnet 5.5 subagent
  reviewed: "independent adversarial review, 2026-10-22 (Claude Sonnet 5.5 subagent); findings F1-F5 applied, not re-reviewed"
---

# Australasian fossil species checklists

## Summary

Expert-curated lists of Australian fossil species, maintained by the
Australasian Palaeontologists (AAP) as nine "National Fossil Species Lists"
and, since 2023, extended by annotated checklists in Alcheringa. They are the
authority against which a fossil occurrence database's names can be checked:
which species are valid, under which name, and what synonyms they absorb.
None is a database: the AAP lists are name lists in PDFs with no licence, and
of the Alcheringa checklists only Poropat et al.'s Mesozoic tetrapods (2023)
is open. We mirror that paper and extract its occurrence tables (taxon, rock
unit, age, references); the rest are documented. Against PBDB, 89 of
Poropat's 90 species names are present once spelling variants are allowed and
the age window reaches the late Permian; the extraction and the comparison
are committed code.

## Contents

**AAP National Fossil Species Lists.** Dates, compilers, species counts and
PBDB shares are source claims from the scan (a Claude Sonnet subagent), not
checked here; the counts are the scan's approximate parse, and "in PBDB" is
the share of those binomials it found in PBDB's taxonomy. The scan's matching
rule was not saved; our test on Poropat's names (below) shows that exact-string
matching misses spelling variants.

| List | Compilers | Date | Species (approx.) | In PBDB |
| --- | --- | --- | ---: | ---: |
| Fossil mammals, Australia and New Guinea | Travouillon et al. | 16 June 2026 | 462 | 64% |
| Fossil birds, Australia | Worthy, Nguyen, Travouillon | June 2026 | 96 | 96% |
| Reptiles and amphibians | Thorn et al. | 17 November 2021 | 169 | 85% |
| Trilobites | Jell et al. | 27 January 2023 | 895 | 36% |
| Echinoderms (except echinoids) | Jell | 27 January 2023 | 299 | 53% |
| Echinoids | McNamara et al. | 25 January 2023 | 161 | 17% |
| Archaeocyaths and allies | Kruse | 16 November 2023 | 217 | 18% |
| Microbialites | Grey and Allen | 27 November 2020 | 69 | 12% |
| Triassic dinoflagellate cysts | Mantle | 25 January 2023 | 32 | 19% |

Each is a classified list of accepted names with authorities and synonyms; no
ages, localities or references (source claim). Poropat et al.'s reference list
cites the mammal, bird and reptile-and-amphibian lists as Travouillon et al.
(2021), Worthy, Nguyen and Travouillon (2021) and Thorn et al. (2021)
(checked), which agrees with the compilers above.

**Alcheringa checklists and related papers:**

- *Poropat et al. (2023), Australian Mesozoic tetrapods*, CC BY 4.0, mirrored.
  Its twelve appendix tables list occurrences by rock unit with age range and
  references; our extraction ([poropat_tables.py](poropat_tables.py);
  [table](profile/poropat2023_appendix_tables.tsv)) has 299 rows (checked):
  temnospondyls 49, parareptiles and basal neodiapsids 2, ichthyosauromorphs
  12, lepidosaurs 6, sauropterygians 41, turtles 16, non-archosaurian
  archosauromorphs 4, crocodylomorphs 5, pterosaurs 12, dinosaurs (with birds)
  75, synapsids (with mammals) 16 and ichnofossils 61, across 55 rock-unit
  strings (50 after normalisation: case, upper/lower/middle, bracketed parent
  units, and trailing rank and lithology words folded). It expands on the
  AAP reptile and amphibian list (Thorn et al. 2021), by its own account.
- *Jackson et al. (2024), Australasian fossil mammals*: 482 taxa (406
  Australian), with type material, type locality, unit and age; closed
  access, no data supplement (source claim; the scan could not read the
  paper).
- *Jell and Cook (2025), Australian Mesozoic marine macroinvertebrates*: over
  900 taxa; closed (source claim).
- *Worthy and Nguyen (2020), An annotated checklist of the fossil birds of
  Australia*, Transactions of the Royal Society of South Australia 144: 66-108
  (checked, from Poropat et al.'s reference list; the journal is not
  Alcheringa). CC BY-NC-ND 4.0 and the source of the AAP bird list's content
  (source claim); the publisher blocks scripted downloads.

## Provenance and lineage

The AAP lists are compiled by committees of specialists and replaced in place
on the association's site. Poropat et al. (2023) calls itself the inaugural
contribution to a series of reference articles in Alcheringa for the
Australian Fossil National Species List, to run alongside a continuously
updated open-access online framework (checked: stated in the mirrored paper);
no online framework was found (source scan). Jackson et al. (2024) and Jell
and Cook (2025) are later items in the same effort (source claim: closed
access). Poropat et al. was published online on 12 September 2023 and
corrected in 2025 (doi:10.1080/03115518.2025.2508434); the mirrored PDF
carries the correction notice, so it is the corrected version (checked).

## Structure

AAP lists: indented PDF text (higher taxa, accepted names with authority,
synonyms marked "•" or "="), parseable by indentation (source claim).
Poropat tables: four columns (taxon, rock unit, age range, reference), with
ages as stage names, not numbers (Table A12 heads its age column
"Chronostratigraphic Range"). The PDF has no table structure, so
[poropat_tables.py](poropat_tables.py) assigns words to columns by position,
starts a row when a line has both a taxon and a rock unit, and appends other
lines to the row above, including a row split across a page break. It maps
the font's separate accent glyphs (read by pdfplumber as `(cid:2)`, grave, and
`(cid:3)`, acute) back to letters and its "¼" to "=".

## Access

- **AAP.** `https://www.australasianpalaeontologists.com/national-fossil-species-lists`
  (PDF links at `/s/<name>.pdf`). Each PDF's "How to cite" line still names
  the old `.org/databases` address, which no longer resolves; Poropat et al.
  cite it too.
- **Mirror.** `deep-server:/data/paleodata/fossil-checklists/poropat2023/`:
  `raw/2026-10-22T0900Z_url/` (the PDF, fetched on the laptop with
  `data_mirror.py url` because the publisher refused requests from
  deep-server) and `derived/2026-10-22T0900Z_url/` (the extracted tables).
  Index: [snapshots.tsv](snapshots.tsv).
- **Rebuild.** On deep-server, with `$RAW` and `$DER` the `raw/` and
  `derived/` version directories above and `$P` = `/data/paleodata`; both
  scripts need `pdftotext`, and the outputs are in [profile/](profile/):

  ```sh
  PDF=$RAW/poropat2023_mesozoic_tetrapods.pdf
  uv run poropat_tables.py $PDF $DER/poropat2023_appendix_tables.tsv profile/poropat_tables_check.tsv
  python3 poropat_overlap.py $PDF $DER/poropat2023_appendix_tables.tsv \
      $P/pbdb/au-ng/derived/2026-10-23T0329Z_url $P/pbdb/intervals/raw/2026-10-22T0611Z_url/intervals.csv \
      $P/asud/raw/2026-10-22T0604Z_wfs/StratigraphicUnit.csv profile/poropat_overlap.tsv
  ```

## Strengths

- Expert, current names and synonymy for Australian fossil vertebrates and
  several invertebrate groups, updated as recently as June 2026 (source
  claim).
- Poropat et al. gives an occurrence-level, referenced inventory of every
  Australian Mesozoic tetrapod, under an open licence.

## Weaknesses and pitfalls

- **No licence on the AAP lists**, so we cannot redistribute them or tables
  derived from them; the old domain cited in every PDF is dead. The
  access tier above describes only what we hold.
- **Name lists, not data.** The AAP lists have no ages or localities.
- **Closed checklists.** The richest lists (mammals, marine
  macroinvertebrates) are paywalled with no data supplements.
- **Extraction.** The Poropat table is parsed from PDF layout. The script
  asserts that no cell holds a `(cid:` placeholder or is empty, that brackets
  balance, and that every text segment of every appendix line (headers,
  captions and "(continued)" markers aside) occurs in a cell of its table and
  that the non-space characters match; the run passes
  ([profile/poropat_tables_check.tsv](profile/poropat_tables_check.tsv)). The
  first version failed these checks: a row's reference lost its tail at a
  page break (*Diamantinasaurus matildae*, A10) and three cells kept `(cid:N)`
  placeholders. Cell contents are not otherwise compared against the page
  images here.
- **Errors printed in the appendix, kept as printed.** Table A5 omits the
  closing bracket after *Elasmosauridae incertae sedis* ('Plesiosaurus'
  macrospondylus (page image checked); the *Eiectus longmani* reference
  prints "Goméz-Pérez" (acute accent on the e); the first A9 row (*Pterosauria*
  indet., Eumeralla Formation) has a reference ending in a comma (page images
  checked). Two species names are misspelt in the appendix against the paper's
  own text: *Cratochelone byrnei* (the text uses *berneyi* eight times, the
  appendix *byrnei* once) and *Eomurunna yurrgensis* (the systematic section
  uses *Eomurruna* five times; *Eomurunna* appears in a table on PDF p. 4, a
  figure caption and Table A2). Match names to other sources with spelling
  variants allowed.
- **Names and ages differ from PBDB's in places.** PBDB spells *Minmi
  paravertebrata* where the paper writes *paravertebra* (eight times in the
  text, once in the appendix); PBDB dates *Trucheosaurus major* to the
  Wuchiapingian (259.9-254.1 Ma) where Poropat gives the uppermost Permian.
- **Rock-unit names follow the paper, not ASUD** (below).

## Overlap with other sources

All figures in this section are checked
([poropat_overlap.py](poropat_overlap.py);
[output](profile/poropat_overlap.tsv)) unless marked otherwise.

- **PBDB, taxa.** Poropat's body-fossil tables (A1-A11, 238 rows) name 90
  distinct binomials. Names are compared with those of Australian non-fish
  chordate occurrences in PBDB's Australia and New Guinea region (public
  records, cut from the 2026-10-23 global snapshot; see the pbdb entry), by
  interval midpoint:
  - exact, midpoint 66-256 Ma (760 occurrences, the original window): 85;
  - exact, window widened to the base of the Wuchiapingian, 259.9 Ma (763
    occurrences; Mesozoic plus Lopingian): 86, adding *Trucheosaurus major*,
    one occurrence at 259.9-254.1 Ma whose midpoint fell just above the old
    cut;
  - plus spelling variants (same genus and an epithet within two edits, or
    a genus within two edits): 89. The three are *Cratochelone byrnei*
    (PBDB: *C. berneyi*, one occurrence, 106.3-100.5 Ma), *Eomurunna
    yurrgensis* (PBDB: *Eomurruna yurrgensis*, two occurrences, 251.9-250.8
    Ma) and *Minmi paravertebra* (PBDB: *M. paravertebrata*, one occurrence,
    132.6-119.6 Ma);
  - absent: *Eiectus longmani*, with no exact or variant name anywhere in the
    region (10,659 distinct binomials across all taxa, ages and
    occurrence and taxon tables). The earlier account, that four of the five
    "absent" names were species described in 2021-2023, was wrong: only
    *Eiectus* is recent and absent.
  - Genera: the 90 binomials have 86 distinct genera; 84 are in PBDB in the
    wide window, 85 with *Eomurruna*. The older "144 genera, 119 in PBDB"
    counted the first word of every taxon cell, which includes higher taxa
    from "indet." rows (144 first words, 126 matching a PBDB name of any rank).
- **PBDB, rock units.** Poropat's 55 unit strings reduce to 50. A formation
  column on non-fish chordates alone matches 28 of the 50 (29 in the wide
  window), which understates coverage. Adding member and group names gives
  38 in the wide window. For any Australian PBDB occurrence in the window, 45 of 50 match; the
  five without are Alinga, Frazer Beach, Marburg, Patonga Claystone and
  Tuggerah.
- **PBDB, AAP lists.** The scan matched 64-96% of the vertebrate lists' names
  but 12-53% of the invertebrate and microfossil lists' (source claim). It
  matched against PBDB's taxonomy overall, not its Australian records, and the
  matching rule is unrecorded, so we cannot say how many misses are
  spelling variants. That the specialist lists are ahead of PBDB's Australian
  invertebrate taxonomy is an inference, not a measurement (inferred).
- **ASUD.** 49 of Poropat's 50 normalised units match an ASUD name. The
  exception is the Windalia Sandstone Member; ASUD has "Windalia Sand Member"
  (125.8-113.2 Ma), which is probably the same unit under a different name
  (inferred from the names and ages), and "Windalia Radiolarite", which
  Poropat lists separately and which matches. For the 49, the unit's Poropat
  age (stage ages from PBDB's interval table) overlaps the age of an
  ASUD unit of the same name for 47. The two others are Allaru Mudstone
  (ASUD gives 45-44 Ma, a known ASUD error; contact item C9) and Purlawaugh
  Formation (ASUD 192.9-165.3 Ma; Poropat Kimmeridgian-Tithonian, a 10.5 Myr
  gap). The test is lenient: any same-named ASUD unit counts, in any state.
- **FosSahul.** The mammal and bird lists cover the Quaternary taxa in
  FosSahul (source claim); a name crosswalk has not been built.

## EPRP relevance

The reference taxonomy for Australian fossil vertebrates and selected
invertebrates: name harmonisation for PBDB, FosSahul and NSB-derived analyses,
and Poropat's inventory as a ready occurrence table for Mesozoic tetrapod
questions. It cannot support numeric ages (stage names only) or coordinates.

## Citation and terms

Cite each list by its compilers and date. Poropat et al. (2023) is CC BY 4.0
and the extracted table is a derived table of it; Worthy and Nguyen (2020) is
CC BY-NC-ND 4.0; the AAP lists carry no licence (use for research, cite, do
not redistribute).

## Verification log

- 2026-10-22, checked: Poropat et al. (2023) mirrored; sha256 and licence in
  [snapshots.tsv](snapshots.tsv). Read in the mirrored PDF: the "inaugural"
  and "continuously updated online framework" statements, the 12 September
  2023 online date, the correction notice, the CC BY licence statement, and
  the reference-list entries for Worthy and Nguyen (2020), Travouillon et al.
  (2021), Worthy, Nguyen and Travouillon (2021) and Thorn et al. (2021).
- 2026-10-22, checked: appendix tables extracted ([poropat_tables.py](poropat_tables.py),
  run on deep-server from the mirrored PDF): 299 rows, no `(cid:` placeholder,
  no empty cell, balanced brackets except the one printed defect, every
  `pdftotext -layout` text segment present in its table's cells (0 unmatched;
  8 page headers, 1 appendix title, 17 captions, 17 column headers and 5
  "(continued)" markers set aside) and 0 differences in non-space character
  counts ([profile/poropat_tables_check.tsv](profile/poropat_tables_check.tsv)).
  The same check applied to the first version's output flags the truncated
  *Diamantinasaurus* reference and the three accent cells. Page images of
  Table A5 (the *Eiectus* reference and the 'Plesiosaurus' rows) read at
  220-300 dpi.
- 2026-10-23, checked (rerun): overlap of the Poropat tables with PBDB's
  Australia and New Guinea region (public records, cut from the global
  snapshot 2026-10-23T0329Z), PBDB's interval table (2026-10-22T0611Z) and
  ASUD (2026-10-22T0604Z) ([poropat_overlap.py](poropat_overlap.py)): the
  figures in the Overlap section; spelling counts in the paper's text. [Detail
  withheld pending disclosure to the data custodian.] The final rerun against
  2026-10-23T0329Z, on the evening of 23 October, reproduced the committed
  profile byte for byte.
- 2026-10-22, source claim (independent review, not rerun): the review
  compared the page images of pp. 71-78 with the extracted rows and found
  cell contents to match for all 299 rows apart from the defects fixed here.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): AAP site,
  list dates, compilers, approximate counts and PBDB match rates; licences,
  access and contents of the Alcheringa papers, including the authors, title,
  pages and DOI of Jackson et al. (2024), the scope of Jell and Cook (2025),
  and the licence of Worthy and Nguyen (2020). The Worthy and Nguyen download
  returned an HTML bot check.
- 2026-10-22, inferred: the specialist lists are ahead of PBDB's Australian
  invertebrate taxonomy (see Overlap); Windalia Sand Member is Poropat's
  Windalia Sandstone Member.
