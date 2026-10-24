# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pygplates==1.0.0"]
# ///
"""Profile the mirrored plate models, and test them against the palaeocoordinates in NSB, Triton and PBDB.

Usage: uv run palaeogeography_profile.py MODELS_RAW WRIGHT_RAW PALEODEM_RAW NSB_SQLITE TRITON_TSV_GZ PBDB_GLOBAL_RAW OUT_TSV

Inventory: for each model in the GPlates Plate Model Manager snapshot, the rotation
files' pole count, moving plate IDs and time span, and the static polygons' count;
the PaleoDEM zips' members, and the ages their file names give.

Reconstruction: a present-day point takes the plate ID of the static polygon it
falls in (partitioned at 0 Ma) and is rotated to the requested age, relative to
the model's anchor plate 0. A point whose polygon begins after that age (e.g.
young ocean floor) has no palaeoposition. Distances are great-circle degrees.

Tests (each one sentence in the output):
  1. NSB's own Seton et al. (2012) palaeocoordinates (neptune_paleogeography)
     against seton2012 here; NSB's assigned plate IDs against ours.
  2. The same NSB holes and ages under matthews2016 (mantle and palaeomagnetic
     reference frames): how far the palaeolatitudes move.
  3. Triton's non-Neptune rows (Matthews et al. 2016, whole-Ma ages) against
     both matthews2016 frames; Triton's Neptune rows (NSB's Seton coordinates)
     against matthews2016 at the row's age.
  4. PBDB's palaeocoordinates (three models per collection) against candidate
     models here: seton2012, the Wright et al. (2013) supplement, paleomap and
     scotese_and_wright2018.
"""

import collections
import csv
import glob
import gzip
import math
import os
import re
import sqlite3
import statistics
import sys
import tempfile
import zipfile

import pygplates

models_raw, wright_raw, paleodem_raw, nsb_db, triton_gz, pbdb_raw, out_tsv = sys.argv[1:8]
csv.field_size_limit(1 << 30)
out = []
TMP = tempfile.mkdtemp()


def put(table, metric, key, value):
    out.append([table, metric, key, value])


def unzip(path, sub):
    d = os.path.join(TMP, sub)
    with zipfile.ZipFile(path) as z:
        z.extractall(d)
    return d


def files(d, exts):
    return sorted(p for p in glob.glob(os.path.join(d, "**", "*"), recursive=True)
                  if p.lower().endswith(exts) and "__MACOSX" not in p and not os.path.basename(p).startswith("._"))


class Model:
    def __init__(self, name, rot_files, poly_files):
        self.name = name
        self.rot = pygplates.RotationModel(rot_files)
        self.polys = [f for p in poly_files for f in pygplates.FeatureCollection(p)]
        self.part = pygplates.PlatePartitioner(self.polys, self.rot)
        self.cache = {}

    def plate(self, lat, lon):
        k = (round(lat, 4), round(lon, 4))
        if k not in self.cache:
            rfg = self.part.partition_point(pygplates.PointOnSphere(lat, lon))
            if rfg is None:
                self.cache[k] = None
            else:
                f = rfg.get_feature()
                begin = f.get_valid_time()[0]  # a float; the distant past is +inf
                self.cache[k] = (f.get_reconstruction_plate_id(), float(begin))
        return self.cache[k]

    def reconstruct(self, lat, lon, age):
        p = self.plate(lat, lon)
        if p is None or p[1] < age:
            return None
        rot = self.rot.get_rotation(float(age), p[0])
        la, lo = (rot * pygplates.PointOnSphere(lat, lon)).to_lat_lon()
        return la, lo, p[0]


def gc(a_lat, a_lon, b_lat, b_lon):
    p1, p2 = math.radians(a_lat), math.radians(b_lat)
    d = math.sin((p2 - p1) / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(math.radians(b_lon - a_lon) / 2) ** 2
    return math.degrees(2 * math.asin(min(1, math.sqrt(d))))


def q(xs, f):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(f * len(xs)))] if xs else float("nan")


def summary(ds):
    if not ds:
        return "none"
    return (f"n {len(ds)}; median {statistics.median(ds):.2f}; 95th {q(ds, 0.95):.2f}; max {max(ds):.2f}; "
            f"within 0.5 {sum(d <= 0.5 for d in ds) / len(ds):.1%}; within 1 {sum(d <= 1 for d in ds) / len(ds):.1%}; "
            f"over 10: {sum(d > 10 for d in ds)}")


