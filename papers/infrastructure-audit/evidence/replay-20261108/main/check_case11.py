"""Independent binomial recurrence, exact complement, and R-library check."""
import hashlib
import json
import math
import subprocess
from fractions import Fraction
from pathlib import Path


def check():
    n, k = 47, 28
    p = Fraction(11, 20)
    mass = (1 - p) ** n
    lower = Fraction(0)
    for j in range(k):
        lower += mass
        mass *= Fraction(n - j, j + 1) * p / (1 - p)
    exact = 1 - lower
    upper = math.fsum(math.comb(n, j) * .55**j * .45**(n-j) for j in range(k, n+1))
    r = subprocess.run(['Rscript', '--vanilla', '-e',
        'cat(format(pbinom(27,47,.55,lower.tail=FALSE),digits=17),"\\n");cat(as.character(getRversion()),"\\n")'],
        check=True, capture_output=True, text=True).stdout.splitlines()
    r_tail = float(r[0])
    assert abs(float(exact) - upper) < 2e-15
    assert abs(float(exact) - r_tail) < 2e-15
    source_check = Path(__file__).resolve().parents[5] / 'literature/checks/rampino_2025_binomial.py'
    return {
        'case': 11, 'doi': '10.1016/j.earscirev.2025.105100',
        'n': n, 'k': k, 'p': float(p), 'reported_probability': 3.4e-16,
        'exact_complement_recurrence_tail': float(exact),
        'exact_numerator': str(exact.numerator), 'exact_denominator': str(exact.denominator),
        'direct_floating_tail': upper, 'R_pbinom_tail': r_tail, 'R_version': r[1].strip(),
        'original_check_sha256': hashlib.sha256(source_check.read_bytes()).hexdigest(),
        'source_pdf_sha256': '7ba178cce4c5359152e474f027171faae2d317b931e124ba9ddef5e63c20fc71',
        'source_location': 'Printed pages 3-4; page 4 visually checked again in this replay',
        'limit': 'Checks the binomial contract stated in the paper. It does not choose a geological null, rerun spectral tests or refute periodicity.'
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, sort_keys=True))
