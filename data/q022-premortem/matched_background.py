# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy==2.3.3", "pandas==2.3.3"]
# ///
"""Q-022 follow-up (Codex 76/1306): compare each event slice with background slices matched on lineage
count n and loss fraction m/n, instead of the pooled background. Reads the per-slice tables written by
premortem.py (no tree recomputation). Run from the repository root:
    uv run data/q022-premortem/matched_background.py
"""

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DERIVED = ROOT / "data" / "derived" / "q022-premortem"
OUT = Path(__file__).resolve().parent
N_FACTOR = 1.5      # background n within [n_event / 1.5, 1.5 n_event]
F_TOL = 0.10        # background m/n within +/- 0.10 of the event's
MIN_POOL = 10       # minimum matched background slices for a percentile
Z_DETECT = 1.645 + 0.842  # one-sided alpha 0.05, power 0.8, single event vs normal background


def matched(bg, n, f):
    return bg[(bg.n >= n / N_FACTOR) & (bg.n <= n * N_FACTOR) & ((bg.f - f).abs() <= F_TOL)]


def main():
    ev = pd.read_csv(DERIVED / "event_slices.tsv", sep="\t").dropna(subset=["ses"])
    bg = pd.read_csv(DERIVED / "background_slices.tsv", sep="\t").dropna(subset=["ses"])
    ev["f"], bg["f"] = ev.m / ev.n, bg.m / bg.n
    rows = []
    for (ds, w), e in ev.groupby(["dataset", "window"], sort=False):
        b_all = bg[(bg.dataset == ds) & (bg.window == w)]
        same_n, same_pct, pool_n, pool_pct, pool_sd, shift, ages = [], [], [], [], [], [], []
        for r in e.itertuples():
            same = matched(b_all[b_all.tree == r.tree], r.n, r.f)
            pool = matched(b_all, r.n, r.f)
            same_n.append(len(same))
            if len(same) >= MIN_POOL:
                same_pct.append(float(np.mean(same.ses < r.ses)))
            pool_n.append(len(pool))
            if len(pool) >= MIN_POOL:
                pool_pct.append(float(np.mean(pool.ses < r.ses)))
                pool_sd.append(float(pool.ses.std()))
                shift.append(r.ses - float(pool.ses.median()))
                ages.extend(pool.t.tolist())
        pool_pct = np.array(pool_pct)
        sd = float(np.median(pool_sd)) if pool_sd else np.nan
        rows.append(dict(
            dataset=ds, clade=e.clade.iloc[0], event=e.event.iloc[0], window_myr=w,
            trees=len(e), event_n_median=int(e.n.median()), event_loss_fraction_median=round(e.f.median(), 2),
            event_ses_median=round(e.ses.median(), 2),
            same_tree_matched_median=int(np.median(same_n)),
            trees_with_same_tree_pool=len(same_pct),
            pooled_matched_median=int(np.median(pool_n)),
            trees_with_pooled_pool=len(pool_pct),
            pooled_percentile_median=round(float(np.median(pool_pct)), 2) if len(pool_pct) else np.nan,
            share_trees_above_p95=round(float(np.mean(pool_pct > 0.95)), 2) if len(pool_pct) else np.nan,
            share_trees_below_p05=round(float(np.mean(pool_pct < 0.05)), 2) if len(pool_pct) else np.nan,
            event_minus_matched_median=round(float(np.median(shift)), 2) if shift else np.nan,
            matched_background_ses_sd=round(sd, 2),
            detectable_ses_shift=round(Z_DETECT * sd, 2) if sd == sd else np.nan,
            matched_background_age_range=f"{min(ages):g}-{max(ages):g}" if ages else "",
        ))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "matched_summary.tsv", sep="\t", index=False, lineterminator="\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
