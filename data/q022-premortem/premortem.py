# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.5.3", "dendropy==5.0.8"]
# ///
"""Q-022 pre-mortem: does event-level phylogenetic-diversity (PD) loss stand out from
background slices and from tree/window choices, on open dated palaeo-trees?

Pre-event tree frozen at slice S = T + w (lineages crossing S); a lineage is a victim if no
descendant tip is younger than T - w. Lost PD = branch length (from the MRCA of crossing
lineages, truncated at S) no longer represented by survivors. Null: m of n lineages lost
uniformly at random; exact mean (Codex 76/1262) and exact variance (descendant sets are
nested or disjoint). Run from the repository root:  uv run data/q022-premortem/premortem.py
"""

import csv
import math
from pathlib import Path

import dendropy
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "cantalapiedra2019"
OUT = Path(__file__).resolve().parent
CASES = [  # dataset, clade, event, onset (Ma); all anchored by extant tips at age 0
    ("S4", "planktonic foraminifera", "EOT", 33.9),
    ("S1", "Ruminantia", "EOT", 33.9),
    ("S5", "Equinae", "Miocene-Pliocene", 5.33),
    ("S9", "Mysticeti", "Pliocene marine turnover", 3.0),
]
WINDOWS = [0.5, 1.0, 2.0]
BACKGROUND_STEP = 1.0


def node_ages(tree):
    dist = {n: n.distance_from_root() for n in tree.preorder_node_iter()}
    dmax = max(dist[lf] for lf in tree.leaf_node_iter())
    return {n: dmax - d for n, d in dist.items()}


def slice_structure(tree, age, S, end):
    """Crossing lineages at S, victim flags, and pre-event edges as (length, lo, hi)."""
    min_tip = {}
    for n in tree.postorder_node_iter():
        min_tip[n] = age[n] if n.is_leaf() else min(min_tip[c] for c in n.child_nodes())
    order, victim, edges = [], [], []

    def visit(n):  # returns (lo, hi) interval of crossing lineages under n, or None
        lo = len(order)
        for c in n.child_nodes():
            if age[n] > S >= age[c]:  # edge n->c crosses the slice: one lineage
                i = len(order)
                order.append(c)
                victim.append(min_tip[c] >= end)
                edges.append([age[n] - S, i, i, n])
            elif age[c] > S:
                sub = visit(c)
                if sub is not None:
                    edges.append([age[n] - age[c], sub[0], sub[1], n])
        return (lo, len(order) - 1) if len(order) > lo else None

    rootiv = visit(tree.seed_node)
    if rootiv is None:
        return None
    n_lin = len(order)
    # fixed root at the MRCA of crossing lineages: drop edges whose interval spans all lineages
    edges = [(l, lo, hi) for l, lo, hi, _ in edges if not (lo == 0 and hi == n_lin - 1)]
    return n_lin, np.array(victim, bool), np.array(edges, float)


def log_comb_ratio(m, n, s):
    """log[C(m,s)/C(n,s)] for arrays s; -inf where s > m."""
    s = np.asarray(s, float)
    ok = np.isfinite(s) & (s <= m)
    safe = np.where(ok, s, 0.0)
    lg = np.vectorize(math.lgamma)
    out = math.lgamma(m + 1) - lg(m - safe + 1) - math.lgamma(n + 1) + lg(n - safe + 1)
    return np.where(ok, out, -np.inf)


def lost_and_null(n, victim, edges):
    m = int(victim.sum())
    L, lo, hi = edges[:, 0], edges[:, 1].astype(int), edges[:, 2].astype(int)
    d = hi - lo + 1
    cum = np.concatenate([[0], np.cumsum(~victim)])
    obs = float(np.sum(L * ((cum[hi + 1] - cum[lo]) == 0)))
    if m == 0 or n - m <= 1:
        return obs, m, math.nan, math.nan
    p = np.exp(log_comb_ratio(m, n, d))
    mean = float(np.sum(L * p))
    nested = ((lo[:, None] <= lo[None, :]) & (hi[None, :] <= hi[:, None])) | \
             ((lo[None, :] <= lo[:, None]) & (hi[:, None] <= hi[None, :]))
    disjoint = (hi[:, None] < lo[None, :]) | (hi[None, :] < lo[:, None])
    union = np.where(nested, np.maximum(d[:, None], d[None, :]), d[:, None] + d[None, :])
    union = np.where(nested | disjoint, union, np.nan)
    pj = np.exp(log_comb_ratio(m, n, union))
    var = float(np.sum(L[:, None] * L[None, :] * (pj - p[:, None] * p[None, :])))
    return obs, m, mean, math.sqrt(var) if var > 1e-12 else math.nan


