# Software catalogue

A catalogue of published software for quantitative and theoretical
palaeobiology: R and Python packages, standalone programs, simulation
frameworks, Earth-system and biogeochemical models, and documented workflows.
Each entry says what a tool does and on what method, how to install it
reproducibly, what we have verified it does correctly, and where it fails.
The tools we rely on also get a pinned environment and validation scripts,
so an analysis can start from a known-good stack.

This is side work, kept apart from the main EPRP agents (Barry, 23 October
2026). It serves the whole programme: entries link to the question registers,
and what the tools make possible is recorded as leads for those registers.
Entries follow [the evidence conventions](../../docs/evidence.md). Like a data
source, a tool is fit or unfit only relative to a question.

## Layout

```text
resources/software/
  README.md            this file: conventions, tiers, template, lessons
  LANDSCAPE.md         the broad survey, generated: every tool found (tier T0)
  landscape.tsv        its source: one row per tool, the scans' facts with their labels
  landscape_check.tsv  registry metadata (CRAN, PyPI, GitHub) written by landscape.py
  landscape.py         queries the registries and renders LANDSCAPE.md
  LEADS.md             capabilities that bear on register questions or suggest new ones
  data-handoff.md      data products the scans met, for the data catalogue
  CONTACTS.md          issues for tool authors, held for Barry's outreach tranche
  <id>/README.md       the entry: YAML front matter + guide (tier T1 and above)
  <id>/env/            lockfile (renv.lock, uv.lock) and Dockerfile, if any
  <id>/validate/       validation scripts, each declaring its truth and tolerance
  <id>/results/        committed outputs that the entry quotes
```

Built images, installed libraries and large run outputs live on `deep-server`
under the same `<id>`, beside the data mirror:

```text
/data/paleosoft/<id>/   images (saved tarballs), library caches, run outputs
```

Data-access packages (PBDB, Macrostrat, Neotoma and GPlates clients) are
catalogued here as software. The data they reach belongs to the
[data source catalogue](../sources/README.md); link to its entry rather than
describing the data twice.

## Entries

| Entry | Tier | Validated uses (see entry) |
| --- | --- | --- |
| [FossilSim](fossilsim/README.md) | T2 | Poisson fossil sampling; morphospecies counts; with TreeSim, birth–death histories |
| [paleobuddy](paleobuddy/README.md) | T2 | constant and piecewise birth–death; Poisson fossil sampling |
| [divDyn](divdyn/README.md) | T2 | binned rates under complete sampling |
| [PyRate](pyrate/README.md) | T2 | constant λ and μ at high preservation (biased, no undercoverage detected); q failed |
| [RevBayes](revbayes/README.md) | T1 | none: FBD range process disabled in releases |
| [admtools](admtools/README.md) | T2 | `time_to_strat`, hiatus accounting; `strat_to_time` failed |
| [StratPal](stratpal/README.md) | T2 | `p3`, `thin` |
| [paleoAM](paleoam/README.md) | T1 | subsampling self-consistency only |
| [tbea](tbea/README.md) | T2 | Strauss–Sadler one-endpoint bound |
| [EDE](ede/README.md) | T2 | Strauss–Sadler; others characterised |
| [Rextinct](rextinct/README.md) | T1 | characterised only (GRIWM) |
| [agnostic.R](agnostic-r/README.md) | T1 | characterised only |
| [palaeoverse](palaeoverse/README.md) | T2 | `bin_time` (four methods, continuous ages); `tax_range_time`; `palaeorotate` consistent with pyGPlates for three models |
| [fossilbrush](fossilbrush/README.md) | T2 | `check_taxonomy` conflicts and formatting; `flag_ranges` failed |
| [chronosphere](chronosphere/README.md) | T1 | [Detail withheld pending disclosure to the data custodian.] |
| [iNEXT](inext/README.md) | T2 | coverage-standardised richness under fewer collections; K5 failed under smaller collections; biased by evenness change |
| [DeepDive and DeepDiveR](deepdive/README.md) | T1 | runs after three configuration fixes; characterised only (overestimates, misreads evenness) |
| [richness (Alroy)](alroy-richness/README.md) | T2 | CEGS (the geometric Weibull, on our inference) under its own model; lowest absolute error on the tranche-4 records (characterised, one generator family) |
| [cGENIE.muffin](cgenie-muffin/README.md) | T2 | 540 Ma cold-baseline volume means and field correlations against deposited output; local discrepancies remain |
| [cGENIE metabolic index](cgenie-metabolic-index-pohl/README.md) | T2 | viability and oxygen partial pressure for one deposited field and configuration; mask missing values by evaluation domain |
| [gen3sis](gen3sis/README.md) | T2 | one-step Weibull dispersal and a two-cell speciation check; ten deposited configurations audited, eight living-species counts match |
| [INDITEK-2.0](inditek-2/README.md) | T2 | specified rate/capacity controls and three proof-proposal diversity vectors; saved scores and inverse sampler remain unresolved |

