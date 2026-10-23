"""C3: field (Kerr et al., Dryad 10.5061/dryad.p5hqbzm03, CC0) versus OBIS composite gradient on matched latitudes.
Usage: python3 -I attenuation.py FIELD_DIR OBIS_JSON"""
import collections, csv, json, math, sys
import numpy as np

def hurlbert(counts, n):
    N = sum(counts)
    if N < n:
        return float("nan")
    lc = math.lgamma
    base = lc(N + 1) - lc(n + 1) - lc(N - n + 1)
    return sum(1 - math.exp(lc(N - c + 1) - lc(n + 1) - lc(N - c - n + 1) - base) if N - c >= n else 1.0 for c in counts)

fdir, obis = sys.argv[1], sys.argv[2]
sites = {r["site"]: float(r["lat"]) for r in csv.DictReader(open(f"{fdir}/SiteMetadata.csv"), delimiter=";")}
field = collections.defaultdict(collections.Counter)
for r in csv.DictReader(open(f"{fdir}/bivalvefieldcollection_Kerr.csv"), delimiter=";"):
    if r["species"].strip():
        field[r["site"]][r["species"].strip()] += int(r["n"])
rows = [r for r in json.load(open(obis))["rows"] if r.get("species") and r.get("decimalLatitude") is not None]
spec = {"PreservedSpecimen", "MATERIAL_SAMPLE", "MaterialSample", "LivingSpecimen", "Occurrence"}
obs = {"HumanObservation"}

def obis_window(lat, sub, half=1.0):
    c = collections.Counter(r["species"] for r in sub if abs(r["decimalLatitude"] - lat) <= half)
    return list(c.values())

out = []
nf = min(sum(c.values()) for c in field.values())
for site, lat in sorted(sites.items(), key=lambda x: -x[1]):
    c = list(field[site].values())
    out.append(dict(site=site, lat=lat, field_valves=sum(c), field_S=len(c), field_rare=hurlbert(c, min(nf, 150)),
                    obis_all=obis_window(lat, rows), obis_spec=obis_window(lat, [r for r in rows if r.get("basisOfRecord") in spec]),
                    obis_obs=obis_window(lat, [r for r in rows if r.get("basisOfRecord") in obs])))
nr = 150
print(f"min field valves per site {nf}; rarefaction to {min(nf, nr)} valves (field) and {nr} records (OBIS, +-1 deg windows)")
def slope(key):
    lat = np.array([abs(o["lat"]) for o in out])
    y = np.array([o[key] for o in out])
    ok = np.isfinite(y) & (y > 0)
    b, a = np.polyfit(lat[ok], np.log(y[ok]), 1)
    r = np.corrcoef(lat[ok], np.log(y[ok]))[0, 1]
    return b, r, int(ok.sum())
for o in out:
    o["obis_all_rare"] = hurlbert(o["obis_all"], nr); o["obis_spec_rare"] = hurlbert(o["obis_spec"], nr)
    o["obis_obs_rare"] = hurlbert(o["obis_obs"], nr)
    print(f"{o['site']:16s} {o['lat']:6.2f} field valves {o['field_valves']:5d} S {o['field_S']:3d} rare {o['field_rare']:5.1f} | "
          f"OBIS all {sum(o['obis_all']):5d} rare {o['obis_all_rare']:6.1f} | spec rare {o['obis_spec_rare']:6.1f} | obs rare {o['obis_obs_rare']:6.1f}")
res = {}
for key in ("field_rare", "obis_all_rare", "obis_spec_rare", "obis_obs_rare"):
    b, r, k = slope(key)
    res[key] = dict(slope_per_degree=b, change_over_10_degrees=math.exp(10 * b), r=r, sites=k)
    print(f"{key:15s} slope {b:+.4f}/deg  x{math.exp(10*b):.2f} per 10 deg  r={r:+.2f}  n={k}")
for key in ("obis_all_rare", "obis_spec_rare", "obis_obs_rare"):
    res[key]["attenuation_vs_field"] = res[key]["slope_per_degree"] / res["field_rare"]["slope_per_degree"]
    print(f"attenuation {key}: {res[key]['attenuation_vs_field']:+.2f} of the field slope")
json.dump(dict(rarefaction_field=min(nf, nr), rarefaction_obis=nr, window_deg=1.0, results=res,
               sites=[{k: v for k, v in o.items() if not isinstance(v, list)} for o in out]),
          open(sys.argv[3] if len(sys.argv) > 3 else "attenuation.json", "w"), indent=1)
