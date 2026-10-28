from contextlib import closing
import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest.mock import patch

import build_annotations as ba
import count_conventions as cc


class AnnotationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.database = self.root / "assembly.sqlite"
        self.profile = self.root / "profile"
        self.profile.mkdir()
        self.destination = self.root / "annotations.sqlite"
        self.paths = ba.input_paths(self.profile)
        con = self.enterContext(closing(sqlite3.connect(self.database)))
        register_fields = list(ba.REGISTER_FIELDS.values())
        sample_fields = list(ba.SAMPLE_FIELDS.values())
        quote = lambda value: '"' + value.replace('"', '""') + '"'
        for table, fields in [("register_rows", register_fields), ("samples_rows", sample_fields)]:
            con.execute(f"CREATE TABLE {table} ({','.join(quote(k) + ' TEXT' for k in fields)})")
        for number, ref, sample in [(1, "3996", "s1"), (2, "4030", "s1"),
                                    (3, "4414", "s2"), (4, "existing", "s1")]:
            con.execute("INSERT INTO register_rows VALUES (?,?,?,?,?,?,?,?,?)",
                        (f"r{number}", "i1", sample, ref, '"Original genus"', "sp.",
                         "ungulates", "007", 'MNI 2; "original comments"' if number == 1 else ""))
        for row_id, sample in [("sa", "s1"), ("sb", "s1"), ("sc", "s2")]:
            con.execute("INSERT INTO samples_rows VALUES (?,?,?,?,?,?,?,?,?)",
                        (row_id, "i1", sample, "original sample", "3996", "cave", "", "", "dry sieving"))
        con.execute("CREATE VIEW register_linked AS SELECT *, CASE WHEN \"ref no\"='existing' THEN 'resolved' ELSE 'unresolved' END AS _fw_reference_status FROM register_rows")
        con.commit()
        con.close()
        self.base_hash = ba.digest(self.database)
        review = {"assembly_sha256": self.base_hash, "rows": [{"row_id": "r1",
            "expected": {"count": "007", "comments": 'MNI 2; "original comments"'},
            "unit": "minimum_individuals", "level": "provider_comment_reviewed", "review_id": "C1",
            "issues": [{"kind": "illustrative", "source_value": 2}]}]}
        self.paths["count_review"].write_text(json.dumps(review))
        cc.build(self.database, self.paths["count_summary"].parent, self.paths["count_review"])
        references = []
        for ref, sample in [("3996", "s1"), ("4030", "s1"), ("4414", "s2")]:
            references.append({"ref_no": ref, "provider_citation": f"Exact provider punctuation. 2015 [ER {ref}]",
                "status": "provider_metadata_recovered", "affected_register_rows": 1,
                "affected_sample_ids": [sample], "provider_sample_ids": [sample],
                "expected_sample_ids_missing_on_page": [],
                "source": {"ref_no": ref, "sha256": "original evidence digest", "body_file": f"ref-{ref}.html"},
                "source_collection": "supplemental_sample_page" if ref == "4414" else "initial_reference_pages"})
        self.paths["reference_recovery"].write_text(json.dumps({"database_sha256": self.base_hash,
            "counts": {"provider_metadata_recovered": 3}, "references": references}))
        self.paths["bibliographic_checks"].write_text(json.dumps({"checks": [
            {"ref_no": r, "status": "selected_check", "unmodified_evidence": {"year": 2024}}
            for r in ("3996", "4030", "4414")]}))
        self.constants = patch.multiple(ba, BASE_SHA256=self.base_hash,
            EXPECTED_COHORT=(3, 3, 2), EXPECTED_SOURCE_ROWS=(4, 3, 2))
        self.constants.start()
        self.addCleanup(self.constants.stop)

    def hashes(self):
        return {key: ba.digest(path) for key, path in self.paths.items()}

    def build(self, hashes=None):
        return ba.build(self.database, self.profile, self.destination, hashes or self.hashes())

    def change_json(self, label, mutation):
        value = json.loads(self.paths[label].read_text())
        mutation(value)
        self.paths[label].write_text(json.dumps(value))

    def change_rows(self, label, mutation):
        rows = ba.read_tsv(self.paths[label].read_bytes())
        mutation(rows)
        cc.write_tsv(self.paths[label], rows)
        name = self.paths[label].name
        self.change_json("count_summary", lambda value: value["outputs"].update({name: {
            "sha256": ba.digest(self.paths[label]), "bytes": self.paths[label].stat().st_size}}))

    def assert_rejected(self, pattern):
        with self.assertRaisesRegex(ValueError, pattern):
            self.build()
        self.assertFalse(self.destination.exists())
        self.assertEqual(list(self.root.glob(".annotations-*")), [])
        self.assertEqual(ba.digest(self.database), self.base_hash)

    def test_end_to_end_preserves_values_evidence_and_cardinality(self):
        hashes = self.hashes()
        result = self.build(hashes)
        self.assertEqual(result["sidecar_sha256"], ba.digest(self.destination))
        self.assertEqual(ba.digest(self.database), self.base_hash)
        self.assertEqual(self.hashes(), hashes)
        with closing(sqlite3.connect(self.destination)) as con:
            self.assertEqual(con.execute("PRAGMA integrity_check").fetchone(), ("ok",))
            documents = con.execute("SELECT label,sha256,content FROM input_documents").fetchall()
            for label, digest, data in documents:
                self.assertEqual(data, self.paths[label].read_bytes())
                self.assertEqual(digest, hashes[label])
            self.assertEqual(len(documents), 6)
            self.assertEqual(con.execute("SELECT count_raw,count_unit FROM register_count_evidence WHERE row_id='r1'").fetchone(), ("007", "minimum_individuals"))
            self.assertEqual(con.execute("SELECT count_unit FROM register_count_evidence WHERE row_id='r2'").fetchone(), ("unknown",))
            recovery = con.execute("SELECT provider_citation,evidence_json FROM reference_recovery WHERE ref_no='4414'").fetchone()
            self.assertEqual(recovery[0], "Exact provider punctuation. 2015 [ER 4414]")
            self.assertEqual(json.loads(recovery[1])["source_collection"], "supplemental_sample_page")
            self.assertEqual(con.execute("SELECT count(*) FROM bibliographic_checks").fetchone(), (3,))
            self.assertEqual(con.execute("SELECT name FROM suggested_queries").fetchone(), ("attach_and_join",))
        with closing(sqlite3.connect(self.database.as_uri() + "?mode=ro", uri=True)) as con:
            suggested = ba.JOIN_QUERIES.replace("/absolute/path/annotations.sqlite", str(self.destination))
            results = []
            for statement in suggested.split(";"):
                cursor = con.execute(statement)
                if cursor.description:
                    results.append(cursor.fetchall())
            self.assertEqual([len(rows) for rows in results], [4, 3])
            self.assertEqual(con.execute('''SELECT count(*) FROM register_linked r
                LEFT JOIN annotations.register_count_evidence c ON c.row_id=r._fw_row_id
                LEFT JOIN annotations.reference_recovery rr ON rr.ref_no=r."ref no"
                LEFT JOIN annotations.bibliographic_checks b ON b.ref_no=r."ref no"''').fetchone(), (4,))
            self.assertEqual(con.execute('''SELECT count(*) FROM samples_rows s
                LEFT JOIN annotations.sample_count_evidence c ON c.sample_source_row_id=s._fw_row_id''').fetchone(), (3,))

    def test_input_hash_mismatch_creates_no_output(self):
        hashes = self.hashes()
        self.paths["reference_recovery"].write_bytes(b"changed")
        with self.assertRaisesRegex(ValueError, "Input SHA256 mismatch"):
            self.build(hashes)
        self.assertFalse(self.destination.exists())

    def test_wrong_base_hash_creates_no_output(self):
        with patch.object(ba, "BASE_SHA256", "0" * 64):
            self.assert_rejected("Assembly SHA256")

    def test_duplicate_register_annotation(self):
        self.change_rows("count_register", lambda rows: rows.append(rows[0].copy()))
        self.assert_rejected("duplicate row_id")

    def test_exact_raw_guard_catches_count_comments_and_taxon_changes(self):
        for field in ("count_raw", "comments_raw", "genus_raw"):
            original = {k: p.read_bytes() for k, p in self.paths.items()}
            self.change_rows("count_register", lambda rows: rows[0].update({field: "changed"}))
            self.assert_rejected("Raw source mismatch")
            for key, data in original.items():
                self.paths[key].write_bytes(data)

    def test_unit_does_not_escape_guarded_review(self):
        self.change_rows("count_register", lambda rows: rows[1].update(count_unit="minimum_individuals"))
        self.assert_rejected("does not reproduce review")

    def test_missing_source_row_is_rejected(self):
        self.change_rows("count_register", lambda rows: rows.pop())
        self.assert_rejected("coverage differs")

    def test_duplicate_sample_source_row_is_rejected(self):
        self.change_rows("count_samples", lambda rows: rows[1].update(sample_source_row_id=rows[0]["sample_source_row_id"]))
        self.assert_rejected("duplicate sample_source_row_id")

    def test_sample_aggregation_is_verified(self):
        self.change_rows("count_samples", lambda rows: rows[0].update(register_rows="999"))
        self.assert_rejected("aggregation differs")

    def test_summary_receipt_hash_is_verified(self):
        self.change_json("count_summary", lambda value: value["outputs"]["register-count-evidence.tsv"].update(sha256="bad"))
        self.assert_rejected("hash/size mismatch")

    def test_missing_recovered_reference_is_rejected(self):
        self.change_json("reference_recovery", lambda value: value["references"].pop())
        self.assert_rejected("IDs differ")

    def test_recovery_row_sample_and_exact_citation_id_guards(self):
        for field, changed, message in [("affected_register_rows", 42, "metadata mismatch"),
                ("affected_sample_ids", ["wrong"], "metadata mismatch"),
                ("provider_citation", "Wrong [ER 111]", "citation ID mismatch")]:
            original = self.paths["reference_recovery"].read_bytes()
            self.change_json("reference_recovery", lambda value: value["references"][0].update({field: changed}))
            self.assert_rejected(message)
            self.paths["reference_recovery"].write_bytes(original)

    def test_duplicate_bibliography_is_rejected(self):
        self.change_json("bibliographic_checks", lambda value: value["checks"].append(value["checks"][0]))
        self.assert_rejected("duplicate ref_no")

    def test_destination_is_never_overwritten(self):
        self.destination.write_bytes(b"prior result")
        with self.assertRaises(FileExistsError):
            self.build()
        self.assertEqual(self.destination.read_bytes(), b"prior result")

    def test_concurrent_destination_is_never_overwritten(self):
        original_link = ba.os.link

        def collision(source, destination):
            Path(destination).write_bytes(b"concurrent result")
            original_link(source, destination)

        with patch.object(ba.os, "link", side_effect=collision):
            with self.assertRaises(FileExistsError):
                self.build()
        self.assertEqual(self.destination.read_bytes(), b"concurrent result")
        self.assertEqual(list(self.root.glob(".annotations-*")), [])

    def test_late_input_change_removes_temporary_output(self):
        original_writer = ba.write_text_table

        def mutate_input(*args):
            original_writer(*args)
            self.paths["bibliographic_checks"].write_bytes(b"changed during build")

        with patch.object(ba, "write_text_table", side_effect=mutate_input):
            self.assert_rejected("input changed")


if __name__ == "__main__":
    unittest.main()
