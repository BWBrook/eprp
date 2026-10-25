# Disturbance route, duration and life-history persistence: bounded prior check

Codex source check, 25 October 2026. Scope: Card 2 in
`ideas/2026-10-25-nominations-claude.md` and seed 1 in
`ideas/2026-10-24-2003-interests-and-new-seeds-codex.md`. This is a targeted
orientation, not a systematic review. No empirical dataset or published code
was reproduced. No private archive or text-mining corpus was read.

## Decision for the contract

**The broad theoretical idea is occupied.** Stage-specific disturbance,
longevity-dependent resistance and recovery, and environmental regimes
favouring different life histories have close explicit precedents. White et
al. (2022) is a substantially closer starting point than the Quaternary
papers. Murray et al. (2026) explicitly claim that structured disturbances
favour either fast or slow variants; its final abstract is accessible, but
its final main text was not obtained. Koons et al. (2008) already derive
opposite responses of reproductive-delay selection to fertility versus
survival variability across life-history backgrounds. These are not all the
same endpoint as finite-population extinction.

**A narrower contract remains testable:** under explicitly fixed baseline
growth, abundance, initial stage structure, dose convention and observation
horizon, identify where recruitment suppression versus adult mortality
changes the sign of the fast–slow difference in finite-horizon extinction
probability. Establish whether any reversal survives those controls and adds
something beyond the closest models. Its novelty remains unverified.

The empirical bridge is weaker. Johnson and Botha-Brink provide contrasting
life-history arguments in particular extinction settings. They do not jointly
establish a controlled cross-event reversal. Valentine & Jablonski (1986)
actually supply a directly relevant contrary result for the intuitive
planktonic-food-collapse prediction.

## Search boundary and access

Search service: web search/open, 25 October 2026; no date filters. Primary
papers, author/institutional copies and publisher/PubMed records were
preferred. Discovery queries included:

- `demographic life history fast slow survival reproduction disturbance duration stochastic transient buffering extinction recruitment failure adult mortality`
- `Johnson 2002 determinants loss mammal species late Quaternary life history ecology`
- `Botha Brink 2016 Lystrosaurus life history breeding young unstable environment`
- `demographic buffering lability Morris Doak 2004 Pfister 1998 variable environments life history stochastic population`
- `Jablonski 1986 background mass extinctions larval development mode Cretaceous Tertiary Science 231`
- exact-title searches for White, Murray, Capdevila, Le Coeur, and their
  available copies/correction; citation-following to Koons (2008) and
  Valentine & Jablonski (1986).

Stopping rule: obtain the closest route/duration model, a finite-population
extinction baseline, stochastic/ transient counterexamples, and the nominated
Quaternary/deep-time anchors; stop when these change the contract disposition.
This search does not establish coverage of every relevant demographic model
or every fossil extinction event. Search snippets alone do not establish
novelty or absence.

Access was uneven. Wiley HTML sometimes exposed complete indexed sections
then timed out on reopening; PMC sometimes presented a browser challenge.
NOAA's White PDF and institutional Johnson/Botha-Brink PDFs were retrieved
and text-extracted locally into temporary files. Murray's older preprint was
read through web PDF extraction; it is explicitly distinguished below from
the final article. No figures were quantitatively reanalysed. Locations below
are printed pages where available, otherwise named sections. All access
depths refer to this check, not an earlier session's reading.

## Closest sources and what they actually establish

### 1. White et al. (2022): the closest route/duration demographic model

