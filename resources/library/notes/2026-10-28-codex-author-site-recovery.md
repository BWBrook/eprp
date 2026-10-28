# Author-site full-text recovery: first Codex staging batch

Codex, 28 October 2026. This is a bounded acquisition and handover record,
not a modification of the library manifest, index or existing worktree. Barry
asked for more library building and deeper searches for copies the existing
fetcher had not secured. Claude's References session was contacted in
Correspondence 76/2428 for current ownership and handover; no response had
arrived at this checkpoint.

## Result

Thirteen candidates were taken from the 25 October `works.tsv` snapshot,
which lists them as `failed` or `no_copy`. Twelve publicly reachable PDFs
were downloaded and title-checked; the thirteenth returned HTTP 404. The
[table](../review/2026-10-28-codex-author-site-candidates.tsv) records work ID,
DOI, exact source and final URL, prior index status, page and byte counts,
SHA-256, title-check route and outcome. The 12 PDFs and a copy of that table
are staged separately at
`deep-server:/data/codex/artifacts/eprp/author-pdfs-20261028-codex/`;
every copied file's SHA-256 was independently checked at the destination.
The shared `/data/paleodata/library/` store, its catalogue, and its indexes
were not changed. Prior `works.tsv` status is a dated catalogue snapshot;
a read-only check of the current manifest found no held entry for these IDs.

The batch includes [Chen and Benton 2012](https://doi.org/10.1038/ngeo1475),
the full review of end-Permian recovery previously read at abstract depth in
B-001, and [Hull 2015](https://doi.org/10.1016/j.cub.2015.08.053), on
Earth-system succession. Other papers cover non-marine extinction,
Triassic dinosaurs, fossil-record completeness, competition and diversity,
and the Red Queen/Court Jester. The source of 11 successful files is Michael
Benton's [University of Bristol publication page](https://benton.blogs.bristol.ac.uk/publications/),
where the author lists and links the papers; Hull's copy is on the
[Yale Earth and Planetary Sciences site](https://earth.yale.edu/sites/default/files/2024-12/Hull%20pdf%209.pdf).
Both are author-affiliated institutional websites, publicly accessible without
credentials. The files include publisher versions with copyright notices;
public accessibility and author-site provenance are recorded facts, **not**
a determination of licence, permission to redistribute, or a Creative Commons
licence. No TDM copy was used. Do not publish or redistribute them on the basis
of this record.

## Discovery and checking

- The Chen–Benton and Hull copies arose in question-led web searches for
  extinction and recovery; their first pages contain matching titles and DOIs.
- Benton’s public bibliography was parsed at its list-item level. Titles were
  normalised and exactly matched against records in the cited-ID, canon or
  Barry 2003-list tiers whose indexed status was `failed`, `no_copy` or
  `not_tried`. A result had to include an explicitly labelled PDF link in that
  same bibliography item. This is a pilot over one author's page, not a field
  coverage estimate or a general-purpose search engine.
- Each successful response began with PDF magic and passed `pdfinfo`; title
  checks used `pdftotext` over the first three pages. Seven required first-page
  rendering and Tesseract OCR because their embedded text was absent or
  incomplete. The OCR title was checked against the record; the 1986 article
  begins part-way through a page containing the end of another article.
  Title checks do not verify every page, the DOI in every scan, or whether a
  version is identical to the journal's final publication. The image-only
  scans do not yet have usable searchable full text.
- The 1985 *Nature* link matched its bibliography item but returned HTTP 404;
  this is a retrieval failure, not evidence that no copy exists.
- The existing held Dai et al. 2023 PDF (`W4319812171`) also illustrates why
  first-page checks are insufficient: its HAL cover page extracts correctly,
  but much of the subsequent embedded text is garbled. This observation does
  not establish how often that problem affects the collection.

## Next action

Agree the handover and allowed acquisition route with the References owner,
then import the individually accepted files using a provenance-preserving,
locked library operation and refresh the index. Preserve `no_text`/OCR-derived
text distinctions; do not label image scans `ok` merely because an OCR title
matched. Before broadening, check author identity and title/DOI collisions,
verify the source and rights metadata per file, deduplicate against the live
manifest, and respect publisher TDM restrictions. Separately, a bounded audit
of extraction quality beyond the first page could identify searchable texts
that are garbled; do not interpret this single example as a collection-wide
failure rate.