# ---- inventory ----------------------------------------------------------------
v = sorted(glob.glob(os.path.join(models_raw, "*")))[-1]  # url snapshots are timestamped, so names sort by time
names = sorted({os.path.basename(p).split("__")[0] for p in glob.glob(os.path.join(v, "*__Rotations.zip"))})
put("models", "snapshot", "", os.path.basename(v))
put("models", "models with rotations", "", len(names))
loaded = {}
for n in names:
    rd = unzip(os.path.join(v, f"{n}__Rotations.zip"), f"{n}_rot")
    rots = files(rd, (".rot", ".grot"))
    poles, plates, ages = 0, set(), []
    for r in rots:
        for f in pygplates.FeatureCollection(r):
            trs = f.get_total_reconstruction_pole()
            if trs:
                fixed, moving, seq = trs
                plates.add(moving)
                for s in seq.get_enabled_time_samples():
                    poles += 1
                    ages.append(float(s.get_time()))
    sp = os.path.join(v, f"{n}__StaticPolygons.zip")
    polys = files(unzip(sp, f"{n}_sp"), (".gpml", ".gpmlz", ".shp")) if os.path.exists(sp) else []
    if any(p.endswith((".gpml", ".gpmlz")) for p in polys):
        polys = [p for p in polys if p.endswith((".gpml", ".gpmlz"))]
    npoly = sum(len(pygplates.FeatureCollection(p)) for p in polys)
    put("models", n, "rotation files; poles; moving plates; oldest pole (Ma); static polygons",
        f"{len(rots)}; {poles}; {len(plates)}; {max(ages) if ages else 0:g}; {npoly}")
    if polys and rots:
        loaded[n] = (rots, polys)


pv = sorted(glob.glob(os.path.join(paleodem_raw, "*")))[-1]
put("paleodem", "version", "", os.path.basename(pv))
for zp in sorted(glob.glob(os.path.join(pv, "*.zip"))):
    with zipfile.ZipFile(zp) as z:
        names = [i.filename for i in z.infolist() if not i.is_dir() and "__MACOSX" not in i.filename]
    exts = collections.Counter(n.rsplit(".", 1)[-1].lower() for n in names if "." in os.path.basename(n))
    ages = sorted({float(m) for n in names for m in re.findall(r"_(\d+(?:\.\d+)?)Ma\.(?:nc|csv)$", n)})
    put("paleodem", os.path.basename(zp), "members; by extension; ages from file names (Ma)",
        f"{len(names)}; {', '.join(f'{e} {c}' for e, c in exts.most_common(6))}; "
        + (f"{len(ages)} ages, {ages[0]:g}-{ages[-1]:g}" if ages else "none"))


def model(n):
    if n not in loaded:
        return None
    if isinstance(loaded[n], tuple):
        loaded[n] = Model(n, *loaded[n])
    return loaded[n]


# Wright et al. 2013 supplement
wv = sorted(glob.glob(os.path.join(wright_raw, "*")))[-1]
wd = unzip(glob.glob(os.path.join(wv, "*.zip"))[0], "wright")
inner = files(wd, (".zip",))
for i, zp in enumerate(inner):
    unzip(zp, f"wright/inner{i}")
w_rots, w_polys = files(wd, (".rot", ".grot")), files(wd, (".gpml", ".gpmlz", ".shp"))
put("wright2013", "supplement files (rotations, polygons)", "", "; ".join(os.path.relpath(p, wd) for p in w_rots + w_polys)[:900])
# the supplement has no static polygons; its continental regions partition the points
w_static = ([p for p in w_polys if "static" in os.path.basename(p).lower()]
            or [p for p in w_polys if "continentalregions" in os.path.basename(p).lower()])
if w_rots and w_static:
    loaded["wright2013"] = (w_rots, w_static)
    put("wright2013", "rotation files; static polygon files used", "", f"{'; '.join(os.path.basename(p) for p in w_rots)} | {'; '.join(os.path.basename(p) for p in w_static)}")


def compare(label, rows, mdl, key=""):
    """rows: (lat, lon, age, ref_lat, ref_lon, ref_plate or None)"""
    m = model(mdl)
    if m is None:
        put(label, mdl, key, "model not loaded")
        return
    ds, dlat, plate_same, plate_n, none = [], [], 0, 0, 0
    for lat, lon, age, rlat, rlon, rplate in rows:
        r = m.reconstruct(lat, lon, age)
        if r is None:
            none += 1
            continue
        ds.append(gc(r[0], r[1], rlat, rlon))
        dlat.append(abs(r[0] - rlat))
        if rplate not in (None, ""):
            plate_n += 1
            plate_same += int(r[2]) == int(float(rplate))
    put(label, mdl, key + "distance (deg)", summary(ds))
    put(label, mdl, key + "abs palaeolatitude difference (deg)", summary(dlat))
    put(label, mdl, key + "not reconstructable here", none)
    if plate_n:
        put(label, mdl, key + "plate ID agrees", f"{plate_same} of {plate_n} ({plate_same / plate_n:.1%})")


