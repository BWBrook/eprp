# /// script
# requires-python = ">=3.10"
# dependencies = ["netCDF4==1.7.2", "numpy==2.2.6"]
# ///
"""Profile Beyer et al. (2020) Late Quaternary climate NetCDFs for Sahul.

Usage: uv run beyer_profile.py ENVIRONMENT_NC MONTHLY_NPP_NC OUT_TSV

Reports dimensions, attributes and coordinate units; for a Sahul window
(110-155E, 45S-0) the land area implied by the data's own land mask, mean BIO1
and BIO12 over land, and biome counts at chosen times; and how the annual
biome and NPP in the monthly-NPP file differ from the main file.
"""

import csv
import sys

import netCDF4
import numpy as np

TIMES = [0, -6000, -12000, -21000, -30000, -40000, -50000, -60000, -80000, -100000, -120000]
out = []


def add(*row):
    out.append(row)


env = netCDF4.Dataset(sys.argv[1])
npp = netCDF4.Dataset(sys.argv[2])
for k in env.ncattrs():
    if k != "Contact":  # a personal email address; not reproduced
        add("attrs", "global", k, str(env.getncattr(k))[:200])
for name, d in env.dimensions.items():
    add("dims", name, "", len(d))
for name, v in env.variables.items():
    add("variables", name, str(v.dimensions), f'{getattr(v, "units", "")} | {getattr(v, "long_name", "")}'[:160])
lon, lat, time = env["longitude"][:], env["latitude"][:], env["time"][:]
add("time", "steps", "", len(time))
add("time", "range", "", f"{time.min()} to {time.max()}")
xi = np.where((lon >= 110) & (lon <= 155))[0]
yi = np.where((lat >= -45) & (lat <= 0))[0]
cell_km2 = (0.5 * 111.32) ** 2 * np.cos(np.radians(lat[yi]))[:, None] * np.ones(len(xi))[None, :]
LA, LO = np.meshgrid(lat[yi], lon[xi], indexing="ij")
sahul = (((LA <= -10.6) & (LO >= 112)) | ((LO >= 130.8) & (LA >= -12))
         | ((LO >= 141) & (LO <= 144.5) & (LA > -10.6) & (LA <= -9)))  # boxes as in rpd_profile.py
sahul_now = None
for t in TIMES:
    ti = int(np.where(time == t)[0][0])
    b1 = np.ma.filled(env["BIO1"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
    b12 = np.ma.filled(env["BIO12"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
    land = ~np.isnan(b1)
    add("sahul_window", "land_cells", t, int(land.sum()))
    add("sahul_window", "land_area_km2", t, int(cell_km2[land].sum()))
    s_area = float(cell_km2[land & sahul].sum())
    sahul_now = s_area if t == 0 else sahul_now
    add("sahul_boxes", "land_area_km2", t, int(s_area))
    add("sahul_boxes", "land_gain_vs_0ka_km2", t, int(s_area - sahul_now))
    add("sahul_window", "bio1_mean_land_c", t, round(float(np.nanmean(b1)), 2))
    add("sahul_window", "bio12_mean_land_mm", t, round(float(np.nanmean(b12)), 1))
    if t in (0, -21000):
        bio = np.ma.filled(env["biome"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
        vals, counts = np.unique(bio[~np.isnan(bio)], return_counts=True)
        for v, c in sorted(zip(vals, counts), key=lambda x: -x[1])[:8]:
            add("sahul_window", f"biome_cells_{t}", int(v), int(c))
        bio2 = np.ma.filled(npp["biome"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
        both = ~np.isnan(bio) & ~np.isnan(bio2)
        add("monthly_npp_file_vs_main", "biome_cells_differing", t, int((bio[both] != bio2[both]).sum()))
        n1 = np.ma.filled(env["npp"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
        n2 = np.ma.filled(npp["npp"][ti, yi[0]:yi[-1] + 1, xi[0]:xi[-1] + 1].astype(float), np.nan)
        ok = ~np.isnan(n1) & ~np.isnan(n2)
        add("monthly_npp_file_vs_main", "npp_correlation", t, round(float(np.corrcoef(n1[ok], n2[ok])[0, 1]), 3))
        add("monthly_npp_file_vs_main", "same_land_mask", t, bool((np.isnan(n1) == np.isnan(n2)).all()))

with open(sys.argv[3], "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
