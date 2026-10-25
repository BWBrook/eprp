#!/usr/bin/env bash
# Mirror the deposits cited by the EPRP question registers, ideation notes,
# literature notes and data READMEs (latest version each).
# Usage: register_deposits_snapshot.sh [dryad] [zenodo] [figshare] [pangaea] [esm] [index] [other] [github] [cran] (default: all)
#   dryad     Dryad deposits, with the Dryad API account on the host (credentials outside the repository)
#   zenodo    Zenodo records up to 5 GB, four at a time (Zenodo serves about 0.3 MB/s per connection)
#   figshare  Figshare articles
#   pangaea   PANGAEA datasets as tab-delimited text (the IODP U1313 series of the Q-050 crosswalk)
#   esm       publisher supplementary files with no repository deposit (Knope et al. 2015's
#             Supplementary Data 1, B-001's guild coding; Cao et al. 2022's Table S1 and
#             supplementary PDF, Q-021's Shangsi lithium series)
#   index     version indexes only, for the Zenodo and Dryad records over 5 GB (fetch on demand)
#   other     Mendeley Data, OSF and ANU Data Commons deposits, as plain-URL snapshots checked
#             against the providers' sha256 or MD5 (other_repos.py); each run takes a new dated
#             snapshot. The Harvard Dataverse record over 5 GB as a file list only
#   github    code repositories cited with their data (Rozzi et al. 2023; Tennant et al. 2018's
#             OSF-linked repository), newest commit
#   cran      paleotree, the CRAN package carrying Aze et al. 2011's Appendix S5 tables: the current
#             version, checked against the MD5 in CRAN's PACKAGES, tables written to derived/
set -uo pipefail
cd /data/paleodata
M="python3 _tools/data_mirror.py"
ROUTES=" $* "
want() { [ "$ROUTES" = "  " ] || [[ "$ROUTES" == *" $1 "* ]]; }

if want dryad; then
while read -r code slug; do
  echo "== dryad $code $slug"
  $M dryad "10.5061/dryad.$code" "register-deposits/$slug" --latest || echo "$code FAILED"
done <<'EOF'
931zcrjqw monarrez2023-selectivity
c17p8 walton2018-ammonoid-ontogeny
3v0p84v close2019-tetrapod-local-richness
8jf2k brombacher2017-foram-allometry
m010p hunt2015-trait-stasis
gd8038s cantalapiedra2019-phylogenetic-diversity
sqv9s4ndb slattery2025-nuculid-stasis
6djh9w1bx benson2025-marine-latitudinal-diversity
nk218ht franeck2018-ordovician-radiation
5dv41nsmd stigall2026-ordovician-species
1vhhmgr44 leventhal2025-bryozoan-brooding
zpc866t6s liow2021-cheilostome-cyclostome
tx95x69vr hunt2020-ostracod-dimorphism
vx0k6dk71 crampton2026-extinction-spectrum
1ns1rn91g malanoski2024-climate-extinction-risk
0k6djhb6h freitas2026-patch-biogeography-simulations
1mg27 holland2016-stratigraphy-mass-extinction
4j0zpc8hx holstad2024-evolvability-macroevolution
63xsj3tzv kontopoulos2020-phytoplankton-thermal
8w9ghx3w6 tang2024-proterozoic-eukaryotes-dryad
9ghx3ffts malanoski2026-paleogeography-extinction-risk
bg30k dunhill2018-late-triassic-functional-diversity
mgqnk992f xiong2022-hybrid-incompatibilities
p5hqbzm03 kerr2025-regional-databases
pg4f4qs50 alroy2026-coverage-rarefaction
s7576 syverson2017-crinoid-spinosity
vd80g8n saupe2019-range-size-niche-breadth
EOF
fi

