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
tpac_expect_ssh "cd $(tpac_quote "$REMOTE") && bash pbs/pack.sh $(tpac_quote "$SCEN")"
tpac_set_expect_timeout 1800
tpac_expect_scp "$KUNANYI_SSH_ALIAS:$REMOTE/fetch-$SCEN.tar.gz" "$DEST/"
tar xzf "$DEST/fetch-$SCEN.tar.gz" -C "$DEST"
sha256sum "$DEST/fetch-$SCEN.tar.gz"
echo "Fetched into $DEST"
