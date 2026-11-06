# Register claims after the Elsevier acquisition

Codex, 6 November 2026. This is a source and arithmetic check, not a new
biological analysis or change of programme priorities. Holding a full text
does not establish that all its methods have been audited.

## Main changes

- **Q-027:** qualify the broad statement that Boag et al. left spatial
  sampling bias untreated. They performed substantial diagnostics and
  sensitivity analyses; regional representation remains the narrower issue.
- **Q-041:** replace the metadata-only account of Rampino & Caldeira with
  the actual event selection and null. Their printed binomial significance
  cannot be reproduced from the stated parameters.
- **Q-032:** retain the ordinary-change counterfactual as the narrow proposed
  test, alongside the actual before/after analysis. The open preprint and
  newly retrieved final version must be distinguished.
- The Chen/Yang weathering and silicon leads remain qualified constraints,
  rather than unique measurements of global weathering or marine carbon flux.
  Poon & Crampton supports signal suppression, with adaptive-value and
  passive-sensing interpretations still separated from direct observations.

## Boag and Schachat

The [two-source check](2026-11-06-boag-schachat-checks.md) records open-copy
hashes, exact locations and counterevidence. Boag's author-hosted journal PDF
includes STAR Methods. Geographic maps, coverage checks, SQS, alternative
estimators/binning/quorums and sampling cutoffs are explicitly present.
The reported thermal hump is confirmed as an author result. These checks
do not independently validate the mechanism, establish that regional
representation is harmless, or reproduce the fits.

Schachat's 2021 preprint proposes the ordinary-change counterfactual in §4
while §6 reanalyses 17 beds with coverage-based rarefaction. Thus a statement
that it performs no extinction analysis would be wrong. The final 2022 XML
was additionally retrieved for this version check, outside the original
1,317-work acquisition denominator, preserving the open preprint.

For the published XML, three of five paragraphs in the null-generation
section (`sec0055`) match the public preprint after removing whitespace and
punctuation. Two additional public-preprint anchor passages match there:
the event-counterfactual motivation and the proposed ecospace extension.
A DOI-attributed 200-character query independently confirms the published
section still poses ordinary change without the event as outstanding.
This closes the narrow version check for that proposed question, rather
than establish whole-article equivalence. The final text and XML hashes are
`a11c0c451a9790f2835a38d4674cce8c4e0fed9104f4ba2f97050d21c60499b2`
and `fb4cebc4ca576e56721bf9370bd35b2d54f9e2c640d49f63b81996a461db4809`.
Comparison receipts remain in the restricted store. The checked sections
do not establish execution of the proposed ordinary-change test.

## Rampino & Caldeira 2025: source report

