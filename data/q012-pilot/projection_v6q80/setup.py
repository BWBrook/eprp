import json, sys, pathlib
import numpy as np, pandas as pd
W = pathlib.Path(sys.argv[1])
d = json.loads(pathlib.Path("data/q012-pilot/payload_v6d/data/P11.json").read_text())
for Q in (64, 80):
    t, w = np.polynomial.hermite.hermgauss(Q)
    dq = dict(d, Q=Q, gh_t=[float(x) for x in t], gh_w=[float(x) for x in w])
    (W / f"P11_Q{Q}.json").write_text(json.dumps(dq))
bank = pathlib.Path("scratch/q012-pilot/fetch-20261018-v6p2/runs/P11/attempt1")
for k in (1, 3):
    lines = (bank / f"chain{k}.csv").read_text().splitlines()
    i = next(j for j, ln in enumerate(lines) if ln.startswith("# Diagonal elements"))
    metric = [float(x) for x in lines[i + 1][2:].split(",")]
    (W / f"metric_c{k}.json").write_text(json.dumps({"inv_metric": metric}))
    x = pd.read_csv(bank / f"chain{k}.csv", comment="#").iloc[3000]
    init = dict(log_h0_1=x.log_h0_1, z_rw=[x[f"z_rw.{j}"] for j in range(1, 25)], tau=x.tau,
                **{n: x[n] for n in ("log_k", "log_lambda0", "kappa", "log_b0", "kappa_b", "beta", "gamma", "sigma", "rho")},
                w=[x[f"w.{j}"] for j in range(1, d["N"] + 1)])
    (W / f"init_c{k}.json").write_text(json.dumps({k2: (float(v) if not isinstance(v, list) else [float(u) for u in v]) for k2, v in init.items()}))
    print(k, x.stepsize__)
