import hashlib
import json
import sys
from pathlib import Path

import netCDF4 as nc
import numpy as np
from scipy.special import ndtr


root = Path(sys.argv[1])
experiment = "AP.540ebP2_.bg.PO4.Tdep.pCO2FKr_x0.5.PO4PD.pO2PD_radfor.SPIN"
reference = root / "inputs/pohl_mi/deposit" / experiment / "biogem/fields_biogem_3d.nc"
mi_paths = list((root / "work/mi/output").glob("*habitat_viability.nc"))
assert len(mi_paths) == 1
mi_path = mi_paths[0]


def sha256(path):
    h = hashlib.sha256()
    with path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def valid(a):
    return np.ma.masked_invalid(np.ma.asarray(a, dtype=float))


ref = nc.Dataset(reference)
times = np.asarray(ref["time"][:], dtype=float)
graded_times = times[times >= 999.5]
assert len(graded_times) == 10
thickness = np.abs(np.diff(ref["zt_edges"][:]))
volume = thickness[:, None, None] * ref["grid_area"][:][None, :, :]
results = {}
for name in ("gf9-v0935", "gf11-v0978", "gf9-v0978"):
    path = root / "runs" / name / "home/cgenie_output" / experiment / "biogem/fields_biogem_3d.nc"
    run = nc.Dataset(path)
    run_times = np.asarray(run["time"][:], dtype=float)
    rows = []
    for t in graded_times:
        match = np.flatnonzero(np.isclose(run_times, t, rtol=0, atol=1e-6))
        assert len(match) == 1, (name, t, match.tolist())
        i = int(np.flatnonzero(times == t)[0])
        row = {"year": float(t)}
        for variable, factor in (("ocn_temp", 1), ("ocn_O2", 1e6)):
            a = valid(run[variable][match[0]]) * factor
            b = valid(ref[variable][i]) * factor
            mask_a, mask_b = np.ma.getmaskarray(a), np.ma.getmaskarray(b)
            wet = ~(mask_a | mask_b)
            weights = np.asarray(volume)[wet]
            av, bv = a.data[wet], b.data[wet]
            row[variable] = {
                "mean_diff": float(np.average(av - bv, weights=weights)),
                "correlation": float(np.corrcoef(av, bv)[0, 1]),
                "mask_mismatch": int(np.count_nonzero(mask_a != mask_b)),
                "wet_cells": int(wet.sum()),
                "max_cell_abs_diff": float(np.max(np.abs(av - bv))),
            }
            if variable == "ocn_O2":
                row[variable]["cells_abs_diff_gt_10"] = int(np.count_nonzero(np.abs(av - bv) > 10))
                row[variable]["threshold_disagreements"] = {
                    str(threshold): int(np.count_nonzero((av < threshold) != (bv < threshold)))
                    for threshold in (10, 20, 60)
                }
        row["pass"] = bool(abs(row["ocn_temp"]["mean_diff"]) <= 0.05 and abs(row["ocn_O2"]["mean_diff"]) <= 1 and row["ocn_temp"]["correlation"] >= 0.99 and row["ocn_O2"]["correlation"] >= 0.99)
        rows.append(row)
    results[name] = {"sha256": sha256(path), "run_times": run_times.tolist(), "all_declared_slices_pass": all(row["pass"] for row in rows), "slices": rows}
    run.close()

mi = nc.Dataset(mi_path)
hv, temp, oxygen = (valid(mi[key][:]) for key in ("habitat_viability", "temperature", "pO2"))
observed = ~(np.ma.getmaskarray(hv) | np.ma.getmaskarray(temp) | np.ma.getmaskarray(oxygen))
T, P = temp.data[observed] + 273.15, oxygen.data[observed]
A, E, C = (np.asarray(mi[key][:], dtype=float) for key in ("A0", "E0", "phi_crit"))
x = (1 / T - 1 / 288.15) / 8.61733326e-5
positive = P > 0
p = np.zeros_like(P)
p[positive] = ndtr((3.01 + np.log(P[positive]) + 0.41 * x[positive] - 1.10) / np.sqrt(0.49**2 + 0.42**2 + 0.29**2 * x[positive]**2))
se = np.sqrt(np.maximum(p * (1 - p), 1 / len(A)) / len(A))
phi = A[None, :] * P[:, None] * np.exp(E[None, :] * x[:, None])
predicted = phi >= C[None, :]
stored = mi["ecotype_viability"][:]
stored_valid = ~np.ma.getmaskarray(stored)
stored_data = np.ma.asarray(stored).filled(0)
matrix = stored_data[:, observed].T
outside = ~observed
source_time = int(np.flatnonzero(np.isclose(times, 7999.5, atol=1e-6, rtol=0))[0])
depth = np.asarray(mi["Depth"][:])
source_depth = np.asarray(ref["zt"][:])
indices = [int(np.argmin(abs(source_depth - d))) for d in depth]
source_temp = valid(ref["ocn_temp"][source_time][indices])
summary = {
    "reference_sha256": sha256(reference),
    "mi_sha256": sha256(mi_path),
    "reference_times": times.tolist(),
    "cgenie": results,
    "metabolic": {
        "evaluated_cells": int(observed.sum()),
        "nonpositive_po2_cells": int((~positive).sum()),
        "m1_max_abs_z": float(np.max(np.abs((hv.data[observed] / 100 - p) / se))),
        "m2_max_abs_diff_percent": float(np.max(np.abs(predicted.mean(axis=1) * 100 - hv.data[observed]))),
        "m2_matrix_mismatches": int(np.count_nonzero(matrix != predicted)),
        "unevaluated_cells": int(outside.sum()),
        "unmasked_ecotype_values_outside_evaluated_cells": int(stored_valid[:, outside].sum()),
        "source_temp_max_abs_difference": float(np.max(np.abs(source_temp.data[observed] - temp.data[observed]))),
        "source_temp_missing_in_evaluated_cells": int(np.ma.getmaskarray(source_temp)[observed].sum()),
    },
}
print(json.dumps(summary, indent=2, allow_nan=False))
