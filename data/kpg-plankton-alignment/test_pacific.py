import csv
import tempfile
import unittest
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

import align_pacific as alignment


class PacificAlignmentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.workbook = self.root / 'source.xlsx'
        self.table = self.root / 'pangaea-893919.txt'
        headers = {alignment.column_name(i): f'genus_{i}' for i in range(17, 90)}
        headers.update({'Q': 'initials', 'R': 'site', 'S': 'hole', 'T': 'core', 'U': 'type',
                        'V': 'section', 'W': 'top_cm', 'X': 'bot_cm', 'Y': 'mid_cm',
                        'Z': 'depth_mbsf', 'AA': 'depth_rmcd', 'AB': 'depth_rmcd_adj',
                        'AC': 'Age_(Myr_ago)', 'AJ': 'coccolithus', 'AL': 'cruciplacolithus_small',
                        'AM': 'cruciplacolithus_large', 'AP': 'neobiscutum', 'AQ': 'praeprinsius'})
        sample = {'Q': 'SA', 'R': 'U1209', 'S': 'A', 'T': '21', 'U': 'H', 'V': '1',
                  'W': '3.9999999999999', 'X': '5', 'Y': '4.5', 'Z': '188.74499999999998',
                  'AA': '208.845', 'AB': '207.897', 'AC': '65.12345', 'AJ': '0',
                  'AL': '', 'AM': '1', 'AP': '0', 'AQ': '2'}
        xml = ('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' +
               self.xml_row(8, headers) + self.xml_row(9, sample) + '</sheetData></worksheet>')
        with zipfile.ZipFile(self.workbook, 'w') as z:
            z.writestr('xl/sharedStrings.xml', '<sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"/>')
            z.writestr('xl/worksheets/sheet1.xml', xml)
        self.header = 'Event\tInvestigator\tSample label\tDepth sed [m]\tDepth comp r [rmcd]\tDepth adj rmcd [armcd]\tAge [ka BP]\n'
        self.row = '198-1209A\tSA\t198-1209A-21H-1,4-5\t188.75\t208.85\t207.90\t65123\n'
        self.write_table(self.row)

    @staticmethod
    def xml_row(number, cells):
        return '<row r="{}">{}</row>'.format(number, ''.join(
            f'<c r="{col}{number}" t="inlineStr"><is><t>{escape(value)}</t></is></c>'
            for col, value in cells.items()))

    def write_table(self, rows):
        self.table.write_text('metadata\n*/\n' + self.header + rows, encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_join_preserves_blanks_zeroes_and_workbook_precision(self):
        out = self.root / 'out'
        alignment.build(self.workbook, self.table, out)
        with (out / 'pacific-original-percentages-private.tsv').open(newline='') as f:
            row = next(csv.DictReader(f, delimiter='\t'))
        self.assertEqual(row['sample_label'], '198-1209A-21H-1,4-5')
        self.assertEqual(row['source_W_top_cm'], '3.9999999999999')
        self.assertEqual(row['Coccolithus_pct'], '0')
        self.assertEqual(row['source_AL_cruciplacolithus_small_pct'], '')
        self.assertEqual(row['Cruciplacolithus_pct'], '')

    def test_duplicate_or_unmatched_sample_is_rejected(self):
        self.write_table(self.row * 2)
        with self.assertRaisesRegex(ValueError, 'Duplicate PANGAEA'):
            alignment.build(self.workbook, self.table, self.root / 'out')
        self.write_table(self.row.replace('21H-1,4-5', '22H-1,4-5'))
        with self.assertRaisesRegex(ValueError, 'do not agree'):
            alignment.build(self.workbook, self.table, self.root / 'out')

    def test_mismatched_age_or_depth_is_rejected(self):
        self.write_table(self.row.replace('65123', '65130'))
        with self.assertRaisesRegex(ValueError, 'age_ka outside'):
            alignment.build(self.workbook, self.table, self.root / 'out')
        self.write_table(self.row.replace('188.75', '188.85'))
        with self.assertRaisesRegex(ValueError, 'mbsf outside'):
            alignment.build(self.workbook, self.table, self.root / 'out')

    def test_workbook_sample_with_missing_age_is_not_silently_dropped(self):
        with zipfile.ZipFile(self.workbook) as z:
            shared = z.read('xl/sharedStrings.xml')
            sheet = z.read('xl/worksheets/sheet1.xml').decode().replace('65.12345', '')
        with zipfile.ZipFile(self.workbook, 'w') as z:
            z.writestr('xl/sharedStrings.xml', shared)
            z.writestr('xl/worksheets/sheet1.xml', sheet)
        with self.assertRaisesRegex(ValueError, 'metadata without an age'):
            alignment.build(self.workbook, self.table, self.root / 'out')


if __name__ == '__main__':
    unittest.main()
