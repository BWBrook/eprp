#!/usr/bin/env python3
"""Check that provider TSV quotation marks remain literal source text."""

from pathlib import Path
import tempfile
import unittest

from acquire_intervals import parse_table


class LiteralTSVTests(unittest.TestCase):
    def test_quotes_do_not_strip_text_or_merge_physical_records(self):
        data = 'taxon\tcount\tcomments\nMuntiacus\t43\t"ssp.1\'\'\nCapricornis\t4\t"Naemorhedus sumatraensis"\n'
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "register.txt"
            path.write_text(data, encoding="utf-8")
            header, rows = parse_table(path)
        self.assertEqual(header, ["taxon", "count", "comments"])
        self.assertEqual(rows, [
            ["Muntiacus", "43", '"ssp.1\'\''],
            ["Capricornis", "4", '"Naemorhedus sumatraensis"'],
        ])


if __name__ == "__main__":
    unittest.main()
