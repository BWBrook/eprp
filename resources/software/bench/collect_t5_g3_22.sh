#!/usr/bin/env bash
set -euo pipefail
remote_dir=${1:?remote task directory required}
local_dir=${2:?local receipt directory required}
case "$remote_dir" in
  *[!a-zA-Z0-9_./-]*|'') printf '%s\n' 'invalid remote path' >&2; exit 1 ;;
esac
mkdir -p "$local_dir"

copy_receipt() {
  local remote_file=$1 local_file=$2
  scp -q -o BatchMode=yes -o ConnectTimeout=10 \
    "deep-server:$remote_dir/$remote_file" "$local_dir/$local_file.tmp" || return 1
  mv "$local_dir/$local_file.tmp" "$local_dir/$local_file" || return 1
}

while :; do
  if remote_status=$(ssh -n -o BatchMode=yes -o ConnectTimeout=10 deep-server \
    "cat '$remote_dir/audit/status.txt'" 2>/dev/null); then
    case "$remote_status" in
      *'input checks and independent recount passed'*)
        if copy_receipt status.txt simulation-status.txt && \
           copy_receipt audit/status.txt audit-status.txt && \
           copy_receipt audit/input-check.txt input-check.txt && \
           copy_receipt audit/landscape-after-sha256.txt landscape-after-sha256.txt && \
           copy_receipt audit/final-audit.tsv final-audit.tsv; then
          printf '%s\n' "$(date -u +%FT%TZ) collected successful independent audit" > "$local_dir/collector-status.txt"
          exit 0
        fi
        ;;
      *'audit failed at line '*|*'simulation session ended without a completion receipt'*|*'simulation did not exit successfully'*)
        if copy_receipt status.txt simulation-status.txt && copy_receipt audit/status.txt audit-status.txt; then
          printf '%s\n' "$(date -u +%FT%TZ) collected failure status; no successful audit claimed" > "$local_dir/collector-status.txt"
          exit 2
        fi
        ;;
    esac
  fi
  sleep 60
done
