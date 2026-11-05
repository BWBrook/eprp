import contextlib
import csv
import http.client
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

import elsevier


DOI = "10.1016/j.test.2001.01.001"
BODY = "Synthetic fossil recovery evidence describes marine communities and extinction dynamics. " * 15


def article(doi=DOI, mode="body"):
    return (f'<full-text-retrieval-response xmlns:dc="urn:dc" xmlns:p="urn:prism">'
            f'<coredata><p:doi>{doi}</p:doi><dc:title>Private title must not appear in fetch output</dc:title></coredata>'
            f'<originalText><{mode}><section><para>{BODY}</para><bib-reference>OMITTEDREFERENCE</bib-reference>'
            f'</section></{mode}></originalText></full-text-retrieval-response>').encode()


class Response:
    def __init__(self, data, url, status=200, headers=None):
        self.data, self.url, self.status = data, url, status
        self.headers = headers or {}

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def read(self, count):
        return self.data[:count]

    def geturl(self):
        return self.url


class Opener:
    def __init__(self, replies=None):
        self.calls = []
        self.replies = list(replies or [])

    def open(self, req, timeout):
        self.calls.append(req)
        if self.replies:
            reply = self.replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return Response(reply, req.full_url)
        return Response(article(), req.full_url)


class XMLTests(unittest.TestCase):
    def test_structured_body_excludes_metadata_and_references(self):
        text, counts = elsevier.parse_article(article(), DOI)
        self.assertIn("Synthetic fossil", text)
        self.assertNotIn("Private title", text)
        self.assertNotIn("OMITTEDREFERENCE", text)
        self.assertEqual(counts["bodies"], 1)
        self.assertEqual(counts["sections"], 1)
        self.assertEqual(counts["references"], 1)
        self.assertIn("not_content_verified", counts["completeness"])

    def test_rawtext_is_marked_unsegmented(self):
        _, counts = elsevier.parse_article(article(mode="rawtext"), DOI)
        self.assertEqual(counts["mode"], "rawtext")
        self.assertIn("unsegmented", counts["completeness"])

    def test_rejects_wrong_doi_metadata_only_and_malformed(self):
        for data, expected in [(article("10.1016/wrong"), "doi_mismatch"),
                               (article().split(b"<originalText>")[0] + b"</full-text-retrieval-response>", "metadata_only"),
                               (b"<bad", "malformed_xml"),
                               (b"<service-error/>", "service_error_xml"),
                               (article().replace(BODY.encode(), b"tiny"), "insufficient_body_text")]:
            with self.subTest(expected=expected), self.assertRaisesRegex(elsevier.Rejected, expected):
                elsevier.parse_article(data, DOI)

    def test_rejects_dtd_and_entities_including_utf16(self):
        for data in [b'<!DOCTYPE x SYSTEM "file:///secret">' + article(),
                     b'<!DOCTYPE x [<!ENTITY a "anything">]>' + article(),
                     ('<!DOCTYPE x SYSTEM "file:///secret">' + article().decode()).encode("utf-16")]:
            with self.assertRaisesRegex(elsevier.Rejected, "dtd_or_entity"):
                elsevier.parse_article(data, DOI)

    def test_rejects_oversize(self):
        with patch.object(elsevier, "MAX_BYTES", 30), self.assertRaisesRegex(elsevier.Rejected, "too_large"):
            elsevier.parse_article(article(), DOI)

    def test_credentials_stay_in_header_and_no_redirects(self):
        opener = Opener()
        elsevier.request_article(DOI, "PRIVATEKEY", opener)
        req = opener.calls[0]
        self.assertTrue(req.full_url.startswith("https://api.elsevier.com/"))
        self.assertNotIn("PRIVATEKEY", req.full_url)
        self.assertEqual(req.get_header("X-els-apikey"), "PRIVATEKEY")
        with self.assertRaisesRegex(elsevier.Rejected, "redirect_refused"):
            elsevier.NoRedirect().redirect_request(req, None, 302, "", {}, "https://attacker.invalid/")
        class Redirecting:
            def open(self, req, timeout):
                return Response(article(), "https://attacker.invalid/")
        with self.assertRaisesRegex(elsevier.Rejected, "redirect_refused"):
            elsevier.request_article(DOI, "PRIVATEKEY", Redirecting())


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)
        self.store = self.base / "overlay"
        self.root = self.store / "tdm" / "elsevier"
        self.catalogue = self.base / "works.tsv"
        self.rows = [{"openalex_id": "W1", "doi": DOI, "fulltext": "failed", "tiers": "canon",
                      "first_author": "Synthetic Author", "year": "2001", "venue": "Synthetic Journal"}]
        self.write_catalogue()
        self.receipt = self.base / "receipt.txt"
        self.receipt.write_text("Synthetic explicit user permission for bounded non-commercial snippets.")
        self.receipt.chmod(0o600)
        self.approval = self.base / "approval.json"
        self.approval.write_text(json.dumps({"approved_snippets": True, "receipt_path": str(self.receipt),
                                           "receipt_sha256": elsevier.sha(self.receipt.read_bytes())}))
        self.approval.chmod(0o600)
        self.keypatch = patch.object(elsevier, "key_file", return_value="PRIVATEKEY")
        self.keypatch.start()
        self.sleep = patch.object(elsevier.time, "sleep")
        self.sleep.start()

    def tearDown(self):
        self.sleep.stop()
        self.keypatch.stop()
        self.tmp.cleanup()

    def write_catalogue(self):
        with self.catalogue.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.rows[0]), delimiter="\t")
            writer.writeheader()
            writer.writerows(self.rows)

    def fetch(self, opener=None, **kwargs):
        with contextlib.redirect_stdout(io.StringIO()) as output:
            result = elsevier.fetch(self.catalogue, self.store, opener=opener or Opener(), **kwargs)
        self.assertNotIn("Synthetic fossil", output.getvalue())
        self.assertNotIn("Private title", output.getvalue())
        self.assertNotIn("PRIVATEKEY", output.getvalue())
        return result

    def query(self, **kwargs):
        return elsevier.query(self.catalogue, self.store, DOI, "recovery", self.approval, **kwargs)

    def expire_pacing(self):
        (self.root / "rate-state.json").write_text('{"not_before":0}')

    def test_fetch_resume_immutable_raw_and_permissions(self):
        opener = Opener()
        self.assertEqual(self.fetch(opener)["fetched"], 1)
        self.assertEqual(self.fetch(opener)["held"], 1)
        self.assertEqual(len(opener.calls), 1)
        self.assertEqual((self.root / "xml/W1.xml").read_bytes(), article())
        for path in [self.root, self.root / "xml", self.root / "text"]:
            self.assertEqual(path.stat().st_mode & 0o077, 0)
        for path in [self.root / "xml/W1.xml", self.root / "text/W1.txt", self.root / "manifest.tsv"]:
            self.assertEqual(path.stat().st_mode & 0o077, 0)
        self.assertFalse((self.store / "manifest.tsv").exists())

    def test_corrupt_held_hash_fails_without_request(self):
        self.fetch()
        path = self.root / "text/W1.txt"
        path.chmod(0o600)
        path.write_text("corruption")
        opener = Opener()
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.fetch(opener)
        self.assertEqual(len(opener.calls), 0)
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.query()

    def test_404_skipped_unless_retry_requested(self):
        opener = Opener([urllib.error.HTTPError("https://api.elsevier.com/", 404, "missing", {}, None)])
        self.assertEqual(self.fetch(opener)["rejected"], 1)
        self.assertEqual(self.fetch(opener)["skipped_failed"], 1)
        self.expire_pacing()
        self.assertEqual(self.fetch(opener, retry_failed=True)["fetched"], 1)

    def test_rejected_xml_is_quarantined_with_original_hash(self):
        bad = article("10.1016/wrong")
        self.fetch(Opener([bad]))
        paths = list((self.root / "quarantine").glob("*.xml"))
        self.assertEqual(len(paths), 1)
        self.assertEqual(paths[0].read_bytes(), bad)
        self.assertFalse((self.root / "manifest.tsv").exists())

    def test_stop_429_and_durable_retry_after(self):
        self.rows.append(dict(self.rows[0], openalex_id="W2", doi="10.1016/next"))
        self.write_catalogue()
        opener = Opener([urllib.error.HTTPError("https://api.elsevier.com/", 429, "limited",
                                               {"Retry-After": "120"}, None)])
        self.assertEqual(self.fetch(opener)["stopped"], "http_429")
        self.assertEqual(len(opener.calls), 1)
        self.assertEqual(self.fetch(opener)["stopped"], "cooldown")
        self.assertEqual(len(opener.calls), 1)
        state = json.loads((self.root / "rate-state.json").read_text())
        self.assertGreater(state["not_before"], elsevier.time.time() + 115)

    def test_stop_auth_and_exhausted_quota(self):
        for status in [401, 403]:
            if (self.root / "rate-state.json").exists():
                self.expire_pacing()
            opener = Opener([urllib.error.HTTPError("https://api.elsevier.com/", status, "refusal", {}, None)])
            self.assertEqual(self.fetch(opener)["stopped"], f"http_{status}")
        class Quota:
            def open(inner, req, timeout):
                return Response(article(), req.full_url, headers={"X-RateLimit-Remaining": "0"})
        self.expire_pacing()
        self.assertEqual(self.fetch(Quota())["stopped"], "quota_exhausted")

    def test_core_priority_open_skip_rejected_skip_and_explicit_doi(self):
        self.rows = [dict(self.rows[0], openalex_id="W2", doi="10.1006/second", tiers="field-test"),
                     self.rows[0], dict(self.rows[0], openalex_id="W3", doi="10.1016/open", fulltext="ok"),
                     dict(self.rows[0], openalex_id="W4", doi="10.1016/rejected", fulltext="withdrawn"),
                     dict(self.rows[0], openalex_id="W5", doi="10.1530/not-assumed"),
                     dict(self.rows[0], openalex_id="W6", doi="10.1016/unsupported-type", fulltext="skipped_type")]
        self.write_catalogue()
        self.assertEqual([r["openalex_id"] for r in elsevier.candidates(self.catalogue)], ["W1", "W2"])
        self.assertEqual([r["openalex_id"] for r in elsevier.candidates(self.catalogue, dois=["10.1530/not-assumed"])], ["W5"])
        priority = self.base / "priority.txt"
        priority.write_text("W2\n")
        self.assertEqual(elsevier.candidates(self.catalogue, ids=priority)[0]["openalex_id"], "W2")

    def test_query_cumulative_budget_across_calls_and_new_approval(self):
        self.fetch()
        first = self.query(chars=80)
        second = self.query(chars=80)
        third = self.query(chars=80)
        self.assertEqual([x["excerpt_chars"] for x in [first, second, third]], [80, 80, 40])
        self.assertEqual(self.query()["status"], "budget_exhausted")
        self.assertEqual(sum(x["excerpt_chars"] for x in [first, second, third]), 200)
        self.assertIn("https://doi.org/", first["url"])
        self.assertIn("Synthetic Author", first["credit"])
        self.assertIn("non-commercial", first["notice"])
        self.assertNotIn("excerpt", (self.root / "snippet-exports.json").read_text().replace("last_excerpt_sha256", "hash"))
        self.approval.write_text(json.dumps({"approved_snippets": True, "receipt_path": str(self.receipt),
                                           "receipt_sha256": elsevier.sha(self.receipt.read_bytes()), "new": True}))
        self.assertEqual(self.query()["status"], "budget_exhausted")

    def test_query_fail_closed_missing_or_unapproved_receipt_or_ledger(self):
        self.fetch()
        self.receipt.write_text("modified")
        with self.assertRaisesRegex(ValueError, "checksum"):
            self.query()
        self.approval.write_text(json.dumps({"approved_snippets": False, "receipt_sha256": "0" * 64}))
        with self.assertRaisesRegex(ValueError, "not_approved"):
            self.query()
        self.approval.write_text(json.dumps({"approved_snippets": True, "receipt_path": str(self.receipt),
                                           "receipt_sha256": elsevier.sha(self.receipt.read_bytes())}))
        (self.root / "snippet-exports.json").unlink()
        with self.assertRaisesRegex(ValueError, "ledger_missing"):
            self.query()

    def test_query_no_match_spends_no_budget(self):
        self.fetch()
        result = elsevier.query(self.catalogue, self.store, DOI, "NEVERMATCHED", self.approval)
        self.assertEqual(result["status"], "no_match")
        self.assertEqual(self.query()["excerpt_chars"], 200)

    def test_query_rejects_catalogue_doi_change_without_spending_budget(self):
        self.fetch()
        self.query(chars=80)
        ledger = self.root / "snippet-exports.json"
        before = ledger.read_bytes()
        changed = "10.1016/j.changed.2002.02.002"
        self.rows[0]["doi"] = changed
        self.write_catalogue()
        with self.assertRaisesRegex(ValueError, "held_doi_changed"):
            elsevier.query(self.catalogue, self.store, changed, "recovery", self.approval)
        self.assertEqual(ledger.read_bytes(), before)

    def test_bad_status_line_never_reaches_output(self):
        marker = "LICENSED_SERVER_STATUSLINE_MARKER"
        opener = Opener([http.client.BadStatusLine(marker)])
        output, errors = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            result = elsevier.fetch(self.catalogue, self.store, opener=opener)
        self.assertEqual(result["stopped"], "transport_error")
        self.assertNotIn(marker, output.getvalue() + errors.getvalue())
        self.assertNotIn(marker, (self.root / "attempts.tsv").read_text())
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(elsevier, "fetch", side_effect=RuntimeError(marker)):
            with contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
                code = elsevier.main(["fetch", "--catalogue", str(self.catalogue), "--store", str(self.store)])
        self.assertEqual(code, 1)
        self.assertEqual(json.loads(errors.getvalue()), {"error": "operation_failed", "command": "fetch"})
        self.assertNotIn(marker, output.getvalue() + errors.getvalue())

    def test_concurrent_writer_refused(self):
        with elsevier.locked(self.store):
            with self.assertRaises(BlockingIOError):
                self.fetch()

    def test_store_ancestor_symlink_rejected_before_writes(self):
        outside = self.base / "outside"
        outside.mkdir()
        linked = self.base / "linked"
        linked.symlink_to(outside, target_is_directory=True)
        opener = Opener()
        with self.assertRaisesRegex(ValueError, "restricted_path_symlink"):
            elsevier.fetch(self.catalogue, linked / "overlay", opener=opener)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertEqual(len(opener.calls), 0)

    def test_text_directory_symlink_rejected_without_export(self):
        self.fetch()
        ledger = self.root / "snippet-exports.json"
        before = ledger.read_bytes()
        texts = self.root / "text"
        outside = self.base / "external-text"
        texts.rename(outside)
        texts.symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "restricted_path_symlink"):
            self.query()
        self.assertEqual(ledger.read_bytes(), before)

    def test_normal_pacing_persists_across_limit_resume(self):
        second = "10.1016/next"
        self.rows.append(dict(self.rows[0], openalex_id="W2", doi=second))
        self.write_catalogue()
        opener = Opener([article(), article(second)])
        with patch.object(elsevier.time, "time", return_value=1000.0):
            self.assertEqual(self.fetch(opener, limit=1)["fetched"], 1)
            self.assertEqual(self.fetch(opener, limit=1)["stopped"], "cooldown")
            state = json.loads((self.root / "rate-state.json").read_text())
            self.assertGreaterEqual(state["not_before"], 1003.0)
        self.assertEqual(len(opener.calls), 1)
        with patch.object(elsevier.time, "time", return_value=1003.1):
            self.assertEqual(self.fetch(opener, limit=1)["fetched"], 1)
        self.assertEqual(len(opener.calls), 2)


if __name__ == "__main__":
    unittest.main()
