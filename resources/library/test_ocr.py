import hashlib
import json
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import library


class OCRTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.store = Path(self.tmp.name)
        for d in ('pdf', 'text', 'openalex'):
            (self.store / d).mkdir()
        self.pdf = self.store / 'pdf' / 'W1.pdf'
        self.pdf.write_bytes(b'%PDF-test')
        self.original = self.store / 'text' / 'W1.txt'
        self.original.write_text('original extraction', encoding='utf-8')
        (self.store / 'openalex' / 'W1.json').write_text(json.dumps(
            {'id': 'https://openalex.org/W1', 'title': 'Triassic marine ecological recovery'}))
        self.row = {k: '' for k in library.MANIFEST_FIELDS}
        self.row.update(openalex_id='W1', status='no_text', path='pdf/W1.pdf', pages='2',
                        sha256=hashlib.sha256(self.pdf.read_bytes()).hexdigest())
        library.append_tsv(self.store / 'manifest.tsv', self.row, library.MANIFEST_FIELDS, threading.Lock())

    def tearDown(self):
        self.tmp.cleanup()

    def run_ocr(self, body=None):
        def run(args, **kwargs):
            if args[:2] == ['tesseract', '--version']:
                return SimpleNamespace(stdout='tesseract test\n')
            if args[0] == 'tesseract':
                text = body if body is not None else 'Triassic marine ecological recovery ' + 'fossil extinction recovery ' * 35
                return SimpleNamespace(stdout=text.encode())
            return SimpleNamespace(stdout=b'')
        with patch.object(library, 'pdf_pages', return_value=2), patch.object(library.subprocess, 'run', side_effect=run):
            library.ocr(self.store, ['W1'])

    def test_ocr_preserves_source_and_is_idempotent(self):
        self.run_ocr()
        self.assertEqual(self.pdf.read_bytes(), b'%PDF-test')
        self.assertEqual(self.original.read_text(), 'original extraction')
        self.assertEqual(library.load_manifest(self.store)['W1']['status'], 'ocr_ok')
        receipt = json.loads((self.store / 'ocr' / 'W1.json').read_text())
        self.assertEqual(receipt['ocr_sha256'], hashlib.sha256((self.store / 'ocr' / 'W1.txt').read_bytes()).hexdigest())
        self.run_ocr()
        self.assertEqual(len(library.read_tsv(self.store / 'manifest.tsv')), 2)

    def test_refuses_bad_checksum_and_tdm(self):
        self.pdf.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.run_ocr()
        self.row['status'] = 'tdm_no_text'
        library.append_tsv(self.store / 'manifest.tsv', self.row, library.MANIFEST_FIELDS, threading.Lock())
        with self.assertRaisesRegex(ValueError, 'only held open'):
            self.run_ocr()

    def test_rejects_unusable_ocr_without_promoting_status(self):
        with self.assertRaisesRegex(ValueError, 'coverage failed'):
            self.run_ocr('Triassic marine ecological recovery')
        self.assertEqual(library.load_manifest(self.store)['W1']['status'], 'no_text')
        self.assertFalse((self.store / 'ocr' / 'W1.txt').exists())

    def test_withdraw_moves_derived_ocr_and_preserves_manifest_history(self):
        self.run_ocr()
        library.withdraw(self.store, ['W1'], 'test')
        self.assertFalse((self.store / 'ocr' / 'W1.txt').exists())
        self.assertTrue((self.store / 'quarantine' / 'withdrawn' / 'W1.ocr.txt').exists())
        self.assertEqual(library.load_manifest(self.store)['W1']['status'], 'withdrawn')

    def test_withdraw_refuses_existing_destination_before_moving_any_source(self):
        self.run_ocr()
        dest = self.store / 'quarantine' / 'withdrawn'
        dest.mkdir(parents=True)
        (dest / 'W1.ocr.txt').write_text('prior copy', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'destination exists'):
            library.withdraw(self.store, ['W1'], 'test')
        self.assertTrue(self.pdf.exists())
        self.assertTrue((self.store / 'ocr' / 'W1.txt').exists())
        self.assertEqual((dest / 'W1.ocr.txt').read_text(), 'prior copy')
        self.assertEqual(library.load_manifest(self.store)['W1']['status'], 'ocr_ok')

    def test_text_index_uses_ocr_instead_of_original_extraction(self):
        self.run_ocr()
        row = {'openalex_id': 'W1', 'year': '1993', 'first_author': 'Test', 'title': 'Triassic marine ecological recovery',
               'venue': 'Test', 'doi': '', 'tiers': 'canon', 'fulltext': 'ocr_ok', 'cited_by': 0}
        rec = {'id': 'https://openalex.org/W1'}
        with patch.object(library, 'load_records', return_value={'W1': rec}), \
             patch.object(library, 'catalogue', return_value=([row], [], {})):
            library.textindex(self.store)
        db = sqlite3.connect(self.store / 'search.sqlite')
        self.assertEqual(db.execute("select count(*) from docs where docs match 'fossil' and part='fulltext'").fetchone()[0], 1)
        self.assertEqual(db.execute("select count(*) from docs where docs match 'original' and part='fulltext'").fetchone()[0], 0)
        db.close()


if __name__ == '__main__':
    unittest.main()