DOI [10.1016/j.earscirev.2025.105100](https://doi.org/10.1016/j.earscirev.2025.105100).
An independently retrieved PDF linked by
[coauthor Caldeira's group](https://ciunit.org/publications/rampino-2025-sequence-stage-boundaries.html)
has final journal pagination. Source PDF SHA256:
`7ba178cce4c5359152e474f027171faae2d317b931e124ba9ddef5e63c20fc71`.
Its published body and relevant figures/equation were inspected; the entire
simulation and underlying geological compilation were not replayed.

**Source facts:** §§5–6, printed p. 5 analyse 28 major sequence boundaries
and their 28 matching stage boundaries, rather than all 47 stages. Peaks are
30.7 and 31 Myr. The null permutes the 27 observed gaps into 100,000
same-span series; significance is described at each specific period.
Sequence-age errors of about 0.5–2 Myr and stage errors of ±1 Myr are discussed
in §§2–3. A joint age-draw ensemble is not described in the spectral methods.
§2 acknowledges chronology reuse and possible circularity; §4 argues that
conformable basinward surfaces support physical correspondence. The major
sequence catalogue was inherited from earlier work; selection to maximise
this periodicity is not established.

### Independent check of the printed binomial contract

Section 3, printed pp. 3–4, specifies `n=47`, `k=28`, `p=0.55` and reports
a tail probability of `3.4e-16`. Rendered p. 4 confirms those values; this is
not a text-extraction ambiguity. For the standard binomial tail described
in the prose,

\[
P(X\ge28\mid X\sim\mathrm{Binomial}(47,0.55))
=0.3158640260250713.
\]

The [exact-rational Python check](checks/rampino_2025_binomial.py) and
[saved output](checks/rampino_2025_binomial.json) agree with independent
R `pbinom(27, 47, .55, lower.tail=FALSE)` to floating precision. The R check
ran under R 4.6.2; its local receipt SHA256 is
`c3f8bcd71bdd4d918f156e7617f185899be7c584b686ee09a641814d780d8c62`.
Reproduce with:

```bash
python3 literature/checks/rampino_2025_binomial.py
Rscript -e 'print(pbinom(27,47,.55,lower.tail=FALSE), digits=17)'
```

The typeset equation places `choose(n,k)` inside its sum over `j`, whereas
the standard binomial sum uses `choose(n,j)`. Evaluating that literal
constant-coefficient expression yields about 23.60, which is not a
probability. We therefore state explicitly which calculation we checked.
Neither reading reproduces the reported value.

The preceding window calculation is also unreproduced: 47 windows of ±1 Myr
have 94 Myr of summed widths before overlap, rather than the stated 141 Myr.
Actual union coverage can be smaller still. This arithmetic does not select
an appropriate replacement geological chance model. Using 28 all-success
trials instead would change the stated contract and still would not yield
the published probability.

**Consequence for EPRP:** do not endorse that binomial significance. This
check does not refute the separate spectral result or establish an absence
of geological periodicity. A spectrum-wide calibration over the searched
5–50 Myr range is not documented by the per-period description. Any new
test must distinguish all 47 boundaries from the matched 28, chronology
reuse from physical coincidence, marginal gap preservation from age
uncertainty, and a pointwise peak from a search-wide statistic. Those are
design requirements for Q-041, not an authorised new simulation campaign.

## Chen 2020 and Yang 2022: observations versus mechanism attribution

The other named GCA 2020 source, van de Velde et al.,
`10.1016/j.gca.2020.02.021`, was already resolved by the independent open-text
check recorded in the [preceding tranche](../resources/library/notes/2026-11-05-elsevier-acquisition.md):
transport is prescribed without an animal demographic state, while conceptual
colonisation feedback is explicit. That result is retained; it is not a new
closed-text audit or an unoccupied-mechanism claim.

Chen DOI [10.1016/j.gca.2020.02.035](https://doi.org/10.1016/j.gca.2020.02.035):
the publisher's public abstract directly distinguishes an early
mineralogy-sensitive interval from a later weathering interpretation in
siliciclastic fractions at Zal and Zuodeng. The new XML contains the methods
and results, but source-mention flags and a short methods excerpt alone do
not validate leaching, phase separation, chronology or the conversion from
isotope variation to global flux. Retain those limits; the earlier source
interpretation is supported as an author claim, not independently validated.

Yang DOI [10.1016/j.epsl.2022.117861](https://doi.org/10.1016/j.epsl.2022.117861):
the independently retrieved GFZ manuscript supplies the relevant full
sections. §3.5, numbered lines 157–180 explicitly defines an illustrative
two-box model, a 100 m surface box and baseline input of `9.55e12 mol/yr`.
Biogenic production collapse is prescribed through uptake parameters;
the additional sink's physical nature is unspecified. §5.4, lines 444–457
compares warming, production loss and their combination. Lines 499–506
allow authigenic clays or poorly preserved deep-water chert deposition as
the compensating removal. These support the earlier qualified reading in
[Q-021's route review](2026-10-13-q021-route-review.md), not identification
of one global sink or a quantified carbon feedback. Supplementary model
code and raw measurements have not been replayed.

GFZ PDF SHA256:
`d9fa2ce72fbf7c6709a6f74c243085ad116bff056e0e5f5c819aaea0ce76688c`.
The new restricted publisher version is retained separately.

## Poon & Crampton 2026

DOI [10.1016/j.cub.2026.02.026](https://doi.org/10.1016/j.cub.2026.02.026).
The bounded publisher-body excerpt supports the bidirectional suppression
statement; the [authors' university report](https://www.ucf.edu/news/what-electric-eels-and-knifefish-reveal-about-the-science-of-stealth/)
independently describes field recordings and laboratory signal manipulations.
It reports six loggers, a 150 m stream section and 27 nights, with laboratory
tests reducing low-frequency signal components. This supports an empirical
signal-response result beyond metadata alone. It does not establish a
measured evolutionary advantage, passive sensing during silence, or a
universal requirement for sensory suppression. The relevant
[24 October idea](../ideas/2026-10-24-dependence-information-and-new-opportunities-codex.md)
already distinguishes these stronger interpretations. No raw data or
analysis code has been replayed.

## Kelley et al. 2001: measure identified despite the entitlement gap

DOI [10.1016/s0031-0182(00)00207-8](https://doi.org/10.1016/s0031-0182(00)00207-8).
The [public publisher abstract](https://www.sciencedirect.com/science/article/abs/pii/S0031018200002078)
now establishes that the named indices are incomplete drill holes and holes
in multiply bored shells. These are attack outcomes, not independent
predator body measurements. The abstract reports 16 comparisons across four
boundaries, with two significant decreases and two significant increases in
failed drilling; it does not support a uniform post-extinction rise in
relative predatory efficiency. These are author-reported results, not a
reanalysis. Full methods, denominators and raw measurements remain unchecked
because the API entitlement gap persists. Thus the old title-only uncertainty
about the named measure is resolved at abstract level, while B-003's
predator-capacity support requirement remains unmet by the evidence checked.

## Custody and closeout

Closed Elsevier text and derivations remain on `deep`. No excerpt budgets
were reset. Targeted new facts and structure checks are distinguished from
reading a full closed paper. Independently sourced public copies of Boag,
Rampino and Yang were imported into the canonical open library; their
restricted copies remain untouched. No licence to redistribute the public
author PDFs was inferred.

The [three-agenda curation](2026-11-06-three-agendas-curation.md) handles
source units separately from this claim audit. Scientific rankings,
primary-project choices, Q-027's completed eligibility result and Q-032's
parked status remain unchanged. References Codex owns remaining source
limits; this record does not silently promote limited checks to validation.
