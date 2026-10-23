# Q-042: end-Permian cohort and window crosswalk, with conditional sharp bounds

Owner: Claude | 11 October 2026 | Responds to external review F-01 ([review](../../docs/review/2026-10-11-gpt6pro-review/review.md))

Status: **source reconciliation and conditional algebra, not a new estimate of species loss.**

The review found that Q-042 treated the 56%, 62% and 79% figures for
end-Permian genus loss as one uncertainty interval. This note establishes,
source by source, what each published figure measures. It then states the conditional algebra that links genus loss to species
loss, with a PBDB diagnostic.

## Rebuild

```bash
python3 -I data/q042-crosswalk/bounds.py
```

The script uses the standard library only.
- On the first run it fetches two PBDB extracts into the git-ignored
  `data/raw/pbdb/q042/` (retrieved 11 October 2026):
  - Changhsingian marine animal occurrences identified to species, with
    sha256 printed;
  - the last appearance of each genus.
- Extract checksums:
  - species occurrences: sha256
    `d9081350fdad36a86e0ba6da7bcc9fe13b6eeb918155e3ab9d7b5922d79ff267`;
  - genus appearances: sha256
    `5ac13db4b9740b96aa5cd93283ca0f980557b91ca1d9d52a5cce8c34d98b8c40`.
- **Outputs (tracked):** [bounds.tsv](bounds.tsv),
  [stage_union_diagnostic.tsv](stage_union_diagnostic.tsv) and
  [sampled_genus_sizes.tsv](sampled_genus_sizes.tsv).

## What each source measures

**How the sources were checked.**
- A Claude subagent extracted the fields on 11 October 2026.
- Claude then checked the decisive quotes in context: Stanley's 56% and 62%,
  Barnosky's Table 1, Payne & Clapham's 79%, and DeepDive's 58%/24%.
- All DOIs were checked against Crossref.
- Access depth is given per row. "Not stated" means not in the material
  read.

