# Q-012 v6q80 what-if (evidence for Codex, not a gate change): every order_preflight_v6q80 normaliser point scored
# against the mode-centred local reference (800/1,600 intervals, L 12/16) with its own resolution and domain checks.
# Run from the repository root: uv run --python 3.12 --with numpy==2.1.3 --with pandas==2.2.3 --with cmdstanpy==1.2.4 \
#   --with scipy==1.14.1 python -I data/q012-pilot/order_local_reference_whatif.py OUT.json
import importlib.util, json, sys
import numpy as np
spec = importlib.util.spec_from_file_location("pilot", "data/q012-pilot/pilot.py"); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
P = M.P
pre = json.load(open("data/q012-pilot/order_preflight_v6q80.json"))
D = {sc: json.load(open(f"data/q012-pilot/payload_v6q80/data/{sc}.json")) for sc in ("P11", "R00")}
stress = json.load(open("scratch/q012-capture-review-codex/inputs/fixed_48_stress_states.json"))["states"]
# Rebuild the 64 point states exactly as order_preflight does.
pts = {}
for sc in D:
    for k in range(1, 5):
        pts[f"start_{sc}_chain{k}"] = (sc, json.load(open(f"data/q012-pilot/payload_v6q80/inits/{sc}/chain{k}.json")), ())
s1 = json.load(open("data/q012-pilot/payload_v6q80/inits/P11/chain1.json"))
for sg in (0.01, 0.001):
    pts[f"P11_start1_sigma_{sg}"] = ("P11", dict(s1, sigma=sg, w=[x / s1["sigma"] ** 0.2 * sg ** 0.2 for x in s1["w"]]), ())
for nm, q in stress.items():
    pts[f"stress_{nm}"] = ("P11", q, ())
import pathlib
tdir = pathlib.Path("scratch/q012-pilot/fetch-20261019-v6d/runs/P11/attempt1")
for k in (1, 2):
    e = next(x for x in M.read_trace(tdir / f"chain{k}.trace.jsonl") if x.get("type") == "divergence" and x["phase"] == "sampling")
    for st in ("initial", "previous", "failing"):
        c = M.constrain(e[st]["q"], D["P11"]["N"]); sig = c["sigma"]
        pts[f"capture_c{k}_{e['transition']}_{st}"] = ("P11", dict({kk: v for kk, v in c.items() if kk != "eps"}, w=[x * sig ** 0.2 for x in c["eps"]]), ("log_k", "log_h0_1"))
assert set(pts) == set(pre["normaliser_points"]), "point set differs from the preflight"
out = {}
for nm, (sc, qw, extra) in pts.items():
    d, q = D[sc], M.w_to_eps(qw)
    agh = M._values(d, q, lambda p: P.log_norm_agh(d, p, P.cohort_A(d, p)), extra)
    a = M._values(d, q, lambda p: M.local_reference(d, p, 800, 12.0), extra)
    b = M._values(d, q, lambda p: M.local_reference(d, p, 1600, 12.0), extra)
    c = M._values(d, q, lambda p: M.local_reference(d, p, 1600, 16.0), extra)
    res, dom = M._converged(a, b), M._converged(b, c)
    row = dict(local_converged=res["converged"] and dom["converged"], log_err=abs(agh["value"] - c["value"]),
               max_d_err=max(abs(agh[k] - c[k]) for k in agh if k != "value"),
               preflight_reference=pre["normaliser_points"][nm]["reference"], preflight_pass=pre["normaliser_points"][nm]["pass"])
    row["pass_local"] = bool(row["local_converged"] and row["log_err"] <= 1e-4 and row["max_d_err"] <= 1e-3)
    out[nm] = row
summ = dict(points=len(out), local_unconverged=[k for k, v in out.items() if not v["local_converged"]],
            fail_local=[k for k, v in out.items() if not v["pass_local"]], max_log_err=max(v["log_err"] for v in out.values()),
            max_d_err=max(v["max_d_err"] for v in out.values()))
json.dump(dict(summary=summ, points=out), open(sys.argv[1], "w"), indent=1, default=float)
print(json.dumps(summ, indent=1, default=float))
