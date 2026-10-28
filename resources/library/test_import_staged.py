import csv
import hashlib
import json
import tempfile
import threading
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

    def test_open_import_supersedes_but_preserves_tdm_copy(self):
        tdm = self.store / 'tdm' / 'wiley' / 'pdf' / 'W1.pdf'
        tdm.parent.mkdir(parents=True)
        tdm.write_bytes(b'licensed copy')
        tdm_text = self.store / 'tdm' / 'wiley' / 'text' / 'W1.txt'
        tdm_text.parent.mkdir(parents=True)
        tdm_text.write_text('licensed text', encoding='utf-8')
        prior = {k: '' for k in library.MANIFEST_FIELDS}
        prior.update(openalex_id='W1', status='tdm_ok', path='tdm/wiley/pdf/W1.pdf')
        library.append_tsv(self.store / 'manifest.tsv', prior, library.MANIFEST_FIELDS, threading.Lock())
        self.run_import()
        self.assertEqual(tdm.read_bytes(), b'licensed copy')
        self.assertEqual(tdm_text.read_text(), 'licensed text')
        current = library.load_manifest(self.store)['W1']
        self.assertEqual(current['status'], 'ok')
        self.assertIn('does not alter', current['note'])
        self.run_import()
        self.assertEqual(len(library.read_tsv(self.store / 'manifest.tsv')), 3)

    def test_missing_tdm_copy_aborts_batch_before_import(self):
        prior = {k: '' for k in library.MANIFEST_FIELDS}
        prior.update(openalex_id='W1', status='tdm_ok', path='tdm/wiley/pdf/W1.pdf')
        library.append_tsv(self.store / 'manifest.tsv', prior, library.MANIFEST_FIELDS, threading.Lock())
        with self.assertRaisesRegex(ValueError, 'TDM path missing or invalid'):
            self.run_import()
        self.assertFalse((self.store / 'pdf' / 'W1.pdf').exists())
        self.assertFalse((self.store / 'pdf' / 'W2.pdf').exists())

    def test_rejected_figure_is_retained_and_replaced_by_verified_article(self):
        (self.store / 'pdf').mkdir()
        (self.store / 'text').mkdir()
        original = b'%PDF-only-a-figure'
        (self.store / 'pdf' / 'W1.pdf').write_bytes(original)
        (self.store / 'text' / 'W1.txt').write_text('plot', encoding='utf-8')
        prior = {k: '' for k in library.MANIFEST_FIELDS}
        prior.update(openalex_id='W1', status='no_text', path='pdf/W1.pdf',
                     sha256=hashlib.sha256(original).hexdigest())
        library.append_tsv(self.store / 'manifest.tsv', prior, library.MANIFEST_FIELDS, threading.Lock())
        library.withdraw(self.store, ['W1'], 'figure rather than article', rejected=True)
        self.run_import()
        self.assertEqual((self.store / 'quarantine' / 'rejected' / 'W1.pdf').read_bytes(), original)
        self.assertEqual((self.store / 'pdf' / 'W1.pdf').read_bytes(), (self.stage / 'W1.pdf').read_bytes())
        self.assertIn('rejected incomplete copy', library.load_manifest(self.store)['W1']['note'])

    def test_regular_withdrawal_is_not_eligible_for_replacement(self):
        prior = {k: '' for k in library.MANIFEST_FIELDS}
        prior.update(openalex_id='W1', status='withdrawn', path='quarantine/withdrawn/W1.pdf')
        library.append_tsv(self.store / 'manifest.tsv', prior, library.MANIFEST_FIELDS, threading.Lock())
        with self.assertRaisesRegex(ValueError, 'existing manifest'):
            self.run_import()

    def test_fetch_does_not_reacquire_a_rejected_work_even_on_retry(self):
        prior = {k: '' for k in library.MANIFEST_FIELDS}
        prior.update(openalex_id='W1', status='rejected', path='quarantine/rejected/W1.pdf',
                     url='https://example.org/figure.pdf')
        library.append_tsv(self.store / 'manifest.tsv', prior, library.MANIFEST_FIELDS, threading.Lock())
        with patch.object(library, 'load_records', return_value={'W1': {'id': 'W1', 'type': 'article'}}), \
             patch.object(library, 'load_aliases', return_value={}), \
             patch.object(library, 'load_seeds', return_value={'canon': [{'key': 'W1'}]}), \
             patch.object(library, 'seed_wid', return_value='W1'), \
             patch.object(library, 'load_attempts', return_value=[]), \
             patch.object(library, 'duplicate_map', return_value={}), \
             patch.object(library, 'fetch_one') as fetch_one:
            for retry in (False, True):
                library.fetch(self.store, None, 1, retry)
            fetch_one.assert_not_called()


if __name__ == '__main__':
    unittest.main()
