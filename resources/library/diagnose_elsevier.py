#!/usr/bin/env python3
"""Metadata-only failure classification, finite access probes and cached recovery.

Run beside the versioned elsevier.py and library.py on the restricted host.
Payloads and all sidecars stay in STORE/tdm/elsevier/diagnostics/20261106.
No article or server error text is emitted. This never resets snippet budgets.
"""
import argparse
import collections
import http.client
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import elsevier as e
import library

TIERS = {"canon", "cited-ids", "cited-authoryear", "barry-2003-list", "barry-2003-endnote"}
KELLEY = "10.1016/s0031-0182(00)00207-8"
SUBDIR = "diagnostics/20261106"


def core(row):
    return bool(TIERS.intersection(row.get("tiers", "").split(";")))


def xml_root(data):
    if len(data) > e.MAX_BYTES or any(x in data.replace(b"\0", b"").upper() for x in (b"<!DOCTYPE", b"<!ENTITY")):
        raise ValueError("unsafe_xml")
    return ET.fromstring(data)


def structure(data):
    root = xml_root(data)
    originals = [n for n in root.iter() if e.local_name(n) == "originaltext"]
    chapters = [n for o in originals for n in o.iter() if e.local_name(n) == "chapter"]
    sections = [n for n in chapters[0] if e.local_name(n) == "sections"] if len(chapters) == 1 else []
    counts = collections.Counter(e.local_name(n) for o in originals for n in o.iter())
    return {"originals": len(originals), "chapters": len(chapters), "chapter_sections": len(sections),
            "bodies": counts["body"], "rawtext": counts["rawtext"], "paragraphs": counts["para"],
            "front_back_matter": counts["fb-non-chapter"],
            "chapter_section_chars": sum(len(e.content(n)) for n in sections)}


def inputs(catalogue, root):
    rows = {r["openalex_id"]: r for r in e.read_tsv(catalogue)}
    attempts, held = e.latest(root / "attempts.tsv"), e.latest(root / "manifest.tsv")
    failures = [dict(rows[w], failure=a["status"], attempt_sha256=a["xml_sha256"])
                for w, a in attempts.items() if w not in held]
    return rows, failures, held


def classify(catalogue, store):
    with e.locked(store) as root:
        baseline = root / SUBDIR / "classification.json"
        if baseline.exists():
            existing = json.loads(baseline.read_text())
            return {k: v for k, v in existing.items() if k != "works"}
        rows, failures, held = inputs(catalogue, root)
        records = []
        for row in failures:
            x = {k: row.get(k, "") for k in ("openalex_id", "doi", "year", "type", "venue", "tiers", "failure")}
            x["core"] = core(row)
            doi = row["doi"]
            x["doi_pattern"] = "academic_press_1006" if doi.startswith("10.1006/") else "isbn_chapter" if doi.startswith("10.1016/b978") else "book_concept" if doi.startswith("10.1016/c") else "legacy_serial" if re.match(r"10\.1016/s\d", doi) else "journal_style"
            x["category"], x["evidence"] = "unresolved", "original_fetch_outcome_only"
            if row["failure"] == "metadata_only":
                path = root / "quarantine" / f"{row['openalex_id']}-{row['attempt_sha256']}.xml"
                e.check_ancestors(path)
                data = path.read_bytes()
                if e.sha(data) != row["attempt_sha256"]:
                    raise ValueError("quarantine_checksum_failure")
                x["structure"] = structure(data)
                x["category"] = "chapter_selector_omission" if x["structure"]["chapter_sections"] else "no_body_in_returned_xml"
                x["evidence"] = "direct_cached_xml_structure"
            records.append(x)
        counters = {k: dict(collections.Counter(str(x[k]) for x in records)) for k in ("failure", "type", "venue", "doi_pattern", "category")}
        coverage = []
        for tiers in (TIERS, TIERS | {"agendas"}):
            selected = [x for x in rows.values() if tiers.intersection(x["tiers"].split(";"))]
            ev = [x for x in selected if x["doi"].startswith(e.PREFIXES)]
            coverage.append({"tiers": sorted(tiers), "catalogue_all_publishers": len(selected), "catalogue_elsevier": len(ev),
                             "open_held": sum(x["fulltext"] in e.OPEN_HELD for x in ev),
                             "tdm_held": sum(x["openalex_id"] in held for x in ev),
                             "selected_failures": sum(x["openalex_id"] in {r["openalex_id"] for r in failures} for x in ev)})
        report = {"utc": e.now(), "held": len(held), "failures": len(records), "counts": counters,
                  "core_failed": sum(x["core"] for x in records), "coverage": coverage, "works": records}
        e.atomic(root / SUBDIR / "classification.json", json.dumps(report, sort_keys=True).encode())
        return {k: v for k, v in report.items() if k != "works"}


