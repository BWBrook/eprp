# Fossilworks count-based question feasibility, 28 October 2026

[Detail withheld pending disclosure to the data custodian.]

## Replay

Run from the EPRP checkout; output goes to the local shell's redirection target:

```sh
ssh -o BatchMode=yes -o ConnectTimeout=8 deep-server python3 -W error::ResourceWarning - \
  /data/paleodata/fossilworks/derived/2026-10-28-assembly-v1/fossilworks.sqlite \
  /data/paleodata/fossilworks/derived/2026-10-28-annotations-v1/fossilworks-annotations.sqlite \
  < data/fossilworks-ideation-20261028/profile_counts.py \
  > /tmp/fossilworks-ideation-replay.json
cmp data/fossilworks-ideation-20261028/aggregate-profile.json /tmp/fossilworks-ideation-replay.json
```

Two initial executions produced identical JSON. A subsequent replay with
explicit connection closure and `ResourceWarning` promoted to an error also
matched. Aggregate JSON SHA256:
`6ef1f7005114da856ad7923b4c5cdaac905b6b1c9a378aac6e0c9170185f66a1`.
Separate exploratory SQL queries agreed on sample counts, age anomalies,
size/richness medians, source/coordinate reuse and key candidate strata.
These are implementation and descriptive checks, not biological validation.

## What the resource supports

There are 1,675 exact sample IDs in 1,697 source summaries. The 22 repeated
summaries match in every field except source row ID: the script proves that
before using one representative for descriptive summaries. All 26,046
register records remain in sums, including repeated taxon keys. No sample ID
recurs across selected interval exports. Biological independence does not
follow: 696 IDs share exact coordinates in 232 groups; 935 IDs belong to
287 references containing multiple samples. There are 38 repeated
sample/genus/qualifier/species keys with 39 excess register rows; combining
these requires interpretation, not automatic deduplication.

- Median count sum is 140 (IQR 40–537); 720 samples have at least 200 units,
  439 at least 500, and 258 at least 1,000. These are sums of source counts,
  potentially mixing operational units. Provider richness has median 12
  (IQR 7–20), maximum 129; it is not an independently harmonised species count.
- Strong coverage is terrestrial and Cenozoic: 359 Holocene and 336 Late
  Pleistocene samples; ungulates occur in 1,072 samples and rodents in 1,031.
  There are 96 recorded countries, led by the United States (362), Spain
  (164), and France (136). All coordinate strings are nonempty; their numeric
  validity and accuracy were not tested, and they are not palaeocoordinates.
- Only 58 register rows have a reviewed unit assignment; primary-source
  checking covers 26 rows in two samples, both with mixed counting protocols.
  No globally comparable abundance matrix is established. The documented
  eight large-mammal rows from Ein Gev share a table protocol; they do not
  constitute a cross-site community-abundance validation set.
- Context retrieval finds human accumulation in 493 sample IDs, carnivore
  accumulation in 106, bird accumulation in 86, pitfall in 55, and cave in
  333; 485 IDs have blank context. These categories overlap. Sampling methods
  include quarry (535), quarry plus screenwash (450), screenwash (255), and
  blank (331); labels do not establish equivalent mesh sizes or effort.

Age information is a major limitation. There are 1,383 valid numeric bound
pairs, 291 samples missing at least one bound, and one reversed pair:
sample 4918, PAM 207, has `max Ma=9.11`, `min Ma=9.79`, `Ma=9.45`.
It is flagged without repair. Valid envelope width has median 0.1173 Ma
(IQR 0.002632–1.39 Ma); 630 samples have width at most 0.1 Ma and 256
at most 0.001 Ma. These are reported age envelopes, not measured durations
of accumulation. Six zero-width pairs do not establish instantaneous deposition.
Among 1,263 within-reference pairs with valid bounds, 702 strictly overlap
and 561 have identical bounds, including zero-width pairs; these counts overlap.
Bounds are not age probability distributions.

## Question-specific opportunities

All candidates below are proposals. Original protocols, taxonomic mapping and
nearest-prior checking remain outstanding; the source citation titles already
show that several broad ecological and taphonomic questions have been studied.

**Can a fauna retain its species while replacing its dominant ecological
structure?** Counts can distinguish taxon replacement from abundance
redistribution among persisting taxa, which occurrence-only turnover cannot.
Candidate local series include Cheremukhovo-1 (ref 3798: 11 beds,
124–5,282 units, richness 12–29), Boomplaas (3779: 13 samples,
51–1,888 units, richness 12–24), and Sehonghong (3742: 11 samples,
25–1,668 units, richness 8–39). Compare persistent-taxon concentration,
rank reversals and turnover after coverage control; use section-level
replication rather than treating beds as independent sites. A strong rival
is changed accumulator or recovery protocol. Boomplaas explicitly changes
recorded accumulator combinations and is therefore a discrimination case,
not a clean climate trajectory. At Cheremukhovo, six Holocene beds share
0–11.7 ka bounds and four Pleistocene beds share 25.15–31.5 ka bounds:
stratigraphic order and source age models are necessary before any trajectory
or lead–lag claim. No universal tipping threshold follows from rank shifts.