if want zenodo; then
mkdir -p /data/codex/scratch/eprp-paleodata/register-deposits/logs
cat <<'EOF' | xargs -P 4 -L 1 bash -c 'echo "== zenodo $0 $1"; python3 _tools/data_mirror.py zenodo "$0" "register-deposits/$1" --latest > "/data/codex/scratch/eprp-paleodata/register-deposits/logs/$1.log" 2>&1 && echo "done $1" || echo "$0 $1 FAILED"'
10014585 cooke2023-extinct-birds
10149114 foster2023-siliceous-permian-triassic
10403766 penn2023-mi-traits-obis
13294509 tsuboi2024-paradox-of-predictability
14903138 gavirneni2025-bivalve-metabolic-rate
11400588 beckerman2024-toarcian-secondary-extinction
11522106 alaswad2024-end-permian-homogenization
1211555 kocsis2018-biogeographic-imprint
12187757 rogger2024-lip-climate-sensitivity
12735901 tang2024-proterozoic-eukaryotes
1285673 padfield2016-metabolic-traits
14918283 leventhal2025-bryozoan-brooding-supplement
15079899 wang2025-trace-fossil-trajectories
15096088 natscher2025-ectotherm-body-size
15269137 close2025-marine-latitudinal-diversity-code
18512912 minsky2026-snowball-limit-cycle
18700674 rui2026-cgenie-kpg
21414007 lamyman2026-pforam-phylogeny
18926572 rogger2026-treed-vegetation-model
19824423 cribb2026-ecosystem-engineers
3701302 ward2020-mcm-model
3770348 carrillo2020-south-american-mammals
5519730 stockey2021-cgenie-metabolic-index
21933976 seebens2026-sinas
5899743 penn2022-metabolic-index-extinction
6535496 garciacomas2022-inditek
7242861 swain2022-palaeoherbivory-review
7816408 monarrez2023-selectivity-code
8154672 smith2023-biodeeptime
8341743 monarrez2023-selectivity-zenodo
8398420 cribb2023-ete-ecospace
5394385 liow2021-cheilostome-cyclostome-code
10541354 malanoski2024-climate-extinction-risk-code
14104269 leventhal2025-bryozoan-brooding-code
10610771 pohl2024-late-ordovician-foam
10979237 cooper2024-deepdive
18217914 liu2026-phanerozoic-productivity-oxygen
7545805 ridgwell-cgenie-muffin
7545809 ridgwell-muffingen
EOF
# the releases the transfer-inputs note names, besides the newest
$M zenodo 7545805 register-deposits/ridgwell-cgenie-muffin --only v0.9.35_7545805 || echo "cgenie.muffin v0.9.35 FAILED"
$M zenodo 7545809 register-deposits/ridgwell-muffingen --only v0.9.24_7545809 || echo "muffingen v0.9.24 FAILED"
fi

if want index; then
while read -r prov rec slug; do
  echo "== $prov index-only $rec $slug"
  $M "$prov" "$rec" "register-deposits/$slug" --index-only || echo "$rec FAILED"
done <<'EOF'
zenodo 11001479 rahman2024-ediacaran-animal-forests
zenodo 17035672 rahman2025-ediacaran-hydrodynamics
zenodo 17252973 rogger2025-petm-vegetation
dryad 10.5061/dryad.nzs7h44pv kagawa2020-admixture-radiation
dryad 10.5061/dryad.5hqbzkhcf shum2026-dark-land-refugia
EOF
fi

if want figshare; then
while read -r art slug; do
  echo "== figshare $art $slug"
  $M figshare "article/$art" "register-deposits/$slug" --latest || echo "$art FAILED"
done <<'EOF'
26103031 qvarnstrom2024-supplementary-figures
27201498 balembois2025-marine-biodiversity-drivers
27909116 craffey2024-ediacaran-cooccurrence-figshare
5046964 klompmaker2017-external-database-2
7357193 penn2018-end-permian-climate
28046414 edie2025-kpg-functional-diversity
19686396 rozzi2023-island-mammals-data
19686423 rozzi2023-island-mammals-trees
19779709 rozzi2023-island-mammals-pyrate
EOF
fi

if want pangaea; then
P="https://doi.pangaea.de/10.1594/PANGAEA"
$M url register-deposits/pangaea-u1313 \
  "PANGAEA.736778.tab::$P.736778?format=textfile" "PANGAEA.761442.tab::$P.761442?format=textfile" \
  "PANGAEA.761443.tab::$P.761443?format=textfile" "PANGAEA.892803.tab::$P.892803?format=textfile" \
  "PANGAEA.892804.tab::$P.892804?format=textfile" --pause 2 \
  --license "CC BY 3.0 (PANGAEA dataset metadata, all five)" || echo "pangaea FAILED"
fi

if want esm; then
E="https://media.springernature.com/original/springer-static/esm"
$M url register-deposits/knope2015-guild-coding \
  "41467_2015_BFncomms7455_MOESM1087_ESM.xls::$E/art%3A10.1038%2Fncomms7455/MediaObjects/41467_2015_BFncomms7455_MOESM1087_ESM.xls" \
  --license "CC BY 4.0 (Nature Communications article and its supplementary information)" || echo "knope2015 FAILED"
