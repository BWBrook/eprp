#!/usr/bin/env python3
"""EPRP literature library: harvest the works the repository cites, resolve every
seed to an OpenAlex record, grow outward through reference lists, and mirror
open-access full texts.

Usage:
  python3 library.py harvest REPO_ROOT
  python3 library.py resolve [--store DIR] [--recheck]
  python3 library.py expand [--store DIR] [--min-refs K] [--out DIR]
  python3 library.py fetch [--store DIR] [--tier TIER ...] [--workers N] [--retry-failed] [--limit N]
  python3 library.py withdraw W [W ...] --reason TEXT [--store DIR]
  python3 library.py index [--store DIR] [--out DIR]

harvest scans git-tracked text files for DOIs (as written, including SICI forms),
PMC ids (converted to DOIs by NCBI's id converter), PubMed ids and arXiv ids, and
writes seeds/cited-ids.tsv with the files and questions (Q-NNN, B-NNN,
src:<catalogue id>) citing each. Every seeds/*.tsv is a tier named after its
file; a seed row gives an openalex_id, doi or pmid. resolve fetches full OpenAlex
records for all seeds into STORE/openalex/<W>.json (batched, 1 credit per 50
works), keeps seed-key aliases in STORE/aliases.tsv, and records keys it cannot
resolve in STORE/unresolved-keys.tsv. expand writes the neighbours tier from the
stored reference lists. fetch downloads PDFs from open copies only (OpenAlex
open-access locations, the PubMed Central open-access bucket, repository landing
pages, CORE's repository copies when ~/.config/core/api_key exists, Semantic
Scholar's open-access link), accepts one only when its first pages
contain the work's title, stores it read-only as STORE/pdf/<W>.pdf with text in
STORE/text/<W>.txt, and appends to STORE/manifest.tsv; every attempt goes to
STORE/attempts.tsv. withdraw removes held copies with a recorded reason. index
writes works.tsv, unresolved.tsv, INDEX.md and by-question.md to --out.

Needs Python 3.9+ and poppler's pdftotext and pdfinfo. The store lives on
deep-server. No email or personal identifier is sent to any service. An OpenAlex
API key is used if OPENALEX_API_KEY or ~/.config/openalex/api_key is set; without
one, OpenAlex allows each IP address about 1,000 credits a day.
"""

import argparse
import concurrent.futures
import csv
import datetime
import fcntl
import hashlib
import html
import http.client
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEEDS = HERE / "seeds"
DEFAULT_STORE = Path("/data/paleodata/library")
UA = "EPRP-library/0.2 (private research mirror; python-urllib)"
csv.field_size_limit(sys.maxsize)

TEXT_EXT = {".md", ".qmd", ".txt", ".bib", ".yaml", ".yml", ".py", ".R", ".r", ".sh"}
HEADING_EXT = {".md", ".qmd"}
DOI_RE = re.compile(r"10\.\d{4,9}/[^\s\"'<>`\[\]{}|,;“”‘’—–…]+")
SICI_RE = re.compile(r"10\.\d{4,9}/\d{4}-\d{3}[\dX]\(\d{4}\)\d+(?:<[^>\s]+>|\[[^\]\s]+\])[\d.]+\.CO;\d", re.I)
SICI_PARTS_RE = re.compile(r"(10\.\d+/\d{4}-\d{3}[\dx]\(\d{4}\))(\d+)[<\[](\d+):([^>\]]*)[>\]](.*)$")
URL_TAIL_RE = re.compile(r"(/(full|abstract|pdf|epdf|summary|meta|fulltext(\.html?)?|suppl_file/.*|mediaobjects/.*)"
                         r"|\.full(\.pdf)?|\.pdf|&\w+=.*)$", re.I)
QTOKEN_RE = re.compile(r"(?<![A-Za-z0-9])([QqBb])-?(\d{3})(?![0-9])")
HEADING_RE = re.compile(r"^#{1,6}\s")
PMCID_RE = re.compile(r"\bPMC(\d{4,9})\b")
PMID_RE = re.compile(r"(?:pubmed\.ncbi\.nlm\.nih\.gov/|\bPMID:?\s*)(\d{6,9})\b", re.I)
ARXIV_RE = re.compile(r"(?:arxiv\.org/(?:abs|pdf)/|\barXiv:\s*)(\d{4}\.\d{4,5})", re.I)
SKIP_TYPES = {"dataset", "software", "paratext", "erratum", "retraction", "editorial", "letter", "peer-review",
              "grant", "standard", "supplementary-materials"}