def error_category(data, code):
    try:
        root = xml_root(data)
    except (ValueError, ET.ParseError):
        return "unrecognised_payload"
    values = " ".join((n.text or "") for n in root.iter() if e.local_name(n) in {"statustext", "status-text", "message"}).lower()
    if "not entitled" in values or "notentitled" in values:
        return "resource_not_entitled"
    if "view" in values and "not valid" in values:
        return "view_invalid"
    if "api" in values and ("invalid" in values or "missing" in values):
        return "credential_error"
    if e.local_name(root) == "document-entitlement" and "requestor is entitled" in values:
        return "document_entitled"
    if code == 404:
        return "resource_not_found"
    if e.local_name(root) == "full-text-retrieval-response":
        return "retrieval_xml"
    return "unclassified_error"


def request(doi, view, key, opener=None, accept="text/xml"):
    url = e.API + urllib.parse.quote(doi, safe="") + ("?view=" + view if view else "")
    parsed = urllib.parse.urlsplit(url)
    if (parsed.scheme != "https" or parsed.netloc != "api.elsevier.com" or accept not in {"text/xml", "application/pdf"}
            or view not in ({None} if accept == "application/pdf" else {"FULL", "ENTITLED"})):
        raise ValueError("request_refused")
    req = urllib.request.Request(url, headers={"Accept": accept, "X-ELS-APIKey": key,
                                              "User-Agent": "EPRP-library-diagnosis/1.0"})
    opener = opener or urllib.request.build_opener(e.NoRedirect())
    try:
        response = opener.open(req, timeout=90)
    except urllib.error.HTTPError as err:
        response = err
    with response:
        if response.geturl() != url:
            raise e.Rejected("redirect_refused")
        data = response.read(e.MAX_BYTES + 1)
        if len(data) > e.MAX_BYTES:
            raise e.Rejected("too_large")
        return response.code, {k.lower(): v for k, v in response.headers.items()}, data


def pdf_coverage(result, expected):
    out = dict(result, expected_pages=expected,
               page_coverage=result.get("pages", 0) / expected if expected else None)
    if expected and 0 < result.get("pages", 0) < expected:
        out.update(status="pdf_incomplete_preview", body_confidence="incomplete_page_coverage")
    elif (expected and result.get("pages") == expected and result.get("first_page_title_match", 0) >= 0.8
          and result.get("novel_tokens_beyond_cached_xml", 0) >= 100):
        out.update(status="pdf_recovered_verified_identity_and_pages",
                   body_confidence="page_coverage_verified_substantial_text_not_content_reviewed")
    return out


def audit_pdfs(root, results):
    attempts = e.latest(root / "attempts.tsv")
    audited = []
    for result in results:
        if not result.get("pages"):
            audited.append(result)
            continue
        wid = result["openalex_id"]
        path = root / result["path"]
        e.check_ancestors(path)
        if e.sha(path.read_bytes()) != result["sha256"]:
            raise ValueError("pdf_checksum_failure")
        digest = attempts[wid]["xml_sha256"]
        cached = root / "quarantine" / f"{wid}-{digest}.xml"
        e.check_ancestors(cached)
        data = cached.read_bytes()
        if e.sha(data) != digest:
            raise ValueError("quarantine_checksum_failure")
        xml = xml_root(data)
        expected = {int(n.text) for n in xml.iter() if e.local_name(n) == "web-pdf-page-count" and (n.text or "").isdigit()}
        checked = pdf_coverage(result, next(iter(expected)) if len(expected) == 1 else 0)
        checked.update(source_xml_path=str(cached.relative_to(root)), source_xml_sha256=digest)
        audited.append(checked)
    return audited


