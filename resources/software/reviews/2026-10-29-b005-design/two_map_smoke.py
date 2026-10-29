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
output = Path(sys.argv[2]).resolve()
output.mkdir(parents=True, exist_ok=False)
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
    grid["X"] = x.copy()
    grid["Y"] = y.copy()
    return x, y, d


module.inditek_gridding_alphadiv = capture_grid
results = []
theta = [161, 19, 0.035, 0.002, 2.0]
for model in ("proof", "expo"):
    record = {"model": model}
    started = time.perf_counter()
    try:
        grid.clear()
        with contextlib.redirect_stdout(sys.stderr):
            rss, prediction, residuals = module.inditek_main(
                0.5, theta[1], fields["food_shelf"], fields["temp_shelf"], rho_ext, time_ext,
                theta[0], theta[3], theta[2], theta[4], 0, 0, ages["shelf_lonlatAge"],
                ages["Point_timeslices"].astype(int), 2.5, 2.5, londeg,
                mask["landShelfOcean_Lat"], mask["landShelfOcean_Lon"], mask_grid, proof, model)
        d = grid["value"]
        path = output / (model + ".npz")
        np.savez_compressed(path, diversity=d, X=grid["X"], Y=grid["Y"])
        finite = np.isfinite(d)
        record.update({"shape": list(d.shape), "finite_cells": int(finite.sum()),
                       "nan_cells": int(np.isnan(d).sum()), "inf_cells": int(np.isinf(d).sum()),
                       "all_native_values_finite": bool(np.isfinite(prediction).all()),
                       "minimum_finite": float(d[finite].min()) if finite.any() else None,
                       "maximum_finite": float(d[finite].max()) if finite.any() else None,
                       "sum_finite_local_richness": float(d[finite].sum()) if finite.any() else None,
                       "map_path": str(path), "map_sha256": sha256(path)})
    except Exception:
        record["error"] = traceback.format_exc()
    record["elapsed_seconds"] = round(time.perf_counter()-started, 3)
    results.append(record)
print(json.dumps({"parameters": theta, "source_and_input_sha256": hashes,
                  "python_version": sys.version.split()[0], "numpy_version": np.__version__,
                  "spatial_grid": "native 0.5 degree present continental shelf endpoint",
                  "history": "full deposited time slices, forcing, initial D0=1",
                  "results": results}, indent=2, allow_nan=False))
