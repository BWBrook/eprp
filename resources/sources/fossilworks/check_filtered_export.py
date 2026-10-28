#!/usr/bin/env python3
"""Compare two small Fossilworks exports; print a JSON receipt to stdout."""

import csv
import datetime
import io
import json
import urllib.parse
import urllib.request

BASE = "https://fossilworks.org/"
QUERY = {
    "a": "downloadResults",
    "pot": "",
    "country": "Australia",
    "Late Pleistocene": "yes",
    "southern_limit": "-37.5",
    "northern_limit": "-37",
    "western_limit": "144.5",
    "eastern_limit": "145",
}


def fetch(query):
    request = urllib.request.Request(BASE, urllib.parse.urlencode(query).encode())
    with urllib.request.urlopen(request, timeout=90) as response:
        result = response.read().decode("utf-8", errors="replace")
    tables = {}
    for name in ("register", "samples"):
        path = f"/eco/downloads/{name}.txt"
        if path not in result:
            raise RuntimeError(f"result does not link {path}")
        with urllib.request.urlopen(BASE.rstrip("/") + path, timeout=90) as response:
            text = response.read().decode("utf-8-sig")
        tables[name] = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
    register_samples = {r["sample no"] for r in tables["register"]}
    sample_ids = {r["sample no"] for r in tables["samples"]}
    if register_samples != sample_ids:
        raise RuntimeError("register and sample exports do not have the same sample IDs; files may have changed between requests")
    return tables


def summarise(tables):
    return {
        "register_rows": len(tables["register"]),
        "samples": {
            row["sample no"]: {
                "total_count": row["total count"],
                "richness": row["richness"],
                "gw_richness": row["GW richness"],
            }
            for row in tables["samples"]
        },
    }


filtered = dict(QUERY, genus="Diprotodon")
first = fetch(filtered)
second = fetch(QUERY)
if set(summarise(first)["samples"]) != set(summarise(second)["samples"]):
    raise RuntimeError("the two queries returned different sample sets")
print(json.dumps({
    "retrieved_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "filtered_request": filtered,
    "unfiltered_request": QUERY,
    "filtered": summarise(first),
    "unfiltered": summarise(second),
    "limitation": "Mutable unversioned export URLs; cross-user overwrite is not ruled out.",
}, indent=2, ensure_ascii=False))
