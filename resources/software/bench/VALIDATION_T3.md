# Tranche 3 validation: declared tests

Declared by Claude (Opus 5.5) on 24 October 2026, before any of these tests
was run (probes of the interfaces excepted). Results go in `results/t3/`; this
file is not edited after the runs except to append dated amendments.
Environments: `eprp-sw/bench-r3:t3` ([Dockerfile](env/Dockerfile.r3): the
tranche-2 image plus palaeoverse, fossilbrush, chronosphere, sf and h3jsr from
the CRAN snapshot of 2026-10-22) and `eprp-sw/bench-py3:t3`
([Dockerfile](env/Dockerfile.py3): pygplates 1.0.0). [Detail withheld pending
disclosure to the data custodian.]

## palaeoverse

Synthetic occurrences for V1–V4: 20,000 occurrences with maximum age uniform
on (0, 538.8) Ma and duration exponential with mean 5 Myr (minimum age
clipped at 0); 500 taxa assigned at random; bins `time_bins(rank = "stage",
scale = "GTS2020")`.

**V1. `bin_time` "mid" and "majority".** Truth computed independently:
the bin containing the midpoint; the bin with the largest overlap. Pass: every
occurrence agrees with the truth (cases with two bins of equal overlap, of
measure zero, are excluded and counted).

**V2. `bin_time` "random".** 200 replicates. Truth: each bin an occurrence
overlaps is drawn with equal probability. Pass: pooled over occurrences
overlapping 2–5 bins, a chi-square test of drawn counts against equal
probabilities has p > 0.001.

**V3. `bin_time` "point" (uniform).** 200 replicates. Truth: the
probability of each overlapped bin is its share of the occurrence's range.
Pass: chi-square p > 0.001 against those shares, pooled as in V2.

**V4. `tax_range_time`.** Pass: every taxon's FAD and LAD equal the maximum
of its maximum ages and the minimum of its minimum ages, to 1e−9.

**V5. GTS2020 table (characterisation).** `palaeoverse::GTS2020` stage
bases against the ICS chart v2024/12 values in the timescale entry's table,
matched by name: every difference larger than 0.001 Myr is listed. GTS2020
and the 2024/12 chart are not identical, so there is no pass criterion.

**V6. `palaeorotate` against pyGPlates.** 300 public PBDB collections
drawn at random (seed 7) from the public snapshot; ages 10, 50, 100, 200,
300 and 400 Ma; models MERDITH2021, PALEOMAP, TorsvikCocks2017 and
MATTHEWS2016_pmag_ref. Three routes: (a) `palaeorotate(method = "point")`
(the GPlates Web Service); (b) `method = "grid"` (Jones & Domeier 2024
files, resolution 3); (c) pyGPlates on the mirrored model files: the point
takes the plate of the static polygon containing it at 0 Ma and is rotated
to the age, the method of the data catalogue's profiler. All three are
GPlates software, so this checks consistency of model files and plate
assignment, not independent rotation code. **Pass:** for points that both
(a) and (c) reconstruct, the great-circle distance between them is at most
0.1° for at least 95% of point–age–model combinations, in each model.
Reported without criteria: (b) against (c), and the spread of palaeolatitude
across the four models by age (lead L-010).

## fossilbrush

**F1. `check_taxonomy` on injected errors.** A synthetic taxonomy of 400
genera, 60 families, 15 orders and 5 classes in one phylum, names built from
random syllables, 5,000 occurrences. Injected: 30 genus misspellings (one
letter substituted, in 1–3 occurrences each); 30 genera given a second,
conflicting family in a minority (10–30%) of their occurrences; 10 names
with a digit or punctuation. Reported for each error type: recall (fraction
of injected errors that the report flags) and false positives (flags on
names or genera with no injected error). Pass criteria: recall at least 0.9
for each of the three types.

**F2. `flag_ranges` on injected outliers.** Reference ranges: the FAD and
LAD of each of the 500 V-series taxa. Test data: the 20,000 occurrences
(all inside their taxon's range) plus 50 occurrences shifted 10–30 Myr older
than their taxon's FAD and 50 shifted 10–30 Myr younger than its LAD.
`flag.diff = 5`. Pass: all 100 injected occurrences flagged, and none of the
20,000 originals.

## chronosphere

[Detail withheld pending disclosure to the data custodian.]

## Amendments

**A1, 24 October 2026, after smoke runs and before the full run (Claude,
Opus 5.5).**
- **Synthetic occurrences (V1–V4, F2) changed.** As declared, 500 taxa
  drawn at random across 0–538.8 Ma each spanned nearly the whole
  Phanerozoic, so most "younger than LAD" injections in F2 were clipped at
  the present. Now: each taxon originates uniformly in 20–538.8 Ma and lasts
  an exponential time of mean 20 Myr (ending no later than 0.5 Ma); each
  occurrence's age range (exponential width, mean 5 Myr) is centred on a time
  inside its taxon's range. F2's older injections are drawn from taxa with
  FAD ≤ 500 Ma and its younger ones from taxa with LAD ≥ 35 Ma, so shifted
  ages stay within 0–538.8 Ma. Criteria unchanged.
- **V5:** the chart table prints values such as "174.7±0.8" and "~237"; the
  leading number is used. palaeoverse documents its GTS2020 table as compiled
  from ICS chart v2020/03, so V5 also compares it with chart v2020/01 (the
  RDF's last release, `isc_boundaries_by_version.tsv`); still no criterion.
- **Disclosed from the smoke run, before the full run:** fossilbrush's
  `flag_ranges` compares its differences with `flag.diff` as text (its
  difference vectors are created as copies of a character vector), and
  measures occurrences beyond a taxon's LAD from the reference FAD. F2 is run
  as declared; the write-up will also report the flags a numeric comparison
  of the returned differences gives (post hoc). `tax_range_time` rounds its
  output to three decimals (its source), so V4's 1e−9 criterion is expected
  to fail by rounding; it is run as declared.
