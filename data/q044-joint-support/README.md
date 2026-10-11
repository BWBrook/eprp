# Q-044 joint-support screen: can the window hierarchy be estimated for non-marine tetrapods?

Owner: Claude | Built 11 October 2026; revised the same day after [Codex's ceiling audit](../q044-support-audit/README.md) | Status: **a presence and overlap screen (a data contract), not an estimate of α, β or Γ**

Q-044 asks whether, from the Late Triassic to the Neogene, differentiation
*between* regions rose while within-region richness stayed flat. Its estimand,
per time bin, is

ln Γ_K = ln ᾱ + ln β_within + ln β_between

over K equal-spread windows with fixed weights (see the
[register](../../ideas/register.md#q-044-why-is-life-on-land-so-diverse-if-regional-terrestrial-richness-is-bounded)).
This screen asks, before any estimate, three things:
- how many disjoint, adequately sampled windows each bin has;
- where those windows are;
- whether they share any taxa.

## Rebuild

```bash
uv run data/q044-joint-support/build.py
```

- About 20 s and 0.65 GB peak memory; pandas and numpy are pinned inline.
- Input: Barry's download of the Close et al. 2019 Dryad deposit
  (10.5061/dryad.3v0p84v). It is extracted, git-ignored, under
  `data/raw/close2019/`.
  - Outer zip sha256: `fb5d7457d3c21d20262772fad26a5175a3aaa4be5b4318f695ec3308233d7010`.
  - `alpha_tetrapodomorpha.csv` sha256: `2c57030860c72be16f1e01d8740de4d07056ee030dfa7c8ced8f02f461230e63`.
- The deposit's R code was read, not run. The exclusions below re-express it.
- Continents come from the country-code table in the Benson et al. archive
  (`data/raw/benson2025/`), read as literal strings.
- **Outputs (tracked):** [per_bin.tsv](per_bin.tsv),
  [per_window.tsv](per_window.tsv) and [summary.tsv](summary.tsv).

## Source and contract

| Item | Finding |
| --- | --- |
| Deposit | Code and raw PBDB downloads for Close et al. 2019, *Nat Ecol Evol* (10.1038/s41559-019-0811-8), on local-community richness. The zip has no README, no licence file and no outputs: `output/` is empty |
| Download | `alpha_tetrapodomorpha.csv`: 157,847 occurrences in 33,346 collections. The PBDB query (`base_name=Tetrapodomorpha`, `idtype=latest`, `pres=regular`) is recorded only in a comment in `01 load-alpha-data.R`. No download date is recorded; the latest `modified` stamp is 12 December 2017. Palaeocoordinates are `gp_mid` |
| Reproducibility of the source | Not runnable as deposited. `PGS`, `multitonRatio` and `rescaledMultitonRatio` are called but not defined. `geoMST` is sourced from a Dropbox path, and the master script names a missing file |
| What the source estimates | Collection-level and formation-level species richness (local α). Spatial spread, such as summed MST length, appears only as a sampling covariate. **There is no window-level (γ_w) or union (Γ_K) estimate to reuse** |
| Unit | The occurrence, nested in a collection, in a window, in a bin. A collection is the local community, as in the source |
| Exclusions (re-expressed from the source) | Trace, egg and marine terms, matched on order, family or genus. Marine clades (cetaceans, pinnipeds, sirenians). Trace preservation. Listed dubious occurrences and collections. Implausibly aged dinosaurs, mammals and squamates. Collections at group or formation stratigraphic scale, or basin geographic scale. Pliocene and younger caves, tar pits, mires and sinkholes. Unlithified sediments at 100 Ma or younger. **119,315 occurrences remain**, with palaeocoordinates and a bin |
| Time support | The source's 41 roughly equal-length bins (mean about 9 Myr), assigned by age-range midpoint as in the source. The focus is the 26 bins from Tr3 (Carnian) to Ng3 (Pliocene). `share_spilling_bin` is the share of occurrences whose age-range *duration* exceeds the bin's duration: up to 0.88 in K7 (Campanian), and over 0.4 in K3–K5 and Pg3. Crossing a bin boundary is a different, broader measure: 33% of occurrences in primary windows (Codex) |
| Taxon identity | Shared identity uses accepted species binomials, with subgenus brackets stripped and subspecies collapsed, and genus names from species- or genus-rank records. Indeterminate records count as collection presence but not as identities |
| Windows | Circles of 500 or 1,000 km radius, centred on collections. They are chosen greedily: densest first, kept only if each centre is at least 2r from all others, so the circles are disjoint. Each needs at least 5, 10 or 20 collections. **Primary: 1,000 km and at least 10 collections.** Greedy packing gives a lower bound on the possible K, not an optimum |
| Coverage | Good's u per primary window (1 − species singletons / species occurrences). Reported at 0.5 and 0.7. `mean_collection_species` in [per_window.tsv](per_window.tsv) averages only the collections that have named species, so it is conditional richness, not α over all collections |
| Outcome independence | Not applicable to a support count. Note, though, that window placement is chosen *by sampling density*, so the windows and the estimates share one sampling process |

## Result

| Bins (of 26) with at least 4 windows | |
| --- | --- |
| 1,000 km radius, at least 10 collections (primary) | 19 |
| Primary, with Good's u ≥ 0.5 | 16 |
| Primary, with Good's u ≥ 0.7 | 5 (Pg3, Pg5, Ng1, Ng2 and Ng3); no Mesozoic bin |
| 500 km radius, at least 10 collections | 22 |
| 1,000 km radius, at least 20 collections | 17 |

Bins failing the primary rule are Tr5 (latest Triassic), J2–J4 (late Early
to Middle Jurassic), K1–K2 (earliest Cretaceous) and Pg0 (early
Palaeocene). Adding the coverage condition (u ≥ 0.5) also removes Tr3, J5
and K6.

The gaps fall in the Jurassic, when Pangaea's break-up should begin to raise
between-region differentiation. That is the interval Q-044 most needs.

**Three findings matter more than the counts.**

1. **Recorded species names barely overlap between windows.**
   - Among the primary windows' union, the share of species found in two or
     more windows is 0–0.033 in every Mesozoic and Palaeogene bin, and
     0.05–0.12 in the Neogene.
   - At genus level the share is 0–0.12 in the Mesozoic, 0.01–0.14 in the
     Palaeogene, and 0.22–0.35 in the Neogene.
   - Codex's audit gives the exact quantity. With equal weights and q = 0,
     recorded β/K is 0.973–1 in the Mesozoic and 0.965–1 in the Palaeogene.
   - **This is recorded, not biological, saturation** (Codex, accepted).
     - Withdrawn: the first version's "cannot rise" and "would reflect …
       taxonomic practice …, not biology".
     - Sparse detection alone can make recorded β/K about 0.985 even when
       every species occurs in every window.
     - The ceiling of K holds only for equal weights.
     - Two primary windows have no named species at all, and 31% of
       collections in primary windows have no species-level identity.
   - **But the overlap falls with distance even at high coverage**
     ([pair_overlap.py](pair_overlap.py), 96 pairs of windows that both have
     Good's u ≥ 0.7):

     | Window pairs | Distance between centres | Species Sørensen | Genus Sørensen |
     | --- | --- | --- | --- |
     | Different continents (87) | median 10,000 km | mean 0.002 | mean 0.042 |
     | Same continent (9) | median 3,300 km | mean 0.055 | mean 0.193 |
     | Under 3,000 km (4) | | median 0.114 | median 0.326 |

     - Uniform detection failure predicts low overlap at every distance, so
       this pattern argues against it.
     - Regional naming practice would also produce decay with distance, so
       the check does not separate naming from biology.
     - Only 9 same-continent pairs reach this coverage.
     - Inference: between continents, near-maximal species turnover is the
       *expected* biological state, as it is between continents today. A
       contrast built on windows on different continents carries little
       information about change; partial sharing exists only at
       intracontinental separations.
2. **The windows are mostly on different continents and far apart.**
   - Mean distance between centres is 5,300–6,400 km in the Late Triassic,
     and mostly 7,400–12,000 km afterwards. J5, at 4,900 km, is the
     exception.
   - Only 5 bins (K7, Pg5, Ng1, Ng2 and Ng3) have at least four primary
     windows on one continent.
   - The greedy, densest-first rule picks the major collecting regions:
     western North America, Europe, China, Argentina and so on. So, as
     specified, β_between measures the differentiation of continents. That
     follows palaeogeography by construction, and its separation changes
     through time.
3. **"Equal spread" is not achieved by circles.**
   - Summed MST length within primary windows ranges from 0 to 15,847 km,
     with a median of 2,433 km.
   - A circle caps extent but not spread. The estimator must subsample each
     window to a fixed MST length, or use divvy-style clusters.
   - Fixing the *configuration* of the K windows (their mutual distances) is
     a choice of target, not a requirement (Codex). A reference geography
     asks about turnover at fixed separation. Letting the geography vary
     keeps fragmentation, part of Q-044's hypothesised mechanism, inside the
     estimand. Choose the target first.

## Consequences for Q-044

- **D stays 2.** Support for counting windows is ample from the Late
  Cretaceous onwards, and patchy in the Early–Middle Jurassic and earliest
  Cretaceous.
- **First, a contract for observation-aware support** (Codex's proposal,
  accepted). Specify:
  - fixed K and fixed weights;
  - which collections are eligible, by whether they carry identities;
  - how unknown identities and uncertain ages are treated;
  - a test separating biological endemism from non-overlap produced by
    observation.

  The distance-decay check above is a first, small instance of that test.
- **Then decide the estimand** (my view, not agreed). Species-level
  β_between across continents is expected to be near its maximum
  biologically as well as in the records. Its change therefore carries
  little information, and continental separation is confounded with
  palaeogeography. Options, each with its own support problem:
  - **Within-continent window sets at fixed separation**, for example K = 4
    windows whose centres span a fixed distance. Supported only in about 5
    bins, nearly all Cenozoic. This approaches Close & Reijenga 2025's
    North American design.
  - **Genus level, or a phylogenetic or Hill-number turnover measure**,
    which is less saturated. But genus-level sharing is itself rising
    towards the Neogene, partly because there are more same-continent
    windows.
  - **A model-based distance–decay of shared identity, at fixed separations,**
    as the between-region quantity. The register says distance decay is
    only a diagnostic, because taxa can be strongly partitioned among
    windows with a flat distance relationship. That argument should be
    revisited if the hierarchy cannot be estimated.
- **Kill criterion.** I wrote that the current rule was "unreachable".
  **That is wrong** (Codex). An interval such as [−0.05, 0.02] contains 0 and
  excludes ln 1.5. Near a ceiling the rule is *easier* to trigger.
  - The real problem: on a quantity pinned near its ceiling, the kill could
    trigger because of the design, whatever happened biologically.
  - Rewrite it for the chosen estimand, stating:
    - the interval;
    - the direction;
    - the effect threshold;
    - an outcome for "insufficient information".

    An equivalence test may be the cleaner form.
- The data-vintage check (2017 deposit against a current PBDB extract, by
  occurrence number) remains to do. The PBDB query is recorded, so the check
  is feasible.

## Limits

- Circles and greedy packing are a screen, not divvy or the source's MST
  method.
- Coverage is Good's u at species level per window, not the iNEXT or SQS
  eligibility that a real estimator would use.
- Continents come from modern countries, so palaeocontinental identity is not
  resolved.
- Only Close et al.'s 2017 download is used. Close et al. 2020, on regional
  diversity, has its own deposit, which was not opened here.