DEAD_KEY_STATUS = {"datacite", "invalid", "deleted", "not_found"}
VERSION_RANK = {"publishedVersion": 0, "acceptedVersion": 1, "submittedVersion": 2, None: 3}
TIER_RANK = {"canon": 1, "neighbours": 2}
STOPWORDS = {"the", "and", "for", "with", "from", "into", "its", "are", "was", "were", "not", "but", "has", "how",
             "why", "new", "can", "our", "out", "all", "any", "via", "who", "what", "when", "der", "die", "das",
             "und", "les", "des", "une", "von"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_tsv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with open(tmp, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    os.replace(tmp, path)


def append_tsv(path, row, fields, lock):
    with lock:
        new = not path.exists()
        with open(path, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
            if new:
                w.writeheader()
            w.writerow(row)


def store_lock(store):
    """Hold an exclusive lock on the store for the life of the process; refuse a second writer."""
    store.mkdir(parents=True, exist_ok=True)
    f = open(store / ".lock", "w")
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        sys.exit(f"{store} is locked by another library.py run")
    return f


def clean_doi(raw):
    s = urllib.parse.unquote(raw).split("?", 1)[0].split("#", 1)[0]
    while True:
        t = URL_TAIL_RE.sub("", s.rstrip(".:*_~'/"))
        if t.endswith(")") and t.count("(") < t.count(")"):
            t = t[:-1]
        if t == s:
            return s.lower()
        s = t


def sici_variants(doi):
    """Registered SICI DOIs differ in bracket style and zero padding, and text often alters both;
    return the other three or four spellings to try when the written one does not resolve."""
    m = SICI_PARTS_RE.match(doi)
    if not m:
        return []
    head, vol, page, code, tail = m.groups()
    out = [f"{head}{v}{o}{p}:{code}{c}{tail}" for v, p in ((vol, page), (f"{int(vol):03d}", f"{int(page):04d}"))
           for o, c in (("<", ">"), ("[", "]"))]
    return [x for x in dict.fromkeys(out) if x != doi]


def norm_doi(doi):
    doi = (doi or "").strip().lower()
    for p in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(p):
            doi = doi[len(p):]
    return doi


def short_wid(wid):
    return (wid or "").strip().rsplit("/", 1)[-1].upper()


def questions_from_path(path):
    out = {f"{m.group(1).upper()}-{m.group(2)}" for m in QTOKEN_RE.finditer(path)}
    parts = Path(path).parts
    if len(parts) > 3 and parts[:2] == ("resources", "sources"):
        out.add(f"src:{parts[2]}")
    return out


# ---------------------------------------------------------------- harvest

def harvest(repo):
    repo = Path(repo).resolve()
    files = subprocess.run(["git", "-C", str(repo), "ls-files", "-z"], capture_output=True, text=True,
                           check=True).stdout.split("\0")
    own = str(HERE.relative_to(repo)) + "/" if HERE.is_relative_to(repo) else None
    mentions = defaultdict(list)
    questions = defaultdict(set)
    for rel in files:
        if not rel or Path(rel).suffix not in TEXT_EXT or (own and rel.startswith(own)):
            continue
        try:
            lines = (repo / rel).read_text(encoding="utf-8").splitlines()
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        base_q = questions_from_path(rel)
        section_q = set()
        headings = Path(rel).suffix in HEADING_EXT
        for i, line in enumerate(lines, 1):
            if headings and HEADING_RE.match(line):
                section_q = {f"{m.group(1).upper()}-{m.group(2)}" for m in QTOKEN_RE.finditer(line)}
            line = html.unescape(urllib.parse.unquote(line))
            sici = [m.group(0).lower() for m in SICI_RE.finditer(line)]
            keys = [f"doi:{d}" for d in sici + [clean_doi(m.group(0)) for m in DOI_RE.finditer(SICI_RE.sub(" ", line))]
                    if "/" in d and "$" not in d]
            keys += [f"pmc:PMC{m.group(1)}" for m in PMCID_RE.finditer(line)]
            keys += [f"pmid:{m.group(1)}" for m in PMID_RE.finditer(line)]
            keys += [f"doi:10.48550/arxiv.{m.group(1)}" for m in ARXIV_RE.finditer(line)]
            for key in keys:
                mentions[key].append(f"{rel}:{i}")
                questions[key] |= base_q | section_q
    pmc = pmc_to_doi(sorted(k[4:] for k in mentions if k.startswith("pmc:")))
    for k in [k for k in mentions if k.startswith("pmc:")]:
        locs, qs = mentions.pop(k), questions.pop(k)
        if k[4:] in pmc:
            mentions[pmc[k[4:]]] += locs
            questions[pmc[k[4:]]] |= qs
        else:
            print(f"{k[4:]}: PMC records no DOI or PubMed id; dropped", file=sys.stderr)
    rows = []
    for key in sorted(mentions):
        firsts = {}
        for loc in mentions[key]:
            firsts.setdefault(loc.rsplit(":", 1)[0], loc)
        kind, value = key.split(":", 1)
        rows.append({"doi": value if kind == "doi" else "", "pmid": value if kind == "pmid" else "",
                     "mentions": len(mentions[key]), "files": ";".join(firsts.values()),
                     "questions": ";".join(sorted(questions[key]))})
    write_tsv(SEEDS / "cited-ids.tsv", rows, ["doi", "pmid", "mentions", "files", "questions"])
    print(f"{len(rows)} identifiers ({sum(1 for r in rows if r['pmid'])} PubMed-only) from "
          f"{sum(len(v) for v in mentions.values())} mentions -> seeds/cited-ids.tsv")


def pmc_to_doi(pmcids):
    """Map PMC ids to doi:... (or pmid:... when PMC records no DOI) with NCBI's id converter."""
    out = {}
    for i in range(0, len(pmcids), 100):
        url = ("https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?format=json&tool=eprp-library&ids="
               + ",".join(pmcids[i:i + 100]))
        data, _ = get_json(url)
        for rec in data.get("records", []):
            if rec.get("doi"):
                out[rec["requested-id"]] = f"doi:{rec['doi'].lower()}"
            elif rec.get("pmid"):
                out[rec["requested-id"]] = f"pmid:{rec['pmid']}"
    return out


# ---------------------------------------------------------------- http

class Truncated(Exception):
    pass


def api_key():
    key = os.environ.get("OPENALEX_API_KEY")
    p = Path.home() / ".config/openalex/api_key"
    if not key and p.exists():
        key = p.read_text().strip()
    return key


def safe_url(url):
    return urllib.parse.quote(url, safe=":/?&=%#+,;@~!$'()*[]")


def key_file(name):
    """A credential from ~/.config/<name>, or '' if absent."""
    p = Path.home() / ".config" / name
    return p.read_text().strip() if p.exists() else ""


def http_get(url, accept="application/json", timeout=60, max_bytes=None, headers=None):
    req = urllib.request.Request(safe_url(url), headers={"User-Agent": UA, "Accept": accept, **(headers or {})})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        data = r.read(max_bytes + 1) if max_bytes else r.read()
        if max_bytes and len(data) > max_bytes:
            raise Truncated(f"larger than {max_bytes} bytes")
        declared = r.headers.get("Content-Length")
        if declared and declared.isdigit() and not r.headers.get("Content-Encoding") and len(data) < int(declared):
            raise Truncated(f"{len(data)} of {declared} bytes")
        return r.status, r.geturl(), r.headers, data


TRANSIENT_ERRORS = (urllib.error.URLError, TimeoutError, ConnectionError, http.client.HTTPException,
                    json.JSONDecodeError, Truncated)


def retry_after(headers, default):
    value = (headers or {}).get("Retry-After") or ""
    return min(float(value), 60.0) if value.replace(".", "", 1).isdigit() else default


def get_json(url, tries=5, headers=None):
    for attempt in range(tries):
        try:
            _, _, response_headers, data = http_get(url, headers=headers)
            return json.loads(data), response_headers
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries - 1:
                time.sleep(retry_after(e.headers, 2 ** attempt * 5))
                continue
            raise
        except TRANSIENT_ERRORS:
            if attempt < tries - 1:
                time.sleep(2 ** attempt * 5)
                continue
            raise


def openalex_url(path, params=None):
    params = dict(params or {})
    key = api_key()
    if key:
        params["api_key"] = key
    return f"https://api.openalex.org/{path}" + ("?" + urllib.parse.urlencode(params, safe=":/|") if params else "")


def openalex_list(filter_expr):
    data, headers = get_json(openalex_url("works", {"filter": filter_expr, "per-page": "100"}))
    return data["results"], headers.get("x-ratelimit-remaining")


def openalex_one(path):
    """A single work by id or doi:..., following merges; None if OpenAlex has no such work."""
    try:
        return get_json(openalex_url(f"works/{path}"), tries=3)[0]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


# ---------------------------------------------------------------- seeds and store

def load_seeds():
    """Return {tier: [row, ...]} from seeds/*.tsv. Each row gives an openalex_id, doi or pmid; its key
    is the first of these present (W..., doi:..., pmid:...)."""
    tiers = {}
    for path in sorted(SEEDS.glob("*.tsv")):
        rows = read_tsv(path)
        for r in rows:
            r["doi"] = norm_doi(r.get("doi"))
            r["openalex_id"] = short_wid(r.get("openalex_id"))
            r["pmid"] = (r.get("pmid") or "").strip()
            r["key"] = r["openalex_id"] or (f"doi:{r['doi']}" if r["doi"] else (f"pmid:{r['pmid']}" if r["pmid"] else ""))
        tiers[path.stem] = rows
    return tiers


def seed_wid(r, aliases):
    return aliases.get(r["key"], r["openalex_id"])


def load_records(store):
    recs = {}
    for p in (store / "openalex").glob("W*.json"):
        try:
            recs[p.stem] = json.loads(p.read_text())
        except json.JSONDecodeError:
            print(f"{p}: unreadable record, ignored (resolve refetches it)", file=sys.stderr)
    return recs


def load_aliases(store):
    p = store / "aliases.tsv"
    return {r["key"]: r["openalex_id"] for r in read_tsv(p)} if p.exists() else {}


def save_aliases(store, aliases):
    write_tsv(store / "aliases.tsv", [{"key": k, "openalex_id": v} for k, v in sorted(aliases.items())],
              ["key", "openalex_id"])


def load_attempts(store):
    p = store / "attempts.tsv"
    return read_tsv(p) if p.exists() else []


def load_manifest(store):
    """Latest manifest row per work (later rows, e.g. withdrawals, supersede earlier ones)."""
    p = store / "manifest.tsv"
    return {r["openalex_id"]: r for r in read_tsv(p)} if p.exists() else {}


# ---------------------------------------------------------------- resolve

def registry_of(doi):
    for name, url in (("crossref", f"https://api.crossref.org/works/{urllib.parse.quote(doi, safe='/')}"),
                      ("datacite", f"https://api.datacite.org/dois/{urllib.parse.quote(doi, safe='/')}")):
        try:
            http_get(url, timeout=30)
            return name
        except urllib.error.HTTPError as e:
            if e.code != 404:
                return "unchecked"
        except TRANSIENT_ERRORS:
            return "unchecked"
    return "invalid"


def resolve(store, recheck=False):
    lock = store_lock(store)
    (store / "openalex").mkdir(parents=True, exist_ok=True)
    records = load_records(store)
    have = set(records)
    aliases = load_aliases(store)
    dead_path = store / "unresolved-keys.tsv"
    dead = {r["key"]: r for r in read_tsv(dead_path)} if dead_path.exists() else {}
    skip = set() if recheck else {k for k, r in dead.items() if r["status"] in DEAD_KEY_STATUS}
    want_doi, want_wid, want_pmid = set(), set(), set()
    for rows in load_seeds().values():
        for r in rows:
            if not r["key"] or r["key"] in skip:
                continue
            if r["openalex_id"]:
                if seed_wid(r, aliases) not in have:
                    want_wid.add(r["openalex_id"])
            elif r["key"] not in aliases:
                (want_doi if r["doi"] else want_pmid).add(r["doi"] or r["pmid"])
    print(f"to resolve: {len(want_doi)} DOIs, {len(want_pmid)} PubMed ids, {len(want_wid)} OpenAlex ids; "
          f"{len(skip)} known-dead keys skipped")
    remaining, failed = None, {}

    def save(rec):
        wid = short_wid(rec["id"])
        path = store / "openalex" / f"{wid}.json"
        tmp = path.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(rec, ensure_ascii=False))
        os.replace(tmp, path)
        have.add(wid)
        return wid

    try:
        dois = sorted(want_doi)
        found = defaultdict(list)
        for i in range(0, len(dois), 50):
            batch = dois[i:i + 50]
            try:
                results, remaining = openalex_list("doi:" + "|".join(batch))
            except urllib.error.HTTPError as e:
                print(f"DOI batch {i}: HTTP {e.code}; resolving singly below", file=sys.stderr)
                results = []
            for rec in results:
                found[norm_doi(rec.get("doi"))].append((rec.get("cited_by_count") or 0, save(rec)))
            print(f"  DOIs {i + len(batch)}/{len(dois)} (credits left {remaining})")
        for d in dois:
            if found.get(d):
                aliases[f"doi:{d}"] = max(found[d])[1]
                continue
            # Batch filters miss alias DOIs (JSTOR 10.2307/...) and SICI spellings; single lookups follow them.
            for spelling in [d] + sici_variants(d):
                rec = openalex_one(f"doi:{urllib.parse.quote(spelling, safe='/')}")
                if rec:
                    aliases[f"doi:{d}"] = save(rec)
                    break
        save_aliases(store, aliases)

        pmids = sorted(want_pmid)
        for i in range(0, len(pmids), 50):
            try:
                results, remaining = openalex_list("pmid:" + "|".join(pmids[i:i + 50]))
            except urllib.error.HTTPError as e:
                print(f"PubMed batch {i}: HTTP {e.code}", file=sys.stderr)
                failed.update({f"pmid:{p}": "error" for p in pmids[i:i + 50]})
                continue
            for rec in results:
                pm = ((rec.get("ids") or {}).get("pmid") or "").rsplit("/", 1)[-1]
                aliases[f"pmid:{pm}"] = save(rec)
        save_aliases(store, aliases)

        wids = sorted(want_wid)
        for i in range(0, len(wids), 50):
            batch = wids[i:i + 50]
            try:
                results, remaining = openalex_list("openalex:" + "|".join(batch))
            except urllib.error.HTTPError as e:
                print(f"id batch {i}: HTTP {e.code}; resolving singly", file=sys.stderr)
                results = []
            got = {save(rec) for rec in results}
            for w in batch:
                if w not in got:  # merged ids redirect to the surviving work; deleted ones 404
                    rec = openalex_one(w)
                    if rec:
                        aliases[w] = save(rec)
            print(f"  ids {i + len(batch)}/{len(wids)} (credits left {remaining})")
        save_aliases(store, aliases)
    finally:
        save_aliases(store, aliases)

    stamp = now()
    for d in dois:
        if f"doi:{d}" not in aliases:
            dead[f"doi:{d}"] = {"key": f"doi:{d}", "status": registry_of(d), "checked": stamp}
    for p in want_pmid:
        if f"pmid:{p}" not in aliases:
            dead[f"pmid:{p}"] = {"key": f"pmid:{p}", "status": failed.get(f"pmid:{p}", "not_found"), "checked": stamp}
    for w in want_wid:
        if w not in have and w not in aliases:
            dead[w] = {"key": w, "status": "deleted", "checked": stamp}
    for k in [k for k in dead if k in aliases or k in have]:
        del dead[k]
    write_tsv(dead_path, [dead[k] for k in sorted(dead)], ["key", "status", "checked"])
    print(f"unresolved keys by status: {dict(Counter(r['status'] for r in dead.values()))}")
    lock.close()


# ---------------------------------------------------------------- expand

def expand(store, k, out):
    """Write the neighbours tier: works outside the other tiers that at least k seed works reference.
    Each inherits the questions of the seed works that reference it."""
    recs = load_records(store)
    aliases = load_aliases(store)
    seed_q = defaultdict(set)
    for tier, rows in load_seeds().items():
        if tier == "neighbours":
            continue
        for r in rows:
            wid = seed_wid(r, aliases)
            if wid in recs:
                seed_q[wid] |= {q for q in (r.get("questions") or "").split(";") if q}
    count, qs = Counter(), defaultdict(set)
    for wid, q in seed_q.items():
        for ref in {short_wid(x) for x in recs[wid].get("referenced_works") or []}:
            count[ref] += 1
            qs[ref] |= q
    rows = [{"openalex_id": w, "ref_count": n, "questions": ";".join(sorted(qs[w]))}
            for w, n in count.most_common() if n >= k and w not in seed_q]
    write_tsv(out / "neighbours.tsv", rows, ["openalex_id", "ref_count", "questions"])
    print(f"{len(seed_q)} seed works reference {len(count)} works; {len(rows)} outside the seeds with >= {k} "
          f"-> {out / 'neighbours.tsv'}")


# ---------------------------------------------------------------- fetch

# CORE allows registered academic users 10 requests a minute; Wiley's TDM API 60 per 10 minutes.
HOST_INTERVAL = {"api.core.ac.uk": 6.5, "api.wiley.com": 10.0}


class HostPacer:
    """Per-host spacing between requests, and per-host pauses after a rate-limit refusal."""

    def __init__(self, interval):
        self.interval = interval
        self.lock = threading.Lock()
        self.next_ok = defaultdict(float)
        self.paused_until = {}

    def wait(self, url):
        host = urllib.parse.urlsplit(url).hostname or ""
        with self.lock:
            t = max(time.monotonic(), self.next_ok[host])
            self.next_ok[host] = t + HOST_INTERVAL.get(host, self.interval)
        time.sleep(max(0.0, t - time.monotonic()))

    def pause(self, host, seconds):
        with self.lock:
            self.paused_until[host] = time.monotonic() + seconds
        print(f"  {host} refused with HTTP 429; skipping it for {seconds / 60:.0f} min", flush=True)

    def paused(self, host):
        return time.monotonic() < self.paused_until.get(host, 0.0)


def pause_seconds(headers, default=3600.0):
    """Seconds until a rate-limited host accepts requests again (Retry-After or CORE's reset timestamp)."""
    headers = headers or {}
    value = headers.get("Retry-After") or ""
    if value.replace(".", "", 1).isdigit():
        return float(value)
    try:
        reset = datetime.datetime.fromisoformat(headers.get("x-ratelimit-retry-after") or "")
        return max(60.0, (reset - datetime.datetime.now(datetime.timezone.utc)).total_seconds())
    except ValueError:
        return default


PMC_RE = re.compile(r"/pmc/articles/(?:PMC)?(\d+)", re.I)
META_PDF_RE = [re.compile(r"""<meta[^>]+name=["']citation_pdf_url["'][^>]*content=["']([^"']+)""", re.I),
               re.compile(r"""<meta[^>]+content=["']([^"']+)["'][^>]*name=["']citation_pdf_url["']""", re.I)]
PMC_BUCKET = "https://pmc-oa-opendata.s3.amazonaws.com/"
HREF_RE = re.compile(r"""<a\s[^>]*href=["']([^"'#]+)["']""", re.I)
FILE_LINK_RE = re.compile(r"(\.pdf($|\?)|/bitstream/|/files/\d+/|viewcontent\.cgi|/download/|/document$)", re.I)
S2_API = "https://api.semanticscholar.org/graph/v1/paper/DOI:"


class FetchFail(Exception):
    def __init__(self, outcome, detail=""):
        super().__init__(outcome)
        self.outcome, self.detail = outcome, detail


def transient(outcome):
    return outcome.endswith("error") or outcome in ("http_408", "http_429") or outcome.startswith("http_5")


def is_lookup(outcome):
    return outcome.startswith(("s2_", "core_"))


def candidates(rec):
    """Ordered (kind, url, host, version, licence) tuples from open-access locations only: published
    versions first, direct PDFs before landing pages. kind is pdf, landing (follow its citation_pdf_url
    or a same-host file link) or pmc (the PMC open-access bucket)."""
    out, pmc = [], {}
    pmcid = (rec.get("ids") or {}).get("pmcid")
    if pmcid:
        pmc[re.sub(r"\D", "", pmcid.rsplit("/", 1)[-1])] = ("publishedVersion", "")
    for loc in rec.get("locations") or []:
        src = loc.get("source") or {}
        host, version, lic = src.get("display_name") or "", loc.get("version"), loc.get("license") or ""
        landing, pdf = loc.get("landing_page_url") or "", loc.get("pdf_url") or ""
        m = PMC_RE.search(landing) or PMC_RE.search(pdf)
        if m:
            pmc[m.group(1)] = (version or "publishedVersion", lic)
            continue
        if not loc.get("is_oa") or ("pubmed.ncbi.nlm.nih.gov" in landing and not pdf):
            continue
        rank = (VERSION_RANK.get(version, 3), 0 if src.get("type") == "repository" else 1)
        if pdf:
            out.append((rank[0], 0, rank[1], "pdf", pdf, host, version or "", lic))
        elif landing and "doi.org/" not in landing:
            kind = "pdf" if landing.lower().endswith(".pdf") else "landing"
            out.append((rank[0], 1, rank[1], kind, landing, host, version or "", lic))
    for n, (version, lic) in pmc.items():
        out.append((0, 0, 0, "pmc", f"PMC{n}", "PubMed Central OA", version, lic))
    seen, ordered = set(), []
    for c in sorted(out):
        if c[4] not in seen:
            seen.add(c[4])
            ordered.append(c[3:])
    return ordered


def get_bytes(url, pacer, accept="application/pdf,*/*;q=0.5", headers=None):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https"):
        raise FetchFail("bad_scheme", url[:60])
    pacer.wait(url)
    try:
        _, final, response_headers, data = http_get(url, accept=accept, timeout=120, max_bytes=300_000_000,
                                                    headers=headers)
    except urllib.error.HTTPError as e:
        if e.code == 429:
            pacer.pause(parts.hostname, pause_seconds(e.headers, 600.0))
        raise FetchFail(f"http_{e.code}")
    return final, response_headers, data


def download(kind, url, pacer, headers=None):
    """Return (final_url, pdf_bytes) or raise FetchFail. headers go only to the first request."""
    if kind == "pmc":
        listing = get_bytes(f"{PMC_BUCKET}?list-type=2&prefix={url}.", pacer, accept="application/xml")[2].decode()
        keys = sorted(re.findall(rf"<Key>({url}\.(\d+)/{url}\.\2\.pdf)</Key>", listing), key=lambda k: int(k[1]))
        if not keys:
            raise FetchFail("pmc_not_oa")
        url, kind = PMC_BUCKET + keys[-1][0], "pdf"
    final, headers, data = get_bytes(url, pacer, accept="application/pdf,text/html;q=0.9,*/*;q=0.5", headers=headers)
    if data.startswith(b"%PDF-"):
        return final, data
    if kind == "pdf":
        raise FetchFail("not_pdf", (headers.get("Content-Type") or "")[:60])
    page = data[:2_000_000].decode("utf-8", "replace")
    here = urllib.parse.urlsplit(final).hostname
    meta = [m.group(1) for rx in META_PDF_RE for m in rx.finditer(page)][:1]
    anchors = [urllib.parse.urljoin(final, html.unescape(h)) for h in HREF_RE.findall(page)]
    files = [u for u in dict.fromkeys(anchors) if urllib.parse.urlsplit(u).hostname == here and FILE_LINK_RE.search(u)]
    links = list(dict.fromkeys(meta + files[:2] + ([final.rstrip("/") + "/document"] if "hal.science/" in final else [])))
    for link in links:
        try:
            got, headers, data = get_bytes(urllib.parse.urljoin(final, html.unescape(link)), pacer)
        except FetchFail:
            continue
        if data.startswith(b"%PDF-"):
            return got, data
    raise FetchFail("no_pdf_link" if not links else "not_pdf", f"{len(links)} links tried")


def tokens(text):
    text = unicodedata.normalize("NFKC", text or "").casefold()
    return [t for t in re.findall(r"[^\W\d_]{3,}", text) if t not in STOPWORDS]


def compact(text):
    return re.sub(r"[\W_]+", "", unicodedata.normalize("NFKC", text or "").casefold())


def title_match(title, text):
    """Share of the title's content words found in the text; titles with fewer than two content words
    must appear whole (ignoring spacing and punctuation)."""
    title = re.sub(r"<[^>]+>", " ", title or "")
    body = re.sub(r"-\s*\n\s*", "", unicodedata.normalize("NFKC", text))
    want = set(tokens(title))
    if len(want) < 2:
        return 1.0 if compact(title) and compact(title) in compact(body) else 0.0
    return len(want & set(tokens(body))) / len(want)


def pdf_text(path, last_page=None):
    """Text of the PDF, or None if pdftotext fails (corrupt or encrypted file)."""
    cmd = ["pdftotext", "-q", "-enc", "UTF-8"] + (["-l", str(last_page)] if last_page else []) + [str(path), "-"]
    r = subprocess.run(cmd, capture_output=True, timeout=300)
    return r.stdout.decode("utf-8", "replace") if r.returncode == 0 else None


def pdf_pages(path):
    r = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, timeout=60)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return int(m.group(1)) if r.returncode == 0 and m else 0


MANIFEST_FIELDS = ["openalex_id", "doi", "status", "url", "host", "version", "license", "sha256", "bytes",
                   "pages", "text_chars", "title_match", "retrieved", "tool_sha256", "note", "path"]
ATTEMPT_FIELDS = ["openalex_id", "url", "host", "outcome", "detail", "when"]
OPEN_HELD = ("ok", "no_text")
TDM_HELD = ("tdm_ok", "tdm_no_text")
TDM_NOTE = "TDM copy: local search and mining only until UTAS confirms AI-service processing is licensed"

# Publisher text-and-data-mining routes, tried after every open route fails. Copies go to tdm/<name>/.
TDM_ROUTES = {
    "wiley": {"host": "Wiley TDM", "key": "wiley/tdm_token", "header": "Wiley-TDM-Client-Token",
              "url": "https://api.wiley.com/onlinelibrary/tdm/v1/articles/{}",
              "prefixes": ("10.1111/", "10.1002/", "10.1029/", "10.1046/", "10.1034/", "10.1890/")},
}


def text_path(pdf_path):
    return pdf_path.parent.parent / "text" / f"{pdf_path.stem}.txt"


def try_candidate(rec, cand, store, pacer, lock, tool_sha, area=".", headers=None, tdm=False):
    """Download, check and store one candidate under STORE/<area>/pdf and text; return (outcome, detail).
    A TDM copy is recorded with status tdm_<outcome> and its API request URL rather than the signed link."""
    kind, url, host, version, license_ = cand
    wid = short_wid(rec["id"])
    tmp = None
    try:
        final, data = download(kind, url, pacer, headers)
        fd, tmp = tempfile.mkstemp(suffix=".pdf", dir=store / "tmp")
        os.close(fd)
        with open(tmp, "wb") as f:
            f.write(data)
        pages = pdf_pages(tmp)
        first = pdf_text(tmp, last_page=3)
        if not pages or first is None:
            return "bad_pdf", "pdfinfo or pdftotext failed"
        score = title_match(rec.get("title"), first)
        if len(first.strip()) < 200:
            outcome = "no_text"
        elif score >= 0.6:
            outcome = "ok"
        else:
            shutil.move(tmp, store / "quarantine" / f"{wid}__{hashlib.sha256(url.encode()).hexdigest()[:8]}.pdf")
            tmp = None
            return "mismatch", f"title_match={score:.2f}"
        full = pdf_text(tmp) or ""
        rel = Path(area) / "pdf" / f"{wid}.pdf"
        dest = store / rel
        (store / text_path(rel)).parent.mkdir(parents=True, exist_ok=True)
        dest.parent.mkdir(parents=True, exist_ok=True)
        (store / text_path(rel)).write_text(full, encoding="utf-8")
        os.replace(tmp, dest)
        tmp = None
        dest.chmod(0o444)
        append_tsv(store / "manifest.tsv", {
            "openalex_id": wid, "doi": norm_doi(rec.get("doi")), "status": ("tdm_" if tdm else "") + outcome,
            "url": url if tdm else final, "host": host, "version": version, "license": license_,
            "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "pages": pages, "text_chars": len(full),
            "title_match": f"{score:.2f}", "retrieved": now(), "tool_sha256": tool_sha,
            "note": TDM_NOTE if tdm else "", "path": str(rel)}, MANIFEST_FIELDS, lock)
        return outcome, ""
    except FetchFail as e:
        return e.outcome, e.detail
    except Exception as e:  # network errors, timeouts, truncation: transient, retried next run
        return "error", f"{type(e).__name__}: {e}"[:120]
    finally:
        if tmp and os.path.exists(tmp):
            os.remove(tmp)


def lookup_json(url, pacer, headers=None):
    """GET JSON for a lookup service: (data, outcome); outcome is None on success, 'skipped' when the
    host is rate-limited (it is then paused for this run), 'none' for 404 and 'error' otherwise."""
    host = urllib.parse.urlsplit(url).hostname
    if pacer.paused(host):
        return None, "skipped"
    pacer.wait(url)
    try:
        return get_json(url, tries=2, headers=headers)[0], None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            pacer.pause(host, pause_seconds(e.headers))
            return None, "skipped"
        return None, "none" if e.code == 404 else "error"
    except TRANSIENT_ERRORS:
        return None, "error"


def s2_lookup(doi, pacer):
    """Semantic Scholar's open-access PDF link for a DOI: (outcome, [url])."""
    data, outcome = lookup_json(S2_API + urllib.parse.quote(doi, safe="/") + "?fields=openAccessPdf", pacer)
    if outcome:
        return outcome, []
    pdf = (data.get("openAccessPdf") or {}).get("url") or ""
    return ("found" if pdf else "none"), [pdf] if pdf else []


def core_lookup(doi, pacer):
    """CORE's copies of a DOI, which it aggregates from open repositories: (outcome, [url, ...])."""
    url = CORE_API + "?" + urllib.parse.urlencode({"q": f'doi:"{doi}"', "limit": "5"})
    data, outcome = lookup_json(url, pacer, {"Authorization": f"Bearer {key_file('core/api_key')}"})
    if outcome:
        return outcome, []
    urls = []
    for r in data.get("results") or []:
        if norm_doi(r.get("doi")) == doi:
            urls += [r.get("downloadUrl") or ""] + list(r.get("sourceFulltextUrls") or [])
    # CORE's own downloads (core.ac.uk, and the API's /download) sit behind a browser challenge, and some
    # source "URLs" are reference-list text; keep the repositories' own http(s) links.
    urls = [u for u in dict.fromkeys(urls) if re.match(r"https?://", u) and "core.ac.uk" not in u]
    return ("found" if urls else "none"), urls


CORE_API = "https://api.core.ac.uk/v3/search/works/"
LOOKUPS = [("core", "CORE", core_lookup, lambda: bool(key_file("core/api_key"))),
           ("s2", "Semantic Scholar", s2_lookup, lambda: True)]


def fetch_one(rec, store, pacer, tried, tdm_done, lock, tool_sha):
    """Try the work's open-access locations, then CORE (with a key) and Semantic Scholar by DOI, then
    any publisher TDM route whose key is installed."""
    wid = short_wid(rec["id"])

    def record(url, host, outcome, detail=""):
        append_tsv(store / "attempts.tsv", {"openalex_id": wid, "url": url, "host": host, "outcome": outcome,
                                            "detail": detail, "when": now()}, ATTEMPT_FIELDS, lock)

    def attempt(cand, **kw):
        outcome, detail = try_candidate(rec, cand, store, pacer, lock, tool_sha, **kw)
        record(cand[1], cand[2], outcome, detail)
        return outcome in OPEN_HELD and outcome

    cands = [c for c in candidates(rec) if c[1] not in tried]
    for cand in cands:
        if result := attempt(cand):
            return result
    doi = norm_doi(rec.get("doi"))
    for prefix, host, lookup, enabled in LOOKUPS:
        if not doi or f"{prefix}:{doi}" in tried or not enabled():
            continue
        outcome, urls = lookup(doi, pacer)
        if outcome == "skipped":
            continue
        record(f"{prefix}:{doi}", host, f"{prefix}_{outcome}", " ".join(urls)[:300])
        for u in [u for u in urls if u not in tried]:
            cands.append(("landing", u, host, "", ""))
            if result := attempt(cands[-1]):
                return result
    for name, route in TDM_ROUTES.items():
        url = route["url"].format(urllib.parse.quote(doi, safe=""))
        token = key_file(route["key"])
        if (wid in tdm_done or not doi.startswith(route["prefixes"]) or url in tried or not token
                or pacer.paused(urllib.parse.urlsplit(url).hostname)):
            continue
        cands.append(("pdf", url, route["host"], "publishedVersion", ""))
        if result := attempt(cands[-1], area=f"tdm/{name}", headers={route["header"]: token}, tdm=True):
            return f"tdm_{result}"
    return "failed" if cands else "no_copy"


def held(store, manifest, statuses=OPEN_HELD):
    """Works whose latest manifest row has one of these statuses and whose file is present."""
    return {w for w, r in manifest.items()
            if r["status"] in statuses and (store / (r.get("path") or f"pdf/{w}.pdf")).exists()}


def fetch(store, tiers, workers, retry_failed, limit=None):
    lock_file = store_lock(store)
    for d in ("pdf", "text", "tmp", "quarantine"):
        (store / d).mkdir(parents=True, exist_ok=True)
    recs = load_records(store)
    aliases = load_aliases(store)
    order = {}
    for tier, rows in load_seeds().items():
        if tiers and tier not in tiers:
            continue
        rank = TIER_RANK.get(tier, 0)
        for r in rows:
            wid = seed_wid(r, aliases)
            if wid in recs:
                key = (rank, -int(r.get("ref_count") or 0), wid)
                order[wid] = min(order.get(wid, key), key)
    manifest = load_manifest(store)
    done, tdm_done = held(store, manifest), held(store, manifest, TDM_HELD)
    latest = {}
    for r in load_attempts(store):
        latest[r["url"]] = r["outcome"]
    tried = set() if retry_failed else {u for u, o in latest.items() if not transient(o)}
    tried |= {r["url"] for r in manifest.values() if r["status"] == "withdrawn"}
    todo = [recs[w] for w in sorted(set(order) - done, key=order.get) if recs[w].get("type") not in SKIP_TYPES]
    todo = todo[:limit] if limit else todo
    print(f"{len(order)} works selected; {len(done & set(order))} held open, {len(tdm_done & set(order))} held "
          f"as TDM copies; {len(todo)} to try", flush=True)
    tool_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    pacer, lock = HostPacer(3.0), threading.Lock()
    results = Counter()
    with concurrent.futures.ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(fetch_one, r, store, pacer, tried, tdm_done, lock, tool_sha) for r in todo]
        for n, f in enumerate(concurrent.futures.as_completed(futs), 1):
            results[f.result()] += 1
            if n % 25 == 0 or n == len(todo):
                print(f"  {n}/{len(todo)} {dict(results)}", flush=True)
    lock_file.close()