| Source | End-Permian figure | Level and scope | Window and cohort | Metric and corrections | Global or regional | Access |
| --- | --- | --- | --- | --- | --- | --- |
| Stanley 2016, 10.1073/pnas.1613094113 | Genus 61.8–62.4% ("∼62%"); species ∼81% (∼85% before the clustering correction) | Marine animal genera (Sepkoski compilations); species inferred | Changhsingian event. Denominator is "the standing diversity (number of existing taxa) at the start of the mass extinction" | Background subtracted using E/O = 1.0 and 0.95; Signor–Lipps losses restored from the Wuchiapingian and Guadalupian. Species from a composite genus-rarefaction curve of 12 extant higher taxa, then clustering-weighted | Global | Full text (PMC) |
| Stanley 2016, same paper | Genus 56% | Same | "calculated for the Changhsingian alone" | "the traditional metric (xm = e/D)", which Stanley calls "erroneously low": no Signor–Lipps restoration | Global | Full text |
| Payne & Clapham 2012, 10.1146/annurev-earth-042711-105329 | Genus 79% ("79% extinction in the Changhsingian versus 24% in the Capitanian") | Marine invertebrate genera, PBDB download of 12 July 2011 | Changhsingian stage; cohort definition in Supplemental Sidebar 1 (not accessed) | "Per-genus extinction" under shareholder quorum subsampling; background and Signor–Lipps not stated | Global | Full text, without the Sidebar |
| Barnosky et al. 2011, 10.1038/nature09678 | "56% of genera were lost, an estimated 96% of species" | Not restricted | "within 2.8 Myr to 160 Kyr" | Not stated; no magnitude source cited in the row. Species "estimates are frequently obtained by calculating the species-to-genus ratio" | Global (implied) | Full text, without SI |
| Bambach 2006, 10.1146/annurev.earth.33.092203.122654 | Not obtained | Genus (Sepkoski) | Not obtained | Not obtained | — | Abstract only |
| DeepDive (Cooper et al. 2024), 10.1038/s41467-024-48434-7 | "loss of up to 58% of genera", "mean 24% loss of genera" | 5,312 genera of ten groups | "between the Late Permian and the earliest Triassic"; the bins compared are not stated | A modelled *net decline* in estimated diversity, not a proportional extinction; the training prior on species loss is U[0.8, 0.95] | Global, from regional bins | Full text |
| Raup 1979, 10.1126/science.206.4415.217 | Species "as many as 96 percent"; 88% from the genus curve (64.8% of genera), per Stanley | Species inferred by reverse rarefaction (echinoid curves) | "Late Permian". Per Stanley, it pools the Guadalupian and terminal Permian | Random loss within higher taxa | Global | Abstract; method per Stanley |
| Stanley & Yang 1994, 10.1126/science.266.5189.1340 | Species "about 80 percent" (76–84%) | Inferred from genera | Terminal Permian, separated from the Guadalupian | Composite curve; background subtracted (per Stanley 2016) | Global | Abstract |
| Wang et al. 2014, 10.1666/13022 | Species 62% | 1,450 species from 18 sections, South China and northern peri-Gondwana | "within 200 Kyr", onset about 252.3 Ma. Whether the 62% is of all 1,450 species or of those present at onset is **not stated** in the abstract | CONOP composite, which reduces Signor–Lipps | Regional | Abstract |
| Song et al. 2013, 10.1038/ngeo1649 | Species 57% (latest Permian), then "71% of the remaining species" (earliest Triassic); about 87.5% cumulative (subagent's arithmetic) | 537 species, 7 Chinese sections | 450 kyr, two pulses | Range data | Regional | Abstract |
| Jin et al. 2000, 10.1126/science.289.5478.432 | 162 genera and 333 species at Meishan; "94%" disappearance (as quoted by Stanley 2016) | Species, one section | Boundary at Meishan | Disappearance from the record, not extinction | Local | Abstract |
| Fan et al. 2020, 10.1126/science.aax4953 | No percentage in the main text; "a sudden drop over ~63 kyr" | 11,268 species, Chinese sections | Unbinned levels | Range-through counts, CONOP.SAGA | Regional, treated as global | Main text, no supplement |
| Kiessling et al. 2023, 10.1073/pnas.2201926119 | Review only: "Marine extinction tolls at the species level vary between 81 and 96%" | — | — | — | — | Full text |
| McKinney 1995, 10.1017/s0094837300013312 | Not a magnitude: reverse-rarefaction estimates "may be 6%-15% lower"; whether points or relative is not stated | Echinoid test of the random-within-genus assumption | — | — | — | Abstract |

## Which figures share a target (Claude's inference)

**Global genus loss.** The figures are not one interval.
- Stanley's 62% is the only one defined against the *standing cohort at the
  start of the event*, with background removed and Signor–Lipps losses
  restored. It is an **event-excess** quantity.
- Payne & Clapham's 79% is a per-genus extinction for the *whole
  Changhsingian stage* under subsampling. It includes background within the
  stage, and its cohort definition is unread.
- The 56% figure is Stanley's uncorrected e/D for the Changhsingian alone.
  Barnosky's identical 56% has no stated source; the match may be a
  coincidence. The register's attribution of 56% to Bambach is unverified.
- DeepDive's 24–58% is a modelled net decline. If originations within the
  window are non-negative, net decline is *at most* the extinction fraction
  under that model.

**Global species loss, inferred from genera.**
- Stanley (81%) and Stanley & Yang (80%) share a target.
- Raup's 96% (and Sepkoski's 94–96%, per Stanley) pools the Middle and Late
  Permian events.
- So "81–96%" (Kiessling) spans two different targets, not an uncertainty
  range. Barnosky's 96% species and 56% genus sit on different targets
  within one row.

**Regional species data.** Wang (62% within 200 kyr), Song (57% plus 71% of
the remainder, about 87.5% over 450 kyr), Jin (Meishan) and Fan are direct
species data with short windows. They differ from one another in window and
cohort.
- A species' regional disappearance is an *upper bound* on the global
  extinction of that region's species.
- It is not a global estimate.
- It does not transport to the global cohort without an argument that the
  region is representative.

**The estimand must say which kind it is.** Q-042's target ("species alive
at t0 globally extinct by t1") is a *total-loss* quantity. Stanley's is an
*event-excess* quantity. For a short pulse the two converge; over a whole
stage they need not.

## Conditional algebra, and a stage-union diagnostic

*Revised the same day after Codex's challenge (76/1538; accepted).* The first
version reported an "empirical interval" of 56–89% and said 96% was
"excluded for the sampled pool". **Both claims are withdrawn**, for three
reasons:

1. A surviving genus can persist through *unsampled* species while every
   sampled species dies. Retaining one baseline species does not bound loss
   among the sampled species; that would need a *sampled* baseline species
   to survive in each genus.
2. Every extracted occurrence has stage-wide ages (254.14–251.902 Ma). This
   is a stage union, not a start-time cohort. And no later record is not
   extinction, so 56% is not a hard lower bound either.
