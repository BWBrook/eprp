# Repository-blind GPT-6 Pro consultation (Ediacaran–Cambrian): assessment

Owner: Claude | 21 October 2026 | For Codex's independent view, together with
the [first three briefs](2026-10-21-gpt6pro-proposals-assessment-claude.md);
no register change.

Barry ran the [blind prompt](../docs/review/2026-10-21-gpt6pro-blind-prompt.md)
as a test of whether a consultant without our notes returns less
in-distribution ideas. The response is filed verbatim:
[ediacaran_cambrian_consultation.md](../docs/review/2026-10-21-gpt6pro-blind-ediacaran/ediacaran_cambrian_consultation.md),
SHA-256 `b9dd8d4d…7ebb`, 10,051 words.

## What came back

GPT-6 Pro returned **six** cards, not ten. It said that three further ideas
failed its own gates: prior work and verified data access. It then gave
two deep dives and a consultant's view.

| # | Question (short) | Kind | Its odds: novel / answerable |
| --- | --- | --- | --- |
| 1 | Does canopy mixing still prevent oxygen depletion in dense Ediacaran communities, and can removing a structural taxon starve its neighbours? | CFD and reactive transport | 65% / 75% bounded, 25% historical |
| 2 | Which claims of order and synchrony between end-Marjuman trilobite loss, SPICE and redox survive once correlations derived from those events are withheld? | Dependency audit | 75% / 85% audit, 40% for global synchrony |
| 3 | Does the late-Ediacaran rise in trail smoothness survive a common image-resolution observation model? | Measurement calibration | 80% / 70% |
| 4 | Can recruitment under changing currents mimic the spatial signature attributed to stolon reproduction? | Point-process identifiability | 70% / 75% mechanism, 40% historical |
| 5 | Does the bioturbation–exclusion association survive differential detection and reporting? | Partial identification | 70% / 65% |
| 6 | Could burrows connect oxygenated refuges without oxygenating sediment on average? | Reaction–diffusion bounds | 70% / 55% |
| C | The consultant's "most under-asked question": why do successful ecological innovations so often fail to become persistent community states, as with orthid blooms after Cambrian trilobite crises? | Macroevolution | not given |

**Its references are reliable.** All 25 literature DOIs resolve in
Crossref to the cited first author, year and title, checked by Claude
without contact parameters. The Farrell supplement DOI resolves through
doi.org to its figshare record.
- Reading depth is declared per source: full text, abstract only, or not
  read.
- Failed downloads are reported, not glossed.
- Two sources postdate my training data, so I cannot judge their content:
  Mitchell & Manica (Nature Ecology & Evolution, June 2026) and Wang & Chen
  (Palaeo3, 2026). The record of each matches.

## Assessment against our gates

**1. A chronology dependency audit (card 2, deep dive B2). The strongest
item, and stronger generalised.**
- **The specific case.** Farrell et al. (2025) fix several biomere
  boundaries as synchronous in their CONOP composite. That chronology
  cannot then test those boundaries' synchrony with SPICE.
- **The general question:** *which claims that a mass extinction coincided
  with an environmental perturbation rest on independent time control, and
  which on correlations built from the events themselves?*
  - Causal stories for every event lean on synchrony.
  - Palaeozoic events depend most on correlation; the end-Permian and K–Pg
    rely more on direct U–Pb or Ar–Ar dating.
- **Fit.** It sits squarely in our identification programme:
  - Q-041 already requires "chronology provenance";
  - Q-005 (precursors) and Q-003 (thresholds) depend on the same thing;
  - B-007 asks whether stratigraphic architecture alone produces boundary
    clustering.
- **The design is right:** a provenance graph, ablations that withhold the
  targets, local-order models, synthetic offsets, and a 0.5 Myr
  equivalence tolerance.
- **Answerability.** The Smithfield reproduction is public. The full CONOP
  occurrence compilation is partly unpublished, so the Cambrian pilot may
  be limited to a *public-input sensitivity audit*. That is an honest
  outcome.
- **Proposed:** a blue-sky candidate in the generalised form, with the
  SPICE/end-Marjuman case as the pilot. Its first gate is a bounded prior
  check for existing audits of correlation circularity in extinction
  timing.

**2. Engineers or fossil evidence (card 5). Second.**
- Bioturbation changes habitat *and* preservation. The negative
  co-occurrence used as evidence for biotic replacement at the end of the
  Ediacaran could therefore be partly a detection effect.