# ---------------------------------------------------------------- withdraw

def withdraw(store, wids, reason):
    """Remove held copies: move PDF and text to quarantine/withdrawn/ and append a manifest row."""
    lock_file = store_lock(store)
    manifest = load_manifest(store)
    dest = store / "quarantine" / "withdrawn"
    dest.mkdir(parents=True, exist_ok=True)
    lock = threading.Lock()
    for w in map(short_wid, wids):
        row = manifest.get(w)
        if not row or row["status"] not in OPEN_HELD + TDM_HELD:
            print(f"{w}: no held copy", file=sys.stderr)
            continue
        pdf = Path(row.get("path") or f"pdf/{w}.pdf")
        for src in (store / pdf, store / text_path(pdf)):
            if src.exists():
                os.replace(src, dest / src.name)
        append_tsv(store / "manifest.tsv", dict(row, status="withdrawn", retrieved=now(), note=reason,
                                                path=f"quarantine/withdrawn/{pdf.name}"), MANIFEST_FIELDS, lock)
        print(f"{w}: withdrawn")
    lock_file.close()


# ---------------------------------------------------------------- index

def surname(authorship):
    name = (authorship.get("author") or {}).get("display_name") or authorship.get("raw_author_name") or ""
    return name.split()[-1] if name.split() else ""


