# Missing-reference metadata recovery, 28 October 2026

All **58 original missing reference IDs** now have a separately recovered
provider citation. They affect **1,266 original register rows and 96 distinct
sample IDs**. The original interval sheets and assembled database were not
changed. Their missing-reference flags still describe the original exports;
the [overlay](reference-recovery-overlay-2026-10-28.json) is an explicit later
join by `ref_no`, not a replacement reference sheet.

## Evidence and exceptions

The public Fossilworks reference search form explicitly accepts an
"EcoRegister ID number". Ordinary GET requests to
`https://fossilworks.org/?a=getRefs&ref_no=ID` returned an unambiguous full
citation ending in `[ER ID]` for **57 IDs**. Every corresponding original
sample ID occurred in the reference page's sample links. The full 58-page
attempt, including the unsuccessful page, is retained in the
[initial evidence manifest](reference-recovery-evidence-2026-10-28/manifest.json).
Requests were sequential with at least one second between them, without
authentication or bulk-export endpoints.

For **4414**, the reference search returned HTTP 200 with "No matching
references were found", although its footer named Christophel et al. 1992.
The footer alone did not qualify for recovery. The ordinary
[sample 4697 page](https://fossilworks.org/?a=sampleResults&sample_no=4697)
supplied an explicit `Sample no: 4697` and a full citation ending `[ER 4414]`:
Christophel, Scriven and Greenwood (1992), *An Eocene megafossil flora from
Nelly Creek, South Australia*, *Transactions of the Royal Society of South
Australia* 116(2):65–76. That exact sample/reference pairing supports the
recovery. Its [separate receipt](reference-recovery-supplement-2026-10-28/manifest.json)
and the initial unsuccessful reference-page result remain in the overlay.
The difference between the reference and sample routes is observed provider
behaviour; its internal cause has not been established.

The collector preserves original response bodies, URLs, request/completion
times, status, response headers, sizes and SHA256 hashes. The overlay's
citation text decodes HTML entities and collapses rendered whitespace;
the response bodies preserve original bytes. It records supporting sample
links and does not infer biological independence. The snapshot cohort is
pinned by the [input extract](reference-recovery-input-2026-10-28.json), whose
row IDs retain the original source-file/data-row keys.

## Bibliographic accuracy remains separate

Provider metadata recovery is not verification of the paper or its specimen
counts. The [bibliographic annotations](reference-recovery-bibliographic-checks-2026-10-28.json)
preserve these selected checks separately:

- **4030:** the provider prints `J. Hirs` and **2015**. The same title,
  journal, volume, issue, other authors and page range identify the
  [journal's Hidas paper](https://hrcak.srce.hr/en/314667), published **2024**,
  DOI **10.4154/gc.2024.03**, by János Hir, Márton Venczel and Krisztina
  Sebe. Expose the journal year/name alongside the provider values rather
  than overwriting them. Crossref's registered metadata independently gives
  2024 but itself has pages `15-18` and affiliation strings among authors;
  the journal landing page gives `15-28`. No wholesale metadata substitution
  is justified.
- **3996:** the provider's **2015** agrees with the registered online date,
  **22 October 2015**, while volume 90(1):101–123 has registered print date
  **March 2016**, DOI **10.1007/s12542-015-0275-3**. Both date conventions
  are retained; 2015 is not labelled an established error.
- **4414:** a BHL search result agrees with the recovered citation, but a
  direct BHL GET returned HTTP 403 and browser retrieval timed out. This is
  an access limit. The ID-to-citation recovery relies on the provider's full
  sample page, not that discovery result.

The [bibliographic evidence manifest](reference-recovery-bibliographic-evidence-2026-10-28/manifest.json)
records two complete Crossref responses, the journal landing page and the
failed BHL request. Receipt headers omit `Set-Cookie`. No source full text was
read for these bibliographic checks, and public access does not establish
new redistribution rights.

## Reproduction and verification

The original database is
`deep-server:/data/paleodata/fossilworks/derived/2026-10-28-assembly-v1/fossilworks.sqlite`,
SHA256 `ae1fdeb113ade4a72d9fd23a08d9082720c308d0b0c593f6bf9fb4ed36861610`.
Its hash matched before and after this work. Remote operations were read-only;
the input extract travelled over stdout and all recovery outputs were written
in the local checkout.

From the repository root, rebuild the overlay offline to a **new** path:

```sh
python3 resources/sources/fossilworks/reference_recovery.py build \
  resources/sources/fossilworks/profile/reference-recovery-input-2026-10-28.json \
  resources/sources/fossilworks/profile/reference-recovery-evidence-2026-10-28 \
  NEW-OVERLAY.json \
  --supplement resources/sources/fossilworks/profile/reference-recovery-supplement-2026-10-28
python3 -m unittest discover -s resources/sources/fossilworks -p test_reference_recovery.py -v
```

`extract-input DATABASE NEW-INPUT.json` recreates the cohort from a verified,
read-only local copy of the pinned database. Use output `-` for stdout.
`collect INPUT.json NEW-DIRECTORY` performs a fresh sequential reference-page
collection; `collect INPUT.json NEW-SUPPLEMENT --missing-from DIRECTORY`
queries an original sample page only for initially unresolved IDs. Fresh
responses are later observations and need not have the retained hashes.

The offline builder checks cohort cardinality, the manifest's input hash,
individual receipt equality, every used response's size/hash, exact citation
IDs and supporting sample IDs. It refuses an existing output. Ten tests cover
wrong IDs, duplicate citations, login/error pages, missing or mismatching sample
identity, the pinned database requirement, overwrite refusal, retained-data
replay, altered evidence and removal of `Set-Cookie` from future receipts.
The retained overlay rebuild is byte-identical.

The integration and bounded original count-table checks are described in the
[annotation record](../annotations.md). Full citation auditing remains separate;
none of these recoveries validates ecological abundance or explains the source
export omissions.
