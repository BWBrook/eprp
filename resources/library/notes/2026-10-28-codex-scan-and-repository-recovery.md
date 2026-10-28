# Open-copy and scan recovery, 28 October 2026

Codex took over the library following Claude's handover on the EPRP board
(76/2444–2445). This tranche used university-hosted open copies and the
existing private store; no Wiley TDM text was brought into an agent session.
The [candidate receipt](../review/2026-10-28-codex-question-list-repositories.tsv)
records source URLs, versions, hashes and verification.

## Added and corrected

- Patiño et al. 2017, the 50 island-biology questions: the published copy from
  the University of La Laguna. No licence for reproducing the question wording
  in Git was established. Fifty numbered candidates were captured privately
  for subsequent checking; see [the agenda note](question-agendas.md).
- Kiessling et al. 2019, conservation questions and palaeontological data:
  the accepted manuscript from the Oxford Research Archive, under its terms.
- Sutherland et al. 2013, 100 fundamental ecological questions: the accepted
  manuscript from the Warwick Research Archive, under its stated research-use
  terms. It supersedes the catalogue's TDM-only status. The pre-existing Wiley
  TDM PDF and extraction remain under `tdm/`, with their hashes unchanged and
  their earlier manifest record retained.
- O'Reilly and Donoghue 2021, fossilization and tip-calibrated divergence
  times: the previous `no_text` PDF was visually checked and found to be a
  single plot, not the article. It was retained under `quarantine/rejected/`;
  the full 11-page article was imported from an author-affiliated Bristol
  site. Both hashes and the rejection/import history were checked.
- The 349-page book *Artificial Earth* was marked `no_text` because its early
  pages yielded little embedded text. Its title is present within the first
  15 pages, and a fresh extraction matches the existing 714,965-byte text;
  it is now correctly marked `ok`, without changing either original file.

## OCR

Twenty open scans, totalling **322 pages**, received separate machine OCR:
`W1966077680`, `W1970741654`, `W1976474576`, `W1977126382`,
`W1991129334`, `W1991750000`, `W1998804687`, `W2010154591`,
`W2028095175`, `W2030169181`, `W2039087123`, `W2046967232`,
`W2057220513`, `W2084849445`, `W2088655444`, `W2107127140`,
`W2143497948`, `W2258629589`, `W2274199726`, and `W3095349119`.
The last is Portuguese and used Tesseract's Portuguese language model; the
others used English. For each work, `ocr/<W>.json` records the source and OCR
hashes, title check, page-level word counts, engine and script. Source PDF and
original extraction hashes were verified unchanged after processing. The
Portuguese language model's SHA-256 is in its receipt.

OCR passed identity and minimum text-coverage checks, not a full transcription
audit. Reading order, figures, tables and individual words still need checking
against the scan before supporting a precise claim. One source with a
three-column layout was visually inspected. The per-run source-hash records,
first-page preflight and isolated pilot remain at
`deep-server:/data/codex/artifacts/eprp/library-ocr-20261028/`.

The 19 English scans plus the Portuguese scan account for 20
records; the two other previously `no_text` records are the corrected figure
and book above. `reject-incomplete` keeps rejected content quarantined and
requires a reviewed replacement; ordinary fetch cannot silently reacquire it.
Unit tests cover these paths, and an independent Codex review identified and
confirmed the repair of an automatic-refetch loophole.
