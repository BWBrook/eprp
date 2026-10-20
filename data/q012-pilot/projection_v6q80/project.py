import re, json, sys, gzip, pathlib
import numpy as np, pandas as pd
W = pathlib.Path("scratch/q012-pilot/q80_projection/warm")
bank = pathlib.Path("scratch/q012-pilot/fetch-20261018-v6p2/runs/P11/attempt1")
def elapsed(text):
    w = float(re.search(r"([0-9.]+) seconds \(Warm-up\)", text).group(1)); s = float(re.search(r"([0-9.]+) seconds \(Sampling\)", text).group(1))
    return w, s
# Kunanyi Q64 per-leapfrog cost, from v6p2's sampling phase (8,000 draws per chain).
kq64 = []
for k in range(1, 5):
    x = pd.read_csv(bank / f"chain{k}.csv", comment="#")
    w, s = elapsed(gzip.open(f"data/q012-pilot/results/P11-amended-20261018-v6p2/chain{k}.log.gz", "rt").read())
    kq64.append(s / x.n_leapfrog__.sum())
kq64 = float(np.mean(kq64))
rows = []
for k in range(1, 5):
    x = pd.read_csv(W / f"chain{k}.csv", comment="#")
    w, s = elapsed((W / f"chain{k}.csv").read_text())
    local_per_leap = s / x.n_leapfrog__.sum()
    rows.append(dict(chain=k, stepsize=float(x.stepsize__.iloc[0]), accept=float(x.accept_stat__.mean()), mean_leap=float(x.n_leapfrog__.mean()),
                     depth={int(a): int(b) for a, b in x.treedepth__.value_counts().sort_index().items()}, divergences=int(x.divergent__.sum()),
                     local_warmup_s=w, local_sampling_s=s, local_s_per_leap=local_per_leap))
out = dict(kunanyi_q64_s_per_leap_v6p2=kq64, q80_over_q64=[1.5, 1.6], chains=rows)
for ratio in (1.5, 1.6):
    kq80 = kq64 * ratio
    proj = []
    for r in rows:
        scale = kq80 / r["local_s_per_leap"]          # local -> kunanyi conversion at Q80
        warm = r["local_warmup_s"] * scale
        samp = 6000 * r["mean_leap"] * kq80
        proj.append(dict(chain=r["chain"], warmup_h=warm / 3600, sampling_h=samp / 3600, total_h=(warm + samp) / 3600))
    out[f"projection_ratio_{ratio}"] = proj
json.dump(out, open(W / "projection.json", "w"), indent=1)
print(f"kunanyi Q64 s/leapfrog (v6p2 sampling mean): {kq64:.5f}")
for r in rows:
    print({k: (round(v, 4) if isinstance(v, float) else v) for k, v in r.items()})
for ratio in (1.5, 1.6):
    print(ratio, [(p["chain"], round(p["warmup_h"], 2), round(p["sampling_h"], 2), round(p["total_h"], 2)) for p in out[f"projection_ratio_{ratio}"]])
