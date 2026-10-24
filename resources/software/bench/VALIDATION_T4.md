# Tranche 4 validation: declared tests

Declared by Claude (Opus 5.5) on 24 October 2026, before any estimator was
run on the generated records. Results go in `results/t4/`; this file is not
edited after the runs except to append dated amendments.
Environments: `eprp-sw/bench-r4:t4` ([Dockerfile](env/Dockerfile.r4): the
tranche-3 R image plus iNEXT 3.0.2 from the CRAN snapshot of 2026-10-22 and
DeepDiveR 0.1.0 at GitHub `b1592de`) and `eprp-sw/bench-py4:t4`
([Dockerfile](env/Dockerfile.py4): DeepDive v.1.0.28 with TensorFlow 2.15.1,
pinned because DeepDive's `setup.py` leaves TensorFlow and Keras unpinned).

## Generator (independent of every estimator, including DeepDive's simulator)

[validate/t4_generate.R](validate/t4_generate.R). Time runs from 100 Ma to
0 in 20 bins of 5 Myr (bin 1 is 100–95 Ma). Species come from paleobuddy
`bd.sim` with 400 starting species and λ = μ = 0.05 per Myr. Eight areas lie
in a row; each species occupies a contiguous block of 1 + Geometric(0.5)
areas from a uniform start, truncated at area 8. Each species has a fixed
z ~ N(0, 1) and, in bin b, abundance exp(σ_b·z). The number of collections
per area and bin is Poisson(10 · w_a · s_b), with w_a lognormal(0, 0.5) per
area and replicate, and each area–bin independently has no collections with
probability 0.15. A collection draws 40 individuals, multinomially, from the
species alive in its area during the bin, weighted by abundance × the
fraction of the bin the species was alive. An occurrence is a species
present in a collection. Truth per bin: global richness (species alive at
any time in the bin) and sampled-area richness (alive in the bin in an area
that has at least one collection that bin).

Three scenarios, 20 replicates each (seed 4000 + 1000·scenario + replicate):
- **S, sampling:** σ_b = 1; s_b = 1 in bins 1–10 and 0.3 in bins 11–20.
  True richness is stationary in expectation; effort falls by 70%.
- **E, evenness:** s_b = 1; σ_b = 0.5 in bins 1–10 and 2.0 in bins 11–20.
  True richness is stationary in expectation; the abundance distribution
  becomes much less even.
- **M, mass extinction:** σ_b = 1, s_b = 1; at 50 Ma (the bin 10–11
  boundary) each living species survives with probability 0.4, after which
  λ = 0.07 (a second `bd.sim` started from the survivors).

**Pilot disclosed.** The parameters were set from a pilot that ran only the
generator and [validate/t4_pilot.R](validate/t4_pilot.R) (occurrence counts
and Good's u = 1 − occurrence singletons / occurrences; no estimator). With
λ = μ = 0.15 and 20 individuals per collection, true richness drifted 35%
between halves and the low-effort bins of scenario S fell to u = 0.48, below
any usable quorum, so SQS would have failed by construction. With the
settings above, replicates 1–4 of scenario S (the same seeds as the run)
gave u ≥ 0.70 in every low-effort bin (mean 0.80) and ≥ 0.92 in the others.

## Estimators (per bin)

- Raw sampled-in-bin richness, and range-through richness (divDyn `divDyn`).
- Chao2 from divDyn `indices` (taxon vector of the bin's occurrences) and
  from iNEXT `ChaoRichness` (incidence frequencies, T = collections in the
  bin).
- Squares from divDyn `indices`.
- SQS: divDyn `subsample(type = "sqs", q = 0.6)`, 100 iterations, defaults
  otherwise (Good's u, occurrence singletons, dominant taxon kept),
  sampled-in-bin richness.
- iNEXT coverage-standardised richness: `estimateD(datatype =
  "incidence_freq", base = "coverage", level = 0.6, q = 0)`.
- DeepDive: DeepDiveR `prep_dd_input` (Region = area, Locality = collection,
  MinAge and MaxAge the bin edges, `age_m = "median"`, r = 1, since ages are
  known to the bin) and `create_config` (8 regions, autotune on, no present
  diversity, defaults otherwise: 10,000 training and 100 test simulations,
  LSTM 64-32, dense 64-32). One model per scenario is trained by
  `run_dd_config.py` on the config autotuned to replicate 1, then applied to
  all 20 replicates with DeepDive's `predict_from_config`. Under these
  defaults DeepDive returns a point prediction (one model, no dropout, and
  one age replicate), so no interval coverage is assessed.

## Tests

**K1. squares implementation.** divDyn's squares against an independent
implementation of Alroy (2018), S + S₁²·Σn²/(N² − S₁·S), on every bin of
every replicate. Pass: equal to 1e−9.

**K2. Invariance to sampling intensity (scenario S).** For SQS and for the
iNEXT coverage estimate: the log ratio of the mean estimate over bins 11–20
to the mean over bins 1–10, minus the same log ratio for true global
richness, averaged over the 20 replicates. These methods are designed to
remove the effect of sampling intensity. Pass: |mean bias| ≤ 0.10 for each,
separately.

**Reported without criteria:**
- the K2 bias for every estimator in scenarios S and E (Alroy 2026 argues
  that coverage-based rarefaction fails to quantify relative richness; the
  scenario E bias of SQS and iNEXT measures that on known truth);
- scenario M: each estimator's log ratio of mean richness in bins 11–12 to
  bins 9–10, against the truth;
- for every scenario and estimator: Spearman correlation across bins with
  true global richness; for the absolute estimators (Chao2, squares,
  DeepDive), median absolute log error against global and against
  sampled-area richness; DeepDive's own test-set error;
- K3: divDyn's Chao2 against iNEXT's. divDyn's `Chao2Method` computes
  S + (S − 1)/S · f₁(f₁ − 1)/(2(f₂ + 1)) with S the observed richness,
  where Chao's incidence estimator has (T − 1)/T with T the number of
  sampling units; iNEXT uses (T − 1)/T · f₁²/(2f₂) when f₂ > 0.

## Amendment A1 (24 October 2026, after a smoke test, before the full run)

A smoke test ran every step on replicates 1–2 of scenario M (the run's own
seeds), with DeepDive trained on 240 simulations. Its estimator output was
inspected for format only and never compared with the truth. It found:

1. divDyn's `subsample(type = "sqs")` stops with "missing value where
   TRUE/FALSE needed" when taxa are integer IDs, and `indices()` takes a
   numeric vector as abundances. Taxa are passed to divDyn as character
   names.
2. With no present diversity, DeepDiveR's config leaves `extant_sp = NA`.
   Autotune fills it only when present diversity is given, and DeepDive
   1.0.28 then stops trying to parse "NA" as a number. `extant_sp` is set to
   "0 inf", `bd_simulator`'s own default (no conditioning on extant
   diversity).
3. DeepDiveR's default `s_species = 1` starts every training clade from one
   species at 80–100 Ma. In the smoke run's 240 training simulations the
   oldest bin never held more than 7.1 species; the generator has about 490
   there. A model trained on that prior cannot describe a window that opens
   on a diverse clade, so the DeepDive arm sets `s_species = NA`, the
   setting DeepDive's autotune notes give for this case (starting richness
   drawn from U[1, 5 × the maximum range-through richness]). The default's
   prior is reported as a finding, not benchmarked.
4. DeepDive simulations take about 21 s each per core under the default
   prior and about 54 s with `s_species = NA` (a second smoke run of 72
   training simulations, whose oldest-bin richness reached 0–3,458). Each
   scenario trains on 16 cores at `nice 10`, about 9.5 h for 10,108
   simulations (DeepDive rounds the 100 test simulations up to a multiple
   of the core count).
5. The generator's truth table gains an `extant` column (species alive at
   0 Ma). No random draw changes.
