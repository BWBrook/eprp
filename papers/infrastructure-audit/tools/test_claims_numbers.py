"""Regress checksum parsing and scientific-number comparisons in the ledger check."""
import unittest
import tempfile
from decimal import Decimal
from pathlib import Path

from claims import check_doc, numbers, same


class NumberChecks(unittest.TestCase):
    def test_checksum_is_not_numeric_evidence(self):
        checksum = '63960550e99255500323f6b7a5aa4108b8b848695911b97aaa0eed5d7f9c04ed5'
        for prose in (True, False):
            self.assertEqual(numbers('"' + checksum + '"', prose), [])

    def test_scientific_and_grouped_values_survive(self):
        self.assertEqual(numbers('1,454; 0.315864; ~5e-14; −2.7'), [
            (False, Decimal('1454')), (False, Decimal('0.315864')),
            (True, Decimal('5e-14')), (False, Decimal('-2.7'))])

    def test_large_exponent_does_not_crash_or_match(self):
        self.assertFalse(same(Decimal('0.315864'), Decimal('1e9999999')))

    def test_display_precision_matches(self):
        self.assertTrue(same(Decimal('0.466'), Decimal('0.4659138824790183')))
        self.assertFalse(same(Decimal('0.465'), Decimal('0.4659138824790183')))

    def test_sentence_full_stop_is_not_decimal_continuation(self):
        self.assertEqual(numbers('0.999.'), [(False, Decimal('0.999'))])
        self.assertEqual(numbers('1,454.'), [(False, Decimal('1454'))])
        self.assertEqual(numbers('1,454.0abc'), [])
        self.assertEqual(numbers('3.12.3'), [])

    def test_json_array_separators_preserve_numbers(self):
        self.assertEqual(numbers('[47,28]', prose=False), [
            (False, Decimal('47')), (False, Decimal('28'))])

    def test_sentence_final_bad_numeric_citation_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            doc = Path(folder) / 'text.md'
            doc.write_text('[0.999.]{.C096}')
            errors = []
            check_doc(doc, {'C096': {'status': 'supported', 'value': '0.466'}}, set(), errors)
            self.assertEqual(len(errors), 1)
            self.assertIn('quotes 0.999', errors[0])


if __name__ == '__main__':
    unittest.main()
