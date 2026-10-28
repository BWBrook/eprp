import csv
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import align


class AlignmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.rows = {
            '893899': [{'Age [ka BP]': '66000', 'Neobiscutum spp. [%]': '10',
                       'Praeprinsius spp. [%]': '3', 'Cruciplacolithus spp. [%] (small)': '4',
                       'Cruciplacolithus spp. [%] (large)': '5', 'Coccolithus spp. [%]': '2'}],
            '893919': [{'Event': '198-1209A'}],
            '997794': [{'H': 'E', 'Core': '1', 'Depth sect [cm]': '1', 'Depth comp r [rmcd]': '2'},
                       {'H': 'E', 'Core': '1', 'Depth sect [cm]': '2', 'Depth comp r [rmcd]': '3'}],
            '997781': [{'H': 'E', 'Core': '1', 'Depth sect [cm]': '1', 'Age [Ma] one': '66.1',
                       'Age [Ma] two': '66.2', 'Neobiscutum [#]': '10', 'Praeprinsius [#]': '20',
                       'Cruciplacolithus [#]': '30', 'Coccolithus [#]': '40'}],
            '997793': [{'H': 'E', 'Core': '1', 'Depth sect [cm]': '1', 'Age [Ma] one': '66.1',
                       'Age [Ma] two': '66.2', 'Neobiscutum [%]': '10', 'Praeprinsius [%]': '20',
                       'Cruciplacolithus [%]': '30', 'Coccolithus [%]': '40'}],
        }

    def tearDown(self):
        self.tmp.cleanup()

    def run_build(self):
        def source(path):
            ident = path.stem.split('-')[-1]
            return self.rows[ident], '0' * 64
        with patch.object(align, 'read_source', side_effect=source):
            align.build(self.root, self.root / 'out')

    def test_unmatched_samples_are_retained_and_size_classes_combined(self):
        self.run_build()
        with (self.root / 'out' / 'el-kef-private.tsv').open(newline='') as f:
            rows = list(csv.DictReader(f, delimiter='\t'))
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[1]['source_age_model_1_ma'], '')
        self.assertEqual(rows[1]['Neobiscutum_pct'], '')
        self.assertEqual(rows[0]['source_age_model_2_ma'], '66.2')
        with (self.root / 'out' / 'pacific-private.tsv').open(newline='') as f:
            p = next(csv.DictReader(f, delimiter='\t'))
        self.assertEqual(p['Cruciplacolithus_pct'], '9')
        self.assertEqual(p['source_age_ka_bp'], '66000')

    def test_inconsistent_percentages_abort(self):
        self.rows['997793'][0]['Coccolithus [%]'] = '41'
        with self.assertRaisesRegex(ValueError, 'percentage mismatch'):
            self.run_build()

    def test_duplicate_sample_key_aborts(self):
        self.rows['997794'].append(dict(self.rows['997794'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate'):
            self.run_build()


if __name__ == '__main__':
    unittest.main()
