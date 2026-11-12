# Infrastructure-audit reconstruction: source checks

Checked 12 November 2026 against `papers/infrastructure-audit/reconstruction/3b-paragraph-abstracts.md`
at `48e55e3`. Request: Board 76/3280, updated by Claude at 3285; acceptance: 3287.
Main Codex integrated three bounded GPT-6.1 Sol source checks and verified model identities,
documentation and access refinements. Claude retains bibliography and manuscript edits.

The [metadata receipt](2026-11-12-infrastructure-audit-citations.metadata.json) preserves twenty
selected identity records, metadata authorities, retrieval dates and response hashes. It contains
no full text. The [brief](../../../papers/infrastructure-audit/docs/audits/2026-11-12-paragraph-abstracts-citation-brief.md)
defines the fourteen slots and two additional passage checks. A slot is not necessarily one paper.

## Decisions for drafting

All slots were assessed. Twelve have passage support for the specified, bounded uses. **S02 has
verified book/chapter identity and publisher description, but no chapter passage; S08 has checked
exact-version implementation documentation, but its original paper's passages remain inaccessible.**
The additional Raup check remains identity-only; Smith's narrow rock-availability use is supported
by its primary abstract. Neither is represented as a full-body check.

| Slot | Paragraph | Return |
|---|---|---|
| S01 | I1, M2, R2 | Peters–McClennen API paper and versioned PBDB field documentation checked |
| S02 | I1 | GTS2020 identity/catalogue checked; substantive chapter passage unresolved |
| S03 | I2 | Dillon et al. 2023 review, relevant section checked |
| S04 | I4 | One CORE-Bench reproduction precedent; context only |
| S05 | R4/S1 | admtools method paper plus exact 0.7.0 manual/source identity checked |
| S06 | R4/S1 | fossilbrush article identity plus exact 1.0.6 manual checked |
| S07 | R5 | Book identity and cached official Bristol digital-product passages checked |
| S08 | R6 | Robson–Whitlock original identity; exact EDE 0.2.0 operation checked; original passage open |
| S09 | R6 | Tested PALEOMAP index points to Scotese 2016 PaleoAtlas v3, not the 2018 PaleoDEM deposit |
| S10 | R6 | Torsvik–Cocks book identity and author reconstruction procedure checked; retain model name separately |
| S11 | D3 | van Hinsbergen et al. 2015: reference frames and propagated uncertainty checked |
| S12 | D3 | Bradshaw 2012 full relevant methods checked through public author copy; existing citation adequate |
| S13 | D2/D4 | Official GBIF download-predicate, metadata/DOI and citation documentation checked |
| S14 | D5 | Yesson et al. 2007: validation and processing-quality example; motivation only |
| P01 | I2 | Raup 1972 identity verified; passage unresolved |
| P02 | I2 | Smith 2001 primary abstract checked; body/PDF unresolved |

Use the directly read Dillon review for the generic bias sentence while P01 is open. Use S02
bibliographically to identify the named reference work, without attributing an unread chapter's
specific conclusions. For S08, distinguish historical attribution from what the tested software
actually implements. CORE-Bench supplies a precedent, not evidence for EPRP's coverage or capability.
The word “every” in I4 needs EPRP's own component inventory/receipts; this source check does not
verify that exhaustive coverage. “The checks reported here” avoids an unsupported coverage claim.

## S01. PBDB overview, access and interval semantics

