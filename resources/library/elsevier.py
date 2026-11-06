#!/usr/bin/env python3
"""Restricted Elsevier XML acquisition and approval-gated bounded excerpts.

Fetch never prints article text. All payloads, derivatives and export accounting
stay below STORE/tdm/elsevier. The ordinary PDF library is never changed.
"""

import argparse
import contextlib
import csv
import email.utils
import fcntl
import hashlib
import http.client
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

from library import OPEN_HELD, key_file, norm_doi, now, pdf_pages, read_tsv

API = "https://api.elsevier.com/content/article/doi/"
PREFIXES = ("10.1016/", "10.1006/")
MAX_BYTES = 32 * 1024 * 1024
NOTICE = ("Some rights reserved. This work permits non-commercial use, distribution and reproduction in any medium, "
          "provided the original author and source are credited.")
FIELDS = ["utc", "openalex_id", "doi", "status", "http", "xml_path", "xml_sha256",
          "text_path", "text_sha256", "bytes", "chars", "words", "mode", "bodies",
          "sections", "paragraphs", "figures", "tables", "references", "completeness", "url", "tool_sha256"]
ATTEMPT_FIELDS = ["utc", "openalex_id", "doi", "status", "http", "bytes", "xml_sha256", "retry_after"]
EXCLUDED = {"coredata", "bibliography", "references", "reference", "ref-list", "bib-reference", "bib-reference-list"}


class Rejected(ValueError):
    pass


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise Rejected("redirect_refused")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def check_ancestors(path):
    path = Path(path).absolute()
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("restricted_path_symlink")


def private_dir(path):
    check_ancestors(path)
    path.mkdir(parents=True, exist_ok=True, mode=0o700)
    path.chmod(0o700)


