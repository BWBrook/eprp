"""Tranche-3 follow-up checks after the independent review (../VALIDATION_T3.md A2).

Usage: python t3_checks.py <results_t3_dir> <models_raw_dir>
1. TorsvikCocks2017: per age, the best rigid rotation taking the pyGPlates
   positions onto the GPlates Web Service positions (Kabsch on unit vectors):
   residual, angle and pole. MERDITH2021 as a control.
2. The palaeolatitude spread across MERDITH2021, PALEOMAP and
   MATTHEWS2016_pmag_ref (pyGPlates), by age, for all reconstructable points
   and for the points reconstructable at every age.
3. The mirrored TorsvikCocks2017 StaticPolygons and Coastlines layers: members
   and sizes; points left without a plate, by model.
4. Grid-route omissions: point-ages the Web Service reconstructs but the grid
   does not.
"""

import json
import pathlib
import sys
import zipfile

import numpy as np
import pandas as pd

d, raw = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
m = pd.read_csv(d / "v6_merged.tsv", sep="\t")
out = {}


def unit(lat, lng):
    la, lo = np.radians(lat), np.radians(lng)
    return np.column_stack([np.cos(la) * np.cos(lo), np.cos(la) * np.sin(lo), np.sin(la)])


def kabsch(p, q):
    h = p.T @ q
    u, _, vt = np.linalg.svd(h)
    s = np.diag([1, 1, np.sign(np.linalg.det(vt.T @ u.T))])
    r = vt.T @ s @ u.T
    resid = np.degrees(np.arccos(np.clip(np.sum((p @ r.T) * q, axis=1), -1, 1)))
    angle = np.degrees(np.arccos(np.clip((np.trace(r) - 1) / 2, -1, 1)))
    w, v = np.linalg.eig(r)
    axis = np.real(v[:, np.argmin(np.abs(w - 1))])
    pole = (float(np.degrees(np.arcsin(axis[2]))), float(np.degrees(np.arctan2(axis[1], axis[0]))))
    return float(np.max(resid)), float(np.median(resid)), float(angle), pole


out["frame_fit"] = {}
for model in ("TorsvikCocks2017", "MERDITH2021"):
    x = m[(m.model == model)].dropna(subset=["a_lat", "p_lat"])
    out["frame_fit"][model] = {}
    for age, g in x.groupby("age"):
        mx, md, ang, pole = kabsch(unit(g.p_lat, g.p_lng), unit(g.a_lat, g.a_lng))
        out["frame_fit"][model][str(int(age))] = {"n": int(len(g)), "max_residual_deg": mx, "median_residual_deg": md,
                                                  "rotation_deg": ang, "pole_lat_lng": pole,
                                                  "median_offset_before_deg": float(g.d_ac.median())}

three = ["MERDITH2021", "PALEOMAP", "MATTHEWS2016_pmag_ref"]
w = m.pivot_table(index=["collection_no", "age"], columns="model", values="p_lat")[three].dropna()
sp = w.max(axis=1) - w.min(axis=1)
always = sp.groupby(level="collection_no").size()
always = set(always[always == 6].index)
out["spread_three_models"] = {}
for label, s in (("all_reconstructable", sp), ("reconstructable_at_all_ages", sp[sp.index.get_level_values(0).isin(always)])):
    out["spread_three_models"][label] = {str(int(a)): {"n": int(len(v)), "median_deg": float(v.median()), "q90_deg": float(v.quantile(0.9))}
                                         for a, v in s.groupby(level="age")}

layers = {}
for layer in ("StaticPolygons", "Coastlines"):
    with zipfile.ZipFile(raw / f"torsvikcocks2017__{layer}.zip") as z:
        layers[layer] = [(i.filename, i.file_size) for i in z.infolist() if not i.is_dir()]
out["torsvikcocks2017_layers"] = layers
out["unassigned_points_pygplates"] = {mod: int(m[(m.model == mod) & (m.age == 10)].plate_id.isna().sum()) for mod in m.model.unique()}
out["grid_omissions"] = {mod: int((m[m.model == mod].a_lat.notna() & m[m.model == mod].b_lat.isna()).sum()) for mod in m.model.unique()}
(d / "t3_checks.json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
