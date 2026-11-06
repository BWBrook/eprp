import contextlib
import csv
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import diagnose_elsevier as d
import elsevier as e

DOI = "10.1016/b978-0-12-000001-1.00001-1"
BODY = "Synthetic chapter body describes fossil evidence and recovery patterns. " * 30


def chapter(doi=DOI):
    return (f'<full-text-retrieval-response><coredata><doi>{doi}</doi></coredata><originalText>'
            f'<doc><nonserial-item><chapter><head>HEADSECRET</head><sections><section><para>{BODY}</para>'
            f'</section></sections><bibliography>REFSECRET</bibliography></chapter></nonserial-item></doc>'
            f'</originalText></full-text-retrieval-response>').encode()


class DiagnosisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.base = Path(self.temp.name)
        self.store = self.base / "store"
        self.root = self.store / "tdm/elsevier"
        self.catalogue = self.base / "catalogue.tsv"
        self.ids = self.base / "ids.txt"
        self.ids.write_text("W1\n")
        self.row = {"openalex_id": "W1", "doi": DOI, "year": "2020", "type": "book-chapter",
                    "venue": "Synthetic Venue", "tiers": "canon", "fulltext": "failed"}
        with self.catalogue.open("w") as f:
            w = csv.DictWriter(f, list(self.row), delimiter="\t")
            w.writeheader()
            w.writerow(self.row)
        with e.locked(self.store):
            data = chapter()
            digest = e.sha(data)
            e.atomic(self.root / "quarantine" / f"W1-{digest}.xml", data, 0o400)
            e.append(self.root / "attempts.tsv", dict(self.row, utc=e.now(), status="metadata_only", http=200,
                     bytes=len(data), xml_sha256=digest), e.ATTEMPT_FIELDS)
            e.atomic(self.root / "snippet-exports.json", b'{"version":1,"exports":{"other":{"chars":200}}}')

    def tearDown(self):
        self.temp.cleanup()

    def test_classify_is_metadata_only_and_labels_cached_structure(self):
        result = d.classify(self.catalogue, self.store)
        self.assertEqual(result["counts"]["category"], {"chapter_selector_omission": 1})
        self.assertEqual(result["core_failed"], 1)
        self.assertNotIn("Synthetic chapter body", json.dumps(result))

    def test_recover_preserves_xml_attempts_and_snippet_ledger(self):
        before = (self.root / "attempts.tsv").read_bytes()
        ledger = (self.root / "snippet-exports.json").read_bytes()
        receipt = d.recover(self.catalogue, self.store)
        self.assertEqual(receipt["recovered"], 1)
        self.assertEqual((self.root / "xml/W1.xml").read_bytes(), chapter())
        text = (self.root / "text/W1.txt").read_text()
        self.assertIn("Synthetic chapter body", text)
        self.assertNotIn("HEADSECRET", text)
        self.assertNotIn("REFSECRET", text)
        self.assertEqual((self.root / "attempts.tsv").read_bytes(), before)
        self.assertEqual((self.root / "snippet-exports.json").read_bytes(), ledger)
        self.assertEqual(e.latest(self.root / "manifest.tsv")["W1"]["mode"], "chapter_sections")
        repeated = d.recover(self.catalogue, self.store)
        self.assertEqual(repeated["newly_recovered"], 0)
        self.assertEqual(repeated["recovered"], 1)

    def test_summary_preserves_initial_denominator_and_direct_recovery_grade(self):
        d.classify(self.catalogue, self.store)
        d.recover(self.catalogue, self.store)
        d.recover(self.catalogue, self.store)
        self.assertEqual(d.classify(self.catalogue, self.store)["failures"], 1)
        e.atomic(self.root / d.SUBDIR / "probes.jsonl", b"")
        result = d.summarize(self.catalogue, self.store)
        self.assertEqual(result["initial_failures"], 1)
        self.assertEqual(result["category_counts"], {"recovered_chapter_sections": 1})

    def test_recovery_rejects_corrupt_cache(self):
        path = next((self.root / "quarantine").glob("*.xml"))
        path.chmod(0o600)
        path.write_bytes(b"corrupt")
        with self.assertRaisesRegex(ValueError, "checksum"):
            d.recover(self.catalogue, self.store)
        self.assertFalse((self.root / "manifest.tsv").exists())

    def test_error_categories_never_export_server_text(self):
        for message, code, category in [("Requestor is not entitled to the resource", 401, "resource_not_entitled"),
                                        ("View parameter specified in request is not valid", 400, "view_invalid"),
                                        ("APIKey is invalid", 401, "credential_error")]:
            payload = f"<service-error><statusText>{message}</statusText></service-error>".encode()
            self.assertEqual(d.error_category(payload, code), category)
        self.assertEqual(d.error_category(b"<document-entitlement><status>ENTITLED</status><message>Requestor is entitled to the requested resource</message></document-entitlement>", 200), "document_entitled")

    def test_probe_stops_credentials_and_does_not_print_payload(self):
        payload = b"<service-error><statusText>APIKey invalid SECRETERROR</statusText></service-error>"
        with patch.object(d.e, "key_file", return_value="PRIVATEKEY"), patch.object(d, "request", return_value=(401, {}, payload)):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                result = d.probe(self.catalogue, self.store, self.ids, ["ENTITLED"], 12)
        self.assertEqual(result["stopped"], "http_401")
        self.assertNotIn("SECRETERROR", output.getvalue())
        self.assertNotIn("PRIVATEKEY", output.getvalue())
        self.assertNotIn("SECRETERROR", (self.root / d.SUBDIR / "probes.jsonl").read_text())

    def test_resource_denial_is_classified_without_bypassing_entitlement(self):
        payload = b"<service-error><statusText>Requestor is not entitled to the resource</statusText></service-error>"
        with patch.object(d.e, "key_file", return_value="PRIVATEKEY"), patch.object(d, "request", return_value=(401, {}, payload)) as request:
            with contextlib.redirect_stdout(io.StringIO()):
                result = d.probe(self.catalogue, self.store, self.ids, ["ENTITLED"], 12)
        self.assertEqual(result["stopped"], "complete")
        self.assertEqual(request.call_count, 1)
        self.assertIn("ENTITLED:401:resource_not_entitled", result["counts"])

    def test_unknown_id_and_malicious_xml_refused(self):
        self.ids.write_text("W999\n")
        with self.assertRaisesRegex(ValueError, "existing_failure"):
            d.probe(self.catalogue, self.store, self.ids, ["FULL"], 12)
        with self.assertRaisesRegex(ValueError, "unsafe_xml"):
            d.structure(b'<!DOCTYPE x SYSTEM "file:///secret"><x/>')

    def test_cli_sanitizes_unexpected_exceptions(self):
        with patch.object(d, "classify", side_effect=RuntimeError("SECRETPAYLOAD")):
            with contextlib.redirect_stderr(io.StringIO()) as errors:
                code = d.main(["classify", "--catalogue", str(self.catalogue), "--store", str(self.store)])
        self.assertEqual(code, 1)
        self.assertNotIn("SECRETPAYLOAD", errors.getvalue())

    def test_pdf_request_uses_official_host_header_and_no_view_or_redirect(self):
        class Response:
            code = 200
            headers = {"Content-Type": "application/pdf"}
            def __init__(self, url):
                self.url = url
            def __enter__(self):
                return self
            def __exit__(self, *args):
                pass
            def geturl(self):
                return self.url
            def read(self, cap):
                return b"%PDF-synthetic"
        class Opener:
            redirect = False
            def open(self, req, timeout):
                self.req = req
                return Response("https://other.invalid/paper" if self.redirect else req.full_url)
        opener = Opener()
        code, _, data = d.request(DOI, None, "PRIVATEKEY", opener, accept="application/pdf")
        self.assertEqual(code, 200)
        self.assertEqual(data, b"%PDF-synthetic")
        self.assertTrue(opener.req.full_url.startswith("https://api.elsevier.com/"))
        self.assertNotIn("view=", opener.req.full_url)
        self.assertNotIn("PRIVATEKEY", opener.req.full_url)
        self.assertEqual(opener.req.get_header("Accept"), "application/pdf")
        opener.redirect = True
        with self.assertRaisesRegex(e.Rejected, "redirect_refused"):
            d.request(DOI, None, "PRIVATEKEY", opener, accept="application/pdf")

    def test_pdf_first_page_preview_is_not_full_recovery(self):
        result = {"pages": 1, "first_page_title_match": 1.0, "novel_tokens_beyond_cached_xml": 110,
                  "status": "pdf_identity_verified"}
        preview = d.pdf_coverage(result, 11)
        self.assertEqual(preview["status"], "pdf_incomplete_preview")
        self.assertEqual(preview["body_confidence"], "incomplete_page_coverage")
        full = d.pdf_coverage(dict(result, pages=18, novel_tokens_beyond_cached_xml=1780), 18)
        self.assertEqual(full["status"], "pdf_recovered_verified_identity_and_pages")
        unknown = d.pdf_coverage(result, 0)
        self.assertNotEqual(unknown["status"], "pdf_recovered_verified_identity_and_pages")


if __name__ == "__main__":
    unittest.main()
