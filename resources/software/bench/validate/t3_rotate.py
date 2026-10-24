"""Tranche-3 V6, route (c): pyGPlates on the mirrored plate models (../VALIDATION_T3.md).

Usage: python t3_rotate.py <models_raw_dir> <points_tsv> <out_tsv>
A point takes the plate of the static polygon containing it at 0 Ma and is
rotated to the age relative to anchor plate 0, following the data
catalogue's palaeogeography profiler (`palaeogeography_profile.py`, Model).
"""

import csv
import glob
import os
import sys
import tempfile
import zipfile

import pygplates

raw, points_tsv, out_tsv = sys.argv[1:4]
MODELS = {"MERDITH2021": "merdith2021", "PALEOMAP": "paleomap", "TorsvikCocks2017": "torsvikcocks2017",
          "MATTHEWS2016_pmag_ref": "matthews2016_pmag_ref"}
AGES = [10, 50, 100, 200, 300, 400]
tmp = tempfile.mkdtemp()


def unpack(name, layer):
    d = os.path.join(tmp, name, layer)
    with zipfile.ZipFile(os.path.join(raw, f"{name}__{layer}.zip")) as z:
        z.extractall(d)
    keep = (".rot", ".grot") if layer == "Rotations" else (".gpml", ".gpmlz", ".shp")
    return sorted(p for p in glob.glob(os.path.join(d, "**", "*"), recursive=True)
                  if p.lower().endswith(keep) and "__MACOSX" not in p and not os.path.basename(p).startswith("._"))


with open(points_tsv) as f:
    pts = list(csv.DictReader(f, delimiter="\t"))

with open(out_tsv, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["collection_no", "lng", "lat", "age", "model", "plate_id", "p_lng", "p_lat"])
    for model, name in MODELS.items():
        rot = pygplates.RotationModel(unpack(name, "Rotations"))
        polys = [ft for p in unpack(name, "StaticPolygons") for ft in pygplates.FeatureCollection(p)]
        part = pygplates.PlatePartitioner(polys, rot)
        for p in pts:
            lat, lng = float(p["lat"]), float(p["lng"])
            rfg = part.partition_point(pygplates.PointOnSphere(lat, lng))
            plate = begin = None
            if rfg is not None:
                ft = rfg.get_feature()
                plate, begin = ft.get_reconstruction_plate_id(), float(ft.get_valid_time()[0])
            for age in AGES:
                if plate is None or begin < age:
                    w.writerow([p["collection_no"], lng, lat, age, model, plate if plate is not None else "", "", ""])
                    continue
                la, lo = (rot.get_rotation(float(age), plate) * pygplates.PointOnSphere(lat, lng)).to_lat_lon()
                w.writerow([p["collection_no"], lng, lat, age, model, plate, f"{lo:.6f}", f"{la:.6f}"])
        print(model, "done", flush=True)
