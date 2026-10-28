#!/usr/bin/env python3
"""Regression fixtures for lossless assembly, unresolved links and QC semantics."""

import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

import assemble


HEADERS = {
    "register": ["ref no", "sample no", "sample name", "time interval", "genus", "qualifier", "species", "count", "comments"],
    "samples": ["ref no", "sample no", "sample name", "time interval", "total count", "richness"],
    "references": ["ref_no", "title"],
    "species": ["species", "total count"],
    "matrix": ["species", "Name", "Collision", "Unknown"],
}


def tsv(header, rows):
    return ("\r\n".join("\t".join(row) for row in [header, *rows]) + "\r\n").encode("utf-8")


class AssemblyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.snapshot = self.root / "snapshot"
        self.snapshot.mkdir()
        self.output = self.root / "assembled.sqlite"
        self.audit_path = self.root / "selection.json"
        self.sheets = {
            "01-first": {
                "register": [
                    ["r1", "s1", "Name", "First", "A", "cf.", "alpha", "9", 'MNI café; second line  '],
                    ["r1", "s1", "Name", "First", "A", "cf.", "alpha", "9", 'MNI café; second line  '],
                    ["r1", "s1", "Name", "First", "A", "cf.", "alpha", "1", "NISP"],
                    ["rCross", "s4", "Fourth", "First", "B", "aff.", "beta", "0.1", ""],
                    ["missing", "s4", "Fourth", "First", "B", "?", "indet.", "0.2", ""],
                    ["rAmb", "absent", "Absent", "First", "Higher rank", "", "indet.", "2", ""],
                    ["", "", "", "First", "C", "", "gamma", "3", ""],
                ],
                "samples": [
                    ["r1", "s1", "Name", "First", "10", "1"],
                    ["r1", "s1", "Name", "First", "10", "1"],
                    ["r1", "s2", "Collision", "First", "0", "0"],
                    ["r1", "s3", "Collision", "First", "0", "0"],
                    ["rCross", "s4", "Fourth", "First", "0.3", "2"],
                    ["rCross", "s4", "Fourth", "First", "0.3", "3"],
                ],
                "references": [["r1", "Original"], ["r1", "Original"], ["rAmb", "One"], ["rAmb", "Two"]],
                "species": [["A alpha", "19"]],
                "matrix": [["A alpha", "1", "7", ""]],
            },
            "02-second": {
                "register": [["r1", "s1", "Name", "Second", "A", "cf.", "alpha", "4", "NISP"]],
                "samples": [["r1", "s1", "Name", "Second", "4", "1"]],
                "references": [["r1", "Changed title"], ["rCross", "Elsewhere only"]],
                "species": [["A alpha", "4"]],
                "matrix": [["A alpha", "4", "0", "0"]],
            },
        }
        self.write_fixture()

    def write_fixture(self):
        files, selections, intervals = [], [], []
        for directory, tables in self.sheets.items():
            label = "First" if directory == "01-first" else "Second"
            attempt = f"{directory}/attempt-1"
            work = self.snapshot / attempt
            work.mkdir(parents=True, exist_ok=True)
            selected = []
            for table in assemble.TABLES:
                data = tsv(HEADERS[table], tables[table])
                key = f"{attempt}/{table}.txt"
                (self.snapshot / key).write_bytes(data)
                record = {"key": key, "size": len(data), "sha256": assemble.digest(data)}
                files.append(record)
                selected.append(record)
            for suffix, value in (("request.json", {"parameters": {label: "yes"}}), ("receipts.json", [{"started_utc": "retained source value"}])):
                data = json.dumps(value).encode()
                key = f"{attempt}/{suffix}"
                (self.snapshot / key).write_bytes(data)
                files.append({"key": key, "size": len(data), "sha256": assemble.digest(data)})
            intervals.append({"directory": directory, "interval": label})
            selections.append({"source_attempt": attempt, "interval": label, "source_files": selected,
                               "state": "downloaded_source_inconsistency", "expected_rows": {"register": 999},
                               "validation": {"rows": {k: len(v) for k, v in tables.items()}}})
        manifest = {"files": files, "intervals": intervals}
        manifest_bytes = json.dumps(manifest).encode()
        (self.snapshot / "MANIFEST.json").write_bytes(manifest_bytes)
        self.manifest_sha = assemble.digest(manifest_bytes)
        audit = {"manifest_sha256": self.manifest_sha, "manifest_hash_failures": [], "intervals": selections}
        self.audit_path.write_text(json.dumps(audit))
        self.audit_sha = assemble.digest(self.audit_path.read_bytes())

    def run_assembly(self):
        return assemble.assemble(self.snapshot, self.output, self.audit_path,
                                 manifest_sha256=self.manifest_sha, audit_sha256=self.audit_sha)

    def connect(self):
        connection = sqlite3.connect(self.output)
        self.addCleanup(connection.close)
        return connection

    def test_lossless_rows_duplicates_original_columns_and_line_spans(self):
        summary = self.run_assembly()
        self.assertEqual(summary["register"], 8)
        db = self.connect()
        self.assertEqual(db.execute('SELECT count(*) FROM register_rows').fetchone()[0], 8)
        self.assertEqual(db.execute('SELECT count(*) FROM register_linked').fetchone()[0], 8)
        for file_id, header_json in db.execute('SELECT file_id,header_json FROM source_files'):
            table = Path(file_id).stem
            directory = file_id.split('/')[0]
            self.assertEqual(json.loads(header_json), HEADERS[table])
            actual = [json.loads(r[0]) for r in db.execute('SELECT values_json FROM source_rows WHERE file_id=? ORDER BY record_number', (file_id,))]
            self.assertEqual(actual, self.sheets[directory][table])
        first = db.execute('SELECT line_start,line_end,values_json FROM source_rows WHERE row_id=?', ('01-first/attempt-1/register.txt#1',)).fetchone()
        self.assertEqual(first[:2], (2, 2))
        self.assertEqual(json.loads(first[2])[-1], 'MNI café; second line  ')
        row_ids = db.execute('SELECT _fw_row_id FROM register_rows WHERE comments=?', ('MNI café; second line  ',)).fetchall()
        self.assertEqual(len(set(row_ids)), 2)
        self.assertEqual(db.execute('SELECT qualifier FROM register_rows WHERE _fw_row_id=?', ('01-first/attempt-1/register.txt#4',)).fetchone()[0], 'aff.')
        self.assertEqual(db.execute('PRAGMA foreign_key_check').fetchall(), [])
        self.assertEqual(db.execute('PRAGMA integrity_check').fetchone()[0], 'ok')

    def test_candidate_links_never_multiply_or_resolve_across_intervals(self):
        self.run_assembly()
        db = self.connect()
        def link(row, kind):
            return db.execute('SELECT status,within_interval_rows,within_interval_variants,other_interval_rows FROM row_links WHERE owner_row_id=? AND kind=?', (f'01-first/attempt-1/register.txt#{row}', kind)).fetchone()
        self.assertEqual(link(1, 'sample'), ('repeated_identical', 2, 1, 1))
        self.assertEqual(link(1, 'reference'), ('repeated_identical', 2, 1, 1))
        self.assertEqual(link(4, 'sample'), ('ambiguous', 2, 2, 0))
        self.assertEqual(link(4, 'reference'), ('unresolved', 0, 0, 1))
        self.assertEqual(link(5, 'reference'), ('unresolved', 0, 0, 0))
        self.assertEqual(link(6, 'reference'), ('ambiguous', 2, 2, 0))
        self.assertEqual(link(6, 'sample'), ('unresolved', 0, 0, 0))
        self.assertEqual(link(7, 'reference'), ('missing_identifier', 0, 0, 0))
        self.assertEqual(link(7, 'sample'), ('missing_identifier', 0, 0, 0))
        candidates = db.execute("SELECT scope FROM link_candidates WHERE owner_row_id='01-first/attempt-1/register.txt#4' AND kind='reference'").fetchall()
        self.assertEqual(candidates, [('other_interval',)])

    def test_within_and_cross_interval_changes_and_register_key_groups(self):
        self.run_assembly()
        db = self.connect()
        group = db.execute("SELECT row_count,variant_count,changed_columns_json FROM identity_groups WHERE kind='sample' AND scope='cross_interval' AND source_key_json=?", ('["s1"]',)).fetchone()
        self.assertEqual(group[:2], (3, 2))
        self.assertEqual(json.loads(group[2]), ['time interval', 'total count'])
        group = db.execute("SELECT row_count,variant_count,classification FROM identity_groups WHERE kind='sample' AND scope='within_interval' AND interval_id='01-first' AND source_key_json=?", ('["s1"]',)).fetchone()
        self.assertEqual(group, (2, 1, 'repeated_identical'))
        key = assemble.encoded(['s1', 'r1', 'A', 'cf.', 'alpha'])
        group = db.execute("SELECT row_count,variant_count,changed_columns_json FROM identity_groups WHERE kind='register_key' AND scope='within_interval' AND interval_id='01-first' AND source_key_json=?", (key,)).fetchone()
        self.assertEqual(group[:2], (3, 2))
        self.assertEqual(json.loads(group[2]), ['count', 'comments'])

    def test_matrix_is_qc_and_name_collisions_are_not_resolved(self):
        self.run_assembly()
        db = self.connect()
        qc = db.execute("SELECT matrix_value_raw,status,summed_register_count,last_register_count,register_row_ids_json FROM matrix_qc WHERE matrix_row_id='01-first/attempt-1/matrix.txt#1' AND column_number=2").fetchone()
        self.assertEqual(qc[:4], ('1', 'different', '19', '1'))
        self.assertEqual(len(json.loads(qc[4])), 3)
        self.assertEqual(db.execute("SELECT differs_from_sum,differs_from_last FROM matrix_qc WHERE matrix_row_id='01-first/attempt-1/matrix.txt#1' AND column_number=2").fetchone(), (1, 0))
        self.assertEqual(db.execute("SELECT differing_cells_either,differing_from_sum,differing_from_last FROM interval_qc WHERE interval_id='01-first'").fetchone(), (1, 1, 0))
        collision = db.execute("SELECT status,distinct_sample_ids FROM matrix_columns WHERE file_id='01-first/attempt-1/matrix.txt' AND column_number=3").fetchone()
        self.assertEqual(collision, ('ambiguous', 2))
        self.assertEqual(db.execute("SELECT status FROM matrix_qc WHERE matrix_row_id='01-first/attempt-1/matrix.txt#1' AND column_number=3").fetchone()[0], 'ambiguous_or_unresolved_names')
        self.assertEqual(db.execute("SELECT count FROM register_rows WHERE _fw_row_id='01-first/attempt-1/register.txt#1'").fetchone()[0], '9')

    def test_each_sample_summary_is_compared_and_decimals_remain_exact(self):
        self.run_assembly()
        db = self.connect()
        qc = db.execute("SELECT status,summed_register_count,register_row_count FROM sample_qc WHERE sample_row_id='01-first/attempt-1/samples.txt#1'").fetchone()
        self.assertEqual(qc, ('summary_lower', '19', 3))
        self.assertEqual(db.execute('SELECT count(*) FROM sample_qc').fetchone()[0], 7)
        self.assertEqual(db.execute("SELECT status,summed_register_count FROM sample_qc WHERE sample_row_id='01-first/attempt-1/samples.txt#5'").fetchone(), ('equal', '0.3'))
        self.assertEqual(db.execute("SELECT status FROM sample_qc WHERE sample_row_id='01-first/attempt-1/samples.txt#3'").fetchone()[0], 'no_register_rows')

    def test_empty_counts_are_unavailable_except_blank_matrix_cells(self):
        self.sheets['01-first']['register'][0][-2] = ''
        self.sheets['02-second']['samples'][0][-2] = ''
        self.sheets['02-second']['matrix'][0][1] = ''
        self.write_fixture()
        self.run_assembly()
        db = self.connect()
        self.assertEqual(db.execute("SELECT status FROM sample_qc WHERE sample_row_id='01-first/attempt-1/samples.txt#1'").fetchone()[0], 'nonnumeric_count')
        self.assertEqual(db.execute("SELECT status FROM sample_qc WHERE sample_row_id='02-second/attempt-1/samples.txt#1'").fetchone()[0], 'nonnumeric_count')
        self.assertEqual(db.execute("SELECT matrix_value_raw,status,summed_register_count FROM matrix_qc WHERE matrix_row_id='02-second/attempt-1/matrix.txt#1' AND column_number=2").fetchone(), ('', 'different', '4'))

    def test_hash_mismatches_fail_before_any_output(self):
        path = self.snapshot / '01-first/attempt-1/register.txt'
        original = path.read_bytes()
        path.write_bytes(original + b'changed')
        with self.assertRaisesRegex(ValueError, 'Manifest file mismatch'):
            self.run_assembly()
        self.assertFalse(self.output.exists())
        path.write_bytes(original)
        self.audit_path.write_text(self.audit_path.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'Selection audit SHA256 mismatch'):
            self.run_assembly()
        self.assertFalse(self.output.exists())
        with self.assertRaisesRegex(ValueError, 'Manifest SHA256 mismatch'):
            assemble.assemble(self.snapshot, self.output, self.audit_path)

    def test_selected_hash_disagreement_fails_even_if_manifest_is_valid(self):
        audit = json.loads(self.audit_path.read_bytes())
        audit['intervals'][0]['source_files'][0]['sha256'] = '0' * 64
        self.audit_path.write_text(json.dumps(audit))
        self.audit_sha = assemble.digest(self.audit_path.read_bytes())
        with self.assertRaisesRegex(ValueError, 'Selected sheet differs'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_existing_output_and_source_directory_are_never_overwritten(self):
        self.output.write_bytes(b'precious existing output')
        with self.assertRaises(FileExistsError):
            self.run_assembly()
        self.assertEqual(self.output.read_bytes(), b'precious existing output')
        self.output = self.snapshot / 'derived.sqlite'
        with self.assertRaisesRegex(ValueError, 'outside the source snapshot'):
            self.run_assembly()
        self.assertFalse(self.output.exists())

    def test_literal_quotes_and_apparent_quoted_fields_are_preserved(self):
        comments = ['"Felis caracal"', '"Tamias spp." tentatively referred',
                    '"ssp.1\'\'', '"Naemorhedus sumatraensis"', 'embedded "quote"; ""doubled""']
        for row, comment in zip(self.sheets['01-first']['register'], comments):
            row[-1] = comment
        self.write_fixture()
        self.run_assembly()
        db = self.connect()
        actual = [r[0] for r in db.execute("SELECT comments FROM register_rows WHERE _fw_interval_id='01-first' ORDER BY _fw_row_id")]
        self.assertEqual(actual[:len(comments)], comments)
        self.assertEqual(db.execute("SELECT count(*) FROM register_rows").fetchone()[0], 8)

    def test_historical_csv_row_merging_is_reported_not_repeated(self):
        import csv
        import io
        raw = b'ref no\tsample no\tcomments\n4570\t4922\t"ssp.1\'\'\n4570\t4922\t"Naemorhedus sumatraensis"\n'
        old = list(csv.reader(io.StringIO(raw.decode()), delimiter='\t'))
        self.assertEqual(len(old), 2)
        header, rows = assemble.parse(raw, 'retained-example.txt')
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0][-1][-1], '"ssp.1\'\'')
        self.assertEqual(rows[1][-1][-1], '"Naemorhedus sumatraensis"')
        self.assertEqual(rows[1][1:3], (3, 3))
        audit = json.loads(self.audit_path.read_bytes())
        audit['intervals'][0]['validation']['rows']['register'] -= 1
        self.audit_path.write_text(json.dumps(audit))
        self.audit_sha = assemble.digest(self.audit_path.read_bytes())
        summary = self.run_assembly()
        self.assertEqual(summary['historical_row_count_disagreements'], [{
            'file_id': '01-first/attempt-1/register.txt', 'observed_literal_rows': 7,
            'historical_csv_audit_rows': 6}])
        db = self.connect()
        self.assertEqual(db.execute("SELECT row_count,historical_csv_audit_row_count,row_count_matches_historical_audit FROM source_files WHERE file_id='01-first/attempt-1/register.txt'").fetchone(), (7, 6, 0))

    def test_embedded_newlines_and_tabs_fail_without_guessing_quote_syntax(self):
        for comment in ('unquoted\nnewline', '"quoted\nnewline"', 'literal\ttab'):
            self.sheets['01-first']['register'][0][-1] = comment
            self.write_fixture()
            with self.assertRaisesRegex(ValueError, 'Ragged physical record'):
                self.run_assembly()
            self.assertFalse(self.output.exists())

    def test_literal_parser_handles_crlf_bom_no_final_newline_and_inner_carriage_return(self):
        header, rows = assemble.parse(b'\xef\xbb\xbfleft\tright\r\n"quoted"\tliteral\rreturn', 'example.txt')
        self.assertEqual(header, ['left', 'right'])
        self.assertEqual(rows, [(1, 2, 2, ['"quoted"', 'literal\rreturn'])])

    def test_ragged_sources_fail_without_partial_database(self):
        self.sheets['01-first']['register'][0].pop()
        self.write_fixture()
        with self.assertRaisesRegex(ValueError, 'Ragged physical record'):
            self.run_assembly()
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.glob('.fossilworks-*')), [])

    def test_nonnumeric_and_nonfinite_counts_remain_source_values(self):
        self.sheets['01-first']['register'][0][-2] = 'NaN'
        self.sheets['02-second']['matrix'][0][1] = 'unknown'
        self.write_fixture()
        self.run_assembly()
        db = self.connect()
        self.assertEqual(db.execute("SELECT count FROM register_rows WHERE _fw_row_id='01-first/attempt-1/register.txt#1'").fetchone()[0], 'NaN')
        self.assertEqual(db.execute("SELECT status FROM matrix_qc WHERE matrix_row_id='01-first/attempt-1/matrix.txt#1' AND column_number=2").fetchone()[0], 'nonnumeric_count')
        self.assertEqual(db.execute("SELECT status FROM matrix_qc WHERE matrix_row_id='02-second/attempt-1/matrix.txt#1' AND column_number=2").fetchone()[0], 'nonnumeric_count')


if __name__ == '__main__':
    unittest.main()
