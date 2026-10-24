"""E1 follow-up: replicate-level standard errors for divDyn's rates.

The per-bin values in e1_divdyn_bins.tsv share data between adjacent bins, so
their pooled standard error is optimistic. This averages within each replicate
first and takes the standard error across replicates.
Usage: python divdyn_se.py <e1_dir>
"""

import json
import pathlib
import sys

import numpy as np
import pandas as pd

e1 = pathlib.Path(sys.argv[1])
d = pd.read_csv(e1 / "e1_divdyn_bins.tsv", sep="\t").replace([np.inf, -np.inf], np.nan)
truth = {"ext": 0.2, "ori": 0.25}
out = {}
for arm in ("complete", "sampled"):
    a = d[d["arm"] == arm]
    out[arm] = {}
    for col in [c for c in d.columns if c not in ("bin", "rep", "arm")]:
        per_rep = a.groupby("rep")[col].mean().dropna()
        t = truth[col[:3]]
        m, se = float(per_rep.mean()), float(per_rep.std(ddof=1) / np.sqrt(len(per_rep)))
        out[arm][col] = {"mean": m, "rel_bias": m / t - 1, "se_replicate": se, "bias_in_se": (m - t) / se}
(e1 / "e1_divdyn_se.json").write_text(json.dumps(out, indent=2))
print(json.dumps({arm: {c: [round(v["rel_bias"], 4), round(v["bias_in_se"], 1)] for c, v in out[arm].items()} for arm in out}, indent=1))