C="$E/art%3A10.1038%2Fs41561-022-01009-x/MediaObjects"
$M url register-deposits/cao2022-reverse-weathering-esm \
  "41561_2022_1009_MOESM1_ESM.pdf::$C/41561_2022_1009_MOESM1_ESM.pdf" \
  "41561_2022_1009_MOESM2_ESM.xlsx::$C/41561_2022_1009_MOESM2_ESM.xlsx" --pause 1 \
  --license "Springer Nature TDM licence (Crossref; not open access); held privately under Barry's 23 October 2026 mirroring decision" \
  || echo "cao2022 FAILED"
fi

if want other; then
O="python3 _tools/register-deposits_other_repos.py"
TMP=$(mktemp -d)
while read -r prov id slug; do
  echo "== $prov $id $slug"
  meta=$($O specs "$prov" "$id" "$TMP/$slug.specs" "$TMP/$slug.expected") || { echo "$id FAILED"; continue; }
  echo "$meta"
  lic=$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["licence"])' "$meta")
  $M url "register-deposits/$slug" --specs-file "$TMP/$slug.specs" --pause 1 --license "$lic" || { echo "$id FAILED"; continue; }
  v=$(ls -d register-deposits/$slug/raw/*_url | tail -1)
  cp "$TMP/$slug.expected" "register-deposits/$slug/provider-checksums-$(basename "$v").tsv"
  if $O check "$v" "$TMP/$slug.expected" > "$TMP/$slug.check"; then tail -1 "$TMP/$slug.check"
  else grep -v '^ok ' "$TMP/$slug.check"; echo "$id FAILED the provider checksums"; fi
done <<'EOF'
osf 2cdqg senel2023-chicxulub-dust
osf nuhqx tennant2018-dinosaur-research-history
mendeley g2g74cj4x7/2 gougeon2024-chapel-island-ichnology
mendeley g2g74cj4x7/1 gougeon2024-chapel-island-ichnology-v1
mendeley r2h822zzxp/1 sara2026-mussel-disturbance
anu anudc:5981 aze2011-anu-datapacks
EOF
# Harvard Dataverse, 26.6 GB of CT volumes and video: the provider's file list only, dated,
# with the download URLs (each carrying the Dataverse file id) beside it
H=register-deposits/howman2024-armandia-burrows/$(date -u +%Y-%m-%d)
mkdir -p "$H"
$O specs dataverse doi:10.7910/DVN/3DU1VW "$H/specs.txt" "$H/files.tsv"
rm -rf "$TMP"
fi

if want github; then
$M github RobRozzi/Island_mammals register-deposits/rozzi2023-island-mammals-code --latest || echo "rozzi github FAILED"
# the GitHub storage linked from Tennant et al.'s OSF project (not in its osfstorage)
$M github Protohedgehog/SQS register-deposits/tennant2018-sqs-code --latest || echo "tennant github FAILED"
fi

if want cran; then
# the current paleotree version and its MD5 from CRAN's PACKAGES; the tables written to derived/
read -r ver md5 < <(curl -sf -A "eprp-data-mirror/4 (research data archive)" https://cran.r-project.org/src/contrib/PACKAGES |
  awk '/^Package: /{p=($2=="paleotree")} p&&/^Version: /{v=$2} p&&/^MD5sum: /{print v, $2; exit}')
D=register-deposits/aze2011-paleotree-cran
if [ -n "${ver:-}" ] && $M url "$D" "paleotree_$ver.tar.gz::https://cran.r-project.org/src/contrib/paleotree_$ver.tar.gz" \
     --license "CC0 (paleotree's DESCRIPTION); the tables are Aze et al. 2011, Appendix S5, terms not stated"; then
  v=$(ls -d $D/raw/*_url | tail -1)
  printf 'name\tsize\talgorithm\tvalue\npaleotree_%s.tar.gz\t\tmd5\t%s\n' "$ver" "$md5" > "$D/provider-checksums-$(basename "$v").tsv"
  python3 _tools/register-deposits_other_repos.py check "$v" "$D/provider-checksums-$(basename "$v").tsv" | tail -1
  mkdir -p "$D/derived/$(basename "$v")"
  Rscript --vanilla _tools/register-deposits_aze_paleotree_tables.R "$v/paleotree_$ver.tar.gz" "$D/derived/$(basename "$v")"
else echo "paleotree FAILED"; fi
fi
echo DONE
