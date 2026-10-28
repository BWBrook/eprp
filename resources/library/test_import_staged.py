import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import library


class ImportStagedTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.store = self.root / 'store'
        self.stage = self.root / 'stage'
        (self.store / 'openalex').mkdir(parents=True)
        self.stage.mkdir()
        self.rows = []
        for wid, title, scan in [('W1', 'Distinct extinction recovery dynamics', False),
                                  ('W2', 'Triassic marine ecological recovery', True)]:
            doi = '10.1234/' + wid.lower()
            data = ('%PDF-1.4 ' + title).encode()
            (self.stage / (wid + '.pdf')).write_bytes(data)
            (self.store / 'openalex' / (wid + '.json')).write_text(json.dumps(
                {'id': 'https://openalex.org/' + wid, 'doi': 'https://doi.org/' + doi, 'title': title}))
            self.rows.append({'openalex_id': wid, 'doi': doi, 'sha256': hashlib.sha256(data).hexdigest(),
                              'bytes': str(len(data)), 'url': 'https://author.example/' + wid + '.pdf',
                              'final_url': '', 'verification': 'first-page OCR' if scan else 'embedded text',
                              'outcome': 'staged'})
        self.batch = self.root / 'batch.tsv'
        self.save(self.rows)

    def tearDown(self):
        self.tmp.cleanup()

    def save(self, rows):
        with self.batch.open('w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=self.rows[0], delimiter='\t')
            w.writeheader()
            w.writerows(rows)

    def run_import(self):
        def text(path, last_page=None):
            return path.read_bytes().decode().removeprefix('%PDF-1.4 ')

        def proc(args, **kwargs):
            return SimpleNamespace(stdout=b'Triassic marine ecological recovery')

        with patch.object(library, 'pdf_pages', return_value=1), patch.object(library, 'pdf_text', side_effect=text), \
             patch.object(library.subprocess, 'run', side_effect=proc):
            library.import_staged(self.store, self.batch, self.stage)

    def test_import_is_idempotent_and_scans_are_not_indexed_as_full_text(self):
        self.run_import()
        m = library.load_manifest(self.store)
        self.assertEqual(m['W1']['status'], 'ok')
        self.assertEqual(m['W2']['status'], 'no_text')
        self.assertEqual((self.store / 'text' / 'W2.txt').read_text(), '')
        self.run_import()
        self.assertEqual(len(library.read_tsv(self.store / 'manifest.tsv')), 2)

    def test_bad_checksum_aborts_before_any_pdf_is_imported(self):
        rows = [dict(r) for r in self.rows]
        rows[1]['sha256'] = '0' * 64
        self.save(rows)
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.run_import()
        self.assertEqual(list((self.store / 'pdf').iterdir()), [])

    def test_existing_unregistered_or_corrupt_copy_is_not_overwritten(self):
        self.run_import()
        pdf = self.store / 'pdf' / 'W1.pdf'
        pdf.chmod(0o644)
        pdf.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'existing manifest'):
            self.run_import()
        self.assertEqual(pdf.read_bytes(), b'changed')


if __name__ == '__main__':
    unittest.main()
