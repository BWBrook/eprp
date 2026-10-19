import importlib.util, json, pathlib, sys
import numpy as np
spec = importlib.util.spec_from_file_location("pilot", "data/q012-pilot/pilot.py"); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
A = pathlib.Path("scratch/q012-pilot/fetch-20261019-v6d/runs/P11/attempt1")
old = pathlib.Path("data/q012-pilot/payload_v6p/data/P11.json")
new = pathlib.Path("data/q012-pilot/payload_v6d/data/P11.json")
dn, do = json.loads(new.read_text()), json.loads(old.read_text())
diff = sorted(k for k in dn if dn[k] != do[k])
exe = M.trace_binary()
work = M.CACHE / "ftol_locate"
out = dict(old_data=str(old), old_data_sha256=M.sha(old), new_data=str(new), data_fields_differing=diff, binary_sha256=M.sha(exe), states=[])
for f in sorted(A.glob("chain*.trace.jsonl")):
    for e in M.read_trace(f):
        if e.get("type") != "divergence" or not e.get("captured"):
            continue
        for which in ("previous", "failing"):
            q = np.array(e[which]["q"])
            lp_o, g_o, err_o = M.lp_grad(exe, q, old, work)
            lp_n, g_n, err_n = M.lp_grad(exe, q, new, work)
            row = dict(chain=e["chain"], transition=e["transition"], phase=e["phase"], state=which,
                       new_data=("rejected: " + err_n[22:110]) if err_n else "finite",
                       old_data=("rejected: " + err_o[22:110]) if err_o else "finite")
            if not err_o and not err_n:
                row["identical_lp_grad"] = bool(lp_o == lp_n and np.array_equal(g_o, g_n))
            out["states"].append(row)
json.dump(out, open(sys.argv[1], "w"), indent=1)
print("fields differing:", diff)
for r in out["states"]:
    if r["old_data"] != r["new_data"] or r.get("identical_lp_grad") is False:
        print(r)
print("states:", len(out["states"]), "all others identical")
