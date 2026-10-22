# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.1.3", "pandas==2.2.3"]
# ///
"""Derives deposit_constants.json: the fixed affine feature transforms (all-deposit transitions, both classes) and the
per-stage first-record counts used as generator entries. Recovered verbatim from the 22 October 2026 session that
wrote the file; inputs and output hashes are in the probe README.
    uv run --python 3.12 data/q038-probe/deposit_constants.py"""
import pandas as pd, numpy as np, json
o = pd.read_csv("data/raw/monarrez2023/pbdb.cleaned.classes.csv", usecols=["class","genus_no","reference_no","max_ma","min_ma"])
o = o[o["class"].isin(["Rhynchonellata","Bivalvia"])]
bases = sorted(o["max_ma"].unique(), reverse=True); smap = {b:i+1 for i,b in enumerate(bases)}
o["s"] = o["max_ma"].map(smap)
st = pd.read_csv("data/q038-predictor-contract/stages.tsv", sep="\t").sort_values("s")
maxma = dict(zip(st.s, st.max_ma)); minma = dict(zip(st.s, st.min_ma))
cnt = o.groupby(["class","genus_no","s"])["reference_no"].nunique().reset_index(name="refs")
rows = []
for (cl, g), d in cnt.groupby(["class","genus_no"]):
    c = dict(zip(d.s, d.refs)); f = min(c); lad = max(c)
    for s in range(f, lad):            # transitions s -> s+1 within the observed range
        recs = [t for t in c if t < s] + ([f] if f not in [t for t in c if t < s] else [])
        recs = sorted(set(recs)); l = max(recs)
        rows.append(dict(cl=cl, log_refs=np.log(c[l]), rec=max(0.0, minma[l] - maxma[s]), age=maxma[f] - maxma[s],
                         comp=len(recs) / (l - f + 1)))
df = pd.DataFrame(rows)
out = {k: dict(mean=round(float(df[k].mean()), 3), sd=round(float(df[k].std()), 3)) for k in ("log_refs","rec","age","comp")}
first = cnt.groupby(["class","genus_no"])["s"].min().reset_index()
entries = {cl: [int(x) for x in np.bincount(first[first["class"]==cl]["s"], minlength=88)[1:88]] for cl in ("Rhynchonellata","Bivalvia")}
print(json.dumps(dict(transform=out, n_transitions=len(df)), indent=1)); print({k: sum(v) for k,v in entries.items()})
json.dump(dict(transform=out, n_transitions=len(df), first_record_counts=entries), open("data/q038-probe/deposit_constants.json","w"), indent=1)
