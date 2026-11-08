"""Run raw-model pyGPlates replay, then separate Euler/geometry controls.

Usage: python replay_plate.py REPO_ROOT RAW_MODEL_DIR OUTPUT_DIR
Model archives and the archived service response are fixed inputs, not live APIs.
"""
import csv
import hashlib
import json
import math
import pathlib
import platform
import statistics
import subprocess
import sys
import tempfile

import numpy as np
import pygplates

repo, raw, out = map(pathlib.Path, sys.argv[1:])
out.mkdir(parents=True, exist_ok=True)
bench = repo / "resources/software/bench"


def digest(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rows(p):
    with open(p) as f:
        return list(csv.DictReader(f, delimiter="\t"))


def vector(lat, lon):
    a, b = math.radians(float(lat)), math.radians(float(lon))
    return np.array([math.cos(a)*math.cos(b), math.cos(a)*math.sin(b), math.sin(a)])


def distances(p, q):
    return np.degrees(np.arctan2(np.linalg.norm(np.cross(p, q), axis=-1), np.sum(p*q, axis=-1)))


def basis(a, b):
    a = a / np.linalg.norm(a)
    c = b - np.dot(a, b)*a
    c /= np.linalg.norm(c)
    return np.column_stack((a, c, np.cross(a, c)))


def frame(p, q):
    # One well-conditioned point pair defines oriented bases; no optimisation/SVD.
    first = 0
    second = int(np.argmin(np.abs(p @ p[first])))
    r = basis(q[first], q[second]) @ basis(p[first], p[second]).T
    residual = distances(p @ r.T, q)
    pairwise = np.max(np.abs(p @ p.T - q @ q.T))
    return dict(n=len(p), selected_pair=[first, second],
                max_residual_deg=float(max(residual)), median_residual_deg=float(statistics.median(residual)),
                rotation_deg=float(math.degrees(math.acos(np.clip((np.trace(r)-1)/2, -1, 1)))),
                max_pairwise_dot_change=float(pairwise), determinant=float(np.linalg.det(r)))


def quantile(x, p):
    x = sorted(x)
    j = (len(x)-1)*p
    i = int(j)
    return x[i] + (j-i)*(x[min(i+1, len(x)-1)]-x[i])


with tempfile.TemporaryDirectory() as tmp:
    fresh = pathlib.Path(tmp)/"fresh.tsv"
    subprocess.run([sys.executable, str(bench/"validate/t3_rotate.py"), str(raw),
                    str(bench/"results/t3/v6_points.tsv"), str(fresh)], check=True)
    replay = rows(fresh)
    fresh_hash = digest(fresh)

old = rows(bench/"results/t3/v6_merged.tsv")
key = lambda x: (x["collection_no"], x["age"], x["model"])
old_map = {key(x): x for x in old}
assert len(old_map) == len(replay) == 7200
missing_agrees = all(bool(r["p_lat"]) == bool(old_map[key(r)]["p_lat"]) for r in replay)
assert missing_agrees
archive_delta = max(abs(float(r[c])-float(old_map[key(r)][c])) for r in replay if r["p_lat"] for c in ("p_lat", "p_lng"))
assert archive_delta < 1e-10

models = {"MERDITH2021":"merdith2021", "PALEOMAP":"paleomap",
          "TorsvikCocks2017":"torsvikcocks2017", "MATTHEWS2016_pmag_ref":"matthews2016_pmag_ref"}
archive_hashes = {f"{name}__{layer}.zip":digest(raw/f"{name}__{layer}.zip")
                  for name in models.values() for layer in ("Rotations", "StaticPolygons")}
frame_results = {}
for model in ("TorsvikCocks2017", "MERDITH2021"):
    frame_results[model] = {}
    for age in (10,50,100,200,300,400):
        g = [r for r in replay if r["model"] == model and int(r["age"]) == age and r["p_lat"] and old_map[key(r)]["a_lat"]]
        p = np.array([vector(r["p_lat"],r["p_lng"]) for r in g])
        q = np.array([vector(old_map[key(r)]["a_lat"],old_map[key(r)]["a_lng"]) for r in g])
        fitted = frame(p,q)
        fitted["median_offset_before_deg"] = float(statistics.median(distances(p,q)))
        frame_results[model][str(age)] = fitted
        assert fitted["max_residual_deg"] < 0.0002

fixed = np.array([vector(10,20),vector(-20,70),vector(50,-110),vector(-30,-150)])
a = math.radians(23)
r = np.array([[math.cos(a),-math.sin(a),0],[math.sin(a),math.cos(a),0],[0,0,1]])
positive = frame(fixed, fixed @ r.T)
damaged = fixed @ r.T
damaged[3] = vector(-20,-127)
negative = frame(fixed, damaged)
assert positive["max_residual_deg"] < 1e-10 and negative["max_residual_deg"] > 1

three = {"MERDITH2021", "PALEOMAP", "MATTHEWS2016_pmag_ref"}
latitudes = {}
for r in replay:
    if r["model"] in three and r["p_lat"]:
        latitudes.setdefault((r["collection_no"],int(r["age"])),{})[r["model"]] = float(r["p_lat"])
spreads = {k:max(v.values())-min(v.values()) for k,v in latitudes.items() if len(v)==3}
ids = {k[0] for k in spreads}
always = {i for i in ids if sum(k[0]==i for k in spreads)==6}
spread_results = {}
for label, values in (("all_reconstructable",spreads), ("reconstructable_at_all_ages",{k:v for k,v in spreads.items() if k[0] in always})):
    spread_results[label] = {}
    for age in (10,50,100,200,300,400):
        v = [v for k,v in values.items() if k[1]==age]
        spread_results[label][str(age)] = dict(n=len(v), median_deg=statistics.median(v), q90_deg=quantile(v,.9))

result = dict(case=9, claims=["C123","C125"], environment=dict(python=platform.python_version(), numpy=np.__version__,pygplates=str(pygplates.Version.get_imported_version())),
    inputs=dict(model_archive_sha256=archive_hashes, points_sha256=digest(bench/"results/t3/v6_points.tsv"),
                archived_routes_sha256=digest(bench/"results/t3/v6_merged.tsv"), original_script_sha256=digest(bench/"validate/t3_rotate.py")),
    raw_model_replay=dict(rows=len(replay), fresh_tsv_sha256=fresh_hash, max_coordinate_delta_from_retained=archive_delta, missing_pattern_agrees=missing_agrees),
    independent_route="Two-point oriented orthonormal basis rotation and all-pair dot-product invariance, no least-squares/SVD; plain-Python latitude spread census",
    frame_fit=frame_results, frame_controls=dict(rigid_positive=positive, nonrigid_negative=negative), spread_three_models=spread_results,
    limits="Raw model reconstructions replayed in pyGPlates 1.0.0. Frame comparison uses fixed archived web-service coordinates; no fresh web-service request or independent plate partition implementation. Near-rigid differences established only for these sampled ages and points, not a proof of globally identical relative plate motions. Neither frame is identified as incorrect. Spread is structural model choice, not calibrated error.")
(out/"case09_plate_models.json").write_text(json.dumps(result,indent=2)+"\n")