def pdf_diagnostic(catalogue, store, opener=None):
    cases = ["W1964939024", "W2141405378", "W4252129349"]
    with e.locked(store) as root:
        rows, _, _ = inputs(catalogue, root)
        attempts = e.latest(root / "attempts.tsv")
        folder = root / SUBDIR
        existing_pdf = folder / "pdf-format.json"
        results = []
        if existing_pdf.exists():
            previous = json.loads(existing_pdf.read_text())
            audited = audit_pdfs(root, previous)
            archive = folder / "pdf-format-initial.json"
            if not archive.exists():
                e.atomic(archive, existing_pdf.read_bytes())
            e.atomic(existing_pdf, json.dumps(audited, sort_keys=True).encode())
            results = audited
            if set(cases).issubset({x["openalex_id"] for x in audited}):
                return {"pdf_requests": len(audited), "results": audited, "resumed_without_new_requests": True}
        ledger_before = e.sha((root / "snippet-exports.json").read_bytes())
        prior = [json.loads(x) for x in (folder / "probes.jsonl").read_text().splitlines()]
        attemptpath = folder / "pdf-requested-ids.json"
        requested = set(json.loads(attemptpath.read_text())) if attemptpath.exists() else {x["openalex_id"] for x in results}
        for wid in cases:
            if wid in requested:
                continue
            row = rows[wid]
            entitlement = next(x for x in prior if x["openalex_id"] == wid and x["view"] == "ENTITLED" and x["http"] == 200)
            payload = root / entitlement["payload_path"]
            e.check_ancestors(payload)
            data = payload.read_bytes()
            if e.sha(data) != entitlement["payload_sha256"] or error_category(data, 200) != "document_entitled":
                raise ValueError("positive_entitlement_required")
            digest = attempts[wid]["xml_sha256"]
            cached = root / "quarantine" / f"{wid}-{digest}.xml"
            e.check_ancestors(cached)
            data = cached.read_bytes()
            if e.sha(data) != digest:
                raise ValueError("quarantine_checksum_failure")
            xml = xml_root(data)
            dois = {e.norm_doi(n.text) for c in xml if e.local_name(c) == "coredata" for n in c if e.local_name(n) == "doi"}
            if dois != {row["doi"]}:
                raise ValueError("cached_doi_mismatch")
            statepath = root / "rate-state.json"
            state = json.loads(statepath.read_text()) if statepath.exists() else {}
            wait = max(0, state.get("not_before", 0) - time.time())
            if wait > 60:
                raise ValueError("cooldown")
            if wait:
                time.sleep(wait)
            key = e.key_file("elsevier/api_key")
            if not key:
                raise ValueError("key_missing")
            requested.add(wid)
            e.atomic(attemptpath, json.dumps(sorted(requested)).encode())
            code, headers, data = request(row["doi"], None, key, opener, accept="application/pdf")
            e.atomic(statepath, json.dumps({"not_before": time.time() + max(3, e.delay(headers), e.quota_delay(headers)), "reason": "finite_pdf_format_diagnostic"}).encode())
            digest = e.sha(data)
            path = folder / "pdf-candidates" / f"{wid}-{digest}{'.pdf' if data.startswith(b'%PDF-') else '.response'}"
            e.atomic(path, data, 0o400)
            result = {"utc": e.now(), "openalex_id": wid, "doi": row["doi"], "http": code,
                      "content_type": headers.get("content-type", ""), "bytes": len(data), "sha256": digest,
                      "path": str(path.relative_to(root)), "xml_manifest_unchanged": True,
                      "status": "format_or_api_permission_gap", "doi_metadata_verified": True}
            if code == 200 and data.startswith(b"%PDF-"):
                pages = library.pdf_pages(path)
                first = library.pdf_text(path, last_page=1) or ""
                text = library.pdf_text(path) or ""
                score = library.title_match(row["title"], first)
                known = set(re.findall(r"\w+", " ".join(xml.itertext()).lower()))
                novel = len(set(re.findall(r"\w+", text.lower())) - known)
                textpath = path.with_suffix(".txt")
                e.atomic(textpath, text.encode(), 0o400)
                result.update(status="pdf_identity_verified" if pages and score >= 0.8 else "pdf_candidate_identity_unverified",
                              pages=pages, first_page_title_match=score, embedded_doi_present=row["doi"] in first.lower(),
                              words=len(text.split()), novel_tokens_beyond_cached_xml=novel, ocr_needed=len(first.strip()) < 200,
                              body_confidence="substantial_new_text_requires_content_review" if novel >= 100 else "body_not_established",
                              text_path=str(textpath.relative_to(root)), text_sha256=e.sha(text.encode()))
            else:
                result["error_category"] = error_category(data, code)
            results.append(result)
            if e.sha((root / "snippet-exports.json").read_bytes()) != ledger_before:
                raise ValueError("snippet_ledger_changed")
            e.atomic(folder / "pdf-format.json", json.dumps(results, sort_keys=True).encode())
            print(json.dumps(result, sort_keys=True), flush=True)
            if code != 200 or not data.startswith(b"%PDF-") or e.quota_delay(headers):
                break
        audited = audit_pdfs(root, results)
        e.atomic(folder / "pdf-format.json", json.dumps(audited, sort_keys=True).encode())
        return {"pdf_requests": len(audited), "results": audited}


