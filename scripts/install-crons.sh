#!/usr/bin/env bash
# Installs the two FaizOS crons into the user's crontab. Run this yourself; nothing installs
# automatically. Both jobs are deterministic fetch only; no model runs unattended.
#
#   daily  07:30  venture stage 1 ingest (evidence fetch; classification waits for a session)
#   weekly Mon 08:00  frontier fetch for the current tracks
#
# Remove later with: crontab -e (delete the FaizOS lines)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TSX="$ROOT/faizos-core/node_modules/.bin/tsx"
LOG_DIR="$HOME/faizos-backups/cron-logs"
mkdir -p "$LOG_DIR"

DAILY="30 7 * * * cd \"$ROOT/faizos-core\" && \"$TSX\" src/venture.ts ingest >> \"$LOG_DIR/venture-ingest.log\" 2>&1 # FaizOS venture ingest"
WEEKLY="0 8 * * 1 cd \"$ROOT/faizos-core\" && \"$TSX\" src/frontier.ts fetch >> \"$LOG_DIR/frontier-ingest.log\" 2>&1 # FaizOS frontier ingest"

current="$(crontab -l 2>/dev/null || true)"
filtered="$(printf '%s\n' "$current" | grep -v '# FaizOS' || true)"
printf '%s\n%s\n%s\n' "$filtered" "$DAILY" "$WEEKLY" | sed '/^$/d' | crontab -
echo "installed. current crontab:"
crontab -l | grep 'FaizOS'
