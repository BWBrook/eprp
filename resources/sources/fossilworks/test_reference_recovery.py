import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import reference_recovery as recovery


def page(ref_no="3996", samples=("4412",)):
    links = "".join('<a href="?a=sampleResults&amp;sample_no=' + sample + '">S</a>' for sample in samples)
    return ('<div id="mainPanel"><div class="title">Full citation</div><div>'
            '<div>A. Author and B. Coauthor. 2001. A fossil study. <i>Journal</i> '
            '<b>2</b>:3-8 [ER ' + ref_no + ']</div>'
            '<div>Contributed by Contributor, entered by Enterer on 2026-01-01</div>'
            '<div>Samples: ' + links + '</div></div></div>').encode()


class RecoveryTests(unittest.TestCase):
    def test_collector_omits_cookie_headers_from_receipts(self):
        response = mock.MagicMock()
        response.__enter__.return_value = response
        response.status = 200
        response.url = recovery.BASE + "?a=getRefs&ref_no=3996"
        response.headers = {"Set-Cookie": "anonymous-token=example", "sEt-CoOkIe": "other=example",
                            "Content-Type": "text/html"}
        response.read.return_value = page()
        inputs = {"missing_references": [{"ref_no": "3996", "sample_ids": ["4412"]}]}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            input_path = root / "input.json"
            input_path.write_text("{}")
            evidence = root / "evidence"
            with mock.patch.object(recovery, "read_input", return_value=inputs), \
                    mock.patch.object(recovery, "urlopen", return_value=response):
                recovery.collect(input_path, evidence)
            receipt = json.loads((evidence / "receipt-3996.json").read_text())
            manifest = json.loads((evidence / "manifest.json").read_text())
            self.assertEqual(receipt["response_headers"], {"Content-Type": "text/html"})
            self.assertEqual(manifest["receipts"][0]["response_headers"], {"Content-Type": "text/html"})

    def test_exact_id_and_expected_samples_recovered(self):
        result = recovery.parse_reference(page(), "3996", ["4412"])
        self.assertEqual(result["status"], "provider_metadata_recovered")
        self.assertIn("Journal 2:3-8 [ER 3996]", result["provider_citation"])
        self.assertEqual(result["external_bibliographic_verification"], "not_performed")

    def test_wrong_provider_id_stays_unresolved(self):
        result = recovery.parse_reference(page("4010"), "3996", ["4412"])
        self.assertEqual(result["status"], "unresolved_no_unique_exact_id")
        self.assertIsNone(result["provider_citation"])

    def test_duplicate_citations_stay_unresolved(self):
        result = recovery.parse_reference(page() + page(), "3996", ["4412"])
        self.assertEqual(result["status"], "unresolved_no_unique_exact_id")

    def test_sample_links_are_explicit_checks(self):
        result = recovery.parse_reference(page(samples=("4413",)), "3996", ["4412"])
        self.assertEqual(result["status"], "exact_id_sample_link_discrepancy")
        self.assertEqual(result["expected_sample_ids_missing_on_page"], ["4412"])

    def test_login_error_page_cannot_be_recovered(self):
        result = recovery.parse_reference(b"<div>Please log in</div>", "3996", ["4412"])
        self.assertEqual(result["status"], "unresolved_no_unique_exact_id")

    def test_sample_page_requires_explicit_identity(self):
        body = page(samples=()).replace(b"A. Author", b"Reference: A. Author")
        result = recovery.parse_reference(body, "3996", ["4412"], "4412")
        self.assertEqual(result["status"], "unresolved_no_unique_exact_id")
        body += b"<div><b>Sample no</b>: 4412</div>"
        result = recovery.parse_reference(body, "3996", ["4412"], "4412")
        self.assertEqual(result["status"], "provider_metadata_recovered")
        self.assertFalse(result["provider_citation"].startswith("Reference:"))

    def test_incorrect_database_is_rejected_without_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "wrong.sqlite"
            path.write_bytes(b"not the original database")
            before = path.read_bytes()
            with self.assertRaisesRegex(ValueError, "pinned"):
                recovery.extract_input(path)
            self.assertEqual(path.read_bytes(), before)

    def test_output_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "output.json"
            recovery.write_new(path, {"original": True})
            with self.assertRaises(FileExistsError):
                recovery.write_new(path, {"original": False})
            self.assertEqual(json.loads(path.read_text()), {"original": True})

    def test_retained_evidence_build_and_mutations(self):
        profile = Path(__file__).parent / "profile"
        input_path = profile / "reference-recovery-input-2026-10-28.json"
        evidence = profile / "reference-recovery-evidence-2026-10-28"
        if not (evidence / "manifest.json").exists():
            self.skipTest("Retained acquisition has not completed")
        result = recovery.build(input_path, evidence)
        self.assertEqual(len(result["references"]), 58)
        self.assertEqual(sum(r["affected_register_rows"] for r in result["references"]), 1266)
        supplement = profile / "reference-recovery-supplement-2026-10-28"
        if (supplement / "manifest.json").exists():
            result = recovery.build(input_path, evidence, supplement)
            self.assertEqual(result["counts"], {"provider_metadata_recovered": 58})
            entry = next(r for r in result["references"] if r["ref_no"] == "4414")
            self.assertIn("Christophel", entry["provider_citation"])
            self.assertEqual(entry["initial_reference_page_result"]["status"], "unresolved_no_unique_exact_id")
        with tempfile.TemporaryDirectory() as directory:
            destination = Path(directory)
            for source in evidence.iterdir():
                (destination / source.name).write_bytes(source.read_bytes())
            manifest_path = destination / "manifest.json"
            manifest = json.loads(manifest_path.read_text())
            broken = copy.deepcopy(manifest)
            broken["input_sha256"] = "0" * 64
            manifest_path.write_text(json.dumps(broken))
            with self.assertRaisesRegex(ValueError, "Input does not match"):
                recovery.build(input_path, destination)
            manifest_path.write_text(json.dumps(manifest))
            body = destination / manifest["receipts"][0]["body_file"]
            body.write_bytes(body.read_bytes() + b"alteration")
            with self.assertRaisesRegex(ValueError, "hash/size mismatch"):
                recovery.build(input_path, destination)


if __name__ == "__main__":
    unittest.main()