def first_author(rec):
    auths = rec.get("authorships") or []
    if len(auths) > 2:
        return f"{surname(auths[0])} et al."
    return " & ".join(surname(a) for a in auths)


def venue(rec):
    return (((rec.get("primary_location") or {}).get("source")) or {}).get("display_name") or ""


def index(store, out):
    recs = load_records(store)
    aliases = load_aliases(store)
    manifest = load_manifest(store)
    attempts = defaultdict(set)
    for r in load_attempts(store):
        attempts[r["openalex_id"]].add(r["outcome"])
    work_tiers, work_qs, work_topic = defaultdict(set), defaultdict(set), {}
    unresolved = []
    for tier, rows in load_seeds().items():
        for r in rows:
            wid = seed_wid(r, aliases)
            if wid not in recs:
                unresolved.append({"tier": tier, "key": r["key"], "files": r.get("files", ""),
                                   "questions": r.get("questions", ""), "citation": r.get("citation", "")})
                continue
            work_tiers[wid].add(tier)
            if tier.startswith("cited"):
                work_qs[wid] |= {q for q in (r.get("questions") or "").split(";") if q}
            if r.get("topic"):
                work_topic.setdefault(wid, r["topic"])
    rows = []
    for wid in sorted(work_tiers, key=lambda w: (recs[w].get("publication_year") or 0, w)):
        rec = recs[wid]
        oa = rec.get("open_access") or {}
        m = manifest.get(wid)
        if m:
            ft = m["status"]
        elif rec.get("type") in SKIP_TYPES:
            ft = "skipped_type"
        elif any(not is_lookup(o) for o in attempts[wid]):
            ft = "failed"
        elif attempts[wid] or not (rec.get("doi") or candidates(rec)):
            ft = "no_copy"
        else:
            ft = "not_tried"
        rows.append({"openalex_id": wid, "doi": norm_doi(rec.get("doi")), "year": rec.get("publication_year") or "",
                     "first_author": first_author(rec), "title": re.sub(r"\s+", " ", rec.get("title") or "").strip(),
                     "venue": venue(rec), "type": rec.get("type") or "", "cited_by": rec.get("cited_by_count") or 0,
                     "oa_status": oa.get("oa_status") or "", "fulltext": ft, "tiers": ";".join(sorted(work_tiers[wid])),
                     "questions": ";".join(sorted(work_qs[wid])), "topic": work_topic.get(wid, ""),
                     "oa_topic": ((rec.get("primary_topic") or {}).get("display_name") or "")})
    out.mkdir(parents=True, exist_ok=True)
    fields = ["openalex_id", "doi", "year", "first_author", "title", "venue", "type", "cited_by", "oa_status",
              "fulltext", "tiers", "questions", "topic", "oa_topic"]
    write_tsv(out / "works.tsv", rows, fields)
    write_tsv(out / "unresolved.tsv", unresolved, ["tier", "key", "citation", "files", "questions"])
    write_index_md(out, rows, unresolved)
    write_by_question(out, rows)
    print(f"{len(rows)} works, {len(unresolved)} unresolved seed rows -> {out}")


