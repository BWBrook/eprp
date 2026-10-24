# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check landscape.tsv against CRAN, PyPI and GitHub, then render LANDSCAPE.md.

Usage:
  uv run resources/software/landscape.py           # query registries, write landscape_check.tsv, render
  uv run resources/software/landscape.py --render  # render from the existing landscape_check.tsv

GitHub queries go through the authenticated `gh` CLI. No contact details are sent.
"""

import csv
import datetime as dt
import json
import pathlib
import re
import subprocess
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).parent
LANDSCAPE = ROOT / "landscape.tsv"
CHECK = ROOT / "landscape_check.tsv"
OUT = ROOT / "LANDSCAPE.md"
UA = {"User-Agent": "eprp-software-landscape/1"}
CHECK_FIELDS = ["id", "registry", "key", "state", "version", "date", "licence", "archived", "note", "pushed", "stars", "checked_utc"]

DOMAINS = {
    "data-access": "Data access and preparation",
    "chronology": "Chronology and age models",
    "palaeogeography": "Palaeogeography",
    "palaeoclimate": "Palaeoclimate data and proxies",
    "diversity-rates": "Diversity, sampling and rates",
    "extinction-timing": "Extinction timing and range ends",
    "biostratigraphy": "Quantitative biostratigraphy",
    "phylogenetic": "Phylogenetic inference and diversification",
    "traits-morphology": "Traits, morphology and disparity",
    "biogeography": "Historical biogeography",
    "sim-ecoevo": "Eco-evolutionary and metacommunity simulation",
    "sim-foodweb": "Ecosystem and food-web models",
    "earth-system": "Earth-system and biogeochemical models",
    "fossil-record-forward": "Forward models of the fossil record",
    "meta": "Hubs, tutorials and infrastructure",
}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, ""


def read_tsv(path):
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def cran_index():
    _, text = get("https://cran.r-project.org/src/contrib/PACKAGES")
    index = {}
    for block in text.split("\n\n"):
        fields = dict(re.findall(r"^([\w/]+): (.*(?:\n\s+.*)*)", block, re.M))
        if "Package" in fields:
            index[fields["Package"]] = fields
    return index


def check_cran(name, index):
    if name in index:
        p = index[name]
        return {"state": "ok", "version": p.get("Version", ""), "date": p.get("Published", "")[:10],
                "licence": " ".join(p.get("License", "").split()), "archived": "no"}
    status, html = get(f"https://cran.r-project.org/web/packages/{name}/index.html")
    if "was removed from the CRAN repository" not in html:
        return {"state": f"not_found ({status})"}
    m = re.search(r"Archived on (\d{4}-\d{2}-\d{2})(.*?)</p>", html, re.S)
    return {"state": "ok", "archived": "yes", "date": m.group(1) if m else "",
            "note": " ".join(m.group(2).split()).strip(" .") if m else "removed; no archive date stated"}


def check_pypi(name):
    status, text = get(f"https://pypi.org/pypi/{name}/json")
    if status != 200:
        return {"state": f"not_found ({status})"}
    data = json.loads(text)
    info = data["info"]
    files = data.get("releases", {}).get(info["version"], [])
    date = min((f["upload_time"] for f in files), default="")[:10]
    classifiers = [c.split(" :: ")[-1] for c in info.get("classifiers", []) if c.startswith("License ::")]
    licence = info.get("license_expression") or "; ".join(classifiers) or (info.get("license") or "").strip()
    return {"state": "ok", "version": info["version"], "date": date,
            "licence": licence if len(licence) <= 40 else "see PyPI",
            "archived": "yanked" if all(f.get("yanked") for f in files) and files else "no",
            "note": (info.get("summary") or "")[:100]}


def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    return json.loads(r.stdout) if r.returncode == 0 else None


def check_github(repo):
    meta = gh(f"repos/{repo}")
    if meta is None:
        return {"state": "not_found"}
    rel = gh(f"repos/{repo}/releases/latest") or {}
    if meta.get("full_name", "").lower() != repo.lower():
        note = f"moved to {meta['full_name']}"
    else:
        note = ""
    return {"state": "ok", "version": rel.get("tag_name", ""), "date": (rel.get("published_at") or "")[:10],
            "licence": (meta.get("license") or {}).get("spdx_id", "") or "none",
            "archived": "yes" if meta.get("archived") else "no", "note": note,
            "pushed": (meta.get("pushed_at") or "")[:10], "stars": str(meta.get("stargazers_count", ""))}


def run_checks(rows):
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    index = cran_index()
    checkers = {"cran": lambda k: check_cran(k, index), "pypi": check_pypi, "github": check_github}
    jobs = [(row["id"], registry, row[registry]) for row in rows for registry in checkers if row[registry]]

    def one(job):
        rid, registry, key = job
        result = checkers[registry](key)
        print(rid, registry, result["state"], file=sys.stderr, flush=True)
        return {f: "" for f in CHECK_FIELDS} | result | {"id": rid, "registry": registry, "key": key, "checked_utc": now}

    with ThreadPoolExecutor(max_workers=8) as pool:
        out = list(pool.map(one, jobs))
    with CHECK.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, CHECK_FIELDS, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(out)


def cell(text):
    return str(text or "").replace("|", "\\|").strip()


def activity(checks):
    dates = [c[k] for c in checks for k in ("date", "pushed") if c.get(k) and c["state"] == "ok" and c.get("archived") != "yes"]
    return max(dates, default="")


def registry_facts(checks):
    parts = []
    for c in checks:
        if not c["state"].startswith("ok"):
            parts.append(f"{c['registry']}: not found")
        elif c["registry"] == "cran":
            parts.append(f"CRAN archived {c['date']}" if c["archived"] == "yes" else f"CRAN {c['version']} ({c['date']})")
        elif c["registry"] == "pypi":
            parts.append(f"PyPI {c['version']} ({c['date']})")
        else:
            bits = [("archived, " if c["archived"] == "yes" else "") + f"pushed {c['pushed']}"]
            if c["version"]:
                bits.append(f"release {c['version']} ({c['date']})")
            if c["note"]:
                bits.append(c["note"])
            parts.append("GitHub " + ", ".join(bits))
    return "; ".join(parts)


def licence(row, checks):
    found = sorted({c["licence"] for c in checks if c.get("licence")})
    if len(found) > 1:
        found = [f for f in found if f not in ("none", "NOASSERTION")] or found
    return "; ".join(found) if found else (f"{row['licence_scan']} (scan)" if row["licence_scan"] else "")


def render(rows, checks):
    by_id = {}
    for c in checks:
        by_id.setdefault(c["id"], []).append(c)
    checked = max((c["checked_utc"] for c in checks), default="not run")
    lines = [
        "# Software landscape",
        "",
        "Every tool found by the four landscape scans of 23 October 2026 (Claude",
        "Sonnet subagents; tier T0 in [the conventions](README.md)). Generated by",
        "`landscape.py` from `landscape.tsv` (the scans' facts, with their labels) and",
        f"`landscape_check.tsv` (registry metadata queried {checked}). Registry columns",
        "are `checked`; everything else is the scans' report, labelled `verified`",
        "where a scan read a primary page and `recall` otherwise. Question tags are",
        "the scans' inference. A row here is not a recommendation.",
        "",
        f"{len(rows)} tools. Refresh with `uv run resources/software/landscape.py`.",
        "",
    ]
    for domain, title in DOMAINS.items():
        group = sorted((r for r in rows if r["domain"] == domain), key=lambda r: r["name"].lower())
        if not group:
            continue
        lines += [f"## {title}", "", "| Tool | Kind | What it does | Registry (checked) | Last activity | Licence | Blockers | Questions |",
                  "| --- | --- | --- | --- | --- | --- | --- | --- |"]
        for r in group:
            candidates = [r["home"].split()[0] if r["home"] else "", f"https://github.com/{r['github']}" if r["github"] else "", r["other_repo"].split()[0] if r["other_repo"] else ""]
            url = next((u for u in candidates if u.startswith("http")), "")
            name = f"[{cell(r['name'])}]({url})" if url else cell(r["name"])
            c = by_id.get(r["id"], [])
            lines.append(f"| {name} | {cell(r['kind'])}; {cell(r['languages'])} | {cell(r['summary'])} | {cell(registry_facts(c))} | "
                         f"{activity(c)} | {cell(licence(r, c))} | {cell(r['blockers'])} | {cell(r['eprp_questions'])} |")
        lines.append("")
    OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    rows = read_tsv(LANDSCAPE)
    if "--render" not in sys.argv:
        run_checks(rows)
    render(rows, read_tsv(CHECK) if CHECK.exists() else [])


if __name__ == "__main__":
    main()
