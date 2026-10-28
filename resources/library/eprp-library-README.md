# library: EPRP literature store

Metadata and open-access full texts for the EPRP literature library
(Extinction and Paleontology Research Programme). The conventions, tiers,
access policy and tool are in the private repository `BWBrook/eprp` under
`resources/library/`. This file is a copy of
`resources/library/eprp-library-README.md` there.

## Layout

```text
openalex/<W>.json      full OpenAlex record for work W (metadata, abstract index, references)
pdf/<W>.pdf            open-access full text (read-only)
text/<W>.txt           plain text extracted from pdf/<W>.pdf
ocr/<W>.txt            separately generated machine OCR for open scans
ocr/<W>.json           OCR provenance, page coverage and source/output hashes
quarantine/            downloaded PDFs that failed the title check; not part of the library
quarantine/withdrawn/  copies removed with a recorded reason
tdm/<publisher>/       publisher text-and-data-mining copies (pdf/, text/): local search and mining only
manifest.tsv           provenance of each stored or withdrawn copy: URL, host, version, licence, sha256
attempts.tsv           every download attempt and its outcome
aliases.tsv            seed keys (doi:..., pmid:..., merged ids) mapped to OpenAlex ids
unresolved-keys.tsv    seed keys that OpenAlex lacks
_tools/                the deployed library.py and its seed lists
_provenance/           read-only working files of the curated seed tiers
```

## Rules

- Full texts are private copies of openly available works, for EPRP agents'
  reading and search. Do not redistribute them. Each one's licence, as
  OpenAlex reports it, is in `manifest.tsv`.
- Copies under `tdm/` came through publisher TDM licences. Scripts may mine
  them locally. Until UTAS Library confirms the licences allow it, do not
  read their text in an AI agent session, and that includes grep output;
  counts and aggregates are fine. Delete them when the project ends.
- Change `pdf/`, `text/`, `ocr/`, `tdm/` and `manifest.tsv` only through `library.py`. To
  remove a copy, run `python3 _tools/library.py withdraw W --reason TEXT`.
- To rebuild a text file, run `pdftotext -enc UTF-8 pdf/W.pdf text/W.txt` (or the same under `tdm/<publisher>/`).
- `python3 _tools/library.py ocr W` processes a selected open scan, preserving
  its original PDF and extraction. Machine OCR is searchable but not a
  verified transcription; use the PDF to check wording, figures and tables.
- The library search index combines open extracted and OCR text. Map a `W`
  id to its work with `openalex/<W>.json` or the repository's `works.tsv`.

Maintained by EPRP agents (Claude, Codex) for Barry W. Brook. Created
23 October 2026.