Entries through tranche 4 were reviewed independently (Claude Sonnet subagent,
one review per tranche) and the findings applied. The tranche 5 entries have
a separate [Codex retained-output review](reviews/2026-10-28-tranche5-codex/README.md).
The two generators stay at T2: their
cross-check had little power, so T3 waits for a larger comparison.

The harness and results of every tranche: [bench/](bench/README.md).

## Tiers

| Tier | Meaning | Evidence required |
| --- | --- | --- |
| T0 catalogued | Identity, method, maintenance, licence and blockers recorded | A row in `LANDSCAPE.md`, facts labelled checked or recall |
| T1 installed | Builds from a pinned environment on `deep-server`; a smoke test runs | Lockfile or image digest; the smoke-test log |
| T2 validated | Recovers known truth from simulated input, or reproduces a published number from the deposited input | A test declared before running (truth, tolerance, seed), its script and output committed |
| T3 cross-checked | Agrees with an independent implementation or analytic result, or the disagreement is characterised; reviewed independently | The comparison and the review |

"The vignette runs" is T1, not validation. Two tools that share code, data or
assumptions do not cross-check each other; say what makes a comparison
independent. A tool can sit at T2 for one use and T0 for another; the tier
belongs to the validated uses, which the entry lists.

## Environments

- R: a `rocker/r-ver` image at a fixed R version with a dated Posit Package
  Manager snapshot, plus `renv.lock`. Do not depend on `deep-server`'s host R
  library: its site-library Rcpp is broken (raster and terra fail).
- Python: `uv` with a committed `uv.lock`; Docker only when system libraries
  demand it.
- Compiled models (Fortran, C++): a Dockerfile that builds from a pinned
  commit or release tarball, with the compiler version recorded.
- Java tools (BEAST2): a pinned release and package versions in the Dockerfile.
- Not available on any host: MATLAB, Octave, Julia, Apptainer, conda. A tool
  that needs one is blocked until an open port or a licence decision exists;
  record which.
- Runs longer than about 30 minutes go to `deep-server` (64 cores, shared
  with other projects; check the load first), never the laptop.

## Entry template

```yaml
---
id: short-lowercase-id
name: Display name
kind: r-package | python-package | program | framework | model | workflow | service
domain: data | chronology | palaeogeography | diversity-rates | phylogenetic | traits-morphology | simulation | earth-system | taphonomy-stratigraphy
languages: [R, Python, C++, ...]
home: URL
repo: URL
paper: [DOI, ...]
licence: SPDX id or text
release: {version: x.y.z, date: YYYY-MM-DD, checked: YYYY-MM-DD}
maintenance: {state: active | slow | dormant | archived, last_commit: YYYY-MM-DD, checked: YYYY-MM-DD}
tier: T0 | T1 | T2 | T3
validated_uses: [short descriptions; empty below T2]
environment: {route: renv | uv | docker, lockfile: path, image: name@digest, host: deep-server}
blockers: [text]
related_sources: [ids in ../sources/]
eprp_questions: [Q-..., B-...]
entry: {created: YYYY-MM-DD, updated: YYYY-MM-DD, by: participant (model), reviewed: "who and when, or not yet"}
---
```

Quote any YAML value that contains a comma or colon.

Body sections, in order:

1. **Summary**: what it does and when to reach for it, in one paragraph.
2. **Method**: the model or algorithm, its assumptions, and its lineage
   (what it reimplements or supersedes).
3. **Install**: the pinned environment, how to build it, and what broke.
4. **Validation**: each test as declared (input, truth, tolerance, seed),
   then its result; failures stay recorded.
5. **Strengths**.
6. **Weaknesses and pitfalls**: what will bite an analyst, with evidence,
   including silent defaults.
7. **Alternatives and overlap**: other tools for the same job, and how they
   differ in method, not only in interface.
8. **EPRP relevance**: questions served, what it cannot support, and leads.
9. **Citation and licence**.
10. **Verification log**: dated checks, labelled `checked`, `source claim`,
    `inferred` or `recall`.

## Adding a tool

1. Confirm identity: repository, releases, licence, maintenance, the method
   paper. Read the paper's methods and the documentation, not only the README.
2. Build the pinned environment on `deep-server`; record what failed.
3. Declare the validation tests before running them: known-truth simulation
   (from an independent generator where one exists) or a published number
   with its deposited input.
4. Run, commit scripts and outputs, and write the entry.
5. Commission an independent review before calling the entry settled.
6. Add any bug or documentation issue for the authors to `CONTACTS.md`
   here. It joins the data catalogue's queue (held back) in
   the same tranche; it is kept separate so the two side sessions never edit
   one file. Never contact authors directly; Barry sends the queue.
7. Record in `LEADS.md` anything the tool makes possible that bears on a
   register question. The registers belong to the main agents; leads reach
   them by a tranche note on the board, not by editing the registers.

## Lessons so far

**Landscape scan (23 October 2026).**

