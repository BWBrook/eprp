---
id: fossil-checklists
name: Australasian fossil species checklists (AAP National Fossil Species Lists; Alcheringa annotated checklists)
kind: compilation
status: active
last_update: "2026-06 (AAP mammal and bird lists)"
scope:
  taxa: ["mammals, birds, reptiles and amphibians, Mesozoic tetrapods, trilobites, echinoderms, archaeocyaths, microbialites, Triassic dinocysts"]
  time: "Cambrian to Holocene, by list"
  space: "Australia (mammal list also New Guinea; Jackson et al. also New Zealand and eastern Indonesia)"
  record_unit: "accepted species with authority and synonyms (AAP lists); taxon occurrence by rock unit with age and references (Poropat et al. 2023)"
size:
  as_of: "2026-10-22"
  aap_lists: 9
  poropat_occurrence_rows: 299
access:
  tier: unclear
  licence: "AAP lists: no licence stated (unclear); Poropat et al. 2023: CC-BY-4.0; Worthy and Nguyen 2020: CC-BY-NC-ND-4.0; Jackson et al. 2024 and Jell and Cook 2025: closed, no licence"
  routes:
    - {type: web, url: "https://www.australasianpalaeontologists.com/national-fossil-species-lists", state: "nine PDFs; the cited .org domain is dead", checked: 2026-10-22}
    - {type: journal, url: "doi:10.1080/03115518.2023.2228367 (Poropat et al. 2023, open access)", state: "mirrored", checked: 2026-10-22}
    - {type: journal, url: "doi:10.1080/03115518.2024.2434062 (Jackson et al. 2024); doi:10.1080/03115518.2025.2457423 (Jell and Cook 2025)", state: "closed access; documented only", checked: 2026-10-22}
    - {type: journal, url: "doi:10.1080/03721426.2020.1756560 (Worthy and Nguyen 2020, CC BY-NC-ND)", state: "the publisher served a bot check to scripted requests; not mirrored", checked: 2026-10-22}
  api: none
versioning:
  replay: partial
  notes: "AAP lists are replaced in place (dated inside each PDF); journal checklists are fixed, with published corrections"
mirror:
  path: deep-server:/data/paleodata/fossil-checklists
  policy: "openly licensed checklists only; AAP lists documented until a licence is stated"
  state: "poropat2023 (PDF, and the appendix tables extracted to derived/)"
lineage:
  upstream:
    - "the Australasian Palaeontologists (AAP) National Fossil Species Lists committees; Alcheringa checklist series (from 2023)"
  downstream:
    - "candidate comparators for PBDB's Australian taxonomy"
eprp_questions: []
citation:
  - "Poropat, S. F. et al. (2023). An annotated checklist of Australian Mesozoic tetrapods. Alcheringa 47: 129-205. doi:10.1080/03115518.2023.2228367"
  - "Jackson et al. (2024). An annotated checklist of Australasian fossil mammals. Alcheringa 48: 548-746. doi:10.1080/03115518.2024.2434062"
  - "each AAP list by its compilers and date, as given in its How to cite line"
entry:
  created: 2026-10-22
  updated: 2026-10-22
  by: Claude (Opus 5.5, side session); source scan by a Claude Sonnet subagent
  reviewed: "not yet"
---

# Australasian fossil species checklists

## Summary

Expert-curated lists of Australian fossil species, maintained by the
Australasian Palaeontologists (AAP) as nine "National Fossil Species Lists"
and, since 2023, published as annotated checklists in Alcheringa. They are the
authority against which a fossil occurrence database's names can be checked:
which species are valid, under which name, and what synonyms they absorb.
None is a database: the AAP lists are name lists in PDFs with no licence, and
of the Alcheringa checklists only Poropat et al.'s Mesozoic tetrapods (2023)
is open. We mirror that paper and extract its occurrence tables (taxon, rock
unit, age, references); the rest are documented.

## Contents

