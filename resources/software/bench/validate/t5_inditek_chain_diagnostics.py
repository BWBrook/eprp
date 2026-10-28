import hashlib
import json
import sys
from pathlib import Path

import arviz as az
import numpy as np


root = Path(sys.argv[1])
names = ("Kmax", "Kmin", "spec_max", "spec_min", "Q10")
selected = {"expo": [0, 1, 2, 4, 5], "temp": [1, 2, 3, 4]}
result = {}


def scalar(value):
    value = float(np.asarray(value))
    return value if np.isfinite(value) else None


for model in ("proof", "open", "expo", "food", "temp"):
    path = root / f"inditekMCMCoutput_5002_{model}.npz"
    with np.load(path, allow_pickle=False) as saved:
        history = saved["params_accepted_history"]
        acceptance = saved["acceptance_history"]
        scales = saved["sigma_new"]
    assert history.shape == (5003, 5, 6) and acceptance.shape == (5002, 6) and scales.shape == (5002, 5, 6)
    assert np.isin(acceptance, [0, 1]).all()
    parameters = {}
    for j, name in enumerate(names):
        draws = history[2000:, j, :].T
        if np.isnan(draws).all():
            parameters[name] = {"inactive": True}
            continue
        assert np.isfinite(draws).all(), (model, name, "partially nonfinite")
        pooled = draws.ravel()
        with np.errstate(all="ignore"):
            rhat = scalar(az.rhat(draws, method="rank"))
            bulk = scalar(az.ess(draws, method="bulk"))
            tail = scalar(az.ess(draws, method="tail"))
        vals = {"inactive": False, "pooled_mean": float(np.mean(pooled)),
                "pooled_central95": np.quantile(pooled, [0.025, 0.975]).tolist(),
                "chain_means": np.mean(draws, axis=1).tolist(),
                "rhat_rank_split": rhat, "ess_bulk": bulk, "ess_tail": tail}
        if model in selected:
            vals["trace_plot_subset_mean"] = float(np.mean(draws[selected[model]]))
            vals["subset_minus_all"] = vals["trace_plot_subset_mean"] - vals["pooled_mean"]
        parameters[name] = vals
    after = scales[2000:, :, :]
    valid = np.isfinite(after[1:]) & np.isfinite(after[:-1])
    changes = valid & (after[1:] != after[:-1])
    result[model] = {"input_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                     "chains": 6, "draws_per_chain_in_notebook_slice": 3003,
                     "acceptance_fraction_by_chain": np.mean(acceptance[2000:, :], axis=0).tolist(),
                     "post_2000_proposal_scale_changes_by_parameter_and_chain": changes.sum(axis=0).tolist(),
                     "trace_plot_subset_chain_indices": selected.get(model), "parameters": parameters}

print(json.dumps({"arviz_version": az.__version__, "numpy_version": np.__version__,
                  "burn_slice_start": 2000, "models": result}, indent=2, allow_nan=False))
