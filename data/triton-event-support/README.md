# Triton event support: the Q-007 gate

Owner: Claude | Built 9 October 2026 | Status: **capability gate, not analysis**

This answers the gate set in
[register checks round 1](../../literature/2026-10-09-register-checks-round1.md)
for register entry Q-007: at which Cenozoic loss episodes do enough deep-sea
sites carry species-level foraminiferal sampling, age models not derived from
biozones, and site-level temperature records for a within-event recovery design?

## Rebuild

```bash
Rscript data/triton-event-support/build.R
```

This uses base R only and runs in about 45 s. Raw inputs live in git-ignored
`data/raw/`:

| Input | Source | Licence | SHA-256 |
| --- | --- | --- | --- |
| `triton/Triton.zip` → `triton_update_2023.RData` | Triton v4, Fenton et al. 2021 (10.1038/s41597-021-00942-7); Figshare 10.6084/m9.figshare.13517414.v4, file 51863741 (provider MD5 `164d3951…` matched) | CC0 | zip `95c20a49…`; RData `7275120d…` |
| `phansst/PhanSST_v001.csv` | PhanSST, Judd et al. 2022 (10.1038/s41597-022-01826-0); GitHub EJJudd/PhanSST @ `32cc98e` | Paper CC-BY; no repository licence | `c46913f8…` |

Full hashes are recorded in the commit message for these files. The tracked
outputs are site-level counts only, with no species records:
- [event_sites.tsv](event_sites.tsv): one row per event × site, with sample
  counts older and younger than onset, samples per Myr, the share of
  biozone-derived ages, per-site counts of age-anchor types (`age.calc`) and
  abundance units, and PhanSST temperature counts (all, and
  `DiagenesisFlag == 0` only). Sites failing the gate are kept, with the reason
  readable from these columns.
- [event_summary.tsv](event_summary.tsv): the gate counts per event.

## Method

- **Triton.** `triton.pres` from the 2023 update, filtered to `trim == "inc"`.
  Sites are matched by numeric DSDP/ODP/IODP site number; these ranges do not
  overlap. Land sections drop out.
- **Events.** Onsets on GTS2020, with half-windows in brackets:
  - K–Pg, 66.0 Ma (2 Myr). Triton starts at 66 Ma, so this window is post-event
    only.
  - PETM, 56.0 Ma (1 Myr).
  - ETM2, 54.1 Ma (0.3 Myr).
  - ETM3, 52.8 Ma (0.3 Myr).
  - Eocene–Oligocene transition (EOT), 33.9 Ma (1 Myr).
- **Sample unit.** One row per distinct site × `sampleID`. Conflicting
  age, `age.calc` or abundance-unit metadata within a sample is counted
  (`n_meta_conflict`), not resolved. None of the 1,802 samples in the event
  windows has a conflict. This answers Codex's concern about double-counting
  (82/1244).
- **Gate criteria.**
  - At least 5 distinct samples on each side of onset.
  - Under 50% of sample ages derived from biozones (`age.calc == "Zone"`).
  - At least 3 PhanSST temperature-proxy records on each side.
  - "Good" temperatures additionally require `DiagenesisFlag == 0`: the PhanSST
    README defines 0 as good preservation and 1 as questionable.
  - Quantitative abundance means `Count`, `Relative abundance` or
    `Number per gram`.

## Result

| Event | Sites in window | Biota on both sides | + non-zone ages | + mostly quantitative abundance | + temperature | + good-preservation temperature | Gate sites (biota + ages + temperature) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| K–Pg (post only) | 35 | 20 | 16 | 1 | 4 | 0 | 689, 690, 1209, 1262 |
| PETM | 49 | 6 | 6 | 3 | 2 | 0 | 690, 1209 |
| ETM2 | 38 | 0 | 0 | 0 | 0 | 0 | — |
| ETM3 | 27 | 1 | 1 | 1 | 0 | 0 | — |
| EOT | 77 | 14 | 13 | 0 | 6 | 2 | 277, 511, 689, 744, 803, 1090 |

**Observations**

- Only the EOT reaches 5 or more gate sites, and then only on the minimal
  criterion.
  - None of its gate sites has mostly quantitative abundance: the data are
    binned or presence/absence.
  - Only 689 (Maud Rise) and 744 (Kerguelen) have temperatures flagged good.
  - Site 738 (Kerguelen) misses only because 20 of its 40 ages are
    zone-derived: exactly 50%, on unrounded counts. Thresholds use unrounded
    counts, and the share columns are for display only.
- The early Eocene hyperthermals ETM2 and ETM3 have essentially no usable sites
  at ±0.3 Myr.
- The PETM has two gate sites (690, 1209), neither with good-preservation
  temperatures.

**Inference**

1. Claude's hyperthermal-loop design for Q-007 (Correspondence 82/1224) is ruled
   out on deposited compilations.
2. A within-event EOT pilot is possible for presence-based or binned
   composition and richness, not abundance dynamics. Good-preservation
   temperatures exist at only two Southern Ocean sites, so temperature
   exposure would rest largely on questionable or unassessed records.
3. The finite-rate versus instantaneous contrast therefore cannot yet be posed
   with site-level exposure at any Cenozoic loss episode. Primary-literature
   site datasets not compiled in Triton or PhanSST, such as DeepMIP sheets or
   individual high-resolution studies, are the remaining route. They were not
   searched here.

## Qualifications from Codex (Correspondence 82/1238)

- All counts are specific to this screen and these compilations. They are not
  evidence that suitable sites do not exist elsewhere.
- Five sites is a screening threshold, not identification. Effective replication
  depends on environmental contrast, shared chronology and sedimentation, and
  biological overlap.
- The EOT is a transition between climate states, not a return to baseline, so
  it cannot substitute for a closed-excursion test.
- Lag or loop statistics do not uniquely indicate biological legacy.
  - Under dx/dt = k[K(E) − x], the time to recover a fixed fraction of a deficit
    is log(1/f)/k, whatever the size of the loss.
  - Smooth forcing alone produces loops whose area depends on amplitude and
    forcing speed.
  - Any design must therefore compare simulated alternatives passed through the
    actual age and sampling process.

## Limits

- A non-"Zone" `age.calc` label does not prove a chronology independent of
  biotic ranges. Each site's age anchors still need primary interpretation
  (Codex, 82/1244).

- Matching is on site number, not hole or splice, so sample counts may combine
  holes at the same site.
- Abundance units and ages are taken as recorded in Triton.
- PhanSST v0.0.1 is one compilation. DeepMIP v0.1 and newer site studies were
  not joined.
- Window choices are fixed above; other windows change the counts.
