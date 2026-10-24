"""Tranche-3 V6: compare palaeorotate (point, grid) with pyGPlates (../VALIDATION_T3.md).

Usage: python t3_rotate_summary.py <dir>
"""

import json
import pathlib
import sys

import numpy as np
import pandas as pd

d = pathlib.Path(sys.argv[1])
MODELS = ["MERDITH2021", "PALEOMAP", "TorsvikCocks2017", "MATTHEWS2016_pmag_ref"]


def gc(lat1, lon1, lat2, lon2):
    p1, p2, dl = np.radians(lat1), np.radians(lat2), np.radians(lon2 - lon1)
    a = np.sin((p2 - p1) / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dl / 2) ** 2
    return np.degrees(2 * np.arcsin(np.minimum(1, np.sqrt(a))))


c = pd.read_csv(d / "v6_pygplates.tsv", sep="\t")
pt = pd.read_csv(d / "v6_point.tsv", sep="\t")
gr = pd.read_csv(d / "v6_grid.tsv", sep="\t")
# point output is wide: p_lng_<MODEL>, p_lat_<MODEL>
pt_long = pd.concat([pd.DataFrame({"collection_no": pt.collection_no, "age": pt.age, "model": m,
                                   "a_lng": pt[f"p_lng_{m}"], "a_lat": pt[f"p_lat_{m}"]}) for m in MODELS])
gcol_lat = "p_lat" if "p_lat" in gr.columns else None
gr_long = gr.rename(columns={"p_lng": "b_lng", "p_lat": "b_lat"})[["collection_no", "age", "model", "b_lng", "b_lat"]]
m = c.merge(pt_long, on=["collection_no", "age", "model"], how="left").merge(gr_long, on=["collection_no", "age", "model"], how="left")
m["d_ac"] = gc(m.a_lat, m.a_lng, m.p_lat, m.p_lng)
m["d_bc"] = gc(m.b_lat, m.b_lng, m.p_lat, m.p_lng)
m.to_csv(d / "v6_merged.tsv", sep="\t", index=False)

out = {"points": int(c.collection_no.nunique()), "combinations": int(len(c)), "by_model": {}}
for mod in MODELS:
    x = m[m.model == mod]
    both = x.dropna(subset=["d_ac"])
    s = {"c_reconstructed": int(x.p_lat.notna().sum()), "a_reconstructed": int(x.a_lat.notna().sum()),
         "b_reconstructed": int(x.b_lat.notna().sum()), "both_a_c": int(len(both)),
         "a_only": int((x.a_lat.notna() & x.p_lat.isna()).sum()), "c_only": int((x.a_lat.isna() & x.p_lat.notna()).sum()),
         "frac_ac_within_0.1deg": float((both.d_ac <= 0.1).mean()) if len(both) else None,
         "median_ac_deg": float(both.d_ac.median()) if len(both) else None, "max_ac_deg": float(both.d_ac.max()) if len(both) else None,
         "median_bc_deg": float(x.d_bc.median()), "q95_bc_deg": float(x.d_bc.quantile(0.95)), "max_bc_deg": float(x.d_bc.max()),
         "frac_bc_within_1deg": float((x.d_bc.dropna() <= 1).mean())}
    s["pass"] = bool(s["frac_ac_within_0.1deg"] is not None and s["frac_ac_within_0.1deg"] >= 0.95)
    out["by_model"][mod] = s
# spread of palaeolatitude across the four models (pyGPlates), by age
w = c.pivot_table(index=["collection_no", "age"], columns="model", values="p_lat").dropna()
spread = (w.max(axis=1) - w.min(axis=1)).groupby(level="age")
out["palaeolat_spread_across_models"] = {str(int(a)): {"n": int(len(v)), "median_deg": float(v.median()), "q90_deg": float(v.quantile(0.9))}
                                         for a, v in spread}
out["pass"] = all(s["pass"] for s in out["by_model"].values())
(d / "v6_summary.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
