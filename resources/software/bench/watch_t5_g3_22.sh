#!/usr/bin/env bash
set -euo pipefail
source_dir=/data/paleosoft/bench/t5
task_dir=/data/codex/artifacts/eprp/g3-config22-20261028
audit_dir="$task_dir/audit"
image=eprp-sw/bench-r5g:t5

report() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> "$audit_dir/status.txt"; }
trap 'report "audit failed at line $LINENO"' ERR
report 'waiting for the simulation completion receipt'
while ! grep -q 'finished config 22; exit=' "$task_dir/status.txt"; do
  if ! tmux has-session -t eprp-g3-22 2>/dev/null; then
    if grep -q 'finished config 22; exit=' "$task_dir/status.txt"; then
      break
    fi
    report 'simulation session ended without a completion receipt'
    exit 1
  fi
  sleep 60
done
if ! grep -q 'finished config 22; exit=0$' "$task_dir/status.txt"; then
  report 'simulation did not exit successfully; no audit result claimed'
  exit 1
fi
report 'simulation exited successfully; checking inputs and recounting final state'
sha256sum -c "$task_dir/input-sha256.txt" > "$audit_dir/input-check.txt"
expected_config=$(awk 'NR == 1 {print $1}' "$task_dir/input-sha256.txt")
actual_config=$(sha256sum "$task_dir/work/configs/config_auto_22.R" | awk '{print $1}')
test "$expected_config" = "$actual_config"
test "$(docker image inspect "$image" --format '{{.Id}}')" = "$(cat "$task_dir/image-id.txt")"
(
  cd "$source_dir/work/g3/landscapes/scotese_4d"
  find . -type f -print0 | LC_ALL=C sort -z | xargs -0 sha256sum
) > "$audit_dir/landscape-after-sha256.txt"
cmp "$audit_dir/landscape-during-sha256.txt" "$audit_dir/landscape-after-sha256.txt"
docker run --rm -i --network none --memory=12g \
  -v "$source_dir:/source:ro" -v "$task_dir/work:/work:ro" \
  "$image" Rscript - /source /work 22 < "$audit_dir/t5_g3_single_audit.R" \
  > "$audit_dir/final-audit.tsv"
report 'input checks and independent recount passed'