White, J.W., Barceló, C., Hastings, A. & Botsford, L.W. *Pulse disturbances
in age-structured populations: Life history predicts initial impact and
recovery time.* Journal of Animal Ecology 91:2370–2383.
[DOI](https://doi.org/10.1111/1365-2656.13828);
[NOAA full PDF](https://repository.library.noaa.gov/view/noaa/55042/noaa_55042_DS1.pdf).
**Access:** relevant full-text methods/results/discussion inspected from PDF.

**Source result:** Recruitment-only versus all-age mortality disturbances,
duration, intensity, demographic openness, harvest and density dependence
are explicit. Section 2.5 (p. 2374) varies early-survival reductions over
10–70% and duration over 5–20 years. Sections 3.1–3.3 and Figure 5
(pp. 2375–2378) show greater recruitment-shock losses in shorter-lived
populations, accompanied by faster recovery. Once most age classes are
affected, the strong longevity association with impact disappears while the
recovery association remains. Density-dependent compensation depends on
placing disturbance before the density-dependent survival step (section
3.3, p. 2377).

**Boundary:** abundance/biomass impact and return to 95% of baseline are
the endpoints, not integer-population extinction. Adult-inclusive exposure
is not identical to adult-only exposure. This source already occupies much
of the proposed mechanism but does not validate a universal fast winner
under a long press.

### 2. Murray, Townley & Hodgson (2026): disturbance can favour either strategy

*A Disturbing View of Life History Evolution.* American Naturalist
207:785–799. [Final DOI](https://doi.org/10.1086/739750).
**Access:** final publisher abstract/metadata; final main text gated.
Also inspected relevant introduction/methods of the
[2024 preprint](https://doi.org/10.22541/au.172220827.78164261/v1),
[accessible PDF](https://d197for5662m48.cloudfront.net/documents/publicationstatus/215847/preprint_pdf/ccfa9d47a04a483d5338d25401eceeb1.pdf).
The cover dates it September 2024 and marks it unreviewed; do not silently
attribute its precise implementation to the final article.

**Source result:** The final abstract explicitly attributes fast–slow
advantages to structured catastrophic disturbances and the resistance–
recovery trade-off. The older preprint's Methods (PDF pp. 8–9, manuscript
lines 128–168) equalise undisturbed dominant eigenvalues, then apply random
stage-specific proportional culls before projection. Stochastic growth is
the fitness endpoint. Timing, stage structure and magnitude of disturbance
are thus central prior ingredients.

**Boundary:** final methods/results and archived code remain unchecked;
there is no demonstrated finite-population extinction calculation in the
material inspected. The broad claim cannot be sold as new pending this
paper's full comparison. A publication-supplied Dryad link exists, but its
contents were not inspected.

### 3. Jeppsson & Forslund (2012): finite-population extinction is a separate problem

*Can Life History Predict the Effect of Demographic Stochasticity on
Extinction Risk?* American Naturalist 179:706–720.
[DOI](https://doi.org/10.1086/665696);
[author manuscript](https://arxiv.org/pdf/1303.3920).
**Access:** relevant full methods/results from manuscript PDF.

**Source result:** Matrix models and multitype branching processes compare
life histories at equal deterministic growth, with binomial survival and
Poisson fertility. Methods (manuscript pp. 4–5) set lambda = 1 by adjusting
juvenile survival, initially N = 100 at stable stage composition, and compute
extinction over 100 years. Results (pp. 6–8, Figures 1–3) contain strong
adult-survival × maturation interactions and exceptions to monotonic trait
rules. Higher fecundity often accompanies higher extinction risk under this
matching, because juvenile survival changes too.

**Boundary:** constant environment, no density dependence or imposed
disturbance. This is a design reference for integer extinction, not direct
proof of the route × duration hypothesis. Equalising growth creates a
specified joint life-history contrast; it does not isolate one trait's
causal effect.

### 4. Koons, Metcalf & Tuljapurkar (2008): a direct route-dependent theoretical ancestor

*Evolution of Delayed Reproduction in Uncertain Environments: A Life-History
Perspective.* American Naturalist 172:797–805.
[DOI](https://doi.org/10.1086/592867);
[full PDF](https://research.amnh.org/users/rfr/hbp/koonsetal08.pdf).
**Access:** abstract and relevant full model methods through web PDF extraction.

**Source result:** The abstract (p. 797) states that fertility variability
favours reproductive delay more strongly for high-survival/low-fertility
life histories, whereas survival variability favours delay more strongly
for low-survival life histories. Within-year covariance changes the
evolutionarily stable delay. Methods (pp. 798–799) separately model fertility,
juvenile survival, adult survival and density regulation using two stages;
uncertainty in bounded survival probabilities is scaled relative to its
maximum possible CV.

**Boundary:** evolutionary invasibility/optimal delay under recurring
uncertainty, not extinction of fixed strategies after a finite press.
Nevertheless, the demographic route reversing a life-history prediction is
already an explicit theoretical result. Reproductive delay, adult longevity,
and a one-dimensional pace score must not be equated.

### 5. Le Coeur et al. (2022): buffering and lability need explicit environmental links

Le Coeur, C., Yoccoz, N.G., Salguero-Gómez, R. & Vindenes, Y.
*Life history adaptations to fluctuating environments: Combined effects of
demographic buffering and lability.* Ecology Letters 25:2107–2119.
[DOI/full text](https://onlinelibrary.wiley.com/doi/full/10.1111/ele.14071).
**Access:** abstract, glossary, relevant methods/discussion sections.

**Source result:** Stochastic growth is decomposed into effects of nonlinear
vital-rate responses and their variance/covariance, using 154 animal matrix
models. Abstract and Discussion identify greater potential for both gains
and losses in fast life histories; slow species chiefly buffer. Box 1 and
Introduction define demographic buffering as stabilisation of vital rates,
and lability as tracking environmental fluctuations, with benefits dependent
on curvature and covariance. Discussion explicitly warns that populations
with the same generation time can behave differently.

**Boundary:** these are imposed environmental response scenarios on
empirical demographic templates, not observations of catastrophe survival.
Long-run stochastic growth differs from finite extinction probability. A
short adult-storage buffer and evolved low vital-rate variance are different
meanings of buffering.

### 6. Capdevila et al. (2022), with substantive 2024 correction: transient response

*Life history mediates the trade-offs among different components of
demographic resilience.* Ecology Letters 25:1566–1579.
[Original](https://doi.org/10.1111/ele.14004);
[2024 correction](https://doi.org/10.1111/ele.14468);
[correction text](https://pmc.ncbi.nlm.nih.gov/articles/PMC11472290/).
**Access:** original abstract, definitions and discussion; correction's
indexed explanatory text and Figure 3/S1 captions. PMC reopening was challenged.

**Source result:** Intrinsic resistance, transient compensation and return
to stable structure are derived from demographic matrices for 910 plant/
animal populations. The correction replaces an erroneously reversed
resistance calculation. Corrected resistance increases with generation
time in animals but decreases in plants, and decreases with reproductive
output in both. The original abstract's opposite reproductive-output claim
must not be reused. Both versions discuss mathematical dependence between
life-history and resilience measures extracted from the same matrices.

**Boundary:** structural response potential is not realised survival under
a measured disturbance. Here compensation means transient demographic
amplification; it should not be conflated with density-dependent replacement
or negative covariance between vital rates. The correction is essential to
any substantive use of this source.

### 7. Johnson (2002): relevant Quaternary selectivity, qualified proxy independence

*Determinants of loss of mammal species during the Late Quaternary
‘megafauna’ extinctions: life history and ecology, but not body size.*
Proceedings of the Royal Society B 269:2221–2227.
[DOI](https://doi.org/10.1098/rspb.2002.2130);
[institutional PDF](https://eprints.jcu.edu.au/1056/1/johnson_1.pdf).
**Access:** relevant full introduction/methods/results in PDF.

**Source result:** Extinct–surviving mammal comparisons associate slow
reproduction with extinction and identify habitat/behavioural protection
among slow-reproducing survivors. Methods (p. 2222) estimate reproductive
rates for extinct species from clade-specific regressions against body
mass in living relatives; nine family/superfamily groups meet inclusion
criteria. This is a way of using different mass–reproduction relationships
among lineages, not direct reproductive measurements independent of size.

**Boundary:** the paper's causal interpretation is stronger than its
observational design alone establishes. It provides neither stage-specific
disturbance measurements nor a matched pulse/press comparison. Reuse as a
fully size-independent fossil pace dataset would conceal the estimation
structure.

### 8. Brook & Bowman (2004): multiple mechanisms generate similar selectivity

*The uncertain blitzkrieg of Pleistocene megafauna.* Journal of Biogeography
31:517–523. [DOI/full text](https://doi.org/10.1046/j.1365-2699.2003.01028.x).
**Access:** publisher abstract/introduction and indexed model-description
passage; this check did not reread every full-text section. The seed records
an earlier direct publisher reading of Discussion/Conclusions.

**Source result:** Empirical size selectivity and mechanistic simulations
show that different hunting/habitat scenarios reproduce similar patterns.
The abstract identifies surviving populations depressed below pre-event
densities across successful model scenarios. Introduction explicitly
challenges a simple inference from Johnson to body size being irrelevant,
because size indexes several demographic/ecological attributes. The model
description includes maximal replacement rate, prey equilibrium density,
human density, off-take and naivety.

**Boundary:** this is not a controlled age-structured route × duration
experiment. Body mass is a multivariate proxy, and fitting a selectivity
curve does not identify the demographic route. Lower survivor density is
a mechanism for later vulnerability, not evidence for a unique deep-time
legacy process.

### 9. Botha-Brink et al. (2016): closest deep-time histology–demography bridge

Botha-Brink, J., Codron, D., Huttenlocker, A.K., Angielczyk, K.D. & Ruta, M.
*Breeding Young as a Survival Strategy during Earth's Greatest Mass
Extinction.* Scientific Reports 6:24053.
[Correct DOI](https://doi.org/10.1038/srep24053);
[institutional full PDF](https://www.wits.ac.za/media/wits-university/news-and-events/images/documents/Botha-Brink%20et%20al%202016.pdf).
**Access:** relevant full histological/results/discussion/model methods in PDF.

**Source result:** Histology and skull-size distributions suggest curtailed
life expectancy in Early Triassic therapsids. Earlier breeding is proposed
and tested using hypothetical life tables. Figure 3 and pp. 4–5 contrast
earlier breeding with greater reproductive output. Methods (pp. 7–8) derive
growth from matrices, vary environmental carrying capacity, and call runs
extinct when continuous abundance falls below one.

**Boundary:** age at first reproduction is explicitly unknown; size bins
stand in for age and assume linear growth. This is observational support
plus a plausibility model, not a direct estimate of fossil reproductive age
or demographic stochasticity. A below-one threshold in logistic simulations
is distinct from individual survival/reproduction sampling. The work already
occupies the broad early-reproduction benefit under harsh post-extinction
conditions, but not a cross-event reversal under matched exposure.

### 10. Jablonski (1986), and the more direct Valentine & Jablonski larval test

Jablonski, D. *Background and mass extinctions: the alternation of
macroevolutionary regimes.* Science 231:129–133.
[DOI](https://doi.org/10.1126/science.231.4734.129);
[PubMed](https://pubmed.ncbi.nlm.nih.gov/17842630/).
**Access:** bibliographic record and complete abstract, not full paper.

**Source result:** Planktotrophic development, constituent-species range
and richness favour background survival but lose predictive power at the
end-Cretaceous; overall lineage geographic deployment still matters.
**Boundary:** effect disappearance is not a sign reversal, and larval mode
does not uniquely encode adult longevity or generation time.

The closer companion is Valentine, J.W. & Jablonski, D. (1986), *Mass
extinctions: Sensitivity of marine larval types*, PNAS 83:6912–6914.
[DOI](https://doi.org/10.1073/pnas.83.18.6912);
[PubMed abstract](https://pubmed.ncbi.nlm.nih.gov/16593761/).
**Access:** complete abstract, not scanned full text.
**Source result:** It explicitly predicts selection against feeding larvae
if impact-induced loss of planktonic food lasts months/years, but reports
equal survival of planktotrophic/nonplanktotrophic prosobranchs at the K–Pg.
It contrasts indirect evidence of prolonged end-Permian selection against
planktotrophy. **Boundary:** no controlled generation-time comparison follows
from the abstract. This is already a demographic-route argument confronted
with contrary fossil evidence, and deserves full-text recovery before any
claim that the proposed empirical comparison is new.

## Controls the minimal model needs

The following are Codex inferences/design recommendations, not additional
results attributed to the papers.

1. **Specify persistence.** Report initial loss, minimum abundance,
   endpoint abundance and recovery separately from probability of hitting
   N = 0 (or an explicitly justified quasi-extinction boundary) by a fixed
   horizon. A fast recovery curve does not establish greater survival.
2. **Separate route from dose.** Compare a fixed fraction reduction in
   affected vital rates, then check whether conclusions change when immediate
   population loss or reproductive-value loss is matched. These answer
   different questions; none is automatically the uniquely fair convention.
   Apply survival changes at a declared point in the census cycle. Do not
   multiply a fertility entry and survival again if the entry already includes
   survival.
3. **Declare the joint life-history contrast.** Matching baseline growth
   usually requires another rate to change. Record which one. Vary longevity,
   maturation and reproduction as distinct parameters before interpreting
   their combination as pace. Match initial N; assess biomass/resource
   equivalence separately if that becomes the scientific estimand.
4. **Test onset structure.** Strategy-specific stable composition is a useful
   baseline, not a universal natural condition. Check adult-rich and
   juvenile-rich starts. State how integer initial counts are allocated, and
   whether disturbance begins before or after breeding.
5. **Duration/generation time is not sufficient.** Vary duration in common
   calendar steps as well as D/T. Also declare the time allowed for recovery;
   observing one strategy for more calendar time can change its apparent
   risk. Generation-time standardisation can itself change exposure/horizon.
6. **Do not force a reversal.** With complete recruitment failure, no import
   or dormant stages, equal starting adult counts and independent constant
   adult survival, persistence through the failure is
   `1 - (1 - s_adult^D)^A0`. Higher adult survival wins for every D. Both
   strategies eventually become highly vulnerable; duration alone need not
   produce a fast winner. Partial recruitment, post-event reproduction or a
   changed mortality route supplies different mechanisms that must be named.
7. **Keep competing mechanisms explicit.** Density compensation, Allee
   effects, adult age structure, fecundity dispersion, environmental covariance,
   refugia and immigration can alter rankings. A first model can omit them,
   provided its conclusion remains conditional and the first discriminating
   extension targets the mechanism most likely to change the decision.

## What remains missing, and disposition

The decisive literature gap in this check is access to Murray's final main
text and a careful full-text comparison with Valentine & Jablonski, not
another broad list of extinction-selectivity papers. The source search also
does not establish a compiled fossil dataset with independent adult longevity,
maturation, body size, physiological exposure, demographic route and event
duration for two contrasting events. Histology, growth increments and larval
mode require separate observation models and need not measure the same axis.

Retire the broad mechanistic novelty claim and fold the useful mechanism
into Q-028. The contract's bounded **conditional extinction-ranking test**
can clarify its assumptions, without warranting a new question slot or
investigation campaign. Any residual historical transport/application question
is conditional on an identifiable empirical discriminator. If integer
extinction rankings merely reproduce existing resistance/recovery results,
retain the probe as a teaching/feasibility result. If a robust difference
appears, compare it directly with the above models before considering
promotion. Parent Codex integrates the contract and model; Claude is the
independent crossed reviewer. Nothing here selects a primary project.