def probe(catalogue, store, ids, views, limit, opener=None):
    if not 1 <= limit <= 187:
        raise ValueError("invalid_limit")
    with e.locked(store) as root:
        _, failures, _ = inputs(catalogue, root)
        selected_ids = Path(ids).read_text().splitlines()
        byid = {r["openalex_id"]: r for r in failures}
        if any(w not in byid for w in selected_ids):
            raise ValueError("id_not_an_existing_failure")
        rows = [byid[w] for w in selected_ids if byid[w]["doi"] != KELLEY][:limit]
        key = e.key_file("elsevier/api_key")
        if not key:
            raise ValueError("key_missing")
        folder = root / SUBDIR
        log = folder / "probes.jsonl"
        done = [json.loads(x) for x in log.read_text().splitlines()] if log.exists() else []
        seen = {(x["openalex_id"], x["view"]) for x in done}
        statepath = root / "rate-state.json"
        state = json.loads(statepath.read_text()) if statepath.exists() else {}
        stop = "complete"
        for row in rows:
            for view in views:
                if (row["openalex_id"], view) in seen:
                    continue
                wait = max(0, float(state.get("not_before", 0)) - time.time())
                if wait > 60:
                    stop = "cooldown"
                    break
                if wait:
                    time.sleep(wait)
                code, headers, data = request(row["doi"], view, key, opener)
                category = error_category(data, code)
                digest = e.sha(data)
                path = folder / "payloads" / f"{row['openalex_id']}-{view}-{digest}.xml"
                e.atomic(path, data, 0o400)
                receipt = {"utc": e.now(), "openalex_id": row["openalex_id"], "doi": row["doi"],
                           "view": view, "http": code, "category": category, "payload_sha256": digest,
                           "payload_path": str(path.relative_to(root))}
                done.append(receipt)
                e.atomic(log, ("\n".join(json.dumps(x, sort_keys=True) for x in done) + "\n").encode())
                state = {"not_before": time.time() + max(3, e.delay(headers), e.quota_delay(headers)), "reason": "diagnosis"}
                e.atomic(statepath, json.dumps(state).encode())
                print(json.dumps({k: receipt[k] for k in ("openalex_id", "view", "http", "category")}), flush=True)
                if code in {403, 429} or e.quota_delay(headers) or code >= 500 or (code == 401 and category != "resource_not_entitled"):
                    stop = f"http_{code}"
                    break
            if stop != "complete":
                break
        return {"stopped": stop, "probe_records": len(done), "counts": dict(collections.Counter(f"{x['view']}:{x['http']}:{x['category']}" for x in done))}