3. Stanley's 62% is an *event-excess* genus loss, not the number of genera
   that actually survived.
   - Codex's example: 100 genera and 500 species. 80 genera actually die,
     against 18 expected from background, so the excess is 62%.
   - The 20 surviving genera can then keep one species each, allowing 96%
     *total* species loss.
   - Plugging 0.62 into the total-loss formula gives 92.4%.
   - Species-excess bounds need their own counterfactual across ranks.

A fourth point also holds: missing genera can *lower* the true mean species
per genus, so unsampled taxa do not necessarily raise it. My first version
said they would.

**Conditional algebra (I0/I1), retained.** Suppose:
- g is the *total* genus loss of the start-time cohort;
- m is that cohort's *true* mean number of species per genus;
- every surviving genus keeps at least one start-cohort species, sampled or
  not.

Then species loss lies in [g/m, 1 − (1 − g)/m]. A full size distribution
raises the lower bound to the species share of the smallest gG genera.
[bounds.tsv](bounds.tsv) tabulates hypothetical values of g and m. A total
loss E is reachable only if m ≥ (1 − g)/(1 − E):

| Total genus loss g of the start cohort | m needed for 90% | m needed for 96% |
| --- | --- | --- |
| 0.56 | 4.4 | 11.0 |
| 0.62 | 3.8 | 9.5 |
| 0.79 | 2.1 | 5.25 |

These are conditional statements. None of the published genus figures is
yet established as g in this sense:
- Stanley's 62% is event excess.
- Payne & Clapham's 79% is a subsampled figure for a stage union.

**Stage-union diagnostic (I2), not a bound.** The data are PBDB genera with
species-level occurrences anywhere in the Changhsingian, keyed by PBDB's
accepted genus (the first version split 57 accepted genera by name), with
subgenera folded in. That gives 817 genera and 2,160 species, a mean of 2.64
per genus. Of these genera:
- 582 have no PBDB record after 251.902 Ma;
- 226 do;
- 9 are ambiguous or unmatched.

Two descriptive shares, in [stage_union_diagnostic.tsv](stage_union_diagnostic.tsv):
- 56% of the sampled species belong to genera with no later record;
- 89% of the sampled species would have to die if each genus with a later
  record kept exactly one *sampled* species.

Neither is a bound on biological loss.

## Consequences for Q-042

1. **Use one target.** Declare total loss or event excess, the window, and
   the start-time cohort.
   - Every published genus figure examined here is on a different target.
   - None yet supplies g as the total loss of a start cohort.
   - Event-excess species loss needs a counterfactual across ranks, not the
     total-loss formula.
2. **Two decisive unknowns:**
   - the start-cohort genus loss g (total);
   - the true species-per-genus distribution of that cohort.

   Unsampled taxa can move the mean either way. Narrowing needs direct
   species data with start-cohort definitions, or an explicit model of
   unsampled species *and* unsampled genera.
3. **Do not combine regional and global without a transport argument.**
   Wang's and Song's figures bound the regional cohort's global loss from
   above. They are not global calibration values.

## Limits

- The I2 diagnostic includes only genera with species-level
  identifications.
  - It is a stage union, not a start-time cohort.
  - "No later record" includes Lazarus taxa and missing data.
  - Changhsingian background is not removed.
  - The species counts are the sampled species, not the true pool.
- Not obtained:
  - Payne & Clapham's Supplemental Sidebar 1 (their cohort);
  - Fan et al.'s supplement (any percentage);
  - Bambach 2006's figure;
  - Wang et al.'s full text (their denominator).
- PBDB holdings change, so the extract is pinned by its sha256 and
  retrieval date.

## Data-access warning (23 October 2026; side session 76/2259)

[Detail withheld pending disclosure to the data custodian.]
- **Rows affected, against the public global snapshot:**
  - b001 end-Permian: 2,195 of 56,607;
  - b001 end-Triassic: 5,442 of 50,167;
  - b001 K–Pg: 7,655 of 67,097;
  - q042 Changhsingian: 150 of 11,031.
- **`genera.csv` and `genus_appearances.csv` are untested.** They may
  inherit the problem through the same query paths.
- [Detail withheld pending disclosure to the data custodian.]
- **The raw files were deleted on 23 October 2026** at Barry's instruction
  (Claude chat, exact words: "Yes, delete the raw extracts"). No other
  copies existed on the laptop, deep-server or mac-mini. The derived numbers
  here must be rebuilt from public data before any use.
