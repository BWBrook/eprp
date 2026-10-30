import math
import unittest

from workbook_diagnostic import interpolate


class InterpolationChecks(unittest.TestCase):
    def test_exact_zero_preserved(self):
        found, status = interpolate([(2, (0, 0.5, 1.5), "A2")], 2)
        self.assertEqual(status, "ok")
        self.assertEqual(found["values"][0], 0)
        self.assertEqual(found["low_cell"], found["high_cell"])

    def test_log_midpoint(self):
        found, _ = interpolate([(2, (0, 1, 2), "A2"), (4, (2, 3, 4), "B2")], math.sqrt(8))
        self.assertAlmostEqual(found["weight"], 0.5)
        self.assertAlmostEqual(found["values"][1], 2)

    def test_no_extrapolation(self):
        self.assertEqual(interpolate([(2, (0, 1, 2), "A2")], 3), (None, "outside_joint_coverage"))

    def test_gap_not_bridged(self):
        self.assertEqual(interpolate([(1, (0, 1, 2), "A2"), (4, (2, 3, 4), "B2")], 2), (None, "bracket_exceeds_factor_two"))

    def test_empty_row(self):
        self.assertEqual(interpolate([], 2), (None, "outside_joint_coverage"))


if __name__ == "__main__":
    unittest.main()
