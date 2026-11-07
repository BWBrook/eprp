# Walvis source check: what is actually available

8 November 2026. Bounded GPT-6.1 Sol source audit integrated by main Codex.
Relevant public Methods and complete supplementary files were inspected;
no restricted library, TDM source, author contact or new broad catalogue was
used. The parent reproduced the abundance timing census independently from
the source workbook. Original files remain ignored.

## Abundances

[Gibbs et al. 2020](https://doi.org/10.1126/sciadv.abc9123), public article
Methods, Abundance data, and
[Europe PMC supplementary package](https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7608818/supplementaryFiles).
The workbook is `abc9123_Data_file_S1.xlsx`, SHA256
`fefb143d84e84137250347fec393dae061214b4b1eb9004efbae02c83beb5a78`.
Its sheet is named `Figure 1 data` although cell A1 calls it Figure 2 data.

| Block | Observed content | Interpretation |
| --- | --- | --- |
| Walvis 1262 Danian, rows 791–816, header 790 | 26 dated rows; depth and `age_ma_DT14_La11`; 26 cellular-percentage categories and a derived flagellate fraction | Actual quantitative assemblages from separate sediment samples. Cell percentages follow lith-to-cell conversion; exact raw lith counts/denominators are not provided in this block. |
| Walvis Cretaceous, rows 19–31, columns AL:DQ | 13 rows with sample/depth identifiers and coccolith percentages, attributed to Bernaola & Monechi 2007; no age column in this block | A separate source product, not a dated dense continuation of the Danian block. The original 2007 study was not independently retrieved in this finite check. |
| Newfoundland 1403/1407, rows 821–853 | 33 cell-percentage rows, 61.573514–66.009 Ma; maximum adjacent-age gap 1,104.336 kyr | Another sparse composite, not immediate support for the same short-horizon forecast. |

The Methods reports new Danian Walvis/Newfoundland lith counts. Both Walvis
and Pacific 1209 were counted by S. A. Alvarez using the same taxonomy and
protocol; Newfoundland was counted by H. Kim in collaboration with Alvarez.
Distinct geographic samples do not make analyst, taxonomy or trait assignments
independent. Site 1209 chronology is correlated to Walvis with isotope/XRF
ties; age errors are related as well.

The supplied Walvis ages span 63.594025–66.009302 Ma. Median gap is 94.515 kyr;
maximum is 294.210 kyr. Older/younger row counts in adjacent 150-kyr windows
are respectively (1,2), (3,1), (2,1), (2,2), (2,1) at landmarks 64, 64.5,
65, 65.5 and 66 Ma. None reaches the required three each, before further
boundary/gap exclusions. [walvis_audit.py](walvis_audit.py) reproduces these
aggregates in [walvis-summary.json](walvis-summary.json).

Two source inconsistencies are retained: workbook A11 describes the Walvis
AC summary as Newfoundland, and the supplementary Fig. S1 caption extends
Walvis to 63.2 Ma whereas the supplied dated block ends at 63.594 Ma. The
actual numerical table governs this support check. No missing rows are invented.

## Separate isotope lead

Birch et al. 2016, [10.1130/G37581.1](https://doi.org/10.1130/G37581.1),
public supplement [10.1130/2016088](https://doi.org/10.1130/2016088),
[provider metadata](https://api.figshare.com/v2/articles/12533441).
`2016088-Table DR2.xls` contains 55 depth/age rows, 60.97–66.46 Ma, with
paired carbon/oxygen isotopes for 11 benthic/planktonic taxa. It contains
no abundance columns. The supplementary PDF describes the orbital chronology
and taxon-specific isotope adjustments. This is an actual separate measurement
family at Walvis, but no proxy/abundance join or function forecast was run.

Provider MD5 checks passed; source SHA256:

- `2016088-Table DR2.xls`:
  `4f68ad521fa4888d219481924c063b52c6637381945b0dc3b4e7e43fb04c086b`.
- `2016088.pdf`:
  `d845545ca66c8fc849093d0f061fd8def072ba46791a9b2fd98c82abadb77d85`.

The provider labels the Birch supplement CC BY-NC 4.0; Gibbs XML likewise
specifies CC BY-NC 4.0. Those source terms are retained. Publisher/institutional
Birch full-article routes returned 403; that is an access limit, not evidence
of absent data. The complete public supplement and actual spreadsheet were
inspected. No additional exact raw-Danian-count deposit was established by
the bounded source search; absence elsewhere is not claimed.

**Disposition:** geographic abundance observations and a co-located isotope
lead exist. They are too sparse for direct replication of this 150-kyr design
and do not establish independent count denominators or observer validation.
A coarser comparison would need a new scientific design and support check.