- This is the same separation of observation from biology we are building
  for Q-038. It is adjacent to B-004 (burrowers and deep-water benthos).
- It offers bounds, not point estimates. That is appropriate.
- **Proposed:** candidate, with a gate before anything else: retrieve the
  Craffey Dryad archive (GPT-6 Pro's raw retrieval failed) and audit
  twenty source records.

**3. Innovation persistence (Part C). The most macroevolutionary idea in the
package.**
- The question separates the *origin* of an ecological capability from
  the conditions under which it *persists* as a community state:
  - transient post-crisis blooms (Cambrian orthids, end-Permian *Lingula*
    or *Claraia*, microbialite resurgences);
  - durable transitions.
- It applies across the Phanerozoic, and touches several of our entries:
  B-001 (reassembly order), B-010 (reef capability export), Q-009
  (ecological memory), Q-026 (reversible against terminal decline) and
  Q-043 (survivor composition).
- **Risk:** the disaster-taxon and opportunist literature may already
  occupy it (e.g. Rodland & Bottjer on *Lingula*; this is a lead from
  memory, not verified).
- **Proposed:** candidate, conditional on a bounded prior check. The
  matched-opportunity comparison of transient against persistent outcomes
  is the residual to test.

**4. Trail smoothness and image quality (card 3).** A cheap, decisive
check of measurement against biology, with a days-scale kill test. It is
outside our extinction core. Worth doing only as a quick demonstration of
observation-model-first methods; not a register entry.

**5. Canopy oxygen (card 1), currents and stolons (card 4), burrow refuges
(card 6).**
- All three are careful, but niche. Each rests on unconstrained physiology
  or on withheld data: Bed B of Mitchell & Manica is held back for
  geoconservation.
- **I disagree with GPT-6 Pro's top ranking of card 1.**
  - Its own estimate of historical answerability is 25%.
  - It needs a CFD reactive-transport programme, which is a specialist
    flow-modelling group's comparative advantage, not ours.
  - Its extinction relevance (a cascade after removing a canopy taxon) is
    speculative.
- **Proposed:** not registered.

## The experiment: blind against informed

| | Repository-informed (3 briefs) | Repository-blind (1 consultation) |
| --- | --- | --- |
| Scale | Programme-sized, about 12,000 words each, one question each | Paper-sized: six cards plus two deep dives |
| Anchoring | Our register, vocabulary and adjacency tables | Recent primary literature (2023–2026) and named archives |
| Data checking | Mostly conceptual, plus one archive audit | Downloads attempted per archive; failures reported |
| First step | Weeks: an analytic gate or pilot | Days: reproduce, degrade, audit |
| Overlap with us | Adjacent to registered questions by construction | None by topic; conceptual links found afterwards (Q-041, Q-038, B-001, B-004, B-007) |
| Best item for EPRP | Recruitment selectivity (as an analytic note) | The generalised chronology audit, and innovation persistence |

**The blind run was more useful per word, and produced the two best ideas
in the whole package.**
- **The test is confounded on method, though not on topic.** My prompt
  encoded our standards: inference-reliability quotas, "simulation only
  where decisive", cheapest first steps and stopping rules. The
  methodological resemblance therefore partly reflects the prompt, not the
  repository.
- **To isolate the effect of our standards,** a later run could vary one
  factor: same focus, minimal prompt.

**Combined ranking of all four GPT-6 Pro products for EPRP:**
1. the generalised chronology dependency audit;
2. the recruitment selectivity diagnostic, as an analytic note;
3. engineers or fossil evidence;
4. innovation persistence;
5. hybridisation cascades.

Every other item is noted, not registered.

**Calibration record.** GPT-6 Pro's novelty probabilities (65–80%) are now
on file. When the prior checks above run, record whether each card's novelty
claim survived. That gives the consultant a calibration record, as the
framework notepad's "measuring the framework" item asks.

## Questions for Codex

1. Does the generalised chronology audit survive your prior knowledge? Is
   correlation circularity in extinction timing already audited
   systematically somewhere?
2. Is innovation persistence distinct from the disaster-taxon literature in
   a way that a matched-opportunity design can test?
3. Do you agree that card 1, its top pick, falls outside our comparative
   advantage?
4. Should the three blind candidates enter the blue-sky list now, or wait
   for the paused expansion to reopen?
