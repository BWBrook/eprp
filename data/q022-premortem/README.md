# Q-022 pre-mortem: is event-level phylogenetic-diversity loss distinguishable on open palaeo-trees?

Owner: Claude | Run 9 October 2026 | Status: **feasibility pre-mortem, not a result about mass extinctions**

Register entry Q-022 asks how much evolutionary history each extinction prunes.
Before investing in a harmonised comparison across events, this checks whether
an event-level signal of phylogenetic-diversity (PD) loss on open dated trees
exceeds two things: the noise from tree-construction choices, and the same
statistic measured at background times.

## Rebuild

```bash
uv run data/q022-premortem/premortem.py
```

The script pins numpy and dendropy inline and takes about 18 minutes on the WSL
laptop.
- **Inputs** (git-ignored, in `data/raw/cantalapiedra2019/`): Datasets S1–S10
  of Cantalapiedra et al. 2019 (10.1098/rspb.2018.2896).
  - Taken from the Royal Society's Figshare mirror (articles 8153414–8153441,
    CC BY 4.0), because Dryad (10.5061/dryad.gd8038s) refuses unauthenticated
    downloads (401/403).
  - File MD5s match Figshare's computed values: S1 `dcdf246a…`, S4
    `15b9fa22…`, S5 `02f50d1f…`, S9 `7a2db9e6…`.
- **Tracked output:** [summary.tsv](summary.tsv).
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

**Direct observations**
1. Event PD loss is mostly *above* random pruning: median SES +0.7 to +1.8 for
   ruminants, Equinae and Mysticeti. Foraminifera are near zero and change sign
   with the window.
2. Background slices in the same trees are *also* often above random, with
   upper 5–95% bounds up to +5.4. Event SES sits at the 24th–95th percentile of
   its own tree's background distribution. The single exception is Mysticeti at
   w = 2 Myr, where the event median (0.96) exceeds the background 95th
   percentile (0.92). It does not do so at w = 0.5 or 1 Myr.
3. Within-event spread across the posterior trees (5–95%) is about 1.1–2.9 SES
   units. Changing the window moves the median by up to 0.7 units, and flips the
   sign for foraminifera.
4. Events involve only 15–44 crossing lineages, with 4–25 lost.

**Inference**
- A random-pruning null is the wrong comparator. Phylogenetically clustered loss
  at ordinary times is pervasive in these trees. It could be biological, with
  whole extinct subclades, or produced by how tip-dated fossil trees group
  coeval taxa. The informative contrast is the event against background slices
  in the same tree.
- On that contrast, the four tested Cenozoic events show no robust
  event-specific excess PD loss beyond background: only 1 of 12 clade × window
  cases exceeds it. Tree uncertainty and window choice are as
  large as the effects.
- These are minor events for these clades. The test says nothing directly about
  the Big Five, which cannot be assessed on these trees: dinosaurs are lost
  completely, and the other Mesozoic trees lack an absolute anchor.
- Testing Q-022 on mass extinctions needs fossil-inclusive dated trees that span
  the events *with* survivors, for example brachiopods (Krug & Patzkowsky),
  bivalves (Edie et al. 2025), ammonoids, or early vertebrates
  (Flannery-Sutherland et al. 2026). It also needs a background-slice null.

## Limits

- The extant-tip anchor assumes the youngest tips are at 0 Ma.
- Tip dates and the tree samples are taken as published.
- There is no separate accounting for ancestors sampled as tips or for
  pseudoextinction.
- Background slices overlap each other and the trees, so they are not
  independent replicates.
