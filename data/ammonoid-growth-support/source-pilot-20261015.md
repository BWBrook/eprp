# B-002: small source, specimen and relationship pilot

Codex, 15 October 2026. Follows the [workbook audit](README.md) and
[developmental-route contract](../../literature/2026-10-14-ammonoid-developmental-route-contract.md).

**Result: source/specimen candidates found; no historical transition made
eligible.** This pilot follows the three Sudeticeras rows with conflicting
superfamily labels, plus the four repeated Macrocephalites rows as a source
check. It is a convenience sample selected for traceable provenance questions,
not a representative lineage sample or a failure-rate estimate.

## What the original study clarifies

[Walton & Korn 2017](https://doi.org/10.1111/pala.12308), Methods, Tables 1–2,
Figures 3 and 8, relevant Discussion, were read in publisher full text:

- Selection favoured late-growth CWI 0.60–1.10 and UWI 0.00–0.30, with
  exceptions; Methods describes typical/best-preserved representatives.
- Tables count 179 specimens, versus 177 species; Conclusions says 178.
- Figure 8 identifies two **M. macrocephalus**, MB.C.26517/26518, and two
  **M. verus**, MB.C.26519/26520.
- The illustrated broad phylogram is adapted from House 1988. Discussion
  already proposes stage-specific ecological explanations of recurrent growth.

Our inference: late-shape selection cannot define the denominator of all
possible innovations. The caption supplies candidate specimen sets, not a
verified ordering of workbook rows within each pair. No assignment by list
position is made, and the source's three different count statements are retained.
An independent species-level relationship and observation model remain needed.

## Sudeticeras: the primary source and the candidate link

[Korn 1997, *The Palaeozoic ammonoids of the South Portuguese Zone*](https://docbase.lneg.pt/docs/Memorias/33.pdf),
printed pp. 40–41, identifies **IGML 257**, a sectioned paratype of
S. murracaoense, in Text-figure 29a and a measurement table. This is the
publication named in `Species!H111`; that source-level link is verified.
The specimen-to-row link is a candidate, not a resolved identity.

The parent visually checked the original pages and independently read the
workbook's XML. The following compares source table positions; it does not
alter measurements or assume the trajectories are identical:

| Workbook column (row 111) | Workbook dm | Published IGML 257 dm (mm) | Workbook CWI | Published ww/dm |
| --- | ---: | ---: | ---: | ---: |
| Q | 18.905 | 18.9 | 0.689024 | 0.69 |
| S | 9.343 | 9.4 | 0.856470 | 0.85 |
| U | 5.292 | 5.3 | 0.893991 | 0.89 |
| W | 3.298 | 3.3 | 0.831716 | 0.85 |
| Y | 2.007 | 1.9 | 0.776781 | 0.64 |

The agreement is suggestive, but ordinary rounding does not explain every
entry. Remeasurement is a possibility, not a documented transformation. The
table establishes millimetres for its own measurements; this does not silently
add units to every workbook row.

The original description calls all 311 specimens septate phragmocones and
describes the adult stage above 20 mm. Row 111 ends at 18.905. Neither a
complete body chamber nor independently established adult maturity is supplied
for this candidate. A complete phragmocone is not a complete living shell.

## Bounded crosswalk

| Workbook rows / source labels | Primary specimen candidates | Link status and limit |
| --- | --- | --- |
| 111, S. murracaoense; Korn 1997 | IGML 257, Text-fig. 29a, printed p. 41 | Correct primary publication and species; partial numerical correspondence above. Exact row identity unresolved |
| 112, S. occultornatum; MfN material | MB.C.9078.2, with other sectioned candidates MB.C.9078.13/.3/.4, Klug et al. 2006 Fig. 19 | Catalogue/section candidates. Maximum size of .2 is close to the workbook; no exact row/measurement-chain match |
| 113, S. pusillobatum; MfN material | MB.C.9053.1 and MB.C.9077.1, Klug et al. 2006 Fig. 17 | Both illustrated sections; the inspected published numerical series does not establish the workbook-row identity |
| 177–178, M. macrocephalus; MfN material | MB.C.26517 and MB.C.26518, Walton & Korn Fig. 8A–B | Species-to-specimen-set link; row-to-ID assignment unresolved |
| 179–180, M. verus; MfN material | MB.C.26519 and MB.C.26520, Walton & Korn Fig. 8C–D | Species-to-specimen-set link; row-to-ID assignment unresolved |

[Klug et al. 2006](https://doi.org/10.1002/mmng.200600001), printed pp. 19–23
and the measurement appendix (pp. 56–57), supplies the two Moroccan species descriptions,
catalogue IDs and scaled cross-sections. Such sections improve geometry
prospects but do not by themselves establish shell-wall thickness, original
body chamber, soft tissue or mature endpoints for our rows. Published series
and workbook series must remain separate until their relation is documented.

[Korn & Ebbighausen 2008](https://doi.org/10.1002/mmng.200800004), Sudeticeras
account, Figure 53 and appendix, supplies additional S. murracaoense sections
and catalogue records. These are later material; they cannot replace the
explicit 1997 source of row 111. The genus-level origin discussion uses conch
ontogeny as well as sutures, so it is not independent evidence for a transition
between these three workbook growth programmes. No supported ancestral or
sister pair among the target rows was established by this inspection.

The additional [Korn 1997 cladistic paper](https://www.app.pan.pl/archive/published/app42/app42-177.pdf)
does not include Sudeticeras in its character matrix; it cannot supply the
missing target relationship. A lack of an eligible pair in this small source
set is an access/support finding, not evidence that no such relationship exists.

## Decision and limits

**Complete:** the finite source pilot, a verified publication-level link for
row 111, explicit candidate specimen sets and a preserved numerical mismatch.
The raw workbook SHA-256 remains
`fbe2012f1d420ef7b292141ae0ed0ea8d046c4c15303663565dc72e0727ebe40`.
No source cell, taxonomy or inferred specimen ID was overwritten.

**Not established:** an exact row-to-specimen mapping, complete mature growth
and physical inputs for an eligible pair, or an independently reconstructed
evolutionary relationship. No figure measurements were digitised, models fitted or
evolutionary simulations run. Source-level numerical resemblance is not a
license to concatenate tables or treat repeated taxa as independent transitions.

Hold empirical promotion on this pilot. Do not expand to a 177-species
crosswalk now. The next bounded B-002 choice is a close-prior/generator check
to determine whether a distinct conditional theoretical question survives;
keep that separate from claiming a fossil test. A future empirical reopening
needs an explicit specimen link and relationship source, with maturity and
physical support matched to the intended comparison. Claude next critiques
this disposition alongside the [B-001 response](../../ideas/2026-10-15-blue-sky-support-response-codex.md).

## Retrieval and stopping record

Search date: 15 October 2026. Opportunistic, bounded orientation, not a
systematic review. Started from the exact workbook source string and queries
`Sudeticeras murracaoense Korn 1997`, `Walton Korn 2017 ontogenetic ammonoid`
and `Macrocephalites ontogeny Korn Walton`; the delegate also used
`Sudeticeras occultornatum pusillobatum`, `Korn 1997 murracaoense PDF`, the
exact Portuguese monograph title and `Sudeticeras phylogeny`. Followed the
direct primary descriptions of the three Sudeticeras taxa. Stopped after the source table,
candidate sections, preservation and relationship limitations were explicit.

The publisher HTML was retrieved directly with HTTP 200 (647,682 bytes),
SHA-256 `5269c1491ea09cad3ae142d8b74263f8d28465292c4d074e28314e8c4196a501`,
and retained with its retrieval record under ignored
`data/raw/ammonoid-growth-walton-korn-2018/`. The Portuguese monograph and
open primary PDFs were retrieved from the linked official hosts and inspected
at the sections named above; the local pilot's PDF/source inventory is recorded
below. Raw publications are not committed or redistributed with this note.
The 2006/2008 publisher pages state CC BY 3.0. No broader reuse licence is
asserted here for the other consulted publications.

| Local PDF under ignored `scratch/blue-sky-codex/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `korn-1997-portuguese.pdf` | 25,875,195 | `c363e3e3d2ee9adbdd88c98c5ac7847731fba87048fe10210ab43815f9dc870f` |
| `korn-etal-2006-gara.pdf` | 3,767,493 | `6a25ecfe6da784490e7c42ba56ae30139839dafedfb09ad98de44cbea9246edf` |
| `korn-ebbig-2008-chebket.pdf` | 5,308,886 | `f349f03a6f9e61e5c686fc9880a5a0541b6b7e7d5bf5642d1535a60cedf0da64` |
| `korn-1997-goniatitaceae.pdf` | 1,440,472 | `7815636afe1e9691c4cba7764c3a81e3878cf5f88535dadd4b6bc82c40a36621` |

The Portuguese download initially timed out; a range-resumed download
completed at the recorded size and opened as a 124-page PDF. It is scanned:
the decisive pages were rendered and visually read, including a separate
parent check of the table and preservation/maturity descriptions. Other PDFs
were read at the cited sections using extracted text and selected rendered
figures. The 1997 cladistic check used p. 184, Figure 3 and Table 1; the
2008 check used pp. 126–129 and appendix p. 154. None is labelled a full read
of all monograph or article content.