def self_test(n, victim, edges, rng, draws=4000):
    m = int(victim.sum())
    obs, _, mean, sd = lost_and_null(n, victim, edges)
    sims = []
    for _ in range(draws):
        v = np.zeros(n, bool)
        v[rng.choice(n, m, replace=False)] = True
        sims.append(lost_and_null(n, v, edges)[0])
    sims = np.array(sims)
    assert abs(sims.mean() - mean) < 4 * sims.std() / math.sqrt(draws) + 1e-9, (sims.mean(), mean)
    assert abs(sims.std() - sd) / sd < 0.06, (sims.std(), sd)
    return sims.mean(), mean, sims.std(), sd


def main():
    rng = np.random.default_rng(20261009)
    event_rows, bg_rows, tested = [], [], False
    for ds, clade, event, T in CASES:
        trees = dendropy.TreeList.get(path=RAW / f"{ds}.nex", schema="nexus", preserve_underscores=True)
        for ti, tree in enumerate(trees):
            age = node_ages(tree)
            depth = max(age.values())
            for w in WINDOWS:
                slices = [("event", T)] + [("background", float(b)) for b in
                                           np.arange(BACKGROUND_STEP, depth - 2 * w, BACKGROUND_STEP)
                                           if abs(b - T) > 2 * w + 0.5]
                for kind, t in slices:
                    st = slice_structure(tree, age, t + w, t - w)
                    if st is None:
                        continue
                    n, victim, edges = st
                    if n < 8 or len(edges) == 0:
                        continue
                    if not tested and kind == "event" and 0 < victim.sum() < n - 1:
                        print("self-test (MC mean, exact mean, MC sd, exact sd):",
                              [round(x, 3) for x in self_test(n, victim, edges, rng)])
                        tested = True
                    obs, m, mean, sd = lost_and_null(n, victim, edges)
                    row = dict(dataset=ds, clade=clade, event=event, tree=ti, window=w, kind=kind, t=t,
                               n=n, m=m, pd_total=float(edges[:, 0].sum()), pd_lost=obs,
                               null_mean=mean, null_sd=sd,
                               ses=(obs - mean) / sd if sd == sd and sd > 0 else math.nan)
                    (event_rows if kind == "event" else bg_rows).append(row)
    derived = ROOT / "data" / "derived" / "q022-premortem"
    derived.mkdir(parents=True, exist_ok=True)
    for name, rows in [("event_slices.tsv", event_rows), ("background_slices.tsv", bg_rows)]:
        with open(derived / name, "w", newline="") as f:
            wtr = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t")
            wtr.writeheader()
            wtr.writerows(rows)

    summary = []
    for ds, clade, event, T in CASES:
        for w in WINDOWS:
            ev = np.array([r["ses"] for r in event_rows if r["dataset"] == ds and r["window"] == w])
            ev_m = [r["m"] for r in event_rows if r["dataset"] == ds and r["window"] == w]
            ev_n = [r["n"] for r in event_rows if r["dataset"] == ds and r["window"] == w]
            bg = np.array([r["ses"] for r in bg_rows if r["dataset"] == ds and r["window"] == w])
            ev_ok, bg_ok = ev[~np.isnan(ev)], bg[~np.isnan(bg)]
            if len(ev_ok) == 0:
                continue
            med = float(np.median(ev_ok))
            summary.append(dict(
                dataset=ds, clade=clade, event=event, onset_ma=T, window_myr=w,
                trees_defined=len(ev_ok), trees_total=len(ev),
                median_n=int(np.median(ev_n)), median_m=int(np.median(ev_m)),
                event_ses_median=round(med, 2),
                event_ses_q05=round(float(np.quantile(ev_ok, 0.05)), 2),
                event_ses_q95=round(float(np.quantile(ev_ok, 0.95)), 2),
                share_trees_ses_gt0=round(float(np.mean(ev_ok > 0)), 2),
                background_slices=len(bg_ok),
                background_ses_q05=round(float(np.quantile(bg_ok, 0.05)), 2) if len(bg_ok) else math.nan,
                background_ses_q95=round(float(np.quantile(bg_ok, 0.95)), 2) if len(bg_ok) else math.nan,
                event_percentile_in_background=round(float(np.mean(bg_ok < med)), 2) if len(bg_ok) else math.nan,
            ))
    with open(OUT / "summary.tsv", "w", newline="") as f:
        wtr = csv.DictWriter(f, fieldnames=list(summary[0]), delimiter="\t")
        wtr.writeheader()
        wtr.writerows(summary)
    for r in summary:
        print(r)


if __name__ == "__main__":
    main()
