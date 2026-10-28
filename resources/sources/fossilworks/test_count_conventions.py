import csv
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock

import count_conventions as cc


def row(comment="", row_id="r1", count="7"):
    return {"_fw_row_id": row_id, "_fw_interval_id": "i1", "sample no": "s1",
            "ref no": "ref1", "count": count, "comments": comment}


class EvidenceTests(unittest.TestCase):
    def test_incidental_mni_does_not_assign_unit(self):
        annotation = cc.annotate(row("plus many fragments: MNI 2", count="257"), {})
        self.assertEqual(annotation["count_unit"], "unknown")
        self.assertEqual(annotation["count_raw"], "257")
        self.assertIn("mni_mention", json.loads(annotation["flags"]))

    def test_minimum_is_not_minimum_individuals(self):
        for comment in ["minimum count", "minimum number of maxillae", "MNI",
                        '"or juvenile individuals of Mimomys"']:
            self.assertEqual(cc.annotate(row(comment), {})["count_unit"], "unknown")

    def test_whole_tokens_and_exact_spans(self):
        comment = '"omnivore": MNI based on jaw fragments'
        spans = cc.evidence_spans(comment)
        self.assertEqual(sum(e["flag"] == "mni_mention" for e in spans), 1)
        for span in spans:
            self.assertEqual(comment[span["start"]:span["end"]], span["text"])

    def test_review_guard_rejects_changed_evidence(self):
        review = {"rows": [{"row_id": "r1", "expected": {"comments": "MNI"}}]}
        with self.assertRaisesRegex(ValueError, "guard"):
            cc.checked_reviews([row("MNI 2")], review)

    def test_review_guard_rejects_missing_or_duplicate_row(self):
        item = {"row_id": "r1", "expected": {"comments": "MNI"}}
        for source, items in [([], [item]), ([row("MNI")], [item, item])]:
            with self.assertRaises(ValueError):
                cc.checked_reviews(source, {"rows": items})

    def test_review_does_not_propagate_to_other_rows(self):
        review = {"r1": {"unit": "minimum_individuals", "level": "provider_comment_reviewed",
                         "review_id": "C1"}}
        self.assertEqual(cc.annotate(row("MNI"), review)["count_unit"], "minimum_individuals")
        self.assertEqual(cc.annotate(row("", "r2"), review)["count_unit"], "unknown")

    def test_derived_tsv_roundtrips_literal_quotes(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "overlay.tsv"
            original = {"comment": '"taxon": MNI based on "jaw fragments"', "count": "007"}
            cc.write_tsv(path, [original])
            with path.open(newline="") as stream:
                self.assertEqual(list(csv.DictReader(stream, delimiter="\t")), [original])

    def test_end_to_end_keeps_duplicates_counts_and_input_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            db, rev = temp / "source.sqlite", temp / "review.json"
            con = sqlite3.connect(db)
            con.execute('CREATE TABLE register_rows (_fw_row_id,_fw_interval_id,"sample no","ref no",count,comments)')
            con.executemany("INSERT INTO register_rows VALUES (?,?,?,?,?,?)",
                            [tuple(row("MNI", "r1").values()), tuple(row("", "r2", "29").values())])
            con.execute('CREATE TABLE samples_rows (_fw_row_id,_fw_interval_id,"sample no","sample name","ref no","taphonomic context",preservation,archaeology,"sampling methods")')
            con.executemany("INSERT INTO samples_rows VALUES (?,?,?,?,?,?,?,?,?)",
                            [(i, "i1", "s1", "a", "ref1", "cave", "", "", "quarry") for i in ["s1a", "s1b"]])
            con.commit()
            con.close()
            before = cc.digest(db)
            rev.write_text(json.dumps({"assembly_sha256": before, "rows": [{"row_id": "r1",
                "expected": {"count": "7", "comments": "MNI"}, "unit": "minimum_individuals",
                "level": "provider_comment_reviewed", "review_id": "C1"}]}))
            summary = cc.build(db, temp / "output", rev)
            self.assertEqual(summary["register_rows"], 2)
            self.assertEqual(summary["sample_source_rows"], 2)
            self.assertEqual(summary["distinct_interval_sample_keys"], 1)
            self.assertEqual(summary["unit_counts"], {"minimum_individuals": 1, "unknown": 1})
            self.assertEqual(cc.digest(db), before)
            text = (temp / "output/register-count-evidence.tsv").read_text()
            self.assertIn("29", text)
            with self.assertRaises(FileExistsError):
                cc.build(db, temp / "output", rev)
            invalid_review = json.loads(rev.read_text())
            invalid_review["rows"][0]["expected"]["comments"] = "changed"
            rev.write_text(json.dumps(invalid_review))
            observed = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True)
            with mock.patch.object(cc.sqlite3, "connect", return_value=observed):
                with self.assertRaisesRegex(ValueError, "guard"):
                    cc.build(db, temp / "invalid-review-output", rev)
            with self.assertRaises(sqlite3.ProgrammingError):
                observed.execute("SELECT 1")
            rev.write_text(json.dumps({"assembly_sha256": "bad", "rows": []}))
            with self.assertRaisesRegex(ValueError, "SHA256"):
                cc.build(db, temp / "new-output", rev)
            self.assertFalse((temp / "new-output").exists())


if __name__ == "__main__":
    unittest.main()
