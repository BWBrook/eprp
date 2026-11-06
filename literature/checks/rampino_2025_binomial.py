#!/usr/bin/env python3
"""Check the printed binomial contract; do not infer a replacement chance model."""

import json
import math
from fractions import Fraction


def check():
    n, k = 47, 28
    p = Fraction(11, 20)
    tail = sum(Fraction(math.comb(n, j)) * p**j * (1 - p)**(n - j)
               for j in range(k, n + 1))
    return {
        "doi": "10.1016/j.earscirev.2025.105100",
        "source_pdf_sha256": "7ba178cce4c5359152e474f027171faae2d317b931e124ba9ddef5e63c20fc71",
        "source_location": "Section 3, printed pages 3-4; rendered page 4 checked",
        "stated_n": n, "stated_k": k, "stated_p": float(p),
        "reported_probability": 3.4e-16,
        "standard_binomial_probability_at_least_k": float(tail),
        "exact_tail_numerator": tail.numerator,
        "exact_tail_denominator": tail.denominator,
        "sum_widths_of_47_plus_minus_1_myr_windows": n * 2,
        "printed_window_total_myr": 141,
        "literal_constant_choose_sum": sum(math.comb(n, k) * float(p)**j * float(1 - p)**(n - j)
                                          for j in range(k, n + 1)),
        "different_all_success_contract_n28": float(p**28),
        "limits": "The printed equation uses choose(n,k) within a sum over j; the standard binomial prose contract uses choose(n,j). Neither this arithmetic nor the window-width check establishes an appropriate geological null or refutes periodicity.",
    }


if __name__ == "__main__":
    print(json.dumps(check(), indent=2, sort_keys=True))