**Is regional rarity caused by low local representation, or by concentration
into a few locally dominant populations?** Joint count and occupancy structure
distinguishes these alternatives even when regional incidence is the same.
Regional rodent starting pools include France Early Miocene (23 samples,
14 references), Spain Middle Miocene (16/11), Spain Early Miocene (13/7),
and Spain Late Miocene (13/10). The aggregate JSON supplies the exact queried
counts; these are raw support pools, before comparability exclusions.
Use taxon-specific within-sample representation and spatial occupancy,
stratified by protocol and reference; simulate finite sampling and
preservation-specific detection as rival explanations. A concentrated
distribution is compatible with refugia but does not itself establish
rescue, immigration, population abundance or an impending extinction.

**Is apparent long-term ecological homogenisation a loss of species, or a
convergence of dominance among species that remain geographically distinct?**
This asks for both incidence and abundance-weighted between-sample
dissimilarity, together with within-sample concentration. A bounded deep-time
design could compare regional mammal/rodent assemblages across broad bins,
starting from the France/Spain pools above and US Eocene–Oligocene pools
(23 Early Eocene, 19 Middle Eocene, 21 Early Oligocene rodent samples).
It cannot resolve a sharp Eocene–Oligocene event: late Eocene rodent support
is only one French sample, three Spanish and three US samples. Spatial
footprint and time-averaging changes are strong rivals; common broad age
bounds cannot be treated as simultaneous communities.

**How much apparent ecological organisation is created by the route into the
fossil assemblage?** Source-controlled replication can test whether
concentration and taxon covariance exceed finite subsampling of one common
composition. Mas-de-Pauffié (2390) has nine screenwashed samples,
7–81 units and richness 2–9, all with identical `Ma=26.5` and no bounds;
the provider also labels them Early Oligocene. This is a candidate replicate
heterogeneity design, not a time series, and the original source must resolve
sample relationships and chronology. Brule Lower Nodular Zone (4473) has
nine surface collections, 47–529 units and richness 7–26, all with identical
`Ma=33.41` and missing bounds; eight have overbank and one lake context.
Their collection areas and nesting must be checked before spatial tests.
The nine Turkish ref 4050 samples have 11–534 units and identical
23.2–23.4 Ma envelopes; their shared dating is insufficient to infer succession.

Bluegrass supplies a particularly clear sampling-control lead: macro and micro
samples 3423/3424 share reference 3135 and age bounds, both with reported
richness 40, yet count sums are 1,107 and 169. Ungulate representation is
582 versus 22 units, rodents 115 versus 61, turtles 65 versus five. The same
richness can mask radically different counted composition. This is not a
biological contrast until material selection, counting units and overlap of
the two fractions are established from the paper. It is a useful control
for the other proposed biological questions.

Ref 3701 is a **candidate on hold**, not a ready chronological series. Ten
entries are Kiowa levels 3–12; only one is Yuku, a pooled levels 6–7 entry.
All carry `human accumulation,rock shelter` and sampling method `quarry`.
The parent Codex's source check reports disturbed Yuku chronology, cranial
NISP bias and hand collection; those qualifications require retaining the
hold even where provider bounds appear precise. The provider labels and
bounds below are reported literally; their chronological consistency has
not been resolved here.

| Sample ID | Provider sample | Provider interval | Ma | min Ma–max Ma |
| --- | --- | --- | --- | --- |
| 3896 | Kiowa Level 3 | Holocene | 0.00535 | 0.00484–0.00586 |
| 3897, 3898, 3900 | Kiowa Levels 4, 5, 6 | Holocene | 0.006115 | 0.006035–0.006195 |
| 3899, 3901 | Kiowa Levels 7, 8 | Holocene | 0.008473 | 0.0081–0.008846 |
| 3902 | Kiowa Level 9 | Holocene | 0.009073 | 0.008846–0.0093 |
| 3903, 3904 | Kiowa Levels 10, 11 | Pleistocene - Holocene | 0.00961 | 0.0093–0.00992 |
| 3905 | Kiowa Level 12 | Late Pleistocene | 0.010322 | 0.010233–0.01041 |
| 3906 | Yuku Levels 6–7 | Late Pleistocene | 0.014135 | 0.01394–0.01433 |

## Boundaries and next action

The 116 Campanian/Maastrichtian samples and 51 Palaeocene samples do not
make a global K–Pg community trajectory. For example, Hell Creek contributes
22 Maastrichtian samples (7,198 units) but only four Early Palaeocene samples
(229 units); broad formation identity is not a matched before/after design.
There are only 23 samples containing leaf rows, mostly scattered Cenozoic
sites, not a replicated plant–vertebrate recovery transect.

The highest-value next tranche is primary-source review of a few contrasting
series and replication sets, chosen against a biological hypothesis. Start
with one local dominance/turnover series, one deep-time regional rodent pool,
and Bluegrass as the sampling control. Establish source protocols and sample
relationships before fitting. Counts make several scientific contrasts
possible; the present evidence establishes source support, not novel hypotheses
or ecological identifiability. For candidate dispositions and register integration see the
[ideation brief](../../ideas/2026-10-28-fossilworks-count-questions-codex.md).
