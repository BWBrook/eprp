import hashlib
import json
import sys
from pathlib import Path

import arviz as az
import numpy as np


root = Path(sys.argv[1])
plans = {"proof": (2000, [0, 1, 2, 3, 4, 5]),
         "open": (3000, [0, 1, 2, 3, 4, 5]),
         "expo": (2000, [0, 1, 2, 4, 5]),
         "food": (2000, [0, 1, 2, 3, 4, 5]),
         "temp": (2000, [1, 2, 3, 4])}
names = ["Kmax", "Kmin", "spec_max", "spec_min", "Q10"]
result = {}
for model, (start, chains) in plans.items():
    path = root / f"inditekMCMCoutput_5002_{model}.npz"
    with np.load(path, allow_pickle=False) as saved:
        history = saved["params_accepted_history"]
    assert history.shape == (5003, 5, 6)
    params = {}
    for j, name in enumerate(names):
        draws = history[start:, j, :][:, chains].T
        if np.isnan(draws).all():
            params[name] = {"inactive": True}
            continue
        assert np.isfinite(draws).all()
        rhat = float(np.asarray(az.rhat(draws, method="rank")))
        ess = float(np.asarray(az.ess(draws, method="bulk")))
        params[name] = {"inactive": False, "mean": float(draws.mean()),
                        "rhat_rank_split": rhat if np.isfinite(rhat) else None,
                        "ess_bulk": ess if np.isfinite(ess) else None}
    result[model] = {"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                     "start_index": start, "chain_indices_zero_based": chains,
                     "draws_per_chain": history.shape[0] - start, "parameters": params}

print(json.dumps({"arviz_version": az.__version__, "models": result}, indent=2, allow_nan=False))
