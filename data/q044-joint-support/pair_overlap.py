# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas==2.3.3", "numpy==2.3.3"]
# ///
"""Q-044 follow-up to Codex's ceiling audit: among primary windows with Good's u >= 0.7, does recorded
species/genus sharing fall with distance (biological distance decay) or stay near zero everywhere
(as uniform detection failure would predict)? Imports the unchanged screen (build.py).
Run from the repository root:  uv run data/q044-joint-support/pair_overlap.py
"""
import importlib.util, itertools, sys
from pathlib import Path
import numpy as np, pandas as pd
root = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("screen", root / "data/q044-joint-support/build.py")
s = importlib.util.module_from_spec(spec); spec.loader.exec_module(s)
occ, _ = s.clean()
bins = pd.read_csv(s.SRC / "input-data/equal-length-intervals.csv")
k = np.clip(np.searchsorted(bins.FAD.values, occ.ma_mid.values, side="right"), 0, len(bins) - 1)
ok = (occ.ma_mid.values < bins.FAD.values[k]) & (occ.ma_mid.values >= bins.LAD.values[k]) & ~np.isin(occ.ma_mid.values, bins.FAD.values)
occ = occ[ok].copy(); occ["bin"] = bins.bin.values[k[ok]]
cont = s.continents()
rows = []
for b in s.FOCUS:
    g = occ[occ.bin == b]
    colls = g.groupby("collection_no").agg(paleolat=("paleolat","first"), paleolng=("paleolng","first"), cc=("cc","first")).reset_index()
    ws = []
    for centre, members in s.windows(colls, 1000, 10):
        wc = colls.iloc[members]
        wo = g[g.collection_no.isin(wc.collection_no) & (g.binomial != "")]
        if not len(wo): continue
        f = wo.binomial.value_counts(); u = 1 - (f == 1).sum() / len(wo)
        cn = wc.cc.map(cont).dropna(); c = cn.mode().iloc[0] if len(cn) else "?"
        ws.append((set(f.index), set(g.loc[g.collection_no.isin(wc.collection_no) & (g.genus_name != ""), "genus_name"]), u, c,
                   colls.paleolat.iloc[centre], colls.paleolng.iloc[centre]))
    for (a, ga, ua, ca, la1, lo1), (bb, gb, ub, cb, la2, lo2) in itertools.combinations(ws, 2):
        if min(ua, ub) < 0.7: continue
        sor = 2 * len(a & bb) / (len(a) + len(bb)); sorg = 2 * len(ga & gb) / (len(ga) + len(gb))
        rows.append(dict(bin=b, same_continent=ca == cb, dist_km=float(s.gcd(la1, lo1, la2, lo2)), sorensen_species=sor, sorensen_genera=sorg))
d = pd.DataFrame(rows)
d.round(4).to_csv(root / "data/q044-joint-support/pair_overlap.tsv", sep="\t", index=False, lineterminator="\n")
print(len(d), "pairs of windows both with u >= 0.7; bins:", sorted(d.bin.unique()))
print(d.groupby("same_continent")[["dist_km","sorensen_species","sorensen_genera"]].agg(["count","median","mean"]).round(3).to_string())
d["band"] = pd.cut(d.dist_km, [0, 3000, 6000, 20000])
print(d.groupby("band", observed=True)[["sorensen_species","sorensen_genera"]].agg(["count","median"]).round(3).to_string())
