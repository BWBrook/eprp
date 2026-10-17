#!/usr/bin/env bash
# Submit ONE further fit into an already staged and built pilot directory (no rebuild, no array).
# Run only while Barry has the TPAC jumpbox window open, and only after the release condition for SCEN is met.
#   KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/submit_fit.sh TAG SCEN
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NECTAR="${NECTAR_ROOT:-$HOME/work/nectar}"
# shellcheck source=/dev/null
. "$NECTAR/scripts/lib/common.sh"
# shellcheck source=/dev/null
. "$NECTAR/scripts/lib/kunanyi.sh"
export KUNANYI_SSH_ALIAS="${KUNANYI_SSH_ALIAS:-kunanyi}"
tpac_transport_setup
TAG="${1:?TAG}"
SCEN="${2:?SCEN}"
QSUB="${QSUB:-/opt/pbs/bin/qsub}"
QSTAT="${QSTAT:-/opt/pbs/bin/qstat}"
REMOTE="${REMOTE_BASE:-/u/bwbrook/codex_kunanyi}/q012-pilot-$TAG"
tpac_set_expect_timeout 120
tpac_expect_ssh "set -e; cd $(tpac_quote "$REMOTE"); \
  grep -qx $(tpac_quote "$SCEN") fits.txt || { echo REFUSED: $SCEN is not a permitted fit; exit 2; }; \
  grep -qx status=ok build/receipt.txt || { echo REFUSED: no successful build; exit 2; }; \
  grep -qx manifest_sha256=\$(sha256sum manifest.sha256 | cut -d' ' -f1) build/receipt.txt || { echo REFUSED: build is for another manifest; exit 2; }; \
  F=\$($QSUB -v SCEN=$SCEN pbs/fit.pbs); echo FIT_JOB_$SCEN=\$F | tee -a submitted.txt; \
  $QSTAT -f \$F | grep -E 'Job_Name|Mail_Users|Mail_Points|depend|Resource_List|queue|Variable_List' | cut -c1-200"
echo "Submitted $SCEN in $REMOTE."
