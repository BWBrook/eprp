#!/usr/bin/env bash
# Mirror the LegacyPollen family on PANGAEA: LegacyPollen 1.0 (929773), LegacyAge 1.0 (933132) with the
# 2026 African full-age table (931920), and LegacyPollen 2.0 (965907, published 2025): the superseded
# review zip, harmonisation table, overview and the seven regional count tables (percentages are
# derivable and not mirrored). The LegacyVegetation, REVEALS and climate reconstructions are not
# mirrored.
# Usage: legacypollen_snapshot.sh [v1] [age] [v2] (default: all)
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
D=legacypollen
P=https://doi.pangaea.de/10.1594/PANGAEA
A=https://download.pangaea.de/reference
LIC="CC BY 4.0 (PANGAEA dataset licence)"
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }
TMP=$(mktemp -d)

if want v1; then
  for f in Africa Asia Europe Indopacific Latin_America North_America_East North_America_West; do
    echo "${f}_pollen_datasets.zip::$A/111671/attachments/${f}_pollen_datasets.zip"
  done > "$TMP/v1"
  echo "metadata_LegacyPollen_dataset.csv::$A/113199/attachments/metadata_LegacyPollen_dataset.csv" >> "$TMP/v1"
  echo "2021-03-12_taxa_harmonisation_table.csv::$A/107744/attachments/2021-03-12_taxa_harmonisation_table.csv" >> "$TMP/v1"
  $M url "$D/v1" --specs-file "$TMP/v1" --pause 2 --license "$LIC" || echo "v1 FAILED"
fi
if want age; then
  {
    echo "PANGAEA.933132.tab::$P.933132?format=textfile"
    echo "Bacon_parameters_parameter_description.csv::$A/109084/attachments/Bacon_parameters_parameter_description.csv"
    echo "LegacyAge_1.0_readme.txt::$A/109081/attachments/LegacyAge_1.0_readme.txt"
    n=111158
    for t in Table-S1_chronological_control_points_metadata Table-S2_prior_information_of_dates Table-S3_bacon_parameter_settings \
             Table-S4_original_chronology_metadata_by_pollen_records Table-S5_legacyage_1_0_chronology Table-S6_chronology_comparison \
             Table-S7_references; do
      echo "$t.csv::$A/$n/attachments/$t.csv"; n=$((n + 1))
    done
    echo "PANGAEA.931920_africa_full_age_data.tab::$P.931920?format=textfile"
  } > "$TMP/age"
  $M url "$D/legacyage" --specs-file "$TMP/age" --pause 2 --license "$LIC" || echo "age FAILED"
fi
if want v2; then
  {
    echo "ReviewVersion.zip::$A/127195/attachments/ReviewVersion.zip"
    echo "harmonization_table_new.tab::$A/128391/attachments/harmonization_table_new.tab"
    echo "PANGAEA.971802_overview.tab::$P.971802?format=textfile"
    for pair in 971691:africa 971655:asia 971692:europe 971719:indopacific 971788:south_america \
                971797:north_america_east 971804:north_america_west; do
      echo "PANGAEA.${pair%%:*}_counts_${pair#*:}.tab::$P.${pair%%:*}?format=textfile"
    done
  } > "$TMP/v2"
  $M url "$D/v2" --specs-file "$TMP/v2" --pause 2 --license "$LIC" || echo "v2 FAILED"
fi
rm -rf "$TMP"
echo DONE