**AAP National Fossil Species Lists** (source scan; species counts are the
scan's approximate parse, and "in PBDB" is the share of those binomials found
in PBDB's taxonomy):

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
ages, localities or references.

**Alcheringa checklists and related papers:**

- *Poropat et al. (2023), Australian Mesozoic tetrapods*, CC BY 4.0, mirrored.
  Its twelve appendix tables list occurrences by rock unit with age range and
  references; our extraction ([poropat_tables.py](poropat_tables.py);
  [table](profile/poropat2023_appendix_tables.tsv)) has 299 rows: temnospondyls
  49, parareptiles and basal neodiapsids 2, ichthyosauromorphs 12,
  lepidosaurs 6, sauropterygians 41, turtles 16, non-archosaurian
  archosauromorphs 4, crocodylomorphs 5, pterosaurs 12, dinosaurs (with birds)
  75, synapsids (with mammals) 16 and ichnofossils 61, across 55 rock units.
- *Jackson et al. (2024), Australasian fossil mammals*: 482 taxa (406
  Australian), with type material, type locality, unit and age; closed
  access, no data supplement.
- *Jell and Cook (2025), Australian Mesozoic marine macroinvertebrates*: over
  900 taxa; closed.
- *Worthy and Nguyen (2020), fossil birds of Australia*: CC BY-NC-ND 4.0 (the
  source of the AAP bird list's content); the publisher blocks scripted
  downloads.

## Provenance and lineage

The AAP lists are compiled by committees of specialists and replaced in place
on the association's site; Alcheringa began an annotated checklist series in
2023 with Poropat et al. and Jackson et al. Poropat et al. was corrected in
2025 (doi:10.1080/03115518.2025.2508434); our copy is the corrected version.
Poropat et al. promised a continuously updated online framework; none was
found.

## Structure

AAP lists: indented PDF text (higher taxa, accepted names with authority,
synonyms marked "•" or "="), parseable by indentation. Poropat tables: four
columns (taxon, rock unit, age range, references), extracted by word position
because the PDF has no table structure.

## Access

- **AAP.** `https://www.australasianpalaeontologists.com/national-fossil-species-lists`
  (PDF links at `/s/<name>.pdf`). Each PDF's "How to cite" line still names
  the old `.org/databases` address, which no longer resolves.
- **Mirror.** `deep-server:/data/paleodata/fossil-checklists/poropat2023/`:
  `raw/` (the PDF, fetched on the laptop with `data_mirror.py url` because the
  publisher refused requests from deep-server) and `derived/` (the extracted
  tables). Index: [snapshots.tsv](snapshots.tsv).

## Strengths

- Expert, current names and synonymy for Australian fossil vertebrates and
  several invertebrate groups, updated as recently as June 2026.
- Poropat et al. gives an occurrence-level, referenced inventory of every
  Australian Mesozoic tetrapod, under an open licence.

## Weaknesses and pitfalls

- **No licence on the AAP lists**, so we cannot redistribute them or tables
  derived from them; the old domain cited in every PDF is dead.
- **Name lists, not data.** The AAP lists have no ages or localities.
- **Closed checklists.** The richest lists (mammals, marine
  macroinvertebrates) are paywalled with no data supplements.
- **Extraction caveats.** The Poropat table is parsed from PDF layout; rows
  were spot-checked and all fields are filled, but check against the paper
  before citing a row. Its rock-unit names follow the paper, not ASUD.

## Overlap with other sources

- **PBDB.** 85 of the 90 binomials in Poropat's body-fossil tables appear among
  PBDB's Australian Mesozoic tetrapod names; the five absent include species
  described in 2021–2023 (*Eomurunna yurrgensis*, *Eiectus longmani*) and
  *Minmi paravertebra*. 28 of Poropat's 50 normalised rock units appear among
  PBDB's formation names ([poropat_overlap.py](poropat_overlap.py)). For the
  AAP lists, PBDB matches 64–96% of vertebrate names but only 12–53% of
  invertebrate and microfossil names (source scan), so PBDB's Australian
  invertebrate taxonomy lags the specialist lists.
- **ASUD.** 49 of Poropat's 50 normalised rock units match an ASUD name.
- **FosSahul.** The mammal and bird lists cover the Quaternary taxa in
  FosSahul; a name crosswalk has not been built.

## EPRP relevance

The reference taxonomy for Australian fossil vertebrates and selected
invertebrates: name harmonisation for PBDB, FosSahul and NSB-derived analyses,
and Poropat's inventory as a ready occurrence table for Mesozoic tetrapod
questions.

## Citation and terms

Cite each list by its compilers and date. Poropat et al. (2023) is CC BY 4.0;
Worthy and Nguyen (2020) CC BY-NC-ND 4.0; the AAP lists carry no licence (use
for research, cite, do not redistribute).

## Verification log

- 2026-10-22, checked: Poropat et al. (2023) mirrored and verified; appendix
  tables extracted (299 rows, all fields filled; spot-checked) and compared
  with PBDB and ASUD ([poropat_overlap.py](poropat_overlap.py)); Worthy and
  Nguyen download returned an HTML bot check.
- 2026-10-22, source claim (source scan, Claude Sonnet subagent): AAP site,
  list dates, compilers, approximate counts and PBDB match rates; licences,
  access and contents of the Alcheringa papers.
