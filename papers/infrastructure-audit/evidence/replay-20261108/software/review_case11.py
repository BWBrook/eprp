"""Compare the main recurrence, References direct sum, and integer convolution."""
import hashlib
import importlib.util
import json
import math
import pathlib
import sys

sys.dont_write_bytecode = True


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


repo, out = map(pathlib.Path, sys.argv[1:])
main_path = repo / "papers/infrastructure-audit/evidence/replay-20261108/main/check_case11.py"
references_path = repo / "literature/checks/rampino_2025_binomial.py"
main = module(main_path, "main_case11").check()
references = module(references_path, "references_case11").check()
coefficients = [1]
for _ in range(47):
    nxt = [0] * (len(coefficients) + 1)
    for j, value in enumerate(coefficients):
        nxt[j] += 9 * value
        nxt[j + 1] += 11 * value
    coefficients = nxt
assert sum(coefficients) == 20**47
num, den = sum(coefficients[28:]), 20**47
divisor = math.gcd(num, den)
num, den = num // divisor, den // divisor
assert num == int(main["exact_numerator"]) == references["exact_tail_numerator"]
assert den == int(main["exact_denominator"]) == references["exact_tail_denominator"]
assert num / den == main["exact_complement_recurrence_tail"] == references["standard_binomial_probability_at_least_k"]
assert abs(num / den - main["R_pbinom_tail"]) < 2e-15
result = dict(case=11, status="independent computational review passed",
    files_sha256={str(p.relative_to(repo)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in (main_path, references_path, pathlib.Path(__file__).resolve())},
    independent_route="47-fold integer polynomial convolution of (9 + 11*x), tail coefficients from x^28 onward, divided by 20^47",
    exact_numerator=str(num), exact_denominator=str(den), exact_decimal_p055_tail=num/den,
    references_tail=references["standard_binomial_probability_at_least_k"],
    main_recurrence_tail=main["exact_complement_recurrence_tail"],
    R_pbinom_tail=main["R_pbinom_tail"], R_version=main["R_version"],
    R_minus_exact=main["R_pbinom_tail"]-num/den,
    limits="Independent review of the stated n=47, k>=28, p=0.55 binomial calculation only. The exact route treats decimal 0.55 as rational 11/20; R uses binary floating-point and its numerical tail algorithm. Small rounding differences do not change the claim. Source PDFs, geological null, spectral evidence and periodicity were not re-reviewed.")
(out / "case11_reviewer.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
