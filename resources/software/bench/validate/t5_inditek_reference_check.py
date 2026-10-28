import contextlib
import hashlib
import json
import sys
from pathlib import Path

import mat73
import numpy as np
import pandas as pd
import scipy.io


root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root))
import inditek_main_2 as module


names = ["data/Point_foodtemp.mat", "data/Point_ages_xyz.mat", "data/LonDeg.mat",
         "data/landShelfOceanMask.mat", "data/rhoExt.csv", "data/observed_D.npz",
         "output_data/D_proof.npz", "synthetic_data.py", "inditek_main_2.py"]
hashes = {}
for name in names:
    h = hashlib.sha256()
    with (root / name).open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            h.update(chunk)
    hashes[name] = h.hexdigest()

with contextlib.redirect_stdout(sys.stderr):
    fields = scipy.io.loadmat(root / "data/Point_foodtemp.mat")
    ages = scipy.io.loadmat(root / "data/Point_ages_xyz.mat")
    londeg = scipy.io.loadmat(root / "data/LonDeg.mat")["LonDeg"]
    mask = mat73.loadmat(str(root / "data/landShelfOceanMask.mat"))
    ext = pd.read_csv(root / "data/rhoExt.csv")
    rho_ext = ext.iloc[:, 4]
    time_ext = ext.iloc[:, 0][rho_ext < 0]
    with np.load(root / "data/observed_D.npz", allow_pickle=False) as saved:
        observed = saved["proof"]
    with np.load(root / "output_data/D_proof.npz", allow_pickle=False) as saved:
        reference = saved["D"]

original = module.inditek_gridding_alphadiv
grid = {}


def capture_grid(*args, **kwargs):
    x, y, diversity = original(*args, **kwargs)
    grid["value"] = diversity.copy()
    return x, y, diversity


module.inditek_gridding_alphadiv = capture_grid
theta = [161, 19, 0.035, 0.002, 2.0]
with contextlib.redirect_stdout(sys.stderr):
    rss, prediction, residuals = module.inditek_main(
        0.5, theta[1], fields["food_shelf"], fields["temp_shelf"], rho_ext, time_ext,
        theta[0], theta[3], theta[2], theta[4], 0, 0, ages["shelf_lonlatAge"],
        ages["Point_timeslices"].astype(int), 2.5, 2.5, londeg,
        mask["landShelfOcean_Lat"], mask["landShelfOcean_Lon"],
        np.flip(mask["landShelfOceanMask"], axis=2), observed, "proof")

replayed = grid["value"]
assert replayed.shape == reference.shape == observed.shape
common = np.isfinite(replayed) & np.isfinite(reference)
same_mask = np.array_equal(np.isfinite(replayed), np.isfinite(reference))
assert common.any()
max_difference = float(np.max(np.abs(replayed[common] - reference[common])))
comparison = {}
for label, keep in [("all_common", np.isfinite(reference) & np.isfinite(observed)),
                    ("reference_at_least_10", np.isfinite(reference) & np.isfinite(observed) & (reference >= 10))]:
    delta = observed[keep] - reference[keep]
    assert delta.size
    comparison[label] = {"n": int(delta.size), "mean_observed_minus_reference": float(delta.mean()),
                         "sd_observed_minus_reference": float(delta.std(ddof=1)),
                         "minimum_difference": float(delta.min()), "maximum_difference": float(delta.max())}

print(json.dumps({"input_sha256": hashes, "parameters": theta, "same_reference_mask": bool(same_mask),
                  "common_reference_cells": int(common.sum()), "reference_max_abs_difference": max_difference,
                  "reference_matches_at_1e-9": bool(same_mask and max_difference <= 1e-9),
                  "rss_against_deposited_observation": float(rss), "observation_minus_reference": comparison},
                 indent=2, allow_nan=False))
