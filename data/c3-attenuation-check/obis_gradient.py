import json, sys, math, collections
import numpy as np
d = json.load(open(sys.argv[1]))
rows = [r for r in d["rows"] if r.get("species") and r.get("decimalLatitude") is not None]
def hurlbert(counts, n):
    N = sum(counts)
    if N < n:
        return float("nan")
    lc = math.lgamma
    base = lc(N + 1) - lc(n + 1) - lc(N - n + 1)
    return sum(1 - math.exp(lc(N - c + 1) - lc(n + 1) - lc(N - c - n + 1) - base) if N - c >= n else 1.0 for c in counts)
def gradient(sub, n_rare):
    bands = collections.defaultdict(collections.Counter)
    for r in sub:
        b = math.floor(-r["decimalLatitude"])
        if 11 <= b <= 36:
            bands[b][r["species"]] += 1
    out = []
    for b in sorted(bands):
        c = list(bands[b].values())
        out.append((b + 0.5, sum(c), len(c), hurlbert(c, n_rare)))
    lat = np.array([o[0] for o in out]); rr = np.array([o[3] for o in out]); raw = np.array([o[2] for o in out])
    ok = np.isfinite(rr) & (rr > 0)
    slope = np.polyfit(lat[ok], np.log(rr[ok]), 1)[0] if ok.sum() >= 5 else float("nan")
    slope_raw = np.polyfit(lat, np.log(raw), 1)[0]
    return out, slope, slope_raw, int(ok.sum())
kinds = collections.Counter(r.get("basisOfRecord", "") for r in rows)
print("species-level records", len(rows), dict(kinds.most_common(6)))
obs = {"HumanObservation", "Observation", "MachineObservation"}
spec = {"PreservedSpecimen", "MaterialSample", "FossilSpecimen", "Occurrence", "MaterialCitation"}
for name, sub in (("all", rows), ("specimen-based", [r for r in rows if r.get("basisOfRecord") in spec]),
                  ("observation-based", [r for r in rows if r.get("basisOfRecord") in obs])):
    for n in (100, 300):
        out, s, sraw, k = gradient(sub, n)
        print(f"{name:18s} n_rare={n:3d} records={len(sub):6d} bands_used={k:2d} slope log(rarefied S) per degree S = {s:+.4f}  (x10 deg: {math.exp(10*s):.2f}x)  raw-S slope {sraw:+.4f}")
out, s, sraw, k = gradient(rows, 300)
print("band, records, raw S, rarefied S(300):")
for o in out:
    print(f"  {o[0]:5.1f}S {o[1]:6d} {o[2]:5d} {o[3]:7.1f}")
