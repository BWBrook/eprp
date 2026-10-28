import contextlib
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

import mat73
import numpy as np
import pandas as pd
import scipy
import scipy.io


root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
import inditek_main_2 as module


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


paths = ["data/Point_foodtemp.mat", "data/Point_ages_xyz.mat", "data/LonDeg.mat",
         "data/landShelfOceanMask.mat", "data/rhoExt.csv", "data/observed_D.npz",
         "output_data/inditekMCMCoutput_5002_proof.npz", "inditek_main_2.py",
         "inditek_rhonet_2.py", "inditek_alphadiv_2.py", "inditek_gridding_alphadiv_2.py",
         "inditek_model_proof.py"]
hashes = {name: sha256(root / name) for name in paths}
with contextlib.redirect_stdout(sys.stderr):
    fields = scipy.io.loadmat(root / "data/Point_foodtemp.mat")
    ages = scipy.io.loadmat(root / "data/Point_ages_xyz.mat")
    londeg = scipy.io.loadmat(root / "data/LonDeg.mat")["LonDeg"]
    mask = mat73.loadmat(str(root / "data/landShelfOceanMask.mat"))
    mask_grid = np.flip(mask["landShelfOceanMask"], axis=2)
    ext = pd.read_csv(root / "data/rhoExt.csv")
    rho_ext = ext.iloc[:, 4]
    time_ext = ext.iloc[:, 0][rho_ext < 0]
    with np.load(root / "data/observed_D.npz", allow_pickle=False) as f:
        proof = f["proof"]
    saved = np.load(root / "output_data/inditekMCMCoutput_5002_proof.npz", allow_pickle=False)

orig_gridding = module.inditek_gridding_alphadiv
grid = {}


def capture_grid(*args, **kwargs):
    x, y, d = orig_gridding(*args, **kwargs)
    grid["value"] = d.copy()
    return x, y, d


module.inditek_gridding_alphadiv = capture_grid
results = []
for chain, iteration in ((0, 50), (0, 500), (5, 5000)):
    record = {"chain_index_zero_based": chain, "iteration": iteration, "saved_d_index": iteration // 50}
    t0 = time.perf_counter()
    try:
        theta = saved["params_proposed_history"][iteration, :, chain]
        expected = saved["D"][iteration // 50, :, chain]
        expected_rss = float(saved["rss_proposed_history"][iteration, chain])
        assert np.isfinite(theta).all() and np.isfinite(expected).all() and np.isfinite(expected_rss)
        record["parameters"] = theta.tolist()
        record["saved_acceptance"] = int(saved["acceptance_history"][iteration, chain])
        grid.clear()
        with contextlib.redirect_stdout(sys.stderr):
            observed_rss, prediction, residuals = module.inditek_main(
                0.5, theta[1], fields["food_shelf"], fields["temp_shelf"], rho_ext, time_ext,
                theta[0], theta[3], theta[2], theta[4], 0, 0, ages["shelf_lonlatAge"],
                ages["Point_timeslices"].astype(int), 2.5, 2.5, londeg,
                mask["landShelfOcean_Lat"], mask["landShelfOcean_Lon"], mask_grid, proof, "proof")
        observed_rss = float(observed_rss)
        prediction = np.asarray(prediction, dtype=float)
        residuals = np.asarray(residuals, dtype=float)
        assert prediction.shape == expected.shape == (2978,) and np.isfinite(prediction).all() and np.isfinite(observed_rss)
        model_map = grid["value"]
        same_mask = bool(model_map.shape == proof.shape and np.array_equal(np.isfinite(model_map), np.isfinite(proof)))
        err = prediction - expected
        record.update({"saved_rss": expected_rss, "replayed_rss": observed_rss,
                       "rss_abs_difference": abs(observed_rss - expected_rss),
                       "prediction_max_abs_difference": float(np.max(np.abs(err))),
                       "prediction_rmse": float(np.sqrt(np.mean(err**2))),
                       "prediction_correlation": float(np.corrcoef(prediction, expected)[0, 1]),
                       "model_and_observed_map_masks_identical": same_mask,
                       "F2_pass": bool(np.max(np.abs(err)) <= 1e-9 and abs(observed_rss - expected_rss) <= 1e-6)})
        if same_mask:
            observed = proof[np.isfinite(proof)]
            assert observed.shape == prediction.shape
            manual_residual = ((prediction - observed) / 2) ** 2
            manual_rss = float(np.sum(manual_residual))
            record.update({"independent_rss": manual_rss, "independent_rss_abs_difference": abs(manual_rss - observed_rss),
                           "residual_max_abs_difference": float(np.max(np.abs(manual_residual - residuals))),
                           "F3_pass": bool(abs(manual_rss - observed_rss) <= 1e-6)})
        else:
            record.update({"F3_pass": False, "F3_reason": "model and observed masks differ"})
    except Exception:
        record.update({"F2_pass": False, "F3_pass": False, "error": traceback.format_exc()})
    record["elapsed_seconds"] = round(time.perf_counter() - t0, 3)
    results.append(record)

print(json.dumps({"source_and_input_sha256": hashes, "versions": {"python": sys.version.split()[0],
                  "numpy": np.__version__, "scipy": scipy.__version__, "pandas": pd.__version__},
                  "results": results, "F2_all_pass": all(x["F2_pass"] for x in results),
                  "F3_all_pass": all(x["F3_pass"] for x in results)}, indent=2, allow_nan=False))
