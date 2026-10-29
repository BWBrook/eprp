import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(design_path, maps):
    design = json.loads(design_path.read_text())
    arrays = {}
    for arm in ("expo", "proof"):
        path = maps / f"{arm}.npz"
        if digest(path) != design["map_sha256"][arm]:
            raise ValueError(f"Unexpected map hash: {arm}")
        with np.load(path, allow_pickle=False) as saved:
            arrays[arm] = {key: saved[key] for key in ("diversity", "X", "Y")}
        if any(a.shape != tuple(design["grid_shape"]) for a in arrays[arm].values()):
            raise ValueError(f"Unexpected grid shape: {arm}")
        if np.isinf(arrays[arm]["diversity"]).any():
            raise ValueError(f"Infinite diversity: {arm}")
    for key in ("X", "Y"):
        if not np.array_equal(arrays["expo"][key], arrays["proof"][key]):
            raise ValueError(f"Unequal coordinates: {key}")
        if not np.isfinite(arrays["expo"][key]).all():
            raise ValueError(f"Nonfinite coordinates: {key}")
    mask = np.isfinite(arrays["expo"]["diversity"])
    if not np.array_equal(mask, np.isfinite(arrays["proof"]["diversity"])):
        raise ValueError("Unequal native support")
    if int(mask.sum()) != design["expected_supported_cells"]:
        raise ValueError("Unexpected support count")
    # Native gridding indexes fixed edges, independently of its coordinate labels.
    latitude_centres = -90 + (np.arange(mask.shape[0]) + 0.5) * 0.5
    latitude = np.broadcast_to(latitude_centres[:, None], mask.shape)[mask]
    weights = np.cos(np.deg2rad(latitude))
    weights /= weights.sum()
    profiles, summaries = {}, {}
    for arm in ("expo", "proof"):
        richness = arrays[arm]["diversity"][mask]
        if (richness < 0).any():
            raise ValueError(f"Negative richness: {arm}")
        mass = weights * richness
        total = math.fsum(mass)
        if not math.isfinite(total) or total <= 0:
            raise ValueError(f"Nonpositive weighted mass: {arm}")
        profiles[arm] = mass / total
        summaries[arm] = dict(weighted_mean_local_richness=total,
                              sum_local_richness=math.fsum(richness),
                              retained_weighted_mass_fraction=1.0)
    p0, p1 = profiles["expo"], profiles["proof"]
    h2 = 0.5 * math.fsum((np.sqrt(p0) - np.sqrt(p1)) ** 2)
    affinity = math.fsum(np.sqrt(p0 * p1))
    if not math.isclose(h2, 1 - affinity, abs_tol=1e-14):
        raise ValueError("Hellinger identity failed")
    n, alpha, target = design["n"], design["alpha"], design["target_power"]
    if affinity == 1:
        upper, necessary_n = alpha, None
    elif affinity == 0:
        upper, necessary_n = 1.0, 1
    else:
        upper = min(1.0, alpha + math.sqrt(-math.expm1(2 * n * math.log(affinity))))
        necessary_n = math.ceil(math.log1p(-(target - alpha) ** 2) / (2 * math.log(affinity)))
    return dict(scope=design["scope"], design_sha256=digest(design_path),
                script_sha256=digest(Path(__file__)), map_sha256=design["map_sha256"],
                numpy_version=np.__version__, exact_mask_and_coordinates_equal=True,
                supported_cells=int(mask.sum()), arm_summaries=summaries,
                squared_hellinger=h2, affinity=affinity,
                n=n, alpha=alpha, target_power=target, power_upper=upper,
                necessary_n_lower_bound=necessary_n,
                gate="fails_at_this_budget" if upper < target else "inconclusive",
                attained_power_evaluated=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("design", type=Path)
    parser.add_argument("maps", type=Path)
    args = parser.parse_args()
    print(json.dumps(check(args.design, args.maps), indent=2, allow_nan=False))
