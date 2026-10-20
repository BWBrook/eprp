# Q-012 v6q80: the three failed stress states of order_preflight_v6q80.json (sigma 0.001, log-h0 + 10). Compares
# quadrature orders 64-128 with the fixed-innovation reference (1,600/3,200) and the local-mode reference (L 12/16/24).
# Run from the repository root: uv run --python 3.12 --with numpy==2.1.3 --with pandas==2.2.3 --with cmdstanpy==1.2.4 \
#   --with scipy==1.14.1 python -I data/q012-pilot/order_reference_diagnosis.py OUT.json
import importlib.util, json, math, sys
import numpy as np
spec = importlib.util.spec_from_file_location("pilot", "data/q012-pilot/pilot.py"); M = importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
P = M.P
d80 = json.load(open("data/q012-pilot/payload_v6q80/data/P11.json"))
stress = json.load(open("scratch/q012-capture-review-codex/inputs/fixed_48_stress_states.json"))["states"]
out = {}
for nm in ["grid-s0.001-h10.0-kb-1.5", "grid-s0.001-h10.0-kb0.0", "grid-s0.001-h10.0-kb1.5", "grid-s0.001-h5.0-kb0.0", "grid-s0.1-h10.0-kb0.0"]:
    q = M.w_to_eps(stress[nm])
    A = P.cohort_A(d80, q)
    row = dict(sigma=q["sigma"], max_A=float(np.max(A)))
    for Q in (64, 80, 96, 128):
        row[f"agh_Q{Q}"] = P.log_norm_agh(d80, q, A, Q)
    row["ref_fixed_1600"] = P.log_norm_ref(d80, q, A, 1600)
    row["ref_fixed_3200"] = P.log_norm_ref(d80, q, A, 3200)
    row["ref_local_1600_L12"] = M.local_reference(d80, q, 1600, 12.0)
    row["ref_local_1600_L16"] = M.local_reference(d80, q, 1600, 16.0)
    row["ref_local_3200_L24"] = M.local_reference(d80, q, 3200, 24.0)
    out[nm] = row
    print(nm, json.dumps({k: (round(v, 10) if isinstance(v, float) else v) for k, v in row.items()}))
json.dump(out, open(sys.argv[1], "w"), indent=1)
