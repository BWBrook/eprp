# Q-022 pre-mortem: is event-level phylogenetic-diversity loss distinguishable on open palaeo-trees?

Owner: Claude | Run 9 October 2026; matched-background follow-up 10 October | Status: **feasibility pre-mortem, not a result about mass extinctions**

Register entry Q-022 asks how much evolutionary history each extinction prunes.
Before investing in a harmonised comparison across events, this checks whether
an event-level signal of phylogenetic-diversity (PD) loss on open dated trees
exceeds two things: the noise from tree-construction choices, and the same
statistic measured at background times.

## Rebuild

```bash
uv run data/q022-premortem/premortem.py
uv run data/q022-premortem/matched_background.py
```

`premortem.py` pins numpy and dendropy inline and takes about 18 minutes on the
WSL laptop. `matched_background.py` (numpy, pandas) reads its per-slice tables
and takes about 8 s.
- **Inputs** (git-ignored, in `data/raw/cantalapiedra2019/`): Datasets S1–S10
  of Cantalapiedra et al. 2019 (10.1098/rspb.2018.2896).
  - Taken from the Royal Society's Figshare mirror (articles 8153414–8153441,
    CC BY 4.0), because Dryad (10.5061/dryad.gd8038s) refuses unauthenticated
    downloads (401/403).
  - File MD5s match Figshare's computed values: S1 `dcdf246a…`, S4
    `15b9fa22…`, S5 `02f50d1f…`, S9 `7a2db9e6…`.
- **Tracked outputs:** [summary.tsv](summary.tsv), and
  [matched_summary.tsv](matched_summary.tsv) from `matched_background.py`.
- **Untracked output:** per-tree tables for event and background slices in
  `data/derived/q022-premortem/`.

## Method

1. **Absolute time.** Node ages are the maximum root-to-tip distance minus each
   node's distance from the root. This assumes the youngest tips are extant, so
   only trees with many tips at age about 0 are used:
   - ruminants (S1, 237 extant tips);
   - planktonic foraminifera (S4, one tree);
   - Equinae (S5);
   - Mysticeti (S9).
   The "Dinosauria" tree (S2) is excluded: its youngest tips are Maastrichtian
   non-avian dinosaurs, so every K–Pg lineage is lost and the null is
   undefined. The fish, pterosaur and theropod trees (S3, S7, S8) have no
   extant anchor.
2. **Event slice.** For an event at T with half-window w:
   - Freeze the pre-event lineage set at S = T + w.
   - A crossing lineage is a victim if none of its descendant tips is younger
     than T − w.
   - Lost PD is the branch length of the pre-event tree, rooted at the MRCA of
     the crossing lineages and truncated at S, that survivors no longer
     represent.
3. **Exact null.** m of n lineages are lost uniformly at random.
   - Mean: Σ lₑ C(m,dₑ)/C(n,dₑ) (Codex 76/1262).
   - Exact variance: descendant sets are nested or disjoint, so pairwise joint
     probabilities are hypergeometric.
   - The standardised effect size is SES = (observed − mean)/SD. It is undefined
     when m = 0 or when one or no lineages survive.
   - A Monte Carlo self-test with 4,000 draws on the first event slice gave a
     mean of 151.33 against an exact 151.48, and an SD of 19.99 against an exact
     19.93.
4. **Background comparison.** The same statistic at every 1-Myr slice in the
   same tree, keeping more than 2w + 0.5 Myr from the event, with at least 8
   crossing lineages. Every tree in the posterior sample (100 per clade, 1 for
   foraminifera) is used, at w = 0.5, 1 and 2 Myr.

Events tested:
- foraminifera and ruminants at the Eocene–Oligocene transition (EOT, 33.9 Ma);
- Equinae at the Miocene–Pliocene boundary (5.33 Ma);
- Mysticeti at the Pliocene marine turnover (about 3.0 Ma).

These are tests of the method, not claims that each event was a crisis for that
clade.

## Result

| Clade, event | w (Myr) | Lineages n / lost m (median) | Event SES, median [5–95% across trees] | Background SES 5–95% | Event SES percentile within background |
| --- | --- | --- | --- | --- | --- |
| Foraminifera, EOT | 0.5 / 1 / 2 | 44 / 20–25 | +0.6 / +0.2 / −0.8 (one tree) | about −1.5 to +3.3 | 0.66 / 0.51 / 0.24 |
| Ruminantia, EOT | 0.5 | 29 / 4 | +1.19 [−0.67, 2.24] | −1.28 to 3.31 | 0.64 |
| | 1 | 31 / 9 | +1.76 [0.87, 2.55] | −0.98 to 4.13 | 0.68 |
| | 2 | 33 / 15 | +1.04 [0.10, 1.89] | −0.96 to 5.40 | 0.39 |
| Equinae, Miocene–Pliocene | 0.5 / 1 / 2 | 23–29 / 12–23 | +1.26 / +0.68 / +0.69 | about −2.2 to +2.1 | 0.78 / 0.62 / 0.55 |
| Mysticeti, Pliocene | 0.5 / 1 / 2 | 15–18 / 5–10 | +1.00 / +0.78 / +0.96 | about −1.5 to +1.8 | 0.81 / 0.78 / 0.95 |

This table compares each event with the *pooled* background: every slice in
the clade's trees, whatever its lineage count or loss fraction.

**Direct observations (pooled background)**
1. Event PD loss is mostly *above* random pruning: median SES +0.7 to +1.8 for
   ruminants, Equinae and Mysticeti. Foraminifera are near zero and change sign
   with the window.