**Identity:** Shanan E. Peters and Michael McClennen, *The Paleobiology Database application
programming interface*, *Paleobiology* 42(1):1–7,
[10.1017/pab.2015.39](https://doi.org/10.1017/pab.2015.39). Crossref dates online publication to
23 December 2015 and the paginated issue to February 2016. Use **2016** for that journal citation.

**Read:** [author institutional published PDF](https://strata.geology.wisc.edu/reprints/PetersMcClennen.pdf),
p.1 “The PBDB Data Model”; pp.1–2 “Occurrences” and Fig.1; pp.3–5 API discussion and Table 1.
These support occurrence/collection organization, chronology links and programmatic query access.
They do not document EPRP's mirroring or establish its dated set differences.

For R2, official [Data Service 1.2 interval RESPONSE](https://paleobiodb.org/data1.2/intervals/list_doc.html#RESPONSE)
and [PARAMETERS](https://paleobiodb.org/data1.2/intervals/list_doc.html#PARAMETERS), read on 12 November,
define `b_age`/`t_age` in Ma, interval/scale identifiers and scale selection. The
[occurrence RESPONSE](https://paleobiodb.org/data1.2/occs/list_doc.html#RESPONSE) defines age bounds
and interval fields. Cite versioned documentation for field meaning. The 460/317/17 modal changes,
snapshot membership and regional-screen results remain C076/C191/C192. Current documentation is not
a frozen October schema, and the paper's historical static-age discussion does not establish an
automatic re-dating mechanism.

## S02. Geologic Time Scale 2020

**Identity checked:** *Geologic Time Scale 2020*, first edition, Elsevier, 2020; editors Felix M.
Gradstein, James G. Ogg, Mark D. Schmitz and Gabi M. Ogg. Book DOI
[10.1016/C2020-1-02369-3](https://doi.org/10.1016/C2020-1-02369-3), ISBN 9780128243602.
Crossref supplies book identity/year/ISBN; editor names, edition and description were checked in
the [official publisher catalogue](https://shop.elsevier.com/books/geologic-time-scale-2020/gradstein/978-0-12-824360-2).
The DOI metadata omits editors, so the catalogue is the source for those fields.

**Passage limit:** Gradstein's “Introduction,” vol.1 pp.3–20,
[10.1016/B978-0-12-824360-2.00001-2](https://doi.org/10.1016/B978-0-12-824360-2.00001-2), is also
identity-verified. Publisher chapter access returned 403. Catalogue description/contents were read;
no chapter passage was. An exposed search abstract was not substituted for a read source.
This supports identifying a time-scale reference, not specific unread statements about calibration,
PBDB agreement with ICS or equivalence to the current ICS chart. Keep substantive passage status open.

## S03. Sampling/bias context

**Identity:** Erin M. Dillon et al. (2023), *Challenges and directions in analytical paleobiology*,
*Paleobiology* 49(3):377–393,
[10.1017/pab.2023.3](https://doi.org/10.1017/pab.2023.3). Full author list is in the metadata receipt.

**Read:** [open primary author manuscript](https://pmc.ncbi.nlm.nih.gov/articles/PMC7615171/),
“Challenge 1: Measuring Biodiversity across Space and Time,” especially its sampling, richness-estimator
and geographic-standardization paragraphs. Supports the established context of geological,
preservational and sampling biases and methods for comparing completeness. Nonspatial standardization
does not resolve every geographic/environmental difference.

The same section discusses transparent workflows and cleaning tools. It supports the context, not
a claim that infrastructure concerns were neglected, EPRP's novelty, defect prevalence or agent
superiority. It is adequate for I2's generic bias sentence while older passage checks remain open.

## S04. Agent reproduction precedent

**Identity:** Zachary S. Siegel, Sayash Kapoor, Nitya Nadgir, Benedikt Stroebl and Arvind Narayanan,
*CORE-Bench: Fostering the Credibility of Published Research Through a Computational Reproducibility
Agent Benchmark*, [arXiv:2409.11363v2](https://arxiv.org/abs/2409.11363v2). arXiv API verified
identity/version; first submitted 17 September 2024, checked v2 updated 22 June 2026. No journal DOI
was established here. Preserve **Nadgir**, rather than a misspelled search-result variant.

**Read:** [primary preprint](https://arxiv.org/html/2409.11363v2), §2/Fig.4, §3, §4 and Appendix A.3.
Agents reproduce outputs from supplied code/data; humans construct tasks and reference results,
including three manual runs. This is a directly relevant precedent for evaluating computational
reproduction. It does not test scientific truth, database auditing, superiority to human auditors
or EPRP's own performance. One source is sufficient for this background use; retain program-specific I4.

## S05. admtools identity and tested conversion

**Identity:** Niklas Hohmann, David De Vleeschouwer, Sietske Batenburg and Emilia Jarochowska (2025),
*Nonparametric estimation of age–depth models from sedimentological and stratigraphic information*,
*Geochronology* 7:427–448,
[10.5194/gchron-7-427-2025](https://doi.org/10.5194/gchron-7-427-2025). Separate registered package
identifier: [10.32614/CRAN.package.admtools](https://doi.org/10.32614/CRAN.package.admtools).

**Read:** [published method article](https://gchron.copernicus.org/articles/7/427/2025/), §2.2 Eq.1
and §3 opening; exact [CRAN 0.7.0 archive](https://cran.r-project.org/src/contrib/admtools_0.7.0.tar.gz),
`man/strat_to_time.numeric.Rd` Description/Value and `man/get_time.Rd` Arguments/Details. These
identify height-to-time conversion and hiatus choices. The article used **0.5.0**; tested software
was **0.7.0**, CRAN date 8 October 2026. Cite paper and explicit tested version separately.

Archive SHA256: `ce11b36751f7f10dc6d06779b8c5d9dd5aab81d24091ca4c3bd1fed20b548ef4`.
Its CITATION points to v0.6.0, while an indexed citation page points to v0.5.0: neither is a version
pin for 0.7.0. Use the numeric-method manual rather than the generic dispatch description's direction
label. C096, not these references, supports the synthetic control's error counts and maximum.

## S06. fossilbrush identity and threshold operation

**Identity:** Joseph T. Flannery-Sutherland, Nussaïbah B. Raja, Ádám T. Kocsis and Wolfgang Kiessling
(2022), *fossilbrush: An R package for automated detection and resolution of anomalies in
palaeontological occurrence data*, *Methods in Ecology and Evolution* 13:2404–2418,
[10.1111/2041-210X.13966](https://doi.org/10.1111/2041-210X.13966). Separate package identifier:
[10.32614/CRAN.package.fossilbrush](https://doi.org/10.32614/CRAN.package.fossilbrush).
Paper and package metadata use different forms of some author names; preserve the paper's authors
for its citation.

**Read:** exact [CRAN 1.0.6 archive](https://cran.r-project.org/src/contrib/fossilbrush_1.0.6.tar.gz),
DESCRIPTION, CITATION and `man/flag_ranges.Rd` Description, arguments and Value. Version 1.0.6,
dated 5 June 2025, matches the replay. The manual describes reference-range comparison with a
threshold in Myr, default 5. SHA256:
`ecaabde818ec96e603d759cb63c568b3687a23151cadc5eac238d73ecd4d7177`.

The article identity was checked; no Wiley full text/TDM was used. The manual supports operation;
C102 supplies the text-comparison finding and missed examples. This is not evidence that every
cleaning function fails or that a measured fraction of real records is misflagged.

## S07. Fossil Record 2 book and digital product

**Book:** M. J. Benton (editor), 1993, *The Fossil Record 2*, Chapman & Hall, London;
ISBN 0412393808 / 9780412393808. Checked against the
[publisher catalogue](https://link.springer.com/book/9780412393808) and
[British bibliographic record](https://obnb.uk/p9087300-the-fossil-record-2). Distinguish original
imprint/year from migrated catalogue fields showing a later copyright/imprint. No book DOI was
established in this check.

**Digital passages read:** retained official Bristol pages
[introduction](https://palaeoresources.blogs.bristol.ac.uk/) and
[downloads](https://palaeoresources.blogs.bristol.ac.uk/fr2-downloads/), `wp_pages.json` snapshot
`2026-10-23T0505Z_url`, inspected 12 November. “Introduction to the database” credits Mary Benton's
Excel compilation and describes family/family-surrogate rows, habitat fields and range columns.
“Entire data set” and “Spreadsheet key and conventions” describe the single workbook, 45 chapter
workbooks and field conventions. Source JSON SHA256:
`415e9cb60ca2b249e04cb092a77912fa0ef1648e96f69667944fb311d54d0c0f`.

Live host requests failed, so this is a cached primary-source check. The exact
[`All-Life.xlsx`](https://palaeoresources.blogs.bristol.ac.uk/files/2019/08/All-Life.xlsx) mapping comes
from the acquisition script/replay provenance, since the extracted page text omits href targets.
C048 establishes the 220 shifted cell tails, with distinct consequences; those are not 220 damaged
printed-book rows or necessarily 220 changed geological ranges. Individual chapter authors were not audited.

## S08. Robson–Whitlock: original attribution and exact implementation

**Original identity:** D. S. Robson and J. H. Whitlock (1964), *Estimation of a truncation point*,
*Biometrika* 51(1–2):33–39,
[10.1093/biomet/51.1-2.33](https://doi.org/10.1093/biomet/51.1-2.33). Crossref verified.
Original PDF/JSTOR routes failed or presented access challenges; original assumptions/formula pages
were not read and must not be marked passage-verified.

**Checked operational source:** official
[EDE 0.2.0 archive](https://cran.r-project.org/src/contrib/Archive/EDE/EDE_0.2.0.tar.gz),
`man/robson1964.Rd`, `R/robson1964.R`, and retained caller/version records. Its point estimate is
the latest distinct sighting plus the final gap; its upper bound adds `(1-alpha)/alpha` times that
gap, hence 19 gaps at alpha=0.05, and is labeled one-sided. Older indexed docs describe a different
release. This identifies what was tested, without certifying the original paper's assumptions or
claiming a fresh software run. C194 supplies observed coverage; C196's failed agreement gate remains.
Archive SHA256: `8b8e674711e0cbfb57defbd554964192d74da7671278d51ef349e51e86a9ed97`.

## S09. PALEOMAP source identity

**Correct record:** Christopher Scotese (2016), *PALEOMAP PaleoAtlas for GPlates*, v3,
[10.5281/zenodo.10596610](https://doi.org/10.5281/zenodo.10596610); concept DOI
10.5281/zenodo.10596609. DataCite and the [Zenodo record](https://zenodo.org/records/10596610)
verify author, 2016 publication date, version, description and `Scotese_PaleoAtlas_2016_v3.zip`.
The record was created in 2024; that is not its stated publication year.

**Match and passage:** the committed `gplates-models-index-2026-10-24.json` at `5ec10f1`, entry
`paleomap`, gives that exact Version DOI and the rotation/static-polygon URLs used by the replay.
The [current official model documentation](https://gplates.github.io/plate-model-manager/latest/plate_models.html#scotese2016)
also identifies Paleomap as Scotese2016. Zenodo's Description identifies the PaleoAtlas and loading
project. This is a registry/provenance match; the full Zenodo bundle was not independently byte-compared
with the wrapper archives. The replay already pins their SHA256 values.

Do not substitute Scotese–Wright 2018's PaleoDEMs, concept 10.5281/zenodo.5348491, for this rotation
model. C125 supports the three-model spread, rather than the atlas description.

## S10. Torsvik–Cocks book, model label and frame procedure

**Identity:** Trond H. Torsvik and L. Robin M. Cocks, *Earth History and Palaeogeography*, Cambridge
University Press, [10.1017/9781316225523](https://doi.org/10.1017/9781316225523),
ISBNs 9781316225523 / 9781107105324. Crossref currently gives print 31 October **2016** and online
24 November **2016**; the [publisher catalogue](https://www.cambridge.org/core/books/earth-history-and-palaeogeography/076D4FCFCEE4CAE6F8EF3B449594DD50)
also gives 2016 dates. Use verified edition metadata for the reference year. Keep **TorsvikCocks2017**
as the tested model identifier; a model name is not a bibliographic date. A front-matter download
failed (503); no book chapter was read.

**Primary procedure read:** authors' [GPlates procedure](https://www.earthdynamics.org/earthhistory/data_info.html),
opening four paragraphs and file list. It explicitly distinguishes anchor plate 0's hybrid/mantle
frame from anchor plate 1's paleomagnetic/paleogeographic frame and names
`Torsvik_Cocks_HybridRotationFile.rot`. The pinned index links `torsvikcocks2017` to this page,
Version `2023-12-06_20-09-00`; the replay's rotation routine uses anchor 0.

The documentation makes frame/anchor choice material. It does not show which parameters produced
the archived service coordinates or prove the cause of C123's observed rotations. No frame rerun,
new numerical result or choice of the correct reconstruction is made here.

## S11. Paleolatitude uncertainty

**Identity:** Douwe J. J. van Hinsbergen et al. (2015), *A Paleolatitude Calculator for Paleoclimate
Studies*, *PLOS ONE* 10(6):e0126946,
[10.1371/journal.pone.0126946](https://doi.org/10.1371/journal.pone.0126946). Crossref verified.

**Read:** [published primary text](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0126946),
“An Online Paleolatitude Calculator” following Fig.3/Eqs.2a–2b, “Choosing the appropriate reference
frame,” Fig.5C/Table 2. It propagates pole confidence regions and age bounds, compares frames and
explicitly omits additional plate-reconstruction errors. This supports distinguishing propagated
uncertainty from frame/model sensitivity.

It does not calibrate uncertainty for EPRP's three models, supply universal paleolatitude error bars,
identify C123's correct route or turn greater model spread into greater true error. D3's model/cohort
reporting action is a recommendation motivated by the distinction.

## S12. GRIWM and the uncertainty an interval represents

**Retain the existing citation:** C. J. A. Bradshaw, A. Cooper, C. S. M. Turney and B. W. Brook (2012),
*Robust estimates of extinction time in the geological record*, *Quaternary Science Reviews* 33:14–19,
[10.1016/j.quascirev.2011.11.021](https://doi.org/10.1016/j.quascirev.2011.11.021). Crossref verifies
the issue identity; online availability/acceptance in 2011 does not change its 2012 journal citation.

**Read:** [public author-hosted published personal copy](https://conservationbytes.com/wp-content/uploads/2012/01/bradshaw-et-al-2012-qsr.pdf),
p.15 §2.1 and p.16 §2.2, paragraph after Eq.4 and following coverage paragraph. Author identity/link
was checked through the author's site/publications list. The method simulates fossil recovery,
assigns dating errors, resamples observed dates using Gaussian errors, and separately evaluates
coverage across simulated series. No restricted TDM export was used and no full copy is redistributed.

This is adequate provenance/process context. The article calls its limits confidence limits; it
does not itself state EPRP's conditional interpretation or zero-error result. C110 supplies that
control/interpretation; C098 separately supplies the random-state finding. Preserve that distinction.

**Optional, not required:** Solow, Roberts and Robbirt (2006), *On the Pleistocene extinctions of
Alaskan mammoths and horses*, *PNAS* 103:7351–7353,
[10.1073/pnas.0509480103](https://doi.org/10.1073/pnas.0509480103), was identity-verified and read in
the [publisher full text](https://www.pnas.org/doi/10.1073/pnas.0509480103), Discussion opening and
Methods Eqs.1–2/7. Its model explicitly separates latent uniform fossil ages from normal dating
errors and includes both. It supports explaining those processes, not any assertion about GRIWM's
code or coverage under arbitrary preservation. The extra citation is optional after the Bradshaw
access gap was resolved.

## S13. Version/query and download citation practice

**Official sources, no DOI invented:** GBIF Secretariat,
[API Downloads](https://techdocs.gbif.org/en/data-use/api-downloads#requesting-an-occurrence-download),
“Requesting an occurrence download”; [Citation](https://techdocs.gbif.org/en/data-use/citation);
[download formats](https://techdocs.gbif.org/en/data-use/download-formats), Darwin Core Archive and
“Citation (citations.txt)” sections. Current pages read on 12 November 2026.

The request records a format and filter predicate; download-key metadata includes the resulting
link/DOI. Documentation describes interpreted and verbatim records and download/dataset citations.
This supports identifying a particular extract and retaining its query/provenance alongside files.
Sandve's already checked Rules 1/3/8 support versions and intermediate products. The main GBIF
citation-guidelines page returned 403; no passage from it is needed for this return.

Do not treat a persistent DOI as a guarantee that all files remain available, or the guideline as a
measurement of recommendation effectiveness. These are dated practices, not our database findings.

## S14. Biodiversity-informatics motivation

**Identity:** Chris Yesson et al. (2007), *How Global Is the Global Biodiversity Information
Facility?*, *PLOS ONE* 2(11):e1124,
[10.1371/journal.pone.0001124](https://doi.org/10.1371/journal.pone.0001124). Crossref verified.

**Read:** [published primary text](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0001124),
Methods “Name validation”/“Spatial validation,” Results “Exclusions,” and Discussion on incomplete
distribution references/grid resolution. The study uses taxonomic/distribution comparisons and
identifies processing/coordinate inconsistencies. It also shows how incomplete references or coarse
grids can reject genuine records.

This motivates D5's proposed source-comparison application. It supplies neither today's GBIF defect
frequency nor evidence that this agent workflow works there. Keep the prospective wording and avoid
importing historical exclusion percentages. Meyer et al. 2015 was examined as an alternative; adding
both is unnecessary for this use.

## P01–P02. Outstanding historical passage checks

**P01:** David M. Raup (1972), *Taxonomic Diversity during the Phanerozoic*, *Science* 177:1065–1071,
[10.1126/science.177.4054.1065](https://doi.org/10.1126/science.177.4054.1065). Identity verified.
Publisher requests failed; the bounded open-copy search and retained open-library metadata check
did not supply text. No page-level support is claimed. Use the read review for I2's generic context;
keep Raup in the source queue rather than using it as passage-verified support.

**P02:** Andrew B. Smith (2001), *Large-scale heterogeneity of the fossil record: implications for
Phanerozoic biodiversity studies*, *Phil. Trans. R. Soc. B* 356:351–367,
[10.1098/rstb.2000.0768](https://doi.org/10.1098/rstb.2000.0768). Crossref identity and the actual
[primary abstract](https://pmc.ncbi.nlm.nih.gov/articles/PMC1088432/) were read. It supports a narrow
rock-availability/diversity-pattern connection in post-Paleozoic Western Europe and leaves sampling
versus shelf-area explanations open. PDF/body routes failed; no internal page is claimed read.
The abstract is adequate for that limited context, not a claim that variation is purely artefactual.

## Access, verification and handoff

This was a bounded check of named uses, not a systematic review or novelty search. Discovery used
existing catalogues, publisher/author/repository pages, Crossref, DataCite and arXiv metadata; it
stopped at adequate passages or explicit unresolved access. Raw responses, software archives and
research copies remain outside Git. Wiley TDM text and restricted Elsevier exports were not used.
All source accounts above are paraphrases; metadata, context and EPRP's own findings remain distinct.

Previously checked Alroy 2008, Smith et al. 2025 and Sandve 2013 uses are documented in the
[step 3a review](../../../papers/infrastructure-audit/docs/audits/2026-11-12-section-abstracts-critique.md)
and Board 160/3272 and need no redundant sourcing here. The Zenodo paper-snapshot DOI is still a
release task, not a missing literature identifier.

Claude can integrate the supported uses and exact versions now. Keep S02/original-S08/P01 access
limits visible in the source record and narrow P02 to its abstract; no need to block context drafting
when a directly read alternative supports the sentence. No bibliography regeneration, allowlist change,
manuscript revision, new analysis or release was performed in this source-check tranche.

Next: Claude — integrate the verified sources and retain the stated passage/version limits.