# ---- 1, 2: NSB --------------------------------------------------------------
con = sqlite3.connect(nsb_db)
holes = {h: (la, lo) for h, la, lo in con.execute("select hole_id, latitude, longitude from neptune_hole_summary")}
nsb = [(holes[h][0], holes[h][1], a, plat, plon, pid) for h, a, plon, plat, src, pid in con.execute(
    "select hole_id, reconstructed_age_ma, paleo_longitude, paleo_latitude, rotation_source, assigned_plate_id from neptune_paleogeography")
       if h in holes and holes[h][0] is not None and plat is not None]
put("nsb", "palaeogeography rows with hole coordinates", "", len(nsb))
put("nsb", "ages (Ma)", "", f"{min(r[2] for r in nsb):g}-{max(r[2] for r in nsb):g}")
compare("nsb vs seton2012", nsb, "seton2012")
for m in ("matthews2016_mantle_ref", "matthews2016_pmag_ref"):
    compare("nsb holes, Seton (NSB) vs", [r[:5] + (None,) for r in nsb], m)
    for lo, hi in ((0, 23.03), (23.03, 66.0), (66.0, 145.0), (145.0, 201.0)):
        compare("nsb holes, Seton (NSB) vs", [r[:5] + (None,) for r in nsb if lo <= r[2] < hi], m, f"{lo:g}-{hi:g} Ma: ")

# ---- 3: Triton ----------------------------------------------------------------
nonnep, nep = collections.Counter(), collections.Counter()
with gzip.open(triton_gz, "rt", encoding="utf-8", errors="replace") as f:
    for r in csv.DictReader(f, delimiter="\t"):
        try:
            lat, lon, plat, plon = float(r["latitude"]), float(r["longitude"]), float(r["pal.lat"]), float(r["pal.long"])
        except (TypeError, ValueError):
            continue
        if r["db.source"] == "Neptune":
            nep[(lat, lon, float(r["age"]), plat, plon)] += 1
        else:
            nonnep[(lat, lon, float(r["round.age"]), plat, plon)] += 1
put("triton", "distinct (place, age, palaeoposition): non-Neptune; Neptune", "", f"{len(nonnep)}; {len(nep)}")
for m in ("matthews2016_mantle_ref", "matthews2016_pmag_ref"):
    compare("triton non-Neptune vs", [k + (None,) for k in nonnep], m)
    compare("triton Neptune (Seton, from NSB) vs", [k + (None,) for k in nep], m)

# ---- 4: PBDB --------------------------------------------------------------------
cands = {"seton": ["seton2012"], "gplates": ["wright2013", "matthews2016_mantle_ref"], "scotese": ["paleomap", "scotese_and_wright2018"]}
pb = collections.defaultdict(list)
for p in sorted(glob.glob(os.path.join(pbdb_raw, "collections__p*.csv"))):
    with open(p, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                lat, lon = float(r["lat"]), float(r["lng"])
            except (TypeError, ValueError):
                continue
            for sfx in ("", "2", "3"):
                mod, basis = r.get("paleomodel" + sfx), r.get("paleoage" + sfx)  # basis: early, mid or late
                try:
                    hi, lo = float(r["max_ma"]), float(r["min_ma"])
                    age = {"early": hi, "late": lo, "mid": (hi + lo) / 2}[basis]
                    row = (lat, lon, age, float(r["paleolat" + sfx]), float(r["paleolng" + sfx]), r.get("geoplate" + sfx))
                except (KeyError, TypeError, ValueError):
                    continue
                pb[mod].append(row)
for mod, rows in sorted(pb.items()):
    put("pbdb", f"collections with {mod} palaeocoordinates", "", len(rows))
    step = max(1, len(rows) // 20000)
    sample = rows[::step]
    for m in cands.get(mod, []):
        compare(f"pbdb {mod} vs", sample, m, f"every {step}th collection, age as given: ")
        compare(f"pbdb {mod} vs", [(a, b, round(c), d, e, f) for a, b, c, d, e, f in sample], m, f"every {step}th collection, age rounded to 1 Ma: ")

with open(out_tsv, "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh, delimiter="\t", lineterminator="\n")
    w.writerow(["table", "metric", "key", "value"])
    w.writerows(out)
print(len(out), "rows")