2. Background slices in the same trees are *also* often above random, with
   upper 5–95% bounds up to +5.4. Event SES sits at the 24th–95th percentile of
   the pooled background. The single exception is Mysticeti at w = 2 Myr, where
   the event median (0.96) exceeds the background 95th percentile (0.92).
3. Within-event spread across the posterior trees (5–95%) is about 1.1–2.9 SES
   units. Changing the window moves the median by up to 0.7 units, and flips the
   sign for foraminifera.
4. Events involve only 15–44 crossing lineages, with 4–25 lost.

## Matched-background follow-up (10 October)

Codex (Correspondence 76/1306) pointed out that the pooled percentile is
descriptive, not a calibrated event test. Pooled background slices differ
widely in lineage count, loss fraction, age and tree shape: for ruminants at
w = 0.5 Myr, n runs from 8 to 401 and m/n from 0 to 0.42. SES does not make
them exchangeable.

[matched_background.py](matched_background.py) reads the saved per-slice tables
and does not recompute any trees (about 8 s):
- It keeps background slices with n within a factor of 1.5 of the event's
  and loss fraction within ±0.10 of it.
- Matches are pooled across the clade's posterior trees, because a single tree
  rarely has 10 matches.
- Each tree's event is then placed within its matched pool, provided the pool
  has at least 10 slices.
- The detectable shift is 2.49 × the matched-background SD: the excess a
  single event needs over its background for 80% power at one-sided α = 0.05,
  treating the background as normal.

Output: [matched_summary.tsv](matched_summary.tsv).

| Clade, event | w (Myr) | Trees with ≥10 matches | Event percentile within matched background, median across trees | Trees above matched 95th | Event − matched median (SES) | Detectable shift (SES) | Matched background ages (Ma) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Foraminifera, EOT | all | 0 | — | — | — | — | no background slice matches |
| Ruminantia, EOT | 0.5 | 100 | 0.88 | 0.26 | +1.45 | 2.74 | 22–42 |
| | 1 | 98 | 0.96 | 0.52 | +1.73 | 2.21 | 21–41 |
| | 2 | 59 | 0.95 | 0.47 | +1.15 | 1.88 | 20–39 |
| Equinae, Miocene–Pliocene | 0.5 | 97 | 0.73 | 0.01 | +0.65 | 2.49 | 1–16 |
| | 1 | 100 | 0.61 | 0.19 | +0.14 | 1.49 | 2–15 |
| | 2 | 0 | — | — | — | — | event loss fraction 0.80 exceeds every background slice |
| Mysticeti, Pliocene | 0.5 | 100 | 0.86 | 0.05 | +1.05 | 2.21 | 5–29 |
| | 1 | 100 | 0.83 | 0.09 | +0.79 | 2.00 | 6–28 |
| | 2 | 100 | 0.97 | 0.70 | +1.15 | 1.45 | 8–27 |

**Direct observations (matched background)**
1. All eight testable clade × window cases sit above their matched background
   median, by +0.1 to +1.7 SES units. In no case does the event fall below the
   matched 5th percentile in any tree.
2. Three cases reach the matched 95th percentile at the median tree: ruminants
   at w = 1 and 2 Myr, and Mysticeti at w = 2 Myr. Even there, only about half
   to 70% of the posterior trees exceed it.
3. The shifts are mostly smaller than the detectable shift of 1.5–2.7 SES units.
   As single-event tests, these cases are underpowered.
4. Matching removes the foraminifera, and Equinae at w = 2. Their event loss
   fractions lie outside the background range, which is itself a taxonomic
   signal.
5. The cases are not independent: windows overlap, the three windows share
   lineages, and posterior trees share most of their topology.

**Inference**
- The two nulls answer different questions (Codex 76/1306).
  - Size-matched random pruning answers "is PD loss beyond exchangeable-tip
    loss?". Background slices reject it too, so phylogenetically clustered
    loss is common at ordinary times in these trees. That could be biological,
    with whole extinct subclades, or it could come from how tip-dated fossil
    trees group coeval taxa.
  - Matched background slices answer "is this event's loss different from
    ordinary times of similar size?". An event-specific effect could be a
    deficit as well as an excess.
- The pooled comparison in the first round was too negative. Matched on size
  and loss fraction, these Cenozoic events show a weak, consistently positive
  event-specific excess of PD loss, mostly below single-event detection power.
  This is neither absence of an effect nor evidence of one.
- These are minor events for these clades. The test says nothing directly about
  the Big Five, which cannot be assessed on these trees: dinosaurs are lost
  completely, and the other Mesozoic trees lack an absolute anchor.
- A Q-022 study on mass extinctions therefore needs three things:
  - fossil-inclusive dated trees that span the events *with* survivors, for
    example brachiopods (Krug & Patzkowsky), bivalves (Edie et al. 2025),
    ammonoids, or early vertebrates (Flannery-Sutherland et al. 2026);
  - a matched-background or process-model null;
  - a power calibration, simulating clustered loss of known strength on the
    same trees before any event is tested.

## Limits

- The extant-tip anchor assumes the youngest tips are at 0 Ma.
- Tip dates and the tree samples are taken as published.
- There is no separate accounting for ancestors sampled as tips or for
  pseudoextinction.
- Background slices overlap each other and the trees, so they are not
  independent replicates.
- The matching tolerances (factor 1.5 in n, ±0.10 in loss fraction) and the
  10-slice minimum were chosen once and not tuned. Ages are not matched: the
  Mysticeti and Equinae backgrounds are older than their events.