def recover(catalogue, store):
    with e.locked(store) as root:
        _, failures, _ = inputs(catalogue, root)
        receiptpath = root / SUBDIR / "recovery.json"
        previous = json.loads(receiptpath.read_text()) if receiptpath.exists() else {"works": []}
        recovered, rejected = [], []
        ledger_before = e.sha((root / "snippet-exports.json").read_bytes())
        for row in failures:
            if row["failure"] != "metadata_only":
                continue
            wid, digest = row["openalex_id"], row["attempt_sha256"]
            source = root / "quarantine" / f"{wid}-{digest}.xml"
            e.check_ancestors(source)
            data = source.read_bytes()
            if e.sha(data) != digest:
                raise ValueError("quarantine_checksum_failure")
            try:
                text, counts = e.parse_article(data, row["doi"])
            except e.Rejected as err:
                rejected.append({"openalex_id": wid, "outcome": str(err)})
                continue
            if counts["mode"] != "chapter_sections":
                raise ValueError("unexpected_recovery_mode")
            xmlpath, textpath = root / "xml" / f"{wid}.xml", root / "text" / f"{wid}.txt"
            for path, payload in ((xmlpath, data), (textpath, text.encode())):
                if path.exists() and path.read_bytes() != payload:
                    raise ValueError("recovery_path_collision")
                e.atomic(path, payload, 0o400)
            e.append(root / "manifest.tsv", dict(row, utc=e.now(), status="tdm_xml_ok", http=200,
                     xml_path=str(xmlpath.relative_to(root)), xml_sha256=digest, text_path=str(textpath.relative_to(root)),
                     text_sha256=e.sha(text.encode()), bytes=len(data), url=e.API + urllib.parse.quote(row["doi"], safe="") + "?view=FULL",
                     tool_sha256=e.sha(Path(e.__file__).read_bytes()), **counts), e.FIELDS)
            recovered.append(wid)
        if e.sha((root / "snippet-exports.json").read_bytes()) != ledger_before:
            raise ValueError("snippet_ledger_changed")
        all_recovered = sorted(set(previous["works"]) | set(recovered))
        receipt = {"utc": e.now(), "recovered": len(all_recovered), "newly_recovered": len(recovered),
                   "works": all_recovered, "remaining_cached_failures": rejected,
                   "snippet_ledger_sha256": ledger_before, "recovery_tool_sha256": e.sha(Path(__file__).read_bytes())}
        e.atomic(receiptpath, json.dumps(receipt, sort_keys=True).encode())
        return receipt


