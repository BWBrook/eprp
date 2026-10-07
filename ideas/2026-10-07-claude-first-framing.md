# Claude's first framing of the orientation tranche

Status: sketch | Proposer: Claude | Critic: Codex (invited) | Updated: 7 October 2026

Independent first framing written before convergence, in reply to Codex's
proposal in discussion 76. Process criticism is on the board, not here.
Every source below was checked only at **metadata** depth (title, authors,
year, DOI via the OpenAlex API, 7 October 2026) unless marked **abstract**.
None has been read in full. Novelty of every candidate is **unverified**.

## Position on biological versus identifiability-led orientation

Neither in pure form. Choose questions for biological value; triage them
identifiability-first. For each candidate, the first check is a cheap forward
simulation: if the mechanism were true, would the record we can actually
obtain show it, at the grain and with the biases it has? That makes "simulate
before you extract" the programme's default first move and a cheap filter.
Barry's simulation background and the remit both favour it.

Consequence for allocation: a database/data-contract audit done before the
questions exist has no target. The audit should measure what the simulation
says matters (grain, rank, joint coverage, dating error), so it belongs inside
each question family rather than as a parallel function.

Use existing simulators and fitting tools before writing new ones: for example
FossilSim, the PyRate and DeepDive simulators, and palaeoverse for preparation.
Cooper et al. 2024 (DeepDive, [10.1038/s41467-024-48434-7](https://doi.org/10.1038/s41467-024-48434-7))
is one instance of simulation-trained inference on fossil occurrences. The
wider opportunity, simulation-based inference for mechanistic palaeobiological
models, fits the remit; whether it is under-used is unverified.

## Making deep-time and modern comparisons meaningful

Agent inference; offered as working principles to be challenged.

1. **Compare inferred process parameters, not plotted patterns.** Compare
   quantities such as per-lineage extinction rates estimated with an explicit
   sampling model, at a stated taxonomic rank and time grain.
2. **Rates are grain-dependent.** Measured rates fall as the measurement
   interval lengthens (Gingerich 1983, [10.1126/science.222.4620.159](https://doi.org/10.1126/science.222.4620.159);
   for climate, Kemp et al. 2015, [10.1038/ncomms9890](https://doi.org/10.1038/ncomms9890)).
   A per-Myr fossil rate and a per-century modern rate are not commensurable
   without a scaling model. Spalding & Hull 2021 (**abstract**,
   [10.1098/rspb.2020.2332](https://doi.org/10.1098/rspb.2020.2332)) make the
   same point for the extinction-rate metric.
3. **Degrade, don't upgrade.** Information flows one way: modern data can be
   passed through a fossil-like observation filter, but fossil data cannot be
   sharpened to modern resolution. Plotnick et al. 2016 (**abstract**,
   [10.1111/ele.12589](https://doi.org/10.1111/ele.12589)) did this for
   mammals: fewer than 9% of threatened species have a fossil record, against
   20% of non-threatened species, which roughly halves the apparent magnitude.
4. **Use the Late Quaternary as the calibration window.** It is the one
   interval where fossil and modern observation systems overlap (species-level,
   radiometrically dated, centennial to millennial grain), so it can test
   whether the transfer rules in 1–3 work before they are applied deeper.

## Two contrasting question families

Chosen to maximise contrast in observation scale and in the kind of work.

### A. Rates and thresholds across timescales (Phanerozoic to present)

Deep time, maximal scale gap, theory- and simulation-heavy.
Question: once grain-dependence and detection are modelled, what does the
fossil record imply about the size of a century-scale extinction or warming
pulse needed to match past crises?

- Song et al. 2021 (**abstract**, [10.1038/s41467-021-25019-2](https://doi.org/10.1038/s41467-021-25019-2))
  report mass-extinction thresholds of >5.2 °C and >10 °C/Myr. Agent inference
  to be checked against the full text: any modern warming rate exceeds 10 °C/Myr
  by orders of magnitude, so a rate threshold stated at Myr grain cannot
  discriminate a modern pulse without a scaling argument.
  **Correction (7 October, after full-text check by Codex and Claude):** this
  criticism is incomplete. Rates use event durations of 0.05–6.5 Myr, not the
  ~10 Myr bins. Fig. 3 defines a joint region (ΔT >5.2 °C, R >10 °C/Myr,
  Δt <0.4 Myr). The authors cite Kemp et al. 2015 and state that decadal-to-millennial
  peak rates are unrecoverable. The open question is whether the joint relation
  transports to a century-scale pulse; see discussion 76, messages 1105–1106.
- Malanoski et al. 2024 (**abstract**, [10.1126/science.adj5763](https://doi.org/10.1126/science.adj5763)):
  physiological traits plus climate-change magnitude explain marine invertebrate
  extinction over 485 Myr. Nearest prior work for any climate–extinction coupling.
- Judd et al. 2024 (PhanDA, [10.1126/science.adk3705](https://doi.org/10.1126/science.adk3705)):
  a 485 Myr surface-temperature reconstruction, which would serve as the forcing series.
- Penn et al. 2018 ([10.1126/science.aat1327](https://doi.org/10.1126/science.aat1327))
  and Penn & Deutsch 2022 ([10.1126/science.abe9039](https://doi.org/10.1126/science.abe9039)):
  a mechanistic metabolic-index bridge from end-Permian to modern ocean warming.
- Barnosky et al. 2011 ([10.1038/nature09678](https://doi.org/10.1038/nature09678)),
  Cowie et al. 2022 ([10.1111/brv.12816](https://doi.org/10.1111/brv.12816)),
  Kirchner & Weil 2000 ([10.1038/35004564](https://doi.org/10.1038/35004564)):
  framing for the "sixth mass extinction" comparison and recovery lags.

Smallest useful check: simulate lineages under a known pulse of given duration
and magnitude, observe them through a fossil-like filter at several grains, and
ask whether published threshold and rate-comparison metrics recover the truth.
Abandon if the nearest prior work has already done this with explicit observation models.

### B. The Late Quaternary bridge: selectivity and timing

Shallow time, minimal scale gap, data-heavy.
Question: do Late Quaternary extinction selectivity and chronology carry
information about modern risk beyond what modern traits and threats already provide?

- Resources: PHYLACINE 1.2, which includes extinct Late Quaternary mammals
  ([10.1002/ecy.2443](https://doi.org/10.1002/ecy.2443)); FosSahul 2.0
  ([10.1038/s41597-019-0267-3](https://doi.org/10.1038/s41597-019-0267-3));
  Neotoma; the IUCN Red List (API needs a token).
- Barry's own prior work is central here: megafauna extinction chronology and
  dating quality (e.g. Saltré et al. 2015, [10.1016/j.quascirev.2015.01.022](https://doi.org/10.1016/j.quascirev.2015.01.022);
  Saltré et al. 2016, [10.1038/ncomms10511](https://doi.org/10.1038/ncomms10511)),
  and extinction-date estimation from sighting records (Brook et al. 2019,
  [10.1002/ecy.2787](https://doi.org/10.1002/ecy.2787)). Fossil last
  appearances and modern sightings share one inference problem: dating an
  extinction from a sparse, biased detection record. This gives the fastest
  expert critique, but a project must go beyond his existing results.
- Related: Finnegan et al. 2015 ([10.1126/science.aaa6635](https://doi.org/10.1126/science.aaa6635));
  Harnik et al. 2012 ([10.1098/rspb.2012.1902](https://doi.org/10.1098/rspb.2012.1902));
  Fordham et al. 2020 ([10.1126/science.abc5654](https://doi.org/10.1126/science.abc5654)).

Main risk: a crowded field, so novelty is hardest to establish here.

## Resource gaps relevant to these families

Add these to the catalogue only when a family adopts them:

- **BioDeepTime** (**abstract**, [10.1111/geb.13735](https://doi.org/10.1111/geb.13735)):
  10,062 modern and fossil assemblage time series spanning years to millions of
  years. A direct cross-timescale bridge.
- **Triton** ([10.1038/s41597-021-00942-7](https://doi.org/10.1038/s41597-021-00942-7)):
  species-level Cenozoic planktonic foraminifera. Its dense record makes it a
  candidate testbed for checking estimators against near-complete sampling.
- **PhanDA**, **PHYLACINE**, **FosSahul 2.0** as above.
- **Literature infrastructure.** The OpenAlex API answered about 30 keyless
  queries from WSL on 7 October 2026. It can serve as the reproducible search
  and snowballing backbone, with queries recorded per [evidence.md](../docs/evidence.md).
  Full-text access, not reading throughput, is the binding constraint. Prefer
  open-access copies and record access depth.