- *Check registry facts by code, not by reading.* `landscape.py` queried
  CRAN, PyPI and GitHub for the 316 of 363 tools listed there. No scan
  claim of archival or dormancy was contradicted; the one miss was the
  checker's own (a removed package with no archive date). Rerun it before
  relying on any maintenance claim.
- *Two scans that read the same pages are one source.* Both PBDB-snapshot
  reports came from overlapping READMEs and disagreed on the range; listing
  the registry directly found 1,171 versions, not "at least seven".
- *A package name on PyPI may belong to someone else.* `deepdive` on PyPI is
  an unrelated project; record registry names only from the tool's own
  documentation.
- *Search the tools before deriving a method.* The register's "not located"
  piecewise FBD-range likelihood is an argument of a RevBayes function.
- *CRAN archival is common and recent* (RPANDA, TESS, Momocs, MCMCtreeR,
  sensiPhy in the past year). Pin GitHub commits or CRAN archive tarballs in
  every environment.

**Tranche 1 (23–24 October 2026; [bench](bench/README.md)).**

- *Run a documented function before relying on it.* RevBayes' help page
  describes the FBD range process; every release since April 2024 refuses
  to run it.
- *Check which implementation ran.* PyRate loaded its compiled likelihood,
  not the Python code we first read; they agree, but the citation must be
  to what ran.
- *A test on a mean can miss an ordering error.* E[N(t)] cannot tell rate
  shifts applied forwards from backwards; G3b's midpoint count can.
- *Separate width from bias before calling intervals too narrow.* PyRate's
  q intervals are about the right width and shifted; the fix is in the
  durations, not the preservation likelihood.
- *Rejection on observed data with a full parameter redraw keeps
  simulation-based calibration; rejection at fixed parameters does not.*
- *The independent review earned its cost again.* It found no wrong
  number but five wrong or overstated interpretations, including two of
  ours that had already been written up as mechanisms.

**Tranche 2 (24 October 2026; [bench](bench/README.md)).**

- *A tool can reset the caller's random stream.* `griwm` calls `set.seed`
  inside its loop; our dating errors, drawn in the same parallel worker
  after each call, repeated across cases and invalidated a whole arm. Draw
  every random number a design needs before calling third-party code, and
  check replicates for duplicated values.
- *Test round trips, not one direction.* admtools' `time_to_strat` is
  correct and its inverse is not; only the round trip showed it.
- *Compare against independent truth, not the tool's own generator.*
  paleoAM's mixed sample is built from the same function as the reference
  we compared it with.
- *Score "no answer" deliberately.* Persistence tests that never reject and
  posteriors that never reach 0.95 changed coverage by several points
  depending on how they were counted; declare the rule in advance.
- *Baseline a filter against the same cases without it.* Hiatuses also
  remove fossils, so the right comparison for their effect is the same
  species in the ideal arm, not the nominal 0.95.

**Tranche 3 (24 October 2026; [bench](bench/README.md)).**

- *Fit the structure of a disagreement before naming it.* Two routes for
  TorsvikCocks2017 looked like different models; a rigid-rotation fit showed
  identical relative motions in different absolute frames.
- *Check what a layer file really is.* The mirror's "StaticPolygons" for one
  model is its terrane file.
- *Injected errors interact.* Our format-error names were paired with their
  sources by the spell check, which first looked like false positives.
- *Test boundaries explicitly.* Continuous synthetic ages never hit a bin
  edge; the edge cases broke two of `bin_time`'s methods.
- [Detail withheld pending disclosure to the data custodian.]
- *Type bugs hide behind plausible output.* `flag_ranges` returns numbers
  that look right and flags that look sparse; only an injection test with
  known answers showed the text comparison.

**Tranche 4 (24–25 October 2026; [bench](bench/README.md)).**

- *Pilot the generator before declaring.* A generator-only pilot showed
  the first settings would have made SQS fail by construction; tuning it
  on sampling diagnostics alone, and saying so, kept the test fair.
- *Read the prior a tool trains on.* DeepDiveR's default prior started
  every clade from one species and almost never reached the richness a
  window opening on a diverse clade has; that is an inference from the
  prior's support, not a scored run.
- *Score against the tool's own target as well as yours.* DeepDive's label
  counts part-bin species fractionally; scoring it only against "alive at
  any time" would have flattered its level error (+0.13 to +0.57 against
  global richness, +0.30 to +0.73 against its own label).
- *Declare the tolerance before the ranking.* A band chosen after seeing
  the results (±0.12) made one estimator look as if it passed; on the
  declared ±0.10 it did not.
- *Ask what the target is.* "Recovering 95% of global richness" was partly
  overshooting the species the samples could see.
- *Multi-key `merge` in R sorts on a text key.* Positional half-means after
  it mixed bins 10 and 2 until the rows were reordered.
- *Search the authors' own repositories.* The estimator the scans recorded
  as unpublished was in the author's GitHub package, cited by his preprint.