def summarize(catalogue, store):
    with e.locked(store) as root:
        folder = root / SUBDIR
        initial = json.loads((folder / "classification.json").read_text())
        recovered = set(json.loads((folder / "recovery.json").read_text())["works"])
        pdfpath = folder / "pdf-format.json"
        pdfs = audit_pdfs(root, json.loads(pdfpath.read_text())) if pdfpath.exists() else []
        pdf_recovered = {x["openalex_id"] for x in pdfs if x["status"] == "pdf_recovered_verified_identity_and_pages"}
        probes = [json.loads(x) for x in (folder / "probes.jsonl").read_text().splitlines()]
        entitled = {x["openalex_id"]: x for x in probes if x["view"] == "ENTITLED"}
        for wid, x in entitled.items():
            if x["http"] == 200:
                path = root / x["payload_path"]
                e.check_ancestors(path)
                payload = path.read_bytes()
                if e.sha(payload) != x["payload_sha256"]:
                    raise ValueError("diagnostic_payload_checksum_failure")
                entitled[wid] = dict(x, category=error_category(payload, 200))
        historical = root / "quarantine/kelley-entitled-diagnostic-0.xml"
        historical_receipt = root / "provenance/kelley-entitlement-diagnostic.json"
        e.check_ancestors(historical)
        e.check_ancestors(historical_receipt)
        historical_data = historical.read_bytes() if historical.exists() else b""
        historical_metadata = json.loads(historical_receipt.read_text()) if historical_receipt.exists() else {}
        known_denial = (historical_metadata.get("doi") == KELLEY and historical_metadata.get("entitled_view_status") == 401
                        and error_category(historical_data, 401) == "resource_not_entitled")
        attempts = e.latest(root / "attempts.tsv")
        results = []
        for row in initial["works"]:
            wid = row["openalex_id"]
            x = dict(row)
            probe_result = entitled.get(wid)
            if wid in recovered:
                x.update(category="recovered_chapter_sections", evidence="direct_cached_xml_checksums_and_manifest")
            elif wid in pdf_recovered:
                x.update(category="recovered_pdf_format", evidence="direct_pdf_hash_title_doi_metadata_and_page_coverage")
            elif row["doi"] == KELLEY and known_denial:
                x.update(category="resource_not_entitled", evidence="direct_historical_20261105_entitled_401",
                         diagnostic_payload_sha256=e.sha(historical_data))
            elif row["failure"] == "metadata_only":
                digest = attempts[wid]["xml_sha256"]
                path = root / "quarantine" / f"{wid}-{digest}.xml"
                e.check_ancestors(path)
                payload = path.read_bytes()
                if e.sha(payload) != digest:
                    raise ValueError("quarantine_checksum_failure")
                shape = structure(payload)
                category = "bibliography_backmatter_not_research_body" if shape["front_back_matter"] else "scientific_body_absent_in_returned_xml"
                x.update(category=category, evidence="direct_cached_xml_structure")
            elif probe_result and probe_result["category"] == "resource_not_entitled" and probe_result["http"] == 401:
                x.update(category="resource_not_entitled", evidence="direct_per_work_entitled_401")
            elif probe_result and probe_result["http"] == 404:
                x.update(category="resource_not_found", evidence="direct_per_work_entitled_404")
            elif probe_result:
                x.update(category="unresolved_diagnostic_response", evidence="direct_response_does_not_settle_cause")
            else:
                x.update(category="unresolved_untested", evidence="original_fetch_outcome_only")
            if probe_result:
                x["entitled_http"] = probe_result["http"]
                x["entitled_result"] = probe_result["category"]
                x["diagnostic_payload_sha256"] = probe_result["payload_sha256"]
            results.append(x)
        counts = dict(collections.Counter(x["category"] for x in results))
        batch_xml_held = initial["held"] + len(recovered)
        batch_held = batch_xml_held + len(pdf_recovered)
        store_held = len(e.latest(root / "manifest.tsv"))
        receipt = {"utc": e.now(), "initial_failures": len(results), "category_counts": counts,
                   "core_category_counts": dict(collections.Counter(x["category"] for x in results if x["core"])),
                   "original_batch_selected": initial["held"] + len(results), "original_batch_held": batch_held,
                   "original_batch_xml_held": batch_xml_held, "original_batch_pdf_recovered": len(pdf_recovered),
                   "original_batch_not_held": len(results) - len(recovered) - len(pdf_recovered),
                   "xml_manifest_held": store_held, "store_held_all_formats": store_held + len(pdf_recovered),
                   "additional_held_outside_batch": store_held - batch_xml_held,
                   "probe_records": len(probes), "works": results}
        e.atomic(folder / "diagnosis.json", json.dumps(receipt, sort_keys=True).encode())
        return {k: v for k, v in receipt.items() if k != "works"}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["classify", "probe", "recover", "summarize", "pdf_diagnostic"])
    parser.add_argument("--catalogue", type=Path, required=True)
    parser.add_argument("--store", type=Path, required=True)
    parser.add_argument("--ids", type=Path)
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--views", nargs="+", choices=["FULL", "ENTITLED"], default=["FULL", "ENTITLED"])
    args = parser.parse_args(argv)
    try:
        result = probe(args.catalogue, args.store, args.ids, args.views, args.limit) if args.command == "probe" else globals()[args.command](args.catalogue, args.store)
        print(json.dumps(result, sort_keys=True), flush=True)
        return 0
    except Exception:
        print('{"error":"diagnosis_failed"}', file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