@contextlib.contextmanager
def locked(store):
    root = Path(store) / "tdm" / "elsevier"
    check_ancestors(root)
    private_dir(root.parent)
    private_dir(root)
    fd = os.open(root / ".lock", os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield root
    finally:
        os.close(fd)


def atomic(path, data, mode=0o600):
    check_ancestors(path)
    private_dir(path.parent)
    fd, tmp = tempfile.mkstemp(prefix=".partial-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def append(path, row, fields):
    check_ancestors(path)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields, delimiter="\t", extrasaction="ignore", lineterminator="\n")
        if f.tell() == 0:
            w.writeheader()
        w.writerow(row)
        f.flush()
        os.fsync(f.fileno())


def latest(path):
    return {r["openalex_id"]: r for r in read_tsv(path)} if path.exists() else {}


def local_name(node):
    return node.tag.rsplit("}", 1)[-1].lower() if isinstance(node.tag, str) else ""


def content(node):
    if local_name(node) in EXCLUDED:
        return ""
    out = [node.text or ""]
    for child in node:
        out.extend((content(child), child.tail or ""))
    if local_name(node) in {"para", "p", "section", "sec", "title", "section-title", "row"}:
        out.append("\n")
    return "".join(out)


def parse_article(data, doi):
    if len(data) > MAX_BYTES:
        raise Rejected("too_large")
    # Also catches UTF-16/32 declarations before the XML parser sees them.
    declarations = data.replace(b"\x00", b"").upper()
    if b"<!DOCTYPE" in declarations or b"<!ENTITY" in declarations:
        raise Rejected("dtd_or_entity_refused")
    try:
        root = ET.fromstring(data)
    except (ET.ParseError, RecursionError):
        raise Rejected("malformed_xml") from None
    names = Counter(local_name(n) for n in root.iter())
    if names["service-error"] or names["error-response"] or local_name(root) in {"error", "errors"}:
        raise Rejected("service_error_xml")
    if local_name(root) != "full-text-retrieval-response":
        raise Rejected("unexpected_xml_root")
    core = [n for n in root if local_name(n) == "coredata"]
    found = {norm_doi("".join(n.itertext())) for c in core for n in c.iter() if local_name(n) == "doi"}
    if found != {norm_doi(doi)}:
        raise Rejected("doi_mismatch")
    original = [n for n in root.iter() if local_name(n) == "originaltext"]
    bodies = [n for o in original for n in o.iter() if local_name(n) == "body"]
    raw = [n for o in original for n in o.iter() if local_name(n) == "rawtext"]
    chapters = [n for o in original for n in o.iter() if local_name(n) == "chapter"]
    chapter_sections = [n for n in chapters[0] if local_name(n) == "sections"] if len(chapters) == 1 else []
    selected = bodies or raw or chapter_sections
    if not selected:
        raise Rejected("metadata_only")
    try:
        text = "\n".join(content(n) for n in selected)
    except RecursionError:
        raise Rejected("xml_too_deep") from None
    text = "\n".join(" ".join(line.split()) for line in text.splitlines() if line.strip())
    if len(text) < 200 or len(text.split()) < 30:
        raise Rejected("insufficient_body_text")
    mode = "body" if bodies else "rawtext" if raw else "chapter_sections"
    counts = {"mode": mode, "bodies": len(bodies),
              "sections": names["section"] + names["sec"], "paragraphs": names["para"] + names["p"],
              "figures": names["figure"] + names["fig"], "tables": names["table"],
              "references": names["bib-reference"] + names["ref"],
              "chars": len(text), "words": len(text.split()),
              "completeness": {"body": "structured_body_present_not_content_verified",
                               "rawtext": "rawtext_unsegmented_not_content_verified",
                               "chapter_sections": "chapter_sections_present_not_content_verified"}[mode]}
    return text, counts


def request_article(doi, key, opener=None):
    url = API + urllib.parse.quote(doi, safe="") + "?view=FULL"
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != "https" or parsed.netloc != "api.elsevier.com":
        raise ValueError("credential_host_refused")
    req = urllib.request.Request(url, headers={"Accept": "text/xml", "X-ELS-APIKey": key,
                                             "User-Agent": "EPRP-library-Elsevier/1.0 (research TDM)"})
    opener = opener or urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(req, timeout=90) as response:
            if response.geturl() != url:
                raise Rejected("redirect_refused")
            headers = {k.lower(): v for k, v in response.headers.items()}
            data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise Rejected("too_large")
            if headers.get("content-length", "").isdigit() and int(headers["content-length"]) != len(data):
                raise Rejected("truncated_response")
            return response.status, headers, data
    except urllib.error.HTTPError as e:
        headers = {k.lower(): v for k, v in e.headers.items()}
        e.close()
        return e.code, headers, b""


def delay(headers):
    value = headers.get("retry-after", "")
    try:
        return max(0.0, float(value))
    except ValueError:
        try:
            return max(0.0, email.utils.parsedate_to_datetime(value).timestamp() - time.time())
        except (ValueError, TypeError, OverflowError):
            return 0.0


def quota_delay(headers):
    if headers.get("x-ratelimit-remaining", "").strip() != "0":
        return 0.0
    try:
        reset = float(headers.get("x-ratelimit-reset", ""))
        return max(60.0, reset - time.time())
    except ValueError:
        return 3600.0


def candidates(catalogue, ids=None, dois=None):
    rows = read_tsv(catalogue)
    if not rows or not {"openalex_id", "doi", "fulltext", "tiers"}.issubset(rows[0]):
        raise ValueError("invalid_catalogue")
    byid = {r["openalex_id"]: r for r in rows}
    wanted = [line.strip() for line in Path(ids).read_text().splitlines() if line.strip() and not line.startswith("#")] if ids else []
    if any(w not in byid for w in wanted):
        raise ValueError("unknown_priority_id")
    explicit = {norm_doi(d) for d in (dois or [])}
    if explicit - {norm_doi(r["doi"]) for r in rows}:
        raise ValueError("doi_not_in_catalogue")
    order = {w: n for n, w in enumerate(wanted)}
    def rank(r):
        tiers = set(r["tiers"].split(";"))
        core = "canon" in tiers or any(t.startswith("cited-") for t in tiers)
        return (order.get(r["openalex_id"], len(order)), 0 if core else 1 if "agendas" in tiers else 2)
    out = []
    seen = set()
    for r in sorted(rows, key=rank):
        wid, doi = r["openalex_id"], norm_doi(r["doi"])
        if not re.fullmatch(r"W\d+", wid):
            raise ValueError("invalid_work_id")
        if r["fulltext"] in OPEN_HELD or not doi or doi in seen:
            continue
        if r["fulltext"] in {"rejected", "withdrawn", "quarantined", "quarantine", "skipped_type"}:
            continue
        if explicit and doi not in explicit:
            continue
        if not doi.startswith(PREFIXES) and doi not in explicit:
            continue
        if not re.fullmatch(r"10\.\d{4,9}/[^\s]+", doi):
            raise ValueError("invalid_doi")
        seen.add(doi)
        out.append(dict(r, doi=doi))
    return out


def held(root, row):
    for kind, suffix in (("xml", ".xml"), ("text", ".txt")):
        expected = f"{kind}/{row['openalex_id']}{suffix}"
        if row[f"{kind}_path"] != expected:
            raise ValueError("invalid_manifest_path")
        path = root / expected
        check_ancestors(path)
        if path.is_symlink() or not path.is_file() or sha(path.read_bytes()) != row[f"{kind}_sha256"]:
            raise ValueError("held_checksum_or_path_failure")
    return True


def fetch(catalogue, store, ids=None, dois=None, limit=None, interval=3.0, retry_failed=False, opener=None):
    if interval < 3 or (limit is not None and limit < 1):
        raise ValueError("invalid_limit_or_interval")
    rows = candidates(catalogue, ids, dois)
    summary = Counter(selected=len(rows), held=0, fetched=0, rejected=0, skipped_failed=0, requests=0)
    stop = "complete"
    with locked(store) as root:
        manifests, attempts = latest(root / "manifest.tsv"), latest(root / "attempts.tsv")
        statepath = root / "rate-state.json"
        state = json.loads(statepath.read_text()) if statepath.exists() else {}
        key = key_file("elsevier/api_key")
        if not key:
            raise ValueError("elsevier_key_missing")
        tool_hash = sha(Path(__file__).read_bytes())
        if not (root / "snippet-exports.json").exists() and not manifests:
            atomic(root / "snippet-exports.json", b'{"version":1,"exports":{}}')
        next_at, consecutive_errors = 0.0, 0
        for row in rows:
            wid, doi = row["openalex_id"], row["doi"]
            if wid in manifests:
                if manifests[wid]["doi"] != doi:
                    raise ValueError("held_doi_changed")
                held(root, manifests[wid])
                summary["held"] += 1
                continue
            if wid in attempts and attempts[wid]["status"] not in {"http_401", "http_403", "http_429"} and not retry_failed:
                summary["skipped_failed"] += 1
                continue
            if limit is not None and summary["requests"] >= limit:
                stop = "limit"
                break
            if float(state.get("not_before", 0)) > time.time():
                return dict(summary, stopped="cooldown", not_before=state["not_before"])
            wait = next_at - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            data, headers, code = b"", {}, ""
            try:
                summary["requests"] += 1
                next_at = time.monotonic() + interval
                code, headers, data = request_article(doi, key, opener)
                next_at = time.monotonic() + max(interval, delay(headers))
                if code != 200:
                    raise Rejected(f"http_{code}")
                text, counts = parse_article(data, doi)
                xmlpath, textpath = root / "xml" / f"{wid}.xml", root / "text" / f"{wid}.txt"
                if xmlpath.exists() and xmlpath.read_bytes() != data:
                    raise ValueError("unmanifested_xml_collision")
                atomic(xmlpath, data, 0o400)
                textdata = text.encode("utf-8")
                atomic(textpath, textdata, 0o400)
                append(root / "manifest.tsv", dict(row, utc=now(), status="tdm_xml_ok", http=code,
                       xml_path=str(xmlpath.relative_to(root)), xml_sha256=sha(data),
                       text_path=str(textpath.relative_to(root)), text_sha256=sha(textdata), bytes=len(data),
                       url=API + urllib.parse.quote(doi, safe="") + "?view=FULL", tool_sha256=tool_hash, **counts), FIELDS)
                outcome = "tdm_xml_ok"
                summary["fetched"] += 1
            except Rejected as e:
                outcome = str(e)
                summary["rejected"] += 1
                if data:
                    atomic(root / "quarantine" / f"{wid}-{sha(data)}.xml", data, 0o400)
            except (urllib.error.URLError, http.client.HTTPException, TimeoutError, OSError):
                outcome, stop = "transport_error", "transport_error"
            retry = max(delay(headers), quota_delay(headers))
            append(root / "attempts.tsv", dict(utc=now(), openalex_id=wid, doi=doi, status=outcome,
                   http=code, bytes=len(data), xml_sha256=sha(data) if data else "", retry_after=retry), ATTEMPT_FIELDS)
            print(json.dumps({"work": wid, "status": outcome, "requests": summary["requests"],
                              "fetched": summary["fetched"]}), flush=True)
            if code in {401, 403, 429} or quota_delay(headers) or (isinstance(code, int) and code >= 500):
                stop = f"http_{code}" if code != 200 else "quota_exhausted"
                retry = max(retry, 60 if code == 429 else 0)
            consecutive_errors = consecutive_errors + 1 if outcome in {"redirect_refused", "service_error_xml", "truncated_response", "malformed_xml", "unexpected_xml_root"} else 0
            if consecutive_errors >= 3:
                stop = "repeated_response_errors"
            atomic(statepath, json.dumps({"not_before": time.time() + max(interval, retry), "reason": stop}).encode())
            if stop != "complete":
                break
        return dict(summary, stopped=stop)


def approval_receipt(path):
    path = Path(path)
    if path.is_symlink() or path.stat().st_mode & 0o077:
        raise ValueError("approval_must_be_private_regular_file")
    data = path.read_bytes()
    receipt = json.loads(data)
    if receipt.get("approved_snippets") is not True or not re.fullmatch(r"[0-9a-f]{64}", receipt.get("receipt_sha256", "")):
        raise ValueError("snippets_not_approved")
    source = Path(receipt.get("receipt_path", ""))
    if not source.is_absolute() or source.is_symlink() or not source.is_file() or source.stat().st_mode & 0o077:
        raise ValueError("approval_source_must_be_private_file")
    if sha(source.read_bytes()) != receipt["receipt_sha256"]:
        raise ValueError("approval_receipt_checksum_failure")
    return sha(data)


def verified_pdf(root, rows, doi):
    inventory = root / "diagnostics/20261106/pdf-format.json"
    check_ancestors(inventory)
    if not inventory.exists():
        return None
    ids = {r["openalex_id"] for r in rows}
    matches = [r for r in json.loads(inventory.read_text()) if r["openalex_id"] in ids
               and r["status"] == "pdf_recovered_verified_identity_and_pages"]
    if not matches:
        return None
    row = matches[0]
    wid = row["openalex_id"]
    if not re.fullmatch(r"W\d+", wid) or any(not re.fullmatch(r"[0-9a-f]{64}", row.get(k, ""))
            for k in ("sha256", "text_sha256", "source_xml_sha256")):
        raise ValueError("invalid_pdf_identity_or_hash")
    if norm_doi(row["doi"]) != doi:
        raise ValueError("held_doi_changed")
    if row.get("doi_metadata_verified") is not True:
        raise ValueError("pdf_identity_not_verified")
    expected_paths = {"path": f"diagnostics/20261106/pdf-candidates/{wid}-{row['sha256']}.pdf",
                      "text_path": f"diagnostics/20261106/pdf-candidates/{wid}-{row['sha256']}.txt",
                      "source_xml_path": f"quarantine/{wid}-{row['source_xml_sha256']}.xml"}
    for field, expected in expected_paths.items():
        if row[field] != expected:
            raise ValueError("invalid_pdf_inventory_path")
        path = root / expected
        check_ancestors(path)
        digest = row[{"path": "sha256", "text_path": "text_sha256", "source_xml_path": "source_xml_sha256"}[field]]
        if not path.is_file() or sha(path.read_bytes()) != digest:
            raise ValueError("pdf_inventory_checksum_failure")
    data = (root / row["source_xml_path"]).read_bytes()
    declarations = data.replace(b"\0", b"").upper()
    if len(data) > MAX_BYTES or b"<!DOCTYPE" in declarations or b"<!ENTITY" in declarations:
        raise ValueError("unsafe_pdf_identity_xml")
    xml = ET.fromstring(data)
    dois = {norm_doi(n.text) for c in xml if local_name(c) == "coredata" for n in c if local_name(n) == "doi"}
    expected = {int(n.text) for n in xml.iter() if local_name(n) == "web-pdf-page-count" and (n.text or "").isdigit()}
    if dois != {doi} or len(expected) != 1:
        raise ValueError("pdf_source_identity_mismatch")
    pages = next(iter(expected))
    if (type(row["pages"]) is not int or row["pages"] != pages or row["expected_pages"] != pages
            or row.get("page_coverage") != 1.0 or pdf_pages(root / row["path"]) != pages
            or row.get("first_page_title_match", 0) < 0.8 or row.get("novel_tokens_beyond_cached_xml", 0) < 100):
        raise ValueError("pdf_page_coverage_or_identity_failure")
    return dict(row, source_format="pdf", pdf_sha256=row["sha256"])


def query(catalogue, store, doi, needle, approval, chars=200):
    approval_hash = approval_receipt(approval)
    doi = norm_doi(doi)
    if not needle.strip() or not 1 <= chars <= 200:
        raise ValueError("invalid_query_or_character_limit")
    rows = [r for r in read_tsv(catalogue) if norm_doi(r["doi"]) == doi]
    if not rows:
        raise ValueError("doi_not_in_catalogue")
    with locked(store) as root:
        ledger = root / "snippet-exports.json"
        if not ledger.is_file() or ledger.is_symlink():
            raise ValueError("export_ledger_missing")
        accounting = json.loads(ledger.read_text())
        if accounting.get("version") != 1 or not isinstance(accounting.get("exports"), dict):
            raise ValueError("invalid_export_ledger")
        prior = accounting["exports"].get(doi, {"chars": 0})
        used = prior["chars"]
        if type(used) is not int or not 0 <= used <= 200:
            raise ValueError("invalid_export_budget")
        available = min(chars, 200 - used)
        if not available:
            return {"doi": doi, "status": "budget_exhausted", "remaining_chars": 0}
        manifests = latest(root / "manifest.tsv")
        matches = [manifests[r["openalex_id"]] for r in rows if r["openalex_id"] in manifests]
        row = matches[0] if matches else verified_pdf(root, rows, doi)
        if not row:
            return {"doi": doi, "status": "not_held"}
        if norm_doi(row["doi"]) != doi:
            raise ValueError("held_doi_changed")
        if row.get("source_format") != "pdf":
            held(root, row)
        text = " ".join((root / row["text_path"]).read_text(encoding="utf-8").split())
        match = re.search(re.escape(needle), text, re.IGNORECASE)
        if not match:
            return {"doi": doi, "status": "no_match", "remaining_chars": 200 - used}
        if len(needle) > available:
            return {"doi": doi, "status": "query_exceeds_remaining_budget", "remaining_chars": 200 - used}
        start = max(0, match.start() - (available - len(needle)) // 2)
        excerpt = text[start:start + available]
        accounting["exports"][doi] = {"chars": used + len(excerpt), "utc": now(),
                                      "approval_sha256": approval_hash, "last_excerpt_sha256": sha(excerpt.encode())}
        # Reserve durably before any text can leave the process, including a broken pipe.
        atomic(ledger, json.dumps(accounting, sort_keys=True).encode())
        source = next(r for r in rows if r["openalex_id"] == row["openalex_id"])
        return {"doi": doi, "url": "https://doi.org/" + urllib.parse.quote(doi, safe="/"),
                "title": source.get("title", ""),
                "credit": f"{source.get('first_author') or 'Author not listed in catalogue'}, {source.get('year', '')}; {source.get('venue', '')}; Elsevier",
                "notice": NOTICE, "excerpt": excerpt, "excerpt_chars": len(excerpt),
                "text_sha256": row["text_sha256"], "start_character": start,
                "source_format": row.get("source_format", "xml"),
                "remaining_chars": 200 - used - len(excerpt)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("fetch", "query"):
        p = sub.add_parser(name)
        p.add_argument("--catalogue", type=Path, required=True)
        p.add_argument("--store", type=Path, required=True)
        if name == "fetch":
            p.add_argument("--ids", type=Path)
            p.add_argument("--doi", action="append", dest="dois")
            p.add_argument("--limit", type=int)
            p.add_argument("--interval", type=float, default=3.0)
            p.add_argument("--retry-failed", action="store_true")
        else:
            p.add_argument("--doi", required=True)
            p.add_argument("--needle", required=True)
            p.add_argument("--approval", type=Path, required=True)
            p.add_argument("--chars", type=int, default=200)
    args = vars(parser.parse_args(argv))
    command = args.pop("command")
    try:
        result = fetch(**args) if command == "fetch" else query(**args)
        print(json.dumps(result, sort_keys=True), flush=True)
    except Exception:
        # Exceptions can contain payload text, paths or server-supplied credentials.
        print(json.dumps({"error": "operation_failed", "command": command}), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