def table(counter, head, keyorder=None):
    keys = keyorder or [k for k, _ in counter.most_common()]
    lines = [f"| {head} | Works |", "| --- | ---: |"]
    lines += [f"| {k or '(none)'} | {counter[k]} |" for k in keys if counter[k]]
    return "\n".join(lines)


def write_index_md(out, rows, unresolved):
    tiers = Counter(t for r in rows for t in r["tiers"].split(";"))
    ft = Counter(r["fulltext"] for r in rows)
    held_by_tier = Counter(t for r in rows if r["fulltext"] in OPEN_HELD for t in r["tiers"].split(";"))
    tdm_by_tier = Counter(t for r in rows if r["fulltext"] in TDM_HELD for t in r["tiers"].split(";"))
    types = Counter(r["type"] for r in rows)
    decades = Counter((f"{(int(r['year']) // 10) * 10}s" if r["year"] else "") for r in rows)
    venues = Counter(r["venue"] for r in rows if r["venue"])
    held_n, tdm_n = ft["ok"] + ft["no_text"], ft["tdm_ok"] + ft["tdm_no_text"]
    tier_lines = ["| Tier | Works | Open copy held | TDM copy held |", "| --- | ---: | ---: | ---: |"]
    tier_lines += [f"| {t} | {n} | {held_by_tier[t]} | {tdm_by_tier[t]} |" for t, n in sorted(tiers.items())]
    text = [
        "# Library index",
        "",
        f"Generated by `library.py index` on {now()[:10]}. Do not edit by hand.",
        "",
        f"**{len(rows)} works**; open full text held for **{held_n}** ({ft['ok']} with a text layer checked "
        f"against the title, {ft['no_text']} scans without one), and publisher TDM copies for **{tdm_n}** more "
        f"(local search and mining only). {len(unresolved)} seed rows are unresolved (see `unresolved.tsv`).",
        "",
        "Full-text status: `ok` open copy held and title-checked; `no_text` open scan held, title unchecked; "
        "`tdm_ok`, `tdm_no_text` the same for a publisher TDM copy; `failed` copies tried, none usable; "
        "`no_copy` no copy known; `not_tried` not yet attempted; `withdrawn` removed with a recorded reason; "
        "`skipped_type` datasets, errata and similar.",
        "",
        "## By tier", "", "\n".join(tier_lines), "",
        "## Full-text status", "", table(ft, "Status"), "",
        "## By type", "", table(types, "Type"), "",
        "## By decade", "", table(decades, "Decade", sorted(decades)), "",
        "## Most frequent venues", "", table(Counter(dict(venues.most_common(25))), "Venue"), "",
    ]
    (out / "INDEX.md").write_text("\n".join(text), encoding="utf-8")


