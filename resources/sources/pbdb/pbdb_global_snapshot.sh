#!/usr/bin/env bash
# Global PBDB snapshot. Occurrences and collections are partitioned by record
# creation time (exhaustive and non-overlapping), with a rowcount request
# beside every partition so the profile can reconcile each one. The 306,489
# occurrences stamped 2025-09-21 22:25 share one minute, so that partition is
# paged by occurrence number (order=id, limit and offset). Opinions are fetched
# whole: any rowcount request on opinions returns HTTP 500, so they are checked
# by row count only. Same show blocks, plate models and vocabulary as
# pbdb_snapshot.sh.
set -euo pipefail
cd /data/paleodata
B="https://paleobiodb.org/data1.2"
PGM="pgm=gplates,scotese,seton"
OCC="show=full,ecospace,taphonomy,abund,pres,timebins,strat,lith,env,paleoloc,crmod,ent,entname&$PGM&vocab=pbdb"
COL="show=full,paleoloc,crmod,ent,entname&$PGM&vocab=pbdb"
BULK_A="2025-09-21T22:25:00"
BULK_B="2025-09-21T22:26:00"
args=("datainfo.json::$B/occs/list.json?all_records&limit=0&rowcount&datainfo")

part() {  # name endpoint filter-prefix after before show
  local name=$1 ep=$2 f=$3 after=$4 before=$5 show=$6 q="all_records"
  [ -n "$after" ] && q="$q&${f}_created_after=$after"
  [ -n "$before" ] && q="$q&${f}_created_before=$before"
  args+=("count__$name.json::$B/$ep.json?$q&limit=0&rowcount")
  args+=("$name.csv::$B/$ep.csv?$q&$show")
}

edges=("" 1999-01-01 2001-01-01 2003-01-01 2005-01-01 2008-01-01 2011-01-01 2014-01-01 2018-01-01 2022-01-01 "$BULK_A")
for i in $(seq 1 $((${#edges[@]} - 1))); do
  part "occurrences__p$(printf %02d "$i")" occs/list occs "${edges[$((i - 1))]}" "${edges[$i]}" "$OCC"
done
q="all_records&occs_created_after=$BULK_A&occs_created_before=$BULK_B"
args+=("count__occurrences__p11.json::$B/occs/list.json?$q&limit=0&rowcount")
for off in 0 80000 160000 240000; do
  args+=("occurrences__p11_$(printf %06d "$off").csv::$B/occs/list.csv?$q&order=id&limit=80000&offset=$off&$OCC")
done
part occurrences__p12 occs/list occs "$BULK_B" "" "$OCC"

part collections__p01 colls/list colls "" 2010-01-01 "$COL"
part collections__p02 colls/list colls 2010-01-01 "$BULK_A" "$COL"
part collections__p03 colls/list colls "$BULK_A" "$BULK_B" "$COL"
part collections__p04 colls/list colls "$BULK_B" "" "$COL"

for t in "specimens specs/list all_records show=full" "measurements specs/measurements all_records show=full" \
         "references refs/list all_records show=counts,both" "taxa taxa/list all_taxa show=full,app,crmod"; do
  set -- $t
  args+=("count__$1.json::$B/$2.json?$3&limit=0&rowcount")
  args+=("$1.csv::$B/$2.csv?$3&$4&vocab=pbdb")
done
args+=("opinions.csv::$B/taxa/opinions.csv?all_taxa&show=basis,ref,ent,entname,crmod&vocab=pbdb")
args+=("intervals.csv::$B/intervals/list.csv?all_records&vocab=pbdb")
args+=("config.json::$B/config.json?show=all")
args+=("datainfo_end.json::$B/occs/list.json?all_records&limit=0&rowcount&datainfo")

python3 _tools/data_mirror.py url pbdb/global \
  --license "CC0 (stated in PBDB API datainfo: data_license Creative Commons CC0)" "${args[@]}"
echo DONE
