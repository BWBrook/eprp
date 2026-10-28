import json
import subprocess
import sys
import tempfile
from pathlib import Path

import netCDF4 as nc
import numpy as np


script = Path(sys.argv[1]).resolve()


def fixture(path, times):
    with nc.Dataset(path, "w") as f:
        for name, size in (("time", len(times)), ("z", 2), ("zedge", 3), ("lat", 2), ("lon", 2)):
            f.createDimension(name, size)
        f.createVariable("time", "f8", ("time",))[:] = times
        f.createVariable("zt_edges", "f8", ("zedge",))[:] = [0, 1, 3]
        f.createVariable("grid_area", "f8", ("lat", "lon"))[:] = [[1, 2], [3, 4]]
        for name in ("ocn_temp", "ocn_O2"):
            a = f.createVariable(name, "f8", ("time", "z", "lat", "lon"))
            base = np.arange(1, 9, dtype=float).reshape(2, 2, 2)
            a[:] = np.stack([base if name == "ocn_temp" else base * 1e-6 for _ in times])


with tempfile.TemporaryDirectory() as temp:
    root = Path(temp)
    ref, run, out = (root / name for name in ("reference.nc", "run.nc", "out.json"))
    fixture(ref, [9.5, 999.5, 1999.5])
    for times, complete, missing in (([999.5, 1999.5], True, []), ([999.5], False, [1999.5]), ([9.5], False, [999.5, 1999.5])):
        fixture(run, times)
        subprocess.run([sys.executable, str(script), str(run), str(ref), str(out)], check=True, capture_output=True)
        result = json.loads(out.read_text())
        assert result["complete"] is complete
        assert result["missing_graded_times"] == missing
        assert result["graded_slices_expected"] == 2
        assert result["ungraded_complete"] is (9.5 in times)
        assert result["pass_so_far"] is (True if 999.5 in times else None)
    print("complete, missing-graded, and ungraded-only cases passed")