def write_by_question(out, rows):
    byq = defaultdict(list)
    for r in rows:
        for q in r["questions"].split(";"):
            if q:
                byq[q].append(r)

    def order(q):
        m = re.match(r"([QB])-(\d+)", q)
        return (0, q[0], int(m.group(2))) if m else (1, q, 0)

    text = ["# Works by question", "",
            "Works the repository cites (tiers `cited-ids` and `cited-authoryear`), grouped by the questions "
            "(Q-, B-) and catalogue entries (src:) whose sections or files cite them. Generated by "
            "`library.py index`; do not edit by hand.",
            "Full text: **T** open copy held and title-checked, **S** open scan held, **M** publisher TDM copy "
            "(local search and mining only), blank not held.", ""]
    for q in sorted(byq, key=order):
        text += [f"## {q} ({len(byq[q])})", ""]
        for r in sorted(byq[q], key=lambda r: (r["year"] or 0, r["first_author"])):
            mark = {"ok": "**T** ", "no_text": "**S** ", "tdm_ok": "**M** ", "tdm_no_text": "**M** "}.get(r["fulltext"], "")
            doi = f" [doi](https://doi.org/{r['doi']})" if r["doi"] else ""
            text.append(f"- {mark}{r['first_author']} {r['year']}. {r['title']}. *{r['venue']}*.{doi}")
        text.append("")
    (out / "by-question.md").write_text("\n".join(text), encoding="utf-8")


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("harvest")
    p.add_argument("repo")
    p = sub.add_parser("expand")
    p.add_argument("--store", type=Path, default=DEFAULT_STORE)
    p.add_argument("--min-refs", type=int, default=5, help="minimum number of seed works referencing a work")
    p.add_argument("--out", type=Path, default=SEEDS)
    p = sub.add_parser("withdraw")
    p.add_argument("wids", nargs="+")
    p.add_argument("--reason", required=True)
    p.add_argument("--store", type=Path, default=DEFAULT_STORE)
    for name in ("resolve", "fetch", "index"):
        p = sub.add_parser(name)
        p.add_argument("--store", type=Path, default=DEFAULT_STORE)
        if name == "resolve":
            p.add_argument("--recheck", action="store_true", help="retry keys already found dead (datasets, invalid, deleted)")
        if name == "fetch":
            p.add_argument("--tier", nargs="*", default=None, help="seed tiers to fetch (default: all)")
            p.add_argument("--workers", type=int, default=6)
            p.add_argument("--retry-failed", action="store_true", help="retry URLs that failed permanently before")
            p.add_argument("--limit", type=int, help="try at most this many works (for testing)")
        if name == "index":
            p.add_argument("--out", type=Path, default=HERE)
    a = ap.parse_args()
    if a.cmd == "harvest":
        harvest(a.repo)
    elif a.cmd == "expand":
        expand(a.store, a.min_refs, a.out)
    elif a.cmd == "resolve":
        resolve(a.store, a.recheck)
    elif a.cmd == "fetch":
        fetch(a.store, a.tier, a.workers, a.retry_failed, a.limit)
    elif a.cmd == "withdraw":
        withdraw(a.store, a.wids, a.reason)
    else:
        index(a.store, a.out)


if __name__ == "__main__":
    main()
