import importlib.util, json, math, pathlib, sys
import numpy as np, pandas as pd
spec = importlib.util.spec_from_file_location("pilot", "data/q012-pilot/pilot.py"); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
A = pathlib.Path("scratch/q012-pilot/fetch-20261019-v6d/runs/P11/attempt1")
bank = pathlib.Path("scratch/q012-pilot/fetch-20261018-v6p2/runs/P11/attempt1")
N = 19
names = M.param_names(N)
out = {}
for k in (1, 2):
    df = pd.read_csv(A / f"chain{k}.csv", comment="#")
    for e in M.read_trace(A / f"chain{k}.trace.jsonl"):
        if e.get("type") == "divergence" and e["phase"] == "sampling":
            row = df.iloc[e["transition"] - 2000 - 2]
            u = np.array([float(row[n]) for n in names])
            for n in ("tau", "sigma"):
                u[names.index(n)] = math.log(u[names.index(n)])
            r = u[names.index("rho")]; u[names.index("rho")] = math.log(r) - math.log1p(-r)
            q = np.array(e["initial"]["q"])
            out[f"chain{k}_{e['transition']}"] = dict(saved_row=int(e["transition"] - 2000 - 1),
                max_rel_diff_initial_vs_previous_saved_draw=float(np.max(np.abs(q - u) / np.maximum(1, np.abs(u)))),
                selected_lp_saved=float(df.iloc[e["transition"] - 2000 - 1]["lp__"]))
pool = np.concatenate([pd.read_csv(bank / f"chain{k}.csv", comment="#")["sigma"].to_numpy() for k in range(1, 5)])
out["sigma_upper_tail_v6p2_32000_draws"] = dict(q99=float(np.quantile(pool, .99)), q999=float(np.quantile(pool, .999)), max=float(pool.max()),
    frac_above_1_9=float((pool > 1.9).mean()), frac_above_3_5=float((pool > 3.5).mean()), frac_above_6_2=float((pool > 6.2).mean()))
json.dump(out, open(sys.argv[1], "w"), indent=1)
print(json.dumps(out, indent=1))
