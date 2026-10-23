# /// script
# requires-python = ">=3.12"
# dependencies = ["pandas==2.2.3", "numpy==2.1.3", "requests==2.32.3"]
# ///
"""C1 cheapest check (ideas/2026-10-23-alroy-provocation-claude.md): how fast are fossil genus names invalidated after
description, by clade, in the PBDB's recorded opinions? Public PBDB API (CC BY), no account or contact parameters.
n_occs is NOT used: for a synonym the API reports the senior taxon's occurrence count. Event = currently invalid (synonym, replaced, nomen dubium/nudum/vanum/oblitum, invalid subgroup), dated by the first
invalidating opinion; rank changes are not invalidation; valid names are censored at 2026.
    uv run --python 3.12 data/c1-name-survival-check/check.py"""
import io
import json
import pathlib
import re

import numpy as np
import pandas as pd
import requests

HERE = pathlib.Path(__file__).resolve().parent
API = "https://paleobiodb.org/data1.2"
CLADES = ("Bivalvia", "Brachiopoda", "Trilobita", "Mammalia", "Dinosauria^Aves")   # non-avian dinosaurs
INVALID = {"subjective synonym of", "objective synonym of", "replaced by", "nomen dubium", "nomen nudum", "nomen vanum",
           "nomen oblitum", "invalid subgroup of"}
NOW = 2026


def get(path, **params):
    r = requests.get(f"{API}/{path}", params=params, timeout=600)
    r.raise_for_status()
    return pd.read_csv(io.StringIO(r.text), dtype=str, keep_default_na=False)


def km(times, events, at):
    """Kaplan-Meier survival of validity at the given ages (years since description)."""
    order = np.argsort(times)
    t, e = np.asarray(times)[order], np.asarray(events)[order]
    s, out, i, n = 1.0, {}, 0, len(t)
    for a in sorted(at):
        while i < n and t[i] <= a:
            j = i
            d = 0
            while j < n and t[j] == t[i]:
                d += e[j]; j += 1
            s *= 1 - d / (n - i)
            i = j
        out[a] = s
    return out


rows, summary = [], {}
for cl in CLADES:
    tx = get("taxa/list.txt", base_name=cl, rank="genus", variant="all", show="attr,app")
    tx = tx[tx["orig_no"] == tx["taxon_no"]].copy()
    tx["year"] = tx["taxon_attr"].map(lambda a: int(m.group(0)) if (m := re.search(r"1[6-9]\d\d|20[0-2]\d", a)) else np.nan)
    op = get("taxa/opinions.txt", base_name=cl, rank="genus", op_type="all")
    op["pubyr"] = pd.to_numeric(op["pubyr"], errors="coerce")
    first_inv = op[op["status"].isin(INVALID)].groupby("orig_no")["pubyr"].min()
    tx["invalid_now"] = tx["difference"].isin(INVALID)
    tx["first_invalid_year"] = tx["orig_no"].map(first_inv)
    tx = tx[tx["year"].notna()]
    tx["t"] = np.where(tx["invalid_now"], tx["first_invalid_year"] - tx["year"], NOW - tx["year"])
    tx = tx[tx["t"].notna() & (tx["t"] >= 0)]
    tx["n_occs"] = pd.to_numeric(tx["n_occs"], errors="coerce").fillna(0)
    tx["era"] = pd.cut(tx["year"], [1600, 1899, 1949, 1989, NOW], labels=["<1900", "1900-49", "1950-89", "1990+"])
    s = km(tx["t"].values, tx["invalid_now"].astype(int).values, (10, 25, 50, 100))
    inv = tx[tx["invalid_now"]]
    era = {f"invalid_share_described_{k}": float(g["invalid_now"].mean()) for k, g in tx.groupby("era", observed=True)}
    summary[cl] = dict(genus_names=int(len(tx)), invalid_now=int(tx["invalid_now"].sum()),
                       invalid_share=float(tx["invalid_now"].mean()),
                       median_years_to_invalidation_among_invalid=float(inv["t"].median()) if len(inv) else None,
                       km_validity={f"{a}y": round(v, 3) for a, v in s.items()}, opinions=int(len(op)), **era)
    tx["clade"] = cl
    rows.append(tx[["clade", "orig_no", "taxon_name", "year", "difference", "invalid_now", "first_invalid_year", "t"]])
    print(cl, json.dumps(summary[cl]), flush=True)
pd.concat(rows).to_csv(HERE / "name_survival.tsv", sep="\t", index=False)
(HERE / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
