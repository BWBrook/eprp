#!/usr/bin/env bash
# Fetch one pilot run's receipts, logs, chain output and PBS accounting after Barry's wake-up.
# Run only while Barry has the TPAC jumpbox window open.
#   KUNANYI_SSH_ALIAS=kunanyi data/q012-pilot/fetch.sh TAG SCEN
# Files land in scratch/q012-pilot/fetch-TAG/; screen with: pilot.py diagnose <attempt dir> SCEN
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
REMOTE="/scratch/bwbrook/q012-pilot-$TAG"
DEST="$HERE/../../scratch/q012-pilot/fetch-$TAG"
mkdir -p "$DEST"
tpac_set_expect_timeout 300
tpac_expect_ssh "set -e; cd $(tpac_quote "$REMOTE"); \
  for j in \$(tr ' ' '\n' < submitted.txt | cut -d= -f2); do /opt/pbs/bin/qstat -xf \$j; done > accounting-$SCEN.txt 2>&1 || true; \
  tar czf fetch-$SCEN.tar.gz submitted.txt accounting-$SCEN.txt build/receipt.txt build/*.log build/smoke runs/$SCEN q012_*.o* 2>/dev/null || \
  tar czf fetch-$SCEN.tar.gz submitted.txt accounting-$SCEN.txt build runs/$SCEN; sha256sum fetch-$SCEN.tar.gz"
tpac_set_expect_timeout 1800
tpac_expect_scp "$KUNANYI_SSH_ALIAS:$REMOTE/fetch-$SCEN.tar.gz" "$DEST/"
tar xzf "$DEST/fetch-$SCEN.tar.gz" -C "$DEST"
sha256sum "$DEST/fetch-$SCEN.tar.gz"
echo "Fetched into $DEST"
