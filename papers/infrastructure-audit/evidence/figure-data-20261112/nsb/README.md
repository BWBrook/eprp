# NSB signed age differences for Fig. 2D

`nsb_signed_age_differences.tsv.gz` contains the **56,387 comparable samples**
for C040 in NSB release `2023-06-05_10063218`. The columns are public NSB
`sample_id`, `site_hole`, and `stored_minus_interpolated_age_myr`. A positive
value means that the stored sample age is older than the interpolated age.
Differences are exported at `.17g` precision, sorted by sample ID. Gzip has
no embedded filename and a zero modification time.

The 4,111 absolute differences above 0.01 Myr occur in 56 holes. The receipt
retains the classifications of all 61,862 samples, including 5,475
noncomparable samples. Those samples have no row in the plotting table and
do not enter its denominator.

Reproduce with Python 3.12 or newer, using the explicit path to the held
database and an output directory:

```bash
python3 extract_nsb.py --database INPUT/nsb.sqlite --output-directory OUTPUT
```

The script requires the exact SHA-256 in `receipt.json`, opens SQLite read
only, and checks the input hash before and after extraction. It joins age
model rows to their current revision (`current_flag='Y'`), sorts ties by
`(depth, age)`, selects the first age at an exact tied depth with
`bisect_left`, and uses the last lower tie and first upper tie between depths.
It does not extrapolate. The signed differences preserve the weighted-endpoint
binary-float arithmetic of the 8 November replay.

A separate calculation collapses equal-depth ties to minimum/maximum ages,
looks up unique-depth brackets with `bisect_right`, and interpolates with a
50-digit Decimal slope formula. All comparable category assignments agree;
the receipt records the maximum numerical difference. This check shares the
source SQL and is an arithmetic/tie-convention check, not independent evidence
for the geological ages. The eight samples at conflicting exact-depth ties
remain convention-sensitive: all eight exceed 0.01 Myr under the first-tie
rule, and none does under the last-tie rule.

`receipt.json` records input, script and output hashes, versions, counts,
checks and limits. The reference counts are from
`../../replay-20261108/data/results/nsb_2023-06-05.json`; the extraction method
is the `nsb()` function in `../../replay-20261108/data/replay.py`.
